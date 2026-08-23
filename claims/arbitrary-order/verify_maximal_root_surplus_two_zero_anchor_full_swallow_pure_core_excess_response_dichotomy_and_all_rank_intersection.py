"""Focused exact checks for the GLS41 pure-core/excess reduction."""

from __future__ import annotations

from dataclasses import dataclass

from sympy import Matrix, Rational, eye, zeros


def basis_vector(dimension: int, index: int) -> Matrix:
    vector = zeros(dimension, 1)
    vector[index, 0] = 1
    return vector


def column_matrix(columns: list[Matrix], rows: int) -> Matrix:
    if not columns:
        return zeros(rows, 0)
    return Matrix.hstack(*columns)


def independent_columns(matrix: Matrix) -> Matrix:
    return column_matrix(matrix.columnspace(), matrix.rows)


def intersection_basis(left: Matrix, right: Matrix) -> Matrix:
    """Return an exact column basis for im(left) intersect im(right)."""

    block = left.row_join(-right)
    columns: list[Matrix] = []
    for kernel_vector in block.nullspace():
        right_coordinates = kernel_vector[left.cols :, :]
        columns.append(right * right_coordinates)
    return independent_columns(column_matrix(columns, left.rows))


def matrix_unit(row: int, column: int) -> Matrix:
    return basis_vector(9, 3 * row + column)


@dataclass(frozen=True)
class RootProfile:
    branch: str
    k: int
    c_rank: int
    pure_rank: int
    excess_rank: int
    cylinder_rows: int
    pure_rows: int


def root_profiles() -> list[RootProfile]:
    delta = Matrix.hstack(
        matrix_unit(0, 0), matrix_unit(1, 1), matrix_unit(2, 2)
    )
    epsilon = Matrix([[1] * 9])
    profiles: list[RootProfile] = []

    strata = (
        (
            "q_outside_delta",
            matrix_unit(0, 1),
            [
                matrix_unit(0, 2),
                matrix_unit(1, 0),
                matrix_unit(1, 2),
                matrix_unit(2, 0),
                matrix_unit(2, 1),
            ],
            4,
        ),
        (
            "q_inside_delta",
            matrix_unit(0, 0) + matrix_unit(1, 1),
            [
                matrix_unit(0, 1),
                matrix_unit(0, 2),
                matrix_unit(1, 0),
                matrix_unit(1, 2),
                matrix_unit(2, 0),
                matrix_unit(2, 1),
            ],
            3,
        ),
    )

    for branch, q, extras, s_rank in strata:
        p = (epsilon * q)[0]
        assert p != 0
        projector = p * eye(9) - q * epsilon
        assert projector.rank() == 8
        assert projector * q == zeros(9, 1)
        start = Matrix.hstack(delta, q)
        if branch == "q_inside_delta":
            start = delta
        for k in range(4, 10):
            needed = k - start.rank()
            b_space = independent_columns(
                start.row_join(column_matrix(extras[:needed], 9))
            )
            assert b_space.rank() == k
            c_space = independent_columns(projector * b_space)
            pure_space = independent_columns(projector * delta)
            assert c_space.rank() == k - 1
            assert Matrix.hstack(c_space, pure_space).rank() == c_space.rank()
            excess_rank = c_space.rank() - pure_space.rank()
            assert excess_rank == k - s_rank
            profiles.append(
                RootProfile(
                    branch=branch,
                    k=k,
                    c_rank=c_space.rank(),
                    pure_rank=pure_space.rank(),
                    excess_rank=excess_rank,
                    cylinder_rows=9 * c_space.rank(),
                    pure_rows=9 * pure_space.rank(),
                )
            )
    return profiles


@dataclass(frozen=True)
class CylinderCheck:
    branch: str
    k: int
    middle_dimension: int
    core_quotient_dimension: int
    excess_quotient_dimension: int
    pure_rank_rise: int
    excess_test_survives: bool


