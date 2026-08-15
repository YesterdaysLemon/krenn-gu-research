"""Primary exact checks for the fixed-pair distinct-two-low reduction."""

from __future__ import annotations

import json
from dataclasses import dataclass
from itertools import permutations, product

import sympy as sp

Vector = tuple[sp.Expr, ...]
MatrixRows = tuple[tuple[int, ...], tuple[int, ...]]
CHANNELS = ("m1", "m2", "d0", "d1", "d2")


@dataclass(frozen=True)
class Occurrence:
    """A noncommon exceptional line with one allowed local support."""

    family: int
    line: str
    missing: int
    support: frozenset[int]
    vector: Vector


def add(*vectors: Vector) -> Vector:
    """Add vectors coordinatewise."""
    return tuple(sp.expand(sum(vector[i] for vector in vectors)) for i in range(6))


def scale(value: sp.Expr, vector: Vector) -> Vector:
    """Scale a vector."""
    return tuple(sp.expand(value * entry) for entry in vector)


def evaluate(covector: Vector, vector: Vector) -> sp.Expr:
    """Evaluate a coordinate covector."""
    return sp.expand(sum(x * y for x, y in zip(covector, vector, strict=True)))


def polarized_product(factors: tuple[Vector, ...], vectors: tuple[Vector, ...]) -> sp.Expr:
    """Evaluate the complete polarization of four linear factors."""
    return sp.expand(
        sum(
            sp.prod(
                evaluate(factors[row], vectors[column])
                for row, column in enumerate(order)
            )
            for order in permutations(range(4))
        )
    )


def coordinate_vectors() -> tuple[Vector, ...]:
    """Return the six coordinate vectors."""
    return tuple(tuple(sp.Integer(i == j) for i in range(6)) for j in range(6))


def fixed_quartics() -> dict[str, tuple[sp.Expr, tuple[Vector, ...]]]:
    """Return the five factorized complementary quartics."""
    x0, x1, x2, x3, x4, x5 = coordinate_vectors()
    return {
        "m1": (sp.Integer(1), (x4, x5, x1, add(x3, scale(-1, x2), scale(-1, x0)))),
        "m2": (sp.Integer(1), (x4, x5, x0, add(x3, scale(-1, x2), scale(-1, x1)))),
        "d0": (sp.Integer(1), (x4, x5, add(x1, x2), add(x3, scale(-1, x0)))),
        "d1": (sp.Integer(1), (x4, x5, add(x0, x2), add(x3, scale(-1, x1)))),
        "d2": (sp.Integer(-2), (x4, x5, x0, x1)),
    }


def double_contractions(left: Vector, right: Vector) -> dict[str, sp.Expr]:
    """Contract two R-vectors and extract the remaining x4*x5 scalar."""
    e4, e5 = coordinate_vectors()[4:]
    return {
        name: sp.expand(coefficient * polarized_product(factors, (left, right, e4, e5)))
        for name, (coefficient, factors) in fixed_quartics().items()
    }


def nonempty_subsets(values: frozenset[int]) -> tuple[frozenset[int], ...]:
    """Return the three nonempty subsets of a two-element set."""
    left, right = sorted(values)
    return (frozenset({left}), frozenset({right}), values)


def occurrences(family: int) -> tuple[Occurrence, ...]:
    """Return all noncommon exceptional-line/support occurrences."""
    if family == 1:
        raw = (
            ("A0", 0, frozenset({1, 2}), (1, 0, 0, 1, 0, 0)),
            ("C0", 1, frozenset({0, 2}), (1, 0, -1, 0, 0, 0)),
        )
    else:
        raw = (
            ("A1", 1, frozenset({0, 2}), (0, 1, 0, 1, 0, 0)),
            ("C1", 0, frozenset({1, 2}), (0, 1, -1, 0, 0, 0)),
        )
    return tuple(
        Occurrence(
            family=family,
            line=line,
            missing=missing,
            support=support,
            vector=tuple(sp.Integer(entry) for entry in vector),
        )
        for line, missing, maximal, vector in raw
        for support in nonempty_subsets(maximal)
    )


