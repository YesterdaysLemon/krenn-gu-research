"""Primary exact checks for GLS65 (audit only; not the written proof)."""

from itertools import permutations, product

import sympy as sp

ROWS = ("P", "Q", "A", "B")
P, Q, A, B = range(4)


def permanent(rows: list[list[sp.Expr]]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[i][sigma[i]] for i in range(len(rows)))
            for sigma in permutations(range(len(rows)))
        )
    )


def tensor_permanent(local_columns: list[dict[str, tuple[sp.Expr, ...]]]):
    dimensions = tuple(len(local_columns[i]["P"]) for i in range(4))
    result = {}
    for output in product(*(range(dimension) for dimension in dimensions)):
        result[output] = sp.expand(
            sum(
                sp.prod(local_columns[i][assignment[i]][output[i]] for i in range(4))
                for assignment in permutations(ROWS)
            )
        )
    return result


# The GLS64 factorization has exactly one term for every P,Q,A,B assignment.
factorized_assignments = []
for pair in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)):
    complement = tuple(i for i in range(4) if i not in pair)
    for pq_order in (("P", "Q"), ("Q", "P")):
        for ab_order in (("A", "B"), ("B", "A")):
            assignment = [None] * 4
            assignment[pair[0]], assignment[pair[1]] = pq_order
            assignment[complement[0]], assignment[complement[1]] = ab_order
            factorized_assignments.append(tuple(assignment))

assert len(factorized_assignments) == 24
assert set(factorized_assignments) == set(permutations(ROWS))


# Symbolic audit of the complete all-rank-two orientation census.
u = [[sp.Symbol(f"u{i}{row}") for row in ROWS] for i in range(4)]
unit = {
    P: [sp.Integer(1), 0, 0, 0],
    Q: [0, sp.Integer(1), 0, 0],
}


def binary_coefficient(word: tuple[int, ...], off: frozenset[int]) -> sp.Expr:
    rows = [unit[word[i]] if i in off else u[i] for i in range(4)]
    return permanent(rows)


def nij(i: int, j: int) -> sp.Expr:
    return sp.expand(u[i][A] * u[j][B] + u[i][B] * u[j][A])


lam = permanent(u)
pair_expansion = sp.expand(
    sum(
        u[i][P] * u[j][Q] * nij(*tuple(k for k in range(4) if k not in (i, j)))
        for i in range(4)
        for j in range(4)
        if i != j
    )
)
assert sp.expand(lam - pair_expansion) == 0

all_q = (Q, Q, Q, Q)
all_q_expansion = sum(
    u[i][Q] * binary_coefficient(all_q, frozenset({i})) for i in range(4)
)
assert sp.expand(lam - all_q_expansion) == 0

one_three = (P, Q, Q, Q)
assert binary_coefficient(one_three, frozenset({0, 1})) == nij(2, 3)
assert binary_coefficient(one_three, frozenset({0, 2})) == nij(1, 3)
assert binary_coefficient(one_three, frozenset({0, 3})) == nij(1, 2)

for i, j, k in ((1, 2, 3), (2, 1, 3), (3, 1, 2)):
    expected = u[0][P] * nij(j, k) + u[j][P] * nij(0, k) + u[k][P] * nij(0, j)
    assert sp.expand(binary_coefficient(one_three, frozenset({i})) - expected) == 0

x1, x2, x3 = u[1][P], u[2][P], u[3][P]
one_three_matrix = sp.Matrix([[0, x3, x2], [x3, 0, x1], [x2, x1, 0]])
assert sp.factor(one_three_matrix.det()) == 2 * x1 * x2 * x3

two_two = (P, P, Q, Q)
opposite_pairs = {
    (0, 2): (1, 3),
    (0, 3): (1, 2),
    (1, 2): (0, 3),
    (1, 3): (0, 2),
}
for pair, complement in opposite_pairs.items():
    assert binary_coefficient(two_two, frozenset(pair)) == nij(*complement)

m0 = binary_coefficient(two_two, frozenset({0}))
m2 = binary_coefficient(two_two, frozenset({2}))
assert (
    sp.expand(m0 - (u[1][Q] * nij(2, 3) + u[2][Q] * nij(1, 3) + u[3][Q] * nij(1, 2)))
    == 0
)
assert (
    sp.expand(m2 - (u[0][P] * nij(1, 3) + u[1][P] * nij(0, 3) + u[3][P] * nij(0, 1)))
    == 0
)


# Squarefree-algebra reconstruction of the five displayed mixed-triple products.
aa1, aa2, dd = sp.symbols("a1 a2 d")
bb1, cc1, bb2, cc2, bb3, cc3 = sp.symbols("b1 c1 b2 c2 b3 c3")


