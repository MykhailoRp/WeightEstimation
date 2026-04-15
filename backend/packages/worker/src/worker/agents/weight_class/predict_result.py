from faust import StreamT
from loguru import logger

from common.kafka.faust import faust_app
from common.kafka.messages.weight_class import WeightClassificationMasked
from common.kafka.topics import WeightClassificationMaskedTopic
from worker.pipelines.weight_class import extract_results
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

            logger.info("Predicting weight classification result...")
            await extract_results.extract_results(db_session, messages)
            logger.success("Results predicted")
