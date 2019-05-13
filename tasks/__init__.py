from .analogy_task import AnalogyTask
from .neighborhood_task import NeighborhoodTask
from .similarity_task import SimilarityTask

task_mapping = {'analogy': AnalogyTask, 'neighborhood': NeighborhoodTask, 'similarity': SimilarityTask}

__all__ = [
    "AnalogyTask",
    "NeighborhoodTask",
    "SimilarityTask",
    "task_mapping"
]
