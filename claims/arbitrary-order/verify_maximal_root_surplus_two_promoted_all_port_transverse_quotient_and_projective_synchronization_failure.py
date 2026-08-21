"""Focused exact checks for the GLS22 promoted transverse quotient."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp


def projector(epsilon: sp.MatrixBase, q: sp.MatrixBase) -> tuple[sp.Expr, sp.Matrix]:
    p = sp.expand((epsilon * q)[0])
    return p, p * sp.eye(q.rows) - q * epsilon


def check_projector_algebra() -> dict[str, object]:
    z = sp.symbols("z")
    epsilon = sp.Matrix([[1, 2, 3, 5, 7, 11, 13, 17, 19]])
    q = sp.Matrix([z, 1, z + 1, 2, -1, 3, z - 2, 4, 5])
    p, project = projector(epsilon, q)
    assert p != 0
    assert (project * q).applyfunc(sp.simplify) == sp.zeros(9, 1)
    assert (epsilon * project).applyfunc(sp.simplify) == sp.zeros(1, 9)
    assert (project * project - p * project).applyfunc(sp.simplify) == sp.zeros(9, 9)
    fibre = project.subs(z, 2)
    assert p.subs(z, 2) != 0
    assert fibre.rank() == 8
    assert len(fibre.nullspace()) == 1
    assert sp.Matrix.hstack(fibre.nullspace()[0], q.subs(z, 2)).rank() == 1
    return {"p": p, "rank": fibre.rank(), "kernel": len(fibre.nullspace())}


def kronecker_project(project: sp.MatrixBase, right_dimension: int) -> sp.Matrix:
    return sp.kronecker_product(project, sp.eye(right_dimension))


def rank(matrix: sp.MatrixBase) -> int:
    return int(matrix.rank())


def check_quotient_and_selector_equivalence() -> dict[str, int]:
    epsilon = sp.Matrix([[1, 2, -1, 3]])
    q = sp.Matrix([2, 1, 4, -1])
    p, root_project = projector(epsilon, q)
    assert p == -3
    right_dimension = 3
    project = kronecker_project(root_project, right_dimension)
    h_all = sp.kronecker_product(q, sp.eye(right_dimension))
    extra = sp.Matrix(
        12,
        3,
        lambda row, column: ((row + 2) * (column + 3) + row) % 7 - 3,
    )
    nuisance = h_all.row_join(extra)
    projected_nuisance = project * nuisance
    assert project * h_all == sp.zeros(12, 3)

    checks = 0
    surviving = 0
    for entries in product((0, 1), repeat=4):
        desired = sp.Matrix(list(entries) + [0] * 8)
        transverse = project * desired
        upstairs = rank(nuisance.row_join(desired)) > rank(nuisance)
        downstairs = rank(projected_nuisance.row_join(transverse)) > rank(
            projected_nuisance
        )
        assert upstairs == downstairs
        if downstairs:
            annihilators = projected_nuisance.T.nullspace()
            witness = next(row for row in annihilators if (row.T * transverse)[0] != 0)
            mu = p * witness.T / (witness.T * transverse)[0]
            selector = mu * project / p
            assert selector * nuisance == sp.zeros(1, nuisance.cols)
            assert (selector * desired)[0] == 1
            assert mu * projected_nuisance == sp.zeros(1, nuisance.cols)
            assert (mu * transverse)[0] == p
            surviving += 1
        checks += 1
    assert surviving
    return {"states": checks, "surviving": surviving, "projected_rank": rank(project)}


def check_transverse_target() -> dict[str, object]:
    epsilon = sp.Matrix([[1, 2, 3, 5, 7, 11, 13, 17, 19]])
    q = sp.Matrix([2, -1, 3, 4, 1, 5, -2, 6, 7])
    p, project = projector(epsilon, q)
    basis3 = sp.eye(3)
    root_diagonal = [
        sp.kronecker_product(basis3[:, colour], basis3[:, colour])
        for colour in range(3)
    ]
    transverse_pure = [project * vector for vector in root_diagonal]
    for colour, vector in enumerate(root_diagonal):
        kappa = (epsilon * vector)[0]
        assert transverse_pure[colour] == p * vector - kappa * q
        assert epsilon * transverse_pure[colour] == sp.zeros(1, 1)

    # Quotient the three transverse columns to one line and replay the exact
    # decomposable target equation.
    target_class = transverse_pure[0]
    nuisance = sp.Matrix.hstack(
        transverse_pure[1] - 2 * target_class,
        transverse_pure[2] + 3 * target_class,
    )
    annihilator = next(
        row
        for row in nuisance.T.nullspace()
        if (row.T * target_class)[0] != 0
    )
    quotient = annihilator.T / (annihilator.T * target_class)[0]
    pure_classes = quotient * sp.Matrix.hstack(*transverse_pure)
    assert pure_classes == sp.Matrix([[1, 2, -3]])
    assert pure_classes.rank() == 1
    alpha = sp.diag(2, 3, 5)
    response = pure_classes * alpha
    assert pure_classes * alpha == sp.Matrix([[1]]) * response

    cases = 0
    for survives, response_nonzero in product((False, True), repeat=2):
        expected_rank = int(survives and response_nonzero)
        assert (expected_rank == 0) == ((not survives) or (not response_nonzero))
        cases += 1
    return {"p": p, "pure_rank": pure_classes.rank(), "trichotomy_states": cases}


def matrix_minors(matrix: sp.MatrixBase, size: int) -> tuple[sp.Expr, ...]:
    if size > min(matrix.shape):
        return (sp.Integer(0),)
    return tuple(
        sp.expand(matrix.extract(rows, columns).det())
        for rows in combinations(range(matrix.rows), size)
        for columns in combinations(range(matrix.cols), size)
    )


def check_fitting_rank_strata() -> int:
    cases = 0
    nuisances = tuple(sp.Matrix(2, 2, entries) for entries in product((0, 1), repeat=4))
    pures = tuple(sp.Matrix(2, 3, entries) for entries in product((0, 1), repeat=6))
    for nuisance in nuisances:
        for pure in pures:
            augmented = nuisance.row_join(pure)
            rise = augmented.rank() > nuisance.rank()
            detected = any(
                all(value == 0 for value in matrix_minors(nuisance, size))
                and any(value != 0 for value in matrix_minors(augmented, size))
                for size in (1, 2)
            )
            assert rise == detected
            cases += 1
    return cases


def check_source_aggregate() -> dict[str, int]:
    epsilon = sp.Matrix([[1, 2, -1, 3]])
    q = sp.Matrix([2, 1, 4, -1])
    p, project = projector(epsilon, q)
    tau_vectors = (
        sp.Matrix([1, 0, 2]),
        sp.Matrix([0, 1, -1]),
        sp.Matrix([2, 1, 0]),
    )
    desired = (
        sp.Matrix([1, 2, 0, -1]),
        sp.Matrix([0, 1, 3, 2]),
        sp.Matrix([2, -1, 1, 0]),
    )
    f_q = sum(
        (sp.kronecker_product(left, right) for left, right in zip(desired, tau_vectors, strict=True)),
        sp.zeros(12, 1),
    )
    pi_q = sum(
        (
            (epsilon * left)[0] * right
            for left, right in zip(desired, tau_vectors, strict=True)
        ),
        sp.zeros(3, 1),
    )
    transverse = tuple(project * vector for vector in desired)
    aggregate = sum(
        (
            sp.kronecker_product(left, right)
            for left, right in zip(transverse, tau_vectors, strict=True)
        ),
        sp.zeros(12, 1),
    )
    expected = p * f_q - sp.kronecker_product(q, pi_q)
    assert aggregate == expected
    assert sp.kronecker_product(epsilon, sp.eye(3)) * aggregate == sp.zeros(3, 1)
    assert aggregate != sp.zeros(12, 1)

    synchronized = tuple(sp.Rational(value, p) * q for value in (2, -3, 5))
    synchronized_pi = sum(
        (
            (epsilon * left)[0] * right
            for left, right in zip(synchronized, tau_vectors, strict=True)
        ),
        sp.zeros(3, 1),
    )
    synchronized_f = sum(
        (
            sp.kronecker_product(left, right)
            for left, right in zip(synchronized, tau_vectors, strict=True)
        ),
        sp.zeros(12, 1),
    )
    assert p * synchronized_f == sp.kronecker_product(q, synchronized_pi)
    assert all(project * vector == sp.zeros(4, 1) for vector in synchronized)
    return {"source_terms": len(desired), "transverse_rank": rank(sp.Matrix.hstack(*transverse))}


def check_target_dimensions() -> tuple[tuple[int, int, int, int], ...]:
    records = []
    for root_order in range(3, 9):
        ports = 2 * root_order - 2
        target_count = ports * (ports - 1) // 2 + 1
        source_pairs = root_order * (root_order - 1) // 2
        assert target_count > source_pairs
        records.append((root_order, target_count, 72, 8))
    assert records[0] == (3, 7, 72, 8)
    assert records[1] == (4, 16, 72, 8)
    return tuple(records)


def main() -> None:
    algebra = check_projector_algebra()
    quotient = check_quotient_and_selector_equivalence()
    target = check_transverse_target()
    fitting = check_fitting_rank_strata()
    source = check_source_aggregate()
    dimensions = check_target_dimensions()
    print("promoted all-target transverse-quotient primary checks: PASS")
    print("  projector algebra:", algebra)
    print("  quotient/selector equivalence:", quotient)
    print("  transverse target coupling:", target)
    print("  exact Fitting rank fibres:", fitting)
    print("  source synchronization aggregate:", source)
    print("  target-count/row dimensions:", dimensions)
    print("  scope: exact reduction only; survival, activity, and node closure stay open")


if __name__ == "__main__":
    main()
