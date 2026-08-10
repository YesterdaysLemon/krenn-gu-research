"""Write the 718 triangular-prism half-edge orbit representatives as JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from enumerate_cubic_rankone import nested_pattern
from prism_orbit_screen import prism_orbit_representatives


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    representatives = [
        nested_pattern(pattern)
        for pattern in prism_orbit_representatives()
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(
            {"representatives": representatives},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {args.output}: representatives={len(representatives)}"
    )


if __name__ == "__main__":
    main()
