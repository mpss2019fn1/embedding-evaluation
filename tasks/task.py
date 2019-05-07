from abc import ABC, abstractmethod
from task_logger import FileTaskLogger, NullFileTaskLogger


class Task(ABC):

    def __init__(self, name, csv_wikidata_results, metric, gensim_loader):
        self.name = name
        self.csv_wikidata_results = csv_wikidata_results
        self.metric = metric
        self.gensim_loader = gensim_loader
        self.size = sum(1 for _ in csv_wikidata_results) - 1
        self.csv_wikidata_results.seek(0)

    @property
    def configuration(self):
        return {'task type': self.__class__.__name__,
                'data file': self.csv_wikidata_results.name,
                'metric': self.metric.__name__}

    @abstractmethod
    def __call__(self, *args, **kwargs):
        ...
