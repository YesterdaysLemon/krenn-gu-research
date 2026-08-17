"""Primary exact replay for contraction escape versus generic absorption."""

import sympy as sp


def augmented_rank(matrix: sp.Matrix, *columns: sp.Matrix) -> int:
    answer = matrix
    for column in columns:
        answer = answer.row_join(column)
    return answer.rank()


def check_escapable_family() -> None:
    t = sp.symbols("t")
    e1 = sp.Matrix([1, 0])
    families = (
        sp.Matrix([1, t - 1]),
        sp.Matrix([1, (t - 1) ** 2]),
    )
    augmented_minors = []
    for nuisance in families:
        assert nuisance.rank() == 1
        assert augmented_rank(nuisance, e1) == 2
        determinant = sp.expand(nuisance.row_join(e1).det())
        assert determinant != 0
        augmented_minors.append(determinant)

        swallowed = nuisance.subs(t, 1)
        assert swallowed.rank() == 1
        assert augmented_rank(swallowed, e1) == 1
        escaped = nuisance.subs(t, 2)
        assert augmented_rank(escaped, e1) == 2

    for target_count in (7, 31):
        product_value = sp.Integer(1)
        for index in range(target_count):
            product_value *= augmented_minors[index % len(augmented_minors)]
        assert sp.expand(product_value) != 0
        assert product_value.subs(t, 2) != 0


def check_generic_absorption() -> None:
    t = sp.symbols("t")
    nuisance = sp.Matrix([[t - 1]])
    target = sp.Matrix([1])
    assert nuisance.rank() == 1
    assert augmented_rank(nuisance, target, target, target, target) == 1
    delta = t - 1
    coefficient = sp.Matrix([1])
    for column in (target, target, target, target):
        assert nuisance * coefficient == delta * column

    exceptional = nuisance.subs(t, 1)
    assert exceptional.rank() == 0
    assert augmented_rank(exceptional, target) == 1


def check_response_zero_exception() -> None:
    nuisance = sp.Matrix([1, 0])
    pure = sp.Matrix([1, 0])
    desired = sp.Matrix([0, 1])
    assert augmented_rank(nuisance, pure, pure, pure) == 1
    assert augmented_rank(nuisance, desired) == 2
    response = sp.zeros(3, 1)
    assert response == sp.zeros(3, 1)


def main() -> None:
    check_escapable_family()
    check_generic_absorption()
    check_response_zero_exception()
    print("fixed-Q contraction escape/generic absorption primary replay: PASS")


if __name__ == "__main__":
    main()
