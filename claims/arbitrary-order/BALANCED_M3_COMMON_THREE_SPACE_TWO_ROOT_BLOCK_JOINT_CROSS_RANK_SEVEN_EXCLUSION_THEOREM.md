# Balanced `m=3` common-three-space two-root-block joint-rank-seven exclusion

## Status

**Exact characteristic-zero exclusion of the remaining joint-cross-rank-seven
part of the S2Q common-three-space stratum.**  Let `U` be the total singleton
span of a normalized, target-consistent physical `m=3` common shore, assume

```text
dim U=3,                                                (1)
```

and let

```text
H:X direct-sum Y direct-sum Z
  -> A_1 direct-sum A_2 direct-sum A_3                 (2)
```

be the joint root--nonroot cross-colour map.  If at least two root--root
blocks are nonzero, then

```text
rank H !=7.                                             (3)
```

The preceding S2Z theorem excludes rank seven when exactly one root block is
nonzero; the zero-root-block case cannot have a three-dimensional singleton
span.  Therefore every surviving common-three-space incidence satisfies

```text
rank H<=6.                                              (4)
```

This is a strict local frontier advance, not a resolution.  Joint rank at
most six, the multi-boundary, `beta=0`, and collapsed cross-column component
types outside this rank-seven chart, the rank-one and pair-plane pole strata,
every higher order, the all-balanced branch, a witness, and a counterexample
remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. Codimension two forces the sharp shared-factor derivative

Let `D_B` be the shared derivative of the three root--root blocks and put

```text
K=image H.                                              (5)
```

The physical singleton formula gives

```text
U=D_B(K).                                               (6)
```

At rank seven, `K` has codimension two in the nine-dimensional domain of
`D_B`.  Hence

```text
rank D_B<=rank(D_B restricted to K)+2=5.               (7)
```

Two nonzero root blocks give rank at least five by the pairwise shared-factor
intersection lemma in S2U.  Thus equality holds in (7).  The two blocks are
rank-one and share their common endpoint factor.  A third nonzero block is
impossible: the first two derivative summands have the normal form

```text
(A_1 tensor y+x tensor A_2) tensor z,                 (8)
```

of dimension five, whereas the third summand contains `B_12 tensor z'` for
every `z' in A_3` and cannot be contained in the fixed `z`-factor space (8).

After permuting roots and rescaling, therefore,

```text
B_23=y tensor z,
B_13=x tensor z,
B_12=0,                                               (9)

D_B(a,b,c)=(a tensor y+x tensor b) tensor z.          (10)
```

The derivative has rank five and kernel

```text
N=span((x,-y,0)) direct-sum A_3,          dim N=4.    (11)
```

Since `rank(D_B|K)=3`, rank--nullity gives

```text
N subset K,
K=D_B^(-1)(U).                                        (12)
```

Write

```text
U=U_0 tensor z,
U_0 subset A_1 tensor y+x tensor A_2,       dim U_0=3. (13)
```

The S2R torus-annihilator obstruction forces `z` to be a target coordinate
vector.  Indeed, if `z` used at least two target coordinates, its annihilator
hyperplane would contain a covector nonzero on all three coordinates.
Together with arbitrary fully supported covectors on `A_1,A_2`, that would
give a fully supported decomposable annihilator of `U`.  Thus, for one target
colour `s`,

```text
z=e_(3,s)                                              (14)
```

up to a nonzero scalar.  Target consistency now says

```text
G_N in J+U_0 tensor e_(3,s).                          (15)
```

Let `t,u` be the two colours other than `s`.

## 2. The two involved root block rows have rank three

Let

```text
rho:A_1^* -> W^*,       pi:A_2^* -> W^*,
theta:A_3^* -> W^*,     W=X direct-sum Y direct-sum Z (16)
```

be the three transposed block rows of `H`, and write

```text
r_a=rho(e_a^*),       p_b=pi(e_b^*),       q_c=theta(e_c^*). (17)
```

Equation (12) contains all of `A_3`.  Consequently `theta` is injective and
its image is disjoint from `image rho+image pi`.  Since `rank H=7`,

```text
rank theta=3,
dim(image rho+image pi)=4.                            (18)
```

For `c=t,u`, the root-3 slice of (15) is unaffected by `U`.  Therefore

```text
per(r_a,p_b,q_c)
 =delta_(a,c) delta_(b,c) X_c Y_c Z_c                (19)
```

as an exact polynomial identity for every `a,b`.

Suppose `rho` had a nonzero kernel vector `alpha`.  Contracting (19) by
`alpha` first with `c=t` and then with `c=u` gives

```text
alpha_t=alpha_u=0.                                    (20)
```

Thus `ker rho` has dimension at most one and `rank rho>=2`.  If equality
held, then `ker rho=span(e_s^*)`, so

```text
r_s=0.                                                 (21)
```

Let

```text
K_12=K intersect (A_1 direct-sum A_2).                (22)
```

Equation (21) means every `(a,b) in K_12` has `a_s=0`.
Since the kernel vector `(x,-y)` in (11) belongs to `K_12`, it also gives
`x_s=0`.  Formula (10) then shows that every tensor in `U_0` has zero
root-1 colour-`s` slice.  In particular,

