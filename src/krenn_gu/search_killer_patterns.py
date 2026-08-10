"""Search systems reduced by the forced rank-one killer-edge proposition.

For every centre vertex v and colour c, the audited three-colour proposition
forces some neighbour u such that the oriented block W_(v,u) has support only
in column c.  A pattern chooses one such u for each (v,c), with the three
neighbours at a fixed v distinct.  The resulting zero constraints are imposed
before numerical optimization.

Sampling is exploratory; only exhaustive pattern coverage plus exact
certificates could constitute a proof.
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

REPO_ROOT, HERE = _bootstrap_repository(__file__)

import argparse
import json
from pathlib import Path

import numpy as np

from krenn_gu.search_witness import (
    EquationSystem,
    polish_levenberg_marquardt,
    run_adam,
    save_candidate,
)

Pattern = list[list[int]]


def random_pattern(n: int, rng: np.random.Generator) -> Pattern:
    pattern: Pattern = []
    for vertex in range(n):
        neighbours = [other for other in range(n) if other != vertex]
        pattern.append(
            [int(value) for value in rng.choice(neighbours, size=3, replace=False)]
        )
    return pattern


def active_mask_for_pattern(
    system: EquationSystem, pattern: Pattern
) -> np.ndarray:
    if system.d != 3:
        raise ValueError("killer patterns are currently implemented for d=3")
    active = np.ones(system.variable_count, dtype=bool)
    blocks = active.reshape(len(system.edges), 3, 3)
    for centre, targets in enumerate(pattern):
        if len(set(targets)) != 3 or centre in targets:
            raise ValueError(f"invalid targets at vertex {centre}: {targets}")
        for colour, target in enumerate(targets):
            if centre < target:
                block = blocks[system.edge_index[(centre, target)]]
                for target_colour in range(3):
                    if target_colour != colour:
                        block[:, target_colour] = False
            else:
                block = blocks[system.edge_index[(target, centre)]]
                for target_colour in range(3):
                    if target_colour != colour:
                        block[target_colour, :] = False
    return active


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--patterns", type=int, default=20)
    parser.add_argument("--steps", type=int, default=8_000)
    parser.add_argument("--polish-steps", type=int, default=20)
    parser.add_argument("--learning-rate", type=float, default=0.01)
    parser.add_argument("--required-weight", type=float, default=100.0)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument(
        "--output", type=Path, default=Path("killer_pattern_best_candidate.json")
    )
    parser.add_argument(
        "--pattern-output", type=Path, default=Path("killer_pattern_best.json")
    )
    args = parser.parse_args()

    system = EquationSystem(6, 3, args.required_weight)
    rng = np.random.default_rng(args.seed)
    best_objective = float("inf")
    best_pattern: Pattern | None = None
    best_diagnostic: dict[str, float] | None = None
    best_weights: np.ndarray | None = None
    best_seed = args.seed

    for pattern_index in range(args.patterns):
        pattern = random_pattern(system.n, rng)
        active_mask = active_mask_for_pattern(system, pattern)
        run_seed = args.seed * 100_000 + pattern_index
        print(
            f"pattern={pattern_index} active={int(np.sum(active_mask))} "
            f"seed={run_seed} map={pattern}",
            flush=True,
        )
        weights, _ = run_adam(
            system,
            run_seed,
            args.steps,
            args.learning_rate,
            0,
            active_mask,
        )
        weights, diagnostic = polish_levenberg_marquardt(
            system, weights, args.polish_steps, active_mask
        )
        objective = system.objective_loss(system.amplitudes(weights))
        print(
            f"pattern={pattern_index} objective={objective:.6e} "
            f"diagnostic={diagnostic}",
            flush=True,
        )
        if objective < best_objective:
            best_objective = objective
            best_pattern = pattern
            best_diagnostic = diagnostic
            best_weights = weights
            best_seed = run_seed
            save_candidate(
                args.output, system, weights, diagnostic, best_seed
            )
            args.pattern_output.write_text(
                json.dumps(
                    {
                        "pattern": pattern,
                        "active_variables": int(np.sum(active_mask)),
                        "weighted_objective": objective,
                        "diagnostics": diagnostic,
                        "seed": run_seed,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

    assert best_pattern is not None
    assert best_diagnostic is not None
    assert best_weights is not None
    print(
        f"best pattern={best_pattern}; weighted_objective={best_objective:.6e}; "
        f"diagnostic={best_diagnostic}; "
        f"wrote {args.output} and {args.pattern_output}"
    )


if __name__ == "__main__":
    main()
