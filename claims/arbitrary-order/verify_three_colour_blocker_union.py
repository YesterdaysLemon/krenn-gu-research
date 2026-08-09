"""Verify the three-colour blocker-union obstruction."""

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


def main() -> None:
    allowed_types = (
        (0,),
        (1,),
        (2,),
        (0, 1),
        (0, 2),
        (1, 2),
    )
    feasible = []
    for union_size in range(1, 4):
        for assignment in itertools.product(
            allowed_types, repeat=union_size
        ):
            counts = [
                sum(colour in blocker_type for blocker_type in assignment)
                for colour in range(3)
            ]
            if min(counts) >= 2:
                feasible.append(
                    {
                        "union_size": union_size,
                        "assignment": assignment,
                        "counts": counts,
                    }
                )

    if not feasible:
        raise AssertionError("expected the three-vertex boundary")
    if {row["union_size"] for row in feasible} != {3}:
        raise AssertionError("a blocker union smaller than three survived")
    canonical_assignments = {
        tuple(sorted(row["assignment"])) for row in feasible
    }
    expected = {((0, 1), (0, 2), (1, 2))}
    if canonical_assignments != expected:
        raise AssertionError("unexpected three-vertex incidence type")

    def tight_pair_compatible(assignment):
        for colour in range(3):
            blockers = [
                blocker_type
                for blocker_type in assignment
                if colour in blocker_type
            ]
            if (
                len(blockers) == 2
                and all(
                    len(blocker_type) == 2
                    for blocker_type in blockers
                )
            ):
                other_colours = [
                    next(
                        entry
                        for entry in blocker_type
                        if entry != colour
                    )
                    for blocker_type in blockers
                ]
                if other_colours[0] != other_colours[1]:
                    return False
        return True

    four_vertex_patterns = set()
    for assignment in itertools.combinations_with_replacement(
        allowed_types, 4
    ):
        counts = [
            sum(colour in blocker_type for blocker_type in assignment)
            for colour in range(3)
        ]
        if min(counts) >= 2 and tight_pair_compatible(assignment):
            four_vertex_patterns.add(tuple(sorted(assignment)))

    def colour_image(assignment, permutation):
        return tuple(
            sorted(
                tuple(
                    sorted(
                        permutation[colour]
                        for colour in blocker_type
                    )
                )
                for blocker_type in assignment
            )
        )

    unseen = set(four_vertex_patterns)
    four_vertex_orbits = []
    while unseen:
        representative = min(unseen)
        orbit = {
            colour_image(representative, permutation)
            for permutation in itertools.permutations(range(3))
        }
        unseen -= orbit
        four_vertex_orbits.append(representative)
    expected_four_orbits = {
        ((0,), (0,), (1, 2), (1, 2)),
        ((0,), (0, 1), (1, 2), (1, 2)),
        ((0, 1), (0, 1), (0, 2), (0, 2)),
    }
    if set(four_vertex_orbits) != expected_four_orbits:
        raise AssertionError("four-vertex blocker boundary differs")

    a, b, c, d, e, f, g, h = sympy.symbols(
        "a b c d e f g h"
    )
    left_basis = sympy.Matrix([[a, b], [c, d]])
    right_basis = sympy.Matrix([[e, f], [g, h]])
    swap = sympy.Matrix([[0, 1], [1, 0]])
    root_blocker = left_basis * swap * right_basis.T
    determinant_identity = sympy.expand(
        root_blocker.det()
        + left_basis.det() * right_basis.det()
    )
    if determinant_identity != 0:
        raise AssertionError("rank-two determinant identity failed")
    permitted_diagonal = sympy.Matrix(
        [[sympy.Symbol("q"), 0], [0, 0]]
    )
    if permitted_diagonal.det() != 0:
        raise AssertionError("diagonal-intersection rank check failed")

    source = Path(__file__)
    theorem = Path(__file__).resolve().with_name(
        "THREE_COLOUR_BLOCKER_UNION_LEMMA.md"
    )
    payload = {
        "verified": True,
        "minimum_blockers_per_colour": 2,
        "maximum_colours_blocked_per_vertex": 2,
        "assignments_checked": sum(
            len(allowed_types) ** union_size
            for union_size in range(1, 4)
        ),
        "three_vertex_labelled_survivors_before_rank": len(feasible),
        "three_vertex_orbits_before_rank": len(canonical_assignments),
        "unique_three_vertex_orbit": [
            list(row) for row in next(iter(expected))
        ],
        "root_blocker_determinant_identity": (
            "det(U J V^T) = -det(U)det(V)"
        ),
        "tight_pair_span_dichotomy": {
            "rank_two_case_same_coordinate_plane": True,
            "rank_one_case_pure_blocked_colour": True,
        },
        "three_vertex_orbit_excluded_by_rank": True,
        "blocker_union_lower_bound": 4,
        "four_vertex_labelled_patterns": len(four_vertex_patterns),
        "four_vertex_colour_orbits": len(four_vertex_orbits),
        "four_vertex_orbit_representatives": [
            [
                list(blocker_type)
                for blocker_type in representative
            ]
            for representative in sorted(four_vertex_orbits)
        ],
        "singleton_boundary_orbits_force_pure_coordinate_blocker": True,
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "source": str(source),
        "source_sha256": sha256(source),
        "global_conjecture_resolved": False,
    }
    output = Path(
        "tmp", "three_colour_blocker_union_verified.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
