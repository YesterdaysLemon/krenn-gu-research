"""Independent reconstruction and audit of the n=12 complement profile."""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Glucose4

N = 12
SIDE = N // 2
FULL = (1 << N) - 1
LEFT = (1 << SIDE) - 1


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def balanced(mask: int) -> bool:
    left_count = (mask & LEFT).bit_count()
    right_count = (mask >> SIDE).bit_count()
    return mask != 0 and left_count == right_count


def restricted_growth_partitions(block_count: int):
    labels = [0] * N

    def recurse(position: int, maximum: int):
        if position == N:
            if maximum + 1 != block_count:
                return
            masks = [0] * block_count
            for vertex, label in enumerate(labels):
                masks[label] |= 1 << vertex
            yield tuple(masks)
            return
        upper = min(maximum + 1, block_count - 1)
        for label in range(upper + 1):
            labels[position] = label
            yield from recurse(position + 1, max(maximum, label))

    yield from recurse(1, 0)


def independent_formula():
    variable = {}
    next_variable = 1
    for colour in range(3):
        for mask in range(1, FULL + 1):
            if balanced(mask) and mask.bit_count() % 2 == 0:
                variable[colour, mask] = next_variable
                next_variable += 1

    clauses = [[variable[colour, FULL]] for colour in range(3)]
    identity_pairs = [
        (1 << index) | (1 << (index + SIDE))
        for index in range(SIDE)
    ]
    symmetry_masks = sorted(
        set(identity_pairs + [FULL ^ identity_pairs[0]])
    )
    clauses.extend([variable[0, mask]] for mask in symmetry_masks)

    membership_items = tuple(variable.items())
    expansion_instances = 0
    expansion_witnesses = 0
    for (colour, mask), parent in membership_items:
        if mask.bit_count() < 4:
            continue
        vertices = [
            vertex for vertex in range(N) if mask & (1 << vertex)
        ]
        for vertex in vertices:
            witnesses = []
            for partner in vertices:
                if partner == vertex:
                    continue
                pair = (1 << vertex) | (1 << partner)
                remainder = mask ^ pair
                if (
                    (colour, pair) not in variable
                    or (colour, remainder) not in variable
                ):
                    continue
                witness = next_variable
                next_variable += 1
                witnesses.append(witness)
                clauses.append(
                    [-witness, variable[colour, pair]]
                )
                clauses.append(
                    [-witness, variable[colour, remainder]]
                )
                expansion_witnesses += 1
            clauses.append([-parent] + witnesses)
            expansion_instances += 1

    split_instances = 0
    split_witnesses = 0
    for (colour, mask), parent in membership_items:
        pair_count = mask.bit_count() // 2
        if pair_count < 4:
            continue
        vertices = [
            vertex for vertex in range(N) if mask & (1 << vertex)
        ]
        for left_pair_count in range(
            2, pair_count // 2 + 1
        ):
            left_size = 2 * left_pair_count
            witnesses = []
            for chosen in itertools.combinations(vertices, left_size):
                subset = sum(1 << vertex for vertex in chosen)
                complement = mask ^ subset
                if (
                    subset.bit_count() == complement.bit_count()
                    and subset > complement
                ):
                    continue
                if (
                    (colour, subset) not in variable
                    or (colour, complement) not in variable
                ):
                    continue
                witness = next_variable
                next_variable += 1
                witnesses.append(witness)
                clauses.append(
                    [-witness, variable[colour, subset]]
                )
                clauses.append(
                    [-witness, variable[colour, complement]]
                )
                split_witnesses += 1
            if not witnesses:
                raise AssertionError("split instance has no witness")
            clauses.append([-parent] + witnesses)
            split_instances += 1

    eligible_partitions = []
    for block_count in (2, 3):
        for partition in restricted_growth_partitions(block_count):
            if all(
                block.bit_count() % 2 == 0 and balanced(block)
                for block in partition
            ):
                eligible_partitions.append(partition)
                for colours in itertools.permutations(
                    range(3), block_count
                ):
                    clauses.append(
                        [
                            -variable[colour, block]
                            for colour, block in zip(
                                colours, partition, strict=True
                            )
                        ]
                    )

    stats = {
        "membership_variables": len(variable),
        "variables": next_variable - 1,
        "clauses": len(clauses),
        "eligible_partitions": len(eligible_partitions),
        "expansion_instances": expansion_instances,
        "expansion_witnesses": expansion_witnesses,
        "split_instances": split_instances,
        "split_witnesses": split_witnesses,
    }
    return variable, clauses, stats


def partner_orbits(values, group):
    uncovered = set(values)
    rows = []
    while uncovered:
        seed = min(uncovered)
        orbit = {permutation[seed] for permutation in group}
        if not orbit <= uncovered:
            raise AssertionError("partner orbit escaped its state")
        rows.append(tuple(sorted(orbit)))
        uncovered -= orbit
    return rows


