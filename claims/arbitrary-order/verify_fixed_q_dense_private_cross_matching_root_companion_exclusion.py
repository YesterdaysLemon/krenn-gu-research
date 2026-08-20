"""Exact replay for the GLD21 dense private-cross-matching exclusion."""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations

import sympy as sp


ROOTS = tuple(range(4))
Q0, Q1 = 4, 5
PORTS = tuple(range(6, 10))
VERTICES = ROOTS + (Q0, Q1) + PORTS
ACTIVE = (0, 1)
DEAD = 2


@lru_cache(maxsize=None)
def perfect_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output: list[tuple[tuple[int, int], ...]] = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            output.append(((first, second),) + tail)
    return tuple(output)


MATCHINGS = perfect_matchings(VERTICES)
assert len(MATCHINGS) == 945


class PrivateChart:
    def __init__(
        self,
        h: sp.Expr,
        tau: tuple[tuple[sp.Expr, ...], ...],
        root_root: dict[tuple[int, int, int, int], sp.Expr],
    ) -> None:
        self.h = h
        self.tau = tau
        self.root_root = root_root
        # Dense corrected shores: K(0,0)=2, K(1,1)=-2, dead shore zero.
        self.x = (sp.Integer(1), sp.Integer(1), sp.Integer(0))
        self.y = (sp.Integer(1), sp.Integer(-1), sp.Integer(0))
        self.p0: list[tuple[sp.Expr, ...]] = []
        self.p1: list[tuple[sp.Expr, ...]] = []
        for root in ROOTS:
            l0 = (-h * tau[root][0], sp.Integer(0), sp.Integer(0))
            l1 = (sp.Integer(0), -h * tau[root][1], sp.Integer(0))
            self.p0.append(tuple((l0[c] - l1[c]) / 2 for c in range(3)))
            self.p1.append(tuple((l0[c] + l1[c]) / 2 for c in range(3)))

    def k(self, colour: int) -> sp.Expr:
        return sp.expand(2 * self.x[colour] * self.y[colour])

    def edge_value(
        self,
        left: int,
        right: int,
        root_word: tuple[int, ...],
        port_word: tuple[int, ...],
    ) -> sp.Expr:
        if left > right:
            left, right = right, left

        if left in ROOTS and right in ROOTS:
            return self.root_root[(left, right, root_word[left], root_word[right])]

        if left in ROOTS and right in (Q0, Q1):
            values = self.p0 if right == Q0 else self.p1
            return values[left][root_word[left]]

        if left in ROOTS and right in PORTS:
            port = right - PORTS[0]
            if left != port or root_word[left] != port_word[port]:
                return sp.Integer(0)
            return self.tau[left][root_word[left]]

        if left == Q0 and right == Q1:
            return self.h

        if left in (Q0, Q1) and right in PORTS:
            port = right - PORTS[0]
            shore = self.x if left == Q0 else self.y
            return shore[port_word[port]]

        if left in PORTS and right in PORTS:
            return sp.Integer(0)

        raise AssertionError((left, right))

    def coefficient(
        self, root_word: tuple[int, ...], port_word: tuple[int, ...]
    ) -> sp.Expr:
        total = sp.Integer(0)
        for matching in MATCHINGS:
            term = sp.Integer(1)
            for left, right in matching:
                term *= self.edge_value(left, right, root_word, port_word)
                if term == 0:
                    break
            total += term
        return sp.expand(total)


def symbolic_chart() -> PrivateChart:
    h = sp.Symbol("h", nonzero=True)
    tau = tuple(
        tuple(sp.Symbol(f"t_{root}_{colour}", nonzero=True) for colour in range(3))
        for root in ROOTS
    )
    root_root: dict[tuple[int, int, int, int], sp.Expr] = {}
    for left, right in combinations(ROOTS, 2):
        for left_colour in range(3):
            for right_colour in range(3):
                root_root[(left, right, left_colour, right_colour)] = sp.Symbol(
                    f"w_{left}{right}_{left_colour}{right_colour}"
                )
    return PrivateChart(h, tau, root_root)


def rational_chart() -> PrivateChart:
    h = sp.Integer(7)
    tau = tuple(
        tuple(sp.Integer(2 + 3 * root + colour) for colour in range(3))
        for root in ROOTS
    )
    root_root: dict[tuple[int, int, int, int], sp.Expr] = {}
    for left, right in combinations(ROOTS, 2):
        for left_colour in range(3):
            for right_colour in range(3):
                root_root[(left, right, left_colour, right_colour)] = sp.Integer(
                    11 + 17 * left + 19 * right + 5 * left_colour + right_colour
                )
    return PrivateChart(h, tau, root_root)


