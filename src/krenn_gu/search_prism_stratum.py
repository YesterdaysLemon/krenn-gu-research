"""Search the normalized triangular-prism killer stratum.

The nine selected diagonal entries of three edge-disjoint monochromatic
perfect matchings can be normalized to one by half-edge scalings. The six
complement edges remain unrestricted 3x3 blocks.

Only the 726 non-monochromatic amplitudes are minimized. If they vanished
while all three monochromatic amplitudes stayed nonzero, the scaling lemma
would turn the result into a genuine GHZ witness.
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
from pathlib import Path

import numpy as np

from krenn_gu.search_witness import EquationSystem, save_candidate


PRISM_MATCHINGS = (
    ((0, 1), (2, 3), (4, 5)),
    ((0, 2), (1, 4), (3, 5)),
    ((0, 3), (1, 5), (2, 4)),
)

K33_MATCHINGS = (
    ((0, 1), (2, 3), (4, 5)),
    ((0, 2), (1, 4), (3, 5)),
    ((0, 5), (1, 3), (2, 4)),
)


def normalized_stratum(
    system: EquationSystem,
    matchings: tuple[tuple[tuple[int, int], ...], ...] = PRISM_MATCHINGS,
) -> tuple[np.ndarray, np.ndarray]:
    fixed = np.zeros(system.variable_count, dtype=np.complex128)
    blocks = system.edge_array(fixed)
    prism_edges: set[tuple[int, int]] = set()
    for colour, matching in enumerate(matchings):
        for edge in matching:
            prism_edges.add(edge)
            blocks[system.edge_index[edge], colour, colour] = 1

    active = np.zeros(system.variable_count, dtype=bool)
    active_blocks = active.reshape(len(system.edges), 3, 3)
    for edge in system.edges:
        if edge not in prism_edges:
            active_blocks[system.edge_index[edge], :, :] = True
    return fixed, active


def configure_forbidden_objective(
    system: EquationSystem,
    fixed: np.ndarray,
    maverick_weight: float,
) -> np.ndarray:
    monochromatic = system.target.astype(bool)
    fixed_amplitudes = system.amplitudes(fixed)
    mavericks = np.flatnonzero(
        (~monochromatic) & (np.abs(fixed_amplitudes) > 0)
    )
    if len(mavericks) != 1:
        raise AssertionError(f"expected one maverick, got {mavericks}")
    system.target[:] = 0
    system.equation_weights[:] = 1
    system.equation_weights[monochromatic] = 0
    system.equation_weights[mavericks[0]] = maverick_weight
    return monochromatic


def optimize_adam(
    system: EquationSystem,
    fixed: np.ndarray,
    active: np.ndarray,
    seed: int,
    steps: int,
    learning_rate: float,
    initial_scale: float,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    weights = fixed.copy()
    active_count = int(np.sum(active))
    weights[active] = initial_scale * (
        rng.standard_normal(active_count)
        + 1j * rng.standard_normal(active_count)
    )
    first = np.zeros(system.variable_count, dtype=np.complex128)
    second = np.zeros(system.variable_count, dtype=np.float64)
    best = weights.copy()
    best_loss = float("inf")

    for step in range(1, steps + 1):
        loss, gradient, _ = system.loss_and_gradient(weights)
        gradient[~active] = 0
        if loss < best_loss:
            best_loss = loss
            best = weights.copy()
        first = 0.9 * first + 0.1 * gradient
        second = 0.999 * second + 0.001 * np.abs(gradient) ** 2
        corrected_first = first / (1 - 0.9**step)
        corrected_second = second / (1 - 0.999**step)
        weights -= (
            learning_rate
            * corrected_first
            / (np.sqrt(corrected_second) + 1e-12)
        )
        weights[~active] = fixed[~active]
        if best_loss < 1e-26:
            break
    return best


def polish(
    system: EquationSystem,
    fixed: np.ndarray,
    active: np.ndarray,
    weights: np.ndarray,
    steps: int,
) -> np.ndarray:
    indices = np.flatnonzero(active)
    best = weights.copy()
    best_loss = system.objective_loss(system.amplitudes(best))
    damping = 1e-6
    for _ in range(steps):
        residual, jacobian = system.residual_and_jacobian(best)
        active_jacobian = jacobian[:, indices]
        normal = active_jacobian.conj().T @ active_jacobian
        rhs = -(active_jacobian.conj().T @ residual)
        scale = max(1.0, float(np.max(np.real(np.diag(normal)))))
        accepted = False
        for _ in range(14):
            delta = np.linalg.solve(
                normal + damping * scale * np.eye(len(indices)), rhs
            )
            candidate = best.copy()
            candidate[indices] += delta
            candidate[~active] = fixed[~active]
            loss = system.objective_loss(system.amplitudes(candidate))
            if loss < best_loss:
                best = candidate
                best_loss = loss
                damping = max(1e-16, damping / 3)
                accepted = True
                break
            damping = min(1e16, damping * 10)
        if not accepted or best_loss < 1e-28:
            break
    return best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--restarts", type=int, default=20)
    parser.add_argument("--steps", type=int, default=20_000)
    parser.add_argument("--polish-steps", type=int, default=30)
    parser.add_argument("--learning-rate", type=float, default=0.01)
    parser.add_argument("--initial-scale", type=float, default=1.0)
    parser.add_argument("--maverick-weight", type=float, default=100.0)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument(
        "--output", type=Path, default=Path("prism_stratum_candidate.json")
    )
    args = parser.parse_args()

    system = EquationSystem(6, 3)
    fixed, active = normalized_stratum(system)
    monochromatic = configure_forbidden_objective(
        system, fixed, args.maverick_weight
    )
    best_score = float("inf")
    best_seed = args.seed

    for restart in range(args.restarts):
        seed = args.seed + restart
        weights = optimize_adam(
            system,
            fixed,
            active,
            seed,
            args.steps,
            args.learning_rate,
            args.initial_scale,
        )
        weights = polish(
            system, fixed, active, weights, args.polish_steps
        )
        amplitudes = system.amplitudes(weights)
        forbidden_max = float(np.max(np.abs(amplitudes[~monochromatic])))
        monochromatic_values = amplitudes[monochromatic]
        score = system.objective_loss(amplitudes)
        print(
            f"seed={seed} objective={score:.12e} "
            f"forbidden_max={forbidden_max:.12e} "
            f"monochromatic={monochromatic_values.tolist()} "
            f"active_norm={np.linalg.norm(weights[active]):.6e}",
            flush=True,
        )
        if score < best_score:
            best_score = score
            best_seed = seed
            diagnostic = {
                "loss": score,
                "max_abs_residual": forbidden_max,
                "max_abs_forbidden": forbidden_max,
                "min_abs_required": float(
                    np.min(np.abs(monochromatic_values))
                ),
                "max_required_error": float(
                    np.max(np.abs(monochromatic_values - 1))
                ),
            }
            save_candidate(
                args.output, system, weights, diagnostic, best_seed
            )

    print(
        f"best_seed={best_seed} objective={best_score:.12e} "
        f"wrote={args.output}"
    )


if __name__ == "__main__":
    main()
