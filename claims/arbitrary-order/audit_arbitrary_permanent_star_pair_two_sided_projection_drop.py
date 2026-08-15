"""Independent no-repository-import audit of the star-pair rank-drop theorem."""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement, product

Vector = tuple[int, ...]
Subspace = tuple[Vector, ...]

EDGES = tuple(combinations(range(4), 2))
PAIR = {
    "m1": (-1, 1, 0, 1, 0, 0),
    "m2": (1, -1, 0, 0, -1, 1),
    "d0": (-1, 2, -1, 1, 0, 1),
    "d1": (1, 0, -1, 0, -1, 0),
    "d2": (0, 0, 0, 2, 0, 0),
}
PROJECTIONS = {
    "x3": (0, 0, 0, 1, 0, 0),
    "x4": (0, 0, 0, 0, 1, 0),
    "x5": (0, 0, 0, 0, 0, 1),
    "ell1": (1, 1, -1, 0, 0, 0),
    "z0": (1, 0, 0, -1, 0, 0),
    "ell2": (0, 1, -1, 0, 0, 0),
}


def inverse(value: int, prime: int) -> int:
    """Return a modular inverse."""
    return pow(value % prime, prime - 2, prime)


def rref(rows: list[Vector], width: int, prime: int) -> Subspace:
    """Return a canonical row-space basis over a prime field."""
    matrix = [
        [entry % prime for entry in row]
        for row in rows
        if any(entry % prime for entry in row)
    ]
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column] % prime
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = inverse(matrix[pivot_row][column], prime)
        matrix[pivot_row] = [
            entry * scale % prime for entry in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column] % prime:
                continue
            scale = matrix[row][column]
            matrix[row] = [
                (matrix[row][index] - scale * matrix[pivot_row][index]) % prime
                for index in range(width)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return tuple(tuple(row) for row in matrix[:pivot_row])


def nullspace(rows: list[Vector], width: int, prime: int) -> Subspace:
    """Construct a basis of the right kernel over a prime field."""
    reduced = rref(rows, width, prime)
    pivots = [
        next(index for index, entry in enumerate(row) if entry)
        for row in reduced
    ]
    basis = []
    for free in (index for index in range(width) if index not in pivots):
        vector = [0] * width
        vector[free] = 1
        for row, pivot in zip(reduced, pivots, strict=True):
            vector[pivot] = -row[free] % prime
        basis.append(tuple(vector))
    return tuple(basis)


def edge_product(left: Vector, right: Vector, prime: int) -> Vector:
    """Multiply two four-variable forms in square-free degree two."""
    return tuple(
        (
            left[first] * right[second]
            + left[second] * right[first]
        )
        % prime
        for first, second in EDGES
    )


def sensor_value(quadratic: Vector, vectors: list[Vector], prime: int) -> int:
    """Extract x0...x5 from a quadratic times four linear forms."""
    state: dict[int, int] = {
        (1 << first) | (1 << second): coefficient % prime
        for coefficient, (first, second) in zip(quadratic, EDGES, strict=True)
        if coefficient % prime
    }
    for vector in vectors:
        following: dict[int, int] = {}
        for mask, coefficient in state.items():
            for index, entry in enumerate(vector):
                if not entry % prime or mask & (1 << index):
                    continue
                target = mask | (1 << index)
                following[target] = (
                    following.get(target, 0) + coefficient * entry
                ) % prime
        state = following
    return state.get((1 << 6) - 1, 0)


def pair_and_projection_audit() -> dict[str, object]:
    """Rebuild the star pair, ranks, and three common kernels."""
    u_rows = [(-1, 0, 1, 0), (1, 0, 0, -1), (0, 1, -1, 0)]
    v_rows = [(1, 1, -1, 1), (1, 1, 0, 0), (0, -1, 1, 0)]
    expected = [
        [PAIR["d0"], PAIR["m1"], tuple(-x for x in PAIR["m1"])],
        [PAIR["m2"], PAIR["d1"], tuple(-x for x in PAIR["m2"])],
        [
            tuple(-2 * PAIR["m1"][i] - PAIR["m2"][i] for i in range(6)),
            tuple(-x for x in PAIR["m1"]),
            PAIR["d2"],
        ],
    ]
    ledgers: dict[int, object] = {}
    phi1 = [PROJECTIONS[name] for name in ("x3", "x4", "x5", "ell1")]
    phi2 = [PROJECTIONS[name] for name in ("z0", "x4", "x5", "ell2")]
    common_kernel_rows = [
        [PROJECTIONS["ell1"], *phi2],
        [PROJECTIONS["z0"], *phi1],
        [PROJECTIONS["ell2"], *phi1],
    ]
    n_vector = (0, 1, 1, 0, 0, 0)
    for prime in (5, 7):
        products = [
            [edge_product(left, right, prime) for right in v_rows]
            for left in u_rows
        ]
        assert products == [
            [tuple(x % prime for x in entry) for entry in row]
            for row in expected
        ]
        all_products = [entry for row in products for entry in row]
        mixed = [products[i][j] for i in range(3) for j in range(3) if i != j]
        kernels = [nullspace(rows, 6, prime) for rows in common_kernel_rows]
        assert len(rref(all_products, 6, prime)) == 5
        assert len(rref(mixed, 6, prime)) == 2
        assert len(rref(phi1, 6, prime)) == len(rref(phi2, 6, prime)) == 4
        assert kernels == [(tuple(x % prime for x in n_vector),)] * 3
        ledgers[prime] = {
            "pair_rank": 5,
            "mixed_rank": 2,
            "projection_ranks": (4, 4),
            "common_kernel": n_vector,
        }
    return ledgers


def missing_factor_audit() -> dict[str, object]:
    """Recompute the sixteen common-factor sensor ranks over two fields."""
    expected = {
        "x3": [1, 0, 0, 2],
        "x4": [0, 0, 0, 0],
        "x5": [0, 0, 0, 0],
        "ell1": [3, 0, 0, 1],
    }
    tables: dict[int, dict[str, list[int]]] = {}
    quadratics = list(PAIR.values())
    for prime in (5, 7):
        table: dict[str, list[int]] = {}
        for phi in ("x3", "x4", "x5", "ell1"):
            row = []
            for psi in ("z0", "x4", "x5", "ell2"):
                basis = nullspace(
                    [PROJECTIONS[phi], PROJECTIONS[psi]],
                    6,
                    prime,
                )
                sensor_rows = []
                for indices in combinations_with_replacement(range(len(basis)), 4):
                    vectors = [basis[index] for index in indices]
                    sensor_rows.append([
                        sensor_value(q, vectors, prime) for q in quadratics
                    ])
                row.append(len(rref(sensor_rows, 5, prime)))
            table[phi] = row
        assert table == expected
        tables[prime] = table
    return {"columns": ("z0", "x4", "x5", "ell2"), "tables": tables}


def contraction_audit() -> dict[str, object]:
    """Audit the N contractions directly from coefficient extraction."""
    coordinate = [
        tuple(int(index == position) for index in range(6))
        for position in range(6)
    ]
    n_vector = (0, 1, 1, 0, 0, 0)
    ledgers = {}
    for prime in (5, 7):
        single_checks = 0
        for first in coordinate:
            for second in coordinate:
                for third in coordinate:
                    assert sensor_value(
                        PAIR["d2"],
                        [n_vector, first, second, third],
                        prime,
                    ) == 0
                    single_checks += 1
        double_checks = 0
        for first in coordinate:
            for second in coordinate:
                values = {
                    name: sensor_value(q, [n_vector, n_vector, first, second], prime)
                    for name, q in PAIR.items()
                }
                j_value = (
                    first[4] * second[5] + first[5] * second[4]
                ) % prime
                assert values["m1"] == values["m2"] == values["d2"] == 0
                assert values["d0"] == values["d1"] == -2 * j_value % prime
                double_checks += len(values)
        ledgers[prime] = {
            "single_d2_basis_triples": single_checks,
            "double_basis_values": double_checks,
        }
    return ledgers


def subspaces(dimension: int, prime: int = 3) -> list[Subspace]:
    """Enumerate all subspaces of the requested dimension in F_3^4."""
    nonzero = [vector for vector in product(range(prime), repeat=4) if any(vector)]
    spaces: set[Subspace] = set()
    for generators in combinations(nonzero, dimension):
        space = rref(list(generators), 4, prime)
        if len(space) == dimension:
            spaces.add(space)
    return sorted(spaces)


def product_space(left: Subspace, right: Subspace, prime: int = 3) -> Subspace:
    """Return the span of square-free products of two local subspaces."""
    return rref(
        [edge_product(first, second, prime) for first in left for second in right],
        6,
        prime,
    )


def complement_pair(left: Vector, right: Vector, prime: int = 3) -> int:
    """Evaluate the edge-complement pairing."""
    return sum(left[index] * right[5 - index] for index in range(6)) % prime


def contained(left: Subspace, right: Subspace, prime: int = 3) -> bool:
    """Test subspace containment."""
    return len(rref([*right, *left], 4, prime)) == len(right)


def coordinate_plane(space: Subspace) -> bool:
    """Recognize a coordinate two-plane."""
    support = {
        index for index in range(4) if any(vector[index] for vector in space)
    }
    return len(support) == 2 and all(
        sum(entry != 0 for entry in vector) == 1 for vector in space
    )


def hyperplane_normal(hyperplane: Subspace, prime: int = 3) -> Vector:
    """Return the normalized normal of an F_3 hyperplane."""
    reduced = rref(list(hyperplane), 4, prime)
    pivots = [next(index for index, entry in enumerate(row) if entry) for row in reduced]
    free = next(index for index in range(4) if index not in pivots)
    normal = [0] * 4
    normal[free] = 1
    for row, pivot in zip(reduced, pivots, strict=True):
        normal[pivot] = -row[free] % prime
    scale = inverse(next(entry for entry in normal if entry), prime)
    return tuple(entry * scale % prime for entry in normal)


def product_profile_audit() -> dict[str, object]:
    """Exhaust the HP equality and zero HHPP profiles over F_3."""
    prime = 3
    planes = subspaces(2, prime)
    hyperplanes = subspaces(3, prime)
    assert len(planes) == 130 and len(hyperplanes) == 40
    equality: dict[tuple[int, int], Subspace] = {}
    candidates: dict[int, list[int]] = defaultdict(list)
    equality_types = Counter()
    for h_index, hyperplane in enumerate(hyperplanes):
        normal = hyperplane_normal(hyperplane, prime)
        normal_support = {index for index, entry in enumerate(normal) if entry}
        for p_index, plane in enumerate(planes):
            hp_space = product_space(hyperplane, plane, prime)
            assert len(hp_space) >= 3
            if len(hp_space) != 3:
                continue
            equality[h_index, p_index] = hp_space
            candidates[h_index].append(p_index)
            plane_support = {
                index for index in range(4)
                if any(vector[index] for vector in plane)
            }
            if len(normal_support) == 1 and contained(plane, hyperplane, prime):
                equality_types["coordinate"] += 1
            elif (
                len(normal_support) == 2
                and plane_support == set(range(4)) - normal_support
                and coordinate_plane(plane)
            ):
                equality_types["support_two"] += 1
            else:
                raise AssertionError((normal, plane))
    assert equality_types == {"coordinate": 52, "support_two": 12}

    tuple_types = Counter()
    for first_h, first_space in enumerate(hyperplanes):
        for second_h, second_space in enumerate(hyperplanes):
            common_planes = set(candidates[first_h]) & set(candidates[second_h])
            for first_p in common_planes:
                for second_p in common_planes:
                    pairs = (
                        (equality[first_h, first_p], equality[second_h, second_p]),
                        (equality[first_h, second_p], equality[second_h, first_p]),
                    )
                    if not all(
                        all(
                            complement_pair(x, y, prime) == 0
                            for x in left
                            for y in right
                        )
                        for left, right in pairs
                    ):
                        continue
                    plane_one = planes[first_p]
                    plane_two = planes[second_p]
                    common_coordinate = any(
                        all(
                            vector[index] == 0
                            for space in (
                                first_space,
                                second_space,
                                plane_one,
                                plane_two,
                            )
                            for vector in space
                        )
                        for index in range(4)
                    )
                    if common_coordinate:
                        tuple_types["common_coordinate"] += 1
                    else:
                        assert plane_one == plane_two
                        assert coordinate_plane(plane_one)
                        first_support = {
                            index
                            for index, entry in enumerate(
                                hyperplane_normal(first_space, prime)
                            )
                            if entry
                        }
                        second_support = {
                            index
                            for index, entry in enumerate(
                                hyperplane_normal(second_space, prime)
                            )
                            if entry
                        }
                        assert first_support == second_support
                        assert len(first_support) == 2
                        tuple_types["opposite_exceptional"] += 1
    assert tuple_types == {"common_coordinate": 676, "opposite_exceptional": 12}
    return {
        "field": prime,
        "HP_equality_types": dict(equality_types),
        "HHPP_zero_types": dict(tuple_types),
    }


def radical_audit() -> dict[str, object]:
    """Enumerate all mutually J-orthogonal hyperplane pairs over F_3."""
    prime = 3
    hyperplanes = subspaces(3, prime)

    def j_pair(left: Vector, right: Vector) -> int:
        return (left[1] * right[2] + left[2] * right[1]) % prime

    pairs = [
        (left, right)
        for left in hyperplanes
        for right in hyperplanes
        if all(j_pair(x, y) == 0 for x in left for y in right)
    ]
    radical = rref([(1, 0, 0, 0), (0, 0, 0, 1)], 4, prime)
    assert len(pairs) == 4
    assert all(
        contained(radical, left, prime) and contained(radical, right, prime)
        for left, right in pairs
    )
    return {"field": prime, "pairs": len(pairs), "all_contain_radical": True}


def dangerous_cell_audit() -> dict[str, object]:
    """Check the rational square and rank-one-free cubic slice independently."""
    # A binary quadratic is recorded as coefficients of s^2, st, t^2.
    restricted = {
        "d0": (0, 1, -1),
        "d1": (0, -1, -1),
        "d2": (2, 0, 0),
    }
    integer_square = tuple(
        24 * restricted["d0"][index]
        + 48 * restricted["d1"][index]
        - restricted["d2"][index]
        for index in range(3)
    )
    assert integer_square == (-2, -24, -72)
    assert integer_square == tuple(-2 * entry for entry in (1, 12, 36))

    # Cubic monomial order:
    # r^3,r^2u,r^2v,ru^2,ruv,rv^2,u^3,u^2v,uv^2,v^3.
    slices = [
        (0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
        (0, 0, 1, 0, 0, 0, 0, 0, 0, 0),
        (0, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    ]
    ledgers = {}
    for prime in (5, 7):
        assert len(rref(slices, 10, prime)) == 3
        checked = 0
        survivors = 0
        for a, b, c in product(range(prime), repeat=3):
            if not (a or b or c):
                continue
            cube = (
                a**3,
                3 * a**2 * b,
                3 * a**2 * c,
                3 * a * b**2,
                6 * a * b * c,
                3 * a * c**2,
                b**3,
                3 * b**2 * c,
                3 * b * c**2,
                c**3,
            )
            if len(rref([*slices, cube], 10, prime)) == 3:
                survivors += 1
            checked += 1
        assert survivors == 0
        ledgers[prime] = {"nonzero_cubes_checked": checked, "survivors": 0}
    return {
        "restricted_diagonal_quadratics": restricted,
        "integer_square": "-2(s+6t)^2",
        "slice_rank": 3,
        "finite_field_cube_audits": ledgers,
    }


def main() -> None:
    pair = pair_and_projection_audit()
    missing = missing_factor_audit()
    contractions = contraction_audit()
    profiles = product_profile_audit()
    radical = radical_audit()
    dangerous = dangerous_cell_audit()

    print("star-pair two-sided projection-drop independent audit: PASS")
    print(f"  pair and projection audit: {pair}")
    print(f"  missing-factor tables: {missing}")
    print(f"  common-kernel contractions: {contractions}")
    print(f"  product-profile enumeration: {profiles}")
    print(f"  exceptional radical enumeration: {radical}")
    print(f"  dangerous-cell obstruction: {dangerous}")


if __name__ == "__main__":
    main()