def classify_pair(left: Occurrence, right: Occurrence) -> str | None:
    """Solve the exact matrix equations for one pair of low occurrences."""
    row = double_contractions(left.vector, right.vector)
    overlap = left.support & right.support
    if row["m1"] != 0 or row["m2"] != 0:
        return "Z" if not overlap else None
    nonzero_diagonals = {c for c in range(3) if row[f"d{c}"] != 0}
    if not overlap:
        return "Z"
    if len(overlap) == 1 and nonzero_diagonals == set(overlap):
        return f"E{next(iter(overlap))}"
    return None


def check_symbolic_double_contractions() -> dict[str, dict[str, int]]:
    """Check the six noncommon line-pair channel patterns in the theorem."""
    representatives = {
        occurrence.line: occurrence
        for family in (1, 2)
        for occurrence in occurrences(family)
    }
    pairs = (
        ("A0", "A0"),
        ("A0", "C0"),
        ("C0", "C0"),
        ("A1", "A1"),
        ("A1", "C1"),
        ("C1", "C1"),
        ("A0", "C1"),
        ("C0", "A1"),
        ("A0", "A1"),
        ("C0", "C1"),
    )
    summary: dict[str, dict[str, int]] = {}
    for left_name, right_name in pairs:
        row = double_contractions(
            representatives[left_name].vector,
            representatives[right_name].vector,
        )
        summary[f"{left_name}/{right_name}"] = {
            channel: int(value) for channel, value in row.items() if value != 0
        }

    assert summary["A0/A0"]["m2"] != 0
    assert summary["A0/C0"]["m2"] != 0
    assert summary["C0/C0"]["m2"] != 0
    assert summary["A1/A1"]["m1"] != 0
    assert summary["A1/C1"]["m1"] != 0
    assert summary["C1/C1"]["m1"] != 0
    assert set(summary["A0/C1"]) == {"d1", "d2"}
    assert set(summary["C0/A1"]) == {"d0", "d2"}
    assert set(summary["A0/A1"]) == {"d2"}
    assert set(summary["C0/C1"]) == {"d2"}
    return summary


def check_pair_classification() -> dict[str, object]:
    """Exhaust all noncommon line/support pairs."""
    first = occurrences(1)
    second = occurrences(2)

    same_checked = 0
    same_compatible = 0
    for family_occurrences in (first, second):
        for left in family_occurrences:
            for right in family_occurrences:
                same_checked += 1
                outcome = classify_pair(left, right)
                expected = "Z" if not (left.support & right.support) else None
                assert outcome == expected
                same_compatible += outcome is not None

    cross_compatible: list[tuple[str, str, tuple[int, ...], tuple[int, ...], str]] = []
    for left in first:
        for right in second:
            outcome = classify_pair(left, right)
            overlap = left.support & right.support
            if left.missing == right.missing:
                expected = (
                    "Z"
                    if not overlap and len(left.support) == len(right.support) == 1
                    else None
                )
            elif 2 in overlap:
                expected = "E2"
            else:
                expected = "Z"
                assert not overlap
            assert outcome == expected
            if outcome is not None:
                cross_compatible.append(
                    (
                        left.line,
                        right.line,
                        tuple(sorted(left.support)),
                        tuple(sorted(right.support)),
                        outcome,
                    )
                )

    assert len(cross_compatible) == 22
    assert sum(item[-1] == "E2" for item in cross_compatible) == 8
    return {
        "same_family_pairs_checked": same_checked,
        "same_family_compatible": same_compatible,
        "cross_family_compatible": len(cross_compatible),
        "cross_family_E22": sum(item[-1] == "E2" for item in cross_compatible),
    }


def check_three_low_combinatorics() -> dict[str, int]:
    """Check that a compatible 2+1 low diagram has at most one E22 edge."""
    counts: dict[str, int] = {}
    for majority_family in (1, 2):
        majority = occurrences(majority_family)
        minority = occurrences(3 - majority_family)
        compatible = 0
        live_edges = 0
        for index, left in enumerate(majority):
            for right in majority[index:]:
                if classify_pair(left, right) != "Z":
                    continue
                for third in minority:
                    outcomes = (
                        classify_pair(left, third),
                        classify_pair(right, third),
                    )
                    if None in outcomes:
                        continue
                    compatible += 1
                    number_live = sum(outcome == "E2" for outcome in outcomes)
                    assert number_live <= 1
                    live_edges += number_live
        assert compatible == 14
        counts[f"majority_Phi_{majority_family}_compatible"] = compatible
        counts[f"majority_Phi_{majority_family}_live_edges"] = live_edges

    # Each of two slices may have at most one exceptional line shore.  Two
    # singleton exception sets cannot cover all three line shores.
    exception_choices = (frozenset(), frozenset({0}), frozenset({1}), frozenset({2}))
    assert all(first | second != {0, 1, 2} for first in exception_choices for second in exception_choices)
    counts["two_slice_exception_patterns"] = len(exception_choices) ** 2
    return counts


