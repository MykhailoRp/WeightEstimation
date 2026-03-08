import numpy as np
import numpy.typing as npt

class Sort:
    def __init__(self, max_age: int = 1, min_hits: int = 3, iou_threshold: float = 0.3, score_threshold: float = 0.35):
        """
        Sets key parameters for SORT
        """

    def update(self, dets: npt.NDArray[np.float32] = np.empty((0, 5), np.float32)) -> npt.NDArray[np.float32]:
        """
        Params:
          dets - a numpy array of detections in the format [[x1,y1,x2,y2,score],[x1,y1,x2,y2,score],...]
        Requires: this method must be called once for each frame even with empty detections (use np.empty((0, 5)) for frames without detections).
        Returns the a similar array, where the last column is the object ID.

        NOTE: The number of objects returned may differ from the number of detections provided.
        """
