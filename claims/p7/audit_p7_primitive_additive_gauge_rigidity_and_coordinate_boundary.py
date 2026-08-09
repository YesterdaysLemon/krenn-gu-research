"""Independent no-import audit of primitive P7 additive-gauge rigidity."""

from __future__ import annotations

import itertools
import math
from fractions import Fraction

N = 8
VERTICES = tuple(range(N))
EDGES = tuple(itertools.combinations(VERTICES, 2))
TRIPLES = tuple(itertools.combinations(VERTICES, 3))
Monomial = tuple[str, ...]
Polynomial = dict[Monomial, Fraction]
BooleanElement = dict[int, Polynomial]


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


def poly_scale(scalar: int | Fraction, value: Polynomial) -> Polynomial:
    """Scale a sparse formal polynomial."""
    factor = Fraction(scalar)
    return {
        monomial: factor * coefficient
        for monomial, coefficient in value.items()
        if factor * coefficient != 0
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


def sum_polynomials(values: list[Polynomial]) -> Polynomial:
    """Add a list of sparse polynomials."""
    out: Polynomial = {}
    for value in values:
        out = poly_add(out, value)
    return out


def boolean_add(left: BooleanElement, right: BooleanElement) -> BooleanElement:
    """Add elements of the square-free Boolean algebra."""
    out = {mask: dict(coefficient) for mask, coefficient in left.items()}
    for mask, coefficient in right.items():
        out[mask] = poly_add(out.get(mask, {}), coefficient)
        if not out[mask]:
            del out[mask]
    return out


def boolean_scale(scalar: int, value: BooleanElement) -> BooleanElement:
    """Scale a Boolean-algebra element."""
    return {
        mask: scaled
        for mask, coefficient in value.items()
        if (scaled := poly_scale(scalar, coefficient))
    }


def boolean_mul(left: BooleanElement, right: BooleanElement) -> BooleanElement:
    """Multiply modulo z_i^2=0."""
    out: BooleanElement = {}
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


def boolean_power(value: BooleanElement, power: int) -> BooleanElement:
    """Take a nonnegative Boolean-algebra power."""
    out: BooleanElement = {0: poly_constant(1)}
    for _ in range(power):
        out = boolean_mul(out, value)
    return out


def set_mask(vertices: tuple[int, ...] | set[int]) -> int:
    """Encode a vertex set as a bit mask."""
    out = 0
    for vertex in vertices:
        out |= 1 << vertex
    return out


def exact_rank(integer_matrix: list[list[int]]) -> int:
    """Compute matrix rank by independent rational elimination."""
    if not integer_matrix:
        return 0
    matrix = [[Fraction(entry) for entry in row] for row in integer_matrix]
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        pivot_value = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / pivot_value for entry in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def lefschetz_matrix(source_degree: int, power: int) -> list[list[int]]:
    """Build multiplication by ell^power between square-free degrees."""
    source = tuple(itertools.combinations(VERTICES, source_degree))
    target = tuple(itertools.combinations(VERTICES, source_degree + power))
    return [
        [
            math.factorial(power) if set(column).issubset(row) else 0
            for column in source
        ]
        for row in target
    ]


def support_matrix(support_size: int) -> list[list[int]]:
    """Build multiplication A_2 -> A_3 by a supported linear form."""
    support = set(range(support_size))
    return [
        [
            int(
                set(edge).issubset(triple)
                and next(iter(set(triple) - set(edge))) in support
            )
            for edge in EDGES
        ]
        for triple in TRIPLES
    ]


def inclusion_matrix(size: int, source_degree: int) -> list[list[int]]:
    """Build the one-step unsigned subset-inclusion matrix."""
    source = tuple(itertools.combinations(range(size), source_degree))
    target = tuple(itertools.combinations(range(size), source_degree + 1))
    return [
        [int(set(column).issubset(row)) for column in source]
        for row in target
    ]


def integer_matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    """Multiply two integer matrices independently."""
    right_columns = list(zip(*right, strict=True))
    return [
        [sum(a * b for a, b in zip(row, column, strict=True)) for column in right_columns]
        for row in left
    ]


def integer_linear_combination(
    terms: list[tuple[int, list[list[int]]]],
) -> list[list[int]]:
    """Form an integer linear combination of equally shaped matrices."""
    row_count = len(terms[0][1])
    column_count = len(terms[0][1][0])
    return [
        [
            sum(coefficient * matrix[row][column] for coefficient, matrix in terms)
            for column in range(column_count)
        ]
        for row in range(row_count)
    ]


def integer_identity(size: int) -> list[list[int]]:
    """Return an integer identity matrix."""
    return [[int(row == column) for column in range(size)] for row in range(size)]


def complemented_kneser_matrix() -> list[list[int]]:
    """Return twice the disjointness matrix on three-subsets."""
    return [
        [2 * int(not (set(row) & set(column))) for column in TRIPLES]
        for row in TRIPLES
    ]


def build_formal_data() -> tuple[
    BooleanElement,
    BooleanElement,
    BooleanElement,
    BooleanElement,
    dict[tuple[int, int], Polynomial],
    tuple[Polynomial, ...],
]:
    """Build ell, U, Q, and the directly gauged Q with formal coefficients."""
    b = {edge: poly_variable(f"b_{edge[0]}{edge[1]}") for edge in EDGES}
    u = tuple(poly_variable(f"u_{vertex}") for vertex in VERTICES)
    ell = {1 << vertex: poly_constant(1) for vertex in VERTICES}
    linear_u = {1 << vertex: u[vertex] for vertex in VERTICES}
    quad_b = {set_mask(edge): b[edge] for edge in EDGES}
    direct_gauged = {
        set_mask(edge): sum_polynomials([b[edge], u[edge[0]], u[edge[1]]])
        for edge in EDGES
    }
    return ell, linear_u, quad_b, direct_gauged, b, u


def audit_formal_transition() -> None:
    """Audit the gauge transition and all coordinate equations formally."""
    ell, linear_u, quad_b, direct_gauged, b, u = build_formal_data()
    assert direct_gauged == boolean_add(quad_b, boolean_mul(ell, linear_u))

    difference = boolean_mul(
        ell,
        boolean_add(
            boolean_power(direct_gauged, 2),
            boolean_scale(-1, boolean_power(quad_b, 2)),
        ),
    )
    obstruction = boolean_mul(
        linear_u,
        boolean_add(boolean_scale(2, quad_b), boolean_mul(ell, linear_u)),
    )
    assert difference == boolean_mul(boolean_power(ell, 2), obstruction)
    gauged_defect = boolean_mul(ell, boolean_power(direct_gauged, 2))
    base_defect = boolean_mul(ell, boolean_power(quad_b, 2))
    assert gauged_defect == boolean_add(
        base_defect, boolean_mul(boolean_power(ell, 2), obstruction)
    )

    for i, j, k in TRIPLES:
        expected = poly_scale(
            2,
            sum_polynomials(
                [
                    poly_mul(u[i], b[(j, k)]),
                    poly_mul(u[j], b[(i, k)]),
                    poly_mul(u[k], b[(i, j)]),
                    poly_mul(u[i], u[j]),
                    poly_mul(u[i], u[k]),
                    poly_mul(u[j], u[k]),
                ]
            ),
        )
        assert obstruction[set_mask((i, j, k))] == expected


def audit_boundary_coefficients() -> None:
    """Audit the forced zero edge outside every support of size at most four."""
    ell, _, quad_b, _, b, all_u = build_formal_data()
    for support_size in range(1, 5):
        support = set(range(support_size))
        outside = set(VERTICES) - support
        supported_u = {
            1 << vertex: all_u[vertex]
            for vertex in support
        }
        obstruction = boolean_mul(
            supported_u,
            boolean_add(boolean_scale(2, quad_b), boolean_mul(ell, supported_u)),
        )
        for inside_vertex in support:
            for outside_edge in itertools.combinations(sorted(outside), 2):
                expected = poly_scale(
                    2, poly_mul(all_u[inside_vertex], b[outside_edge])
                )
                mask = set_mask((inside_vertex, *outside_edge))
                assert obstruction[mask] == expected


def audit_star_boundary() -> None:
    """Audit the exact nontrivial boundary family."""
    ell = {1 << vertex: poly_constant(1) for vertex in VERTICES}
    star = {
        set_mask((0, vertex)): poly_variable(f"a_{vertex}")
        for vertex in range(1, N)
    }
    star_u = {1: poly_variable("lambda")}
    gauged_star = boolean_add(star, boolean_mul(ell, star_u))
    assert boolean_power(star, 2) == {}
    assert boolean_power(gauged_star, 2) == {}
    for vertex in range(1, N):
        expected = sum_polynomials(
            [poly_variable(f"a_{vertex}"), poly_variable("lambda")]
        )
        assert gauged_star[set_mask((0, vertex))] == expected
    for edge in itertools.combinations(range(1, N), 2):
        assert set_mask(edge) not in gauged_star


def main() -> None:
    """Run the independent exact audit."""
    audit_formal_transition()

    rank_3_5 = exact_rank(lefschetz_matrix(3, 2))
    rank_2_5 = exact_rank(lefschetz_matrix(2, 3))
    assert rank_3_5 == 56
    assert rank_2_5 == 28

    lefschetz_3_5 = lefschetz_matrix(3, 2)
    target_five_sets = tuple(itertools.combinations(VERTICES, 5))
    target_index = {target: index for index, target in enumerate(target_five_sets)}
    complemented_rows = []
    for triple in TRIPLES:
        complement = tuple(vertex for vertex in VERTICES if vertex not in triple)
        complemented_rows.append(lefschetz_3_5[target_index[complement]])
    kneser = complemented_kneser_matrix()
    assert complemented_rows == kneser

    kneser_squared = integer_matmul(kneser, kneser)
    kneser_cubed = integer_matmul(kneser_squared, kneser)
    kneser_fourth = integer_matmul(kneser_cubed, kneser)
    identity_56 = integer_identity(56)
    zero_56 = [[0 for _ in range(56)] for _ in range(56)]
    minimal_polynomial_value = integer_linear_combination(
        [
            (1, kneser_fourth),
            (-12, kneser_cubed),
            (-220, kneser_squared),
            (1056, kneser),
            (2880, identity_56),
        ]
    )
    assert minimal_polynomial_value == zero_56
    traces = tuple(
        sum(matrix[index][index] for index in range(56))
        for matrix in (kneser, kneser_squared, kneser_cubed)
    )
    assert traces == (0, 2240, 0)
    spectrum = {20: 1, -12: 7, 6: 20, -2: 28}
    assert sum(spectrum.values()) == 56
    for power, expected_trace in ((1, 0), (2, 2240), (3, 0)):
        assert sum(
            multiplicity * eigenvalue**power
            for eigenvalue, multiplicity in spectrum.items()
        ) == expected_trace
    determinant = math.prod(
        eigenvalue**multiplicity
        for eigenvalue, multiplicity in spectrum.items()
    )
    assert determinant == -(2**64) * 3**27 * 5
    inverse_numerator = integer_linear_combination(
        [
            (-1, kneser_cubed),
            (12, kneser_squared),
            (220, kneser),
            (-1056, identity_56),
        ]
    )
    assert integer_matmul(inverse_numerator, kneser) == [
        [2880 * entry for entry in row] for row in identity_56
    ]

    support_ranks = {
        support_size: exact_rank(support_matrix(support_size))
        for support_size in range(1, N + 1)
    }
    assert all(support_ranks[size] == 28 for size in range(5, 9))
    assert all(support_ranks[size] < 28 for size in range(1, 5))

    for support_size in range(5, 9):
        for source_degree in (0, 1, 2):
            matrix = inclusion_matrix(support_size, source_degree)
            column_count = math.comb(support_size, source_degree)
            assert exact_rank(matrix) == column_count

    audit_boundary_coefficients()
    audit_star_boundary()

    print("PASS: independent primitive additive-gauge rigidity audit")
    print(f"  rank(ell^2:A3->A5) = {rank_3_5}")
    print(f"  rank(ell^3:A2->A5) = {rank_2_5}")
    print("  spectrum(2 KG(8,3)) = 20^1, (-12)^7, 6^20, (-2)^28")
    print(f"  complemented determinant = {determinant}")
    print("  fixed cubic inverse for the quadratic Theta gauge system rebuilt")
    print(f"  support ranks A2->A3 = {support_ranks}")
    print("  formal transition and 56 quadratic equations rebuilt independently")
    print("  independent-complement obstruction and sharp boundary family pass")
    print("  primary verifier and project modules were not imported")


if __name__ == "__main__":
    main()
