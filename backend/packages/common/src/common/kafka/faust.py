from faust import App

from common.kafka.config import KafkaConfig

kafka_config = KafkaConfig()

faust_app = App(
    "worker",
    broker=kafka_config.brokers,
)
