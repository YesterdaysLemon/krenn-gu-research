"""Independently audit a partially specified exact-support Singular test."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from eight_vertex_degree4_cegar import full_equations
from eight_vertex_sparse_exact import (
    exact_equations,
    local_allowed_edges,
    singular_program,
)
from generate_partial_support_singular import (
    pure_vanishing_equations,
    star_pure_tensors,
)
from learn_singular_fallback_clauses import singular_unit
from search_witness import EquationSystem


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def wsl_path(path: Path) -> str:
    resolved = str(path.resolve())
    if len(resolved) < 3 or resolved[1:3] != ":\\":
        raise ValueError(f"cannot map path into WSL: {resolved}")
    return (
        f"/mnt/{resolved[0].lower()}/"
        + resolved[3:].replace("\\", "/")
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--rerun-singular-wsl", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(
        args.manifest.read_text(encoding="utf-8")
    )
    batch = Path(str(manifest["batch"]))
    if sha256(batch) != manifest["batch_sha256"]:
        raise AssertionError("source batch hash mismatch")
    center_degree = int(manifest["center_degree"])
    system = EquationSystem(8, 3)
    _, flat_names, _ = full_equations(system)
    allowed = {
        9 * system.edge_index[edge] + 3 * first + second
        for edge in local_allowed_edges(center_degree)
        for first in range(3)
        for second in range(3)
    }
    positive = set(map(int, manifest["positive_flat_indices"]))
    negative = set(map(int, manifest["negative_flat_indices"]))
    free = set(map(int, manifest["free_flat_indices"]))
    if (
        positive & negative
        or positive & free
        or negative & free
        or positive | negative | free != allowed
    ):
        raise AssertionError(
            "positive, negative, and free entries do not partition "
            "the structurally allowed entries"
        )
    stars = [
        (
            int(row["center"]),
            tuple(map(int, row["colour_neighbours"])),
        )
        for row in manifest.get("forced_singleton_stars", [])
    ]
    star_descriptors = star_pure_tensors(stars)
    for center, neighbours in stars:
        if (
            not 0 <= center < 8
            or len(neighbours) != 3
            or center in neighbours
            or len(set(neighbours)) != 3
            or any(not 0 <= neighbour < 8 for neighbour in neighbours)
        ):
            raise AssertionError("malformed forced singleton star")
        for colour, neighbour in enumerate(neighbours):
            edge = tuple(sorted((center, neighbour)))
            block = {
                9 * system.edge_index[edge] + 3 * row + column
                for row in range(3)
                for column in range(3)
            }
            diagonal = (
                9 * system.edge_index[edge] + 3 * colour + colour
            )
            if diagonal not in positive or not (
                block - {diagonal}
            ) <= negative:
                raise AssertionError("declared singleton is not cube-forced")
        allowed_edges = set(local_allowed_edges(center_degree))
        for other in range(8):
            if other == center or other in neighbours:
                continue
            edge = tuple(sorted((center, other)))
            if edge not in allowed_edges:
                continue
            block = {
                9 * system.edge_index[edge] + 3 * row + column
                for row in range(3)
                for column in range(3)
            }
            if not block <= negative:
                raise AssertionError(
                    "declared star does not have cube-forced degree three"
                )
    variables = sorted(positive | free)
    variable_names = {
        index: flat_names[index] for index in variables
    }
    equations = exact_equations(system, variable_names)
    descriptors = [
        (
            tuple(map(int, row["vertices"])),
            int(row["target_colour"]),
        )
        for row in manifest.get("pure_tensors", [])
    ]
    if manifest.get("all_pure_tensors_derived_from_forced_stars"):
        if set(descriptors) != set(star_descriptors):
            raise AssertionError(
                "pure tensors do not match the forced-star consequences"
            )
    derived = pure_vanishing_equations(
        system, variable_names, descriptors
    )
    existing = {tuple(sorted(equation.items())) for equation in equations}
    derived = [
        equation
        for equation in derived
        if tuple(sorted(equation.items())) not in existing
    ]
    equations = [*equations, *derived]
    expected = singular_program(
        [variable_names[index] for index in variables],
        equations,
        int(manifest["characteristic"]),
        saturation_names=[
            variable_names[index] for index in sorted(positive)
        ],
    )
    program = Path(str(manifest["program"]))
    if program.read_text(encoding="utf-8") != expected:
        raise AssertionError("Singular source changed")
    if sha256(program) != manifest["program_sha256"]:
        raise AssertionError("Singular source hash mismatch")
    if (
        int(manifest["ring_variables"]) != len(variables)
        or int(manifest["saturated_variables"]) != len(positive)
        or int(manifest["equations"]) != len(equations)
        or int(manifest.get("derived_pure_vanishing_equations", 0))
        != len(derived)
    ):
        raise AssertionError("recorded ideal dimensions changed")

    log = program.with_suffix(".log")
    stderr = program.with_suffix(".stderr.log")
    if args.rerun_singular_wsl:
        result = subprocess.run(
            [
                "wsl.exe",
                "-d",
                "Ubuntu",
                "--",
                "bash",
                "--noprofile",
                "--norc",
                "-lc",
                f"Singular -q '{wsl_path(program)}'",
            ],
            check=False,
            capture_output=True,
        )
        if result.returncode:
            raise RuntimeError(
                f"Singular returned {result.returncode}"
            )
        if result.stderr:
            raise AssertionError("Singular rerun wrote to stderr")
        if not singular_unit(result.stdout.decode("utf-8")):
            raise AssertionError(
                "Singular rerun did not prove a unit ideal"
            )
        rerun = True
    else:
        if not log.is_file() or not stderr.is_file():
            raise AssertionError("Singular result files are missing")
        if stderr.read_text(encoding="utf-8").strip():
            raise AssertionError("Singular wrote to stderr")
        if not singular_unit(log.read_text(encoding="utf-8")):
            raise AssertionError(
                "recorded Singular log is not a unit ideal"
            )
        rerun = False

    payload = {
        "verified": True,
        "manifest": str(args.manifest),
        "manifest_sha256": sha256(args.manifest),
        "program_sha256": sha256(program),
        "positive_entries": len(positive),
        "negative_entries": len(negative),
        "free_entries": len(free),
        "ring_variables": len(variables),
        "equations": len(equations),
        "singular_rerun": rerun,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
