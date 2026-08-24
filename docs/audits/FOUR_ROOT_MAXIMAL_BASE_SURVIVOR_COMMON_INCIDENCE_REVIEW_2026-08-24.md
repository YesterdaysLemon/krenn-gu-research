# Hostile review: four-root maximal-base-survivor common incidence

Date: 2026-08-24

## Verdict

**Accept at the declared boundary scope.**  The package proves a useful
parent reduction and a bounded physical mixed-target detector.  It does not
prove a universal star/triangle contradiction, and it correctly records why
the remaining exceptional fibres are load-bearing.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

Reviewed artifacts:

- [`FOUR_ROOT_MAXIMAL_BASE_SURVIVOR_COMMON_INCIDENCE_AND_SPARSE_RADICAL_DETECTOR_BOUNDARY_THEOREM.md`](../../claims/arbitrary-order/FOUR_ROOT_MAXIMAL_BASE_SURVIVOR_COMMON_INCIDENCE_AND_SPARSE_RADICAL_DETECTOR_BOUNDARY_THEOREM.md);
- [`verify_four_root_maximal_base_survivor_common_incidence_and_sparse_radical_detector_boundary.py`](../../claims/arbitrary-order/verify_four_root_maximal_base_survivor_common_incidence_and_sparse_radical_detector_boundary.py);
- [`audit_four_root_maximal_base_survivor_common_incidence_and_sparse_radical_detector_boundary.py`](../../claims/arbitrary-order/audit_four_root_maximal_base_survivor_common_incidence_and_sparse_radical_detector_boundary.py).

## 1. Exact claim under review

`GLD68` leaves at most three nonzero pair base classes.  A maximal family is
one of four stars or four triangles.  The reviewed successor asks whether the
three complementary swallowed relations, combined in one module and coupled
to the contracted four-port GHZ identity, force a contradiction.

The package answers in five layers:

1. no at the abstract labelled-coefficient level;
2. the actual six companions have one common physical form
   `J=P_4(xi,eta,-,-)`;
3. with four rank-three ports, every maximal profile forces `rank J=2` and a
   sharp star/triangle hyperplane geometry;
4. the internal six-label pair layer has exact dimension `21` on a star and
   `19` on a triangle and cannot contain weighted concise GHZ;
5. a support-at-most-two radical vector common to the four port images gives
   one decomposable functional annihilating all fifteen order-two labels, so
   its weighted-GHZ value must vanish.

The theorem excludes a point exactly when that last target value is nonzero.
It does not assert that target activity is automatic.

## 2. Type and provenance audit

For a pair target `S`, `Pi_S` lives on the complementary ports `bar S`, while
the complementary nuisance label `I=bar S` has deck tensor on `bar S` and
companion `Pi_(bar S)` on `S`.  The direct-sum module retains these target
labels before summing into the common four-port tensor.  No targetwise
functional is reused on another summand.

On an actual maximum-root chart, evaluation at a local port vector gives a
root-coordinate vector in `X=K^4`.  With the two residual vectors `xi,eta`,
the raw pair companion is exactly

```text
P_4(xi,eta,A_u(-),A_v(-)),
```

not an arbitrary bilinear block.  The common-`J` lift therefore uses physical
provenance absent from the formal countermodels.  The theorem never promotes
those countermodels to graphs or witnesses.

After the residual target slots are contracted, maximum-root grade zero has
exactly the fifteen order-two labels in `Q union U`: six port--port labels,
eight residual--port labels, and `Q`.  Higher even labels require a positive
root--root grade and are not imported into this base identity.

## 3. Hostile checks of the coefficient-only no-go

For each maximal family `A`, assign its three edges the three target colours.
Put a pure tensor of the assigned colour in both the label tensor `H_S` and
its complementary companion `Pi_S`; put every complementary companion and
every other label to zero.  The aggregate is exactly `Delta_4`.

The important extra check is desired-class survival, not merely aggregate
equality.  At a target edge `S`, each other nonzero label leaves one receiver
factor arbitrary and fixes the other to its own, different colour.  Neither
of those two nuisance rulings contains the pure receiver word of colour
`gamma(S)`.  The primary verifier and independent audit replay all
`8*3=24` quotient checks.  Thus the formal examples really do satisfy the
declared foreign port-pair nuisances.

