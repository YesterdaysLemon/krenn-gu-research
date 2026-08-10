"""Independently rebuild a streamed verified-clause-set augmentation."""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)


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


def parse_header(path: Path) -> tuple[int, int, str]:
    with path.open("r", encoding="ascii", newline="") as handle:
        first = handle.readline()
    fields = first.split()
    if len(fields) != 4 or fields[0:2] != ["p", "cnf"]:
        raise AssertionError("unexpected DIMACS header")
    ending = "\r\n" if first.endswith("\r\n") else "\n"
    return int(fields[2]), int(fields[3]), ending


def scan(path: Path, wanted: set[tuple[int, ...]]) -> tuple[int, set]:
    found: set[tuple[int, ...]] = set()
    pending: list[int] = []
    count = 0
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
        != "verified_dimacs_clause_set_materialized"
    ):
        raise AssertionError("unexpected materialization status")

    base = Path(manifest["base_cnf"])
    clause_set_path = Path(manifest["clause_set"])
    verified_path = Path(manifest["verified_clause_set"])
    output = Path(manifest["output_cnf"])
    for path, expected in (
        (base, manifest["base_cnf_sha256"]),
        (clause_set_path, manifest["clause_set_sha256"]),
        (
            verified_path,
            manifest["verified_clause_set_sha256"],
        ),
        (output, manifest["output_cnf_sha256"]),
    ):
        if sha256(path) != expected:
            raise AssertionError(f"hash changed: {path}")

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
        or Path(verified["augmentation"]) != clause_set_path
        or verified["augmentation_sha256"] != sha256(clause_set_path)
        or manifest["certificate_source_cnf"]
        != clause_set["base_cnf"]
        or manifest["certificate_source_cnf_sha256"]
        != clause_set["base_cnf_sha256"]
    ):
        raise AssertionError("source certificate binding changed")
    candidates = [
        tuple(map(int, raw))
        for raw in clause_set["support_no_goods"]
    ]
    if (
        len(candidates)
        != int(clause_set["candidate_support_no_goods"])
        or len(candidates) != int(verified["support_no_goods"])
        or len(set(candidates)) != len(candidates)
    ):
        raise AssertionError("candidate clause set changed")

    variables, base_declared, ending = parse_header(base)
    wanted = {tuple(sorted(clause)) for clause in candidates}
    actual_base, present = scan(base, wanted)
    if actual_base != base_declared:
        raise AssertionError("base DIMACS clause count changed")
    appended = [
        clause
        for clause in candidates
        if tuple(sorted(clause)) not in present
    ]
    if (
        variables != int(manifest["variables"])
        or base_declared != int(manifest["base_clauses"])
        or len(candidates) != int(manifest["candidate_clauses"])
        or len(present) != int(manifest["already_present_clauses"])
        or len(appended) != int(manifest["appended_clauses"])
        or base_declared + len(appended)
        != int(manifest["output_clauses"])
    ):
        raise AssertionError("materialization counts changed")

    output_variables, output_declared, _ = parse_header(output)
    if (
        output_variables != variables
        or output_declared != base_declared + len(appended)
    ):
        raise AssertionError("output DIMACS header changed")
    with tempfile.TemporaryDirectory(
        prefix="verified-clause-set-materialization-audit-"
    ) as raw_directory:
        rebuilt = Path(raw_directory) / "rebuilt.cnf"
        with base.open(
            "r", encoding="ascii", newline=""
        ) as reader, rebuilt.open(
            "w", encoding="ascii", newline=""
        ) as writer:
            reader.readline()
            writer.write(
                f"p cnf {variables} {base_declared + len(appended)}"
                f"{ending}"
            )
            for line in reader:
                writer.write(line)
            for clause in appended:
                writer.write(
                    " ".join(map(str, clause)) + f" 0{ending}"
                )
        if sha256(rebuilt) != sha256(output):
            raise AssertionError(
                "byte-identical DIMACS reconstruction failed"
            )

    payload = {
        "verified": True,
        "status": "materialized_dimacs_clause_set_verified",
        "scope": (
            "independent hash and source-certificate binding, target "
            "clause scan, duplicate removal, header counts, and "
            "byte-identical streamed DIMACS reconstruction"
        ),
        "manifest": str(args.manifest),
        "manifest_sha256": sha256(args.manifest),
        "base_cnf": str(base),
        "base_cnf_sha256": sha256(base),
        "clause_set": str(clause_set_path),
        "clause_set_sha256": sha256(clause_set_path),
        "candidate_clauses": len(candidates),
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
