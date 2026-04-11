from typing import TYPE_CHECKING, Any

from loguru import logger
from pydantic import ValidationError
from sqlalchemy import Select, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.models.customer import Customer
from common.models.user import UserWithRole, new_user_with_role
from common.models.user.otp import OTP
from common.models.weight_class.weight_class import WeightClassification
from common.sql.tables import AdminTable, CustomerTable, OTPTable, SessionTable, UserTable, WeightClassificationTable
from common.types import UserId, WeightClassId

if TYPE_CHECKING:
    from sqlalchemy.sql.dml import ReturningDelete


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


def apply_weight_classification_filter[T: tuple[Any, ...]](
    statement: Select[T],
    *,
    id: WeightClassId | None,
    customer_ids: list[UserId] | None,
    limit: int | None,
    offset: int | None,
) -> Select[T]:
    if id is not None:
        statement = statement.where(WeightClassificationTable.id == id)

    if customer_ids is not None:
        statement = statement.where(WeightClassificationTable.customer_id.in_(customer_ids))

    if limit is not None:
        statement = statement.limit(limit)

    if offset is not None:
        statement = statement.offset(offset)

    return statement


async def count_weight_classifications(
    session: AsyncSession,
    *,
    customer_ids: list[UserId] | None = None,
) -> int:
    statement = apply_weight_classification_filter(
        select(
            func.count(),
        ).select_from(WeightClassificationTable),
        id=None,
        customer_ids=customer_ids,
        limit=None,
        offset=None,
    )

    result = await session.scalar(statement)

    return result or 0


async def get_weight_classifications(
    session: AsyncSession,
    *,
    id: WeightClassId | None = None,
    customer_ids: list[UserId] | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> list[WeightClassification]:
    statement = apply_weight_classification_filter(
        select(
            WeightClassificationTable,
        ),
        id=id,
        customer_ids=customer_ids,
        limit=limit,
        offset=offset,
    )

    result = await session.scalars(statement)

    return [r.m() for r in result]


async def get_weight_classification(session: AsyncSession, *, id: WeightClassId | None, customer_id: UserId | None) -> WeightClassification | None:
    weight_classifications = await get_weight_classifications(session, id=id, customer_ids=[customer_id] if customer_id else None, limit=1)

    return weight_classifications[0] if len(weight_classifications) == 1 else None


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