def independent_branch_tree(variable):
    group = [
        permutation
        for permutation in itertools.permutations(range(SIDE))
        if permutation[0] == 0 and permutation[1] == 1
    ]
    leaves = []
    local_covers = []

    def recurse(pairs, used_rows, used_columns, stabilizer, weight):
        if len(pairs) == SIDE:
            leaves.append((tuple(pairs), weight))
            return
        row = min(set(range(SIDE)) - set(used_rows))
        row_stabilizer = [
            permutation
            for permutation in stabilizer
            if permutation[row] == row
        ]
        columns = sorted(set(range(SIDE)) - set(used_columns))
        orbits = partner_orbits(columns, row_stabilizer)
        if set().union(*map(set, orbits)) != set(columns):
            raise AssertionError("local partner cover is incomplete")
        local_covers.append(
            {
                "depth": len(pairs),
                "row": row,
                "available_columns": columns,
                "orbits": [list(orbit) for orbit in orbits],
            }
        )
        for orbit in orbits:
            column = orbit[0]
            next_stabilizer = [
                permutation
                for permutation in row_stabilizer
                if permutation[column] == column
            ]
            recurse(
                pairs + [(row, column)],
                used_rows + [row],
                used_columns + [column],
                next_stabilizer,
                weight * len(orbit),
            )

    recurse([(0, 1)], [0], [1], group, 1)
    if len(leaves) != 16 or sum(weight for _pairs, weight in leaves) != 120:
        raise AssertionError("independent orbit tree has wrong cover")

    branches = []
    same_pair = (1 << 0) | (1 << SIDE)
    branches.append(
        {
            "kind": "same_first_partner",
            "permutation": None,
            "orbit_weight": 1,
            "assumptions": [
                variable[1, same_pair],
                variable[1, FULL ^ same_pair],
            ],
        }
    )
    for pairs, weight in leaves:
        remainder = FULL
        assumptions = []
        permutation = []
        for row, column in pairs:
            permutation.append(column)
            pair = (1 << row) | (1 << (column + SIDE))
            assumptions.append(variable[1, pair])
            remainder ^= pair
            if remainder:
                assumptions.append(variable[1, remainder])
        if remainder:
            raise AssertionError("branch is not a perfect matching")
        branches.append(
            {
                "kind": "hard_chain_orbit",
                "permutation": permutation,
                "orbit_weight": weight,
                "assumptions": assumptions,
            }
        )
    return branches, local_covers


def audit_selector_extension(base, selector, branches):
    if selector.clauses[: len(base.clauses)] != base.clauses:
        raise AssertionError("selector CNF does not preserve base prefix")
    selectors = [
        base.nv + index + 1 for index in range(len(branches))
    ]
    expected = [selectors]
    for selector_variable, branch in zip(
        selectors, branches, strict=True
    ):
        expected.extend(
            [-selector_variable, literal]
            for literal in branch["assumptions"]
        )
    actual = selector.clauses[len(base.clauses) :]
    if actual != expected:
        raise AssertionError("selector extension differs from audit")
    if selector.nv != base.nv + len(branches):
        raise AssertionError("selector variable count differs")
    return len(expected)


def main() -> None:
    started = time.perf_counter()
    variable, clauses, formula_stats = independent_formula()
    base_path = Path(
        "tmp",
        "twelve_vertex_complement_set_trees_symmetry_broken.cnf",
    )
    selector_path = Path(
        "tmp",
        "twelve_vertex_complement_profile_selector.cnf",
    )
    base = CNF(from_file=str(base_path))
    selector = CNF(from_file=str(selector_path))
    branches, local_covers = independent_branch_tree(variable)
    selector_extension_clauses = audit_selector_extension(
        base, selector, branches
    )

    if formula_stats["variables"] != base.nv:
        raise AssertionError("independent variable count differs")
    if formula_stats["clauses"] != len(base.clauses):
        raise AssertionError("independent clause count differs")

    decisions = []
    with Glucose4(bootstrap_with=clauses) as solver:
        for index, branch in enumerate(branches):
            branch_started = time.perf_counter()
            satisfiable = solver.solve(
                assumptions=branch["assumptions"]
            )
            row = {
                "branch_index": index,
                "kind": branch["kind"],
                "permutation": branch["permutation"],
                "orbit_weight": branch["orbit_weight"],
                "status": "SAT" if satisfiable else "UNSAT",
                "solve_seconds": time.perf_counter() - branch_started,
            }
            decisions.append(row)
            print(json.dumps(row), flush=True)
            if satisfiable:
                break

    verified = (
        len(decisions) == len(branches)
        and all(row["status"] == "UNSAT" for row in decisions)
    )
    payload = {
        "verified": verified,
        "independent_formula_method": (
            "restricted-growth partitions and combination splits"
        ),
        "independent_solver": "Glucose4",
        "formula_stats": formula_stats,
        "base_cnf": str(base_path),
        "base_cnf_sha256": sha256(base_path),
        "base_count_match": True,
        "selector_cnf": str(selector_path),
        "selector_cnf_sha256": sha256(selector_path),
        "selector_extension_clauses": selector_extension_clauses,
        "selector_prefix_and_extension_exact": True,
        "canonical_branches": len(branches),
        "hard_chain_orbits": len(branches) - 1,
        "hard_partner_chains_covered": sum(
            branch["orbit_weight"] for branch in branches[1:]
        ),
        "local_orbit_covers_checked": len(local_covers),
        "decisions": decisions,
        "elapsed_seconds": time.perf_counter() - started,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output = Path(
        "tmp",
        "twelve_vertex_complement_profile_audited.json",
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "verified",
                    "formula_stats",
                    "canonical_branches",
                    "hard_partner_chains_covered",
                    "elapsed_seconds",
                )
            },
            indent=2,
        )
    )
    if not verified:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
