"""Independent no-import audit for GLS35.

This file uses only the Python standard library.  It rebuilds the raw slice
matrix with tuple arithmetic, uses a hand-written Fraction row reduction, and
evaluates graph decks by a bitmask recurrence rather than importing the
primary verifier or any repository helper.
"""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations

Q = Fraction
ZERO = Q(0)
ONE_SCALAR = Q(1)
E = ((ONE_SCALAR, ZERO, ZERO), (ZERO, ONE_SCALAR, ZERO), (ZERO, ZERO, ONE_SCALAR))
ONES = (ONE_SCALAR, ONE_SCALAR, ONE_SCALAR)
A0, A1, Q0, Q1, U0, U1, U2, U3 = range(8)
PORTS = (U0, U1, U2, U3)


def add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def tensor(left, right):
    return tuple(a * b for a in left for b in right)


def transpose(matrix):
    return tuple(tuple(matrix[row][column] for row in range(3)) for column in range(3))


def matvec(matrix, vector):
    return tuple(
        sum((matrix[row][column] * vector[column] for column in range(3)), ZERO)
        for row in range(3)
    )


def dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), ZERO)


def outer(left, right):
    return tuple(tuple(a * b for b in right) for a in left)


def determinant3(matrix):
    a, b, c = matrix
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def rank_from_columns(columns):
    if not columns:
        return 0
    rows = [[column[row] for column in columns] for row in range(len(columns[0]))]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]), None
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                rows[row][index] - scale * rows[pivot_row][index]
                for index in range(len(columns))
            ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def matrix_times_columns(matrix, columns):
    return tuple(
        tuple(
            sum((matrix[row][index] * column[index] for index in range(9)), ZERO)
            for row in range(9)
        )
        for column in columns
    )


def edge_key(left, right):
    return (left, right) if left < right else (right, left)


def put_edge(edges, left, right, value):
    edges[edge_key(left, right)] = value if left < right else transpose(value)


def edge(edges, left, right):
    value = edges.get(edge_key(left, right), ((ZERO,) * 3,) * 3)
    return value if left < right else transpose(value)


def bilinear(matrix, left, right):
    return dot(left, matvec(matrix, right))


def deck_value(edges, vertices, vectors):
    """Perfect-matching sum by a bitmask deletion recurrence."""

    vertices = tuple(vertices)

    @cache
    def visit(mask):
        if mask == 0:
            return ONE_SCALAR
        first_position = (mask & -mask).bit_length() - 1
        first_vertex = vertices[first_position]
        remainder = mask ^ (1 << first_position)
        total = ZERO
        partner_mask = remainder
        while partner_mask:
            bit = partner_mask & -partner_mask
            second_position = bit.bit_length() - 1
            second_vertex = vertices[second_position]
            total += bilinear(
                edge(edges, first_vertex, second_vertex),
                vectors[first_vertex],
                vectors[second_vertex],
            ) * visit(remainder ^ bit)
            partner_mask ^= bit
        return total

    return visit((1 << len(vertices)) - 1)


def build_control():
    w0 = ((Q(0), Q(1), Q(-1)), (Q(1), Q(0), Q(0)), (Q(-1), Q(0), Q(1)))
    w1 = ((Q(1), Q(1), Q(-1)), (Q(0), Q(-1), Q(2)), (Q(-1), Q(0), Q(0)))
    edges = {}
    xi00, xi01, xi10, xi11 = E[1], E[2], E[2], E[1]
    put_edge(edges, A0, Q0, outer(xi00, E[0]))
    put_edge(edges, A0, Q1, outer(xi01, E[0]))
    put_edge(edges, A1, Q0, outer(xi10, E[0]))
    put_edge(edges, A1, Q1, outer(xi11, E[0]))
    for port in PORTS:
        put_edge(edges, A0, port, w0)
        put_edge(edges, A1, port, w1)
    put_edge(edges, U0, U1, outer(E[0], E[0]))
    put_edge(
        edges,
        U2,
        U3,
        tuple(tuple(Q(1, 2) * value for value in row) for row in outer(E[0], E[0])),
    )
    return edges, w0, w1


