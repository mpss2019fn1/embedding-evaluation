import logging
from enum import Enum

from tasks import AnalogyTask, SimilarityTask, NeighborhoodTask, OutlierDetectionTask


class TaskType(Enum):
    ANALOGY = AnalogyTask
    SIMILARITY = SimilarityTask
    NEIGHBORHOOD = NeighborhoodTask
    OUTLIER_DETECTION = OutlierDetectionTask

    @classmethod
    def from_string(cls, task_type):
        for member in TaskType:
            if task_type == member.__name__:
                return member
        logging.error(f"Unable to find TaskType {task_type}")
        raise KeyError
