# import asyncio
# import os

# from faust import StreamT
# from loguru import logger

# from common.kafka.faust import faust_app
# from common.kafka.messages.weight_class import WeightClassificationFrameCreated
# from common.kafka.topics import WeightClassificationFrameCreatedTopic
# from worker.pipelines.weight_class import extract_frames
# from worker.singletons import client_maker, session_maker

# MAX_FRAMES_BATCH = 5

# @faust_app.agent(
#     WeightClassificationFrameCreatedTopic,
#     name="WeightClassification.MaskFrames",
# )
# async def split_frames(stream: StreamT[WeightClassificationFrameCreated]) -> None:
#     """Dowloads frame """
#     async for messages in stream.take(MAX_FRAMES_BATCH, within=3):
#         with logger.contextualize(weight_class_id=message.id, video_url=message.video_url):
#             s3_client = client_maker()
#             db_session = session_maker

#             async with s3_client.file(message.video_url) as video_file:
#                 logger.info("Extracting frames...", file=video_file, file_sz=os.path.getsize(video_file.name))
#                 await asyncio.to_thread(
#                     asyncio.run,
#                     extract_frames.extract_frames(
#                         video_file.name,
#                         weight_class_id=message.id,
#                         db_session=db_session,
#                         s3_client=s3_client,
#                     ),
#                 )

#             logger.success("Frames extracted")
