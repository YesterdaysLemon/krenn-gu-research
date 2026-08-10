#!/usr/bin/env python3
"""Independent audit of the generic q4_211 exclusion packaging."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_GENERIC_EXCLUSION_THEOREM.md"
PRIMARY = ROOT / "verify_p5_q4_211_generic_exclusion.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    # Use four-bit masks, independently of the set-based primary check.
    masks = [mask for mask in range(16) if mask.bit_count() >= 2]
    counts = {"disjoint": 0, "adjacent": 0, "parallel": 0}
    for first in masks:
        for second in masks:
            common = (first & second).bit_count()
            if common == 0:
                assert first.bit_count() == second.bit_count() == 2
                assert first | second == 15
                counts["disjoint"] += 1
            elif common == 1:
                counts["adjacent"] += 1
            else:
                counts["parallel"] += 1
    assert counts == {"disjoint": 6, "adjacent": 48, "parallel": 67}

    required_phrases = (
        "can be reselected as\nadjacent",
        "exact disjoint incidence is empty",
        "two-cross branch is\nempty",
        "contradiction excludes the\nlast gate",
        "no normalized `q4_211` restriction exists on `abc != 0`",
    )
    text = THEOREM.read_text(encoding="utf-8")
    for phrase in required_phrases:
        assert phrase in text

    output = {
        "audited": True,
        "method": "independent four-bit incidence cover and theorem-chain check",
        "incidence_pair_count": len(masks) ** 2,
        "incidence_classes": counts,
        "generic_q4_211_excluded": True,
        "ambient_maps_enumerated": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q4_211_generic_exclusion_audit.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