This no-go is appropriately scoped.  It says a proof cannot use only
anti-simultaneity, three unrelated target quotients, and an aggregate GHZ
sum.  It says nothing against a proof using the common physical `J`.

## 4. Hostile checks of the rank-three compression

If two three-dimensional port images are `J`-orthogonal, the restriction of
the rank-`rho` map `J:X->X^*` to one hyperplane has rank at least `rho-1`.
Its orthogonal complement therefore has dimension at most `5-rho`, but it
contains the other three-space.  Hence `rho<=2`.

The profile also has a nonzero complementary block, so `J` is nonzero.  A
nonzero symmetric rank-one matrix cannot have zero diagonal in
characteristic zero.  Therefore `rank J=2`.

The radical-containment conclusion is valid on a zero edge: both orthogonal
three-spaces contain the two-dimensional radical.  The star consequently has
two hyperplanes, one at the centre and one shared by all leaves.  In the
triangle, only the three sibling hyperplanes are forced to coincide.  The
centre has no incident zero edge and need contain only a one-dimensional
piece of the radical.

This last distinction caught a tempting but invalid proof shortcut.  An
arbitrary change of root basis does not preserve the permanent tensor, and a
rank-two residual form is not restricted to the coordinate example
`xi=e_3, eta=e_2`.  Full-support rank-two residual pairs exist.  Likewise a
triangle centre cannot be replaced silently by `R+Km`.  Both shortcuts were
removed before the theorem was stated.

## 5. Hostile checks of the universal pair layer

For a star, all three nonzero companions are rank-one leaf--leaf blocks.  The
freely varying internal pair labels therefore have image

```text
E_0 tensor (E_1 c_2 c_3+c_1 E_2 c_3+c_1 c_2 E_3),
```

of dimension `3*7=21`.  Quotienting any two leaf spaces by their `c_i` lines
kills the image.  A weighted three-colour diagonal would then put three
independent coordinate covectors into the union of two lines, impossible.

For a triangle, the three sibling images are one maximal isotropic
hyperplane.  Factoring `J=ell tensor m+m tensor ell` makes every nonzero
centre--sibling block `c_i tensor d_3`, even when the centre projects onto the
whole quotient.  The pair layer is

```text
(E_0 E_1 c_2+E_0 c_1 E_2+c_0 E_1 E_2) tensor d_3,
```

of dimension `19`.  Its isolated-port flattening has rank at most one, versus
rank three for weighted GHZ.

The independent hostile council reconstructed both formulas without using
the primary verifier and specifically checked the projection-full triangle
centre branch.  It found exact augmented ranks `21 -> 22` and `19 -> 20`.
This is a universal obstruction for the six internal port-pair labels only.
The complete base equation also has eight residual--port labels and `Q`; no
argument in the package silently removes them.

## 6. Hostile checks of the sparse-radical detector

A rank-two zero-diagonal symmetric form has hyperbolic quotient.  Factoring
it as

```text
kappa(ell tensor m+m tensor ell)
```

and reading the zero diagonal gives disjoint coordinate supports for `ell`
and `m`.  Their common kernel therefore contains a nonzero vector supported
on at most two coordinates.  The no-import audit independently exhausts all
`5^6=15625` zero-diagonal symmetric matrices over `F_5`; all `664` rank-two
matrices have such a sparse radical vector, and none has rank one.

If the same sparse radical vector `r` belongs to every port image, its unique
four local preimages define `chi_r`.  The fifteen labels vanish for three
different reasons which the proof keeps separate:

- a port--port label leaves `J(r,r)=0`;
- a residual--port label leaves `P_4(xi,r,r,r)` or
  `P_4(eta,r,r,r)`, zero because three `r` columns have at most two available
  root rows;
- the `Q` label leaves `P_4(r,r,r,r)=0`.

