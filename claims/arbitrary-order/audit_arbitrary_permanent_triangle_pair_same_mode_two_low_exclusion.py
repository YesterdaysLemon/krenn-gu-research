"""Independent no-import audit of the triangle same-mode exclusion."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations, permutations, product

Number = int | Fraction
Vector = tuple[Number, ...]
Polynomial = dict[tuple[int, ...], int]
Affine = tuple[Fraction, ...]


def quartics() -> dict[str, Polynomial]:
    """Build the five square-free quartics independently as monomial maps."""
    return {
        "f1": {(2, 3, 4, 5): 1, (1, 3, 4, 5): -1, (0, 3, 4, 5): -1},
        "f2": {(0, 2, 4, 5): 1, (0, 1, 4, 5): -1},
        "d0": {(0, 3, 4, 5): 2},
        "d1": {(0, 2, 4, 5): 1, (1, 2, 4, 5): 1},
        "d2": {(0, 1, 4, 5): 1, (1, 2, 4, 5): -1},
    }


def contract_to_residual(poly: Polynomial, vector: Vector) -> Vector:
    """Contract once and extract the residual beside x4*x5."""
    answer: list[Number] = [0, 0, 0, 0]
    for monomial, coefficient in poly.items():
        for position, index in enumerate(monomial):
            remaining = monomial[:position] + monomial[position + 1:]
            if 4 in remaining and 5 in remaining:
                residual_index = next(i for i in remaining if i not in (4, 5))
                answer[residual_index] += coefficient * vector[index]
    return tuple(answer)


def polarized(poly: Polynomial, vectors: tuple[Vector, ...]) -> Number:
    """Evaluate complete polarization directly from square-free monomials."""
    answer: Number = 0
    for monomial, coefficient in poly.items():
        for order in permutations(range(4)):
            term: Number = coefficient
            for factor, slot in enumerate(order):
                term *= vectors[slot][monomial[factor]]
            answer += term
    return answer


def rank_fraction(rows: list[Vector]) -> int:
    """Compute exact row rank with a separate Fraction reducer."""
    matrix = [list(map(Fraction, row)) for row in rows if any(row)]
    if not matrix:
        return 0
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((row for row in range(rank, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        value = matrix[rank][column]
        matrix[rank] = [entry / value for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            value = matrix[row][column]
            matrix[row] = [
                entry - value * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def audit_contractions() -> dict[str, object]:
    """Rebuild every exceptional and propagated-pencil contraction."""
    polys = quartics()
    lines: dict[str, Vector] = {
        "N": (0, 1, 1, 0, 0, 0),
        "B": (1, 0, 1, 0, 0, 0),
        "C": (1, -1, 0, 0, 0, 0),
        "S": (0, 0, 0, 1, 0, 0),
    }
    table = {
        line: {name: contract_to_residual(poly, vector) for name, poly in polys.items()}
        for line, vector in lines.items()
    }
    assert table["B"]["f2"] == table["C"]["f2"] == (1, -1, 1, 0)
    assert table["S"]["f1"] == (-1, -1, 1, 0)
    assert rank_fraction([table["B"]["f2"], table["S"]["f1"]]) == 2
    assert rank_fraction([
        table["B"]["f2"],
        table["S"]["f1"],
        table["B"]["d0"],
    ]) == 3
    assert table["N"]["d1"] == (1, 1, 1, 0)
    assert table["N"]["d2"] == (1, -1, -1, 0)

    # Check the propagated H-pencil at four separating integer points.  The
    # formulas are linear in (s,t), so these checks identify them exactly.
    expected = {
        "f1": lambda s, t: (-t, -t, t, -2 * s),
        "f2": lambda s, _t: (-2 * s, 0, 0, 0),
        "d0": lambda _s, t: (2 * t, 0, 0, 0),
        "d1": lambda s, _t: (-s, -s, s, 0),
        "d2": lambda s, _t: (s, s, -s, 0),
    }
    for s, t in ((1, 0), (0, 1), (1, 1), (2, -1)):
        vector = (0, s, -s, t, 0, 0)
        for name, poly in polys.items():
            assert contract_to_residual(poly, vector) == expected[name](s, t)

    x4 = (0, 0, 0, 0, 1, 0)
    x5 = (0, 0, 0, 0, 0, 1)
    nn = {name: polarized(poly, (lines["N"], lines["N"], x4, x5)) for name, poly in polys.items()}
    ss = {name: polarized(poly, (lines["S"], lines["S"], x4, x5)) for name, poly in polys.items()}
    assert nn == {"f1": 0, "f2": 0, "d0": 0, "d1": 2, "d2": -2}
    assert all(value == 0 for value in ss.values())
    return {
        "single_contraction_lines": sorted(lines),
        "propagated_pencil_points": 4,
        "N_N_scalars": nn,
        "S_S_all_zero": True,
    }


def poly_add(left: Affine, right: Affine) -> Affine:
    """Add coefficient tuples."""
    length = max(len(left), len(right))
    return tuple(
        (left[i] if i < len(left) else 0) + (right[i] if i < len(right) else 0)
        for i in range(length)
    )


def poly_mul(left: Affine, right: Affine) -> Affine:
    """Multiply coefficient tuples."""
    answer = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            answer[i + j] += x * y
    while len(answer) > 1 and answer[-1] == 0:
        answer.pop()
    return tuple(answer)


def affine_basis(index: int) -> tuple[Affine, ...]:
    """Return a constant coordinate basis vector in four variables."""
    return tuple((Fraction(int(i == index)),) for i in range(4))


def affine_add(left: tuple[Affine, ...], right: tuple[Affine, ...], sign: int = 1) -> tuple[Affine, ...]:
    """Add one affine vector and plus/minus t times another."""
    return tuple(poly_add(left[i], (Fraction(0), Fraction(sign) * right[i][0])) for i in range(4))


def cubic_value(
    factor_indices: tuple[tuple[int, int], ...],
    vectors: tuple[tuple[Affine, ...], ...],
) -> Affine:
    """Polarize a cubic whose factors are signed coordinate covectors."""
    answer: Affine = (Fraction(0),)
    for order in permutations(range(3)):
        term: Affine = (Fraction(1),)
        for factor, slot in enumerate(order):
            index, sign = factor_indices[factor]
            term = poly_mul(term, tuple(sign * value for value in vectors[slot][index]))
        answer = poly_add(answer, term)
    while len(answer) > 1 and answer[-1] == 0:
        answer = answer[:-1]
    return answer


def audit_hhpp_profiles() -> dict[str, object]:
    """Independently enumerate the six affine coordinate-plane charts."""
    basis = tuple(affine_basis(i) for i in range(4))
    first_factors = ((1, 1), (2, 1), (3, 1))
    first_negative = ((1, 1), (2, 1), (0, -1))
    second_factors = ((1, 1), (2, 1), (0, 1))
    report: dict[str, dict[str, object]] = {}
    zero_first = []
    for plane_indices in combinations(range(4), 2):
        complement = [index for index in range(4) if index not in plane_indices]
        i, j = complement
        plane = [basis[index] for index in plane_indices]
        high_plus = [*plane, affine_add(basis[i], basis[j], 1)]
        high_minus = [*plane, affine_add(basis[i], basis[j], -1)]
        first_values = []
        second_values = []
        for vectors in product(plane, high_plus, high_minus):
            positive = cubic_value(first_factors, vectors)
            negative = cubic_value(first_negative, vectors)
            first_values.append(poly_add(positive, negative))
            second_values.append(cubic_value(second_factors, vectors))
        first_nonzero = {value for value in first_values if any(value)}
        second_nonzero = any(any(value) for value in second_values)
        key = "".join(str(index) for index in plane_indices)
        report[key] = {
            "first_nonzero_polynomials": sorted(str(value) for value in first_nonzero),
            "second_nonzero": second_nonzero,
        }
        if not first_nonzero:
            zero_first.append((key, second_nonzero))
    assert zero_first == [("03", False)]
    return {"charts": report, "only_zero_first_chart": "03"}


def audit_coefficient_gate() -> dict[str, object]:
    """Independently exhaust the invertible coefficient gate over two fields."""
    reports = []
    for prime in (5, 7):
        patterns = set()
        total = 0
        for r1, r2, s1, s2 in product(range(prime), repeat=4):
            determinant = (r1 * s2 - r2 * s1) % prime
            if not determinant:
                continue
            total += 1
            pattern = (bool(s2), bool(s1), bool(r2), bool(r1))
            if pattern[0] and pattern[2]:
                continue
            if pattern[1] and pattern[3]:
                continue
            patterns.add(pattern)
        expected = {(True, False, False, True), (False, True, True, False)}
        assert patterns == expected
        reports.append({
            "field": f"F_{prime}",
            "invertible_matrices": total,
            "surviving_patterns": sorted(patterns),
        })
    return {"audits": reports}


def fixture() -> list[list[Vector]]:
    """Return the rational near-survivor without using the primary script."""
    return [
        [
            (1, 0, 0, 0, 0, 0),
            (0, 1, 1, 0, 0, 0),
            (0, 0, 0, 1, Fraction(1, 2), Fraction(1, 2)),
        ],
        [
            (0, 0, 0, 1, 0, 0),
            (Fraction(1, 2), Fraction(1, 4), Fraction(1, 4), 0, 0, 0),
            (0, 0, 0, 0, 1, 1),
        ],
        [
            (1, 0, 0, 0, 0, 0),
            (0, 0, 0, 1, Fraction(-1, 2), Fraction(1, 2)),
            (0, 1, 1, 0, 0, 0),
        ],
        [
            (0, 1, -1, 0, 0, 0),
            (0, 0, 0, 0, 1, -1),
            (Fraction(1, 2), 0, Fraction(-1, 2), 0, 0, 0),
        ],
    ]


def projection(vector: Vector, family: int) -> Vector:
    """Evaluate one of the two projection maps directly."""
    x0, x1, x2, x3, x4, x5 = vector
    if family == 1:
        return (x3, x4, x5, x2 - x1 - x0)
    return (x0, x4, x5, x2 - x1)


def audit_fixture() -> dict[str, object]:
    """Replay all exact fixture claims independently."""
    planes = fixture()
    polys = quartics()
    rank_pairs = []
    for plane in planes:
        assert rank_fraction([tuple(vector[i] for vector in plane) for i in range(6)]) == 3
        rank_pairs.append(tuple(
            rank_fraction([tuple(projection(vector, family)[i] for vector in plane) for i in range(4)])
            for family in (1, 2)
        ))
    assert rank_pairs == [(2, 2), (3, 2), (2, 2), (2, 3)]

    def cells(fixed_mode: int, fixed_colour: int) -> dict[str, list[tuple[tuple[int, ...], str]]]:
        remaining = [mode for mode in range(4) if mode != fixed_mode]
        answer = {}
        for name, poly in polys.items():
            nonzero = []
            for colours in product(range(3), repeat=3):
                vectors = [planes[fixed_mode][fixed_colour]]
                vectors.extend(planes[mode][colour] for mode, colour in zip(remaining, colours, strict=True))
                value = polarized(poly, tuple(vectors))
                if value:
                    nonzero.append((colours, str(value)))
            answer[name] = nonzero
        return answer

    first = cells(0, 1)
    second = cells(2, 2)
    x3_slice = cells(1, 0)
    assert first == {"f1": [], "f2": [], "d0": [], "d1": [((1, 1, 1), "1")], "d2": []}
    assert second == {"f1": [], "f2": [], "d0": [], "d1": [], "d2": [((2, 2, 2), "1")]}
    assert x3_slice["f1"] == [((0, 1, 1), "-1")]
    assert x3_slice["d0"] == [((0, 1, 1), "2")]

    # Directly check G_bh=0 under the hyperbolic form.
    for left in planes[1]:
        for right in planes[3]:
            assert left[4] * right[5] + left[5] * right[4] == 0
    assert all(plane[0][4:] == (0, 0) for plane in planes)
    return {
        "projection_rank_pairs": rank_pairs,
        "first_N_live": first["d1"],
        "second_N_live": second["d2"],
        "x3_off_target": {"f1": x3_slice["f1"], "d0": x3_slice["d0"]},
    }


def main() -> None:
    """Run the independent audit and print a deterministic report."""
    report = {
        "contractions": audit_contractions(),
        "hhpp_profiles": audit_hhpp_profiles(),
        "coefficient_gate": audit_coefficient_gate(),
        "near_survivor": audit_fixture(),
        "independent_from_primary": True,
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
