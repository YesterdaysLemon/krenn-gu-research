"""Primary exact checks for the eight-vertex five-root boundary envelope."""

from __future__ import annotations

from collections import Counter
from functools import cache
from itertools import combinations, permutations, product

import sympy as sp

Vertices = tuple[int, ...]
Matching = tuple[tuple[int, int], ...]


@cache
def perfect_matchings(vertices: Vertices) -> tuple[Matching, ...]:
    """Return every labelled perfect matching of ``vertices``."""
    if not vertices:
        return ((),)
    first = vertices[0]
    result: list[Matching] = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            result.append(((first, partner),) + tail)
    return tuple(result)


def check_majority_matching_count() -> dict[str, object]:
    """Check the five-versus-three matching sectors term by term."""
    roots = set(range(5))
    sectors: Counter[tuple[int, int, int]] = Counter()
    for matching in perfect_matchings(tuple(range(8))):
        internal_root = 0
        crossing = 0
        internal_outside = 0
        for left, right in matching:
            if left in roots and right in roots:
                internal_root += 1
            elif left not in roots and right not in roots:
                internal_outside += 1
            else:
                crossing += 1
        assert 2 * internal_root + crossing == 5
        assert 2 * internal_outside + crossing == 3
        assert internal_root == internal_outside + 1
        assert internal_root >= 1
        sectors[(internal_root, crossing, internal_outside)] += 1
    assert sectors == Counter({(1, 3, 0): 60, (2, 1, 1): 45})
    return {
        "perfect_matchings": len(perfect_matchings(tuple(range(8)))),
        "sectors": dict(sectors),
    }


def five_root_intersection_degree() -> int:
    """Count the regular orientations giving the top Chow coefficient."""
    vertices = tuple(range(5))
    edges = tuple(combinations(vertices, 2))
    degree = 0
    for choices in product((0, 1), repeat=len(edges)):
        indegrees = [0] * len(vertices)
        for edge, choice in zip(edges, choices, strict=True):
            indegrees[edge[choice]] += 1
        degree += indegrees == [2] * len(vertices)
    assert degree == 24
    return degree


def check_three_colour_boundary_cover() -> dict[str, object]:
    """Enumerate the 120 nonempty coordinate products covering three monomials."""
    nonempty = []
    profiles: Counter[tuple[int, ...]] = Counter()
    for selector in product(range(5), repeat=3):
        coordinate_sets = [set() for _ in range(5)]
        for colour, vertex in enumerate(selector):
            coordinate_sets[vertex].add(colour)
        if any(len(colours) == 3 for colours in coordinate_sets):
            assert selector[0] == selector[1] == selector[2]
            continue
        dimension = sum(2 - len(colours) for colours in coordinate_sets)
        assert dimension == 7
        fibre_sizes = tuple(sorted((len(colours) for colours in coordinate_sets if colours), reverse=True))
        profiles[fibre_sizes] += 1
        nonempty.append(selector)
    assert len(nonempty) == 120
    assert profiles == Counter({(2, 1): 60, (1, 1, 1): 60})

    projective_coefficient_dimension = 10 * 8
    incidence_dimension = 7 + 10 * 7
    affine_coefficient_dimension = 10 * 9
    affine_lift_dimension = incidence_dimension + 10
    zero_block_dimension = affine_coefficient_dimension - 9
    assert (
        projective_coefficient_dimension,
        incidence_dimension,
        projective_coefficient_dimension - incidence_dimension,
    ) == (80, 77, 3)
    assert (
        affine_coefficient_dimension,
        affine_lift_dimension,
        zero_block_dimension,
    ) == (90, 87, 81)
    return {
        "nonempty_coordinate_products": len(nonempty),
        "empty_constant_selectors": 5,
        "selector_profiles": dict(profiles),
        "projective_coefficient_dimension": projective_coefficient_dimension,
        "incidence_dimension_at_most": incidence_dimension,
        "projective_codimension_at_least": 3,
        "affine_lift_dimension_at_most": affine_lift_dimension,
        "zero_block_codimension": 9,
    }


