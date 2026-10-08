# Parent C attempt — non-coordinate killer exclusion — 2026-10-08

## Status

This is a research note, not a theorem package, frontier entry, or change of
mathematical status.  The global Krenn–Gu conjecture remains **UNRESOLVED**.
**Parent C is not proved and not refuted here.**  Evidence mode for everything
below: hand proof in characteristic zero, `d = 3`, no verifier, no independent
audit, no Lean counterpart.  The only computation was a symbolic check of the
2x2 linear algebra in §4.  No claim here is a computational certificate.

`docs/current-frontier.md` is deliberately not edited: no live-frontier node
changes status.  The results in §3 and §4 are local necessary conditions on
a hypothetical witness (reductions of the question, not exclusions).

## 1. The obligation, and a well-posedness correction

Parent C of [`fibre-exact-targets-2026-09-01.md`](fibre-exact-targets-2026-09-01.md):
in every `d = 3` witness (`T_W = Delta_n`, even `n >= 6`) every column-killer
block `W_vu = w e_c^T` (`w != 0`) has `w` proportional to `e_c`.

Vocabulary used below.  A killer `W_vu = w e_c^T` is

- *monochromatic* if `w ∝ e_c`;
- a *bridge* if `w ∝ e_a`, `a != c`;
- *mixed* if `w` has at least two nonzero entries.

"Bad" means not monochromatic.  Parent C says no bad killer exists.

**Correction (well-posedness).**  The literal statement quantifies over
*every* killer block, but a vertex may have several colour-`c` killers.  The
local killer-flag theorem (§2) only forces `e_c ∈ span(A_k)` for the column-`c`
vectors of a flag of incident blocks.  Two colour-`c` killers `w_1 e_c^T`,
`w_2 e_c^T` with `w_1, w_2` both mixed and `e_c ∈ span(w_1, w_2)` satisfy
that flag condition with no monochromatic block at all.  I did not exclude
such a vertex, and I do not claim it can occur; I claim only that no
*local* theorem recorded so far excludes it.  So the honest proof target is
one of two statements, and they are not equivalent:

