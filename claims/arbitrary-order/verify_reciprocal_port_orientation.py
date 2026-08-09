"""Verify target-task versus inherited-half-colour port orientation.

The three primary killers at a vertex are indexed by target colours.  If
target ``c`` at the left endpoint is paired with target ``r=f_left(c)``
at the right endpoint, the actual inherited half-colours are ``(r,c)``,
not ``(c,r)``.  Reciprocity is necessary but the resulting physical unit
must separately survive the complete balanced-bridge table.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

Normal = tuple[int, int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def allowed(
    left: Normal,
    right: Normal,
    row: int,
    column: int,
) -> bool:
    return all(
        (row, column) == (target, target)
        or row == left[target]
        or column == right[target]
        for target in range(3)
    )


def main() -> None:
    normals = tuple(
        itertools.product((1, 2), (0, 2), (0, 1))
    )
    reciprocal_tasks = 0
    admissible_physical_units = 0
    inadmissible_reciprocal_tasks = 0
    legacy_unswapped_allowed = 0
    endpoint_pair_histogram: Counter[
        tuple[Normal, Normal]
    ] = Counter()

    for left in normals:
        for right in normals:
            for left_target in range(3):
                right_target = left[left_target]
                if right[right_target] != left_target:
                    continue
                reciprocal_tasks += 1
                physical = (right_target, left_target)
                if allowed(left, right, *physical):
                    admissible_physical_units += 1
                    endpoint_pair_histogram[(left, right)] += 1
                else:
                    inadmissible_reciprocal_tasks += 1
                legacy_unswapped_allowed += allowed(
                    left,
                    right,
                    left_target,
                    right_target,
                )

    if (
        len(normals) != 8
        or reciprocal_tasks != 96
        or admissible_physical_units != 72
        or inadmissible_reciprocal_tasks != 24
        or legacy_unswapped_allowed != 18
    ):
        raise AssertionError("port-orientation local census changed")

    # This exact local record occurred in the archived order-twelve
    # residual stream and made the old mismatch directly observable.
    left = (2, 0, 1)
    right = (2, 2, 0)
    legacy = (2, 1)
    corrected = (1, 2)
    if allowed(left, right, *legacy) or not allowed(
        left, right, *corrected
    ):
        raise AssertionError("diagnostic orientation example changed")

    theorem = Path(__file__).resolve().with_name(
        "RECIPROCAL_PORT_ORIENTATION_CORRECTION.md"
    )
    payload = {
        "verified": True,
        "status": "reciprocal_port_orientation_correction",
        "normal_types": len(normals),
        "reciprocal_target_task_transitions": reciprocal_tasks,
        "admissible_swapped_physical_units": (
            admissible_physical_units
        ),
        "reciprocal_but_bridge_forbidden_transitions": (
            inadmissible_reciprocal_tasks
        ),
        "legacy_unswapped_units_that_happen_to_be_allowed": (
            legacy_unswapped_allowed
        ),
        "admissible_endpoint_type_pairs": len(
            endpoint_pair_histogram
        ),
        "diagnostic": {
            "left_normal": list(left),
            "right_normal": list(right),
            "legacy_unswapped_unit": list(legacy),
            "legacy_unit_allowed": False,
            "correct_swapped_unit": list(corrected),
            "correct_unit_allowed": True,
        },
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "global_conjecture_resolved": False,
        "source": str(Path(__file__)),
        "source_sha256": sha256(Path(__file__)),
    }
    output = Path(
        "tmp", "reciprocal_port_orientation_corrected.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "verified": True,
                "reciprocal_target_tasks": reciprocal_tasks,
                "admissible_physical_units": (
                    admissible_physical_units
                ),
                "bridge_forbidden_reciprocal_tasks": (
                    inadmissible_reciprocal_tasks
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
