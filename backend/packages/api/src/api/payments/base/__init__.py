from abc import ABC, abstractmethod
from typing import Protocol

from common.models.customer.invoice import Invoice, NewInvoice


class UserContact(Protocol):
    email: str


class InvoiceWrapper(ABC):
    @abstractmethod
    async def request_invoice(self, user: UserContact, invoice: NewInvoice) -> Invoice:
        pass
