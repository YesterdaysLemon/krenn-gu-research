"""Write the 718 triangular-prism half-edge orbit representatives as JSON."""

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

REPO_ROOT, HERE = _bootstrap_repository(__file__)

import argparse
import json
from pathlib import Path

from krenn_gu.enumerate_cubic_rankone import nested_pattern
from krenn_gu.prism_orbit_screen import prism_orbit_representatives


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
