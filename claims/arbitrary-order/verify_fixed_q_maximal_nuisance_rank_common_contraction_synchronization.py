"""Primary exact replay for maximal-rank contraction synchronization.

The theorem is the principal-open argument in the owning document.  This
script checks finite seven-/thirty-one-target polynomial controls and the
rank-drop-only counterboundary.
"""

import sympy as sp


def nuisance_family(index: int, x, y) -> tuple[sp.Matrix, sp.Matrix, object]:
    nuisance = sp.Matrix(
        [
            [1, 0],
            [0, x + index],
            [0, y + index + 1],
        ]
    )
    desired = sp.Matrix([0, 1, 0])
    response = x + 2 * index + 1
    return nuisance, desired, response


def check_finite_family(size: int) -> None:
    x, y = sp.symbols("x y")
    witness = {x: sp.Integer(2), y: sp.Integer(3)}
    open_product = sp.Integer(1)
    for index in range(1, size + 1):
        nuisance, desired, response = nuisance_family(index, x, y)
        assert nuisance.rank() == 2
        augmented = nuisance.row_join(desired)
        augmented_minor = sp.factor(augmented.det())
        assert augmented_minor == -(y + index + 1)
        nuisance_minor = x + index
        open_product *= nuisance_minor * augmented_minor * response
        assert nuisance.subs(witness).rank() == 2
        assert augmented.subs(witness).rank() == 3
        assert response.subs(witness) != 0
    assert sp.expand(open_product) != 0
    assert open_product.subs(witness) != 0


def check_rank_drop_countercontrol() -> None:
    t = sp.symbols("t")
    desired = sp.Matrix([1])
    first = sp.Matrix([[t - 1]])
    second = sp.Matrix([[t - 2]])
    assert first.rank() == second.rank() == 1
    assert first.subs(t, 1).rank() == 0
    assert first.row_join(desired).subs(t, 1).rank() == 1
    assert second.subs(t, 2).rank() == 0
    assert second.row_join(desired).subs(t, 2).rank() == 1
    for value in (sp.Integer(1), sp.Integer(2)):
        survives_first = (
            first.subs(t, value).rank() < first.row_join(desired).subs(t, value).rank()
        )
        survives_second = (
            second.subs(t, value).rank()
            < second.row_join(desired).subs(t, value).rank()
        )
        assert survives_first != survives_second


def main() -> None:
    check_finite_family(7)
    check_finite_family(31)
    check_rank_drop_countercontrol()
    print("maximal-nuisance-rank synchronization primary replay: PASS")


if __name__ == "__main__":
    main()
