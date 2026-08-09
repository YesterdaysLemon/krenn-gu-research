"""Independent stdlib audit of the P7 zeon harmonic-square theorem."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

Polynomial = dict[tuple[str, ...], Fraction]
BooleanForm = dict[int, Polynomial]
Matrix = list[list[Fraction]]
VERTICES = tuple(range(8))
EDGES = tuple(combinations(VERTICES, 2))
TRIPLES = tuple(combinations(VERTICES, 3))


def poly_constant(value: int | Fraction) -> Polynomial:
    coefficient = Fraction(value)
    return {(): coefficient} if coefficient else {}


def poly_variable(name: str) -> Polynomial:
    return {(name,): Fraction(1)}


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, Fraction(0)) + coefficient
        if not out[monomial]:
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
            if not out[monomial]:
                del out[monomial]
    return out


def poly_sum(values: list[Polynomial] | tuple[Polynomial, ...]) -> Polynomial:
    out: Polynomial = {}
    for value in values:
        out = poly_add(out, value)
    return out


def boolean_add(left: BooleanForm, right: BooleanForm) -> BooleanForm:
    out = {mask: dict(value) for mask, value in left.items()}
    for mask, value in right.items():
        out[mask] = poly_add(out.get(mask, {}), value)
        if not out[mask]:
            del out[mask]
    return out


def boolean_scale(value: int | Fraction, form: BooleanForm) -> BooleanForm:
    return {
        mask: scaled
        for mask, polynomial in form.items()
        if (scaled := poly_scale(value, polynomial))
    }


def boolean_mul(left: BooleanForm, right: BooleanForm) -> BooleanForm:
    out: BooleanForm = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            target = left_mask | right_mask
            out[target] = poly_add(
                out.get(target, {}), poly_mul(left_value, right_value)
            )
            if not out[target]:
                del out[target]
    return out


def partial(vertex: int, form: BooleanForm) -> BooleanForm:
    bit = 1 << vertex
    return {
        mask ^ bit: dict(value)
        for mask, value in form.items()
        if mask & bit
    }


def lowering(form: BooleanForm, vertices: tuple[int, ...]) -> BooleanForm:
    out: BooleanForm = {}
    for vertex in vertices:
        out = boolean_add(out, partial(vertex, form))
    return out


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
            if row == pivot_row or not work[row][column]:
                continue
            scalar = work[row][column]
            work[row] = [
                entry - scalar * pivot_entry
                for entry, pivot_entry in zip(
                    work[row], work[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def verify_leibniz_independently() -> None:
    vertices = tuple(range(3))
    masks = tuple(range(1 << len(vertices)))
    left = {
        mask: poly_variable(f"f{mask}")
        for mask in masks
    }
    right = {
        mask: poly_variable(f"g{mask}")
        for mask in masks
    }
    for vertex in vertices:
        expected = boolean_add(
            boolean_mul(partial(vertex, left), right),
            boolean_mul(left, partial(vertex, right)),
        )
        correction = boolean_scale(
            -2,
            boolean_mul(
                {1 << vertex: poly_constant(1)},
                boolean_mul(partial(vertex, left), partial(vertex, right)),
            ),
        )
        expected = boolean_add(expected, correction)
        assert partial(vertex, boolean_mul(left, right)) == expected


def verify_middle_kernels_independently() -> None:
    four_sets = tuple(combinations(VERTICES, 4))
    five_sets = tuple(combinations(VERTICES, 5))
    triples = tuple(combinations(VERTICES, 3))
    raising = [
        [Fraction(int(set(column) < set(row))) for column in four_sets]
        for row in five_sets
    ]
    lowering_matrix = [
        [Fraction(int(set(row) < set(column))) for column in four_sets]
        for row in triples
    ]
    assert exact_rank(raising) == exact_rank(lowering_matrix) == 56
    assert exact_rank(raising + lowering_matrix) == 56


def verify_contractions_independently() -> None:
    edge_value = {
        edge: poly_variable(f"b{edge[0]}{edge[1]}") for edge in EDGES
    }

    def b(left: int, right: int) -> Polynomial:
        return edge_value[tuple(sorted((left, right)))]

    q_form = {
        (1 << left) | (1 << right): value
        for (left, right), value in edge_value.items()
    }
    h_form = boolean_scale(Fraction(1, 2), boolean_mul(q_form, q_form))
    d_h = lowering(h_form, VERTICES)
    d_q = lowering(q_form, VERTICES)
    correction: BooleanForm = {}
    for vertex in VERTICES:
        correction = boolean_add(
            correction,
            boolean_mul(
                {1 << vertex: poly_constant(1)},
                boolean_mul(partial(vertex, q_form), partial(vertex, q_form)),
            ),
        )
    assert d_h == boolean_add(
        boolean_mul(q_form, d_q), boolean_scale(-1, correction)
    )

    row_sum = {
        vertex: poly_sum(
            [b(vertex, other) for other in VERTICES if other != vertex]
        )
        for vertex in VERTICES
    }
    total = poly_sum(list(row_sum.values()))
    triangle: dict[tuple[int, int, int], Polynomial] = {}
    for i, j, k in TRIPLES:
        left = poly_sum(
            [
                poly_mul(b(i, j), row_sum[k]),
                poly_mul(b(i, k), row_sum[j]),
                poly_mul(b(j, k), row_sum[i]),
            ]
        )
        right = poly_scale(
            2,
            poly_sum(
                [
                    poly_mul(b(i, j), b(i, k)),
                    poly_mul(b(i, j), b(j, k)),
                    poly_mul(b(i, k), b(j, k)),
                ]
            ),
        )
        expression = poly_add(left, poly_scale(-1, right))
        triangle[(i, j, k)] = expression
        triple_mask = (1 << i) | (1 << j) | (1 << k)
        assert d_h[triple_mask] == expression

    riccati: dict[tuple[int, int], Polynomial] = {}
    for i, j in EDGES:
        matrix_square = poly_sum(
            [
                poly_mul(b(i, k), b(k, j))
                for k in VERTICES
                if k not in (i, j)
            ]
        )
        coefficient = poly_add(
            poly_scale(Fraction(1, 2), total),
            poly_scale(-2, poly_add(row_sum[i], row_sum[j])),
        )
        residual = poly_sum(
            [
                matrix_square,
                poly_scale(-1, poly_mul(coefficient, b(i, j))),
                poly_scale(-1, poly_mul(row_sum[i], row_sum[j])),
                poly_scale(-2, poly_mul(b(i, j), b(i, j))),
            ]
        )
        riccati[(i, j)] = residual
        contracted = poly_sum(
            [
                triangle[tuple(sorted((i, j, k)))]
                for k in VERTICES
                if k not in (i, j)
            ]
        )
        assert poly_add(contracted, poly_scale(2, residual)) == {}

    vertex_residual: dict[int, Polynomial] = {}
    for i in VERTICES:
        br_i = poly_sum(
            [
                poly_mul(b(i, j), row_sum[j])
                for j in VERTICES
                if j != i
            ]
        )
        local_squares = poly_sum(
            [
                poly_mul(b(i, j), b(i, j))
                for j in VERTICES
                if j != i
            ]
        )
        radial = poly_mul(
            row_sum[i],
            poly_add(
                poly_scale(Fraction(1, 2), total),
                poly_scale(-1, row_sum[i]),
            ),
        )
        residual = poly_sum([br_i, poly_scale(-1, local_squares), poly_scale(-1, radial)])
        vertex_residual[i] = residual
        incident_riccati = poly_sum(
            [
                riccati[tuple(sorted((i, j)))]
                for j in VERTICES
                if j != i
            ]
        )
        assert poly_add(incident_riccati, poly_scale(-3, residual)) == {}

    casimir = poly_sum(
        [
            poly_mul(total, total),
            poly_scale(
                -4,
                poly_sum(
                    [poly_mul(value, value) for value in row_sum.values()]
                ),
            ),
            poly_scale(
                4,
                poly_sum(
                    [poly_mul(value, value) for value in edge_value.values()]
                ),
            ),
        ]
    )
    assert poly_add(
        poly_scale(2, poly_sum(list(vertex_residual.values()))), casimir
    ) == {}


def main() -> None:
    verify_leibniz_independently()
    verify_middle_kernels_independently()
    verify_contractions_independently()
    print("AUDIT PASS: independent corrected zeon Leibniz rule")
    print("AUDIT PASS: independent middle kernel equality, dimension 14")
    print("AUDIT PASS: harmonic-square, Riccati, vertex, and Casimir identities")
    print("imports_from_primary=0 imports_from_project=0")
    print("searches=0 finite_fields=0 graph_enumerations=0")
    print("SCOPE: complex primitive-square torus and global Krenn-Gu remain unresolved")


if __name__ == "__main__":
    main()
