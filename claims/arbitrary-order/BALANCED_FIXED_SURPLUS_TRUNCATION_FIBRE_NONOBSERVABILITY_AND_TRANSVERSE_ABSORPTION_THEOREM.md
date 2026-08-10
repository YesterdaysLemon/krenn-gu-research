# Balanced fixed-surplus truncation, fibre nonobservability, and transverse absorption theorem

## Status

This is an exact characteristic-zero structural theorem inside the `r>=2`
branch of the maximal torus-root reduction.  If the fixed physical surplus is
`2q`, rebalancing the vertices across a half--half cut exposes the complete
even principal hafnian deck, but contraction of the old roots annihilates
every column above depth `2q`.  A legal column lies in that forced-zero range
exactly when `r>=q+2`.  At the parity boundary `r=q+1` the truncation is
vacuous, although the ternary contracted sensor is still rank-deficient by
dimension.

The fixed-surplus layer does not determine the rank of the **uncontracted**
balanced sensor.  At surplus zero, and at surplus two in the maximal-root
scope, one fixed-layer fibre contains both a rank-deficient canonical shore
and a generically full-rank shore.  On a synchronized physical two-row Wick
cell, even the contractions with zero or one old-root slot open admit an
exact affine gauge.  Higher mixed-root equations remain necessary.

The theorem does not prove that a hypothetical witness has a full balanced
sensor, that its outside blocks synchronize through two common rows, or that
the global Wick lift exists or fails.  It supplies neither a proof nor a
counterexample to the original conjecture.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## 1. Fixed-surplus setup

Work over `C` with ternary local spaces `L_v=C^3`.  Let `R` be a
maximum-cardinality torus-root set in a hypothetical witness, assume

```text
|R|=r>=2,
```

and choose its fully supported root vectors `x_i`, `i in R`.  Put

```text
B=Omega-R,             |B|=r+2q,                     (1)
```

where `q>=0`.  For `u in B`, let

```text
h_(i,u)=W_iu(x_i,-),
H_u[i,-]=h_(i,u),
X_c=product_(i in R) x_i[c] != 0.                    (2)
```

For every even `S subset B`, let `H_S` be the physical perfect-matching
tensor of the graph induced by `S`, with `H_empty=1`.  The maximal-root
principal-hafnian identity is

```text
Lambda_(r,2q)
 = sum_(S subset B, |S|=2q)
     H_S tensor P_r(H_u:u in B-S)
 = sum_(c=0)^2 X_c e_c^(star tensor B).               (3)
```

Here `P_r` is the unsigned permanent tensor of the `r` persistent root rows.

Fix any `Q subset B` with `|Q|=q`, and put

```text
N=B-Q,
A=R disjoint-union Q,
|A|=|N|=m=r+q.                                        (4)
```

For parity-legal `D subset N`, let `G_D^Q` be the balanced companion tensor
of the cut `A|N` from the balanced half-sensor theorem.  Thus `G_D^Q` sums
the matchings in which the cross partners on the `N` shore are exactly `D`.
Contract only the old roots:

```text
bar G_D^Q
 = (tensor_(i in R) ev_(x_i)) G_D^Q.                  (5)
```

The result retains the `Q` covector slots and the present `N` slots in `D`.

## 2. Exact regrouping and contracted truncation

### Theorem 1 (balanced regrouping of the fixed layer)

For every `Q` in (4),

```text
sum_(I subset N, |I| even)
  bar G_(N-I)^Q tensor H_I
 = sum_(c=0)^2
     X_c e_c^(star tensor Q) tensor e_c^(star tensor N).            (6)
```

Moreover,

```text
bar G_(N-I)^Q=0                  whenever |I|>2q.      (7)
```

### Proof

Apply the balanced matching partition to `A|N` and then evaluate the old
root slots at `x_R`.  The left side is the original graph tensor with the
old roots contracted, so (3) gives the right side of (6).

