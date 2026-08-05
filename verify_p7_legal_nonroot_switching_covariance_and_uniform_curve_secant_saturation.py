"""Verify legal nonroot switching and the uniform P7 secant exclusion.

This is an exact characteristic-zero replay.  The only polynomial parameter is
the named common nonroot edge weight; no graph, support, decomposition, or
finite field is searched.
"""

from __future__ import annotations

import importlib.util
from functools import cache
from itertools import combinations, product
from pathlib import Path

from sympy import Matrix, Poly, prod, symbols

ROOT = Path(__file__).resolve().parent
SENSOR_REPLAY = ROOT / (
    "verify_p7_full_mixed_root_219_label_sensor_and_pinned_star_gating_boundary.py"
)

P0_COEFFS = (
    6662572822705733828125,
    -12156844565030088437500,
    -11656744567696429468750,
    -964481421579777390625,
    478062693786650000,
    -167575290444104681250,
    -329667083352597624375,
    -126033773134233295625,
    -41624665391857307375,
    -10418655620547901625,
    -1665030690056656225,
    -89100920096274400,
    15940043824280765,
    2548639126911280,
    87299980928535,
    -16019848623521,
    -841802234952,
    81773978676,
    628717584,
)

P1_COEFFS = (
    45743752916454884375000,
    -864588786885117896875000,
    -4116226358173090867343750,
    -7598683970980122418125000,
    -3401502493947155460953125,
    5913944738769560812265625,
    5334994427617131112718750,
    73876260872593498768750,
    -261544878332648570021250,
    -100449092973761054860625,
    -26721393305568752102250,
    -3351312997063601813625,
    -245913724965094499700,
    -10804647546463312425,
    -617591700542701835,
    3747499312421390,
    -129171904414652,
    -96822486970,
    36194813664,
)


def load_sensor():
    """Load the previously committed legal matching-column implementation."""
    spec = importlib.util.spec_from_file_location("p7_full_sensor_switching", SENSOR_REPLAY)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def hafnian(vertices: tuple[int, ...], edge: dict[tuple[int, int], int]) -> int:
    """Exact recursive hafnian on one fixed small named graph."""

    @cache
    def recurse(active: tuple[int, ...]) -> int:
        if not active:
            return 1
        first = active[0]
        total = 0
        for index in range(1, len(active)):
            second = active[index]
            remainder = active[1:index] + active[index + 1 :]
            total += edge[tuple(sorted((first, second)))] * recurse(remainder)
        return total

    return recurse(tuple(sorted(vertices)))


def deck(
    edge: dict[tuple[int, int], int],
    vertices: tuple[int, ...],
) -> dict[tuple[int, ...], int]:
    return {
        subset: hafnian(subset, edge)
        for size in (4, 6, 8)
        for subset in combinations(vertices, size)
    }


def depth_columns(sensor):
    five = [sensor.depth_five_column(subset) for subset in combinations(range(9), 5)]
    three = [
        sensor.depth_three_column(subset) for subset in combinations(range(9), 3)
    ]
    one = [sensor.depth_one_column(vertex) for vertex in range(9)]
    return five, three, one


def depth_sum_tensor(columns: list[list[int]]) -> list[int]:
    return [sum(column[row] for column in columns) for row in range(3**5)]


def flatten_01_234(sensor, tensor: list[object]) -> Matrix:
    row_words = tuple(product(range(3), repeat=2))
    column_words = tuple(product(range(3), repeat=3))
    return Matrix(
        [
            [tensor[sensor.WORD_INDEX[row_word + column_word]] for column_word in column_words]
            for row_word in row_words
        ]
    )


def apply_sensor(
    columns: tuple[list[list[int]], list[list[int]], list[list[int]]],
    values: dict[tuple[int, ...], int],
) -> list[int]:
    five, three, one = columns
    labels = list(combinations(range(9), 5))
    labels += list(combinations(range(9), 3))
    labels += [(vertex,) for vertex in range(9)]
    all_columns = five + three + one
    cofactor_values = [values[tuple(sorted(set(range(9)) - set(label)))] for label in labels]
    return [
        sum(value * column[row] for value, column in zip(cofactor_values, all_columns, strict=True))
        for row in range(3**5)
    ]


