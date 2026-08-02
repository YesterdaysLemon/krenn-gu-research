# A projectively constant row obstructs the arbitrary six-blocker cofactor

## Status

**Exact characteristic-zero obstruction for arbitrary cofactor blocks.**  Let
`H_0,...,H_5` be the four-row, three-column matrices in the six-blocker
cofactor map

```text
Lambda_H(W)=sum_(u<v) W_uv tensor
            P_4(H_m:m notin {u,v}).                     (1)
```

The blocks `W_uv` in (1) may be arbitrary three-by-three bilinear forms.  If
one common row family of the six matrices `H_u` is projectively constant,
then `Lambda_H(W)` cannot be a diagonal sextic with three nonzero diagonal
coefficients.  Equivalently,

```text
J_H=Lambda_H(ker Lambda_H^off)
```

does not meet `(C^*)^3` on this stratum.

Combined with the exact arbitrary-order four-root/six-blocker cofactor
transfer, this proves that every one of the four root-row families in such a
global cell must span at least a two-dimensional covector space across the
six blockers.  This is a necessary condition for that cell, not a closure of
the remaining projectively varying cores.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## Arbitrary-block equal-input factor

Fix a common source-row index `i`.  Suppose there are scalars `kappa_u` and a
fixed nonzero target covector `ell` such that

```text
H_u[i,-]=kappa_u ell,          u=0,...,5.               (2)
```

No nonvanishing hypothesis on the individual `kappa_u` is imposed.  If the
row family is identically zero, every complementary permanent in (1)
vanishes and the conclusion is immediate, so (2) includes every nonzero
row family of span at most one.

Evaluate all six output modes at the same target vector `t`.  Write

```text
E_W(t)=Lambda_H(W)(t,t,t,t,t,t).
```

The cofactor expansion (1) gives

```text
E_W(t)=sum_(u<v) W_uv(t,t)
        per([H_m[-,t]]_(m notin {u,v})).                (3)
```

For a fixed unused pair `{u,v}`, every monomial of the four-by-four
permanent in (3) uses row `i` exactly once.  If it uses that row in column
`m`, its corresponding factor is

```text
H_m[i,-](t)=kappa_m ell(t).                             (4)
```

Thus each of the `4!=24` permanent assignments in each of the 15 edge
summands contains `ell(t)` before any terms are collected.  The arbitrary
quadratic multiplier `W_uv(t,t)` does not change this divisibility.  Hence

```text
ell(t) divides E_W(t)       for every family W.         (5)
```

This is strictly an arbitrary-cofactor statement: neither the equations
`Lambda_H^off(W)=0` nor an effective representation
`W_uv=a_u^T b_v+b_u^T a_v` is used.

## A torus diagonal sextic has no linear factor

If `Lambda_H(W)` represented a coefficient-torus point, then for nonzero
`d_0,d_1,d_2` its equal-input polynomial would be

```text
D(t)=d_0 t_0^6+d_1 t_1^6+d_2 t_2^6.                   (6)
```

Over `C`, the polynomial (6) has no linear factor.  Indeed, suppose the line

```text
alpha t_0+beta t_1+gamma t_2=0                        (7)
```

were a component.  When `gamma!=0`, substitute
`t_2=-(alpha t_0+beta t_1)/gamma` and clear `gamma^6`.
The coefficients of `t_0^5 t_1` and `t_0 t_1^5` are respectively

```text
6 d_2 alpha^5 beta,       6 d_2 alpha beta^5.          (8)
```

Characteristic zero and `d_2!=0` force `alpha beta=0`.  If `alpha=0`, the
nonzero coefficient `gamma^6 d_0` of `t_0^6` remains; if `beta=0`, the
nonzero coefficient `gamma^6 d_1` of `t_1^6` remains.  If `gamma=0`, the line
involves only `t_0,t_1`, so the free term `d_2 t_2^6` remains.  Every case is
a contradiction.

Equations (5) and (6) are therefore incompatible.  Consequently

```text
J_H intersects (C^*)^3: NO
whenever one common row family has span at most one.    (9)
```

## Arbitrary-order four-root/six-blocker consequence

The exact matching bijection in
[`FOUR_ROOT_SIX_BLOCKER_ARBITRARY_ORDER_KERNEL_SUPPORT_OBSTRUCTION.md`](FOUR_ROOT_SIX_BLOCKER_ARBITRARY_ORDER_KERNEL_SUPPORT_OBSTRUCTION.md)
starts with four fully supported pairwise-zero roots whose total blocker
union is exactly six.  At arbitrary even ambient order it constructs actual
residual blocks `W_uv` and forces

```text
Lambda_H(W)=sum_(c=0)^2 d_c e_c^6,
d_0*d_1*d_2!=0.                                        (10)
```

Apply (9) to those arbitrary residual blocks.  For every one of the four
roots `r_i`, its incident covectors at the six blockers must satisfy

```text
dim span{H_u[i,-]:u in B} >= 2.                        (11)
```

Thus the projectively constant row stratum is excluded in the
arbitrary-order four-root/exactly-six-blocker cell.  No order-twelve
truncation and no effective-block factorization enter this transfer.

## Relation to the direct `P_6` obstruction

[`P6_PROJECTIVELY_CONSTANT_SOURCE_ROW_OBSTRUCTION.md`](P6_PROJECTIVELY_CONSTANT_SOURCE_ROW_OBSTRUCTION.md)
proves the analogous common-factor obstruction for a direct concise
restriction of `P_6`.  The present theorem is stronger in the direction
needed here: it proves the factor termwise for the cofactor sum (1), with
completely arbitrary `W_uv`, and then combines it with the exact global
matching transfer.

## Boundary

```text
projectively constant row for arbitrary Lambda_H blocks: EXCLUDED;
torus J_H on that stratum: NO;
arbitrary-order four-root/exactly-six-blocker constant row: EXCLUDED;
all four row families must have span at least two: PROVED;
projectively varying six-blocker cores: UNKNOWN;
at-most-two non-coordinate-kernel survivor strata: UNKNOWN;
effective factorization on surviving cores: UNKNOWN;
full arbitrary-order local-to-global reduction: UNKNOWN;
global Krenn--Gu conjecture: UNRESOLVED.
```

## Replay

Replay the direct and transfer dependencies first:

```text
uv run --with sympy python verify_p6_projectively_constant_source_row_obstruction.py
python audit_p6_projectively_constant_source_row_obstruction.py

python verify_four_root_six_blocker_arbitrary_order_kernel_support_obstruction.py
python audit_four_root_six_blocker_arbitrary_order_kernel_support_obstruction.py
```

Then run:

```text
uv run --with sympy python verify_six_blocker_arbitrary_cofactor_projectively_constant_row_obstruction.py
python audit_six_blocker_arbitrary_cofactor_projectively_constant_row_obstruction.py
```

The primary verifier expands all 15 complementary cofactors and all 360
permanent assignments over a characteristic-zero symbolic ring, checks the
common factor before specializing the arbitrary block multipliers, and
checks the diagonal-line coefficient argument.  The independent no-import
audit uses a separate exact integer polynomial implementation with genuinely
quadratic block evaluations and separately audits the line case split.  No
finite-field inference is used.
