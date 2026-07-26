"""Numerical search for Krenn--Gu monochromatic quantum graphs.

The edge data are stored as W[e, a, b], where e=(u,v), u<v, and a,b are
the endpoint colours.  For a colouring s of all vertices, its amplitude is
the hafnian

    sum_M product_(u,v in M) W[(u,v), s[u], s[v]]

over all perfect matchings M.  The target tensor is 1 on constant colourings
and 0 everywhere else.

This is an exploratory optimizer, not a proof.  A claimed witness must pass
``verify_witness.py`` (and, ultimately, exact or interval verification).
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np


def perfect_matchings(vertices: tuple[int, ...]) -> list[tuple[tuple[int, int], ...]]:
    if not vertices:
        return [()]
    first = vertices[0]
    result: list[tuple[tuple[int, int], ...]] = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for matching in perfect_matchings(remainder):
            result.append(((first, second),) + matching)
    return result


class EquationSystem:
    def __init__(self, n: int, d: int, required_weight: float = 1.0) -> None:
        if n % 2:
            raise ValueError("n must be even")
        self.n = n
        self.d = d
        self.edges = tuple(itertools.combinations(range(n), 2))
        self.edge_index = {edge: i for i, edge in enumerate(self.edges)}
        self.matchings = perfect_matchings(tuple(range(n)))
        self.colourings = np.array(
            list(itertools.product(range(d), repeat=n)), dtype=np.int16
        )
        self.target = np.all(self.colourings == self.colourings[:, :1], axis=1).astype(
            np.complex128
        )
        self.equation_weights = np.where(
            self.target.astype(bool), float(required_weight), 1.0
        )
        self.variable_ids = self._build_variable_ids()
        self.variable_count = len(self.edges) * d * d

    def _build_variable_ids(self) -> np.ndarray:
        ids = np.empty(
            (len(self.matchings), len(self.colourings), self.n // 2), dtype=np.int32
        )
        for matching_index, matching in enumerate(self.matchings):
            for pair_index, (u, v) in enumerate(matching):
                ids[matching_index, :, pair_index] = (
                    self.edge_index[(u, v)] * self.d * self.d
                    + self.colourings[:, u] * self.d
                    + self.colourings[:, v]
                )
        return ids

    def amplitudes(self, weights: np.ndarray) -> np.ndarray:
        selected = weights[self.variable_ids]
        return np.prod(selected, axis=2).sum(axis=0)

    def loss_and_gradient(
        self, weights: np.ndarray
    ) -> tuple[float, np.ndarray, np.ndarray]:
        selected = weights[self.variable_ids]
        products = np.prod(selected, axis=2)
        amplitudes = products.sum(axis=0)
        residual = amplitudes - self.target
        loss = float(np.mean(self.equation_weights * np.abs(residual) ** 2))

        # Wirtinger derivative d(loss)/d(conj(weights)).  Updating a complex
        # variable against this derivative is ordinary real steepest descent.
        gradient = np.zeros(self.variable_count, dtype=np.complex128)
        matching_count, colouring_count, pair_count = self.variable_ids.shape
        normalizer = float(colouring_count)
        for matching_index in range(matching_count):
            for pair_index in range(pair_count):
                other_product = np.ones(colouring_count, dtype=np.complex128)
                for other_index in range(pair_count):
                    if other_index != pair_index:
                        other_product *= selected[
                            matching_index, :, other_index
                        ]
                contribution = (
                    self.equation_weights
                    * residual
                    * np.conj(other_product)
                    / normalizer
                )
                np.add.at(
                    gradient,
                    self.variable_ids[matching_index, :, pair_index],
                    contribution,
                )
        return loss, gradient, amplitudes

    def residual_and_jacobian(
        self, weights: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        selected = weights[self.variable_ids]
        products = np.prod(selected, axis=2)
        residual = products.sum(axis=0) - self.target
        jacobian = np.zeros(
            (len(self.colourings), self.variable_count), dtype=np.complex128
        )
        matching_count, colouring_count, pair_count = self.variable_ids.shape
        row_ids = np.arange(colouring_count)
        for matching_index in range(matching_count):
            for pair_index in range(pair_count):
                other_product = np.ones(colouring_count, dtype=np.complex128)
                for other_index in range(pair_count):
                    if other_index != pair_index:
                        other_product *= selected[
                            matching_index, :, other_index
                        ]
                np.add.at(
                    jacobian,
                    (row_ids, self.variable_ids[matching_index, :, pair_index]),
                    other_product,
                )
        square_root_weights = np.sqrt(self.equation_weights)
        return residual * square_root_weights, jacobian * square_root_weights[:, None]

    def diagnostics(self, amplitudes: np.ndarray) -> dict[str, float]:
        residual = amplitudes - self.target
        constant = self.target.astype(bool)
        return {
            "loss": float(np.mean(np.abs(residual) ** 2)),
            "max_abs_residual": float(np.max(np.abs(residual))),
            "max_abs_forbidden": float(np.max(np.abs(amplitudes[~constant]))),
            "min_abs_required": float(np.min(np.abs(amplitudes[constant]))),
            "max_required_error": float(
                np.max(np.abs(amplitudes[constant] - 1))
            ),
        }

    def objective_loss(self, amplitudes: np.ndarray) -> float:
        residual = amplitudes - self.target
        return float(np.mean(self.equation_weights * np.abs(residual) ** 2))

    def edge_array(self, weights: np.ndarray) -> np.ndarray:
        return weights.reshape(len(self.edges), self.d, self.d)


def balance_vertex_gauge(
    system: EquationSystem, weights: np.ndarray, iterations: int = 30
) -> np.ndarray:
    """Minimize the weight norm over positive vertex gauges with product one.

    Multiplying every block W[(i,j)] by exp(t[i]+t[j]) multiplies every
    perfect-matching amplitude by exp(sum(t)).  The constraint sum(t)=0
    therefore leaves the entire equation system unchanged.
    """

    block_norms = np.sum(np.abs(system.edge_array(weights)) ** 2, axis=(1, 2))
    t = np.zeros(system.n, dtype=np.float64)
    for _ in range(iterations):
        scaled = np.empty(len(system.edges), dtype=np.float64)
        gradient = np.zeros(system.n, dtype=np.float64)
        hessian = np.zeros((system.n, system.n), dtype=np.float64)
        for edge_index, (u, v) in enumerate(system.edges):
            value = block_norms[edge_index] * math.exp(2 * (t[u] + t[v]))
            scaled[edge_index] = value
            gradient[u] += 2 * value
            gradient[v] += 2 * value
            hessian[u, u] += 4 * value
            hessian[v, v] += 4 * value
            hessian[u, v] += 4 * value
            hessian[v, u] += 4 * value
        kkt = np.zeros((system.n + 1, system.n + 1), dtype=np.float64)
        kkt[: system.n, : system.n] = hessian
        kkt[: system.n, system.n] = 1
        kkt[system.n, : system.n] = 1
        rhs = np.concatenate((-gradient, [0.0]))
        try:
            step = np.linalg.solve(kkt, rhs)[: system.n]
        except np.linalg.LinAlgError:
            break
        t += step
        t -= np.mean(t)
        if np.max(np.abs(step)) < 1e-12:
            break
    balanced = system.edge_array(weights.copy())
    for edge_index, (u, v) in enumerate(system.edges):
        balanced[edge_index] *= math.exp(t[u] + t[v])
    return balanced.reshape(-1)


def gradient_check(system: EquationSystem, seed: int = 0) -> None:
    rng = np.random.default_rng(seed)
    weights = 0.3 * (
        rng.standard_normal(system.variable_count)
        + 1j * rng.standard_normal(system.variable_count)
    )
    _, gradient, _ = system.loss_and_gradient(weights)
    direction = (
        rng.standard_normal(system.variable_count)
        + 1j * rng.standard_normal(system.variable_count)
    )
    direction /= np.linalg.norm(direction)
    epsilon = 1e-6
    plus, _, _ = system.loss_and_gradient(weights + epsilon * direction)
    minus, _, _ = system.loss_and_gradient(weights - epsilon * direction)
    finite_difference = (plus - minus) / (2 * epsilon)
    analytic = 2 * float(np.real(np.vdot(gradient, direction)))
    relative_error = abs(finite_difference - analytic) / max(
        1.0, abs(finite_difference), abs(analytic)
    )
    if relative_error > 1e-7:
        raise AssertionError(
            f"gradient check failed: finite={finite_difference}, "
            f"analytic={analytic}, relative_error={relative_error}"
        )


def run_adam(
    system: EquationSystem,
    seed: int,
    steps: int,
    learning_rate: float,
    report_every: int,
    active_mask: np.ndarray | None = None,
) -> tuple[np.ndarray, dict[str, float]]:
    rng = np.random.default_rng(seed)
    scale = (1.0 / len(system.matchings)) ** (1.0 / (system.n // 2))
    weights = scale * (
        rng.standard_normal(system.variable_count)
        + 1j * rng.standard_normal(system.variable_count)
    ) / math.sqrt(2)
    if active_mask is not None:
        weights[~active_mask] = 0

    first_moment = np.zeros_like(weights)
    second_moment = np.zeros(system.variable_count, dtype=np.float64)
    beta1 = 0.9
    beta2 = 0.999
    best_weights = weights.copy()
    best_loss = math.inf

    for step in range(1, steps + 1):
        loss, gradient, amplitudes = system.loss_and_gradient(weights)
        if active_mask is not None:
            gradient[~active_mask] = 0
        if loss < best_loss:
            best_loss = loss
            best_weights = weights.copy()

        first_moment = beta1 * first_moment + (1 - beta1) * gradient
        second_moment = beta2 * second_moment + (1 - beta2) * np.abs(gradient) ** 2
        corrected_first = first_moment / (1 - beta1**step)
        corrected_second = second_moment / (1 - beta2**step)
        weights -= learning_rate * corrected_first / (
            np.sqrt(corrected_second) + 1e-12
        )
        if active_mask is not None:
            weights[~active_mask] = 0
        if step % 100 == 0:
            weights = balance_vertex_gauge(system, weights)

        if report_every and (step == 1 or step % report_every == 0):
            diagnostic = system.diagnostics(amplitudes)
            print(
                f"seed={seed} step={step} loss={diagnostic['loss']:.6e} "
                f"max={diagnostic['max_abs_residual']:.6e} "
                f"|W|={np.linalg.norm(weights):.6e}",
                flush=True,
            )

        if best_loss < 1e-24:
            break

    amplitudes = system.amplitudes(best_weights)
    return best_weights, system.diagnostics(amplitudes)


def polish_levenberg_marquardt(
    system: EquationSystem,
    weights: np.ndarray,
    steps: int,
    active_mask: np.ndarray | None = None,
) -> tuple[np.ndarray, dict[str, float]]:
    weights = balance_vertex_gauge(system, weights)
    damping = 1e-6
    best_weights = weights.copy()
    best_amplitudes = system.amplitudes(weights)
    best_loss = system.objective_loss(best_amplitudes)
    for step in range(1, steps + 1):
        residual, jacobian = system.residual_and_jacobian(weights)
        if active_mask is None:
            active_indices = np.arange(system.variable_count)
        else:
            active_indices = np.flatnonzero(active_mask)
        active_jacobian = jacobian[:, active_indices]
        normal_matrix = active_jacobian.conj().T @ active_jacobian
        normal_rhs = -(active_jacobian.conj().T @ residual)
        diagonal_scale = max(
            1.0, float(np.max(np.real(np.diag(normal_matrix))))
        )
        accepted = False
        for _ in range(12):
            delta = np.linalg.solve(
                normal_matrix
                + damping * diagonal_scale * np.eye(len(active_indices)),
                normal_rhs,
            )
            full_delta = np.zeros(system.variable_count, dtype=np.complex128)
            full_delta[active_indices] = delta
            candidate = balance_vertex_gauge(system, weights + full_delta)
            if active_mask is not None:
                candidate[~active_mask] = 0
            amplitudes = system.amplitudes(candidate)
            loss = system.objective_loss(amplitudes)
            if loss < best_loss:
                weights = candidate
                best_weights = candidate.copy()
                best_amplitudes = amplitudes
                best_loss = loss
                damping = max(1e-16, damping / 3)
                accepted = True
                break
            damping = min(1e16, damping * 10)
        print(
            f"polish step={step} loss={best_loss:.6e} "
            f"max={np.max(np.abs(best_amplitudes - system.target)):.6e} "
            f"|W|={np.linalg.norm(best_weights):.6e} damping={damping:.3e}",
            flush=True,
        )
        if not accepted or best_loss < 1e-28:
            break
    return best_weights, system.diagnostics(best_amplitudes)


def save_candidate(
    path: Path,
    system: EquationSystem,
    weights: np.ndarray,
    diagnostic: dict[str, float],
    seed: int,
) -> None:
    edge_weights = system.edge_array(weights)
    payload = {
        "n": system.n,
        "d": system.d,
        "seed": seed,
        "diagnostics": diagnostic,
        "edges": [
            {
                "vertices": list(edge),
                "weights": [
                    [
                        [float(value.real), float(value.imag)]
                        for value in row
                    ]
                    for row in edge_weights[edge_index]
                ],
            }
            for edge_index, edge in enumerate(system.edges)
        ],
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def load_candidate(
    path: Path, system: EquationSystem
) -> tuple[np.ndarray, int]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if int(payload["n"]) != system.n or int(payload["d"]) != system.d:
        raise ValueError("candidate n/d does not match the requested equation system")
    by_edge = {
        tuple(edge["vertices"]): edge["weights"] for edge in payload["edges"]
    }
    weights = np.empty(system.variable_count, dtype=np.complex128)
    array = system.edge_array(weights)
    for edge_index, edge in enumerate(system.edges):
        encoded = np.asarray(by_edge[edge], dtype=np.float64)
        array[edge_index] = encoded[:, :, 0] + 1j * encoded[:, :, 1]
    return weights, int(payload.get("seed", 0))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--d", type=int, default=3)
    parser.add_argument("--steps", type=int, default=20_000)
    parser.add_argument("--restarts", type=int, default=8)
    parser.add_argument("--learning-rate", type=float, default=0.02)
    parser.add_argument(
        "--required-weight",
        type=float,
        default=1.0,
        help="optimization weight for each required monochromatic equation",
    )
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--report-every", type=int, default=1_000)
    parser.add_argument("--polish-steps", type=int, default=12)
    parser.add_argument("--output", type=Path, default=Path("best_candidate.json"))
    parser.add_argument(
        "--input",
        type=Path,
        help="polish this candidate instead of starting random restarts",
    )
    args = parser.parse_args()

    system = EquationSystem(args.n, args.d, args.required_weight)
    gradient_check(system, args.seed)
    print(
        f"n={args.n} d={args.d}: {len(system.edges)} edges, "
        f"{len(system.matchings)} perfect matchings, "
        f"{len(system.colourings)} equations, {system.variable_count} variables"
    )

    if args.input is not None:
        weights, seed = load_candidate(args.input, system)
        weights, diagnostic = polish_levenberg_marquardt(
            system, weights, args.polish_steps
        )
        save_candidate(args.output, system, weights, diagnostic, seed)
        print(f"wrote {args.output}; diagnostics={diagnostic}")
        return

    overall_weights: np.ndarray | None = None
    overall_diagnostic: dict[str, float] | None = None
    overall_seed = args.seed
    for restart in range(args.restarts):
        seed = args.seed + restart
        weights, diagnostic = run_adam(
            system,
            seed,
            args.steps,
            args.learning_rate,
            args.report_every,
            None,
        )
        if args.polish_steps:
            weights, diagnostic = polish_levenberg_marquardt(
                system, weights, args.polish_steps
            )
        print(f"restart={restart} seed={seed} final={diagnostic}", flush=True)
        if (
            overall_diagnostic is None
            or diagnostic["loss"] < overall_diagnostic["loss"]
        ):
            overall_weights = weights
            overall_diagnostic = diagnostic
            overall_seed = seed
            save_candidate(
                args.output, system, weights, diagnostic, overall_seed
            )

    assert overall_weights is not None and overall_diagnostic is not None
    print(
        f"best seed={overall_seed}; wrote {args.output}; "
        f"diagnostics={overall_diagnostic}"
    )


if __name__ == "__main__":
    main()