def rank_mod(matrix: MatrixRows, prime: int) -> int:
    """Compute a two-row matrix rank modulo an odd prime."""
    work = [[value % prime for value in row] for row in matrix]
    row = 0
    for column in range(3):
        pivot = next((i for i in range(row, 2) if work[i][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column], prime - 2, prime)
        work[row] = [(inverse * value) % prime for value in work[row]]
        for i in range(2):
            if i == row:
                continue
            factor = work[i][column]
            work[i] = [
                (value - factor * pivot_value) % prime
                for value, pivot_value in zip(work[i], work[row], strict=True)
            ]
        row += 1
        if row == 2:
            break
    return row


def pairing_matrix(left: MatrixRows, right: MatrixRows, prime: int) -> tuple[tuple[int, ...], ...]:
    """Return left^T J right over a finite field."""
    return tuple(
        tuple(
            (left[0][i] * right[1][j] + left[1][i] * right[0][j]) % prime
            for j in range(3)
        )
        for i in range(3)
    )


def check_rank_boundaries_over_f3() -> dict[str, int]:
    """Exhaust the zero and E22 high-shore rank consequences over F3."""
    prime = 3
    maps: tuple[MatrixRows, ...] = tuple(
        (entries[:3], entries[3:]) for entries in product(range(prime), repeat=6)
    )
    ranks = {matrix: rank_mod(matrix, prime) for matrix in maps}
    zero_pairs = 0
    e22_pairs = 0
    for left in maps:
        rank_left = ranks[left]
        if rank_left == 0:
            continue
        for right in maps:
            rank_right = ranks[right]
            if rank_right == 0:
                continue
            matrix = pairing_matrix(left, right, prime)
            if all(value == 0 for row in matrix for value in row):
                assert (rank_left, rank_right) == (1, 1)
                zero_pairs += 1
                continue
            if all(
                matrix[i][j] == 0
                for i in range(3)
                for j in range(3)
                if (i, j) != (2, 2)
            ):
                assert matrix[2][2] != 0
                assert (rank_left, rank_right) in {(1, 1), (1, 2), (2, 1)}
                if rank_left == 1:
                    assert left[0][:2] == left[1][:2] == (0, 0)
                if rank_right == 1:
                    assert right[0][:2] == right[1][:2] == (0, 0)
                e22_pairs += 1
    assert zero_pairs > 0 and e22_pairs > 0
    return {"zero_pairs": zero_pairs, "E22_pairs": e22_pairs}


def matrix_from_columns(columns: tuple[tuple[int, ...], ...]) -> sp.Matrix:
    """Build a matrix from integer columns."""
    return sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))


ZERO_FIXTURE = (
    ((0, 1, 0, 0, 0, 1), (1, 0, 0, 1, 0, 0), (0, 0, 0, 1, 0, 1)),
    ((0, 1, 0, 1, 0, 0), (1, 0, 0, 0, 0, 1), (0, 0, 0, 1, 0, 1)),
    ((1, 0, 0, -1, 0, 0), (0, 1, 0, 0, 1, 0), (0, 0, 0, 1, 1, 0)),
    ((1, 0, 0, 0, 1, 0), (0, 1, 0, -1, 0, 0), (0, 0, 0, 1, 1, 0)),
)

E22_FIXTURE = (
    ((2, 1, 0, 2, 1, 0), (2, 1, 1, -2, 0, 1), (1, 0, 0, 1, 0, 0)),
    ((-2, 0, 0, 0, 0, 1), (-1, 0, -1, 2, 1, 0), (0, 1, 0, 1, 0, 0)),
    ((1, 0, 0, -1, 0, 0), (0, 1, 0, -1, 0, 0), (-1, 1, -2, 2, 1, 0)),
    ((1, 0, 0, 0, 1, 0), (0, 2, 0, -2, 1, 0), (-1, -2, 1, 0, 0, 1)),
)


