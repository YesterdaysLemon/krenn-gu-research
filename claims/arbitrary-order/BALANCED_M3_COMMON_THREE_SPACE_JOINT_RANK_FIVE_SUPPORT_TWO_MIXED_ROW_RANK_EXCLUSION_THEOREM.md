# Balanced `m=3` common-three-space joint-rank-five support-two mixed-row-rank exclusion

## Status

**Exact characteristic-zero exclusion of the transverse joint-rank-five
support-two `(3,2)` and `(2,3)` involved-row profiles.**  Let `U` be the total
singleton span of a normalized, target-consistent physical `m=3` common
shore.  Assume

```text
dim U=3,                         rank H=5,             (1)
```

and retain the transverse two-root branch of S2AG with a rank-two third row
whose one-dimensional kernel has support exactly two.  If the two involved
root-row ranks are `3` and `2` in either order, then the physical full-sensor
conditions are inconsistent.

The proof does not use the S2AD beta-zero atlas, a monomial or separable
root--root block, genericity, full singleton independence, or a finite-field
search.  The rank-two involved shore makes the relation three-plane a graph
whose image misses the third target colour.  The full target equation then
pins every singleton correction to the pure line `T_2`.  But the two
supported third-root rows are proportional, while their colour-one target
slices differ by the independent line `T_1`.  This is impossible.

This theorem does **not** exclude the support-two `(3,3)` profile, support
one, a three-root Hilbert--Burch boundary, joint rank at most four, another
S2T/S2Q component, the all-rank-drop branch, or a higher order.  Global
Krenn--Gu remains **UNRESOLVED**.

The support-two `(3,3)` successor closes that final involved-row profile
without changing this theorem's proof or scope.

## 1. The mixed profile is a rank-two graph

Use the transverse notation of S2AG and S2AI.  After permuting the two
involved roots,

```text
B_23=B!=0,                  B_13=C!=0,       B_12=0,

D_(B,C)(a,b,c)=a tensor B+C tensor b,
rank D_(B,C)=6.                                      (2)
```

There are a three-plane `P` and a two-plane `N_3` such that

```text
K=P direct-sum N_3,
P subset A_1 direct-sum A_2,
U=D_(B,C)(P).                                        (3)
```

Write the transposed root-row maps as

```text
rho:A_1^*->W^*,        pi:A_2^*->W^*,
theta:A_3^*->W^*,      W=X direct-sum Y direct-sum Z. (4)
```

Orient the mixed profile as

```text
rank rho=3,                 rank pi=2,
rank theta=2,               ker theta=span(eta),
|support eta|=2.                                      (5)
```

The projection of `P` to `A_1` is an isomorphism, while its projection to
`A_2` has rank two.  Hence

```text
P={(a,L a):a in A_1},                  rank L=2.       (6)
```

Let `delta` span `ker pi`.  Contract the full target equation in the second
root by `delta`.  The all-cross permanent vanishes because `pi(delta)=0`,
and the singleton image contracts into

```text
A_1 tensor span((delta tensor id)(B)).
```

For every colour in the coordinate support of `delta`, the corresponding
nonzero diagonal target coefficient therefore forces the fixed second factor
`(delta tensor id)(B)` onto that colour's coordinate line.  Two different
colours cannot use the same nonzero line, while a zero contraction cannot
absorb any target coefficient.  Hence `delta` has support one.  For some `d`
and some `kappa!=0`,

```text
ker pi=span(e_d^*),                 image L=e_d^perp. (7)
(e_d^* tensor id)(B)=kappa e_d.
```

Relabel the two supported colours and, if necessary, exchange their names so
that the exact support-two contraction of S2AG is

```text
support eta={0,1},
b_eta=(id tensor eta)(B)=beta e_0,
c_eta=(id tensor eta)(C)=chi e_1,
beta chi!=0.                                           (8)
```

Contracting (3) by `eta` gives

```text
eta(U)={beta a tensor e_0+chi e_1 tensor L a:a in A_1}. (9)
```

The colour-one target coefficient is nonzero, so `e_1 tensor e_1` belongs
to (9), up to a nonzero scalar.  Its preimage must be a nonzero multiple of
`e_1`: projection of (9) in its first factor to
`(A_1/span(e_1)) tensor A_2` kills every other possibility.  Therefore
there is a nonzero scalar `nu` such that

```text
beta e_0+chi L e_1=nu e_1,

L e_1=-(beta/chi)e_0+(nu/chi)e_1.                    (10)
```

Both displayed coordinates in (10) are nonzero.  Since the image of `L` is
the coordinate plane in (7), neither `d=0` nor `d=1` is possible.  Thus

```text
d=2,                 image L=span(e_0,e_1),
p_2=pi(e_2^*)=0.                                     (11)
```

No monomiality, separability, rank-one form, or restriction beyond the
inherited contractions (7)--(8) has been imposed on `B` or `C`.

