import time

import yaml

ROOT_LABEL = "configuration"
LABEL_TASK_SECTIONS = "tests"


class TaskCollection:

    def __init__(self):
        self.imported = time.time()

    @staticmethod
    def from_test_definition(definition_file):
        with open(definition_file, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
        configuration = [*data_loaded]
        tests = configuration[ROOT_LABEL][LABEL_TASK_SECTIONS]
        for category in tests:
            # create tasks
            pass
