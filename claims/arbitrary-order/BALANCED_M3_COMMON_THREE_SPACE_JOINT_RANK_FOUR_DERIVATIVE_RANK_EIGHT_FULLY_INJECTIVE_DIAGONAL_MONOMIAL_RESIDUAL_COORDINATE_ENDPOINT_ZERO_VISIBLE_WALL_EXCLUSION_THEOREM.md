# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight fully-injective diagonal-monomial coordinate-endpoint zero-visible-wall exclusion

## Status

**Exact characteristic-zero exclusion of the complete zero-visible wall at
the surviving diagonal monomial coordinate endpoints.**  Retain the
normalized physical full-sensor hypotheses and notation of S2CF:

```text
dim U=3,                 K=image H=D^(-1)(U),       dim K=4,
rank rho=rank pi=rank theta=3,

D(a,b,c)=(a tensor y-x tensor b) tensor e_0
          +lambda e_2 tensor e_2 tensor c,
lambda!=0,

ker D=span((x,y,0)) subset K,
x not proportional e_2,       y not proportional e_2.       (1)
```

For `alpha in x^perp`, `beta in y^perp`, and
`Q=span(q_0,q_1,q_2)`, S2CF gives the corrected cube

```text
per(r_alpha,p_beta,q_k)
 =alpha_k beta_k T_k+lambda alpha_2 beta_2 S_k.      (2)
```

Suppose neither `T_0` nor `T_1` is visible in a nonexceptional cell of
this cube, in the exact sense of S2CF's visibility census.  Then no physical
point exists.

The proof is analytic.  The simultaneous visibility failures force the two
shared factors onto the crossed coordinate pair `(e_0,e_1)` or `(e_1,e_0)`.
In either orientation, (2) makes a two-dimensional involved-row plane a
radical shore of one nonzero row inside the physical third-row three-space.
The full-sensor alternating-tensor interface and S2CG's radical-line theorem
allow radical dimension at most one.

This theorem does not exclude either one-visible wall or the two-visible
open cell.  It does not close a diagonal coordinate endpoint.  Every other
nonmonomial residual, lower-rank target cell, pair gate, component, pole
stratum, higher order, and all-rank-drop branch remains open.  Global
Krenn--Gu remains **UNRESOLVED**.

## 1. The physical third-row space is an alternating three-space

Put

```text
N=ker D=span((x,y,0)),               L=N^perp.       (3)
```

Since `N subset K`, one has `K^perp subset L`.  Rank and dimension give

```text
dim L=8,              dim K^perp=5,
V=H^T(L),             dim V=3.                       (4)
```

Every third-root covector `(0,0,gamma)` belongs to `L`, so

```text
Q=image theta subset V.                              (5)
```

Third-row injectivity makes `dim Q=3`; hence `Q=V`.  The quotient maps

```text
H_bar:W -> K/N,                 D_bar:K/N -> U
```

are respectively onto and invertible.  As in S2CG, the separated determinant
of the three singleton columns of `D_bar H_bar` is a nonzero basis factor
times

```text
Alt(v_0,v_1,v_2)
 =sum_(sigma in S_3) sign(sigma)
   (v_(sigma(0)))_X tensor
   (v_(sigma(1)))_Y tensor
   (v_(sigma(2)))_Z.                                 (6)
```

Full-sensor rank therefore proves

```text
Alt(Q)!=0.                                           (7)
```

S2CG Corollary 2 applies to every nonzero `u in Q` and gives

```text
Rad_Q(u)={v in Q:per(u,v,Q)=0},
dim Rad_Q(u)<=1.                                     (8)
```

Only this proved general three-space consequence of S2CG is imported; the
canonical-binomial residual excluded there is not assumed here.

## 2. Exact classification of the zero-visible wall

S2CF proves

```text
T_0 visible outside the corrected cell iff
  x not proportional e_0,
  y not proportional e_0,
  (x_1,y_1)!=(0,0);

T_1 visible outside the corrected cell iff
  x not proportional e_1,
  y not proportional e_1,
  (x_0,y_0)!=(0,0).                                  (9)
```

Thus invisibility of `T_0` is the disjunction

```text
x proportional e_0,       or y proportional e_0,
or x_1=y_1=0,                                      (10)
```

