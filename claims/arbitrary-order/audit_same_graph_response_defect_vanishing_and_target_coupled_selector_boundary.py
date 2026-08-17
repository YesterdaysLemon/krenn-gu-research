"""Independent no-import audit of the response-defect/selector boundary.

This file imports neither SymPy nor the primary verifier.  It uses exact
Fractions, bitmask matching sums, and a separate matrix implementation.
"""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations

Q = Fraction


def matching_sum(mask: int, weights: dict[tuple[int, int], Q]) -> Q:
    @cache
    def recurse(active: int) -> Q:
        if active == 0:
            return Q(1)
        if active.bit_count() % 2:
            return Q(0)
        first_bit = active & -active
        first = first_bit.bit_length() - 1
        rest = active ^ first_bit
        total = Q(0)
        cursor = rest
        while cursor:
            partner_bit = cursor & -cursor
            partner = partner_bit.bit_length() - 1
            total += weights.get(tuple(sorted((first, partner))), Q(0)) * recurse(
                rest ^ partner_bit
            )
            cursor ^= partner_bit
        return total

    return recurse(mask)


def subset_mask(subset: tuple[int, ...]) -> int:
    return sum(1 << vertex for vertex in subset)


def audit_insertion_identity() -> None:
    ports = 6
    q0, q1 = ports, ports + 1
    port_weights = {
        (i, j): Q((i + 2) * (j + 3) - 5) for i, j in combinations(range(ports), 2)
    }
    full_weights = dict(port_weights)
    full_weights[(q0, q1)] = Q(5)
    for port in range(ports):
        full_weights[(port, q0)] = Q(3 * port + 1)
        full_weights[(port, q1)] = Q(2 - port)

    moments: dict[tuple[int, ...], Q] = {}
    responses: dict[tuple[int, ...], Q] = {}
    for size in range(0, ports + 1, 2):
        for subset in combinations(range(ports), size):
            moments[subset] = matching_sum(subset_mask(subset), port_weights)
            responses[subset] = matching_sum(
                subset_mask((*subset, q0, q1)), full_weights
            )

    h = responses[()]
    assert h == 5
    for subset, response in responses.items():
        pointed = Q(0)
        for edge in combinations(subset, 2):
            complement = tuple(vertex for vertex in subset if vertex not in edge)
            pointed += responses[edge] * moments[complement]
        defect = response - pointed + Q(len(subset) // 2 - 1) * h * moments[subset]
        assert defect == 0


def outer(left: tuple[Q, ...], right: tuple[Q, ...]) -> tuple[tuple[Q, ...], ...]:
    return tuple(tuple(x * y for y in right) for x in left)


def add_matrix(*matrices: tuple[tuple[Q, ...], ...]) -> tuple[tuple[Q, ...], ...]:
    return tuple(
        tuple(
            sum(matrix[i][j] for matrix in matrices) for j in range(len(matrices[0][0]))
        )
        for i in range(len(matrices[0]))
    )


def audit_top_control() -> None:
    identity = tuple(tuple(Q(i == j) for j in range(3)) for i in range(3))
    e01 = tuple(tuple(Q(i == 0 and j == 1) for j in range(3)) for i in range(3))
    direct = add_matrix(identity, e01)
    corrected = outer((Q(1), Q(0), Q(0)), (Q(0), Q(-1), Q(0)))
    top = add_matrix(direct, corrected)
    assert corrected[0][1] == -1
    assert top == identity


def audit_selector_identity() -> None:
    samples = [
        (Q(2), Q(3), Q(5), Q(7), Q(11)),
        (Q(-4), Q(5, 2), Q(3, 7), Q(-9), Q(2, 3)),
    ]
    for omega, h, u, corrected, nuisance in samples:
        top = h * u + corrected
        selected = omega * u + nuisance
        assert omega * corrected == omega * top - h * selected + h * nuisance
        selected_clean = omega * u
        mixed_target_value = -omega * corrected / h
        assert mixed_target_value == (omega * Q(0) - omega * corrected) / h
        assert selected_clean - omega * u == 0


def audit_augmented_parity() -> None:
    for r in range(1, 8):
        q0, q1 = r, r + 1
        weights: dict[tuple[int, int], Q] = {}
        for i, j in combinations(range(r), 2):
            weights[(i, j)] = Q((i + 1) * (j + 1))
        for root in range(r):
            weights[(root, q0)] = Q(root + 2)
            weights[(root, q1)] = Q(3 - root)
        general = matching_sum((1 << (r + 2)) - 1, weights)
        if r % 2:
            assert general == 0

        base_weights = {
            edge: value for edge, value in weights.items() if q0 in edge or q1 in edge
        }
        base = matching_sum((1 << (r + 2)) - 1, base_weights)
        if r == 2:
            assert base != 0
        else:
            assert base == 0


def matmul(left, right):
    columns = tuple(zip(*right, strict=True))
    return tuple(
        tuple(
            sum(x * y for x, y in zip(row, column, strict=True)) for column in columns
        )
        for row in left
    )


def inv2(matrix):
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    return (
        (matrix[1][1] / determinant, -matrix[0][1] / determinant),
        (-matrix[1][0] / determinant, matrix[0][0] / determinant),
    )


def audit_coboundary() -> None:
    identity = ((Q(1), Q(0)), (Q(0), Q(1)))
    gauges = (
        identity,
        ((Q(2), Q(0)), (Q(0), Q(1, 2))),
        ((Q(0), Q(1)), (Q(1), Q(0))),
    )
    transitions = tuple(matmul(inv2(gauges[(i + 1) % 3]), gauges[i]) for i in range(3))
    holonomy = matmul(transitions[2], matmul(transitions[1], transitions[0]))
    assert holonomy == identity


def main() -> None:
    audit_insertion_identity()
    audit_top_control()
    audit_selector_identity()
    audit_augmented_parity()
    audit_coboundary()
    print("independent same-graph response-defect/selector audit: PASS")


if __name__ == "__main__":
    main()
