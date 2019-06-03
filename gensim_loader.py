from gensim.models.keyedvectors import KeyedVectors


def load_embedding_file(embedding_file):
    return KeyedVectors.load_word2vec_format(embedding_file)


class EmbeddingEntryNotFound(Exception):
    def __init__(self, message, key):
        super().__init__(message)
        self.key = key


class VectorLoader:
    def __init__(self, embedding_file):
        self.vectors = load_embedding_file(embedding_file)

    def __getitem__(self, item):
        try:
            return self.vectors[item]
        except KeyError:
            raise EmbeddingEntryNotFound(f"embedding for key {item} not found", item)
