import math
import os
import csv

from csv import DictReader
from tqdm import tqdm
from metrics import mean_squared_pairwise_distance
from gensim_loader import GensimLoader

from tasks.task import Task


class NeighborhoodTask(Task):

    def vectors(self, statistics):
        """
        Returns a list of embeddings. The embeddings are fetched by using the wikidata id to get the wikipedia page id
        and then using the wikipedia page id to get the title to that that id. The title is then passed to the model
        to receive the embedding.
        :return: List of embedding vectors to 'hopefully' every entry in 'csv_wikidata_results'
        """

        csv_reader = DictReader(self.csv_wikidata_results)
        header_fields = csv_reader.fieldnames
        assert len(header_fields) == 1
        pbar = tqdm(csv_reader, total=self.size)
        embeddings = []
        for row in pbar:
            statistics.wikidata_entry_count = statistics.wikidata_entry_count + 1
            embedding = self.gensim_loader.entity_vector(row[header_fields[0]].split('/Q')[-1])
            if embedding is not self.gensim_loader.null_vector:
                embeddings.append(embedding)
                statistics.embeddings_found = statistics.embeddings_found + 1
        return embeddings

    def compute(self, *args, **kwargs):
        # Each vector in vectors corresponds to an embedding
        self.statistics = self.Statistics()
        self.statistics.name_of__metric = self.metric.__name__
        embeddings = self.vectors(self.statistics)
        self.statistics.score = self.metric(embeddings)
        return self.statistics.score

    class Statistics:
        def __init__(self):
            self.score = math.nan
            self.wikidata_entry_count = 0
            self.embeddings_found = 0
            self.name_of_metric = "NoName"


if __name__ == '__main__':
    loader = GensimLoader('doc2vec.binary.model')

    print("dataset;name_of_metric;wikidata_entries;found_embeddings;score")

    for filename in os.listdir('avg_query_results'):
        if filename.endswith('.csv'):
            with open("avg_query_results/" + filename, encoding='utf-8') as file:
                task = NeighborhoodTask(file, mean_squared_pairwise_distance, loader)
                task()
                print(f'{filename[:-4]};{task.statistics.name_of_metric};{task.statistics.wikidata_entry_count};'
                      f'{task.statistics.embeddings_found};{task.statistics.score}')


