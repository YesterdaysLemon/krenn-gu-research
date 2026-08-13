# Balanced `m=3` common-three-space annihilator-component trichotomy

## Status

**Exact characteristic-zero component reduction on the S2Q common-three-space
pole stratum.**  Let `U` be the total singleton span of a normalized,
target-consistent physical `m=3` common shore, and suppose

```text
dim U=3.                                               (1)
```

Every irreducible component of the product-annihilator section has dimension
at least three.  S2R puts every such component on the target coordinate
boundary, and S2S then gives the following exhaustive trichotomy:

1. the component is contained in at least two target-coordinate boundary
   divisors;
2. all three root--root contractions vanish identically on the component;
   or
3. generically exactly one target coordinate is missing, the root--root
   contraction vector is nonzero, and the three missing-colour cross-column
   spans have total dimension at most three.

In the third case the total dimension bound improves to two unless the
missing coordinate vector at the boundary root already belongs to that
root's cross-column span.  The two surviving-colour contracted cross matrices
are simultaneously fully supported and rank one by S2S.

This does not exclude any of the three branches.  The first contains the
target-diagonal sharp boundary from S2R, though that particular plane cannot
support a full sensor.  The second and third still require the remaining
physical target equations.  No rank-one or pair-plane S2Q stratum, `m>=4`,
all-balanced rank-drop branch, witness, counterexample, or global resolution
is claimed.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The product-annihilator section

Let the root spaces be `A_1,A_2,A_3`, each of dimension three, and put

```text
Sigma=Seg(P(A_1^*) x P(A_2^*) x P(A_3^*)) subset P(A^*),
A=A_1 tensor A_2 tensor A_3.                           (2)
```

The product-annihilator section of `U` is

```text
X=Sigma intersect P(U^perp).                          (3)
```

Since `Sigma` has dimension six and `P(U^perp)` has codimension three in
`P(A^*)`, the projective dimension theorem gives, for every irreducible
component `Z` of `X`,

```text
dim Z>=3.                                             (4)
```

S2R proves that `X` has no point in the root coordinate torus.  Thus

```text
X subset union_(i=1)^3 union_(c=0)^2 H_(i,c),
H_(i,c)={a_i(e_(i,c))=0}.                             (5)
```

Irreducibility and the finiteness of the union imply that every `Z` is
contained in at least one fixed divisor `H_(j,d)`.

For a product functional `a=a_1 tensor a_2 tensor a_3`, recall the S2S
root--root contraction vector

```text
beta(a)=(
 (a_2 tensor a_3)(B_23),
 (a_1 tensor a_3)(B_13),
 (a_1 tensor a_2)(B_12)).                             (6)
```

## 2. Cross-column maps at a missing target colour

Fix a target colour `d`.  At root `i`, collect the three physical cross-edge
columns with nonroot endpoint colour `d`:

```text
C_(i,d)=span{
 W_(i,x)(-,e_(x,d)),
 W_(i,y)(-,e_(y,d)),
 W_(i,r)(-,e_(r,d))} subset A_i,                     (7)

r_(i,d)=dim C_(i,d),
K_(i,d)=C_(i,d)^perp subset A_i^*.                   (8)
```

The vector-valued linear map

```text
F_(i,d):A_i^* -> C^3,
a_i |-> (
 a_i(W_(i,x)(-,e_(x,d))),
 a_i(W_(i,y)(-,e_(y,d))),
 a_i(W_(i,r)(-,e_(r,d))))                            (9)
```

has rank `r_(i,d)` and kernel `K_(i,d)`.

### Lemma 1 (dimension budget on a binary component)

Let `Z` be an irreducible component of `X` such that

```text
Z subset H_(j,d),
Z is contained in no other H_(i,c),
beta is not identically zero on Z.                    (10)
```

Then

```text
sum_(i=1)^3 r_(i,d) <=3.                              (11)
```

If moreover

```text
e_(j,d) notin C_(j,d),                               (12)
```

then

```text
sum_(i=1)^3 r_(i,d) <=2.                              (13)
```

### Proof

There is a dense open subset of `Z` on which exactly the coordinate in
(10) vanishes and `beta!=0`.  Thus exactly two target diagonal coefficients
survive.  Corollary 4 of S2S says that the missing-colour contracted cross
matrix is zero.  Equivalently,

```text
F_(i,d)(a_i)=0                         for i=1,2,3.   (14)
```

These are closed linear equations in each factor, so density promotes them
to all of `Z`.  Hence

```text
Z subset
 P(K_(1,d)) x P(K_(2,d)) x P(K_(3,d)),               (15)
```

with the `j`-th factor additionally cut by `a_j(e_(j,d))=0`.

Put

```text
k_i=dim K_(i,d)=3-r_(i,d).
```

The boundary equation on the `j`-th factor is redundant exactly when

```text
K_(j,d) subset e_(j,d)^perp,
```

which by double annihilation is equivalent to
`e_(j,d) in C_(j,d)`.  Let `epsilon=0` in that case and `epsilon=1`
otherwise.  The ambient product in (15), including the boundary equation,
has dimension

```text
sum_i(k_i-1)-epsilon
 =6-sum_i r_(i,d)-epsilon.                            (16)
```

Equations (4) and (16) give

```text
3 <= 6-sum_i r_(i,d)-epsilon,
```

or

```text
sum_i r_(i,d) <=3-epsilon.                            (17)
```

This is (11), and condition (12) makes `epsilon=1`, giving (13).  QED.

On the same dense open subset, S2S gives more than (14).  For each surviving
colour, the root-by-nonroot matrix (19) of that theorem is fully supported
and rank one.  Lemma 1 uses only the missing-colour half because that half
closes to fixed linear subspaces and yields the clean dimension budget.

## 3. Component trichotomy

### Theorem 2 (three exhaustive component types)

Every irreducible component `Z` of (3) satisfies at least one of:

```text
M: Z lies in H_(i,c) intersect H_(j,d)
   for two distinct coordinate divisors;

B: beta(a)=0 identically on Z;

C: Z lies in exactly one H_(j,d), beta is generically nonzero,
   and the missing-colour spans obey (11), sharpened to (13)
   under (12).                                         (18)
```

### Proof

Choose one divisor containing `Z` by (5).  If a second distinct divisor also
contains it, case M holds.  Otherwise exactly one does.  On that component,
the polynomial vector (6) either vanishes identically, giving B, or is
nonzero on a dense open subset.  In the latter case the hypotheses of
Lemma 1 hold and give C.  These alternatives are exhaustive.  QED.

The alternatives can overlap on special loci; the theorem is a case cover,
not a disjoint stratification.

## 4. Sharpness of the dimension arithmetic

The bounds in Lemma 1 cannot be improved by its dimension argument alone.
Fix `d=2` and `j=1`.

For the redundant-boundary case, take

```text
C_(1,2)=C_(2,2)=C_(3,2)=span(e_2).                   (19)
```

Every `r_(i,2)=1`; all three kernel planes are `e_2^perp`, and the selected
boundary is already automatic.  Their projective product has dimension
three, attaining (11) with equality.

For the independent-boundary case, take

```text
C_(1,2)=0,
C_(2,2)=span(e_0),
C_(3,2)=span(e_1).                                   (20)
```

The first kernel is all of `(C^3)^*` and the selected coordinate boundary
cuts it to a projective line; the other two kernels are projective lines.
Again the product has dimension three, now with total rank two, attaining
(13).

These are sharpness controls for the linear dimension budget.  They are not
asserted to be singleton spans, target-consistent shores, full sensors, or
graphs.

Case M is also genuinely needed geometrically.  For the target diagonal
plane

```text
D=span(e_(1,c) tensor e_(2,c) tensor e_(3,c):c=0,1,2), (21)
```

its product-annihilator equations are

```text
a_1[c]a_2[c]a_3[c]=0,                 c=0,1,2.       (22)
```

Every irreducible component chooses at least one coordinate divisor for each
colour and is therefore multi-boundary.  S2R already proves that `U=D` is
incompatible with full sensor rank under target consistency; (21) is a
sharpness example for the component geometry only.

## 5. Proof-topology consequence

The S2Q common-three-space branch now has the exact component cover

```text
product-annihilator component, dimension at least 3
  -> multi-coordinate boundary component;             OPEN;
  or root-root contraction beta identically zero;      OPEN;
  or one missing colour with total cross-column
       rank at most 3 (usually at most 2),
       plus two full-support rank-one colour matrices; OPEN.

common-three-space pole stratum:                       NOT EXCLUDED;
rank-one and pair-plane pole strata:                   NOT ADDRESSED;
higher balanced orders / all-rank-drop:                OPEN;
global Krenn--Gu conjecture:                           UNRESOLVED.       (23)
```

The next exact obligation is no longer an arbitrary boundary-component
search: it is to combine cases M, B, and C with full sensor rank and the
uncontracted physical target equations.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_annihilator_component_trichotomy.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_annihilator_component_trichotomy.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_annihilator_component_trichotomy.py claims/arbitrary-order/audit_balanced_m3_common_three_space_annihilator_component_trichotomy.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_annihilator_component_trichotomy.py claims/arbitrary-order/audit_balanced_m3_common_three_space_annihilator_component_trichotomy.py
```

The primary replay checks the kernel/span duality, all integer dimension
budgets, both sharp rank configurations, and the diagonal multi-boundary
control with SymPy.  The independent no-import audit reconstructs those
calculations with exact `Fraction` row reduction and a separate coordinate
model.  Projective dimension, irreducibility, density, and the exhaustive
case split are the written proof above.

## Dependencies

- [`BALANCED_M3_FULL_SENSOR_SEPARATED_SINGLETON_POLE_LOCALIZATION_THEOREM.md`](BALANCED_M3_FULL_SENSOR_SEPARATED_SINGLETON_POLE_LOCALIZATION_THEOREM.md)
- [`BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md`](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
- [`BALANCED_M3_BOUNDARY_ANNIHILATOR_COMMON_QUOTIENT_P3_ORBIT_THEOREM.md`](BALANCED_M3_BOUNDARY_ANNIHILATOR_COMMON_QUOTIENT_P3_ORBIT_THEOREM.md)
