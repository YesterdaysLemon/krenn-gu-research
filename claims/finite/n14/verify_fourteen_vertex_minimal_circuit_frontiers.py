"""Cross-audit the three aggregate minimal-circuit orbit frontiers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


OUTPUT = Path(
    "tmp/fourteen_vertex_minimal_circuit_frontiers_verified.json"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_frontier(
    *,
    audit_path: Path,
    condition_path: Path,
    solve_path: Path,
    replay_path: Path,
    total_orbits: int,
    expected_count: int,
    expected_global_sha: str,
    expected_condition_sha: str,
    expected_proof_sha: str,
) -> tuple[set[int], dict[str, object]]:
    audit = load(audit_path)
    if not audit.get("verified"):
        raise AssertionError(f"{audit_path} is not verified")
    if int(audit["unsat_selector_count"]) != expected_count:
        raise AssertionError("selector exclusion count changed")
    orbits = set(map(int, audit["unsat_selector_orbits"]))
    if len(orbits) != expected_count:
        raise AssertionError("selector exclusion list has duplicates")
    if not orbits <= set(range(total_orbits)):
        raise AssertionError("selector exclusion left the orbit census")

    augmentation_path = Path(str(audit["augmentation"]))
    augmentation = load(augmentation_path)
    if (
        sha256(augmentation_path)
        != str(audit["augmentation_sha256"])
    ):
        raise AssertionError("augmentation audit hash changed")
    if augmentation["unsat_selector_orbits"] != sorted(orbits):
        raise AssertionError("augmentation selector list changed")
    output_cnf = Path(str(augmentation["output_cnf"]))
    if sha256(output_cnf) != expected_global_sha:
        raise AssertionError("global CNF hash changed")
    if str(augmentation["output_cnf_sha256"]) != expected_global_sha:
        raise AssertionError("augmentation global hash changed")

    condition = load(condition_path)
    if str(condition["input_cnf_sha256"]) != expected_global_sha:
        raise AssertionError("condition input hash changed")
    expected_selector_clause = sorted(232 + orbit for orbit in orbits)
    if list(map(int, condition["selector_clause"])) != (
        expected_selector_clause
    ):
        raise AssertionError("condition selector clause changed")
    conditioned_cnf = Path(str(condition["output_cnf"]))
    if sha256(conditioned_cnf) != expected_condition_sha:
        raise AssertionError("conditioned CNF hash changed")
    if str(condition["output_cnf_sha256"]) != expected_condition_sha:
        raise AssertionError("condition manifest hash changed")

    solve = load(solve_path)
    if solve.get("status") != "UNSAT":
        raise AssertionError("Kissat result stopped being UNSAT")
    if str(solve["cnf_sha256"]) != expected_condition_sha:
        raise AssertionError("Kissat input hash changed")
    proof = Path(str(solve["proof"]))
    if sha256(proof) != expected_proof_sha:
        raise AssertionError("DRAT proof hash changed")
    if str(solve["proof_sha256"]) != expected_proof_sha:
        raise AssertionError("Kissat proof hash changed")

    replay = load(replay_path)
    if not replay.get("verified"):
        raise AssertionError("drat-trim replay is not verified")
    if str(replay["cnf_sha256"]) != expected_condition_sha:
        raise AssertionError("drat-trim input hash changed")
    if str(replay["proof_sha256"]) != expected_proof_sha:
        raise AssertionError("drat-trim proof hash changed")
    if int(replay["proof_bytes"]) != proof.stat().st_size:
        raise AssertionError("DRAT byte count changed")
    return orbits, {
        "augmentation_audit": str(audit_path),
        "augmentation_audit_sha256": sha256(audit_path),
        "global_cnf_sha256": expected_global_sha,
        "conditioned_cnf_sha256": expected_condition_sha,
        "proof_sha256": expected_proof_sha,
        "proof_bytes": proof.stat().st_size,
        "excluded_orbits": expected_count,
        "drat_trim_verify_seconds": float(replay["verify_seconds"]),
    }


def require_verified(path: Path) -> dict[str, object]:
    payload = load(path)
    if not payload.get("verified"):
        raise AssertionError(f"{path} is not verified")
    return payload


def main() -> None:
    c68, c68_record = audit_frontier(
        audit_path=Path(
            "tmp/fourteen_vertex_c6_8_rule_sat_global_merge_"
            "v32_minimal_circuits_augmentation_verified.json"
        ),
        condition_path=Path(
            "tmp/fourteen_vertex_c6_8_292_orbits_"
            "v32_minimal_circuits_condition.json"
        ),
        solve_path=Path(
            "tmp/fourteen_vertex_c6_8_292_orbits_"
            "v32_minimal_circuits_kissat.json"
        ),
        replay_path=Path(
            "tmp/fourteen_vertex_c6_8_292_orbits_"
            "v32_minimal_circuits_drat_trim.json"
        ),
        total_orbits=328,
        expected_count=292,
        expected_global_sha=(
            "70ad534437167f5b5c1ee1e4ab6b1b9a"
            "5cd2abd1335b5378a24c463180ecea81"
        ),
        expected_condition_sha=(
            "9e9cfeb68ee891240de55437b309a4552"
            "e0636295832e46e20a0612d40bfe41b"
        ),
        expected_proof_sha=(
            "8d05cd6c305c5c4c0e03943644380c6c"
            "c22e348ae328c1764350e8c06d1fc527"
        ),
    )
    c410, c410_record = audit_frontier(
        audit_path=Path(
            "tmp/fourteen_vertex_c4_10_rule_sat_global_merge_"
            "v10_orbit2_closed_minimal_circuits_"
            "augmentation_verified.json"
        ),
        condition_path=Path(
            "tmp/fourteen_vertex_c4_10_364_orbits_"
            "v10_minimal_circuits_condition.json"
        ),
        solve_path=Path(
            "tmp/fourteen_vertex_c4_10_364_orbits_"
            "v10_minimal_circuits_kissat.json"
        ),
        replay_path=Path(
            "tmp/fourteen_vertex_c4_10_364_orbits_"
            "v10_minimal_circuits_drat_trim.json"
        ),
        total_orbits=425,
        expected_count=364,
        expected_global_sha=(
            "0c49048f193c9b4184497d4e0abcc7df"
            "9caa209715678c5a6648c76decaba3e0"
        ),
        expected_condition_sha=(
            "6b322fa791c5c88a17fe176b6f6e6522"
            "1c0faeea3dce64452c5dc15055aa5003"
        ),
        expected_proof_sha=(
            "8b9afc9e1b9b9ca8a66536594d0d4870"
            "637b53998f6d1921e10ce3a1d7164c05"
        ),
    )
    c446, c446_record = audit_frontier(
        audit_path=Path(
            "tmp/fourteen_vertex_c4_c4_c6_rule_sat_late_combined_"
            "v7_orbit8_partial2_minimal_circuits_kappa3_"
            "augmentation_verified.json"
        ),
        condition_path=Path(
            "tmp/fourteen_vertex_c4_c4_c6_63_orbits_"
            "v7_minimal_circuits_kappa3_condition.json"
        ),
        solve_path=Path(
            "tmp/fourteen_vertex_c4_c4_c6_63_orbits_"
            "v7_minimal_circuits_kappa3_kissat.json"
        ),
        replay_path=Path(
            "tmp/fourteen_vertex_c4_c4_c6_63_orbits_"
            "v7_minimal_circuits_kappa3_drat_trim.json"
        ),
        total_orbits=93,
        expected_count=63,
        expected_global_sha=(
            "9d0e0e3da2b1c759f17b0f874766af8c"
            "ff8b8e921b5e1ccea236970df9a42918"
        ),
        expected_condition_sha=(
            "946887be7dd4c99c7738815687bdae3f"
            "557c9af9fb25dac2638fac78ca4c30c0"
        ),
        expected_proof_sha=(
            "08cd7bb800c3e34e895a7c34d2dcdd70"
            "73989eb2dabb19b2f83e271a0a811d45"
        ),
    )

    orbit0 = require_verified(
        Path("tmp/fourteen_vertex_c4_10_orbit0_final_verified.json")
    )
    if set(map(int, orbit0["unsat_first_factor_orbits"])) != {0}:
        raise AssertionError("prior C4+C10 orbit-0 certificate changed")
    c410_union = c410 | {0}
    if len(c410_union) != 365:
        raise AssertionError("C4+C10 union frontier changed")

    prior_paths = [
        Path(
            "tmp/fourteen_vertex_c4_c4_c6_"
            "late_combined_v3_58_orbits_final_verified.json"
        ),
        Path("tmp/fourteen_vertex_c4_c4_c6_orbit5_final_verified.json"),
        Path("tmp/fourteen_vertex_c4_c4_c6_orbit6_final_verified.json"),
        Path("tmp/fourteen_vertex_c4_c4_c6_orbit7_final_verified.json"),
    ]
    prior = set(
        map(
            int,
            require_verified(prior_paths[0])[
                "excluded_first_factor_orbits"
            ],
        )
    )
    for path in prior_paths[1:]:
        prior.add(
            int(require_verified(path)["excluded_first_factor_orbit"])
        )
    if len(prior) != 61:
        raise AssertionError("prior C4+C4+C6 frontier changed")
    c446_union = c446 | prior
    if len(c446_union) != 65:
        raise AssertionError("C4+C4+C6 union frontier changed")

    c410_complement = sorted(set(range(425)) - c410_union)
    c68_complement = sorted(set(range(328)) - c68)
    c446_complement = sorted(set(range(93)) - c446_union)
    if len(c410_complement) != 60:
        raise AssertionError("C4+C10 complement changed")
    if len(c68_complement) != 36:
        raise AssertionError("C6+C8 complement changed")
    if len(c446_complement) != 28:
        raise AssertionError("C4+C4+C6 complement changed")

    payload = {
        "verified": True,
        "status": "fourteen_vertex_minimal_circuit_frontiers_verified",
        "scope": (
            "cross-bound aggregate CNFs, selector conditions, Kissat "
            "proofs, independent drat-trim replays, and prior-union gates"
        ),
        "C4+C10": {
            **c410_record,
            "union_excluded_orbits": len(c410_union),
            "remaining_orbits": c410_complement,
        },
        "C6+C8": {
            **c68_record,
            "union_excluded_orbits": len(c68),
            "remaining_orbits": c68_complement,
        },
        "C4+C4+C6": {
            **c446_record,
            "union_excluded_orbits": len(c446_union),
            "remaining_orbits": c446_complement,
        },
        "global_conjecture_resolved": False,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