def add_poly(*polys: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    result: dict[int, sp.Expr] = {}
    for poly in polys:
        for mask, coefficient in poly.items():
            result[mask] = sp.expand(result.get(mask, 0) + coefficient)
    return {
        mask: coefficient for mask, coefficient in result.items() if coefficient != 0
    }


def mul_poly(left: dict[int, sp.Expr], right: dict[int, sp.Expr]) -> dict[int, sp.Expr]:
    result: dict[int, sp.Expr] = {}
    for mask_left, coefficient_left in left.items():
        for mask_right, coefficient_right in right.items():
            if mask_left & mask_right:
                continue
            mask = mask_left | mask_right
            result[mask] = sp.expand(
                result.get(mask, 0) + coefficient_left * coefficient_right
            )
    return result


def linear_form(*coefficients: sp.Expr) -> dict[int, sp.Expr]:
    return {
        1 << i: coefficient
        for i, coefficient in enumerate(coefficients)
        if coefficient != 0
    }


e_p = linear_form(1, 0, 0, 0)
e_q = linear_form(0, 1, 0, 0)
u1 = linear_form(0, aa1, bb1, cc1)
u2 = linear_form(0, aa2, bb2, cc2)
u3 = linear_form(dd, 0, bb3, cc3)

mixed_products = (
    mul_poly(mul_poly(e_p, e_q), u1),
    mul_poly(mul_poly(e_p, e_q), u2),
    mul_poly(mul_poly(u1, u2), e_q),
    mul_poly(mul_poly(e_p, u2), u3),
    mul_poly(mul_poly(u1, e_p), u3),
)
expected_products = (
    {7: bb1, 11: cc1},
    {7: bb2, 11: cc2},
    {14: bb1 * cc2 + cc1 * bb2},
    {7: aa2 * bb3, 11: aa2 * cc3, 13: bb2 * cc3 + cc2 * bb3},
    {7: aa1 * bb3, 11: aa1 * cc3, 13: bb1 * cc3 + cc1 * bb3},
)
for actual, expected in zip(mixed_products, expected_products, strict=True):
    assert all(
        sp.expand(actual.get(mask, 0) - expected.get(mask, 0)) == 0
        for mask in set(actual) | set(expected)
    )


# Anchor expansion and the three permanent row-symmetry identities.
x = sp.symbols("x1:4")
alpha = sp.symbols("alpha1:4")
beta = sp.symbols("beta1:4")
h_p = []
h_a = []
h_b = []
for i in range(3):
    j, k = tuple(index for index in range(3) if index != i)
    h_p.append(alpha[j] * beta[k] + beta[j] * alpha[k])
    h_a.append(x[j] * beta[k] + beta[j] * x[k])
    h_b.append(x[j] * alpha[k] + alpha[j] * x[k])

k_p4 = permanent([[x[i], alpha[i], beta[i]] for i in range(3)])
assert sp.expand(k_p4 - sum(x[i] * h_p[i] for i in range(3))) == 0
assert sp.expand(k_p4 - sum(alpha[i] * h_a[i] for i in range(3))) == 0
assert sp.expand(k_p4 - sum(beta[i] * h_b[i] for i in range(3))) == 0

p0 = sp.symbols("p00:3")
q0 = sp.symbols("q00:3")
a0 = sp.symbols("a00:3")
b0 = sp.symbols("b00:3")
y = sp.symbols("y1:4")
t = sp.symbols("t1:4", nonzero=True)

anchor_columns = [{"P": p0, "Q": q0, "A": a0, "B": b0}]
for i in range(3):
    anchor_columns.append(
        {
            "P": (x[i], 0),
            "Q": (y[i], t[i]),
            "A": (alpha[i], 0),
            "B": (beta[i], 0),
        }
    )

anchor_tensor = tensor_permanent(anchor_columns)
for output, actual in anchor_tensor.items():
    expected = sp.Integer(0)
    port0_coordinate = output[0]
    if output[1:] == (0, 0, 0):
        expected += q0[port0_coordinate] * k_p4
        expected += sum(
            (
                h_p[i] * p0[port0_coordinate]
                + h_a[i] * a0[port0_coordinate]
                + h_b[i] * b0[port0_coordinate]
            )
            * y[i]
            for i in range(3)
        )
    for i in range(3):
        expected_off = tuple(1 if j == i else 0 for j in range(3))
        if output[1:] == expected_off:
            expected += (
                h_p[i] * p0[port0_coordinate]
                + h_a[i] * a0[port0_coordinate]
                + h_b[i] * b0[port0_coordinate]
            ) * t[i]
    assert sp.expand(actual - expected) == 0


# Fixed-fibre mixed control and its exact three-port q-flat.
s_values = (-2, 1, 1, 1)
binary_columns = []
for coefficient in s_values:
    binary_columns.append(
        {
            "P": (1, 0),
            "Q": (0, 1),
            "A": (coefficient, 0),
            "B": (1, 0),
        }
    )

binary_tensor = tensor_permanent(binary_columns)
assert binary_tensor[(1, 0, 0, 0)] == 6
assert all(
    value == 0 for output, value in binary_tensor.items() if output != (1, 0, 0, 0)
)

flat_q = [sp.symbols(f"q{i}_0 q{i}_1 q{i}_2") for i in range(1, 4)]
flat_columns = [binary_columns[0]]
for i in range(3):
    flat_columns.append(
        {
            "P": (1, 0, 0),
            "Q": flat_q[i],
            "A": (1, 0, 0),
            "B": (1, 0, 0),
        }
    )

flat_tensor = tensor_permanent(flat_columns)
assert flat_tensor[(1, 0, 0, 0)] == 6
assert all(
    value == 0 for output, value in flat_tensor.items() if output != (1, 0, 0, 0)
)

print("factorized_P4_terms: 24")
print("all_rank_two_orientation_types: 3")
print("all_rank_two_labelled_words_covered: 16")
print("one_plus_three_active_minor: 2*x1*x2*x3")
print("mixed_triple_displayed_products: 5")
print("anchor_permanent_identities: 3")
print("fixed_fibre_nonzero_binary_coefficients: 1")
print("q_flat_arbitrary_vectors: 3")
print(
    "PASS: GLS65 permanent extraction and local-rank localization algebra "
    "(audit only; 2233 residual and global conjecture remain unresolved)"
)
