"""Encode the anchor-sensitive branch of the degree-three e=19 split.

This branch assumes that the three normalized star edges are the only
monochromatic singleton blocks.  It forbids every monochromatic reciprocal
killer in the seven-vertex core and requires at least seven reciprocal
killer edges in total, as implied by the reciprocal-anchor incidence count.
"""

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
        raise ValueError(f"{path} is not DIMACS CNF")
    return int(variables), int(clauses)


def require_prefix(prefix: Path, extension: Path) -> None:
    with prefix.open("r", encoding="ascii") as first, extension.open(
        "r", encoding="ascii"
    ) as second:
        next(first)
        next(second)
        for line_number, line in enumerate(first, start=2):
            if second.readline() != line:
                raise AssertionError(
                    f"source prefix changed at line {line_number}"
                )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument(
        "--reciprocal-manifest", type=Path, required=True
    )
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--minimum-reciprocals", type=int, default=7)
    args = parser.parse_args()

    source = json.loads(
        args.reciprocal_manifest.read_text(encoding="utf-8")
    )
    if (
        int(source["center_degree"]),
        int(source["candidate_base"]),
        int(source["minimum_reciprocals"]),
    ) != (3, 750, 5):
        raise AssertionError(
            "unexpected source reciprocal-cardinality encoding"
        )
    source_cnf = Path(str(source["output_cnf"]))
    if sha256(source_cnf) != source["output_cnf_sha256"]:
        raise AssertionError("source reciprocal CNF hash mismatch")
    require_prefix(source_cnf, args.base_cnf)

    old_variables, old_clauses = header(args.base_cnf)
    reciprocal_rows = list(source["reciprocals"])
    reciprocal_variables = [
        int(row["reciprocal_variable"]) for row in reciprocal_rows
    ]
    if len(reciprocal_variables) != 216:
        raise AssertionError("expected 216 reciprocal variables")
    forbidden = [
        int(row["reciprocal_variable"])
        for row in reciprocal_rows
        if int(row["edge"][0]) > 0
        and int(row["colours"][0]) == int(row["colours"][1])
    ]
    if len(forbidden) != 63:
        raise AssertionError(
            "expected 21 core edges times three diagonal colours"
        )

    cardinality = CardEnc.atleast(
        lits=reciprocal_variables,
        bound=args.minimum_reciprocals,
        top_id=old_variables,
        encoding=EncType.seqcounter,
    )
    appended = [
        *([-variable] for variable in forbidden),
        *(list(map(int, clause)) for clause in cardinality.clauses),
    ]
    new_variables = int(cardinality.nv)
    new_clauses = old_clauses + len(appended)
    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    with args.base_cnf.open("r", encoding="ascii") as reader, (
        args.output_cnf.open("w", encoding="ascii")
    ) as writer:
        next(reader)
        writer.write(f"p cnf {new_variables} {new_clauses}\n")
        for line in reader:
            writer.write(line)
        for clause in appended:
            writer.write(" ".join(map(str, clause)) + " 0\n")

    payload = {
        "scope": (
            "anchor-sensitive no-extra-monochromatic-singleton branch"
        ),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "reciprocal_manifest": str(args.reciprocal_manifest),
        "reciprocal_manifest_sha256": sha256(
            args.reciprocal_manifest
        ),
        "source_reciprocal_cnf": str(source_cnf),
        "source_reciprocal_cnf_sha256": sha256(source_cnf),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "old_variables": old_variables,
        "old_clauses": old_clauses,
        "new_variables": new_variables,
        "new_clauses": new_clauses,
        "reciprocal_variables": len(reciprocal_variables),
        "forbidden_core_monochromatic_reciprocals": len(forbidden),
        "minimum_reciprocals": args.minimum_reciprocals,
        "cardinality_clauses": len(cardinality.clauses),
        "forbidden_reciprocal_variables": forbidden,
        "counting_reason": (
            "if no core monochromatic singleton exists, every vertex "
            "touched by a bichromatic reciprocal needs an anchor edge "
            "outside its incoming/outgoing killer union; summing gives "
            "2m >= 6n - 2r + N_b, hence at n=8,m=19 at least four "
            "bichromatic core reciprocals and seven total reciprocals"
        ),
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
