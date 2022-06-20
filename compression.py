#!/usr/bin/env python3
"""Data compression with LVQ."""
import argparse
import math
import random
import typing
import numpy as np
import numba as nb  # type:ignore


class Argparser:  # pylint: disable=too-few-public-methods
    """Argparser class."""

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--n", "-n", type=int, help="vector count", default=1000
        )
        parser.add_argument(
            "--m", "-m", type=int, help="vector length", default=4
        )
        parser.add_argument(
            "--c", "-c", type=int, help="number of classes", default=4
        )
        parser.add_argument(
            "--v", "-v", type=int, help="number of codebook vectors", default=4
        )
        parser.add_argument("--alpha", "-a", type=float, help="learning rate")
        parser.add_argument("--epsilon", "-e", type=float, help="tolerance")
        parser.add_argument(
            "--maxiter",
            "-i",
            type=int,
            help="maximum number of iterations",
            default=100,
        )
        self.args = parser.parse_args()


@nb.jit(nopython=True, cache=True, parallel=True, fastmath=True)
def random_init(mat, m, n) -> None:
    """Initialize a matrix to random values."""
    for i in nb.prange(0, m):
        for j in nb.prange(0, n):
            mat[i, j] = random.uniform(0, 1)


@nb.jit(nopython=True, cache=True, parallel=True, fastmath=True)
def get_codebook_vectors(
    v, m: int
) -> np.ndarray[typing.Any, np.dtype[np.float32]]:
    """Generates a number of codebook vectors."""
    V: np.ndarray[typing.Any, np.dtype[np.float32]] = np.zeros(
        (m, v), dtype=np.float32
    )
    for j in nb.prange(0, m):
        for i in nb.prange(0, v):
            V[j, i] = random.uniform(0, 1)

    return V


@nb.jit(nopython=True, cache=True, parallel=True, fastmath=True)
def genrate_input_classes(n, c: int) -> typing.List[int]:
    """Our classification function."""
    class_list: typing.List[int] = [0] * n
    for i in nb.prange(0, n):
        class_list[i] = math.floor(random.uniform(0, c))

    return class_list


def classification_function(class_list: typing.List[int], i: int) -> int:
    """Returns the class of a input."""
    return class_list[i]


@nb.jit(nopython=True, cache=True, parallel=True, fastmath=True)
def get_distance(
    v1, v2: np.ndarray[typing.Any, np.dtype[np.float32]]
) -> float:
    """The distance function."""
    return sum(v1 - v2)


def get_calculated_class(
    v, V: np.ndarray[typing.Any, np.dtype[np.float32]]
) -> int:
    """Get the calculated calss."""
    distances: typing.List[float] = [0] * V.shape[1]
    for i in nb.prange(0, V.shape[1]):
        distances[i] = get_distance(v, V[None, i : i + 1])

    minimum = min(distances)
    minimum_index = distances.index(minimum)

    return minimum_index


def lvq(
    inputs,
    V: np.ndarray[typing.Any, np.dtype[np.float32]],
    i,
    n,
    c: int,
    class_list: typing.List[int],
    alpha: float,
):
    """LVQ."""
    for _ in nb.prange(0, i):
        for j in nb.prange(0, n):
            calc_class = get_calculated_class(inputs[None, j : j + 1], V)
            real_class = classification_function(class_list, j)
            if calc_class == real_class:
                V[None, real_class : real_class + 1] = V[
                    None, real_class : real_class + 1
                ] + alpha * (
                    inputs[None, j : j + 1],
                    V[None, real_class : real_class + 1],
                )
            else:
                V[None, real_class : real_class + 1] = V[
                    None, real_class : real_class + 1
                ] - alpha * (
                    inputs[None, j : j + 1],
                    V[None, real_class : real_class + 1],
                )


def main():
    """The entry point."""
    argparser = Argparser()
    inputs: np.ndarray = np.ndarray(
        (argparser.args.m, argparser.args.n), dtype=np.float32
    )
    random_init(inputs, argparser.args.m, argparser.args.n)
    print("inputs:\n", inputs)
    V = get_codebook_vectors(argparser.args.v, argparser.args.m)
    print("V:\n", V)
    class_list = genrate_input_classes(argparser.args.n, argparser.args.c)
    print("class_list:\n", class_list)


if __name__ == "__main__":
    main()
