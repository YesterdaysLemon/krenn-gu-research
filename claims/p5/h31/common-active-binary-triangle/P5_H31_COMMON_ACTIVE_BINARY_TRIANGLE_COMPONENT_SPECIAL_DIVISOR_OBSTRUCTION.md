# Special-divisor `H31` exclusion for component twenty

## Status

**Exact characteristic-zero divisor-generic theorem.**  The complete marked
`H31` fibre is empty over the generic point of each of nine affine special
divisors in the normalized common-active binary-triangle chart:

```text
q=p+2,   q=p,   2pq-p+q=0,
p=0,     p=-1,  q=0,       q=1,
q=1/2,   p=-1/2.
```

This statement is deliberately only divisor-generic.  It does not close
intersections among these divisors, the omitted `p+q=0` normalization chart,
the `p-q+1=0` intrinsic-basis boundary, projective/source-torus limits,
weighted `H22`, component exhaustiveness, or the global Krenn--Gu
conjecture.

## Why the generic theorem missed these fibres

Use the intrinsic bases of
[`P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md),
with marked rows `beta_i+h_i alpha_i`.  For deletion `d`, impose

```text
M_d(h)z=0,       A_d(h)z != 0,       B_d(h)z != 0.       (1)
```

The earlier theorem eliminated (1) over `C(p,q)`, so any incidence supported
only on a proper base divisor disappeared.  Repeating the elimination over
`Q[p,q]`, normalizing `A_3z=1`, inverting `B_3z`, and then eliminating both
`z` and `h` gives the principal base ideal

```text
p(p+1)q(q-1)(q-p)(q-p-2)(2pq-p+q).                  (2)
```

Bidirectional standard-basis reduction checks equality with (2), rather than
only containment.  Thus the seven factors in (2) are the exact affine base
support of deletion-three binary-neighbour incidence in this normalized
chart.

The deletion-one and deletion-two projections also have two marking-space
discriminants omitted from the earlier handoff:

```text
q=1/2:   d=1 has the two axes h1*h2=0,
p=-1/2:  d=2 has the two axes h1*h2=0,               (3)
```

always with `h0=h3=0`.  These are marking degenerations, not additional
deletion-three factors.

## Exact projections on the nine divisors

Write `t` for the free base parameter and `r` for a marking-line parameter.
Deletions not listed below retain the two isolated generic markings or have
unit projected ideal exactly as in the generic theorem.

| divisor | special projected marking strata |
|---|---|
| `q=p` | `d=3: h=(0,0,t,0)` |
| `q=p+2` | `d=3: h=(0,t+1,0,0)` |
| `2pq-p+q=0`, `q=t/(2t+1)` | `d=3: h0=h3=0`, `h1=h2`, `h2^2=0` |
| `p=0` | `d=2: h=(0,r,0,0)`; `d=3: h=(0,t-1,0,0)` |
| `p=-1` | `d=2: h=(0,0,r,0)`; `d=3: h=(0,0,t,0)` |
| `q=0` | `d=1: h=(0,r,0,0)`; `d=3: h=(0,t+1,0,0)` |
| `q=1` | `d=1: h=(0,0,r,0)`; `d=3: h=(0,0,t,0)` |
| `q=1/2` | `d=1: h=(0,r,0,0)` or `(0,0,r,0)` |
| `p=-1/2` | `d=2: h=(0,r,0,0)` or `(0,0,r,0)` |

For `2pq-p+q=0`, the nilpotent `h2^2` records a nonreduced projected scheme;
its geometric point is still only `h=0`.  The verifier proves every displayed
projected ideal in both containment directions over the corresponding
function field `C(t)`.

## Uniform marked-minor obstruction

On every projected point or line above, and on the residual generic marking
points for the other deletions, the mixed matrix has rank six.  Let `N_3(z)`
be the neighbouring mode-three one-marked map.  One of the two row sets

```text
0147,   0247                                             (4)
```

has nonzero determinant on the entire binary open (1).  This is checked
without choosing a parameter grid: for every marking stratum, exact
characteristic-zero standard-basis reduction gives

```text
<M_d(h)z, A_d(h)z-1, w B_d(h)z-1,
  det N_3(z)[selected rows]> = <1>.                    (5)
```

When a marking line is present, `r` remains a polynomial variable in (5), so
the certificate covers every point of the line, including its intersections
with the other marking component.  A fixed pure mode-three entry in the
deleted source column is also nonzero over `C(t)` on each stratum.

Consequently the same linear argument as in the generic theorem applies.
Injectivity of `N_3(z)` forces the third target-coordinate row in mode three
onto the deleted pure coordinate; the pure transverse entry kills that last
coefficient.  Target rank three is impossible.

## Scope of the component boundary

All nine divisors retain the generic pair profile `(4,4,4,3,3,3)` on a dense
open of the displayed component chart.  In particular, the four loci
`p=0,-1` and `q=0,1` are special for the marked-extension projection, not
because a rank-four pair drops: the exact stacked-plane determinants for the
first three pairs are `2(p+q)`, `2(p+q)`, and `-2`.  This theorem closes the
divisor-generic marked `H31` fibres; it does not classify their intersections
or decide whether special points lie in older component closures.

The points `(-1,0)` and `(0,1)` have zero pure tensor.  The line `p+q=0` is
outside the normalized `U0` chart, while `p-q+1=0` makes the displayed
intrinsic pure basis dependent.  None is silently included in the present
claim.

## Exact replay

```text
uv run --with sympy python \
  claims/p5/h31/common-active-binary-triangle/verify_p5_h31_common_active_binary_triangle_component_special_divisor_obstruction.py

uv run --with sympy python \
  claims/p5/h31/common-active-binary-triangle/audit_p5_h31_common_active_binary_triangle_component_special_divisor_obstruction.py
```

The primary verifier performs all characteristic-zero eliminations and
minor-open emptiness certificates.  The independent audit rebuilds the
permanent maps without importing the primary verifier, checks the residual
identities exactly, and exhausts representative finite-field markings only
as a regression audit.  No finite-field census is used to infer the
characteristic-zero theorem.
