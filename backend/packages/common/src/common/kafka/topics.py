from common.kafka.faust import faust_app
from common.kafka.messages.weight_class import WeightClassificationCreated, WeightClassificationFrameCreated

WeightClassificationCreatedTopic = faust_app.topic(
    "weight_classification.created",
    key_type=str,
    value_type=WeightClassificationCreated,
)

WeightClassificationFrameCreatedTopic = faust_app.topic(
    "weight_classification_frame.created",
    key_type=str,
    value_type=WeightClassificationFrameCreated,
)
