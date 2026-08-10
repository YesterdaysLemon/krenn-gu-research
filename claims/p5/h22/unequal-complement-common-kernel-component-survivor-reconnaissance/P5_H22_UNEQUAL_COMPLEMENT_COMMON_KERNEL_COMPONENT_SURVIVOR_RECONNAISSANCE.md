# Exact weighted-`H22` survivor reconnaissance on component twenty-two

## Status

**Exact characteristic-zero partial result; generic fibre still UNKNOWN.**
Two rational points of the finite `D01` binary-incidence scheme over the
unequal-complement common-kernel component are exhibited below.  Both have
nonzero pure diagonals, so they are genuine binary survivors rather than
solutions created by a diagonal-zero saturation failure.  Nevertheless all
four one-marked ternary maps have rank four at each point.  Hence neither
point lifts to a weighted-`H22` restriction and neither is a counterexample.

This package does not classify the complete survivor scheme, prove that the
generic weighted-`H22` fibre is empty, or settle any special/projective fibre.
The Krenn--Gu conjecture remains **UNRESOLVED**.

## Model

Use the component-twenty-two basis from
[`P4_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT.md`](../../../p4/classifications/P4_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT.md)
on its first sheet.  At `(A,R,D)=(1,1,2)`, let `alpha_i,beta_i` be the four
ordered basis pairs and replace

```text
beta_i by beta_i+h_i alpha_i.
```

For an extension vector

```text
z=(x_0,x_1,x_2,x_3;y_0,y_1,y_2,y_3)
```

and finite weight `rho`, the `D01` projected rows are

```text
alpha'_i=(rho alpha_i0+alpha_i1, alpha_i2, alpha_i3, x_i),
beta'_i =(rho beta_i0 +beta_i1,  beta_i2,  beta_i3,  y_i).       (1)
```

The first exact point is

```text
rho=-2,
h=(1,0,0,-1),
z=(8/5,4/5,2/25,-18/25;3/25,6/25,6/25,1).                      (2)
```

All fourteen mixed coefficients of the projected binary tensor vanish, while
the two pure diagonals are

```text
(-192/25,-18/25).                                               (3)
```

The second point is

```text
rho=3,
h=(0,0,0,1),
z=(-3,5,6,1;-15/2,-2,-2,1),                                    (4)
```

with pure diagonals

```text
(72,-24).                                                       (5)
```

At both points the four lifted two-planes in five-space have all-pair profile
`(4,4,4,4,4,4)`, while their `D01` projections have profile
`(4,4,4,3,3,3)`.  Thus neither point is discarded by a lower-pair accident.

## Exact ternary obstruction

For each marked mode `q=0,1,2,3`, form the `8 x 4` one-marked map of the
projected four-dimensional rows.  On rows `0137`, its determinant is,
respectively, at (2),

```text
(27648/3125, -31104/3125, -31104/3125, -27648/15625),           (6)
```

and at (4),

```text
(73728,15552,15552,110592).                                    (7)
```

Every entry in (6)--(7) is nonzero.  Consequently every one-marked map has
rank four, whereas an `H22` lift would require the ternary image rank to be at
most three.  These binary survivors are therefore exact false positives.

## Replay and boundary

```text
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-survivor-reconnaissance/verify_p5_h22_unequal_complement_common_kernel_component_survivor_reconnaissance.py
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-survivor-reconnaissance/audit_p5_h22_unequal_complement_common_kernel_component_survivor_reconnaissance.py
```

Both scripts use rational arithmetic.  The audit independently rebuilds the
permanent, pair products, contractions, and one-marked matrices without
importing the primary verifier.  No finite-field computation is used.
