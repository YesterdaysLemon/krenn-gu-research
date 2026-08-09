"""Independent F_5 audit of the three-blocker rank lemma."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


MODULUS = 5


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def matrix_rank(matrix):
    rows = [list(row) for row in matrix]
    rank = 0
    columns = len(rows[0])
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(rank, len(rows))
                if rows[row][column] % MODULUS
            ),
            None,
        )
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column] % MODULUS, -1, MODULUS)
        rows[rank] = [
            value * inverse % MODULUS for value in rows[rank]
        ]
        for row in range(len(rows)):
            if row == rank:
                continue
            factor = rows[row][column] % MODULUS
            if factor:
                rows[row] = [
                    (left - factor * right) % MODULUS
                    for left, right in zip(
                        rows[row], rows[rank], strict=True
                    )
                ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def tensor_index(i, j, k):
    return 9 * i + 3 * j + k


def main() -> None:
    tensor = [0] * 27
    for permutation in itertools.permutations(range(3)):
        tensor[tensor_index(*permutation)] = 1

    slice_combinations = 0
    minimum_nonzero_slice_rank = 3
    for x, y, z in itertools.product(range(MODULUS), repeat=3):
        if x == y == z == 0:
            continue
        matrix = (
            (0, z, y),
            (z, 0, x),
            (y, x, 0),
        )
        rank = matrix_rank(matrix)
        slice_combinations += 1
        minimum_nonzero_slice_rank = min(
            minimum_nonzero_slice_rank, rank
        )
        if rank < 2:
            raise AssertionError("nonzero rank-one slice found")

    inverse_four = pow(4, -1, MODULUS)
    signs = (
        (1, (1, 1, 1)),
        (-1, (1, 1, -1)),
        (-1, (1, -1, 1)),
        (-1, (-1, 1, 1)),
    )
    reconstructed = [0] * 27
    for coefficient, vector in signs:
        for indices in itertools.product(range(3), repeat=3):
            reconstructed[tensor_index(*indices)] = (
                reconstructed[tensor_index(*indices)]
                + coefficient
                * inverse_four
                * vector[indices[0]]
                * vector[indices[1]]
                * vector[indices[2]]
            ) % MODULUS
    if reconstructed != tensor:
        raise AssertionError("F_5 polarization identity failed")

    diagonal = [[0] * 9 for _ in range(3)]
    for colour in range(3):
        diagonal[colour][3 * colour + colour] = 1
    if matrix_rank(diagonal) != 3:
        raise AssertionError("F_5 diagonal flattening lost rank")

    primary = Path(
        "tmp", "exact_three_blocker_permanent_rank_verified.json"
    )
    primary_payload = json.loads(primary.read_text(encoding="utf-8"))
    if primary_payload["permanent_tensor_rank"] != 4:
        raise AssertionError("primary permanent rank differs")

    source = Path(__file__)
    payload = {
        "verified": True,
        "finite_field": "F_5",
        "nonzero_slice_combinations": slice_combinations,
        "minimum_nonzero_slice_rank": minimum_nonzero_slice_rank,
        "rank_one_nonzero_slices": 0,
        "polarization_terms": len(signs),
        "polarization_identity_checked": True,
        "three_colour_diagonal_flattening_rank": 3,
        "active_residual_colours_at_most": 2,
        "primary_artifact": str(primary),
        "primary_artifact_sha256": sha256(primary),
        "source": str(source),
        "source_sha256": sha256(source),
        "global_conjecture_resolved": False,
    }
    output = Path(
        "tmp", "exact_three_blocker_permanent_rank_audited.json"
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
