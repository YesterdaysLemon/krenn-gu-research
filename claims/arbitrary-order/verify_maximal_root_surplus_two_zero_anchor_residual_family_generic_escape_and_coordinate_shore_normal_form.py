"""Exact checks for the GLS27 residual-family shore normal forms."""

from __future__ import annotations

from collections import Counter

import sympy as sp


def tensor(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, right)


def in_span(columns: sp.Matrix, item: sp.Matrix) -> bool:
    return sp.Matrix.hstack(columns, item).rank() == columns.rank()


def pair_tensor(shore0: sp.Matrix, shore1: sp.Matrix) -> sp.Matrix:
    return tensor(shore0[:, 0], shore1[:, 1]) + tensor(shore0[:, 1], shore1[:, 0])


def matrix_from_tensor(item: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(3, 3, list(item))


def check_generic_escape() -> dict[str, object]:
    z, w = sp.symbols("z w", nonzero=True)
    e0, e1, e2 = sp.eye(3).columnspace()
    shore0 = sp.Matrix.hstack(e0 + z * e2, e1)
    shore1 = sp.Matrix.hstack(e0, e1 + w * e2)
    assert shore0.rank() == shore1.rank() == 2
    assert sp.factor(sp.Matrix.hstack(shore0, e2).det()) == 1
    assert sp.factor(sp.Matrix.hstack(shore1, e2).det()) == 1
    assert not in_span(shore0, e2)
    assert not in_span(shore1, e2)

    specialized0 = shore0.subs({z: 2})
    specialized1 = shore1.subs({w: 3})
    assert not in_span(specialized0, e2)
    assert not in_span(specialized1, e2)
    return {
        "generic_ranks": (shore0.rank(), shore1.rank()),
        "missing_colour": 2,
        "escape_product": 1,
    }


def check_normal_forms() -> dict[str, object]:
    t = sp.symbols("t")
    e0, e1, e2 = sp.eye(3).columnspace()

    c12_0 = sp.Matrix.hstack(e0, 2 * e0)
    c12_1 = sp.Matrix.hstack(e1, e2)
    q12 = matrix_from_tensor(pair_tensor(c12_0, c12_1))
    assert c12_0.rank() == 1
    assert c12_1.rank() == 2
    assert q12.rank() == 1
    assert all(q12[index, index] == 0 for index in range(3))
    assert all(in_span(c12_0, e0) or in_span(c12_1, e0) for _ in range(1))
    assert all(in_span(c12_0, basis) or in_span(c12_1, basis) for basis in (e0, e1, e2))

    v = e1 + t * e2
    c22_0 = sp.Matrix.hstack(e0, v)
    c22_1 = sp.Matrix.hstack(e1, e2)
    q22 = matrix_from_tensor(pair_tensor(c22_0, c22_1))
    assert c22_0.rank() == c22_1.rank() == 2
    assert q22.rank() == 2
    assert q22[:, 0] == sp.zeros(3, 1)
    assert sp.Matrix.hstack(*q22.columnspace()).rank() == 2
    assert sp.Matrix.hstack(*q22.T.columnspace()).rank() == 2
    assert all(in_span(c22_0, basis) or in_span(c22_1, basis) for basis in (e0, e1, e2))

    transpose_q12 = q12.T
    assert transpose_q12.rank() == 1
    assert all(transpose_q12[index, index] == 0 for index in range(3))
    return {
        "C12_rank": q12.rank(),
        "C21_rank": transpose_q12.rank(),
        "C22_rank": q22.rank(),
        "C22_zero_column": 0,
    }


ROOT_TABLE = (
    (1, 0, 2, None, 0, 2),
    (2, None, None, 1, 2, 0),
    (None, 1, 0, 2, None, 1),
    (0, 2, 1, 0, 1, None),
)
OUTSIDE_COLOURS = {
    (0, 1): 0,
    (0, 2): 2,
    (0, 3): 0,
    (0, 4): 2,
    (0, 5): 0,
    (1, 2): 1,
    (1, 3): 1,
    (1, 4): 2,
    (1, 5): 0,
    (2, 3): 0,
    (2, 4): 1,
    (2, 5): 2,
    (3, 4): 1,
    (3, 5): 0,
    (4, 5): 0,
}


def edge_colour(left: int, right: int) -> int | None:
    if left > right:
        left, right = right, left
    if right < 4:
        return None
    if left < 4:
        return ROOT_TABLE[left][right - 4]
    return OUTSIDE_COLOURS[(left - 4, right - 4)]


def matching_assignments(vertices: tuple[int, ...]) -> list[dict[int, int]]:
    if not vertices:
        return [{}]
    first = vertices[0]
    result = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        colour = edge_colour(first, second)
        if colour is None:
            continue
        remaining = vertices[1:index] + vertices[index + 1 :]
        for assignment in matching_assignments(remaining):
            result.append(assignment | {first: colour, second: colour})
    return result


def check_gld11_control() -> dict[str, object]:
    z00, _z01, _z02, z10, z11, z12 = sp.symbols("z00 z01 z02 z10 z11 z12", nonzero=True)
    e0, e1, e2 = sp.eye(3).columnspace()

    # Probe roots A=(r0,r2), residual columns Q=(q0,q1).
    shore0 = sp.Matrix.hstack(z00 * e0, z12 * e2)
    shore1 = sp.Matrix.hstack(sp.zeros(3, 1), z11 * e1)
    q = matrix_from_tensor(pair_tensor(shore0, shore1))
    assert shore0.rank() == 2
    assert shore1.rank() == 1
    assert q == z00 * z11 * (e0 * e1.T)
    assert q.rank() == 1
    assert all(
        in_span(shore0, basis) or in_span(shore1, basis) for basis in (e0, e1, e2)
    )
    p = sum(q)
    h = z00 * z10
    assert sp.factor(p - z00 * z11) == 0
    assert h != 0

    # The all-colour-one root-to-U injection r0-u0, r1-u3,
    # r2-u1, r3-u2 proves Pi_Q is nonzero.
    injection = ((0, 0), (1, 3), (2, 1), (3, 2))
    assert all(ROOT_TABLE[root][port] == 1 for root, port in injection)

    full_vertices = tuple(range(10))
    counter = Counter(
        tuple(assignment[vertex] for vertex in full_vertices)
        for assignment in matching_assignments(full_vertices)
    )
    mixed = tuple(int(digit) for digit in "1200100020")
    assert counter[mixed] == 1
    for colour in range(3):
        assert counter[(colour,) * 10] == 1

    return {
        "shore_ranks": (shore0.rank(), shore1.rank()),
        "p": p,
        "h": h,
        "Pi_Q_colour_one_injection": injection,
        "full_matching_terms": sum(counter.values()),
        "mixed_word_coefficient": counter[mixed],
    }


def main() -> None:
    escape = check_generic_escape()
    forms = check_normal_forms()
    control = check_gld11_control()
    print("zero-anchor residual-family primary checks: PASS")
    print("  generic escape:", escape)
    print("  coordinate-shore normal forms:", forms)
    print("  GLD11 maximum-root sharpness:", control)
    print("  scope: residual-family reduction only; attachment remains open")


if __name__ == "__main__":
    main()
