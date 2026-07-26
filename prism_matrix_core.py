"""Six matrix identities hidden inside the 54-equation prism core."""

from __future__ import annotations

import itertools
from dataclasses import dataclass

import numpy as np

from search_witness import EquationSystem

Edge = tuple[int, int]


@dataclass(frozen=True)
class MatrixIdentity:
    edge: Edge
    scalar: complex
    outer_product: np.ndarray
    residual: np.ndarray


def prism_matrix_identities(
    system: EquationSystem, weights: np.ndarray
) -> tuple[MatrixIdentity, ...]:
    blocks = system.edge_array(weights)

    def block(edge: Edge) -> np.ndarray:
        return blocks[system.edge_index[edge]]

    x04 = block((0, 4))
    x05 = block((0, 5))
    x12 = block((1, 2))
    x13 = block((1, 3))
    x25 = block((2, 5))
    x34 = block((3, 4))

    data = (
        (
            (0, 4),
            1 + x13[2, 0] * x25[0, 2],
            x12[2, 0] * np.outer(x05[:, 2], x34[0, :]),
            x04,
        ),
        (
            (0, 5),
            1 + x12[1, 0] * x34[0, 1],
            x13[1, 0] * np.outer(x04[:, 1], x25[0, :]),
            x05,
        ),
        (
            (1, 2),
            1 + x05[2, 0] * x34[2, 0],
            x04[2, 0] * np.outer(x13[:, 2], x25[:, 0]),
            x12,
        ),
        (
            (1, 3),
            1 + x04[1, 0] * x25[1, 0],
            x05[1, 0] * np.outer(x12[:, 1], x34[:, 0]),
            x13,
        ),
        (
            (2, 5),
            1 + x04[2, 1] * x13[1, 2],
            x34[2, 1] * np.outer(x12[1, :], x05[2, :]),
            x25,
        ),
        (
            (3, 4),
            1 + x05[1, 2] * x12[2, 1],
            x25[1, 2] * np.outer(x13[2, :], x04[1, :]),
            x34,
        ),
    )
    return tuple(
        MatrixIdentity(edge, scalar, outer, scalar * matrix + outer)
        for edge, scalar, outer, matrix in data
    )


def all_two_by_two_minors(matrix: np.ndarray) -> np.ndarray:
    return np.array(
        [
            matrix[first_row, first_column]
            * matrix[second_row, second_column]
            - matrix[first_row, second_column]
            * matrix[second_row, first_column]
            for first_row in range(3)
            for second_row in range(first_row + 1, 3)
            for first_column in range(3)
            for second_column in range(first_column + 1, 3)
        ]
    )


def normalized_prism_automorphisms(
    system: EquationSystem, fixed: np.ndarray
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    blocks = system.edge_array(fixed)
    coloured_edges = {
        frozenset(((u, int(row)), (v, int(column))))
        for edge_index, (u, v) in enumerate(system.edges)
        for row, column in zip(*np.nonzero(blocks[edge_index]))
    }
    result = []
    for vertices in itertools.permutations(range(6)):
        for colours in itertools.permutations(range(3)):
            image = {
                frozenset(
                    (vertices[vertex], colours[colour])
                    for vertex, colour in edge
                )
                for edge in coloured_edges
            }
            if image == coloured_edges:
                result.append((vertices, colours))
    return tuple(result)
