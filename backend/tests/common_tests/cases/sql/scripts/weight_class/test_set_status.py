import uuid
from collections.abc import AsyncGenerator
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.models.bounding_box import BoundingBox
from common.models.customer import Customer
from common.models.user import User
from common.models.weight_class import Frame, WeightClassification, WeightClassResult, WeightClassStatus, WheelFeatures, WheelReading, WheelReadingData
from common.sql.scripts.weight_class import try_set_weight_class_status
from common.sql.tables import CustomerTable, FrameTable, UserTable, WeightClassificationTable, WheelReadingTable
from common.types import FrameId, S3Key, UserId, WeightClassId, WheelId

user = User(
    id=UserId(uuid.UUID(int=1)),
    email="-",
    email_verified=True,
    password_hash="-",
    created_at=datetime.now(tz=UTC),
)

customer = Customer(
    id=user.id,
    funds=0,
)

completed_class = WeightClassification(
    id=WeightClassId(uuid.UUID("00000000-0000-0000-0000-000000000001")),
    customer_id=customer.id,
    vehicle_identifier="1",
    status=WeightClassStatus.FRAMES_SPLIT,
    assigned=WeightClassResult.EMPTY,
    result=None,
    created_at=datetime.now(tz=UTC),
    updated_at=datetime.now(tz=UTC),
    finished_at=None,
    video_key=S3Key("some_key"),
    processing_cost=None,
)

uncompleted_class = WeightClassification(
    id=WeightClassId(uuid.UUID("00000000-0000-0000-0000-000000000002")),
    customer_id=customer.id,
    vehicle_identifier="2",
    status=WeightClassStatus.FRAMES_SPLIT,
    assigned=WeightClassResult.EMPTY,
    result=None,
    created_at=datetime.now(tz=UTC),
    updated_at=datetime.now(tz=UTC),
    finished_at=None,
    video_key=S3Key("some_key"),
    processing_cost=None,
)

completed_frame = Frame(
    id=FrameId(1),
    weight_class_id=completed_class.id,
    s3_key=S3Key("some_key"),
)

uncompleted_frame = Frame(
    id=FrameId(1),
    weight_class_id=uncompleted_class.id,
    s3_key=S3Key("some_key"),
)

completed_reading = WheelReading(
    weight_class_id=completed_class.id,
    frame_id=completed_frame.id,
    id=WheelId(0),
    raw_features=WheelFeatures(
        rim=BoundingBox(x=0, y=0, h=0, w=0),
        tire=BoundingBox(x=0, y=0, h=0, w=0),
    ),
    masked_features=WheelFeatures(
        rim=BoundingBox(x=0, y=0, h=0, w=0),
        tire=BoundingBox(x=0, y=0, h=0, w=0),
    ),
    compression=0.9,
    data=WheelReadingData(),
)

uncompleted_reading = WheelReading(
    weight_class_id=uncompleted_class.id,
    frame_id=uncompleted_frame.id,
    id=WheelId(0),
    raw_features=WheelFeatures(
        rim=BoundingBox(x=0, y=0, h=0, w=0),
        tire=BoundingBox(x=0, y=0, h=0, w=0),
    ),
    masked_features=None,
    compression=None,
    data=WheelReadingData(),
)


@pytest_asyncio.fixture(scope="module")
async def module_session(session_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    async with session_session.begin_nested() as nested:
        session_session.add_all(
            [
                UserTable.new(user),
                CustomerTable.new(customer),
                WeightClassificationTable.new(completed_class),
                WeightClassificationTable.new(uncompleted_class),
                FrameTable.new(completed_frame),
                FrameTable.new(uncompleted_frame),
                WheelReadingTable.new(completed_reading),
                WheelReadingTable.new(uncompleted_reading),
            ],
        )
        await session_session.flush()
        yield session_session
        await nested.rollback()


@pytest.mark.asyncio
async def test_set_weight_class_status_masks_extracted(function_session: AsyncSession) -> None:
    result = await try_set_weight_class_status(function_session, [completed_class.id, uncompleted_class.id], WeightClassStatus.MASKS_EXTRACTED)

    complted_status = await function_session.scalar(select(WeightClassificationTable.status).where(WeightClassificationTable.id == completed_class.id))
    uncomplted_status = await function_session.scalar(select(WeightClassificationTable.status).where(WeightClassificationTable.id == uncompleted_class.id))

    assert complted_status is WeightClassStatus.MASKS_EXTRACTED
    assert uncomplted_status is WeightClassStatus.FRAMES_SPLIT

    assert [r.id for r in result] == [completed_class.id]
