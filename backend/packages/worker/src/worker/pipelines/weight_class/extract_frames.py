import os
from collections.abc import Sequence
from tempfile import TemporaryDirectory

import cv2
import numpy as np
import numpy.typing as npt
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from common.models.bounding_box import BoundingBox
from common.models.weight_class.frame import Frame, FrameStatus, WheelBBX
from common.s3.client import S3Client
from common.sql.tables.frame import FrameTable
from common.types import FrameId, WeightClassId
from worker.custom import Sort

np.seterr(all="raise")

T_Circles = npt.NDArray[np.float32]
T_RawBBX = npt.NDArray[np.float32]
T_ScoredBBX = npt.NDArray[np.float32]


def find_contained_circle_pairs(
    circles: T_Circles,
    min_radius_ratio: float = 0.3,
    max_radius_ratio: float = 0.65,
    ideal_radius_ratio: float = 0.53,
    eps: float = 0.0,
) -> tuple[npt.NDArray[np.int8], npt.NDArray[np.int8], npt.NDArray[np.int8]]:
    if len(circles) == 0:
        return np.empty((0, 2), np.int8), np.empty((0, 2), np.int8), np.empty((0, 2), np.int8)

    circles = np.asarray(circles, dtype=float)

    centers = circles[:, :2]
    radii = circles[:, 2]

    # Pairwise center distances
    dist = np.linalg.norm(
        centers[:, None, :] - centers[None, :, :],
        axis=-1,
    )

    # i = outer, j = inner
    containment = dist + radii[None, :] <= radii[:, None] + eps
    np.fill_diagonal(containment, False)

    is_root = ~containment.any(axis=0)

    child_free = ~containment.any(axis=1)

    # radius ratio constraint (inner / outer)
    ratio = radii[None, :] / radii[:, None]

    ratio_ok = (ratio >= min_radius_ratio) & (ratio <= max_radius_ratio)

    score = np.abs(ratio - ideal_radius_ratio) + (~(containment & is_root[:, None]) * 1)
    is_best_w = score == score.min(axis=1)[:, None]
    is_best_h = score == score.min(axis=0)[None, :]
    is_best = is_best_w & is_best_h

    mask = containment & ratio_ok & is_best & is_root[:, None]

    # remove self-pairs
    np.fill_diagonal(mask, False)

    pairs = np.argwhere(mask)

    if pairs.size == 0:
        return pairs.astype(np.int8), np.flatnonzero(is_root & ~child_free).astype(np.int8), np.flatnonzero(is_root & child_free).astype(np.int8)

    used_roots = np.zeros(len(circles), dtype=bool)
    used_roots[pairs[:, 0]] = True

    unidentified = is_root & ~used_roots & ~child_free  # outer circles with at least one inner that were not matched

    discarded = is_root & ~used_roots & child_free  # outer circles without children

    return pairs.astype(np.int8), np.flatnonzero(unidentified).astype(np.int8), np.flatnonzero(discarded).astype(np.int8)


def normalize_lighting(image: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    equ = cv2.equalizeHist(hsv[:, :, 2])  # Equalize the Value channel
    new_hsv = cv2.merge((hsv[:, :, 0], hsv[:, :, 1], equ))
    return cv2.cvtColor(new_hsv, cv2.COLOR_HSV2BGR).astype(np.uint8)


def detect_circles(
    image: npt.NDArray[np.uint8],
    blur_k: int = 7,
    sigma: float = 2.0,
    scale: int = 96,  # 1920 / 96 = 20, we need 20 in dp
    min_dist: int = 70,
    param1: int = 100,
    param2: float = 0.7,
    min_r: int = 70,
    max_r: int = -1,
) -> T_Circles:
    gray = cv2.cvtColor(normalize_lighting(image), cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (blur_k, blur_k), sigma)

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT_ALT,
        dp=image.shape[0] / scale,
        minDist=min_dist,
        param1=param1,
        param2=param2,
        minRadius=min_r,
        maxRadius=max_r,
    )

    return np.array(circles[0]).astype(np.float32) if circles is not None and len(circles) > 0 else np.empty((0, 3), np.float32)


def circle_to_box(circles: T_Circles, rad_mult: float = 1.0) -> T_RawBBX:

    if len(circles) == 0:
        return np.empty((0, 4), np.float32)

    bbxs = np.zeros((len(circles), 4), np.float32)
    bbxs[:, 0] = circles[:, 0] - circles[:, 2] * rad_mult
    bbxs[:, 1] = circles[:, 1] - circles[:, 2] * rad_mult
    bbxs[:, 2] = circles[:, 0] + circles[:, 2] * rad_mult
    bbxs[:, 3] = circles[:, 1] + circles[:, 2] * rad_mult
    return bbxs


def limit_boxes[T_BBX: T_ScoredBBX | T_RawBBX](bbxs: T_BBX, image: npt.NDArray[np.uint8]) -> T_BBX:
    height, width, _ = image.shape
    bbxs[:, [0, 2]] = np.clip(bbxs[:, [0, 2]], 0, width)
    bbxs[:, [1, 3]] = np.clip(bbxs[:, [1, 3]], 0, height)
    return bbxs


def calc_score(
    ratios: npt.NDArray[np.float32],
    base_score: float = 0.35,
    min_ratio: float = 0.3,
    max_ratio: float = 0.65,
    ideal_ratio: float = 0.53,
) -> npt.NDArray[np.float32]:
    score = np.zeros_like(ratios, np.float32)
    score[ratios <= ideal_ratio] = (ratios[ratios <= ideal_ratio] - min_ratio) / (ideal_ratio - min_ratio)
    score[ratios > ideal_ratio] = 1 - (ratios[ratios > ideal_ratio] - ideal_ratio) / (max_ratio - ideal_ratio)
    return base_score + (1 - base_score) * score


