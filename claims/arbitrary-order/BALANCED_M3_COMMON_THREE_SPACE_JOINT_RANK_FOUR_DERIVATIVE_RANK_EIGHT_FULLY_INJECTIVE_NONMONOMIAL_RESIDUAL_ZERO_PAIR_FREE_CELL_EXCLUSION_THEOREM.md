# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight fully-injective nonmonomial-residual zero-pair-free-cell exclusion

## Status

**Exact characteristic-zero exclusion of the zero-pair-free successor left by
S2CL in the fully-injective actual-nonmonomial residual cell.**  Retain S2CL's
physical hypotheses and notation:

```text
D(a,b,c)=(a tensor y-x tensor b) tensor e_t+C tensor c,
ker D=span((x,y,0)) subset K,                         rank D=8,

rank rho=rank pi=rank theta=3,
R=rho(x^perp),                 P=pi(y^perp),
Q=span(q_0,q_1,q_2),           Alt(Q)!=0,                         (1)
```

where the **actual** residual block `C` is nonmonomial and outside
`A_1 tensor y+x tensor A_2`.  On `x^perp by y^perp`, the exact corrected
cube is

```text
M_(r_alpha,p_beta)(q_k)
 =alpha_k beta_k T_k+C(alpha,beta)S_k.                           (2)
```

S2CL proves that every mixed zero pair is structural and belongs to an
explicit union of at most four projective points; correcting zero pairs are
impossible.  This theorem proves that the structural locus cannot be empty.
Equivalently,

```text
every surviving actual nonmonomial residual point
has at least one and at most four structural mixed zero pairs.             (3)
```

The proof exhausts S2BQ's remaining root-torus alternatives.  When `x,y` are
both noncoordinate, the tangent-quotient monomial supplies a correction-free
mixed map containing two transverse targets.  When one shared factor is
coordinate, the restriction of `C` is a `2 x 2` matrix; both its rank-one and
rank-two cases produce the same forbidden mixed map.  S2CK's exact
two-transverse mixed-map obstruction excludes every case.

This result does not exclude the structural-zero cells themselves.  It does
not address lower-rank derivatives, pair coupling elsewhere, other components
or poles, higher orders, or all-rank drop.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. Exhaustive S2BQ split

Since the actual `C` is nonmonomial, S2BQ first makes `w` coordinate, as used
in (1).  Its second root-torus condition is the exhaustive alternative

```text
x is coordinate, or y is coordinate, or

C(alpha,beta)=lambda alpha_d beta_e
  on x^perp by y^perp,              lambda!=0,
  with x,y both noncoordinate.                                      (4)
```

The restriction of `C` to `x^perp by y^perp` is nonzero because the kernel
of that restriction is exactly the tangent space
`A_1 tensor y+x tensor A_2`, and the rank-eight premise excludes `C` from
that space.

Assume for contradiction that there is no structural zero pair.  By S2CL
there is then no mixed zero pair of any kind.  We exclude the two branches
in (4).

## 2. Both shared factors noncoordinate

Assume the last alternative of (4).  Since `x` is not coordinate, the
coordinate evaluation `alpha -> alpha_d` is nonzero on the plane `x^perp`.
Choose a nonzero covector on its kernel line:

```text
0!=alpha in x^perp,                  alpha_d=0.                     (5)
```

If `alpha` were supported on one coordinate `a`, then `a!=d`.  The two
hyperplanes `y^perp` and `{beta:beta_a=0}` meet in a nonzero line, so choose

```text
0!=beta in y^perp,                   beta_a=0.                      (6)
```

The supports of `alpha,beta` are disjoint and (4)--(5) give
`C(alpha,beta)=0`.  This is a structural zero pair, contrary to the standing
assumption.  Therefore `alpha` has both coordinates complementary to `d` in
its support.  Write them as `i,j`:

```text
support alpha={i,j},                 {i,j,d}={0,1,2}.                (7)
```

Because `y` is noncoordinate, neither coordinate evaluation `beta_i` nor
`beta_j` vanishes identically on `y^perp`.  Over the infinite
characteristic-zero field, their two kernel lines do not cover that plane.
Choose

```text
beta in y^perp,                      beta_i beta_j!=0.               (8)
```

Again `C(alpha,beta)=0`, now because `alpha_d=0`.  Equations (2), (7), and
(8) give

```text
M_(r_alpha,p_beta)(q_i)=alpha_i beta_i T_i!=0,
M_(r_alpha,p_beta)(q_j)=alpha_j beta_j T_j!=0,
M_(r_alpha,p_beta)(q_d)=0.                                          (9)
```

Thus one mixed map from the physical three-space lies in
`span(T_i,T_j)` and contains both fully transverse decomposable endpoints.
S2CK Lemma 1 says this is impossible.

## 3. One shared factor coordinate

Assume after root exchange that

