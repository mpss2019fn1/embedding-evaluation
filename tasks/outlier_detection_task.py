from tasks.task import Task


class OutlierDetectionTask(Task):

    @classmethod
    def __name__(cls):
        return "outlier_detection"

    def compute(self):
        pass