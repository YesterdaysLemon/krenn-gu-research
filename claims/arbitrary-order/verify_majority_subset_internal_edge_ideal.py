"""Primary checks for the majority-subset internal-edge ideal hierarchy."""

from __future__ import annotations

from itertools import product

import sympy as sp


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second),) + matching


def check_count_identity():
    a, b, d, m, r = sp.symbols("a b d m r")
    left_count = sp.Eq(2 * a + b, m + r)
    right_count = sp.Eq(2 * d + b, m - r)
    difference = sp.expand(
        (left_count.lhs - left_count.rhs) - (right_count.lhs - right_count.rhs)
    )
    assert sp.expand(difference - 2 * (a - d - r)) == 0


def contracted_coefficient(
    vertex_count, colour_count, subset, colouring, complement_colour
):
    marker = sp.Symbol("z")
    total = 0
    for matching in perfect_matchings(range(vertex_count)):
        term = 1
        for i, j in matching:
            if i in subset and j in subset:
                left_colour = colouring[i]
                right_colour = colouring[j]
                term *= marker * sp.Symbol(f"w{i}{j}_{left_colour}{right_colour}")
            elif i not in subset and j not in subset:
                term *= sp.Symbol(f"w{i}{j}_{complement_colour}{complement_colour}")
            else:
                inside = i if i in subset else j
                outside = j if i in subset else i
                left_colour = colouring[inside]
                if inside < outside:
                    term *= sp.Symbol(
                        f"w{inside}{outside}_{left_colour}{complement_colour}"
                    )
                else:
                    term *= sp.Symbol(
                        f"w{outside}{inside}_{complement_colour}{left_colour}"
                    )
        total += term
    return sp.Poly(sp.expand(total), marker)


def check_generic_six_vertex_divisibility():
    vertex_count = 6
    m = vertex_count // 2
    colour_count = 2
    for r in (1, 2):
        subset = frozenset(range(m + r))
        for colours in product(range(colour_count), repeat=len(subset)):
            colouring = dict(zip(sorted(subset), colours))
            polynomial = contracted_coefficient(
                vertex_count,
                colour_count,
                subset,
                colouring,
                complement_colour=0,
            )
            assert min(exponent[0] for exponent, _ in polynomial.terms()) >= r


if __name__ == "__main__":
    check_count_identity()
    check_generic_six_vertex_divisibility()
    print("majority-subset internal-edge ideal primary verifier: PASS")