For (7), a term in `G_(N-I)^Q` leaves exactly `|I|` vertices of `A`
internally matched.  An internal edge between two old roots evaluates to
zero.  Hence every leftover old root must use a distinct leftover vertex of
`Q`.  If `a` old roots and `t` vertices of `Q` are left, then

```text
a<=t<=q,                 |I|=a+t<=2q.                 (8)
```

Thus every term with `|I|>2q` vanishes.  The argument is pointwise and
termwise; it uses no genericity or division.

### Corollary 2 (rank and the exact parity boundary)

Over the function field of the `N` variables, let `bar Gamma_Q` be the
contracted balanced sensor whose columns are the tensors in (5).  The
complete even deck has

```text
K(m)=2^(m-1)                                            (9)
```

columns, while at most

```text
M(m,q)
 = sum_(j=0)^min(q,floor(m/2)) binom(m,2j)             (10)
```

can survive (7).  Since the remaining open root shore is `Q`,

```text
rank(bar Gamma_Q)<=min(3^q,M(m,q)).                    (11)
```

There is a legal even column in the forced-zero range if and only if

```text
2 floor(m/2)>2q
  iff r>=q+2.                                          (12)
```

This is the precise missing-column boundary.  When `r=q+1`, one has
`m=2q+1`, whose largest legal even depth is exactly `2q`; (7) is then
vacuous.  Nevertheless, for `q>=1`,

```text
rank(bar Gamma_Q)<=3^q<4^q=2^(m-1).                   (13)
```

More generally, full column rank of the ternary contracted sensor requires

```text
3^q>=2^(r+q-1).                                       (14)
```

For `r>=3`, (14) fails whenever `q<=r`, so `q>r` is necessary but not
sufficient.  None of these contracted rank bounds is a statement about the
rank of the uncontracted balanced sensor `Gamma_Q`.

### Corollary 3 (unnormalized top-cut reconstruction)

Regard the all-cross column

```text
K_Q=bar G_N^Q                                          (15)
```

as a tensor on all of `B`.  Then

```text
sum_(Q subset B, |Q|=q) K_Q=2^q Lambda_(r,2q).         (16)
```

Every matching contributing to (3) has exactly `q` outside--outside edges.
It is all-cross for `R union Q | B-Q` for exactly `2^q` choices of `Q`, one
endpoint of each outside--outside edge.  This proves (16) with multiplicity
one before the final `2^q` count.  Equation (16) is an unnormalized sum.  The
ordinary average is

```text
(2^q/binom(r+2q,q)) Lambda_(r,2q).                    (17)
```

For each target colour separately, some cut has a nonzero monochromatic top
coefficient.  The equation does not supply one common cut for all colours.

## 3. Fixed-layer fibre nonobservability

Fix the root vectors `x_R`, all contracted rows `H_u`, and all outside
blocks `W_uv`, `u,v in B`.  The **fixed-layer fibre** consists of choices of
the root--outside and root--root blocks satisfying

```text
W_iu(x_i,-)=h_(i,u),
W_ij(x_i,x_j)=0,                                      (18)
```

with the outside graph unchanged.  Every member has the same tensor (3).
The fibre is not required to preserve the uncontracted GHZ equation or the
maximum-cardinality property of `R`.

Choose covectors `xi_i in L_i^*` with `xi_i(x_i)=1`.  The canonical shore

```text
W_iu^0=xi_i tensor h_(i,u),
W_ij^0=0                                               (19)
```

lies in the fibre.

At `q=0`, only the all-cross column can be nonzero, and the canonical sensor
has rank one.  At `q=1`, every canonical column lies in

```text
(tensor_(i in R) xi_i) tensor L_Q^*,                  (20)
```

so its rank is at most three.  In the maximal-root `q=1` cell, the
five-outside-mode bound gives `r>=3`, and hence

```text
rank(Gamma_Q^0)<=3<2^r.                               (21)
```

