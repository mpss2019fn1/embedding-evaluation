from csv import DictReader
from operator import itemgetter

from .source import Source


class CSVSource(Source):

    source_type = 'csv'

    def __init__(self, source_config):
        super().__init__(source_config)
        self.csv_file = open(self.config['path'])
        self.reader = DictReader(self.csv_file, delimiter=self.config['csv_delimiter'])
        self.columns = list(self.config['columns']['input'].keys())
        output_columns = list(self.config['columns'].get('output', {}).keys())
        self.columns.extend(output_columns)

    def __iter__(self):
        for row in self.reader:
            yield itemgetter(*self.columns)(row)

