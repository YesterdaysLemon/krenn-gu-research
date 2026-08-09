"""Independent audit of the order-ten balanced set-tree obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

from pysat.solvers import Glucose4

N = 10
FULL = (1 << N) - 1


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


def cube_image(profile, coordinate_order, toggles):
    image = [0] * 8
    for source, count in enumerate(profile):
        bits = [(source >> bit) & 1 for bit in range(3)]
        target_bits = [
            bits[coordinate_order[position]] ^ toggles[position]
            for position in range(3)
        ]
        target = sum(
            value << position
            for position, value in enumerate(target_bits)
        )
        image[target] = count
    return tuple(image)


def canonical(profile):
    return min(
        cube_image(profile, order, toggles)
        for order in itertools.permutations((2, 1, 0))
        for toggles in itertools.product((1, 0), repeat=3)
    )


def restricted_growth_partitions():
    labels = [0] * N

    def visit(position: int, maximum: int):
        if position == N:
            blocks = [0] * (maximum + 1)
            for vertex, label in enumerate(labels):
                blocks[label] |= 1 << vertex
            yield tuple(blocks)
            return
        for label in range(maximum + 2):
            labels[position] = label
            yield from visit(position + 1, max(maximum, label))

    yield from visit(1, 0)


EVEN_PARTITIONS = tuple(
    partition
    for partition in restricted_growth_partitions()
    if len(partition) in (2, 3)
    and all(block.bit_count() % 2 == 0 for block in partition)
)


def profile_types(profile):
    return tuple(
        tuple((type_id >> bit) & 1 for bit in (2, 1, 0))
        for type_id in range(7, -1, -1)
        for _copy in range(profile[type_id])
    )


def allowed(types, mask: int, colour: int) -> bool:
    if not mask or mask.bit_count() % 2:
        return False
    stored_colour = 2 - colour
    other = [
        coordinate
        for coordinate in range(3)
        if coordinate != stored_colour
    ]
    counts = [0, 0, 0, 0]
    for vertex, bit_type in enumerate(types):
        if (mask >> vertex) & 1:
            counts[
                2 * bit_type[other[0]] + bit_type[other[1]]
            ] += 1
    return counts[0] == counts[3] and counts[1] == counts[2]


def formula(profile):
    types = profile_types(profile)
    variable = {}
    next_variable = 1
    for mask in range(FULL, 0, -1):
        for colour in (2, 1, 0):
            if allowed(types, mask, colour):
                variable[colour, mask] = next_variable
                next_variable += 1

    clauses = [[variable[colour, FULL]] for colour in (2, 1, 0)]
    for (colour, mask), parent in list(variable.items())[::-1]:
        if mask.bit_count() < 4:
            continue
        for vertex in range(N - 1, -1, -1):
            if not ((mask >> vertex) & 1):
                continue
            witnesses = []
            for partner in range(N - 1, -1, -1):
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

    for partition in EVEN_PARTITIONS:
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
        "tmp", "ten_vertex_balanced_set_trees_certified.json"
    )
    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    theorem = Path(
        "TEN_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md"
    )
    if (
        primary.get("verified") is not True
        or primary.get("theorem_sha256") != sha256(theorem)
        or primary.get("profile_orbits") != 10
    ):
        raise AssertionError("primary binding changed")

    profiles = [
        profile
        for profile in reverse_compositions(N, 8)
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
    representatives = sorted({canonical(item) for item in profiles})
    if (
        len(profiles) != 104
        or len(representatives) != 10
        or set(representatives)
        != {
            tuple(row["representative"])
            for row in primary["orbits"]
        }
        or len(EVEN_PARTITIONS) != 2460
    ):
        raise AssertionError("independent orbit census changed")

    rows = []
    for index, representative in enumerate(representatives):
        variables, clauses = formula(representative)
        with Glucose4(bootstrap_with=clauses) as solver:
            satisfiable = solver.solve()
        if satisfiable:
            raise AssertionError(f"audit orbit {index} is SAT")
        rows.append(
            {
                "audit_orbit_index": index,
                "representative": list(representative),
                "variables": variables,
                "clauses": len(clauses),
                "glucose4_status": "UNSAT",
            }
        )

    cnf = Path(primary["combined_cnf"])
    kissat_path = Path(
        "tmp", "ten_vertex_balanced_set_trees_kissat_run.json"
    )
    replay_path = Path(
        "tmp", "ten_vertex_balanced_set_trees_drat_replay.json"
    )
    kissat = json.loads(kissat_path.read_text(encoding="utf-8"))
    replay = json.loads(replay_path.read_text(encoding="utf-8"))
    if (
        sha256(cnf) != primary["combined_cnf_sha256"]
        or kissat.get("status") != "UNSAT"
        or kissat.get("cnf_sha256") != sha256(cnf)
        or replay.get("verified") is not True
        or replay.get("cnf_sha256") != sha256(cnf)
        or replay.get("proof_sha256") != kissat.get("proof_sha256")
    ):
        raise AssertionError("external proof binding failed")

    payload = {
        "verified": True,
        "status": (
            "ten_vertex_balanced_set_trees_independently_audited"
        ),
        "method": (
            "reverse profiles, independent cube action, restricted-growth "
            "partitions, reversed variables, Glucose4, and DRAT replay"
        ),
        "balanced_type_multiplicity_profiles": len(profiles),
        "profile_orbits": len(representatives),
        "independent_unsat_orbits": len(rows),
        "even_set_partitions": len(EVEN_PARTITIONS),
        "combined_cnf": str(cnf),
        "combined_cnf_sha256": sha256(cnf),
        "kissat_run": str(kissat_path),
        "kissat_run_sha256": sha256(kissat_path),
        "drat_replay": str(replay_path),
        "drat_replay_sha256": sha256(replay_path),
        "orbits": rows,
        "primary": str(primary_path),
        "primary_sha256": sha256(primary_path),
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp", "ten_vertex_balanced_set_trees_audited.json"
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
                "orbits": len(representatives),
                "independent_unsat": len(rows),
                "cnf_sha256": payload["combined_cnf_sha256"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