### Theorem 4 (a full shore in the same fibre at `q=0`)

Assume `q=0` and label `B={u_i:i in R}`.  Choose linearly independent

```text
a_i,b_i in Ann(x_i)                                   (22)
```

and choose `ell_i in L_(u_i)^*` and a point `z_(u_i)` with
`ell_i(z_(u_i))=1`.  Starting from (19), add

```text
delta W_(i,u_i)=lambda a_i tensor ell_i,
delta W_ij=mu b_i tensor b_j.                         (23)
```

Index the balanced sensor by the even deck set `I subset N=B`.  Projecting
to the binary word that uses `b_i` exactly when `u_i in I`, its leading
coefficient is

```text
(|I|-1)!! lambda^(r-|I|) mu^(|I|/2),                 (24)
```

where `(-1)!!=1`.  Indeed, every `u_i notin I` uses its private cross edge,
while the `|I|` remaining roots are internally matched.  Each of their
`(|I|-1)!!` matchings contributes the same `b` word.

The parity-selected binary words are independent.  Their dual word rows
make the displayed initial-coefficient minor diagonal with nonzero diagonal,
so the uncontracted balanced sensor is generically full.  The perturbations
in (23) have an old-root factor in `Ann(x_i)`, and therefore preserve (18)
and (3).

### Theorem 5 (a full shore in the same fibre at `q=1`)

Assume `q=1`.  The left side of (3) is linear in the outside pair blocks and
its right side is nonzero, so at least one outside block is nonzero.  Choose
such an edge `qv`, take the suitable cut

```text
Q={q},
N={v,u_1,...,u_r},                                    (25)
```

and choose `z_v` so that

```text
a_q=W_qv(-,z_v)!=0.                                   (26)
```

Choose `b_q` independent of `a_q`; choose independent
`a_i,b_i in Ann(x_i)`; and choose `ell_i(z_(u_i))=1`.  Add to the canonical
shore

```text
delta W_(i,u_i)=lambda a_i tensor ell_i,
delta W_ij=lambda b_i tensor b_j,
delta W_(i,q)=lambda mu b_i tensor b_q.               (27)
```

For every even `I subset N`, define the binary tensor word `w_I` on the
balanced root shore `R union Q` by

```text
root i uses b_i  iff u_i in I,
root q uses b_q  iff v in I;                          (28)
```

the other letters are `a_i` and `a_q`.  The lexicographically leading
selected-word coefficients are

```text
v notin I:
  (|I|-1)!! lambda^(r-|I|/2) w_I,

v in I:
  (|I|-1)!! lambda^(r-|I|/2+1) mu w_I.               (29)
```

For `v notin I`, the fixed edge `qv` is used, the roots indexed by `I` are
internally matched, and the others use their private cross edges.  For
`v in I`, put `J={i:u_i in I}`.  Then `|J|=|I|-1` is odd.  Maximal
`lambda` degree forces `q` to meet one root in `J`; the remaining roots of
`J` pair internally.  The number of choices is

```text
|J| (|J|-2)!!=|J|!!=(|I|-1)!!.                       (30)
```

Canonical edges incident with an old root carry the letter `xi_i` and vanish
on the selected binary rows.  In the column indexed by `I`, the displayed
term is the only selected row at its maximal `lambda` degree.  A competing
term in which `q` crosses to some `u_k` can enter another selected row, but it
has one lower `lambda` degree in that same column.  Therefore the highest
`lambda` term of the selected-word determinant is the product of the
nonzero diagonal entries in (29).  This proves that the perturbed
uncontracted sensor is generically full.

All perturbations in (27) have an old-root factor annihilating `x_i`, so the
fixed rows, evaluated root--root zeros, outside deck, and (3) are unchanged.
This proves existence for a suitable cut `Q` chosen as an endpoint of a
nonzero outside edge.  It makes no assertion for every `q=1` cut.

