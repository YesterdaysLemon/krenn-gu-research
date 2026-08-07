# A fifteenth pure `P_4` component from a disjoint secant kernel

## Status

**Exact characteristic-zero classification and component theorem.**  Suppose
a nonzero pure `P_4` restriction has an exact rank-two pair whose kernel line
is secant to the Segre quadric at two genuine zero products with disjoint
two-coordinate supports.  Then the opposite-plane purity problem is a pair
of complementary hyperbolic forms.

Its two maximal strata are exchanged by swapping the opposite modes.  Their
closures contain every smaller disjoint-secant stratum.  Restoring the two
binary source ratios gives a generically smooth six-dimensional irreducible
component with pair profile

```text
(r_01,r_02,r_03,r_12,r_13,r_23)=(2,3,4,3,4,4).     (1)
```

The sorted profile `(2,3,3,4,4,4)` matches the earlier six-dimensional
lower-pair component, but its rank-two kernel supports form a disjoint
`2+2` partition rather than an overlapping `1+3` center.  This invariant
separates the two.  Dimension separates the five-dimensional full-support
tangent component.  Hence the repository now certifies at least fifteen
symmetry-inequivalent pure-`P_4` component orbits.

The overlapping secant center is subsequently identified with the earlier
sixfold in
[`P4_OVERLAPPING_SECANT_LOWER_PAIR_CLASSIFICATION.md`](../overlapping-secant-lower-pair/P4_OVERLAPPING_SECANT_LOWER_PAIR_CLASSIFICATION.md).
Support-one secants are subsequently placed in this component's closure in
[`P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md`](../../../boundaries/pair-geometry/support-one-secant/P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md).
The component's generic marked `H31` fibre is subsequently proved empty in
[`P5_H31_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md`](../../../../../P5_H31_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md).
Its generic weighted `H22` fibre is subsequently proved empty in
[`P5_H22_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md`](../../../../../P5_H22_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md).
The full pure-`P_4` component exhaustiveness problem away from the
lower-pair locus and the global Krenn--Gu conjecture remain open.

## Two complementary hyperbolic planes

On the source blocks `{0,1}` and `{2,3}`, choose opposite binary directions

```text
a=X_0+sX_1,       a_bar=X_0-sX_1,
b=X_2+tX_3,       b_bar=X_2-tX_3.                  (2)
```

The secant pair is

```text
U_0=span(a,b),       U_1=span(a_bar,b_bar),         (3)
```

with kernel products `a*a_bar=0` and `b*b_bar=0`.  Its two cross-products are

```text
q=a*b_bar,       r=b*a_bar.                         (4)
```

Let `Q,R` be their top-degree catalecticant forms on the opposite source
rows.  Then

```text
P=span(a,b_bar),       K=span(a_bar,b),

rad(Q)=K,       Q|P is hyperbolic,
rad(R)=P,       R|K is hyperbolic.                  (5)
```

For opposite planes `A=U_2,B=U_3`, purity must select exactly one of the two
cross-products in (4).  Up to swapping rows in the secant pair, it is
equivalent to

```text
Q(A,B)=0,
rank(R|A x B)=1 nonzero.                            (6)
```

This is a double-Witt problem, not a permanent system.

## The flag classification

Let `pi_P,pi_K` be projection along the decomposition `R_1=P direct_sum K`,
and put

```text
p_A=dim pi_P(A),       p_B=dim pi_P(B).
```

The first condition in (6) and nondegeneracy on the two-dimensional `P` give

```text
p_A+p_B<=2.                                           (7)
```

The second condition says that both `K` projections are nonzero and at least
one is a line.  The maximal case has

```text
p_A=p_B=1,
pi_P(B)=pi_P(A)^perp_Q,
dim pi_K(A)=1,       dim pi_K(B)=2,                 (8)
```

or the mode-swapped alternative.  Choose the four flag parameters
`lambda,m,n,rho` and write

```text
ell=a+lambda b_bar,        ell_bar=a-lambda b_bar,
k=a_bar+m b,
k_bar=b+n a_bar.                                      (9)
```

Then the first maximal branch is

```text
A=span(k,ell),
B=span(k_bar,ell_bar+rho a_bar).                    (10)
```

Here `ell,ell_bar` are polar lines in `P`; `A` has a line as its `K`
projection, while `B` has full `K` projection when `rho!=0`.  Formula (6)
is immediate from (5).

