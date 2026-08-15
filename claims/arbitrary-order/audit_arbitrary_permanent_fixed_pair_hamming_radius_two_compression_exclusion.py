"""Independent no-import audit of the W/V radius-two compression exclusion."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product

Vector = tuple[int, ...]
Pair = tuple[int, int]
Array = tuple[Pair, Pair, Pair]

EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
FULL_MASK = (1 << 6) - 1

M1 = (0, 1, -1, 0, 0, -1)
M2 = (0, 0, 0, 1, -1, -1)
D0 = (1, 1, 0, 0, -1, -1)
D1 = (1, 0, -1, 1, 0, -1)
D2 = (0, 0, 0, 0, 0, -2)


def sparse_linear(vector: Vector, prime: int) -> dict[int, int]:
    """Encode a linear form modulo a prime."""
    return {
        1 << index: value % prime
        for index, value in enumerate(vector)
        if value % prime
    }


def sparse_quadratic(vector: Vector, prime: int) -> dict[int, int]:
    """Encode a first-four-variable quadratic modulo a prime."""
    return {
        (1 << first) | (1 << second): value % prime
        for value, (first, second) in zip(vector, EDGES, strict=True)
        if value % prime
    }


def sparse_multiply(
    left: dict[int, int],
    right: dict[int, int],
    prime: int,
) -> dict[int, int]:
    """Multiply in the square-free algebra modulo a prime."""
    result: dict[int, int] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = (
                result.get(mask, 0) + left_value * right_value
            ) % prime
    return {mask: value for mask, value in result.items() if value}


def full_coefficient(
    quadratic: Vector,
    linear_vectors: list[Vector],
    prime: int,
) -> int:
    """Compute one full square-free coefficient modulo a prime."""
    result = sparse_quadratic(quadratic, prime)
    for vector in linear_vectors:
        result = sparse_multiply(result, sparse_linear(vector, prime), prime)
    return result.get(FULL_MASK, 0)


def j_pair(left: Pair, right: Pair, prime: int) -> int:
    """Evaluate J on the two special-coordinate vectors."""
    return (left[0] * right[1] + left[1] * right[0]) % prime


def c_value(
    r_vectors: list[Pair],
    a_vectors: list[Pair],
    prime: int,
) -> Pair:
    """Evaluate the R-valued trilinear map C modulo a prime."""
    result = [0, 0]
    for mode in range(3):
        others = [index for index in range(3) if index != mode]
        scalar = j_pair(a_vectors[others[0]], a_vectors[others[1]], prime)
        result[0] = (result[0] + r_vectors[mode][0] * scalar) % prime
        result[1] = (result[1] + r_vectors[mode][1] * scalar) % prime
    return result[0], result[1]


def basis_tensor_audit() -> dict[str, object]:
    """Check every W^3 x V basis entry of all five sensors over three fields."""
    w_vectors = [
        (0, 1, 0, 1, 0, 0),
        (0, 0, 1, 1, 0, 0),
        (0, 0, 0, 0, 1, 0),
        (0, 0, 0, 0, 0, 1),
    ]
    w_r = [(1, 0), (0, 1), (0, 0), (0, 0)]
    w_a = [(0, 0), (0, 0), (1, 0), (0, 1)]
    v_vectors = [
        (1, 0, 0, 1, 0, 0),
        (0, 1, 0, -1, 0, 0),
        (0, 0, 1, 1, 0, 0),
    ]
    v_coordinates = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    quadratics = (M1, M2, D0, D1, D2)

    ledgers: dict[int, int] = {}
    for prime in (3, 5, 7):
        checked = 0
        for word in product(range(4), repeat=3):
            r_vectors = [w_r[index] for index in word]
            a_vectors = [w_a[index] for index in word]
            c_result = c_value(r_vectors, a_vectors, prime)
            p_values = (
                (c_result[0] + c_result[1]) % prime,
                c_result[1],
                c_result[0],
            )
            for v_index, z in enumerate(v_vectors):
                gamma, delta, epsilon = v_coordinates[v_index]
                q_values = (
                    epsilon % prime,
                    (gamma - delta + epsilon) % prime,
                    gamma % prime,
                )
                actual = tuple(
                    full_coefficient(
                        quadratic,
                        [*(w_vectors[index] for index in word), z],
                        prime,
                    )
                    for quadratic in quadratics
                )
                expected = (
                    0,
                    0,
                    2 * q_values[0] * p_values[0],
                    2 * q_values[1] * p_values[1],
                    -2 * q_values[2] * p_values[2],
                )
                assert actual == tuple(value % prime for value in expected)
                checked += len(quadratics)
        assert checked == 4**3 * 3 * 5
        ledgers[prime] = checked
    return {
        "basis_tensor_entries_by_field": ledgers,
        "multilinear_domain_dimensions": (4, 4, 4, 3),
    }


def shell_audit() -> dict[str, object]:
    """Independently count the 54 equations and check the p-row cover."""
    p_rows = ((1, 1), (0, 1), (1, 0))
    shell_counts: Counter[tuple[int, int]] = Counter()
    cover_histogram: Counter[int] = Counter()

    for anchor in range(3):
        for word in product(range(3), repeat=3):
            distance = sum(colour != anchor for colour in word)
            if distance in (1, 2):
                shell_counts[(anchor, distance)] += 1

    for word in product(range(3), repeat=3):
        if len(set(word)) == 1:
            continue
        anchors = [
            anchor
            for anchor in range(3)
            if sum(colour != anchor for colour in word) in (1, 2)
        ]
        determinants = [
            p_rows[first][0] * p_rows[second][1]
            - p_rows[first][1] * p_rows[second][0]
            for first, second in combinations(anchors, 2)
        ]
        assert any(determinant != 0 for determinant in determinants)
        cover_histogram[len(anchors)] += 1

    assert sum(shell_counts.values()) == 54
    assert cover_histogram == {2: 18, 3: 6}
    return {
        "shell_counts": dict(sorted(shell_counts.items())),
        "nonconstant_anchor_cover": dict(sorted(cover_histogram.items())),
    }


def array_rank(array: Array, prime: int) -> int:
    """Return the span dimension of three columns in a two-space."""
    if all(vector == (0, 0) for vector in array):
        return 0
    for first, second in combinations(range(3), 2):
        determinant = (
            array[first][0] * array[second][1]
            - array[first][1] * array[second][0]
        ) % prime
        if determinant:
            return 2
    return 1


def compatible(first: Array, second: Array, prime: int) -> bool:
    """Check all off-diagonal J-orthogonality equations for two arrays."""
    return all(
        j_pair(first[left], second[right], prime) == 0
        for left in range(3)
        for right in range(3)
        if left != right
    )


def diagonal_can_be_nonzero(arrays: tuple[Array, Array, Array], prime: int) -> bool:
    """Check the necessary matched-pair condition for all three C diagonals."""
    return all(
        any(
            j_pair(arrays[first][label], arrays[second][label], prime) != 0
            for first, second in combinations(range(3), 2)
        )
        for label in range(3)
    )


def exhaustive_projection_audit() -> dict[str, object]:
    """Exhaust the abstract A-array obstruction over F_3."""
    prime = 3
    vectors = list(product(range(prime), repeat=2))
    arrays: list[Array] = list(product(vectors, repeat=3))[1:]
    assert len(arrays) == 728
    rank_histogram = Counter(array_rank(array, prime) for array in arrays)
    assert rank_histogram == {1: 104, 2: 624}

    adjacency: list[set[int]] = []
    for first in arrays:
        adjacency.append({
            index
            for index, second in enumerate(arrays)
            if compatible(first, second, prime)
        })
    directed_pairs = sum(len(neighbours) for neighbours in adjacency)
    assert directed_pairs == 5728

    unordered_compatible_triples = 0
    surviving_diagonal_condition = 0
    for first in range(len(arrays)):
        for second in adjacency[first]:
            if second < first:
                continue
            for third in adjacency[first] & adjacency[second]:
                if third < second:
                    continue
                unordered_compatible_triples += 1
                triple = (arrays[first], arrays[second], arrays[third])
                if diagonal_can_be_nonzero(triple, prime):
                    surviving_diagonal_condition += 1

    assert unordered_compatible_triples == 9504
    assert surviving_diagonal_condition == 0
    return {
        "field": prime,
        "nonzero_arrays": len(arrays),
        "array_rank_histogram": dict(sorted(rank_histogram.items())),
        "directed_compatible_pairs": directed_pairs,
        "unordered_pairwise_compatible_triples": unordered_compatible_triples,
        "triples_with_all_three_possible_diagonals": surviving_diagonal_condition,
    }


def coordinate_and_fixture_audit() -> dict[str, object]:
    """Check q-duality coordinates and inclusion of the prior sharp fixture."""
    q_matrix = (
        (0, 0, 1),
        (1, -1, 1),
        (1, 0, 0),
    )
    determinant = (
        q_matrix[0][0] * (q_matrix[1][1] * q_matrix[2][2] - q_matrix[1][2] * q_matrix[2][1])
        - q_matrix[0][1] * (q_matrix[1][0] * q_matrix[2][2] - q_matrix[1][2] * q_matrix[2][0])
        + q_matrix[0][2] * (q_matrix[1][0] * q_matrix[2][1] - q_matrix[1][1] * q_matrix[2][0])
    )
    assert determinant == 1

    h = (0, 1, -2, -1, 0, 0)
    x4 = (0, 0, 0, 0, 1, 0)
    x5 = (0, 0, 0, 0, 0, 1)
    mode_five = (
        (0, 2, 2, 0, 0, 0),
        (0, 2, 0, -2, 0, 0),
        (1, 1, 0, 0, 0, 0),
    )
    assert all(
        vector[0] == 0 and vector[3] - vector[2] - vector[1] == 0
        for vector in (x4, x5, h)
    )
    assert all(
        vector[4] == vector[5] == 0
        and vector[3] - vector[2] - vector[0] == -vector[1]
        for vector in mode_five
    )
    return {"q_determinant": determinant, "sharp_fixture_in_WV": True}


def main() -> None:
    tensors = basis_tensor_audit()
    shell = shell_audit()
    projection = exhaustive_projection_audit()
    coordinates = coordinate_and_fixture_audit()

    print("fixed-pair Hamming-radius-two compression independent audit: PASS")
    print(f"  W^3 x V basis-tensor audit: {tensors}")
    print(f"  shell audit: {shell}")
    print(f"  exhaustive F3 projection audit: {projection}")
    print(f"  coordinate and fixture audit: {coordinates}")


if __name__ == "__main__":
    main()
