"""Independent audit of the order-eight balanced set-tree obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

from pysat.solvers import Glucose4

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)



def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reverse_compositions(total: int, parts: int, suffix=()):
    if parts == 1:
        yield (total,) + suffix
        return
    for last in range(total, -1, -1):
        yield from reverse_compositions(
            total - last, parts - 1, (last,) + suffix
        )


def restricted_growth_partitions(size: int):
    labels = [0] * size

    def visit(position: int, maximum: int):
        if position == size:
            blocks = [0] * (maximum + 1)
            for vertex, label in enumerate(labels):
                blocks[label] |= 1 << vertex
            yield tuple(blocks)
            return
        for label in range(maximum + 2):
            labels[position] = label
            yield from visit(position + 1, max(maximum, label))

    yield from visit(1, 0)


def types_from_profile(profile):
    return tuple(
        tuple((type_id >> bit) & 1 for bit in (2, 1, 0))
        for type_id in range(7, -1, -1)
        for _copy in range(profile[type_id])
    )


def transform_type(
    type_id: int,
    permutation: tuple[int, int, int],
    flip_mask: int,
) -> int:
    source = tuple((type_id >> bit) & 1 for bit in range(3))
    target = tuple(
        source[permutation[coordinate]]
        ^ ((flip_mask >> coordinate) & 1)
        for coordinate in range(3)
    )
    return sum(bit << coordinate for coordinate, bit in enumerate(target))


def cube_orbit(profile):
    images = set()
    for permutation in itertools.permutations((2, 1, 0)):
        for flip_mask in range(7, -1, -1):
            image = [0] * 8
            for type_id in range(7, -1, -1):
                image[
                    transform_type(type_id, permutation, flip_mask)
                ] = profile[type_id]
            images.add(tuple(image))
    return images


def admissible_subset(types, mask: int, colour: int) -> bool:
    if mask == 0 or mask.bit_count() & 1:
        return False
    # Types are stored in reversed coordinate order.  Translate colour.
    stored_colour = 2 - colour
    other = [
        coordinate
        for coordinate in range(3)
        if coordinate != stored_colour
    ]
    counts = {}
    for vertex, bit_type in enumerate(types):
        if (mask >> vertex) & 1:
            key = (bit_type[other[0]], bit_type[other[1]])
            counts[key] = counts.get(key, 0) + 1
    return (
        counts.get((0, 0), 0) == counts.get((1, 1), 0)
        and counts.get((0, 1), 0)
        == counts.get((1, 0), 0)
    )


def independent_formula(profile):
    types = types_from_profile(profile)
    full = 255
    variable = {}
    next_variable = 1
    for mask in range(full, 0, -1):
        for colour in (2, 1, 0):
            if admissible_subset(types, mask, colour):
                variable[colour, mask] = next_variable
                next_variable += 1

    clauses = [[variable[colour, full]] for colour in (2, 1, 0)]
    for (colour, mask), parent in list(variable.items())[::-1]:
        if mask.bit_count() < 4:
            continue
        for vertex in range(7, -1, -1):
            if not ((mask >> vertex) & 1):
                continue
            choices = []
            for partner in range(7, -1, -1):
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
                choices.append(witness)
                clauses.extend(
                    (
                        [-witness, variable[colour, pair]],
                        [-witness, variable[colour, remainder]],
                    )
                )
            clauses.append([-parent] + choices)

    for partition in restricted_growth_partitions(8):
        if (
            len(partition) not in (2, 3)
            or any(block.bit_count() & 1 for block in partition)
        ):
            continue
        for colours in itertools.permutations(
            (2, 1, 0), len(partition)
        ):
            literals = []
            for colour, block in zip(
                colours, partition, strict=True
            ):
                entry = variable.get((colour, block))
                if entry is None:
                    break
                literals.append(-entry)
            else:
                clauses.append(literals)
    return next_variable - 1, clauses


def main() -> None:
    primary_path = Path(
        "tmp",
        "eight_vertex_balanced_set_trees_certified.json",
    )
    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    theorem = HERE / "EIGHT_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md"
    if (
        primary.get("verified") is not True
        or primary.get("theorem_sha256") != sha256(theorem)
        or primary.get("balanced_type_multiplicity_profiles") != 57
        or primary.get("profile_orbits") != 8
    ):
        raise AssertionError("primary certificate binding changed")

    profiles = []
    for profile in reverse_compositions(8, 8):
        if all(
            sum(
                profile[type_id]
                for type_id in range(8)
                if (type_id >> bit) & 1
            )
            == 4
            for bit in range(3)
        ):
            profiles.append(profile)
    if (
        len(profiles) != 57
        or set().union(*(cube_orbit(profile) for profile in profiles))
        != set(profiles)
    ):
        raise AssertionError(
            "independent balanced-profile census changed"
        )

    profile_set = set(profiles)
    reps = sorted({min(cube_orbit(profile)) for profile in profiles})
    primary_reps = {
        tuple(row["representative"]): row
        for row in primary["orbits"]
    }
    if len(reps) != 8 or set(reps) != set(primary_reps):
        raise AssertionError("independent cube-orbit census changed")

    rows = []
    unsat_orbits = 0
    sat_orbits = 0
    excluded_profiles = 0
    exceptional_profiles = set()
    for index, profile in enumerate(reps):
        variable_count, clauses = independent_formula(profile)
        with Glucose4(bootstrap_with=clauses) as solver:
            satisfiable = solver.solve()
        orbit_profiles = cube_orbit(profile) & profile_set
        expected_status = primary_reps[profile]["cadical195_status"]
        status = "SAT" if satisfiable else "UNSAT"
        if status != expected_status:
            raise AssertionError(f"orbit {index} solver disagreement")
        if satisfiable:
            sat_orbits += 1
            exceptional_profiles.update(orbit_profiles)
        else:
            unsat_orbits += 1
            excluded_profiles += len(orbit_profiles)
        rows.append(
            {
                "audit_orbit_index": index,
                "representative": list(profile),
                "balanced_profile_orbit_size": len(orbit_profiles),
                "variables": variable_count,
                "clauses": len(clauses),
                "glucose4_status": status,
            }
        )
    if (
        unsat_orbits != 7
        or sat_orbits != 1
        or excluded_profiles != 55
        or exceptional_profiles
        != {
            (0, 2, 2, 0, 2, 0, 0, 2),
            (2, 0, 0, 2, 0, 2, 2, 0),
        }
    ):
        raise AssertionError("independent orbit classification changed")

    cnf = Path(primary["combined_cnf"])
    if sha256(cnf) != primary["combined_cnf_sha256"]:
        raise AssertionError("combined CNF hash changed")
    kissat_path = Path(
        "tmp",
        "eight_vertex_balanced_set_trees_kissat_run.json",
    )
    replay_path = Path(
        "tmp",
        "eight_vertex_balanced_set_trees_drat_replay.json",
    )
    kissat = json.loads(kissat_path.read_text(encoding="utf-8"))
    replay = json.loads(replay_path.read_text(encoding="utf-8"))
    if (
        kissat.get("status") != "UNSAT"
        or kissat.get("cnf_sha256") != sha256(cnf)
        or replay.get("verified") is not True
        or replay.get("cnf_sha256") != sha256(cnf)
        or replay.get("proof_sha256") != kissat.get("proof_sha256")
    ):
        raise AssertionError("external UNSAT proof binding failed")

    payload = {
        "verified": True,
        "status": (
            "eight_vertex_balanced_set_tree_classification_audited"
        ),
        "method": (
            "reverse profiles, restricted-growth partitions, reversed "
            "partner order, Glucose4, and external DRAT replay"
        ),
        "balanced_type_multiplicity_profiles": len(profiles),
        "profile_orbits": len(reps),
        "independent_unsat_orbits": unsat_orbits,
        "independent_sat_orbits": sat_orbits,
        "excluded_profiles": excluded_profiles,
        "exceptional_profiles": [
            list(profile) for profile in sorted(exceptional_profiles)
        ],
        "combined_cnf": str(cnf),
        "combined_cnf_sha256": sha256(cnf),
        "kissat_run": str(kissat_path),
        "kissat_run_sha256": sha256(kissat_path),
        "drat_replay": str(replay_path),
        "drat_replay_sha256": sha256(replay_path),
        "profiles": rows,
        "primary": str(primary_path),
        "primary_sha256": sha256(primary_path),
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp",
        "eight_vertex_balanced_set_trees_audited.json",
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
                "independent_unsat_orbits": unsat_orbits,
                "independent_sat_orbits": sat_orbits,
                "excluded_profiles": excluded_profiles,
                "cnf_sha256": payload["combined_cnf_sha256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
