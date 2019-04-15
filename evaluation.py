from csv import DictReader
from pathlib import Path
from itertools import combinations
from gensim_loader import GensimLoader
import numpy as np
import scipy
from tqdm import tqdm

query_result_directory = Path('query_results')
embedding_file = Path('')
difference_vector_directory = Path('difference_vectors')


def difference_vector(vec_loader, entity1, entity2):
    vec1 = vec_loader.entity_vector(entity1)
    vec2 = vec_loader.entity_vector(entity2)
    return vec1 - vec2


def compute_vec_similarity(vectors):
    similarity_values = []
    for a, b in combinations(vectors, 2):
        similarity = scipy.spatial.distance.cosine(a, b)
        if not np.isnan(similarity):
            similarity_values.append(similarity)
    return np.mean(similarity_values)


def main():
    vec_loader = GensimLoader('doc2vec.binary.model')
    for query_result_file in query_result_directory.iterdir():
        with query_result_file.open() as f:
            csv_reader = DictReader(f)
            vec_diffs = [difference_vector(vec_loader, row['a'].split('/Q')[-1], row['b'].split('/Q')[-1]) for row in
                         tqdm(csv_reader)]
        score = compute_vec_similarity(vec_diffs)
        print(query_result_file.stem, score)


if __name__ == '__main__':
    main()
