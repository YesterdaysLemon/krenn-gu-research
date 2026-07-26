"""Certify that the exceptional order-eight parity orbit is unrealizable.

The saturated graph of each colour is two disjoint K_2,2 components.
This produces a 24-variable necessary support CNF: every component must
support a perfect matching, while every structurally possible
nonmonochromatic colouring must lose at least one required singleton
edge.  UNSAT excludes all weighted realizations, including cancellations
inside the six full 2x2 permanents.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

from pysat.solvers import Cadical195

N = 8
FULL = (1 << N) - 1
TYPES = (1, 1, 2, 2, 4, 4, 7, 7)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def type_bit(vertex: int, coordinate: int) -> int:
    return (TYPES[vertex] >> coordinate) & 1


def saturated(colour: int, left: int, right: int) -> bool:
    return all(
        type_bit(left, coordinate) != type_bit(right, coordinate)
        for coordinate in range(3)
        if coordinate != colour
    )


def colour_components(colour: int):
    remaining = set(range(N))
    components = []
    while remaining:
        root = min(remaining)
        component = {root}
        frontier = [root]
        while frontier:
            vertex = frontier.pop()
            for other in range(N):
                if (
                    other not in component
                    and other != vertex
                    and saturated(colour, vertex, other)
                ):
                    component.add(other)
                    frontier.append(other)
        type_classes = {}
        for vertex in component:
            type_classes.setdefault(TYPES[vertex], []).append(vertex)
        sides = tuple(
            tuple(sorted(vertices))
            for _type_id, vertices in sorted(type_classes.items())
        )
        if len(sides) != 2 or any(len(side) != 2 for side in sides):
            raise AssertionError("saturated component is not K_2,2")
        components.append(sides)
        remaining -= component
    components.sort()
    if len(components) != 2:
        raise AssertionError("saturated component census changed")
    return tuple(components)


def main() -> None:
    components = tuple(colour_components(colour) for colour in range(3))
    variable = {}
    next_variable = 1
    for colour in range(3):
        for component_index, (left, right) in enumerate(
            components[colour]
        ):
            for left_index, u in enumerate(left):
                for right_index, v in enumerate(right):
                    variable[colour, u, v] = next_variable
                    next_variable += 1

    clauses = []
    component_matching_clauses = 0
    for colour in range(3):
        for left, right in components[colour]:
            e00 = variable[colour, left[0], right[0]]
            e01 = variable[colour, left[0], right[1]]
            e10 = variable[colour, left[1], right[0]]
            e11 = variable[colour, left[1], right[1]]
            # (e00 and e11) or (e01 and e10).
            clauses.extend(
                (
                    [e00, e01],
                    [e00, e10],
                    [e11, e01],
                    [e11, e10],
                )
            )
            component_matching_clauses += 4

    colouring_clauses = set()
    structurally_zero_colourings = 0
    structurally_possible_colourings = 0
    for colouring in itertools.product(range(3), repeat=N):
        if len(set(colouring)) == 1:
            continue
        required_edges = []
        structurally_zero = False
        for colour in range(3):
            selected = {
                vertex
                for vertex, assigned in enumerate(colouring)
                if assigned == colour
            }
            for left, right in components[colour]:
                selected_left = [u for u in left if u in selected]
                selected_right = [v for v in right if v in selected]
                if len(selected_left) != len(selected_right):
                    structurally_zero = True
                    break
                if len(selected_left) == 1:
                    required_edges.append(
                        variable[
                            colour,
                            selected_left[0],
                            selected_right[0],
                        ]
                    )
            if structurally_zero:
                break
        if structurally_zero:
            structurally_zero_colourings += 1
            continue
        structurally_possible_colourings += 1
        colouring_clauses.add(tuple(sorted(-entry for entry in required_edges)))

    if () in colouring_clauses:
        raise AssertionError(
            "an edge-free nonmonochromatic coefficient is structurally nonzero"
        )
    clauses.extend([list(clause) for clause in sorted(colouring_clauses)])
    variable_count = next_variable - 1
    with Cadical195(bootstrap_with=clauses) as solver:
        satisfiable = solver.solve()
    if satisfiable:
        raise AssertionError("exceptional parity support CNF is SAT")

    cnf = Path("tmp", "eight_vertex_parity_hafnian_supports.cnf")
    cnf.parent.mkdir(parents=True, exist_ok=True)
    with cnf.open("w", encoding="ascii", newline="\n") as handle:
        handle.write(f"p cnf {variable_count} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")

    theorem = Path(
        "EIGHT_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md"
    )
    payload = {
        "verified": True,
        "status": "order_eight_parity_hafnian_support_cnf_unsat",
        "normal_type_profile": [0, 2, 2, 0, 2, 0, 0, 2],
        "vertex_types": list(TYPES),
        "components": [
            [
                [list(side) for side in component]
                for component in colour_components
            ]
            for colour_components in components
        ],
        "support_variables": variable_count,
        "component_matching_clauses": component_matching_clauses,
        "nonmonochromatic_colourings": 3**N - 3,
        "structurally_zero_colourings": structurally_zero_colourings,
        "structurally_possible_colourings": (
            structurally_possible_colourings
        ),
        "distinct_colouring_nogoods": len(colouring_clauses),
        "clauses": len(clauses),
        "cadical195_status": "UNSAT",
        "cnf": str(cnf),
        "cnf_sha256": sha256(cnf),
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp",
        "eight_vertex_parity_hafnian_supports_certified.json",
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
