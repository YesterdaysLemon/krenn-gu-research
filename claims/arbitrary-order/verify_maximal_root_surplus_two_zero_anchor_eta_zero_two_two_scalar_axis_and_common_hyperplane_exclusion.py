"""Primary exact checks for GLS66 (audit only; not the written proof)."""

import sympy as sp

SOURCE_DIM = 4
PAIRS = tuple((i, j) for i in range(SOURCE_DIM) for j in range(i + 1, SOURCE_DIM))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}


def squarefree_product(u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    """Multiply two source-linear rows in the squarefree Frobenius algebra."""
    return sp.Matrix([u[i] * v[j] + u[j] * v[i] for i, j in PAIRS])


def complement_matrix() -> sp.Matrix:
    matrix = sp.zeros(len(PAIRS))
    full = set(range(SOURCE_DIM))
    for pair, index in PAIR_INDEX.items():
        complement = tuple(sorted(full - set(pair)))
        matrix[index, PAIR_INDEX[complement]] = 1
    return matrix


def pair(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return sp.expand((left.T * COMPLEMENT * right)[0])


# GLS64 scalar-axis normal form.
ar, lam, x, y = sp.symbols("ar lam x y", nonzero=True)
av = lam * ar
w_st, w_rv = sp.symbols("w_st w_rv")
w_sr = x
w_tr = y
w_sv = -lam * x
w_tv = -lam * y

cofactor_t = sp.expand(ar * w_tv + av * w_tr)
cofactor_s = sp.expand(ar * w_sv + av * w_sr)
matching = sp.expand(w_st * w_rv + w_sr * w_tv + w_sv * w_tr)

assert cofactor_t == 0
assert cofactor_s == 0
assert sp.expand(matching.subs(w_st, 0) + 2 * lam * x * y) == 0


# Common-hyperplane squarefree algebra. Coordinates are P,Q,A,B.
tau = sp.Symbol("tau", nonzero=True)
P = sp.Matrix([1, 0, 0, 0])
Q = sp.Matrix([0, 1, 0, 0])
A = sp.Matrix([0, 0, 1, 0])
B = sp.Matrix([0, 0, 0, 1])
R0 = P - tau * B
S0 = P + tau * B
U = (Q, A, R0)
COMPLEMENT = complement_matrix()

uu_generators = (
    squarefree_product(Q, A),
    squarefree_product(Q, R0),
    squarefree_product(A, R0),
    squarefree_product(R0, R0),
)
uu_matrix = sp.Matrix.hstack(*uu_generators)
assert uu_matrix.rank() == 4

annihilator_generators = (squarefree_product(Q, S0), squarefree_product(A, S0))
annihilator_matrix = sp.Matrix.hstack(*annihilator_generators)
assert annihilator_matrix.rank() == 2
assert uu_matrix.T * COMPLEMENT * annihilator_matrix == sp.zeros(4, 2)

# Both X-oriented silent rows reduce modulo the annihilator to S0^2.
alpha_s, beta_s, alpha_t, beta_t = sp.symbols(
    "alpha_s beta_s alpha_t beta_t", nonzero=True
)
u_s = alpha_s * S0 + beta_s * Q
u_t = alpha_t * S0 + beta_t * Q
silent_product = squarefree_product(u_s, u_t)
remainder = sp.expand(
    silent_product
    - (alpha_s * beta_t + beta_s * alpha_t) * annihilator_generators[0]
    - alpha_s * alpha_t * squarefree_product(S0, S0)
)
assert remainder == sp.zeros(6, 1)

PB = squarefree_product(P, B)
target_slice = sp.Matrix(
    [[pair(squarefree_product(left, right), PB) for right in U] for left in U]
)
assert target_slice == sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
assert target_slice.rank() == 2

# At tau=0 the common pair image is its own totally isotropic annihilator.
U0 = (P, Q, A)
uu0 = sp.Matrix.hstack(
    squarefree_product(P, Q), squarefree_product(P, A), squarefree_product(Q, A)
)
assert uu0.rank() == 3
assert uu0.T * COMPLEMENT * uu0 == sp.zeros(3)

print("scalar_axis_cofactors: 2")
print("scalar_axis_matching_identity: H=-2*lambda*w_sr*w_tr")
print(f"degree_two_basis_size: {len(PAIRS)}")
print(f"common_hyperplane_pair_image_rank: {uu_matrix.rank()}")
print(f"common_hyperplane_annihilator_rank: {annihilator_matrix.rank()}")
print(f"nonzero_tau_target_slice_rank: {target_slice.rank()}")
print("zero_tau_pair_image_totally_isotropic: true")
print(
    "PASS: GLS66 scalar-axis and common-hyperplane displayed algebra "
    "(audit only; global Krenn-Gu conjecture remains unresolved)"
)
