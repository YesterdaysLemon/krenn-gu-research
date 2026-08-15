"""Independent no-import audit of the triangle-pair rank-drop theorem."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations, product

Vector = tuple[int, ...]
Subspace = tuple[Vector, ...]

PRIME = 3
EDGES = tuple(combinations(range(4), 2))
FULL_MASK = (1 << 6) - 1

M1 = (1, -1, 0, -1, 0, 0)
M2 = (0, 0, 0, 0, 1, -1)
D0 = (0, 0, 0, 2, 0, 0)
D1 = (0, 0, 1, 0, 1, 0)
D2 = (0, 0, -1, 0, 0, 1)
B_BASIS = (M1, M2, D0, D1, D2)


def inverse(value: int, prime: int = PRIME) -> int:
    """Return a nonzero modular inverse."""
    return pow(value % prime, prime - 2, prime)


def rref(rows: list[Vector], width: int, prime: int = PRIME) -> Subspace:
    """Return a canonical modular row space."""
    matrix = [
        [value % prime for value in row]
        for row in rows
        if any(value % prime for value in row)
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
        matrix[pivot_row] = [value * scale % prime for value in matrix[pivot_row]]
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
    """Enumerate all requested subspaces of F_3^4."""
    nonzero = [vector for vector in product(range(PRIME), repeat=4) if any(vector)]
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
    return rref(
        [edge_product(first, second) for first in left for second in right],
        6,
    )


def complement_pair(left: Vector, right: Vector) -> int:
    """Evaluate the edge-complement pairing modulo three."""
    return sum(left[index] * right[5 - index] for index in range(6)) % PRIME


def orthogonal(left: Subspace, right: Subspace) -> bool:
    """Test orthogonality of two product spaces."""
    return all(complement_pair(x, y) == 0 for x in left for y in right)


def contained(left: Subspace, right: Subspace) -> bool:
    """Test subspace containment."""
    return len(rref([*right, *left], 4)) == len(right)


def hyperplane_normal(hyperplane: Subspace) -> Vector:
    """Return the normalized normal of a hyperplane in F_3^4."""
    pivots = [next(index for index, value in enumerate(row) if value) for row in hyperplane]
    free = next(index for index in range(4) if index not in pivots)
    normal = [0, 0, 0, 0]
    normal[free] = 1
    for row, pivot in zip(hyperplane, pivots, strict=True):
        normal[pivot] = -row[free] % PRIME
    first = next(value for value in normal if value)
    scale = inverse(first)
    return tuple(value * scale % PRIME for value in normal)


def coordinate_plane(space: Subspace) -> bool:
    """Test whether a plane is spanned by coordinate vectors."""
    support = {
        index for index in range(4) if any(vector[index] for vector in space)
    }
    return len(support) == 2 and all(
        sum(value != 0 for value in vector) == 1 for vector in space
    )


def hp_hhpp_profile_audit() -> dict[str, object]:
    """Exhaust HP equality, HHPP zeros, and the fixed high profiles over F_3."""
    planes = subspaces(2)
    hyperplanes = subspaces(3)
    assert len(planes) == 130
    assert len(hyperplanes) == 40

    equality: dict[tuple[int, int], Subspace] = {}
    candidates: dict[int, list[int]] = defaultdict(list)
    equality_types = Counter()
    for h_index, hyperplane in enumerate(hyperplanes):
        normal = hyperplane_normal(hyperplane)
        normal_support = {index for index, value in enumerate(normal) if value}
        for p_index, plane in enumerate(planes):
            hp_space = product_space(hyperplane, plane)
            assert len(hp_space) >= 3
            if len(hp_space) != 3:
                continue
            equality[h_index, p_index] = hp_space
            candidates[h_index].append(p_index)
            plane_support = {
                index
                for index in range(4)
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

    hhpp_types = Counter()
    for first_h, first_space in enumerate(hyperplanes):
        for second_h, second_space in enumerate(hyperplanes):
            common_planes = set(candidates[first_h]) & set(candidates[second_h])
            for first_p in common_planes:
                for second_p in common_planes:
                    if not orthogonal(
                        equality[first_h, first_p], equality[second_h, second_p]
                    ):
                        continue
                    if not orthogonal(
                        equality[first_h, second_p], equality[second_h, first_p]
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
                        hhpp_types["common_coordinate"] += 1
                    else:
                        assert plane_one == plane_two
                        assert coordinate_plane(plane_one)
                        first_support = {
                            index
                            for index, value in enumerate(hyperplane_normal(first_space))
                            if value
                        }
                        second_support = {
                            index
                            for index, value in enumerate(hyperplane_normal(second_space))
                            if value
                        }
                        assert first_support == second_support
                        assert len(first_support) == 2
                        hhpp_types["opposite_exceptional"] += 1
    assert hhpp_types == {"common_coordinate": 676, "opposite_exceptional": 12}

    h_bar = rref([(1, 0, 0, 1), (0, 1, 0, 0), (0, 0, 1, 0)], 4)
    h_bar_planes = [plane for plane in planes if contained(plane, h_bar)]
    assert len(h_bar_planes) == 13
    high_product = product_space(h_bar, h_bar)
    fixed_profile_zeros = {"HHHH": int(orthogonal(high_product, high_product))}
    fixed_profile_zeros["HHHP"] = sum(
        orthogonal(high_product, product_space(h_bar, plane))
        for plane in h_bar_planes
    )
    fixed_profile_zeros["HHPP"] = sum(
        orthogonal(high_product, product_space(first, second))
        for first in h_bar_planes
        for second in h_bar_planes
    )
    assert fixed_profile_zeros == {"HHHH": 0, "HHHP": 0, "HHPP": 0}
    return {
        "field": PRIME,
        "planes": len(planes),
        "hyperplanes": len(hyperplanes),
        "HP_equality_types": dict(equality_types),
        "HHPP_zero_types": dict(hhpp_types),
        "fixed_noncoordinate_high_zero_profiles": fixed_profile_zeros,
    }


def fraction_rref(rows: list[tuple[Fraction, ...]], width: int) -> tuple[tuple[Fraction, ...], ...]:
    """Canonical exact row reduction over the rationals."""
    matrix = [list(row) for row in rows if any(row)]
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                value - multiple * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return tuple(tuple(row) for row in matrix[:pivot_row])


def fraction_nullspace(rows: list[Vector], width: int) -> tuple[tuple[Fraction, ...], ...]:
    """Compute an exact rational nullspace basis."""
    reduced = fraction_rref(
        [tuple(Fraction(value) for value in row) for row in rows], width
    )
    pivots = [next(index for index, value in enumerate(row) if value) for row in reduced]
    free_columns = [index for index in range(width) if index not in pivots]
    basis = []
    for free in free_columns:
        vector = [Fraction(0) for _ in range(width)]
        vector[free] = Fraction(1)
        for row, pivot in zip(reduced, pivots, strict=True):
            vector[pivot] = -row[free]
        basis.append(tuple(vector))
    return tuple(basis)


def fraction_rank(rows: list[tuple[Fraction, ...]]) -> int:
    """Return exact rational row rank."""
    return len(fraction_rref(rows, len(rows[0]))) if rows else 0


def multiply_polynomials(
    left: dict[int, Fraction], right: dict[int, Fraction]
) -> dict[int, Fraction]:
    """Multiply sparse square-free polynomials exactly."""
    result: dict[int, Fraction] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = result.get(mask, Fraction(0)) + left_value * right_value
    return {mask: value for mask, value in result.items() if value}


def full_coefficient(quadratic: Vector, vectors: list[tuple[Fraction, ...]]) -> Fraction:
    """Extract the full coefficient of one quadratic and four linear forms."""
    polynomial = {
        (1 << first) | (1 << second): Fraction(value)
        for value, (first, second) in zip(quadratic, EDGES, strict=True)
        if value
    }
    for vector in vectors:
        linear = {
            1 << index: value for index, value in enumerate(vector) if value
        }
        polynomial = multiply_polynomials(polynomial, linear)
    return polynomial.get(FULL_MASK, Fraction(0))


def pair_and_hodge_audit() -> dict[str, object]:
    """Independently reconstruct the fixed pair and its five Hodge quartics."""
    left = (
        (0, 1, -1, 0),
        (0, 0, 0, 1),
        (-1, 0, 1, 0),
    )
    right = (
        (0, -1, 1, 0),
        (1, 1, 0, 0),
        (0, 0, 0, 1),
    )

    def integer_edge_product(first: Vector, second: Vector) -> Vector:
        return tuple(
            first[i] * second[j] + first[j] * second[i] for i, j in EDGES
        )

    zero = (0, 0, 0, 0, 0, 0)
    expected = (
        (D0, M1, M2),
        (tuple(-value for value in M2), D1, zero),
        (M1, tuple(-value for value in M1), D2),
    )
    table = tuple(
        tuple(integer_edge_product(first, second) for second in right)
        for first in left
    )
    assert table == expected
    assert fraction_rank(
        [tuple(Fraction(value) for value in row) for row in B_BASIS]
    ) == 5

    coordinate = [
        tuple(Fraction(index == position) for index in range(6))
        for position in range(6)
    ]

    def add(*vectors: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
        return tuple(sum(vector[index] for vector in vectors) for index in range(6))

    def scale(value: int, vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
        return tuple(value * entry for entry in vector)

    def linear_polynomial(vector: tuple[Fraction, ...]) -> dict[int, Fraction]:
        return {1 << index: value for index, value in enumerate(vector) if value}

    def factor_product(
        factors: tuple[tuple[Fraction, ...], ...], scalar: int
    ) -> dict[int, Fraction]:
        polynomial = {0: Fraction(scalar)}
        for factor in factors:
            polynomial = multiply_polynomials(polynomial, linear_polynomial(factor))
        return polynomial

    x0, x1, x2, x3, x4, x5 = coordinate
    ell1 = add(x2, scale(-1, x1), scale(-1, x0))
    ell2 = add(x2, scale(-1, x1))
    factorizations = {
        M1: (1, (x4, x5, x3, ell1)),
        M2: (1, (x4, x5, x0, ell2)),
        D0: (2, (x4, x5, x0, x3)),
        D1: (1, (x4, x5, x2, add(x0, x1))),
        D2: (1, (x4, x5, x1, add(x0, scale(-1, x2)))),
    }
    for quadratic, (scalar, factors) in factorizations.items():
        hodge = {
            FULL_MASK ^ ((1 << first) | (1 << second)): Fraction(value)
            for value, (first, second) in zip(quadratic, EDGES, strict=True)
            if value
        }
        assert hodge == factor_product(factors, scalar)
    return {"pair_product_rank": 5, "mixed_rank": 2, "Hodge_quartics": 5}


def sensor_table_audit() -> dict[str, object]:
    """Generate all sixteen common-factor sensors with rational arithmetic."""
    covectors = {
        "x3": (0, 0, 0, 1, 0, 0),
        "x4": (0, 0, 0, 0, 1, 0),
        "x5": (0, 0, 0, 0, 0, 1),
        "ell1": (-1, -1, 1, 0, 0, 0),
        "x0": (1, 0, 0, 0, 0, 0),
        "ell2": (0, -1, 1, 0, 0, 0),
    }
    rows = ("x3", "x4", "x5", "ell1")
    columns = ("x0", "x4", "x5", "ell2")
    expected = {
        "x3": (1, 0, 0, 2),
        "x4": (0, 0, 0, 0),
        "x5": (0, 0, 0, 0),
        "ell1": (1, 0, 0, 1),
    }
    ranks: dict[str, tuple[int, ...]] = {}
    for row_name in rows:
        row_ranks = []
        for column_name in columns:
            basis = fraction_nullspace(
                [covectors[row_name], covectors[column_name]], 6
            )
            sensor_rows = []
            for indices in combinations_with_replacement(range(len(basis)), 4):
                vectors = [basis[index] for index in indices]
                sensor_rows.append(
                    tuple(full_coefficient(quadratic, vectors) for quadratic in B_BASIS)
                )
            row_ranks.append(fraction_rank(sensor_rows))
        ranks[row_name] = tuple(row_ranks)
    assert ranks == expected
    return {"columns": columns, "rows": ranks}


def factor_evaluation(factor: Vector, vector: Vector, prime: int) -> int:
    """Evaluate one covector modulo a prime."""
    return sum(a * b for a, b in zip(factor, vector, strict=True)) % prime


def polarized_product(
    factors: tuple[Vector, ...], vectors: tuple[Vector, ...], prime: int
) -> int:
    """Evaluate one polarized four-factor product modulo a prime."""
    total = 0
    for order in permutations(range(4)):
        value = 1
        for row, column in enumerate(order):
            value *= factor_evaluation(factors[row], vectors[column], prime)
        total += value
    return total % prime


def contraction_audit() -> dict[str, object]:
    """Replay the N and variable-kernel contractions over three odd fields."""
    coordinate = [
        tuple(int(index == position) for index in range(6)) for position in range(6)
    ]
    x0, x1, x2, x3, x4, x5 = coordinate

    def add(*vectors: Vector) -> Vector:
        return tuple(sum(vector[index] for vector in vectors) for index in range(6))

    def scale(value: int, vector: Vector) -> Vector:
        return tuple(value * entry for entry in vector)

    factors = {
        "d0": (2, (x4, x5, x0, x3)),
        "d1": (1, (x4, x5, x2, add(x0, x1))),
        "d2": (1, (x4, x5, x1, add(x0, scale(-1, x2)))),
    }
    n_vector = add(x1, x2)
    checked: dict[int, int] = {}
    for prime in (3, 5, 7):
        count = 0
        for y in coordinate:
            for z in coordinate:
                j_value = (y[4] * z[5] + y[5] * z[4]) % prime
                n_values = {
                    name: scale_value
                    * polarized_product(rows, (n_vector, n_vector, y, z), prime)
                    % prime
                    for name, (scale_value, rows) in factors.items()
                }
                assert n_values["d0"] == 0
                assert n_values["d1"] == 2 * j_value % prime
                assert n_values["d2"] == -2 * j_value % prime
                count += 3
                for s_value in range(prime):
                    for t_value in range(prime):
                        k_s = add(x3, scale(s_value, n_vector))
                        k_t = add(x3, scale(t_value, n_vector))
                        values = {
                            name: scale_factor
                            * polarized_product(rows, (k_s, k_t, y, z), prime)
                            % prime
                            for name, (scale_factor, rows) in factors.items()
                        }
                        assert values["d0"] == 0
                        assert values["d1"] == 2 * s_value * t_value * j_value % prime
                        assert values["d2"] == -2 * s_value * t_value * j_value % prime
                        count += 3
        checked[prime] = count

    nonzero_two = [vector for vector in product(range(PRIME), repeat=2) if any(vector)]
    compatible_two = [
        (left, right)
        for left in nonzero_two
        for right in nonzero_two
        if all(left[index] * right[index] % PRIME == 0 for index in range(2))
    ]
    assert not any(
        all((triple[first], triple[second]) in compatible_two for first, second in combinations(range(3), 2))
        for triple in product(nonzero_two, repeat=3)
    )

    nonzero_three = [vector for vector in product(range(PRIME), repeat=3) if any(vector)]
    compatible_three = [
        (left, right)
        for left in nonzero_three
        for right in nonzero_three
        if all(left[index] * right[index] % PRIME == 0 for index in range(3))
    ]
    triples = [
        triple
        for triple in product(nonzero_three, repeat=3)
        if all(
            (triple[first], triple[second]) in compatible_three
            for first, second in combinations(range(3), 2)
        )
    ]
    assert triples
    assert all(
        all(sum(value != 0 for value in vector) == 1 for vector in triple)
        and {
            next(index for index, value in enumerate(vector) if value)
            for vector in triple
        }
        == {0, 1, 2}
        for triple in triples
    )
    assert not any(
        all(
            (quadruple[first], quadruple[second]) in compatible_three
            for first, second in combinations(range(4), 2)
        )
        for quadruple in product(nonzero_three, repeat=4)
    )
    return {
        "basis_checks_by_field": checked,
        "N_compatible_triples_over_F3": 0,
        "variable_kernel_triples_over_F3": len(triples),
        "variable_kernel_compatible_quadruples": 0,
    }


def j_geometry_audit() -> dict[str, object]:
    """Audit both J-radical contradictions over F_3."""
    planes = subspaces(2)
    hyperplanes = subspaces(3)

    def j_pair(left: Vector, right: Vector) -> int:
        return (left[1] * right[2] + left[2] * right[1]) % PRIME

    mutually_orthogonal = [
        (left, right)
        for left in hyperplanes
        for right in hyperplanes
        if all(j_pair(x, y) == 0 for x in left for y in right)
    ]
    radical = rref([(1, 0, 0, 0), (0, 0, 0, 1)], 4)
    assert len(mutually_orthogonal) == 4
    assert all(
        contained(radical, left) and contained(radical, right)
        for left, right in mutually_orthogonal
    )

    h_bar = rref([(1, 0, 0, 1), (0, 1, 0, 0), (0, 0, 1, 0)], 4)
    h_bar_planes = [plane for plane in planes if contained(plane, h_bar)]
    orthogonal_planes = [
        plane
        for plane in h_bar_planes
        if all(j_pair(x, y) == 0 for x in plane for y in h_bar)
    ]
    assert not orthogonal_planes
    return {
        "mutually_orthogonal_hyperplane_pairs": len(mutually_orthogonal),
        "all_contain_J_radical": True,
        "planes_P_in_Hbar_with_J(P,Hbar)=0": len(orthogonal_planes),
    }


def main() -> None:
    """Run all independent no-import audits."""
    pair = pair_and_hodge_audit()
    profiles = hp_hhpp_profile_audit()
    sensors = sensor_table_audit()
    contractions = contraction_audit()
    geometry = j_geometry_audit()
    print("triangle-pair two-sided projection-drop independent audit: PASS")
    print(f"  pair and Hodge reconstruction: {pair}")
    print(f"  HP/HHPP and fixed-high profiles: {profiles}")
    print(f"  rational sensor table: {sensors}")
    print(f"  contraction and support audit: {contractions}")
    print(f"  J geometry audit: {geometry}")


if __name__ == "__main__":
    main()
