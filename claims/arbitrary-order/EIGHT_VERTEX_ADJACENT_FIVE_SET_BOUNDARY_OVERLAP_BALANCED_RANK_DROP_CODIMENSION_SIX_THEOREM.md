# Eight-vertex adjacent five-set overlap inside balanced rank drop

## Status

**Exact ternary characteristic-zero necessary condition at eight vertices.**
Fix two five-sets `S=A union {u}` and `T=A union {v}` with `|A|=4`.  The
adjacent-five-set boundary-overlap theorem places every hypothetical witness
in an affine incidence envelope of codimension at least five.  This note
proves that, after imposing the all-balanced sensor rank-drop condition
`B_all`, the same adjacent-pair envelope has codimension at least six in the
full `252`-dimensional affine block-graph space.

The only source strata that previously stopped at codimension five have all
four common roots synchronized and use one common nonconstant selector

```text
f:{0,1,2}->A.                                         (1)
```

Each such equality source is irreducible.  An explicit balanced full-sensor
chart lies on it, so its intersection with the pullback of `B_all` is a
proper closed subset and costs at least one further dimension.

This is a set-theoretic dimension bound.  It does not prove a regular or
transverse cut, exact codimension six, independence among adjacent pairs, or
emptiness of the residual.  An exact common-quadratic graph lies in both
selector orbits and in `B_all`, so the residual is genuinely nonempty in the
ambient incidence geometry.  Eight-vertex witness exclusion, the full S3
branch, and the global Krenn--Gu conjecture remain **OPEN/UNRESOLVED**.

## 1. The affine incidence sources

Work over an algebraically closed characteristic-zero field.  Let `Omega`
have eight vertices, every local space `L_i` have dimension three, and put

```text
G_Omega
 = product_({i,j} subset Omega) (L_i tensor L_j)^*
 isomorphic to A^252.                                  (2)
```

Take

```text
A={0,1,2,3},
S=A union {u},       T=A union {v},       u!=v.        (3)
```

The predecessor theorem chooses boundary roots on `S` and `T`, nonconstant
colour-zero selectors `f,g`, and stratifies their exact synchronization set
`R subset A`.  Write `r=|R|`,

```text
delta_R=2r-a_R,                                       (4)
```

where `a_R` counts colours assigned by both selectors to the same
synchronized vertex.  The root stratum has dimension at most
`14-delta_R`.  Its fourteen union blocks obey

```text
20-binomial(r,2)                                      (5)
```

independent evaluation equations, while the other fourteen blocks are free.
Hence the corresponding full affine incidence source has dimension at most

```text
(14-delta_R)
 + (252-(20-binomial(r,2)))
 =246+binomial(r,2)-delta_R.                          (6)
```

Every source except

```text
r=4,       a_R=3,       f=g:{0,1,2}->A               (7)
```

already has dimension at most `246`.

## 2. The sixty equality sources

Fix one nonconstant map `f` in (7), and put `F_i=f^(-1)(i)`.  Its common-root
base is

```text
Y_f
 = product_(i in A) P(intersection_(c in F_i) ker e_(i,c)^*)
   times P(L_u) times P(L_v).                         (8)
```

The first product has dimension

```text
sum_(i in A)(2-|F_i|)=8-3=5,                         (9)
```

and the two outer roots contribute four more dimensions.  Thus `Y_f` is a
nonempty irreducible product of projective spaces of dimension nine.

Let `J_f subset Y_f times G_Omega` impose the six common-edge evaluations

```text
W_ij(z_i,z_j)=0,                     i<j in A,         (10)
```

and the eight outer-edge evaluations

```text
W_iu(z_i,x_u)=0,       W_iv(z_i,y_v)=0,   i in A.     (11)
```

Each is one nonzero linear functional on its own nine-dimensional block
space.  Consequently `J_f -> Y_f` is a vector bundle of rank `252-14=238`.
In particular,

```text
J_f is irreducible,       dim J_f=9+238=247.          (12)
```

The sixty selectors split into two orbits under colour and common-vertex
permutations:

```text
fibre sizes (2,1):       4*3*3 =36 selectors;
fibre sizes (1,1,1):     4*3*2 =24 selectors.         (13)
```

Selector nonuniqueness is harmless: these are labelled source pieces, not a
claim about distinct intrinsic components of their coefficient images.

## 3. A full balanced sensor on every equality source

Use the balanced partition

```text
R=A,       N=Omega minus A,       |R|=|N|=4.          (14)
```

Fix any point of `Y_f`.  Since each common root `z_i` is nonzero, choose
independent covectors

```text
a_i,b_i in z_i^perp subset L_i^*.                    (15)
```

Order `N={N_0,N_1,N_2,N_3}`.  Choose nonzero contraction points `s_j in
L_(N_j)` and covectors `ell_j` with `ell_j(s_j)=1`.  On the root-root and
cross blocks put

```text
W_(i,k)=b_i tensor b_k,                               i<k in A,
W_(i,N_j)=c_ij a_i tensor ell_j.                     (16)
```

Begin with `C=(c_ij)=I_4`.  This is the explicit balanced full-rank chart:
its eight parity-legal sensor columns are the eight distinct binary words in
the independent pairs `(a_i,b_i)`, up to nonzero double-factorial scalars.

Every evaluation in (10)--(11) vanishes because its common-root factor is
`a_i(z_i)` or `b_i(z_i)`.  Thus (16) lies in `J_f`, regardless of the two
outer boundary roots.

To keep every cross block nonzero, replace `I_4` by

```text
C(t)=I_4+t(J_4-I_4).                                  (17)
```

