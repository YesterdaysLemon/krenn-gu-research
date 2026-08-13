# Balanced root-quadric basepoint permanent-restriction and gauge-sharpness theorem

## Status

**Exact characteristic-zero balanced-shore bridge and eight-vertex
sharpness fixture.**  Fix a balanced cut

```text
Omega=R disjoint-union N,       |R|=|N|=m>=2,
```

and fixed isomorphisms from the root spaces to one three-dimensional space.
If the diagonal root quadrics have a common projective zero at which every
pulled-back target coordinate is nonzero, then any hypothetical ternary GHZ
witness supplies an exact restriction

```text
P_m -> Delta_3.                                      (1)
```

This is a new proof-DAG edge, not a new permanent-extraction theorem: the
matching extraction is the zero-surplus case of the existing maximal
torus-root theorem.  The new application observes that a common nondegenerate
root quadric always supplies the required fully supported point.  Therefore
the entire common-root-quadric shore, including nonseparable cross blocks, is
impossible for `m=3,4`; for `m>=5` it reduces to the live arbitrary permanent
restriction problem.

The same matching partition gives a more general root-ideal residue identity.
It does not, however, extract a projective basepoint from balanced sensor rank
drop.  An exact normalized rational eight-vertex common-quadratic-orbit graph
has every balanced sensor rank at most seven, all edge blocks invertible, and
root quadrics spanning all ternary quadrics in one prescribed target gauge.
Its fixed-gauge projective base locus is empty and one mixed coefficient is
`-1`, so it is not a witness.  The graph is latently synchronized after
independent vertex gauges; it is a warning about fixed-gauge extraction, not a
counterexample to existential synchronization or to the conjecture.

The all-balanced witness locus and the arbitrary `P_m -> Delta_3` problem for
`m>=5` remain open.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Balanced root ideal and the complete matching residue

Work over `C`; equivalently, extend any characteristic-zero base field to an
algebraic closure.  For each `i in R`, fix an isomorphism

```text
A_i:L_i -> V,                 dim V=3.                (2)
```

For distinct roots define

```text
b_ij(x)=W_ij(A_i^(-1)x,A_j^(-1)x) in Sym^2(V^*),
I_R=(b_ij : i<j in R) subset C[V].                    (3)
```

For a target coordinate word `alpha:N->{0,1,2}`, put

```text
H_alpha(x)[i,u]
 =W_iu(A_i^(-1)x,e_(u,alpha(u))).                    (4)
```

Let `Match_r(S)` denote the `r`-edge matchings on a vertex set `S`.  If
`P in Match_r(S)`, write `V(P)` for its used vertices.  Also set

```text
d_uv(alpha)=W_uv(e_(u,alpha(u)),e_(v,alpha(v))).      (5)
```

Contract the nonroots against the word `alpha` and put the same transformed
vector `x` into every root.  Partition each perfect matching by its internal
root matching `P` and internal nonroot matching `Q`.  Balanced shore sizes
force `P` and `Q` to have the same number of edges.  The remaining vertices
cross bijectively.  Hence the full contraction is exactly

```text
F_alpha(x)
 = sum_(r=0)^floor(m/2)
     sum_(P in Match_r(R), Q in Match_r(N))
       (product_(ij in P) b_ij(x))
       (product_(uv in Q) d_uv(alpha))
       per H_alpha(x)[R-V(P),N-V(Q)].                 (6)
```

The empty permanent and empty products are one.  There are no determinant
signs or hidden multiplicities: fixing `P`, `Q`, and the remaining bijection
fixes one perfect matching.

The `r=0` term is the full all-cross permanent.  Every term with `r>=1`
contains a root-quadric generator, so (6) gives the polynomial congruence

```text
F_alpha(x)=per H_alpha(x) mod I_R.                   (7)
```

For a hypothetical ternary GHZ witness define the nonzero root linear forms

```text
R_(i,c)(x)=e_(i,c)^*(A_i^(-1)x).                     (8)
```

