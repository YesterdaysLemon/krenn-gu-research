"""Independent no-import audit of the P7 quotient-singular incidence."""

from __future__ import annotations

import itertools
from fractions import Fraction
from math import gcd

VERTICES = tuple(range(8))
LEAVES = tuple(range(1, 8))
EDGES = tuple(itertools.combinations(VERTICES, 2))
LEAF_EDGES = tuple(itertools.combinations(LEAVES, 2))
TRIPLES = tuple(itertools.combinations(LEAVES, 3))
FOUR_SETS = tuple(itertools.combinations(LEAVES, 4))
FIVE_SETS = tuple(itertools.combinations(LEAVES, 5))
SIX_SETS = tuple(itertools.combinations(LEAVES, 6))
GLOBAL_FOUR_SETS = tuple(itertools.combinations(VERTICES, 4))
GLOBAL_SIX_SETS = tuple(itertools.combinations(VERTICES, 6))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
LEAF_EDGE_INDEX = {edge: index for index, edge in enumerate(LEAF_EDGES)}
FOUR_INDEX = {subset: index for index, subset in enumerate(FOUR_SETS)}
FIVE_INDEX = {subset: index for index, subset in enumerate(FIVE_SETS)}
Polynomial = dict[tuple[str, ...], Fraction]
FormalBoolean = dict[int, Polynomial]