- (C-lit) every killer is monochromatic (the brief's proposition);
- (C-span) for each `(v,c)` the killer vectors of colour `c` at `v` span a
  space containing `e_c`.

When a vertex has exactly one colour-`c` killer the two coincide.

## 2. What is already known (pointers)

- Column-killer theorem: [`THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md`](../../claims/arbitrary-order/THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md).
- Singleton word equations (used in the brief for degree 3).  In compact form,
  for every `v`:

  ```text
  sum_u W_vu D_vu = I_3,    D_vu = diag(tau^0_vu, tau^1_vu, tau^2_vu),
  tau^c_vu = haf(L^c[V - v - u]),   L^c_ij = W_ij[c,c].          (S)
  ```

  Column `c` of (S) is `sum_u tau^c_vu W_vu[:,c] = e_c`.
- Diagonal-anchor refinement and the killer-flag (failure-hyperplane backup)
  theorem, `docs/research-notes.md`, sections "Failure-hyperplane backup
  theorem" and "Diagonal-anchor refinement".  For `(v,c)` there is a flag of
  at most three incident edges `E_1,...,E_k` with `b_i = E_i[:,c]`,
  `A_i = span(b_1..b_i)`, `b_i ∉ A_{i-1}`, `E_i[:,j] ∈ A_{i-1}` (`j != c`),
  and `e_c ∈ A_k`.  Anchor/killer incidence: an anchor of colour `c` is
  either the colour-`c` killer or lies outside `{K_0,K_1,K_2}`.
- [`DOUBLE_STAR_ANNIHILATION_LEMMA.md`](../../claims/arbitrary-order/DOUBLE_STAR_ANNIHILATION_LEMMA.md),
  section "Consequence for a non-coordinate killer": every non-coordinate
  killer has two double-star witnesses, each backup-shaped at the tail or with
  a two-column rank defect at the head.  Its "Global all-bridge boundary"
  shows that if, for one colour, every vertex has a non-coordinate primary
  killer and every edge restricts to a coordinate product on the failure
  planes, the only surviving normal form is the balanced `alpha/beta`
  partition, which is not excluded in general (only in the regimes covered by
  the all-bridge theorem family).
- All-bridge branch: the bridge subcase of Parent C is the "three off-diagonal
  singleton killers per vertex" normal form of the all-bridge lane
  (`A1`-`A3`; `ALL_BRIDGE_ACTIVE_DECK_*`, `*_BALANCED_ALL_BRIDGE_SET_TREE_*`),
  which is excluded for 4-regular supports, `Delta(D) <= 4`, and several
  finite orders, but not in general.  Parent C would imply the all-bridge
  branch is empty; conversely the all-bridge theorems are partial evidence
  for it.
- Degree 3: every killer is monochromatic (singleton equations, brief).
  Degree 4: at least one killer is monochromatic (brief).  §3 recovers and
  refines both.
- Task statement (not located in the repository by me): at the support level
  (zero patterns, Laplace accessibility, singleton noncancellation, GHZ zero
  pattern, killers) a non-coordinate killer is consistent at `n = 6`.  I take
  this as given; it is why every mechanism below must consult weights.

## 3. New local results (hand-proved, scope: `d = 3`, exact, fibre-exact)

Throughout, `B_u = W_vu` for `u ∈ N(v)`, and `H_u(x)` denotes the
contraction of `T_{W - v - u}` against the vectors `x_y`, `y ∈ V - v - u`.
Identity V (contract everything except `v`): `sum_u B_u x_u H_u = g`, with
`g_b = prod_{y != v} x_y[b]`.

### Lemma M (three backups for a mixed killer)

Let `W_vu = w e_c^T` with `w` mixed.  Then for **each** colour `beta` in
`{0,1,2}` there is a neighbour `y_beta != u` with

```text
B_{y_beta}[:,j] ∈ span(w)   for j != beta,        B_{y_beta}[:,beta] ∉ span(w).
```

The three `y_beta` are distinct (so `deg(v) >= 4`), and a colour-`b` killer
can serve only as `y_b`, and only if its vector is not parallel to `w`.

*Proof.*  Let `D'` be the full-support points of the plane `w^⊥`; it is a
nonempty open subset of `w^⊥` because `w` is not a multiple of any `e_b`.
For `x ∈ D'` put `a_y = x^T B_y` and restrict each `x_y` to `ker a_y`
(all of `C^3` if `a_y = 0`; this includes `y = u`, since `x·w = 0`).  Every
matching pairs `v` with some `y`, so `H_W` vanishes on the product, hence
`sum_b x[b] prod_y z_y[b] = 0` there.  Absorb `x[b] != 0` into one factor and
apply the hyperplane-annihilation theorem: for every `beta` some `y` has
`ker a_y ⊂ {z[beta]=0}`, i.e. `x^T B_y ∈ C^× e_beta^T`, and `y != u`.
Cover `D'` by the constructible sets `C_y = (D' ∩ L_y) \ M_y`,
`L_y = {x: x^T B_y[:,j] = 0, j != beta}`, `M_y = {x: x^T B_y[:,beta] = 0}`.
Since `D'` is irreducible, some `L_y ⊇ D'`; the `y` with `L_y ⊇ D'` and
`M_y ⊇ D'` have `C_y = ∅`, and the remaining `y` have `D' ∩ L_y` proper, so
they cannot cover `D'`.  Hence some `y` has `L_y ⊇ D'` and `M_y ⊉ D'`,
which is the displayed condition.  Distinctness: two colours would force all
columns into `span(w)`.  A colour-`b` killer `m e_b^T` has columns `j != b`
equal to zero, so it satisfies the condition exactly for `beta = b` with
`m ∉ span(w)`.  ∎

This is the per-colour strengthening of the recorded flag theorem (which treats
only `beta = c`).  It is stated for mixed killers; for bridge killers the
plane `w^⊥` lies in a coordinate hyperplane, full-support points do not
exist, and the two-term degeneration of the hyperplane theorem intervenes.
The recorded flag theorem treats `beta = c` there; I did not extend Lemma M
to bridges.

**Corollary 1 (degree 3).**  A vertex of degree 3 has no mixed killer.  (With
the singleton equations, bridges are also excluded; this is the brief's
degree-3 statement.)

### Proposition D4 (degree four, no bridge killers)

Let `deg(v) = 4`, `N(v) = {K_c, K_d, K_e, s}` with `K_b` a colour-`b` killer
`w^b e_b^T`, and assume no killer at `v` is a bridge.  Let "bad colours" be
those with `w^b` mixed.

1. At most two colours are bad.
2. If `c` is bad, `K_b` backs up `c` only at `beta = b` and requires
   `w^b ∦ w^c`, and `s` is the colour-`c` backup:
   `s[:,j] ∈ span(w^c)` for `j != c`, `s[:,c] ∉ span(w^c)`.
3. Two bad colours `c, d` (third colour `e`): `w^c ∦ w^d`, `s[:,e] = 0` and
   `s = rho w^d e_c^T + sigma w^c e_d^T`, `rho sigma != 0`; `K_e = lambda e_e e_e^T`
   is monochromatic; and the singleton equations force

   ```text
   w^c = (beta e_c - alpha' e_d)/Delta,   w^d = (alpha e_d - beta' e_c)/Delta,
   alpha = tau^c_{vK_c}, beta = tau^d_{vK_d}, alpha' = rho tau^c_{vs},
   beta' = sigma tau^d_{vs}, Delta = alpha beta - alpha' beta' != 0.
   ```
4. Exactly one bad colour `c`: `K_d = lambda_d e_d e_d^T`,
   `K_e = lambda_e e_e e_e^T`, `w^c ∦ e_d, e_e`, the singleton equations give
   `tau^d_{vK_d} lambda_d = 1 = tau^e_{vK_e} lambda_e`, and
   `tau^d_{vs} s[:,d] = 0 = tau^e_{vs} s[:,e]`.

*Proof sketch.*  Lemma M applied to each bad killer, with the observation that
the only neighbours other than the killer are the two other killers and
`s`.  If all three were bad, `s[:,j] ∈ ∩_{k != j} span(w^k)`, an intersection
of two non-parallel lines, so `s = 0`.  Items 3 and 4 are linear algebra in
the singleton equations (S) at `(v,c)`, `(v,d)`, `(v,e)`; the 2x2 solve was
checked symbolically.  ∎

This recovers "at least one killer is monochromatic" at degree four and shows
the two residual degree-four branches are exactly 3 (two bad) and 4 (one bad).

### Proposition K (killer of a killer, degree four at the partner)

Let `W_vu = w e_c^T` with `w` mixed, so `W_uv = e_c w^T` has a single
nonzero row.  Then `v` is neither a killer nor an anchor of `u` at any
colour, and `u` needs three killers elsewhere, so `deg(u) >= 4`.  If
`deg(u) = 4` and `u` has no bridge killers, then every killer of `u` is
monochromatic and `tau^b_{uv} = haf(L^b[V-u-v]) = 0` for every `b != c` with
`w_b != 0`.

*Proof.*  `N(u) = {v} ∪ {K'_0,K'_1,K'_2}`, so `v` plays the role of `s` in
Proposition D4 for `u`.  Two or three bad colours at `u` force `W_uv` to have
rank 2 or to vanish, but it has rank 1.  One bad colour `c''` forces
`(W_uv)[:,j] = w_j e_c ∈ span(w')` for `j != c''`, and `e_c ∉ span(w')`
(column `c''` is nonzero and outside `span(w')`), so `w_j = 0` for `j != c''`
and `w ∝ e_{c''}`, contradicting mixedness.  With all killers at `u`
monochromatic, column `b` of (S) at `u` reads
`(tau^b_{uK'_b} lambda'_b - 1) e_b + tau^b_{uv} w_b e_c = 0`, which for
`b != c` gives the displayed vanishing.  ∎

### Reciprocity reformulation

For a killer `W_vu = w e_c^T`, `W_uv = e_c w^T`, so
`W_uv[c,:] = w^T` and all other rows vanish.  Hence

```text
w ∝ e_c   <=>   v is a row-c anchor of u.
```

Parent C (C-lit, for one-killer colours) is therefore equivalent to a
*reciprocity* statement: the killer pair `(v,u)` is also an anchor pair.  The
anchor at `(u,c)` exists (diagonal-anchor refinement) but a priori is some
other neighbour; the content of Parent C is that it can be taken to be `v`.

## 4. The simplest surviving local configuration (mechanism iv)

Take the degree-four two-bad branch (item 3 of D4).  It is the simplest
configuration the local theorems leave open.  The exact equations that
Identity V imposes, beyond the ones used above, are (components of
`sum_u B_u x_u H_u = g`):

- `e`-component: `lambda x_{K_e}[e] H_{K_e} = prod_{y != v} x_y[e]`, i.e.
  **`T_{W - v - K_e} = lambda^{-1} e_e^{⊗(n-2)}`**: the induced subgraph on
  `V - {v, K_e}` has a pure single-word tensor.
- `(c,d)`-plane: with `P = x_{K_c}[c] H_{K_c} + sigma x_s[d] H_s` and
  `Q = x_{K_d}[d] H_{K_d} + rho x_s[c] H_s`,

  ```text
  P = alpha g_c + beta' g_d,        Q = alpha' g_c + beta g_d.
  ```

  Comparing coefficients in `x_{K_c}`, `x_{K_d}`, `x_s`: the tensor
  `T_{W - v - s}` has no component with colour `e` at `K_c` or `K_d`; the word
  with `K_c = d` is nonzero only when everything else is `d` (value
  `tau^d_{vs}`); the word with `K_d = c` is nonzero only when everything else
  is `c` (value `tau^c_{vs}`); the words with `(K_c,K_d) = (d,c)` vanish;
  and `H_{K_c}` has no `x_s[e]` component (symmetrically `H_{K_d}`).
- The two analogous equations for the reciprocal blocks at `K_c`, `K_d`,
  `K_e`, `s` (rows `W_{K_c v} = e_c (w^c)^T`, etc.), which are the same
  equations read at the other endpoint and pair this local model with the
  killer flags of those neighbours (Proposition K applies when they have
  degree four).

I did **not** find a contradiction from these, and I did not construct a
global completion.  They are the data a degree-four exclusion must defeat;
the pure-word identity for `T_{W - v - K_e}` is the cleanest handle (it says
an `(n-2)`-vertex subgraph supports exactly one word).  The one-bad branch
(item 4) has even fewer constraints.  So an all-order obstruction is
*plausible but unproved*; no counter-scenario has been shown to satisfy the
non-local equations either.

## 5. Mechanisms tried and exactly where each fails

**(i) Interaction with the killers at `u`.**  Gives Proposition K: a mixed
killer makes `v` useless to `u` (no killer or anchor role), pushing `u` to
degree `>= 4`, and at degree 4 forces all killers of `u` monochromatic plus
the cofactor vanishings `tau^b_{uv} = 0`.  It fails to close because the
constraints propagate only to vanishing of monochromatic hafnian cofactors,
which the singleton equations do not contradict, and because for
`deg(u) >= 5` the extra neighbours absorb the slack.

**(ii) Pinned-row anchors.**  Anchor `A_a` for row `a` at `v` cannot be
`K_c` for `c != a`, and equals `K_a` iff `w^a_a != 0`.  Monochromatic killers
anchor themselves.  For a bad colour `c` the only extra demand is
`s[c,j] = 0` (`j != c`) when `w^c_c = 0`, which holds automatically in the
degree-four models.  This mechanism adds no contradiction there; it only
gives a nonzero diagonal entry `s[c,c]` in the case `w^c_c = 0`.

**(iii) Torus degeneration.**  Entrywise, a one-parameter subgroup of the GHZ
stabiliser acts by `W_ij[a,b] -> lambda^{s_i^a + s_j^b} W_ij[a,b]` with
`sum_v s_v^a = 0` for each `a`, and fixes `T_W = Delta_n` (non-constant
words are zero, constant words have total weight 0).  If all exponents on the
support are `>= 0` and one is `> 0`, the `lambda -> 0` limit is a witness
with strictly smaller entry support.  By the Stiemke/Farkas alternative such a
subgroup exists unless there are positive weights `mu` on the support entries
and constants `q_a` with `sum_{entries at (v,a)} mu = q_a` for all `v`
(endpoint-label balance; same argument as in
[`MATRIX_UNIT_GHZ_DIAGONAL_TORUS_POLYSTABILITY_ENDPOINT_BALANCE_AND_ACTIVE_TRANSPORT_SHARPNESS_THEOREM.md`](../../claims/arbitrary-order/MATRIX_UNIT_GHZ_DIAGONAL_TORUS_POLYSTABILITY_ENDPOINT_BALANCE_AND_ACTIVE_TRANSPORT_SHARPNESS_THEOREM.md),
which I did not re-verify for full blocks).  So a general degeneration to
force `w ∝ e_c` **does not exist**: balance holds on supports containing bad
killers.  Explicit example: three monochromatic perfect matchings `M_0, M_1, M_2`
(entries `(i,k;j,k)`, `ij ∈ M_k`), `u = M_c(v)`, `y = M_a(v)`, plus the two
bad entries `(v,a;u,c)` and `(v,c;y,a)`; take `mu = 1` on the matching
entries except `1 - eps` on `(v,c;u,c)` and `(v,a;y,a)`, and `mu = eps` on the
bad entries.  Every `(vertex, colour)` then has total weight 1, so this support is
endpoint-balanced.  Its killer pattern at `v` is the two-bad pattern of
D4 item 3 (support level only; nothing here says weights exist).  Conclusion:
torus degeneration yields only "support-minimal witnesses are balanced" and
cannot by itself decide Parent C.  It could still combine with the equations
(for example to force the `s` block of D4 to avoid the cross entries), which I
did not pursue.

**Direct multi-killer/backups argument** (Lemma M, D4).  Closes degree 3,
shows degree 4 is the first open case, and reduces degree 4 to two explicit
local models.  Fails beyond degree 4 because backups can be supplied by
unconstrained extra neighbours.

## 6. Sharpest honest statements

1. Parent C (C-lit) is equivalent, for vertices with a unique colour-`c`
   killer, to **reciprocal anchoring**: the killer's tail is a row-`c` anchor
   of the killer's head.  (Proved, trivial.)
2. Parent C holds at every vertex of degree 3, and at degree 4 the only
   configurations not excluded by the local theorems are the two models in D4
   items 3 and 4 (assuming no bridge killers).  (Proved here, local.)
3. Mixed killers force `deg >= 4` at both endpoints, and at a degree-four
   head all killers there are monochromatic with explicit vanishing of
   monochromatic hafnian cofactors (Proposition K).  (Proved here, local.)
4. Torus degeneration does not prove Parent C: bad killers are
   endpoint-balanced at the support level.  (Constructed example.)
5. The literal statement (C-lit) is not forced by any recorded local theorem
   when a vertex has two same-colour killers; (C-span) is the natural
   well-posed target.  (Observation; not a counterexample.)

## 7. Strictly sharper next lemmas

- **Degree-four closure.**  Decide the two D4 branches using the second-order
  word equations (two deviating positions), starting from the pure-word
  identity `T_{W - v - K_e} = lambda^{-1} e_e^{⊗(n-2)}` and the restricted
  structure of `T_{W - v - s}`.  A proof closes Parent C at all degree-four
  vertices (modulo bridges); an exact local model surviving them together with
  the reciprocal equations at the four neighbours is the adversarial target.
- **Bridges.**  Extend Lemma M to bridge killers (two-term degeneration of the
  hyperplane theorem), to remove the "no bridge" hypothesis.
- **Degree >= 5.**  Needs a mechanism that bounds how many neighbours can
  serve as backups; none of the mechanisms above supplies one.

## 8. Checks run

Symbolic check (sympy) of the 2x2 solve in D4 item 3: `alpha w^c + alpha' w^d = e_c`,
`beta' w^c + beta w^d = e_d`, and `N^{-1} = [[alpha, beta'],[alpha', beta]]` for
`N = [w^c w^d]`.  All other statements are hand proofs and have no
independent audit.
