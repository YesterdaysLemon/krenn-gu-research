# Marked-`H31` obstruction on component twenty-three's `k=infinity` boundary

## Status

**Exact characteristic-zero normalized-boundary theorem.**  On the omitted
`k=infinity` chart of component twenty-three, the complete marked-`H31`
fibre is empty on

```text
S=Q[r,1/((r-1)(r+1))].
```

This covers every marked basis, all four source-coordinate insertion
positions, and every projective extension direction.  It includes `r=0`,
where the boundary meets component thirteen.  The points `r=+1,-1` have a
rank-two pair and are outside the all-pair statement.

The theorem concerns the displayed normalized source chart.  It does not
cover arbitrary source or ambient changes, the distinct `s=0,rt=1` face,
other omitted component charts, arbitrary-order gluing, or the global
Krenn--Gu conjecture, which remains **UNRESOLVED**.

## Boundary rows and pair locus

Put

```text
A=(1,1,0,0),   C=(1,-1,0,0),
B=(0,0,1,1),   D=(0,0,1,-1).
```

On the reciprocal chart `q=1/k`, rescale the first row of plane one.  The
pure boundary is `q=0,t=r`, with rows

```text
alpha=(A,D,A-C+B+rD,-A-C+B+rD),
beta =(B,B+C,C,C).                                  (1)
```

All tensor coefficients vanish except `T1111=-4`.  In edge order
`01,02,03,12,13,23`, the pair profile over `Q(r)` is

```text
(3,3,3,4,4,3).                                     (2)
```

The gcd of the nonzero maximal minors on edge `23` is
`4(r-1)(r+1)`.  At either endpoint `r=+1,-1`, the profile is
`(3,3,3,4,4,2)`.  Thus (1) is all-pair precisely on the open used above.
The exact component-twenty-two change of basis from the weighted-`H22`
boundary theorem specializes at `r=0` to its equal-complement direction
`(A,R,D)=(-1,2,0)`, hence to the certified component-thirteen intersection.

## Complete marking and projective-extension incidence

Every marked basis with first row `alpha_i` has, after rescaling its second
row,

```text
beta_i(h)=beta_i+h_i alpha_i,       h_i in S.       (3)
```

There is no additional projective marking endpoint: the omitted point has
second row proportional to `alpha_i`, so it is not a basis.  For insertion
position `d`, delete source coordinate `d`, append the eight extension
entries

```text
z=(x0,x1,x2,x3;y0,y1,y2,y3)^T,
```

and let `M_d(h)` be the fourteen mixed rows and `a_d,b_d` the two diagonal
rows.  A genuine binary neighbour is a projective direction satisfying

```text
M_d(h)z=0,       (a_d z)(b_d z)!=0.                (4)
```

Because `a_d z!=0`, the normalization `a_d z=1` covers every projective
extension direction in (4).  Inverting `b_d z` and eliminating `(z,w)` over
`S` gives unit ideals for `d=2,3`.  For `d=0`, the projected ideal is exactly
the intersection of

```text
J00=<h0,h2,h3,       4r h1-r^2-3>,
J01=<h0,h2,2h3+1,    r h1-1>,                     (5)
```

and for `d=1` it is the intersection of

```text
J10=<h0,h3,h2,       4r h1-r^2-3>,
J11=<h0,h3,2h2+1,    r h1-1>.                     (6)
```

All ideals in (5)--(6) are taken in `S[h0,h1,h2,h3]`.  In particular each
branch forces `r` to be a unit.  Direct specialization to `r=0`, followed by
the same diagonal saturation, gives `<1>` for all four insertions.  Hence
the component-thirteen intersection has no affine marking with a genuine
binary neighbour, rather than being inferred by dividing by `r`.

## Uniform ternary obstruction on the four branches

Write `Delta=r^2-1`.  Each branch in (5)--(6) has `rank M_d=6`; the primary
replay supplies two displayed vectors spanning its complete mixed kernel.
Uniformity is certified by the following fixed six-by-six minors (mixed-row
and extension-column sets are zero based):

```text
branch   rows           columns       determinant
J00      0137(11)(13)   012346        -32 r^2 Delta^2
J01      0137(11)(13)   012345         128 r^2 Delta^2
J10      0137(11)(12)   012346          32 r^2 Delta^2
J11      0137(11)(12)   012345         128 r^2 Delta^2.          (7)
```

These are units on their respective branch bases, while the two displayed
kernel vectors force rank at most six.  Thus no unlisted special value of
`r` acquires extra extension directions.
For `z=p e0+w e1`, the diagonal values and a mode-zero one-marked minor are:

```text
branch   (a_d z,b_d z)                    rows   determinant

J00      (16r(p-w), -4w)                  0137   -r(a_d z)(b_d z)^2
J01      (4r(2p-w), -2w)                  0127   -(a_d z)^2(b_d z)/2
J10      (16r(p-w),  4w)                  0137    r(a_d z)(b_d z)^2
J11      (-4r(p-2w), 2p)                  0127    (a_d z)^2(b_d z)/2.   (8)
```

Every determinant in (8) is nonzero on the genuine-binary open (4).  Thus
the neighbouring one-marked map has rank four.  The pure mode-zero map has
the transverse entries

```text
d=0: -4r,          d=1: 4r.                       (9)
```

They too are nonzero on every branch.  The standard transverse-coordinate
argument now forces the third target row first to be supported only on the
deleted source coordinate and then, by (9), to vanish there as well.  This
contradicts the rank-three target map required by `H31`.

Combining (5)--(9), the direct `r=0` unit certificates, and the empty
`d=2,3` projections proves

```text
marked H31 fibre((1), r^2!=1)=empty.              (10)
```

## Replay

```powershell
uv run --with sympy python verify_p5_h31_common_center_kernel_star_component_k_infinity_all_pair_boundary_obstruction.py
uv run --with sympy python audit_p5_h31_common_center_kernel_star_component_k_infinity_all_pair_boundary_obstruction.py
```

The primary verifier performs the localized characteristic-zero
eliminations, checks both ideal inclusions in (5)--(6), verifies the four
complete kernel frames and determinant identities, and separately proves
the four `r=0` unit ideals.  The audit has no repository imports: it rebuilds
the permanent tensors, pair matrices, saturated projections, branch frames,
and one-marked maps independently over characteristic zero.  No finite-field
calculation is used.
