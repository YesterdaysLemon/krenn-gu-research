# Four-root torus-star equal-leaf survivor center-rank determinantal chart reduction

## Status

**Exact finite parent reduction (`GLD84`).**  Work over `K=Q(i)` and then
extend scalars to `C`.  On the complete scale-fixed equal-leaf survivor base
of `GLD83`, the ten survivor equations are affine-linear in eight center
variables.  Their `10 x 8` coefficient matrix gives an exhaustive finite
rank-eight, rank-seven, and rank-at-most-six cover.  Every rank-eight chart is
an exact six-variable/two-equation Schur model; every named rank-seven chart
is an exact seven-variable/three-equation model, with the remaining center
parameter free on the exact rank-seven stratum.

At the `GLD72` point the center rank is seven, but a named rank-eight minor
has derivative `48i` along one normalized tangent of the smooth survivor
germ.  Thus the rank-eight open is nonempty on the `GLD72` component and the
Gaussian rank-seven calculation cannot stand in for that component.

This is a sharp parameter and local rank-stratum reduction for the intrinsic `GLD83`
residual `V(I_Pl) intersect D(Omega)`.  It does **not** compute the pulled-back
Fitting ideal, exclude any new point of that residual, cover other survivor
gauges/components, or resolve Krenn--Gu.  The global conjecture remains
**UNRESOLVED**.

Owning dependencies are the `GLD75` exact equal-leaf survivor basis and
smooth-germ theorem, and the [`GLD83` bordered Fitting-open
reduction](FOUR_ROOT_TORUS_STAR_SURVIVOR_BORDERED_PLUCKER_FITTING_OPEN_NONEXTENSION_THEOREM.md).

## 1. The center-linear survivor system

Retain the `GLD83` base

```text
B=Spec K[x_0,...,x_14]/(g_0,...,g_9,x_8).
```

This is the globally defined scale-fixed equal-leaf subincidence in the
displayed affine frame gauge.  It is not asserted to be irreducible or to
exhaust the fixed-star survivor locus.  Put

```text
c=(x_0,...,x_7)^T,
z=(x_9,...,x_14).
```

The center frame enters the GHZ parametrization linearly.  The pinned
`GLD75` bidirectional ideal certificate therefore gives, after `x_8=0`, the
exact identity

```text
g(z,c)=A(z)c+q(z),                                      (1)
A(z) in Mat_(10 x 8)(K[z]),
q(z) in K[z]^10.
```

Equivalently, `A_ij=partial g_i/partial c_j` and `q=g|_(c=0)`.  The portable
verifier checks (1) term by term from the pinned sparse basis; no numerical
fit or sampled interpolation is used.

For `r=7,8`, write `I_r(A)` for the ideal of the `r x r` minors of `A` in
`K[z]`.

## 2. Exhaustive center-rank cover

The underlying geometric points of `B` have the disjoint locally closed
partition

```text
B^[8]  =B intersect D(I_8(A)),
B^[7]  =B intersect V(I_8(A)) intersect D(I_7(A)),
B^[<=6]=B intersect V(I_7(A)).                          (2)
```

This is exhaustive because `A` has eight columns.  More explicitly:

- `B^[8]` is covered by the `binomial(10,8)=45` opens obtained by choosing
  eight rows and taking all eight center columns;
- `B^[7]` is covered by the
  `binomial(10,7)binomial(8,7)=960` locally closed charts obtained by
  choosing seven rows and seven center columns, together with `I_8(A)=0`;
- `B^[<=6]` is the closed determinantal branch cut out by the same `960`
  seven-minor generators.

These counts name a finite cover; they do not assert that every chart or the
rank-at-most-six branch is nonempty.

### Theorem 2.1 (rank-eight Schur charts)

Choose an eight-row set `R`, put

```text
mu_R=det A_R,
```

and let `k` range over the two complementary rows.  Define

```text
rho_(R,k)=mu_R q_k-A_(k,*) adj(A_R)q_R.                 (3)
```

There is an exact isomorphism

```text
B intersect D(mu_R)
  isomorphic to
Spec K[z,1/mu_R]/(rho_(R,k): k notin R),                (4)
```

under which

```text
c=-adj(A_R)q_R/mu_R.                                   (5)
```

Thus each rank-eight chart has six ambient leaf variables and two explicit
residual equations.

#### Proof

