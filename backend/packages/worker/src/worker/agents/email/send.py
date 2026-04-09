import asyncio

from faust import StreamT
from loguru import logger

from common.kafka.faust import faust_app
from common.kafka.messages.email import EmailSend
from common.kafka.topics import EmailSendTopic
from worker.email_sender.send import send_system_email
from worker.singletons import EMAIL_CONFIG

MAX_EMAILS_BATCH = 8


@faust_app.agent(
    EmailSendTopic,
    name="Email.Send",
)
async def send_emails(stream: StreamT[bytes]) -> None:
    """Sends emails"""
    async for messages_bytes in stream.take(MAX_EMAILS_BATCH, within=3):
        messages = [EmailSend.model_validate_json(message_bytes) for message_bytes in messages_bytes]
        with logger.contextualize(messages_sz=len(messages)):
            await asyncio.gather(
                *[
                    send_system_email(
                        EMAIL_CONFIG,
                        message,
                    )
                    for message in messages
                ],
            )
