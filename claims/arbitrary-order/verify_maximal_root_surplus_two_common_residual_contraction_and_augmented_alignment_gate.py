"""Focused exact replay for the common-contraction and alignment gate."""

from __future__ import annotations

import sympy as sp

PAIR_LABELS = ((1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4))


def complement_matrix() -> sp.Matrix:
    """Complement root pairs in the fixed PAIR_LABELS ordering."""

    index = {pair: position for position, pair in enumerate(PAIR_LABELS)}
    matrix = sp.zeros(6)
    roots = frozenset((1, 2, 3, 4))
    for position, pair in enumerate(PAIR_LABELS):
        complement = tuple(sorted(roots - frozenset(pair)))
        matrix[index[complement], position] = 1
    return matrix


def basis_matrix(columns: list[sp.Matrix], ambient: int) -> sp.Matrix:
    """Return an independent-column presentation, including the zero space."""

    if not columns:
        return sp.zeros(ambient, 0)
    joined = sp.Matrix.hstack(*columns)
    independent = joined.columnspace()
    return sp.Matrix.hstack(*independent) if independent else sp.zeros(ambient, 0)


def column_basis(matrix: sp.Matrix) -> sp.Matrix:
    return basis_matrix(matrix.columnspace(), matrix.rows)


def span(*spaces: sp.Matrix) -> sp.Matrix:
    """Column-space sum."""

    if not spaces:
        raise ValueError("at least one ambient space is required")
    ambient = spaces[0].rows
    return basis_matrix(
        [column for space in spaces for column in space.columnspace()], ambient
    )


