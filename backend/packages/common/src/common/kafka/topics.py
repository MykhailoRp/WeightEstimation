from common.kafka.faust import faust_app

WeightClassificationCreatedTopic = faust_app.topic(
    "weight_classification.created",
    key_type=str,
    value_type=bytes,
)

WheelReadingCreatedTopic = faust_app.topic(
    "wheel_reading.created",
    key_type=str,
    value_type=bytes,
)
