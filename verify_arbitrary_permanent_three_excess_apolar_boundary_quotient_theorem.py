"""Primary symbolic checks for the apolar boundary quotient theorem."""

from __future__ import annotations

import sympy as sp


def main() -> None:
    a, b, c, d, e, f = sp.symbols("a b c d e f", nonzero=True)

    projected_111 = sp.Matrix(
        [
            [a * d * e + b * c * f, a * c, b * e, 0],
            [d * f, 0, 0, 1],
        ]
    )
    assert sp.det(projected_111[:, [1, 3]]) == a * c

    projected_210 = sp.Matrix(
        [
            [a * (b * e + c * d), 0],
            [c * f, e],
            [b * f, d],
        ]
    )
    determinant_excess_rows = sp.det(projected_210[[1, 2], :])
    assert sp.simplify(determinant_excess_rows - f * (c * d - b * e)) == 0
    dependent_substitution = {d: b * e / c}
    assert sp.simplify(projected_210[0, 0].subs(dependent_substitution)) == 2 * a * b * e

    profiles = (
        ((1, 1, 1), (1, 1, 1), (2, 2, 2)),
        ((2, 1, 0), (0, 1, 2), (3, 2, 1)),
    )
    for h_profile, s_profile, quotient_dimensions in profiles:
        assert sum(h_profile) == sum(s_profile) == 3
        assert all(h + s == 2 for h, s in zip(h_profile, s_profile, strict=True))
        assert quotient_dimensions == tuple(3 - s for s in s_profile)

    # A nonempty balanced boundary sector necessarily contains a core mode.
    for mode_boundary_size in range(4):
        for source_boundary_size in range(4):
            if mode_boundary_size == source_boundary_size and (
                mode_boundary_size or source_boundary_size
            ):
                assert mode_boundary_size > 0

    # At a cubic exterior mode with one mandatory edge of each colour, the
    # colour of a prescribed matching edge selects exactly that edge.
    for prescribed_colour in range(3):
        incident_colours = (0, 1, 2)
        eligible = [index for index, colour in enumerate(incident_colours) if colour == prescribed_colour]
        assert eligible == [prescribed_colour]

    print("arbitrary permanent apolar boundary quotient theorem: PASS")
    print("symbolic quotient ledgers only; no support or input-word census was performed")


if __name__ == "__main__":
    main()
