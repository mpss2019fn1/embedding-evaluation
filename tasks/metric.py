import logging
from enum import Enum


class Metric(Enum):
    COSINE_SIMILARITY = "cosine"
    EUCLIDEAN_DISTANCE = "euclidean"

    @classmethod
    def from_string(cls, metric):
        if metric not in Metric:
            logging.error(f"Unsupported metric type {metric}")
            raise KeyError
        return Metric[metric]
