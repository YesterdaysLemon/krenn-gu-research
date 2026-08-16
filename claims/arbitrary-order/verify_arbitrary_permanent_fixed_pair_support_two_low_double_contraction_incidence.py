"""Primary exact checks for the support-two low incidence theorem."""

from __future__ import annotations

import json
from itertools import combinations_with_replacement, permutations, product

import sympy as sp

Vector = tuple[sp.Expr, ...]
CHANNELS = ("m1", "m2", "d0", "d1", "d2")


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
    return sp.expand(sum(
        sp.prod(evaluate(factors[row], vectors[column]) for row, column in enumerate(order))
        for order in permutations(range(4))
    ))


def fixed_quartics() -> dict[str, tuple[sp.Expr, tuple[Vector, ...]]]:
    """Return the five factorized complementary quartics."""
    coordinates = tuple(
        tuple(sp.Integer(i == j) for i in range(6))
        for j in range(6)
    )
    x0, x1, x2, x3, x4, x5 = coordinates
    return {
        "m1": (sp.Integer(1), (x4, x5, x1, add(x3, scale(-1, x2), scale(-1, x0)))),
        "m2": (sp.Integer(1), (x4, x5, x0, add(x3, scale(-1, x2), scale(-1, x1)))),
        "d0": (sp.Integer(1), (x4, x5, add(x1, x2), add(x3, scale(-1, x0)))),
        "d1": (sp.Integer(1), (x4, x5, add(x0, x2), add(x3, scale(-1, x1)))),
        "d2": (sp.Integer(-2), (x4, x5, x0, x1)),
    }


def double_contractions(left: Vector, right: Vector) -> dict[str, sp.Expr]:
    """Contract two R-vectors and extract the remaining x4*x5 scalar."""
    e4 = tuple(sp.Integer(i == 4) for i in range(6))
    e5 = tuple(sp.Integer(i == 5) for i in range(6))
    return {
        name: sp.expand(coefficient * polarized_product(factors, (left, right, e4, e5)))
        for name, (coefficient, factors) in fixed_quartics().items()
    }


def check_symbolic_tables() -> dict[str, object]:
    """Derive all three displayed double-contraction rows symbolically."""
    a, b, c, d, aa, bb, cc, dd = sp.symbols("a b c d A B C D")
    p1 = (a, 0, b, a + b, 0, 0)
    q1 = (aa, 0, bb, aa + bb, 0, 0)
    p2 = (0, c, d, c + d, 0, 0)
    q2 = (0, cc, dd, cc + dd, 0, 0)
    actual = {
        "cross": double_contractions(p1, p2),
        "Phi_1": double_contractions(p1, q1),
        "Phi_2": double_contractions(p2, q2),
    }
    expected = {
        "cross": {
            "m1": 0,
            "m2": 0,
            "d0": 2 * b * (c + d),
            "d1": 2 * d * (a + b),
            "d2": -2 * a * c,
        },
        "Phi_1": {
            "m1": 0,
            "m2": 2 * a * aa,
            "d0": 2 * b * bb,
            "d1": 2 * (a + b) * (aa + bb),
            "d2": 0,
        },
        "Phi_2": {
            "m1": 2 * c * cc,
            "m2": 0,
            "d0": 2 * (c + d) * (cc + dd),
            "d1": 2 * d * dd,
            "d2": 0,
        },
    }
    for family in actual:
        for channel in CHANNELS:
            assert sp.expand(actual[family][channel] - expected[family][channel]) == 0
    return {
        family: {channel: str(sp.factor(value)) for channel, value in row.items()}
        for family, row in actual.items()
    }


def exceptional_lines(family: int) -> dict[str, dict[str, object]]:
    """Return normalized exceptional vectors, missed colours, and supports."""
    if family == 1:
        return {
            "N": {"vector": (0, 0, 1, 1, 0, 0), "missing": 2, "support": {0, 1}},
            "A0": {"vector": (1, 0, 0, 1, 0, 0), "missing": 0, "support": {1, 2}},
            "C0": {"vector": (1, 0, -1, 0, 0, 0), "missing": 1, "support": {0, 2}},
        }
    return {
        "N": {"vector": (0, 0, 1, 1, 0, 0), "missing": 2, "support": {0, 1}},
        "A1": {"vector": (0, 1, 0, 1, 0, 0), "missing": 1, "support": {0, 2}},
        "C1": {"vector": (0, 1, -1, 0, 0, 0), "missing": 0, "support": {1, 2}},
    }


def nonzero_diagonals(row: dict[str, sp.Expr]) -> set[int]:
    """Return diagonal channel indices having nonzero scalar."""
    return {colour for colour in range(3) if row[f"d{colour}"] != 0}


