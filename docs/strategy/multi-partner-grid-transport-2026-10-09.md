# Multi-partner grid-rank transport, and why it does not exclude S156 — 2026-10-09

This is a dated research record.  The global Krenn–Gu status is
**UNRESOLVED**, and nothing here changes it.  It proves a general
all-order transport lemma, encodes it as support-level clauses, and tests
it on the eight-vertex support survivor S156.  **S156 is not excluded.**
`docs/current-frontier.md` is updated by the integrator (Section 8).

Evidence labels:

- **[EXACT]**: a hand proof, together with an exact check by the committed
  verifier
  [`verify_s156_multi_partner_grid_transport.py`](../../claims/finite/n08/verify_s156_multi_partner_grid_transport.py)
  where one is stated.  That verifier uses integer arithmetic and sympy.
- **[EXACT-POINT]**: an exact integer computation at one explicit
  configuration `W*` on the S156 support.  `W*` is seeded, with entries in
  `±{1..97}`, and is not a witness.  It is used only to exhibit a
  support-level model.
- **[OBSERVATION]**: a reading or comparison, not a theorem.
- **[NUMERIC-EXPLORATION]**: floating-point; steering only, never evidence.

## 1. Question and inputs

S156 is the 156-entry zero pattern of
[`hyperdeterminant-crossing-2026-10-09.md`](hyperdeterminant-crossing-2026-10-09.md),
Section 3.4.  It has sixteen full `3 x 3` blocks on a 4-regular graph `F`
and twelve single entries on the complementary 3-regular graph `H`.  It
survives every encoded support family:

- column killers;
- the holonomy rules H2 and H3 of
  [`holonomy-support-model-2026-10-08.md`](holonomy-support-model-2026-10-08.md);
- plane rigidity (PR) of
  [`PERMANENT_PLANE_RESTRICTION_HYPERDETERMINANT_THEOREM.md`](../../claims/arbitrary-order/PERMANENT_PLANE_RESTRICTION_HYPERDETERMINANT_THEOREM.md).

The companion note `docs/strategy/n8-support-realizability-2026-10-09.md`
shows that S156 survives these families at every level.  That note is on
the unmerged branch `claude/n8-realizability-20261009`, commit `a77664e1`.
Its Section 5 asked for a multi-partner (`k = 4`) analogue of the `k = 2`
rank-one grid transport H3, which kills S128.

The fixture `pattern_S156.json` was copied read-only into the untracked
`tmp/`.  The verifier embeds the pattern verbatim from Section 3.4 and
asserts its 156 entries.

**Conventions** are those of the model script:

- `W_ij[a,b]` for `i < j`, where `a` is the colour at `i`;
- `T_A(w)` is the matching sum over the perfect matchings of `A`;
- a witness has `T_V = GHZ`, up to the diagonal torus: nonconstant words
  vanish and constant words are nonzero.

**Laplace expansion at a hub `p`.**  For every `A`, `w` and `p`, and for
every configuration,

```text
T_A(w) = sum_{u in A-p} W_pu[w_p, w_u] * T_{A-{p,u}}(w|).            (1)
```

Write `c` for a colouring of `V - p`.  Define the coordinates
`(u, z)`, for `u != p` and `z` a colour, by

```text
Phi_c(u,z) = [c_u = z] * T_{V-{p,u}}(c|)     and     r_x(u,z) = W_pu[x, z].
```

Then (1) says `T(x, c) = r_x . Phi_c`.  This is the flattening of `T` at
`p`: `T^(p) = R_p Phi_p`.

## 2. Lemma 1 (hub flattening)  [EXACT]

**Statement.**  Let `n` be even, let `F` be any field, and let `W` be any
configuration with `T_W = GHZ` up to the torus.  Fix a hub `p` and a set
`A` of colours at `p`.  Let `R_A` be the matrix with rows `r_x`, `x in A`.

1. For every colouring `c` of `V - p` other than the constants `a^{n-1}`
   with `a in A`, we have `R_A Phi_c = 0`.  The three rows `r_0, r_1, r_2`
   are linearly independent.
2. **Matroid form.**  Let `L_A(c)` be the set of coordinates with
   `Phi_c != 0` that are not loops of `R_A`, where a loop is a zero column.
   Then `L_A(c)` is a cyclic set (a union of circuits) of the column matroid
   of `R_A`.  For `|A| = 1` this is exactly the column killer: no live set
   of size one.
