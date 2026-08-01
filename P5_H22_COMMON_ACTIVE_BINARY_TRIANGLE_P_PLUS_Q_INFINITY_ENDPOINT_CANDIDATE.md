# Candidate weighted-`H22` analysis on the two component-14 infinity endpoints

## Status and frozen scope

**CANDIDATE.**  This note directly reconstructs the homogeneous projective
weighted directions on the two component-14 faces at `y=-r` in the verified
diagonal-DVR `p+q=0` boundary classification.  It does not specialize the
generic component-14 `H22` theorem.

The on-wall face is obstructed by exact characteristic-zero certificates.
The off-wall face retains an explicit finite--finite binary candidate passing
every individual one-marked rank test performed here.  That surviving pair is
not promoted to an `H22` lift: the remaining two-neighbour compatibility has
not been proved.

No finite-field computation, parameter grid, broad minor scan, non-diagonal
source change, arbitrary-order gluing, or global Krenn--Gu claim is used.

## Direct endpoint planes and homogeneous directions

Use the verified endpoint normalization

```text
e=(1,0,0,0), w=(0,1,1,1), u=(0,1,-1,0),
v1=(0,1,1,0), v2=(0,0,0,1),

alpha=(e,e,-u,2v2-v1),
beta =(w,w,e,gamma e+v1),
```

with `gamma=0` off the wall and `gamma=2` on the wall.  In both orientations
the only squarefree pure coefficient is `T_1111=4`.

For homogeneous weights `[rho:sigma]`, reconstruct

```text
D01^[rho:sigma](z,x)=(rho z0+sigma z1,z2,z3,x),
D23^[rho:sigma](z,x)=(z0,z1,rho z2+sigma z3,x).
```

Finite slope is `[r:1]`; infinity is `[1:0]`.  For every marking
`beta_i(h)=beta_i+h_i alpha_i`, the verifier builds all fourteen mixed rows
and the two binary diagonals `A,B` directly.

## Exact projective marking images

Bidirectional elimination of the normalized incidence

```text
<M(h,r)z,A z-1,w B z-1>
```

gives the following complete projection closures.

For `gamma=0`:

```text
J01^finite=J01^infinity=J23^finite=<h3,h2,h0 h1>,
J23^infinity=<1>.
```

For `gamma=2`:

```text
J01^finite=J23^finite=<h3,h2,h0 h1>,
J01^infinity=<h3,h2,h0+h1,h1^2>,
J23^infinity=<1>.
```

Keeping the finite slope rather than eliminating it produces the same ideals;
there is no hidden slope--marking equation.  Thus every finite actual marking
is on one of the two axes

```text
h=(T,0,0,0), or h=(0,T,0,0),
```

while `gamma=2,D01` infinity is supported only at the origin.  The two axes
are exchanged by the exact `U0<->U1` symmetry together with
`(z0 z1)(z4 z5)`.

## On-wall face: complete `D01` obstruction

It suffices to use `h=(T,0,0,0)` and marked mode zero; the other axis is its
mode-swapped copy.  At finite slope `r`, away from the direct special fibres,
the mixed matrix has rank seven and a complete kernel line.  For a compatible
coordinate `X`,

```text
A=-2X r/(Tr+1),
B= 2X(2r+1).
```

The rank-seven witness is `64 r^6(Tr+1)`.  Direct rebuilds, rather than the
displayed quotient, give

```text
r=0:       A|ker=0,
r=-1/2:    B|ker=0,
Tr+1=0:    B|ker=0.
```

These include all intersections of the special divisors.  On the genuine
open, fixed mode-axis minors give

```text
T!=0, rows 0457:
  -16 T X^3 r^2(2r+1)/(Tr+1)^2,

T=0, rows 0567:
  -8 X^3 r(2r+1).
```

Hence every genuine finite `D01` extension has marked rank four.

At `D01` infinity, direct reconstruction at the origin has mixed rank six and
complete frame

```text
(-1,-1, 2, 2;-2,-2,1,0),
( 0, 0,-1,-1; 1, 1,0,1).
```

Writing the extension as `Xv0+Yv1` gives

```text
A=-4X, B=4Y,
det N2[0127]=-32X^2Y.
```

Thus infinity is also rank-four obstructed on `A B!=0`.  Since `D23`
infinity has empty projection, every projective pair uses one of these
obstructed `D01` directions.  The on-wall weighted-`H22` fibre is therefore
empty, still labelled `CANDIDATE` pending a separate verifier.

