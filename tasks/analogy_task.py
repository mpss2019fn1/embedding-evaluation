from pathlib import Path
from gensim_loader import GensimLoader
from metrics import mean_cosine_similarity
from .task import Task


class AnalogyTask(Task):

    def difference_vector(self, entity1, entity2):
        vec1 = self.gensim_loader.word_vector(entity1)
        vec2 = self.gensim_loader.word_vector(entity2)
        return vec1 - vec2

    def get_difference_vectors(self):

        for row in self.source:
            values = [value for value in row]
            yield self.difference_vector(*values)

    def compute(self, *args, **kwargs):
        difference_vectors = list(self.get_difference_vectors())
        return self.metric(difference_vectors)


if __name__ == '__main__':
    gensim_loader = GensimLoader('doc2vec.binary.model')
    query_result_directory = Path('analogy_query_results')
    for query_result_file in query_result_directory.iterdir():
        with query_result_file.open() as f:
            analogy_task = AnalogyTask(f, mean_cosine_similarity, gensim_loader)
            result = analogy_task()
