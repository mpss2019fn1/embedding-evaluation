import logging
from abc import ABC, abstractmethod
from pathlib import Path

from file_task_logger import FileTaskLogger, NullFileTaskLogger
from tasks.metric import Metric
from tasks.task_type import TaskType


class Task(ABC):
    LABEL_NAME = "name"
    LABEL_TYPE = "type"
    LABEL_TEST_SET = "test_set"
    LABEL_METRIC = "metric"

    def __init__(self, name, test_set, metric, logging=False):
        self.name = name
        self.test_set = test_set
        self.metric = metric
        self.size = sum(1 for _ in test_set) - 1
        self.file_task_logger = FileTaskLogger('logging', self) if logging else NullFileTaskLogger()

    @property
    def configuration(self):
        return {'task type': self.__class__.__name__,
                'metric': self.metric.__name__}

    @abstractmethod
    def compute(self):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        result = self.compute(*args, **kwargs)
        with self.file_task_logger.new_file('result.txt').open('w') as result_file:
            result_file.write(str(result))
        return result

    @staticmethod
    def from_task_configuration(configuration):
        name = Task._extract_name(configuration)
        task_class = TaskType.from_string(configuration[Task.LABEL_TYPE])
        metric = Metric.from_string(configuration[Task.LABEL_METRIC])
        test_set = Task._extract_test_set(configuration)

        return task_class(name, test_set, metric)

    @staticmethod
    def _extract_name(configuration):
        name = configuration[Task.LABEL_NAME]

        if not name:
            logging.error("The provided task name must not be empty")
            raise KeyError

        return name

    @staticmethod
    def _extract_test_set(configuration):
        test_set = Path(configuration[Task.LABEL_TEST_SET])

        if not test_set.exists():
            logging.error(f"The provided test set {test_set} does not exist")
            raise KeyError

        return test_set



