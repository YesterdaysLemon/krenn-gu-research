# Verified marked-`H31` obstruction on the exceptional lower-pair fibres

## Status and scope

**VERIFIED.**  This note records a direct characteristic-zero calculation for
the component-fifteen support-one lower-pair fibres left open by
`P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md`.
It treats the finite centres `a=0,-1` with negative lower-pair valuation.  It
does not use specialization from the generic component-fifteen theorem.

The calculation is limited to marked `H31`.  It proves neither weighted
`H22`, the two component-fourteen infinity endpoints, an arbitrary-order
local-to-global reduction, nor the global Krenn--Gu conjecture.

## Residue parameters and exact planes

Put

```text
e=X0,  L=A-B,  M=A+B,  C=X3,  W=xL+yM.
```

For a diagonal DVR arc write `pi=P0/c1`, `theta=Q0/c2`, and
`Delta=pi+theta`.  The three valuation regimes are encoded by

```text
valuation(y0)>-R:       x=0,              y=0,
valuation(y0)=-R, R<d: x=pi,             y=0,
valuation(y0)=-R, R=d: x=(pi-theta)/2,   y=Delta/2 != 0.             (1)
```

At `a=0`, after the mode order `(V0,V1,V2,V3)=(U1,U3,U2,U0)`, the baseline
family is

```text
V0=<e,L>,  V1=<e,M>,  V2=<e,C+xL+yM>,  V3=<L,C-yM>.                 (2)
```

The last plane has Pluecker coordinates
`(0,0,0,-2y,1,-1)` in the order `01,02,03,12,13,23`.  Thus the deepest
`R=d` fibre retains its `12` coordinate: replacing `V3` by `<L,C>` before
setting `y=0` is invalid.

On the cancellation wall, with `gamma=c0/Delta != 0`, replace only the last
plane by

```text
V3=<L+gamma e,C-xL-yM>,                              (3)
```

whose Pluecker tuple is

```text
(-gamma(x+y), gamma(x-y), gamma, -2y, 1, -1).        (4)
```

At `a=-1`, first swap the two lower modes and then apply the allowed diagonal
source symmetry `e -> -e` before the displayed reordering.  This changes the
first three mode-zero Pluecker coordinates to the `a=0` signs while leaving
`p12,p13,p23` unchanged.  After harmless reparametrization of the nonzero wall
scalar if required by the coordinate convention, the same baseline and wall
normal forms result.

## Pure orientations

The baseline orientation is

```text
alpha=(e,M,e,C-xL-yM),
beta =(L,e,C+xL+yM,L),                               (5)
```

and the wall orientation is obtained by replacing the last entry of `beta`
by `L+gamma e`.  In both cases the only nonzero squarefree permanent
coefficient is

```text
T_1111=-2.                                           (6)
```

## Normalized marked projections

For a marking `h=(h0,h1,h2,h3)`, replace `beta_i` by
`beta_i+h_i alpha_i`.  For deletion `d`, let `M_d(h)` be the fourteen mixed
rows in the eight extension coordinates and let `A_d,B_d` be the two binary
diagonal rows.  The projected ideal is obtained exactly from

```text
<M_d(h)z, A_d z-1, w B_d z-1>
```

by eliminating `(z,w)`.  For the wall family the equation
`gamma_inverse*gamma-1` is also included.  Bidirectional standard-basis
reduction gives the following complete projection ideals.

For the baseline:

```text
J0=<1>,
J1=J2=<h1,h2,h3>,
J3=<h3,h1,(x^2-y^2)h0+xh2, xh2^2, h0h2>.           (7)
```

For the wall, on `gamma!=0`:

```text
J0=<1>,
J1=J2=<h0,h1,h2,h3>,
J3=<h0,h1,h3,xh2>.                                  (8)
```

Thus the baseline `d=1,2` branch has `h=(t,0,0,0)`.  The baseline `d=3`
projection has the exhaustive geometric branches

```text
x^2!=y^2, x!=0: h=0;        x=y!=0: h=(t,0,0,0);
x=-y!=0: h=(t,0,0,0);       x=0,y!=0: h=(0,0,t,0);
x=y=0: h0*h2=0.                                      (9)
```

The wall `d=3` branch is `h=0` for `x!=0`, and
`h=(0,0,t,0)` for `x=0`.

