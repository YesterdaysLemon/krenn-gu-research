"""Verify the complete local cone of admissible D-transition potentials."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

Normal = tuple[int, int, int]
Vector = tuple[int, ...]

PERMUTATIONS = tuple(itertools.permutations(range(3)))
EXTREME_RAYS: tuple[Vector, ...] = (
    (-4, 1, 1, 1, 6, -4),
    (-4, 1, 6, 1, 1, -4),
    (1, -4, 1, 1, -4, 6),
    (1, -4, 1, 6, -4, 1),
    (1, 6, -4, -4, 1, 1),
    (6, 1, -4, -4, 1, 1),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rank(rows: list[list[int]]) -> int:
    matrix = [[Fraction(value) for value in row] for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = (
            matrix[pivot],
            matrix[pivot_row],
        )
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [
            value / scale for value in matrix[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value - factor * base
                for value, base in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def allowed(
    left: Normal, right: Normal, row: int, column: int
) -> bool:
    return all(
        (row, column) == (target, target)
        or row == left[target]
        or column == right[target]
        for target in range(3)
    )


def bits(normal: Normal) -> tuple[int, int, int]:
    return (
        int(normal[0] == 2),
        int(normal[1] == 2),
        int(normal[2] == 1),
    )


def base(normal: Normal) -> tuple[int, int, int]:
    b0, b1, b2 = bits(normal)
    return (
        1 - 2 * b2,
        2 * (b2 - b0),
        2 * (b0 + b1 - 1),
    )


def permuted(
    normal: Normal, permutation: tuple[int, int, int]
) -> tuple[int, int, int]:
    image = [-1, -1, -1]
    for colour in range(3):
        image[permutation[colour]] = permutation[normal[colour]]
    values = base(tuple(image))
    return tuple(values[permutation[colour]] for colour in range(3))


def dot(left: Vector, right: Vector) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def main() -> None:
    normals: tuple[Normal, ...] = tuple(
        tuple(values)
        for values in itertools.product(range(3), repeat=3)
        if all(values[colour] != colour for colour in range(3))
    )
    normal_index = {normal: index for index, normal in enumerate(normals)}
    saturated = tuple(
        (colour, left, right)
        for colour in range(3)
        for left in normals
        for right in normals
        if (
            allowed(left, right, colour, colour)
            and all(
                bits(left)[bit] != bits(right)[bit]
                for bit in range(3)
                if bit != colour
            )
        )
    )
    if len(saturated) != 48:
        raise AssertionError("saturated transition census changed")

    equality_rows: list[list[int]] = []
    optional_rows: list[list[int]] = []
    for colour, left, right in saturated:
        equality = [0] * 24
        equality[3 * normal_index[left] + colour] += 1
        equality[3 * normal_index[right] + colour] += 1
        equality_rows.append(equality)
        for row in range(3):
            for column in range(3):
                if row == column or not allowed(
                    left, right, row, column
                ):
                    continue
                optional = [0] * 24
                optional[3 * normal_index[left] + row] += 1
                optional[3 * normal_index[right] + column] += 1
                optional_rows.append(optional)
    if len(optional_rows) != 42:
        raise AssertionError("optional transition census changed")

    q_rows = [
        [
            permuted(normal, permutation)[colour]
            for permutation in PERMUTATIONS
        ]
        for normal in normals
        for colour in range(3)
    ]
    if rank(equality_rows) != 18 or rank(q_rows) != 6:
        raise AssertionError("potential equality-space rank changed")
    if any(
        sum(row[index] * q_rows[index][column] for index in range(24))
        for row in equality_rows
        for column in range(6)
    ):
        raise AssertionError("displayed potentials lost D neutrality")

    optional_weights = tuple(
        tuple(
            sum(row[index] * q_rows[index][column] for index in range(24))
            for column in range(6)
        )
        for row in optional_rows
    )
    weight_counter = Counter(optional_weights)
    unique_weights = tuple(sorted(weight_counter))
    if len(unique_weights) != 9:
        raise AssertionError("optional inequality census changed")

    ray_matrix_rank = rank(
        [
            [EXTREME_RAYS[column][row] for column in range(6)]
            for row in range(6)
        ]
    )
    if ray_matrix_rank != 6:
        raise AssertionError("extreme rays lost independence")
    transformed = tuple(
        tuple(dot(weight, ray) for ray in EXTREME_RAYS)
        for weight in unique_weights
    )
    if any(value < 0 for row in transformed for value in row):
        raise AssertionError("claimed ray left the closed cone")
    coordinate_facets = {
        tuple(10 if index == coordinate else 0 for index in range(6))
        for coordinate in range(6)
    }
    if not coordinate_facets.issubset(set(transformed)):
        raise AssertionError(
            "transformed inequalities do not force nonnegative ray "
            "coordinates"
        )
    if tuple(
        sum(ray[coordinate] for ray in EXTREME_RAYS)
        for coordinate in range(6)
    ) != (1, 1, 1, 1, 1, 1):
        raise AssertionError("interior refinement identity changed")
    for normal_position, normal in enumerate(normals):
        s0, s1, s2 = tuple(
            1 if bit == 0 else -1 for bit in bits(normal)
        )
        expected = (
            (s1, s2, -s1),
            (s1, -s0, -s1),
            (s2, -s2, s1),
            (s2, -s2, s0),
            (-s2, s0, -s0),
            (-s1, s0, -s0),
        )
        for ray_index, ray in enumerate(EXTREME_RAYS):
            actual = tuple(
                dot(tuple(q_rows[3 * normal_position + colour]), ray)
                for colour in range(3)
            )
            if actual != tuple(
                5 * value for value in expected[ray_index]
            ):
                raise AssertionError(
                    "Boolean extreme-potential table changed"
                )

    payload = {
        "verified": True,
        "status": "complete_admissible_local_potential_cone",
        "normal_colour_states": 24,
        "oriented_saturated_D_transitions": len(saturated),
        "D_neutrality_rank": rank(equality_rows),
        "D_neutrality_nullity": 24 - rank(equality_rows),
        "permuted_potential_rank": rank(q_rows),
        "optional_transitions": len(optional_rows),
        "unique_optional_inequalities": [
            {
                "coefficient_vector": list(weight),
                "multiplicity": weight_counter[weight],
                "extreme_coordinate_row": list(transformed[index]),
            }
            for index, weight in enumerate(unique_weights)
        ],
        "closed_cone_extreme_rays_in_permuted_basis": [
            list(ray) for ray in EXTREME_RAYS
        ],
        "extreme_ray_rank": ray_matrix_rank,
        "extreme_rays_sum": [1, 1, 1, 1, 1, 1],
        "boolean_extreme_values_verified": True,
        "boolean_extreme_value_set": [-5, 5],
        "cone_certificate": (
            "all transformed inequality coefficients are nonnegative, "
            "and six transformed rows are 10 times the six coordinate "
            "functionals; hence the closed cone is exactly the "
            "nonnegative span of the six displayed extreme rays"
        ),
        "strict_cone_certificate": (
            "strict optional positivity is equivalent to every extreme-"
            "ray coordinate being positive"
        ),
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path("tmp", "full_admissible_potential_cone_verified.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "verified": True,
                "D_neutrality_nullity": 6,
                "unique_optional_inequalities": 9,
                "extreme_rays": 6,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
