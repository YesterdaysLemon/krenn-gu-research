# Balanced `m=3` singleton-span torus-annihilator permanent-rank obstruction

## Status

**Exact characteristic-zero obstruction for every normalized physical `m=3`
target incidence.**  Let `U` be the total root-tensor span of the nine
singleton slices of one physical balanced shore.  No decomposable root
functional can both annihilate `U` and be nonzero on all nine local
colour coordinates.

Indeed, such a functional kills all three pair-column contributions.  The
physical empty companion contracts to a local image of the order-three
permanent tensor `P_3`, while the GHZ target contracts to a three-term
diagonal tensor with all coefficients nonzero.  Its three flattening ranks
force all local maps on `P_3` to be invertible.  Tensor rank is then preserved,
contradicting

```text
rank(P_3)=4,              rank(Delta_3)=3.             (1)
```

Consequently the projective product-annihilator section of `U` is contained
entirely in the coordinate boundary.  In the common-three-space pole stratum
localized by S2Q, projective dimension guarantees an annihilator family of
dimension at least three, so that whole family must be boundary-supported.

This does not prove that such boundary-supported singleton spaces are
impossible.  It does not exclude the rank-one, pair-plane, or common-three-
space pole strata, extend to `m>=4`, exclude the all-balanced rank-drop
branch, or resolve the conjecture.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. Physical `m=3` target incidence modulo singleton columns

Work over `C`; the final field-extension remark below gives the same
obstruction over characteristic zero.  Use the physical common-shore notation
of the
[`singleton-slice and empty-permanent theorem`](BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md).
The three root spaces are `A_1,A_2,A_3`, the nonroots are `x,y,r`, and the
three singleton columns are

```text
G_x(x),             G_y(y),             G_r(r)
 in A=A_1 tensor A_2 tensor A_3.                         (2)
```

Define their fixed total image space

```text
U=span_C(image G_x, image G_y, image G_r) subset A.      (3)
```

Suppose the sensor is target-consistent and has empty normalization.  The
three rational pair components then satisfy

```text
J-G_N=G_x C_yr+G_y C_xr+G_r C_xy.                       (4)
```

The right side lies in `U` over the function field.  Composing (4) with the
fixed quotient `A -> A/U` gives a polynomial section that vanishes at the
generic point, hence vanishes identically:

```text
G_N congruent J                  modulo U.               (5)
```

No regularity of the rational pair components is needed for (5).

## 2. Product annihilators and the `P_3` contraction

Let

```text
a=a_1 tensor a_2 tensor a_3 in A^*,
a_i in A_i^*,                                         (6)
```

be a nonzero decomposable functional.  In the target coordinate bases, call
`a` **fully supported** when

```text
a_i(e_(i,c)) !=0              for every i and c.        (7)
```

Assume for contradiction that

```text
a annihilates U.                                      (8)
```

For each nonroot `u in {x,y,r}`, collect the three contracted cross-edge
forms into a linear map

```text
L_u:C^3 -> L_u^*,
L_u(e_i)=W_(i,u)(a_i,-).                              (9)
```

Here the source basis labels which of the three roots is paired to `u`.
The six cross matchings in the physical empty companion give exactly

```text
a(G_N)=(L_x tensor L_y tensor L_r) P_3,              (10)

P_3=sum_(sigma in S_3)
      e_(sigma(1)) tensor e_(sigma(2)) tensor e_(sigma(3)). (11)
```

On the other hand, (5), (7), and (8) give

```text
a(G_N)=a(J)
 =sum_(c=0)^2 kappa_c x_c tensor y_c tensor r_c,

kappa_c=product_(i=1)^3 a_i(e_(i,c)) !=0.            (12)
```

Thus a local image of `P_3` is a concise three-term diagonal tensor.

## 3. The torus-annihilator obstruction

### Theorem 1 (fully supported product annihilators are impossible)

Under the physical target-consistency and normalization hypotheses of
Section 1,

```text
P(U^perp) intersect Seg(P(A_1^*) x P(A_2^*) x P(A_3^*))
```

contains no point satisfying (7).

### Proof

Every one-mode flattening of the diagonal tensor (12) has rank three.  The
corresponding flattening of the local image (10) has rank at most
`rank(L_u)`.  Hence

```text
rank(L_x)=rank(L_y)=rank(L_r)=3.                      (13)
```

All three maps are invertible.  Their tensor product therefore preserves
tensor rank.

The exact three-blocker permanent-rank lemma proves

```text
rank(P_3)=4.                                         (14)
```

For completeness, the first-mode slice space of `P_3` is

```text
[ 0 z y ]
[ z 0 x ].                                           (15)
[ y x 0 ]
```

Its principal `2 x 2` minors are `-z^2,-y^2,-x^2`, so it contains no
nonzero rank-one matrix.  A rank-three decomposition, together with the
three rank-three flattenings, would put three nonzero rank-one matrices in
that slice space.  This proves the lower bound four.  The standard four-term
polarization gives the matching upper bound.

The tensor in (12) has tensor rank exactly three: its flattening rank is
three and its displayed expression has three terms.  Equations (10), (13),
and (14) would therefore make its tensor rank four and three simultaneously.
This contradiction proves the theorem.  QED.

The argument is defined by finitely many coefficients.  A putative solution
over any characteristic-zero field descends to a finitely generated extension
of `Q`, which embeds in `C`, so the same obstruction holds there.

