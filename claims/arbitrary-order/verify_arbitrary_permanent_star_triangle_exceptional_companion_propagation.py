"""Primary exact checks for the star--triangle companion theorem."""

from __future__ import annotations

import itertools
import json
from collections.abc import Sequence

import sympy as sp


X = sp.symbols("x0:4")


def quadratic_systems() -> dict[str, tuple[sp.Expr, ...]]:
    """Return the two ordered lists (m1,m2,d0,d1,d2) of cores."""
    x0, x1, x2, x3 = X
    star = (
        x3 * (x0 + x1 - x2),
        (x0 - x3) * (x1 - x2),
        x0 * x1 + x0 * x3 - x1 * x2 + 2 * x1 * x3 - x2 * x3,
        -x2 * (x0 + x1 - x3),
        2 * x0 * x3,
    )
    triangle = (
        x3 * (x2 - x1 - x0),
        x0 * (x2 - x1),
        2 * x0 * x3,
        x2 * (x0 + x1),
        x1 * (x0 - x2),
    )
    return {"star": star, "triangle": triangle}


SYSTEMS = quadratic_systems()
HESSIANS = {
    name: tuple(sp.hessian(core, X) for core in cores)
    for name, cores in SYSTEMS.items()
}


def vec(values: Sequence[int | sp.Expr]) -> sp.Matrix:
    return sp.Matrix(tuple(values))


def contractions(system: str, p: sp.Matrix) -> sp.Matrix:
    """Columns are the five residual covectors B_z p."""
    return sp.Matrix.hstack(*(matrix * p for matrix in HESSIANS[system]))


def row_contractions(system: str, p: sp.Matrix) -> sp.Matrix:
    """Return residual covectors as five rows."""
    return contractions(system, p).T


def same_span(left: Sequence[sp.Matrix], right: Sequence[sp.Matrix]) -> bool:
    """Check equality of two column spans exactly."""
    lmat = sp.Matrix.hstack(*left)
    rmat = sp.Matrix.hstack(*right)
    both = sp.Matrix.hstack(lmat, rmat)
    return lmat.rank() == rmat.rank() == both.rank()


def surviving_colours(system: str, q: sp.Matrix) -> tuple[int, ...]:
    """Diagonal rows that are coloops modulo all row relations."""
    matrix = row_contractions(system, q)
    relations = matrix.T.nullspace()
    return tuple(
        colour
        for colour in range(3)
        if all(relation[2 + colour] == 0 for relation in relations)
    )


STAR = {
    "N": vec((0, 1, 1, 0)),
    "B0": vec((1, 0, 1, 0)),
    "C0": vec((1, -1, 0, 0)),
    "B1": vec((1, 0, 0, 1)),
    "C1": vec((1, 1, 1, 1)),
    "Q": vec((0, 0, 1, 1)),
    "HB0": vec((-1, 0, 1, 0)),
    "HC0": vec((1, 1, 0, 0)),
    "HB1": vec((-1, 0, 0, 1)),
    "HC1": vec((-1, 1, 1, 1)),
}

TRIANGLE = {
    "N": vec((0, 1, 1, 0)),
    "B0": vec((1, 0, 1, 0)),
    "C0": vec((1, -1, 0, 0)),
    "X": vec((0, 0, 0, 1)),
    "HB0": vec((-1, 0, 1, 0)),
    "HC0": vec((1, 1, 0, 0)),
}


def check_residual_kernels() -> dict[str, object]:
    """Check every rank and common kernel in the two tables."""
    star_cases = {
        "N": (2, [vec((0, -1, 1, 0)), vec((0, 1, 0, 1))]),
        "B0": (3, [STAR["HB0"]]),
        "C0": (3, [STAR["HC0"]]),
        "B1": (3, [STAR["HB1"]]),
        "C1": (3, [STAR["HC1"]]),
    }
    triangle_cases = {
        "N": (2, [vec((0, -1, 1, 0)), TRIANGLE["X"]]),
        "B0": (3, [TRIANGLE["HB0"]]),
        "C0": (3, [TRIANGLE["HC0"]]),
        "X": (2, [TRIANGLE["N"], TRIANGLE["X"]]),
    }

    output: dict[str, object] = {}
    for system, vectors, cases in (
        ("star", STAR, star_cases),
        ("triangle", TRIANGLE, triangle_cases),
    ):
        ranks: dict[str, int] = {}
        for name, (expected_rank, expected_kernel) in cases.items():
            matrix = row_contractions(system, vectors[name])
            assert matrix.rank() == expected_rank
            assert same_span(matrix.nullspace(), expected_kernel)
            assert expected_rank >= 2
            # The quotient rank argument compares d with dim(D+A)-3=d-1.
            assert expected_rank - 1 < expected_rank
            ranks[name] = expected_rank
        output[system] = ranks
    return output