```text
e_(1,s) tensor e_(2,s) notin U_0.                    (23)
```

But (21) makes the root-1 colour-`s` slice of `G_N` zero.  The coefficient of
the pure source word `X_sY_sZ_s` in (15) would then require precisely the
tensor excluded by (23).  This contradiction proves `rank rho=3`.

The symmetric argument proves

```text
rank rho=rank pi=3.                                   (24)
```

Combining (18) and (24), the two three-dimensional row spaces meet in a
two-plane.  No classification of that intersection will be needed.

## 3. Pointwise matrix slices give the contradiction

Choose arbitrary local colour vectors

```text
xi in X,       eta in Y,       zeta in Z.             (25)
```

For `w=(w_X,w_Y,w_Z) in W^*`, put

```text
hat w=(w_X(xi),w_Y(eta),w_Z(zeta)) in K^3.            (26)
```

Let `R(xi,eta,zeta)` and `P(xi,eta,zeta)` be the `3 x 3` matrices whose
rows are `hat r_a` and `hat p_b`, and let `hat q_c` be the evaluated vector
for `q_c`.  Define the zero-diagonal symmetric matrix

```text
             [       0  q_Z  q_Y ]
M(q_X,q_Y,q_Z)=[ q_Z       0  q_X ].                  (27)
             [ q_Y     q_X       0 ]
```

Direct expansion of the six permanent terms gives

```text
[per(r_a,p_b,q_c)(xi,eta,zeta)]_(a,b)
 =R M(hat q_c) P^T.                                   (28)
```

On the dense open set where both pure target monomials are nonzero, (19)
becomes

```text
R M(hat q_t) P^T=mu_t E_(t,t),
R M(hat q_u) P^T=mu_u E_(u,u),       mu_t mu_u!=0.    (29)
```

The two column spaces on the right show that `column(R)` contains the two
independent vectors `e_t,e_u`; the two row spaces show the same for
`column(P)`.  Thus both evaluated matrices have rank at least two.

If `det R` vanished identically as a polynomial in (25), its generic rank
would be exactly two.  Equations (29) would then force

```text
column(R)=span(e_t,e_u),                              (30)
```

so the entire colour-`s` row of `R` would vanish on a dense open set.  The
three linear forms comprising `r_s` would vanish identically, contradicting
`rank rho=3`.  Hence `det R` is not the zero polynomial.  The same argument
applies to `P`.

We may therefore choose one point of (25) at which

```text
mu_t mu_u det(R) det(P)!=0.                           (31)
```

At that point the first equation in (29) and invertibility of `R,P` give

```text
rank M(hat q_t)=1.                                    (32)
```

This is impossible.  The right side of (29) is nonzero, so `hat q_t!=0`.
Every nonzero coordinate of `q` supplies a nonzero principal `2 x 2` minor
of (27), equal to `-q_i^2`.  Therefore every nonzero `M(q)` has rank at least
two.  This contradicts (32) and proves (3).

## 4. Proof-topology consequence

Together with S2X, S2Y, and S2Z, the exact common-three-space joint-rank
frontier is now

```text
rank H=9:                                  IMPOSSIBLE (S2X);
rank H=8:                                  IMPOSSIBLE (S2Y);
rank H=7, one root block:                  IMPOSSIBLE (S2Z);
rank H=7, at least two root blocks:        IMPOSSIBLE (here);
rank H<=6:                                 OPEN;
other S2T component types / S2Q strata:   OPEN;
global Krenn--Gu conjecture:              UNRESOLVED.             (33)
```

The sharp derivative normal form (9)--(13) is load-bearing.  Merely setting
two output rows to zero checks only a coordinate tangent subcase and is not
a valid gauge for the general rank-seven branch.  Likewise, monomial support
counting alone is insufficient: some partial supports realize the two
unexceptional pure slices while missing the third.  The pointwise rank
argument uses the full coefficient identities and avoids both invalid
shortcuts.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_two_root_block_joint_cross_rank_seven_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_two_root_block_joint_cross_rank_seven_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_two_root_block_joint_cross_rank_seven_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_two_root_block_joint_cross_rank_seven_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_two_root_block_joint_cross_rank_seven_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_two_root_block_joint_cross_rank_seven_exclusion.py
```

The primary replay checks the sharp derivative rank and kernel, strict rank
growth from a third block, the rank-two-row missing-pure-colour obstruction,
the pointwise permanent matrix identity, and every nonzero support orbit of
the zero-diagonal matrix.  The independent no-import audit reconstructs the
same calculations with `Fraction` row reduction and a separately expanded
six-term permanent.  The arbitrary-tensor shared-factor lemma, dense-open
argument, and coefficient proof above establish the theorem in
characteristic zero.

## Dependencies

- [`BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_EIGHT_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_EIGHT_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_SINGLE_ROOT_BLOCK_JOINT_CROSS_RANK_SEVEN_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_SINGLE_ROOT_BLOCK_JOINT_CROSS_RANK_SEVEN_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md`](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
