from csv import DictReader
from tqdm import tqdm
from gensim_loader import GensimLoader
from metrics import mean_cosine_similarity
from pathlib import Path


class AnalogyTask:

    def __init__(self, csv_wikidata_results, metric, gensim_loader):
        self.csv_wikidata_results = csv_wikidata_results
        self.metric = metric
        self.gensim_loader = gensim_loader
        self.size = sum(1 for _ in csv_wikidata_results)
        self.csv_wikidata_results.seek(0)

    def difference_vector(self, entity1, entity2):
        vec1 = self.gensim_loader.entity_vector(entity1)
        vec2 = self.gensim_loader.entity_vector(entity2)
        return vec1 - vec2

    def get_difference_vectors(self):
        csv_reader = DictReader(self.csv_wikidata_results)
        header_fields = csv_reader.fieldnames
        pbar = tqdm(csv_reader, total=self.size)
        for row in pbar:
            values = [row[field].split('/Q')[-1] for field in header_fields]
            pbar.set_description(f'Processing pair: {values}')
            yield self.difference_vector(*values)

    def __call__(self, *args, **kwargs):
        difference_vectors = list(self.get_difference_vectors())
        return self.metric(difference_vectors)


if __name__ == '__main__':
    gensim_loader = GensimLoader('doc2vec.binary.model')
    query_result_directory = Path('analogy_query_results')
    for query_result_file in query_result_directory.iterdir():
        with query_result_file.open() as f:
            analogy_task = AnalogyTask(f, mean_cosine_similarity, gensim_loader)
            result = analogy_task()
