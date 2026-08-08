# Binary polarity kills weighted `H22` on the twelfth component

## Status

**Exact characteristic-zero generic-component theorem.**  The complete
weighted marked-basis fibre over the generic point of the transverse
binary-polarity component is empty for `H22`.

One required weighted binary neighbor has zero all-kernel diagonal for every
fifth-coordinate extension, every marking, every homogeneous merge weight,
and every diagonal source scaling.  No mixed equation, elimination, rank
minor, or ternary test is needed.

Together with the preceding `H31` theorem, all twelve currently certified
pure-`P_4` component orbits are now generically closed for both marked types.
Special parameter/projective boundaries, component exhaustiveness, and the
global Krenn--Gu conjecture remain open.

## The kernel rows

Use the dense component normal form

```text
a=X_0+X_1,       c=X_0-X_1,
d=(r+2)(k+1)X_1+X_2+kX_3,
n=-(k-1)(r+2)X_0-X_2+kX_3.                         (1)
```

Its intrinsic kernel rows are

```text
alpha_0=n,       alpha_1=a,
alpha_2=a,       alpha_3=d.                         (2)
```

Active-row shifts change no row in (2), so the obstruction below is
simultaneous in the complete affine marking chart.

Restore arbitrary source scalings

```text
diag(t_0,t_1,t_2,t_3)                               (3)
```

and merge `X_0,X_1` with homogeneous weights `(lambda,mu)`.  Append arbitrary
fifth-coordinate entries `x_i`.  In the target channels

```text
(lambda X_0+mu X_1, X_2, X_3, X_4),                (4)
```

the four extended kernel rows have the shape

```text
A_0=(*, -t_2, k t_3,x_0),
A_1=(lambda t_0+mu t_1,0,0,x_1),
A_2=(lambda t_0+mu t_1,0,0,x_2),
A_3=(*,  t_2, k t_3,x_3).                          (5)
```

The starred merged entries are irrelevant.

## The saturated two-channel cut

Rows `A_1,A_2` are supported only on the merged and fifth channels.  Every
perfect matching assigns them to exactly those two channels, leaving rows
`A_0,A_3` on `X_2,X_3`.  Their residual permanent is

```text
per [[-t_2,k t_3],
     [ t_2,k t_3]]

=(-t_2)(k t_3)+(k t_3)t_2=0.                      (6)
```

Therefore

```text
per(A_0,A_1,A_2,A_3)=0                             (7)
```

identically in `r,k,t_i,lambda,mu,x_i`.  A binary `Delta_2` restriction in
the marked basis requires both opposite diagonal coefficients to be nonzero.
Equation (7) kills the all-kernel diagonal of the weighted `01` neighbor, so
that neighbor cannot be binary and a weighted `H22` lift is impossible.

The identity is homogeneous in `(lambda,mu)`, so it covers both affine slope
charts and their projective endpoints.  Zero, equal, and opposite weights
require no separate cases.

## The geometry that survives projection

Equation (6) is exactly

```text
(-X_2+kX_3)(X_2+kX_3)=0                            (8)
```

in the squarefree binary block.  In the component theorem this pair is the
graph of the split polarity involution on `P^1`; in the weighted theorem it
is a zero two-channel transfer.  The same object appears in three languages:

```text
binary invariant theory:  polarity conjugates,
commutative algebra:       an exact pair of zero divisors,
tensor networks:           a saturated cut with zero transfer permanent.
```

Kustin--Striuli--Vraciu's general exact-zero-divisor framework
([arXiv:1304.0411](https://arxiv.org/abs/1304.0411)) and
Abdesselam--Chipalkatti's quadratic involutions on binary forms
([arXiv:1008.3117](https://arxiv.org/abs/1008.3117)) supply the neighboring
languages.  The new point here is that the polarity pair is isolated by the
weighted channel cut, making the obstruction literal rather than
determinantal.

## Proof boundary

The twelfth component is now generically closed for both `H31` and weighted
`H22`, as are the eleven earlier components.  This is still a finite
generic-component theorem.  It does not close special component parameters,
projective compactification boundaries, unknown pure components, or the
global graph conjecture.

## Verification

Run:

```text
uv run --with sympy python claims/p5/h22/transverse-common-factor/verify_p5_h22_transverse_common_factor_component_generic_obstruction.py
uv run --with sympy python claims/p5/h22/transverse-common-factor/audit_p5_h22_transverse_common_factor_component_generic_obstruction.py
```

The primary verifier reconstructs the component rows, pure coefficient,
arbitrary source scalings, homogeneous merge weights, and (5)--(7).  The
independent audit imports no constructor from the primary verifier; it uses a
subset-dynamic-programming permanent, independent kernel-row scalings, and a
within-block source swap.  Both are fixed symbolic identities, not searches.