def product_tau(chart: PrivateChart, word: tuple[int, ...]) -> sp.Expr:
    return sp.prod(chart.tau[index][colour] for index, colour in enumerate(word))


def check_symbolic_canonical_package() -> None:
    chart = symbolic_chart()
    edge = (0, 1)
    complement = (2, 3)
    repeated = 0
    other = 1

    all_dead = (DEAD,) * 4
    assert (
        sp.expand(
            chart.coefficient(all_dead, all_dead)
            - chart.h * product_tau(chart, all_dead)
        )
        == 0
    )

    for port in ROOTS:
        for colour in ACTIVE:
            word = [DEAD] * 4
            word[port] = colour
            word_tuple = tuple(word)
            assert chart.coefficient(word_tuple, word_tuple) == 0

    # Repeat the other active colour on edge 01, but flip both corresponding
    # roots to ``repeated``.  Zero/one-flip nuisance columns cannot reach it.
    opposite_port = (other, other, repeated, DEAD)
    double_flip_root = (repeated, repeated, repeated, DEAD)
    expected_double_flip = (
        chart.k(other)
        * chart.tau[complement[0]][repeated]
        * chart.tau[complement[1]][DEAD]
        * chart.root_root[(edge[0], edge[1], repeated, repeated)]
    )
    assert (
        sp.expand(
            chart.coefficient(double_flip_root, opposite_port) - expected_double_flip
        )
        == 0
    )

    matching_word = (repeated, repeated, other, DEAD)
    expected_matching = (
        -2 * chart.h * product_tau(chart, matching_word)
        + chart.k(repeated)
        * chart.tau[complement[0]][other]
        * chart.tau[complement[1]][DEAD]
        * chart.root_root[(edge[0], edge[1], repeated, repeated)]
    )
    assert (
        sp.expand(chart.coefficient(matching_word, matching_word) - expected_matching)
        == 0
    )

    killed = expected_matching.subs(
        chart.root_root[(edge[0], edge[1], repeated, repeated)], 0
    )
    assert sp.factor(killed) == -2 * chart.h * product_tau(chart, matching_word)


def oriented_words(
    edge: tuple[int, int], repeated: int, orientation: int
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, int]]:
    complement = tuple(index for index in ROOTS if index not in edge)
    if orientation:
        complement = (complement[1], complement[0])
    other = 1 - repeated
    port_word = [DEAD] * 4
    port_word[edge[0]] = repeated
    port_word[edge[1]] = repeated
    port_word[complement[0]] = other
    port_word[complement[1]] = DEAD
    return tuple(port_word), complement, edge


def check_full_orbit() -> None:
    chart = rational_chart()
    checked_double_flips = 0
    checked_mixed_detectors = 0

    for edge in combinations(ROOTS, 2):
        for repeated in ACTIVE:
            other = 1 - repeated
            for orientation in (0, 1):
                matching_word, complement, _ = oriented_words(
                    edge, repeated, orientation
                )

                # The package with the opposite repeated colour forces the
                # diagonal root-root entry used by the matching package.
                opposite_port = list(matching_word)
                opposite_port[edge[0]] = other
                opposite_port[edge[1]] = other
                opposite_port[complement[0]] = repeated
                opposite_port = tuple(opposite_port)
                double_flip_root = list(opposite_port)
                double_flip_root[edge[0]] = repeated
                double_flip_root[edge[1]] = repeated
                double_flip_root = tuple(double_flip_root)

                expected_double = (
                    chart.k(other)
                    * chart.tau[complement[0]][repeated]
                    * chart.tau[complement[1]][DEAD]
                    * chart.root_root[(edge[0], edge[1], repeated, repeated)]
                )
                assert (
                    chart.coefficient(double_flip_root, opposite_port)
                    == expected_double
                )
                assert expected_double != 0
                checked_double_flips += 1

                expected_matching = (
                    -2 * chart.h * product_tau(chart, matching_word)
                    + chart.k(repeated)
                    * chart.tau[complement[0]][other]
                    * chart.tau[complement[1]][DEAD]
                    * chart.root_root[(edge[0], edge[1], repeated, repeated)]
                )
                assert (
                    chart.coefficient(matching_word, matching_word) == expected_matching
                )

                # Apply the already-forced root-root diagonal vanishing.
                obstruction = -2 * chart.h * product_tau(chart, matching_word)
                assert obstruction != 0
                checked_mixed_detectors += 1

    assert checked_double_flips == 24
    assert checked_mixed_detectors == 24


def main() -> None:
    check_symbolic_canonical_package()
    check_full_orbit()
    print(
        "PASS: private matching gives 24 double-flip diagonal gates and "
        "24 nonzero -2hP dense mixed detectors"
    )


if __name__ == "__main__":
    main()
