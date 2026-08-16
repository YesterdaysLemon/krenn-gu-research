"""Primary exact checks for the co-two r=4 based-frame classification.

The characteristic-zero proof is the accompanying theorem document.  This
script derives the multiplication-dual equations, solves all projective
pivot charts exactly, enumerates the colour triples and stabilizer orbits,
and replays one integral frame for every ordered-pair orbit.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import sympy as sp

Vector = tuple[int, ...]
Basis = tuple[Vector, ...]
Point = tuple[Vector, Vector]
Permutation = tuple[int, ...]

EDGES = tuple(combinations(range(4), 2))


@dataclass(frozen=True)
class OrbitData:
    """Exact data for one admissible unbased r=4 orbit."""

    name: str
    normal_left: Vector
    normal_right: Vector
    left: Basis
    right: Basis
    equations: tuple[tuple[int, ...], ...]
    points: tuple[Point, ...]
    valid_triples: tuple[tuple[int, int, int], ...]
    ordered_generators: tuple[Permutation, ...]
    ordered_representatives: tuple[tuple[int, int, int], ...]
    ordered_sizes: tuple[int, ...]
    swap_generator: Permutation
    swap_representatives: tuple[tuple[int, int, int], ...]
    swap_sizes: tuple[int, ...]


@dataclass(frozen=True)
class Frame:
    """One integral based-frame representative."""

    orbit: str
    label: str
    point_indices: tuple[int, int, int]
    left: Basis
    right: Basis


def orbit_data() -> tuple[OrbitData, ...]:
    """Return the three exact rank-one catalogs and group actions."""

    return (
        OrbitData(
            "(3,1)",
            (1, 1, 1, 0),
            (1, -1, -1, 0),
            ((0, 1, -1, 0), (0, 0, 0, 1), (-1, 0, 1, 0)),
            ((0, -1, 1, 0), (1, 1, 0, 0), (0, 0, 0, 1)),
            (
                (0, 0, 1, 1, 0, 0, 0, 0, 0),
                (0, 0, 0, 0, 0, 1, 0, 0, 0),
                (0, -1, 0, 0, 0, 0, 1, 0, 0),
                (0, 1, 0, 0, 0, 0, 0, 1, 0),
            ),
            (
                ((0, 0, 1), (0, 0, 1)),
                ((0, 1, 0), (0, 1, 0)),
                ((1, 0, 0), (1, 0, 0)),
                ((1, 0, -1), (1, -1, 0)),
            ),
            ((0, 1, 2), (0, 1, 3)),
            ((0, 1, 3, 2),),
            ((0, 1, 2),),
            (2,),
            (1, 0, 3, 2),
            ((0, 1, 2),),
            (2,),
        ),
        OrbitData(
            "(4,1)",
            (1, 1, 1, 1),
            (1, -1, -1, -1),
            ((-1, 0, 1, 0), (1, 0, 0, -1), (0, 1, -1, 0)),
            ((1, 1, -1, 1), (1, 1, 0, 0), (0, -1, 1, 0)),
            (
                (0, 1, 1, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, 1, 0, 1, 0, 0, 0),
                (0, 2, 0, 1, 0, 0, 1, 0, 0),
                (0, 1, 0, 0, 0, 0, 0, 1, 0),
            ),
            (
                ((0, 0, 1), (0, 0, 1)),
                ((0, 1, 0), (0, 1, 0)),
                ((0, 1, -1), (1, 0, -1)),
                ((1, 0, 0), (1, 0, 0)),
                ((1, 0, -1), (2, 1, -1)),
                ((1, -1, -1), (1, 1, -1)),
            ),
            (
                (0, 1, 3),
                (0, 1, 4),
                (0, 1, 5),
                (0, 2, 4),
                (0, 2, 5),
                (0, 3, 5),
                (0, 4, 5),
                (1, 2, 3),
                (1, 2, 4),
                (1, 3, 4),
                (1, 3, 5),
                (2, 3, 4),
                (2, 3, 5),
                (2, 4, 5),
            ),
            (
                (4, 1, 5, 3, 0, 2),
                (0, 4, 3, 2, 1, 5),
            ),
            ((0, 1, 4), (0, 1, 3), (0, 2, 5), (2, 3, 5)),
            (1, 6, 6, 1),
            (5, 3, 4, 1, 2, 0),
            ((0, 1, 4), (0, 1, 3)),
            (2, 12),
        ),
        OrbitData(
            "(4,2)",
            (1, 1, 1, 1),
            (1, 1, -1, -1),
            ((1, 0, 0, -1), (0, 1, 0, -1), (0, 0, 1, -1)),
            ((0, 1, 1, 0), (1, 0, 1, 0), (0, 0, 1, -1)),
            (
                (0, -1, 1, 0, 0, 0, 0, 0, 0),
                (0, 0, 0, -1, 0, 1, 0, 0, 0),
                (0, 0, 0, 1, 0, 0, -1, 0, 0),
                (0, 1, 0, 0, 0, 0, 0, -1, 0),
            ),
            (
                ((0, 0, 1), (0, 0, 1)),
                ((0, 1, 0), (0, 1, 0)),
                ((0, 1, 1), (1, 0, 1)),
                ((1, 0, 0), (1, 0, 0)),
                ((1, 0, 1), (0, 1, 1)),
                ((1, 1, 1), (1, 1, 1)),
            ),
            (
                (0, 1, 3),
                (0, 1, 5),
                (0, 2, 4),
                (0, 2, 5),
                (0, 3, 5),
                (0, 4, 5),
                (1, 2, 3),
                (1, 2, 4),
                (1, 3, 4),
                (1, 3, 5),
                (2, 3, 4),
                (2, 4, 5),
            ),
            (
                (0, 3, 4, 1, 2, 5),
                (5, 1, 4, 3, 2, 0),
                (3, 5, 2, 0, 4, 1),
            ),
            ((0, 1, 3), (0, 2, 5), (0, 2, 4)),
            (4, 4, 4),
            (5, 3, 4, 1, 2, 0),
            ((0, 1, 3), (0, 2, 5), (0, 2, 4)),
            (4, 4, 4),
        ),
    )


def frames() -> tuple[Frame, ...]:
    """Return one integral frame for each ordered-pair orbit."""

    return (
        Frame(
            "(3,1)",
            "unique",
            (0, 1, 2),
            ((0, 1, -1, 0), (0, 0, 0, 1), (-1, 0, 1, 0)),
            ((0, -1, 1, 0), (1, 1, 0, 0), (0, 0, 0, 1)),
        ),
        Frame(
            "(4,1)",
            "k=3",
            (0, 1, 4),
            ((1, -1, 0, 0), (1, 0, 0, -1), (1, 0, -1, 0)),
            ((1, -1, 1, 1), (1, 1, 1, -1), (1, 1, -1, 1)),
        ),
        Frame(
            "(4,1)",
            "k=2 displayed",
            (0, 1, 3),
            ((-1, 0, 1, 0), (1, 0, 0, -1), (0, 1, -1, 0)),
            ((1, 1, -1, 1), (1, 1, 0, 0), (0, -1, 1, 0)),
        ),
        Frame(
            "(4,1)",
            "k=1",
            (0, 2, 5),
            ((1, -1, -1, 1), (0, 0, 1, -1), (1, 0, -1, 0)),
            ((1, 0, 0, 1), (0, 0, 1, -1), (1, 1, 0, 0)),
        ),
        Frame(
            "(4,1)",
            "k=0",
            (2, 3, 5),
            ((1, -1, 1, -1), (1, -1, -1, 1), (1, 1, -1, -1)),
            ((1, 0, 1, 0), (1, 0, 0, 1), (1, 1, 0, 0)),
        ),
        Frame(
            "(4,2)",
            "e=0 displayed",
            (0, 1, 3),
            ((1, 0, 0, -1), (0, 1, 0, -1), (0, 0, 1, -1)),
            ((0, 1, 1, 0), (1, 0, 1, 0), (0, 0, 1, -1)),
        ),
        Frame(
            "(4,2)",
            "e=1",
            (0, 2, 5),
            ((0, 1, -1, 0), (1, -1, 0, 0), (1, 0, 0, -1)),
            ((0, 1, 0, 1), (1, -1, 0, 0), (1, 0, 1, 0)),
        ),
        Frame(
            "(4,2)",
            "e=2",
            (0, 2, 4),
            ((1, 1, -1, -1), (0, 1, 0, -1), (1, 0, 0, -1)),
            ((1, 1, 1, 1), (0, 1, 1, 0), (1, 0, 1, 0)),
        ),
    )


def product(left: Vector, right: Vector) -> Vector:
    """Multiply two linear forms in the square-free degree-two algebra."""

    return tuple(
        left[i] * right[j] + left[j] * right[i] for i, j in EDGES
    )


def product_table(left: Basis, right: Basis) -> tuple[tuple[Vector, ...], ...]:
    """Return the three-by-three product table."""

    return tuple(tuple(product(u, v) for v in right) for u in left)


def rank(rows: list[Vector] | tuple[Vector, ...]) -> int:
    """Return exact rational row rank."""

    return int(sp.Matrix(rows).rank()) if rows else 0


def flattened(table: tuple[tuple[Vector, ...], ...]) -> list[Vector]:
    """Flatten a three-by-three table in row-major order."""

    return [table[i][j] for i in range(3) for j in range(3)]


def normalize(vector: sp.Matrix | Vector) -> tuple[sp.Expr, ...]:
    """Normalize a nonzero projective vector by its first nonzero entry."""

    values = [sp.sympify(value) for value in vector]
    pivot = next(value for value in values if value != 0)
    return tuple(sp.cancel(value / pivot) for value in values)


def equation_space(data: OrbitData) -> list[sp.Matrix]:
    """Derive the four bilinear equations defining rank-one membership."""

    table = product_table(data.left, data.right)
    edge_matrices = [
        [table[i][j][edge] for i in range(3) for j in range(3)]
        for edge in range(6)
    ]
    equations = sp.Matrix(edge_matrices).nullspace()
    assert len(equations) == 4
    expected = [sp.Matrix(row) for row in data.equations]
    observed_rows = sp.Matrix.hstack(*equations).T
    expected_rows = sp.Matrix.hstack(*expected).T
    assert observed_rows.rank() == expected_rows.rank() == 4
    assert sp.Matrix.vstack(observed_rows, expected_rows).rank() == 4
    return equations


def chart_solutions(equations: list[sp.Matrix]) -> set[Point]:
    """Solve all nine disjoint projective pivot charts exactly."""

    a = sp.symbols("a0:3")
    b = sp.symbols("b0:3")
    polynomials = [
        sp.expand(
            sum(eq[3 * i + j] * a[i] * b[j] for i in range(3) for j in range(3))
        )
        for eq in equations
    ]
    solutions: set[Point] = set()
    for pivot_a in range(3):
        for pivot_b in range(3):
            substitutions = {
                **{a[i]: 0 for i in range(pivot_a)},
                a[pivot_a]: 1,
                **{b[j]: 0 for j in range(pivot_b)},
                b[pivot_b]: 1,
            }
            unknowns = [*a[pivot_a + 1 :], *b[pivot_b + 1 :]]
            reduced = [sp.expand(poly.subs(substitutions)) for poly in polynomials]
            reduced = [poly for poly in reduced if poly != 0]
            if any(poly.is_number and poly != 0 for poly in reduced):
                answers: list[dict[sp.Symbol, sp.Expr]] = []
            elif not unknowns:
                answers = [{}]
            else:
                answers = sp.solve(reduced, unknowns, dict=True)
                assert all(
                    all(symbol in answer for symbol in unknowns) for answer in answers
                ), "positive-dimensional or unresolved chart"
            for answer in answers:
                def resolved(symbol: sp.Symbol) -> sp.Expr:
                    return substitutions[symbol] if symbol in substitutions else answer[symbol]

                left = tuple(
                    sp.cancel(resolved(symbol)) for symbol in a
                )
                right = tuple(
                    sp.cancel(resolved(symbol)) for symbol in b
                )
                solutions.add((left, right))
    return solutions


def group_closure(size: int, generators: tuple[Permutation, ...]) -> set[Permutation]:
    """Return the finite permutation group generated by the given actions."""

    identity = tuple(range(size))
    group = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            composite = tuple(generator[current[index]] for index in range(size))
            if composite not in group:
                group.add(composite)
                frontier.append(composite)
    return group


def triple_orbit(
    triple: tuple[int, int, int], group: set[Permutation]
) -> set[frozenset[int]]:
    """Return the unordered-triple orbit."""

    return {frozenset(action[index] for index in triple) for action in group}


def verify_catalog_and_actions(data: OrbitData) -> dict[str, object]:
    """Verify equations, complete catalog, spanning triples, and orbit counts."""

    assert rank(data.left) == rank(data.right) == 3
    assert all(
        sum(value * normal for value, normal in zip(row, data.normal_left, strict=True))
        == 0
        for row in data.left
    )
    assert all(
        sum(value * normal for value, normal in zip(row, data.normal_right, strict=True))
        == 0
        for row in data.right
    )
    table = product_table(data.left, data.right)
    assert rank(flattened(table)) == 5

    equations = equation_space(data)
    observed_points = chart_solutions(equations)
    expected_points = {
        (normalize(left), normalize(right)) for left, right in data.points
    }
    assert observed_points == expected_points

    valid = {
        tuple(indices)
        for indices in combinations(range(len(data.points)), 3)
        if rank([data.points[index][0] for index in indices]) == 3
        and rank([data.points[index][1] for index in indices]) == 3
    }
    assert valid == set(data.valid_triples)

    ordered_group = group_closure(len(data.points), data.ordered_generators)
    ordered_orbits = [
        triple_orbit(representative, ordered_group)
        for representative in data.ordered_representatives
    ]
    assert tuple(len(orbit) for orbit in ordered_orbits) == data.ordered_sizes
    assert set().union(*ordered_orbits) == {frozenset(triple) for triple in valid}
    assert sum(map(len, ordered_orbits)) == len(valid)

    swap_group = group_closure(
        len(data.points), (*data.ordered_generators, data.swap_generator)
    )
    swap_orbits = [
        triple_orbit(representative, swap_group)
        for representative in data.swap_representatives
    ]
    assert tuple(len(orbit) for orbit in swap_orbits) == data.swap_sizes
    assert set().union(*swap_orbits) == {frozenset(triple) for triple in valid}
    assert sum(map(len, swap_orbits)) == len(valid)

    return {
        "rank_one_points": len(data.points),
        "valid_colour_triples": len(valid),
        "ordered_group_order": len(ordered_group),
        "ordered_orbit_sizes": data.ordered_sizes,
        "swap_group_order": len(swap_group),
        "swap_orbit_sizes": data.swap_sizes,
    }


def coordinates_in_basis(frame: Basis, basis: Basis) -> sp.Matrix:
    """Return S with frame=S*basis for two row bases of one hyperplane."""

    frame_matrix = sp.Matrix(frame)
    basis_matrix = sp.Matrix(basis)
    right_inverse = basis_matrix.T * (basis_matrix * basis_matrix.T).inv()
    result = frame_matrix * right_inverse
    assert result * basis_matrix == frame_matrix
    return result


def frame_point_indices(frame: Frame, data: OrbitData) -> frozenset[int]:
    """Recover the paired dual rank-one points of an integral frame."""

    left_change = coordinates_in_basis(frame.left, data.left)
    right_change = coordinates_in_basis(frame.right, data.right)
    left_duals = left_change.inv()
    right_duals = right_change.inv()
    indices: list[int] = []
    for colour in range(3):
        point = (
            normalize(left_duals.col(colour)),
            normalize(right_duals.col(colour)),
        )
        index = next(
            index
            for index, (left, right) in enumerate(data.points)
            if point == (normalize(left), normalize(right))
        )
        indices.append(index)
    return frozenset(indices)


def verify_frame(frame: Frame, data: OrbitData) -> dict[str, object]:
    """Replay one integral frame and identify its catalog orbit."""

    assert rank(frame.left) == rank(frame.right) == 3
    assert all(
        sum(value * normal for value, normal in zip(row, data.normal_left, strict=True))
        == 0
        for row in frame.left
    )
    assert all(
        sum(value * normal for value, normal in zip(row, data.normal_right, strict=True))
        == 0
        for row in frame.right
    )
    table = product_table(frame.left, frame.right)
    mixed = [table[i][j] for i in range(3) for j in range(3) if i != j]
    diagonal = [table[i][i] for i in range(3)]
    assert rank(mixed) == 2
    assert rank(flattened(table)) == 5
    assert rank([*mixed, *diagonal]) == 5
    observed_indices = frame_point_indices(frame, data)
    assert observed_indices == frozenset(frame.point_indices)
    return {
        "label": frame.label,
        "points": tuple(sorted(observed_indices)),
        "mixed_rank": 2,
        "product_rank": 5,
    }


def main() -> None:
    """Run the complete exact primary verification."""

    data_by_name = {data.name: data for data in orbit_data()}
    catalogs = {
        name: verify_catalog_and_actions(data) for name, data in data_by_name.items()
    }
    frame_checks = [verify_frame(frame, data_by_name[frame.orbit]) for frame in frames()]

    print("co-two r=4 based-frame orbit classification primary: PASS")
    print(f"  catalogs={catalogs}")
    print(f"  integral_frames={frame_checks}")
    print("  ordered-pair orbit counts=(1,4,3)")
    print("  with omitted-mode swap=(1,2,3)")
    print("  full-extension transport: NOT CLAIMED")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
