from common.kafka.faust import faust_app
from common.kafka.messages.weight_class import WeightClassificationCreated

WeightClassificationCreatedTopic = faust_app.topic(
    "weight_classification.created",
    key_type=str,
    value_type=WeightClassificationCreated,
)
