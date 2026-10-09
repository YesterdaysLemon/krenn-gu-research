# Three-column bilinear grid and permanent plane rigidity

## Status

**Proved.**  Theorem 1 holds for every even order `n >= 4` and Theorem 2 for
every even order `n >= 6` (at `n = 4` its hypotheses cannot be met, so it is
vacuous there).  Theorem 1 holds over every commutative ring.  Theorem 2's identity holds over every
commutative ring, and its conclusion holds over every field of characteristic
not two.  Theorem 3 holds over every field of characteristic not two.
Proposition 4 is an identity over `Z`; its conclusion needs `2 != 0`.
A same-day adversarial [review](../../docs/audits/THREE_COLUMN_BILINEAR_GRID_THEOREM_REVIEW_2026-10-08.md)
passed Theorems 2 and 3, Proposition 4, and Corollary 5 (i); it corrected
one false paraphrase of Corollary 5 (ii) in the companion note and several
wordings, recorded below where they occur.  No independent audit and no
Lean formalization exist.

These are conditional implications about the first relation type that the
two-term closure misses (see
[`TWO_TERM_RELATION_CLOSURE_THEOREMS.md`](TWO_TERM_RELATION_CLOSURE_THEOREMS.md)).
Each excludes a witness only under explicit support or coefficient premises.
None is an occurrence theorem, and none closes an order or changes the
frontier.  The verifier replays the displayed identities and the finite
linear-algebra facts; the proofs are the hand arguments below.  There is no
independent audit and no Lean formalization.  The global Krenn–Gu conjecture
remains **UNRESOLVED**.

The six-vertex instances, and the measurement that these are the cheapest
certificates for the 51-entry survivor, are in
[`multilinear-certificate-shape-2026-10-08.md`](../../docs/strategy/multilinear-certificate-shape-2026-10-08.md).

## Setting

There are three colours and an even vertex set `V`, with blocks
`W_ij in F^{3x3}` and `W_ji = W_ij^T`.  For a vertex set `A` and a word `w`,
`T_A(w)` is the sum over perfect matchings `M` of `A` of
`prod_{ij in M} W_ij[w_i, w_j]`.  Here `T_{} = 1` and `T(w) = T_V(w)`.  A
witness has `T = Delta`: `T(w) = 1` on the three constant words and `0` on
every mixed word.  `perm(x, y, z) = sum_{pi in S_3} x_{pi1} y_{pi2} z_{pi3}`
is the permanent of the `3 x 3` matrix with rows `x, y, z`.  A vector in
`F^3` is *full* if none of its coordinates is zero.  `H_u = {x : x_u = 0}`
is a coordinate plane.

## Theorem 1 (two-vertex bilinear expansion)

Let `a != b`, `R = V - {a, b}`, `c` a word on `R`, and `w_{beta gamma}` the
word with `beta` at `a`, `gamma` at `b` and `c` on `R`.  Put
`y_beta[u] = W_au[beta, c_u]`, `z_gamma[v] = W_bv[gamma, c_v]`, and
`H_uv = T_{R - {u, v}}(c)` for distinct `u, v in R`.  Then

```text
T(w_{beta gamma}) = W_ab[beta, gamma] T_R(c) + sum_{u != v in R} y_beta[u] z_gamma[v] H_uv.
```

*Proof.*  Split the perfect matchings by the partner of `a`.  If it is `b`,
the contribution is `W_ab T_R(c)`.  Otherwise `a ~ u` and `b ~ v` with
`u != v` in `R`, and the rest is a perfect matching of `R - {u, v}`.  ∎

So, with the `W_ab` term removed, a two-vertex colour grid is the bilinear
form `y^T H z` of the symmetric zero-diagonal matrix `H` of order-`(n-4)`
complementary coefficients.  Theorem A of the two-term document is the
special case in which the grid has exactly two live matchings, i.e. `H` has
rank two on the live coordinates.  This document treats the hollow rank-three
case.

## Theorem 2 (three-column bilinear grid)

Keep the notation of Theorem 1 and fix `C = {u_1, u_2, u_3} subset R`.
Assume:

1. `H_uv = 0` whenever `{u, v}` is not contained in `C`;
2. `W_ab[beta, gamma] T_R(c) = 0` for the four colour pairs used below.

Write `h_kl = H_{u_k u_l}`, `H_C = [[0, h12, h13], [h12, 0, h23], [h13, h23, 0]]`,
and restrict `y_beta`, `z_gamma` to `C`.  Then `T(w_{beta gamma}) =
y_beta^T H_C z_gamma`.  For colours `beta_1, beta_2` at `a`, `gamma_1,
gamma_2` at `b` and indices `p, q in {1, 2, 3}`, put

```text
Y = [y_beta1  y_beta2  e_p],   Z = [z_gamma1  z_gamma2  e_q],   G = Z^T H_C Y,
```

so that `G_ij = T(w_{beta_j gamma_i})` for `i, j <= 2`.  Then

