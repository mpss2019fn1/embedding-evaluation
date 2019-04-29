import numpy as np


def mean_cosine_similarity(vectors):
    matrix = np.array(vectors)
    dot_products = matrix.dot(matrix.T)
    norms = np.array([np.linalg.linalg.norm(matrix, axis=1)]) * np.array([np.linalg.linalg.norm(matrix, axis=1)]).T

    # if entry is 0/0 ignore entry and set as nan.
    with np.errstate(divide='ignore', invalid='ignore'):
        cosine_similarity = dot_products / norms
    cosine_distance = 1 - cosine_similarity

    # ignore all values set to nan for mean calc.
    return np.nanmean(cosine_distance)
