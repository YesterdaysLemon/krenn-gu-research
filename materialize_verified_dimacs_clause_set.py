"""Stream a separately verified clause set into a DIMACS CNF.

The clause-set certificate may have been discovered against an older CNF.
This utility keeps that provenance intact and only performs the mechanical
operation of appending clauses that are not already present in a newer CNF.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def header(path: Path) -> tuple[int, int, str]:
    with path.open("r", encoding="ascii", newline="") as handle:
        first = handle.readline()
    fields = first.split()
    if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
        raise ValueError("the DIMACS header must be the first line")
    ending = "\r\n" if first.endswith("\r\n") else "\n"
    return int(fields[2]), int(fields[3]), ending


def clauses(path: Path):
    pending: list[int] = []
    saw_header = False
    with path.open("r", encoding="ascii") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("c"):
                continue
            if stripped.startswith("p"):
                if saw_header:
                    raise ValueError("multiple DIMACS headers")
                saw_header = True
                continue
            if not saw_header:
                raise ValueError("DIMACS clause precedes header")
            for token in stripped.split():
                literal = int(token)
                if literal:
                    pending.append(literal)
                    continue
                if not pending:
                    raise ValueError("empty DIMACS clause")
                yield tuple(pending)
                pending.clear()
    if pending:
        raise ValueError("unterminated DIMACS clause")


def load_verified_clause_set(
    clause_set_path: Path,
    verified_path: Path,
) -> tuple[dict[str, object], list[tuple[int, ...]]]:
    clause_set = json.loads(
        clause_set_path.read_text(encoding="utf-8")
    )
    verified = json.loads(verified_path.read_text(encoding="utf-8"))
    if (
        clause_set.get("status")
        != "verified_binomial_support_no_goods_clause_set"
        or not verified.get("verified")
        or verified.get("status")
        != "binomial_support_no_good_clause_set_verified"
        or Path(str(verified.get("augmentation"))) != clause_set_path
        or verified.get("augmentation_sha256") != sha256(clause_set_path)
    ):
        raise ValueError("clause-set verifier binding is invalid")
    raw_clauses = clause_set.get("support_no_goods")
    if not isinstance(raw_clauses, list):
        raise ValueError("clause set has no support_no_goods array")
    parsed = [tuple(map(int, item)) for item in raw_clauses]
    if (
        any(not item or 0 in item for item in parsed)
        or len(set(parsed)) != len(parsed)
        or len(parsed)
        != int(clause_set.get("candidate_support_no_goods", -1))
        or len(parsed) != int(verified.get("support_no_goods", -1))
    ):
        raise ValueError("clause-set cardinality or contents changed")
    return clause_set, parsed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--clause-set", type=Path, required=True)
    parser.add_argument(
        "--verified-clause-set", type=Path, required=True
    )
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()

    clause_set, candidates = load_verified_clause_set(
        args.clause_set, args.verified_clause_set
    )
    variables, declared_clauses, ending = header(args.base_cnf)
    if any(
        max(abs(literal) for literal in clause) > variables
        for clause in candidates
    ):
        raise ValueError(
            "verified clause set references an unknown target variable"
        )

    candidate_keys = {
        tuple(sorted(clause)) for clause in candidates
    }
    present: set[tuple[int, ...]] = set()
    actual_clauses = 0
    for clause in clauses(args.base_cnf):
        actual_clauses += 1
        key = tuple(sorted(clause))
        if key in candidate_keys:
            present.add(key)
    if actual_clauses != declared_clauses:
        raise ValueError("target DIMACS clause count changed")
    appended = [
        clause
        for clause in candidates
        if tuple(sorted(clause)) not in present
    ]

    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    with args.base_cnf.open(
        "r", encoding="ascii", newline=""
    ) as reader, args.output_cnf.open(
        "w", encoding="ascii", newline=""
    ) as writer:
        reader.readline()
        writer.write(
            f"p cnf {variables} {declared_clauses + len(appended)}"
            f"{ending}"
        )
        for line in reader:
            writer.write(line)
        for clause in appended:
            writer.write(
                " ".join(map(str, clause)) + f" 0{ending}"
            )

    payload = {
        "status": "verified_dimacs_clause_set_materialized",
        "scope": (
            "hash-bound independently verified clause set, target DIMACS "
            "scan, duplicate removal, and deterministic streaming append"
        ),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "clause_set": str(args.clause_set),
        "clause_set_sha256": sha256(args.clause_set),
        "verified_clause_set": str(args.verified_clause_set),
        "verified_clause_set_sha256": sha256(
            args.verified_clause_set
        ),
        "certificate_source_cnf": clause_set["base_cnf"],
        "certificate_source_cnf_sha256": clause_set[
            "base_cnf_sha256"
        ],
        "variables": variables,
        "base_clauses": declared_clauses,
        "candidate_clauses": len(candidates),
        "already_present_clauses": len(present),
        "appended_clauses": len(appended),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "output_clauses": declared_clauses + len(appended),
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
