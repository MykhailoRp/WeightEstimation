from faust import StreamT
from loguru import logger

from common.kafka.faust import faust_app
from common.kafka.messages.weight_class import WeightClassificationMasked
from common.kafka.topics import WeightClassificationMaskedTopic
from common.sql.scripts.weight_class import generate_aggregations, predict_result
from worker.singletons import session_maker

READ_BATCH = 10


@faust_app.agent(
    WeightClassificationMaskedTopic,
    name="WeightClassification.Predict",
)
async def mask_frames(stream: StreamT[bytes]) -> None:
    """Assigns a prediction on weight classification"""
    async for messages_bytes in stream.take(READ_BATCH, within=3):
        messages = [WeightClassificationMasked.model_validate_json(message_bytes) for message_bytes in messages_bytes]
        with logger.contextualize(messages_sz=len(messages)):
            db_session = session_maker

            logger.info("Extracting aggregations...")
            async with db_session() as session:
                aggregations = await generate_aggregations(
                    session=session,
                    weight_class_ids=[m.id for m in messages],
                )
                logger.info(aggregations)

                for message in messages:
                    await predict_result(
                        session=session,
                        weight_class_id=message.id,
                        vehicle_identifier=message.vehicle_identifier,
                    )

                await session.commit()
            logger.success("Aggregations extracted")