## 2. The zero row pins every correction to `T_2`

Use the standard graph basis of the singleton plane,

```text
u_i=D_(B,C)(e_i,L e_i)=e_i tensor B+C tensor L e_i,
i=0,1,2.                                             (12)
```

Write the full target equation coefficientwise as

```text
G_N-J=S_0 u_0+S_1 u_1+S_2 u_2,                      (13)
```

where `S_i` are tensors in the three nonroot target factors.  Let

```text
T_i=X_i tensor Y_i tensor Z_i.                       (14)
```

Because every `L e_i` has zero colour-two coordinate, the root-2 row `b=2`
of (12) is

```text
u_i(a,2,c)=delta_(a,i) B_(2,c).                      (15)
```

The all-cross permanent vanishes on this row because `p_2=0`.  Equations
(7), (13), and (15), compared at all rows `(a,2,c)`, give

```text
-delta_(a,2)delta_(c,2)T_2
  =delta_(c,2) kappa S_a.                            (16)
```

The rows `(0,2,2)`, `(1,2,2)`, and `(2,2,2)` give the exact identities

```text
S_0=S_1=0,                    S_2=-kappa^(-1) T_2.   (17)
```

Consequently **every** correction in (13), on every remaining root row, is
a scalar multiple of `T_2`.  The entries not fixed by (7)--(10) remain
arbitrary.

## 3. Proportional quotient rows cannot carry two target lines

Write

```text
eta=eta_0 e_0^*+eta_1 e_1^*,       eta_0 eta_1!=0,
q_c=theta(e_c^*).                                      (18)
```

Since `theta(eta)=0`,

```text
eta_0 q_0+eta_1 q_1=0,
q_1=gamma q_0,                    gamma=-eta_0/eta_1!=0. (19)
```

For `u,v,q in W^*`, write

```text
M_(u,v)(q)=per(u,v,q) in X^* tensor Y^* tensor Z^*. (20)
```

Compare (13) in the fixed first-two-root row pair `(1,1)`.  Equations
(17) and the absence of a target at `(1,1,0)` give a scalar `lambda_0` with

```text
M_(r_1,p_1)(q_0)=lambda_0 T_2.                       (21)
```

At `(1,1,1)`, the physical target contributes `T_1`, while the singleton
correction is still on `T_2`.  Hence for another scalar `lambda_1`,

```text
M_(r_1,p_1)(q_1)=T_1+lambda_1 T_2.                  (22)
```

But linearity and (19) make the left side of (22) equal to `gamma` times
the left side of (21), which belongs to `span(T_2)`.  The right side of
(22) does not: `T_1,T_2` are distinct target-basis tensors.  This
contradiction excludes `(rank rho,rank pi)=(3,2)`.  Exchanging the two
involved roots excludes `(2,3)` as well.  Therefore

```text
support-two rank-five involved-row profiles (3,2)/(2,3): IMPOSSIBLE.   (23)
```

### Why this does not decide `(3,3)`

The rank-two shore is load-bearing.  With an invertible graph map there is
no zero row like `p_2=0`, so (17) does not pin all corrections to `T_2`.
At the isolated pair of slices used above, the formal table

```text
q_1=-q_0,
M(q_0)=M(q_1)=0,
R_0=0,                         R_1=-T_1              (24)
```

satisfies `M(q_c)-delta_(c,1)T_1=R_c`.  This is an exact local sharpness
control, not a physical Krenn--Gu witness; it shows only that the proportional-
row comparison cannot be carried into `(3,3)` without new control of the
singleton corrections.

## 4. Proof-topology consequence

The transverse rank-five support-two branch is now

```text
involved rows (2,2):                                  IMPOSSIBLE (S2AI);
involved rows (3,2)/(2,3):                            IMPOSSIBLE (this theorem);
involved rows (3,3):                                  IMPOSSIBLE (successor);

third-row kernel support one:                         OPEN;
three-root Hilbert--Burch coordinate atlases:         OPEN;
joint rank at most four / other physical branches:    OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.       (25)
```

The successor controls those correction tensors through the binary diagonal
plane and closes the `(3,3)` graph profile.  The next transverse obligations
are support one and the three Hilbert--Burch coordinate atlases.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_two_mixed_row_rank_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_two_mixed_row_rank_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_two_mixed_row_rank_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_two_mixed_row_rank_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_support_two_mixed_row_rank_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_support_two_mixed_row_rank_exclusion.py
```

The primary verifier checks the contracted graph identity, the missing-colour
decision, the complete symbolic zero-row target table with arbitrary
uncontracted block entries, the target-line contradiction, and the `(3,3)`
local sharpness control.  The independent audit imports no repository module
and no third-party package; it rebuilds the graph and sparse target table with
standard-library `Fraction` arithmetic and separately checks that no scalar
multiple of `T_2` can absorb `T_1`.