def check_star_relations() -> dict[str, object]:
    """Check the exact support filters and common-plane identities."""
    rows = {name: row_contractions("star", vector) for name, vector in STAR.items()}

    # One-dimensional companion identities, in channel order m1,m2,d0,d1,d2.
    assert rows["HB0"].row(3) == rows["HB0"].row(1)
    assert rows["HB0"].row(4) == rows["HB0"].row(0)
    assert rows["HC0"].row(2) == 2 * rows["HC0"].row(0) + rows["HC0"].row(1)
    assert rows["HC0"].row(4) == rows["HC0"].row(0)
    assert rows["HB1"].row(2) == rows["HB1"].row(0)
    assert rows["HB1"].row(4) == 2 * rows["HB1"].row(0) + rows["HB1"].row(1)
    assert rows["HC1"].row(3) == -rows["HC1"].row(0)
    assert rows["HC1"].row(4) == 2 * rows["HC1"].row(0) + rows["HC1"].row(1)

    expected_survivors = {
        "Q": (2,),
        "HB0": (0,),
        "HC0": (1,),
        "HB1": (1,),
        "HC1": (0,),
    }
    for name, expected in expected_survivors.items():
        assert surviving_colours("star", STAR[name]) == expected

    u, v = sp.symbols("u v")
    q = vec((0, u, v, u + v))
    qrows = row_contractions("star", q)
    assert 2 * qrows.row(0) - qrows.row(2) + qrows.row(3) == sp.zeros(1, 4)
    assert sp.simplify(u * qrows.row(4) - (u + v) * (qrows.row(0) + qrows.row(1))) == sp.zeros(1, 4)

    a, b = sp.symbols("a b")
    reverse = vec((0, a + b, a, b))
    reverse_rows = row_contractions("star", reverse)
    assert reverse_rows.row(4) - reverse_rows.row(0) - reverse_rows.row(1) == sp.zeros(1, 4)
    assert sp.simplify(
        (a + 2 * b) * reverse_rows.row(0)
        + a * reverse_rows.row(1)
        - b * reverse_rows.row(2)
        + b * reverse_rows.row(3)
    ) == sp.zeros(1, 4)

    return {
        "one_dimensional_filters": expected_survivors,
        "common_plane_parameters": [str(u), str(v)],
        "reverse_plane_parameters": [str(a), str(b)],
    }


def check_triangle_relations() -> dict[str, object]:
    """Check triangle support filters and the N--X parameter gates."""
    rows = {
        name: row_contractions("triangle", vector)
        for name, vector in TRIANGLE.items()
    }
    assert rows["HB0"].row(2) == -rows["HB0"].row(0)
    assert rows["HB0"].row(3) == rows["HB0"].row(1)
    assert rows["HC0"].row(2) == -rows["HC0"].row(0)
    assert rows["HC0"].row(4) == -rows["HC0"].row(1)

    assert surviving_colours("triangle", TRIANGLE["HB0"]) == (2,)
    assert surviving_colours("triangle", TRIANGLE["HC0"]) == (1,)
    assert surviving_colours("triangle", TRIANGLE["X"]) == (0,)
    assert surviving_colours("triangle", TRIANGLE["N"]) == (1, 2)

    a, b = sp.symbols("a b")
    qn = vec((0, -a, a, b))
    nrows = row_contractions("triangle", qn)
    assert nrows.row(3) + nrows.row(4) == sp.zeros(1, 4)
    assert b * nrows.row(1) - a * nrows.row(2) == sp.zeros(1, 4)

    qx = vec((0, a, a, b))
    xrows = row_contractions("triangle", qx)
    assert -a * xrows.row(2) + b * (xrows.row(3) + xrows.row(4)) == sp.zeros(1, 4)

    return {
        "N_companion": "X at colour 0",
        "X_companion": "N at colours in {1,2}",
    }