If one `P` projection vanishes, that plane is `K` and the other plane has
line `K` projection.  It is a limit of the opposite maximal branch: add a
small polar `P` direction to the plane approaching `K` while keeping the
other `K` projection a line.  If both `P` projections are lines but both
`K` projections are lines, the tuple is the intersection of the two maximal
branches.  The cases `(p_A,p_B)=(0,2),(2,0)` are obtained by letting the
appropriate polar line fill its graph chart.  Thus the two mode-swapped
closures of (10) exhaust the disjoint-secant purity locus.

## Exact pure family

Take the six parameters

```text
(s,t,lambda,m,n,rho).                               (11)
```

Equations (2), (3), (9), and (10) define four planes.  Direct expansion
leaves only

```text
T_1000=-4st(mn+1),
T_1001=-4m rho st.                                  (12)
```

Hence

```text
P_4|U=-4st y_0x_1x_2((mn+1)x_3+m rho y_3).          (13)
```

The family is nonzero and pure on a dense open set.

## Smooth component certificate

Use pivot-`02` Grassmann charts.  Row reduction gives

```text
U_0: (s,0,0,t),
U_1: (-s,0,0,-t),

U_2:
( s(-lambda-m)/(lambda-m), 2lambda m t/(lambda-m),
  2s/(lambda-m),            t(-lambda-m)/(lambda-m)),

U_3, with D=lambda n+rho+1:
( s(-lambda n-rho+1)/D, 2lambda t/D,
 -2ns/D,                    t(-lambda n+rho+1)/D).   (14)
```

At

```text
(s,t,lambda,m,n,rho)=(1,2,3,4,5,6),                (15)
```

the family-chart Jacobian has rank six.  Rows

```text
(0,3,8,9,12,14)                                    (16)
```

give a six-by-six minor of determinant

```text
48/1331.                                            (17)
```

Anchor the target Segre chart at `1000`.  After row reduction, the twenty
plane/target coordinates are

```text
(1,0,0,2,  -1,0,0,-2,
 7,-48,-2,14,  -10/11,6/11,-5/11,-8/11,
 0,0,-1/3,9/29).                                   (18)
```

The fifteen universal Segre-incidence equations vanish there.  Their
Jacobian has rank fourteen; rows `0,...,13` and columns

```text
(0,1,...,11,16,17)                                 (19)
```

give determinant

```text
136141760102400/19487171.                           (20)
```

Thus the incidence is smooth of dimension `20-14=6` at (15).  The
irreducible family has six independent directions through the same point,
so its closure is the unique local irreducible component.  Projection away
from the unique nonzero target Segre point preserves the component.

## Why this is component fifteen

At a generic family point, (1) holds.  The rank-two kernel intersects the
Segre quadric in the reduced points

```text
[a tensor a_bar],       [b tensor b_bar],            (21)
```

whose support pairs `{0,1}` and `{2,3}` are disjoint.  In the earlier
six-dimensional lower-pair component, the corresponding support pairs meet
in one coordinate.  Secant/tangent type and the intersection cardinality of
the two zero-product supports are invariant under source-coordinate
permutations, diagonal scaling, row-basis changes, and mode permutations.

Every earlier fivefold has a different generic rank profile, except the
full-support tangent component, which is separated by dimension and kernel
type.  The embedded-`P_3` and equal-support sixfolds also have different pair
profiles.  Therefore (10) supplies a new symmetry orbit.

## Across the mathematical fence

The classification is a pair of opposite Witt decompositions.  The secant
kernel supplies two complementary hyperbolic planes `P,K`; purity asks for
orthogonal flags in `P` and a rank-one incidence in `K`.  The two maximal
branches are the two choices of which opposite plane has line `K`
projection.

This is the geometry of orthogonal flag varieties and rank-one graph maps.
It explains both the six parameters and the mode-swapped branching before
any tensor coefficient is expanded.

## Verification

Run:

```text
uv run --with sympy python claims/p4/classifications/pair-geometry/disjoint-secant-lower-pair/verify_p4_disjoint_secant_lower_pair_component.py
python claims/p4/classifications/pair-geometry/disjoint-secant-lower-pair/audit_p4_disjoint_secant_lower_pair_component.py
```

The primary verifier derives (12), the chart formulas, both exact minors,
the pair profile, and the disjoint kernel supports.  The independent audit
uses dual-number subset-DP permanents and rational row reduction for both
Jacobians.  Neither performs a search.
