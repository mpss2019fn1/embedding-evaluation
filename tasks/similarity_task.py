from csv import DictReader
from math import isnan

from scipy.stats import spearmanr
from tqdm import tqdm

from .task import Task


class SimilarityTask(Task):

    def compute(self, *args, **kwargs):
        our_similarities = []
        data_similarities = []
        with self.file_task_logger.new_file('similarities.csv').open('w') as similarity_file:
            for row in self.source:
                word1, word2, score = row
                word1_vector = self.get_word_vector(word1)
                word2_vector = self.get_word_vector(word2)
                x = self.metric(word1_vector, word2_vector)
                similarity_file.write(','.join((word1, word2, str(x))) + '\n')
                if not isnan(x):
                    our_similarities.append(x)
                    data_similarities.append(score)
        spearmanr_result = spearmanr(our_similarities, data_similarities)
        with self.file_task_logger.new_file('p-value.txt').open('w') as p_value_file:
            p_value_file.write(str(spearmanr_result.pvalue))
        return spearmanr_result.correlation
