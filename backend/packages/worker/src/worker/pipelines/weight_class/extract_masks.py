# from itertools import batched
# from typing import List

# import cv2
# import numpy as np
# import numpy.typing as npt
# import torch
# import tqdm
# from matplotlib import pyplot as plt
# from src.tire_extractor import ExtractedBox, ExtractedTire
# from transformers import Sam2Model, Sam2Processor

# from common.models.weight_class.frame import WheelBBX

# from .model import SAMExtraction

# SUBBATCH_SIZE = 3

# def masks_to_boxes(masks: np.ndarray) -> np.ndarray:
#     if len(masks.shape) == 4:
#         masks = masks.squeeze(1)

#     clean_masks = []

#     for mask in masks:
#         temp = mask.astype(np.uint8)
#         median = cv2.medianBlur(temp, 5)
#         clean_mask = np.zeros(median.shape)
#         contours, hierarchy = cv2.findContours(median, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#         try:
#             largest_contour = max(contours, key=cv2.contourArea)
#             cv2.drawContours(clean_mask, [largest_contour], 0, 1, -1)
#         except ValueError:
#             pass

#         clean_masks.append(clean_mask)

#     N = len(clean_masks)
#     boxes = np.zeros((N, 4), dtype=np.float32)

#     for i in range(N):
#         rows = np.any(clean_masks[i], axis=1)
#         cols = np.any(clean_masks[i], axis=0)

#         if not rows.any() or not cols.any():
#             continue

#         y1, y2 = np.where(rows)[0][[0, -1]]
#         x1, x2 = np.where(cols)[0][[0, -1]]

#         boxes[i] = [x1, y1, x2 - x1, y2 - y1]

#     return boxes

# SAM2ImagePredictor(
#     sam_model=build_sam2(
#         self.model_cfg,
#         self.sam2_checkpoint,
#         device=self.device,
#     ),
#     mask_threshold=0.95,
#     max_hole_area=300,
#     max_sprinkle_area=300,
# )

# class SamFeatureExtractor:

#     def __init__(self):
#         self.device = "cuda" if torch.cuda.is_available() else "cpu"
#         self.model = Sam2Model.from_pretrained("facebook/sam2.1-hiera-small").to(self.device)
#         self.processor = Sam2Processor.from_pretrained("facebook/sam2.1-hiera-small")

#     def extract_batch(self, all_frames: npt.NDArray[np.uint8], all_wheel_batch: list[list[WheelBBX]]) -> list[list[SAMExtraction]]:

#         sub_batches_results = []

#         for packed in batched(zip(all_frames, all_wheel_batch), SUBBATCH_SIZE):

#             frames, wheel_batch = map(list, zip(*packed))

#             box_batch = [
#                 np.array([
#                     box.x1y1x2y2 for wheel in frame_wheel for box in (wheel.rim, wheel.tire)
#                 ])
#                 for frame_wheel in wheel_batch
#             ]

#             inputs = self.processor(images=frames, input_boxes=box_batch)

#             with torch.no_grad():
#                 outputs = self.model(**inputs)

#             masks = self.processor.post_process_masks(outputs.pred_masks.cpu(), inputs["original_sizes"])

#             mask_bbx_batch = [masks_to_boxes(masks) for masks in masks]

#             results_batch = [
#                 [
#                     SAMExtraction(
#                         index=org.index,
#                         new=org.new,
#                         tire=ExtractedBox(
#                             x=tire[0],
#                             y=tire[1],
#                             w=tire[2],
#                             h=tire[3],
#                         ),
#                         rim=ExtractedBox(
#                             x=rim[0],
#                             y=rim[1],
#                             w=rim[2],
#                             h=rim[3],
#                         ),
#                     )
#                     for (rim, tire), org in zip(batched(mask_bbx, 2), wheel_frame)
#                 ]
#                 for mask_bbx, wheel_frame in zip(mask_bbx_batch, wheel_batch)
#             ]

#             sub_batches_results.extend(results_batch)

#         return sub_batches_results
