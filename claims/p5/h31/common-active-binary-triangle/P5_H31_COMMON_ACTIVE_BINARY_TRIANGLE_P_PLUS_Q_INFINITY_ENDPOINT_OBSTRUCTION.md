# Direct `H31` obstruction on the two component-14 infinity endpoints

## Status

**VERIFIED after fresh independent replay.**  Exact characteristic-zero
matrix reconstruction gives an empty marked `H31` fibre on both infinity
endpoint faces displayed by the diagonal-source-torus `p+q=0` classification.
No finite-field computation or broad search is used.  This does not address
weighted `H22`, other projective limits, non-diagonal source transformations,
local-to-global gluing, or the global Krenn--Gu conjecture.

## Endpoint normalization and bases

Permute component modes as `(endpoint 1,2,3,0)` and normalize source
coordinates by

```text
A -> A/(P0 c1),        B -> -B/(P0 c2),        C -> C.
```

The component-14 parameters are `(p,q)=(-1,0)`, hence `S=p+q+1=0`.  Put

```text
e=(1,0,0,0), w=(0,1,1,1), u=(0,1,-1,0),
v1=(0,1,1,0), v2=(0,0,0,1),

alpha=(e,e,-u,2v2-v1),
beta =(w,w,e,gamma e+v1).                            (1)
```

For `gamma=0`, the last plane is `<A+B,C>`, the off-wall endpoint `t=0`.
For `gamma=2`, it is `<2e+A+B,e+C>`, the on-wall endpoint `t=1/2` after
rescaling `e`.

Every marked basis is `beta_i(h)=beta_i+h_i alpha_i`.  Saturating the mixed
extension incidence by the two diagonal coefficients `A*B` gives exactly

```text
gamma=0: I0=I3=<1>, I1=I2=<h3,h2,h0 h1>,
gamma=2: I0=I3=<1>, I1=I2=<h3,h2,h0+h1,h1^2>.       (2)
```

Thus the off-wall marking scheme is the union of both axes
`(T,0,0,0)` and `(0,T,0,0)`, while the on-wall scheme is supported only at
the origin.  The primary and audit reconstruct all eight saturated
projections bidirectionally.

## Complete kernels and the fixed minor

For deleted coordinates `d=1,2`, every displayed mixed matrix has rank six.
The verifiers construct a complete two-column kernel frame and write
`z=x k0+y k1`.  Their diagonal rows are

```text
d=1: A=-4x,          d=2: A=4x,

gamma=0, either axis: B=4(Tx+y),
gamma=2, origin:     B=4y.                           (3)
```

For marked mode two, the fixed `4 x 4` minor on rows `0127` is

```text
gamma=0: -32 x^2 (Tx+y),
gamma=2: -32 x^2 y.                                 (4)
```

On the genuine-neighbour open `A*B!=0`, (3) makes the corresponding factor
in (4) nonzero.  The marked map therefore has rank four, contradicting the
rank-at-most-three condition for an `H31` lift.  This covers both axes,
their common origin, both deleted coordinates, and both endpoint faces.

## Why the generic component-14 certificate is not specialized

The generic quotient uses `D00=(2tab)^-1`, which is undefined on the
off-wall endpoint `t=0`.  Its cleared `0147/0457` formulas vanish when
`S=0`, and its endpoint resultant ratios are `0/0` in that singular gauge.
These are retained as failed proof routes, not endpoint evidence.  The direct
bases (1), saturated projections (2), complete kernels (3), and minor (4)
replace the invalid specialization.  The same row minors computed in the
direct endpoint gauge need not vanish and are not identified with the
singular generic formulas.

One attempted direct symbolic specialization of the generic pencil machinery
timed out after 34 seconds and emitted no certificate.  It is discarded as
evidence.  The bounded direct endpoint reconstruction above replaces it.

## Exact replay

```text
uv run --with sympy python verify_p5_h31_common_active_binary_triangle_p_plus_q_infinity_endpoint_obstruction.py
uv run --with sympy python audit_p5_h31_common_active_binary_triangle_p_plus_q_infinity_endpoint_obstruction.py
```

Both commands are exact and bounded.  They use characteristic zero with
`2` invertible, explicitly reconstruct mixed and marked matrices, and do not
infer from a solver exit code alone.  A fresh verifier independently
reconstructed all eight projections and six uniform kernel/minor cases, so
the two displayed diagonal-DVR infinity faces are `VERIFIED` `H31`-empty.