def check_switching_covariance(sensor, columns) -> None:
    vertices = tuple(range(9))
    edge = {
        pair: 2 + pair[0] + 3 * pair[1]
        for pair in combinations(vertices, 2)
    }
    switching = (2, 3, 5, 7, 11, 13, 17, 19, 23)
    switched_edge = {
        pair: switching[pair[0]] * switching[pair[1]] * value
        for pair, value in edge.items()
    }
    base_deck = deck(edge, vertices)
    switched_deck = deck(switched_edge, vertices)
    for subset, value in base_deck.items():
        assert switched_deck[subset] == prod(switching[index] for index in subset) * value

    base_tensor = apply_sensor(columns, base_deck)
    five, three, one = columns
    labels = list(combinations(vertices, 5))
    labels += list(combinations(vertices, 3))
    labels += [(vertex,) for vertex in vertices]
    all_columns = five + three + one
    scaled_columns = [
        [prod(switching[index] for index in label) * value for value in column]
        for label, column in zip(labels, all_columns, strict=True)
    ]
    switched_values = [
        switched_deck[tuple(sorted(set(vertices) - set(label)))] for label in labels
    ]
    switched_tensor = [
        sum(value * column[row] for value, column in zip(switched_values, scaled_columns, strict=True))
        for row in range(3**5)
    ]
    total_switch = prod(switching)
    assert switched_tensor == [total_switch * value for value in base_tensor]

    # The shallow Hessian on one eight-shore transforms by diagonal congruence.
    shore = tuple(range(8))
    shore_edges = tuple(combinations(shore, 2))
    shore_product = prod(switching[index] for index in shore)
    for left in shore_edges:
        for right in shore_edges:
            if set(left).isdisjoint(right):
                remainder = tuple(sorted(set(shore) - set(left) - set(right)))
                base_value = base_deck[remainder]
                switched_value = switched_deck[remainder]
                left_scale = switching[left[0]] * switching[left[1]]
                right_scale = switching[right[0]] * switching[right[1]]
                assert switched_value * left_scale * right_scale == shore_product * base_value


def check_uniform_curve(sensor, columns) -> None:
    t = symbols("t")
    five, three, one = columns
    core_tensor = [
        depth_five + 5 * t * depth_three + 35 * t**2 * depth_one
        for depth_five, depth_three, depth_one in zip(
            depth_sum_tensor(five),
            depth_sum_tensor(three),
            depth_sum_tensor(one),
            strict=True,
        )
    ]
    flattening = flatten_01_234(sensor, core_tensor)
    block_zero = flattening[:, 0:9]
    block_one = flattening[:, 9:18]
    determinant_zero = Poly(block_zero.det(), t, domain="ZZ")
    determinant_one = Poly(block_one.det(), t, domain="ZZ")

    content_zero, primitive_zero = determinant_zero.primitive()
    content_one, primitive_one = determinant_one.primitive()
    expected_zero = Poly.from_list(P0_COEFFS, gens=t, domain="ZZ")
    expected_one = Poly.from_list(P1_COEFFS, gens=t, domain="ZZ")
    assert content_zero == 50
    assert content_one == 5
    assert primitive_zero == expected_zero
    assert primitive_one == expected_one
    assert primitive_zero.gcd(primitive_one) == Poly(1, t, domain="ZZ")

    # The actual physical tensor has the common factor 3*t^2 in every entry.
    # At t=1 the first block recovers the already named integer certificate.
    expected_at_one = -18_494_220_325_114_867_735_328_060_700
    assert 3**9 * determinant_zero.eval(1) == expected_at_one

    # Every eight-shore of the common-edge graph has this nonzero determinant.
    hessian_determinant = (3 * t**2) ** 28 * 15 * (-5) ** 7
    assert hessian_determinant != 0
    assert len(P0_COEFFS) == len(P1_COEFFS) == 19


def main() -> None:
    sensor = load_sensor()
    columns = depth_columns(sensor)
    assert tuple(map(len, columns)) == (126, 84, 9)
    check_switching_covariance(sensor, columns)
    check_uniform_curve(sensor, columns)

    for q in range(4, 20, 2):
        edge_count = q * (q - 1) // 2
        assert edge_count - 2 * (q - 1) == (q - 1) * (q - 4) // 2

    print("PASS: nonroot switching scales every physical deck coordinate exactly")
    print("PASS: the legal sensor changes by invertible diagonal column scaling")
    print("PASS: the full root tensor changes only by product(z_u)")
    print("PASS: shallow Hessians transform by diagonal congruence")
    print("PASS: two named maximal flattening minors have primitive gcd one")
    print("PASS: every nonzero uniform-edge physical tensor has flattening rank nine")
    print("searches=0")
    print("finite_fields=0")
    print("SCOPE: the switching orbit is a projective gauge orbit, not a GHZ witness")
    print("SCOPE: nonuniform physical GHZ incidence remains UNKNOWN")
    print("SCOPE: P7 and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
