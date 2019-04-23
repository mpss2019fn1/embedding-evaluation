import argparse
import numpy as np
from gensim_loader import GensimLoader
from pathlib import Path
from csv import DictReader
from tqdm import tqdm
from scipy.spatial.distance import cdist
from gensim.models.doc2vec import Doc2Vec


def main(args):
    vec_loader = GensimLoader(args.embedding_file)
    for query_result_file in args.query_result_directory.iterdir():
        with query_result_file.open() as f:
            csv_reader = DictReader(f)
            embeddings = [vec_loader.entity_vector(row['a'].split('/Q')[-1]) for row in tqdm(csv_reader)]
            matrix = np.array(embeddings)
            euclidean_distances = cdist(matrix, matrix, 'euclidean')
            score = np.nanmean(euclidean_distances)
            print(score)
    model = Doc2Vec.load('doc2vec.binary.model')
    euclidean_distances_all = cdist(model.wv.vectors, model.wv.vectors, 'euclidean')
    score = np.nanmean(euclidean_distances_all)
    print(score)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-query_result_directory",
        type=Path,
        help="Path to the query result directory",
        default=Path(__file__).absolute().parent / "avg_query_results",
    )
    parser.add_argument(
        "-embedding_file",
        type=str,
        help="Path to the embedding file directory",
        default="doc2vec.binary.model",
    )
    args = parser.parse_args()
    main(args)

