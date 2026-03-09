from collections.abc import Sequence
from dataclasses import dataclass
from itertools import batched
from pathlib import Path
from typing import Protocol, Self

import cv2
import numpy as np
import numpy.typing as npt
import torch
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from transformers import Sam2Model, Sam2Processor

from common.models.bounding_box import BoundingBox
from common.models.weight_class.frame import WheelBBX
from common.models.weight_class.wheel_feature import WheelFeature
from common.s3.client import S3Client
from common.sql.tables.wheel_feature import WheelFeatureTable
from common.types import FrameId, S3Key, WeightClassId

SUBBATCH_SIZE = 3

Mask = npt.NDArray[np.bool]


def mask_to_box(mask: Mask) -> BoundingBox:
    if len(mask.shape) == 3:
        mask = mask.squeeze(0)

    temp = mask.astype(np.uint8)
    median = cv2.medianBlur(temp, 5)
    clean_mask = np.zeros(median.shape)
    contours, _hierarchy = cv2.findContours(median, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    try:
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(clean_mask, [largest_contour], 0, 1, -1)
    except ValueError:
        pass

    rows = np.any(clean_mask, axis=1)
    cols = np.any(clean_mask, axis=0)

    if not rows.any() or not cols.any():
        return BoundingBox(x=0, y=0, h=0, w=0)

    y1, y2 = np.where(rows)[0][[0, -1]]
    x1, x2 = np.where(cols)[0][[0, -1]]

    return BoundingBox(x=x1, y=y1, h=y2 - y1, w=x2 - x1)


class SamRequest(Protocol):
    id: FrameId
    weight_class_id: WeightClassId
    wheel_bbxs: list[WheelBBX]
    s3_key: S3Key


@dataclass
class SamExtraction:
    tire_mask: Mask
    rim_mask: Mask


@dataclass
class SamProcessed:
    tire_bbx: BoundingBox
    rim_bbx: BoundingBox

    @classmethod
    def process(cls, raw: SamExtraction, /) -> Self:
        return cls(
            tire_bbx=mask_to_box(raw.tire_mask),
            rim_bbx=mask_to_box(raw.rim_mask),
        )


SAM_CHECKPOINT = Path(__file__).parents[6] / "checkpoints" / "sam2"


class SamFeatureExtractor:
    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model: Sam2Model = Sam2Model.from_pretrained(SAM_CHECKPOINT).to(self.device)  # type: ignore[arg-type]
        self.processor: Sam2Processor = Sam2Processor.from_pretrained(SAM_CHECKPOINT)

    def _extract_masks(
        self,
        frames: list[Image.Image],
        wheel_batch: list[list[WheelBBX]],
    ) -> list[list[SamExtraction]]:

        box_batch = [[box.x1y1x2y2 for wheel in frame_wheels for box in (wheel.rim, wheel.tire)] for frame_wheels in wheel_batch]

        inputs = self.processor(images=frames, input_boxes=box_batch, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)

        masks = self.processor.post_process_masks(outputs.pred_masks.cpu(), inputs["original_sizes"])  # type: ignore[no-untyped-call]

        results_batch = [
            [
                SamExtraction(
                    rim_mask=rim[0].numpy(),
                    tire_mask=tire[0].numpy(),
                )
                for rim, tire in batched(frame_masks, 2)
            ]
            for frame_masks in masks
        ]

        return results_batch

    # def _save_masks(self, extracted: list[list[SamExtraction]]) -> list[list[SamProcessed]]:
    #     return [
    #         [
    #             SamProcessed.process(raw)
    #             for raw in frame_raw
    #         ]
    #         for frame_raw in extracted
    #     ]

    @staticmethod
    def _post_process_masks(extracted: list[list[SamExtraction]]) -> list[list[SamProcessed]]:
        return [[SamProcessed.process(raw) for raw in frame_raw] for frame_raw in extracted]

    async def extract_features(
        self,
        requests: Sequence[SamRequest],
        db_session: async_sessionmaker[AsyncSession],
        s3_client: S3Client,
    ) -> None:
        frames_raw = await s3_client.get_files([request.s3_key for request in requests])
        frames = [Image.open(frame_raw).convert("RGB") for frame_raw in frames_raw]

        masks = self._extract_masks(frames=frames, wheel_batch=[request.wheel_bbxs for request in requests])

        boxes = self._post_process_masks(extracted=masks)

        features = [
            WheelFeature(
                id=wheel_data.id,
                frame_id=request.id,
                weight_class_id=request.weight_class_id,
                rim=box_pair.rim_bbx,
                tire=box_pair.tire_bbx,
                data=None,
            )
            for frame_boxes, request in zip(boxes, requests, strict=True)
            for box_pair, wheel_data in zip(frame_boxes, request.wheel_bbxs, strict=True)
        ]

        async with db_session() as session:
            session.add_all([WheelFeatureTable.new(feature) for feature in features])
            await session.commit()
