# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight target-kernel atlas and distinct-missing-colour exclusion

## Status

**Exact characteristic-zero target-row localization on the joint-rank-four,
derivative-rank-eight three-root cell, with one complete row-profile subcell
excluded.**  Retain the normalized, target-consistent physical `m=3`
common-three-space full-sensor hypotheses, let `U` be the total singleton
span, put `K=image H`, and assume

```text
dim U=3,                         dim K=4.             (1)
```

On the rank-eight chart of S2BQ, after permuting roots and rescaling,

```text
B_23=y tensor w,
B_13=-x tensor w,
B_12=C,                                              (2)

D(a,b,c)=(a tensor y-x tensor b) tensor w+C tensor c,
ker D=span((x,y,0)),
C notin A_1 tensor y+x tensor A_2.                  (3)
```

Here `K=D^(-1)(U)` and the displayed kernel line is contained in `K`.
Every one of the three transposed root-row maps has rank at least two.  A
rank-two first- or second-root row has one target-coordinate kernel, forces
the matching row or column of `C` to be a nonzero diagonal row or column,
and forces the corresponding coordinate of `x` or `y` to vanish.  A
rank-two third-root row has a one- or two-colour kernel supported only on
coordinate lines represented by `x` or `y`, and that kernel does not
annihilate `w`.

If both first and second root rows have rank two, their missing colours are
necessarily the **same**.  Distinct missing colours are inconsistent with
one coefficient of the complete empty-permanent target identity.  In the
same-colour survivor, `C` has an isolated nonzero diagonal entry, `x` and
`y` avoid that colour, and the third-root projection of `K` contains the
matching coordinate line.

This is the first full-empty-target exclusion inside the lower-rank
three-root rank-eight cell.  It is not a complete exclusion of that cell:
the `(3,3)`, mixed `(2,3)/(3,2)`, and same-missing-colour `(2,2)` profiles
remain, as do derivative rank seven, joint rank three, the pair gate, other
components and pole strata, higher orders, and the all-rank-drop branch.
It constructs neither a graph nor a counterexample.  Global Krenn--Gu
remains **UNRESOLVED**.

## 1. Physical rows and the coefficientwise target identity

Let

```text
rho:A_1^*->W^*,       pi:A_2^*->W^*,
theta:A_3^*->W^*,     W=X direct-sum Y direct-sum Z, (4)
```

be the three transposed root-row maps.  Since `H:W->K` is onto, these maps
are the restrictions of the three coordinate-dual families to `K`, followed
by the injection `H^*:K^*->W^*`.  Consequently

```text
rank rho=dim pr_1 K,
rank pi=dim pr_2 K,
rank theta=dim pr_3 K.                              (5)
```

Write the physical target identity coefficientwise in the source tensor
space `X^* tensor Y^* tensor Z^*` as

```text
G_N-J=sum_E E u_E,                   u_E in U,       (6)
```

where `E` ranges over any tensor basis containing the three pure target
monomials

```text
T_s=X_s tensor Y_s tensor Z_s,       s=0,1,2.       (7)
```

No regularity of the rational pair deck is used below.  Equation (6) is the
complete empty-permanent congruence, not a selected root slice.  If a root
covector lies in the kernel of one map in (4), multilinearity of the physical
six-term permanent kills the corresponding contraction of `G_N`.

## 2. First- and second-root kernel atlas

### Lemma 1 (a deficient involved row has one coordinate kernel)

For every nonzero `alpha in ker rho`, there is a unique colour `d` and a
nonzero scalar multiple such that

```text
alpha proportional e_d^*,
x_d=0,
(alpha tensor id)C proportional e_d and is nonzero. (8)
```

In particular,

```text
rank rho>=2.                                         (9)
```

If equality holds, after fixing the kernel generator,

```text
ker rho=span(e_d^*),
x_d=0,
(e_d^* tensor id)C=kappa e_d,       kappa!=0.       (10)
```

The root-exchanged statement is

```text
rank pi>=2,                                          (11)

rank pi=2 implies
ker pi=span(e_e^*),
y_e=0,
(id tensor e_e^*)C=lambda e_e,      lambda!=0.      (12)
```

#### Proof

Take `(a,b,c) in K`.  Because `alpha` annihilates `pr_1 K`, it annihilates
both `a` and `x`, the first component of the kernel vector in (3).  Contract
the derivative:

