import uuid
from collections.abc import AsyncGenerator
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from common.models.weight_class import WeightClassification, WeightClassResult, WeightClassStatus, WheelAggregation
from common.sql.scripts.weight_class import predict_result
from common.sql.tables import WeightClassificationTable
from common.sql.tables.wheel_aggregation import WheelAggregationTable
from common.types import S3Key, WeightClassId, WheelId

unpredicted_class_loaded = WeightClassification(
    id=WeightClassId(uuid.UUID("00000000-0000-0000-0000-000000000001")),
    vehicle_identifier="1",
    status=WeightClassStatus.MASKS_EXTRACTED,
    assigned=WeightClassResult.EMPTY,
    result=None,
    created_at=datetime.now(tz=UTC),
    updated_at=datetime.now(tz=UTC),
    finished_at=None,
    video_key=S3Key("some_key"),
    processing_cost=None,
)

unprocessed_aggregation = WheelAggregation(
    weight_class_id=unpredicted_class_loaded.id,
    id=WheelId(1),
    median=0.5,
    std=0.0001,
)

predicted_class_loaded_1 = WeightClassification(
    id=WeightClassId(uuid.UUID("00000000-0000-0000-0000-000000000002")),
    vehicle_identifier="1",
    status=WeightClassStatus.COMPLETED,
    assigned=WeightClassResult.LOADED,
    result=WeightClassResult.LOADED,
    created_at=datetime.now(tz=UTC),
    updated_at=datetime.now(tz=UTC),
    finished_at=datetime.now(tz=UTC),
    video_key=S3Key("some_key"),
    processing_cost=None,
)

processed_aggregation_loaded_1 = WheelAggregation(
    weight_class_id=predicted_class_loaded_1.id,
    id=WheelId(1),
    median=0.55,
    std=0.0001,
)

predicted_class_loaded_2 = WeightClassification(
    id=WeightClassId(uuid.UUID("00000000-0000-0000-0000-000000000003")),
    vehicle_identifier="1",
    status=WeightClassStatus.COMPLETED,
    assigned=WeightClassResult.EMPTY,
    result=WeightClassResult.LOADED,
    created_at=datetime.now(tz=UTC),
    updated_at=datetime.now(tz=UTC),
    finished_at=datetime.now(tz=UTC),
    video_key=S3Key("some_key"),
    processing_cost=None,
)

processed_aggregation_loaded_2 = WheelAggregation(
    weight_class_id=predicted_class_loaded_2.id,
    id=WheelId(1),
    median=0.45,
    std=0.0001,
)

predicted_class_empty_1 = WeightClassification(
    id=WeightClassId(uuid.UUID("00000000-0000-0000-0000-000000000004")),
    vehicle_identifier="1",
    status=WeightClassStatus.COMPLETED,
    assigned=WeightClassResult.EMPTY,
    result=WeightClassResult.EMPTY,
    created_at=datetime.now(tz=UTC),
    updated_at=datetime.now(tz=UTC),
    finished_at=datetime.now(tz=UTC),
    video_key=S3Key("some_key"),
    processing_cost=None,
)

processed_aggregation_empty_1 = WheelAggregation(
    weight_class_id=predicted_class_empty_1.id,
    id=WheelId(1),
    median=0.85,
    std=0.0001,
)

predicted_class_empty_2 = WeightClassification(
    id=WeightClassId(uuid.UUID("00000000-0000-0000-0000-000000000005")),
    vehicle_identifier="1",
    status=WeightClassStatus.COMPLETED,
    assigned=WeightClassResult.EMPTY,
    result=WeightClassResult.EMPTY,
    created_at=datetime.now(tz=UTC),
    updated_at=datetime.now(tz=UTC),
    finished_at=datetime.now(tz=UTC),
    video_key=S3Key("some_key"),
    processing_cost=None,
)

processed_aggregation_empty_2 = WheelAggregation(
    weight_class_id=predicted_class_empty_2.id,
    id=WheelId(1),
    median=0.95,
    std=0.0001,
)


