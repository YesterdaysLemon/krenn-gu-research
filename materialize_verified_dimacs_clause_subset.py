"""Append a selected subset of independently verified clauses to DIMACS.

The selection mechanism is deliberately irrelevant to soundness.  Every
selected clause must occur verbatim in at least one independently verified
source clause set.  A later SAT proof decides whether the chosen sound
subset is sufficient.
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


def dimacs_header(path: Path) -> tuple[int, int, str]:
    with path.open("r", encoding="ascii", newline="") as handle:
        line = handle.readline()
    fields = line.split()
    if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
        raise ValueError("DIMACS header must be the first line")
    ending = "\r\n" if line.endswith("\r\n") else "\n"
    return int(fields[2]), int(fields[3]), ending


def dimacs_clauses(path: Path):
    pending: list[int] = []
    header_seen = False
    with path.open("r", encoding="ascii") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("c"):
                continue
            if stripped.startswith("p"):
                if header_seen:
                    raise ValueError("multiple DIMACS headers")
                header_seen = True
                continue
            if not header_seen:
                raise ValueError("clause before DIMACS header")
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


def verified_source(
    clause_set_path: Path,
    verifier_path: Path,
) -> tuple[dict[str, object], list[tuple[int, ...]]]:
    clause_set = json.loads(
        clause_set_path.read_text(encoding="utf-8")
    )
    verifier = json.loads(verifier_path.read_text(encoding="utf-8"))
    if (
        clause_set.get("status")
        != "verified_binomial_support_no_goods_clause_set"
        or verifier.get("verified") is not True
        or verifier.get("status")
        != "binomial_support_no_good_clause_set_verified"
        or Path(str(verifier.get("augmentation"))) != clause_set_path
        or verifier.get("augmentation_sha256")
        != sha256(clause_set_path)
    ):
        raise ValueError("invalid source clause-set verifier binding")
    raw = clause_set.get("support_no_goods")
    if not isinstance(raw, list):
        raise ValueError("source has no support_no_goods")
    clauses = [tuple(map(int, item)) for item in raw]
    if (
        any(not item or 0 in item for item in clauses)
        or len(set(clauses)) != len(clauses)
        or len(clauses)
        != int(clause_set.get("candidate_support_no_goods", -1))
        or len(clauses)
        != int(verifier.get("support_no_goods", -1))
    ):
        raise ValueError("source clause set changed")
    return clause_set, clauses


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--subset", type=Path, required=True)
    parser.add_argument(
        "--clause-set", type=Path, action="append", required=True
    )
    parser.add_argument(
        "--verified-clause-set",
        type=Path,
        action="append",
        required=True,
    )
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    if len(args.clause_set) != len(args.verified_clause_set):
        raise ValueError("source and verifier counts differ")

    subset_payload = json.loads(
        args.subset.read_text(encoding="utf-8")
    )
    raw_subset = subset_payload.get("clauses")
    if not isinstance(raw_subset, list):
        raise ValueError("subset artifact has no clauses array")
    selected = [tuple(map(int, item)) for item in raw_subset]
    if (
        not selected
        or any(not item or 0 in item for item in selected)
        or len(set(selected)) != len(selected)
    ):
        raise ValueError("selected clauses are empty, invalid, or repeated")

    source_records = []
    memberships: dict[tuple[int, ...], list[int]] = {
        clause: [] for clause in selected
    }
    for source_id, (clause_path, verifier_path) in enumerate(
        zip(
            args.clause_set,
            args.verified_clause_set,
            strict=True,
        )
    ):
        clause_set, source_clauses = verified_source(
            clause_path, verifier_path
        )
        source_lookup = set(source_clauses)
        for clause in selected:
            if clause in source_lookup:
                memberships[clause].append(source_id)
        source_records.append(
            {
                "clause_set": str(clause_path),
                "clause_set_sha256": sha256(clause_path),
                "verified_clause_set": str(verifier_path),
                "verified_clause_set_sha256": sha256(verifier_path),
                "source_clauses": len(source_clauses),
                "certificate_source_cnf": clause_set["base_cnf"],
                "certificate_source_cnf_sha256": clause_set[
                    "base_cnf_sha256"
                ],
            }
        )
    if any(not source_ids for source_ids in memberships.values()):
        raise ValueError("a selected clause has no verified source")

    variables, declared, ending = dimacs_header(args.base_cnf)
    if any(
        max(map(abs, clause)) > variables for clause in selected
    ):
        raise ValueError("selected clause references unknown variable")
    selected_keys = {
        tuple(sorted(clause)) for clause in selected
    }
    present = set()
    actual = 0
    for clause in dimacs_clauses(args.base_cnf):
        actual += 1
        key = tuple(sorted(clause))
        if key in selected_keys:
            present.add(key)
    if actual != declared:
        raise ValueError("base DIMACS clause count changed")
    appended = [
        clause
        for clause in selected
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
            f"p cnf {variables} {declared + len(appended)}{ending}"
        )
        for line in reader:
            writer.write(line)
        for clause in appended:
            writer.write(
                " ".join(map(str, clause)) + f" 0{ending}"
            )

    membership_counts = [0] * len(source_records)
    for source_ids in memberships.values():
        for source_id in source_ids:
            membership_counts[source_id] += 1
    for record, count in zip(
        source_records, membership_counts, strict=True
    ):
        record["selected_clause_memberships"] = count

    payload = {
        "status": "verified_dimacs_clause_subset_materialized",
        "scope": (
            "verbatim membership of every selected clause in an "
            "independently verified source, base scan, duplicate removal, "
            "and deterministic streamed DIMACS append"
        ),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "subset": str(args.subset),
        "subset_sha256": sha256(args.subset),
        "sources": source_records,
        "variables": variables,
        "base_clauses": declared,
        "selected_clauses": len(selected),
        "already_present_clauses": len(present),
        "appended_clauses": len(appended),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "output_clauses": declared + len(appended),
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
