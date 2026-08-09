"""Independently audit a verified-source DIMACS clause subset append."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import tempfile
import time


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def header(path: Path) -> tuple[int, int, str]:
    with path.open("r", encoding="ascii", newline="") as handle:
        line = handle.readline()
    fields = line.split()
    if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
        raise AssertionError("unexpected DIMACS header")
    return (
        int(fields[2]),
        int(fields[3]),
        "\r\n" if line.endswith("\r\n") else "\n",
    )


def scan(path: Path, wanted: set[tuple[int, ...]]) -> tuple[int, set]:
    count = 0
    found = set()
    pending: list[int] = []
    with path.open("r", encoding="ascii") as handle:
        first = handle.readline()
        if not first.startswith("p cnf "):
            raise AssertionError("DIMACS header moved")
        for line in handle:
            stripped = line.strip()
            if not stripped or stripped.startswith("c"):
                continue
            for token in stripped.split():
                literal = int(token)
                if literal:
                    pending.append(literal)
                    continue
                if not pending:
                    raise AssertionError("empty DIMACS clause")
                count += 1
                key = tuple(sorted(pending))
                if key in wanted:
                    found.add(key)
                pending.clear()
    if pending:
        raise AssertionError("unterminated DIMACS clause")
    return count, found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    manifest = json.loads(
        args.manifest.read_text(encoding="utf-8")
    )
    if (
        manifest.get("status")
        != "verified_dimacs_clause_subset_materialized"
    ):
        raise AssertionError("unexpected materialization status")

    base = Path(manifest["base_cnf"])
    subset_path = Path(manifest["subset"])
    output = Path(manifest["output_cnf"])
    for path, expected in (
        (base, manifest["base_cnf_sha256"]),
        (subset_path, manifest["subset_sha256"]),
        (output, manifest["output_cnf_sha256"]),
    ):
        if sha256(path) != expected:
            raise AssertionError(f"hash changed: {path}")

    subset_payload = json.loads(
        subset_path.read_text(encoding="utf-8")
    )
    selected = [
        tuple(map(int, item)) for item in subset_payload["clauses"]
    ]
    if (
        not selected
        or len(set(selected)) != len(selected)
        or any(not item or 0 in item for item in selected)
    ):
        raise AssertionError("selected clause set changed")

    independent_memberships = [0] * len(manifest["sources"])
    covered = {clause: False for clause in selected}
    for source_id, record in enumerate(manifest["sources"]):
        clause_path = Path(record["clause_set"])
        verifier_path = Path(record["verified_clause_set"])
        for path, expected in (
            (clause_path, record["clause_set_sha256"]),
            (
                verifier_path,
                record["verified_clause_set_sha256"],
            ),
        ):
            if sha256(path) != expected:
                raise AssertionError(f"source hash changed: {path}")
        clause_set = json.loads(
            clause_path.read_text(encoding="utf-8")
        )
        verifier = json.loads(
            verifier_path.read_text(encoding="utf-8")
        )
        if (
            clause_set.get("status")
            != "verified_binomial_support_no_goods_clause_set"
            or verifier.get("verified") is not True
            or verifier.get("status")
            != "binomial_support_no_good_clause_set_verified"
            or Path(verifier["augmentation"]) != clause_path
            or verifier["augmentation_sha256"] != sha256(clause_path)
            or record["certificate_source_cnf"]
            != clause_set["base_cnf"]
            or record["certificate_source_cnf_sha256"]
            != clause_set["base_cnf_sha256"]
        ):
            raise AssertionError("source certificate binding changed")
        source_clauses = [
            tuple(map(int, item))
            for item in clause_set["support_no_goods"]
        ]
        if (
            len(source_clauses)
            != int(clause_set["candidate_support_no_goods"])
            or len(source_clauses)
            != int(verifier["support_no_goods"])
            or len(set(source_clauses)) != len(source_clauses)
            or len(source_clauses) != int(record["source_clauses"])
        ):
            raise AssertionError("source clause cardinality changed")
        lookup = set(source_clauses)
        for clause in selected:
            if clause in lookup:
                covered[clause] = True
                independent_memberships[source_id] += 1
        if independent_memberships[source_id] != int(
            record["selected_clause_memberships"]
        ):
            raise AssertionError("source membership count changed")
    if not all(covered.values()):
        raise AssertionError("selected clause lacks verified source")

    variables, declared, ending = header(base)
    wanted = {tuple(sorted(clause)) for clause in selected}
    actual, present = scan(base, wanted)
    appended = [
        clause
        for clause in selected
        if tuple(sorted(clause)) not in present
    ]
    if (
        actual != declared
        or variables != int(manifest["variables"])
        or declared != int(manifest["base_clauses"])
        or len(selected) != int(manifest["selected_clauses"])
        or len(present)
        != int(manifest["already_present_clauses"])
        or len(appended) != int(manifest["appended_clauses"])
        or declared + len(appended)
        != int(manifest["output_clauses"])
    ):
        raise AssertionError("materialization counts changed")

    output_variables, output_declared, _ = header(output)
    if (
        output_variables != variables
        or output_declared != declared + len(appended)
    ):
        raise AssertionError("output header changed")
    with tempfile.TemporaryDirectory(
        prefix="verified-clause-subset-audit-"
    ) as raw:
        rebuilt = Path(raw) / "rebuilt.cnf"
        with base.open(
            "r", encoding="ascii", newline=""
        ) as reader, rebuilt.open(
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
        if sha256(rebuilt) != sha256(output):
            raise AssertionError("byte-identical reconstruction failed")

    payload = {
        "verified": True,
        "status": "materialized_dimacs_clause_subset_verified",
        "scope": (
            "independent source hashes and certificate bindings, exact "
            "selected-clause memberships, base scan, header counts, and "
            "byte-identical DIMACS reconstruction"
        ),
        "manifest": str(args.manifest),
        "manifest_sha256": sha256(args.manifest),
        "base_cnf": str(base),
        "base_cnf_sha256": sha256(base),
        "subset": str(subset_path),
        "subset_sha256": sha256(subset_path),
        "source_membership_counts": independent_memberships,
        "selected_clauses": len(selected),
        "already_present_clauses": len(present),
        "appended_clauses": len(appended),
        "output_cnf": str(output),
        "output_cnf_sha256": sha256(output),
        "output_clauses": output_declared,
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