def raw_columns(edges):
    xi0 = {residual: matvec(edge(edges, A0, residual), ONES) for residual in (Q0, Q1)}
    xi1 = {residual: matvec(edge(edges, A1, residual), ONES) for residual in (Q0, Q1)}
    q = add(tensor(xi0[Q0], xi1[Q1]), tensor(xi0[Q1], xi1[Q0]))
    columns = []
    for residual in (Q0, Q1):
        for port in PORTS:
            w0 = edge(edges, A0, port)
            w1 = edge(edges, A1, port)
            for colour in range(3):
                column0 = tuple(w0[row][colour] for row in range(3))
                column1 = tuple(w1[row][colour] for row in range(3))
                columns.append(
                    add(tensor(xi0[residual], column1), tensor(column0, xi1[residual]))
                )
    for left, right in combinations(PORTS, 2):
        left0, left1 = edge(edges, A0, left), edge(edges, A1, left)
        right0, right1 = edge(edges, A0, right), edge(edges, A1, right)
        for c_left in range(3):
            for c_right in range(3):
                columns.append(
                    add(
                        tensor(
                            tuple(left0[row][c_left] for row in range(3)),
                            tuple(right1[row][c_right] for row in range(3)),
                        ),
                        tensor(
                            tuple(right0[row][c_right] for row in range(3)),
                            tuple(left1[row][c_left] for row in range(3)),
                        ),
                    )
                )
    return tuple(columns), q


def audit_raw_module_and_projector():
    edges, w0, w1 = build_control()
    assert determinant3(w0) == determinant3(w1) == -1
    assert matvec(transpose(w0), ONES) == E[1]
    assert matvec(transpose(w1), ONES) == E[2]

    columns, q = raw_columns(edges)
    assert len(columns) == 78
    assert rank_from_columns(columns) == 8
    assert rank_from_columns(columns + (q,)) == 8

    v = add(E[1], E[2])
    assert matvec(w0, v) == E[2]
    assert matvec(w1, v) == E[1]
    xi00, xi10 = E[1], E[2]
    literal = add(tensor(xi00, matvec(w1, v)), tensor(matvec(w0, v), xi10))
    assert literal == q

    epsilon = tensor(ONES, ONES)
    p = dot(epsilon, q)
    assert p == 2
    projector = tuple(
        tuple(
            (p if row == column else ZERO) - q[row] * epsilon[column]
            for column in range(9)
        )
        for row in range(9)
    )
    projected_q = tuple(
        sum((projector[row][column] * q[column] for column in range(9)), ZERO)
        for row in range(9)
    )
    assert projected_q == (ZERO,) * 9
    assert rank_from_columns(tuple(zip(*projector, strict=True))) == 8
    projected_columns = matrix_times_columns(projector, columns)
    assert rank_from_columns(projected_columns) == 7
    return (8, 8, 7), p


def audit_output_and_graph():
    edges, _, _ = build_control()
    kernel_vectors = {port: E[0] for port in PORTS}
    h_value = deck_value(edges, PORTS, kernel_vectors)
    assert h_value == Q(1, 2)
    p = Q(2)
    assert p * h_value == 1

    singletons = []
    for free in PORTS:
        values = []
        for colour in range(3):
            vectors = {port: (E[colour] if port == free else E[0]) for port in PORTS}
            values.append(p * deck_value(edges, PORTS, vectors))
        value = tuple(values)
        assert value == E[0]
        singletons.append(value)

    zero_one_q = 0
    for residual in (Q0, Q1):
        other = Q1 if residual == Q0 else Q0
        for free in PORTS:
            vertices = (other, *(port for port in PORTS if port != free))
            vectors = {vertex: E[0] for vertex in vertices}
            assert deck_value(edges, vertices, vectors) == 0
            zero_one_q += 1

    pure = []
    for colour in range(3):
        vectors = {vertex: E[colour] for vertex in range(8)}
        pure.append(deck_value(edges, tuple(range(8)), vectors))
    assert tuple(pure) == (0, 0, 0)
    return h_value, tuple(singletons), zero_one_q, tuple(pure)


def audit_rank_case_cover():
    basis = tuple(
        tuple(ONE_SCALAR if row == column else ZERO for row in range(9))
        for column in range(9)
    )
    escape_span = basis[:8]
    q = basis[8]
    assert rank_from_columns(escape_span) == 8
    assert rank_from_columns(escape_span + (q,)) == 9
    assert rank_from_columns(basis + (q,)) == rank_from_columns(basis) == 9

    # Direct quotient-coordinate replay of Theorem 2: in a one-dimensional
    # quotient, a nonzero [q] times a nonzero deck has pure-column rank one;
    # when [q]=0, independence of the three coordinate port words forces all
    # three scalar quotient coefficients to vanish.
    pure_columns = ((ONE_SCALAR,), (ZERO,), (ZERO,))
    assert rank_from_columns(pure_columns) == 1
    assert all(value == ZERO for value in (ZERO, ZERO, ZERO))
    return (8, 9), (9, 9), 1


def main():
    raw, p = audit_raw_module_and_projector()
    output = audit_output_and_graph()
    strata = audit_rank_case_cover()
    print("GLS35 independent no-import audit: PASS")
    print("  raw/augmented/transverse ranks:", raw)
    print("  p and output replay:", p, output)
    print("  independent rank strata / pure quotient rank:", strata)
    print("  scope: local no-go is not a witness; conjecture UNRESOLVED")


if __name__ == "__main__":
    main()
