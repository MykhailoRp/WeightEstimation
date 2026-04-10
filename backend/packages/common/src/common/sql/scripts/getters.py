from typing import TYPE_CHECKING

from loguru import logger
from pydantic import ValidationError
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.models.customer import Customer
from common.models.user import UserWithRole, new_user_with_role
from common.models.user.otp import OTP
from common.sql.tables import AdminTable, CustomerTable, UserTable
from common.sql.tables.user.otp import OTPTable
from common.sql.tables.user.session import SessionTable
from common.types import UserId

if TYPE_CHECKING:
    from sqlalchemy.sql.dml import ReturningDelete, Select


async def get_user_with_role(
    session: AsyncSession,
    *,
    id: UserId | None = None,
    email: str | None = None,
    session_token: str | None = None,
) -> UserWithRole | None:

    statement = (
        select(
            UserTable,
            AdminTable.id.isnot(None),
            CustomerTable.id.isnot(None),
        )
        .join(AdminTable, onclause=UserTable.id == AdminTable.id, isouter=True)
        .join(CustomerTable, onclause=UserTable.id == CustomerTable.id, isouter=True)
    )

    if id is not None:
        statement = statement.where(UserTable.id == id)

    if email is not None:
        statement = statement.where(UserTable.email == email)

    if session_token is not None:
        statement = statement.join(SessionTable).where(SessionTable.token == session_token, SessionTable.expire_at > func.now())

    result = (await session.execute(statement)).t.one_or_none()

    if result is None:
        return None

    user, is_admin, is_customer = result
    return new_user_with_role(user.m(), is_admin=is_admin, is_customer=is_customer)


async def get_customer(session: AsyncSession, *, id: UserId | None = None) -> Customer | None:
    statement = select(
        CustomerTable,
    )

    if id is not None:
        statement = statement.where(CustomerTable.id == id)

    result = (await session.execute(statement)).t.one_or_none()

    if result is None:
        return None

    (customer,) = result
    return customer.m()


async def validate_otp[T: OTP](session: AsyncSession, type: type[T], password: str, user_id: UserId | None = None, *, delete_after: bool) -> T | None:
    with logger.contextualize(type=type, user_id=user_id, delete_after=delete_after):
        logger.info("Validating OTP")

        statement: Select[tuple[OTPTable]] | ReturningDelete[tuple[OTPTable]]
        if delete_after:
            statement = delete(OTPTable).returning(OTPTable)
        else:
            statement = select(OTPTable)

        statement = statement.where(
            OTPTable.password == password,
            OTPTable.expire_at > func.now(),
        )

        if user_id is not None:
            statement = statement.where(OTPTable.user_id == user_id)

        record = (await session.scalars(statement)).one_or_none()

        if record is None:
            logger.warning("Did not find OTP")
            return record

        try:
            return type.model_validate(record.m().model_dump())
        except ValidationError:
            logger.exception("Did not validate OTP")
            return None
