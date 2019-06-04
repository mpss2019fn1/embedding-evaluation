from abc import ABC, abstractmethod
from pathlib import Path
import yaml

METADATA_FILE = 'metadata.yaml'


class Visualizer(ABC):

    @property
    @classmethod
    @abstractmethod
    def log_file(cls):
        return NotImplementedError

    @property
    @classmethod
    @abstractmethod
    def task_type(cls):
        return NotImplementedError

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    @classmethod
    def from_logging_directory(cls, logging_directory: Path):
        with logging_directory.joinpath(METADATA_FILE).open('r') as metadata_file:
            output_dir = logging_directory.joinpath('plots')
            output_dir.mkdir(parents=True, exist_ok=True)
            metadata = yaml.safe_load(metadata_file)
            gold_standard = metadata['data file']
            visualizer = [subclass for subclass in cls.__subclasses__() if subclass.task_type == metadata['task type']]
            if len(visualizer) < 1:
                raise NotImplementedError(f'No Visualization for Task Type {metadata["task type"]}')
            visualizer = visualizer[0]
            log_file = logging_directory.joinpath(visualizer.log_file)
            return visualizer(output_dir, gold_standard, log_file)
