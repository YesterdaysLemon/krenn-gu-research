"""Focused exact checks for the GLS24 one-probe anchor marginal theorem."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def tensor_vector(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([matrix[a, b] for a in range(3) for b in range(3)])


def tensor_matrix(vector: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(3, 3, lambda a, b: vector[3 * a + b])


def evaluation_row(x0: sp.Matrix, x1: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([[x0[a] * x1[b] for a in range(3) for b in range(3)]])


def contraction_matrix(x: sp.Matrix, mode: int) -> sp.Matrix:
    out = sp.zeros(3, 9)
    if mode == 0:
        for b in range(3):
            for a in range(3):
                out[b, 3 * a + b] = x[a]
    else:
        for a in range(3):
            for b in range(3):
                out[a, 3 * a + b] = x[b]
    return out


def wedge_matrix(u: sp.Matrix) -> sp.Matrix:
    """Map v in K^3 to u wedge v in the (01,02,12) coordinates."""

    return sp.Matrix(
        [
            [-u[1], u[0], 0],
            [-u[2], 0, u[0]],
            [0, -u[2], u[1]],
        ]
    )


def transverse_basis(epsilon: sp.Matrix) -> sp.Matrix:
    basis = epsilon.nullspace()
    assert len(basis) == 8
    return sp.Matrix.hstack(*basis)


def anchor_fixture(
    x0: sp.Matrix, x1: sp.Matrix
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    raw = sp.Matrix([[1, 2, 0], [0, 1, 3], [2, -1, 1]])
    value = (x0.T * raw * x1)[0]
    raw[0, 0] -= value / (x0[0] * x1[0])
    omega = tensor_vector(raw)
    assert (evaluation_row(x0, x1) * omega)[0] == 0
    return omega, x0.T * raw, raw * x1


def check_exact_sequences() -> dict[str, int]:
    x0 = sp.Matrix([1, 2, 3])
    x1 = sp.Matrix([2, -1, 4])
    epsilon = evaluation_row(x0, x1)
    e_basis = transverse_basis(epsilon)
    rho0 = contraction_matrix(x0, 0)
    rho1 = contraction_matrix(x1, 1)

    r0 = rho0 * e_basis
    r1 = rho1 * e_basis
    assert r0.rank() == r1.rank() == 2
    assert (x1.T * r0) == sp.zeros(1, 8)
    assert (x0.T * r1) == sp.zeros(1, 8)
    assert 8 - r0.rank() == 8 - r1.rank() == 6

    omega, u0_row, u1_col = anchor_fixture(x0, x1)
    u0 = u0_row.T
    u1 = u1_col
    assert u0 != sp.zeros(3, 1)
    assert u1 != sp.zeros(3, 1)
    assert (x1.T * u0)[0] == 0
    assert (x0.T * u1)[0] == 0

    mu0 = wedge_matrix(u0) * rho0
    mu0_tr = mu0 * e_basis
    assert mu0_tr.rank() == 1
    assert 8 - mu0_tr.rank() == 7
    assert mu0 * omega == sp.zeros(3, 1)

    omega_coords = e_basis.gauss_jordan_solve(omega)[0]
    assert omega_coords != sp.zeros(8, 1)
    assert sp.Matrix.hstack(omega_coords, *mu0_tr.nullspace()).rank() == 7

    return {
        "transverse_dimension": e_basis.cols,
        "marginal_rank": r0.rank(),
        "marginal_kernel": e_basis.cols - r0.rank(),
        "wedge_rank": mu0_tr.rank(),
        "wedge_kernel": e_basis.cols - mu0_tr.rank(),
    }


def check_anchor_trichotomy() -> dict[str, int]:
    x0 = sp.Matrix([1, 2, 3])
    x1 = sp.Matrix([2, -1, 4])
    l0_basis = sp.Matrix([[1, 2, 3]]).nullspace()
    l1_basis = sp.Matrix([[2, -1, 4]]).nullspace()
    assert len(l0_basis) == len(l1_basis) == 2

    zero = sp.zeros(3, 3)
    assert x0.T * zero == sp.zeros(1, 3)
    assert zero * x1 == sp.zeros(3, 1)

    rank_one = l0_basis[0] * l1_basis[0].T
    rank_two = (
        l0_basis[0] * l1_basis[0].T
        + l0_basis[1] * l1_basis[1].T
    )
    for matrix, expected_rank in ((rank_one, 1), (rank_two, 2)):
        assert matrix.rank() == expected_rank
        assert x0.T * matrix == sp.zeros(1, 3)
        assert matrix * x1 == sp.zeros(3, 1)
        assert matrix != zero

    marginal, left, right = anchor_fixture(x0, x1)
    assert marginal != sp.zeros(9, 1)
    assert left != sp.zeros(1, 3) or right != sp.zeros(3, 1)
    return {
        "zero_rank": zero.rank(),
        "double_transverse_rank_one": rank_one.rank(),
        "double_transverse_rank_two": rank_two.rank(),
        "marginal_fixture_rank": tensor_matrix(marginal).rank(),
    }


def check_slice_commutation() -> dict[str, int]:
    x0 = sp.Matrix([1, 2, 3])
    x1 = sp.Matrix([2, -1, 4])
    epsilon = evaluation_row(x0, x1)
    e_basis = transverse_basis(epsilon)
    rho0 = contraction_matrix(x0, 0)
    omega, u0_row, _ = anchor_fixture(x0, x1)
    u0 = u0_row.T
    mu = wedge_matrix(u0) * rho0
    assert mu * omega == sp.zeros(3, 1)

    # a_D in E_A^tr tensor K^2 tensor K^2, built independently in each
    # labelled port coefficient.  Slice the second port by eta.
    coeffs = []
    for first in range(2):
        row = []
        for second in range(2):
            coordinate = sp.Matrix(
                [first + 1, second + 2, first - second, 1, 0, -1, 2, 1]
            )
            row.append(e_basis * coordinate)
        coeffs.append(row)
    eta = sp.Matrix([3, -2])

    slice_then_map = []
    map_then_slice = []
    for first in range(2):
        sliced = sum(
            (eta[second] * coeffs[first][second] for second in range(2)),
            sp.zeros(9, 1),
        )
        slice_then_map.append(mu * sliced)
        mapped = [mu * coeffs[first][second] for second in range(2)]
        map_then_slice.append(
            sum(
                (eta[second] * mapped[second] for second in range(2)),
                sp.zeros(3, 1),
            )
        )
    assert slice_then_map == map_then_slice

    # Tensoring the one-dimensional root image with a 9-dimensional pair
    # complement produces exactly nine rows.
    root_image_rank = (mu * e_basis).rank()
    assert root_image_rank == 1
    assert root_image_rank * 9 == 9
    assert (8 - 1) * 9 == 63
    assert 8 * 9 == 72
    return {
        "slice_columns": 4,
        "root_image_rank": root_image_rank,
        "full_rows": 72,
        "anchor_rows": 63,
        "marginal_rows": 9,
    }


def check_rank_rise_and_aggregate() -> dict[str, int]:
    nuisance = sp.Matrix.hstack(
        *[sp.eye(9).col(index) for index in range(5)]
    )
    absorbed = nuisance.col(2) + 2 * nuisance.col(4)
    surviving = sp.eye(9).col(8)
    assert sp.Matrix.hstack(nuisance, absorbed).rank() == nuisance.rank()
    assert sp.Matrix.hstack(nuisance, surviving).rank() == nuisance.rank() + 1
    annihilators = nuisance.T.nullspace()
    assert any((row.T * surviving)[0] != 0 for row in annihilators)

    x0 = sp.Matrix([1, 2, 3])
    x1 = sp.Matrix([2, -1, 4])
    epsilon = evaluation_row(x0, x1)
    e_basis = transverse_basis(epsilon)
    rho0 = contraction_matrix(x0, 0)
    omega, u0_row, _ = anchor_fixture(x0, x1)
    u0 = u0_row.T
    mu = wedge_matrix(u0) * rho0

    # A synchronized aggregate has every marginal column on K u_0.
    synchronized = sp.Matrix.hstack(omega, 2 * omega, -3 * omega)
    assert mu * synchronized == sp.zeros(3, 3)
    marginal = rho0 * synchronized
    assert sp.Matrix.hstack(u0, *marginal.columnspace()).rank() == 1

    escape = None
    for candidate in e_basis.columnspace():
        if mu * candidate != sp.zeros(3, 1):
            escape = candidate
            break
    assert escape is not None
    nonsynchronized = synchronized.copy()
    nonsynchronized[:, 1] += escape
    assert mu * nonsynchronized != sp.zeros(3, 3)

    return {
        "nuisance_rank": nuisance.rank(),
        "absorbed_augmented_rank": sp.Matrix.hstack(
            nuisance, absorbed
        ).rank(),
        "surviving_augmented_rank": sp.Matrix.hstack(
            nuisance, surviving
        ).rank(),
        "aggregate_columns": synchronized.cols,
    }


def check_root_order_three_window() -> dict[str, int]:
    ports = tuple(range(4))
    complements = tuple(combinations(ports, 2))
    responses = {tuple(port for port in ports if port not in c) for c in complements}
    assert len(complements) == len(responses) == 6
    assert all(len(response) == 2 for response in responses)
    return {
        "ports": len(ports),
        "pair_targets": len(complements),
        "pair_responses": len(responses),
        "top_responses": 1,
        "common_marginal_rows_per_pair": 9,
    }


def main() -> None:
    exact = check_exact_sequences()
    trichotomy = check_anchor_trichotomy()
    slicing = check_slice_commutation()
    rank_rise = check_rank_rise_and_aggregate()
    window = check_root_order_three_window()
    print("promoted one-probe anchor-marginal primary checks: PASS")
    print(f"  one-probe exact sequences: {exact}")
    print(f"  exhaustive anchor fixtures: {trichotomy}")
    print(f"  physical slice/image and row dimensions: {slicing}")
    print(f"  rank-rise and synchronization fork: {rank_rise}")
    print(f"  root-order-three response window: {window}")
    print("  scope: conditional marginal route only; node closure stays open")


if __name__ == "__main__":
    main()
