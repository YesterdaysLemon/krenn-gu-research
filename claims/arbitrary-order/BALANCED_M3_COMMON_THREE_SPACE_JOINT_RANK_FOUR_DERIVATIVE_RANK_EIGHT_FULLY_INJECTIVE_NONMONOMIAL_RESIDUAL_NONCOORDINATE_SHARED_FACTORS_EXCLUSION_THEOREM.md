# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight fully-injective nonmonomial-residual noncoordinate-shared-factors exclusion

## Status

**Exact characteristic-zero exclusion of the structural-zero successor in
which both shared factors are noncoordinate.**  Retain S2CL--S2CM's physical
hypotheses and notation.  Thus

```text
D(a,b,c)=(a tensor y-x tensor b) tensor e_t+C tensor c,
ker D=span((x,y,0)) subset K,                         rank D=8,

R=rho(x^perp),             P=pi(y^perp),
Q=span(q_0,q_1,q_2),       Alt(Q)!=0,                              (1)
```

the **actual** residual block `C` is nonmonomial, and on
`x^perp by y^perp` the complete target implies

```text
M_(r_alpha,p_beta)(q_s)
 =alpha_s beta_s T_s+C(alpha,beta)S_s.                            (2)
```

S2CL excludes every correcting mixed zero and S2CM proves that at least one
structural mixed zero exists.  This theorem proves

```text
actual nonmonomial survivor in this fully-injective rank cell
  => x is coordinate or y is coordinate.                            (3)
```

The proof first uses S2CK to make one structural shore coordinate.  Its
one-sided target table is then coupled to S2CG's zero-pair classification.
An independent pair gives an aligned split plane or split three-space and a
retained face makes the actual `C` monomial.  A dependent pair is pure; a
one-factor source slab forces the two shared factors onto the same
two-coordinate support, which supplies a second structural corner.  S2CI's
two-cross incidence dichotomy and the same retained-face quotient finish the
proof.

The coordinate-`x`/coordinate-`y` structural cells remain open in this
theorem.  It does not address lower derivative ranks, pair coupling
elsewhere, other components or poles, higher orders, or all-rank drop.
Global Krenn--Gu remains **UNRESOLVED**.

## 1. The S2BQ quotient and a coordinate shore

Assume for contradiction that both `x` and `y` are noncoordinate.  S2BQ
then gives, on the perpendicular planes,

```text
C(alpha,beta)=lambda alpha_d beta_e,                lambda!=0.     (4)
```

Choose a nonzero row on the kernel line

```text
alpha in x^perp,                    alpha_d=0.                      (5)
```

If `alpha` had two nonzero coordinates, noncoordinate `y` would let us
choose `beta in y^perp` nonzero on both of them.  Equation (4) would make the
correction zero, while (2) would put both corresponding fully transverse
targets in one mixed map.  This is forbidden by S2CK Lemma 1.  Since
`alpha_d=0`, the only alternative is

```text
alpha=epsilon_a,          a!=d,          x_a=0,
support x={0,1,2} minus {a}.                              (6)
```

For every `b in y^perp`, (2), (4), and (6) now give the exact one-sided
table

```text
M_(r_a,p_b)|Q=b_a lambda_a tensor T_a,
lambda_a(q_s)=delta_(a=s).                                        (7)
```

The functional `b -> b_a` is nonzero on `y^perp`, since otherwise `y` would
be proportional to `e_a`.  Choose its nonzero kernel row `beta` and a
complement `b` with `b_a!=0`, and put

```text
u=r_a,              v=p_beta,              B=p_b.                  (8)
```

Injectivity gives two-planes `R,P subset Q`, the rows `v,B` are independent,
and

```text
M_(u,v)|Q=0,                    M_(u,B)|Q!=0.                       (9)
```

We split according to whether `u,v` are independent.

## 2. Independent zero pair

S2CG Lemma 1 writes, after permuting the three physical sources,

```text
u=xi+eta,              v=mu(xi-eta),
H=span(xi,eta),        xi in X^*, eta in Y^*.                      (10)
```

