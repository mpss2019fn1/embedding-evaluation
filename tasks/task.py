from abc import ABC, abstractmethod
from file_task_logger import FileTaskLogger, NullFileTaskLogger


class Task(ABC):

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
