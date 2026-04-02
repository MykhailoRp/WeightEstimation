import asyncio
import io
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import batched
from pathlib import Path
from typing import Self

import cv2
import numpy as np
import numpy.typing as npt
import torch
from PIL import Image
from pydantic import BaseModel
from sqlalchemy import UUID, Float, Integer, String, column, func, update, values
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from transformers import Sam2Model, Sam2Processor

from common.kafka.messages.weight_class import WeightClassificationMasked, WheelReadingCreated
from common.kafka.topics import WeightClassificationMaskedTopic
from common.models.bounding_box import BoundingBox
from common.models.weight_class.weight_class import WeightClassStatus
from common.models.weight_class.wheel_reading import WheelFeatures
from common.s3.client import S3Client
from common.sql.scripts.weight_class import try_set_weight_class_status
from common.sql.tables import WheelReadingTable
from common.sql.types.pydantic_type import PydanticJSONB
from common.types import S3Key

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


@dataclass
class SamExtraction:
    tire_mask: Mask
    rim_mask: Mask


class SamProcessed(BaseModel):
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
        frames: Sequence[Image.Image],
        wheel_batch: Sequence[WheelFeatures],
    ) -> list[SamExtraction]:

        box_batch = [[box.x1y1x2y2 for box in (wheel.rim, wheel.tire)] for wheel in wheel_batch]

        inputs = self.processor(images=frames, input_boxes=box_batch, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)

        masks = self.processor.post_process_masks(outputs.pred_masks.cpu(), inputs["original_sizes"])  # type: ignore[no-untyped-call]

        results_batch = [
            SamExtraction(
                rim_mask=rim[0].numpy(),
                tire_mask=tire[0].numpy(),
            )
            for sub_masks in masks
            for rim, tire in batched(sub_masks, 2)
        ]

        return results_batch

    async def _save_masks(self, s3_client: S3Client, requests: Sequence[WheelReadingCreated], extracted: Sequence[SamExtraction]) -> list[tuple[S3Key, S3Key]]:

        masks = []
        key_pairs = []

        for request, extraction in zip(requests, extracted, strict=True):
            rim_mask = io.BytesIO()
            Image.fromarray((extraction.rim_mask * (255 / extraction.rim_mask.max())).astype(np.uint8)).save(rim_mask, "JPEG")
            rim_mask.seek(0)
            masks.append(rim_mask)

            tire_mask = io.BytesIO()
            Image.fromarray((extraction.tire_mask * (255 / extraction.tire_mask.max())).astype(np.uint8)).save(tire_mask, "JPEG")
            masks.append(tire_mask)
            tire_mask.seek(0)

            key_pairs.append(
                (
                    s3_client.config.get_wheel_mask(weight_class_id=request.weight_class_id, frame_id=request.frame_id, wheel_id=request.id, t="rim"),
                    s3_client.config.get_wheel_mask(weight_class_id=request.weight_class_id, frame_id=request.frame_id, wheel_id=request.id, t="tire"),
                ),
            )

        await s3_client.batch_upload_bytes_to(masks, (key for pair in key_pairs for key in pair))

        return key_pairs

    @staticmethod
    def _post_process_masks(extracted: Sequence[SamExtraction]) -> list[SamProcessed]:
        return [SamProcessed.process(raw) for raw in extracted]

    async def _commit_features(
        self,
        db_session: async_sessionmaker[AsyncSession],
        requests: Sequence[WheelReadingCreated],
        boxes: list[SamProcessed],
        masks_on_s3: Sequence[tuple[S3Key, S3Key]],
    ) -> None:
        update_batch = [
            (
                r.weight_class_id,
                r.frame_id,
                r.id,
                WheelFeatures(rim=b.rim_bbx, tire=b.tire_bbx),
                WheelFeatures(rim=b.rim_bbx, tire=b.tire_bbx).get_compression(),
                *s3_masks,
            )
            for r, b, s3_masks in zip(requests, boxes, masks_on_s3, strict=True)
        ]

        values_table = (
            values(
                column("weight_class_id", UUID),
                column("frame_id", Integer),
                column("id", Integer),
                column("masked_features", PydanticJSONB(WheelFeatures)),
                column("compression", Float),
                column("rim_mask_key", String),
                column("tire_mask_key", String),
            )
            .data(update_batch)
            .alias("v")
        )

        statement = (
            update(WheelReadingTable)
            .where(
                WheelReadingTable.weight_class_id == values_table.c.weight_class_id,
                WheelReadingTable.frame_id == values_table.c.frame_id,
                WheelReadingTable.id == values_table.c.id,
            )
            .values(
                masked_features=values_table.c.masked_features,
                compression=values_table.c.compression,
                data=WheelReadingTable.data
                + func.jsonb_build_object(
                    "rim_mask_key",
                    values_table.c.rim_mask_key,
                    "tire_mask_key",
                    values_table.c.tire_mask_key,
                    "model_name",
                    "sam2",
                ),
            )
        )

        async with db_session() as session:
            await session.execute(statement)
            commited_statuses = await try_set_weight_class_status(session, list({r.weight_class_id for r in requests}), WeightClassStatus.MASKS_EXTRACTED)
            await session.commit()

        for weight_class in commited_statuses:
            await WeightClassificationMaskedTopic.send(
                key=WeightClassificationMasked.key(weight_class.vehicle_identifier),
                value=WeightClassificationMasked(
                    id=weight_class.id,
                    vehicle_identifier=weight_class.vehicle_identifier,
                ).model_dump_json(),
            )

    async def extract_features(
        self,
        requests: Sequence[WheelReadingCreated],
        db_session: async_sessionmaker[AsyncSession],
        s3_client: S3Client,
    ) -> None:
        frames_raw = await s3_client.get_files([request.s3_key for request in requests])
        frames = [Image.open(frame_raw).convert("RGB") for frame_raw in frames_raw]

        masks = await asyncio.to_thread(self._extract_masks, frames, [request.raw_features for request in requests])

        masks_on_s3 = await self._save_masks(s3_client, requests, masks)

        boxes = self._post_process_masks(extracted=masks)

        await self._commit_features(db_session, requests, boxes, masks_on_s3)
