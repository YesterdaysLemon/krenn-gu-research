# Component 23 `s=0, rt=1` marked-`H31` obstruction

## Status

**Exact characteristic-zero normalized-face theorem.**  The complete
marked-`H31` fibre is empty on the normalized all-pair face

```text
s=0,       rt=1,       r(r-1)(r+1)!=0,
```

with `k` arbitrary.  This includes the rank-drop divisor `k=0`.  Every
marked basis, all four source-coordinate insertions, and every projective
extension direction are covered.

The endpoints `r=+/-1` are lower-pair points and are outside this theorem.
Other normalized faces, arbitrary ambient/source changes, arbitrary-order
gluing, and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Face geometry

Put

```text
A=(1,1,0,0), C=(1,-1,0,0),
B=(0,0,1,1), D=(0,0,1,-1).
```

On the face the four planes have rows

```text
alpha=(A, A+kD, B+rD, B+D/r),
beta =(B, B,    C,    C).                         (1)
```

Only `T1111=-4` is nonzero.  The generic pair profile is
`(3,3,3,4,4,3)`; at `k=0` it is `(3,3,3,3,3,3)`, still all-pair.  Edge
`23` has rank two at `r=+/-1`, explaining the stated localization.

Every marked basis is represented uniquely up to rescaling by

```text
beta_i(h)=beta_i+h_i alpha_i.                     (2)
```

There is no missing projective marking endpoint: a second row proportional
to `alpha_i` is not a basis.

## Exact binary projection

For insertion `d`, let `M_d(h)` be the fourteen mixed rows and let `a_d,b_d`
be its two diagonal rows.  Normalize `a_d z=1` and invert `b_d z`; this
covers every projective genuine-binary extension.  Exact elimination over

```text
S=Q[r,k,1/(r(r-1)(r+1))]
```

gives unit ideals for `d=0,1`, and for both `d=2,3` gives exactly

```text
<h0,h1,h2*h3>.                                    (3)
```

Thus only four punctured branches and their common intersection remain.

## Punctured branches

Write the extension parameters as `(c,p,q,w)`.  On `h2=0,h3=g`, use

```text
d=2: z=(0,kq,c,p; q,w,0, gc/r),
d=3: z=(0,-kq,c,p; q,w,0,-gc/r),                 (4)
```

and on `h3=0,h2=g`, use

```text
d=2: z=(0,kq,p,c; q,w,grc,0),
d=3: z=(0,-kq,p,c; q,w,-grc,0).                  (5)
```

These four displayed parameterizations span the complete four-dimensional
mixed kernels, including `k=0`.  On the punctured branches `g!=0`, the two
selected one-marked minors have, after removing their common nonzero
factors, the residual pairs

```text
                    R0                         R1
d2,h2=0:     pr+(r-1)w                 c+(r-1)w
d2,h3=0:      p-(r-1)w                -cr+(r-1)w
d3,h2=0:     pr+(r+1)w                -c+(r+1)w
d3,h3=0:      p+(r+1)w                -cr+(r+1)w.                 (6)
```

The relevant difference or sum in each row is precisely `pr-c`, `p-cr`,
`pr+c`, or `p+cr`, respectively, hence a nonzero scalar multiple of the
alpha diagonal.  The beta diagonal is `-2(q+w)`.  Therefore a genuine
binary extension makes at least one selected minor nonzero.  The pure
transverse entries for the same marked modes are

```text
d2,h2=0: 2(r-1)/r,    d2,h3=0: -2(r-1),
d3,h2=0: 2(r+1)/r,    d3,h3=0:  2(r+1).           (7)
```

The standard transverse-coordinate argument then forces the third target
row to vanish, contradicting target rank three.

## The common intersection and the essential `k=0` split

At `h=0`, parameterizations (4)--(5) agree.  Stack the neighbouring
one-marked `8 x 4` matrix into the columns consisting of the three common
source coordinates and the new coordinate, and stack the pure one-marked
`8 x 4` matrix into the four original source columns.  This gives the exact
`16 x 5` linear conditions on a possible third target row.

For `k!=0`, in one-marked mode zero the determinant on stacked rows
`(0,7,11,13,15)` is

```text
d=2: -64 k (pr-c)(r-1)/r,
d=3: -64 k (pr+c)(r+1)/r.                         (8)
```

The factors `pr-c` and `pr+c` are the alpha diagonals up to units.  Hence
the stack has rank five on the genuine-binary open.

At `k=0`, (8) vanishes and must not be used.  The stack instead has rank
four.  Polynomial generators of its mode-zero and mode-one kernels are

```text
d=2: gamma0=(0,0, 1,-1,w), gamma1=(0,0, 1,-1,q),
d=3: gamma0=(0,0,-1, 1,w), gamma1=(0,0,-1, 1,q).  (9)
```

The verifier checks the complete kernel equations and that each generator
is independent of its corresponding two-row local plane.  Nevertheless the
pure coefficient with target word `2211` is exactly

```text
per(gamma0,gamma1,beta2,beta3)=4.                 (10)
```

This forbidden two-third-row coefficient rules out a ternary diagonal lift.
Thus the rank drop at `k=0` is an obstruction, not a survivor.

Combining (3), the punctured certificates (6)--(7), and the intersection
certificates (8)--(10) proves that the marked-`H31` fibre of (1) is empty.

## Replay

```powershell
uv run --with sympy python verify_p5_h31_common_center_kernel_star_component_s_zero_rt_one_all_pair_obstruction.py
uv run --with sympy python audit_p5_h31_common_center_kernel_star_component_s_zero_rt_one_all_pair_obstruction.py
```

The primary verifier performs exact localized eliminations and symbolic
kernel/minor identities.  The no-import audit independently rebuilds the
rows, projections, stacks, and the `k=0` higher-mixed obstruction.  No
finite-field calculation is used.