No response nonvanishing, selector normalization, division, generic-point
promotion, or numerical inference enters this calculation.  Evaluating the
target gives the displayed weighted diagonal scalar `D_r`, so `D_r!=0` is a
literal complete-target contradiction.

## 7. Attempts to strengthen the claim

### 7.1 Drop common physical incidence

Rejected by the eight exact formal models.  The three targetwise quotient
functionals do not become one functional merely because their outputs are
summed.

### 7.2 Canonicalize every rank-two `J` by an arbitrary root basis change

Rejected.  `P_4` is not invariant under general `GL_4`.  Such a reduction
would lose the one-residual and zero-residual companions used by the fifteen
label identity.  The final proof uses only the intrinsic radical and standard
coordinate support forced by the zero diagonal.

### 7.3 Force nonzero detector activity from the star geometry

Rejected by the exact rank-three incidence control.  The four inverse images
of the radical can occupy local coordinate planes with supports

```text
{0,1}, {0,1}, {1,2}, {0,2}.
```

Every target colour is then absent at one port and `D_r` vanishes identically
on the radical plane.  This is not a graph witness, but it is sufficient to
show that the declared incidence hypotheses do not force target activity.

### 7.4 Put the triangle centre over the whole radical

Rejected by the exact `2+2` support control.  For

```text
ell=x_0+x_1,       m=x_2+x_3,
U_0={x_0=x_2},     B=ker ell,
```

the sibling hyperplane `B` is totally isotropic and the centre--sibling block
is nonzero, but

```text
U_0 intersect rad J=K(1,-1,1,-1).
```

The only common radical line has full support.  The sparse detector therefore
does not apply.

### 7.5 Infer the lower-port-rank cases

Rejected.  The dimension argument uses two rank-three orthogonal port images.
The upstream maximum-root deficiency budget does not force all four port
ranks to equal three.  No lower-rank profile is claimed closed.

### 7.6 Promote the pair-layer obstruction to the complete base equation

Rejected at present.  The pair-layer quotient does not annihilate the nine
labels meeting `Q`.  Exact rational and finite-field searches by the hostile
council found no common-incidence model of the complete contracted GHZ
equation, but they also found no basis-free separator covering the
scalar-zero, nonsparse-centre, and lower-rank cases.  Absence of a found
countermodel is evidence, not proof.  A legal `Q`-layer annihilator or an
equivalent synchronization invariant remains the smallest universal bridge.

## 8. Verification evidence

The primary verifier reports:

```text
four-root maximal-survivor common-incidence boundary: PASS
  formal maximal / star / triangle countermodels: (8, 4, 4, 24)
  typed common-J pullback coordinates: 54
  star / triangle pair-layer augmented ranks: ((21, 22), (19, 20))
  annihilated labels / active detector: (15, 1)
  scalar-zero star samples: 49
  triangle intersection checks / support: (81, 4)
```

The independent no-import audit reports:

```text
independent GLD69 common-incidence boundary audit: PASS
  F5 zero / rank-two / rank-four forms: (1, 664, 12400)
  formal maximal / star / triangle models: (8, 4, 4, 24)
  star / triangle pair-layer augmented ranks: ((21, 22), (19, 20))
  annihilated labels / nonzero target value: (15, 2310)
  scalar-zero / nonsparse-centre checks: (121, 121)
```

The scripts replay identities, finite case coverage, and controls.  The
characteristic-zero rank and factorization arguments remain the written
proof, not a finite-field inference.

## 9. Accepted frontier delta

The parent attempt materially changes the live obligation:

- the coefficient-only swallowed-circuit route is closed as an argument;
- the physical maximal rank-three locus is compressed to one rank-two common
  form;
- the internal port-pair layer is universally excluded in exact dimensions
  `21` and `19`, leaving the nine `Q`-meeting labels as the precise missing
  full-equation bridge;
- maximal stars have an explicit one-functional nonzero-scalar detector;
- the exact residuals are the simultaneous star scalar-zero divisor, the
  triangle full-support centre--radical line and its scalar-zero fibre, lower
  port ranks, fewer survivors, and non-leading/promoted supply.

No third targetwise sibling theorem is warranted before one of those parent
obligations is attacked.
