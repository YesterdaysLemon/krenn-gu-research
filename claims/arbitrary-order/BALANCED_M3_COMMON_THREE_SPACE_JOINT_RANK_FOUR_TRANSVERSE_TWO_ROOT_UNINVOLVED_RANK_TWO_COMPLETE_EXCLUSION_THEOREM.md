# Balanced `m=3` common-three-space joint-rank-four transverse two-root uninvolved-rank-two complete exclusion

## Status

**Exact characteristic-zero exclusion of the complete uninvolved-row-rank-two
part of the joint-rank-four transverse two-root branch.**  Let `U` be the
total singleton span of a normalized, target-consistent physical `m=3`
common shore whose complete four-column sensor has full function-field rank.
Put `K=image H` and assume

```text
dim U=3,                         rank H=4.             (1)
```

Suppose exactly two root--root blocks are nonzero.  S2AG makes their
derivative transverse of rank six.  If the uninvolved third-root row has
rank two, then the physical full-sensor equations are inconsistent.

The load-bearing new statement is an incidence strengthening of the
S2AI/S2AK common-zero atlas.  Let `V` be a three-plane and `Q` a two-plane.
If a square on `Q` has one decomposable target image and the three mixed
maps land in the diagonal plane spanned by targets fully transverse to it,
then the alternating singleton tensor vanishes whenever `Q` is **not
contained** in `V`.  The only old atlas chart that could use a nonzero
intersection is the two-source conjugate-tangent chart.  Its last mixed
permanent forces the second generator of `Q` into `V` as well.  Thus it can
populate `Q subset V`, the joint-rank-three incidence, but not the
joint-rank-four line-intersection incidence.

This theorem closes only the `q=2` joint-rank-four cell.  The exact S2BM
`q=1` joint-rank-four pole control remains populated, and the sharp fixture
in Section 3 shows that the new incidence lemma cannot exclude the
joint-rank-three `Q subset V` boundary.  Rank three, the `q=1` pole residue,
three-root lower-rank derivatives, other S2T/S2Q components and pole strata,
higher orders, the all-rank-drop branch, a witness, and a counterexample
remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The rank-four cell has one row-space intersection line

After permuting roots, write

```text
B_23=B!=0,                  B_13=C!=0,       B_12=0,

D_(B,C)(a,b,c)=a tensor B+C tensor b,
rank D_(B,C)=6,             ker D_(B,C)=A_3.          (2)
```

By S2BM, projection of `K` to the two involved roots is a three-plane

```text
P=pr_(1,2)K subset A_1 direct-sum A_2,
U=D_(B,C)(P),                                      (3)
```

and the derivative restricts to an isomorphism from `P` to `U`.  Transpose
the three root rows:

```text
rho:A_1^*->K^*,        pi:A_2^*->K^*,
theta:A_3^*->K^*,

V=image rho+image pi,             Q=image theta.     (4)
```

For the cell considered here, S2BM gives

```text
dim V=3,        dim Q=2,        V+Q=K^*,
dim(V intersect Q)=1,          Q not subset V.       (5)
```

Both involved rows have rank at least two.  Indeed, suppose for example
that `rank rho<=1`.  Then `ker rho` contains a two-plane.  For any nonzero
`alpha in ker rho`, contract the complete target equation in the first
root.  The all-cross permanent vanishes and the singleton contraction has
the form

```text
pr_2(P) tensor c_alpha,
c_alpha=(alpha tensor id)(C).                       (6)
```

Every target colour in the coordinate support of `alpha` would force its
diagonal `e_i tensor e_i` into (6).  The fixed third-root factor can carry
at most one such coordinate diagonal, so every vector of the two-plane `ker rho`
would have support at most one.  Over an infinite field a two-plane cannot
be contained in the union of three coordinate lines.  Thus `rank rho>=2`;
the same proof gives `rank pi>=2`.  Consequently

```text
(rank rho,rank pi) in {(2,2),(2,3),(3,2),(3,3)}.    (7)
```

S2BM also proves that the kernel generator of the rank-two map `theta` has
coordinate support one or two.  Equations (5)--(7) are therefore an
exhaustive finite profile census; no genericity or sampled case split is
being added below.

## 2. A noncontained-plane common-zero lemma

For `u,v,q in W^*=X^* direct-sum Y^* direct-sum Z^*`, write

```text
M_(u,v)(q)=per(u,v,q) in X^* tensor Y^* tensor Z^*. (8)
```

Choose three pairwise fully transverse decomposable target tensors

```text
T_i=x_i tensor y_i tensor z_i,              i=0,1,2, (9)
```

