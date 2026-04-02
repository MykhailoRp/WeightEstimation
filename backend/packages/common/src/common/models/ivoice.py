from enum import StrEnum


class Currency(StrEnum):
    UAH = "UAH"


class InvoiceStatus(StrEnum):
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
