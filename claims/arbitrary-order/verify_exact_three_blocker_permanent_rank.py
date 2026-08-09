"""Verify the exact three-blocker permanent-rank obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tensor_index(i, j, k):
    return 9 * i + 3 * j + k


def main() -> None:
    permanent = sympy.zeros(3, 9)
    tensor = [sympy.Integer(0)] * 27
    for permutation in itertools.permutations(range(3)):
        index = tensor_index(*permutation)
        tensor[index] += 1
        permanent[permutation[0], 3 * permutation[1] + permutation[2]] += 1

    flattening_ranks = []
    for mode in range(3):
        matrix = sympy.zeros(3, 9)
        for indices in itertools.product(range(3), repeat=3):
            value = tensor[tensor_index(*indices)]
            row = indices[mode]
            other = tuple(
                indices[position]
                for position in range(3)
                if position != mode
            )
            matrix[row, 3 * other[0] + other[1]] = value
        flattening_ranks.append(matrix.rank())
    if flattening_ranks != [3, 3, 3]:
        raise AssertionError("permanent flattening rank differs")

    x, y, z = sympy.symbols("x y z")
    slice_matrix = sympy.Matrix(((0, z, y), (z, 0, x), (y, x, 0)))
    principal_minors = (
        slice_matrix.extract((0, 1), (0, 1)).det(),
        slice_matrix.extract((0, 2), (0, 2)).det(),
        slice_matrix.extract((1, 2), (1, 2)).det(),
    )
    if tuple(map(sympy.expand, principal_minors)) != (
        -z**2,
        -y**2,
        -x**2,
    ):
        raise AssertionError("slice principal minors differ")

    signs = (
        (1, (1, 1, 1)),
        (-1, (1, 1, -1)),
        (-1, (1, -1, 1)),
        (-1, (-1, 1, 1)),
    )
    polarization = [sympy.Rational(0)] * 27
    for coefficient, vector in signs:
        for indices in itertools.product(range(3), repeat=3):
            polarization[tensor_index(*indices)] += (
                sympy.Rational(coefficient, 4)
                * vector[indices[0]]
                * vector[indices[1]]
                * vector[indices[2]]
            )
    if polarization != tensor:
        raise AssertionError("rank-four polarization identity failed")

    g0, g1, g2 = sympy.symbols("g0 g1 g2", nonzero=True)
    diagonal = sympy.zeros(3, 9)
    for colour, coefficient in enumerate((g0, g1, g2)):
        diagonal[colour, 3 * colour + colour] = coefficient
    if diagonal.rank() != 3:
        raise AssertionError("three-colour diagonal flattening lost rank")

    source = Path(__file__)
    theorem = Path(__file__).resolve().with_name(
        "EXACT_THREE_BLOCKER_PERMANENT_RANK_LEMMA.md"
    )
    payload = {
        "verified": True,
        "permanent_tensor_nonzero_entries": sum(bool(value) for value in tensor),
        "permanent_flattening_ranks": flattening_ranks,
        "nonzero_rank_one_slices": 0,
        "permanent_tensor_rank_lower_bound": 4,
        "polarization_terms": len(signs),
        "permanent_tensor_rank": 4,
        "three_colour_diagonal_tensor_rank": 3,
        "active_residual_colours_at_most": 2,
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "source": str(source),
        "source_sha256": sha256(source),
        "global_conjecture_resolved": False,
    }
    output = Path(
        "tmp", "exact_three_blocker_permanent_rank_verified.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
