"""Independently recompute all coloring amplitudes in a candidate JSON file."""

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
from pathlib import Path

from krenn_gu.search_witness import EquationSystem, load_candidate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--tolerance", type=float, default=1e-10)
    args = parser.parse_args()

    import json

    payload = json.loads(args.candidate.read_text(encoding="utf-8"))
    system = EquationSystem(int(payload["n"]), int(payload["d"]))
    weights, _ = load_candidate(args.candidate, system)

    amplitudes = system.amplitudes(weights)
    diagnostic = system.diagnostics(amplitudes)
    print(json.dumps(diagnostic, indent=2))
    if diagnostic["max_abs_residual"] > args.tolerance:
        raise SystemExit(
            f"candidate is not a witness at tolerance {args.tolerance:g}"
        )


if __name__ == "__main__":
    main()
