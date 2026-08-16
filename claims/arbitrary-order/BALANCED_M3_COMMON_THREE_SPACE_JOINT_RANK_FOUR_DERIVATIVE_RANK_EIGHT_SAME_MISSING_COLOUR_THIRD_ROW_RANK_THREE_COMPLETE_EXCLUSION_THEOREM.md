# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight same-missing-colour third-row-rank-three complete exclusion

## Status

**Exact characteristic-zero exclusion of the complete same-missing-colour
`(2,2,3)` row profile in the S2BR joint-rank-four, derivative-rank-eight
three-root cell.**  Retain the normalized, target-consistent physical `m=3`
common-three-space full-sensor hypotheses with

```text
dim U=3,                         dim K=4,             (1)
```

all three root blocks nonzero and shared-derivative rank eight.  Suppose the
first and second transposed root rows have rank two with the same missing
target colour `d`, while the third row has rank three.  Put `s,t` for the two
colours complementary to `d`.

The two missing rows first reduce the **complete** singleton correction to
one source-target line.  If its remaining root coefficient were nonzero, a
root evaluation would make the order-three permanent tensor `P_3`, of tensor
rank four, locally equivalent to a concise three-term diagonal tensor of
rank three.  Hence that coefficient is zero, and the physical empty
permanent has the exact binary table

```text
Perm(r_a,p_b,q_c)=delta_(a,b,c) T_c,
a,b in {s,t},                  c in {d,s,t}.         (2)
```

Here only the two entries `(s,s,s)` and `(t,t,t)` are nonzero.  The third-row
vector `q_d` is therefore a common zero for the two involved row planes.
Adding arbitrary multiples of `q_d` to `q_s,q_t` preserves (2).  The exact
intersecting-plane binary-frame obstruction inherited from S2BF forces every
one of those shifted binary third-row planes to be transverse to each
involved plane.  Dimension in the four-dimensional joint row space then
forces `q_d` into both involved planes, contradicting their required
transversality.  Thus the entire `(2,2,3)` cell is empty before the pair
gate.

Together with S2BU--S2BW, this closes the complete same-colour involved-row
`(2,2,q)` profile for `q=2,3`.  Mixed `(2,3,q)/(3,2,q)`, injective
`(3,3,q)`, joint-rank-three/rank-eight cells, derivative-rank-seven cells,
other components and pole strata, higher orders, and all-rank drop remain
open.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The zero rows leave one exact correction line

Use the S2BR shared-factor derivative normal form

```text
D(a,b,c)=(a tensor y-x tensor b) tensor w+C tensor c,

ker D=span((x,y,0)),
C=kappa e_d tensor e_d+C_bar,       kappa!=0,
x_d=y_d=0.                                           (3)
```

The derivative syzygy belongs to `K`.  Since the third root row has rank
three,

```text
dim pr_3 K=3.
```

The kernel of `pr_3:K->A_3` is therefore one-dimensional, so (3) gives

```text
ker(pr_3|K)=ker D.                                  (4)
```

Choose graph lifts

```text
k_c=(a_c,b_c,e_c) in K,              c=d,s,t.       (5)
```

Together with `(x,y,0)`, they form a basis of `K`.  Their derivative images

```text
U_c=D(k_c)                                           (6)
```

form a basis of `U=D(K)`, because `D|K` has exactly the kernel (4).

Let `T_c=X_c tensor Y_c tensor Z_c` be the three pure source targets.  The
complete coefficientwise target identity has unique source tensors `S_c`
such that

```text
G_N-J=S_d U_d+S_s U_s+S_t U_t.                     (7)
```

The common missing first row is `r_d=0`.  Contracting (7) in the first root
by `e_d^*` kills `G_N`.  Every first component in (5), as well as `x`, lies
in the complementary coordinate plane, while the isolated row of `C` is
`kappa e_d`.  Hence

```text
(e_d^* tensor id tensor id)U_c
  =kappa e_d tensor e_c.                            (8)
```

