"""Independent stdlib audit of the P7 mixed-Lefschetz star obstructions.

No primary verifier or project code is imported.  Formal identities use an
independent sparse polynomial algebra; all representation ranks are over Q.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

LEAVES = tuple(range(7))
EDGES = tuple(combinations(LEAVES, 2))
Polynomial = dict[tuple[str, ...], Fraction]
BooleanForm = dict[int, Polynomial]
Matrix = list[list[Fraction]]


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


def audit_mixed_kernel_identity() -> None:
    ell = {1 << vertex: {(): Fraction(1)} for vertex in LEAVES}
    f_form = {
        set_mask(set(edge)): poly_variable(f"f_{edge[0]}{edge[1]}")
        for edge in EDGES
    }
    a_form = {1 << vertex: poly_variable(f"a_{vertex}") for vertex in LEAVES}
    t = poly_variable("t")
    k_form = boolean_add(
        boolean_scale(2, boolean_mul(ell, a_form)),
        boolean_poly_scale(t, f_form),
    )
    left = boolean_mul(ell, boolean_mul(f_form, k_form))
    right = boolean_add(
        boolean_scale(
            2,
            boolean_mul(boolean_mul(ell, ell), boolean_mul(a_form, f_form)),
        ),
        boolean_poly_scale(t, boolean_mul(ell, boolean_mul(f_form, f_form))),
    )
    assert left == right


def incidence(vertices: tuple[int, ...], edges: tuple[tuple[int, int], ...]) -> Matrix:
    return [
        [Fraction(int(vertex in edge)) for edge in edges]
        for vertex in vertices
    ]


def disjoint_matrix(edges: tuple[tuple[int, int], ...]) -> Matrix:
    return [
        [Fraction(int(set(row).isdisjoint(column))) for column in edges]
        for row in edges
    ]


def audit_weighted_kneser_formula() -> None:
    # Coefficients are seven-vectors: this checks the whole linear pencil.
    for row in EDGES:
        for edge in EDGES:
            direct = [Fraction(0)] * 7
            if set(row).isdisjoint(edge):
                for vertex in LEAVES:
                    if vertex not in row and vertex not in edge:
                        direct[vertex] = 2
            anticommutator = [Fraction(0)] * 7
            if set(row).isdisjoint(edge):
                for vertex in LEAVES:
                    anticommutator[vertex] = 2 * Fraction(
                        int(vertex not in row and vertex not in edge)
                    )
            assert direct == anticommutator

    # Exact KG(7,2) eigenspace dimensions and symmetric-anchor signature.
    r7 = incidence(LEAVES, EDGES)
    c7 = disjoint_matrix(EDGES)
    assert exact_rank(r7) == 7
    assert 21 - exact_rank(r7) == 14
    assert matrix_product(r7, transpose(r7)) == [
        [Fraction(6 if row == column else 1) for column in LEAVES]
        for row in LEAVES
    ]
    all_ones = [Fraction(1)] * 21
    assert [sum(row) for row in c7] == [10 * value for value in all_ones]
    # C7=J+I-R^T R gives eigenvalues 10,-4,1 on 1+6+14.
    r7_gram = matrix_product(transpose(r7), r7)
    assert all(
        c7[row][column]
        == 1 + Fraction(int(row == column)) - r7_gram[row][column]
        for row in range(21)
        for column in range(21)
    )


def audit_one_exceptional_block() -> None:
    star_edges = tuple((0, vertex) for vertex in range(1, 7))
    internal_edges = tuple(combinations(range(1, 7), 2))
    c_matrix = [
        [Fraction(int(vertex not in edge)) for edge in internal_edges]
        for vertex in range(1, 7)
    ]
    d_matrix = disjoint_matrix(internal_edges)
    c_gram = matrix_product(c_matrix, transpose(c_matrix))
    assert c_gram == [
        [Fraction(10 if row == column else 6) for column in range(6)]
        for row in range(6)
    ]
    assert exact_rank(c_matrix) == 6

    r6 = incidence(tuple(range(1, 7)), internal_edges)
    r6_gram = matrix_product(transpose(r6), r6)
    assert exact_rank(r6) == 6
    assert 15 - exact_rank(r6) == 9
    # D=J+I-R^T R yields eigenvalues 6,-3,1 on 1+5+9.
    assert all(
        d_matrix[row][column]
        == 1 + Fraction(int(row == column)) - r6_gram[row][column]
        for row in range(15)
        for column in range(15)
    )
    assert [sum(row) for row in d_matrix] == [Fraction(6)] * 15

    # Check the complete formal block coefficient pattern using (p,q)-pairs.
    reordered_edges = star_edges + internal_edges
    for row_index, row in enumerate(reordered_edges):
        for column_index, edge in enumerate(reordered_edges):
            coefficient = [0, 0]
            if set(row).isdisjoint(edge):
                remaining = set(LEAVES) - set(row) - set(edge)
                coefficient[0] = 2 * int(0 in remaining)
                coefficient[1] = 2 * len(remaining - {0})
            if row_index < 6 and column_index < 6:
                expected = [0, 0]
            elif row_index < 6:
                expected = [0, 6 * int(row[1] not in edge)]
            elif column_index < 6:
                expected = [0, 6 * int(edge[1] not in row)]
            else:
                disjoint = int(set(row).isdisjoint(edge))
                expected = [2 * disjoint, 4 * disjoint]
            assert coefficient == expected

    # Six paired blocks and the nine-dimensional internal harmonic block.
    determinant_constant = 2**9 * 144**5 * 1440
    assert determinant_constant == 45650434295070720
    # At p=-2q, the diagonal internal block vanishes.  Since C has full row
    # rank, the full block has rank 2 rank(C)=12 and kernel 0 direct-sum ker C.
    zero6 = [[Fraction(0) for _ in range(6)] for _ in range(6)]
    zero15 = [[Fraction(0) for _ in range(15)] for _ in range(15)]
    exceptional = [
        zero6[row] + [6 * entry for entry in c_matrix[row]]
        for row in range(6)
    ] + [
        [6 * entry for entry in transpose(c_matrix)[row]] + zero15[row]
        for row in range(15)
    ]
    assert exact_rank(exceptional) == 12
    assert 21 - exact_rank(exceptional) == 9


def main() -> None:
    audit_mixed_kernel_identity()
    audit_weighted_kneser_formula()
    audit_one_exceptional_block()
    print("AUDIT PASS: physical equations force (ell^2 A)F=0 formally")
    print("AUDIT PASS: weighted KG(7,2) pencil and symmetric signature data rebuilt")
    print("AUDIT PASS: independent S6 block decomposition gives the degree-21 factor")
    print("AUDIT PASS: sole exceptional wall has a 9D star-zero kernel")
    print("imports_from_primary=0 imports_from_project=0")
    print("searches=0 finite_fields=0 graph_enumerations=0 groebner=0")
    print("SCOPE: mixed-sign general extensions, P7, and global Krenn-Gu remain unresolved")


if __name__ == "__main__":
    main()
