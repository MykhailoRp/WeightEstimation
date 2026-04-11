from typing import NewType
from uuid import UUID

UserId = NewType("UserId", UUID)
InvoiceId = NewType("InvoiceId", UUID)
WeightClassId = NewType("WeightClassId", UUID)
FileId = NewType("FileId", UUID)
FrameId = NewType("FrameId", int)
WheelId = NewType("WheelId", int)
S3Key = NewType("S3Key", str)
S3Url = NewType("S3Url", str)
ApiTokenStr = NewType("ApiTokenStr", str)
