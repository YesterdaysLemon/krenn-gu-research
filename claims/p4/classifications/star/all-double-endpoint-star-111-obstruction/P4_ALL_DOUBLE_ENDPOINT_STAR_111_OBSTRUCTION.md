# All-double-endpoint star `(1,1,1)` obstruction

## Status

**Exact characteristic-zero orientation obstruction.**  A nonzero pure
`P_4` compression cannot have a rank-one exceptional star whose three
selected relations are all kernel--kernel relations.

This removes the all-double-endpoint orientation from the sole open
all-pair `P_4` cell.  It does not classify stars with only one or two
kernel--kernel spokes, or the remaining directed support collisions.  The
Krenn--Gu conjecture remains **UNRESOLVED**.

## The common annihilator line

Center the selected star at mode zero and choose pure-factor bases
`(y_i,x_i)`, with `y_i` the pure-kernel row.  The hypothesis is

```text
y_0 y_1=y_0 y_2=y_0 y_3=0.                       (1)
```

For two nonzero degree-one forms in the squarefree Frobenius algebra,
zero product has support one or two.  Moreover the annihilator of a fixed
nonzero zero divisor is a single line.  Consequently all three leaf kernel
rows are proportional.  After row scaling there are only two cases.

If the common support is a singleton, normalize

```text
y_0=y_1=y_2=y_3=X_0.                              (2)
```

Shifting each active row by its kernel row removes its `X_0` coefficient.
The four active rows then lie in the three-space
`span(X_1,X_2,X_3)`, so their squarefree permanent is zero.  The restricted
tensor cannot be nonzero pure.

## The genuine binary support

Diagonal source scaling and a coordinate permutation normalize

```text
A=X_0+X_1,       C=X_0-X_1,
B=X_2+X_3,       D=X_2-X_3,

y_0=A,           y_1=y_2=y_3=C.                  (3)
```

Legal row shifts give the completely general active rows

```text
x_0=a_0 C+b_0 B+d_0 D,
x_i=a_i A+b_i B+d_i D       (i=1,2,3).            (4)
```

Put

```text
E_i=b_0 b_i-d_0 d_i.                              (5)
```

Three mixed coefficients of the restricted tensor are

```text
T_1001=-4E_3,       T_1010=-4E_2,
T_1100=-4E_1.                                      (6)
```

Purity forces all three to vanish.  But the all-active coefficient is the
exact syzygy

```text
T_1111=4(a_1 a_2 E_3+a_1 a_3 E_2+a_2 a_3 E_1).   (7)
```

Thus `T_1111=0`, contradicting the assumed nonzero pure tensor.  No pair-rank
specialization or denominator is used, so the obstruction includes every
support-two boundary inside this endpoint orientation.

## Replay

```text
uv run --with sympy python claims/p4/classifications/star/all-double-endpoint-star-111-obstruction/verify_p4_all_double_endpoint_star_111_obstruction.py
uv run --with sympy python claims/p4/classifications/star/all-double-endpoint-star-111-obstruction/audit_p4_all_double_endpoint_star_111_obstruction.py
```

The primary verifier reconstructs the singleton gauge, the three mixed
coefficients, and syzygy (7) over a symbolic characteristic-zero field.  The
no-import audit uses a separate subset-DP permanent after unequal source
scales and a coordinate permutation.  No finite-field inference is used.