```text
(alpha tensor id tensor id)D(a,b,c)
  =((alpha tensor id)C) tensor c.                   (13)
```

Thus every tensor in `alpha(U)` has one fixed second-root factor line.
On the other hand `rho(alpha)=0` kills `alpha(G_N)`, while the coefficient
of `T_s` in `alpha(J)` is

```text
alpha(e_s) e_s tensor e_s.                          (14)
```

For every `s` in the coordinate support of `alpha`, equations (6), (13),
and (14) force `e_s` onto the one line `(alpha tensor id)C`.  Two distinct
supported colours are impossible.  Hence `alpha` is a coordinate covector,
the fixed contraction of `C` is the matching nonzero coordinate vector, and
`alpha(x)=0` gives `x_d=0`.

A kernel of dimension at least two contains a nonzero vector supported on
at least two target coordinates, so (9) follows.  The same argument after
exchanging roots one and two proves (11)--(12).  QED.

## 3. Third-root kernel atlas

Put

```text
T_(x,y)=A_1 tensor y+x tensor A_2.                  (15)
```

### Lemma 2 (third-row support is represented by the tangent factors)

For every nonzero `gamma in ker theta`,

```text
gamma(w)!=0,                                        (16)

s in support(gamma) implies
x proportional e_s or y proportional e_s.          (17)
```

Consequently

```text
rank theta>=2.                                      (18)
```

If `rank theta=2`, its kernel generator has support one or two.  A
two-colour support forces `x,y`, in one order, onto those two distinct
coordinate lines.

#### Proof

The covector `gamma` annihilates `pr_3 K`, so `gamma(c)=0` for every
`(a,b,c) in K`.  Contracting (3) gives

```text
(id tensor id tensor gamma)D(a,b,c)
  =gamma(w)(a tensor y-x tensor b).                 (19)
```

If `gamma(w)=0`, then `gamma(U)=0`, whereas the nonzero diagonal contraction
`gamma(J)` cannot be cancelled in (6).  This proves (16).  For every
`s in support(gamma)`, equations (6) and (19) require

```text
e_s tensor e_s in T_(x,y).                          (20)
```

Quotienting by `K x` in the first factor and `K y` in the second turns
(20) into

```text
(e_s mod K x) tensor (e_s mod K y)=0.               (21)
```

A pure tensor is zero exactly when one factor is zero, proving (17).
There are at most two such colours.  If `ker theta` had dimension at least
two, the linear functional `gamma |-> gamma(w)` would have a nonzero kernel
on it, contradicting (16).  Thus (18) holds.  The final statement follows
immediately from (17).  QED.

## 4. Distinct involved missing colours are impossible

### Theorem 3 (the `(2,2)` missing colours coincide)

Suppose

```text
rank rho=rank pi=2.                                 (22)
```

Let `d,e` be the kernel colours in (10) and (12).  Then

```text
d=e.                                                (23)
```

#### Proof

Assume `d!=e`.  Let `u_d` be the coefficient of `T_d` on the right side of
(6).  Since `r_d=rho(e_d^*)=0`, contracting (6) in the first root and taking
the `T_d` coefficient gives, up to the harmless global sign convention in
(6),

```text
(e_d^* tensor id tensor id)u_d=-e_d tensor e_d.     (24)
```

Choose `(a_d,b_d,c_d) in K` with

```text
D(a_d,b_d,c_d)=u_d.                                 (25)
```

The choice is unique modulo `ker D=span((x,y,0))`, so its third component is
well defined.  Equations (10), (13), and (24) force

```text
c_d=-kappa^(-1)e_d.                                 (26)
```

Now contract the same coefficient by the missing second-root row
`e_e^*`.  Because `d!=e`, the `T_d` coefficient of `e_e^*(J)` is zero, and
`p_e=0` kills the corresponding empty permanent.  Hence (6) requires

```text
(id tensor e_e^* tensor id)u_d=0.                   (27)
```

But `e_e^*` annihilates both `b_d` and `y`, so (3), (12), and (26) give

```text
(id tensor e_e^* tensor id)u_d
 =lambda e_e tensor c_d
 =-lambda kappa^(-1)e_e tensor e_d !=0,             (28)
```

