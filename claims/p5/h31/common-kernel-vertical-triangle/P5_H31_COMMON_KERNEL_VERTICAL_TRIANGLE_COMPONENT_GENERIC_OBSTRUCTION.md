# Generic `H31` exclusion for component nineteen

## Status

**Exact characteristic-zero generic-fibre theorem.**  The complete marked
`H31` fibre over the generic point of the common-kernel vertical-triangle
component is empty.

The proof treats every marked basis, all four distinguished source
coordinates, and every projective extension direction.  Exact open-incidence
projection leaves only four rational marking lines.  Two fixed one-marked
minors exclude each punctured line, and two different fixed minors exclude
their shared endpoints.  No parameter grid or ambient graph search is used.

This is a generic theorem.  It does not close the component's special or
projective boundary fibres, weighted `H22`, pure-`P_4` component
exhaustiveness, or the global Krenn--Gu conjecture.

## The intrinsic pure marking

Use the normal form of
[`P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md`](P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md):

```text
A=X0+X1,       Abar=X0-X1,
B=X2+X3,       Bbar=X2-X3,

U0=span(Abar+pB, Bbar+qB),
U1=span(B,A),
U2=span(Bbar,A),
U3=span(Abar,B+phi Bbar).                            (1)
```

Put `r=q-phi` and choose

```text
alpha0=r(Abar+pB)-p(Bbar+qB),   beta0=Abar+pB,
alpha1=B,                       beta1=A,
alpha2=Bbar,                    beta2=A,
alpha3=Abar,                    beta3=B+phi Bbar.    (2)
```

Direct permanent expansion gives

```text
T_w=0 for w!=1111,       T_1111=4p.                 (3)
```

Thus the `alpha_i` are the four intrinsic pure-kernel rows.  Every marked
basis over the same generic four-plane point is, after harmless nonzero row
rescaling,

```text
beta_i(h)=beta_i+h_i alpha_i,       i=0,1,2,3.       (4)
```

The omitted diagonal source torus does not affect the argument: after a
coordinate deletion its nonzero scalings act by invertible column scalings,
and they preserve all mixed kernels, diagonal nonvanishing tests, and
one-marked ranks.

## Exact projection to the marking fibre

For distinguished source coordinate `d`, delete `d`, append the fifth-source
extension column, and write its eight entries as

```text
z=(x0,x1,x2,x3;y0,y1,y2,y3)^T.                     (5)
```

Let `M_d(h)` be the `14 x 8` mixed-coefficient matrix and let `A_d(h),B_d(h)`
be its two diagonal rows.  A genuine binary neighbour requires

```text
M_d(h)z=0,       A_d(h)z B_d(h)z !=0.               (6)
```

Normalize `A_dz=1`, invert `B_dz`, and eliminate `(z,w)` over
`K=C(p,q,phi)`.  Bidirectional standard-basis reduction gives exactly

```text
d=0:  (1),
d=1:  (1),

d=2,3:
  <h3, r h0+1, h1 h2>.                              (7)
```

Hence deletions zero and one have no genuine binary neighbour.  Each of the
other two deletions leaves precisely the two affine marking lines

```text
L1: h0=-1/r, h1=0, h2=t, h3=0,
L2: h0=-1/r, h1=t, h2=0, h3=0.                     (8)
```

There are no hidden marking sheets.

## Two-minor covers on the punctured lines

On every case in (8), `M_d` has rank four.  The verifier gives an explicit
four-coordinate polynomial frame `(a,b,c,e)` for its entire kernel.  Write
the last frame coordinate below as `e` to distinguish it from deletion `d`.
Both binary diagonals are explicit, and `A_dz` is a nonzero scalar times
`a-c`.

For `t!=0`, take the one-marked mode `1` on `L1` and mode `2` on `L2`.
The minors with row sets `0127` and `0237`, divided by the nonzero product
`(A_dz)(B_dz)`, are nonzero scalar multiples of the following residual pairs:

```text
                         0127                 0237
d=2, L1:       a(phi-1)+e          c(phi-1)+e
d=2, L2:       a(phi-1)-e          c(phi-1)-e
d=3, L1:       a(phi+1)+e          c(phi+1)+e
d=3, L2:       a(phi+1)+e          c(phi+1)+e.       (9)
```

