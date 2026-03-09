from typing import NewType
from uuid import UUID

UserId = NewType("UserId", UUID)
WeightClassId = NewType("WeightClassId", UUID)
FileId = NewType("FileId", UUID)
FrameId = NewType("FrameId", int)
WheelId = NewType("WheelId", int)
S3Key = NewType("S3Key", str)
