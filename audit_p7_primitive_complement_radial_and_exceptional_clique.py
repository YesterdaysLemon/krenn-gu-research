"""No-import audit of primitive P7 radial closure and exceptional cliques."""

from itertools import combinations, permutations
from math import gcd

Poly = dict[tuple[int, int, int], int]


def integer_rank(matrix: list[list[int]]) -> int:
    """Exact fraction-free rank with row-content control."""
    work = [row[:] for row in matrix]
    if not work:
        return 0
    nrows, ncols = len(work), len(work[0])
    pivot_row = 0
    for column in range(ncols):
        pivot = next((row for row in range(pivot_row, nrows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        for row in range(nrows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            tail = [
                pivot_value * work[row][j] - factor * work[pivot_row][j]
                for j in range(column, ncols)
            ]
            divisor = 0
            for value in tail:
                divisor = gcd(divisor, abs(value))
            if divisor > 1:
                tail = [value // divisor for value in tail]
            work[row][column:] = tail
        pivot_row += 1
        if pivot_row == nrows:
            break
    return pivot_row


def matmul(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    """Integer matrix product."""
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right))) for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def poly_add(*polys: Poly) -> Poly:
    result: Poly = {}
    for poly in polys:
        for monomial, coefficient in poly.items():
            result[monomial] = result.get(monomial, 0) + coefficient
            if result[monomial] == 0:
                del result[monomial]
    return result


def poly_scale(poly: Poly, scalar: int) -> Poly:
    return {monomial: scalar * coefficient for monomial, coefficient in poly.items() if coefficient}


def poly_mul(*polys: Poly) -> Poly:
    result: Poly = {(0, 0, 0): 1}
    for poly in polys:
        product: Poly = {}
        for left_monomial, left_coefficient in result.items():
            for right_monomial, right_coefficient in poly.items():
                monomial = tuple(
                    left + right
                    for left, right in zip(left_monomial, right_monomial, strict=True)
                )
                product[monomial] = (
                    product.get(monomial, 0) + left_coefficient * right_coefficient
                )
        result = {monomial: coefficient for monomial, coefficient in product.items() if coefficient}
    return result


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def poly_determinant(matrix: list[list[Poly]]) -> Poly:
    """Leibniz determinant for the fixed matrices of size at most six."""
    size = len(matrix)
    result: Poly = {}
    for permutation in permutations(range(size)):
        term = poly_mul(*(matrix[row][permutation[row]] for row in range(size)))
        result = poly_add(result, poly_scale(term, permutation_sign(permutation)))
    return result


def hafnian_monomials(
    vertices: tuple[int, ...], weights: dict[tuple[int, int], tuple[str, ...]]
) -> list[tuple[str, ...]]:
    """Return the fixed hafnian expansion as a multiset of factor monomials."""
    if not vertices:
        return [()]
    first = vertices[0]
    result = []
    for partner in vertices[1:]:
        edge = tuple(sorted((first, partner)))
        remainder = tuple(vertex for vertex in vertices[1:] if vertex != partner)
        for monomial in hafnian_monomials(remainder, weights):
            result.append(tuple(sorted((*weights[edge], *monomial))))
    return sorted(result)


ZERO: Poly = {}
ONE: Poly = {(0, 0, 0): 1}
S: Poly = {(1, 0, 0): 1}
P: Poly = {(0, 1, 0): 1}
Q: Poly = {(0, 0, 1): 1}


def exceptional_matrix(c_size: int, outside: list[Poly]) -> list[list[Poly]]:
    outside_edges = list(combinations(range(len(outside)), 2))
    size = len(outside) + len(outside_edges)
    matrix = [[ZERO for _ in range(size)] for _ in range(size)]
    for index, weight in enumerate(outside):
        matrix[index][index] = poly_add(poly_scale(S, c_size + 2), poly_scale(weight, -2))
        for edge_index, (left, right) in enumerate(outside_edges):
            column = len(outside) + edge_index
            if index == left:
                matrix[index][column] = poly_scale(
                    poly_mul(poly_add(S, poly_scale(weight, -1)), outside[right]), -2
                )
            elif index == right:
                matrix[index][column] = poly_scale(
                    poly_mul(poly_add(S, poly_scale(weight, -1)), outside[left]), -2
                )
    for edge_index, (left, right) in enumerate(outside_edges):
        row = len(outside) + edge_index
        matrix[row][left] = ONE
        matrix[row][right] = ONE
        matrix[row][row] = poly_add(
            poly_scale(S, 4), poly_scale(outside[left], -2), poly_scale(outside[right], -2)
        )
    return matrix


def main() -> None:
    vertices = tuple(range(8))
    leaves = tuple(range(1, 8))
    triples = list(combinations(vertices, 3))
    four_sets = list(combinations(vertices, 4))
    triple_position = {triple: index for index, triple in enumerate(triples)}
    four_position = {four: index for index, four in enumerate(four_sets)}

    lowering = [[0] * 70 for _ in range(56)]
    for row, triple in enumerate(triples):
        for vertex in vertices:
            if vertex not in triple:
                lowering[row][four_position[tuple(sorted((*triple, vertex)))]] = 1
    assert integer_rank(lowering) == 56

    complement_matrix = [[0] * 70 for _ in range(70)]
    complement_plus = [[0] * 35 for _ in range(70)]
    for four in four_sets:
        other = tuple(sorted(set(vertices) - set(four)))
        complement_matrix[four_position[other]][four_position[four]] = 1
    for column, leaf_triple in enumerate(combinations(leaves, 3)):
        anchor_four = (0, *leaf_triple)
        other = tuple(sorted(set(vertices) - set(anchor_four)))
        complement_plus[four_position[anchor_four]][column] = 1
        complement_plus[four_position[other]][column] = 1

    restricted = matmul(lowering, complement_plus)
    star_rows = [triple_position[(0, *pair)] for pair in combinations(leaves, 2)]
    assert integer_rank(restricted) == integer_rank([restricted[row] for row in star_rows]) == 21

    # ker(lowering) is complement fixed: row(C-I) is contained in row(lowering).
    complement_minus_identity = [
        [complement_matrix[i][j] - int(i == j) for j in range(70)] for i in range(70)
    ]
    assert integer_rank(lowering + complement_minus_identity) == 56

    # Independent ranks for the two radial nonvanishing statements.
    leaf_pairs = list(combinations(leaves, 2))
    leaf_triples = list(combinations(leaves, 3))
    w23 = [[int(set(pair) < set(triple)) for pair in leaf_pairs] for triple in leaf_triples]
    assert integer_rank(w23) == 21
    singleton_to_triples = [
        [int(vertex in triple) for vertex in range(5)] for triple in combinations(range(5), 3)
    ]
    assert integer_rank(singleton_to_triples) == 5

    # Separate fixed matching recursion for both sides of the radial
    # complement formula H_(0T)=t*u_T and H_(L\T)=t^2*v_T.
    symbolic_weights: dict[tuple[int, int], tuple[str, ...]] = {}
    for leaf in leaves:
        symbolic_weights[(0, leaf)] = (f"a{leaf}",)
    for left, right in combinations(leaves, 2):
        symbolic_weights[(left, right)] = (
            "t",
            f"a{left}",
            f"a{right}",
            f"x{left}{right}",
        )
    common_anchor = ("a1", "a2", "a3", "t")
    expected_anchor = sorted(
        tuple(sorted((*common_anchor, edge_factor)))
        for edge_factor in ("x12", "x13", "x23")
    )
    assert hafnian_monomials((0, 1, 2, 3), symbolic_weights) == expected_anchor
    common_complement = ("a4", "a5", "a6", "a7", "t", "t")
    expected_complement = sorted(
        tuple(sorted((*common_complement, first, second)))
        for first, second in (("x45", "x67"), ("x46", "x57"), ("x47", "x56"))
    )
    assert hafnian_monomials((4, 5, 6, 7), symbolic_weights) == expected_complement

    # Independent sparse-polynomial exceptional-clique determinants.
    minus_two_s = poly_scale(S, -2)
    det6 = poly_determinant(exceptional_matrix(6, [minus_two_s]))
    assert det6 == poly_scale(S, 12)

    minus_s_minus_p = poly_add(poly_scale(S, -1), poly_scale(P, -1))
    det5 = poly_determinant(exceptional_matrix(5, [P, minus_s_minus_p]))
    assert det5 == poly_scale(poly_mul(S, S, S), 360)

    r = poly_add(poly_scale(P, -1), poly_scale(Q, -1))
    det4 = poly_determinant(exceptional_matrix(4, [P, Q, r]))
    e2 = poly_add(poly_mul(P, Q), poly_mul(P, r), poly_mul(Q, r))
    e3 = poly_mul(P, Q, r)
    cubic = poly_add(poly_scale(e3, 3), poly_scale(poly_mul(S, e2), 2), poly_scale(poly_mul(S, S, S), 12))
    expected4 = poly_scale(poly_mul(S, S, S, cubic), 1152)
    assert det4 == expected4

    assert 35 * 34 // 2 == 595
    assert 23 + 44 == 67

    print("PASS: no-import Boolean complement/anchor kernel equality")
    print("PASS: no-import radial linear and four-hafnian nonvanishing ranks")
    print("PASS: no-import matching recursion for both radial complement formulas")
    print("PASS: sparse-polynomial exceptional clique determinants and cubic")
    print("UNKNOWN: degree-67 corank-one torus incidence")
    print("UNKNOWN: corank-at-least-two primitive torus incidence")
    print("UNRESOLVED: global Krenn--Gu conjecture")


if __name__ == "__main__":
    main()
