"""Symbolically verify the four-blocker ideal obstruction."""

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


def blocker_orbits():
    allowed = (
        (0,),
        (1,),
        (2,),
        (0, 1),
        (0, 2),
        (1, 2),
    )

    def tight_pair_compatible(assignment):
        for colour in range(3):
            blockers = [
                blocker_type
                for blocker_type in assignment
                if colour in blocker_type
            ]
            if (
                len(blockers) == 2
                and all(len(blocker_type) == 2 for blocker_type in blockers)
            ):
                other = [
                    next(entry for entry in blocker_type if entry != colour)
                    for blocker_type in blockers
                ]
                if other[0] != other[1]:
                    return False
        return True

    patterns = {
        tuple(sorted(assignment))
        for assignment in itertools.combinations_with_replacement(allowed, 4)
        if all(
            sum(colour in blocker_type for blocker_type in assignment) >= 2
            for colour in range(3)
        )
        and tight_pair_compatible(assignment)
    }

    def colour_image(assignment, permutation):
        return tuple(
            sorted(
                tuple(sorted(permutation[colour] for colour in blocker_type))
                for blocker_type in assignment
            )
        )

    unseen = set(patterns)
    representatives = []
    while unseen:
        representative = min(unseen)
        orbit = {
            colour_image(representative, permutation)
            for permutation in itertools.permutations(range(3))
        }
        unseen -= orbit
        representatives.append(representative)
    return patterns, tuple(sorted(representatives))


def root_pair(matrix_left, matrix_right, vector_left, vector_right):
    swap = sympy.Matrix(((0, 1), (1, 0)))
    left = matrix_left * vector_left
    right = matrix_right * vector_right
    return sympy.expand((left.T * swap * right)[0])


def all_pair_values(matrices, vectors):
    return tuple(
        root_pair(matrices[i], matrices[j], vectors[i], vectors[j])
        for i, j in itertools.combinations(range(4), 2)
    )


def assert_common_zero(name, matrices, vectors, target_colour):
    values = all_pair_values(matrices, vectors)
    if any(sympy.simplify(value) != 0 for value in values):
        raise AssertionError(f"{name}: root-pair generators did not vanish")
    target = sympy.prod(vector[target_colour] for vector in vectors)
    if sympy.simplify(target) == 0:
        raise AssertionError(f"{name}: selected diagonal target vanished")
    for colour in set(range(3)) - {target_colour}:
        other = sympy.prod(vector[colour] for vector in vectors)
        if sympy.simplify(other) != 0:
            raise AssertionError(f"{name}: another target colour survived")
    return sympy.factor(target)


def main() -> None:
    patterns, representatives = blocker_orbits()
    expected = {
        ((0,), (0,), (1, 2), (1, 2)),
        ((0,), (0, 1), (1, 2), (1, 2)),
        ((0, 1), (0, 1), (0, 2), (0, 2)),
    }
    if len(patterns) != 12 or set(representatives) != expected:
        raise AssertionError("four-blocker incidence classification differs")

    alpha, beta = sympy.symbols("alpha beta", nonzero=True)
    d0, d1, d2 = sympy.symbols("d0 d1 d2", nonzero=True)
    e0, e2 = sympy.symbols("e0 e2", nonzero=True)

    pure_0 = sympy.Matrix(((1, 0, 0), (0, 0, 0)))
    singleton_0 = sympy.Matrix(
        ((0, alpha, beta), (1, 0, 0))
    )
    plane_01 = sympy.Matrix(((0, 1, 0), (1, 0, 0)))
    plane_12_left = sympy.Matrix(((0, 1, 0), (0, 0, 1)))
    plane_12_right = sympy.Matrix(
        ((0, 0, d2), (0, d1, 0))
    )
    plane_01_left = sympy.Matrix(((1, 0, 0), (0, 1, 0)))
    plane_01_right = sympy.Matrix(
        ((0, d1, 0), (d0, 0, 0))
    )
    plane_02_left = sympy.Matrix(((1, 0, 0), (0, 0, 1)))
    plane_02_right = sympy.Matrix(
        ((0, 0, e2), (e0, 0, 0))
    )

    zero_12_left = sympy.Matrix((0, 1, 1))
    zero_12_right = sympy.Matrix((0, d2, -d1))
    zero_01_left = sympy.Matrix((1, 1, 0))
    zero_01_right = sympy.Matrix((d1, -d0, 0))

    checks = {}
    checks["A_rank_two_singleton"] = assert_common_zero(
        "pattern A, rank-two singleton",
        (
            pure_0,
            singleton_0,
            plane_12_left,
            plane_12_right,
        ),
        (
            sympy.Matrix((0, 1, 0)),
            sympy.Matrix((0, beta, -alpha)),
            zero_12_left,
            zero_12_right,
        ),
        1,
    )
    checks["A_pure_singletons"] = assert_common_zero(
        "pattern A, pure singleton pair",
        (
            pure_0,
            pure_0,
            plane_12_left,
            plane_12_right,
        ),
        (
            sympy.Matrix((0, 1, 0)),
            sympy.Matrix((0, 1, 0)),
            zero_12_left,
            zero_12_right,
        ),
        1,
    )
    checks["B"] = assert_common_zero(
        "pattern B",
        (
            pure_0,
            plane_01,
            plane_12_left,
            plane_12_right,
        ),
        (
            sympy.Matrix((0, 0, 1)),
            sympy.Matrix((0, 0, 1)),
            zero_12_left,
            zero_12_right,
        ),
        2,
    )
    checks["C"] = assert_common_zero(
        "pattern C",
        (
            plane_01_left,
            plane_01_right,
            plane_02_left,
            plane_02_right,
        ),
        (
            zero_01_left,
            zero_01_right,
            sympy.Matrix((0, 1, 0)),
            sympy.Matrix((0, 1, 0)),
        ),
        1,
    )

    source = Path(__file__)
    theorem = Path(__file__).resolve().with_name(
        "FOUR_BLOCKER_IDEAL_OBSTRUCTION.md"
    )
    payload = {
        "verified": True,
        "four_vertex_labelled_patterns": len(patterns),
        "four_vertex_colour_orbits": len(representatives),
        "orbit_representatives": [
            [list(blocker_type) for blocker_type in representative]
            for representative in representatives
        ],
        "symbolic_common_zero_cases": len(checks),
        "selected_nonzero_target_products": {
            name: str(value) for name, value in checks.items()
        },
        "all_six_root_pair_generators_zero_in_every_case": True,
        "four_blocker_patterns_excluded": True,
        "blocker_union_lower_bound": 5,
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "source": str(source),
        "source_sha256": sha256(source),
        "global_conjecture_resolved": False,
    }
    output = Path("tmp", "four_blocker_ideal_obstruction_verified.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