Then (7) yields the complete fixed-root-gauge residues

```text
per H_alpha belongs to I_R                 if alpha is nonconstant,

per H_(c^m)-product_(i in R) R_(i,c)
  belongs to I_R                           for c=0,1,2.              (9)
```

This contains the principal common-quadric residue theorem as the special
case `I_R subset (Q)`, but it does not assume the ideal is principal or has a
projective zero.

## 2. A fully supported basepoint exposes the permanent

### Theorem 1 (balanced basepoint-to-permanent bridge)

Assume a hypothetical ternary witness and suppose there is a projective point
`[x] in P(V)` satisfying

```text
b_ij(x)=0                         for every i<j in R,
R_(i,c)(x)!=0                     for every i in R and c=0,1,2.     (10)
```

Then the local root-to-nonroot maps give the restriction (1).

### Proof

Set `x_i=A_i^(-1)x`.  Conditions (10) say that the `m` root vectors are fully
target-supported and pairwise zero-coupled.  Leave every `z_u in L_u`,
`u in N`, free.  In a nonzero perfect matching no two roots can pair.  Because
there are exactly `m` roots and `m` nonroots, every root must pair with a
distinct nonroot and every nonroot is used.  Thus the surviving matchings are
exactly the bijections `R->N`, and

```text
T_W(x_R,z_N)
 = per [W_iu(x_i,z_u)]_(i in R,u in N).              (11)
```

Define

```text
phi_u:L_u -> C^R,
(phi_u z)_i=W_iu(x_i,z).                              (12)
```

Equation (11) is the pullback of the order-`m` permanent form by the maps
`phi_u`.  The target equality gives simultaneously

```text
T_W(x_R,z_N)
 = sum_(c=0)^2 X_c product_(u in N)e_(u,c)^*(z_u),
X_c=product_(i in R)e_(i,c)^*(x_i)!=0.               (13)
```

This is a concise weighted `Delta_3`.  An invertible diagonal rescaling in
one nonroot mode normalizes the three weights, proving `P_m->Delta_3`.

Equivalently, for `m>=3`, the Krenn--Gu range covered by the maximal
torus-root package, the multi-star bound makes a root set of size `m=n/2`
maximum, and the principal-hafnian identity in that theorem has surplus zero.
Its displayed `s=0` specialization is exactly (11)--(13).  Thus the extraction
step in the conjecture's range is an existing theorem interface; Theorem 1
records its balanced-basepoint input.  At `m=2`, the direct matching argument
(11)--(13) proves the statement without invoking that package.  QED.

## 3. Common nondegenerate quadrics route to the permanent frontier

### Corollary 2 (complete common-root-quadric reduction)

Suppose there is a nondegenerate `Q in Sym^2(V^*)` and scalars `rho_ij` such
that

```text
b_ij=rho_ij Q                     for every i<j in R. (14)
```

Then a hypothetical ternary witness gives `P_m->Delta_3`, with no condition
on any root-to-nonroot or nonroot-to-nonroot block.

### Proof

Over the algebraic closure, `Q=0` is a smooth irreducible projective conic.
Every `R_(i,c)` in (8) is a nonzero linear form because `A_i` is an
isomorphism.  A line cannot contain the irreducible conic, so its intersection
with the conic is finite.  The conic is not covered by the finite union of the
`3m` target-coordinate lines.  Choose `[x]` on `Q=0` outside that union.
Then (14) and the choice of `x` give (10), and Theorem 1 applies.  QED.

The exact low-order consequences are:

- `m=2` is impossible already by one-mode flattening rank: `P_2` has local
  rank two and `Delta_3` has local rank three.  This order lies outside the
  conjecture's `n>=6` range.
- `m=3` is impossible.  Concision of the target forces all three local maps
  on `P_3` to be invertible, while `rank(P_3)=4` and `rank(Delta_3)=3`.
- `m=4` is impossible because the exact subrank of `P_4` is two.
- For `m>=5`, this is an exact reduction to the live arbitrary permanent
  restriction family, not an exclusion.

