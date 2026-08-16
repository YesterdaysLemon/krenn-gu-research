"""Independent no-import audit of the fixed-pair two-sided rank-drop theorem."""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, permutations, product

Vector = tuple[int, ...]
Subspace = tuple[Vector, ...]

PRIME = 3
EDGES = tuple(combinations(range(4), 2))


def inverse(value: int, prime: int = PRIME) -> int:
    """Return a nonzero modular inverse."""
    return pow(value % prime, prime - 2, prime)


def rref(rows: list[Vector], width: int, prime: int = PRIME) -> Subspace:
    """Canonical modular row space."""
    matrix = [list(value % prime for value in row) for row in rows if any(
        value % prime for value in row
    )]
    pivot_row = 0
    for column in range(width):
        pivot = next((
            row for row in range(pivot_row, len(matrix))
            if matrix[row][column] % prime
        ), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = inverse(matrix[pivot_row][column], prime)
        matrix[pivot_row] = [(value * scale) % prime for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column] % prime:
                continue
            scale = matrix[row][column] % prime
            matrix[row] = [
                (matrix[row][index] - scale * matrix[pivot_row][index]) % prime
                for index in range(width)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return tuple(tuple(row) for row in matrix[:pivot_row])


def subspaces(dimension: int) -> list[Subspace]:
    """Enumerate all subspaces of the requested dimension in F_3^4."""
    nonzero = [
        vector for vector in product(range(PRIME), repeat=4) if any(vector)
    ]
    spaces: set[Subspace] = set()
    for generators in combinations(nonzero, dimension):
        space = rref(list(generators), 4)
        if len(space) == dimension:
            spaces.add(space)
    return sorted(spaces)


def edge_product(left: Vector, right: Vector, prime: int = PRIME) -> Vector:
    """Multiply two forms in the four-variable square-free algebra."""
    return tuple(
        (left[first] * right[second] + left[second] * right[first]) % prime
        for first, second in EDGES
    )


def product_space(left: Subspace, right: Subspace) -> Subspace:
    """Return the degree-two product span."""
    return rref([
        edge_product(first, second)
        for first in left
        for second in right
    ], 6)


def complement_pair(left: Vector, right: Vector) -> int:
    """Evaluate the edge-complement pairing modulo three."""
    return sum(left[index] * right[5 - index] for index in range(6)) % PRIME


def orthogonal(left: Subspace, right: Subspace) -> bool:
    """Test orthogonality of two product spaces."""
    return all(complement_pair(x, y) == 0 for x in left for y in right)


def hyperplane_normal(hyperplane: Subspace) -> Vector:
    """Return the normalized normal of a three-space in F_3^4."""
    augmented = rref(list(hyperplane), 4)
    pivots = [next(index for index, value in enumerate(row) if value) for row in augmented]
    free = next(index for index in range(4) if index not in pivots)
    normal = [0] * 4
    normal[free] = 1
    for row, pivot in zip(augmented, pivots, strict=True):
        normal[pivot] = -row[free] % PRIME
    first = next(value for value in normal if value)
    scale = inverse(first)
    return tuple(value * scale % PRIME for value in normal)


def contained(left: Subspace, right: Subspace) -> bool:
    """Test whether left is contained in right."""
    return len(rref([*right, *left], 4)) == len(right)


def coordinate_plane(space: Subspace) -> bool:
    """Test whether a two-space is spanned by two coordinate vectors."""
    support = {
        index for index in range(4) if any(vector[index] for vector in space)
    }
    return len(support) == 2 and all(
        sum(value != 0 for value in vector) == 1 for vector in space
    )


def hp_and_hhpp_audit() -> dict[str, object]:
    """Exhaust HP equality and the (3,3,2,2) zero-permanent tuples over F_3."""
    planes = subspaces(2)
    hyperplanes = subspaces(3)
    assert len(planes) == 130
    assert len(hyperplanes) == 40

    equality: dict[tuple[int, int], Subspace] = {}
    equality_types = Counter()
    candidates: dict[int, list[int]] = defaultdict(list)
    for h_index, hyperplane in enumerate(hyperplanes):
        normal = hyperplane_normal(hyperplane)
        normal_support = {
            index for index, value in enumerate(normal) if value
        }
        for p_index, plane in enumerate(planes):
            hp_space = product_space(hyperplane, plane)
            assert len(hp_space) >= 3
            if len(hp_space) != 3:
                continue
            equality[h_index, p_index] = hp_space
            candidates[h_index].append(p_index)
            plane_support = {
                index for index in range(4)
                if any(vector[index] for vector in plane)
            }
            if len(normal_support) == 1 and contained(plane, hyperplane):
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
                    if not orthogonal(
                        equality[first_h, first_p],
                        equality[second_h, second_p],
                    ):
                        continue
                    if not orthogonal(
                        equality[first_h, second_p],
                        equality[second_h, first_p],
                    ):
                        continue
                    plane_one = planes[first_p]
                    plane_two = planes[second_p]
                    common_coordinate = any(
                        all(
                            vector[index] == 0
                            for space in (first_space, second_space, plane_one, plane_two)
                            for vector in space
                        )
                        for index in range(4)
                    )
                    if common_coordinate:
                        tuple_types["common_coordinate"] += 1
                    else:
                        assert plane_one == plane_two
                        assert coordinate_plane(plane_one)
                        first_normal = hyperplane_normal(first_space)
                        second_normal = hyperplane_normal(second_space)
                        first_support = {
                            index for index, value in enumerate(first_normal) if value
                        }
                        second_support = {
                            index for index, value in enumerate(second_normal) if value
                        }
                        assert first_support == second_support
                        assert len(first_support) == 2
                        tuple_types["opposite_exceptional"] += 1
    assert tuple_types == {
        "common_coordinate": 676,
        "opposite_exceptional": 12,
    }
    return {
        "field": PRIME,
        "planes": len(planes),
        "hyperplanes": len(hyperplanes),
        "HP_equality_types": dict(equality_types),
        "HHPP_zero_types": dict(tuple_types),
    }


def factor_evaluation(factor: Vector, vector: Vector, prime: int) -> int:
    """Evaluate a covector on a vector modulo prime."""
    return sum(x * y for x, y in zip(factor, vector, strict=True)) % prime


def polarized_product(factors: tuple[Vector, ...], vectors: tuple[Vector, ...], prime: int) -> int:
    """Evaluate a four-factor polarization modulo prime."""
    return sum(
        product_value(factors, vectors, order, prime)
        for order in permutations(range(4))
    ) % prime


def product_value(
    factors: tuple[Vector, ...],
    vectors: tuple[Vector, ...],
    order: tuple[int, ...],
    prime: int,
) -> int:
    """Evaluate one permanent summand."""
    value = 1
    for row, column in enumerate(order):
        value *= factor_evaluation(factors[row], vectors[column], prime)
    return value % prime


def contraction_audit() -> dict[str, object]:
    """Audit common-kernel contractions independently over three fields."""
    coordinate = [
        tuple(int(index == position) for index in range(6))
        for position in range(6)
    ]
    x0, x1, x2, x3, x4, x5 = coordinate

    def add(*vectors: Vector) -> Vector:
        return tuple(sum(vector[index] for vector in vectors) for index in range(6))

    def scale(value: int, vector: Vector) -> Vector:
        return tuple(value * entry for entry in vector)

    factors = {
        "m1": (x4, x5, x1, add(x3, scale(-1, x2), scale(-1, x0))),
        "m2": (x4, x5, x0, add(x3, scale(-1, x2), scale(-1, x1))),
        "d0": (x4, x5, add(x1, x2), add(x3, scale(-1, x0))),
        "d1": (x4, x5, add(x0, x2), add(x3, scale(-1, x1))),
        "d2": (x4, x5, x0, x1),
    }
    n_vector = add(x2, x3)
    ledgers: dict[int, int] = {}
    for prime in (3, 5, 7):
        checked = 0
        for y in coordinate:
            for z in coordinate:
                values = {
                    name: polarized_product(rows, (n_vector, n_vector, y, z), prime)
                    for name, rows in factors.items()
                }
                j_value = (y[4] * z[5] + y[5] * z[4]) % prime
                assert values["m1"] == values["m2"] == values["d2"] == 0
                assert values["d0"] == values["d1"] == 2 * j_value % prime
                checked += len(values)
        ledgers[prime] = checked

    nonzero_pairs = [
        vector for vector in product(range(PRIME), repeat=2) if any(vector)
    ]
    compatible = [
        (first, second)
        for first in nonzero_pairs
        for second in nonzero_pairs
        if first[0] * second[0] % PRIME == 0
        and first[1] * second[1] % PRIME == 0
    ]
    assert all(
        sum(value != 0 for value in first) == 1
        and sum(value != 0 for value in second) == 1
        and next(index for index, value in enumerate(first) if value)
        != next(index for index, value in enumerate(second) if value)
        for first, second in compatible
    )
    assert not any(
        all((first, second) in compatible for first, second in combinations(triple, 2))
        for triple in product(nonzero_pairs, repeat=3)
    )
    return {
        "basis_contractions_by_field": ledgers,
        "compatible_kernel_pairs_over_F3": len(compatible),
        "compatible_kernel_triples_over_F3": 0,
    }


def radical_audit() -> dict[str, object]:
    """Enumerate mutually J-orthogonal hyperplanes over F_3."""
    hyperplanes = subspaces(3)

    def j_pair(left: Vector, right: Vector) -> int:
        return (left[1] * right[2] + left[2] * right[1]) % PRIME

    pairs = [
        (left, right)
        for left in hyperplanes
        for right in hyperplanes
        if all(j_pair(x, y) == 0 for x in left for y in right)
    ]
    radical = rref([(1, 0, 0, 0), (0, 0, 0, 1)], 4)
    assert len(pairs) == 4
    assert all(contained(radical, left) and contained(radical, right) for left, right in pairs)
    return {
        "field": PRIME,
        "mutually_J_orthogonal_hyperplane_pairs": len(pairs),
        "all_contain_radical": True,
    }


def main() -> None:
    product_geometry = hp_and_hhpp_audit()
    contractions = contraction_audit()
    radical = radical_audit()

    print("fixed-pair two-sided projection-drop independent audit: PASS")
    print(f"  HP and HHPP exhaustive audit: {product_geometry}")
    print(f"  common-kernel contraction audit: {contractions}")
    print(f"  rank-two radical audit: {radical}")


if __name__ == "__main__":
    main()