The same contraction of `J` is `e_d tensor e_d T_d`.  Comparing the three
independent last-root coordinates in (7)--(8) gives

```text
S_d=-kappa^(-1)T_d,                 S_s=S_t=0.      (9)
```

Thus the complete empty target, not merely its three pure source
coefficients, is

```text
G_N=J-kappa^(-1)T_d U_d.                            (10)
```

## 2. The remaining coefficient vanishes by tensor rank

Write the `T_d` root coefficient in (10) as

```text
F_d=e_d tensor e_d tensor e_d-kappa^(-1)U_d.       (11)
```

Suppose `F_d` were nonzero.  The three root trilinear polynomials

```text
F_d(alpha,beta,gamma),
alpha_s beta_s gamma_s,
alpha_t beta_t gamma_t                               (12)
```

are nonzero.  Their product is nonzero in the polynomial ring over the
infinite characteristic-zero field, so there are root covectors
`alpha,beta,gamma` on which all three values are nonzero.  Evaluating (10)
there gives

```text
G_N(alpha,beta,gamma)
 =lambda_d T_d+lambda_s T_s+lambda_t T_t,
lambda_d lambda_s lambda_t!=0.                      (13)
```

On the other hand, put

```text
u=rho(alpha),             v=pi(beta),
z=theta(gamma).
```

The left side of (13) is the six-term polarized source permanent
`Perm(u,v,z)`.  If `L_X,L_Y,L_Z` send the three supplier basis vectors to
the `X,Y,Z` components of `u,v,z`, respectively, then

```text
Perm(u,v,z)=(L_X tensor L_Y tensor L_Z)P_3.         (14)
```

Every one-mode flattening of (13) has rank three.  Therefore all three maps
in (14) have rank three and are invertible.  They preserve tensor rank.  But

```text
tensor-rank(P_3)=4,
tensor-rank(lambda_d T_d+lambda_s T_s+lambda_t T_t)=3. (15)
```

The first equality is the exact order-three permanent-rank theorem used in
S2R; the second follows from the displayed three-term decomposition and any
rank-three flattening.  This contradiction proves

```text
F_d=0,                    U_d=kappa e_d tensor e_d tensor e_d. (16)
```

Consequently

```text
G_N=e_s tensor e_s tensor e_s T_s
   +e_t tensor e_t tensor e_t T_t.                  (17)
```

## 3. The exact binary table and its shifted planes

Let

```text
R=span(r_s,r_t),             P=span(p_s,p_t),
Q_0=span(q_s,q_t),           Q=span(q_d,q_s,q_t).   (18)
```

The row-rank hypotheses give dimensions `2,2,2,3`, respectively.  The joint
row space

```text
V=span(R,P,Q)                                      (19)
```

is the injective image of `K^*` under `H^*`, so `dim V=4`.  Equation (17)
is exactly the table (2).  In particular,

```text
Perm(R,P,q_d)=0.                                    (20)
```

We use the following direct corollary of S2BF's exact
intersecting-middle-plane binary obstruction.

### Lemma 1 (binary-frame planes in a four-space are pairwise transverse)

If three two-planes `A,B,C` in a four-space carry an exact binary diagonal
table with two fully transverse nonzero target tensors, then

```text
A intersect B=A intersect C=B intersect C=0.        (21)
```

Indeed, if (say) `A intersect C` were nonzero, a three-space `S` could be
chosen to contain `A+C`.  The dimension formula makes the middle plane `B`
meet `S` nontrivially.  S2BF's obstruction excludes precisely that
configuration.  The other two intersections follow by symmetry of the
polarized permanent.  This argument also covers `A=C` after enlarging their
sum to a three-space.

Applying Lemma 1 to `(R,P,Q_0)` gives

```text
R intersect P=R intersect Q_0=P intersect Q_0=0.   (22)
```

For arbitrary scalars `lambda_s,lambda_t`, put

