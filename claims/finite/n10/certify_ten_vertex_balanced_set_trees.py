"""Certify the order-ten parity-constrained set-tree obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

from pysat.solvers import Cadical195

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


N = 10
FULL = (1 << N) - 1


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


def balanced_profiles():
    profiles = [
        profile
        for profile in compositions(N, 8)
        if all(
            sum(
                profile[type_id]
                for type_id in range(8)
                if (type_id >> bit) & 1
            )
            == N // 2
            for bit in range(3)
        )
    ]
    if len(profiles) != 104:
        raise AssertionError("order-ten profile census changed")
    return profiles


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


def orbit(profile):
    images = set()
    for permutation in itertools.permutations(range(3)):
        for flip_mask in range(8):
            image = [0] * 8
            for type_id, count in enumerate(profile):
                image[
                    transform_type(
                        type_id, permutation, flip_mask
                    )
                ] = count
            images.add(tuple(image))
    return images


def representatives(profiles):
    representatives = sorted({min(orbit(item)) for item in profiles})
    if len(representatives) != 10:
        raise AssertionError("cube orbit census changed")
    return representatives


def profile_types(profile):
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


EVEN_PARTITIONS = tuple(
    partition
    for partition in set_partitions(FULL)
    if len(partition) in (2, 3)
    and all(block.bit_count() % 2 == 0 for block in partition)
)


def colour_balanced(types, mask: int, colour: int) -> bool:
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


def build_formula(profile):
    types = profile_types(profile)
    variable = {}
    next_variable = 1
    for colour in range(3):
        for mask in range(1, FULL + 1):
            if colour_balanced(types, mask, colour):
                variable[colour, mask] = next_variable
                next_variable += 1

    clauses = [[variable[colour, FULL]] for colour in range(3)]
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
                clauses.extend(
                    (
                        [-witness, variable[colour, pair]],
                        [-witness, variable[colour, remainder]],
                    )
                )
            clauses.append([-parent] + witnesses)

    incompatibility = 0
    for partition in EVEN_PARTITIONS:
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
                incompatibility += 1
    return next_variable - 1, clauses, incompatibility


def main() -> None:
    profiles = balanced_profiles()
    reps = representatives(profiles)
    rows = []
    formulas = []
    for index, profile in enumerate(reps):
        variables, clauses, incompatibility = build_formula(profile)
        with Cadical195(bootstrap_with=clauses) as solver:
            satisfiable = solver.solve()
        if satisfiable:
            raise AssertionError(f"orbit {index} is SAT")
        orbit_size = len(orbit(profile) & set(profiles))
        formulas.append((variables, clauses))
        rows.append(
            {
                "orbit_index": index,
                "representative": list(profile),
                "balanced_profile_orbit_size": orbit_size,
                "variables": variables,
                "clauses": len(clauses),
                "incompatibility_clauses": incompatibility,
                "cadical195_status": "UNSAT",
            }
        )
    if sum(row["balanced_profile_orbit_size"] for row in rows) != 104:
        raise AssertionError("profile orbits do not cover the domain")

    selector_count = len(reps)
    combined = [list(range(1, selector_count + 1))]
    offset = selector_count
    for index, (variables, clauses) in enumerate(formulas):
        selector = index + 1
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
        offset += variables

    cnf = Path(
        "tmp", "ten_vertex_balanced_set_trees_all_orbits.cnf"
    )
    with cnf.open("w", encoding="ascii", newline="\n") as handle:
        handle.write(f"p cnf {offset} {len(combined)}\n")
        for clause in combined:
            handle.write(" ".join(map(str, clause)) + " 0\n")

    theorem = HERE / "TEN_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md"
    payload = {
        "verified": True,
        "status": (
            "ten_vertex_balanced_set_tree_orbits_certified"
        ),
        "balanced_type_multiplicity_profiles": len(profiles),
        "cube_symmetry_group_order": 48,
        "profile_orbits": len(reps),
        "local_unsat_orbits": len(rows),
        "even_set_partitions": len(EVEN_PARTITIONS),
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
        "tmp", "ten_vertex_balanced_set_trees_certified.json"
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
                "combined_variables": offset,
                "combined_clauses": len(combined),
                "cnf_sha256": payload["combined_cnf_sha256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
