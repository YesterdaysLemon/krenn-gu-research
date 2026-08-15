"""Independent no-import audit of the same-mode N/N q-plus exclusion.

This file intentionally imports neither SymPy nor the primary verifier.  It
uses square-free monomial dictionaries, Fraction arithmetic, an independently
written permutation polarizer, and a small finite-field hyperplane stress test.
The finite-field enumeration is labelled stress evidence only; the exact
characteristic-zero argument is in the theorem.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product
import json
from pathlib import Path
from typing import Iterable


Vector = tuple[Fraction, ...]
Matrix = tuple[Vector, ...]
Quadratic = dict[tuple[int, int], Fraction]

Q: dict[str, Quadratic] = {
    "m1": {(1, 3): Fraction(1), (1, 2): Fraction(-1), (0, 1): Fraction(-1)},
    "m2": {(0, 3): Fraction(1), (0, 2): Fraction(-1), (0, 1): Fraction(-1)},
    "d0": {
        (1, 3): Fraction(1),
        (2, 3): Fraction(1),
        (0, 1): Fraction(-1),
        (0, 2): Fraction(-1),
    },
    "d1": {
        (0, 3): Fraction(1),
        (2, 3): Fraction(1),
        (0, 1): Fraction(-1),
        (1, 2): Fraction(-1),
    },
    "d2": {(0, 1): Fraction(-2)},
}


def vec(*entries: int | Fraction) -> Vector:
    """Construct a rational vector."""
    return tuple(Fraction(entry) for entry in entries)


def vadd(*vectors: Vector) -> Vector:
    """Add vectors."""
    return tuple(sum(entries, Fraction(0)) for entries in zip(*vectors, strict=True))


def scale(scalar: int | Fraction, vector: Vector) -> Vector:
    """Scale a vector."""
    scalar = Fraction(scalar)
    return tuple(scalar * entry for entry in vector)


def dot(left: Vector, right: Vector) -> Fraction:
    """Dot product."""
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def transpose(matrix: Matrix) -> Matrix:
    """Transpose a rectangular matrix."""
    return tuple(tuple(row[j] for row in matrix) for j in range(len(matrix[0])))


def matmul(left: Matrix, right: Matrix) -> Matrix:
    """Multiply rational matrices."""
    right_t = transpose(right)
    return tuple(tuple(dot(row, column) for column in right_t) for row in left)


def rank(matrix: Iterable[Iterable[int | Fraction]]) -> int:
    """Fraction Gaussian rank, independently implemented."""
    rows = [[Fraction(value) for value in row] for row in matrix]
    if not rows:
        return 0
    width = len(rows[0])
    pivot_row = 0
    for column in range(width):
        pivot = next((i for i in range(pivot_row, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        pivot_value = rows[pivot_row][column]
        rows[pivot_row] = [value / pivot_value for value in rows[pivot_row]]
        for i, row in enumerate(rows):
            if i == pivot_row or not row[column]:
                continue
            factor = row[column]
            rows[i] = [value - factor * lead for value, lead in zip(row, rows[pivot_row], strict=True)]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def contract(quadratic: Quadratic, vector: Vector) -> Vector:
    """Contract a square-free quadratic by one R-vector."""
    answer = [Fraction(0)] * 4
    for (i, j), coefficient in quadratic.items():
        answer[i] += coefficient * vector[j]
        answer[j] += coefficient * vector[i]
    return tuple(answer)


def residuals(vector: Vector) -> dict[str, Vector]:
    """Return all five residual rows."""
    return {name: contract(quadratic, vector) for name, quadratic in Q.items()}


def double_contract(quadratic: Quadratic, left: Vector, right: Vector) -> Fraction:
    """Evaluate a polarized square-free quadratic."""
    return sum(
        (
            coefficient * (left[i] * right[j] + left[j] * right[i])
            for (i, j), coefficient in quadratic.items()
        ),
        Fraction(0),
    )


def monomial_polarization(
    variables: tuple[int, ...],
    vectors: tuple[Vector, ...],
) -> Fraction:
    """Polarize one square-free monomial by direct slot permutations."""
    assert len(variables) == len(vectors)
    total = Fraction(0)
    for assignment in permutations(variables):
        term = Fraction(1)
        for slot, variable in enumerate(assignment):
            term *= vectors[slot][variable]
        total += term
    return total


def quartic_value(quadratic: Quadratic, vectors: tuple[Vector, Vector, Vector, Vector]) -> Fraction:
    """Polarize x4*x5*Q using monomial assignments, not Hessians."""
    return sum(
        (
            coefficient * monomial_polarization((i, j, 4, 5), vectors)
            for (i, j), coefficient in quadratic.items()
        ),
        Fraction(0),
    )


def cubic_value(row: Vector, vectors: tuple[Vector, Vector, Vector]) -> Fraction:
    """Polarize x4*x5*ell by direct monomial assignments."""
    return sum(
        (row[i] * monomial_polarization((i, 4, 5), vectors) for i in range(4)),
        Fraction(0),
    )


def outer3(left: Vector, middle: Vector, right: Vector) -> tuple[Fraction, ...]:
    """Flatten a decomposable 3-tensor."""
    return tuple(a * b * c for a in left for b in middle for c in right)


def tensor_sum(*terms: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    """Add flattened tensors."""
    return tuple(sum(cell, Fraction(0)) for cell in zip(*terms, strict=True))


def check_monomial_contractions() -> dict[str, object]:
    """Rebuild every contraction table from monomial masks."""
    n = vec(0, 0, 1, 1)
    p = vec(1, -1, 0, 0)
    m = vec(1, 1, 0, 0)
    h0 = vec(-1, 1, 1, 1)
    h1 = vec(1, -1, 1, 1)
    ell = vec(-1, -1, -1, 1)
    assert residuals(n) == {
        "m1": vec(0, 0, 0, 0),
        "m2": vec(0, 0, 0, 0),
        "d0": h0,
        "d1": h1,
        "d2": vec(0, 0, 0, 0),
    }
    assert residuals(m) == {
        "m1": ell,
        "m2": ell,
        "d0": ell,
        "d1": ell,
        "d2": scale(-2, m),
    }

    p_rows = residuals(p)
    a = vec(1, -1, 1, -1)
    b = vec(1, -1, -1, 1)
    c = vec(1, -1, -1, -1)
    d = vec(1, -1, 1, 1)
    e = vec(2, -2, 0, 0)
    assert p_rows == {"m1": a, "m2": b, "d0": c, "d1": d, "d2": e}
    assert vadd(a, b) == vadd(c, d) == e
    assert residuals(n)["d0"] == scale(-1, c)
    assert residuals(n)["d1"] == d
    assert all(double_contract(poly, m, p) == 0 for poly in Q.values())

    for rho in (-4, -1, 0, 1, 3):
        r = vadd(scale(rho, n), p)
        rows = residuals(r)
        assert rows["m1"] == a and rows["m2"] == b
        assert rows["d0"] == scale(rho - 1, h0)
        assert rows["d1"] == scale(rho + 1, h1)
        assert rows["d2"] == e

    double_n = {name: double_contract(poly, n, n) for name, poly in Q.items()}
    assert double_n == {"m1": 0, "m2": 0, "d0": 2, "d1": 2, "d2": 0}
    return {
        "residual_tables": 8,
        "P_relation": "a+b=c+d=e",
        "double_N": {name: int(value) for name, value in double_n.items()},
    }


def check_independent_polarization() -> dict[str, object]:
    """Compare direct monomial quartics with independently polarized residuals."""
    triples = (
        (
            vec(1, 0, 2, -1, 1, 0),
            vec(0, 1, 1, 2, 0, 2),
            vec(2, -1, 0, 1, 3, 1),
        ),
        (
            vec(0, 1, 2, 1, 0, 3),
            vec(2, -1, 0, 1, 1, 1),
            vec(1, 2, 1, -2, 2, 0),
        ),
        (
            vec(2, -1, 1, 0, 1, 2),
            vec(1, 0, 3, 2, 2, 0),
            vec(0, 1, -1, 2, 0, 1),
        ),
    )
    fixed = (
        vec(0, 0, 1, 1),
        vec(1, 1, 0, 0),
        vec(1, -1, 0, 0),
        vec(-1, 1, 1, 1),
        vec(1, -1, 1, 1),
    )
    entries = 0
    for contraction_vector in fixed:
        vector6 = contraction_vector + vec(0, 0)
        rows = residuals(contraction_vector)
        for name, quadratic in Q.items():
            for i, j, k in product(range(3), repeat=3):
                remaining = (triples[0][i], triples[1][j], triples[2][k])
                assert quartic_value(quadratic, (vector6, *remaining)) == cubic_value(
                    rows[name], remaining
                )
                entries += 1
    return {"monomial_polarization_entries": entries}


def check_exact_ranks_and_kernels() -> dict[str, object]:
    """Audit all common-kernel dimensions with Fraction row rank."""
    n = vec(0, 0, 1, 1)
    p = vec(1, -1, 0, 0)
    m = vec(1, 1, 0, 0)
    ell = vec(-1, -1, -1, 1)
    h0 = vec(-1, 1, 1, 1)
    h1 = vec(1, -1, 1, 1)
    h2p = vec(-1, 1, -1, 1)
    k = vec(-1, 1, 1, -1)
    a_plus = vec(1, -1, 1, -1)
    b_plus = vec(1, -1, -1, 1)
    q_minus = vec(1, 1, -1, 1)

    claims = (
        ((ell, m), (n, p), 2),
        ((ell, h0, h1), (q_minus,), 1),
        ((h2p, k, p), (m, n), 2),
        ((h2p, k, p, h0), (m,), 1),
        ((a_plus, b_plus, h1), (m,), 1),
    )
    for rows, candidates, nullity in claims:
        assert 4 - rank(rows) == nullity
        assert all(all(dot(row, candidate) == 0 for row in rows) for candidate in candidates)
        assert rank(candidates) == nullity
    assert rank((ell, h0, h1, m)) == 4
    assert rank(tuple(tuple(dot(row, basis) for basis in (n, p)) for row in (h0, h1))) == 2
    return {
        "kernel_checks": len(claims) + 2,
        "q_plus_H_dimension": 2,
        "same_colour_final_kernel_dimension": 1,
    }


def matrix_restrict(basis_left: Matrix, form: Matrix, basis_right: Matrix, prime: int) -> Matrix:
    """Restrict a form over F_p."""
    left_t = transpose(basis_left)
    raw = matmul(matmul(left_t, form), basis_right)
    return tuple(tuple(Fraction(int(value) % prime) for value in row) for row in raw)


def inv_mod(value: int, prime: int) -> int:
    """Invert a nonzero residue."""
    return pow(value % prime, prime - 2, prime)


def normalize_projective(vector: tuple[int, ...], prime: int) -> tuple[int, ...]:
    """Normalize a nonzero projective vector."""
    first = next(value for value in vector if value % prime)
    inverse = inv_mod(first, prime)
    return tuple((value * inverse) % prime for value in vector)


def hyperplane_basis(normal: tuple[int, ...], prime: int) -> Matrix:
    """Build a 4-by-3 column basis of a finite-field hyperplane."""
    pivot = next(i for i, value in enumerate(normal) if value % prime)
    columns: list[Vector] = []
    for free in range(4):
        if free == pivot:
            continue
        column = [0] * 4
        column[free] = 1
        column[pivot] = (-normal[free] * inv_mod(normal[pivot], prime)) % prime
        columns.append(vec(*column))
    return transpose(tuple(columns))


def zero_mod(matrix: Matrix, prime: int) -> bool:
    """Test whether every entry vanishes modulo prime."""
    return all(int(value) % prime == 0 for row in matrix for value in row)


def check_finite_hyperplane_stress() -> dict[str, object]:
    """Enumerate the two quotient charts over F5 (stress evidence only)."""
    prime = 5
    normals = sorted(
        {
            normalize_projective(candidate, prime)
            for candidate in product(range(prime), repeat=4)
            if any(candidate)
        }
    )
    assert len(normals) == 156
    bases = {normal: hyperplane_basis(normal, prime) for normal in normals}

    f0_iso = tuple(vec(*row) for row in ((0, 0, 0, 1), (0, 0, 0, 0), (0, 0, 0, 1), (1, 0, 1, 0)))
    f1_iso = tuple(vec(*row) for row in ((0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 0, 0), (0, 1, 0, 0)))
    f0_pure = tuple(vec(*row) for row in ((0, 0, 0, 1), (0, 0, 0, 0), (0, 0, 0, 0), (1, 0, 0, 0)))
    f1_pure = tuple(vec(*row) for row in ((0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 0, 0), (0, 1, 0, 0)))
    f0_a_zero = tuple(vec(*row) for row in ((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0)))
    zero_form = tuple(vec(0, 0, 0, 0) for _ in range(4))

    def pairs_for(forms: tuple[Matrix, Matrix]) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
        pairs: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
        for left_normal, left_basis in bases.items():
            for right_normal, right_basis in bases.items():
                if all(
                    zero_mod(matrix_restrict(left_basis, form, right_basis, prime), prime)
                    for form in forms
                ):
                    pairs.append((left_normal, right_normal))
        return pairs

    iso_pairs = pairs_for((f0_iso, f1_iso))
    pure_pairs = pairs_for((f0_pure, f1_pure))
    a_zero_pairs = pairs_for((f0_a_zero, zero_form))
    beta_normal = (0, 0, 0, 1)
    assert iso_pairs == [(beta_normal, beta_normal)]
    assert pure_pairs == [(beta_normal, beta_normal)]
    assert len(a_zero_pairs) == prime + 1
    return {
        "field": prime,
        "hyperplanes": len(normals),
        "isotropic_chart_pairs": len(iso_pairs),
        "pure_A_chart_pairs": len(pure_pairs),
        "a_zero_orthogonal_pairs": len(a_zero_pairs),
        "evidence_mode": "finite-field stress only",
    }


def check_tensor_forks_independently() -> dict[str, object]:
    """Audit coordinate forks with sparse tensor supports."""
    e0, e1, e2 = vec(1, 0, 0), vec(0, 1, 0), vec(0, 0, 1)
    zero = vec(0, 0, 0)

    branch_one = (
        tensor_sum(outer3(e0, e0, e0), outer3(e1, zero, zero)),
        tensor_sum(outer3(zero, e0, e0), outer3(e1, zero, e1)),
        tensor_sum(outer3(e0, zero, e0), outer3(e1, e1, zero)),
        tensor_sum(outer3(zero, zero, e0), outer3(e1, e1, e1)),
    )
    assert branch_one == (outer3(e0, e0, e0), (Fraction(0),) * 27, (Fraction(0),) * 27, outer3(e1, e1, e1))

    branch_two = (
        tensor_sum(outer3(zero, zero, e1), outer3(e0, e0, e0)),
        tensor_sum(outer3(e1, zero, e1), outer3(e0, e0, zero)),
        tensor_sum(outer3(zero, e1, e1), outer3(e0, zero, e0)),
        tensor_sum(outer3(e1, e1, e1), outer3(e0, zero, zero)),
    )
    assert branch_two == branch_one

    # Coincident companion-mode equation (58): its 27-by-6 coefficient
    # matrix has full column rank for independent epsilon,pi.
    epsilon, pi = e1, e2
    alpha, gamma = vec(2, -1, 3), vec(1, 4, -2)
    coefficient_columns: list[tuple[Fraction, ...]] = []
    for coordinate in range(3):
        unit = tuple(Fraction(int(i == coordinate)) for i in range(3))
        coefficient_columns.append(outer3(epsilon, unit, gamma))
    for coordinate in range(3):
        unit = tuple(Fraction(int(i == coordinate)) for i in range(3))
        coefficient_columns.append(outer3(pi, alpha, unit))
    assert rank(transpose(tuple(coefficient_columns))) == 6
    assert epsilon[0] == pi[0] == 0 and rank((epsilon, pi)) == 2
    return {
        "generic_axis_forks": 2,
        "coincident_zero_tensor_rank": 6,
        "coincident_first_factor_rank": 2,
    }


def check_half_shift_fraction() -> dict[str, object]:
    """Check the p=0 half-shift without symbolic algebra."""
    # A separating rational fixture; bilinearity makes this identity general.
    c0, d0, h = Fraction(3), Fraction(-5), Fraction(7)
    alpha, beta = Fraction(2), Fraction(-4)
    r = vec(5, -2)
    dvec, evec = vec(1, 6), vec(-3, 4)
    original = vadd(
        scale(c0 * beta, dvec),
        scale(d0 * alpha, evec),
        scale(h * alpha * beta, r),
    )
    shifted_d = vadd(dvec, scale(h * alpha / (2 * c0), r))
    shifted_e = vadd(evec, scale(h * beta / (2 * d0), r))
    shifted = vadd(scale(c0 * beta, shifted_d), scale(d0 * alpha, shifted_e))
    assert original == shifted
    return {"half_shift_fixture": [str(value) for value in original], "exact": True}


def check_status() -> dict[str, object]:
    """Fail if the theorem silently strengthens its scope."""
    theorem_path = Path(__file__).with_name(
        "ARBITRARY_PERMANENT_FIXED_PAIR_SAME_MODE_NN_Q_PLUS_EXCLUSION_THEOREM.md"
    )
    theorem = theorem_path.read_text(encoding="utf-8")
    required = (
        "q_+:                                  EXCLUDED",
        "q_-:                                  SIBLING THEOREM",
        "combined same-mode synthesis:                          NOT CLAIMED HERE",
        "global Krenn--Gu conjecture:                           UNRESOLVED",
        "The scripts replay the displayed algebra; the\nwritten characteristic-zero argument proves the theorem.",
        "### 9.2 A second `N` in the companion mode",
    )
    for phrase in required:
        assert phrase in theorem
    assert "global Krenn--Gu conjecture:                           RESOLVED" not in theorem
    return {"scope_markers": len(required), "global_status": "UNRESOLVED"}


def main() -> None:
    """Run the independent audit."""
    report = {
        "monomials": check_monomial_contractions(),
        "polarization": check_independent_polarization(),
        "kernels": check_exact_ranks_and_kernels(),
        "hyperplane_stress": check_finite_hyperplane_stress(),
        "tensor_forks": check_tensor_forks_independently(),
        "half_shift": check_half_shift_fraction(),
        "status": check_status(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    print("same-mode N/N q-plus independent no-import audit: PASS")


if __name__ == "__main__":
    main()
