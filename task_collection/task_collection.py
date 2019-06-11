import time

import yaml

from task_collection.test_category import TestCategory


class TaskCollection:

    LABEL_ROOT = "configuration"
    LABEL_TASK_SECTIONS = "tests"

    def __init__(self, categories):
        self.imported = time.time()
        self.categories = categories

    @staticmethod
    def from_test_definition(definition_file):
        with open(definition_file, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
        configuration = [*data_loaded]
        tests = configuration[TaskCollection.LABEL_ROOT][TaskCollection.LABEL_TASK_SECTIONS]
        categories = []
        for category_name in tests:
            categories.append(TestCategory.from_test_category_configuration(category_name, tests[category_name]))
