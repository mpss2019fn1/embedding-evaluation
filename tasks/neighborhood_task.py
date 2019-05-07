from csv import DictReader
from tqdm import tqdm
from functools import lru_cache

from .task import Task


@lru_cache(maxsize=None)
def all_avg_distance(gensim_loader, metric):
    return metric(gensim_loader.vectors())



# generiere eine baseline
# wähle zufällig x Datensätze aus (word vectors / entity vectors)
# wende Metrik auf sie an.







class NeighborhoodTask(Task):

    def vectors(self):
        """
        Returns a list of embeddings. The embeddings are fetched by using the wikidata id to get the wikipedia page id
        and then using the wikipedia page id to get the title to that that id. The title is then passed to the model
        to receive the embedding.
        :return: List of embedding vectors to 'hopefully' every entry in 'csv_wikidata_results'
        """

        # to improve performance we need the following:
        # collect all wikidata ids
        # get all wikipedia page ids
        # get all titles to wikipedia page ids in one request,l

        csv_reader = DictReader(self.csv_wikidata_results)
        header_fields = csv_reader.fieldnames
        assert len(header_fields) == 1
        pbar = tqdm(csv_reader, total=self.size)
        for row in pbar:
            yield self.gensim_loader.entity_vector(row[header_fields[0]].split('/Q')[-1])

    def compute(self, *args, **kwargs):
        # Each vector in vectors corresponds to an embedding
        return self.metric(list(self.vectors())) / all_avg_distance(self.gensim_loader, self.metric)