In particular, the nonseparable simultaneous common-`Q` residue systems left
by the earlier divisibility theorem are no longer a separate balanced-shore
obligation.  At `m=3,4` they are empty; at `m>=5` any hypothetical survivor
must solve `P_m->Delta_3`.

## 4. All-cut rank drop does not force a fixed-gauge basepoint

The basepoint hypothesis in Theorem 1 cannot be inferred from balanced sensor
rank drop in one prescribed family of root identifications, even after adding
complete support, invertible blocks, local concision, and normalized pure
coefficients.

Let the eight rational matrices `G_1,...,G_8` be

```text
G_1 = [ 1  0  0;  0  1  0;  0  0  1 ],
G_2 = [-1  0  0;  0  1 -1;  0  0 -1 ],
G_3 = [ 0  0 -1;  0 -1  0;  1  0  0 ],
G_4 = [ 0 -1  0;  0  1  1; -1  0  1 ],
G_5 = [ 0  1  0; -1  0  0;  0  0 -1 ],
G_6 = [ 1  0  0;  0  1  0;  0  0 -1 ],
G_7 = [-1  0  0;  0  0  1;  0  1  0 ],
G_8 = [ 0    0  1/6;  1/3  0    0;  0  1/3  0 ].    (15)
```

For `i<j`, define the physical edge block

```text
W_ij=transpose(G_i) G_j.                              (16)
```

Every `G_i` and every `W_ij` is invertible.  The graph is in the nondegenerate
vertex-gauge common-quadratic orbit, since with `y_i=G_i z_i` every edge form
becomes `transpose(y_i)y_j`.  The common-quadratic sensor theorem therefore
puts every one of its seventy balanced sensors in rank at most

```text
binomial(4,2)+1=7<8.                                 (17)
```

It also gives local concision.  Direct exact matching expansion gives

```text
T_W(0,0,0,0,0,0,0,0)=1,
T_W(1,1,1,1,1,1,1,1)=1,
T_W(2,2,2,2,2,2,2,2)=1,
T_W(0,0,1,1,1,1,1,1)=-1.                            (18)
```

Thus the pure coefficients are normalized, while the displayed mixed word
certifies that this graph is not a witness.

Now take `R={1,2,3,4}` and use the identity as the prescribed root
identification at every root.  In the monomial basis

```text
(x_0^2,x_1^2,x_2^2,x_0 x_1,x_0 x_2,x_1 x_2),
```

the six columns of the quadrics `x^T W_ij x`, `i<j in R`, form

```text
C = [-1  0  0  0  0 -1;
      1 -1  1 -1  1 -1;
     -1  0  1  0 -2  0;
      0  0 -1  0  1  0;
      0  0 -1  0  1  1;
     -1  0  1  1  0  0],       det(C)=-1.            (19)
```

They are a basis of `Sym^2(V^*)`, so

```text
I_R=(x_0,x_1,x_2)^2,
V_+(I_R)=empty.                                      (20)
```

This does not contradict Corollary 2.  Re-identify root `i` using `G_i`.
For every edge,

```text
G_i^(-T) W_ij G_j^(-1)=I_3,                          (21)
```

so the same graph has the latent common quadric `x_0^2+x_1^2+x_2^2` and
therefore fully supported root tuples in that gauge.  The fixture refutes
only the route

```text
all balanced sensors rank-drop
  => a prescribed same-vector root ideal has a basepoint.          (22)
```

It does not refute an existential multiroot basepoint theorem using
independent root vectors or a theorem forcing latent synchronization from the
full mixed witness equations.

## 5. Proof-topology consequence

The exact update is