PERMUTATIONS = tuple(permutations(range(3)))


def parity_change(old: tuple[int, int], new: tuple[int, int]) -> tuple[int, int, int]:
    """Return the latent-count change modulo two."""
    parity = [0, 0, 0]
    for label in old + new:
        parity[label] ^= 1
    return tuple(parity)


def check_monomial_mixed_shells() -> dict[str, int]:
    """Prove Hamming-one blindness and the four-cell Hamming-two detector."""
    hamming_one_cases = 0
    hamming_two_cases = 0
    equal_label_cases = 0
    unequal_label_cases = 0
    for left in PERMUTATIONS:
        for colour in range(3):
            for replacement in range(3):
                if replacement == colour:
                    continue
                change = parity_change(
                    (left[colour], left[colour]),
                    (left[colour], left[replacement]),
                )
                assert change != (0, 0, 0)
                hamming_one_cases += 1

        for right in PERMUTATIONS:
            for colour in range(3):
                alternatives = tuple(value for value in range(3) if value != colour)
                good = []
                for left_new, right_new in product(alternatives, repeat=2):
                    change = parity_change(
                        (left[colour], right[colour]),
                        (left[left_new], right[right_new]),
                    )
                    if change == (0, 0, 0):
                        good.append((left_new, right_new))
                expected = 2 if left[colour] == right[colour] else 1
                assert len(good) == expected
                equal_label_cases += expected == 2
                unequal_label_cases += expected == 1
                hamming_two_cases += 1

    pure_admissible_tables = 0
    for table in product(PERMUTATIONS, repeat=8):
        admissible = True
        for colour in range(3):
            counts = Counter(permutation[colour] for permutation in table)
            if any(counts[label] % 2 for label in range(3)):
                admissible = False
                break
        pure_admissible_tables += admissible
    assert pure_admissible_tables == 105_216
    assert hamming_one_cases == 36
    assert hamming_two_cases == 108
    assert (equal_label_cases, unequal_label_cases) == (36, 72)
    return {
        "local_hamming_one_cases": hamming_one_cases,
        "local_hamming_two_cases": hamming_two_cases,
        "equal_latent_label_cases": equal_label_cases,
        "unequal_latent_label_cases": unequal_label_cases,
        "pure_admissible_eight_vertex_permutation_tables": pure_admissible_tables,
    }


def construction_matrices() -> tuple[sp.Matrix, ...]:
    """Return the normalized adjacent-cut monomial common-form fixture."""
    third = sp.Rational(1, 3)
    return (
        sp.eye(3),
        sp.Matrix([[-1, 0, 0], [0, 0, -1], [0, -1, 0]]),
        sp.diag(-1, -1, 1),
        sp.Matrix([[0, 1, 0], [0, 0, -1], [1, 0, 0]]),
        sp.Matrix([[0, -1, 0], [-1, 0, 0], [0, 0, -1]]),
        -sp.eye(3),
        sp.Matrix([[0, 0, -1], [-1, 0, 0], [0, -1, 0]]),
        sp.Matrix([[0, 0, -third], [0, -third, 0], [-third, 0, 0]]),
    )


def tensor_coefficient(
    word: tuple[int, ...], blocks: dict[tuple[int, int], sp.Matrix]
) -> sp.Expr:
    """Evaluate one coordinate coefficient by direct matching enumeration."""
    return sp.simplify(
        sum(
            sp.prod(
                blocks[(left, right)][word[left], word[right]]
                for left, right in matching
            )
            for matching in perfect_matchings(tuple(range(len(word))))
        )
    )