The chosen full-rank minor is a polynomial in `t` and is nonzero at `t=0`.
Only finitely many `t` are bad.  Since the field is infinite, choose a
nonzero good `t`; then every entry of `C(t)` is nonzero and the sensor is
still full.  Choose the six blocks internal to `N` arbitrarily nonzero; they
do not enter this balanced sensor.

The resulting graph belongs to `J_f` but not to `B_all`, because its sensor
for (14) has rank `2^(4-1)=8` at `s_N`.  Therefore

```text
J_f intersection (Y_f times B_all)                   (18)
```

is a proper closed subset of the irreducible variety `J_f`, and hence has
dimension at most `246`.

## 4. Proper projection gives the codimension-six envelope

The projection from `Y_f times G_Omega` to `G_Omega` is projective, hence
proper.  The coefficient image of (18) is therefore closed, lies in `B_all`,
and has dimension at most `246`.  Intersect each non-equality exact-
synchronization source with the pullback of `B_all`; its dimension was
already at most `246` by (6).  Its coefficient image may be only
constructible, but taking its closure does not increase dimension, and the
closure remains in the closed set `B_all`.  Taking the finite union over
selectors and strata therefore produces a fixed closed affine envelope
inside `B_all` of dimension at most

```text
246.                                                   (19)
```

The affine vector-bundle fibres already include whole-zero constrained and
free blocks.  Such loci are lower-dimensional subbundles; they require no
separate projective scaling or zero-block branch.  The predecessor
boundary-root and selector cover is expressed by the same evaluation
equations there.

Equivalently, that envelope has codimension at least six in `G_Omega`.

The argument is deliberately affine.  The equations defining `B_all` need
not descend under independent projectivization of every edge block, because
sensor columns sum matching monomials involving different block subsets.
No fourteen-block projective intersection is asserted.

## 5. The balanced cut is nonempty

The gain in (19) is not an exclusion.  In target coordinates let every one
of the 28 blocks equal

```text
Q = [[0,0,1],
     [0,1,0],
     [1,0,0]].                                        (20)
```

This invertible common-quadratic graph lies in `B_all` by the proved
common-quadratic rank-drop theorem.  On `A` choose synchronized roots

```text
(z_0,z_1,z_2,z_3)=(e_0,e_0,e_0,e_1),                 (21)
```

and choose both outer roots to be `e_0`.  All fourteen evaluations
(10)--(11) vanish.  The same root tuple supports representatives of both
selector orbits:

```text
(2,1):     f(0)=3, f(1)=0, f(2)=0;
(1,1,1):   f(0)=3, f(1)=0, f(2)=1.                   (22)
```

Thus `B_all` meets both types of equality source, with every physical block
nonzero.  The construction is not a witness: the common-quadratic orbit is
separately excluded from the GHZ equations by its two-flattening rank.

## 6. Proof-topology consequence

The exact update is

```text
adjacent five-set pair envelope:                     CODIMENSION >=5;
B_all-constrained adjacent-pair envelope,
  ambient codimension:                               >=6;
only former bound-five sources:                      60 FULL-K4-SYNC PIECES;
B_all contains any equality source:                  NO;
B_all meets the equality residual:                   YES;
regular/transverse or additive cut:                  NOT CLAIMED;
eight-vertex witness exclusion:                      OPEN;
all-balanced witness exclusion:                      OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.          (23)
```

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_eight_vertex_adjacent_five_set_boundary_overlap_balanced_rank_drop_codimension_six.py
python -I claims/arbitrary-order/audit_eight_vertex_adjacent_five_set_boundary_overlap_balanced_rank_drop_codimension_six.py
uv run --with sympy python claims/arbitrary-order/verify_eight_vertex_adjacent_five_set_boundary_overlap_codimension_five.py
python -I claims/arbitrary-order/audit_eight_vertex_adjacent_five_set_boundary_overlap_codimension_five.py
python -m py_compile claims/arbitrary-order/verify_eight_vertex_adjacent_five_set_boundary_overlap_balanced_rank_drop_codimension_six.py claims/arbitrary-order/audit_eight_vertex_adjacent_five_set_boundary_overlap_balanced_rank_drop_codimension_six.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_eight_vertex_adjacent_five_set_boundary_overlap_balanced_rank_drop_codimension_six.py claims/arbitrary-order/audit_eight_vertex_adjacent_five_set_boundary_overlap_balanced_rank_drop_codimension_six.py
```

The primary verifier checks the two selector orbits, exact incidence
dimensions, both all-blocks-nonzero full-rank fixtures, and the common-`Q`
rank-seven sharpness fixture with exact SymPy arithmetic.  The independent
no-import audit uses a separate selector count, permanent formula for the
eight binary sensor coordinates, custom rational elimination, and a direct
tensor walk for the common-`Q` graph.  The finite checks audit the formulas;
the irreducible-vector-bundle and proper-closed-cut arguments prove the
codimension theorem.

## Dependencies and lineage

- [`EIGHT_VERTEX_ADJACENT_FIVE_SET_BOUNDARY_OVERLAP_CODIMENSION_FIVE_THEOREM.md`](EIGHT_VERTEX_ADJACENT_FIVE_SET_BOUNDARY_OVERLAP_CODIMENSION_FIVE_THEOREM.md)
- [`BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md`](BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md)
- [`BALANCED_COMMON_QUADRATIC_ORBIT_RANK_DROP_AND_FLATTENING_EXCLUSION_THEOREM.md`](BALANCED_COMMON_QUADRATIC_ORBIT_RANK_DROP_AND_FLATTENING_EXCLUSION_THEOREM.md)