def exact_rank(matrix: list[list[int]]) -> int:
    """Compute exact rank by fraction-free integer elimination."""
    if not matrix:
        return 0
    work = [row[:] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        for row in range(len(work)):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            tail = [
                pivot_value * work[row][inner]
                - factor * work[pivot_row][inner]
                for inner in range(column, len(work[0]))
            ]
            divisor = 0
            for value in tail:
                divisor = gcd(divisor, abs(value))
            if divisor > 1:
                tail = [value // divisor for value in tail]
            work[row][column:] = tail
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def bareiss_determinant(matrix: list[list[int]]) -> int:
    """Compute a square integer determinant by fraction-free Bareiss."""
    work = [row[:] for row in matrix]
    size = len(work)
    sign = 1
    previous = 1
    for column in range(size - 1):
        pivot = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1
        pivot_value = work[column][column]
        for row in range(column + 1, size):
            for inner in range(column + 1, size):
                numerator = (
                    work[row][inner] * pivot_value
                    - work[row][column] * work[column][inner]
                )
                assert numerator % previous == 0
                work[row][inner] = numerator // previous
            work[row][column] = 0
        previous = pivot_value
    return sign * work[-1][-1]


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """Transpose an integer matrix."""
    return [list(row) for row in zip(*matrix, strict=True)]


def mat_vec(matrix: list[list[int]], vector: list[int]) -> list[int]:
    """Multiply an integer matrix by a vector."""
    return [
        sum(entry * value for entry, value in zip(row, vector, strict=True))
        for row in matrix
    ]


def set_mask(vertices: tuple[int, ...]) -> int:
    """Encode a subset by a bit mask."""
    out = 0
    for vertex in vertices:
        out |= 1 << vertex
    return out


def standard_tableaux() -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    """Return all fourteen standard (4,4) tableaux."""
    tableaux = []
    for top in itertools.combinations(VERTICES, 4):
        bottom = tuple(vertex for vertex in VERTICES if vertex not in top)
        if all(left < right for left, right in zip(top, bottom, strict=True)):
            tableaux.append((top, bottom))
    return tableaux


def polytabloid(
    top: tuple[int, ...], bottom: tuple[int, ...]
) -> dict[tuple[int, ...], int]:
    """Expand a (4,4) column polytabloid independently."""
    out = {subset: 0 for subset in GLOBAL_FOUR_SETS}
    for choices in itertools.product((0, 1), repeat=4):
        subset = tuple(
            sorted(
                bottom[index] if choice else top[index]
                for index, choice in enumerate(choices)
            )
        )
        out[subset] += (-1) ** sum(choices)
    return out


def leaf_primitive_vectors() -> list[list[int]]:
    """Restrict the fourteen global primitive polytabloids to leaf four-sets."""
    return [
        [polytabloid(top, bottom)[subset] for subset in FOUR_SETS]
        for top, bottom in standard_tableaux()
    ]


def leaf_total_zero_basis() -> list[list[int]]:
    """Return the twenty columns of the total-zero leaf-edge hyperplane."""
    columns = []
    for free_index in range(20):
        column = [0] * 21
        column[free_index] = 1
        column[20] = -1
        columns.append(column)
    return columns


def leaf_down(g_vector: list[int]) -> list[int]:
    """Take the seven leaf row sums of an edge vector."""
    return [
        sum(
            g_vector[LEAF_EDGE_INDEX[edge]]
            for edge in LEAF_EDGES
            if vertex in edge
        )
        for vertex in LEAVES
    ]


def iota(g_vector: list[int]) -> list[int]:
    """Embed a total-zero leaf quadratic into the global zero-row quotient."""
    down = leaf_down(g_vector)
    out = [0] * 28
    for row, edge in enumerate(LEAF_EDGES):
        out[EDGE_INDEX[edge]] = g_vector[row]
    for row, vertex in enumerate(LEAVES):
        out[EDGE_INDEX[(0, vertex)]] = -down[row]
    return out


def global_h(n_vector: list[int]) -> dict[tuple[int, ...], int]:
    """Build H_N=z_0 JN+N."""
    out = {}
    for subset in GLOBAL_FOUR_SETS:
        if 0 not in subset:
            out[subset] = n_vector[FOUR_INDEX[subset]]
        else:
            triple = tuple(vertex for vertex in subset if vertex != 0)
            complement = tuple(vertex for vertex in LEAVES if vertex not in triple)
            out[subset] = n_vector[FOUR_INDEX[complement]]
    return out


def catalecticant(h_vector: dict[tuple[int, ...], int]) -> list[list[int]]:
    """Build the global edge catalecticant."""
    return [
        [
            h_vector[tuple(sorted((*edge, *other)))]
            if set(edge).isdisjoint(other)
            else 0
            for other in EDGES
        ]
        for edge in EDGES
    ]


def phi(n_vector: list[int], g_vector: list[int]) -> list[int]:
    """Compute Phi_N(G)=G(JN)-(partial G)N on leaf five-sets."""
    down = leaf_down(g_vector)
    out = []
    for five in FIVE_SETS:
        first = 0
        for edge in itertools.combinations(five, 2):
            triple = tuple(vertex for vertex in five if vertex not in edge)
            complement = tuple(vertex for vertex in LEAVES if vertex not in triple)
            first += (
                g_vector[LEAF_EDGE_INDEX[edge]]
                * n_vector[FOUR_INDEX[complement]]
            )
        second = sum(
            down[LEAVES.index(vertex)]
            * n_vector[FOUR_INDEX[tuple(item for item in five if item != vertex)]]
            for vertex in five
        )
        out.append(first - second)
    return out


def complement_phi(phi_vector: list[int]) -> list[int]:
    """Complement leaf five-sets to leaf edges."""
    return [
        phi_vector[
            FIVE_INDEX[tuple(vertex for vertex in LEAVES if vertex not in edge)]
        ]
        for edge in LEAF_EDGES
    ]


def multiply_w_h(
    w_vector: list[int], h_vector: dict[tuple[int, ...], int]
) -> dict[tuple[int, ...], int]:
    """Multiply a global quadratic by a global four-form."""
    out = {}
    for six in GLOBAL_SIX_SETS:
        out[six] = sum(
            w_vector[EDGE_INDEX[edge]]
            * h_vector[tuple(vertex for vertex in six if vertex not in edge)]
            for edge in itertools.combinations(six, 2)
        )
    return out


def factored_six_form(phi_vector: list[int]) -> dict[tuple[int, ...], int]:
    """Build (z_0-ell_L)Phi in degree six."""
    out = {}
    for six in GLOBAL_SIX_SETS:
        if 0 in six:
            five = tuple(vertex for vertex in six if vertex != 0)
            out[six] = phi_vector[FIVE_INDEX[five]]
        else:
            out[six] = -sum(
                phi_vector[
                    FIVE_INDEX[tuple(vertex for vertex in six if vertex != omitted)]
                ]
                for omitted in six
            )
    return out


def verify_leaf_primitive(n_vector: list[int]) -> None:
    """Verify ell N=0 and N+ell JN=0 coefficientwise."""
    for five in FIVE_SETS:
        assert (
            sum(
                n_vector[
                    FOUR_INDEX[tuple(vertex for vertex in five if vertex != omitted)]
                ]
                for omitted in five
            )
            == 0
        )
    for four in FOUR_SETS:
        ell_jn = 0
        for omitted in four:
            triple = tuple(vertex for vertex in four if vertex != omitted)
            complement = tuple(vertex for vertex in LEAVES if vertex not in triple)
            ell_jn += n_vector[FOUR_INDEX[complement]]
        assert n_vector[FOUR_INDEX[four]] + ell_jn == 0


def poly_variable(name: str) -> Polynomial:
    """Return one independent formal variable."""
    return {(name,): Fraction(1)}


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    """Add sparse formal polynomials."""
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, Fraction(0)) + coefficient
        if out[monomial] == 0:
            del out[monomial]
    return out


def poly_scale(value: Fraction, polynomial: Polynomial) -> Polynomial:
    """Scale a sparse formal polynomial."""
    return {
        monomial: value * coefficient
        for monomial, coefficient in polynomial.items()
        if value * coefficient
    }


def poly_mul(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply sparse formal polynomials."""
    out: Polynomial = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            out[monomial] = (
                out.get(monomial, Fraction(0))
                + left_coefficient * right_coefficient
            )
    return {monomial: coefficient for monomial, coefficient in out.items() if coefficient}


def formal_add(left: FormalBoolean, right: FormalBoolean) -> FormalBoolean:
    """Add formal Boolean-algebra elements."""
    out = {mask: dict(coefficient) for mask, coefficient in left.items()}
    for mask, coefficient in right.items():
        out[mask] = poly_add(out.get(mask, {}), coefficient)
        if not out[mask]:
            del out[mask]
    return out


def formal_scale(value: Fraction, form: FormalBoolean) -> FormalBoolean:
    """Scale a formal Boolean-algebra element."""
    return {
        mask: coefficient
        for mask, polynomial in form.items()
        if (coefficient := poly_scale(value, polynomial))
    }


def formal_mul(left: FormalBoolean, right: FormalBoolean) -> FormalBoolean:
    """Multiply formal expressions modulo z_i^2=0."""
    out: FormalBoolean = {}
    for left_mask, left_coefficient in left.items():
        for right_mask, right_coefficient in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            out[mask] = poly_add(
                out.get(mask, {}), poly_mul(left_coefficient, right_coefficient)
            )
    return {mask: coefficient for mask, coefficient in out.items() if coefficient}


def audit_physical_dictionary() -> None:
    """Independently audit M=AF, N=F^2/2, and Q^2/2."""
    linear_a = {1 << vertex: poly_variable(f"a_{vertex}") for vertex in LEAVES}
    physical_f = {}
    for edge in LEAF_EDGES:
        coefficient = poly_mul(
            poly_mul(poly_variable(f"a_{edge[0]}"), poly_variable(f"a_{edge[1]}")),
            poly_variable(f"x_{edge[0]}{edge[1]}"),
        )
        physical_f[set_mask(edge)] = coefficient
    physical_m = formal_mul(linear_a, physical_f)
    physical_n = formal_scale(Fraction(1, 2), formal_mul(physical_f, physical_f))

    for triple in TRIPLES:
        expected: Polynomial = {}
        a_product: Polynomial = {(): Fraction(1)}
        for vertex in triple:
            a_product = poly_mul(a_product, poly_variable(f"a_{vertex}"))
        for edge in itertools.combinations(triple, 2):
            expected = poly_add(
                expected, poly_mul(a_product, poly_variable(f"x_{edge[0]}{edge[1]}"))
            )
        assert physical_m[set_mask(triple)] == expected

    for four in FOUR_SETS:
        a_product = {(): Fraction(1)}
        for vertex in four:
            a_product = poly_mul(a_product, poly_variable(f"a_{vertex}"))
        p, q, r, s = four
        expected: Polynomial = {}
        for left, right in (
            ((p, q), (r, s)),
            ((p, r), (q, s)),
            ((p, s), (q, r)),
        ):
            matching = poly_mul(
                poly_variable(f"x_{left[0]}{left[1]}"),
                poly_variable(f"x_{right[0]}{right[1]}"),
            )
            expected = poly_add(expected, poly_mul(a_product, matching))
        assert physical_n[set_mask(four)] == expected

    star = {
        set_mask((0, vertex)): coefficient
        for vertex, coefficient in zip(LEAVES, linear_a.values(), strict=True)
    }
    t_f = {
        mask: poly_mul(poly_variable("t"), coefficient)
        for mask, coefficient in physical_f.items()
    }
    q_form = formal_add(star, t_f)
    q_square_half = formal_scale(Fraction(1, 2), formal_mul(q_form, q_form))
    expected_expansion: FormalBoolean = {}
    for mask, coefficient in physical_m.items():
        expected_expansion[mask | 1] = poly_mul(poly_variable("t"), coefficient)
    for mask, coefficient in physical_n.items():
        expected_expansion[mask] = poly_mul(
            poly_mul(poly_variable("t"), poly_variable("t")), coefficient
        )
    assert q_square_half == expected_expansion


def main() -> None:
    """Run the independent exact audit."""
    primitive_vectors = leaf_primitive_vectors()
    assert len(primitive_vectors) == 14
    assert exact_rank(primitive_vectors) == 14
    for n_vector in primitive_vectors:
        verify_leaf_primitive(n_vector)

    leaf_basis = leaf_total_zero_basis()
    assert exact_rank(leaf_basis) == 20
    iota_columns = [iota(column) for column in leaf_basis]
    assert exact_rank(iota_columns) == 20
    incidence = [[int(vertex in edge) for edge in EDGES] for vertex in VERTICES]
    for column in iota_columns:
        assert mat_vec(incidence, column) == [0] * 8

    for n_vector in primitive_vectors:
        h_vector = global_h(n_vector)
        d_matrix = catalecticant(h_vector)
        for subset in GLOBAL_FOUR_SETS:
            complement = tuple(vertex for vertex in VERTICES if vertex not in subset)
            assert h_vector[subset] == h_vector[complement]
        for g_vector, w_vector in zip(leaf_basis, iota_columns, strict=True):
            phi_vector = phi(n_vector, g_vector)
            complemented = complement_phi(phi_vector)
            assert sum(complemented) == 0
            assert multiply_w_h(w_vector, h_vector) == factored_six_form(phi_vector)
            assert mat_vec(d_matrix, w_vector) == iota(complemented)

    control_n = [
        sum(vector[index] for vector in primitive_vectors)
        for index in range(len(FOUR_SETS))
    ]
    verify_leaf_primitive(control_n)
    control_columns = [complement_phi(phi(control_n, column)) for column in leaf_basis]
    control_square = [column[:20] for column in control_columns]
    assert exact_rank(control_square) == 20
    control_determinant = bareiss_determinant(control_square)
    assert control_determinant == 1_519_811_734_108_372_992
    control_global = global_h(control_n)
    assert exact_rank(catalecticant(control_global)) == 20

    # Perfect-pairing normalization on every edge pair for the fixed control.
    for edge in EDGES:
        for other in EDGES:
            entry = catalecticant(control_global)[EDGE_INDEX[edge]][EDGE_INDEX[other]]
            if set(edge).isdisjoint(other):
                union = tuple(sorted((*edge, *other)))
                complement = tuple(vertex for vertex in VERTICES if vertex not in union)
                assert entry == control_global[complement]
            else:
                assert entry == 0

    audit_physical_dictionary()

    print("AUDIT PASS: fourteen-dimensional leaf primitive module rebuilt")
    print("AUDIT PASS: N+ell*JN=0 on a complete exact basis")
    print("AUDIT PASS: total-zero leaf hyperplane is the global quotient P")
    print("AUDIT PASS: annihilator factorization and conjugacy on 280 basis pairs")
    print("AUDIT PASS: fixed Phi determinant = 2^24*3^13*7*8117")
    print("AUDIT PASS: physical radial coefficient dictionary rebuilt formally")
    print("imports_from_primary=0 imports_from_project=0")
    print("searches=0 finite_fields=0 graph_enumerations=0 groebner=0")
    print("SCOPE: fixed rank-20 control is not asserted physical")
    print("SCOPE: physical quotient-singular incidence remains UNKNOWN")
    print("SCOPE: P7 and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
