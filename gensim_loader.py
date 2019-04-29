import numpy as np
from gensim.models.doc2vec import Doc2Vec

from wikidata2wikipedia import WikidataEntry


class GensimLoader:

    def __init__(self, model_file):
        self.model = Doc2Vec.load(model_file)

    def entity_vector(self, entity_id):
        try:
            wikidata_entry = WikidataEntry(entity_id)
            return self.model[wikidata_entry.identifier]
        except KeyError:
            return np.zeros(self.model.vector_size)


if __name__ == '__main__':
    loader = GensimLoader('doc2vec.binary.model')
