import numpy as np
from scipy.spatial.distance import pdist

metrics = dict()


# Decorator to add the metric to the metrics dictionary
def metric(func):
    metrics[func.__name__] = func
    return func


@metric
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


@metric
def mean_squared_pairwise_distance(vectors):
    matrix = np.array(vectors)
    return np.var(matrix, 0, ddof=1).sum() * 2


@metric
def mean_pairwise_distance(vectors):
    matrix = np.array(vectors)
    euclidean_distances = pdist(matrix, 'euclidean')
    return np.nanmean(euclidean_distances)