def concat_score(bbxs: T_RawBBX, scores: npt.NDArray[np.float32]) -> T_ScoredBBX:
    if bbxs.size == 0:
        return np.empty((0, 5), np.float32)
    return np.concatenate([bbxs, scores[:, None]], axis=1, dtype=np.float32)


def add_score(bbxs: T_RawBBX, score: float) -> T_ScoredBBX:
    if bbxs.size == 0:
        return np.empty((0, 5), np.float32)

    scores = np.full((bbxs.shape[0], 1), score, dtype=float)
    return np.concatenate([bbxs, scores], axis=1, dtype=np.float32)


def get_roi(image: npt.NDArray[np.uint8], x: float = 0.6, y: float = 0.85) -> tuple[npt.NDArray[np.uint8], int, int]:
    height, width, _ = image.shape
    result_h, result_w = int(height * y), int(width * x)

    x1 = (width - result_w) // 2
    x2 = result_w + x1

    y1 = (height - result_h) // 2
    y2 = result_h + y1

    return image[y1:y2, x1:x2], x1, y1


def detect_tires(image: npt.NDArray[np.uint8]) -> T_ScoredBBX:

    roi, pad_lef, pad_top = get_roi(image)

    circles = detect_circles(roi)

    if len(circles) == 0:
        return np.empty((0, 5), np.float32)

    circles[:, 0] += pad_lef
    circles[:, 1] += pad_top

    identified_tires, possible_tires, _ = find_contained_circle_pairs(circles)

    return limit_boxes(
        np.concatenate(
            [
                concat_score(
                    circle_to_box(circles[identified_tires[:, 0]]),
                    calc_score(circles[identified_tires[:, 1], 2] / circles[identified_tires[:, 0], 2]),
                ),
                add_score(
                    circle_to_box(circles[possible_tires], rad_mult=1.45),
                    0.3,
                ),
            ],
            dtype=np.float32,
        ),
        image,
    ).astype(np.float32)


async def extract_from_frame(frame: npt.NDArray[np.uint8], sort: Sort) -> list[WheelBBX] | None:
    results = []

    detected_tires = detect_tires(image=frame)

    if len(detected_tires) == 0:
        sort.update()
        return None

    tracked = sort.update(detected_tires.astype(np.float32)).astype(np.float32)

    for x1, y1, x2, y2, index in tracked:
        tire = BoundingBox(
            x=int(x1),
            y=int(y1),
            w=int(x2 - x1),
            h=int(y2 - y1),
        ).scale(0.95)

        results.append(
            WheelBBX(
                id=index,
                rim=tire.scale(0.6),
                tire=tire,
            ),
        )

    return results


class ExtractedFrame(BaseModel):
    id: FrameId
    weight_class_id: WeightClassId

    status: FrameStatus = FrameStatus.NEW

    loc: str

    tire_bbxs: list[WheelBBX]

    def create(self, s3_client: S3Client) -> Frame:
        return Frame(
            id=self.id,
            weight_class_id=self.weight_class_id,
            status=self.status,
            s3_key=s3_client.config.get_weight_class_frame(weight_class_id=self.weight_class_id, frame_id=self.id),
            wheel_bbxs=self.tire_bbxs,
        )


async def upload_batch(s3_client: S3Client, db_session: async_sessionmaker[AsyncSession], batch: Sequence[ExtractedFrame], max_size: int) -> bool:
    if len(batch) > max_size:
        frames = [e_f.create(s3_client) for e_f in batch]

        async with db_session() as session:
            frame_reps = [FrameTable.new(f) for f in frames]
            session.add_all(frame_reps)
            await session.flush()

            await s3_client.batch_upload_files_to(
                fs=(f.loc for f in batch),
                ts=(f.s3_key for f in frames),
            )

            await session.commit()

        return True
    else:
        return False


async def extract_frames(
    video_file_name: str,
    weight_class_id: WeightClassId,
    db_session: async_sessionmaker[AsyncSession],
    s3_client: S3Client,
    *,
    skip_frame: int = 1,
    frame_batch_size: int = 2**5,
) -> None:

    assert skip_frame >= 0

    extracted_frames_batch: list[ExtractedFrame] = []
    frame_id = 0
    saved_frames = 0

    sort = Sort(
        max_age=15,
        min_hits=5,
        iou_threshold=0.3,
    )

    cap = cv2.VideoCapture(video_file_name)

    try:
        with TemporaryDirectory() as temp_dir:
            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    break

                frame_id += 1

                if frame_id % (skip_frame + 1) != 0:
                    continue

                extracted_tires = await extract_from_frame(frame=frame.astype(np.uint8), sort=sort)

                if extracted_tires is not None and len(extracted_tires) > 0:
                    frame_file = os.path.join(temp_dir, f"{frame_id}.jpg")
                    cv2.imwrite(frame_file, frame)

                    extracted_frames_batch.append(
                        ExtractedFrame(
                            id=FrameId(frame_id),
                            weight_class_id=weight_class_id,
                            loc=frame_file,
                            tire_bbxs=extracted_tires,
                        ),
                    )

                    if await upload_batch(s3_client, db_session, extracted_frames_batch, frame_batch_size):
                        saved_frames += len(extracted_frames_batch)
                        extracted_frames_batch.clear()

            await upload_batch(s3_client, db_session, extracted_frames_batch, 0)
            saved_frames += len(extracted_frames_batch)
    finally:
        cap.release()

    if frame_id == 0:
        raise RuntimeError("Did not process the video file")
    if saved_frames == 0:
        raise RuntimeError("Did not find frames with tires")
