"""Transport certified first-factor exclusions to all three colour roles.

The equality architecture and its target are invariant under a common
permutation of the three colours.  Hence a singleton factor orbit excluded
when it is assigned colour zero is excluded in either other colour role as
well.  This compiler appends the corresponding width-seven factor no-goods.
"""

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

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])


import argparse
import hashlib
import json
from pathlib import Path

from pysat.formula import CNF

from analyze_fourteen_vertex_c4_c4_c6_transport_rules import (
    ELIGIBLE_EDGE_ID,
    full_automorphisms,
    parse_factor,
    transform_factor,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument(
        "--frontier-audit",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_minimal_circuit_frontiers_verified.json"
        ),
    )
    parser.add_argument(
        "--orbit8-audit",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_orbit8_final_verified.json"
        ),
    )
    parser.add_argument(
        "--factor-census",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_4_6_factor_orbit_census.json"
        ),
    )
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    frontier = json.loads(
        args.frontier_audit.read_text(encoding="utf-8")
    )
    orbit8 = json.loads(args.orbit8_audit.read_text(encoding="utf-8"))
    census = json.loads(args.factor_census.read_text(encoding="utf-8"))
    if (
        frontier.get("verified") is not True
        or frontier.get("status")
        != "fourteen_vertex_minimal_circuit_frontiers_verified"
    ):
        raise ValueError("frontier audit is not verified")
    if (
        orbit8.get("verified") is not True
        or orbit8.get("status")
        != "C4+C4+C6_first_factor_orbit_8_excluded"
        or orbit8.get("global_conjecture_resolved") is not False
    ):
        raise ValueError("orbit-8 audit is not verified")
    if (
        Path(orbit8["global_cnf"]) != args.base_cnf
        or orbit8["global_cnf_sha256"] != sha256(args.base_cnf)
    ):
        raise ValueError("base CNF is not the audited orbit-8 global CNF")
    if census.get("status") != "factor_orbit_census_complete":
        raise ValueError("factor census is incomplete")
    if list(map(int, census["partition"])) != [4, 4, 6]:
        raise ValueError("factor census has the wrong partition")

    frontier_remaining = sorted(
        map(int, frontier["C4+C4+C6"]["remaining_orbits"])
    )
    if 8 not in frontier_remaining:
        raise AssertionError("pre-orbit-8 frontier no longer contains 8")
    if int(orbit8["excluded_first_factor_orbit"]) != 8:
        raise AssertionError("orbit-8 audit changed its excluded selector")
    remaining = [item for item in frontier_remaining if item != 8]
    excluded = [item for item in range(93) if item not in remaining]
    if len(excluded) != 66 or len(remaining) != 27:
        raise AssertionError("expected the certified 66/93 frontier")

    actions = full_automorphisms()
    if len(actions) != int(census["full_automorphisms"]):
        raise AssertionError("factor automorphism count changed")
    if len(census["factor_orbits"]) != 93:
        raise AssertionError("factor orbit count changed")

    excluded_factors = set()
    for orbit in excluded:
        row = census["factor_orbits"][orbit]
        representative = parse_factor(row["representative"])
        images = {
            transform_factor(representative, action)
            for action in actions
        }
        if len(images) != int(row["orbit_size"]):
            raise AssertionError(
                f"factor orbit {orbit} has the wrong size"
            )
        if excluded_factors & images:
            raise AssertionError("factor census orbits overlap")
        excluded_factors.update(images)
    if len(excluded_factors) != 38500:
        raise AssertionError("excluded factor count changed")

    candidate_clauses = sorted(
        {
            tuple(
                sorted(
                    -(
                        colour * len(ELIGIBLE_EDGE_ID)
                        + ELIGIBLE_EDGE_ID[item]
                        + 1
                    )
                    for item in factor
                )
            )
            for colour in range(3)
            for factor in excluded_factors
        }
    )
    if (
        len(candidate_clauses) != 3 * len(excluded_factors)
        or any(len(clause) != 7 for clause in candidate_clauses)
    ):
        raise AssertionError("colour-symmetric factor clauses changed")

    formula = CNF(from_file=str(args.base_cnf))
    existing = {tuple(map(int, clause)) for clause in formula.clauses}
    new_clauses = [
        clause for clause in candidate_clauses if clause not in existing
    ]
    formula.extend(new_clauses)
    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    formula.to_file(str(args.output_cnf))

    payload = {
        "status": "colour_symmetric_factor_orbit_exclusions_augmented",
        "scope": (
            "order-14 C4+C4+C6 equality architecture with skeleton "
            "vertex connectivity at least three"
        ),
        "reason": (
            "a certified impossible singleton-factor orbit remains "
            "impossible after any common permutation of the target colours"
        ),
        "frontier_audit": str(args.frontier_audit),
        "frontier_audit_sha256": sha256(args.frontier_audit),
        "orbit8_audit": str(args.orbit8_audit),
        "orbit8_audit_sha256": sha256(args.orbit8_audit),
        "factor_census": str(args.factor_census),
        "factor_census_sha256": sha256(args.factor_census),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "base_variables": formula.nv,
        "base_clauses": len(formula.clauses) - len(new_clauses),
        "excluded_factor_orbits": excluded,
        "remaining_factor_orbits": remaining,
        "excluded_factors": len(excluded_factors),
        "remaining_factors": int(census["eligible_singleton_factors"])
        - len(excluded_factors),
        "colour_roles": 3,
        "candidate_factor_no_goods": len(candidate_clauses),
        "new_factor_no_goods": len(new_clauses),
        "factor_no_good_widths": sorted(
            {len(clause) for clause in new_clauses}
        ),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "output_variables": formula.nv,
        "output_clauses": len(formula.clauses),
        "global_conjecture_resolved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
