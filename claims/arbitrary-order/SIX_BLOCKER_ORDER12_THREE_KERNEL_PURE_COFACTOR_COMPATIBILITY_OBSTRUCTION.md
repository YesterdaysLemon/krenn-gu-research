# Three forced pure cofactors are incompatible at order twelve

## Status

**Exact characteristic-zero compatibility obstruction.**  Continue with the
order-twelve common-row cofactor map

```text
J_H=Lambda_H(ker Lambda_H^off)
    subset span{e_0^6,e_1^6,e_2^6}.
```

The double- and triple-kernel theorem leaves one apparent extremal pattern
with three common-row kernel vectors of support two: after permuting modes
and colours, they miss colours zero, one, and two respectively.  Every pair
then forces the complementary four-mode cofactor to be a nonzero pure
`P_4` tensor in the unique colour shared by the two kernels.

Those three pure cofactors cannot coexist.  Splicing their three active
source columns into one synthetic local map would give a concise

```text
P_4 -> Delta_3,
```

contradicting the exact characteristic-zero identity
`subrank(P_4)=2`.  Consequently a core whose `J_H` meets `(C^*)^3` has at
most **two** modes admitting kernel vectors supported on at least two
colours.

The result applies before imposing the effective-block equations

```text
W_uv=a_u^T b_v+b_u^T a_v.
```

It does not classify the surviving zero-, one-, or two-mode patterns, prove
that any of them has torus-intersecting `J_H`, or settle unrestricted
`P_6 -> Delta_3`.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Root dependencies

For four-row, three-column matrices `H_0,...,H_5`, write

```text
K_uv=P_4(H_m:m notin {u,v}).                         (1)
```

The exact double-contraction theorem in
[`SIX_BLOCKER_ORDER12_KERNEL_SUPPORT_COVER_NO_TORUS_P6.md`](SIX_BLOCKER_ORDER12_KERNEL_SUPPORT_COVER_NO_TORUS_P6.md)
says that if

```text
Lambda_H(W)=sum_c d_c e_c^6,        d_0*d_1*d_2!=0, (2)
```

and `z_u in ker H_u`, `z_v in ker H_v`, then

```text
sum_c d_c z_u[c]z_v[c] e_c^4
 =W_uv(z_u,z_v) K_uv.                                 (3)
```

If the support intersection is nonempty, the scalar in (3) is nonzero and
`K_uv` is exactly the displayed weighted diagonal on that intersection.
The exact theorem
[`FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md`](FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md)
proves over `C` that such an intersection has size at most two.

The triple-contraction part of the first dependency says that the zero sets
of any three kernel vectors cover all three colours.  Thus, if three modes
admit support-at-least-two kernel vectors, each vector has support exactly
two and their missing colours are distinct.  This constant-size support
reduction is exact; no finite-field inference enters it.

## The forced pure cofactors

Normalize the three deficient modes to `0,1,2` and their supports to

```text
supp(z_0)={1,2},
supp(z_1)={0,2},
supp(z_2)={0,1}.                                      (4)
```

Their pairwise intersections are the three singleton colours.  Equation
(3) therefore forces nonzero scalars `lambda_c` such that

```text
K_12=P_4(H_0,H_3,H_4,H_5)=lambda_0 e_0^4,
K_02=P_4(H_1,H_3,H_4,H_5)=lambda_1 e_1^4,
K_01=P_4(H_2,H_3,H_4,H_5)=lambda_2 e_2^4.            (5)
```

These are three four-mode tensors sharing the tail maps `H_3,H_4,H_5`.
The remaining leading map changes from `H_0` to `H_1` to `H_2`.

## Column splicing

Let

```text
h_c=H_c[:,c] in C^4,       c=0,1,2,                  (6)
```

and form the synthetic four-by-three matrix

```text
D=[h_0 h_1 h_2].                                     (7)
```

For `t=(t_3,t_4,t_5) in {0,1,2}^3`, multilinearity of the permanent gives
the coefficient identity

```text
[c,t_3,t_4,t_5] P_4(D,H_3,H_4,H_5)
 =[c,t_3,t_4,t_5] P_4(H_c,H_3,H_4,H_5).              (8)
```

Indeed both sides use the identical leading source column `h_c` followed by
the same three tail columns.  Substituting (5) into (8) yields

```text
P_4(D,H_3,H_4,H_5)
 =lambda_0 e_0^4+lambda_1 e_1^4+lambda_2 e_2^4.      (9)
```

All three coefficients are nonzero.  Rescaling the three columns of `D`
turns (9) into `Delta_3`, an impossible restriction because
`subrank(P_4)=2`.  This contradiction excludes (4).

No rank hypothesis on `D` is missing: equality (9) itself has first-mode
flattening rank three, so it would force every local map in the alleged
restriction to have rank at least three.

## Sharpened survivor ledger

Combining the present compatibility obstruction with the root theorem gives

```text
J_H meets (C^*)^3
 => at most two modes admit a kernel vector of support at least two. (10)
```

In particular:

```text
three support-two kernels missing distinct colours: EXCLUDED;
three arbitrary support-at-least-two kernel modes: EXCLUDED;
four such modes: already excluded by the triple support cover;
two fully supported kernel modes: already excluded by subrank(P_4)=2.
```

The remaining patterns may have at most two non-coordinate kernel modes;
all other rank-two common-row kernels must be coordinate lines, while
rank-three common-row matrices have no kernel.  This is a necessary ledger,
not an existence theorem.

## Boundary

```text
extremal three support-two kernel pattern: EXCLUDED;
three forced complementary pure P_4 cofactors: INCOMPATIBLE;
torus J_H with three support-at-least-two kernel modes: NO;
torus J_H with at most two such modes: UNKNOWN;
effective two-row factorisation on surviving cores: UNKNOWN;
arbitrary ambient/source/projective realization: UNKNOWN;
global Krenn--Gu conjecture: UNRESOLVED.
```

## Replay

Replay the two exact root packages first:

```text
python claims/arbitrary-order/verify_six_blocker_order12_kernel_support_cover_no_torus_p6.py
python claims/arbitrary-order/audit_six_blocker_order12_kernel_support_cover_no_torus_p6.py
uv run --with sympy python claims/arbitrary-order/verify_fourth_order_permanent_subrank.py
python claims/arbitrary-order/audit_fourth_order_permanent_subrank.py
```

Then run:

```text
python claims/arbitrary-order/verify_six_blocker_order12_three_kernel_pure_cofactor_compatibility_obstruction.py
python claims/arbitrary-order/audit_six_blocker_order12_three_kernel_pure_cofactor_compatibility_obstruction.py
```

The primary verifier checks all 81 symbolic coefficient identities in the
column-splicing map, the six normalized support patterns, and the weighted
diagonal recombination.  The independent no-import audit uses different
integer matrices and a separate permanent routine, then reconstructs the
same support ledger.  No finite-field inference is used.