## Off-wall face: direct infinity obstruction

At `D01` infinity, each marking axis has mixed rank six.  On the `h0` axis a
complete frame is

```text
v0=(-1,-1,0,-2T;2T,T,1,0),
v1=( 0, 0,-1, -1; 1,1,0,1).
```

For `z=Xv0+Yv1`,

```text
A=-4X,
B=4(TX+Y),
det N2[0127]=-32X^2(TX+Y).
```

The `h1` axis is the exact mode swap.  Hence no genuine infinite `D01`
extension survives.  Again `D23` infinity has empty projection.

## Off-wall finite `D01` survivor

For finite slope `s`, the `h0`-axis mixed matrix has rank seven on `s!=0`;
the fixed witness is `-16s^6`.  Its complete kernel is

```text
k=(-1,-1,0,-2T;2T,T,1,0).
```

For `z=Ck`,

```text
A=-4Cs, B=4C(Ts+1).
```

At `s=0`, a direct rank-one rebuild has `A|ker=0`; at `Ts+1=0`, the complete
rank-seven kernel has `B|ker=0`.  Every genuine point therefore satisfies

```text
C s(Ts+1) != 0.
```

The corresponding mode-zero one-marked map has rank exactly three throughout
this genuine family.  It is not individually obstructed.

## Off-wall finite `D23` factor cover

For the same marking axis, the generic finite-`D23` mixed matrix has rank six.
A fixed rank witness is

```text
-4(2r-1)^2(2r+1)(4r+1).
```

On its ordinary kernel chart `z=Xv0+Yv1`, direct substitution and the fixed
mode-zero rows `0167` give

```text
A=4X,
B=4(r+1)[T X(2r+1)+Y(r+1)]/(4r+1),

det N0[0167]
 =32XY r(r+1)(2r-1)[T X(2r+1)+Y(r+1)]
   /[(2r+1)(4r+1)].
```

Outside the displayed rank-witness divisors, every genuine point is rank four
unless `Y=0`, `r=0`, or `r=1/2`.  Direct kernels on those divisors give the
complete surviving set:

```text
r=0:        every genuine kernel point has marked rank 3;
r=1/2:      every genuine kernel point has marked rank 3;
ordinary r: Y=0 survives exactly when T!=0 and B!=0;
r=-1/4:     T!=0 is rank-4 obstructed, while T=0 is rank 3;
r=-1/2,-1: no genuine neighbour because B|ker=0.
```

The direct `r=-1/4,T!=0` minor is `-9XY^2/T` in its complete local frame;
at `T=0` the rebuilt frame has `A=4Y,B=X` and marked rank three.  These direct
checks retain, rather than divide by, every exceptional slope.

## Complete surviving binary pair

A particularly simple survivor exists over every off-wall marking on either
axis.  On `h=(T,0,0,0)`, choose

```text
D01 finite:
  slope s, extension Ck,
  C s(Ts+1)!=0;

D23 finite at r=0:
  extension U f0+V f1,

  f0=(-1,-1,0,-2T;2T,T,1,0),
  f1=( 0, 0,1, -1; 1,1,0,1),

  A23=4U, B23=4(TU+V),
  U(TU+V)!=0.
```

Both complete mixed kernels and both diagonals are nonzero under the displayed
conditions.  Their relevant one-marked maps have rank exactly three.  The
mode-swapped formulas give the complete partner on the `h1` axis.

This is a complete machine-readable **binary candidate certificate**, not a
ternary `H22` certificate.  A future proof must either construct the common
two-neighbour lift or find an additional stacked/transverse compatibility
obstruction.  No such step is claimed here.

## Retained failures and boundary

- The generic component-14 proof is not specialized: its endpoint gauge and
  resultant ratios degenerate at `S=0`.
- A preliminary check of only rows `0147`, `0457`, and `0127` on the off-wall
  finite `D01` map returned zero.  Rebuilding the entire map showed rank three;
  those zero determinants are retained as a genuine survivor, not discarded.
- No computation timed out.  No finite-field result contributes evidence.
- The off-wall face remains unresolved after the one-marked tests.

## Exact replay

```text
uv run --with sympy python \
  derive_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_candidate.py
```

The command emits the full proof-b run report with UTC date, commit, exact
input/output SHA-256 hashes, method, command, limitations, all projection
certificates, special fibres, and the surviving candidate frames.
