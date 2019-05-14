from abc import ABC, abstractmethod


class Source(ABC):
    def __init__(self, source_config):
        self.config = source_config

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError
