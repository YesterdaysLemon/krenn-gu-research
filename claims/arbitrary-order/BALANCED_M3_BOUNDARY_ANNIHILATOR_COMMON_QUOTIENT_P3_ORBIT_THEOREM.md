# Balanced `m=3` boundary-annihilator common-quotient `P_3` orbit theorem

## Status

**Exact characteristic-zero refinement of the coordinate-boundary left by
S2R.**  For a product functional annihilating all nine singleton slices of a
physical `m=3` common shore, the three contractions of the root--root blocks
form one vector

```text
beta=(beta_1,beta_2,beta_3).                         (1)
```

The same vector lies in the kernel of each of the three contracted
root--nonroot maps.  If `beta` is nonzero, the contracted empty companion
therefore factors through the **same binary quotient in all three modes**:

```text
(L_x tensor L_y tensor L_r)P_3
 = (bar L_x tensor bar L_y tensor bar L_r) Q_beta,

Q_beta=(q_beta tensor q_beta tensor q_beta)P_3,
q_beta:C^3 -> C^3/<beta>.                            (2)
```

The binary tensor `Q_beta` has a complete orbit classification determined
only by the coordinate support of `beta`:

```text
|support(beta)|=1  -> Q_beta=0;
|support(beta)|=2  -> Q_beta has tensor rank 3 (binary W orbit);
|support(beta)|=3  -> Q_beta has tensor rank 2 (binary GHZ orbit). (3)
```

Consequently, when a boundary product annihilator leaves exactly two target
colours nonzero, nonzero `beta` is forced to have full coordinate support and
all three contracted cross maps have rank two.  More sharply, for each of
the two surviving target colours, the `3 x 3` matrix of contracted cross
entries across roots and nonroots has rank one and no zero entry; the missing
target-colour matrix is zero.  When exactly one target colour remains, at
least one cross map has rank one.  A zero target contraction with three
rank-two cross maps forces `beta` onto a coordinate line.

This is not an exclusion of the surviving binary case.  It isolates that
case as a common full-support quotient of `P_3`, and separates it from the
`beta=0` root--root degeneration and from rank-one cross-map degenerations.
It does not classify which such data extend to a target-consistent full
sensor, exclude any of the three S2Q pole strata, treat `m>=4`, exclude the
all-balanced rank-drop branch, or resolve the conjecture.  Global Krenn--Gu
remains **UNRESOLVED**.

## 1. The common kernel forced by the singleton equations

Work over `C`.  Use the physical common-shore notation of the
[`m=3` singleton-slice theorem](BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md).
Let

```text
a=a_1 tensor a_2 tensor a_3
```

be a nonzero decomposable root functional annihilating the total singleton
span `U`.  Contract the three root--root blocks and put

```text
beta_1=(a_2 tensor a_3)(B_23),
beta_2=(a_1 tensor a_3)(B_13),
beta_3=(a_1 tensor a_2)(B_12).                       (4)
```

For each nonroot `u in {x,y,r}`, define

```text
ell_(i,u)=W_(i,u)(a_i,-),
L_u:C^3 -> A_u^*,          L_u(e_i)=ell_(i,u).       (5)
```

Here `A_u` is the ternary colour space at `u`; the source basis of `L_u`
records which root is paired to `u`.

### Lemma 1 (one common source-kernel vector)

Every singleton equation is equivalent to

```text
L_x(beta)=L_y(beta)=L_r(beta)=0.                     (6)
```

### Proof

The colour-`c` singleton slice at `u` is

```text
h_(1,u)^(c) tensor B_23
+ insert_2(B_13,h_(2,u)^(c))
+ B_12 tensor h_(3,u)^(c).                          (7)
```

Contracting (7) by `a_1 tensor a_2 tensor a_3` gives

```text
beta_1 ell_(1,u)(e_c)
+ beta_2 ell_(2,u)(e_c)
+ beta_3 ell_(3,u)(e_c).                            (8)
```

The functional `a` annihilates all three colour slices at `u`, so (8)
vanishes for `c=0,1,2`.  Those three scalar equations say precisely
`L_u(beta)=0`.  Applying the same argument at all three nonroots proves
(6).  QED.

If `beta!=0`, (6) uniquely factors every map in (5) as

```text
L_u=bar L_u q_beta,
q_beta:C^3 -> C^3/<beta>.                            (9)
```

The six cross matchings in the physical empty companion give

```text
a(G_N)=(L_x tensor L_y tensor L_r)P_3.              (10)
```

Substitution of (9) proves the common-quotient identity (2).  Notice that
this is stronger than merely knowing that the three maps have rank at most
two: their kernel lines contain the **same** vector, whose coordinates come
from the root--root blocks.

## 2. Exact orbit of the common binary quotient

Let `H_beta=beta^perp` be the dual plane to `C^3/<beta>`.  The tensor
`Q_beta` is equivalently the restriction of the permanent trilinear form
`P_3` to