meaning that the three factor lines are distinct in every source.  Let `D`
be the span of either one or both of `T_0,T_1`.

### Lemma 1 (noncontained-plane diagonal common zeros)

Let

```text
V=span(u_0,u_1,v),              dim V=3,
Q a two-plane,                  Q not subset V.     (10)
```

Suppose

```text
M_(v,v)|_Q has rank one with image span(T_2),       (11)

M_(u_0,v)(Q) subset D,
M_(u_1,v)(Q) subset D,
M_(u_0,u_1)(Q) subset D.                            (12)
```

Then

```text
Alt_XYZ(u_0,u_1,v)=0.                              (13)
```

Here `Alt_XYZ` is the alternating separated tensor obtained by assigning
the three vectors to `X,Y,Z` with the sign of the assignment.

### Proof

A vector supported in one source has zero square, so `v` uses two or three
sources.  The square-rank-one argument of S2AK is incidence-free.  If
`v=x+y`, every mixed value `M_(v,u)(q)` lies in

```text
x tensor Y^* tensor Z^* + X^* tensor y tensor Z^*. (14)
```

If `v=x+y+z`, the decomposable square image shares two base factor lines;
after permuting sources it is `T_2=x tensor y tensor t`.  Quotienting the
square identity first by `x` and then by `y` again puts every mixed value in
(14).  Project (14) to

```text
(X^*/span(x)) tensor (Y^*/span(y)) tensor Z^*.      (15)
```

The images of `T_0,T_1` are independent because their `Z` factors are
independent.  Hence (14) intersects `D` only at zero, and the first two maps
in (12) vanish.

The exact S2AI common-zero atlas now applies.  In the nonconjugate
two-source chart the common-zero space is a line.  In the fully conjugate
chart and in every three-source chart, its displayed polarized identities
already make (13) vanish without any incidence assumption.  Only the
two-source conjugate chart with a nonzero tangent term needs new work.

In that chart one may rescale and write

```text
v=x+y,                     w=x-y,
q_0=w,                     q_1=d+e+t,
u=-d-e+t,                                             (16)

Q=span(w,q_1),
common-zero(v,Q)=span(w,u),
x tensor e+d tensor y !=0.                           (17)
```

If `u_0,u_1` are dependent then (13) is immediate.  Otherwise write

```text
u_0=A w+B u,                  u_1=C w+D u,
Delta=A D-B C!=0.                                    (18)
```

Direct polarized expansion gives

```text
(1/2)M_(u_0,u_1)(q_0)
 =-(A D+B C)x tensor y tensor t
   +B D(d tensor y tensor t-x tensor e tensor t),   (19)

(1/2)M_(u_0,u_1)(q_1)
 =-A C x tensor y tensor t-B D d tensor e tensor t, (20)

Alt_XYZ(u_0,u_1,v)=-2 Delta x tensor y tensor t.    (21)
```

Both tensors (19)--(20) lie in
`X^* tensor Y^* tensor span(t)`.  This space meets `D` only at zero because
`z_0,z_1,t` are independent.  In particular (19) vanishes.

If `B D=0`, then either `B=0`, in which case `A D=Delta!=0`, or `D=0`, in
which case `B C=-Delta!=0`.  Equation (19) is nonzero in either case.
Therefore `B D!=0`.  Project (19) successively to

```text
(X^*/span(x)) tensor span(y) tensor span(t),
span(x) tensor (Y^*/span(y)) tensor span(t).         (22)
```

It follows that

```text
d in span(x),                         e in span(y).  (23)
```

All five vectors `w,u,v,q_0,q_1` consequently lie in
`span(x,y,t)`.  Since the three vectors in (10) span a three-plane,

```text
V=span(x,y,t),                       Q subset V,     (24)
```

contrary to (10).  The last surviving atlas chart is therefore impossible,
and (13) holds.  QED.

The proof used only exact tensor identities and linear-space incidence.
Characteristic zero is load-bearing in the factors of two and in the
inherited common-zero atlas.

## 3. The containment boundary is exactly populated

The hypothesis `Q not subset V` cannot be removed.  Take nonzero forms
`x in X^*`, `y in Y^*`, `t in Z^*` and put

```text
v=x+y,
u_0=-2y+t,                   u_1=2x-t,
q_0=x-y,                    q_1=x+y+t.              (25)
```

Then

```text
V=span(u_0,u_1,v)=span(x,y,t),
Q=span(q_0,q_1) subset V,                            (26)

M_(v,v)(q_0)=0,              M_(v,v)(q_1)=2x tensor y tensor t,

M_(u_0,v)|_Q=M_(u_1,v)|_Q=M_(u_0,u_1)|_Q=0,        (27)

Alt_XYZ(u_0,u_1,v)=4x tensor y tensor t!=0.         (28)
```

