from csv import DictReader
from math import isnan

from scipy.stats import spearmanr
from tqdm import tqdm

from .task import Task


class SimilarityTask(Task):

    def __call__(self, *args, **kwargs):
        our_similarities = []
        data_similarities = []
        csv_reader = DictReader(self.csv_wikidata_results)
        header_fields = csv_reader.fieldnames
        assert len(header_fields) == 3
        pbar = tqdm(csv_reader, total=self.size)
        for row in pbar:
            word1 = self.gensim_loader.word_vector(row['word1'])
            word2 = self.gensim_loader.word_vector(row['word2'])
            x = self.metric(word1, word2)
            if not isnan(x):
                our_similarities.append(x)
                data_similarities.append(row['score'])
        return spearmanr(our_similarities, data_similarities).correlation