In each row, subtracting the two residuals gives

```text
(phi-1)(a-c)       for d=2,
(phi+1)(a-c)       for d=3.                         (10)
```

Both factors `phi-1` and `phi+1` are nonzero in `K`.  Equations (9)--(10)
show that the two minors cannot vanish simultaneously on the genuine-binary
open (6): their common zero would force `a=c`, hence `A_dz=0`.  Therefore the
neighbouring one-marked map has rank four.

That rank statement alone is not yet the global `H31` contradiction.  It
first forces the third target row to vanish on the neighbouring hyperplane,
so that row can still be supported on the deleted source coordinate.  The
pure one-marked map removes this last possibility.  In row `000` and column
`d`, its exact transverse entries are

```text
                         pure transverse entry
d=2, L1:                         2r
d=2, L2:                        -2r
d=3, L1:                        -2r
d=3, L2:                        -2r.                (11)
```

They are nonzero in `K`.  Thus the remaining deleted-coordinate coefficient
also vanishes, making the third target row globally zero and contradicting
the required target rank three.  This closes all four punctured lines.

## The common endpoint

The factors of `t` removed above make `t=0` a separate obligation, not an
allowed cancellation.  At that common endpoint of `L1` and `L2`, use
one-marked mode `3` and row sets `0137` and `0357`.

For deletion two, put

```text
F2=p e(q-1)-b r(phi-1),
R1=a(phi-1)+e,
R3=ap(q-1)+br.                                      (12)
```

The two minors divided by `(A_2z)(B_2z)` are respectively nonzero scalar
multiples of `R1,R3`, while

```text
F2=p(q-1)R1-(phi-1)R3.                              (13)
```

For deletion three, put

```text
F3=p e(q+1)+b r(phi+1),
S1=a(phi+1)-e,
S3=ap(q+1)+br.                                      (14)
```

Again the two normalized minors are nonzero scalar multiples of `S1,S3`, and

```text
F3=(phi+1)S3-p(q+1)S1.                              (15)
```

The second binary diagonal is `2F_d/r`.  Thus simultaneous rank drop of the
two selected minors forces `F_d=0`, hence `B_dz=0`, again contradicting (6).
Consequently the neighbouring mode-three one-marked map has rank four.

For the same logical reason as on the punctured lines, inspect the pure
mode-three one-marked map.  Its row `011`, column `d` entry is

```text
d=2: -2p(phi-1),          d=3: -2p(phi+1).          (16)
```

Both are nonzero in `K`.  The neighbouring rank-four condition first confines
the third target row to the deleted coordinate; (16) then kills that final
coefficient.  The third row would be globally zero, contradicting target rank
three.  This closes both endpoint fibres without dividing by `t`.

## Consequence and scope

For every genuine binary extension, equations (9)--(10) or (12)--(15) force
a neighbouring one-marked map to have rank four.  Since the third target row
vanishes on that binary hyperplane, injectivity confines it to the deleted
source coordinate.  The nonzero pure transverse entries (11) and (16) force
that remaining coefficient to vanish as well.  A globally zero third target
row contradicts the rank-three local map required by `H31`.  Together with
the exact projection (7), this proves

```text
generic marked H31 fibre(component 19)=empty.       (17)
```

Component nineteen's weighted `H22` fibre and every special/projective
component boundary remain open.

## Exact replay

```text
uv run --with sympy python \
  verify_p5_h31_common_kernel_vertical_triangle_component_generic_obstruction.py

python audit_p5_h31_common_kernel_vertical_triangle_component_generic_obstruction.py
```

The primary verifier reconstructs (1)--(4), checks all sixteen pure
coefficients, proves all four projection ideals in (7) in both directions,
rebuilds the complete four-dimensional mixed kernels on (8), and verifies
every determinant ratio, endpoint syzygy, and pure transverse entry in
(9)--(16) over characteristic zero.  The replay is a fixed-size exact symbolic
certificate, not a parameter search.  The independent no-import audit
exhausts every affine marking and every genuine residual extension at two
finite-field samples, verifies the kernel charts, minor identities, endpoint,
and pure transverse entries, and checks that the projective marking endpoint
is not a basis.  Those modular calculations corroborate but do not imply the
characteristic-zero theorem.
