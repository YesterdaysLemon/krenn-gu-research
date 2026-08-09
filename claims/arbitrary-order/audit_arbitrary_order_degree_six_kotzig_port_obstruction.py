"""Independent audit of the corrected physical-port sign table."""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    # Build types directly from bit triples, in reverse lexicographic
    # order from the primary verifier.
    records = []
    for b2, b1, b0 in itertools.product((1, 0), repeat=3):
        normal = (
            1 + b0,
            2 if b1 else 0,
            1 if b2 else 0,
        )
        values = (
            1 - 2 * b2,
            2 * (b2 - b0),
            2 * (b0 + b1 - 1),
        )
        records.append((normal, values))
    if len({normal for normal, _values in records}) != 8:
        raise AssertionError("independent normal construction changed")

    def plane_survives(
        left,
        right,
        row: int,
        column: int,
    ) -> bool:
        # Test each matrix unit directly on both endpoint coordinate
        # planes for every target.
        for target in range(3):
            left_plane_contains_row = row != left[target]
            right_plane_contains_column = (
                column != right[target]
            )
            if (
                left_plane_contains_row
                and right_plane_contains_column
                and (row, column) != (target, target)
            ):
                return False
        return True

    reciprocal = 0
    allowed_ports = 0
    values = Counter()
    endpoint_counts = Counter()
    for left, left_q in records:
        for right, right_q in records:
            for c in (2, 1, 0):
                r = left[c]
                if right[r] != c:
                    continue
                reciprocal += 1
                if not plane_survives(
                    left, right, r, c
                ):
                    continue
                allowed_ports += 1
                values[left_q[r] + right_q[c]] += 1
                endpoint_counts[(left, right)] += 1

    expected = Counter({1: 24, 2: 16, 3: 24, 4: 8})
    if (
        reciprocal != 96
        or allowed_ports != 72
        or values != expected
        or min(values) <= 0
    ):
        raise AssertionError("independent physical-port audit failed")

    primary = Path(
        "tmp",
        "arbitrary_order_degree_six_kotzig_port_obstruction_verified.json",
    )
    primary_data = json.loads(
        primary.read_text(encoding="utf-8")
    )
    if (
        primary_data.get("verified") is not True
        or primary_data.get(
            "admissible_corrected_physical_ports"
        )
        != allowed_ports
        or primary_data.get(
            "physical_port_potential_histogram"
        )
        != {
            str(key): value
            for key, value in sorted(values.items())
        }
    ):
        raise AssertionError(
            "primary and independent sign tables disagree"
        )

    theorem = Path(__file__).resolve().with_name(
        "ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md"
    )
    payload = {
        "verified": True,
        "status": (
            "independent_arbitrary_order_degree_six_port_sign_audit"
        ),
        "method": (
            "bit-first normal construction and direct coordinate-plane "
            "matrix-unit restrictions"
        ),
        "reciprocal_target_task_transitions": reciprocal,
        "admissible_corrected_physical_ports": allowed_ports,
        "admissible_endpoint_type_pairs": len(endpoint_counts),
        "physical_port_potential_histogram": {
            str(key): value
            for key, value in sorted(values.items())
        },
        "primary": str(primary),
        "primary_sha256": sha256(primary),
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp",
        "arbitrary_order_degree_six_kotzig_port_obstruction_audited.json",
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "verified": True,
                "physical_ports": allowed_ports,
                "port_potential_histogram": dict(
                    sorted(values.items())
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