3. **Rank form.**  Let `K` be a set of coordinates and `𝒞` a set of
   colourings as in (i).  Suppose that for every `c` in `𝒞`, every
   coordinate outside `K` with `Phi_c != 0` is a loop of `R_A`.  Then

   ```text
   rank R_{A,K} + rank Phi_K(𝒞) <= |K|.
   ```

**Proof.**

- (i) The word `(x, c)` is nonconstant, so `r_x . Phi_c = T(x, c) = 0`.
  For independence, `r_x . Phi_{y^{n-1}} = δ_xy λ_y` with `λ_y != 0`.
- (ii) `sum_{i in L} Phi_c(i) * col_i(R_A) = 0` with every coefficient
  nonzero, and the support of a linear dependency is a union of circuits.
- (iii) `R_{A,K} Phi_K(𝒞) = 0`, and then Sylvester's rank inequality
  applies.

All three statements are pure linear algebra on (1).  They hold for every
witness, at every even order, and over every field.  No genericity enters.

What is **not** forced is the matroid of `R_A` and the zero pattern of
`Phi`.  These depend on the configuration.  A support-level clause can use
only what the zero pattern certifies (Section 4).

## 3. Lemma 2 (multi-partner grid transport)  [EXACT]

### 3.1 The bilinear identity

Let `R` be a commutative ring, `k = r + s` with `r, s >= 1`, and let
`a_0, ..., a_r` and `b_0, ..., b_s` be vectors in `R^k`.  Put
`E_ij = a_i . b_j`.  For an `r`-subset `I` of the coordinates, let:

- `p_I` be the `r x r` minor of `(a_1; ...; a_r)` on the columns `I`;
- `q_{I^c}` be the `s x s` minor of `(b_1; ...; b_s)` on the complementary
  columns.

Then

```text
p_I * q_{I^c} * E_00   lies in the ideal   ( E_ij : (i,j) != (0,0) ).       (2)
```

**Proof.**  Let `Z` be the `k x k` matrix with rows `a_1..a_r` and the unit
rows `e_l` for `l` in `I^c`.  Let `Y` be the matrix with rows `b_1..b_s` and
`e_l` for `l` in `I`.  Then `det Z = ±p_I` and `det Y = ±q_{I^c}`.  From
`adj(Y^T) Y^T = det(Y) * 1` and `adj(Z) Z = det(Z) * 1`, and
`adj(Z Y^T) = adj(Y^T) adj(Z)`:

```text
det Z * det Y * E_00 = (a_0 Y^T) * adj(Z Y^T) * (Z b_0^T).
```

The vector `a_0 Y^T` has entries `E_0j` at the `b` positions and `a_0[I]`
at the `e_I` positions.  The vector `Z b_0^T` has entries `E_i0` at the `a`
positions and `b_0[I^c]` at the `e_{I^c}` positions.  The matrix `Z Y^T`
reduces, modulo the ideal, to

```text
N = [[E', A'_I], [B'_{I^c}^T, 0]],     with E' = (E_ij)_{i,j >= 1}.
```

So only one block of the right side survives modulo the ideal: rows
indexed by the `e_I` columns and columns indexed by the `e_{I^c}` rows of
`adj(N)`.  That block vanishes at `E' = 0`.  Deleting one `e_{I^c}` row and
one `e_I` column of `N|_{E'=0}` leaves the `r` rows `a_1..a_r` supported on
only `r - 1` columns, so every such minor is 0.  ∎

Verifier part A checks two things:

- (2) itself, by solving for multilinear cofactors, for
  `(k, r) = (2,1), (3,1), (3,2), (4,2)` and every `I`;
- the vanishing of the adjugate block for every `1 <= r < k <= 6`.

### 3.2 Witness form

Take a Shape II grid:

- hub `p`;
- varied vertex `v != p`, with colour `y` at `v`;
- colour `x` at `p`;
- a fixed colouring `c` of `V - {p, v}`;
- `E(x, y) = T(w_xy)`.

For a partner set `K`, a subset of `V - {p, v}` with `|K| = k`, put

```text
E_K(x,y) = sum_{u in K} a_u(x) b_u(y),   a_u(x) = W_pu[x, c_u],   b_u(y) = T_{V-{p,u}}(w_xy|).
```