This is an exact common-zero fixture for the joint-rank-three incidence,
not a physical graph, a regular pair lift, or a counterexample.  It proves
that the rank-three successor must use the rest of the complete target
equation or pole/deck information rather than Lemma 1 alone.

## 4. Exhaustion of the rank-four `q=2` profiles

All reductions cited below occur before the old rank-five proofs invoke
`V intersect Q=0`.  They use only the derivative isomorphism (3), the
three-plane `P`, the fact that `Q` is a two-plane, and the complete physical
target equation.  Those data are unchanged at joint rank four.

### Kernel support one

S2AL excludes profiles `(3,3)`, `(3,2)`, and `(2,3)`.  Its square-pencil,
tangent-line, and binary five-product arguments are stated for an arbitrary
two-plane `Q` and never use the incidence of `Q` with `V`.

For profile `(2,2)`, S2AM's two zero rows give its exact relation-plane
normal form and the complete target table.  That table has a rank-one
`T_j` square and places the three mixed maps in
`span(T_c,T_d)`.  The only rank-five-specific input in the last step is the
old disjoint-plane version of the common-zero lemma.  Here (5) gives
`Q not subset V`, so Lemma 1 applies and contradicts full singleton rank.
Thus every support-one profile is impossible.

### Kernel support two

S2AJ's target-line argument excludes the mixed profiles `(3,2)` and `(2,3)`
without using any `V,Q` incidence.

For profile `(2,2)`, S2AI's exhaustive beta-zero atlas and zero-row target
table reduce the complete profile to a rank-one square, one zero mixed map,
and the other two mixed maps on one fully transverse target line.  For
profile `(3,3)`, S2AK's graph contraction and permanent symmetry give a
rank-one `T_2` square and all three mixed maps in
`span(T_0,T_1)`.  Both are instances of Lemma 1 under (5), so both
alternating singleton tensors vanish, contrary to physical full-sensor
rank.  Thus every support-two profile is impossible.

Combining the two support cases and the exhaustive profile census (7)
proves

```text
rank H=4, transverse two-root derivative rank 6,
rank theta=2:                                      IMPOSSIBLE.        (29)
```

## 5. Proof-topology consequence

The transverse two-root lower-rank frontier is now

```text
joint rank 4, uninvolved-row rank q=2:              IMPOSSIBLE;

joint rank 4, q=1:
  exact physical local incidence control with pair poles (S2BM),
  pole-residue / higher-deck obstruction:           OPEN;

joint rank 3, q=2:
  Q subset V and exact common-zero fixture:          OPEN;

joint rank 3, q=1:
  exact physical local incidence control with pair poles (S2BM),
  pole-residue / higher-deck obstruction:           OPEN.            (30)
```

No finite-field scan, numerical specialization, bounded sample,
generic-point promotion, or unproved case cover enters the theorem.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_transverse_two_root_uninvolved_rank_two_complete_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_transverse_two_root_uninvolved_rank_two_complete_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_transverse_two_root_uninvolved_rank_two_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_transverse_two_root_uninvolved_rank_two_complete_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_transverse_two_root_uninvolved_rank_two_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_transverse_two_root_uninvolved_rank_two_complete_exclusion.py
```

The primary verifier expands the conjugate-tangent chart symbolically,
checks the quotient coefficients and determinant factor, and verifies the
sharp `Q subset V` fixture with exact SymPy arithmetic.  The independent
audit imports no repository module or third-party package; it rebuilds the
polarized and alternating tensors with a separate sparse-polynomial engine
over `Fraction` and checks the same fixture in a different basis order.
The scripts replay the displayed identities.  The arbitrary-vector quotient
and atlas-exhaustion arguments are the proof above and the cited exact
predecessors, not claims inferred from a finite computation.

## Dependencies

- [`lower-joint-rank transverse localization and pole controls`](BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_TRANSVERSE_TWO_ROOT_LOCALIZATION_AND_POLE_CONTROLS_THEOREM.md)
- [`support-two (2,2) complete exclusion and common-zero atlas`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_TWO_BY_TWO_COMPLETE_EXCLUSION_THEOREM.md)
- [`support-two mixed-row-rank exclusion`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_MIXED_ROW_RANK_EXCLUSION_THEOREM.md)
- [`support-two (3,3) exclusion`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_THREE_BY_THREE_EXCLUSION_THEOREM.md)
- [`support-one higher-row-rank exclusion`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md)
- [`support-one (2,2) complete exclusion`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_TWO_BY_TWO_COMPLETE_EXCLUSION_THEOREM.md)
