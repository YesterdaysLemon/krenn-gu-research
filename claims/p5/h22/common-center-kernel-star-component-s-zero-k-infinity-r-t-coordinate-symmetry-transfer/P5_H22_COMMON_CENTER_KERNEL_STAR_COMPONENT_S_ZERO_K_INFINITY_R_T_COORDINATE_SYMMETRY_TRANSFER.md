# Component twenty-three corner `r=0` to `t=0` finite-`H22` symmetry transfer

## Status

**Exact characteristic-zero corner-symmetry theorem.**  On the simultaneous
`s=0,k=infinity` corner of component twenty-three, the tensor-mode
transposition `(2 3)` carries

```text
(r,t) -> (t,r).                                   (1)
```

It fixes the ambient source coordinates, both labelled contractions `D01`
and `D23`, and the common homogeneous weight `[mu:nu]`.  Consequently the
verified theorem that every finite-weight ternary weighted-`H22` incidence
is empty on

```text
r=0,  t finite
```

transfers without an omitted zero-weight slice to

```text
t=0,  r finite.                                   (2)
```

This is a symmetry corollary of the separately replayable `r=0` theorem.  It
does not close the projective weight `[1:0]`, `r=infinity`, another corner or
component chart, arbitrary source order, global gluing, or the global
Krenn--Gu conjecture.  Those scopes remain **UNKNOWN** or **UNRESOLVED** as
appropriate.  No finite-field computation is used.

## The corner-only involution

Put

```text
A=(1,1,0,0),   C=(1,-1,0,0),
B=(0,0,1,1),   D=(0,0,1,-1).
```

After the legal row rescaling used to reach `k=infinity`, the corner rows are

```text
alpha=(A,D,B+rD,B+tD),
beta =(B,B,C,C).                                   (3)
```

Let

```text
rho=(0,1,3,2).
```

Then direct row comparison gives

```text
alpha_rho(i)(r,t)=alpha_i(t,r),
beta _rho(i)(r,t)=beta _i(t,r)                    (4)
```

for all four modes.  Thus no ambient transformation is needed: (4) is just
the legal permutation of tensor factors `(2 3)`.  In particular it is an
involution and preserves the permanent exactly.

For the affine marked rows

```text
marked_i=beta_i+h_i alpha_i,
```

the induced marking and extension-coordinate maps are

```text
h'=(h0,h1,h3,h2),
x'=(x0,x1,x3,x2; x4,x5,x7,x6).                   (5)
```

Both maps are involutions.  The primary and no-import audit also check that
all four marked row pairs remain bases of their planes.  For the two
parameter-dependent planes, complementary two-by-two minors are

```text
(-(u+1), u-1),
```

which never vanish simultaneously in characteristic zero.

## Homogeneous weighted covariance

Write the common homogeneous weight as `[mu:nu]` and use

```text
D01(v,e;[mu:nu])=(mu*v0+nu*v1,v2,v3,e),
D23(v,e;[mu:nu])=(v0,v1,mu*v2+nu*v3,e).           (6)
```

Because the mode permutation in (4) does not touch the source coordinates,
neither contraction nor its weight changes.  If `C^d_epsilon` is the binary
coefficient with row word `epsilon`, and

```text
epsilon^rho=(epsilon0,epsilon1,epsilon3,epsilon2),
```

then for `d=D01,D23`, direct expansion gives

```text
C^d_epsilon(t,r,h';[mu:nu],x')
 = C^d_(epsilon^rho)(r,t,h;[mu:nu],x).            (7)
```

The primary and independent audit check (7) for all sixteen words in each
contraction.  Hence all fourteen mixed equations, both pure diagonals,
shared-extension kernels, and the genuine diagonal nonvanishing conditions
are transported bijectively in both directions.

The identity weight action is essential.  In particular,

```text
[0:1] -> [0:1],       [1:0] -> [1:0].             (8)
```

Thus the finite zero-weight target is covered by the finite zero-weight
source theorem.  By contrast, the ambient involution

```text
J(v0,v1,v2,v3)=(-v1,-v0,v3,v2)
```

used on the normalized affine sheet sends `[mu:nu]` to `[nu:mu]`.  Applying
that involution here would exchange finite zero weight with projective
weight and therefore would **not** prove (2).  The proof uses the extra
corner symmetry (4), not `J`.

## Exact ternary compatibility

Let `gamma_i` be an arbitrary missing third row in mode `i`, including its
extension coordinate.  Set

```text
gamma'_i=gamma_rho(i).                             (9)
```

Equations (4), (5), and (9) identify every four-row selection made from
`alpha`, `marked`, and `gamma` with the corresponding selection after the
mode transposition.  Permanent invariance therefore transports every
ternary coefficient, not merely the binary incidence.

The primary checks all `3^4=81` ternary row words structurally and directly
expands all sixty-four one-`gamma` equations (four missing-row positions,
eight binary choices, and two contractions).  The no-import audit rebuilds
the five-by-five permanent by subset dynamic programming and expands all
eighty-one ternary words independently for each of `D01` and `D23`.  Hence
the one-`gamma` full-rank obstruction used on the source divisor is a legal
obstruction after transfer, with the obstructed mode relabelled by `rho`.

## Transfer of the finite coordinate divisor

On the verified source divisor write `(r,t)=(0,s)` with `s` finite.  Equation
(1) gives

```text
(0,s) -> (s,0).                                   (10)
```

The source theorem has two parts: for `s!=0` it classifies the complete
genuine shared binary survivor and excludes every member by a uniform
one-`gamma` determinant; at `s=0` a separate exact saturation already makes
the genuine shared binary incidence empty.  Equations (5)--(9) are
bijective and retain the same finite weight.  They therefore transfer both
parts and prove (2) for every marking and every finite weight, including
`[0:1]`.

The source theorem leaves `[1:0]` and `s=infinity` open.  Since the symmetry
fixes the projective weight and sends `s=infinity` to `r=infinity`, those
boundaries remain open rather than being silently imported into the claim.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-s-zero-k-infinity-coordinate-survivor/verify_p5_h22_common_center_kernel_star_component_s_zero_k_infinity_coordinate_survivor.py
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-s-zero-k-infinity-coordinate-survivor/audit_p5_h22_common_center_kernel_star_component_s_zero_k_infinity_coordinate_survivor.py
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-s-zero-k-infinity-r-t-coordinate-symmetry-transfer/verify_p5_h22_common_center_kernel_star_component_s_zero_k_infinity_r_t_coordinate_symmetry_transfer.py
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-s-zero-k-infinity-r-t-coordinate-symmetry-transfer/audit_p5_h22_common_center_kernel_star_component_s_zero_k_infinity_r_t_coordinate_symmetry_transfer.py
```

The first two commands replay the source finite-divisor theorem.  The last
two check the exact corner symmetry and its binary and ternary covariance in
both directions.  The audit has no repository imports.
