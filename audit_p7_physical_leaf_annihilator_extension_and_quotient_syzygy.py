"""Independent no-import audit of the physical P7 leaf-annihilator theorem."""

from __future__ import annotations

import itertools
import math
from fractions import Fraction
from math import gcd

LEAVES = tuple(range(1, 8))
EDGES = tuple(itertools.combinations(LEAVES, 2))
TRIPLES = tuple(itertools.combinations(LEAVES, 3))
FOUR_SETS = tuple(itertools.combinations(LEAVES, 4))
FIVE_SETS = tuple(itertools.combinations(LEAVES, 5))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
Polynomial = dict[tuple[str, ...], Fraction]
BooleanForm = dict[int, Polynomial]


def exact_rank(matrix: list[list[int]]) -> int:
    """Compute exact rank by fraction-free elimination."""
    if not matrix:
        return 0
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
        for row in range(len(work)):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            tail = [
                pivot_value * work[row][inner]
                - factor * work[pivot_row][inner]
                for inner in range(column, len(work[0]))
            ]
            divisor = 0
            for value in tail:
                divisor = gcd(divisor, abs(value))
            if divisor > 1:
                tail = [value // divisor for value in tail]
            work[row][column:] = tail
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def lefschetz_matrix(source_degree: int, power: int) -> list[list[int]]:
    """Build multiplication by ell^power on seven square-free variables."""
    source = tuple(itertools.combinations(LEAVES, source_degree))
    target = tuple(itertools.combinations(LEAVES, source_degree + power))
    return [
        [
            math.factorial(power) if set(column).issubset(row) else 0
            for column in source
        ]
        for row in target
    ]


def set_mask(vertices: tuple[int, ...] | frozenset[int]) -> int:
    """Encode a subset by a bit mask."""
    out = 0
    for vertex in vertices:
        out |= 1 << vertex
    return out


def poly_constant(value: int | Fraction) -> Polynomial:
    """Return a constant sparse polynomial."""
    coefficient = Fraction(value)
    return {} if coefficient == 0 else {(): coefficient}


def poly_variable(name: str) -> Polynomial:
    """Return one formal variable."""
    return {(name,): Fraction(1)}


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    """Add sparse formal polynomials."""
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, Fraction(0)) + coefficient
        if out[monomial] == 0:
            del out[monomial]
    return out


