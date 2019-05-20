import numpy as np
from gensim.models.doc2vec import Doc2Vec
from wikipedia_props_fetcher import WikipediaPropsFetcher


class GensimLoader:
    def __init__(self, model_file):
        self.model = Doc2Vec.load(model_file)
        self.props_fetcher = None
        self.null_vector = np.zeros(self.model.vector_size)
        self.embedding_not_found_set = set()
        self.identifier_not_found_set = set()

    def entity_vector(self, wikidata_id):
        key = self.props_fetcher.get_identifier(wikidata_id)
        if key is None:
            self.identifier_not_found_set.add(wikidata_id)
            return self.null_vector
        try:
            return self.model[key]
        except KeyError:
            self.embedding_not_found_set.add(key)
            return self.null_vector

    def word_vector(self, word):
        try:
            return self.model[word]
        except KeyError:
            return self.null_vector

    def vectors(self):
        return self.model.wv.vectors

    @staticmethod
    def save_to_file(iterable, filename):
        with open(filename, "w+") as file:
            {file.write(entry + "\n") for entry in iterable}




if __name__ == '__main__':
    loader = GensimLoader('doc2vec.binary.model')
