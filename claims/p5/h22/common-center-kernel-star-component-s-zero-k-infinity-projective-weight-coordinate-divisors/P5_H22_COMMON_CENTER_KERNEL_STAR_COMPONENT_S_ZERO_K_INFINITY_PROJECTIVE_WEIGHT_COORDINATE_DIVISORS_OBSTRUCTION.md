# Component twenty-three corner projective-weight coordinate-divisor obstruction

## Status

**Exact characteristic-zero normalized-corner theorem.**  On the simultaneous
`s=0,k=infinity` corner of component twenty-three, the complete ternary
weighted-`H22` incidence at projective weight

```text
[mu:nu]=[1:0]
```

is empty on both finite coordinate divisors

```text
r=0,  t finite,       and       t=0,  r finite.   (1)
```

On the first divisor, exact saturated elimination leaves a genuine shared
binary survivor when `t!=0`, but a uniform one-missing-row determinant
excludes every member from a ternary lift.  At `t=0`, even the genuine shared
binary incidence is empty.  The second divisor follows from the exact
corner-only mode transposition `(2 3)`, which fixes projective weight.

This theorem is for the fixed normalized component order.  The parameter
endpoints `t=infinity` and `r=infinity`, other component charts, arbitrary
source order or ambient changes, global gluing, and the global Krenn--Gu
conjecture remain **UNKNOWN** or **UNRESOLVED** as appropriate.  No
finite-field calculation is used.

## Corner rows and projective contractions

Put

```text
A=(1,1,0,0),   C=(1,-1,0,0),
B=(0,0,1,1),   D=(0,0,1,-1).
```

After the legal row rescaling defining the `k=infinity` limit, the corner is

```text
alpha=(A,D,B+rD,B+tD),
beta =(B,B,C,C).                                   (2)
```

Fix `r=0` and mark every plane by

```text
marked_i=beta_i+h_i alpha_i.                      (3)
```

This is a complete marked-basis chart: once `alpha_i` is fixed, every second
basis row has nonzero `beta_i` coefficient and can be uniquely rescaled to
(3).  At `[1:0]`, the two homogeneous projections are

```text
D01(v,e)=(v0,v2,v3,e),
D23(v,e)=(v0,v1,v2,e).                            (4)
```

Let `x=(x0,...,x3;y0,...,y3)` be the common extension coordinates.  Expand
all sixteen binary permanent coefficients for each projection in (4), and
let `M` be the combined `28 x 8` matrix of the fourteen mixed coefficients
from each contraction.  In diagonal order

```text
(A01,B01,A23,B23),
```

one has `A23=0` identically.  The genuine weighted-`H22` open is therefore

```text
A01*B01*B23 != 0,                                 (5)
```

because both beta diagonals and at least one alpha diagonal are required.

## Complete shared binary incidence

Saturate the twenty-eight mixed equations by the product in (5) and eliminate
the eight extension coordinates.  Exact elimination in both directions
gives

```text
<h3,h0,t*h1-1>.                                   (6)
```

Thus `t=0` has no genuine shared binary incidence.  For `t!=0`, every genuine
point has

```text
h=(0,1/t,H,0).                                    (7)
```

On (7), the mixed matrix kills

```text
z0=(0,0,-1,-1;0,1,0,0).                          (8)
```

Its minor on rows `(1,3,4,8,9,12,16)` and columns
`(0,1,2,3,4,6,7)` is

```text
-128*t^2.                                         (9)
```

Hence `M` has rank exactly seven for `t!=0`, and (8) spans its projective
kernel.  Evaluating the four diagonals on (8) gives

```text
(A01,B01,A23,B23)=(2t,2H,0,-2).                  (10)
```

Consequently the complete genuine binary survivor is exactly (7)--(8) on

```text
t*H != 0.                                         (11)
```

## Uniform ternary obstruction

Append (8) to the four `alpha` and four marked rows.  The contraction rows
corresponding to (4) are

```text
q01=(0,1,0,0,0),       q23=(0,0,0,1,0).          (12)
```

Let `gamma_0` be the missing third row in mode zero.  Keeping `gamma_0`,
choosing `alpha` or `marked` independently in the other three modes, and
contracting with both rows in (12) gives a `16 x 5` linear one-`gamma` matrix
`F_0`.  In the row order consisting of the eight `q01` words followed by the
eight `q23` words,

```text
det F_0[0,1,2,7,9] = 8*H*t^2.                    (13)
```

Equation (13) is nonzero everywhere on (11).  Therefore `F_0 gamma_0=0`
forces `gamma_0=0`, contradicting a genuine third row in the local ternary
space.  Every binary survivor is obstructed before coefficients containing
two or more missing rows need to be considered.  Together with the empty
`t=0` binary fibre from (6), this proves the first half of (1).

## Transfer to the other coordinate divisor

The corner rows (2) have an extra symmetry not present on the normalized
affine sheet.  The tensor-mode transposition `(2 3)` sends

```text
(r,t) -> (t,r),
h -> (h0,h1,h3,h2),
x -> (x0,x1,x3,x2;x4,x5,x7,x6).                 (14)
```

It acts trivially on the ambient source, so it fixes both contractions in
(4) and the projective weight `[1:0]`.  The primary checks all sixteen binary
words in both directions.  The independent audit additionally rebuilds all
eighty-one ternary row words for each contraction and verifies their exact
covariance under (14).  Applying (14) to the proved `r=0,t` divisor therefore
closes `t=0,r` for every finite `r`, proving the second half of (1).

The same symmetry sends the still-unproved `t=infinity` source endpoint to
`r=infinity`; it does not close either parameter endpoint.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-s-zero-k-infinity-projective-weight-coordinate-divisors/verify_p5_h22_common_center_kernel_star_component_s_zero_k_infinity_projective_weight_coordinate_divisors_obstruction.py
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-s-zero-k-infinity-projective-weight-coordinate-divisors/audit_p5_h22_common_center_kernel_star_component_s_zero_k_infinity_projective_weight_coordinate_divisors_obstruction.py
```

The primary uses the repository contraction builder, exact saturation,
explicit rank and kernel witnesses, the uniform one-`gamma` determinant, and
direct mode-swap covariance.  The audit has no repository imports: it
rebuilds four- and five-row permanents by subset dynamic programming,
repeats the saturation and witnesses, and checks all binary and ternary
transport identities independently over `Q`.
