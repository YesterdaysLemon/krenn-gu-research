"""Verify the idempotent second/third-jet cycle classification."""

import sympy as sp


def hadamard(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([left[index] * right[index] for index in range(left.rows)])


def bilinear(left: sp.Matrix, matrix: sp.Matrix, right: sp.Matrix):
    return sp.expand((left.T * matrix * right)[0])


def main() -> None:
    u, v = sp.symbols("u v")
    quotient = sp.Matrix((u, v))
    quotient_square = hadamard(quotient, quotient)
    wedge = sp.expand(
        quotient[0] * quotient_square[1]
        - quotient[1] * quotient_square[0]
    )
    assert sp.expand(wedge - u * v * (v - u)) == 0

    a_class = sp.Matrix((1, 0))
    b_class = sp.Matrix((0, 1))
    c_class = sp.Matrix((1, 1))
    for fixed in (a_class, b_class, c_class):
        assert hadamard(fixed, fixed) == fixed

    zero = sp.zeros(2, 1)
    assert hadamard(a_class, b_class) == zero
    assert hadamard(b_class, a_class) == zero
    assert hadamard(a_class, c_class) == a_class
    assert hadamard(b_class, c_class) == b_class
    assert hadamard(c_class, a_class) == a_class
    assert hadamard(c_class, b_class) == b_class

    root = sp.Matrix((1, 1, 1))
    ell = sp.Matrix((1, 0, 0))
    s_form = sp.Matrix((-1, 1, 0))
    t_form = sp.Matrix((-1, 0, 1))
    y_s = sp.Matrix((0, 1, 0))
    y_t = sp.Matrix((0, 0, 1))
    assert s_form.dot(root) == t_form.dot(root) == 0
    assert ell.dot(root) == 1

    matrix_a = s_form * ell.T + ell * s_form.T + s_form * s_form.T
    matrix_b = t_form * ell.T + ell * t_form.T + t_form * t_form.T
    assert matrix_a * root == s_form
    assert matrix_a.T * root == s_form
    assert matrix_b * root == t_form
    assert matrix_b.T * root == t_form
    assert bilinear(y_s, matrix_a, y_s) == 1
    assert bilinear(y_t, matrix_b, y_t) == 1
    assert bilinear(y_s, matrix_b, y_s) == 0
    assert bilinear(y_t, matrix_a, y_t) == 0

    tangent_a = sp.Matrix((0, 1, 0))
    tangent_b = sp.Matrix((0, 0, 1))
    tangent_c = sp.Matrix((0, 1, 1))
    assert hadamard(hadamard(tangent_a, tangent_a), tangent_b) == sp.zeros(3, 1)
    assert hadamard(hadamard(tangent_b, tangent_b), tangent_a) == sp.zeros(3, 1)
    assert hadamard(hadamard(tangent_a, tangent_a), tangent_c) == tangent_a
    assert hadamard(hadamard(tangent_b, tangent_b), tangent_c) == tangent_b
    assert hadamard(hadamard(tangent_c, tangent_c), tangent_a) == tangent_a
    assert hadamard(hadamard(tangent_c, tangent_c), tangent_b) == tangent_b

    # In an even alternating cycle the A and B edge sets are distinct perfect
    # matchings, but both delete the complete root set.  Ten roots are a fixed
    # exact replay of the arbitrary 2k incidence formula in the note.
    cycle_order = 10
    matching_a = tuple((index, index + 1) for index in range(0, cycle_order, 2))
    matching_b = tuple(
        ((index + 1) % cycle_order, (index + 2) % cycle_order)
        for index in range(0, cycle_order, 2)
    )
    roots_a = {vertex for edge in matching_a for vertex in edge}
    roots_b = {vertex for edge in matching_b for vertex in edge}
    assert roots_a == roots_b == set(range(cycle_order))
    assert {frozenset(edge) for edge in matching_a} != {
        frozenset(edge) for edge in matching_b
    }

    # Both graph derivatives are scalar multiples of the same complementary
    # tensor C_R, hence have rank at most one.  The GHZ targets already have
    # rank two on any one remaining three-mode port.
    c_0, c_1, c_2, scalar_a, scalar_b = sp.symbols("c_0 c_1 c_2 a b")
    common_cofactor = sp.Matrix((c_0, c_1, c_2))
    graph_derivatives = sp.Matrix.hstack(
        scalar_a * common_cofactor, scalar_b * common_cofactor
    )
    for first_row in range(3):
        for second_row in range(first_row + 1, 3):
            minor = graph_derivatives.extract((first_row, second_row), (0, 1)).det()
            assert sp.expand(minor) == 0
    ghz_derivatives = sp.Matrix.hstack(tangent_a, tangent_b)
    assert ghz_derivatives.rank() == 2

    print("projective Hadamard fixed-point factor u*v*(v-u): VERIFIED")
    print("second-jet survivor classes A/B/C: VERIFIED")
    print("third-jet adjacency forces A-B alternation and even cycles")
    print("alternating symmetric formal edge blocks: VERIFIED")
    print("full-root A/B matchings share one deletion cofactor: VERIFIED")
    print("common graph line versus independent GHZ targets: CONTRADICTION")
    print("graph_search=0 support_search=0 colour_word_search=0")
    print("GLOBAL_STATUS=UNRESOLVED")


if __name__ == "__main__":
    main()