contradicting (27).  Therefore (23) is necessary.  QED.

## 5. The same-colour `(2,2)` survivor

Let the common missing colour in Theorem 3 be `d`.  Equations (10) and (12)
have the same nonzero `(d,d)` entry, so

```text
C=kappa e_d tensor e_d+C_bar,       kappa!=0,
C_bar in A_(1,bar d) tensor A_(2,bar d),             (29)

x_d=y_d=0.                                           (30)
```

Here `A_(i,bar d)` is the coordinate plane spanned by the other two target
vectors.  Repeating (24)--(26) with the common colour shows

```text
e_d in pr_3 K.                                      (31)
```

If `rank theta=2` and `eta` spans its kernel, then

```text
eta_d=0,
support eta subset {0,1,2}\{d},
eta(w)!=0,                                          (32)
```

and every colour in `support eta` is represented by a coordinate one of
`x,y`.  In particular, support two makes `x,y` the two complementary
coordinate vectors in one order.

Finally, the S2BQ root-torus gate sharpens (29): if `C_bar!=0`, then `C`
is not a monomial, so

```text
w is coordinate.                                   (33)
```

If also `rank theta=2`, (32)--(33) put `w` on one of the coordinate lines
represented in the kernel support.  These are necessary conditions, not an
existence assertion.

## 6. Proof-topology consequence

The joint-rank-four, derivative-rank-eight three-root branch now has the
exact row-rank atlas

```text
(rank rho,rank pi,rank theta) in {2,3}^3;            (34)

rank-two rho/pi:
  one coordinate zero row + matching diagonal C row/column;

rank-two theta:
  one-/two-colour tangent-factor kernel, eta(w)!=0;

(2,2,q), distinct involved missing colours:         IMPOSSIBLE;

(2,2,q), common missing colour:
  isolated diagonal block (29), e_d in pr_3 K;       OPEN;

(3,3,q), (2,3,q), (3,2,q):                          OPEN.             (35)
```

The exclusion in Theorem 3 uses the complete coefficientwise target identity
and is therefore stronger than the derivative/root-torus census alone.  It
does not invoke pair-deck regularity, does not transfer to joint rank three
where the derivative kernel is transverse to `K`, and does not address the
rank-seven Hilbert--Burch cells.

## 7. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_target_kernel_atlas_and_distinct_missing_colour_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_target_kernel_atlas_and_distinct_missing_colour_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_target_kernel_atlas_and_distinct_missing_colour_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_target_kernel_atlas_and_distinct_missing_colour_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_target_kernel_atlas_and_distinct_missing_colour_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_target_kernel_atlas_and_distinct_missing_colour_exclusion.py
```

The primary replay checks the rank-eight derivative normal form, all three
contraction identities, the exact tangent quotient test, every coordinate
support fork, the distinct-colour contradiction, and the same-colour block
shape with SymPy.  The independent no-import audit reconstructs the
derivative, contractions, ranks, quotient membership, and contradiction with
standard-library `Fraction` arithmetic and a different tensor indexing.
The arbitrary-covector, coefficientwise target, and finite-dimensional
kernel arguments above are the proof.

## Dependencies

- [Lower-joint-rank three-root derivative and torus census](BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_THREE_ROOT_DERIVATIVE_AND_TORUS_CENSUS_THEOREM.md)
- [Common-shore singleton-slice and empty-permanent compatibility](BALANCED_FULL_SENSOR_COMMON_SHORE_SINGLETON_SLICE_AND_EMPTY_PERMANENT_COMPATIBILITY_THEOREM.md)
- [Singleton-span torus-annihilator obstruction](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)

## Scope boundary

```text
characteristic-zero rank-four/rank-eight row-kernel atlas: PROVED;
distinct involved missing-colour (2,2) subcell:             IMPOSSIBLE;
same-colour and higher involved-row profiles:               OPEN;
joint-rank-three/rank-eight target coupling:                 OPEN;
lower-rank rank-seven target coupling:                       OPEN;
pair-deck regularity for surviving three-root cells:         OPEN;
other S2T components / S2Q pole strata:                      OPEN;
higher balanced orders:                                     OPEN;
all-balanced rank-drop branch:                               OPEN;
global Krenn--Gu conjecture:                                 UNRESOLVED.    (36)
```
