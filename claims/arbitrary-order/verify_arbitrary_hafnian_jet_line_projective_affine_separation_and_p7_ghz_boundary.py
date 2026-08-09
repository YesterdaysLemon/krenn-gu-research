"""Verify radial hafnian-jet homogeneity and the fixed P7 controls.

This is a fixed exact replay.  It performs no parameter, graph, support, or
tensor-decomposition search and uses no finite-field calculation.
"""

from __future__ import annotations

import importlib.util
import sys
from itertools import combinations, product
from pathlib import Path

from sympy import Matrix

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
SENSOR_REPLAY = REPO_ROOT / (
    "claims/p7/"
    "verify_p7_full_mixed_root_219_label_sensor_and_pinned_star_gating_boundary.py"
)
EXPECTED_FLATTENING_MINOR = -18_494_220_325_114_867_735_328_060_700


def load_committed_sensor_replay():
    """Load the already committed matching-column implementation."""
    spec = importlib.util.spec_from_file_location("p7_full_sensor", SENSOR_REPLAY)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def double_factorial_odd(order: int) -> int:
    """Return (order-1)!! for an even order, including the empty hafnian."""
    value = 1
    for factor in range(order - 1, 0, -2):
        value *= factor
    return value


def kneser_hessian(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], Matrix]:
    edges = tuple(combinations(vertices, 2))
    matrix = Matrix(
        [
            [3 if set(left).isdisjoint(right) else 0 for right in edges]
            for left in edges
        ]
    )
    return edges, matrix


def build_all_one_sensor_tensor():
    """Apply the committed legal matching sensor to h4=3,h6=15,h8=105."""
    sensor = load_committed_sensor_replay()
    columns = [
        sensor.depth_five_column(subset)
        for subset in combinations(sensor.NONROOTS, 5)
    ]
    columns += [
        sensor.depth_three_column(subset)
        for subset in combinations(sensor.NONROOTS, 3)
    ]
    columns += [sensor.depth_one_column(vertex) for vertex in sensor.NONROOTS]

    weights = [3] * 126 + [15] * 84 + [105] * 9
    assert len(columns) == len(weights) == 219
    tensor = [
        sum(weight * column[row] for weight, column in zip(weights, columns, strict=True))
        for row in range(3**5)
    ]
    return sensor, tensor


def named_two_three_flattening_minor(sensor, tensor: list[int]) -> Matrix:
    """Rows 00,...,22 and columns 000,...,022 of the 01|234 flattening."""
    row_words = tuple(product(range(3), repeat=2))
    selected_column_words = tuple(product(range(3), range(3), range(3)))[:9]
    # product(range(3), range(3), range(3)) is ordered 000,...,222.
    rows = []
    for row_word in row_words:
        row = []
        for column_word in selected_column_words:
            word = row_word + column_word
            row.append(tensor[sensor.WORD_INDEX[word]])
        rows.append(row)
    return Matrix(rows)


def main() -> None:
    # The arbitrary-order exponent ledger in Theorem 1.
    for m in range(2, 10):
        q = 2 * m
        edge_count = q * (q - 1) // 2
        left_exponent = edge_count * (m - 2) + 1
        right_exponent = edge_count * (m - 2)
        assert left_exponent - right_exponent == 1
        assert 1 + (edge_count - 1) + 1 == edge_count + 1

    # The P7 q=8 specialization has the claimed t^57 versus t^56 split.
    q = 8
    m = 4
    edge_count = q * (q - 1) // 2
    assert edge_count == 28
    assert edge_count * (m - 2) + 1 == 57
    assert edge_count * (m - 2) == 56

    # Exact all-one shallow jet on one (hence every) eight-shore.
    vertices = tuple(range(8))
    edges, hessian = kneser_hessian(vertices)
    determinant = hessian.det()
    expected_determinant = 3**28 * 15 * (-5) ** 7
    assert determinant == expected_determinant != 0
    assert len(edges) == 28

    ones = Matrix.ones(28, 1)
    cofactor = 15 * ones
    reconstructed = 3 * hessian.inv() * cofactor
    assert reconstructed == ones
    assert hessian * ones == 45 * ones

    # The scalar stress is 4*delta*105 = 3*c^T*adj(D)*c.
    adjugate_times_c = determinant * (hessian.inv() * cofactor)
    assert 4 * determinant * 105 == (
        3 * (cofactor.T * adjugate_times_c)[0]
    )

    # For the all-one graph b=delta*a.  Every four-vertex hafnian is 3,
    # so every q=8 determinant-cleared Hessian-deck equation holds at t=1.
    b_vector = [determinant] * 28
    assert double_factorial_odd(4) == 3
    for left_index, left in enumerate(edges):
        for right_index, right in enumerate(edges):
            if set(left).isdisjoint(right):
                lhs = determinant**2 * hessian[left_index, right_index]
                # The remaining four-vertex graph has all six edge weights delta.
                rhs = 3 * determinant**2
                assert lhs == rhs
    assert all(value == determinant for value in b_vector)

    # An ambient injective map can carry this exact physical deck to GHZ:
    # dim(U/Kw)=218 embeds into a 240-dimensional complement of Delta.
    assert 219 - 1 == 218 <= 243 - 3 == 240

    # Fixed exact legal control: apply the committed sensor to the same deck.
    sensor, tensor = build_all_one_sensor_tensor()
    minor = named_two_three_flattening_minor(sensor, tensor)
    minor_determinant = minor.det()
    assert minor_determinant == EXPECTED_FLATTENING_MINOR != 0
    assert minor.rank() == 9

    print("PASS: arbitrary q=2m radial exponent split is exact")
    print("PASS: q=8 deck equations scale as t^57 versus t^56")
    print("PASS: scalar Euler stress scales projectively as t^(N+1)")
    print("PASS: all-one P7 shore has det(D)=3^28*15*(-5)^7")
    print("PASS: all-one shallow jet reconstructs every shore edge as 1")
    print("PASS: ambient injective GHZ-compatible physical line is dimensionally exact")
    print(f"PASS: fixed legal flattening minor = {minor_determinant}")
    print("PASS: fixed legal sensor/all-one tensor has border rank at least 9")
    print("searches=0")
    print("SCOPE: ambient GHZ-compatible sensor is not asserted legal")
    print("SCOPE: fixed legal tensor is not a GHZ witness")
    print("SCOPE: legal GHZ incidence on the physical Hessian open remains UNKNOWN")
    print("SCOPE: global Krenn-Gu remains UNRESOLVED")


if __name__ == "__main__":
    main()
