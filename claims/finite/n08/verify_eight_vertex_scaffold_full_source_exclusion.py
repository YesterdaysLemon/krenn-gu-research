"""Regenerate the full protected two-K4 source and replay its finite RUP proof.

Standard-library replay; no SAT solver, external proof checker, or discovery
artifacts are required. The mathematical witness-to-CNF bridge is stated in
EIGHT_VERTEX_PROTECTED_SCAFFOLD_EXCLUSION.md and independently reconstructed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

ROOT, _ = bootstrap(__file__)
from krenn_gu.scaffold_source import build  # noqa: E402
from krenn_gu.source_quotient_core import rup_conflict  # noqa: E402

DEFAULT_FIXTURE = ROOT / "tests/fixtures/eight_vertex_scaffold_full_source_rup.json"
EQUATION_SHA256 = "f10ab786a60cb8dc85a575eef373e90cb4fc4ea9eec95ec68b3388ed781780ee"
CNF_SHA256 = "024f9b3a6cee02b4a90327915ea029ff567d3ebb694edfd498e1c5422ec84b6a"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def replay(certificate, generated=None):
    """Check exact origins and every addition before accepting the empty clause."""
    cnf, words, histogram, equation_hash, products = generated or build("full")
    require(certificate.get("schema") == "n8-two-k4-full-source-rup-v1", "wrong schema")
    expected = {
        "word_count": len(words),
        "variable_count": cnf.nv,
        "clause_count": len(cnf.clauses),
        "equation_sha256": equation_hash,
        "cnf_lf_sha256": hashlib.sha256(cnf.dimacs()).hexdigest(),
    }
    require(equation_hash == EQUATION_SHA256, "source equation identity changed")
    require(expected["cnf_lf_sha256"] == CNF_SHA256, "source CNF identity changed")
    for key, value in expected.items():
        require(type(certificate.get(key)) is type(value) and certificate[key] == value,
                f"certificate {key} mismatch")
    indices = certificate.get("core_clause_indices")
    require(isinstance(indices, list) and indices, "missing original clause core")
    require(all(type(i) is int and 0 <= i < len(cnf.clauses) for i in indices),
            "invalid original clause index")
    require(len(set(indices)) == len(indices), "duplicate original clause index")
    additions = certificate.get("rup_additions")
    require(isinstance(additions, list) and additions and additions[-1] == [],
            "proof must end with empty clause")
    clauses = [tuple(cnf.clauses[i]) for i in indices]
    for number, addition in enumerate(additions):
        require(isinstance(addition, list) and
                all(type(v) is int and 0 < abs(v) <= cnf.nv for v in addition),
                f"invalid literal at RUP step {number}")
        require(rup_conflict(clauses, (-v for v in addition)),
                f"RUP step {number} is not implied")
        clauses.append(tuple(addition))
    return {
        "status": "EXACT_FULL_SCAFFOLD_RUP_PASS",
        "scope": "complex n=8 protected two-K4 scaffold; all 96 hollow crossing entries",
        **expected,
        "original_core_clauses": len(indices),
        "checked_rup_additions": len(additions),
        "monomial_flags": products,
        "empty_clause_derived": True,
        "global_status": "UNRESOLVED",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    args = parser.parse_args()
    print(json.dumps(replay(json.loads(args.fixture.read_text(encoding="utf-8"))), indent=2))


if __name__ == "__main__":
    main()