def intersection(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    """Exact intersection of two column spaces."""

    assert left.rows == right.rows
    ambient = left.rows
    if left.cols == 0 or right.cols == 0:
        return sp.zeros(ambient, 0)
    relations = left.row_join(-right).nullspace()
    common = []
    for relation in relations:
        vector = left * relation[: left.cols, :]
        if vector != sp.zeros(ambient, 1):
            common.append(vector)
    return basis_matrix(common, ambient)


def annihilator(space: sp.Matrix) -> sp.Matrix:
    """Coordinate-pairing annihilator as a column space."""

    return basis_matrix(space.T.nullspace(), space.rows)


def same_space(left: sp.Matrix, right: sp.Matrix) -> bool:
    if left.rows != right.rows or left.rank() != right.rank():
        return False
    return left.row_join(right).rank() == left.rank()


def contains(space: sp.Matrix, vector: sp.Matrix) -> bool:
    return space.row_join(vector).rank() == space.rank()


def check_complement_form() -> None:
    """Check J, its involution, and the retained factor two."""

    complement = complement_matrix()
    assert complement == complement.T
    assert complement * complement == sp.eye(6)
    assert complement.det() == -1

    p12, p13, p14, p23, p24, p34 = sp.symbols("p12 p13 p14 p23 p24 p34")
    p = sp.Matrix([p12, p13, p14, p23, p24, p34])
    expected = 2 * (p12 * p34 + p13 * p24 + p14 * p23)
    assert sp.expand((p.T * complement * p)[0]) == expected


def ambient_direct_success(
    direct_map: sp.Matrix, p: sp.Matrix, complement: sp.Matrix
) -> tuple[bool, sp.Matrix | None, sp.Rational | None]:
    """Search the generators p and ker(U) for a nonzero augmented weight."""

    candidates = [(p, sp.Integer(1))]
    candidates.extend(
        (kernel_vector, sp.Integer(0)) for kernel_vector in direct_map.nullspace()
    )
    for aligned, kappa in candidates:
        if (aligned.T * complement * p)[0] != 0:
            assert direct_map * (aligned - kappa * p) == sp.zeros(direct_map.rows, 1)
            return True, aligned, kappa
    return False, None, None


def ambient_criterion(
    direct_map: sp.Matrix, p: sp.Matrix, complement: sp.Matrix
) -> bool:
    """Theorem 2 criterion: not(isotropic and Jp in im U^T)."""

    jp = complement * p
    isotropic = (p.T * jp)[0] == 0
    image_dual = column_basis(direct_map.T)
    return not (isotropic and contains(image_dual, jp))


def varied_rank_map(rank: int) -> sp.Matrix:
    """A deterministic rank-r map with non-coordinate row spaces."""

    assert 0 <= rank <= 6
    invertible_rows = sp.Matrix(
        [
            [1, 1, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 1, 1],
            [0, 0, 0, 0, 0, 1],
        ]
    )
    return invertible_rows[:rank, :]


def check_ambient_gate_all_ranks() -> None:
    """Compare direct alignment search and the dual gate at ranks zero--six."""

    complement = complement_matrix()
    vectors = (
        sp.Matrix([1, 0, 0, 0, 0, 0]),
        sp.Matrix([1, 1, 1, 1, 1, 1]),
        sp.Matrix([1, 2, 3, 4, 5, -22]),
        sp.Matrix([1, 2, 3, 5, 7, 11]),
    )
    assert (vectors[0].T * complement * vectors[0])[0] == 0
    assert (vectors[2].T * complement * vectors[2])[0] == 0
    assert (vectors[1].T * complement * vectors[1])[0] != 0

    for rank in range(7):
        direct_map = varied_rank_map(rank)
        assert direct_map.rank() == rank
        for p in vectors:
            direct, aligned, kappa = ambient_direct_success(direct_map, p, complement)
            criterion = ambient_criterion(direct_map, p, complement)
            assert direct == criterion
            if direct:
                assert aligned is not None and kappa is not None
                assert (aligned.T * complement * p)[0] != 0
            else:
                jp = complement * p
                assert (p.T * jp)[0] == 0
                assert direct_map.T.row_join(jp).rank() == direct_map.T.rank()
                solution = sp.linsolve((direct_map.T, jp))
                assert solution is not sp.EmptySet


def legal_direct_success(
    direct_map: sp.Matrix,
    p: sp.Matrix,
    legal: sp.Matrix,
    complement: sp.Matrix,
) -> tuple[bool, sp.Matrix]:
    """Direct form of Theorem 3 through M intersect (Kp+ker U)."""

    aligned_space = span(p, basis_matrix(direct_map.nullspace(), 6))
    legal_aligned = intersection(legal, aligned_space)
    pairing = (complement * p).T * legal_aligned
    return pairing != sp.zeros(1, legal_aligned.cols), legal_aligned


def check_legal_case(
    direct_map: sp.Matrix,
    p: sp.Matrix,
    legal: sp.Matrix,
    complement: sp.Matrix,
) -> tuple[bool, int]:
    """Compare (26)--(28), including both annihilator identities."""

    success, legal_aligned = legal_direct_success(direct_map, p, legal, complement)
    jp = complement * p
    failure_by_annihilation = contains(annihilator(legal_aligned), jp)
    assert success == (not failure_by_annihilation)

    aligned_space = span(p, basis_matrix(direct_map.nullspace(), 6))
    left_annihilator = annihilator(intersection(legal, aligned_space))
    p_perp = annihilator(p)
    image_dual = column_basis(direct_map.T)
    aligned_annihilator = intersection(p_perp, image_dual)
    formula_space = span(annihilator(legal), aligned_annihilator)
    assert same_space(left_annihilator, formula_space)
    assert failure_by_annihilation == contains(formula_space, jp)
    return success, legal_aligned.rank()


def check_legal_subspaces() -> None:
    """Check contained, transverse, full, and zero-intersection legal spaces."""

    complement = complement_matrix()
    standard = sp.eye(6)
    e = [standard[:, index] for index in range(6)]
    p = e[0]
    direct_map = sp.eye(6)[:5, :]
    assert direct_map.nullspace() == [e[5]]
    aligned = sp.Matrix.hstack(e[0], e[5])

    cases = {
        "contained": aligned,
        "transverse_repair": sp.Matrix.hstack(e[5], e[1]),
        "zero_intersection": sp.Matrix.hstack(e[1], e[2]),
        "full": sp.eye(6),
        "zero": sp.zeros(6, 0),
        "isotropic_p_line": p,
    }
    results = {
        name: check_legal_case(direct_map, p, column_basis(legal), complement)
        for name, legal in cases.items()
    }
    assert results["contained"] == (True, 2)
    assert results["transverse_repair"] == (True, 1)
    assert results["zero_intersection"] == (False, 0)
    assert results["full"] == (True, 2)
    assert results["zero"] == (False, 0)
    assert results["isotropic_p_line"] == (False, 1)

    nonisotropic = sp.ones(6, 1)
    injective = sp.eye(6)
    assert check_legal_case(injective, nonisotropic, nonisotropic, complement) == (
        True,
        1,
    )


def check_isotropic_rank_drop_repair() -> None:
    """Realize p=e12 and verify injective failure versus kernel repair."""

    complement = complement_matrix()
    e = [sp.eye(6)[:, index] for index in range(6)]
    alpha = sp.Matrix([1, 0, 0, 0])
    beta = sp.Matrix([0, 1, 0, 0])
    raw = sp.Matrix(
        [
            alpha[left - 1] * beta[right - 1] + alpha[right - 1] * beta[left - 1]
            for left, right in PAIR_LABELS
        ]
    )
    assert raw == e[0]
    assert (raw.T * complement * raw)[0] == 0

    injective = sp.eye(6)
    assert not ambient_direct_success(injective, raw, complement)[0]
    assert not ambient_criterion(injective, raw, complement)

    rank_drop = sp.eye(6)[:5, :]
    repair = e[5]
    assert rank_drop * repair == sp.zeros(5, 1)
    assert (repair.T * complement * raw)[0] == 1
    success, aligned, kappa = ambient_direct_success(rank_drop, raw, complement)
    assert success and aligned == repair and kappa == 0
    assert ambient_criterion(rank_drop, raw, complement)


def check_common_torus_nonvanishing() -> None:
    """Exhibit one fully supported point where two nonzero bilinear factors meet."""

    z00, z01, z02, z10, z11, z12 = sp.symbols("z00 z01 z02 z10 z11 z12")
    variables = (z00, z01, z02, z10, z11, z12)
    physical_edge = z00 * z10 + 2 * z01 * z12 - z02 * z11
    raw_permanent = (z00 + z01) * (z10 - z12) + z02 * (z10 + 2 * z11)
    product = sp.expand(physical_edge * raw_permanent)

    assert sp.Poly(physical_edge, variables, domain=sp.QQ) != 0
    assert sp.Poly(raw_permanent, variables, domain=sp.QQ) != 0
    assert sp.Poly(product, variables, domain=sp.QQ) != 0
    point = {variable: sp.Integer(1) for variable in variables}
    assert all(value != 0 for value in point.values())
    assert physical_edge.subs(point) == 2
    assert raw_permanent.subs(point) == 3
    assert product.subs(point) == 6


def main() -> None:
    check_complement_form()
    check_ambient_gate_all_ranks()
    check_legal_subspaces()
    check_isotropic_rank_drop_repair()
    check_common_torus_nonvanishing()
    print("common residual contraction and augmented-alignment verifier: PASS")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
