import smtplib
from email.message import EmailMessage as EmailBuilder
from email.utils import formataddr

from loguru import logger

from common.models.email import EmailMessage
from common.utils import to_async
from worker.email_sender.conf import EmailConfig


@to_async
def send_system_email(conf: EmailConfig, message: EmailMessage) -> None:
    with logger.contextualize(recipient=message.to.model_dump(mode="json"), email_type=message.type):
        msg = EmailBuilder()
        msg.add_header("From", formataddr((conf.system_sender, conf.system_address)))
        msg.add_header("To", formataddr((message.to.name, message.to.email)))

        msg.add_header("Subject", message.subject)

        msg.set_content(message.content, "html")
        logger.debug("Connecting to smtp")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(conf.system_address, conf.password)
            server.send_message(msg)
            logger.info("Email sent")
