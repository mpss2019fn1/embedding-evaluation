import operator
from .task import Task


class AnalogyTask(Task):

    @classmethod
    def __name__(cls):
        return "analogy"

    def get_difference_vectors(self):
        for row in self.source:
            assert len(row) == 2
            yield operator.sub(*[entry.vector for entry in row])

    def compute(self, *args, **kwargs):
        difference_vectors = list(self.get_difference_vectors())
        return self.metric(difference_vectors)
