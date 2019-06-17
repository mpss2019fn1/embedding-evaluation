import logging

from tasks.task import Task
from tasks.task_type import TaskType


class TestCategory:
    LABEL_NAME = "name"
    LABEL_ENABLED = "enabled"
    LABEL_TASKS = "tasks"
    LABEL_TASK = "task"
    LABEL_CATEGORIES = "categories"
    LABEL_CATEGORY = "category"

    def __init__(self, name, enabled, tasks, categories):
        self._name = name
        self._enabled = enabled
        self._tasks = tasks
        self._categories = categories

    @staticmethod
    def from_test_category_configuration(configuration):
        name = TestCategory._extract_name(configuration)
        enabled = TestCategory._extract_enabled(configuration)
        tasks = TestCategory._extract_tasks(configuration)
        categories = TestCategory._extract_categories(configuration)
        return TestCategory(name, enabled, tasks, categories)

    @staticmethod
    def _extract_enabled(configuration):
        enabled = str(configuration[TestCategory.LABEL_ENABLED]).lower()

        if enabled not in ["true", "false"]:
            logging.error("The provided boolean value for enabled are not valid")
            raise KeyError

        return enabled == "true"

    @staticmethod
    def _extract_name(configuration):
        name = configuration[TestCategory.LABEL_NAME]

        if not name:
            logging.error("The provided task name must not be empty")
            raise KeyError

        return name

    @staticmethod
    def _extract_tasks(configuration):
        tasks = []
        for task in configuration[TestCategory.LABEL_TASKS]:
            task_configuration = task[TestCategory.LABEL_TASK]
            task_class = TaskType.from_string(task_configuration[Task.LABEL_TYPE])
            tasks.append(task_class.from_task_configuration(task_configuration))
        return tasks

    @staticmethod
    def _extract_categories(configuration):
        categories = []
        for sub_category_configuration in configuration[TestCategory.LABEL_CATEGORIES]:
            sub_category_configuration = sub_category_configuration[TestCategory.LABEL_CATEGORY]
            categories.append(TestCategory.from_test_category_configuration(sub_category_configuration))
        return categories
