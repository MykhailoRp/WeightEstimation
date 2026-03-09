from common.kafka.faust import faust_app

WeightClassificationCreatedTopic = faust_app.topic(
    "weight_classification.created",
    key_type=str,
    value_type=bytes,
)

WeightClassificationFrameCreatedTopic = faust_app.topic(
    "weight_classification_frame.created",
    key_type=str,
    value_type=bytes,
)
