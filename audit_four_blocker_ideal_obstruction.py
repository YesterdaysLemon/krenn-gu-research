"""Independent finite-field audit of the four-blocker obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


MODULUS = 5
SWAP = ((0, 1), (1, 0))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def matrix_vector(matrix, vector):
    return tuple(
        sum(matrix[row][column] * vector[column] for column in range(3))
        % MODULUS
        for row in range(2)
    )


def pair_value(left_matrix, right_matrix, left_vector, right_vector):
    left = matrix_vector(left_matrix, left_vector)
    right = matrix_vector(right_matrix, right_vector)
    return (
        left[0] * right[1] + left[1] * right[0]
    ) % MODULUS


def audit_case(matrices, vectors, target_colour):
    for i, j in itertools.combinations(range(4), 2):
        if pair_value(
            matrices[i], matrices[j], vectors[i], vectors[j]
        ):
            raise AssertionError("finite-field pair generator survived")
    products = [
        (
            vectors[0][colour]
            * vectors[1][colour]
            * vectors[2][colour]
            * vectors[3][colour]
        )
        % MODULUS
        for colour in range(3)
    ]
    if not products[target_colour]:
        raise AssertionError("finite-field selected target vanished")
    if any(
        products[colour]
        for colour in range(3)
        if colour != target_colour
    ):
        raise AssertionError("finite-field extra target survived")


def incidence_orbits():
    masks = tuple(
        mask for mask in range(1, 8) if mask.bit_count() <= 2
    )

    def tight(assignment):
        for colour in range(3):
            bit = 1 << colour
            blockers = [mask for mask in assignment if mask & bit]
            if len(blockers) == 2 and all(
                mask.bit_count() == 2 for mask in blockers
            ):
                if (blockers[0] ^ bit) != (blockers[1] ^ bit):
                    return False
        return True

    patterns = {
        assignment
        for assignment in itertools.combinations_with_replacement(masks, 4)
        if all(
            sum(bool(mask & (1 << colour)) for mask in assignment) >= 2
            for colour in range(3)
        )
        and tight(assignment)
    }

    def permute(mask, permutation):
        image = 0
        for colour in range(3):
            if mask & (1 << colour):
                image |= 1 << permutation[colour]
        return image

    unseen = set(patterns)
    representatives = []
    while unseen:
        representative = min(unseen)
        orbit = {
            tuple(
                sorted(permute(mask, permutation) for mask in representative)
            )
            for permutation in itertools.permutations(range(3))
        }
        unseen -= orbit
        representatives.append(representative)
    return patterns, tuple(sorted(representatives))


def main() -> None:
    patterns, representatives = incidence_orbits()
    expected = {
        (0b001, 0b001, 0b110, 0b110),
        (0b001, 0b011, 0b110, 0b110),
        (0b011, 0b011, 0b101, 0b101),
    }
    if len(patterns) != 12 or set(representatives) != expected:
        raise AssertionError("independent incidence census differs")

    nonzero = range(1, MODULUS)
    cases = {
        "A_rank_two_singleton": 0,
        "A_pure_singletons": 0,
        "B": 0,
        "C": 0,
    }
    pure_0 = ((1, 0, 0), (0, 0, 0))
    plane_01 = ((0, 1, 0), (1, 0, 0))
    plane_12_left = ((0, 1, 0), (0, 0, 1))
    plane_01_left = ((1, 0, 0), (0, 1, 0))
    plane_02_left = ((1, 0, 0), (0, 0, 1))

    for alpha, beta, d1, d2 in itertools.product(
        nonzero, repeat=4
    ):
        singleton_0 = ((0, alpha, beta), (1, 0, 0))
        plane_12_right = ((0, 0, d2), (0, d1, 0))
        zero_left = (0, 1, 1)
        zero_right = (0, d2, -d1 % MODULUS)
        audit_case(
            (
                pure_0,
                singleton_0,
                plane_12_left,
                plane_12_right,
            ),
            (
                (0, 1, 0),
                (0, beta, -alpha % MODULUS),
                zero_left,
                zero_right,
            ),
            1,
        )
        cases["A_rank_two_singleton"] += 1

    for d1, d2 in itertools.product(nonzero, repeat=2):
        plane_12_right = ((0, 0, d2), (0, d1, 0))
        zero_left = (0, 1, 1)
        zero_right = (0, d2, -d1 % MODULUS)
        audit_case(
            (
                pure_0,
                pure_0,
                plane_12_left,
                plane_12_right,
            ),
            ((0, 1, 0), (0, 1, 0), zero_left, zero_right),
            1,
        )
        cases["A_pure_singletons"] += 1
        audit_case(
            (
                pure_0,
                plane_01,
                plane_12_left,
                plane_12_right,
            ),
            ((0, 0, 1), (0, 0, 1), zero_left, zero_right),
            2,
        )
        cases["B"] += 1

    for d0, d1, e0, e2 in itertools.product(
        nonzero, repeat=4
    ):
        plane_01_right = ((0, d1, 0), (d0, 0, 0))
        plane_02_right = ((0, 0, e2), (e0, 0, 0))
        audit_case(
            (
                plane_01_left,
                plane_01_right,
                plane_02_left,
                plane_02_right,
            ),
            (
                (1, 1, 0),
                (d1, -d0 % MODULUS, 0),
                (0, 1, 0),
                (0, 1, 0),
            ),
            1,
        )
        cases["C"] += 1

    primary = Path(
        "tmp", "four_blocker_ideal_obstruction_verified.json"
    )
    primary_payload = json.loads(primary.read_text(encoding="utf-8"))
    if primary_payload["blocker_union_lower_bound"] != 5:
        raise AssertionError("primary lower bound differs")

    source = Path(__file__)
    payload = {
        "verified": True,
        "independent_incidence_encoding": "three-bit masks",
        "four_vertex_labelled_patterns": len(patterns),
        "four_vertex_colour_orbits": len(representatives),
        "finite_field": "F_5",
        "parameter_cases": cases,
        "total_parameter_cases": sum(cases.values()),
        "all_six_root_pair_generators_zero_in_every_case": True,
        "selected_diagonal_target_nonzero_in_every_case": True,
        "four_blocker_patterns_excluded": True,
        "blocker_union_lower_bound": 5,
        "primary_artifact": str(primary),
        "primary_artifact_sha256": sha256(primary),
        "source": str(source),
        "source_sha256": sha256(source),
        "global_conjecture_resolved": False,
    }
    output = Path("tmp", "four_blocker_ideal_obstruction_audited.json")
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
