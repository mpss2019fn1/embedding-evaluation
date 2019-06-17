from math import isnan

from scipy.stats import spearmanr

from .task import Task


class SimilarityTask(Task):

    @classmethod
    def configuration_task_name(cls):
        return "similarity"

    def compute(self, *args, **kwargs):
        our_similarities = []
        data_similarities = []
        with self.file_task_logger.new_file('similarities.csv').open('w') as similarity_file:
            for row in self.source:
                word1, word2, score = row
                x = self.metric(word1.vector, word2.vector)
                similarity_file.write(','.join((word1.name, word2.name, str(x))) + '\n')
                if not isnan(x):
                    our_similarities.append(x)
                    data_similarities.append(score)
        spearmanr_result = spearmanr(our_similarities, data_similarities)
        with self.file_task_logger.new_file('p-value.txt').open('w') as p_value_file:
            p_value_file.write(str(spearmanr_result.pvalue))
        return spearmanr_result.correlation
