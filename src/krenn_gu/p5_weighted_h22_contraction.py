"""Exact four-source weighted-H22 contraction infrastructure for P5.

This module implements only the four-source, eight-extension, four-bit
``D01``/``D23`` model used by the P5 weighted-H22 claim families.  It is a
shared implementation dependency, not a mathematical premise and not an
arbitrary-order contraction interface.
"""

from __future__ import annotations

import itertools

import sympy as sp

__all__ = ("WORDS", "permanent4", "project", "build_model")


WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))


def permanent3(rows):
    return sp.expand(sum(
        sp.prod(rows[i][permutation[i]] for i in range(3))
        for permutation in PERMUTATIONS3
    ))


def permanent4(rows):
    return sp.expand(sum(
        sp.prod(rows[i][permutation[i]] for i in range(4))
        for permutation in PERMUTATIONS4
    ))


def project(row, extension, direction, chart, slope=None):
    if chart == "finite" and direction == "D01":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if chart == "finite" and direction == "D23":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if chart == "infinity" and direction == "D01":
        return (row[0], row[2], row[3], extension)
    if chart == "infinity" and direction == "D23":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def build_model(alpha, beta, extensions, direction, chart, slope=None):
    alpha_rows = tuple(
        project(alpha[i], extensions[i], direction, chart, slope) for i in range(4)
    )
    beta_rows = tuple(
        project(beta[i], extensions[4 + i], direction, chart, slope)
        for i in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(
            beta_rows[i] if word[i] else alpha_rows[i] for i in range(4)
        )
        coefficients[word] = sp.expand(sum(
            selected[i][3]
            * permanent3(tuple(selected[j][:3] for j in range(4) if j != i))
            for i in range(4)
        ))
    return {
        "coefficients": coefficients,
        "mixed": tuple(coefficients[word] for word in MIXED),
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }
