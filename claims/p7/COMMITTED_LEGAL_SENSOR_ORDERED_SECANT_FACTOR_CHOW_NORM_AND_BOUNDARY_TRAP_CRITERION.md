# Committed legal sensor: ordered secant--factor Chow/norm and boundary-trap criterion

## Status

**Exact characteristic-zero decision criterion; committed-sensor outcome not yet
computed.**  This note turns the mandatory intersection from
`LEGAL_P7_SECANT_FACTOR_CODIMENSION_BARRIER_AND_ARTINIAN_PAIR_IDEAL_REDUCTION.md`
into a structured finite calculation.  It does not enumerate labels,
quadruplets, tensors, decompositions, or finite-field points.

The new reduction has three ingredients.

1. One fixed invertible row block of the committed `243 x 219` legal sensor
   replaces 219 free preimage variables by an adjugate formula.  Sensor-image
   membership is then exactly 24 multilinear residual equations.
2. The ordered rank-three secant parameter space has dimension 32, exactly the
   dimension of the third secant.  On its torus-concise open it is a six-sheeted
   cover, by Kruskal uniqueness.
3. The exact seven-variable two-factor ideal has codimension eight, degree 259,
   and a known finite generating set.  Pulling that ideal back through the
   adjugate preimage map produces the expected zero-dimensional scheme directly
   on the ordered parameter space.

A universal symbolic localization by one explicit product decides whether a
point survives in the torus-concise, simple, pair-nonzero, and pinned locus.
On the proper downstairs branch that localized quotient is finite.  If the
larger ordered pullback is also finite, nilpotence versus nonnilpotence of one
multiplication operator gives an equivalent one-matrix boundary test.  The
finite quotient after the `eta=0` and Laurent star-alignment equations then
decides the legal pair sector on that good union.

No claim is made here that the committed scheme has already been built or that
either outcome has been selected.  P7 and global Krenn--Gu remain
**UNRESOLVED**.

## 1. The fixed-sensor adjugate chart

Let

```text
Gamma: U -> T,            dim U=219,
T=(K^3)^(tensor 5),       dim T=243,                 (1)
```

be the committed legal full-rank companion map and put `W=im Gamma`.  In the
column and ternary-row order fixed by
`P7_FULL_MIXED_ROOT_219_LABEL_SENSOR_AND_PINNED_STAR_GATING_BOUNDARY.md`, take
`R` to be the first 219 rows, from `00000` through `22002`.  The named-minor
certificate in that note proves that

```text
B=Gamma_R,              beta=det B !=0.             (2)
```

Thus no pivot search or generic-sensor assumption is needed.  The argument
below also applies to any other exact 219-row pivot block.
For an arbitrary tensor `z in T`, define the determinant-cleared preimage
numerator

```text
v(z)=adj(B) z_R in U.                               (3)
```

For each of the 24 complementary rows `s`, define

```text
rho_s(z)=beta z_s-Gamma_s v(z).                     (4)
```

### Proposition 1 (24-residual membership test)

For every `z in T`,

```text
z in W  <=>  rho_s(z)=0 for all s outside R.        (5)
```

If `z=Gamma q`, then

```text
v(z)=beta q.                                        (6)
```

### Proof

The equations on the pivot rows give

```text
B v(z)=B adj(B)z_R=beta z_R.                        (7)
```

Thus `q'=v(z)/beta` is the unique vector whose image agrees with `z` on
the pivot rows.  Equations (4) say precisely that `Gamma q'` also agrees on
the other 24 rows.  This proves (5).  Substitution of `z_R=Bq` in (3) gives
(6).

This is the first practical gain.  It avoids:

- 219 additional unknown coordinates `q`;
- all `220 x 220` augmented minors of `[Gamma|z]`; and
- elimination of `q` from `Gamma q=z`.

Only one fixed fraction-free solve and 24 residuals are required.  Since
`Gamma`, `B`, `beta`, and `adj(B)` are fixed integers, their exact computation
can be cached once.

## 2. The ordered honest-rank-three parameter space

Let `X=Segre((P^2)^5) subset P(T)` and let `L_c` be the pullback of the
tautological line bundle from the `c`-th factor of `X^3`.  The correct global
ordered parameter space is the projective bundle

```text
Pord=P_(X^3)(L_0 direct-sum L_1 direct-sum L_2),
dim Pord=3*10+2=32.                                  (8)
```

It is locally `X^3 x P^2`, but not canonically that product: rescaling a pure
representative inversely rescales its mixture coefficient.  A point of `Pord`
consists of three ordered pure tensor lines

```text
t_c=a_(0,c) tensor ... tensor a_(4,c),      c=0,1,2,
```

and a line in their direct sum.  After choosing local representatives, write
its mixture coordinates as `[lambda_0:lambda_1:lambda_2]`.  There is a rational
secant map

```text
Phi((t_c),lambda)=z=sum_(c=0)^2 lambda_c t_c.       (9)
```

The map can have a base locus when coincident summands cancel.  It is regular
on `D_tc !=0`, because the three pure tensors are then linearly independent.
The graph closure, rather than the bare projective bundle, is the appropriate
global resolution of collision limits.  Everything below that asserts an
honest survivor is performed on the base-locus-free open `D_tc !=0`.

Fix the five root evaluations `ell_i`.  Put

```text
D_tc = (product_c lambda_c)
       (product_i det[a_(i,0),a_(i,1),a_(i,2)])
       (product_(i,c) ell_i(a_(i,c))).              (10)
```

Although the displayed factors in (10) depend on local representatives, their
common nonvanishing does not.  On `D_tc !=0`, (9) is an honest rank-three
decomposition, the three factors at
each of the five roots form a basis, and all factors lie in the required root
torus.

### Proposition 2 (six ordered lifts on the good open)

Every tensor in the image of `D_tc !=0` has a unique unordered rank-three
decomposition.  Consequently it has exactly `3!=6` points in `Pord`, obtained
by ordering the three summands.

### Proof

Regroup the five modes as

```text
V_0 tensor V_1 tensor (V_2 tensor V_3 tensor V_4).  (11)
```

Each of the first two factor triples has Kruskal rank three.  The three grouped
pure factors also have Kruskal rank three: applying dual functionals at any one
of modes 2, 3, or 4 proves their linear independence.  Thus the three-way
Kruskal inequality is

```text
3+3+3=9 >= 2*3+2=8.                                (12)
```

Kruskal's theorem gives essential uniqueness; splitting each grouped pure
factor into its three projective factors is unique.  The projective-bundle
coordinates already quotient the compensating rescalings, so the only
remaining freedom on `Pord` is permutation of the three summands.