def cylinder_fixture(profile: RootProfile) -> CylinderCheck:
    c_dimension = profile.c_rank
    r_dimension = profile.pure_rank
    l_dimension = 9 * c_dimension
    core_dimension = 9 * r_dimension
    excess_dimension = l_dimension - core_dimension
    core = eye(l_dimension)[:, :core_dimension]

    nuisance_columns: list[Matrix] = []
    for index in range(0, core_dimension, 5):
        nuisance_columns.append(basis_vector(l_dimension, index))
    for offset in range(min(core_dimension, excess_dimension)):
        if offset % 7 == 0:
            nuisance_columns.append(
                basis_vector(l_dimension, offset)
                + Rational(offset + 2, offset + 3)
                * basis_vector(l_dimension, core_dimension + offset)
            )
    nuisance = independent_columns(column_matrix(nuisance_columns, l_dimension))
    intersection = intersection_basis(nuisance, core)
    projection = nuisance[core_dimension:, :]

    middle_dimension = l_dimension - nuisance.rank()
    core_quotient_dimension = core_dimension - intersection.rank()
    excess_quotient_dimension = excess_dimension - projection.rank()
    assert middle_dimension == core_quotient_dimension + excess_quotient_dimension

    pure = Matrix.hstack(
        basis_vector(l_dimension, 0),
        basis_vector(l_dimension, 1),
        basis_vector(l_dimension, 2),
    )
    ambient_rise = Matrix.hstack(nuisance, pure).rank() - nuisance.rank()
    core_rise = Matrix.hstack(intersection, pure).rank() - intersection.rank()
    assert ambient_rise == core_rise

    excess_test_survives = False
    for index in range(core_dimension, l_dimension):
        test = basis_vector(l_dimension, index)
        if Matrix.hstack(nuisance, core, test).rank() > Matrix.hstack(
            nuisance, core
        ).rank():
            excess_test_survives = True
            break
    assert excess_test_survives == (excess_quotient_dimension > 0)

    return CylinderCheck(
        branch=profile.branch,
        k=profile.k,
        middle_dimension=middle_dimension,
        core_quotient_dimension=core_quotient_dimension,
        excess_quotient_dimension=excess_quotient_dimension,
        pure_rank_rise=ambient_rise,
        excess_test_survives=excess_test_survives,
    )


def jumping_intersection_boundary() -> dict[str, tuple[int, int, int]]:
    core = Matrix([[1], [0]])
    pure = core
    data: dict[str, tuple[int, int, int]] = {}
    for name, parameter in (("special", 0), ("generic", 2)):
        nuisance = Matrix([[0, parameter], [1, 0]])
        intersection = intersection_basis(nuisance, core)
        projection_rank = nuisance[1:, :].rank()
        pure_rise = Matrix.hstack(intersection, pure).rank() - intersection.rank()
        data[name] = (projection_rank, intersection.rank(), pure_rise)
    assert data == {"special": (1, 0, 1), "generic": (1, 1, 0)}
    return data


def main() -> None:
    profiles = root_profiles()
    cylinder_checks = [cylinder_fixture(profile) for profile in profiles]
    boundary = jumping_intersection_boundary()

    compact_profiles = {
        branch: tuple(
            (
                profile.k,
                profile.c_rank,
                profile.pure_rank,
                profile.excess_rank,
                profile.pure_rows,
            )
            for profile in profiles
            if profile.branch == branch
        )
        for branch in ("q_outside_delta", "q_inside_delta")
    }
    exact_sequence_checks = sum(
        check.middle_dimension
        == check.core_quotient_dimension + check.excess_quotient_dimension
        for check in cylinder_checks
    )
    pure_rank_checks = sum(check.pure_rank_rise >= 0 for check in cylinder_checks)

    print("GLS41 pure-core/excess-response primary checks: PASS")
    print("  canonical root profiles:", compact_profiles)
    print(
        "  cylinder exact-sequence/rank-rise fixtures:",
        {
            "profiles": len(cylinder_checks),
            "exact_sequences": exact_sequence_checks,
            "pure_rank_checks": pure_rank_checks,
            "pure_rows": tuple(sorted({profile.pure_rows for profile in profiles})),
        },
    )
    print("  projection/intersection jumping boundary:", boundary)
    print("  scope: pointwise reduction only; survival and node closure OPEN")


if __name__ == "__main__":
    main()
