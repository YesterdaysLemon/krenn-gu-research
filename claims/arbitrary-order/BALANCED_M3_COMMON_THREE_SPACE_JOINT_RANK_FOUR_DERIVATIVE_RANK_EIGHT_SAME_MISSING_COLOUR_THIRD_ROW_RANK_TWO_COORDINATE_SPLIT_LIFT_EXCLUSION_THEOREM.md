# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight same-missing-colour third-row-rank-two coordinate split-lift exclusion

## Status

**Exact characteristic-zero exclusion of one complete coordinate split-lift
cell inside the same-missing-colour `(2,2,2)` row profile isolated by
S2BR.**  Retain the normalized, target-consistent physical `m=3`
common-three-space full-sensor hypotheses with

```text
dim U=3,                         dim K=4,             (1)
```

all three root blocks nonzero, and shared-derivative rank eight.  Let
`d,s,t` be the three distinct target colours.  After permuting roots and
colours and rescaling nonzero factors, suppose

```text
x=e_s,                 y=e_t,              w=e_s,
C=e_d tensor e_d+e_s tensor e_s,                    (2)

D(a,b,c)=(a tensor e_t-e_s tensor b) tensor e_s
          +C tensor c.                              (3)
```

Suppose the joint image is the coordinate split-lift four-space

```text
K=span(k_0,k_1,k_2,k_3),                            (4)

k_0=(e_s,e_t,0),
k_1=(0,0,e_d),
k_2=(0,-e_s,0),
k_3=(e_t,0,e_t).                                    (5)
```

Then no physical empty companion can satisfy

```text
G_N congruent J modulo U,             U=D(K).        (6)
```

The row profile in (2)--(5) has the common involved missing colour `d`, a
third-row kernel supported on `s`, exact row ranks `(2,2,2)`, and the
nonmonomial residual block required by the S2BQ torus gate.  The exclusion
uses a new rank-free eight-product obstruction for the polarized permanent:
six zero products cannot coexist with two fully transverse pure products in
the exact incidence forced by (6).

This theorem excludes the entire displayed split-lift cell, including every
choice of the physical cross map `H` onto `K`; it is not a finite sample.
It does not prove that every same-missing-colour `(2,2,2)` point can be put in
(2)--(5).  Nonsplit lifts, other coordinate placements of the complementary
block, third-row rank three, mixed or injective involved rows, joint rank
three, derivative rank seven, the pair gate, other components and pole
strata, higher orders, and the all-rank-drop branch remain open.  Global
Krenn--Gu remains **UNRESOLVED**.

## 1. Derivative and row incidence of the split-lift cell

The derivative in (3) has

```text
ker D=span(k_0),                    rank D=8.         (7)
```

Indeed the first two summands have the five-dimensional tangent image

```text
(A_1 tensor e_t+e_s tensor A_2) tensor e_s,         (8)
```

while `C` lies outside the two-factor tangent plane because of its
`e_d tensor e_d` term.  Direct substitution gives

```text
D(k_0)=0,
D(k_1)=C tensor e_d,
D(k_2)=e_s tensor e_s tensor e_s,
D(k_3)=e_t tensor e_t tensor e_s+C tensor e_t.      (9)
```

The last three tensors are independent, so

```text
U=span(D(k_1),D(k_2),D(k_3)),       dim U=3.        (10)
```

The three coordinate projections of `K` are

```text
pr_1 K=span(e_s,e_t),
pr_2 K=span(e_s,e_t),
pr_3 K=span(e_d,e_t).                               (11)
```

Thus the first and second row kernels are both `span(e_d^*)`, while the
third is `span(e_s^*)`.  This is exactly the same-missing-colour,
third-row-support-one `(2,2,2)` cell allowed by S2BR.

## 2. The eight quotient coefficients

Let `g_i in W^*`, `0<=i<=3`, be the images under the injective transpose
`H^*:K^*->W^*` of the basis dual to (5).  For `u,v,z in W^*`, write

```text
P(u,v,z)=per(u,v,z) in X^* tensor Y^* tensor Z^*.   (12)
```

The polarized root permanent on the basis (5) has exactly eight nonzero
unordered products:

```text
Perm(k_0,k_0,k_1)= 2 e_s tensor e_t tensor e_d,
Perm(k_0,k_0,k_3)= 2 e_s tensor e_t tensor e_t,
Perm(k_0,k_1,k_2)=-  e_s tensor e_s tensor e_d,
Perm(k_0,k_1,k_3)=   e_t tensor e_t tensor e_d,
Perm(k_0,k_2,k_3)=-  e_s tensor e_s tensor e_t,
Perm(k_0,k_3,k_3)= 2 e_t tensor e_t tensor e_t,
Perm(k_1,k_2,k_3)=-  e_t tensor e_s tensor e_d,
Perm(k_2,k_3,k_3)=-2 e_t tensor e_s tensor e_t.     (13)
```

