from abc import ABC, abstractmethod
from attr import dataclass

from embedding_entry import EmbeddingEntry
from gensim_loader import PropsFetcherEntryNotFound, EmbeddingEntryNotFound


def log_unknown_entries(f):
    def function(self, entry):
        try:
            return f(self, entry)
        except PropsFetcherEntryNotFound as exception:
            self.unknown_knowledge_base_mapping.append(exception.key)
            return self.gensim_loader.null_vector
        except EmbeddingEntryNotFound as exception:
            self.unknown_embedding_entries.append(exception.key)
            return self.gensim_loader.null_vector
    return function


class Source(ABC):
    def __init__(self, source_config, logger, gensim_loader=None):
        self.config = source_config
        self.gensim_loader = gensim_loader
        self.unknown_embedding_entries = []
        self.unknown_knowledge_base_mapping = []
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
        with self.logger.new_file('unknown_embedding_entries.txt').open('w') as unknown_embedding_entries_file:
            for entry in sorted(self.unknown_embedding_entries):
                unknown_embedding_entries_file.write(entry + '\n')
        with self.logger.new_file('unknown_knowledge_base_mapping.txt').open('w') as unknown_mapping_file:
            for entry in sorted(self.unknown_knowledge_base_mapping):
                unknown_mapping_file.write(entry + '\n')

    @property
    @classmethod
    @abstractmethod
    def source_type(cls):
        return NotImplementedError

    @dataclass
    class Statistics:
        entries_found: int
        entry_misses: int
