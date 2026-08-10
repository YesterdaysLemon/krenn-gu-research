# Legal nonroot switching is a cofactor gauge, and the fixed-sensor uniform curve misses even border rank eight

## Status

**Exact characteristic-zero covariance theorem and symbolic P7 exclusion.**
There are two distinct multiplicative deformations of the committed legal
five-root sensor, and separating them closes a useful part of the current
GHZ/Hessian boundary.

1. Simultaneously switch every edge incident to a nonroot `u` by a nonzero
   factor `z_u`.  The legal companion map changes only by invertible diagonal
   column scaling, its image is unchanged, every shallow Hessian is changed by
   diagonal congruence, and the full five-root tensor changes only by the
   common scalar `product_u z_u`.  Thus the nonroot switching torus is a
   **projective gauge orbit**.  It cannot move a legal sensor into or out of
   GHZ incidence and cannot cross a Hessian discriminant.
2. Keep the committed companion blocks fixed and give every nonroot--nonroot
   edge the same weight `t`.  This is not the gauge deformation in item 1.
   On this physical one-parameter curve, two named maximal minors of the
   `(roots 0,1)|(roots 2,3,4)` flattening have coprime primitive factors.
   Consequently, for every `t!=0` over every characteristic-zero field, the
   flattening has rank exactly nine.  The tensor has border rank at least nine
   while all nine eight-shore hafnian Hessians are invertible.

Therefore the committed legal sensor has an entire common-Hessian-open
physical curve, and its full nonroot switching gauge saturation, which is
disjoint not only from the torus-concise rank-three orbit but from the whole
border-rank-at-most-eight variety.  Any physical GHZ point for this sensor
must break common nonroot edge uniformity; switching a uniform point cannot
repair it.

This is a genuine family exclusion, not a conclusion from the previously
checked point `t=1`.  It neither excludes nonuniform physical graphs nor proves
that the legal secant intersection contains no physical point.  `P_7` and the
global Krenn--Gu conjecture remain **UNRESOLVED**.

