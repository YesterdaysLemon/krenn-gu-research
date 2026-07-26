"""Audit the normalized reciprocal-killer split of the dense n=8 CNF."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise AssertionError(f"{path} is not a DIMACS CNF")
    return int(variables), int(clauses)


def clause_set(path: Path, variables: set[int]) -> set[tuple[int, ...]]:
    result: set[tuple[int, ...]] = set()
    with path.open("r", encoding="ascii") as handle:
        next(handle)
        for line in handle:
            clause = tuple(int(token) for token in line.split()[:-1])
            if any(abs(literal) in variables for literal in clause):
                result.add(clause)
    return result


def verify_extension(
    base: Path,
    manifest_path: Path,
    expected_unit: int,
) -> dict[str, object]:
    manifest = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )
    output = Path(str(manifest["output_cnf"]))
    if Path(str(manifest["base_cnf"])) != base:
        raise AssertionError("extension names a different base CNF")
    if manifest["base_cnf_sha256"] != sha256(base):
        raise AssertionError("extension base hash mismatch")
    if manifest["output_cnf_sha256"] != sha256(output):
        raise AssertionError("extension output hash mismatch")
    if manifest["appended_clauses"] != [[expected_unit]]:
        raise AssertionError("extension has an unexpected unit")

    base_variables, base_clauses = header(base)
    output_variables, output_clauses = header(output)
    if (output_variables, output_clauses) != (
        base_variables,
        base_clauses + 1,
    ):
        raise AssertionError("extension header is inconsistent")
    with base.open("r", encoding="ascii") as old, output.open(
        "r", encoding="ascii"
    ) as new:
        next(old)
        next(new)
        for index, line in enumerate(old, start=1):
            if new.readline() != line:
                raise AssertionError(
                    f"extension changed base clause {index}"
                )
        if new.readline() != f"{expected_unit} 0\n":
            raise AssertionError("extension tail unit changed")
        if new.readline():
            raise AssertionError("extension has an unexpected tail")
    return {
        "manifest": str(manifest_path),
        "manifest_sha256": sha256(manifest_path),
        "output_cnf": str(output),
        "output_cnf_sha256": manifest["output_cnf_sha256"],
        "unit": expected_unit,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-cnf",
        type=Path,
        default=Path(
            "tmp/eight_vertex_normalized_killers_flag_max20.cnf"
        ),
    )
    parser.add_argument(
        "--same-manifest",
        type=Path,
        default=Path(
            "tmp/eight_vertex_normalized_killers_"
            "reciprocal_same_max20.json"
        ),
    )
    parser.add_argument(
        "--different-manifest",
        type=Path,
        default=Path(
            "tmp/eight_vertex_normalized_killers_"
            "reciprocal_different_max20.json"
        ),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    relevant = clause_set(args.base_cnf, {905, 968, 989})
    normalized_definition = {
        (-905, -2),
        (-905, -3),
        (-905, -5),
        (-905, -6),
        (-905, -8),
        (-905, -9),
        (-905, 1, 4, 7),
        (905,),
    }
    same_definition = {
        (-968, -4),
        (-968, -5),
        (-968, -6),
        (-968, -7),
        (-968, -8),
        (-968, -9),
        (-968, 1, 2, 3),
    }
    different_definition = {
        (-989, -1),
        (-989, -2),
        (-989, -3),
        (-989, -7),
        (-989, -8),
        (-989, -9),
        (-989, 4, 5, 6),
    }
    required = (
        normalized_definition
        | same_definition
        | different_definition
    )
    missing = required - relevant
    if missing:
        raise AssertionError(
            f"candidate defining clauses changed: {sorted(missing)}"
        )

    same = verify_extension(args.base_cnf, args.same_manifest, 968)
    different = verify_extension(
        args.base_cnf, args.different_manifest, 989
    )
    payload = {
        "verified": True,
        "scope": (
            "n=8 normalized reciprocal-killer partition below 24 blocks"
        ),
        "counted_directed_killer_incidences": 24,
        "density_threshold": 24,
        "normalized_killer_variable": 905,
        "same_colour_reciprocal_variable": 968,
        "same_colour_surviving_entry_variable": 1,
        "different_colour_reciprocal_variable": 989,
        "different_colour_surviving_entry_variable": 4,
        "base_cnf_sha256": sha256(args.base_cnf),
        "cases": [same, different],
    }
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
