from abc import ABC, abstractmethod
from file_task_logger import FileTaskLogger, NullFileTaskLogger


class Task(ABC):

    def __init__(self, name, csv_wikidata_results, metric, gensim_loader, logging=False):
        self.name = name
        self.csv_wikidata_results = csv_wikidata_results
        self.metric = metric
        self.gensim_loader = gensim_loader
        self.size = sum(1 for _ in csv_wikidata_results) - 1
        self.csv_wikidata_results.seek(0)
        self.file_task_logger = FileTaskLogger('logging', self) if logging else NullFileTaskLogger()
        self.unknown_words = []

    def __del__(self):
        with self.file_task_logger.new_file('unknown_words.txt').open('w') as unknown_words_file:
            for word in sorted(self.unknown_words):
                unknown_words_file.write(word + '\n')

    def get_word_vector(self, word):
        if word not in self.gensim_loader.model.wv.vocab:
            self.unknown_words.append(word)
        return self.gensim_loader.word_vector(word)

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
