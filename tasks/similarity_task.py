from csv import DictReader
from math import isnan

from scipy.stats import spearmanr
from tqdm import tqdm

from .task import Task


class SimilarityTask(Task):

    def compute(self, *args, **kwargs):
        our_similarities = []
        data_similarities = []
        csv_reader = DictReader(self.csv_wikidata_results)
        header_fields = csv_reader.fieldnames
        assert len(header_fields) == 3
        pbar = tqdm(csv_reader, total=self.size)
        with self.file_task_logger.new_file('similarities.csv').open('w') as similarity_file:
            for row in pbar:
                word1 = self.get_word_vector(row['word1'])
                word2 = self.get_word_vector(row['word2'])
                x = self.metric(word1, word2)
                similarity_file.write(','.join((row['word1'], row['word2'], str(x))) + '\n')
                if not isnan(x):
                    our_similarities.append(x)
                    data_similarities.append(row['score'])
        spearmanr_result = spearmanr(our_similarities, data_similarities)
        with self.file_task_logger.new_file('p-value.txt').open('w') as p_value_file:
            p_value_file.write(str(spearmanr_result.pvalue))
        return spearmanr_result.correlation
