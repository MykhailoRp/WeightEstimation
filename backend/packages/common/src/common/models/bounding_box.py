from collections.abc import Sequence
from typing import Self

from pydantic import BaseModel


class BoundingBox(BaseModel):
    x: int
    y: int
    h: int
    w: int

    @property
    def bbx(self) -> Sequence[int]:
        return self.x, self.y, self.w, self.h

    @property
    def pt1(self) -> Sequence[int]:
        return self.x, self.y

    @property
    def pt2(self) -> Sequence[int]:
        return self.x + self.w, self.y + self.h

    @property
    def x1y1x2y2(self) -> list[int]:
        return [self.x, self.y, self.x + self.w, self.y + self.h]

    @property
    def ratio(self) -> float:
        return self.w / self.h

    @property
    def center(self) -> tuple[int, int]:
        return self.x + self.w // 2, self.y + self.h // 2

    def is_square(self) -> bool:
        if self.h == 0 or self.w == 0:
            return False
        return 0.98 < self.ratio < 1.02

    def scale(self, pad: float) -> Self:
        x_pad = int(self.w * ((pad - 1) / 2))
        y_pad = int(self.h * ((pad - 1) / 2))
        return self.__class__(
            x=self.x - x_pad,
            y=self.y - y_pad,
            w=self.w + x_pad * 2,
            h=self.h + y_pad * 2,
        )
