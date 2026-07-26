"""Independently audit the order-eight parity-orbit support obstruction.

For the odd-parity profile there are two copies of each type 1, 2, 4,
and 7.  For each colour, the saturated diagonal graph is the disjoint
union of two K_2,2 components.  A required full hafnian forces each
component permanent to be nonzero, hence its support contains a perfect
matching.  This program independently enumerates all 7^6 component
support choices and tests the exact nonzero-subhafnian pattern implied
by that decomposition.  It then binds the separately generated CNF and
replayed DRAT proof.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

N = 8
FULL = (1 << N) - 1
TYPES = (1, 1, 2, 2, 4, 4, 7, 7)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def bits(type_id: int) -> tuple[int, int, int]:
    return tuple((type_id >> coordinate) & 1 for coordinate in range(3))


def saturated(colour: int, left: int, right: int) -> bool:
    return all(
        bits(TYPES[left])[coordinate]
        != bits(TYPES[right])[coordinate]
        for coordinate in range(3)
        if coordinate != colour
    )


def components(colour: int):
    adjacency = {
        vertex: {
            other
            for other in range(N)
            if other != vertex and saturated(colour, vertex, other)
        }
        for vertex in range(N)
    }
    unseen = set(range(N))
    result = []
    while unseen:
        root = min(unseen)
        component = {root}
        frontier = [root]
        while frontier:
            vertex = frontier.pop()
            for other in adjacency[vertex]:
                if other not in component:
                    component.add(other)
                    frontier.append(other)
        unseen -= component
        type_classes = {}
        for vertex in component:
            type_classes.setdefault(TYPES[vertex], []).append(vertex)
        if sorted(map(len, type_classes.values())) != [2, 2]:
            raise AssertionError("component is not K_2,2 by type class")
        sides = tuple(
            tuple(sorted(vertices))
            for _type_id, vertices in sorted(type_classes.items())
        )
        result.append(sides)
    result.sort()
    if len(result) != 2:
        raise AssertionError("expected two components")
    return tuple(result)


def component_supports(sides):
    left, right = sides
    edges = tuple((u, v) for u in left for v in right)
    supports = []
    for edge_mask in range(1 << 4):
        chosen = {
            edges[index]
            for index in range(4)
            if (edge_mask >> index) & 1
        }
        diagonal = {(left[0], right[0]), (left[1], right[1])}
        antidiagonal = {(left[0], right[1]), (left[1], right[0])}
        if diagonal <= chosen or antidiagonal <= chosen:
            supports.append(frozenset(chosen))
    if len(supports) != 7:
        raise AssertionError("2x2 support census changed")
    return tuple(supports)


def factor_nonzero(
    subset: int,
    sides,
    support: frozenset[tuple[int, int]],
) -> bool:
    left, right = sides
    selected_left = [u for u in left if (subset >> u) & 1]
    selected_right = [v for v in right if (subset >> v) & 1]
    if len(selected_left) != len(selected_right):
        return False
    if not selected_left:
        return True
    if len(selected_left) == 2:
        # The full component permanent is assumed nonzero, not merely
        # support-feasible.  This is forced by the required full hafnian.
        return True
    return (selected_left[0], selected_right[0]) in support


def colour_states(colour: int):
    colour_components = components(colour)
    support_options = [
        component_supports(component)
        for component in colour_components
    ]
    states = []
    for supports in itertools.product(*support_options):
        true_subsets = frozenset(
            subset
            for subset in range(1, FULL + 1)
            if subset.bit_count() % 2 == 0
            and all(
                factor_nonzero(subset, component, support)
                for component, support in zip(
                    colour_components, supports, strict=True
                )
            )
        )
        states.append(
            {
                "supports": supports,
                "true_subsets": true_subsets,
            }
        )
    if len(states) != 49:
        raise AssertionError("colour-state census changed")
    return colour_components, states


def has_two_colour_partition(left_state, right_state) -> bool:
    return any(
        (FULL ^ subset) in right_state["true_subsets"]
        for subset in left_state["true_subsets"]
        if subset != FULL
    )


def main() -> None:
    per_colour = [colour_states(colour) for colour in range(3)]
    states = [entry[1] for entry in per_colour]
    all_state_mask = (1 << len(states[2])) - 1

    subset_state_masks = []
    for colour in range(3):
        lookup = [0] * (FULL + 1)
        for state_index, state in enumerate(states[colour]):
            for subset in state["true_subsets"]:
                lookup[subset] |= 1 << state_index
        subset_state_masks.append(lookup)

    pair_bad = {}
    for left_colour, right_colour in ((0, 1), (0, 2), (1, 2)):
        pair_bad[left_colour, right_colour] = [
            [
                has_two_colour_partition(left_state, right_state)
                for right_state in states[right_colour]
            ]
            for left_state in states[left_colour]
        ]

    survivors = []
    tested = 0
    for first_index, first in enumerate(states[0]):
        for second_index, second in enumerate(states[1]):
            if pair_bad[0, 1][first_index][second_index]:
                tested += len(states[2])
                continue
            forbidden_third = 0
            for third_index in range(len(states[2])):
                if (
                    pair_bad[0, 2][first_index][third_index]
                    or pair_bad[1, 2][second_index][third_index]
                ):
                    forbidden_third |= 1 << third_index
            for first_subset in first["true_subsets"]:
                if first_subset == FULL:
                    continue
                available = FULL ^ first_subset
                for second_subset in second["true_subsets"]:
                    if (
                        second_subset == FULL
                        or second_subset & first_subset
                    ):
                        continue
                    third_subset = available ^ second_subset
                    if third_subset:
                        forbidden_third |= subset_state_masks[2][
                            third_subset
                        ]
                    if forbidden_third == all_state_mask:
                        break
                if forbidden_third == all_state_mask:
                    break
            allowed_third = all_state_mask ^ forbidden_third
            for third_index in range(len(states[2])):
                tested += 1
                if (allowed_third >> third_index) & 1:
                    survivors.append(
                        (first_index, second_index, third_index)
                    )

    if tested != 49**3:
        raise AssertionError("support-product census changed")
    if survivors:
        raise AssertionError("a support-level parity-orbit model survived")

    primary_path = Path(
        "tmp",
        "eight_vertex_parity_hafnian_supports_certified.json",
    )
    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    cnf = Path(primary["cnf"])
    kissat_path = Path(
        "tmp",
        "eight_vertex_parity_hafnian_supports_kissat_run.json",
    )
    replay_path = Path(
        "tmp",
        "eight_vertex_parity_hafnian_supports_drat_replay.json",
    )
    kissat = json.loads(kissat_path.read_text(encoding="utf-8"))
    replay = json.loads(replay_path.read_text(encoding="utf-8"))
    theorem = Path(
        "EIGHT_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md"
    )
    if (
        primary.get("verified") is not True
        or primary.get("support_variables") != 24
        or primary.get("clauses") != 72
        or primary.get("cnf_sha256") != sha256(cnf)
        or primary.get("theorem_sha256") != sha256(theorem)
        or kissat.get("status") != "UNSAT"
        or kissat.get("cnf_sha256") != sha256(cnf)
        or replay.get("verified") is not True
        or replay.get("cnf_sha256") != sha256(cnf)
        or replay.get("proof_sha256") != kissat.get("proof_sha256")
    ):
        raise AssertionError("CNF/proof/theorem binding changed")

    payload = {
        "verified": True,
        "status": (
            "order_eight_parity_hafnian_supports_independently_audited"
        ),
        "method": (
            "enumerate the seven perfect-matching support patterns of "
            "each of six K_2,2 components and test all 7^6 products"
        ),
        "normal_type_profile": [0, 2, 2, 0, 2, 0, 0, 2],
        "vertex_types": list(TYPES),
        "components": [
            [
                [list(side) for side in component]
                for component in colour_components
            ]
            for colour_components, _states in per_colour
        ],
        "component_supports_with_perfect_matching": 7,
        "states_per_colour": 49,
        "support_triples_tested": tested,
        "surviving_support_triples": len(survivors),
        "interpretation": (
            "zero survivors excludes actual saturated-diagonal hafnian "
            "families for the exceptional abstract set-tree orbit"
        ),
        "primary": str(primary_path),
        "primary_sha256": sha256(primary_path),
        "cnf": str(cnf),
        "cnf_sha256": sha256(cnf),
        "kissat_run": str(kissat_path),
        "kissat_run_sha256": sha256(kissat_path),
        "drat_replay": str(replay_path),
        "drat_replay_sha256": sha256(replay_path),
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp",
        "eight_vertex_parity_hafnian_supports_audited.json",
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
