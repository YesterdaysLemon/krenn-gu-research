"""The exact triangular-prism degeneration for the unresolved (n,d)=(6,3) case.

For every finite nonzero x this is *not* a witness: one forbidden colouring
has amplitude x**-6.  As x tends to infinity the target is approached while
the edge weights diverge.  This is the boundary basin found independently by
the numerical search in ``search_witness.py``.
"""

from __future__ import annotations

import argparse

import numpy as np

from search_witness import EquationSystem


def prism_weights(x: complex) -> tuple[EquationSystem, np.ndarray]:
    if x == 0:
        raise ValueError("x must be nonzero")
    system = EquationSystem(6, 3)
    weights = np.zeros(system.variable_count, dtype=np.complex128)
    edge_weights = system.edge_array(weights)

    # Two triangles joined by three rungs.  Each colour class is a perfect
    # matching with two triangle edges of weight x and one rung of x^-2.
    colour_matchings = (
        (((0, 4), x**-2), ((2, 5), x), ((1, 3), x)),
        (((1, 2), x**-2), ((0, 5), x), ((3, 4), x)),
        (((3, 5), x**-2), ((0, 2), x), ((1, 4), x)),
    )
    for colour, weighted_matching in enumerate(colour_matchings):
        for edge, value in weighted_matching:
            edge_weights[system.edge_index[edge], colour, colour] = value
    return system, weights


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--x", type=float, default=10.0)
    args = parser.parse_args()

    system, weights = prism_weights(complex(args.x))
    amplitudes = system.amplitudes(weights)
    diagnostic = system.diagnostics(amplitudes)
    forbidden = np.flatnonzero(
        (~system.target.astype(bool)) & (np.abs(amplitudes) > 0)
    )
    print(f"x={args.x:g}")
    print(f"diagnostics={diagnostic}")
    for index in forbidden:
        print(
            "remaining forbidden colouring="
            f"{tuple(int(c) for c in system.colourings[index])}, "
            f"amplitude={amplitudes[index]}"
        )
    expected = abs(args.x) ** -6
    if not np.isclose(diagnostic["max_abs_residual"], expected):
        raise AssertionError(
            f"expected maximum residual {expected}, got "
            f"{diagnostic['max_abs_residual']}"
        )


if __name__ == "__main__":
    main()
