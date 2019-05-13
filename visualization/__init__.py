from .visualizer import Visualizer
from .similarity_visualizer import SimilarityVisualizer

visualizer_mapping = {'SimilarityTask': SimilarityVisualizer}

__all__ = [
    "Visualizer",
    "SimilarityVisualizer"
]