def check_cross_family_cases() -> dict[str, object]:
    """Exhaust the nine cross-family exceptional-line pairs."""
    first = exceptional_lines(1)
    second = exceptional_lines(2)
    excluded: list[str] = []
    surviving: list[dict[str, object]] = []
    for name1, data1 in first.items():
        for name2, data2 in second.items():
            row = double_contractions(data1["vector"], data2["vector"])
            assert row["m1"] == row["m2"] == 0
            overlap = data1["support"] & data2["support"]
            diagonal = nonzero_diagonals(row)
            if data1["missing"] == data2["missing"]:
                assert len(overlap) == 2
                assert diagonal == overlap
                excluded.append(f"{name1}/{name2}")
            else:
                assert len(overlap) == 1
                assert diagonal == overlap
                colour = next(iter(overlap))
                surviving.append({
                    "lines": f"{name1}/{name2}",
                    "common_colour": colour,
                    "channel": f"d{colour}",
                    "scalar": int(row[f"d{colour}"]),
                })
    assert excluded == ["N/N", "A0/C1", "C0/A1"]
    assert len(surviving) == 6
    return {"excluded_same_missing": excluded, "surviving": surviving}


def check_same_family_cases() -> dict[str, object]:
    """Exhaust same-family pairs and the at-most-two combinatorics."""
    summary: dict[str, object] = {}
    for family in (1, 2):
        lines = exceptional_lines(family)
        allowed: list[dict[str, object]] = []
        forbidden: list[str] = []
        for name1, name2 in combinations_with_replacement(lines, 2):
            data1, data2 = lines[name1], lines[name2]
            row = double_contractions(data1["vector"], data2["vector"])
            if name1 != "N" and name2 != "N":
                assert 2 in data1["support"] & data2["support"]
                assert row["d2"] == 0
                forbidden.append(f"{name1}/{name2}")
            elif name1 == name2 == "N":
                assert nonzero_diagonals(row) == {0, 1}
                forbidden.append("N/N")
            else:
                overlap = data1["support"] & data2["support"]
                assert len(overlap) == 1
                assert nonzero_diagonals(row) == overlap
                colour = next(iter(overlap))
                allowed.append({
                    "lines": f"{name1}/{name2}",
                    "common_colour": colour,
                    "channel": f"d{colour}",
                })

        names = tuple(lines)
        valid_triples = []
        for triple in product(names, repeat=3):
            if all(
                (triple[i] == "N") != (triple[j] == "N")
                for i, j in ((0, 1), (0, 2), (1, 2))
            ):
                valid_triples.append(triple)
        assert not valid_triples
        assert len(allowed) == 2
        summary[f"Phi_{family}"] = {
            "allowed": allowed,
            "forbidden": forbidden,
            "valid_three_mode_type_assignments": 0,
        }
    return summary


def rank_mod(matrix: tuple[tuple[int, ...], ...], prime: int) -> int:
    """Compute a small matrix rank modulo a prime."""
    if not matrix:
        return 0
    work = [[value % prime for value in row] for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(row, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column], prime - 2, prime)
        work[row] = [(inverse * value) % prime for value in work[row]]
        for i in range(len(work)):
            if i == row:
                continue
            factor = work[i][column]
            work[i] = [
                (value - factor * pivot_value) % prime
                for value, pivot_value in zip(work[i], work[row], strict=True)
            ]
        row += 1
        if row == len(work):
            break
    return row


def pairing_matrix(
    left: tuple[tuple[int, int, int], tuple[int, int, int]],
    right: tuple[tuple[int, int, int], tuple[int, int, int]],
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    """Return P^T J Q for the hyperbolic two-dimensional form."""
    return tuple(
        tuple(
            (left[0][i] * right[1][j] + left[1][i] * right[0][j]) % prime
            for j in range(3)
        )
        for i in range(3)
    )


def check_rank_one_shore_over_f3() -> dict[str, int]:
    """Exhaust the rank consequence for every pair of 2x3 matrices over F3."""
    prime = 3
    maps = tuple(
        (entries[:3], entries[3:])
        for entries in product(range(prime), repeat=6)
    )
    checked = 0
    one_cell = 0
    for left in maps:
        rank_left = rank_mod(left, prime)
        for right in maps:
            rank_right = rank_mod(right, prime)
            matrix = pairing_matrix(left, right, prime)
            rank_matrix = rank_mod(matrix, prime)
            if rank_left == rank_right == 2:
                assert rank_matrix == 2
            nonzero_cells = [
                (i, j)
                for i in range(3)
                for j in range(3)
                if matrix[i][j]
            ]
            if len(nonzero_cells) != 1 or nonzero_cells[0][0] != nonzero_cells[0][1]:
                continue
            one_cell += 1
            colour = nonzero_cells[0][0]
            assert (rank_left, rank_right) in {(1, 1), (1, 2), (2, 1)}
            if rank_left == 1:
                assert all(left[row][i] == 0 for row in range(2) for i in range(3) if i != colour)
            if rank_right == 1:
                assert all(right[row][i] == 0 for row in range(2) for i in range(3) if i != colour)
            checked += 1
    assert checked == one_cell > 0
    return {
        "ordered_map_pairs": len(maps) ** 2,
        "single_nonzero_diagonal_cell_pairs": one_cell,
    }


def main() -> None:
    """Run all exact checks and print a deterministic summary."""
    report = {
        "symbolic_double_contractions": check_symbolic_tables(),
        "cross_family_exceptional_pairs": check_cross_family_cases(),
        "same_family_exceptional_pairs": check_same_family_cases(),
        "rank_one_shore_F3": check_rank_one_shore_over_f3(),
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