These eight tensors form a basis of

```text
span(e_s,e_t) tensor span(e_s,e_t)
  tensor span(e_d,e_t).                              (14)
```

Moreover (10) meets (14) only in zero.  Each generator in (9) has a unique
component outside (14): respectively `e_d tensor e_d tensor e_d`, third
factor `e_s`, and either a first/second `e_d` or third factor `e_s`.

Modulo `U`, the three target diagonals reduce to

```text
e_d tensor e_d tensor e_d
  congruent -e_s tensor e_s tensor e_d,

e_s tensor e_s tensor e_s congruent 0,

e_t tensor e_t tensor e_t unchanged.               (15)
```

Expanding the physical empty permanent in the basis (5), comparing (13)
coefficientwise, and using (15), equation (6) is therefore equivalent to

```text
P(g_0,g_0,g_1)=0,
P(g_0,g_0,g_3)=0,
P(g_0,g_1,g_3)=0,
P(g_0,g_2,g_3)=0,
P(g_1,g_2,g_3)=0,
P(g_2,g_3,g_3)=0,                                  (16)

P(g_0,g_1,g_2)=T_d,
P(g_0,g_3,g_3)=T_t,                                 (17)
```

up to independent nonzero scalars, where

```text
T_c=X_c tensor Y_c tensor Z_c.                      (18)
```

The repeated-index factors `2` in (13) are exactly the repeated terms in
the six-term polarization (12), so no factorial is missing in (16)--(17).
The two tensors in (17) are nonzero and fully transverse.

## 3. A rank-free eight-product obstruction

### Lemma 1 (two transverse products cannot occupy the eight-product table)

Let `X,Y,Z` be vector spaces over a characteristic-zero field and put
`W=X direct-sum Y direct-sum Z`.  There do not exist `u,r,q,v in W` for
which

```text
P(u,u,r)=P(u,u,v)=P(u,r,v)=0,
P(u,q,v)=P(r,q,v)=P(q,v,v)=0,                       (19)

P(u,r,q)=T_0!=0,
P(u,v,v)=T_1!=0,                                    (20)
```

with `T_0,T_1` decomposable and fully transverse.

#### Proof

A vector supported in one source has zero square, so `v` uses two or three
source summands.

### 3.1 The repeated vector uses two sources

After permuting sources, write

```text
v=x+y,                     0!=x in X, 0!=y in Y.    (21)
```

The second tensor in (20) is

```text
P(u,v,v)=2 x tensor y tensor u_Z.                   (22)
```

Put `z=u_Z!=0`; the three factor lines of `T_1` are `x,y,z`.  The zero
`P(u,u,v)=0` gives

```text
x tensor u_Y+u_X tensor y=0,                        (23)
```

so, for one scalar `lambda`,

```text
u=lambda(x-y)+z.                                    (24)
```

For any `h=(h_X,h_Y,h_Z)`, direct expansion cancels the `lambda` terms and
gives

```text
P(u,h,v)
 =(x tensor h_Y+h_X tensor y) tensor z.             (25)
```

The two zeros in (19) involving `(u,-,v)` therefore put

```text
r=mu(x-y)+c,             q=nu(x-y)+d,
c,d in Z.                                           (26)
```

The zero `P(q,v,v)=0` forces `d=0`.  Since `P(u,r,q)!=0`, one has
`nu!=0`.

If `lambda=0`, then `u=z` is pure.  The only surviving part of
`P(u,r,q)` is a scalar multiple of `x tensor y tensor z`, so it is zero or
shares all three factor lines with `T_1`, contrary to (20).

If `lambda!=0`, the zero `P(u,u,r)=0` is

```text
lambda c+2 mu z=0                                  (27)
```

after removing the common nonzero scalar and the fixed `x tensor y`
factor.  Thus `c` lies on `z`; again `P(u,r,q)` is zero or lies on
`x tensor y tensor z`.  It cannot be fully transverse to `T_1`.  The
two-source case is impossible.

### 3.2 The repeated vector uses all three sources

Write

```text
v=x+y+z,                    xyz!=0.                  (28)
```

The tensor `P(u,v,v)` lies in the Segre tangent space at
`x tensor y tensor z`.  A nonzero decomposable tensor in that tangent
space shares at least two base factor lines.  Permute sources so that it has
the form

```text
P(u,v,v)=xi tensor y tensor z.                      (29)
```

Quotienting (29) by the lines `y,z` gives

```text
u_Y=beta y,             u_Z=gamma z,
xi=u_X+(beta+gamma)x.                               (30)
```

The zero `P(u,u,v)=0` becomes

