import numpy as np
from gensim.models.doc2vec import Doc2Vec
from wikipedia_props_fetcher import WikipediaPropsFetcher


class EmbeddingEntryNotFound(Exception):
    def __init__(self, message, key):
        super().__init__(message)
        self.key = key


class PropsFetcherEntryNotFound(Exception):
    def __init__(self, message, key):
        super().__init__(message)
        self.key = key


class VectorLoader:
    def __init__(self, model_file):
        self.model = Doc2Vec.load(model_file)
        self.props_fetcher = WikipediaPropsFetcher('data/living_people_wikidata_id_wikipedia_page_id_title.csv', ';')
        self.null_vector = np.zeros(self.model.vector_size)

    def entity_vector(self, wikidata_id):
        key = self.props_fetcher.get_identifier(wikidata_id)
        if key is None:
            raise PropsFetcherEntryNotFound(f"{key} was not found in the props fetcher file", wikidata_id)
        return self.get_embedding(key, self.model)

    def word_vector(self, word):
        return self.get_embedding(word, self.model.wv)

    def get_embedding(self, key, embedding_dictionary):
        try:
            return embedding_dictionary[key]
        except KeyError:
            raise EmbeddingEntryNotFound(f"{key} was not found in the embedding", key)

    def vectors(self):
        return self.model.wv.vectors

    @staticmethod
    def save_to_file(iterable, filename):
        with open(filename, 'w+') as file:
            for entry in iterable:
                file.write(entry + '\n')
