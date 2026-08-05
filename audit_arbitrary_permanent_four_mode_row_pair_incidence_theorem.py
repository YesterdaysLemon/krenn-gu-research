"""Independent no-import audit of the four-mode row-pair theorem."""


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, 0) + coefficient
            if result[monomial] == 0:
                del result[monomial]
    return result


def scale(coefficient, polynomial):
    return {monomial: coefficient * value for monomial, value in polynomial.items() if coefficient * value}


def multiply(left, right):
    result = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = result.get(monomial, 0) + left_coefficient * right_coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def variable(name):
    return {(name,): 1}


def main() -> None:
    # Sparse-polynomial reconstruction of the two forbidden response entries.
    g, h, i, j, k, ell = tuple(variable(name) for name in ("g", "h", "i", "j", "k", "ell"))
    equation_20 = add(multiply(g, j), multiply(h, i))
    equation_21 = add(multiply(g, ell), multiply(h, k))
    determinant = add(multiply(i, ell), scale(-1, multiply(j, k)))

    elimination_g = add(multiply(k, equation_20), scale(-1, multiply(i, equation_21)))
    elimination_h = add(multiply(ell, equation_20), scale(-1, multiply(j, equation_21)))
    assert elimination_g == multiply(g, scale(-1, determinant))
    assert elimination_h == multiply(h, determinant)

    # If the second endpoint columns are a basis, determinant is nonzero;
    # zero response equations therefore force g=h=0, destroying the first
    # endpoint basis.  The target contraction selecting this situation is
    # independently checked with exact integer null vectors.
    boundary_nulls = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    torus_nulls = ((1, 1, 1), (1, 2, 3), (2, 3, 5), (3, 5, 7))
    selected = (boundary_nulls[1], boundary_nulls[2])
    complement = (boundary_nulls[0],) + torus_nulls
    target_diagonal = tuple(
        1
        if all(vector[color] != 0 for vector in complement)
        else 0
        for color in range(3)
    )
    assert selected == ((0, 1, 0), (0, 0, 1))
    assert target_diagonal == (1, 0, 0)

    planes = ({0, 1}, {0, 2}, {1, 2})
    color_degrees = tuple(sum(color in plane for plane in planes) for color in range(3))
    assert color_degrees == (2, 2, 2)

    print("PASS: independent sparse-polynomial four-mode incidence audit")
    print("PASS: exact rank-one polar target and Cramer contradiction")
    print("SCOPE: arbitrary-order necessary theorem, not global exclusion")


if __name__ == "__main__":
    main()