```text
x proportional e_s,                 {i,j}={0,1,2} minus {s}.        (10)
```

Then `x^perp=span(epsilon_i,epsilon_j)`.  First, the no-structural-zero
assumption forces

```text
y_s!=0.                                                             (11)
```

Indeed, if `y_s=0`, then `beta=epsilon_s` lies in `y^perp`.  The linear
functional `alpha -> C(alpha,epsilon_s)` on the two-plane `x^perp` has a
nonzero kernel.  Any nonzero kernel row has support disjoint from
`epsilon_s`, producing a structural zero.

Condition (11) makes coordinate projection an isomorphism

```text
pr_(i,j):y^perp -> F^2.                                              (12)
```

Use (12) to represent the nonzero restriction of `C` by a `2 x 2` matrix

```text
D=(D_(a,b))_(a,b in {i,j}).                                         (13)
```

Both cross entries are nonzero:

```text
D_(i,j)D_(j,i)!=0.                                                   (14)
```

For example, if `D_(i,j)=0`, take `alpha=epsilon_i` and the unique
`beta in y^perp` whose `(i,j)` projection is `epsilon_j`.  The support of
`beta` avoids `i`, so this is a structural zero.  The other cross entry is
identical after exchanging `i,j`.

### Rank two

Suppose `det D!=0`.  In the two-dimensional `alpha` plane avoid the four
proper lines

```text
alpha_i=0,                  alpha_j=0,
(alpha^T D)_i=0,            (alpha^T D)_j=0.                        (15)
```

Their finite union does not cover the plane over an infinite field.  For the
chosen `alpha`, write

```text
alpha^T D=(r_i,r_j),                  r_i r_j!=0.                   (16)
```

Choose `beta in y^perp` using (12) so that

```text
(beta_i,beta_j)=(r_j,-r_i).                                         (17)
```

Then

```text
C(alpha,beta)=alpha^T D beta=0,
alpha_i alpha_j beta_i beta_j!=0.                                  (18)
```

### Rank one

Suppose `rank D=1`.  Over the base field write

```text
D=u v^T.                                                            (19)
```

The two nonzero cross entries in (14) force all four coordinates of `u,v`
to be nonzero.  Take a nonzero full-support left-kernel covector, for example

```text
alpha=(u_j,-u_i),                                                    (20)
```

and choose any `beta in y^perp` whose `(i,j)` projection has both entries
nonzero.  Then (18) holds again.

In either rank case, `alpha_s=0`, so the third coordinate product vanishes.
The exact cube gives

```text
M_(r_alpha,p_beta)(q_i)=alpha_i beta_i T_i!=0,
M_(r_alpha,p_beta)(q_j)=alpha_j beta_j T_j!=0,
M_(r_alpha,p_beta)(q_s)=0.                                         (21)
```

This is again the forbidden S2CK transverse secant.  Root exchange handles
the alternative in which `y`, rather than `x`, is coordinate.

The branches in (4) are exhaustive, so the zero-pair-free cell is empty.
Combining this with S2CL proves (3).

## 4. Evidence and proof ownership

The primary symbolic replay checks the support-wall constructions, the exact
correction zeros and two-target values, both `2 x 2` rank branches, and the
root-exchanged cases.  The independent standard-library audit reconstructs
those interfaces with separate rational linear algebra, reversed support and
coordinate-wall traversals, and independent rational fixtures.  The scripts
do not replace the analytic S2BQ root-torus atlas or S2CK mixed-map
obstruction.

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_nonmonomial_residual_zero_pair_free_cell_exclusion.py
python -B -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_nonmonomial_residual_zero_pair_free_cell_exclusion.py
```

## Dependencies

- [Lower-joint-rank three-root derivative and torus census](BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_THREE_ROOT_DERIVATIVE_AND_TORUS_CENSUS_THEOREM.md)
- [Nonmonomial complete-target zero-pair localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_NONMONOMIAL_RESIDUAL_COMPLETE_TARGET_ZERO_PAIR_LOCALIZATION_THEOREM.md)
- [Diagonal two-visible-cell exclusion and mixed-map lemma](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_TWO_VISIBLE_CELL_EXCLUSION_THEOREM.md)

## Scope boundary

```text
fully-injective rank-four/rank-eight actual nonmonomial residual:
  correcting mixed zero pairs:                          IMPOSSIBLE (S2CL);
  zero-pair-free cell:                                  IMPOSSIBLE;
  structural mixed zero pairs per point:                BETWEEN ONE AND FOUR;
  structural-zero cells after incidence localization:   OPEN;

monomial residual branch:                               CLOSED (S2CC--S2CK);
other lower-rank cells / components / poles:             OPEN;
higher balanced orders / all-balanced rank drop:         OPEN;
global Krenn--Gu conjecture:                             UNRESOLVED.       (22)
```