On `D(mu_R)`, the eight equations indexed by `R` are equivalent to (5).
Substitution in the remaining two equations and multiplication by the unit
`mu_R` gives exactly (3).  Conversely (3) and (5) recover all ten equations.
This constructs inverse localized coordinate-ring maps.  `square`

### Theorem 2.2 (rank-seven Schur charts)

Choose seven rows `R` and seven columns `C`.  Let `j` be the omitted center
column, put

```text
nu_(R,C)=det A_(R,C),
t=c_j,
```

and, for the three rows `k` outside `R`, define

```text
sigma_(R,C,k)=
  nu_(R,C)(q_k+A_(k,j)t)
  -A_(k,C)adj(A_(R,C))(q_R+A_(R,j)t).                  (6)
```

Then

```text
B intersect D(nu_(R,C))
  isomorphic to
Spec K[z,t,1/nu_(R,C)]/
     (sigma_(R,C,k): k notin R),                       (7)
```

with

```text
c_C=-adj(A_(R,C))(q_R+A_(R,j)t)/nu_(R,C).              (8)
```

The exact rank-seven part of this chart is obtained by imposing
`I_8(A)=0`.  There the coefficient of `t` in each equation (6) is, up to the
unit sign fixed by the chosen row and column order, the corresponding
`8 x 8` minor of `A`.  Hence it vanishes on `V(I_8(A))`: the three remaining
compatibility equations depend only on `z`, and `t` is the one free kernel
coordinate.  Conversely, after `nu_(R,C)` is inverted, these three
coefficients generate the localized ideal `I_8(A)`: pivot row and column
operations reduce `A` to a rank-seven identity block with a `3 x 1` Schur
complement.  Thus one may replace all forty-five eight-minors by the three
Schur rank equations on this chart.

#### Proof

The first statement is the same localized solve as Theorem 2.1, now for the
seven variables `c_C`, leaving `t`.  The coefficient of `t` in (6) is the
bordered determinant expansion of the eight-row/eight-column matrix formed
by adjoining row `k` and column `j`.  All such minors vanish on the rank-
seven stratum.  `square`

The rank-at-most-six branch is retained as `B intersect V(I_7(A))`; no
seventh pivot is selected or divided away there.

## 3. Exact geometry at the Gaussian survivor

At the origin `F_0` of the shifted chart,

```text
rank A(F_0)=7.                                          (9)
ker A(F_0)=K(1,-1,0,0,0,0,1,0)^T.
```

Since `q(F_0)=0`, the center fibre over the Gaussian leaf coordinates is
exactly this affine line in the shifted center variables.

The named Gaussian rank-seven pivot is

```text
R_7=(0,1,2,3,4,5,6),
C_7=(0,1,2,3,4,5,7),
nu_(R_7,C_7)(F_0)=12.                                  (10)
```

Take also

```text
R_8=(0,1,2,3,4,5,6,7),
mu_0=det A_(R_8,{0,...,7}).                            (11)
```

The `GLD75` scale-fixed germ is smooth of dimension four at `F_0`; its
normalized free coordinates are `(x_6,x_12,x_13,x_14)`.  Let `tau_14` be the
unique normalized tangent with `x_14` component one and the other three free
components zero.  Exact calculation gives

```text
mu_0(F_0)=0,
partial mu_0/partial x_14 (F_0)=0,
d mu_0(F_0)(tau_14)=48i.                               (12)
```

The distinction in (12) matters: `x_9` and `x_10` are dependent survivor
coordinates and vary along `tau_14`; the nonzero number is the derivative on
the survivor germ, not the ambient partial derivative holding them fixed.

### Corollary 3.1 (rank-eight open meets the GLD72 component)

The function `mu_0` is nonzero in the regular local ring of the scale-fixed
survivor germ at `F_0`.  Consequently `D(mu_0)` is a nonempty survivor open
whose closure contains `F_0`; in particular the component through `GLD72`
has rank-eight center points.  The exact rank-seven locus is contained in the
proper local divisor `V(mu_0)`.

#### Proof

The nonzero cotangent class in (12) implies that `mu_0` is not the zero
function in the smooth local ring.  Its nonvanishing locus is therefore
nonempty and dense in the local irreducible germ.  Every point of
`D(mu_0)` has center rank eight.  `square`

This does not prove that `V(mu_0)` equals the full rank-seven locus: all
forty-five eight-minors must vanish for rank seven.

## 4. Pullback of the GLD83 Fitting residual

Let

```text
Z_83=V(I_Pl) intersect D(Omega) subset B               (13)
```

