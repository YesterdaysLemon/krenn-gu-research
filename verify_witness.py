"""Independently recompute all coloring amplitudes in a candidate JSON file."""

from __future__ import annotations

import argparse
from pathlib import Path

from search_witness import EquationSystem, load_candidate


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