Choose rows `X'` (`|X'| = r`), columns `Y'` (`|Y'| = s`), and a corner
`(x0, y0)` outside them.  The **premise** has three parts:

- every word of the subgrid `(X' + x0) x (Y' + y0)` is nonconstant;
- at every corner other than `(x0, y0)`, every live term of (1) at `p`
  belongs to `K`;
- at `(x0, y0)`, the live terms outside `K` sum to `σ`.

Then `E = E_K = 0` at those corners, and `E_K(x0,y0) = -σ`.  By (2):

```text
p_I * q_{I^c} * σ = 0      for every r-subset I of K.                      (3)
```

If exactly one term outside `K` is live at `(x0, y0)`, then `σ != 0`, and
**every** product `p_I q_{I^c}` vanishes.

The same identity applies to any grid in which each term of `K` factors as
`f(x) g(y)`.  This includes the Shape I grids of H3, where one factor of a
term depends on `y` and the other on `x`.

### 3.3 Recovery of H3 and of the S128 identity

Take `k = 2` and `r = s = 1`.  Then `p_I = a_{k1}(x1)` and
`q_{I^c} = b_{k2}(y1)`.  If both terms are live at the corner `(x1, y1)`,
these are nonzero, so (3) transports the cancellation to the corner
`(x0, y0)`.  This is the square rule of H3 (Lemma B′ of the holonomy note),
and iterating squares gives its path closure.

The S128 identity of the realizability note,

```text
p1*Y0*Z = p1*Y0*E01 - p0*Y0*E11 + p0*Y1*E10 - p1*Y1*E00,
```

is the instance `p = 0`, `v = 2`, `K = {5, 7}`, `(x0, y0) = (0, 1)`,
`X' = {1}`, `Y' = {0}`, with `σ = Z`.  The verifier's census (part D1)
finds exactly this instance on S128.

### 3.4 Support-level clause family and soundness

**Grid clause G(r, s).**  Its literals are:

- the `g`/`m` literals stating the premise of 3.2, with exactly one live
  term outside `K` at `(x0, y0)`;
- for some `I`, an `r x r` submatrix of `(W_pu[x, c_u])_{x in X', u in I}`
  whose support pattern has exactly one transversal;
- an `s x s` submatrix of `(T_{V-{p,u}}(w_{x y}))_{y in Y', u in I^c}`
  whose `m`-pattern has exactly one transversal.

The clause forbids this conjunction.

**Soundness.**  At any configuration whose zero pattern satisfies the
conjunction, `σ` is a single nonzero term.  A minor whose pattern has one
transversal equals plus or minus a product of nonzero numbers.  So (3) is
violated.

The rank hypotheses of Lemma 2 are certified **only** this way.  A minor
with two or more supported transversals is a polynomial with at least two
terms.  The zero pattern cannot certify that it is nonzero, so such
instances need genericity and are not clauses.

**Hub clause M(p, A).**  For every `c`, `L_A(c)` must be cyclic in some
matroid realizable by a matrix with the support of `R_A`.  Soundness is
Lemma 1 (ii).

H3, the killers, and the S128 certificate are all instances:

- H3 is G(1,1) with liveness supplying both `1 x 1` minors;
- the killers are M with `|A| = 1`.

## 4. Test on S156

### 4.1 Support facts  [EXACT]

From verifier part B:

- `F` is 4-regular, with 16 full blocks; `H` has 12 single entries.
- For **every** pair `{p, u}`, `F[V - {p,u}]` has at least **two** perfect
  matchings (the minimum, 2, is attained).
- Hence every Laplace coefficient `T_{V-{p,u}}(c)` is a nonzero polynomial
  with at least two monomials, for every colouring `c`.
- The rows of `p` meeting only full blocks are:
  - vertex 0, colour 2;
  - vertex 1, colour 0;
  - vertex 2, colours 0 and 1;
  - vertex 3, colour 2;
  - vertex 4, colours 0 and 2;
  - vertex 6, colour 1;
  - vertex 7, colour 2.

### 4.2 The hub clause is silent  [EXACT-POINT]

At `W*`, part C of the verifier takes every hub `p`, every row set `A`,
and every admissible `c`: 122,376 instances.  For each, it computes:

