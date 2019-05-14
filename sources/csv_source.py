from csv import DictReader
from operator import itemgetter

from .source import Source


class CSVSource(Source):
    def __init__(self, source_config):
        super().__init__(source_config)
        self.reader = DictReader(self.config['path'], delimiter=self.config['csv_delimiter'])
        self.columns = list(self.config['columns']['input'].keys())
        output_columns = list(self.config['columns']['output'].keys())
        self.columns.extend(output_columns)

    def __iter__(self):
        for row in self.reader:
            yield itemgetter(*self.columns)(row)
