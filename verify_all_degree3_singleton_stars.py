"""Independently replay all conditional degree-three singleton stars."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from augment_all_degree3_singleton_stars import extension


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
        raise AssertionError("invalid DIMACS header")
    return int(variables), int(clauses)


def parse(line: str) -> list[int]:
    values = list(map(int, line.split()))
    if not values or values[-1] != 0:
        raise AssertionError("unterminated clause")
    return values[:-1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(
        args.manifest.read_text(encoding="utf-8")
    )
    base = Path(str(manifest["base_cnf"]))
    output = Path(str(manifest["output_cnf"]))
    if sha256(base) != manifest["base_cnf_sha256"]:
        raise AssertionError("base CNF hash mismatch")
    if sha256(output) != manifest["output_cnf_sha256"]:
        raise AssertionError("output CNF hash mismatch")
    old_variables, old_clauses = header(base)
    expected, rows, new_variables = extension(old_variables)
    if manifest["neighbourhoods"] != rows:
        raise AssertionError("neighbourhood enumeration changed")
    if (
        int(manifest["neighbourhood_indicators"]) != len(rows)
        or int(manifest["appended_clauses"]) != len(expected)
    ):
        raise AssertionError("extension counts changed")
    new_header = header(output)
    if new_header != (
        new_variables,
        old_clauses + len(expected),
    ):
        raise AssertionError("output DIMACS header mismatch")

    with base.open("r", encoding="ascii") as first, output.open(
        "r", encoding="ascii"
    ) as second:
        next(first)
        next(second)
        for line_number, line in enumerate(first, start=2):
            if second.readline() != line:
                raise AssertionError(
                    f"base prefix changed at line {line_number}"
                )
        observed = [parse(line) for line in second]
    if observed != expected:
        raise AssertionError("singleton-star clause tail changed")

    payload = {
        "verified": True,
        "manifest": str(args.manifest),
        "base_cnf_sha256": sha256(base),
        "output_cnf_sha256": sha256(output),
        "neighbourhood_indicators": len(rows),
        "appended_clauses": len(expected),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
