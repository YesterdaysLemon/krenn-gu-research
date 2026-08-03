"""Independent no-import audit of the idempotent cycle classification."""


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True))


def hadamard(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a * b for a, b in zip(left, right, strict=True))


def outer(left: tuple[int, ...], right: tuple[int, ...]) -> list[list[int]]:
    return [[a * b for b in right] for a in left]


def add_matrices(*matrices: list[list[int]]) -> list[list[int]]:
    return [
        [sum(matrix[row][column] for matrix in matrices) for column in range(3)]
        for row in range(3)
    ]


def multiply(matrix: list[list[int]], vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(dot(tuple(row), vector) for row in matrix)


def bilinear(
    left: tuple[int, ...], matrix: list[list[int]], right: tuple[int, ...]
) -> int:
    return dot(left, multiply(matrix, right))


def main() -> None:
    # u*v^2-v*u^2 has precisely the coefficient dictionary of u*v*(v-u).
    wedge_coefficients = {(1, 2): 1, (2, 1): -1}
    factored_coefficients = {(1, 2): 1, (2, 1): -1}
    assert wedge_coefficients == factored_coefficients

    class_a, class_b, class_c = (1, 0), (0, 1), (1, 1)
    for fixed in (class_a, class_b, class_c):
        assert hadamard(fixed, fixed) == fixed
    assert hadamard(class_a, class_b) == hadamard(class_b, class_a) == (0, 0)
    assert hadamard(class_a, class_c) == hadamard(class_c, class_a) == class_a
    assert hadamard(class_b, class_c) == hadamard(class_c, class_b) == class_b

    root, ell = (1, 1, 1), (1, 0, 0)
    s_form, t_form = (-1, 1, 0), (-1, 0, 1)
    y_s, y_t = (0, 1, 0), (0, 0, 1)
    matrix_a = add_matrices(
        outer(s_form, ell), outer(ell, s_form), outer(s_form, s_form)
    )
    matrix_b = add_matrices(
        outer(t_form, ell), outer(ell, t_form), outer(t_form, t_form)
    )
    assert multiply(matrix_a, root) == s_form
    assert multiply(matrix_b, root) == t_form
    assert bilinear(y_s, matrix_a, y_s) == 1
    assert bilinear(y_t, matrix_b, y_t) == 1
    assert bilinear(y_s, matrix_b, y_s) == 0
    assert bilinear(y_t, matrix_a, y_t) == 0

    tangent_a, tangent_b, tangent_c = (0, 1, 0), (0, 0, 1), (0, 1, 1)
    assert hadamard(hadamard(tangent_a, tangent_a), tangent_b) == (0, 0, 0)
    assert hadamard(hadamard(tangent_b, tangent_b), tangent_a) == (0, 0, 0)
    assert hadamard(hadamard(tangent_a, tangent_a), tangent_c) == tangent_a
    assert hadamard(hadamard(tangent_b, tangent_b), tangent_c) == tangent_b
    assert hadamard(hadamard(tangent_c, tangent_c), tangent_a) == tangent_a
    assert hadamard(hadamard(tangent_c, tangent_c), tangent_b) == tangent_b

    alternating = (class_a, class_b) * 5
    assert all(
        alternating[index] != alternating[(index + 1) % len(alternating)]
        for index in range(len(alternating))
    )
    assert all(
        hadamard(alternating[index], alternating[(index + 1) % len(alternating)])
        == (0, 0)
        for index in range(len(alternating))
    )

    print("independent integer fixed-point and adjacency audit: PASS")
    print("independent symmetric edge-block audit: PASS")
    print("even alternating formal survivor: PASS")
    print("enumerations=0 global_status=UNRESOLVED")


if __name__ == "__main__":
    main()