Let `Z^*` denote the omitted source.  If `B_Z=0`, then `B in H`: indeed,
`H` is the two-dimensional kernel of the nonzero projection `Q -> Z^*`.
The nonzero map in (9) is a scalar multiple of

```text
q -> xi tensor eta tensor q_Z.                                   (11)
```

Consequently

```text
P=H=ker lambda_a,                                                 (12)
```

and the two source lines in `H` together with the omitted projection of
`Q` are the three factor lines of `T_a`.

If `B_Z!=0`, evaluation of `M_(u,B)` at `u` aligns `B_Z` with the omitted
factor of `T_a`.  Evaluation at `B`, followed by quotienting the `xi` and
`eta` factor lines, gives

```text
B_X in span(xi),                 B_Y in span(eta).                 (13)
```

Subtracting these two components from `B` puts a pure omitted-source row in
`Q`.  Hence

```text
Q=span(xi,eta,zeta)                                                   (14)
```

is a split three-source space aligned with `T_a`.

Write `{i,j}={0,1,2} minus {a}` and choose

```text
ell in {i,j},                       ell!=t.                         (15)
```

Such a colour always exists; when `t=a`, either complementary colour is
retained.

In (12), `q_ell in H`; in (14), every `q_ell` is a sum of the three aligned
pure rows.  Quotient all three physical source factors by the factor lines
of `T_a`.  In either case the entire physical slice `P^(ell)` dies.  The
same quotient of the corrected cube gives, for a nonzero scalar `c_ell`,

```text
bar S_ell=-c_ell bar T_ell.                                        (16)
```

Here `c_ell!=0` because the restricted coordinate bilinear form, the
nonzero restriction of `C`, and `bar T_ell` are all nonzero.  Since
`ell!=t`, the complete retained face is

```text
P^(ell)-E_(ell,ell)T_ell=C S_ell.                                 (17)
```

After quotienting, (16)--(17) force

```text
C=c_ell^(-1) E_(ell,ell),                                         (18)
```

contrary to the standing actual-nonmonomial premise.  Thus the independent
case is impossible.

## 3. Dependent zero pair and the one-factor slab

Assume `u,v` are dependent.  Since `M_(u,u)|Q=0`, the square-zero branch of
S2CG Corollary 2 makes their common nonzero row pure.  Normalize

```text
u=X_a.                                                             (19)
```

Write `B=B_X+B_Y+B_Z`.  At least one of `B_Y,B_Z` is nonzero, because the
map `M_(u,B)` in (9) is nonzero.  If `B_Z!=0` and `B_Y=0`, the fixed-line
identity

```text
M_(u,B)(q)
 =X_a tensor (B_Y tensor q_Z+q_Y tensor B_Z)
 in span(T_a)                                                       (20)
```

first supplies a row with nonzero `Y` component, aligns `B_Z` with the `Z`
factor of `T_a`, and then forces the `Y`-projection of every row in `Q` onto
the `Y` factor line of `T_a`.  If `B_Y B_Z!=0`, evaluation at `B` first
aligns both components with their target factor lines; quotienting those
lines then fixes both projections of `Q`.  The case `B_Y!=0,B_Z=0` is the
source-exchanged version.  Thus every permanent of three rows of `Q`
belongs to at least one one-factor slab `L` through `T_a`; no cancellation
between unaligned components is being assumed.

For each `s!=a`, reduce (2) modulo that slab.  The physical permanent dies,
whereas `bar T_s` survives, and simple-tensor separation gives

```text
b_s=c_s bar C,                    c_s!=0,
bar S_s=-c_s bar T_s,                                             (21)
```

where

```text
b_s=(epsilon_s|x^perp) tensor (epsilon_s|y^perp),
bar C=C|_(x^perp by y^perp).                                      (22)
```

For the two colours `{i,j}={0,1,2} minus {a}`, (21) makes
`b_i,b_j` proportional.  Since `x_a=0` already and both shared factors are
noncoordinate, proportionality of these restricted coordinate evaluations
forces