Together, (19), Theorem 4, and Theorem 5 prove that the fixed layer does not
determine uncontracted balanced-sensor rank.  The full shores are not claimed
to be hypothetical witnesses.

## 4. Single-open-root equation and transverse absorption

Fix `i in R`.  For `y in L_i`, define

```text
k_(i,u)(y)=W_iu(y,-),
ell_ij(y)=W_ij(y,x_j).                                (31)
```

Let `L_i(k)` be the fixed-surplus expression (3) with persistent row `i`
replaced by the family `k_u`.  For `j!=i`, put

```text
Lambda^+_(ij)
 = sum_(T subset B, |T|=2q+2)
     H_T tensor
     P_(r-2)(H_u[R-{i,j},-]:u in B-T).                (32)
```

### Theorem 6 (exact single-open-root equation)

Leaving root `i` open and fixing every other root at its `x_j` gives

```text
L_i(k_i(y)) + sum_(j!=i) ell_ij(y) Lambda^+_(ij)
 = sum_(c=0)^2
     y[c] product_(h!=i)x_h[c] e_c^(star tensor B).   (33)
```

### Proof

Root `i` either meets an outside vertex, giving the replaced-row fixed
surplus, or meets one fixed root `j`, leaving `2q+2` outside vertices
internally matched.  Any further edge between two fixed old roots evaluates
to zero.  The two cases are disjoint and exhaustive.

### Theorem 7 (physical absorption identity)

Fix `j!=i`.  Suppose that one family `a_u in L_u^*` satisfies the exact
physical factorization

```text
W_uv
 = a_u tensor h_(j,v) + h_(j,u) tensor a_v           (34)
```

for every distinct `u,v in B`.  Then

```text
L_i(a)=(q+1)Lambda^+_(ij).                            (35)
```

### Proof

Expand the permanent in `L_i(a)` along the rows `a` and `h_j`.  For a fixed
`(2q+2)`-set `T`, its coefficient is

```text
sum_({u,v} subset T) H_(T-{u,v}) W_uv.                (36)
```

Every perfect matching of `T` occurs once for each choice of one of its
`q+1` distinguished edges.  Therefore (36) is `(q+1)H_T`, proving (35).

Choose covectors `kappa_i in L_i^*` and `eta_j in L_j^*` with

```text
kappa_i(x_i)=0,
eta_j(x_j)=1.                                         (37)
```

The affine perturbation

```text
delta W_(i,u)=tau kappa_i tensor a_u,
delta W_ij=-tau(q+1) kappa_i tensor eta_j             (38)
```

with the transposed convention in the opposite vertex order preserves the
fixed layer and every contraction having either zero or exactly one old-root
slot open.  At root `i`, the changes in (33) are

```text
tau kappa_i(y)L_i(a),
-tau(q+1)kappa_i(y)Lambda^+_(ij),                     (39)
```

which cancel by (35).  At another single-open root, the old `i` slot is
`x_i` and kills (38).  The invariance is exact in `tau`, since a perfect
matching uses at most one edge incident with `i`.

This is not invariance of all parameter jets.  If a fixed partial matching
of `p` additional old-root pairs disjoint from `{i,j}` is activated while
`j` remains pinned, the same edge-pointing calculation has factor

```text
q+p+1                                                   (40)
```

instead of `q+1`; after (38), the residual multiplicity on that stratum is
`p`.  This is only a pinned-`j` stratum calculation.  Opening or varying `j`
can already detect the gauge at `p=0`, and no claim is made that `p=1` is the
first possible global detector.

## 5. Physical two-row Wick synchronization

Assume `q>=1` and suppose the entire outside graph has the exact common-row
form

```text
W_uv=a_u tensor b_v+b_u tensor a_v                    (41)
```

for two families defined at every mode in `B`.  For `|S|=2q`,

```text
H_S
 = q! sum_(A subset S, |A|=q) a_A b_(S-A)
 = (1/q!) P_(2q)(a repeated q,b repeated q;S).        (42)
```

