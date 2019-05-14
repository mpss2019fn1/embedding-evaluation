from abc import ABC, abstractmethod


class Source(ABC):
    def __init__(self, source_config):
        self.config = source_config

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError

    @classmethod
    def from_config(cls, source_config):
        source_type = source_config['type']
        source_classes = [subclass for subclass in cls.__subclasses__() if
                          subclass.source_type == source_type]
        if len(source_classes) < 1:
            raise NotImplementedError(f'Source type {source_type} not defined')
        return source_classes[0](source_config)

    @property
    @classmethod
    @abstractmethod
    def source_type(cls):
        return NotImplementedError