def quadratic_column(block: sp.Matrix) -> sp.Matrix:
    """Return coefficients of x^T block x in the fixed monomial order."""
    return sp.Matrix(
        [
            block[0, 0],
            block[1, 1],
            block[2, 2],
            block[0, 1] + block[1, 0],
            block[0, 2] + block[2, 0],
            block[1, 2] + block[2, 1],
        ]
    )


def root_quadric_matrix(
    roots: tuple[int, ...], blocks: dict[tuple[int, int], sp.Matrix]
) -> sp.Matrix:
    """Build the six-by-six fixed-gauge root-quadric coefficient matrix."""
    columns = [quadratic_column(blocks[(left, right)]) for left, right in combinations(roots, 2)]
    return sp.Matrix.hstack(*columns)


def check_adjacent_cut_fixture() -> dict[str, object]:
    """Check the exact H1-blind, H2-detected adjacent-cut control."""
    gauges = construction_matrices()
    blocks = {
        (left, right): gauges[left].T * gauges[right]
        for left in range(8)
        for right in range(left + 1, 8)
    }
    assert all(matrix.det() != 0 for matrix in gauges)
    assert all(matrix.det() != 0 for matrix in blocks.values())
    for (left, right), block in blocks.items():
        assert gauges[left].inv().T * block * gauges[right].inv() == sp.eye(3)

    pure = tuple(tensor_coefficient((colour,) * 8, blocks) for colour in range(3))
    assert pure == (1, 1, 1)
    hamming_one = []
    for colour in range(3):
        for vertex in range(8):
            for replacement in range(3):
                if replacement == colour:
                    continue
                word = [colour] * 8
                word[vertex] = replacement
                hamming_one.append(tensor_coefficient(tuple(word), blocks))
    assert len(hamming_one) == 48
    assert all(value == 0 for value in hamming_one)

    exchanged_hamming_two = tensor_coefficient((0, 0, 0, 2, 2, 0, 0, 0), blocks)
    assert exchanged_hamming_two == -1

    first = root_quadric_matrix((0, 1, 2, 3), blocks)
    second = root_quadric_matrix((0, 1, 2, 4), blocks)
    assert first.det() == 4
    assert second.det() == -8

    expected_first = sp.Matrix(
        [
            [-1, -1, 0, 1, 0, 0],
            [0, -1, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 0, 1, 0, -2, -1],
            [0, 0, 1, 0, 0, 1],
            [-2, 0, -1, 0, 0, 1],
        ]
    )
    expected_second = sp.Matrix(
        [
            [-1, -1, 0, 1, 0, 0],
            [0, -1, 0, 0, 0, 0],
            [0, 1, -1, 0, 0, -1],
            [0, 0, -2, 0, 1, 2],
            [0, 0, 0, 0, 1, 0],
            [-2, 0, 0, 0, 1, 0],
        ]
    )
    assert first == expected_first
    assert second == expected_second

    return {
        "invertible_gauges": len(gauges),
        "invertible_edge_blocks": len(blocks),
        "latent_common_form_edges": len(blocks),
        "pure_coefficients": pure,
        "hamming_one_zero_coefficients": len(hamming_one),
        "mixed_00022000": exchanged_hamming_two,
        "root_quadric_determinants": (first.det(), second.det()),
        "balanced_sensor_rank_bound": 7,
        "balanced_sensor_columns": 8,
    }


def main() -> None:
    majority = check_majority_matching_count()
    degree = five_root_intersection_degree()
    cover = check_three_colour_boundary_cover()
    shells = check_monomial_mixed_shells()
    fixture = check_adjacent_cut_fixture()
    print("eight-vertex five-root boundary envelope primary checks: PASS")
    print(f"  majority matching sectors: {majority}")
    print(f"  five-root intersection degree: {degree}")
    print(f"  three-colour boundary cover: {cover}")
    print(f"  monomial mixed shells: {shells}")
    print(f"  adjacent-cut sharpness fixture: {fixture}")


if __name__ == "__main__":
    main()