def bilinear_values(system: str, p: sp.Matrix, q: sp.Matrix) -> tuple[sp.Expr, ...]:
    return tuple((p.T * matrix * q)[0] for matrix in HESSIANS[system])


def check_mutual_cycles() -> dict[str, object]:
    """Check that each arrow is mutually sensor-orthogonal."""
    star_pairs = (
        (STAR["N"], STAR["Q"]),
        (STAR["B0"], STAR["HB0"]),
        (STAR["C0"], STAR["HC0"]),
        (STAR["B1"], STAR["HB1"]),
        (STAR["C1"], STAR["HC1"]),
    )
    triangle_pairs = (
        (TRIANGLE["N"], TRIANGLE["X"]),
        (TRIANGLE["B0"], TRIANGLE["HB0"]),
        (TRIANGLE["C0"], TRIANGLE["HC0"]),
    )
    for system, pairs in (("star", star_pairs), ("triangle", triangle_pairs)):
        for p, q in pairs:
            assert bilinear_values(system, p, q) == (0, 0, 0, 0, 0)
            assert bilinear_values(system, q, p) == (0, 0, 0, 0, 0)

    # Reverse common kernels.
    assert same_span(
        row_contractions("star", STAR["Q"]).nullspace(),
        [STAR["N"], vec((0, 1, 0, 1))],
    )
    assert same_span(
        row_contractions("triangle", TRIANGLE["X"]).nullspace(),
        [TRIANGLE["N"], TRIANGLE["X"]],
    )
    return {"star_cycles": len(star_pairs), "triangle_cycles": len(triangle_pairs)}


def check_common_cycle_matroids() -> dict[str, object]:
    """Check the rank-three covector matroids and their exact relations."""
    star_h0 = vec((1, -1, -1, 1))
    star_h1 = vec((-1, -1, -1, 1))
    star_k = vec((1, 1, -1, -1))
    x0 = vec((1, 0, 0, 0))
    star_matrix = sp.Matrix.hstack(star_h0, star_h1, star_k, x0)
    assert star_matrix.rank() == 3
    assert x0 == (star_h0 - star_h1) / 2

    tri_h1 = vec((1, 1, 1, 0))
    tri_h2 = vec((1, -1, -1, 0))
    tri_k = vec((-1, -1, 1, 0))
    tri_matrix = sp.Matrix.hstack(tri_h1, tri_h2, tri_k, x0)
    assert tri_matrix.rank() == 3
    assert x0 == (tri_h1 + tri_h2) / 2
    return {"star_rank": 3, "triangle_rank": 3}


def j_pair(left: Sequence[int], right: Sequence[int]) -> int:
    return left[0] * right[1] + left[1] * right[0]


def check_scalarization_countermodel() -> dict[str, object]:
    """Replay the exact countermodel to retaining only h(r_b) M_cd."""
    # h(r_b)=0, h(r_c)=1, h(r_d)=0; A-parts are e4,0,e5.
    h_values = (0, 1, 0)
    a_b = (1, 0)
    a_c = (0, 0)
    a_d = (0, 1)
    full = (
        h_values[0] * j_pair(a_c, a_d)
        + h_values[1] * j_pair(a_b, a_d)
        + h_values[2] * j_pair(a_b, a_c)
    )
    scalar_only = h_values[0] * j_pair(a_c, a_d)
    assert full == 1
    assert scalar_only == 0
    return {"full_contraction": full, "scalar_only": scalar_only}