def check_fixture(
    columns_by_mode: tuple[tuple[tuple[int, ...], ...], ...],
    expected_a_ranks: tuple[int, ...],
    expected_c01_ranks: tuple[int, ...],
    expected_pairing: sp.Matrix,
    companions_in_one_mode: bool,
) -> dict[str, object]:
    """Replay one exact rational incidence-only fixture."""
    modes = tuple(matrix_from_columns(columns) for columns in columns_by_mode)
    phi_1 = sp.Matrix(
        ((0, 1, 0, 0, 0, 0), (0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 0, 1), (-1, 0, -1, 1, 0, 0))
    )
    phi_2 = sp.Matrix(
        ((1, 0, 0, 0, 0, 0), (0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 0, 1), (0, -1, -1, 1, 0, 0))
    )
    projection_ranks = tuple(((phi_1 * mode).rank(), (phi_2 * mode).rank()) for mode in modes)
    assert projection_ranks == ((2, 3), (3, 2), (3, 3), (3, 3))
    assert all(mode.rank() == 3 for mode in modes)

    kernel_1 = (phi_1 * modes[0]).nullspace()
    kernel_2 = (phi_2 * modes[1]).nullspace()
    if companions_in_one_mode:
        assert kernel_1 == [sp.Matrix((0, 0, 1))]
        assert kernel_2 == [sp.Matrix((0, 0, 1))]
        assert modes[2][:, 0] == sp.Matrix((1, 0, 0, -1, 0, 0))
        assert modes[2][:, 1] == sp.Matrix((0, 1, 0, -1, 0, 0))
    else:
        assert kernel_1 == [sp.Matrix((0, 1, 0))]
        assert kernel_2 == [sp.Matrix((1, 0, 0))]
        assert modes[2][:, 0] == sp.Matrix((1, 0, 0, -1, 0, 0))
        assert modes[3][:, 1] == sp.Matrix((0, 1, 0, -1, 0, 0))

    a_maps = tuple(mode[4:6, :] for mode in modes)
    assert tuple(matrix.rank() for matrix in a_maps) == expected_a_ranks
    assert tuple(matrix[:, :2].rank() for matrix in a_maps) == expected_c01_ranks
    j_form = sp.Matrix(((0, 1), (1, 0)))
    assert a_maps[2].T * j_form * a_maps[3] == expected_pairing

    for colour in range(3):
        assert any(
            (a_maps[left][:, colour].T * j_form * a_maps[right][:, colour])[0] != 0
            for left in range(4)
            for right in range(left + 1, 4)
        )

    coefficient, factors = fixed_quartics()["m1"]
    mixed_0000 = coefficient * polarized_product(
        factors, tuple(mode[:, 0] for mode in modes)
    )
    assert mixed_0000 == -2
    return {
        "projection_ranks": projection_ranks,
        "A_ranks": expected_a_ranks,
        "colour_01_A_ranks": expected_c01_ranks,
        "mixed_m1_0000": int(mixed_0000),
    }


def check_fixtures() -> dict[str, object]:
    """Check the zero and E22 incidence-only witnesses."""
    return {
        "zero": check_fixture(
            ZERO_FIXTURE,
            (1, 1, 1, 1),
            (1, 1, 1, 1),
            sp.zeros(3),
            companions_in_one_mode=False,
        ),
        "E22": check_fixture(
            E22_FIXTURE,
            (2, 2, 1, 2),
            (2, 2, 0, 1),
            sp.diag(0, 0, 1),
            companions_in_one_mode=True,
        ),
    }


def main() -> None:
    """Run all primary exact checks."""
    report = {
        "double_contractions": check_symbolic_double_contractions(),
        "pair_classification": check_pair_classification(),
        "three_low_combinatorics": check_three_low_combinatorics(),
        "finite_field_rank_boundaries": check_rank_boundaries_over_f3(),
        "incidence_only_fixtures": check_fixtures(),
        "status": "UNRESOLVED",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
