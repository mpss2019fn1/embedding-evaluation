from csv import DictReader

from .task import Task


class NeighborhoodTask(Task):

    def vectors(self):
        csv_reader = DictReader(self.csv_wikidata_results)
        header_fields = csv_reader.fieldnames
        assert len(header_fields) == 1
        for row in csv_reader:
            yield self.gensim_loader.entity_vector(row[header_fields[0]].split('/Q')[-1])

    def __call__(self, *args, **kwargs):
        return 1