```text
Q_lambda=span(q_s+lambda_s q_d,
              q_t+lambda_t q_d).                   (23)
```

The two displayed vectors are independent modulo `q_d`.  Equation (20)
shows that replacing `q_s,q_t` by them changes no entry of (2).  Lemma 1
therefore gives, for **every** `lambda`,

```text
R intersect Q_lambda=P intersect Q_lambda=0.        (24)
```

## 4. Dimension forces the common zero into both involved planes

Since `dim R=2`, `dim Q=3`, and `dim V=4`, the intersection `R intersect Q`
is nonzero.  Equation (22) makes it exactly a line.  Choose a nonzero vector
on that line and write uniquely

```text
ell=a q_s+b q_t+c q_d.                              (25)
```

The coefficient `c` is nonzero, since otherwise `ell` would belong to
`R intersect Q_0`.  If `(a,b)!=(0,0)`, choose `lambda_s,lambda_t` with

```text
a lambda_s+b lambda_t=c.                            (26)
```

Then

```text
ell=a(q_s+lambda_s q_d)+b(q_t+lambda_t q_d)
     in R intersect Q_lambda,                       (27)
```

contradicting (24).  Hence `a=b=0`, and (25) proves

```text
q_d in R.                                           (28)
```

The identical dimension argument with `P` in place of `R` gives

```text
q_d in P.                                           (29)
```

But `q_d` is nonzero because the third row is injective.  Equations
(28)--(29) contradict `R intersect P=0` in (22).  This excludes the complete
same-colour `(2,2,3)` row profile.

## 5. Proof-topology consequence

Combining this theorem with S2BU--S2BW gives

```text
same-colour involved rows (2,2):
  third-row rank two, support one:   graph cell IMPOSSIBLE (S2BU/S2BV);
  third-row rank two, support two:   IMPOSSIBLE (S2BW);
  third-row rank three:              IMPOSSIBLE (this theorem);

complete same-colour (2,2,q) profile:               CLOSED.          (30)
```

No pair-deck regularity, numerical specialization, finite-field promotion,
generic-point promotion, or unproved plane-incidence case split enters the
new exclusion.  The only inherited case exhaustion is the exact
characteristic-zero binary-frame obstruction of S2BF.

## 6. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_rank_three_complete_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_rank_three_complete_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_rank_three_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_rank_three_complete_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_rank_three_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_rank_three_complete_exclusion.py
```

The primary replay checks the exact missing-row correction system, the
order-three permanent and diagonal flattenings, the four-term permanent
decomposition, the binary table under arbitrary kernel-row shifts, and the
four-space shift trap with SymPy.  The independent no-import audit reverses
tensor indexing and reconstructs those identities, ranks, and every rational
support branch of the shift trap with standard-library `Fraction`
arithmetic.  The nonzero-polynomial evaluation, inherited binary-frame
obstruction, and arbitrary-subspace dimension argument above are the proof.

## Dependencies

- [Rank-four/rank-eight target-kernel atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_TARGET_KERNEL_ATLAS_AND_DISTINCT_MISSING_COLOUR_EXCLUSION_THEOREM.md)
- [Support-two rank-two-third-row exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_SUPPORT_TWO_COMPLETE_EXCLUSION_THEOREM.md)
- [Intersecting-middle-plane binary obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_PROJECTIVE_PENCIL_LOCALIZATION_THEOREM.md#2-a-binary-diagonal-frame-cannot-have-an-arbitrary-middle-intersection)
- [Order-three permanent-rank obstruction](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)

## Scope boundary

```text
same-colour (2,2,3) rank-four/rank-eight cell:       IMPOSSIBLE;
complete same-colour (2,2,q) involved-row profile:  CLOSED;
mixed / injective involved-row profiles:            OPEN;
lower-rank target cells / other components and poles: OPEN;
higher balanced orders / all-balanced rank-drop:    OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.       (31)
```