```text
H_beta tensor H_beta tensor H_beta.                 (11)
```

After permuting source coordinates and scaling, write

```text
beta=(1,A,B).
```

A basis of `H_beta` is

```text
u=(-A,1,0),              v=(-B,0,1).                (12)
```

In the binary basis `(u,v)` in every mode, direct expansion gives

```text
Q_000=Q_111=0,
Q_001=Q_010=Q_100=-2A,
Q_011=Q_101=Q_110=-2B.                              (13)
```

### Theorem 2 (support-orbit trichotomy)

For nonzero `beta`, the alternatives in (3) hold.

### Proof

If `beta` has support one, then `A=B=0` in a suitable chart and (13) is
zero.  This is also the elementary fact that three vectors in one coordinate
plane cannot occupy all three source coordinates in a permanent term.

If `beta` has support two, exactly one of `A,B` is nonzero.  Up to a nonzero
scalar, (13) is

```text
e_0 tensor e_0 tensor e_1
+ e_0 tensor e_1 tensor e_0
+ e_1 tensor e_0 tensor e_0.                        (14)
```

Thus its rank is at most three.  Every binary flattening has rank two, so it
is not decomposable.  If it had tensor rank two, concision would make the two
factor pairs independent in every mode and hence make it locally equivalent
to `Delta_2`.  But the Cayley hyperdeterminant of (14) is zero, whereas that
of `Delta_2` is nonzero.  Its rank is therefore exactly three.

Finally suppose `beta` has support three, so `A B!=0`.  The Cayley
hyperdeterminant of (13) is

```text
-48 A^2 B^2 !=0.                                    (15)
```

The elementary `2 x 2 x 2` matrix-pencil criterion says that a binary tensor
has nonzero hyperdeterminant exactly when it is in the open local-`GL(2)^3`
orbit of `Delta_2`: the determinant pencil has two distinct roots, whose two
rank-one eigendirections give the two product terms.  Hence `Q_beta` has
tensor rank two.  This proves all three cases.  QED.

The coefficients and invariant in (13)--(15) are polynomial identities over
`Z`.  The orbit statement is used over `C`, which is the field of the prize
problem; the same classification holds after algebraic closure over any
characteristic-zero field.

## 3. Consequences for target-coordinate boundary points

Assume now that the physical shore is target-consistent and has empty
normalization.  By S2R, contraction modulo the singleton span gives

```text
(L_x tensor L_y tensor L_r)P_3
 = sum_(c=0)^2 kappa_c x_c tensor y_c tensor r_c,

kappa_c=product_(i=1)^3 a_i(e_(i,c)).                (16)
```

Let

```text
t=number of nonzero kappa_c.                         (17)
```

The right side of (16) has tensor rank and every flattening rank equal to
`t`.

### Corollary 3 (the nonzero-`beta` boundary table)

Suppose `beta!=0`.

1. `t=3` is impossible, since every `L_u` has rank at most two.  The full
   S2R theorem also excludes this case when `beta=0`.
2. If `t=2`, then

   ```text
   rank L_x=rank L_y=rank L_r=2,
   |support(beta)|=3.                                (18)
   ```

3. If `t=1`, then `|support(beta)|>=2` and at least one of the three maps
   `L_u` has rank one.
4. If `t=0` and all three maps `L_u` have rank two, then
   `|support(beta)|=1`.  Equivalently, for support two or three, a zero
   target contraction forces at least one cross map to have rank at most
   one.

### Proof

For `t=2`, each target flattening has rank two, so every `L_u` has rank at
least two.  Equation (6) gives the reverse inequality.  Thus every induced
map `bar L_u` in (9) is invertible and tensor rank is preserved.  Theorem 2
then forces `Q_beta` to be the rank-two, full-support case.

For `t=1`, `Q_beta` cannot be zero.  If all three `L_u` had rank two, all
three induced binary maps would be invertible and Theorem 2 would give tensor
rank two or three, not one.  Hence at least one has rank one.

For `t=0`, three rank-two maps again make the induced maps invertible, so
`Q_beta=0`; Theorem 2 gives support one.  The `t=3` statement follows already
from flattening rank.  QED.

### Corollary 4 (rank-one cross matrices on the binary branch)

Continue with `t=2`, and call the surviving target colours `p,q` and the
missing colour `d`.  Define three root-by-nonroot scalar matrices

```text
M_c[i,u]=a_i(W_(i,u)(-,e_(u,c))),
i in {1,2,3}, u in {x,y,r}.                           (19)
```

Then

```text
M_d=0,
rank M_p=rank M_q=1,                                 (20)
```

and every entry of `M_p,M_q` is nonzero.  There are two fixed independent
fully supported vectors

```text
rho_p,rho_q in beta^perp subset C^3                 (21)
```

