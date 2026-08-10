"""Verify the universal nonnegative balanced-bridge potential table."""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

Normal = tuple[int, int, int]
PERMUTATIONS = tuple(itertools.permutations(range(3)))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
    return tuple(
        values[permutation[colour]] for colour in range(3)
    )


def universal(normal: Normal) -> tuple[int, int, int]:
    return tuple(
        sum(permuted(normal, permutation)[colour]
            for permutation in PERMUTATIONS)
        for colour in range(3)
    )


def closed_universal(normal: Normal) -> tuple[int, int, int]:
    b0, b1, b2 = bits(normal)
    return (
        10 * (1 - b1 - b2),
        10 * (b2 - b0),
        10 * (b0 + b1 - 1),
    )


def allowed(
    left: Normal,
    right: Normal,
    row: int,
    column: int,
) -> bool:
    return all(
        (row, column) == (target, target)
        or row == left[target]
        or column == right[target]
        for target in range(3)
    )


def saturated(
    left: Normal, right: Normal, colour: int
) -> bool:
    left_bits = bits(left)
    right_bits = bits(right)
    return all(
        left_bits[bit] != right_bits[bit]
        for bit in range(3)
        if bit != colour
    )


def main() -> None:
    normals: tuple[Normal, ...] = tuple(
        itertools.product((1, 2), (0, 2), (0, 1))
    )
    if any(
        universal(normal) != closed_universal(normal)
        for normal in normals
    ):
        raise AssertionError("closed universal potential changed")

    histogram: Counter[int] = Counter()
    ray_histograms = [Counter() for _ in PERMUTATIONS]
    zero_units = []
    permitted = 0
    for left in normals:
        for right in normals:
            for row in range(3):
                for column in range(3):
                    if not allowed(left, right, row, column):
                        continue
                    permitted += 1
                    value = (
                        universal(left)[row]
                        + universal(right)[column]
                    )
                    ray_values = tuple(
                        permuted(left, permutation)[row]
                        + permuted(right, permutation)[column]
                        for permutation in PERMUTATIONS
                    )
                    if any(item < 0 for item in ray_values):
                        raise AssertionError(
                            "negative permitted unit on a permuted ray"
                        )
                    for index, item in enumerate(ray_values):
                        ray_histograms[index][item] += 1
                    if sum(ray_values) != value:
                        raise AssertionError(
                            "universal sum disagrees with its rays"
                        )
                    histogram[value] += 1
                    if value == 0:
                        zero_units.append(
                            (left, right, row, column)
                        )
                        if (
                            row != column
                            or not saturated(left, right, row)
                        ):
                            raise AssertionError(
                                "unexpected zero-potential unit"
                            )
                    elif value < 0:
                        raise AssertionError(
                            "negative permitted unit"
                        )

    expected = Counter({0: 48, 10: 96, 20: 36})
    if (
        permitted != 180
        or histogram != expected
        or len(zero_units) != 48
        or any(
            item
            != Counter({0: 56, 1: 24, 2: 60, 3: 24, 4: 16})
            for item in ray_histograms
        )
    ):
        raise AssertionError("universal unit census changed")

    saturated_units = {
        (left, right, colour, colour)
        for colour in range(3)
        for left in normals
        for right in normals
        if saturated(left, right, colour)
        and allowed(left, right, colour, colour)
    }
    if set(zero_units) != saturated_units:
        raise AssertionError(
            "zero layer is not exactly saturated diagonal"
        )

    theorem = Path(
        "UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md"
    )
    payload = {
        "verified": True,
        "status": (
            "universal_saturated_diagonal_zero_layer_verified"
        ),
        "normal_types": len(normals),
        "ordered_type_pairs": len(normals) ** 2,
        "permitted_oriented_units": permitted,
        "universal_edge_potential_histogram": {
            str(key): value
            for key, value in sorted(histogram.items())
        },
        "each_permuted_ray_potential_histogram": {
            str(key): value
            for key, value in sorted(ray_histograms[0].items())
        },
        "all_six_permuted_rays_nonnegative": True,
        "zero_potential_units": len(zero_units),
        "zero_layer_exactly_saturated_monochromatic_diagonal": True,
        "all_permitted_units_nonnegative": True,
        "bogdanov_matching_input": True,
        "global_conjecture_resolved": False,
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp",
        "universal_saturated_diagonal_zero_layer_verified.json",
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "verified": True,
                "permitted_units": permitted,
                "histogram": dict(sorted(histogram.items())),
                "zero_units": len(zero_units),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
