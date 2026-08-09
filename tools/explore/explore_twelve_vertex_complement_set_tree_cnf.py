"""Materialize the full set-tree CNF for the 6+6 complement profile."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

N = 12
FULL = (1 << N) - 1
LEFT = (1 << (N // 2)) - 1


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def balanced(mask: int) -> bool:
    return (
        mask != 0
        and mask.bit_count() % 2 == 0
        and (mask & LEFT).bit_count()
        == (mask >> (N // 2)).bit_count()
    )


def set_partitions(mask: int, blocks_left: int):
    if blocks_left == 0:
        if mask == 0:
            yield ()
        return
    if mask.bit_count() < 2 * blocks_left:
        return
    first = mask & -mask
    rest = mask ^ first
    subset = rest
    while True:
        block = first | subset
        remainder = mask ^ block
        if (
            block.bit_count() % 2 == 0
            and remainder.bit_count() >= 2 * (blocks_left - 1)
        ):
            for tail in set_partitions(remainder, blocks_left - 1):
                yield (block,) + tail
        if subset == 0:
            break
        subset = (subset - 1) & rest


EVEN_PARTITIONS = tuple(
    partition
    for block_count in (2, 3)
    for partition in set_partitions(FULL, block_count)
    if all(balanced(block) for block in partition)
)


def incompatibility_clauses(variable):
    for partition in EVEN_PARTITIONS:
        for colours in itertools.permutations(
            range(3), len(partition)
        ):
            yield [
                -variable[colour, block]
                for colour, block in zip(
                    colours, partition, strict=True
                )
            ]


def main() -> None:
    variable = {}
    next_variable = 1
    for colour in range(3):
        for mask in range(1, FULL + 1):
            if balanced(mask):
                variable[colour, mask] = next_variable
                next_variable += 1

    base_clauses = [
        [variable[colour, FULL]] for colour in range(3)
    ]
    # Every balanced set tree containing FULL contains a recursively
    # exposed bipartite perfect matching together with the suffixes of
    # some deletion order.  The S_6 x S_6 vertex action maps that
    # matching and order to the identity pairs in order, so these units
    # are an equisatisfiable symmetry break for tree colour 0.
    identity_pairs = tuple(
        (1 << index) | (1 << (index + N // 2))
        for index in range(N // 2)
    )
    first_complement = FULL ^ identity_pairs[0]
    symmetry_masks = sorted(
        set(identity_pairs + (first_complement,))
    )
    base_clauses.extend(
        [variable[0, mask]] for mask in symmetry_masks
    )
    for (colour, mask), parent in list(variable.items()):
        if mask.bit_count() < 4:
            continue
        for vertex in range(N):
            if not ((mask >> vertex) & 1):
                continue
            witnesses = []
            for partner in range(N):
                if (
                    partner == vertex
                    or not ((mask >> partner) & 1)
                ):
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
                base_clauses.extend(
                    (
                        [-witness, variable[colour, pair]],
                        [-witness, variable[colour, remainder]],
                    )
                )
            base_clauses.append([-parent] + witnesses)

    split_axiom_clauses = 0
    split_axiom_witnesses = 0
    split_axiom_instances = 0
    for (colour, mask), parent in list(variable.items()):
        edge_count = mask.bit_count() // 2
        if edge_count < 4:
            continue
        for left_edge_count in range(
            2, edge_count // 2 + 1
        ):
            left_size = 2 * left_edge_count
            witnesses = []
            subset = mask
            while subset:
                complement = mask ^ subset
                if (
                    subset.bit_count() == left_size
                    and complement
                    and (colour, subset) in variable
                    and (colour, complement) in variable
                    and (
                        subset.bit_count() != complement.bit_count()
                        or subset < complement
                    )
                ):
                    witness = next_variable
                    next_variable += 1
                    witnesses.append(witness)
                    base_clauses.extend(
                        (
                            [-witness, variable[colour, subset]],
                            [
                                -witness,
                                variable[colour, complement],
                            ],
                        )
                    )
                    split_axiom_clauses += 2
                    split_axiom_witnesses += 1
                subset = (subset - 1) & mask
            if not witnesses:
                raise AssertionError(
                    "nonzero parent has no balanced convolution split"
                )
            base_clauses.append([-parent] + witnesses)
            split_axiom_clauses += 1
            split_axiom_instances += 1

    incompatibility_count = sum(
        1 for _clause in incompatibility_clauses(variable)
    )
    clause_count = len(base_clauses) + incompatibility_count
    incompatibility = list(incompatibility_clauses(variable))
    cnf = Path(
        "tmp",
        "twelve_vertex_complement_set_trees_symmetry_broken.cnf",
    )
    cnf.parent.mkdir(parents=True, exist_ok=True)
    with cnf.open("w", encoding="ascii", newline="\n") as handle:
        handle.write(
            f"p cnf {next_variable - 1} {clause_count}\n"
        )
        for clause in base_clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
        for clause in incompatibility:
            handle.write(" ".join(map(str, clause)) + " 0\n")

    # After fixing the first tree's exposed matching and first edge, the
    # residual diagonal S_5 action has five orbits on the first exposed
    # edge of tree 1.  Every model therefore lies in one of these five
    # branches.  Each branch also asserts the edge complement, as
    # required for the first expansion from FULL.
    branch_endpoints = (
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
        (1, 2),
    )
    branches = []
    all_clauses = base_clauses + incompatibility
    for branch_index, (row, column) in enumerate(branch_endpoints):
        pair = (1 << row) | (1 << (column + N // 2))
        branch_units = (
            [variable[1, pair]],
            [variable[1, FULL ^ pair]],
        )
        branch_clauses = all_clauses + list(branch_units)
        branch_cnf = Path(
            "tmp",
            (
                "twelve_vertex_complement_set_trees_branch_"
                f"{branch_index}.cnf"
            ),
        )
        with branch_cnf.open(
            "w", encoding="ascii", newline="\n"
        ) as handle:
            handle.write(
                f"p cnf {next_variable - 1} "
                f"{len(branch_clauses)}\n"
            )
            for clause in branch_clauses:
                handle.write(" ".join(map(str, clause)) + " 0\n")
        branches.append(
            {
                "branch_index": branch_index,
                "tree_1_first_edge_row": row,
                "tree_1_first_edge_column": column,
                "pair_mask": pair,
                "complement_mask": FULL ^ pair,
                "cnf": str(branch_cnf),
                "cnf_sha256": sha256(branch_cnf),
                "clauses": len(branch_clauses),
            }
        )

    # The only hard first-edge orbit is represented by row 0 to column
    # 1 (its transpose is side-exchange equivalent).  In its complement,
    # expand tree 1 at row 1.  The residual S_4 action on indices 2..5
    # leaves exactly two partner orbits: column 0 and column 2.
    hard_first_pair = (1 << 0) | (1 << (1 + N // 2))
    hard_remainder = FULL ^ hard_first_pair
    second_edge_branches = []
    for subbranch_index, second_column in enumerate((0, 2)):
        second_pair = (1 << 1) | (
            1 << (second_column + N // 2)
        )
        subbranch_units = (
            [variable[1, hard_first_pair]],
            [variable[1, hard_remainder]],
            [variable[1, second_pair]],
            [variable[1, hard_remainder ^ second_pair]],
        )
        subbranch_clauses = all_clauses + list(subbranch_units)
        subbranch_cnf = Path(
            "tmp",
            (
                "twelve_vertex_complement_set_trees_hard_"
                f"subbranch_{subbranch_index}.cnf"
            ),
        )
        with subbranch_cnf.open(
            "w", encoding="ascii", newline="\n"
        ) as handle:
            handle.write(
                f"p cnf {next_variable - 1} "
                f"{len(subbranch_clauses)}\n"
            )
            for clause in subbranch_clauses:
                handle.write(" ".join(map(str, clause)) + " 0\n")
        second_edge_branches.append(
            {
                "subbranch_index": subbranch_index,
                "tree_1_second_edge_row": 1,
                "tree_1_second_edge_column": second_column,
                "second_pair_mask": second_pair,
                "second_remainder_mask": (
                    hard_remainder ^ second_pair
                ),
                "cnf": str(subbranch_cnf),
                "cnf_sha256": sha256(subbranch_cnf),
                "clauses": len(subbranch_clauses),
            }
        )

    # Expand once more at row 2.  Each second-edge branch again has two
    # partner orbits under its residual symmetric group.
    third_edge_branches = []
    third_partner_options = {
        0: (2, 3),
        1: (0, 3),
    }
    for second_branch in second_edge_branches:
        subbranch_index = second_branch["subbranch_index"]
        second_pair = second_branch["second_pair_mask"]
        second_remainder = second_branch["second_remainder_mask"]
        for third_index, third_column in enumerate(
            third_partner_options[subbranch_index]
        ):
            third_pair = (1 << 2) | (
                1 << (third_column + N // 2)
            )
            third_units = (
                [variable[1, hard_first_pair]],
                [variable[1, hard_remainder]],
                [variable[1, second_pair]],
                [variable[1, second_remainder]],
                [variable[1, third_pair]],
                [variable[1, second_remainder ^ third_pair]],
            )
            third_clauses = all_clauses + list(third_units)
            third_cnf = Path(
                "tmp",
                (
                    "twelve_vertex_complement_set_trees_third_"
                    f"branch_{subbranch_index}_{third_index}.cnf"
                ),
            )
            with third_cnf.open(
                "w", encoding="ascii", newline="\n"
            ) as handle:
                handle.write(
                    f"p cnf {next_variable - 1} "
                    f"{len(third_clauses)}\n"
                )
                for clause in third_clauses:
                    handle.write(" ".join(map(str, clause)) + " 0\n")
            third_edge_branches.append(
                {
                    "second_subbranch_index": subbranch_index,
                    "third_partner_orbit_index": third_index,
                    "tree_1_third_edge_row": 2,
                    "tree_1_third_edge_column": third_column,
                    "third_pair_mask": third_pair,
                    "third_remainder_mask": (
                        second_remainder ^ third_pair
                    ),
                    "cnf": str(third_cnf),
                    "cnf_sha256": sha256(third_cnf),
                    "clauses": len(third_clauses),
                }
            )

    payload = {
        "status": "exploratory_complete_complement_profile_cnf",
        "profile": [6, 0, 0, 0, 0, 0, 0, 6],
        "normal_types": ["000", "111"],
        "vertices_per_type": 6,
        "variables": next_variable - 1,
        "base_clauses": len(base_clauses),
        "incompatibility_clauses": incompatibility_count,
        "eligible_even_partitions": len(EVEN_PARTITIONS),
        "hafnian_convolution_split_instances": (
            split_axiom_instances
        ),
        "hafnian_convolution_split_witnesses": (
            split_axiom_witnesses
        ),
        "hafnian_convolution_split_clauses": (
            split_axiom_clauses
        ),
        "symmetry_breaking_units": len(symmetry_masks),
        "symmetry_breaking_tree_colour": 0,
        "symmetry_breaking_identity_pairs": list(identity_pairs),
        "symmetry_breaking_first_complement": first_complement,
        "tree_1_first_edge_orbit_branches": branches,
        "hard_first_edge_second_edge_branches": (
            second_edge_branches
        ),
        "hard_second_edge_third_edge_branches": (
            third_edge_branches
        ),
        "clauses": clause_count,
        "cnf": str(cnf),
        "cnf_sha256": sha256(cnf),
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp",
        "twelve_vertex_complement_set_trees_symmetry_broken_cnf.json",
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
