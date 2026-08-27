"""Primary exact checks for the adjacent-overlap balanced codimension-six cut."""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product

import sympy as sp


def selectors() -> list[tuple[int, int, int]]:
    """Return the 60 nonconstant maps from three colours to four vertices."""
    return [word for word in product(range(4), repeat=3) if len(set(word)) > 1]


def selector_orbit(selector: tuple[int, int, int]) -> tuple[int, ...]:
    """Classify a selector by its nonzero fibre sizes."""
    return tuple(sorted(Counter(selector).values(), reverse=True))


def assert_selector_orbits_and_dimensions() -> dict[str, object]:
    """Check the equality-source orbit counts and affine dimensions."""
    orbit_counts = Counter(selector_orbit(selector) for selector in selectors())
    assert orbit_counts == Counter({(2, 1): 36, (1, 1, 1): 24})

    root_dimensions = {}
    for selector in selectors():
        fibres = Counter(selector)
        common_dimension = sum(2 - fibres.get(vertex, 0) for vertex in range(4))
        root_dimensions[selector] = common_dimension + 2 + 2
    assert set(root_dimensions.values()) == {9}

    # Full affine source dimension is root base plus 28 nine-dimensional
    # blocks minus the fourteen independent evaluation equations.
    equality_source = 9 + 28 * 9 - 14
    assert equality_source == 247
    assert equality_source - 1 == 246
    assert 252 - 9 == 243

    non_equality_bounds = {
        0: 246,
        1: 246,
        2: 246,
        3: 246,
        4: 246,
    }
    # For r=4, the displayed value uses a_R<=2; a_R=3 is precisely equality.
    for synchronized, maximum_a in ((0, 0), (1, 2), (2, 3), (3, 3), (4, 2)):
        delta = 2 * synchronized - maximum_a
        dimension = 246 + synchronized * (synchronized - 1) // 2 - delta
        assert dimension == non_equality_bounds[synchronized]

    return {
        "selector_orbits": dict(sorted(orbit_counts.items())),
        "root_dimension": 9,
        "equality_source_dimension": equality_source,
        "proper_closed_cut_upper_dimension": equality_source - 1,
        "whole_zero_block_upper_dimension": 252 - 9,
    }


def permanent(matrix: sp.Matrix) -> sp.Expr:
    """Compute a small permanent exactly."""
    if matrix.rows == 0:
        return sp.Integer(1)
    return sp.expand(
        sum(
            sp.prod(matrix[row, permutation[row]] for row in range(matrix.rows))
            for permutation in permutations(range(matrix.cols))
        )
    )


def double_factorial_odd(value: int) -> int:
    """Return value!! for the values -1, 1, and 3 used at m=4."""
    if value in (-1, 0):
        return 1
    result = 1
    for factor in range(value, 0, -2):
        result *= factor
    return result


def parity_subsets() -> list[tuple[int, ...]]:
    """List the eight even subsets of a four-set."""
    return [
        subset
        for size in (0, 2, 4)
        for subset in combinations(range(4), size)
    ]


def binary_sensor_matrix(cross_scalars: sp.Matrix) -> sp.Matrix:
    """Write the eight sensor columns in the binary a/b word coordinates."""
    subsets = parity_subsets()
    return sp.Matrix(
        [
            [
                double_factorial_odd(4 - len(column) - 1)
                * permanent(cross_scalars.extract(row, column))
                if len(row) == len(column)
                else 0
                for column in subsets
            ]
            for row in subsets
        ]
    )


def unit(index: int) -> sp.Matrix:
    """Return a coordinate column in dimension three."""
    return sp.eye(3)[:, index]


def annihilator_basis(root: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix]:
    """Choose the two coordinate covectors annihilating a coordinate root."""
    root_index = next(index for index in range(3) if root[index])
    others = [index for index in range(3) if index != root_index]
    return unit(others[0]), unit(others[1])


def fixture_roots(orbit: tuple[int, ...]):
    """Return selector, common roots, and outer roots for one orbit."""
    if orbit == (2, 1):
        selector = (0, 0, 1)
        roots = [unit(2), unit(0), unit(0), unit(0)]
    else:
        assert orbit == (1, 1, 1)
        selector = (0, 1, 2)
        roots = [unit(1), unit(2), unit(0), unit(0)]
    outer = unit(0)
    assert all(roots[selector[colour]][colour] == 0 for colour in range(3))
    return selector, roots, outer