For a fixed `q|q` endpoint split there are exactly `q!` bipartite perfect
matchings.  Unsigned Laplace expansion along the repeated rows therefore
turns (3) into

```text
Lambda_(r,2q)
 = (1/q!)
   P_(r+2q)(H_1,...,H_r,a repeated q,b repeated q)
 = sum_(c=0)^2 X_c e_c^(star tensor B).               (43)
```

After multiplying by the nonzero scalar `q!`, equation (43) is a
`P_(r+2q) -> Delta_3` restriction with all three diagonal weights nonzero.

### Theorem 8 (Hall bound and equality boundary)

The common-row factorization (41) forces

```text
q<=r.                                                  (44)
```

At `q=r`, every `span(a_u,b_u)` is a rank-two coordinate plane, and every
colour belongs to exactly `2q` such local planes.  Since `r=q>=2`, each
family separately is coordinate-proportional: `a_u` takes each coordinate
direction in exactly `q` modes, as does `b_u`, and their directions are
distinct at every mode.

### Proof

Apply the all-subset kernel Hall quota from the arbitrary permanent hierarchy
to the source subset consisting of all `2q` repeated `a` and `b` rows in
(43).  Each target coordinate covector belongs to `span(a_u,b_u)` in at
least `2q` modes.  A subspace of dimension at most two contains at most two
coordinate axes, so

```text
6q<=2(r+2q),                                           (45)
```

which is (44).

At equality every local span contains exactly two coordinate axes, and each
colour reaches its lower quota.  Apply the same Hall theorem separately to
the `q` identical `a` rows and to the `q` identical `b` rows.  Each local
line contains at most one coordinate axis, while each colour must occur in
at least `q` modes.  There are exactly `r+2q=3q` modes, giving the asserted
coordinate counts and distinctness.

### Corollary 9 (an existing-row absorption bound)

If the family `b_u` in (41) satisfies

```text
b_u=rho_u h_(j,u)                                    (46)
```

for scalars `rho_u` at every mode, then the `q` copies of `b` together with
the original row `h_j` are `q+1` locally collinear source rows.  The Hall
quota and the fact that one line contains at most one coordinate axis give

```text
3(q+1)<=r+2q,
r>=q+3.                                                (47)
```

Thus the absorption cell (34) is impossible at `(r,q)=(3,1)`.  At
`(r,q)=(4,1)`, equality forces the six covectors `h_(j,u)` to be coordinate
proportional, exactly two modes of each colour.

For `r>=3`, a full contracted balanced sensor requires `q>r` by (14), while
the physical common-two-row branch requires `q<=r` by (44).  Therefore the
synchronized branch cannot yield a full **contracted** balanced sensor.  It
does not obstruct the full uncontracted sensors of Theorems 4--5 and says
nothing about an unfactorized outside graph.

## 6. Exact phase boundary

```text
q<=r-2:
  legal contracted deck columns above depth 2q are forced to vanish;

q=r-1:
  no legal depth is omitted, but ternary row dimension still fails;

q=r:
  no depth truncation occurs; row dimension fails for r>=3, and the
  common-two-row Wick branch is on its Hall equality boundary;

q>r:
  the exact dimension test (14) may or may not pass, while the
  common-two-row Wick branch is impossible.                           (48)
```

The inequality (14), not merely `q>r`, is the contracted row-capacity test.
The theorem does not exclude the unfactorized high-surplus locus, the
all-balanced rank-drop witness locus, or failure of pole removal and Wick
completion on a full uncontracted sensor.

## 7. Provenance and scope wall

The maximum-root hypotheses, nonzero `X_c`, and fixed physical layer (3) are
imported from
[`MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md`](MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md),
Theorem 3.  The balanced companions and complete even deck are imported from
[`BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md`](BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md),
Theorem 1.  The regrouping after contraction, the `2q` truncation, its exact
parity boundary, and the fixed-layer fibre comparison are new here.

