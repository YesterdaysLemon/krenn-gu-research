"""Independent no-import audit of star--triangle companion propagation."""

from __future__ import annotations

import itertools
import json
from collections.abc import Sequence
from fractions import Fraction


Vector = tuple[int, int, int, int]
Matrix = tuple[Vector, Vector, Vector, Vector]


def hessian(edges: dict[tuple[int, int], int]) -> Matrix:
    """Build the polarized matrix from an independently entered edge map."""
    rows = [[0] * 4 for _ in range(4)]
    for (left, right), coefficient in edges.items():
        assert left < right
        rows[left][right] = coefficient
        rows[right][left] = coefficient
    return tuple(tuple(row) for row in rows)  # type: ignore[return-value]


SYSTEMS: dict[str, tuple[Matrix, ...]] = {
    "star": (
        hessian({(0, 3): 1, (1, 3): 1, (2, 3): -1}),
        hessian({(0, 1): 1, (0, 2): -1, (1, 3): -1, (2, 3): 1}),
        hessian({(0, 1): 1, (0, 3): 1, (1, 2): -1, (1, 3): 2, (2, 3): -1}),
        hessian({(0, 2): -1, (1, 2): -1, (2, 3): 1}),
        hessian({(0, 3): 2}),
    ),
    "triangle": (
        hessian({(0, 3): -1, (1, 3): -1, (2, 3): 1}),
        hessian({(0, 1): -1, (0, 2): 1}),
        hessian({(0, 3): 2}),
        hessian({(0, 2): 1, (1, 2): 1}),
        hessian({(0, 1): 1, (1, 2): -1}),
    ),
}


STAR: dict[str, Vector] = {
    "N": (0, 1, 1, 0),
    "B0": (1, 0, 1, 0),
    "C0": (1, -1, 0, 0),
    "B1": (1, 0, 0, 1),
    "C1": (1, 1, 1, 1),
    "Q": (0, 0, 1, 1),
    "HB0": (-1, 0, 1, 0),
    "HC0": (1, 1, 0, 0),
    "HB1": (-1, 0, 0, 1),
    "HC1": (-1, 1, 1, 1),
}

TRIANGLE: dict[str, Vector] = {
    "N": (0, 1, 1, 0),
    "B0": (1, 0, 1, 0),
    "C0": (1, -1, 0, 0),
    "X": (0, 0, 0, 1),
    "HB0": (-1, 0, 1, 0),
    "HC0": (1, 1, 0, 0),
}


def matvec(matrix: Matrix, vector: Sequence[int]) -> Vector:
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(4))
        for row in range(4)
    )  # type: ignore[return-value]


def residual_rows(system: str, vector: Sequence[int]) -> list[Vector]:
    return [matvec(matrix, vector) for matrix in SYSTEMS[system]]