be the intrinsic fixed-chart residual left by `GLD83`.  Equations (2)--(8)
give the exact finite cover

```text
Z_83=(Z_83 intersect B^[8])
     disjoint-union (Z_83 intersect B^[7])
     disjoint-union (Z_83 intersect B^[<=6]).           (14)
```

On a rank-eight chart, substitute (5) into the polynomial arithmetic circuit
for `Omega` and `A_Pl` and localize at `mu_R`.  The resulting obligation lies
in the six-variable ring

```text
K[z,1/mu_R]/(rho_(R,k): k notin R).                    (15)
```

On a rank-seven chart, substitute (8), impose `I_8(A)`, and localize at
`nu_(R,C)`.  The resulting obligation lies in the seven-variable ring

```text
K[z,t,1/nu_(R,C)]/
(sigma_(R,C,k), I_8(A)),                               (16)
```

where the compatibility equations are independent of `t` on the exact
rank-seven stratum.  The remaining branch is explicitly

```text
V(I_Pl,I_7(A)) intersect D(Omega).                      (17)
```

All denominator clearing in (15)--(16) is interpreted after localization,
or equivalently by saturation with the named minor.  No point on a chart
divisor is silently discarded; it belongs to another chart or the named
lower-rank branch.

More explicitly, choose ambient polynomial lifts of the `GLD83` Fitting
ideal and let `I_B=(g_0,...,g_9,x_8)`.  The exact chart-saturated residual
ideals are

```text
R_(8,R)=(I_B+I_Pl):(Omega mu_R)^infinity,
R_(7,R,C)=(I_B+I_8(A)+I_Pl):(Omega nu_(R,C))^infinity,
R_(<=6)=(I_B+I_7(A)+I_Pl):Omega^infinity.               (18)
```

Equivalently one may pull back the transported blocks `C_F,w_0,w_1,w_2`,
their bordered quadrics, and `A_Pl` through (5) or (8) before forming the
localized Fitting ideal.  The chart coordinate `t` in (6)--(8) is a center-
kernel parameter and is unrelated to the nine homogeneous invariant raw-
response coordinates `y=(u_0,...,u_7,s)` of `GLD83`.

Equations (14)--(18) are a parameter reduction, not a Fitting computation.
They do not assert that the pullback of `I_Pl` is nonzero, the unit ideal, or
empty on any chart.

## 5. Hostile controls and remaining obligation

- `GLD72` remains an exact concise GHZ tensor in the fixed nuisance space and
  lies on the rank-seven center stratum.
- The rank-eight open is proved to meet the same local survivor component;
  the Gaussian rank-seven chart is not promoted to a component theorem.
- The cover is exhaustive only for the displayed equal-leaf base `B`, not
  for other gauges, survivor components, or source presentations.
- Every selected minor is localized or saturated.  Rank drops are named
  branches, not divided away.
- No epsilon or `Q`-generator condition is used as a GHZ-membership test.
- No first-response incidence is newly excluded by `GLD84`; the owning
  exclusion remains `GLD83` on `D(Omega I_Pl)`.
- The global Krenn--Gu conjecture remains **UNRESOLVED**.

The highest-value successor is to compute or certify the pullback of
`I_Pl` first on the named rank-eight chart (11), using the six-variable,
two-equation model (15), and independently on the Gaussian rank-seven chart
(10).  A unit certificate for the first two ideals in (18) would close the
corresponding rank strata.  A selected maximal minor would prove only another
principal-open exclusion.  On a `C_F`-rank-drop branch all bordered quadrics
vanish, so the analysis must return to the full raw incidence
`b alpha=T(F), D_q0(alpha)L=R(F)` rather than infer source integrability from
nuisance membership.  A complete fixed-chart result must also treat the
other finite charts and the rank-at-most-six branch.

## 6. Verification

Run:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_survivor_center_rank_determinantal_chart_reduction.py
python -I claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_survivor_center_rank_determinantal_chart_reduction.py
```

The primary verifier reconstructs the ten exact `GLD75` survivor generators,
checks (1), all Gaussian ranks and minors, the scale-fixed tangent basis, the
directional derivative (12), and the finite chart counts.  The independent
no-import audit parses the pinned sparse certificate directly and recomputes
the center-linear structure, constant center matrix, Gaussian minors,
tangent system, and directional determinant over `Q(i)` without importing
repository Python modules.  The universal Schur isomorphisms and finite rank
partition are the written linear-algebra proof; finite tests are not
substituted for them.
