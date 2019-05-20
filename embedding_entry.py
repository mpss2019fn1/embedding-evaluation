from attr import dataclass
import numpy as np


@dataclass
class EmbeddingEntry:
    name: str
    vector: np.ndarray