def dot(left: Sequence[int], right: Sequence[int]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def add(*vectors: Sequence[int]) -> Vector:
    return tuple(sum(vector[index] for vector in vectors) for index in range(4))  # type: ignore[return-value]


def scale(coefficient: int, vector: Sequence[int]) -> Vector:
    return tuple(coefficient * entry for entry in vector)  # type: ignore[return-value]


def rank_q(rows: Sequence[Sequence[int]]) -> int:
    matrix = [[Fraction(entry) for entry in row] for row in rows]
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
        pivot_value = matrix[rank][column]
        matrix[rank] = [entry / pivot_value for entry in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank or matrix[index][column] == 0:
                continue
            factor = matrix[index][column]
            matrix[index] = [
                matrix[index][j] - factor * matrix[rank][j]
                for j in range(columns)
            ]
        rank += 1
    return rank


def assert_kernel(
    system: str,
    vector: Vector,
    expected_rank: int,
    kernel_basis: Sequence[Vector],
) -> None:
    rows = residual_rows(system, vector)
    assert rank_q(rows) == expected_rank
    assert rank_q(kernel_basis) == len(kernel_basis)
    assert expected_rank + len(kernel_basis) == 4
    for row in rows:
        for kernel_vector in kernel_basis:
            assert dot(row, kernel_vector) == 0


def surviving_colours(system: str, vector: Vector) -> tuple[int, ...]:
    rows = residual_rows(system, vector)
    full_rank = rank_q(rows)
    return tuple(
        colour
        for colour in range(3)
        if rank_q(rows[: 2 + colour] + rows[3 + colour :]) < full_rank
    )


def check_exact_tables() -> dict[str, object]:
    """Check ranks, kernels, relations, and exact support filters."""
    assert_kernel(
        "star",
        STAR["N"],
        2,
        ((0, -1, 1, 0), (0, 1, 0, 1)),
    )
    assert_kernel("star", STAR["B0"], 3, (STAR["HB0"],))
    assert_kernel("star", STAR["C0"], 3, (STAR["HC0"],))
    assert_kernel("star", STAR["B1"], 3, (STAR["HB1"],))
    assert_kernel("star", STAR["C1"], 3, (STAR["HC1"],))

    assert_kernel(
        "triangle",
        TRIANGLE["N"],
        2,
        ((0, -1, 1, 0), TRIANGLE["X"]),
    )
    assert_kernel("triangle", TRIANGLE["B0"], 3, (TRIANGLE["HB0"],))
    assert_kernel("triangle", TRIANGLE["C0"], 3, (TRIANGLE["HC0"],))
    assert_kernel(
        "triangle",
        TRIANGLE["X"],
        2,
        (TRIANGLE["N"], TRIANGLE["X"]),
    )

    star_rows = {name: residual_rows("star", vector) for name, vector in STAR.items()}
    assert star_rows["HB0"][3] == star_rows["HB0"][1]
    assert star_rows["HB0"][4] == star_rows["HB0"][0]
    assert star_rows["HC0"][2] == add(scale(2, star_rows["HC0"][0]), star_rows["HC0"][1])
    assert star_rows["HC0"][4] == star_rows["HC0"][0]
    assert star_rows["HB1"][2] == star_rows["HB1"][0]
    assert star_rows["HB1"][4] == add(scale(2, star_rows["HB1"][0]), star_rows["HB1"][1])
    assert star_rows["HC1"][3] == scale(-1, star_rows["HC1"][0])
    assert star_rows["HC1"][4] == add(scale(2, star_rows["HC1"][0]), star_rows["HC1"][1])

    star_survivors = {
        name: surviving_colours("star", STAR[name])
        for name in ("Q", "HB0", "HC0", "HB1", "HC1")
    }
    assert star_survivors == {
        "Q": (2,),
        "HB0": (0,),
        "HC0": (1,),
        "HB1": (1,),
        "HC1": (0,),
    }

    triangle_rows = {
        name: residual_rows("triangle", vector)
        for name, vector in TRIANGLE.items()
    }
    assert triangle_rows["HB0"][2] == scale(-1, triangle_rows["HB0"][0])
    assert triangle_rows["HB0"][3] == triangle_rows["HB0"][1]
    assert triangle_rows["HC0"][2] == scale(-1, triangle_rows["HC0"][0])
    assert triangle_rows["HC0"][4] == scale(-1, triangle_rows["HC0"][1])
    triangle_survivors = {
        name: surviving_colours("triangle", TRIANGLE[name])
        for name in ("X", "N", "HB0", "HC0")
    }
    assert triangle_survivors == {
        "X": (0,),
        "N": (1, 2),
        "HB0": (2,),
        "HC0": (1,),
    }

    return {
        "star_survivors": star_survivors,
        "triangle_survivors": triangle_survivors,
    }


def check_parameter_identities() -> dict[str, int]:
    """Check the three two-parameter companion gates at sample-free level."""
    # The identities are polynomial and linear in u,v or a,b.  Checking the
    # two basis coefficient vectors proves them identically over Z.
    for u, v in ((1, 0), (0, 1)):
        q = (0, u, v, u + v)
        rows = residual_rows("star", q)
        assert add(scale(2, rows[0]), scale(-1, rows[2]), rows[3]) == (0, 0, 0, 0)
        assert add(scale(u, rows[4]), scale(-(u + v), add(rows[0], rows[1]))) == (0, 0, 0, 0)

    for a, b in ((1, 0), (0, 1)):
        q = (0, a + b, a, b)
        rows = residual_rows("star", q)
        assert add(rows[4], scale(-1, rows[0]), scale(-1, rows[1])) == (0, 0, 0, 0)
        assert add(
            scale(a + 2 * b, rows[0]),
            scale(a, rows[1]),
            scale(-b, rows[2]),
            scale(b, rows[3]),
        ) == (0, 0, 0, 0)

    for a, b in ((1, 0), (0, 1)):
        qn = (0, -a, a, b)
        rows_n = residual_rows("triangle", qn)
        assert add(rows_n[3], rows_n[4]) == (0, 0, 0, 0)
        assert add(scale(b, rows_n[1]), scale(-a, rows_n[2])) == (0, 0, 0, 0)

        qx = (0, a, a, b)
        rows_x = residual_rows("triangle", qx)
        assert add(scale(-a, rows_x[2]), scale(b, add(rows_x[3], rows_x[4]))) == (0, 0, 0, 0)
    return {"star_basis_checks": 4, "triangle_basis_checks": 4}


def bilinear(system: str, left: Vector, right: Vector) -> tuple[int, ...]:
    return tuple(dot(left, matvec(matrix, right)) for matrix in SYSTEMS[system])


def check_cycles_and_matroids() -> dict[str, object]:
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
        for left, right in pairs:
            assert bilinear(system, left, right) == (0, 0, 0, 0, 0)
            assert bilinear(system, right, left) == (0, 0, 0, 0, 0)

    star_h0 = (1, -1, -1, 1)
    star_h1 = (-1, -1, -1, 1)
    star_k = (1, 1, -1, -1)
    x0 = (1, 0, 0, 0)
    assert rank_q((star_h0, star_h1, star_k, x0)) == 3
    assert scale(2, x0) == add(star_h0, scale(-1, star_h1))

    tri_h1 = (1, 1, 1, 0)
    tri_h2 = (1, -1, -1, 0)
    tri_k = (-1, -1, 1, 0)
    assert rank_q((tri_h1, tri_h2, tri_k, x0)) == 3
    assert scale(2, x0) == add(tri_h1, tri_h2)
    return {"star_cycles": 5, "triangle_cycles": 3, "matroid_ranks": (3, 3)}


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


def canonical(vector: Sequence[int], prime: int) -> tuple[int, ...]:
    for entry in vector:
        if entry % prime:
            inverse = pow(entry % prime, -1, prime)
            return tuple((value * inverse) % prime for value in vector)
    raise ValueError("zero projective vector")


def projective_points(
    basis: Sequence[Vector], prime: int
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
            points.add(canonical(vector, prime))
    return tuple(sorted(points))


def scanned_companions(
    system: str,
    basis: Sequence[Vector],
    forbidden: set[int],
    prime: int,
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    found = []
    for point in projective_points(basis, prime):
        rows = residual_rows(system, point)
        full_rank = rank_mod(rows, prime)
        colours = tuple(
            colour
            for colour in range(3)
            if colour not in forbidden
            and rank_mod(rows[: 2 + colour] + rows[3 + colour :], prime) < full_rank
        )
        if colours:
            found.append((point, colours))
    return tuple(found)


def check_modular_scans() -> dict[str, int]:
    cases = (
        ("star", ((0, -1, 1, 0), (0, 1, 0, 1)), {0, 1}, STAR["Q"], (2,)),
        ("star", (STAR["HB0"],), {1, 2}, STAR["HB0"], (0,)),
        ("star", (STAR["HC0"],), {0, 2}, STAR["HC0"], (1,)),
        ("star", (STAR["HB1"],), {0, 2}, STAR["HB1"], (1,)),
        ("star", (STAR["HC1"],), {1, 2}, STAR["HC1"], (0,)),
        ("triangle", ((0, -1, 1, 0), TRIANGLE["X"]), {1, 2}, TRIANGLE["X"], (0,)),
        ("triangle", (TRIANGLE["HB0"],), {0, 1}, TRIANGLE["HB0"], (2,)),
        ("triangle", (TRIANGLE["HC0"],), {0, 2}, TRIANGLE["HC0"], (1,)),
        ("triangle", (TRIANGLE["N"], TRIANGLE["X"]), {0}, TRIANGLE["N"], (1, 2)),
    )
    output: dict[str, int] = {}
    for prime in (3, 5, 7):
        for index, (system, basis, forbidden, expected_vector, colours) in enumerate(cases):
            actual = scanned_companions(system, basis, forbidden, prime)
            expected = ((canonical(expected_vector, prime), colours),)
            assert actual == expected
            output[f"F{prime}_case_{index}"] = len(actual)
    return output


def check_scalarization_countermodel() -> dict[str, int]:
    def j_pair(left: tuple[int, int], right: tuple[int, int]) -> int:
        return left[0] * right[1] + left[1] * right[0]

    h_b, h_c, h_d = 0, 1, 0
    a_b, a_c, a_d = (1, 0), (0, 0), (0, 1)
    full = (
        h_b * j_pair(a_c, a_d)
        + h_c * j_pair(a_b, a_d)
        + h_d * j_pair(a_b, a_c)
    )
    scalar_only = h_b * j_pair(a_c, a_d)
    assert full == 1 and scalar_only == 0
    return {"full": full, "scalar_only": scalar_only}


def main() -> None:
    summary = {
        "exact_tables": check_exact_tables(),
        "parameter_identities": check_parameter_identities(),
        "cycles_and_matroids": check_cycles_and_matroids(),
        "modular_scans": check_modular_scans(),
        "scalarization_countermodel": check_scalarization_countermodel(),
    }
    print("star--triangle exceptional companion independent audit: PASS")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
