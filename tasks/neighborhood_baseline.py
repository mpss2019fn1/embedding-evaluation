import random
from gensim_loader import VectorLoader
from metrics import mean_squared_pairwise_distance


class NeighborhoodBaseline:

    def __init__(self, gensim_loader):
        self.gensim_loader = gensim_loader
        # make gensim loader load wikidata_wikipedia_dictionary
        self.gensim_loader.entity_vector('0')
        self.wikidata_ids = list(self.gensim_loader.props_fetcher.dictionary.keys())

    def compute(self, sample_size):
        """
        Computes a baseline for living people with sample_size many people
        :return:
        """
        # wähle zufällig leute aus

        selected_wikidata_ids = set([])
        embedding_vectors = []

        while len(selected_wikidata_ids) < sample_size:
            wikidata_id = random.choice(self.wikidata_ids)[1:]
            embedding = self.gensim_loader.entity_vector(wikidata_id)
            if embedding is not self.gensim_loader.null_vector:
                embedding_vectors.append(embedding)
                selected_wikidata_ids.add(wikidata_id)

        return mean_squared_pairwise_distance(embedding_vectors)


if __name__ == '__main__':
    loader = VectorLoader('doc2vec.binary.model')
    baseline = NeighborhoodBaseline(loader)
    print("samples;mean_squared_pairwise_distance")
    sample_sizes = [10, 100, 1000, 10000, 100000, 200000]
    repeats = 100
    for sample_size in sample_sizes:
        for i in range(repeats):
            print(f'{sample_size};{baseline.compute(sample_size)}')
