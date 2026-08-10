# Component twenty-two: the `h2=0` terminal minor reduces to `6 x 6`

## Status

**Exact characteristic-zero structural reduction.**  On component twenty-two's
finite `D23` slice

```text
H=2*A*h1+1=0,  h2=0,
```

the selected eight-by-eight mixed minor on rows

```text
(1,2,3,5,6,7,10,12)
```

factors exactly as

```text
-f6*f8*Delta6,                                      (1)
```

where `Delta6` is the six-by-six minor on rows

```text
(2,3,6,7,10,12)
```

and extension columns

```text
(0,1,2,4,5,7).                                     (2)
```

Consequently, on the retained open `f6*f8!=0`, rank drop forces
`Delta6=0`.  This replaces the previously stalled terminal `8 x 8`
calculation by a strictly smaller sparse determinant.

This is a reduction, not a closure theorem.  In particular it does not prove
that `Delta6` is nonzero on the contextual `W=P=0` residue, does not promote
that contextual residue to a replayable theorem, and does not close any of
the other `H=0` divisors.  Those loci and the global Krenn--Gu conjecture
remain **UNRESOLVED**.  No finite field is used.

## Sparse pivot identity

Write

```text
f6=(D-1)*rho+D+1,
f8=(A*D+A+R*D)*rho+A*D-A+R*D.
```

After `h1=-1/(2*A),h2=0`, mixed rows 1 and 5 have support only in extension
columns 3 and 6.  In those columns they are

```text
row 1: (f8+2*A*f6, f8),
row 5: (-f8/(2*A), -f8/(2*A)).                    (3)
```

Their two-by-two determinant is `-f6*f8`.  Generalized Laplace expansion
along these two rows has positive shuffle sign for columns `(3,6)`, and its
complement is exactly (2).  Equations (1)--(3) follow without expanding an
eight-by-eight determinant.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-h2-zero-six-by-six-terminal/verify_p5_h22_unequal_complement_common_kernel_component_d23_h2_zero_six_by_six_terminal_reduction.py
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-h2-zero-six-by-six-terminal/audit_p5_h22_unequal_complement_common_kernel_component_d23_h2_zero_six_by_six_terminal_reduction.py
```

The primary reads the committed component matrix.  The audit rebuilds it from
the low-level permanent model without importing the primary.  Both verify the
support, four pivot entries, pivot determinant, complementary row and column
sets, and Laplace sign exactly over characteristic zero.
