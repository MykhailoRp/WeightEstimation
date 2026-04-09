from common.kafka.messages import BaseMessage
from common.models.email import EmailMessage


class EmailSend(BaseMessage, EmailMessage):
    @staticmethod
    def key() -> None:
        return None