This is a direct use of John Rhodes's
[*A concise proof of Kruskal's theorem on tensor decomposition*](https://arxiv.org/abs/0901.1796).

## 3. Pull back the exact factor ideal without the secant ideal

Let `E=binom({2,...,8},2)` be the 21 named residual-pair coordinates in `U`.
For `p in Pord`, set

```text
v(p)=v(Phi(p))=adj(B) Phi(p)_R,
y_e(p)=v(p)_e,                    e in E.            (13)
```

The common scalar `beta` is irrelevant to the homogeneous factor equations.
Let `I_(7,2)` be the exact off-diagonal two-factor-analysis ideal in the 21
variables `y_e`.  Drton--Sturmfels--Sullivant compute that, for seven observed
variables and two factors, `I_(7,2)` has a minimal generating set of 35 cubics
and 21 pentads, codimension eight, and degree 259; see
[*Algebraic Factor Analysis: Tetrads, Pentads and Beyond*](https://arxiv.org/abs/math/0509390).
The statement is specific to `(7,2)`; no general-generation conjecture is being
used.

Define the ordered committed-sensor scheme

```text
J_Gamma = < rho_s(Phi(p)) : s outside R >
          + < f(y(p)) : f in I_(7,2) >              (14)
```

in the Cox/projective-bundle coordinate ring of `Pord`, or equivalently in
ordinary multihomogeneous coordinates after choosing a local trivialization.

### Proposition 3 (exact ordered model of the mandatory good intersection)

On `D_tc !=0`, the secant map sends `V(J_Gamma)` onto

```text
S_Gamma intersect {honest torus-concise rank three}, (15)
```

and every point downstairs has its six ordered lifts.  No defining equation of
`sigma_3(X)` is needed.

### Proof

Equations (4)--(5) are exactly the condition `Phi(p) in W`.  Equation (6)
shows that the 21 coordinates (13) are the named preimage coordinates, up to
the common nonzero scalar `beta`.  The second summand of (14) is therefore
exactly the factor-locus condition.  Proposition 2 proves the fiber statement.

For comparison, Yang Qi gives set-theoretic equations for third secants of
Segre products via flattening and Strassen-type equations in
[*Equations for the third secant variety of the Segre product of n projective spaces*](https://arxiv.org/abs/1311.2566).
Those equations remain useful for an independent downstairs audit, but (14)
does not need to construct or eliminate with them.

The equation count matches the geometry:

```text
dim Pord - 24 sensor residuals - 8 factor codimension
  =32-24-8=0.                                        (16)
```

Equation (16) is an expected-dimension statement, not a proof that the
committed pullback is proper.

## 4. Exact good-open separators

Let `D(p)=span(t_0,t_1,t_2)`.  On `D_tc !=0`, it is a three-plane containing
`Phi(p)`.  Since `rank Gamma=219`,

```text
dim(W intersect D(p))=1
  <=> rank[Gamma|t_0|t_1|t_2]=221.                  (17)
```

There is a much smaller quotient-space test for (17).  Let

```text
r(t)=(rho_s(t))_(s outside R) in K^24.              (18)
```

By Proposition 1, `ker r=W`.  On `V(J_Gamma)`,

```text
lambda_0 r(t_0)+lambda_1 r(t_1)+lambda_2 r(t_2)=0.  (19)
```

All three `lambda_c` are nonzero on `D_tc`.  Hence

```text
simple incidence
 <=> rank[r(t_0)|r(t_1)|r(t_2)]=2
 <=> r(t_0) wedge r(t_1) !=0 in wedge^2 K^24.       (20)
```

This replaces all `221 x 221` augmented minors by one 24-dimensional
exterior-algebra object.

It also permits a deterministic symbolic union-of-charts test.  Introduce
algebraically independent selectors `u_ab` for `0<=a<b<24` and `z_e` for the
21 pair coordinates, and work over the purely transcendental extension

```text
Kgen=K(u_ab,z_e : a<b, e in E).                      (21)
```

Define

```text
Delta_gen = sum_(a<b) u_ab
  (r(t_0)_a r(t_1)_b-r(t_0)_b r(t_1)_a),
Y_gen = sum_(e in E) z_e y_e.                       (22)
```

For every geometric point, `Delta_gen` is nonzero in `Kgen` exactly when the
bivector in (20) is nonzero, and `Y_gen` is nonzero exactly when the 21-vector
`(y_e)` is nonzero.  This is coefficient comparison, not random
specialization.

Let `d_0(v)` and `d_1(v)` be the two pinned determinants from the prior legal
pullback theorem.  The single universal good-open separator is

```text
G_gen=D_tc Delta_gen Y_gen d_0(v)d_1(v).             (23)
```

Then `G_gen !=0` over `Kgen` means simultaneously:

- honest, torus-concise rank three;
- root-torus admissibility;
- simple diagonal incidence after the legal local basis change;
- a nonzero residual-pair coordinate; and
- membership in the pinned open.

Thus one universal localization over `Kgen` tests the entire union of simple
and pair-nonzero charts.  It does not enumerate augmented minors or choose
among the 21 pair coordinates.  If the full ordered scheme is finite, the same
union can be tested by one multiplication operator.  Individual chart products
remain available as smaller follow-up certificates after the universal test
succeeds.

## 5. Universal localization and Artinian support tests

Collision fibers over the secant boundary need not be finite.  Therefore the
robust construction localizes before assuming that the ordered pullback is
Artinian.  Introduce one inverse variable `w` and set

```text
J_good=J_Gamma+<w G_gen-1>.                           (24a)
```

The factor `D_tc` in `G_gen` removes the rational-map base locus and all
collision fibers.  On this open, Proposition 2 makes the ordered map
six-to-one.  Consequently, whenever the downstairs intersection `S_Gamma` is
proper and finite, `V(J_good)` is finite as well.

Choose a fixed ample projective embedding and contract its homogeneous
coordinates with another family of algebraically independent coefficients.
The resulting generic linear form `H_gen` misses every point of the finite
support over the corresponding rational-function field.  Localizing at
`H_gen` and setting it to one gives one affine algebra containing the whole
good support without enumerating projective charts.  Enlarge `Kgen` by these
dehomogenizer coefficients and write

```text
A_good=Kgen[Pord_affine,w]/J_good,
N_good=dim_Kgen A_good.                               (24b)
```

Then

```text
A_good=0  <=> the mandatory intersection misses the good union;
A_good!=0 <=> the mandatory intersection has a good-union survivor. (24c)
```

Thus (24c) is the unconditional boundary-trap/good-survivor criterion on the
proper downstairs branch.  It uses a finite quotient only after boundary
fibers have been removed.

The following multiplication theorem supplies norms and finer support tests
inside `A_good`, and also gives a one-matrix shortcut if the larger ordered
pullback from (14) is independently certified finite.  Let `A` be any finite
commutative algebra of dimension `N`, and for `g in A` let `M_g` be its
multiplication matrix.

### Theorem 4 (finite open/boundary trichotomy)

Over the algebraic closure:

```text
det M_g !=0   <=> every point of Supp A lies in D(g);
M_g nilpotent <=> every point of Supp A lies in V(g);
M_g nonnilpotent <=> some point of Supp A lies in D(g).          (25)
```

Moreover, nilpotence is decided by the single finite test

```text
M_g^N=0.                                             (26)
```

### Proof

An element of a finite commutative algebra is a unit exactly when its
multiplication map is invertible.  It is nilpotent exactly when it belongs to
the nilradical, which is the intersection of all prime ideals and hence the
ideal of the support.  Cayley--Hamilton bounds the nilpotence exponent by
`N`.

Equivalently, define the support polynomial

```text
C_g(T)=det(T I_N-M_g).                               (27)
```

Then `C_g(T)=T^N` exactly in the boundary-trapped case, while its constant
term, up to sign, is the norm `det M_g`.  Thus the full characteristic
polynomial distinguishes all three cases in one exact object.

If the full ordered scheme from (14) is finite, apply (25) over `Kgen` to
`g=G_gen`.

- If `M_(G_gen)` is nonnilpotent, the mandatory intersection meets the
  meaningful good open.
- If `M_(G_gen)` is nilpotent, all points of the finite ordered scheme
  are trapped in the union of the torus-concise, root-torus, simple-incidence,
  pair-coordinate, and pinned boundaries.
- If `M_(G_gen)` is invertible, the entire support avoids those boundaries, a
  stronger conclusion.

Nonnilpotence is essential here.  A determinant-zero multiplication map can
still have a nonzero eigenvalue, meaning that some support points lie in the
open while others lie on its boundary.  If the full scheme is not finite, use
the localized criterion (24c) instead; no claim of finiteness is inferred from
the expected dimension count (16).

## 6. The `h=0` and star-alignment quotient

Extend scalars to `Kgen` and form the finite Laurent quotient on the universal
good open

```text
A_gen^star =
  A_good[s,s^(-1)] /
  < eta(v),
    s y_ij-khat_ij(v) : 2<=i<j<=8 >.                (28)
```

The variable `s` is the common nonzero amplitude.  Equivalently, introduce an
inverse variable `u` and the equation `su-1`; this keeps the construction
inside ordinary polynomial algebra.

### Corollary 5 (exact legal pair-sector decision on the good union)

```text
A_gen^star !=0
```

if and only if the committed legal `h=0` weighted pair ideal has a point on
the torus-concise, root-torus, simple, pair-nonzero, pinned union.  If the
quotient is zero, the ideal is the unit ideal on that union.  If it is nonzero,
multiplication by the remaining desired open products distinguishes good
support from newly introduced boundary support exactly as in (25).

This decides the pair sector only.  The other 105 four-deck and upper-deck
equations remain separate obligations.

## 7. Chow degree and a finite size certificate

Write

```text
d_3=deg sigma_3(Segre((P^2)^5)).                    (29)
```

No numerical value for `d_3` is assumed.  If `Z_Gamma` has the expected
dimension eight and meets the factor preimage properly, then their classes in
`P(U)=P^218` are

```text
[Z_Gamma]=d_3 H^210,
[F_Q]=259 H^8.                                      (30)
```

Therefore the scheme-theoretic intersection length, counted with
multiplicity, is

```text
length(S_Gamma)=259 d_3.                            (31)
```

On the identifiable torus-concise open, the number of ordered geometric points
is six times the corresponding number downstairs, and hence is at most

```text
6*259*d_3.                                          (32)
```

If the Jacobian of the ordered map has full rank along the finite intersection,
the map is étale there and the factor six also holds scheme-theoretically.
This is an exact maximal-minor check and should precede any claim about ordered
scheme length.  Equations (31)--(32) are a Chow/Bézout size certificate, not a
claim of transversality, reducedness, or étaleness.  If the intersection is
nonproper, one first saturates by a selected chart product and takes a
complementary exact linear slice; the multiplication test then applies
componentwise.

## 8. Exact construction without broad elimination

The committed calculation can be organized as follows.

1. Reuse the certified first-219-row block `R` of the committed `Gamma`, and
   cache `beta` and a fraction-free solver for `B`.  Explicitly materializing
   the full adjugate is optional: Bareiss solves compute the same numerators.
2. Substitute (9) only into the 24 residuals (4).  These equations are
   multilinear in the five factor blocks and linear in `lambda`.
3. Use the 21 linear forms (13) to evaluate the published 35 cubics and 21
   pentads generating `I_(7,2)`.
4. Form the universal exterior and pair contractions (22), adjoin
   `w G_gen-1`, and use the generic ample dehomogenizer `H_gen`.  Exact sparse
   multigraded Macaulay/Koszul linear algebra then decides whether `A_good` is
   zero and, if not, constructs its quotient basis and multiplication matrices.
   This is a fixed structured resultant calculation in dimension 32, not
   elimination over the 219 preimage variables or the 243 tensor coordinates.
5. If `A_good` is nonzero, impose (28) and repeat the finite quotient test.  If
   the larger ordered pullback is separately proved finite, its optional
   one-shot boundary detector is the characteristic polynomial (27) of
   `M_(G_gen)`.
6. Independently verify any claimed solution count against (31), the factor
   degree 259, and the sixfold divisibility on the Kruskal open.

All arithmetic can remain over the exact coefficient field of the committed
integer sensor.  No numerical continuation, finite-field inference, parameter
sampling, timeout, or broad Gröbner basis is evidence for either branch.

## 9. What an empty torus-concise saturation means

If

```text
(J_Gamma : D_tc^infinity)=<1>,                       (33)
```

then the mandatory intersection still exists downstairs, but every point is a
border degeneration or is root-torus inadmissible.  Buczyński--Landsberg's
normal-form analysis of border rank at most three gives the relevant secant
boundary mechanisms: an honest sum of three points; a tangent vector plus a
point; a second-order collision/osculating type; and a two-tangent type along a
line contained in the Segre, together with lower-secant and non-concise
degenerations.  See
[*On the third secant variety*](https://arxiv.org/abs/1111.7005).

Thus (33) is not an unstructured failure.  It redirects the proof to
a finite list of collision normal forms, where the 24 residual equations and
the factor generators can be restricted symbolically again.  Conversely,
`A_good!=0` bypasses the entire border classification and proves an honest
good-open survivor.  When the full ordered pullback is finite, nonnilpotence of
the universal product (23) is the equivalent one-matrix certificate.

## Exact outcome table

```text
J_Gamma saturated by D_tc is zero/empty:
  mandatory intersection is trapped in the classified secant/root boundary;

A_good is zero:
  mandatory intersection is trapped in the torus-concise, root-torus,
  simple-incidence, pair-zero, or pinned boundary;

A_good is nonzero:
  mandatory intersection meets the honest torus-concise, root-torus,
  simple, pair-nonzero, pinned open;

full ordered pullback is finite and M_(G_gen) is nonnilpotent:
  equivalent one-matrix certificate for the preceding good-open outcome;

good-union quotient (28) is zero:
  legal h=0 weighted pair ideal is unit on that good union;

good-union quotient (28) is nonzero:
  legal h=0 weighted pair ideal has a good-union point;

committed calculation not yet performed:
  none of the alternative outcomes above is asserted here.
```

## Scope wall

```text
legal committed rank-219 sensor retained:                         YES;
free 219-coordinate preimage elimination required:                NO;
augmented 220-minor membership equations required:                NO;
exact fixed-sensor membership residuals:                           24;
ordered secant parameter-space dimension:                          32;
torus-concise ordered-cover degree:                                  6;
exact I_(7,2) generators:                        35 CUBICS + 21 PENTADS;
factor-locus codimension and degree:                              8, 259;
expected localized good secant--factor quotient dimension:             0;
universal good localization is finite if downstairs is proper:       YES;
full ordered pullback is finite:                                  UNKNOWN;
nilpotence test if the chosen ambient quotient is finite:             YES;
symbolic Chow length on a proper downstairs intersection:      259*d_3;
numeric value of d_3 used or claimed:                                NO;
committed first-219-row pivot block already certified:              YES;
24 residual formulas explicit:                                     YES;
committed 24 residual coefficient polynomials materialized:          NO;
committed finite Artinian quotient actually constructed:             NO;
mandatory intersection meets torus-concise open:                 UNKNOWN;
mandatory intersection meets simple open:                        UNKNOWN;
mandatory intersection has a nonzero named pair:                  UNKNOWN;
mandatory intersection meets pinned open:                        UNKNOWN;
eta and star-alignment quotient is nonzero:                       UNKNOWN;
legal localized full pair ideal is unit:                         UNKNOWN;
legal localized full pair ideal has a point:                     UNKNOWN;
other 105 four-deck and upper-deck equations:             STILL REQUIRED;
P7 obstruction or construction:                                 UNKNOWN;
global Krenn--Gu:                                             UNRESOLVED.
```

## Exact replay

```powershell
uv run --with sympy python claims/p7/verify_committed_legal_sensor_ordered_secant_factor_chow_norm_boundary.py
python claims/p7/audit_committed_legal_sensor_ordered_secant_factor_chow_norm_boundary.py
python -m py_compile claims/p7/verify_committed_legal_sensor_ordered_secant_factor_chow_norm_boundary.py claims/p7/audit_committed_legal_sensor_ordered_secant_factor_chow_norm_boundary.py
uv run --with ruff ruff check claims/p7/verify_committed_legal_sensor_ordered_secant_factor_chow_norm_boundary.py claims/p7/audit_committed_legal_sensor_ordered_secant_factor_chow_norm_boundary.py
```

The primary replay verifies the determinant-cleared membership lemma, the
simple-incidence rank criterion, the Kruskal and Chow arithmetic, and all three
possibilities in the Artinian multiplication test.  The independent
standard-library audit rebuilds the certificates using separate rational
matrix code.  These are bounded symbolic audits of the criterion, not a
calculation of the committed `243 x 219` sensor outcome.