```text
(beta+gamma)u_X+beta gamma x=0.                     (31)
```

If `u` is not pure, (31) makes

```text
u=(alpha x,beta y,gamma z),
alpha beta+alpha gamma+beta gamma=0,                (32)
```

with all three scalars and all three pairwise sums nonzero.  For an arbitrary
`h`, the equation `P(u,h,v)=0` is

```text
(beta+gamma) h_X tensor y tensor z
 +(alpha+gamma) x tensor h_Y tensor z
 +(alpha+beta) x tensor y tensor h_Z=0.             (33)
```

Successive quotients by `x,y,z` put every component of `h` on the
corresponding base line.  Applying this to `r,q` shows that
`P(u,r,q)` is zero or a multiple of `x tensor y tensor z`, contradicting
full transversality.

It remains that `u` is pure.  After another source permutation, write

```text
u=a in X.                                           (34)
```

For any `h`,

```text
P(u,h,v)=a tensor(h_Y tensor z+y tensor h_Z).       (35)
```

The two mixed zeros in (19) give

```text
r=(A,lambda y,-lambda z),
q=(B,mu y,-mu z).                                   (36)
```

The zero `P(q,v,v)=0` forces `B=0`.  Nonvanishing of `P(u,r,q)` forces
`mu!=0`.  Finally

```text
P(r,q,v)=-2 lambda mu x tensor y tensor z,          (37)
```

so its vanishing gives `lambda=0`.  Then `r` and `u` are both pure in
`X`, making `P(u,r,q)=0`, the last contradiction.  All source-support cases
are exhausted, proving the lemma.  QED.

## 4. Exclusion of the split-lift cell

Apply Lemma 1 to (16)--(17) with

```text
(u,r,q,v)=(g_0,g_1,g_2,g_3),
(T_0,T_1)=(T_d,T_t).                                (38)
```

Every zero in (19) appears in (16), both nonzero products in (20) appear in
(17), and `T_d,T_t` are fully transverse.  This contradiction proves that
no surjective physical cross map `H:W->K` can satisfy (6).  Hence the exact
coordinate split-lift cell (2)--(5) is empty.

No numerical search, generic specialization, finite-field inference, or
pair-deck assumption enters the proof.

## 5. Proof-topology consequence

Inside the S2BR same-missing-colour `(2,2)` survivor, this theorem proves

```text
third-row rank two, kernel support one,
x=e_s, y=e_t, w=e_s,
C=e_d tensor e_d+e_s tensor e_s,
coordinate split-lift K of (5):                    IMPOSSIBLE.        (39)
```

The reusable algebraic leaf is stronger than the application: Lemma 1 is
rank-free and allows arbitrary finite-dimensional source spaces.  Extending
the cell exclusion requires deriving (5), or one of the other split-lift
normal forms, from the remaining target incidences rather than assuming it.

## 6. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_rank_two_coordinate_split_lift_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_rank_two_coordinate_split_lift_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_rank_two_coordinate_split_lift_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_rank_two_coordinate_split_lift_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_rank_two_coordinate_split_lift_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_rank_two_coordinate_split_lift_exclusion.py
```

The primary replay checks the derivative, kernel, row ranks, `U`, the eight
root-permanent coefficients, the direct quotient, the target reductions, and
all two-/three-source identities in Lemma 1 with SymPy.  The independent
no-import audit reverses tensor indexing, rebuilds the derivative and both
permanents with `Fraction` arithmetic, checks all 64 unordered basis products,
and separately replays the obstruction normal forms on exact rational
fixtures.  The arbitrary-vector quotient and rank-one arguments above are
the proof.

## Dependencies

- [Rank-four/rank-eight target-kernel atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_TARGET_KERNEL_ATLAS_AND_DISTINCT_MISSING_COLOUR_EXCLUSION_THEOREM.md)
- [Lower-joint-rank three-root derivative and torus census](BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_THREE_ROOT_DERIVATIVE_AND_TORUS_CENSUS_THEOREM.md)
- [Common-shore singleton-slice and empty-permanent compatibility](BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md)

## Scope boundary

```text
rank-free two-target eight-product obstruction:                PROVED;
displayed rank-four/rank-eight coordinate split-lift cell:     IMPOSSIBLE;
other same-missing-colour rank-two-third-row lifts:             OPEN;
third-row rank three / mixed / injective involved rows:         OPEN;
joint-rank-three and derivative-rank-seven target cells:        OPEN;
pair-deck regularity for surviving three-root cells:            OPEN;
other S2T components / S2Q pole strata:                         OPEN;
higher balanced orders:                                        OPEN;
all-balanced rank-drop branch:                                  OPEN;
global Krenn--Gu conjecture:                                    UNRESOLVED. (40)
```
