from tasks.task import Task


class OutlierDetectionTask(Task):

    @classmethod
    def configuration_task_name(cls):
        return "outlier_detection"

    def compute(self):
        pass