- the live coordinates `L_A(c)`, with `Phi_c` evaluated exactly at `W*`;
- the exact ranks of the columns of `R_A(W*)`.

Every `L_A(c)` is cyclic, and every one has at least four elements.  Each
contains the four `F` coordinates `(u, c_u)`, `u in F(p)`.  These are four
points with full support in `P^{|A|-1}` with `|A| <= 3`, so they span the
space, and they form a circuit for a generic choice.

So the following support-level model satisfies M at every hub, every row
set and every colouring:

- `g = S156`;
- `m` equal to the zero pattern of `W*` at levels 4 and 6;
- `m_V = GHZ`;
- the matroids of `W*`.

**The same model satisfies every previously encoded family.**  The
independent checkers `check_model` ((L), (F'), (G)), `check_holonomy` (H2
and H3 at every level) and `check_plane` (PR at every level) of
`explore_general_block_recursive_support_model.py` were run on it (bounded
run `k4g-a7-checkers`, 22 s).  They reported 0 violations.

- H3 found only 16 grid edges, and nothing was transported.
- No PR premise held.  The failure census was 2,265,680 instances with a
  live outside summand and 1,395,040 with `h` dead, identical to the census
  of the earlier SAT run.

So killers, H2, H3, PR, M and G together **do not exclude S156**.  This is
an explicit model, not a solver run [EXACT-POINT].

### 4.3 The grid clause is silent  [EXACT-POINT]

Part D runs a census of every Shape II subgrid, with `r, s` in `{1, 2}`,
under the Laplace supports of `W*`:

| pattern | (r, s) | premise instances | clause fires |
|---|---|---|---|
| S128 | (1,1) | 3,386 | 3,386 |
| S128 | (1,2) | 4,910 | 367 |
| S128 | (2,1) | 2,575 | 1,179 |
| S128 | (2,2) | 5,839 | 598 |
| S156 | (2,2) | 7,751 | **0** |

On S128 the family fires, including the S128 identity instance.  It also
fires at `k = 3` and `k = 4`.  So on sparse patterns it is strictly
stronger than H3 [OBSERVATION; S128 was already excluded].

On S156, every premise instance has `k = 4`, `K = F(p)`, `v` an
`H`-neighbour of `p`, and `σ` the single `W_pv` term.  `|K| <= 3` never
occurs, because the four `F` partners are always live.  The hypotheses
needed are `2 x 2` minors:

- of two hub rows on the four full `F` blocks at fixed colours (always two
  supported transversals);
- of two Laplace-coefficient vectors (two nonzero coefficients per row,
  hence two transversals).

So **no instance is support-certified**, and the clause never fires.

### 4.4 What Lemma 2 still forces on S156 (conditional)  [EXACT]

At each of the 7,751 instances, the instance's `m` literals may hold at a
witness; they hold for the generic zero pattern.  If they do, (3) gives
`p_I q_{I^c} = 0` for all six `I`.  Equivalently, one of two things
holds:

- the two hub rows `X' = [3] - x0` are parallel on `F(p)` at the colours
  `c`;
- the two coefficient vectors `(T_{V-{p,u}}(w_{x y}))_{u in F(p)}`,
  `y in Y'`, are parallel, or the minors vanish in a mixed pattern.

These are binomial conditions, not zero-pattern conditions.

### 4.5 An unconditional trichotomy at every hub  [EXACT]

Fix a hub `p`, put `K = F(p)`, and let `γ` be a colouring of `K`.  Define
`C_γ` as the set of colourings `c` of `V - p` that:

- extend `γ`;
- avoid, at every `H`-neighbour `h` of `p`, the colour `z_h` that the
  single entry `W_ph` uses at `h`;
- are nonconstant.

For such `c`, every block `W_ph` vanishes on the column `c_h`.  This holds
**by support alone**, with no `m` literal.  Lemma 1 (iii), with `A = [3]`,
then gives

```text
rank R_K(γ) + rank Phi_K(C_γ) <= 4,    R_K(γ) = (W_pu[x, γ_u])_{x in [3], u in K}.     (4)
```

`|C_γ| <= 8`, since `p` has three `H`-neighbours.  At hub 2, `C_γ` is the
box `c_0 in {1,2}`, `c_4 in {0,2}`, `c_5 in {0,1}`: eight colourings, none
constant.

**Selection lemma.**  Let `G_1..G_4` be four sets of nonzero vectors in
`F^3` whose union spans `F^3`, and suppose no three of the `G_i` lie in a
common line.  Then some choice `g_i in G_i` has rank 3.

*Proof.*

1. Some `g_i in G_i` and `g_j in G_j`, with `i != j`, are non-parallel.
   Otherwise all vectors lie in one line.  Put `π = span(g_i, g_j)`.
2. If one of the other two groups meets the complement of `π`, we are done.
   So assume `G_k, G_l ⊂ π`.  Some `x in G_i ∪ G_j` lies outside `π`;
   without loss of generality `x in G_i`.
3. If `G_k ∪ G_l` contains two non-parallel vectors from different groups,
   they span `π`, and together with `x` they have rank 3.
4. Otherwise `G_k ∪ G_l` lies in a line `ℓ ⊂ π`.
   - If `g_j` is not on `ℓ`, then `{x, g_j, g_k}` has rank 3.
   - If `g_j` is on `ℓ`, then some `y in G_j` is off `ℓ` (no three groups
     lie in `ℓ`).  Put `σ = span(y, g_k)`.  If `g_i` were in `σ`, then
     `σ = span(g_i, g_k) = π`, which does not contain `x`.  So `g_i` or `x`
     lies outside `σ` and completes a rank-3 choice.  ∎

**Proposition (hub trichotomy).**  Take any configuration supported within
S156 that has `T = GHZ`, and any hub `p`.  At least one of the following
holds.

- **(a)** The `F`-part of the rows of `p` (a `3 x 12` matrix) has rank at
  most 2.
  - Then some `H`-neighbour `h0` has `T_{V-{p,h0}}(c) = 0` for every
    nonconstant `c` with `c_{h0} = z_{h0}` and `c_h != z_h` for the other
    `H`-neighbours.  That is a box of 324 colourings, minus constants (323
    at hub 2).
  - *Proof.* Take a left kernel vector `ℓ` of the `F`-part.  Then
    `sum_x ℓ_x T(x,c)` is a sum over `H`-neighbours `h` of
    `ℓ_{x_h} W_ph[x_h, z_h] [c_h = z_h] T_{V-{p,h}}(c)`.  If every
    `ℓ_{x_h}` were 0, the rows would be dependent, contradicting Lemma 1
    (i).  The left side is 0 for nonconstant `c`.
- **(b)** Three `F` blocks at `p` are rank one with a common column vector
  `P`, but (a) fails.
  - Then the fourth `F`-neighbour `u4` and some colour `z` have
    `T_{V-{p,u4}}(c) = 0` for every nonconstant `c` with `c_{u4} = z` and
    every `H`-neighbour dead.  That is a box of 216 colourings, minus
    constants.
  - *Proof.* Take `ℓ ⊥ P` with
    `μ(z) = sum_x ℓ_x W_pu4[x, z] != 0`.  If no such `ℓ` existed, all
    twelve columns would lie in `span(P)`, which is case (a).
- **(c)** Otherwise, by the selection lemma, some `γ` has
  `rank R_K(γ) = 3`.  Then, by (4), the up to eight vectors
  `Phi_K(c) in F^4`, `c in C_γ`, are pairwise parallel.  All of them are
  multiples of the cofactor vector `κ(γ)` (the signed `3 x 3` minors of
  `R_K(γ)`).

Neither (a) nor (b) can be refuted at the support level.  Every
coefficient involved has at least two monomials (4.1), so no box
coefficient is a certified nonzero monomial.  An exhaustive scan of all 24
boxes of (a) and the 96 boxes of (b) confirms this; it is a scratch run
that rests on the matching count of 4.1.

### 4.6 Numerical steering  [NUMERIC-EXPLORATION, not evidence]

A Levenberg–Marquardt / TRF least-squares run (scratch, analytic Jacobian,
3 starts, 300 evaluations each) worked on the hub-2 family alone: the 1,944
words `(x, c)` with `c` in some `C_γ`.  It did **not** converge.  The word
residual stayed near `2.4e-3` to `3.6e-3`, with entries drifting toward 0
(`log|W|` down to −5.9).  This says nothing either way.  An earlier
finite-difference run hit its 900 s cap with no output.

## 5. Why the lemma does not fire on S156, and the sharper target

**Precise failing hypothesis.**  Lemma 2 needs the rank hypotheses
`p_I != 0` and `q_{I^c} != 0`.  Lemma 1 needs a live set that is not
automatically cyclic.  On S156 the following hold:

- every hub row pair on `F(p)` is a full-support `2 x 4` matrix, so all its
  minors are binomials;
- every Laplace coefficient attached to an `F` edge has at least two
  monomials (4.1);
- every live set contains the four full `F` coordinates.

The rank hypotheses are therefore genuinely non-support conditions.
Lemma 2 does reach 7,751 premise instances, but at each one the rank drop
it demands can be met by a binomial cancellation that the zero pattern
cannot see.  The obstruction, if there is one, lies in the equations, not
in the zero pattern.

**Sharper target (one statement).**  Exclude the trichotomy at a single
hub.  Hub 2 is the natural choice, because its rows 0 and 1 are `F`-only.
The **parallel-fan exclusion** asks: for no colouring `γ` of
`{1, 3, 6, 7}` with `rank R_{F(2)}(γ) = 3` can the eight vectors

```text
( T_{V-{2,u}}(γ, δ) )_{u in {1,3,6,7}},    δ in {1,2} x {0,2} x {0,1}  (colours of 0, 4, 5),
```

all be multiples of the cofactor vector `κ(γ)`.  This is a determinantal
condition on the seven-vertex configuration `W|_{V-2}` alone, because the
entries at vertex 2 enter only through `κ(γ)`.

Proving it, together with ruling out the two six-vertex box-vanishing
degenerations (a) and (b) at hub 2, would exclude S156 exactly.  Two
caveats:

- because of 4.1, all three parts must use the equations, not supports;
- the six-vertex box statements are the smaller, more tractable pieces.

## 6. Status and scope

- **Lemma 1, Lemma 2 and identity (2)**: proved over every field (Lemma 2
  over every commutative ring), at every even order, for every
  configuration.  They are new support-model clause families G(r, s) and
  M(p, A), with the soundness proofs above.
  - H3 (k = 2) and the killers (|A| = 1) are special cases.
  - No independent audit, no Lean.
  - As statements about witnesses they are consequences of (1) and the
    GHZ target, by construction.  Their value is as zero-pattern clauses.
    The `k = 3, 4` instances that fire on S128 are not H3 instances.
    Whether killers, H2, H3 and PR together already imply them was not
    examined.
- **S156**: **not excluded**, and not shown realizable.
  - The new clauses are satisfiable on S156, by an explicit support-level
    model at `W*`.
  - The proposition of 4.5 is an exact necessary condition on any S156
    witness.  It is not a contradiction.
- **S128**: already excluded by the realizability note.  The census only
  re-finds that obstruction, plus `k = 3, 4` instances.
- The `n = 8` support model remains a relaxation.  Nothing here is about
  unrestricted `n = 8` configurations.

## 7. Commands and runs

The committed check (83 s in the bounded run):

```text
python claims/finite/n08/verify_s156_multi_partner_grid_transport.py
```

Scratch scripts are in the session scratchpad and are not committed.
Bounded run ids, all under `tools/research/run_bounded.py`:

- `k4g-a1-hubmatroid` (11 s);
- `k4g-a2-gridcensus` (6 s);
- `k4g-a3-identity` (9 s);
- `k4g-a4-num-hub2` (timed out at 900 s, no output);
- `k4g-a5-cases` (box scan, under 1 s);
- `k4g-a6-num-hub2` (232 s);
- `k4g-a7-checkers` (22 s);
- `k4g-verifier-1` (83 s) and `k4g-verifier-2` (the final committed
  version).

No process was left running.

## 8. Frontier

**No new node or edge.**  The integrator added one refuted-route row (sound
support-level clause families do not exclude S156) and extended the `SL6`
boundary row with the lemmas and the hub-2 target, because the frontier
previously recorded S156 only as a survivor of three named families.

- No theorem about witnesses changes, no branch closes, and no reduction
  edge is added to the live proof topology.
- Lemmas 1 and 2 are new support-model clause families.  They are proved,
  but they exclude no pattern not already excluded.
- S156 stays an open support survivor of the `n = 8` relaxation.
- The parent obligation that S156 sits under is unchanged.
