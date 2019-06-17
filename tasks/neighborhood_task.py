import numpy as np
from tasks.task import Task


class NeighborhoodTask(Task):

    @classmethod
    def configuration_task_name(cls):
        return "neighborhood"

    def compute(self, *args, **kwargs):
        vectors = [row[0].vector for row in self.source if row[0].vector is not np.zeros(row[0].vector.shape[0])]
        return self.metric(vectors)
