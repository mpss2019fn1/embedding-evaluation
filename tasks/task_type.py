import logging
from enum import Enum

from tasks.analogy_task import AnalogyTask
from tasks.neighborhood_task import NeighborhoodTask
from tasks.outlier_detection_task import OutlierDetectionTask
from tasks.similarity_task import SimilarityTask


class TaskType(Enum):
    ANALOGY = AnalogyTask
    SIMILARITY = SimilarityTask
    NEIGHBORHOOD = NeighborhoodTask
    OUTLIER_DETECTION = OutlierDetectionTask

    @classmethod
    def from_string(cls, task_type):
        for member in TaskType:
            if task_type == member.value.configuration_task_name():
                return member.value
        logging.error(f"Unable to find TaskType {task_type}")
        raise KeyError