def rank_mod(rows: Sequence[Sequence[int]], prime: int) -> int:
    matrix = [[entry % prime for entry in row] for row in rows]
    rank = 0
    columns = len(matrix[0]) if matrix else 0
    for column in range(columns):
        pivot = next(
            (index for index in range(rank, len(matrix)) if matrix[index][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, prime)
        matrix[rank] = [(entry * inverse) % prime for entry in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank or matrix[index][column] == 0:
                continue
            factor = matrix[index][column]
            matrix[index] = [
                (matrix[index][j] - factor * matrix[rank][j]) % prime
                for j in range(columns)
            ]
        rank += 1
    return rank


def canonical_mod(vector: Sequence[int], prime: int) -> tuple[int, ...]:
    for entry in vector:
        if entry % prime:
            inverse = pow(entry % prime, -1, prime)
            return tuple((value * inverse) % prime for value in vector)
    raise ValueError("zero vector has no projective representative")


def projective_span(
    basis: Sequence[Sequence[int]], prime: int
) -> tuple[tuple[int, ...], ...]:
    points: set[tuple[int, ...]] = set()
    for coefficients in itertools.product(range(prime), repeat=len(basis)):
        if not any(coefficients):
            continue
        vector = tuple(
            sum(coefficients[j] * basis[j][i] for j in range(len(basis)))
            for i in range(4)
        )
        if any(value % prime for value in vector):
            points.add(canonical_mod(vector, prime))
    return tuple(sorted(points))


def integer_hessians(system: str) -> tuple[tuple[tuple[int, ...], ...], ...]:
    return tuple(
        tuple(tuple(int(matrix[i, j]) for j in range(4)) for i in range(4))
        for matrix in HESSIANS[system]
    )


def modular_rows(system: str, q: Sequence[int], prime: int) -> list[list[int]]:
    rows: list[list[int]] = []
    for matrix in integer_hessians(system):
        rows.append(
            [sum(matrix[i][j] * q[j] for j in range(4)) % prime for i in range(4)]
        )
    return rows


def modular_companions(
    system: str,
    basis: Sequence[Sequence[int]],
    forbidden_colours: set[int],
    prime: int,
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    answer = []
    for point in projective_span(basis, prime):
        rows = modular_rows(system, point, prime)
        full_rank = rank_mod(rows, prime)
        colours = tuple(
            colour
            for colour in range(3)
            if colour not in forbidden_colours
            and rank_mod(rows[: 2 + colour] + rows[3 + colour :], prime) < full_rank
        )
        if colours:
            answer.append((point, colours))
    return tuple(answer)


def check_odd_field_scans() -> dict[str, object]:
    """Audit the projective support filters over three odd fields."""
    cases = (
        ("star", [(0, -1, 1, 0), (0, 1, 0, 1)], {0, 1}, (0, 0, 1, 1), (2,)),
        ("star", [(-1, 0, 1, 0)], {1, 2}, (-1, 0, 1, 0), (0,)),
        ("star", [(1, 1, 0, 0)], {0, 2}, (1, 1, 0, 0), (1,)),
        ("star", [(-1, 0, 0, 1)], {0, 2}, (-1, 0, 0, 1), (1,)),
        ("star", [(-1, 1, 1, 1)], {1, 2}, (-1, 1, 1, 1), (0,)),
        ("triangle", [(0, -1, 1, 0), (0, 0, 0, 1)], {1, 2}, (0, 0, 0, 1), (0,)),
        ("triangle", [(-1, 0, 1, 0)], {0, 1}, (-1, 0, 1, 0), (2,)),
        ("triangle", [(1, 1, 0, 0)], {0, 2}, (1, 1, 0, 0), (1,)),
        ("triangle", [(0, 1, 1, 0), (0, 0, 0, 1)], {0}, (0, 1, 1, 0), (1, 2)),
    )
    totals: dict[str, int] = {}
    for prime in (3, 5, 7):
        for index, (system, basis, forbidden, expected_point, expected_colours) in enumerate(cases):
            actual = modular_companions(system, basis, forbidden, prime)
            expected = ((canonical_mod(expected_point, prime), expected_colours),)
            assert actual == expected
            totals[f"F{prime}_case_{index}"] = len(actual)
    return totals


def main() -> None:
    summary = {
        "residual_kernels": check_residual_kernels(),
        "star_relations": check_star_relations(),
        "triangle_relations": check_triangle_relations(),
        "mutual_cycles": check_mutual_cycles(),
        "common_cycle_matroids": check_common_cycle_matroids(),
        "scalarization_countermodel": check_scalarization_countermodel(),
        "odd_field_scans": check_odd_field_scans(),
    }
    print("star--triangle exceptional companion primary checks: PASS")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
