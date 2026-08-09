"""Fail-closed audit of the deterministic n=10 C4+C6 proof chain."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--semantic",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_factor_lattice_"
            "minimized_verified.json"
        ),
    )
    parser.add_argument(
        "--solver",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_factor_lattice_"
            "minimized_kissat_proof.json"
        ),
    )
    parser.add_argument(
        "--replay",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_factor_lattice_"
            "minimized_drat_trim_verified.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/ten_vertex_c4_c6_equality_factor_lattice_"
            "final_verified.json"
        ),
    )
    args = parser.parse_args()
    semantic = read_json(args.semantic)
    solver = read_json(args.solver)
    replay = read_json(args.replay)
    if semantic.get("verified") is not True:
        raise AssertionError("semantic reconstruction is not verified")
    if solver.get("status") != "UNSAT" or solver.get("returncode") != 20:
        raise AssertionError("proof-producing solver is not UNSAT")
    if replay.get("verified") is not True:
        raise AssertionError("DRAT replay is not verified")

    cnf = Path(semantic["final_cnf"])
    proof = Path(solver["proof"])
    cnf_hash = sha256(cnf)
    proof_hash = sha256(proof)
    if cnf_hash != semantic["final_cnf_sha256"]:
        raise AssertionError("semantic CNF hash changed")
    if cnf_hash != solver["cnf_sha256"]:
        raise AssertionError("solver used a different CNF")
    if cnf_hash != replay["cnf_sha256"]:
        raise AssertionError("replay used a different CNF")
    if proof_hash != solver["proof_sha256"]:
        raise AssertionError("solver proof hash changed")
    if proof_hash != replay["proof_sha256"]:
        raise AssertionError("replay used a different proof")
    if proof.stat().st_size != int(solver["proof_bytes"]):
        raise AssertionError("solver proof size changed")
    if proof.stat().st_size != int(replay["proof_bytes"]):
        raise AssertionError("replay proof size changed")
    solver_log = Path(solver["stdout"]).read_text(
        encoding="utf-8", errors="replace"
    )
    replay_log = Path(replay["stdout"]).read_text(
        encoding="utf-8", errors="replace"
    )
    if "s UNSATISFIABLE" not in solver_log:
        raise AssertionError("solver log lacks UNSAT status")
    if "s VERIFIED" not in replay_log:
        raise AssertionError("replay log lacks VERIFIED status")

    payload = {
        "verified": True,
        "scope": (
            "one explicit n=10,d=3 equality support with diagonal "
            "singleton 1-factors and full-block C4+C6 2-factor"
        ),
        "claim_scope": (
            "this fixed 105-entry support has no complex assignment "
            "satisfying the target amplitudes; this does not prove the "
            "global Krenn-Gu conjecture"
        ),
        "semantic_manifest": str(args.semantic),
        "semantic_manifest_sha256": sha256(args.semantic),
        "solver_manifest": str(args.solver),
        "solver_manifest_sha256": sha256(args.solver),
        "replay_manifest": str(args.replay),
        "replay_manifest_sha256": sha256(args.replay),
        "selected_entries": int(semantic["selected_entries"]),
        "skeleton_edges": int(semantic["skeleton_edges"]),
        "skeleton_perfect_matchings": int(
            semantic["skeleton_perfect_matchings"]
        ),
        "factor_relations": int(semantic["factor_relations"]),
        "factor_clauses": int(semantic["factor_clauses"]),
        "blocking_clauses": int(semantic["blocking_clauses"]),
        "cnf": str(cnf),
        "cnf_sha256": cnf_hash,
        "proof": str(proof),
        "proof_bytes": proof.stat().st_size,
        "proof_sha256": proof_hash,
        "drat_trim_sha256": replay["drat_trim_sha256"],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
