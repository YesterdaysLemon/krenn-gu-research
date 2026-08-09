"""Independent no-import audit of the mixed-word two-face localization."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations

TERMINALS = ("1", "2", "3", "4", "5", "a", "b")
FULL = (1 << len(TERMINALS)) - 1
Q = (1 << TERMINALS.index("a")) | (1 << TERMINALS.index("b"))
P_MINUS_Q = FULL ^ Q
Polynomial = dict[int, Fraction]


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply exact squarefree subset polynomials."""

    answer: Polynomial = {}
    for left_subset, left_value in left.items():
        for right_subset, right_value in right.items():
            if left_subset & right_subset:
                continue
            subset = left_subset | right_subset
            answer[subset] = answer.get(subset, Fraction(0)) + left_value * right_value
    return {subset: value for subset, value in answer.items() if value}


def wick_moment(
    edge_values: dict[tuple[int, int], Fraction],
) -> Polynomial:
    """Build all even principal hafnians by an independent recurrence."""

    @cache
    def hafnian(subset: int) -> Fraction:
        if subset == 0:
            return Fraction(1)
        if subset.bit_count() % 2:
            return Fraction(0)
        first = (subset & -subset).bit_length() - 1
        rest = subset ^ (1 << first)
        total = Fraction(0)
        remaining = rest
        while remaining:
            right_bit = remaining & -remaining
            right = right_bit.bit_length() - 1
            edge = tuple(sorted((first, right)))
            total += edge_values[edge] * hafnian(rest ^ right_bit)
            remaining ^= right_bit
        return total

    return {
        subset: hafnian(subset)
        for subset in range(1 << len(TERMINALS))
        if subset.bit_count() % 2 == 0
    }


def audit_face_partition() -> None:
    """Audit the 62 zero faces and two free faces."""

    counts: dict[int, int] = {}
    prescribed: set[int] = set()
    for size in (2, 4, 6):
        for deletion in combinations(range(len(TERMINALS)), size):
            mask = sum(1 << index for index in deletion)
            if mask == Q:
                continue
            prescribed.add(mask)
            surviving_degree = (FULL ^ mask).bit_count()
            counts[surviving_degree] = counts.get(surviving_degree, 0) + 1

    assert len(prescribed) == 62
    assert counts == {5: 20, 3: 35, 1: 7}
    assert Q not in prescribed and 0 not in prescribed


def audit_two_face_deconvolution() -> None:
    """Audit the localization over exact rational terminal weights."""

    edges: dict[tuple[int, int], Fraction] = {}
    for left, right in combinations(range(len(TERMINALS)), 2):
        edges[left, right] = Fraction((left + 2) * (right + 3) - 5, 7)
    negative_edges = {edge: -value for edge, value in edges.items()}

    forward = wick_moment(edges)
    backward = wick_moment(negative_edges)
    assert multiply(forward, backward) == {0: Fraction(1)}

    alpha, beta = Fraction(5, 11), Fraction(-7, 13)
    boundary = {P_MINUS_Q: alpha, FULL: beta}
    quotient = multiply(backward, boundary)
    a_index, b_index = TERMINALS.index("a"), TERMINALS.index("b")
    m_ab = edges[tuple(sorted((a_index, b_index)))]
    assert quotient == {
        P_MINUS_Q: alpha,
        FULL: beta - m_ab * alpha,
    }

    # No degree-one, degree-three, or other degree-five face survives.
    assert set(quotient) == {P_MINUS_Q, FULL}
    assert {subset.bit_count() for subset in quotient} == {5, 7}


def main() -> None:
    audit_face_partition()
    audit_two_face_deconvolution()
    print("PASS: independent tensor-coefficient Wick localization audit")
    print("prescribed mixed zero faces: 62")
    print("surviving no-terminal-edge mixed faces: 2")
    print("unique shear: beta -> beta-M_ab*alpha")
    print("support searches: 0")
    print("common seven-core realization: UNRESOLVED")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
