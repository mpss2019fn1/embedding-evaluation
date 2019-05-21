from abc import ABC, abstractmethod
from attr import dataclass

from embedding_entry import EmbeddingEntry


def log_unknown_entries(f):
    def function(self, entry):
        if entry not in self.gensim_loader.model.wv.vocab:
            self.unknown_entries.append(entry)
        return f(self, entry)
    return function


class Source(ABC):
    def __init__(self, source_config, logger, gensim_loader=None):
        self.config = source_config
        self.gensim_loader = gensim_loader
        self.unknown_entries = []
        self.logger = logger

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @classmethod
    def from_config(cls, source_config, *args):
        source_type = source_config['type']
        source_classes = [subclass for subclass in cls.__subclasses__() if
                          subclass.source_type == source_type]
        if len(source_classes) < 1:
            raise NotImplementedError(f'Source type {source_type} not defined')
        return source_classes[0](source_config, *args)

    def create_entry(self, key, value_type):
        if value_type == 'word_vector':
            return EmbeddingEntry(key, self.get_word_vector(key))
        elif value_type == 'wikidata_entity':
            return EmbeddingEntry(key, self.get_entity_vector(key.split('/Q')[-1]))
        else:
            return key

    @log_unknown_entries
    def get_word_vector(self, word):
        return self.gensim_loader.word_vector(word)

    @log_unknown_entries
    def get_entity_vector(self, entity):
        return self.gensim_loader.entity_vector(entity)

    def __del__(self):
        with self.logger.new_file('unknown_entries.txt').open('w') as unknown_words_file:
            for entry in sorted(self.unknown_entries):
                unknown_words_file.write(entry + '\n')

    @property
    @classmethod
    @abstractmethod
    def source_type(cls):
        return NotImplementedError

    @dataclass
    class Statistics:
        entries_found: int
        entry_misses: int


