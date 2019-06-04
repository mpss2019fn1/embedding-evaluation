from abc import ABC, abstractmethod
from file_task_logger import FileTaskLogger, NullFileTaskLogger

from sources import Source


class Task(ABC):

    def __init__(self, name, csv_wikidata_results, metric, gensim_loader, source, logging=False):
        self.name = name
        self.csv_wikidata_results = csv_wikidata_results
        self.metric = metric
        self.size = sum(1 for _ in csv_wikidata_results) - 1
        self.csv_wikidata_results.seek(0)
        self.file_task_logger = FileTaskLogger('logging', self) if logging else NullFileTaskLogger()
        self.source = Source.from_config(source, self.file_task_logger, gensim_loader)

    @property
    def configuration(self):
        return {'task type': self.__class__.__name__,
                'data file': self.csv_wikidata_results.name,
                'metric': self.metric.__name__}

    @abstractmethod
    def compute(self):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        result = self.compute(*args, **kwargs)
        with self.file_task_logger.new_file('result.txt').open('w') as result_file:
            result_file.write(str(result))
        return result
