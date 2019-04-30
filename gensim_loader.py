import numpy as np
from gensim.models.doc2vec import Doc2Vec
from wikipedia_props_fetcher import WikipediaPropsFetcher


class GensimLoader:

    def __init__(self, model_file):
        self.model = Doc2Vec.load(model_file)
        self.props_fetcher = None

    def entity_vector(self, wikidata_id):
        if self.props_fetcher is None:
            self.props_fetcher = WikipediaPropsFetcher('living_people_wikidata_id_wikipedia_page_id_title.csv')
        key = self.props_fetcher.get_identifier(wikidata_id)
        if key is None:
            return np.zeros(self.model.vector_size)
        try:
            return self.model[key]
        except KeyError:
            return np.zeros(self.model.vector_size)

    def vectors(self):
        return self.model.wv.vectors


if __name__ == '__main__':
    loader = GensimLoader('doc2vec.binary.model')
