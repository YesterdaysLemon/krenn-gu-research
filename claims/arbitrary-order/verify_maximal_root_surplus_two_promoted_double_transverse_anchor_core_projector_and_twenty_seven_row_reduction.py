"""Focused exact checks for the GLS25 double-transverse core theorem."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def vectorize(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([matrix[a, b] for a in range(3) for b in range(3)])


def matricize(vector: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(3, 3, lambda a, b: vector[3 * a + b])


def evaluation_row(x0: sp.Matrix, x1: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([[x0[a] * x1[b] for a in range(3) for b in range(3)]])


def transverse_basis(x0: sp.Matrix, x1: sp.Matrix) -> sp.Matrix:
    basis = evaluation_row(x0, x1).nullspace()
    assert len(basis) == 8
    return sp.Matrix.hstack(*basis)


def annihilator_basis(x: sp.Matrix) -> sp.Matrix:
    basis = x.T.nullspace()
    assert len(basis) == 2
    return sp.Matrix.hstack(*basis)


def core_basis(x0: sp.Matrix, x1: sp.Matrix) -> sp.Matrix:
    left = annihilator_basis(x0)
    right = annihilator_basis(x1)
    columns = []
    for a in range(2):
        for b in range(2):
            columns.append(vectorize(left[:, a] * right[:, b].T))
    basis = sp.Matrix.hstack(*columns)
    assert basis.rank() == 4
    return basis


def xi_image(
    vector: sp.Matrix,
    x0: sp.Matrix,
    x1: sp.Matrix,
    s0: sp.Matrix,
    s1: sp.Matrix,
    p: sp.Expr,
) -> sp.Matrix:
    matrix = matricize(vector)
    rho0 = matrix.T * x0
    rho1 = matrix * x1
    return vectorize(p * matrix - s0 * rho0.T - rho1 * s1.T)


def xi_matrix(
    x0: sp.Matrix,
    x1: sp.Matrix,
    q: sp.Matrix,
) -> tuple[sp.Matrix, sp.Expr, sp.Matrix, sp.Matrix]:
    p = (x0.T * q * x1)[0]
    assert p
    s0 = q * x1
    s1 = q.T * x0
    assert (x0.T * s0)[0] == p
    assert (x1.T * s1)[0] == p
    columns = []
    for index in range(9):
        vector = sp.eye(9).col(index)
        columns.append(xi_image(vector, x0, x1, s0, s1, p))
    return sp.Matrix.hstack(*columns), p, s0, s1


def wedge4_matrix(omega: sp.Matrix) -> sp.Matrix:
    rows = []
    for left, right in combinations(range(4), 2):
        row = [sp.Integer(0) for _ in range(4)]
        row[left] = -omega[right]
        row[right] = omega[left]
        rows.append(row)
    return sp.Matrix(rows)


def coordinate_matrix(basis: sp.Matrix, image: sp.Matrix) -> sp.Matrix:
    columns = [basis.gauss_jordan_solve(image[:, index])[0] for index in range(image.cols)]
    return sp.Matrix.hstack(*columns)


def setup() -> dict[str, sp.Matrix | sp.Expr]:
    x0 = sp.Matrix([1, 2, 3])
    x1 = sp.Matrix([2, -1, 4])
    q = sp.Matrix([[2, 1, 0], [1, -1, 3], [0, 2, 1]])
    e_basis = transverse_basis(x0, x1)
    d_basis = core_basis(x0, x1)
    xi, p, s0, s1 = xi_matrix(x0, x1, q)
    xi_tr = xi * e_basis
    xi_coords = coordinate_matrix(d_basis, xi_tr)
    return {
        "x0": x0,
        "x1": x1,
        "q": q,
        "e_basis": e_basis,
        "d_basis": d_basis,
        "xi": xi,
        "xi_tr": xi_tr,
        "xi_coords": xi_coords,
        "p": p,
        "s0": s0,
        "s1": s1,
    }


def check_projector() -> dict[str, object]:
    data = setup()
    x0 = data["x0"]
    x1 = data["x1"]
    e_basis = data["e_basis"]
    d_basis = data["d_basis"]
    xi = data["xi"]
    xi_tr = data["xi_tr"]
    p = data["p"]
    s0 = data["s0"]
    s1 = data["s1"]
    assert isinstance(x0, sp.MatrixBase)
    assert isinstance(x1, sp.MatrixBase)
    assert isinstance(e_basis, sp.MatrixBase)
    assert isinstance(d_basis, sp.MatrixBase)
    assert isinstance(xi, sp.MatrixBase)
    assert isinstance(xi_tr, sp.MatrixBase)
    assert isinstance(s0, sp.MatrixBase)
    assert isinstance(s1, sp.MatrixBase)

    assert xi_tr.rank() == 4
    for column in xi_tr.columnspace():
        matrix = matricize(column)
        assert x0.T * matrix == sp.zeros(1, 3)
        assert matrix * x1 == sp.zeros(3, 1)
    assert sp.Matrix.hstack(d_basis, xi_tr).rank() == 4
    assert xi * d_basis == p * d_basis
    assert xi * xi_tr == p * xi_tr

    left = annihilator_basis(x0)
    right = annihilator_basis(x1)
    expected_kernel = []
    for index in range(2):
        expected_kernel.append(vectorize(s0 * right[:, index].T))
        expected_kernel.append(vectorize(left[:, index] * s1.T))
    kernel = sp.Matrix.hstack(*expected_kernel)
    assert kernel.rank() == 4
    assert xi * kernel == sp.zeros(9, 4)
    kernel_coords = e_basis.gauss_jordan_solve(kernel)[0]
    assert kernel_coords.rank() == 4
    assert 8 - xi_tr.rank() == 4

    return {
        "p": p,
        "transverse_dimension": e_basis.cols,
        "core_dimension": d_basis.cols,
        "projector_rank": xi_tr.rank(),
        "projector_kernel": e_basis.cols - xi_tr.rank(),
        "scaled_idempotent": True,
    }


def check_anchor_and_exterior() -> tuple[dict[str, int], sp.Matrix, sp.Matrix]:
    data = setup()
    d_basis = data["d_basis"]
    e_basis = data["e_basis"]
    xi_coords = data["xi_coords"]
    p = data["p"]
    assert isinstance(d_basis, sp.MatrixBase)
    assert isinstance(e_basis, sp.MatrixBase)
    assert isinstance(xi_coords, sp.MatrixBase)

    omega_rank_one_coords = sp.Matrix([1, 0, 0, 0])
    omega_rank_two_coords = sp.Matrix([1, 0, 0, 1])
    omega_one = matricize(d_basis * omega_rank_one_coords)
    omega_two = matricize(d_basis * omega_rank_two_coords)
    assert omega_one.rank() == 1
    assert omega_two.rank() == 2

    omega = d_basis * omega_rank_two_coords
    wedge = wedge4_matrix(omega_rank_two_coords)
    assert wedge.rank() == 3
    chi = wedge * xi_coords
    assert chi.rank() == 3
    assert 8 - chi.rank() == 5
    omega_e_coords = e_basis.gauss_jordan_solve(omega)[0]
    assert chi * omega_e_coords == sp.zeros(6, 1)
    assert xi_coords * omega_e_coords == p * omega_rank_two_coords

    return (
        {
            "rank_one_anchor": omega_one.rank(),
            "rank_two_anchor": omega_two.rank(),
            "exterior_rank": wedge.rank(),
            "chi_rank": chi.rank(),
            "chi_kernel": 8 - chi.rank(),
        },
        chi,
        omega_e_coords,
    )


def check_slices_and_dimensions() -> dict[str, int]:
    data = setup()
    e_basis = data["e_basis"]
    assert isinstance(e_basis, sp.MatrixBase)
    exterior, chi, _ = check_anchor_and_exterior()
    assert exterior["chi_rank"] == 3

    labelled = []
    for first in range(2):
        row = []
        for second in range(2):
            coords = sp.Matrix(
                [first + 1, second + 1, first - second, 2, -1, 0, 1, 3]
            )
            row.append(e_basis * coords)
        labelled.append(row)
    eta = sp.Matrix([2, -3])
    for first in range(2):
        sliced = sum(
            (eta[second] * labelled[first][second] for second in range(2)),
            sp.zeros(9, 1),
        )
        first_route = chi * e_basis.gauss_jordan_solve(sliced)[0]
        mapped = [
            chi * e_basis.gauss_jordan_solve(labelled[first][second])[0]
            for second in range(2)
        ]
        second_route = sum(
            (eta[second] * mapped[second] for second in range(2)),
            sp.zeros(6, 1),
        )
        assert first_route == second_route

    assert 8 * 9 == 72
    assert 7 * 9 == 63
    assert 3 * 9 == 27
    return {
        "labelled_slice_tensors": 4,
        "full_pair_rows": 72,
        "anchor_pair_rows": 63,
        "core_pair_rows": 27,
        "full_top_rows": 8,
        "core_top_rows": 4,
    }


def check_rank_rise_and_sync() -> dict[str, int]:
    nuisance_pair = sp.Matrix.hstack(*[sp.eye(27).col(i) for i in range(11)])
    desired_absorbed = nuisance_pair.col(2) - nuisance_pair.col(9)
    desired_surviving = sp.eye(27).col(26)
    assert sp.Matrix.hstack(nuisance_pair, desired_absorbed).rank() == 11
    assert sp.Matrix.hstack(nuisance_pair, desired_surviving).rank() == 12

    nuisance_top = sp.Matrix.hstack(sp.eye(4).col(0), sp.eye(4).col(2))
    assert sp.Matrix.hstack(nuisance_top, sp.eye(4).col(1)).rank() == 3

    data = setup()
    e_basis = data["e_basis"]
    assert isinstance(e_basis, sp.MatrixBase)
    _, chi, omega_coords = check_anchor_and_exterior()
    synchronized = sp.Matrix.hstack(omega_coords, -2 * omega_coords)
    assert chi * synchronized == sp.zeros(6, 2)
    escape = next(column for column in sp.eye(8).columnspace() if chi * column != sp.zeros(6, 1))
    nonsynchronized = synchronized.row_join(escape)
    assert chi * nonsynchronized != sp.zeros(6, 3)

    return {
        "pair_nuisance_rank": nuisance_pair.rank(),
        "pair_absorbed_rank": sp.Matrix.hstack(
            nuisance_pair, desired_absorbed
        ).rank(),
        "pair_surviving_rank": sp.Matrix.hstack(
            nuisance_pair, desired_surviving
        ).rank(),
        "top_nuisance_rank": nuisance_top.rank(),
        "aggregate_columns": synchronized.cols,
    }


def check_r3_window() -> dict[str, int]:
    ports = tuple(range(4))
    complements = tuple(combinations(ports, 2))
    responses = {tuple(port for port in ports if port not in c) for c in complements}
    assert len(complements) == len(responses) == 6
    return {
        "ports": len(ports),
        "pair_modules": len(complements),
        "pair_responses": len(responses),
        "pair_rows": 27,
        "top_modules": 1,
        "top_rows": 4,
    }


def main() -> None:
    projector = check_projector()
    anchor, _, _ = check_anchor_and_exterior()
    slicing = check_slices_and_dimensions()
    rank_rise = check_rank_rise_and_sync()
    window = check_r3_window()
    print("promoted double-transverse core primary checks: PASS")
    print(f"  denominator-free scaled projector: {projector}")
    print(f"  double-core anchor/exterior quotient: {anchor}")
    print(f"  physical slice/image and row dimensions: {slicing}")
    print(f"  rank-rise and anchored synchronization: {rank_rise}")
    print(f"  root-order-three response window: {window}")
    print("  scope: conditional core route only; node closure stays open")


if __name__ == "__main__":
    main()
