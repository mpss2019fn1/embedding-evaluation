from csv import DictReader
from operator import itemgetter

from .source import Source


class CSVSource(Source):
    source_type = 'csv'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csv_file = open(self.config['path'])
        self.reader = DictReader(self.csv_file, delimiter=self.config['csv_delimiter'])
        self.columns = self.config['columns']['input']
        output_columns = self.config['columns'].get('output', {})
        self.columns.update(output_columns)

    def __iter__(self):
        for row in self.reader:
            yield [self.create_entry(column, type) for column, type in
                   zip(itemgetter(*self.columns.keys())(row), self.columns.values())]