and invisibility of `T_1` is

```text
x proportional e_1,       or y proportional e_1,
or x_0=y_0=0.                                      (11)
```

Assume first `x proportional e_0`.  Since `x` is not proportional to `e_1`
and `x_0!=0`, the first and third alternatives of (11) fail.  Therefore
`y proportional e_1`.  The same argument with the roots exchanged shows
that `y proportional e_0` forces `x proportional e_1`.

It remains to consider the last alternative of (10), with neither shared
factor proportional to `e_0`.  Then `x_1=y_1=0`, so neither factor is
proportional to `e_1`.  Equation (11) forces `x_0=y_0=0`, making both factors
proportional to `e_2`.  This contradicts (1).  Hence, up to nonzero scalars,

```text
(x,y)=(e_0,e_1)          or          (e_1,e_0).      (12)
```

No generic-point argument enters this Boolean support classification.

## 3. The crossed coordinate pairs create a forbidden radical shore

Normalize the first orientation in (12) as

```text
x=e_0,                         y=e_1.                (13)
```

Take `alpha=e_1 in x^perp`.  Every `beta in y^perp` satisfies `beta_1=0`,
while

```text
alpha_k beta_k=0       for k=0,1,2,
alpha_2 beta_2=0.                                    (14)
```

Equation (2) therefore gives

```text
per(r_alpha,p_beta,q_k)=0
             for every beta in y^perp and k=0,1,2.  (15)
```

The defining root covectors for `r_alpha` and `p_beta` annihilate `N`, so
all these rows lie in `Q=H^T(L)`.  Injectivity of `rho` makes
`r_alpha!=0`, while injectivity of `pi` gives

```text
dim p(y^perp)=2.                                     (16)
```

Equations (15)--(16) say

```text
p(y^perp) subset Rad_Q(r_alpha),
dim Rad_Q(r_alpha)>=2,                               (17)
```

contradicting (8).

For `(x,y)=(e_1,e_0)`, take `alpha=e_0`; every `beta in y^perp` has
`beta_0=0`, and the same calculation proves (15)--(17).  Thus both crossed
coordinate orientations, and hence the entire zero-visible wall, are empty.

## 4. Proof-topology consequence

The exact diagonal endpoint visibility split is now

```text
zero-visible wall:                                  IMPOSSIBLE;
one-visible walls:                                  OPEN;
two-visible open cell:                              OPEN;
complete diagonal coordinate endpoint:              OPEN;
other nonmonomial rank-eight residuals:              OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.       (18)
```

The one-visible same-coordinate quotient controls in S2CF have only a
one-dimensional radical, which is compatible with (8).  Their complete
retained faces and tangent-coset flattening remain load-bearing.

## 5. Focused replay

From repository root:

```bash
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_zero_visible_wall_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_zero_visible_wall_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_zero_visible_wall_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_zero_visible_wall_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_zero_visible_wall_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_fully_injective_diagonal_monomial_residual_coordinate_endpoint_zero_visible_wall_exclusion.py
```

The primary replay checks the complete support-mask classification, both
crossed-coordinate cube contractions, the two-dimensional radical shore, and
the alternating/dimension interface with SymPy.  The independent no-import
audit reverses traversal, uses standard-library `Fraction` arithmetic, and
separately reconstructs the support masks and all twelve cube coefficients
in both orientations.  S2CG's written proof owns the radical-line theorem.

## Dependencies

- [Diagonal coordinate-endpoint full-target reduction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_DIAGONAL_MONOMIAL_RESIDUAL_COORDINATE_ENDPOINT_FULL_TARGET_REDUCTION_THEOREM.md)
- [Canonical-binomial residual exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_FULLY_INJECTIVE_CANONICAL_BINOMIAL_RESIDUAL_EXCLUSION_THEOREM.md)

## Scope boundary

```text
characteristic-zero zero-visible-wall exclusion:     PROVED;
full-sensor alternating-three-space interface:       PROVED;
support-wall coverage:                               PROVED;
radical-shore contradiction:                         PROVED;
one-visible and two-visible cells:                    OPEN;
complete diagonal endpoint exclusion:                OPEN;
other nonmonomial residuals and wider branches:       OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.       (19)
```
