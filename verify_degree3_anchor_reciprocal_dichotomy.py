"""Independently replay the anchor-sensitive degree-three CNF extension."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pysat.card import CardEnc, EncType


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


def clause(line: str) -> list[int]:
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
    source_manifest_path = Path(
        str(manifest["reciprocal_manifest"])
    )
    source = json.loads(
        source_manifest_path.read_text(encoding="utf-8")
    )
    if sha256(base) != manifest["base_cnf_sha256"]:
        raise AssertionError("base hash mismatch")
    if sha256(output) != manifest["output_cnf_sha256"]:
        raise AssertionError("output hash mismatch")
    if (
        sha256(source_manifest_path)
        != manifest["reciprocal_manifest_sha256"]
    ):
        raise AssertionError("source manifest hash mismatch")
    source_cnf = Path(str(source["output_cnf"]))
    if sha256(source_cnf) != source["output_cnf_sha256"]:
        raise AssertionError("source CNF hash mismatch")

    with source_cnf.open("r", encoding="ascii") as first, base.open(
        "r", encoding="ascii"
    ) as second:
        next(first)
        next(second)
        for line_number, line in enumerate(first, start=2):
            if second.readline() != line:
                raise AssertionError(
                    f"source prefix changed at line {line_number}"
                )

    rows = list(source["reciprocals"])
    reciprocal_variables = [
        int(row["reciprocal_variable"]) for row in rows
    ]
    forbidden = [
        int(row["reciprocal_variable"])
        for row in rows
        if int(row["edge"][0]) > 0
        and int(row["colours"][0]) == int(row["colours"][1])
    ]
    if len(rows) != 216 or len(forbidden) != 63:
        raise AssertionError("reciprocal partition changed")
    old_variables, old_clauses = header(base)
    cardinality = CardEnc.atleast(
        lits=reciprocal_variables,
        bound=int(manifest["minimum_reciprocals"]),
        top_id=old_variables,
        encoding=EncType.seqcounter,
    )
    expected = [
        *([-variable] for variable in forbidden),
        *(list(map(int, row)) for row in cardinality.clauses),
    ]

    new_variables, new_clauses = header(output)
    if (
        new_variables != cardinality.nv
        or new_clauses != old_clauses + len(expected)
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
        observed = [clause(line) for line in second]
    if observed != expected:
        raise AssertionError("appended dichotomy clauses changed")

    payload = {
        "verified": True,
        "manifest": str(args.manifest),
        "base_cnf_sha256": sha256(base),
        "output_cnf_sha256": sha256(output),
        "reciprocal_variables": len(reciprocal_variables),
        "forbidden_core_monochromatic_reciprocals": len(forbidden),
        "minimum_reciprocals": int(
            manifest["minimum_reciprocals"]
        ),
        "cardinality_clauses": len(cardinality.clauses),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
