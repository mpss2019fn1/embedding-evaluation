import numpy as np
from gensim.models.doc2vec import Doc2Vec


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
        return self.get_embedding(key, self.model)

    def word_vector(self, word):
        return self.get_embedding(word, self.model.wv)

    def get_embedding(self, key, embedding_dictionary):
        try:
            return embedding_dictionary[key]
        except KeyError:
            self.embedding_not_found_set.add(key)
            return self.null_vector

    def vectors(self):
        return self.model.wv.vectors

    @staticmethod
    def save_to_file(iterable, filename):
        with open(filename, "w+") as file:
            {file.write(entry + "\n") for entry in iterable}

