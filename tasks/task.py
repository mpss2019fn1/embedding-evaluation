from abc import ABC, abstractmethod


class Task(ABC):

    def __init__(self, csv_wikidata_results, metric, gensim_loader):
        self.csv_wikidata_results = csv_wikidata_results
        self.metric = metric
        self.gensim_loader = gensim_loader
        self.size = sum(1 for _ in csv_wikidata_results)
        self.csv_wikidata_results.seek(0)

    @abstractmethod
    def __call__(self, *args, **kwargs):
        ...
