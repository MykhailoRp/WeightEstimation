from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from common.models.customer.invoice import Invoice
from common.sql.tables import InvoiceTable
from common.types import InvoiceId, UserId


def apply_invoice_filter[T: tuple[Any, ...]](
    statement: Select[T],
    *,
    id: InvoiceId | None,
    customer_ids: list[UserId] | None,
    limit: int | None,
    offset: int | None,
) -> Select[T]:
    if id is not None:
        statement = statement.where(InvoiceTable.id == id)

    if customer_ids is not None:
        statement = statement.where(InvoiceTable.customer_id.in_(customer_ids))

    if limit is not None:
        statement = statement.limit(limit)

    if offset is not None:
        statement = statement.offset(offset)

    return statement


async def count_invoices(
    session: AsyncSession,
    *,
    customer_ids: list[UserId] | None = None,
) -> int:
    statement = apply_invoice_filter(
        select(
            func.count(),
        ).select_from(InvoiceTable),
        id=None,
        customer_ids=customer_ids,
        limit=None,
        offset=None,
    )

    result = await session.scalar(statement)

    return result or 0


async def get_invoices(
    session: AsyncSession,
    *,
    id: InvoiceId | None = None,
    customer_ids: list[UserId] | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> list[Invoice]:
    statement = apply_invoice_filter(
        select(
            InvoiceTable,
        ),
        id=id,
        customer_ids=customer_ids,
        limit=limit,
        offset=offset,
    )

    result = await session.scalars(statement)

    return [r.m() for r in result]


async def get_invoice(session: AsyncSession, *, id: InvoiceId | None, customer_id: UserId | None) -> Invoice | None:
    results = await get_invoices(session, id=id, customer_ids=[customer_id] if customer_id else None, limit=1)

    return results[0] if len(results) == 1 else None
