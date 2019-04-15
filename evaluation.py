import argparse
import numpy as np
from csv import DictReader
from pathlib import Path
from gensim_loader import GensimLoader
from tqdm import tqdm


def difference_vector(vec_loader, entity1, entity2):
    vec1 = vec_loader.entity_vector(entity1)
    vec2 = vec_loader.entity_vector(entity2)
    return vec1 - vec2


def compute_vec_similarity(vectors):
    matrix = np.array(vectors)
    dot_products = matrix.dot(matrix.T)
    norms = np.array([np.linalg.linalg.norm(matrix, axis=1)]) * np.array([np.linalg.linalg.norm(matrix, axis=1)]).T

    # if entry is 0/0 ignore entry and set as nan.
    with np.errstate(divide='ignore', invalid='ignore'):
        cosine_similarity = dot_products / norms
    cosine_distance = 1 - cosine_similarity

    # ignore all values set to nan for mean calc.
    return np.nanmean(cosine_distance)


def main(args):
    vec_loader = GensimLoader(args.embedding_file)
    for query_result_file in args.query_result_directory.iterdir():
        with query_result_file.open() as f:
            csv_reader = DictReader(f)
            vec_diffs = [difference_vector(vec_loader, row['a'].split('/Q')[-1], row['b'].split('/Q')[-1]) for row in
                         tqdm(csv_reader)]
        score = compute_vec_similarity(vec_diffs)
        print(query_result_file.stem, score)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-query_result_directory",
        type=Path,
        help="Path to the query result directory",
        default=Path(__file__).absolute().parent / "query_results",
    )
    parser.add_argument(
        "-difference_vector_directory",
        type=Path,
        help="Path to the difference vectors directory",
        default=Path(__file__).absolute().parent / "difference_vectors",
    )
    parser.add_argument(
        "-embedding_file",
        type=str,
        help="Path to the embedding file directory",
        default="doc2vec.binary.model",
    )
    args = parser.parse_args()
    main(args)
