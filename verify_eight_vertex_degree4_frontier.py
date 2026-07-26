"""Fail-closed audit of the n=8 degree-four, at-most-15-edge exclusion."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

EXPECTED = {
    "cnf": (
        "tmp/eight_vertex_local_degree4_full_local_max15.cnf",
        "7f42f33aeee7349dd3a2b97e142f5a25f258115f8ffcf2fd1c593e8271f15fff",
    ),
    "minisat_model": (
        "tmp/eight_vertex_local_degree4_full_local_max15.minisat.model",
        "8e47e39240b5b347f444074f97e7ab4b4c11d3f534469b5cb23f4b6d2f7390df",
    ),
    "minisat_log": (
        "tmp/eight_vertex_local_degree4_full_local_max15.minisat.log",
        "539d705b27269a6f7d6aaa70f84070aecaa9c016b41aaf392bd9402299437500",
    ),
    "proof": (
        "tmp/eight_vertex_local_degree4_full_local_max15_cadical195.drat",
        "ab03b1dd1d02293f199e28a271909addee4e41f46076dffe6baf341c0e091417",
    ),
    "cadical_log": (
        "tmp/eight_vertex_local_degree4_full_local_max15_cadical195.log",
        "1769847f01dcb11f757f49161a64b88a2898711013291908bc4ebbd014ceb7bd",
    ),
    "drat_log": (
        "tmp/eight_vertex_local_degree4_full_local_max15_drat_trim.log",
        "156e6c953dec5036ee3af89bf823547b575d5d9790bbff0f5973f943e51571e6",
    ),
}
EXPECTED_VARIABLES = 394_797
EXPECTED_CLAUSES = 2_849_737
EXPECTED_PROOF_BYTES = 225_486_354
EXPECTED_RESOLUTION_STEPS = "46200153 resolution steps"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    base = Path(".").resolve()
    paths: dict[str, Path] = {}
    hashes: dict[str, str] = {}
    for label, (relative, expected_hash) in EXPECTED.items():
        path = base / relative
        observed = sha256(path)
        if observed != expected_hash:
            raise AssertionError(
                f"{label} hash mismatch: {observed} != {expected_hash}"
            )
        paths[label] = path
        hashes[label] = observed

    with paths["cnf"].open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise AssertionError("bad DIMACS header")
    if (int(variables), int(clauses)) != (
        EXPECTED_VARIABLES,
        EXPECTED_CLAUSES,
    ):
        raise AssertionError("DIMACS dimensions changed")

    if paths["proof"].stat().st_size != EXPECTED_PROOF_BYTES:
        raise AssertionError("proof size changed")
    if paths["minisat_model"].read_text(
        encoding="ascii"
    ).strip() != "UNSAT":
        raise AssertionError("MiniSat result file is not UNSAT")
    if "UNSATISFIABLE" not in paths["minisat_log"].read_text(
        encoding="utf-8"
    ):
        raise AssertionError("MiniSat terminal line missing")
    if "s UNSATISFIABLE" not in paths["cadical_log"].read_text(
        encoding="utf-8"
    ):
        raise AssertionError("CaDiCaL terminal line missing")
    drat_log = paths["drat_log"].read_text(encoding="utf-8")
    if (
        "s VERIFIED" not in drat_log
        or EXPECTED_RESOLUTION_STEPS not in drat_log
    ):
        raise AssertionError("independent DRAT verification missing")

    result = {
        "verified": True,
        "claim": (
            "no n=8 three-colour complex witness with an essential "
            "degree-four vertex and at most 15 skeleton edges"
        ),
        "variables": EXPECTED_VARIABLES,
        "clauses": EXPECTED_CLAUSES,
        "proof_bytes": EXPECTED_PROOF_BYTES,
        "resolution_steps": 46_200_153,
        "hashes": hashes,
    }
    output = base / "tmp/eight_vertex_degree4_frontier_audit.json"
    output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output}: verified=True")


if __name__ == "__main__":
    main()