```text
general balanced root-ideal residue (7)--(9):          PROVED;
fully supported root-ideal basepoint => P_m->Delta_3:  PROVED;
common nondegenerate root quadric => P_m->Delta_3:     PROVED;
common-root-quadric shore at m=3 or m=4:               EXCLUDED;
common-root-quadric shore at m>=5:                     REDUCED TO PR;
B_all => fixed-gauge root-ideal basepoint:             FALSE;
B_all => existential multiroot basepoint/synchrony:    NOT DECIDED;
arbitrary P_m->Delta_3 for m>=5:                       OPEN;
all-balanced witness locus:                            OPEN;
global Krenn--Gu conjecture:                           UNRESOLVED.   (23)
```

The strategic target is therefore not another pure rank-drop-to-fixed-gauge
basepoint assertion.  A useful S3 advance must combine overlapping cuts and
the mixed target equations to force either a fully supported multiroot
basepoint, latent common-quadric synchronization, or a different exact
obstruction inside `B_all`.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_root_quadric_basepoint_permanent_restriction_and_gauge_sharpness.py
python -I claims/arbitrary-order/audit_balanced_root_quadric_basepoint_permanent_restriction_and_gauge_sharpness.py
python -m py_compile claims/arbitrary-order/verify_balanced_root_quadric_basepoint_permanent_restriction_and_gauge_sharpness.py claims/arbitrary-order/audit_balanced_root_quadric_basepoint_permanent_restriction_and_gauge_sharpness.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_root_quadric_basepoint_permanent_restriction_and_gauge_sharpness.py claims/arbitrary-order/audit_balanced_root_quadric_basepoint_permanent_restriction_and_gauge_sharpness.py
uv run --with sympy python claims/arbitrary-order/verify_balanced_common_quadratic_orbit_rank_drop_and_flattening_exclusion.py
python claims/arbitrary-order/audit_balanced_common_quadratic_orbit_rank_drop_and_flattening_exclusion.py
python claims/arbitrary-order/verify_maximal_torus_root_saturation_and_coordinate_absorption.py
python claims/arbitrary-order/audit_maximal_torus_root_saturation_and_coordinate_absorption.py
uv run --with sympy python claims/arbitrary-order/verify_exact_three_blocker_permanent_rank.py
python claims/arbitrary-order/audit_exact_three_blocker_permanent_rank.py
uv run --with sympy python claims/arbitrary-order/verify_fourth_order_permanent_subrank.py
python claims/arbitrary-order/audit_fourth_order_permanent_subrank.py
```

The primary new verifier uses SymPy to replay the balanced matching residue
through ten vertices, checks all 105 matching summands for each of the four
displayed rational eight-vertex coordinate coefficients, verifies the
six-quadrics determinant, and conjugates all 28 edge blocks to the common
form.  The independent audit imports neither SymPy nor the primary; it uses
`Fraction`, a separate matching recursion, hand-written matrix arithmetic,
and extends the all-cross count through twelve vertices.
These bounded calculations audit constants, signs, normalization, and the
gauge caveat.  The arbitrary-order bridge is the written matching partition
and conic-avoidance argument, with the cited maximal-root, `P_3`-rank, and
`P_4`-subrank packages supplying the imported theorem interfaces.

## Dependencies and lineage

- [`BALANCED_COMMON_QUADRIC_MIXED_PERMANENT_DIVISIBILITY_AND_CONFORMAL_SHORE_EXCLUSION_THEOREM.md`](BALANCED_COMMON_QUADRIC_MIXED_PERMANENT_DIVISIBILITY_AND_CONFORMAL_SHORE_EXCLUSION_THEOREM.md)
- [`MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md`](MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md)
- [`MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md`](MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md)
- [`EXACT_THREE_BLOCKER_PERMANENT_RANK_LEMMA.md`](EXACT_THREE_BLOCKER_PERMANENT_RANK_LEMMA.md)
- [`FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md`](FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md)
- [`BALANCED_COMMON_QUADRATIC_ORBIT_RANK_DROP_AND_FLATTENING_EXCLUSION_THEOREM.md`](BALANCED_COMMON_QUADRATIC_ORBIT_RANK_DROP_AND_FLATTENING_EXCLUSION_THEOREM.md)
