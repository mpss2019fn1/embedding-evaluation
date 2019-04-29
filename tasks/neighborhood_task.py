from csv import DictReader
from tqdm import tqdm

from .task import Task


def all_avg_distance(vectors, metric):
    return metric(vectors)


class NeighborhoodTask(Task):

    def vectors(self):
        csv_reader = DictReader(self.csv_wikidata_results)
        header_fields = csv_reader.fieldnames
        assert len(header_fields) == 1
        pbar = tqdm(csv_reader, total=self.size)
        for row in pbar:
            yield self.gensim_loader.entity_vector(row[header_fields[0]].split('/Q')[-1])

    def __call__(self, *args, **kwargs):
        return self.metric(list(self.vectors())) / all_avg_distance(self.gensim_loader.vectors(), self.metric)
