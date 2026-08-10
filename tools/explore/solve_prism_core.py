"""Solve the 54-equation square core of the normalized prism stratum.

At the zero complement-edge point, exactly 54 forbidden equations have a
nonzero linear term, one for each active variable. Their Jacobian is a
permutation matrix. This script uses complex Newton iteration to enumerate
roots of that square subsystem, then checks every forbidden amplitude.
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

import numpy as np

from krenn_gu.search_prism_stratum import normalized_stratum
from krenn_gu.search_witness import EquationSystem


def linear_core(
    system: EquationSystem, fixed: np.ndarray, active: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    original_target = system.target.copy()
    system.target[:] = 0
    _, jacobian = system.residual_and_jacobian(fixed)
    system.target[:] = original_target
    active_indices = np.flatnonzero(active)
    active_jacobian = jacobian[:, active_indices]
    rows = np.flatnonzero(np.linalg.norm(active_jacobian, axis=1) > 1e-12)
    if len(rows) != len(active_indices):
        raise AssertionError(
            f"expected square core, rows={len(rows)}, "
            f"variables={len(active_indices)}"
        )
    if np.linalg.matrix_rank(active_jacobian[rows]) != len(active_indices):
        raise AssertionError("linear core Jacobian is singular")
    return rows, active_indices


def newton_core(
    system: EquationSystem,
    fixed: np.ndarray,
    active: np.ndarray,
    rows: np.ndarray,
    indices: np.ndarray,
    seed: int,
    scale: float,
    steps: int,
) -> tuple[np.ndarray, float, int]:
    rng = np.random.default_rng(seed)
    weights = fixed.copy()
    weights[active] = scale * (
        rng.standard_normal(len(indices))
        + 1j * rng.standard_normal(len(indices))
    )

    for step in range(steps):
        amplitudes = system.amplitudes(weights)
        _, jacobian = system.residual_and_jacobian(weights)
        residual = amplitudes[rows]
        norm = float(np.linalg.norm(residual))
        if norm < 1e-11:
            return weights, norm, step
        try:
            delta = np.linalg.solve(
                jacobian[np.ix_(rows, indices)], -residual
            )
        except np.linalg.LinAlgError:
            return weights, norm, step

        accepted = False
        for power in range(12):
            candidate = weights.copy()
            candidate[indices] += delta / (2**power)
            candidate[~active] = fixed[~active]
            candidate_norm = float(
                np.linalg.norm(system.amplitudes(candidate)[rows])
            )
            if candidate_norm < norm:
                weights = candidate
                accepted = True
                break
        if not accepted:
            return weights, norm, step
    norm = float(np.linalg.norm(system.amplitudes(weights)[rows]))
    return weights, norm, steps


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--restarts", type=int, default=100)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--scale", type=float, default=1.0)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    system = EquationSystem(6, 3)
    fixed, active = normalized_stratum(system)
    rows, indices = linear_core(system, fixed, active)
    monochromatic = system.target.astype(bool)
    best = float("inf")
    converged = 0
    nonzero_roots = 0
    for restart in range(args.restarts):
        seed = args.seed + restart
        weights, core_norm, steps = newton_core(
            system,
            fixed,
            active,
            rows,
            indices,
            seed,
            args.scale,
            args.steps,
        )
        amplitudes = system.amplitudes(weights)
        forbidden_max = float(np.max(np.abs(amplitudes[~monochromatic])))
        active_norm = float(np.linalg.norm(weights[active]))
        best = min(best, forbidden_max)
        if core_norm < 1e-8:
            converged += 1
            if active_norm > 1e-7:
                nonzero_roots += 1
            print(
                f"seed={seed} steps={steps} core_norm={core_norm:.3e} "
                f"all_forbidden_max={forbidden_max:.3e} "
                f"active_norm={active_norm:.3e} "
                f"mono={amplitudes[monochromatic].tolist()}",
                flush=True,
            )
    print(
        f"converged={converged}/{args.restarts} "
        f"nonzero_roots={nonzero_roots} best_forbidden_max={best:.12e}"
    )


if __name__ == "__main__":
    main()
