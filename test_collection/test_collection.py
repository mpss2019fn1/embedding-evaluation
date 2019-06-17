import time

import yaml

from test_collection import TestCategory


class TestCollection:

    LABEL_ROOT = "configuration"
    LABEL_CATEGORIES = "categories"
    LABEL_CATEGORY = "category"

    def __init__(self, categories):
        self.imported = time.time()
        self.categories = categories

    @staticmethod
    def from_test_definition(definition_file):
        with open(definition_file, 'r') as stream:
            configuration = yaml.safe_load(stream)
        categories = configuration[TestCollection.LABEL_ROOT][TestCollection.LABEL_CATEGORIES]
        for category in categories:
            categories.append(TestCategory.from_test_category_configuration(category[TestCollection.LABEL_CATEGORY]))
