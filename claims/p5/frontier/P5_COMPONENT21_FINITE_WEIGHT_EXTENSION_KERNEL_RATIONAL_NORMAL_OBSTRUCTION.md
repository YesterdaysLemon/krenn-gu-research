# Component 21: one finite-weight extension-kernel normal is empty

## Status

**Exact characteristic-zero rational first-normal theorem.**  At the finite
component and weight point

```text
(p,q,kappa,ell,lambda)=(2,3,5,7,1),
```

the stacked `D01/D23` extension map has rank seven and kernel

```text
Z=(-2,0,0,0,-3,0,1,0).                              (1)
```

The complete first normal along the projective extension direction `[Z]` is
empty for weighted `H22`.  This includes arbitrary subordinate extension
coefficients and all first-order variations of `p,q,kappa,ell,lambda`.

This closes one exact rational point of the finite-weight rank-drop locus,
not that locus in general.  Other finite weights and component points, the
two marked-`H31` extension-kernel curves, marking-pole intersections, the
zero base, parameter infinity, arbitrary source/ambient degenerations, and
the global Krenn--Gu conjecture remain **UNRESOLVED**.

No finite-field or numerical rank evidence is used.

## The coupled normal matrix

Let `M(p,q,kappa,ell,lambda)` be the `32 x 8` matrix obtained by stacking the
sixteen binary coefficients of the finite `D01` contraction above the
sixteen coefficients of finite `D23`.  Order the eight subordinate extension
variables first and the five tangent variables as

```text
(z_0,...,z_7, dp,dq,dkappa,dell,dlambda).            (2)
```

Because `M Z=0` at the centre, the complete first normal is the `32 x 13`
matrix

```text
N=[ M | partial_p(MZ) | partial_q(MZ) | partial_kappa(MZ)
      | partial_ell(MZ) | partial_lambda(MZ) ].       (3)
```

Finite marking changes act by invertible triangular transformations on the
binary coefficient rows and extension columns.  Their derivative applied to
`MZ=0` vanishes, while their derivative on `Z` is absorbed by the subordinate
extension variables in (2).  Thus no marking-tangent direction is omitted
from (3).

## Exact rank certificate

Delete the two diagonal words `0000,1111` from each sixteen-row block.  The
resulting `28 x 13` mixed matrix has rank seven.  In global stacked row
indices, rows

```text
(2,3,7,17,18,21,23)
```

and columns

```text
(0,1,2,3,5,7,12)
```

have determinant

```text
5549064192 != 0.                                    (4)
```

All other mixed rows lie in their span.  On the six-dimensional mixed
kernel, the diagonal rows have the exact pattern

```text
D01(0000)=0,
D01(1111)=0,
D23(0000)=0,
D23(1111) possibly nonzero.                         (5)
```

The last possibility is genuine: adjoining global row `31` and using columns

```text
(0,1,2,3,4,5,7,12)
```

gives the `8 x 8` determinant

```text
-22196256768 != 0.                                  (6)
```

Thus (5) is not a zero-normal artefact.  But a genuine binary `H22`
contraction requires both opposite diagonal coefficients after its mixed
coefficients vanish.  The entire `D01` diagonal is zero on every mixed-free
normal, so no weighted-`H22` first normal exists at (1).

## Replay

```powershell
uv run --with sympy python claims/p5/frontier/verify_p5_component21_finite_weight_extension_kernel_rational_normal_obstruction.py
uv run --with sympy python claims/p5/frontier/audit_p5_component21_finite_weight_extension_kernel_rational_normal_obstruction.py
```

The primary builds the normal from the committed component-21 contraction
maps.  The no-import audit reconstructs the bases and permanents using
subset dynamic programming and checks the ranks by an explicit rational
Gaussian algorithm.