The fixed legal matching companions are those in
[`P7_FULL_MIXED_ROOT_219_LABEL_SENSOR_AND_PINNED_STAR_GATING_BOUNDARY.md`](P7_FULL_MIXED_ROOT_219_LABEL_SENSOR_AND_PINNED_STAR_GATING_BOUNDARY.md).
The prior one-point control and radial jet theorem are in
[`ARBITRARY_HAFNIAN_JET_LINE_PROJECTIVE_AFFINE_SEPARATION_AND_P7_GHZ_BOUNDARY.md`](../arbitrary-order/ARBITRARY_HAFNIAN_JET_LINE_PROJECTIVE_AFFINE_SEPARATION_AND_P7_GHZ_BOUNDARY.md).
Ordinary flattening rank as a secant obstruction is part of the standard
tensor toolkit surveyed by Bernardi et al.,
[*Hitchhiker guide to: Secant varieties and tensor decomposition*](https://arxiv.org/abs/1812.10267).
The one-parameter maximal-minor saturation used below is elementary Euclidean
algebra over `Q[t]`; no secant classification is imported.

## 1. Arbitrary-order hafnian switching covariance

Let `Q` have even order

```text
q=2m,              E=binom(Q,2),             n=|E|.  (1)
```

For a symmetric loopless weighted graph `A=(a_ij)` and
`z=(z_i:i in Q)` in `(K^*)^Q`, define its vertex switch by

```text
a_ij^z=z_i z_j a_ij.                                 (2)
```

Write

```text
h=haf A,
c_e=haf A[Q minus e],
D_ef=haf A[Q minus (e union f)]  for e,f disjoint,
D_ef=0                              otherwise.         (3)
```

Put

```text
Z=product_(i in Q) z_i,
z_e=z_i z_j for e={i,j},
S=diag(z_e:e in E).                                  (4)
```

Every perfect matching on an even set uses each vertex exactly once, so for
every even `I subset Q`,

```text
haf A^z[I]=(product_(i in I)z_i) haf A[I].            (5)
```

### Theorem 1 (hafnian cofactor gauge covariance)

The scalar, gradient, and Hessian decks transform as

```text
h^z=Z h,
c^z=Z S^(-1)c,
D^z=Z S^(-1) D S^(-1).                               (6)
```

Consequently

```text
det D^z
 =Z^(n-2(q-1)) det D
 =Z^((q-1)(q-4)/2) det D.                            (7)
```

On `det D!=0`, the Hessian reconstruction is equivariant:

```text
(m-1)(D^z)^(-1)c^z
 =S (m-1)D^(-1)c.                                    (8)
```

Thus switching preserves the Hessian open and returns exactly the switched
edge vector.

### Proof

Equation (5) applied to the three deletion depths gives (6).  Every vertex
occurs in `q-1` edges, hence

```text
product_(e in E) z_e=Z^(q-1).                         (9)
```

Taking the determinant in (6) gives

```text
det D^z=Z^n det(S)^(-2)det D=Z^(n-2(q-1))det D,
```

and `n-2(q-1)=(q-1)(q-4)/2`.  Inverting the last equation of
(6) proves (8).  All statements are identities in Laurent polynomials and
therefore hold over every field on which the displayed nonzero switches are
defined; characteristic zero is used later for the coprimality certificate.

For a P7 eight-shore `U_p`, equation (7) specializes to

```text
delta_p(A^z)=Z_p^14 delta_p(A),
Z_p=product_(u in U_p)z_u.                            (10)
```

Thus all nine Hessian opens, all recovered-overlap equations, and physical
hafnian realization move covariantly under the nine-vertex switching torus.

## 2. Switching the legal companion map

Let `R` be the five roots and `N` the nine nonroots.  For the full mixed-root
expansion, the deletion/matched label `D subset N` has size `5`, `3`, or `1`.
Write

```text
G_D in tensor_(i in R) V_i^*,
C_D=haf A[N minus D],
T_R=sum_D G_D C_D.                                    (11)
```

Here `G_D` is the matching aggregate made from root--nonroot forms and zero,
one, or two root--root blocks.  The labeled legal sensor has the columns
`G_D`:

```text
Gamma:C |-> sum_D G_D C_D.                            (12)
```

Switch the legal graph blocks by

```text
h_(i,u)^z=z_u h_(i,u),
L_ij^z=L_ij,
a_uv^z=z_u z_v a_uv.                                 (13)
```

All root contractions that were zero remain zero, all active blocker
contractions remain nonzero, transpose symmetry is preserved, and residual
nonblockers stay residual.  Hence (13) is a legal deformation.

Put

```text
z_D=product_(u in D)z_u,
Z_N=product_(u in N)z_u,
S_z=diag(z_D:|D| in {5,3,1}).                         (14)
```

### Theorem 2 (the nonroot switching torus is projectively vertical)

Under (13),

```text
G_D^z=z_D G_D,
C_D^z=(Z_N/z_D)C_D,                                  (15)

Gamma_z=Gamma S_z,
im Gamma_z=im Gamma,
rank Gamma_z=rank Gamma,                             (16)

C^z=Z_N S_z^(-1)C,
Gamma_z C^z=Z_N Gamma C.                             (17)
```

In particular, the full tensor has the same projective point and every
tensor flattening has the same rank.  The target-incidence Schubert condition
depends only on `im Gamma`, so it too is unchanged.

### Proof

Every matching contributing to `G_D` uses each member of `D` on exactly one
root--nonroot edge, proving the first equation in (15).  Equation (5) on the
complementary nonroot graph proves the second.  Equations (16)--(17) follow
immediately.  Equivalently, every perfect matching of the full graph covers
each of the nine nonroots once, so every full matching monomial acquires the
same factor `Z_N`.

This is the **nonroot cofactor gauge** terminology used in this note.  The
theorem shows why vertex switching cannot supply any missing projective
tangent or conormal direction at GHZ incidence: its differential is vertical
after projectivizing the full tensor.

## 3. The fixed-sensor uniform physical curve

Now do **not** switch the root--nonroot companion forms.  Freeze the committed
integer sensor `Gamma_leg`, and let `A(t)` be the graph on `N` with

```text
a_uv=t for every u!=v.                               (18)
```

For an even set of order `2k`,

```text
haf A(t)[I]=(2k-1)!! t^k.                             (19)
```

Therefore its named cofactor vector has constant values at each depth:

```text
C_D(t)=3t^2    if |D|=5,
C_D(t)=15t^3   if |D|=3,
C_D(t)=105t^4  if |D|=1.                             (20)
```

Let

```text
T_5=sum_(|D|=5)G_D,
T_3=sum_(|D|=3)G_D,
T_1=sum_(|D|=1)G_D.                                  (21)
```

The full root tensor is the quadratic matrix-curve lift

```text
tau(t)=3t^2 [T_5+5t T_3+35t^2 T_1].                  (22)
```

Flatten the tensor across roots `01|234`.  The nine rows are ordered

```text
00,01,02,10,11,12,20,21,22,                          (23)
```

and the 27 columns are ordered `000,...,222`.  After removing the common
factor `3t^2`, call the resulting `9 x 27` quadratic polynomial matrix
`F(t)`.  Let

```text
F_0(t)=columns 000,...,022,
F_1(t)=columns 100,...,122.                           (24)
```

Direct expansion of the fixed legal matching formulas gives

```text
det F_0(t)=50 P_0(t),
det F_1(t)= 5 P_1(t),                                (25)
```

where the primitive degree-18 coefficient vectors, from highest power to
constant term, are

```text
P_0:
[6662572822705733828125,
 -12156844565030088437500,
 -11656744567696429468750,
 -964481421579777390625,
 478062693786650000,
 -167575290444104681250,
 -329667083352597624375,
 -126033773134233295625,
 -41624665391857307375,
 -10418655620547901625,
 -1665030690056656225,
 -89100920096274400,
 15940043824280765,
 2548639126911280,
 87299980928535,
 -16019848623521,
 -841802234952,
 81773978676,
 628717584],                                         (26)

P_1:
[45743752916454884375000,
 -864588786885117896875000,
 -4116226358173090867343750,
 -7598683970980122418125000,
 -3401502493947155460953125,
 5913944738769560812265625,
 5334994427617131112718750,
 73876260872593498768750,
 -261544878332648570021250,
 -100449092973761054860625,
 -26721393305568752102250,
 -3351312997063601813625,
 -245913724965094499700,
 -10804647546463312425,
 -617591700542701835,
 3747499312421390,
 -129171904414652,
 -96822486970,
 36194813664].                                       (27)
```

The exact Euclidean algorithm in `Z[t]` gives

```text
gcd(P_0,P_1)=1.                                      (28)
```

The successive nonzero remainder degrees are

```text
17,16,15,...,2,1,0.                                  (29)
```

The primary replay constructs both symbolic determinants over `ZZ[t]` and
checks (25)--(29).  The independent no-import audit rebuilds the same tensor
as one fourteen-vertex polynomial hafnian.  Since every entry of `F(t)` has
degree at most two, each determinant has degree at most 18; agreement with
(26)--(27) at 19 named integers is therefore an exact characteristic-zero
polynomial-identity certificate.  Its separate rational Euclidean algorithm
then checks (28).  This is interpolation-based identity auditing, not a
parameter search and not finite-field evidence.

### Theorem 3 (uniform-curve secant saturation)

For every characteristic-zero field `K` and every `t in K^*`,

```text
rank Flat_(01|234)(tau(t))=9,
border-rank(tau(t))>=9.                              (30)
```

Moreover all nine eight-shore hafnian Hessians are invertible:

```text
D_p(t)=3t^2 KG(8,2),
det D_p(t)=(3t^2)^28 15(-5)^7 !=0.                   (31)
```

Thus the complete physical curve (18) is common-Hessian-open and disjoint
from `sigma_8`, hence in particular from the torus-concise part of
`sigma_3`.

### Proof

The actual maximal minors of the flattening of `tau(t)` are

```text
(3t^2)^9 det F_0(t)=984150 t^18 P_0(t),
(3t^2)^9 det F_1(t)= 98415 t^18 P_1(t).              (32)
```

By (28), Bezout's identity supplies `A,B in Q[t]` with

```text
A P_0+B P_1=1.                                       (33)
```

Equivalently, for the two actual maximal minors `M_0,M_1` in (32),

```text
(M_0,M_1):(t)^infinity=Q[t].                         (34)
```

This is the promised one-parameter secant-ideal saturation certificate.

Hence `P_0(t)` and `P_1(t)` cannot vanish simultaneously in any
characteristic-zero extension.  For `t!=0`, at least one maximal minor in
(32) is nonzero.  The flattening has nine rows, so its rank is exactly nine.
Every tensor of border rank at most eight has every ordinary flattening of
rank at most eight, proving (30).  Equation (31) follows from the known
Kneser spectrum

```text
15 (multiplicity 1), -5 (multiplicity 7), 1 (multiplicity 20).
```

At `t=1`, the first determinant in (32) is exactly the prior certificate

```text
-18494220325114867735328060700.                       (35)
```

The coprime second determinant is what upgrades that isolated point to the
whole punctured curve.

### Corollary 4 (switching saturation of the exclusion)

Apply (13) to the sensor and graph at any point `A(t)`, with all `z_u!=0`.
The resulting legal graph has

```text
a_uv^z=t z_u z_v,                                    (36)
```

all nine shore Hessians remain invertible by (10), and its full tensor is
`Z_N tau(t)` by (17).  Therefore its `01|234` flattening still has rank nine.

This corollary is a nine-parameter family of legal graph data but one
projective tensor gauge orbit over each `t`.  It must not be counted as a
nine-dimensional family of new projective target points.

## 4. Exact frontier

```text
arbitrary-order hafnian switching covariance:              PROVED;
Hessian determinant switching exponent:                    (q-1)(q-4)/2;
Hessian-open reconstruction under switching:                EQUIVARIANT;
legal five-root sensor image under nonroot switching:        INVARIANT;
full root tensor under nonroot switching:                    COMMON SCALAR;
nonroot switching supplies projective GHZ tangent direction: NO;
fixed-sensor uniform physical curve common-Hessian-open:     YES FOR t!=0;
two named maximal-minor primitive factors:                   COPRIME;
uniform-curve flattening rank:                               EXACTLY NINE;
uniform-curve tensor border rank:                            AT LEAST NINE;
switching saturation meets border rank <=8:                  NO;
nonuniform physical graph for committed sensor meets GHZ:    UNKNOWN;
arbitrary legal sensor physical GHZ point:                   UNKNOWN;
P7 nonrestriction:                                           UNKNOWN;
global Krenn--Gu conjecture:                                 UNRESOLVED. (37)
```

The remaining legal target-incidence problem is now transverse to two
explicit dead directions:

- pure radial rescaling of a candidate hafnian jet has at most one physical
  amplitude on the Hessian open, by the prior radial theorem;
- simultaneous nonroot vertex switching is projectively invisible, by
  Theorem 2 here.

A successful next invariant must therefore see a genuinely nonuniform
projective deformation of the physical deck.  Pulling additional secant or
Koszul-flattening equations back to the 36-edge nonroot graph, modulo this
switching gauge, is the exact surviving route.  The present maximal-minor
certificate does not establish that the resulting nonuniform ideal is the
unit ideal.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_legal_nonroot_switching_covariance_and_uniform_curve_secant_saturation.py
python claims/p7/audit_p7_legal_nonroot_switching_covariance_and_uniform_curve_secant_saturation.py
python -m py_compile claims/p7/verify_p7_legal_nonroot_switching_covariance_and_uniform_curve_secant_saturation.py claims/p7/audit_p7_legal_nonroot_switching_covariance_and_uniform_curve_secant_saturation.py
uv run --with ruff ruff check claims/p7/verify_p7_legal_nonroot_switching_covariance_and_uniform_curve_secant_saturation.py claims/p7/audit_p7_legal_nonroot_switching_covariance_and_uniform_curve_secant_saturation.py
```

The primary verifier reuses only the committed legal matching-column
implementation, constructs the two polynomial determinants over `ZZ[t]`,
checks their contents, primitive coefficient vectors, rational gcd, switching
covariance, and Hessian congruence.  The independent standard-library audit
imports no project or primary module.  It reconstructs all 243 tensor
coordinates directly by a fourteen-vertex polynomial hafnian recurrence,
checks the two degree-18 identities exactly, runs its own rational polynomial
Euclidean algorithm, and independently verifies full-matching switching
covariance.  Neither replay searches graphs, supports, decompositions,
parameters, or finite fields.
