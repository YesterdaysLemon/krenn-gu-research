"""Independent stdlib audit of the P7 structured-cubic transport theorem.

This file imports neither the primary verifier nor project code.  It uses an
independent sparse formal-polynomial algebra and exact rational matrices.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

LEAVES = tuple(range(7))
EDGES = tuple(combinations(LEAVES, 2))
FULL_MASK = sum(1 << vertex for vertex in LEAVES)
Polynomial = dict[tuple[str, ...], Fraction]
BooleanForm = dict[int, Polynomial]
Matrix = list[list[Fraction]]


def poly_constant(value: int | Fraction) -> Polynomial:
    coefficient = Fraction(value)
    return {} if coefficient == 0 else {(): coefficient}


def poly_variable(name: str) -> Polynomial:
    return {(name,): Fraction(1)}


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, Fraction(0)) + coefficient
        if out[monomial] == 0:
            del out[monomial]
    return out


def poly_scale(value: int | Fraction, polynomial: Polynomial) -> Polynomial:
    scalar = Fraction(value)
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in polynomial.items()
        if scalar * coefficient
    }


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            out[monomial] = (
                out.get(monomial, Fraction(0))
                + left_coefficient * right_coefficient
            )
            if out[monomial] == 0:
                del out[monomial]
    return out


def poly_sum(values: list[Polynomial]) -> Polynomial:
    out: Polynomial = {}
    for value in values:
        out = poly_add(out, value)
    return out


def set_mask(vertices: tuple[int, ...] | set[int]) -> int:
    return sum(1 << vertex for vertex in vertices)


def boolean_add(left: BooleanForm, right: BooleanForm) -> BooleanForm:
    out = {mask: dict(coefficient) for mask, coefficient in left.items()}
    for mask, coefficient in right.items():
        out[mask] = poly_add(out.get(mask, {}), coefficient)
        if not out[mask]:
            del out[mask]
    return out


def boolean_scale(value: int | Fraction, form: BooleanForm) -> BooleanForm:
    return {
        mask: scaled
        for mask, coefficient in form.items()
        if (scaled := poly_scale(value, coefficient))
    }


def boolean_poly_scale(polynomial: Polynomial, form: BooleanForm) -> BooleanForm:
    return {
        mask: scaled
        for mask, coefficient in form.items()
        if (scaled := poly_mul(polynomial, coefficient))
    }


def boolean_mul(left: BooleanForm, right: BooleanForm) -> BooleanForm:
    out: BooleanForm = {}
    for left_mask, left_coefficient in left.items():
        for right_mask, right_coefficient in right.items():
            if left_mask & right_mask:
                continue
            target = left_mask | right_mask
            out[target] = poly_add(
                out.get(target, {}),
                poly_mul(left_coefficient, right_coefficient),
            )
            if not out[target]:
                del out[target]
    return out


def boolean_down(form: BooleanForm) -> BooleanForm:
    out: BooleanForm = {}
    for mask, coefficient in form.items():
        for vertex in LEAVES:
            if not mask & (1 << vertex):
                continue
            target = mask ^ (1 << vertex)
            out[target] = poly_add(out.get(target, {}), coefficient)
    return out


def quadratic_sum(form: BooleanForm) -> Polynomial:
    assert all(mask.bit_count() == 2 for mask in form)
    return poly_sum(list(form.values()))


def transpose(matrix: Matrix) -> Matrix:
    return [list(column) for column in zip(*matrix, strict=True)]


def matrix_product(left: Matrix, right: Matrix) -> Matrix:
    right_transpose = transpose(right)
    return [
        [
            sum(
                (a * b for a, b in zip(row, column, strict=True)),
                Fraction(0),
            )
            for column in right_transpose
        ]
        for row in left
    ]


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return [
        [a + b for a, b in zip(left_row, right_row, strict=True)]
        for left_row, right_row in zip(left, right, strict=True)
    ]


def matrix_scale(value: int | Fraction, matrix: Matrix) -> Matrix:
    scalar = Fraction(value)
    return [[scalar * entry for entry in row] for row in matrix]


def identity(size: int) -> Matrix:
    return [
        [Fraction(int(row == column)) for column in range(size)]
        for row in range(size)
    ]


def exact_rank(matrix: Matrix) -> int:
    work = [row[:] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or work[row][column] == 0:
                continue
            scale = work[row][column]
            work[row] = [
                entry - scale * pivot_entry
                for entry, pivot_entry in zip(
                    work[row], work[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def exact_determinant(matrix: Matrix) -> Fraction:
    work = [row[:] for row in matrix]
    determinant = Fraction(1)
    sign = 1
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        determinant *= pivot_value
        for row in range(column + 1, len(work)):
            if work[row][column] == 0:
                continue
            scale = work[row][column] / pivot_value
            for inner in range(column, len(work)):
                work[row][inner] -= scale * work[column][inner]
    return sign * determinant


def audit_transport() -> None:
    down = [
        [Fraction(int(vertex in edge)) for edge in EDGES]
        for vertex in LEAVES
    ]
    up_down = matrix_product(transpose(down), down)
    transport = matrix_add(identity(21), up_down)
    g0_basis = [
        [
            Fraction(int(row == column) - int(row == 20))
            for column in range(20)
        ]
        for row in range(21)
    ]
    transported = matrix_product(transport, g0_basis)
    assert all(sum(transported[row][column] for row in range(21)) == 0 for column in range(20))
    restricted = [row[:] for row in transported[:20]]
    restricted_identity = identity(20)
    minus_one = matrix_add(restricted, matrix_scale(-1, restricted_identity))
    minus_six = matrix_add(restricted, matrix_scale(-6, restricted_identity))
    assert matrix_product(minus_one, minus_six) == matrix_scale(0, restricted_identity)
    assert exact_rank(minus_one) == 6
    assert exact_rank(minus_six) == 14
    assert exact_determinant(restricted) == 6**6
    inverse_full = matrix_add(identity(21), matrix_scale(Fraction(-1, 6), up_down))
    inverse_restricted = matrix_product(inverse_full, g0_basis)[:20]
    assert matrix_product(restricted, inverse_restricted) == restricted_identity


def build_formal_data() -> dict[str, BooleanForm | Polynomial]:
    ell = {1 << vertex: poly_constant(1) for vertex in LEAVES}
    omega = boolean_scale(Fraction(1, 2), boolean_mul(ell, ell))
    f_form = {
        set_mask(set(edge)): poly_variable(f"f_{edge[0]}{edge[1]}")
        for edge in EDGES
    }
    a_form = {
        1 << vertex: poly_variable(f"a_{vertex}") for vertex in LEAVES
    }
    t = poly_variable("t")
    k_form = boolean_add(
        boolean_scale(2, boolean_mul(ell, a_form)),
        boolean_poly_scale(t, f_form),
    )
    s = quadratic_sum(k_form)
    h_form = boolean_add(
        boolean_poly_scale(s, omega),
        boolean_scale(-21, k_form),
    )
    h_down = boolean_down(h_form)
    canonical_g = boolean_add(
        h_form,
        boolean_scale(Fraction(-1, 6), boolean_mul(ell, h_down)),
    )
    canonical_d = boolean_down(canonical_g)
    return {
        "ell": ell,
        "omega": omega,
        "f": f_form,
        "a": a_form,
        "t": t,
        "k": k_form,
        "s": s,
        "h": h_form,
        "g": canonical_g,
        "d": canonical_d,
    }


def audit_formal_covariant(data: dict[str, BooleanForm | Polynomial]) -> None:
    ell = data["ell"]
    omega = data["omega"]
    f_form = data["f"]
    a_form = data["a"]
    t = data["t"]
    k_form = data["k"]
    s = data["s"]
    h_form = data["h"]
    canonical_g = data["g"]
    canonical_d = data["d"]
    assert isinstance(ell, dict)
    assert isinstance(omega, dict)
    assert isinstance(f_form, dict)
    assert isinstance(a_form, dict)
    assert isinstance(t, dict)
    assert isinstance(k_form, dict)
    assert isinstance(s, dict)
    assert isinstance(h_form, dict)
    assert isinstance(canonical_g, dict)
    assert isinstance(canonical_d, dict)

    assert quadratic_sum(omega) == poly_constant(21)
    assert quadratic_sum(h_form) == {}
    assert quadratic_sum(canonical_g) == {}
    transported_g = boolean_add(
        canonical_g,
        boolean_mul(ell, canonical_d),
    )
    assert transported_g == h_form

    identity_16_left = boolean_mul(ell, boolean_mul(f_form, k_form))
    identity_16_right = boolean_add(
        boolean_scale(4, boolean_mul(f_form, boolean_mul(a_form, omega))),
        boolean_poly_scale(t, boolean_mul(ell, boolean_mul(f_form, f_form))),
    )
    assert identity_16_left == identity_16_right

    canonical_c = boolean_add(
        boolean_scale(2, boolean_mul(a_form, canonical_g)),
        boolean_scale(-1, boolean_poly_scale(t, boolean_mul(canonical_d, f_form))),
    )
    c_via_h = boolean_add(
        boolean_scale(2, boolean_mul(a_form, h_form)),
        boolean_scale(-1, boolean_mul(canonical_d, k_form)),
    )
    assert canonical_c == c_via_h

    linear_factor = boolean_add(
        boolean_add(
            boolean_poly_scale(poly_scale(Fraction(1, 2), s), ell),
            boolean_scale(-42, a_form),
        ),
        boolean_scale(-1, canonical_d),
    )
    essential_term = boolean_poly_scale(
        poly_scale(Fraction(-1, 2), poly_mul(t, s)),
        boolean_mul(ell, f_form),
    )
    covariant_right = boolean_add(
        essential_term,
        boolean_mul(linear_factor, k_form),
    )
    assert canonical_c == covariant_right

    forced_right = boolean_add(
        boolean_poly_scale(
            poly_scale(Fraction(-1, 2), poly_mul(t, s)),
            boolean_mul(ell, boolean_mul(f_form, f_form)),
        ),
        boolean_mul(linear_factor, boolean_mul(f_form, k_form)),
    )
    assert boolean_mul(f_form, canonical_c) == forced_right


def audit_hessian_pairing(data: dict[str, BooleanForm | Polynomial]) -> None:
    ell = data["ell"]
    f_form = data["f"]
    a_form = data["a"]
    t = data["t"]
    k_form = data["k"]
    assert isinstance(ell, dict)
    assert isinstance(f_form, dict)
    assert isinstance(a_form, dict)
    assert isinstance(t, dict)
    assert isinstance(k_form, dict)

    a_variables = {vertex: poly_variable(f"a_{vertex}") for vertex in LEAVES}
    f_variables = {edge: poly_variable(f"f_{edge[0]}{edge[1]}") for edge in EDGES}
    hessian: list[list[Polynomial]] = []
    pairing: list[list[Polynomial]] = []
    for first_edge in EDGES:
        hessian_row: list[Polynomial] = []
        pairing_row: list[Polynomial] = []
        first_form = {set_mask(set(first_edge)): poly_constant(1)}
        for second_edge in EDGES:
            overlap = set(first_edge) & set(second_edge)
            if overlap:
                hessian_entry: Polynomial = {}
            else:
                union = set(first_edge) | set(second_edge)
                hessian_entry = poly_sum(
                    [
                        poly_mul(
                            a_variables[vertex],
                            f_variables[
                                tuple(sorted(set(LEAVES) - union - {vertex}))
                            ],
                        )
                        for vertex in set(LEAVES) - union
                    ]
                )
            hessian_row.append(hessian_entry)
            second_form = {set_mask(set(second_edge)): poly_constant(1)}
            product = boolean_mul(
                boolean_mul(boolean_mul(first_form, second_form), a_form),
                f_form,
            )
            pairing_row.append(product.get(FULL_MASK, {}))
        hessian.append(hessian_row)
        pairing.append(pairing_row)
    assert hessian == pairing

    physical_numerator = boolean_add(
        boolean_mul(ell, boolean_mul(f_form, k_form)),
        boolean_scale(
            -1,
            boolean_poly_scale(t, boolean_mul(ell, boolean_mul(f_form, f_form))),
        ),
    )
    for row, edge in enumerate(EDGES):
        four_hessian_omega = poly_scale(4, poly_sum(hessian[row]))
        edge_form = {set_mask(set(edge)): poly_constant(1)}
        paired_numerator = boolean_mul(edge_form, physical_numerator).get(
            FULL_MASK, {}
        )
        assert four_hessian_omega == paired_numerator


def main() -> None:
    audit_transport()
    data = build_formal_data()
    audit_formal_covariant(data)
    audit_hessian_pairing(data)
    print("AUDIT PASS: exact G_0 transport has spectrum 1^14,6^6 and determinant 6^6")
    print("AUDIT PASS: canonical H,G,C covariant rebuilt in independent formal algebra")
    print("AUDIT PASS: C class reduces exactly to sigma(K)[ell F]")
    print("AUDIT PASS: inverse-system Hessian pairing and forced Omega kernel agree")
    print("imports_from_primary=0 imports_from_project=0")
    print("searches=0 finite_fields=0 graph_enumerations=0 groebner=0")
    print("SCOPE: physical extension existence, P7, and global Krenn-Gu remain unresolved")


if __name__ == "__main__":
    main()
