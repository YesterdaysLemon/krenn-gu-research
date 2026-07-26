"""Independent symbolic audit of the full admissible potential cone."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path

from sympy import Matrix

Normal = tuple[int, int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def allowed(
    left: Normal, right: Normal, row: int, column: int
) -> bool:
    for target in range(3):
        if (
            (row, column) != (target, target)
            and row != left[target]
            and column != right[target]
        ):
            return False
    return True


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


def relabel(
    normal: Normal, permutation: tuple[int, int, int]
) -> tuple[int, int, int]:
    image = [-1, -1, -1]
    for colour in range(3):
        image[permutation[colour]] = permutation[normal[colour]]
    values = base(tuple(image))
    return tuple(values[permutation[colour]] for colour in range(3))


def primitive(vector: Matrix) -> tuple[int, ...]:
    denominator = math.lcm(
        *(int(value.q) for value in vector)
    )
    values = [int(value * denominator) for value in vector]
    divisor = math.gcd(*(abs(value) for value in values if value))
    return tuple(value // divisor for value in values)


def main() -> None:
    primary_path = Path(
        "tmp", "full_admissible_potential_cone_verified.json"
    )
    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    normals: tuple[Normal, ...] = tuple(
        tuple(values)
        for values in itertools.product(range(3), repeat=3)
        if all(values[colour] != colour for colour in range(3))
    )
    position = {normal: index for index, normal in enumerate(normals)}
    equality_rows = []
    optional_rows = []
    for colour in range(3):
        for left in normals:
            for right in normals:
                if not all(
                    bits(left)[bit] != bits(right)[bit]
                    for bit in range(3)
                    if bit != colour
                ):
                    continue
                if not allowed(left, right, colour, colour):
                    continue
                equality = [0] * 24
                equality[3 * position[left] + colour] += 1
                equality[3 * position[right] + colour] += 1
                equality_rows.append(equality)
                for row in range(3):
                    for column in range(3):
                        if row == column or not allowed(
                            left, right, row, column
                        ):
                            continue
                        optional = [0] * 24
                        optional[3 * position[left] + row] += 1
                        optional[3 * position[right] + column] += 1
                        optional_rows.append(optional)

    permutations = tuple(itertools.permutations(range(3)))
    q = Matrix(
        [
            [
                relabel(normal, permutation)[colour]
                for permutation in permutations
            ]
            for normal in normals
            for colour in range(3)
        ]
    )
    equality = Matrix(equality_rows)
    optional = Matrix(optional_rows)
    if (
        equality.rank() != 18
        or q.rank() != 6
        or equality * q != Matrix.zeros(len(equality_rows), 6)
    ):
        raise AssertionError("symbolic neutrality audit failed")
    weights = sorted(
        {
            tuple(map(int, row))
            for row in (optional * q).tolist()
        }
    )
    if len(weights) != 9:
        raise AssertionError("symbolic inequality audit failed")
    weight_matrix = Matrix(weights)

    extreme_rays: set[tuple[int, ...]] = set()
    for active in itertools.combinations(range(len(weights)), 5):
        submatrix = Matrix([weights[index] for index in active])
        nullspace = submatrix.nullspace()
        if len(nullspace) != 1:
            continue
        candidate = primitive(nullspace[0])
        values = [
            sum(
                weight[index] * candidate[index]
                for index in range(6)
            )
            for weight in weights
        ]
        if all(value <= 0 for value in values):
            candidate = tuple(-value for value in candidate)
            values = [-value for value in values]
        if all(value >= 0 for value in values):
            extreme_rays.add(candidate)

    expected = {
        tuple(map(int, ray))
        for ray in primary[
            "closed_cone_extreme_rays_in_permuted_basis"
        ]
    }
    if len(extreme_rays) != 6 or extreme_rays != expected:
        raise AssertionError("symbolic extreme-ray audit failed")
    ray_matrix = Matrix.hstack(
        *(Matrix(ray) for ray in sorted(extreme_rays))
    )
    transformed = weight_matrix * ray_matrix
    if (
        ray_matrix.rank() != 6
        or any(value < 0 for value in transformed)
    ):
        raise AssertionError("symbolic cone transform failed")
    transformed_rows = {
        tuple(map(int, row)) for row in transformed.tolist()
    }
    for coordinate in range(6):
        row = tuple(
            10 if index == coordinate else 0
            for index in range(6)
        )
        if row not in transformed_rows:
            raise AssertionError("symbolic coordinate facet missing")

    payload = {
        "verified": True,
        "status": "independent_symbolic_admissible_cone_audit",
        "primary": str(primary_path),
        "primary_sha256": sha256(primary_path),
        "neutrality_rank": equality.rank(),
        "neutrality_nullity": 24 - equality.rank(),
        "basis_rank": q.rank(),
        "optional_transitions": len(optional_rows),
        "unique_inequalities": len(weights),
        "extreme_rays": [list(ray) for ray in sorted(extreme_rays)],
        "extreme_ray_rank": ray_matrix.rank(),
        "coordinate_facets_verified": 6,
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp", "full_admissible_potential_cone_audited.json"
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "verified": True,
                "neutrality_nullity": 6,
                "unique_inequalities": 9,
                "extreme_rays": 6,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