@pytest_asyncio.fixture(scope="module")
async def module_session(session_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    async with session_session.begin_nested() as nested:
        session_session.add_all(
            [
                WeightClassificationTable.new(unpredicted_class_loaded),
                WeightClassificationTable.new(predicted_class_loaded_1),
                WeightClassificationTable.new(predicted_class_loaded_2),
                WeightClassificationTable.new(predicted_class_empty_1),
                WeightClassificationTable.new(predicted_class_empty_2),
                WheelAggregationTable.new(unprocessed_aggregation),
                WheelAggregationTable.new(processed_aggregation_loaded_1),
                WheelAggregationTable.new(processed_aggregation_loaded_2),
                WheelAggregationTable.new(processed_aggregation_empty_1),
                WheelAggregationTable.new(processed_aggregation_empty_2),
            ],
        )
        await session_session.flush()
        yield session_session
        await nested.rollback()


@pytest_asyncio.fixture(scope="function")
async def function_session_scenario_complete(session_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    async with session_session.begin_nested() as nested:
        session_session.add_all(
            [
                WeightClassificationTable.new(unpredicted_class_loaded),
                WeightClassificationTable.new(predicted_class_loaded_1),
                WeightClassificationTable.new(predicted_class_loaded_2),
                WeightClassificationTable.new(predicted_class_empty_1),
                WeightClassificationTable.new(predicted_class_empty_2),
                WheelAggregationTable.new(unprocessed_aggregation),
                WheelAggregationTable.new(processed_aggregation_loaded_1),
                WheelAggregationTable.new(processed_aggregation_loaded_2),
                WheelAggregationTable.new(processed_aggregation_empty_1),
                WheelAggregationTable.new(processed_aggregation_empty_2),
            ],
        )
        await session_session.flush()
        yield session_session
        await nested.rollback()


@pytest.mark.asyncio
async def test_predict_normal_scenario(function_session_scenario_complete: AsyncSession) -> None:
    result = await predict_result(function_session_scenario_complete, unpredicted_class_loaded.vehicle_identifier, unpredicted_class_loaded.id)

    assert result == WeightClassResult.LOADED


@pytest_asyncio.fixture(scope="function")
async def function_session_scenario_single_reading_per_result(session_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    async with session_session.begin_nested() as nested:
        session_session.add_all(
            [
                WeightClassificationTable.new(unpredicted_class_loaded),
                WeightClassificationTable.new(predicted_class_loaded_1),
                WeightClassificationTable.new(predicted_class_empty_1),
                WheelAggregationTable.new(unprocessed_aggregation),
                WheelAggregationTable.new(processed_aggregation_loaded_1),
                WheelAggregationTable.new(processed_aggregation_empty_1),
            ],
        )
        await session_session.flush()
        yield session_session
        await nested.rollback()


@pytest.mark.asyncio
async def test_predict_single_aggregation_per_result_scenario(function_session_scenario_single_reading_per_result: AsyncSession) -> None:
    result = await predict_result(function_session_scenario_single_reading_per_result, unpredicted_class_loaded.vehicle_identifier, unpredicted_class_loaded.id)

    assert result == WeightClassResult.LOADED


@pytest_asyncio.fixture(scope="function")
async def function_session_scenario_single_aggregation(session_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    async with session_session.begin_nested() as nested:
        session_session.add_all(
            [
                WeightClassificationTable.new(unpredicted_class_loaded),
                WeightClassificationTable.new(predicted_class_loaded_1),
                WheelAggregationTable.new(unprocessed_aggregation),
                WheelAggregationTable.new(processed_aggregation_loaded_1),
            ],
        )
        await session_session.flush()
        yield session_session
        await nested.rollback()


@pytest.mark.asyncio
async def test_predict_single_aggregation_scenario(function_session_scenario_single_aggregation: AsyncSession) -> None:
    result = await predict_result(function_session_scenario_single_aggregation, unpredicted_class_loaded.vehicle_identifier, unpredicted_class_loaded.id)

    assert result == WeightClassResult.LOADED


@pytest_asyncio.fixture(scope="function")
async def function_session_scenario_no_previous_aggregations(session_session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    async with session_session.begin_nested() as nested:
        session_session.add_all(
            [
                WeightClassificationTable.new(unpredicted_class_loaded),
                WheelAggregationTable.new(unprocessed_aggregation),
            ],
        )
        await session_session.flush()
        yield session_session
        await nested.rollback()


@pytest.mark.asyncio
async def test_predict_no_previous_aggregations_scenario(function_session_scenario_no_previous_aggregations: AsyncSession) -> None:
    result = await predict_result(function_session_scenario_no_previous_aggregations, unpredicted_class_loaded.vehicle_identifier, unpredicted_class_loaded.id)

    assert result is None
