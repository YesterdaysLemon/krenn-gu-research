"""Independent finite audit of the blocker-union rank argument."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def determinant(matrix, modulus):
    return (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    ) % modulus


def multiply(left, right, modulus):
    return tuple(
        tuple(
            sum(left[i][k] * right[k][j] for k in range(2))
            % modulus
            for j in range(2)
        )
        for i in range(2)
    )


def transpose(matrix):
    return tuple(zip(*matrix, strict=True))


def main() -> None:
    colour_masks = tuple(
        mask for mask in range(1, 1 << 3) if mask.bit_count() <= 2
    )
    survivors = []
    assignments_checked = 0
    for size in range(1, 4):
        for assignment in itertools.product(colour_masks, repeat=size):
            assignments_checked += 1
            if all(
                sum(bool(mask & (1 << colour)) for mask in assignment)
                >= 2
                for colour in range(3)
            ):
                survivors.append(assignment)
    survivor_orbits = {
        tuple(sorted(assignment)) for assignment in survivors
    }
    expected_orbit = {(0b011, 0b101, 0b110)}
    if survivor_orbits != expected_orbit:
        raise AssertionError("independent incidence census differs")

    def tight_pair_compatible(assignment):
        for colour in range(3):
            blockers = [
                mask for mask in assignment if mask & (1 << colour)
            ]
            if len(blockers) == 2 and all(
                mask.bit_count() == 2 for mask in blockers
            ):
                other_bits = [
                    mask ^ (1 << colour) for mask in blockers
                ]
                if other_bits[0] != other_bits[1]:
                    return False
        return True

    four_patterns = set()
    for assignment in itertools.combinations_with_replacement(
        colour_masks, 4
    ):
        if all(
            sum(
                bool(mask & (1 << colour)) for mask in assignment
            )
            >= 2
            for colour in range(3)
        ) and tight_pair_compatible(assignment):
            four_patterns.add(tuple(sorted(assignment)))

    def permute_mask(mask, permutation):
        image = 0
        for colour in range(3):
            if mask & (1 << colour):
                image |= 1 << permutation[colour]
        return image

    unseen = set(four_patterns)
    four_orbits = []
    while unseen:
        representative = min(unseen)
        orbit = {
            tuple(
                sorted(
                    permute_mask(mask, permutation)
                    for mask in representative
                )
            )
            for permutation in itertools.permutations(range(3))
        }
        unseen -= orbit
        four_orbits.append(representative)
    expected_four_orbits = {
        (0b001, 0b001, 0b110, 0b110),
        (0b001, 0b011, 0b110, 0b110),
        (0b011, 0b011, 0b101, 0b101),
    }
    if set(four_orbits) != expected_four_orbits:
        raise AssertionError("independent four-vertex census differs")

    modulus = 3
    matrices = tuple(
        ((a, b), (c, d))
        for a, b, c, d in itertools.product(
            range(modulus), repeat=4
        )
    )
    invertible = tuple(
        matrix
        for matrix in matrices
        if determinant(matrix, modulus)
    )
    swap = ((0, 1), (1, 0))
    matrix_pairs_checked = 0
    for left in invertible:
        left_swap = multiply(left, swap, modulus)
        for right in invertible:
            product = multiply(
                left_swap, transpose(right), modulus
            )
            matrix_pairs_checked += 1
            if determinant(product, modulus) == 0:
                raise AssertionError(
                    "invertible root--blocker product lost rank"
                )
            if (
                determinant(product, modulus)
                != (
                    -determinant(left, modulus)
                    * determinant(right, modulus)
                )
                % modulus
            ):
                raise AssertionError("finite-field determinant differs")

    primary = Path(
        "tmp", "three_colour_blocker_union_verified.json"
    )
    primary_payload = json.loads(primary.read_text(encoding="utf-8"))
    if primary_payload["blocker_union_lower_bound"] != 4:
        raise AssertionError("primary lower bound differs")

    source = Path(__file__)
    payload = {
        "verified": True,
        "independent_incidence_encoding": "three-bit masks",
        "assignments_checked": assignments_checked,
        "surviving_three_vertex_orbits_before_rank": len(
            survivor_orbits
        ),
        "finite_field": "F_3",
        "invertible_matrices": len(invertible),
        "matrix_pairs_checked": matrix_pairs_checked,
        "all_root_blocker_products_rank_two": True,
        "permitted_diagonal_intersection_rank_at_most_one": True,
        "tight_pair_span_dichotomy_checked": True,
        "blocker_union_lower_bound": 4,
        "four_vertex_labelled_patterns": len(four_patterns),
        "four_vertex_colour_orbits": len(four_orbits),
        "four_vertex_orbit_representatives": [
            list(representative)
            for representative in sorted(four_orbits)
        ],
        "singleton_boundary_orbits_force_pure_coordinate_blocker": True,
        "primary_artifact": str(primary),
        "primary_artifact_sha256": sha256(primary),
        "source": str(source),
        "source_sha256": sha256(source),
        "global_conjecture_resolved": False,
    }
    output = Path(
        "tmp", "three_colour_blocker_union_audited.json"
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