def poly_scale(value: int | Fraction, polynomial: Polynomial) -> Polynomial:
    """Scale a sparse formal polynomial."""
    scalar = Fraction(value)
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in polynomial.items()
        if scalar * coefficient
    }


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply sparse formal polynomials."""
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
    """Add a list of sparse polynomials."""
    out: Polynomial = {}
    for value in values:
        out = poly_add(out, value)
    return out


def boolean_add(left: BooleanForm, right: BooleanForm) -> BooleanForm:
    """Add formal Boolean-algebra elements."""
    out = {mask: dict(coefficient) for mask, coefficient in left.items()}
    for mask, coefficient in right.items():
        out[mask] = poly_add(out.get(mask, {}), coefficient)
        if not out[mask]:
            del out[mask]
    return out


def boolean_scale(value: int | Fraction, form: BooleanForm) -> BooleanForm:
    """Scale a formal Boolean-algebra element."""
    return {
        mask: coefficient
        for mask, polynomial in form.items()
        if (coefficient := poly_scale(value, polynomial))
    }


def boolean_mul(left: BooleanForm, right: BooleanForm) -> BooleanForm:
    """Multiply modulo z_i^2=0."""
    out: BooleanForm = {}
    for left_mask, left_coefficient in left.items():
        for right_mask, right_coefficient in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            out[mask] = poly_add(
                out.get(mask, {}), poly_mul(left_coefficient, right_coefficient)
            )
            if not out[mask]:
                del out[mask]
    return out


def build_formal_system() -> dict[str, BooleanForm]:
    """Build the universal radial and syzygy expressions independently."""
    ell = {1 << vertex: poly_constant(1) for vertex in LEAVES}
    f_form = {
        set_mask(edge): poly_variable(f"f_{edge[0]}{edge[1]}") for edge in EDGES
    }
    a_form = {
        1 << vertex: poly_variable(f"a_{vertex}") for vertex in LEAVES
    }
    t = poly_variable("t")
    n_form = boolean_scale(Fraction(1, 2), boolean_mul(f_form, f_form))
    jn_form = {
        set_mask(triple): n_form[
            set_mask(tuple(vertex for vertex in LEAVES if vertex not in triple))
        ]
        for triple in TRIPLES
    }
    residual = boolean_add(
        boolean_mul(a_form, f_form),
        {
            mask: poly_scale(-1, poly_mul(t, coefficient))
            for mask, coefficient in jn_form.items()
        },
    )
    k_form = boolean_add(
        boolean_scale(2, boolean_mul(ell, a_form)),
        {mask: poly_mul(t, coefficient) for mask, coefficient in f_form.items()},
    )
    primitive_defect = boolean_add(n_form, boolean_mul(ell, jn_form))

    free_g = [poly_variable(f"g_{index}") for index in range(20)]
    g_coefficients = free_g + [poly_scale(-1, poly_sum(free_g))]
    g_form = {
        set_mask(edge): g_coefficients[index] for index, edge in enumerate(EDGES)
    }
    down_form = {}
    for vertex in LEAVES:
        down_form[1 << vertex] = poly_sum(
            [g_coefficients[EDGE_INDEX[edge]] for edge in EDGES if vertex in edge]
        )
    phi_form = boolean_add(
        boolean_mul(g_form, jn_form),
        boolean_scale(-1, boolean_mul(down_form, n_form)),
    )
    c_form = boolean_add(
        boolean_scale(2, boolean_mul(a_form, g_form)),
        {
            mask: poly_scale(-1, poly_mul(t, coefficient))
            for mask, coefficient in boolean_mul(down_form, f_form).items()
        },
    )
    return {
        "ell": ell,
        "f": f_form,
        "a": a_form,
        "t": {0: t},
        "n": n_form,
        "jn": jn_form,
        "residual": residual,
        "k": k_form,
        "primitive_defect": primitive_defect,
        "g": g_form,
        "phi": phi_form,
        "c": c_form,
    }


def audit_master_identities(system: dict[str, BooleanForm]) -> None:
    """Audit the radial and cubic-syzygy master identities formally."""
    t_polynomial = system["t"][0]
    fk = boolean_mul(system["f"], system["k"])
    radial_term = boolean_scale(2, boolean_mul(system["ell"], system["residual"]))
    defect_term = {
        mask: poly_scale(2, poly_mul(t_polynomial, coefficient))
        for mask, coefficient in system["primitive_defect"].items()
    }
    assert fk == boolean_add(radial_term, defect_term)

    fc = boolean_mul(system["f"], system["c"])
    phi_term = {
        mask: poly_scale(2, poly_mul(t_polynomial, coefficient))
        for mask, coefficient in system["phi"].items()
    }
    residual_term = boolean_scale(
        2, boolean_mul(system["g"], system["residual"])
    )
    assert fc == boolean_add(phi_term, residual_term)


def audit_adjoint_multiplication() -> None:
    """Audit that mu_3 is the complemented transpose of mu_2."""
    for edge in EDGES:
        for four in FOUR_SETS:
            mu_two_entry = (
                tuple(vertex for vertex in four if vertex not in edge)
                if set(edge).issubset(four)
                else None
            )
            five = tuple(vertex for vertex in LEAVES if vertex not in edge)
            triple = tuple(vertex for vertex in LEAVES if vertex not in four)
            mu_three_entry = (
                tuple(vertex for vertex in five if vertex not in triple)
                if set(triple).issubset(five)
                else None
            )
            assert mu_two_entry == mu_three_entry


def audit_uniform_switching() -> None:
    """Audit the uniform inclusion rank and diagonal switching formula."""
    inclusion = [
        [int(set(edge).issubset(four)) for edge in EDGES] for four in FOUR_SETS
    ]
    assert exact_rank(inclusion) == 21
    for four in FOUR_SETS:
        for edge in EDGES:
            if not set(edge).issubset(four):
                continue
            complement = tuple(vertex for vertex in four if vertex not in edge)
            row_variables = {f"s_{vertex}" for vertex in four}
            column_variables = {f"s_{vertex}" for vertex in edge}
            assert row_variables - column_variables == {
                f"s_{vertex}" for vertex in complement
            }


def audit_boundary_family() -> None:
    """Audit the exact square-zero coordinate-boundary family."""
    ell = {1 << vertex: poly_constant(1) for vertex in LEAVES}
    f_form = {
        set_mask((1, vertex)): poly_variable(f"q_{vertex}")
        for vertex in LEAVES
        if vertex != 1
    }
    a_form = {1 << 1: poly_constant(1)}
    t = poly_variable("t")
    k_form = boolean_add(
        boolean_scale(2, boolean_mul(ell, a_form)),
        {mask: poly_mul(t, coefficient) for mask, coefficient in f_form.items()},
    )
    assert boolean_mul(f_form, f_form) == {}
    assert boolean_mul(a_form, f_form) == {}
    assert boolean_mul(f_form, k_form) == {}


def main() -> None:
    """Run the independent exact audit."""
    lefschetz_3_4 = lefschetz_matrix(3, 1)
    lefschetz_2_5 = lefschetz_matrix(2, 3)
    assert exact_rank(lefschetz_3_4) == 35
    assert exact_rank(lefschetz_2_5) == 21

    incidence = [[int(vertex in edge) for vertex in LEAVES] for edge in EDGES]
    assert exact_rank(incidence) == 7
    assert 21 - exact_rank(incidence) == 14

    system = build_formal_system()
    audit_master_identities(system)
    audit_adjoint_multiplication()
    audit_uniform_switching()
    audit_boundary_family()

    assert len(system["g"]) == 21
    assert len(system["c"]) == 35
    assert len(system["phi"]) == 21

    print("AUDIT PASS: both seven-leaf Lefschetz maps are isomorphisms")
    print("AUDIT PASS: FK radial-extension identity rebuilt formally")
    print("AUDIT PASS: incidence/quotient dimensions are 7+14")
    print("AUDIT PASS: mu_3 is the complemented transpose of mu_2")
    print("AUDIT PASS: uniform switching family has exact rank 21")
    print("AUDIT PASS: cubic-syzygy factor identity rebuilt formally")
    print("AUDIT PASS: exact square-zero coordinate-boundary family")
    print("imports_from_primary=0 imports_from_project=0")
    print("searches=0 finite_fields=0 graph_enumerations=0 groebner=0")
    print("SCOPE: both physical annihilator branches remain UNKNOWN")
    print("SCOPE: quotient rank-at-most-18 incidence remains separate")
    print("SCOPE: P7 and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
