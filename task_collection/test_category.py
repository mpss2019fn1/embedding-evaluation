import logging
from pathlib import Path

from tasks import SimilarityTask, AnalogyTask, NeighborhoodTask
from tasks.metric import Metric


class TestCategory:
    LABEL_TASKS = "tasks"
    LABEL_TEST_SET = "test_set"
    LABEL_METRIC = "metric"
    LABEL_CATEGORIES = "categories"
    LABEL_ENABLED = "enabled"
    SUPPORTED_TASKS = {
        "similarity": SimilarityTask,
        "analogy": AnalogyTask,
        "neighborhood": NeighborhoodTask,
        "outlier_detection": NotImplementedError
    }

    def __init__(self, name, enabled, tasks, categories):
        self._name = name
        self._enabled = enabled
        self._tasks = tasks
        self._categories = categories

    @staticmethod
    def from_test_category_configuration(name, test_category_configuration):
        tasks = []
        categories = []
        for task_name in test_category_configuration[TestCategory.LABEL_TASKS]:
            if task_name not in TestCategory.SUPPORTED_TASKS:
                logging.error(f"Unsupported test task type {task_name}")
                continue
            task = TestCategory._create_task(task_name, test_category_configuration)
            if task:
                tasks.append(task)

        for sub_category_name in test_category_configuration[TestCategory.LABEL_CATEGORIES]:
            subcategory_config = test_category_configuration[TestCategory.LABEL_CATEGORIES][sub_category_name]
            categories.append(TestCategory.from_test_category_configuration(sub_category_name, subcategory_config))

        return TestCategory(name, test_category_configuration[TestCategory.LABEL_ENABLED], tasks, categories)

    @staticmethod
    def _create_task(task_name, category_configuration):
        metric = category_configuration[TestCategory.LABEL_METRIC]
        test_set = Path(category_configuration[TestCategory.LABEL_TEST_SET])

        if metric not in Metric:
            logging.error(f"Unsupported metric type {metric}")
            return None

        if not test_set.exists():
            logging.error(f"The provided test set {test_set} does not exist")
            return None

        return TestCategory.SUPPORTED_TASKS[task_name](task_name, test_set, Metric[metric])
