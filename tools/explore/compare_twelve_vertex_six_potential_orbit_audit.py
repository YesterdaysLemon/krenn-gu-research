"""Compare the independent compiled order-twelve audit to the primary run."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)



def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--primary",
        type=Path,
        default=Path(
            "tmp", "twelve_vertex_six_potential_orbits_exhausted.json"
        ),
    )
    parser.add_argument(
        "--audit-tsv",
        type=Path,
        default=Path(
            "tmp",
            "twelve_vertex_six_potential_orbits_independent_audit.tsv",
        ),
    )
    parser.add_argument(
        "--primary-source",
        type=Path,
        default=REPO_ROOT / "claims/finite/n12/exhaust_twelve_vertex_six_potential_orbits.cpp",
    )
    parser.add_argument(
        "--audit-source",
        type=Path,
        default=REPO_ROOT / "claims/finite/n12/audit_twelve_vertex_six_potential_orbits.cpp",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp",
            "twelve_vertex_six_potential_orbits_independently_audited.json",
        ),
    )
    args = parser.parse_args()
    primary = json.loads(args.primary.read_text(encoding="utf-8"))
    audit_rows = tuple(
        tuple(map(int, line.split()))
        for line in args.audit_tsv.read_text(
            encoding="utf-8"
        ).splitlines()
    )
    if (
        primary.get("verified") is not True
        or len(primary["cell_results"]) != 154
        or len(audit_rows) != 154
    ):
        raise AssertionError("compiled audit input binding changed")

    global_masks = [0] * 64
    total_ports = 0
    total_survivors = 0
    for expected, row in zip(
        primary["cell_results"], audit_rows, strict=True
    ):
        if len(row) != 7 + 64:
            raise AssertionError("independent audit row width changed")
        (
            cell_id,
            ports,
            survivors,
            port_xor,
            port_sum,
            classification_xor,
            classification_sum,
        ) = row[:7]
        masks = row[7:]
        expected_masks = [0] * 64
        for key, value in expected["success_mask_histogram"].items():
            expected_masks[int(key)] = int(value)
        comparisons = (
            cell_id == int(expected["cell_id"]),
            ports == int(expected["observed_ports"]),
            survivors == int(expected["survivors"]),
            port_xor == int(expected["port_hash_xor"]),
            port_sum == int(expected["port_hash_sum"]),
            classification_xor
            == int(expected["classification_hash_xor"]),
            classification_sum
            == int(expected["classification_hash_sum"]),
            list(masks) == expected_masks,
        )
        if not all(comparisons):
            raise AssertionError(
                f"independent compiled audit disagrees at cell {cell_id}"
            )
        total_ports += ports
        total_survivors += survivors
        for mask, count in enumerate(masks):
            global_masks[mask] += count

    expected_global = [0] * 64
    for key, value in primary["success_mask_histogram"].items():
        expected_global[int(key)] = int(value)
    if (
        total_ports != int(primary["representative_port_realizations"])
        or total_survivors
        != int(primary["all_six_potential_survivors"])
        or global_masks != expected_global
    ):
        raise AssertionError("independent compiled global totals disagree")

    payload = {
        "verified": True,
        "status": "independent_compiled_order_twelve_orbit_audit",
        "scope": (
            "exact per-cell comparison of port counts, survivor counts, "
            "all 64 success-mask counts, and independent port and "
            "classification hash aggregates"
        ),
        "primary": str(args.primary),
        "primary_sha256": sha256(args.primary),
        "audit_tsv": str(args.audit_tsv),
        "audit_tsv_sha256": sha256(args.audit_tsv),
        "primary_source": str(args.primary_source),
        "primary_source_sha256": sha256(args.primary_source),
        "audit_source": str(args.audit_source),
        "audit_source_sha256": sha256(args.audit_source),
        "cell_orbits": len(audit_rows),
        "representative_port_realizations": total_ports,
        "all_six_potential_residuals": total_survivors,
        "exact_cell_records_matched": len(audit_rows),
        "global_conjecture_resolved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "verified": True,
                "cell_orbits": len(audit_rows),
                "representative_port_realizations": total_ports,
                "all_six_potential_residuals": total_survivors,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