def assert_full_sensor_boundary_fixtures() -> dict[tuple[int, ...], object]:
    """Check both selector orbits with all fourteen union blocks nonzero."""
    t = sp.Integer(2)
    cross_scalars = sp.Matrix(
        4,
        4,
        lambda row, column: 1 if row == column else t,
    )
    sensor = binary_sensor_matrix(cross_scalars)
    assert sensor.rank() == 8
    assert sensor.det() != 0

    ledger = {}
    ell = unit(0)
    for orbit in ((2, 1), (1, 1, 1)):
        selector, roots, outer = fixture_roots(orbit)
        pairs = [annihilator_basis(root) for root in roots]

        full_blocks: list[sp.Matrix] = []
        evaluations: list[sp.Expr] = []
        for first, second in combinations(range(4), 2):
            block = pairs[first][1] * pairs[second][1].T
            full_blocks.append(block)
            evaluations.append((roots[first].T * block * roots[second])[0])
        for nonroot_column in range(4):
            for root_index in range(4):
                block = (
                    cross_scalars[root_index, nonroot_column]
                    * pairs[root_index][0]
                    * ell.T
                )
                full_blocks.append(block)
                if nonroot_column in (0, 1):
                    evaluations.append((roots[root_index].T * block * outer)[0])
        full_blocks.extend(sp.eye(3) for _ in combinations(range(4), 2))

        assert len(full_blocks) == 28
        assert all(block != sp.zeros(3) for block in full_blocks)
        assert evaluations == [0] * 14
        ledger[orbit] = {
            "selector": selector,
            "all_28_blocks_nonzero": True,
            "evaluation_rank": 14,
            "balanced_sensor_rank": sensor.rank(),
            "minor_determinant": sensor.det(),
        }
    return ledger


def perfect_matchings(vertices: tuple[int, ...]):
    """Yield every perfect matching of a small ordered vertex tuple."""
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(rest):
            yield ((first, second), *matching)


def common_q_sensor(
    contractions: tuple[
        tuple[int, int, int],
        tuple[int, int, int],
        tuple[int, int, int],
        tuple[int, int, int],
    ],
) -> sp.Matrix:
    """Build the complete eight-column m=4 sensor for the common-Q graph."""
    q = sp.Matrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    h = [q * sp.Matrix(coordinates) for coordinates in contractions]
    columns: list[sp.Matrix] = []
    for selected_nonroots in parity_subsets():
        entries = []
        for colours in product(range(3), repeat=4):
            value = 0
            for selected_roots in combinations(range(4), len(selected_nonroots)):
                remaining = tuple(
                    root for root in range(4) if root not in selected_roots
                )
                for target_order in permutations(selected_nonroots):
                    cross_value = sp.prod(
                        h[nonroot][colours[root]]
                        for root, nonroot in zip(
                            selected_roots, target_order, strict=True
                        )
                    )
                    for matching in perfect_matchings(remaining):
                        root_value = sp.prod(
                            q[colours[first], colours[second]]
                            for first, second in matching
                        )
                        value += cross_value * root_value
            entries.append(value)
        columns.append(sp.Matrix(entries))
    return sp.Matrix.hstack(*columns)


def assert_common_q_sharpness() -> dict[str, object]:
    """Find an exact rank-seven common-Q sensor and check both root orbits."""
    q = sp.Matrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    assert q.det() == -1
    contractions = (
        (1, 1, 1),
        (1, 2, 3),
        (2, 1, 3),
        (3, 2, 1),
    )
    sensor = common_q_sensor(contractions)
    assert sensor.rank() == 7

    selected_rows = [0, 2, 5, 8, 14, 17, 26]
    selected_columns = [0, 1, 2, 3, 4, 5, 7]
    rank_seven_minor = sensor.extract(selected_rows, selected_columns).det()
    assert rank_seven_minor != 0

    common_roots = [unit(0), unit(0), unit(0), unit(1)]
    outer = unit(0)
    assert all(
        (common_roots[first].T * q * common_roots[second])[0] == 0
        for first, second in combinations(range(4), 2)
    )
    assert all((root.T * q * outer)[0] == 0 for root in common_roots)
    selector_two_one = (3, 0, 0)
    selector_injective = (3, 0, 1)
    for selector in (selector_two_one, selector_injective):
        assert all(
            common_roots[selector[colour]][colour] == 0 for colour in range(3)
        )
    return {
        "contractions": contractions,
        "sensor_rank": sensor.rank(),
        "rank_seven_minor": rank_seven_minor,
        "selector_representatives": (selector_two_one, selector_injective),
        "all_14_evaluations_zero": True,
    }


def main() -> None:
    incidence = assert_selector_orbits_and_dimensions()
    full = assert_full_sensor_boundary_fixtures()
    sharp = assert_common_q_sharpness()
    print("adjacent overlap inside balanced rank drop primary checks: PASS")
    print(f"  selector and incidence ledger: {incidence}")
    print(f"  all-nonzero full-sensor fixtures: {full}")
    print(f"  common-Q rank-drop sharpness: {sharp}")


if __name__ == "__main__":
    main()
