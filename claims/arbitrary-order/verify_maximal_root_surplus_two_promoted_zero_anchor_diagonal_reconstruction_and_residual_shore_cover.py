"""Exact checks for the GLS26 zero-anchor residual-shore theorem."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp


def col(*entries: int) -> sp.Matrix:
    return sp.Matrix(entries)


def independent_columns(columns: list[sp.Matrix]) -> sp.Matrix:
    matrix = sp.Matrix.hstack(*columns)
    return sp.Matrix.hstack(*matrix.columnspace())


def tensor(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, right)


def tensor_space(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    columns = [
        tensor(left[:, i], right[:, j])
        for i in range(left.cols)
        for j in range(right.cols)
    ]
    return independent_columns(columns)


def sum_space(*spaces: sp.Matrix) -> sp.Matrix:
    return independent_columns(
        [space[:, index] for space in spaces for index in range(space.cols)]
    )


def contains(space: sp.Matrix, vector: sp.Matrix) -> bool:
    return sp.Matrix.hstack(space, vector).rank() == space.rank()


@dataclass(frozen=True)
class Fixture:
    name: str
    x0: tuple[sp.Matrix, sp.Matrix]
    x1: tuple[sp.Matrix, sp.Matrix]
    root0: sp.Matrix
    root1: sp.Matrix


def analyze(fixture: Fixture) -> dict[str, int | bool]:
    identity = sp.eye(3)
    shore0 = independent_columns(list(fixture.x0))
    shore1 = independent_columns(list(fixture.x1))
    d0 = shore0.cols
    d1 = shore1.cols

    tangent = sum_space(
        tensor_space(shore0, identity),
        tensor_space(identity, shore1),
    )
    expected_tangent = 3 * d0 + 3 * d1 - d0 * d1
    assert tangent.rank() == expected_tangent

    q = tensor(fixture.x0[0], fixture.x1[1]) + tensor(fixture.x0[1], fixture.x1[0])
    epsilon = tensor(fixture.root0, fixture.root1)
    p = (epsilon.T * q)[0]
    assert p != 0
    assert contains(tangent, q)

    projector = p * sp.eye(9) - q * epsilon.T
    assert projector * q == sp.zeros(9, 1)
    assert epsilon.T * projector == sp.zeros(1, 9)
    assert projector * projector == p * projector
    assert projector.rank() == 8

    tangent_image = independent_columns(
        [projector * tangent[:, index] for index in range(tangent.cols)]
    )
    assert tangent_image.rank() == expected_tangent - 1
    assert tangent_image.rank() <= 7

    diagonal = sp.Matrix.hstack(
        tensor(identity[:, 0], identity[:, 0]),
        tensor(identity[:, 1], identity[:, 1]),
        tensor(identity[:, 2], identity[:, 2]),
    )
    delta = independent_columns([projector * diagonal[:, index] for index in range(3)])
    q_diagonal = contains(diagonal, q)
    assert delta.rank() == (2 if q_diagonal else 3)

    defect = sp.Matrix.hstack(tangent, diagonal).rank() - tangent.rank()
    projected_defect = (
        sp.Matrix.hstack(tangent_image, delta).rank() - tangent_image.rank()
    )
    assert defect == projected_defect

    coordinate_cover = all(
        contains(shore0, identity[:, colour]) or contains(shore1, identity[:, colour])
        for colour in range(3)
    )
    assert (defect == 0) == coordinate_cover

    # Directly replay the one-residual matching formula (6).  Every port
    # slice is in the corresponding residual tangent shore, hence its
    # transverse image is in P_Q(T_Q).
    port0 = sp.Matrix([[1, 2, 0], [0, 1, 3], [2, 0, 1]])
    port1 = sp.Matrix([[0, 1, 1], [2, 1, 0], [1, 3, 2]])
    singleton_checks = 0
    for residual in range(2):
        residual_tangent = sum_space(
            tensor_space(sp.Matrix.hstack(fixture.x0[residual]), identity),
            tensor_space(identity, sp.Matrix.hstack(fixture.x1[residual])),
        )
        for port_colour in range(3):
            root_slice = tensor(fixture.x0[residual], port1[:, port_colour]) + tensor(
                port0[:, port_colour], fixture.x1[residual]
            )
            assert contains(residual_tangent, root_slice)
            assert contains(tangent, root_slice)
            assert contains(tangent_image, projector * root_slice)
            singleton_checks += 1

    # An abstract exact reconstruction fixture uses Delta itself as the
    # pair-label contribution after the one-residual tangent quotient.  It
    # checks the rank statement without pretending to construct a witness.
    reconstruction = sum_space(tangent_image, delta)
    assert reconstruction.rank() - tangent_image.rank() == defect
    essential_pair = defect > 0
    assert essential_pair == (not coordinate_cover)

    return {
        "d0": d0,
        "d1": d1,
        "tangent_rank": tangent.rank(),
        "transverse_tangent_rank": tangent_image.rank(),
        "diagonal_rank": delta.rank(),
        "defect": defect,
        "coordinate_cover": coordinate_cover,
        "singleton_checks": singleton_checks,
    }


def main() -> None:
    e0, e1, e2 = sp.eye(3).columnspace()
    fixtures = (
        Fixture(
            "rank-two generic essential pair",
            (col(1, 1, 0), col(0, 1, 1)),
            (col(1, 0, 1), col(1, 1, 0)),
            col(1, 2, 3),
            col(2, 3, 5),
        ),
        Fixture(
            "rank-two coordinate shore cover",
            (e0, e1),
            (e1, e2),
            col(1, 2, 3),
            col(2, 3, 5),
        ),
        Fixture(
            "rank-one rank-two coordinate shore cover",
            (e0, e0),
            (e1, e2),
            col(1, 2, 3),
            col(2, 3, 5),
        ),
        Fixture(
            "rank-one noncover",
            (e0, 2 * e0),
            (e1, 3 * e1),
            col(1, 2, 3),
            col(2, 3, 5),
        ),
    )

    results = {fixture.name: analyze(fixture) for fixture in fixtures}
    assert results["rank-two generic essential pair"]["defect"] > 0
    assert results["rank-two coordinate shore cover"]["defect"] == 0
    assert results["rank-one rank-two coordinate shore cover"]["defect"] == 0
    assert results["rank-one noncover"]["defect"] > 0

    print("promoted zero-anchor residual-shore primary checks: PASS")
    for name, result in results.items():
        print(f"  {name}: {result}")


if __name__ == "__main__":
    main()