```text
2 h12 h13 h23 det(Y) det(Z) = g11 G11 + g12 G12 + g21 G21 + g22 G22,
g11 = G22 G33 - G23 G32,   g12 = G23 G31 - G21 G33,
g21 = G13 G32,             g22 = -G13 G31.
```

Consequently, if the four words `w_{beta_j gamma_i}` are mixed, every witness
satisfies `h12 h13 h23 det(Y) det(Z) = 0`.

*Proof.*  By Theorem 1 and hypotheses 1 and 2, only terms with
`u, v in C` survive.  This gives `T = y^T H_C z`, hence `G_ij` for
`i, j <= 2`.  By multiplicativity, `det G = det Z det H_C det Y`, and
`det H_C = 2 h12 h13 h23`.  In the Leibniz expansion of the `3 x 3`
determinant `det G`, rows 1 and 2 cannot both be sent to column 3.  So
every term contains a factor `G_ij` with `i, j <= 2`.  Grouping the six
terms gives the displayed cofactors.  ∎

**Support form.**  `det[y, y', e_p]` is `+-(y_u y'_j - y_j y'_u)` with
`{u, j, p} = {1, 2, 3}`.  It is a single monomial whenever exactly one of
`y_u y'_j`, `y_j y'_u` is supported (a *staircase* pair: for example `y'_u = 0`
while `y_u, y'_j` are supported).  So no witness can satisfy all of the
following at once:

- the three `h_kl` are nonzero;
- both row pairs are staircase pairs;
- the four grid words are mixed;
- hypotheses 1 and 2 hold.

At `n = 6`, `R - {u, v}` is a pair, so each `H_uv` is a single entry and
`T_R(c)` is a three-term four-vertex hafnian.  Every hypothesis is then
support-checkable.  Hypothesis 1 says that `C` is independent at `c`, and
`h_kl != 0` says that the fourth vertex `r = R - C` is joined to all of `C`
at `c`.  Hypothesis 2 is then automatic: every matching of `R` has an edge
inside `C`.  At `n >= 8`, the `H_uv` are recursive coefficients.  The
hypotheses are then literals of the recursive support model (`m`-variables),
and the theorem is a valid clause family at every level `A`, not only at
`A = V`.  As a clause it reads: premises imply that one of the four values
`T_A(w_ij)` is nonzero.

**Degree.**  At `n = 6`, `G_ij` (`i, j <= 2`) has degree 3 in the entries,
`G_i3` and `G_3j` have degree 2, and `G33` is `h_pq` or `0`.  So the
multipliers `g_ij` have degree 4, and the certificate is a monomial of
degree 7 times 2.

## Theorem 3 (permanent plane rigidity)

Let `F` be a field of characteristic not two, and let `V_0, V_1, V_2` be
two-dimensional subspaces of `F^3` with `perm(x, y, z) = 0` for all
`x in V_0`, `y in V_1`, `z in V_2`.  Then `V_0 = V_1 = V_2 = H_u` for some
coordinate `u`.  Conversely, every `H_u` triple has this property.

*Proof.*

- **(a) Full-row lemma.**  `perm(x, y, z) = y^T B_x z` with
  `B_x = [[0, x3, x2], [x3, 0, x1], [x2, x1, 0]]` and
  `det B_x = 2 x1 x2 x3`.  If `x` is full, `B_x` is invertible.  Then
  `perm(x, V_1, V_2) = 0` forces `V_2 subset (B_x V_1)^perp`.  Hence
  `dim V_1 + dim V_2 <= 3`.
- **(b) Full vectors.**  A two-dimensional `V = l^perp` that is not a
  coordinate plane contains a full vector.  If `l` is full, take
  `(1/l1, 1/l2, -2/l3)`; this uses characteristic not two.  If `l` has
  exactly two nonzero coordinates, say `l3 = 0`, take `(1/l1, -1/l2, 1)`.
- **(c) Conclusion.**  By (a) applied to each `V_t` in turn (the form is
  symmetric in its three arguments), no `V_t` contains a full vector.  By
  (b), `V_t = H_{u_t}`.  If the `u_t` are not all equal, some permutation
  `pi` has `pi(t) != u_t` for all `t`.  Then `e_{pi(t)} in V_t` and
  `perm(e_{pi0}, e_{pi1}, e_{pi2}) = 1`, a contradiction.  If all three
  are `H_u`, every term of `perm` uses coordinate `u` of some argument, so
  `perm` vanishes.  ∎

(a) alone is the content of Theorem 2 at `n = 6`.  With `x` the full row of
the third inner vertex, the four grid values are `y^T B_x z`.

## Proposition 4 (degree-three cube identity)

For `Y_0, Y_1, Y_2 in R^{3 x 2}` (`R` any commutative ring), put
`A_ijk = perm(Y_0[:, i], Y_1[:, j], Y_2[:, k])` for `i, j, k in {0, 1}`.
Let `D_I(Y)` be the `2 x 2` minor on the ordered row pair `I`, and

```text
phi(a, b, c) = c_1 (a_1 b_2 + a_2 b_1) - a_1 b_1 c_2.
```

