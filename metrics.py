import numpy as np
from scipy.spatial.distance import pdist

metrics = dict()


# Decorator to add the metric to the metrics dictionary
def metric(func):
    metrics[func.__name__] = func
    return func


@metric
def mean_cosine_similarity(vectors):
    """
    Metric to compute the mean cosine similarity of the given vectors.

    For example used for the AnalogyTask.

    :param vectors: input vectors
    :return: mean cosine similarity
    """
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
    """
    Metric to compute the mean squared pairwise distance.
    It is equivalent to calculating the variance with n-1.

    For example used for the Neighborhood Task.

    :param vectors: input vectors
    :return: mean squared pairwise distance
    """
    matrix = np.array(vectors)
    return np.var(matrix, 0, ddof=1).sum() * 2


@metric
def mean_pairwise_distance(vectors):
    """
    Metric to compute the mean pairwise distance.

    For large input sizes use the mean_squared_pairwise_distance.

    For example used for the Neighborhood Task.

    :param vectors: input vectors
    :return: mean pairwise distance
    """
    matrix = np.array(vectors)
    euclidean_distances = pdist(matrix, 'euclidean')
    return np.nanmean(euclidean_distances)
