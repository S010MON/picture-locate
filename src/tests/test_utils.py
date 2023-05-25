import time

import numpy as np
import scipy

from ..utils import recall_at_k


def distance_matrix_loop(x_1: np.ndarray, x_2: np.ndarray) -> np.ndarray:
    """
    A slow (but guarunteed correct) distance matrix generator to test that the lin alg
    solution is correct
    """
    D = np.zeros(shape=(len(x_1), len(x_2)))
    for i in range(len(x_1)):
        for j in range(len(x_2)):
            D[i, j] = np.square(np.linalg.norm(x_1[i] - x_2[j]))
    return D


def distance_matrix_vector(x_1: np.ndarray, x_2: np.ndarray) -> np.ndarray:
    """
    Source: https://samuelalbanie.com/files/Euclidean_distance_trick.pdf
    :param x_1: a matrix of embeddings (batch_size, dimensions)
    :param x_2: a matrix of embeddings (batch_size, dimensions)
    :return: a matrix of l2 distances (batch_size, batch_size)
    """
    D = np.sum((x_1[:, np.newaxis] - x_2) ** 2, axis=2)
    return D


def test_distance_matrix_benchmark():
    x = np.random.rand(3000, 256)
    y = np.random.rand(3000, 256)

    print("\nBenchmarking distance matrix ...")
    start = time.time()
    d_1 = distance_matrix_loop(x, y)
    print(f"\nloop: {time.time() - start}")

    start = time.time()
    d_2 = distance_matrix_vector(x, y)
    print(f"\nvector: {time.time() - start}")

    start = time.time()
    d_3 = np.square(scipy.spatial.distance.cdist(x, y))
    print(f"\nscipy: {time.time() - start}")

    assert np.allclose(d_1, d_2, atol=1e-3)
    assert np.allclose(d_1, d_3, atol=1e-3)
    assert np.allclose(d_2, d_3, atol=1e-3)


def test_recall_at_k_100():
    distances = np.array([[2.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 2.0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 2.0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 2.0, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 2.0, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 2.0, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 2.0, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 2.0, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 2.0, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 2.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0]])
    results = recall_at_k(distances)
    assert np.round(results[0]) == 100.0
    assert np.round(results[1]) == 100.0
    assert np.round(results[2]) == 100.0
    assert np.round(results[3]) == 100.0
    assert np.round(results[4]) == 100.0
    assert np.round(results[5]) == 100.0


def test_recall_at_k_50():
    distances = np.array([[0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.0, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.0, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 2.0, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 2.0, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 2.0, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 2.0, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 2.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 2.0]])
    results = recall_at_k(distances)
    assert np.round(results[0]) == 55.0
    assert np.round(results[1]) == 55.0
    assert np.round(results[2]) == 64.0
    assert np.round(results[3]) == 64.0
    assert np.round(results[4]) == 64.0
    assert np.round(results[5]) == 55.0


def test_recall_at_k_0():
    distances = np.array([[0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.0, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.0, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.0, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.0, 0.7, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.0, 0.8, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.0, 0.9, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.0, 1.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.0, 1.1],
                          [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.0]])
    results = recall_at_k(distances)
    assert np.round(results[0]) == 9.0
    assert np.round(results[1]) == 9.0
    assert np.round(results[2]) == 9.0
    assert np.round(results[3]) == 9.0
    assert np.round(results[4]) == 9.0
    assert np.round(results[5]) == 9.0