Then

```text
sum_{i,j,k} (-1)^(i+j+k) phi(Y_0[:, 1-i], Y_1[:, 1-j], Y_2[:, 1-k]) A_ijk
    = 2 D_{12}(Y_0) D_{12}(Y_1) D_{13}(Y_2).
```

The same holds after any simultaneous permutation of the coordinates and
any permutation of the three matrices, because `perm` is invariant under
both.  So the product of three minors whose row pairs have exactly two
equal (`I_s = I_t != I_r`) lies in the ideal of the eight cube permanents,
with trilinear multipliers.

The verifier also checks, by exact linear algebra over `Q`, two negative
cases.  If the three row pairs are all equal or pairwise distinct, the
product is **not** in the span of trilinear multiples of the `A_ijk`.  All
27 choices of `(I_0, I_1, I_2)` fall into these three symmetry classes.  The
all-equal product is not even in the radical (`H_u^3` is isotropic).  The
pairwise-distinct product is in the radical by Theorem 3, so a *power* of it
lies in the ideal, but the product itself is not in the span of multiples
of the `A_ijk` of any degree that was tested; the verifier checks the
trilinear degree only.

## Corollary 5 (six-vertex cut form)

Let `n = 6`, `V = T ⊔ U` with `|T| = |U| = 3`, and let `sigma` colour `U`
with `W_uu'[sigma_u, sigma_u'] = 0` for `u != u'` in `U` (`U` independent at
`sigma`).  For `t in T` and a colour `alpha`, put
`r_{t, alpha} = (W_tu[alpha, sigma_u])_{u in U}`.  On the 27 words with `U`
pinned to `sigma`,

```text
T(w) = perm(r_{t1, w_t1}, r_{t2, w_t2}, r_{t3, w_t3}),
```

because every matching that uses a `T`–`T` edge also uses a `U`–`U` edge.
If these words are mixed (for example, if `sigma` is injective), no witness
has a support in which either of the following holds:

- **(i)** some `t` has a full row, and the other two inner vertices each
  have a staircase row pair.  This is Theorem 2 with `{a, b} = T - t`,
  `c = (alpha at t, sigma on U)` and `C = U`; the multiplier degree is 4.
- **(ii)** every `t` has two rows spanning a plane that contains a full
  vector.  This is Theorem 3, a statement about values: no nonzero
  assignment makes all 27 permanents vanish.  It is **not** a unit-ideal
  statement (proportional full rows give a counterexample at the ideal
  level; see the review), and necessity of (i) or (ii) is not proved.  When the three monomial minors can be chosen
  with exactly two equal row pairs, Proposition 4 gives a certificate with
  multiplier degree 3.

## All-order forms and boundaries

- **Theorem 2 is the all-order form.**  Its "cut" is `{a, b}`, a background
  `c` on `R`, and three columns `C subset R` outside which every
  order-`(n-4)` complementary coefficient vanishes.  The six-vertex
  inner/outer triangle is the case `n = 6`, `{a, b} = T - t`,
  `C = U`, `r = t`.
- **`k`-vs-`k` cuts.**  If `n = 2k` and `U` is independent at `sigma`, then
  the slice is `perm_k` of the `k` row families (verifier, `k = 3, 4`).  If
  `k - 3` inner vertices have single-entry rows `lambda e_u` at distinct
  columns, then
  `perm_k(lambda e_{u_4}, ..., y, z, v) = (prod lambda) perm_3(y|_C, z|_C, v|_C)`,
  and Corollary 5 applies to the remaining three columns.
- **The naive `k`-ary extensions are false.**
  - Plane rigidity fails at `k = 2`: `perm_2((1,1), (1,-1)) = 0`.
  - The full-row bound fails at `k = 4`.  For the full vectors
    `x = (1,1,1,1)` and `x' = (1,-4,-4,-1)`, the form
    `B(y, z) = perm_4(x, x', y, z)` is singular.  So `perm_4` vanishes on
    `<x> x <x'> x F^4 x <ker B>`.
  - `det B_{x,x'}` is `-4` times a 12-term polynomial of bidegree `(4, 4)`
    (computed with a scratch SymPy script; not part of the verifier).  The
    monomial determinant `det B_x = 2 x1 x2 x3` is special to `k = 3`, and
    this is what makes the `k = 3` statement support-level.

## Verification

```text
python claims/arbitrary-order/verify_three_column_bilinear_grid_theorem.py              # ~10 s
python claims/finite/n06/verify_51_entry_survivor_bilinear_grid_certificates.py        # ~30 s
```

The first replays:

- Theorem 1 symbolically at `n = 4` (all words), `n = 6` (samples) and
  `n = 8` (samples);
- the certificate identity of Theorem 2 for all `p, q`;
- the ingredients of Theorem 3;
- the closed form of Proposition 4 and its negative cases;
- the `k`-vs-`k` and contraction identities, and the two boundary examples.

The second replays every six-vertex instance against the actual word
polynomials of the supports.  It is a primary verifier only; no independent
audit exists.