## 4. Geometry of the surviving annihilator section

Let

```text
Sigma=Seg(P(A_1^*) x P(A_2^*) x P(A_3^*)) subset P(A^*).
                                                               (16)
```

It has dimension six.  If `s=dim U`, then `P(U^perp)` is a linear subspace
of codimension `s` in `P(A^*)`.  For `s<=6`, the projective dimension theorem
gives

```text
dim(Sigma intersect P(U^perp)) >= 6-s.               (17)
```

Theorem 1 says every point of this intersection lies in the union of the
nine coordinate boundary divisors

```text
a_i(e_(i,c))=0.                                      (18)
```

In particular, on the S2Q common-three-space pole stratum `s=3`, there is an
annihilator family of dimension at least three, but it is entirely contained
in (18).  This converts that pole stratum into a concrete boundary-incidence
problem rather than an arbitrary rational-section problem.

There is one immediate full-rank boundary.  Let

```text
D=span(e_(1,c) tensor e_(2,c) tensor e_(3,c):0<=c<=2)
                                                               (19)
```

be the target diagonal root plane.  If `D subset U`, then `J` lies in `U`.
Equation (5) puts `G_N` in `U` as well, so all four sensor columns lie in the
three-dimensional space `U` when `s=3`.  A common-three-space full sensor
therefore cannot have `U=D`.  This does not exclude other boundary-blocking
three-spaces.

## 5. Sharp boundary

The fully-supported qualifier in Theorem 1 is load-bearing.  Take

```text
U=D.                                                  (20)
```

To annihilate `U`, a product functional must satisfy

```text
product_i a_i(e_(i,c))=0             for c=0,1,2,    (21)
```

so every product annihilator lies in the coordinate boundary.  Thus a
three-space can genuinely block the root torus.  As just noted, this
particular three-space is incompatible with full sensor rank under target
consistency; it is a sharpness example for the annihilator geometry, not a
physical target incidence or graph.

Likewise, if (12) has only two nonzero `kappa_c`, its tensor rank is two and
the flattening argument forces only `rank(L_u)>=2`.  Rank-two restrictions of
`P_3` are not excluded by the rank-four-versus-rank-three argument.  Boundary
annihilators therefore require a separate zero/binary/decomposable analysis;
Theorem 1 does not silently dispose of them.

## 6. Proof-topology consequence

Together with S2Q, the `m=3` physical incidence boundary is now

```text
any pair pole
  -> rank-one singleton, pair-plane, or common-three-space incidence;

any normalized physical target incidence
  -> its total singleton span blocks every fully supported
     decomposable root annihilator;

common-three-space pole incidence
  -> a positive-dimensional product-annihilator section exists,
     but every component is forced onto the coordinate boundary.   (22)
```

The next exact obligation is to classify those boundary product-annihilator
components against the physical shared-factor map and the zero, binary, and
decomposable restrictions of `P_3`.

```text
physical empty companion contracts from P_3:          PROVED;
fully supported singleton-span annihilator:            IMPOSSIBLE;
common-three-space annihilator dimension at least 3:   PROVED;
all such annihilators boundary-supported:               PROVED;
target diagonal three-space supports full sensor:      IMPOSSIBLE;
boundary product-annihilator classification:            OPEN;
three S2Q exceptional pole strata:                     OPEN;
arbitrary m full-sensor gate:                          OPEN;
all-balanced rank-drop branch:                         OPEN;
global Krenn--Gu conjecture:                           UNRESOLVED.         (23)
```

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_singleton_span_torus_annihilator_permanent_rank_obstruction.py
python -I claims/arbitrary-order/audit_balanced_m3_singleton_span_torus_annihilator_permanent_rank_obstruction.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_singleton_span_torus_annihilator_permanent_rank_obstruction.py claims/arbitrary-order/audit_balanced_m3_singleton_span_torus_annihilator_permanent_rank_obstruction.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_singleton_span_torus_annihilator_permanent_rank_obstruction.py claims/arbitrary-order/audit_balanced_m3_singleton_span_torus_annihilator_permanent_rank_obstruction.py
```

The primary replay reconstructs the six-term `P_3` contraction interface,
all three flattenings, the no-rank-one slice certificate, the four-term
polarization, the diagonal rank, and the target-plane boundary.  The
independent no-import audit uses exact `Fraction` row reduction, a separate
sparse tensor implementation, direct permutation contraction, and a separate
polarization replay.  The projective dimension and target-incidence arguments
are the written proofs above.

## Dependencies

- [`BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md`](BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md)
- [`BALANCED_M3_FULL_SENSOR_SEPARATED_SINGLETON_POLE_LOCALIZATION_THEOREM.md`](BALANCED_M3_FULL_SENSOR_SEPARATED_SINGLETON_POLE_LOCALIZATION_THEOREM.md)
- [`EXACT_THREE_BLOCKER_PERMANENT_RANK_LEMMA.md`](EXACT_THREE_BLOCKER_PERMANENT_RANK_LEMMA.md)
- [`P3_ZERO_HYPERPLANE_PRODUCT_THEOREM.md`](../p3/restrictions/P3_ZERO_HYPERPLANE_PRODUCT_THEOREM.md)
- [`P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md`](../p3/restrictions/P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md)
