"""Certify the order-eight parity-constrained set-tree obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

from pysat.solvers import Cadical195

Profile = tuple[int, ...]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compositions(total: int, parts: int, prefix=()):
    if parts == 1:
        yield prefix + (total,)
        return
    for first in range(total + 1):
        yield from compositions(
            total - first, parts - 1, prefix + (first,)
        )


def balanced_profiles() -> list[Profile]:
    result = []
    for profile in compositions(8, 8):
        if all(
            sum(
                profile[type_id]
                for type_id in range(8)
                if (type_id >> bit) & 1
            )
            == 4
            for bit in range(3)
        ):
            result.append(profile)
    if len(result) != 57:
        raise AssertionError("balanced profile census changed")
    return result


def transform_type(
    type_id: int,
    permutation: tuple[int, int, int],
    flip_mask: int,
) -> int:
    old = tuple((type_id >> bit) & 1 for bit in range(3))
    new = tuple(
        old[permutation[bit]] ^ ((flip_mask >> bit) & 1)
        for bit in range(3)
    )
    return sum(value << bit for bit, value in enumerate(new))


def orbit(profile: Profile) -> set[Profile]:
    images = set()
    for permutation in itertools.permutations(range(3)):
        for flip_mask in range(8):
            image = [0] * 8
            for type_id, count in enumerate(profile):
                image[
                    transform_type(type_id, permutation, flip_mask)
                ] = count
            images.add(tuple(image))
    return images


def representatives(profiles: list[Profile]) -> list[Profile]:
    result = sorted({min(orbit(profile)) for profile in profiles})
    if len(result) != 8:
        raise AssertionError("cube orbit census changed")
    return result


def profile_types(profile: Profile) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple((type_id >> bit) & 1 for bit in range(3))
        for type_id, count in enumerate(profile)
        for _copy in range(count)
    )


def set_partitions(mask: int):
    if mask == 0:
        yield ()
        return
    first = mask & -mask
    rest = mask ^ first
    subset = rest
    while True:
        block = first | subset
        for tail in set_partitions(mask ^ block):
            yield (block,) + tail
        if subset == 0:
            break
        subset = (subset - 1) & rest


def colour_balanced(
    types: tuple[tuple[int, ...], ...],
    mask: int,
    colour: int,
) -> bool:
    if not mask or mask.bit_count() % 2:
        return False
    first_bit, second_bit = (
        bit for bit in range(3) if bit != colour
    )
    counts = [0, 0, 0, 0]
    for vertex, bit_type in enumerate(types):
        if (mask >> vertex) & 1:
            counts[
                2 * bit_type[first_bit] + bit_type[second_bit]
            ] += 1
    return counts[0] == counts[3] and counts[1] == counts[2]


def build_formula(profile: Profile):
    types = profile_types(profile)
    full = (1 << 8) - 1
    variable = {}
    next_variable = 1
    allowed_counts = []
    for colour in range(3):
        count = 0
        for mask in range(1, full + 1):
            if colour_balanced(types, mask, colour):
                variable[colour, mask] = next_variable
                next_variable += 1
                count += 1
        allowed_counts.append(count)

    clauses = [[variable[colour, full]] for colour in range(3)]
    expansion_clauses = 0
    for (colour, mask), parent in list(variable.items()):
        if mask.bit_count() < 4:
            continue
        for vertex in range(8):
            if not ((mask >> vertex) & 1):
                continue
            witnesses = []
            for partner in range(8):
                if (
                    partner == vertex
                    or not ((mask >> partner) & 1)
                ):
                    continue
                pair = (1 << vertex) | (1 << partner)
                complement = mask ^ pair
                if (
                    (colour, pair) not in variable
                    or (colour, complement) not in variable
                ):
                    continue
                witness = next_variable
                next_variable += 1
                witnesses.append(witness)
                clauses.append(
                    [-witness, variable[colour, pair]]
                )
                clauses.append(
                    [-witness, variable[colour, complement]]
                )
                expansion_clauses += 2
            clauses.append([-parent] + witnesses)
            expansion_clauses += 1

    incompatibility_clauses = 0
    for partition in set_partitions(full):
        if (
            len(partition) not in (2, 3)
            or any(block.bit_count() % 2 for block in partition)
        ):
            continue
        for colours in itertools.permutations(
            range(3), len(partition)
        ):
            if all(
                (colour, block) in variable
                for colour, block in zip(
                    colours, partition, strict=True
                )
            ):
                clauses.append(
                    [
                        -variable[colour, block]
                        for colour, block in zip(
                            colours, partition, strict=True
                        )
                    ]
                )
                incompatibility_clauses += 1

    return (
        next_variable - 1,
        clauses,
        {
            "allowed_subset_counts": allowed_counts,
            "expansion_clauses": expansion_clauses,
            "incompatibility_clauses": incompatibility_clauses,
        },
        variable,
    )


def main() -> None:
    profiles = balanced_profiles()
    profile_set = set(profiles)
    reps = representatives(profiles)
    rows = []
    unsat_formulas = []
    excluded_profiles = 0
    exceptional_profiles = []
    for index, profile in enumerate(reps):
        variable_count, clauses, stats, variable = build_formula(
            profile
        )
        with Cadical195(bootstrap_with=clauses) as solver:
            satisfiable = solver.solve()
            model = solver.get_model() if satisfiable else None
        orbit_profiles = sorted(orbit(profile) & profile_set)
        row = {
            "orbit_index": index,
            "representative": list(profile),
            "balanced_profile_orbit_size": len(orbit_profiles),
            "variables": variable_count,
            "clauses": len(clauses),
            **stats,
            "cadical195_status": "SAT" if satisfiable else "UNSAT",
        }
        if satisfiable:
            positive = {literal for literal in model if literal > 0}
            row["sat_tree_subsets"] = {
                str(colour): [
                    {
                        "mask": mask,
                        "vertices": [
                            vertex
                            for vertex in range(8)
                            if (mask >> vertex) & 1
                        ],
                    }
                    for (entry_colour, mask), entry in sorted(
                        variable.items()
                    )
                    if entry_colour == colour and entry in positive
                ]
                for colour in range(3)
            }
            exceptional_profiles.extend(orbit_profiles)
        else:
            unsat_formulas.append((variable_count, clauses))
            excluded_profiles += len(orbit_profiles)
        rows.append(row)

    if (
        len(unsat_formulas) != 7
        or excluded_profiles != 55
        or len(exceptional_profiles) != 2
        or set(exceptional_profiles)
        != {
            (0, 2, 2, 0, 2, 0, 0, 2),
            (2, 0, 0, 2, 0, 2, 2, 0),
        }
    ):
        raise AssertionError("corrected SAT/UNSAT orbit census changed")

    selector_count = len(unsat_formulas)
    combined = [list(range(1, selector_count + 1))]
    offset = selector_count
    for orbit_index, (variable_count, clauses) in enumerate(
        unsat_formulas
    ):
        selector = orbit_index + 1
        for clause in clauses:
            combined.append(
                [-selector]
                + [
                    (offset + literal)
                    if literal > 0
                    else -(offset - literal)
                    for literal in clause
                ]
            )
        offset += variable_count

    cnf = Path(
        "tmp",
        "eight_vertex_balanced_set_trees_excluded_orbits.cnf",
    )
    cnf.parent.mkdir(parents=True, exist_ok=True)
    with cnf.open("w", encoding="ascii", newline="\n") as handle:
        handle.write(f"p cnf {offset} {len(combined)}\n")
        for clause in combined:
            handle.write(" ".join(map(str, clause)) + " 0\n")

    theorem = Path(
        "EIGHT_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md"
    )
    payload = {
        "verified": True,
        "status": (
            "eight_vertex_balanced_set_tree_orbits_classified"
        ),
        "balanced_type_multiplicity_profiles": len(profiles),
        "cube_symmetry_group_order": 48,
        "profile_orbits": len(reps),
        "local_unsat_orbits": len(unsat_formulas),
        "local_sat_orbits": 1,
        "excluded_profiles": excluded_profiles,
        "exceptional_profiles": [
            list(profile) for profile in sorted(exceptional_profiles)
        ],
        "local_solver": "Cadical195 via PySAT",
        "combined_selectors": selector_count,
        "combined_variables": offset,
        "combined_clauses": len(combined),
        "combined_cnf": str(cnf),
        "combined_cnf_sha256": sha256(cnf),
        "orbits": rows,
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp",
        "eight_vertex_balanced_set_trees_certified.json",
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "verified": True,
                "profiles": len(profiles),
                "orbits": len(reps),
                "excluded_profiles": excluded_profiles,
                "exceptional_profiles": len(exceptional_profiles),
                "combined_variables": offset,
                "combined_clauses": len(combined),
                "cnf_sha256": payload["combined_cnf_sha256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