```text
support x=support y={i,j}.                                        (23)
```

In particular, `epsilon_a in y^perp`.  Let `alpha_0` span the line

```text
x^perp intersect {alpha:alpha_a=0},
```

and put `A=r_(alpha_0)`.  The two rows `u,A` form a basis of `R`, while
`u,p_a` form a basis of `P`.  Equation (21) also makes `bar C` proportional
to either non-`a` coordinate bilinear form.  Therefore

```text
M_(A,p_a)|Q=0,                 M_(u,u)|Q=0,
M_(u,p_a)|Q=lambda_a tensor T_a!=0.                               (24)
```

The target products and correction in the first identity vanish
separately; no cancellation or divisor is used.

## 4. The second corner and the retained face

Apply S2CI's two-cross-pair incidence dichotomy to the bases

```text
R=span(u,A),                 P=span(p_a,u).                         (25)
```

The two zeros and visible corner in (24) give exactly one of

```text
(i)  Q is a split three-source space aligned with T_a;

(ii) R=P=H=ker lambda_a is a split two-source plane
     aligned with the two used-source factor lines of T_a.         (26)
```

Take again `ell in {i,j}` with `ell!=t`.  In (i), every `q_ell` is a sum of the three
aligned pure rows; in (ii), `q_ell in H`.  Quotienting the three factor lines
of `T_a` therefore kills the complete physical slice `P^(ell)`.  Equation
(21) remains

```text
bar S_ell=-c_ell bar T_ell,
```

and the retained face (17) again forces the actual identity (18).  This is
impossible for nonmonomial `C` and closes the dependent case.

Combining Sections 2 and 4 proves (3).

## 5. Evidence and proof ownership

The primary symbolic replay checks the finite support/kernel gate, the
one-sided table, both independent incidences, the dependent one-factor slab,
the proportional bilinear forms, the manufactured opposite corner, and the
retained-face sign.  The independent standard-library audit reconstructs
the same interfaces with separate rational fixtures and reversed support,
source, and incidence traversal.  The scripts do not replace S2BQ's torus
atlas, S2CG's zero-pair classification, S2CI's incidence dichotomy, or S2CK's
mixed-map lemma.

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_nonmonomial_residual_noncoordinate_shared_factors_exclusion.py
python -B -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_nonmonomial_residual_noncoordinate_shared_factors_exclusion.py
```

## Dependencies

- [Lower-joint-rank three-root derivative and torus census](BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_THREE_ROOT_DERIVATIVE_AND_TORUS_CENSUS_THEOREM.md)
- [Canonical-binomial zero-pair geometry](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_CANONICAL_BINOMIAL_RESIDUAL_EXCLUSION_THEOREM.md)
- [Same-coordinate one-visible two-cross incidence dichotomy](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_SAME_COORDINATE_ONE_VISIBLE_WALL_EXCLUSION_THEOREM.md)
- [Diagonal two-visible mixed-map obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_TWO_VISIBLE_CELL_EXCLUSION_THEOREM.md)
- [Nonmonomial complete-target zero-pair localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_NONMONOMIAL_RESIDUAL_COMPLETE_TARGET_ZERO_PAIR_LOCALIZATION_THEOREM.md)
- [Nonmonomial zero-pair-free-cell exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_NONMONOMIAL_RESIDUAL_ZERO_PAIR_FREE_CELL_EXCLUSION_THEOREM.md)

## Scope boundary

```text
fully-injective rank-four/rank-eight actual nonmonomial residual:
  correcting mixed zero pairs:                          IMPOSSIBLE (S2CL);
  zero-pair-free cell:                                  IMPOSSIBLE (S2CM);
  both shared factors noncoordinate:                    IMPOSSIBLE;
  x coordinate or y coordinate structural cells:       OPEN;

monomial residual branch:                               CLOSED (S2CC--S2CK);
other lower-rank cells / components / poles:             OPEN;
higher balanced orders / all-balanced rank drop:         OPEN;
global Krenn--Gu conjecture:                             UNRESOLVED.       (27)
```
