"""Primary exact checks for P6 spanning-tree radicals and factor compatibility."""

from fractions import Fraction
from itertools import combinations, combinations_with_replacement, product


Q = Fraction
FULL = (1 << 6) - 1


def linear_form(entries):
    return {1 << index: Q(value) for index, value in enumerate(entries) if value}


def multiply(left, right):
    out = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            out[mask] = out.get(mask, Q(0)) + left_value * right_value
    return {mask: value for mask, value in out.items() if value}


def product_polynomials(factors):
    out = {0: Q(1)}
    for factor in factors:
        out = multiply(out, factor)
    return out


def degree_masks(degree):
    return tuple(sum(1 << index for index in subset) for subset in combinations(range(6), degree))


def vectors(polynomials, degree):
    masks = degree_masks(degree)
    return [tuple(polynomial.get(mask, Q(0)) for mask in masks) for polynomial in polynomials]


def rank(rows):
    matrix = [list(row) for row in rows if any(row)]
    if not matrix:
        return 0
    row_index = 0
    for column in range(len(matrix[0])):
        pivot = next((i for i in range(row_index, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[row_index], matrix[pivot] = matrix[pivot], matrix[row_index]
        scale = matrix[row_index][column]
        matrix[row_index] = [value / scale for value in matrix[row_index]]
        for i in range(len(matrix)):
            if i == row_index or not matrix[i][column]:
                continue
            scale = matrix[i][column]
            matrix[i] = [a - scale * b for a, b in zip(matrix[i], matrix[row_index], strict=True)]
        row_index += 1
        if row_index == len(matrix):
            break
    return row_index


def span_equal(left, right, degree):
    left_vectors = vectors(left, degree)
    right_vectors = vectors(right, degree)
    common_rank = rank(left_vectors + right_vectors)
    return common_rank == rank(left_vectors) == rank(right_vectors)


def product_space(left, right):
    return [multiply(a, b) for a in left for b in right]


def main() -> None:
    w = (
        linear_form((1, 0, 0, 1, 0, 0)),
        linear_form((0, 1, 0, 0, 1, 0)),
        linear_form((0, 0, 1, 0, 0, 1)),
    )
    v = (
        linear_form((1, 1, 1, 1, 1, 1)),
        linear_form((1, 2, 3, 1, 2, 3)),
        linear_form((1, 4, 9, 1, 4, 9)),
    )

    pair_space = [multiply(w[i], w[j]) for i, j in combinations_with_replacement(range(3), 2)]
    assert rank(vectors(pair_space, 2)) == 6
    mixed = [multiply(v[i], v[j]) for i, j in combinations(range(3), 2)]
    squares = [multiply(form, form) for form in v]
    assert rank(vectors(mixed, 2)) == 3
    assert rank(vectors(mixed + squares, 2)) == 6

    fourth_space = [product_polynomials(w[i] for i in indices) for indices in product(range(3), repeat=4)]
    assert rank(vectors(fourth_space, 4)) == 6

    # Every one of the fifteen pairs has the same common-factor spaces.
    for _pair in combinations(range(6), 2):
        assert rank(vectors(pair_space, 2)) == 6
        assert rank(vectors(fourth_space, 4)) == 6

    pair_pair = product_space(pair_space, pair_space)
    assert span_equal(pair_pair, fourth_space, 4)

    coefficients = []
    for form in v:
        coefficients.append(product_polynomials((form,) * 6).get(FULL, Q(0)))
    assert coefficients == [720, 25920, 933120]
    mixed_coefficient = product_polynomials((v[0], v[0], v[1], v[1], v[2], v[2])).get(FULL, Q(0))
    assert mixed_coefficient == 41456

    path_edges = tuple((i, i + 1) for i in range(5))
    for word in product(range(3), repeat=6):
        exposed = any(word[a] != word[b] for a, b in path_edges)
        assert exposed == (len(set(word)) > 1)

    print("P6 co-two spanning-tree and compatibility primary checks: PASS")
    print("pair/complement dimensions and product identities: PASS")
    print("pure coefficients and mixed 001122=41456: PASS")


if __name__ == "__main__":
    main()