## Complete kernels and fixed minors

All statements below refer to complete symbolic nullspaces of `M_d`, not to
sampled extension vectors.  Write the kernel coefficients as `X,Y,Z`.

For baseline `d=1,2`, `rank(M_d)=5` and `nullity(M_d)=3`.  The binary
diagonals and the fixed mode-one minor on rows `0137` are

```text
d=1: A=-2X, B=-2(Xt+Z), det= 8X^2(Xt+Z),
d=2: A=-2X, B= 2(Xt+Z), det=-8X^2(Xt+Z).            (10)
```

The pure mode-one transverse entry is respectively row `011`, column `1`
equal to `-1`, and row `011`, column `2` equal to `1`.

For every baseline `d=3` branch with `y!=0`, `rank(M_3)=6` and nullity is
two.  On mode-one rows `0157`, with pure transverse entry row `101`, column
`3` equal to `-2`, the complete-kernel formulas are

```text
h=0:             A=4Xy, B=-2Y,             det= 32X^2Yy,
x=y,h0=t:        A=4Xy, B=-2(2Xty+Y),      det= 32X^2y(2Xty+Y),
x=-y,h0=t:       A=4Xy, B= 2(2Xty-Y),      det=-32X^2y(2Xty-Y),
x=0,h2=t:        A=4Xy, B=-2(Xt+Y),        det= 32X^2y(Xt+Y).       (11)
```

For the wall, `d=1,2` again have rank five and nullity three:

```text
d=1: A=-2X, B=-2Z, det= 8X^2Z,
d=2: A=-2X, B= 2Z, det=-8X^2Z.                       (12)
```

On wall `d=3`, `y!=0` gives rank six and nullity two.  The same fixed rows
and transverse entry give

```text
x!=0,h=0:
  A=4Yy/gamma, B=-2(X+2Yx),
  det=32Y^2y(X+2Yx)/gamma^2;
x=0,h2=t:
  A=4Yy/gamma, B=-2(X gamma+Yt)/gamma,
  det=32Y^2y(X gamma+Yt)/gamma^3.                    (13)
```

In each displayed `y!=0` branch, simultaneous nonvanishing of the two binary
diagonals makes the fixed minor nonzero.  The injective marked mode, followed
by the fixed pure transverse entry, excludes a third target row.

## The `y=0` correction

The `y=0` specializations must be rebuilt; (11) and (13) cannot be divided by
`y`.  Their complete kernels give:

```text
baseline y=0,x!=0,h=0: rank 4, nullity 4, A|ker=0;
baseline x=y=0,h0=t:   rank 2, nullity 6, A|ker=0;
baseline x=y=0,h2=t:   rank 2, nullity 6, A|ker=0;
wall y=0,x!=0,h=0:     rank 4, nullity 4, A|ker=0;
wall x=y=0,h2=t:       rank 2, nullity 6, A|ker=0.   (14)
```

Hence these projection branches contain no genuine binary neighbour; they
are not counterexamples obtained by specializing a `y!=0` kernel.

## Retained boundaries and replay

- Projection ideals are closures; (14) is the direct fibre check required to
  interpret them.
- `gamma!=0` is essential on the wall and is saturated explicitly.
- No finite-field computation is used.  Every identity is over
  characteristic zero.
- A fresh no-import audit independently reconstructed the exact planes,
  projections, complete kernels, fixed minors, transverse entries, and `y=0`
  correction before this claim was promoted to `VERIFIED`.

Replay with

```text
uv run --with sympy python claims/p5/h31/common-active-binary-triangle/verify_p5_h31_common_active_binary_triangle_p_plus_q_exceptional_lower_pair_obstruction.py
uv run --with sympy python claims/p5/h31/common-active-binary-triangle/audit_p5_h31_common_active_binary_triangle_p_plus_q_exceptional_lower_pair_obstruction.py
```

The primary reconstructs all matrices from the standard marked-basis helper,
checks (1)--(14), and proves (7)--(8) by exact bidirectional elimination.  The
audit has its own permanent and matrix construction, repeats every displayed
complete-kernel, diagonal, fixed-minor, transverse, and `y=0` check, and
spot-audits the two nontrivial `d=3` projection ideals without importing the
primary.
