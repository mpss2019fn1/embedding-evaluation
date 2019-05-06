from .task import Task

from csv import DictReader
from tqdm import tqdm

from scipy.stats import spearmanr


class SimilarityTask(Task):

    def __init__(self, csv_wikidata_results, metric, gensim_loader):
        super().__init__(csv_wikidata_results, metric, gensim_loader)
        self.our_similarities = []
        self.data_similarities = []

    def score(self):
        csv_reader = DictReader(self.csv_wikidata_results)
        header_fields = csv_reader.fieldnames
        assert len(header_fields) == 3
        pbar = tqdm(csv_reader, total=self.size)
        for row in pbar:
            word1 = self.gensim_loader.word_vector(row['word1'])
            word2 = self.gensim_loader.word_vector(row['word2'])
            self.our_similarities.append(self.metric(word1, word2))
            self.data_similarities.append(row['score'])
        return spearmanr(self.our_similarities, self.data_similarities).correlation

    def __call__(self, *args, **kwargs):
        return self.score()