and nonzero scalars `gamma_(u,c)` such that the source covector giving the
colour-`c` output of `L_u` is

```text
(M_c[1,u],M_c[2,u],M_c[3,u])
 = gamma_(u,c) rho_c,              c in {p,q}.        (22)
```

After writing `beta=(1,A,B)` and choosing a primitive cube root
`omega`, the two fixed lines may be represented in the plane basis (12) by

```text
(1,(A/B) omega),       (1,(A/B) omega^2).             (23)
```

### Proof

The mode-`u` flattening image of the right side of (16) is the coordinate
plane `span(e_p,e_q)`.  It is contained in `image L_u`; both spaces have
dimension two by Corollary 3, so they are equal.  This proves `M_d=0`.

The rank-two binary tensor `Q_beta` is concise.  Its two-term product
decomposition is unique up to rescaling and exchanging its terms: after one
mode is flattened, the two rank-one matrix directions are the two distinct
roots of its determinant pencil, and the other two factor lines are then
forced.  Pulling the two displayed diagonal terms of (16) back through the
three invertible maps `bar L_u` therefore gives the same two input lines in
`beta^perp` at every nonroot.  Equivalently, (22) holds.  Hence both matrices
in (20) are outer products and have rank one.

For a direct coordinate check, substitute vectors `(1,s)` and `(1,t)` in
(13).  The two mixed polar values vanish, with `s!=t`, exactly when

```text
s+t=-A/B,                st=A^2/B^2.                 (24)
```

The roots are the two vectors in (23).  They are independent and all three
coordinates of their lifts through (12) are nonzero when `A B!=0`; thus the
two vectors in (21) are fully supported.

Finally, the pure target coefficients are

```text
kappa_c=per(M_c)
       =6 product_i rho_c[i] product_u gamma_(u,c) !=0. (25)
```

Every factor in (25) is therefore nonzero.  QED.

The only nonzero-`beta` boundary capable of retaining a concise binary target
is therefore

```text
one missing target colour;
three rank-two cross maps with one common kernel line;
that kernel generator beta has all three source coordinates nonzero;
each surviving-colour root-by-nonroot contraction matrix is
  fully supported and rank one;
the common quotient of P_3 is in the Delta_2 orbit.  (26)
```

This is an exact reduction, not a contradiction: a full-support common
quotient of `P_3` really is binary GHZ.  Any exclusion must use the way
`beta`, the missing target coordinate, the three local root functionals, and
the remaining singleton/full-sensor equations arise from the **same physical
blocks**.

## 4. Remaining boundary and proof topology

The coordinate-boundary obligation left by S2R now splits as follows:

```text
beta != 0, exactly two target colours survive
  -> common full-support binary P3 quotient (26);       OPEN physically;

beta != 0, exactly one target colour survives
  -> at least one contracted cross map has rank one;    OPEN;

beta != 0, no target colour survives
  -> coordinate-line beta or a rank-one cross map;      OPEN;

beta = 0
  -> all three root--root contractions vanish;          OPEN;

all three target colours survive
  -> impossible by S2R;                                 PROVED;

three S2Q pole strata:                                  OPEN;
higher balanced order and all-rank-drop branch:         OPEN;
global Krenn--Gu conjecture:                            UNRESOLVED.       (27)
```

The binary-GHZ quotient in (19) and the lower-rank branches may overlap in
closures, but their generic rank statements are disjoint.  No component
exhaustion of the product-annihilator variety is claimed.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_boundary_annihilator_common_quotient_p3_orbit.py
python -I claims/arbitrary-order/audit_balanced_m3_boundary_annihilator_common_quotient_p3_orbit.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_boundary_annihilator_common_quotient_p3_orbit.py claims/arbitrary-order/audit_balanced_m3_boundary_annihilator_common_quotient_p3_orbit.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_boundary_annihilator_common_quotient_p3_orbit.py claims/arbitrary-order/audit_balanced_m3_boundary_annihilator_common_quotient_p3_orbit.py
```

The primary replay expands the physical singleton contraction, reconstructs
the common-kernel equation, computes all eight binary quotient coefficients,
verifies the three support cases, flattenings, and hyperdeterminant, and
checks the two common diagonalizing lines symbolically.  The independent
no-import audit uses exact `Fraction` arithmetic, a separate sparse permanent
tensor, direct quotient-plane evaluation, separate Gaussian elimination, a
separately coded Cayley invariant, and its own arithmetic in
`Q[omega]/(omega^2+omega+1)`.  The support exhaustion, uniqueness, and rank
implications are the written proof above.

## Dependencies

- [`BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md`](BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md)
- [`BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md`](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
- [`P3_ZERO_HYPERPLANE_PRODUCT_THEOREM.md`](../p3/restrictions/P3_ZERO_HYPERPLANE_PRODUCT_THEOREM.md)
- [`P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md`](../p3/restrictions/P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md)