The matching-filtration viewpoint is compatible with
[`MIXED_ROOT_DELETION_FILTRATION_AND_HERALD_FREE_PAIR_NO_GO.md`](MIXED_ROOT_DELETION_FILTRATION_AND_HERALD_FREE_PAIR_NO_GO.md),
Theorem 1, but that theorem does not itself assert the balanced truncation.
The double-factorial chart mechanism is compatible with
[`LOWER_MIXED_ROOT_JET_DELETION_LABEL_TOMOGRAPHY_AND_SQUAREFREE_GAUGE_THEOREM.md`](LOWER_MIXED_ROOT_JET_DELETION_LABEL_TOMOGRAPHY_AND_SQUAREFREE_GAUGE_THEOREM.md)
and the explicit chart in the balanced half-sensor theorem.  The constrained
`Ann(x_i)` fibre charts in Theorems 4--5 are new.

The repeated-row Laplace ancestry of (43) is
[`ARBITRARY_SURPLUS_COMMON_ROW_FULL_SPAN_OBSTRUCTION.md`](ARBITRARY_SURPLUS_COMMON_ROW_FULL_SPAN_OBSTRUCTION.md),
especially its factored-port equation, together with the two-port
specialization in
[`ARBITRARY_ORDER_TWO_RESIDUAL_STRICT_SUPPORT_STAIRCASE_AND_COORDINATE_FORCING.md`](ARBITRARY_ORDER_TWO_RESIDUAL_STRICT_SUPPORT_STAIRCASE_AND_COORDINATE_FORCING.md).
The physical hafnian coefficient `q!` and the present Hall consequences are
the new specialization.

The Hall statements import Theorem 1 of
[`ARBITRARY_PERMANENT_KERNEL_DELETION_HIERARCHY.md`](ARBITRARY_PERMANENT_KERNEL_DELETION_HIERARCHY.md).
They are not consequences of a new finite search.  The same-graph global
section and all-order Wick criterion remain exactly those of the balanced
half-sensor theorem.  The present theorem explains why the fixed layer and
all single-open-root contractions do not by themselves supply that lift.

```text
contracted balanced regrouping:                   PROVED;
forced-zero depth |I|>2q:                         PROVED;
actual forced-zero range iff r>=q+2:              PROVED;
q=0 and suitable q=1 fixed-fibre rank ambiguity:  PROVED;
zero/single-open-root transverse gauge:           PROVED CONDITIONALLY ON (34);
physical common-two-row Hall bound q<=r:          PROVED CONDITIONALLY ON (41);
unfactorized high-surplus exclusion:              UNKNOWN;
all-balanced witness rank-drop exclusion:         UNKNOWN;
global projective Wick lift success or failure:   UNKNOWN;
global Krenn--Gu conjecture:                       UNRESOLVED.
```

## Focused check

Run from repository root:

```text
python claims/arbitrary-order/verify_balanced_fixed_surplus_truncation_fibre_nonobservability.py
python claims/arbitrary-order/audit_balanced_fixed_surplus_truncation_fibre_nonobservability.py
```

The primary checker independently enumerates small labelled matching
partitions to test (6)--(7), the corrected parity boundary, the `2^q`
top-cut multiplicity, the `q=0,1` initial-word coefficients, the absorption
factor `q+1`, selected higher-stratum factors `q+p+1`, and the Hall incidence
arithmetic.  These are bounded convention and falsification checks.  The
arbitrary-order proofs are the written matching bijections, initial-term
arguments, hafnian edge-pointing identity, and imported Hall theorem.

The independent no-import audit uses a separate leftover-root bitmask ledger,
exact rational row reduction on explicit `q=0,1` fibre charts, and independent
matching/permutation counts for the Wick and absorption constants together
with separate Hall incidence arithmetic.  It
was derived without opening or importing the primary verifier.  Both scripts
remain bounded supporting checks rather than substitutes for the written
arbitrary-order proofs.
