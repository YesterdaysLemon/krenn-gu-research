# Component 20 intrinsic zero diagonal-DVR atlas — VERIFIED

```yaml
role: construction
date_utc: 2026-08-01T14:43:55Z
git_commit: f997c8366b461f3952faef0d35b512318341909d
claim_label: VERIFIED
discovery_claim_label: CANDIDATE
scope: complete diagonal source-torus DVR/Puiseux atlas over (p,q)=(0,1),(-1,0)
inputs: recorded by SHA-256 in the replay output
method: exact Plucker limits, Z3 min-plus exhaustion, exact symbolic minors/permanents, Hall support
command: uv run --with sympy --with z3-solver python claims/p4/disputed-ownership/component20-intrinsic-boundary/zero-diagonal-dvr-atlas/derive_component20_intrinsic_zero_diagonal_dvr_atlas_candidate.py
outputs: this report, the JSON certificate, and the replay script
limitations: independently verified for diagonal arcs only; closure placement only; no arbitrary GL4 classification; global conjecture unresolved
```

## Frozen statement

At `(p,q)=(0,1)` put `u=p`, `v=q-1`; at `(-1,0)` put
`u=p+1`, `v=q`.  Let

`r=val(u)>0`, `s=val(v)>0`, `w=val(u-v)`, `h=min(r,s)`,

and act by

`D=diag(c0*t^x0,c1*t^x1,c2*t^x2,1)`, with `c0*c1*c2 != 0`.

For finite `r,s,w`, the normalized pure-tensor exponent is

`E=3*x0+x1+x2+z+a0-m0-m1-m2-m3`,

where

```
z  = min(x0,x1,x2)
a0 = min(r+x1,s+x2,w)
m0 = min(r+x0+x1,s+x0+x2,w+x0,x1+x2,x1,x2)
m1 = min(x0+x1,s+x0+x2,x0)
m2 = min(r+x0+x1,x0+x2,x0)
m3 = min(x0+x1,x0+x2).
```

At the second centre `m1,m2` are exchanged, leaving `E` unchanged.  Exact
real-linear Z3 queries on all four ultrametric branches and all three exact
axes prove, within this frozen model,

`E >= 0`, and `E=0` iff `x1=x2=0` and `x0<=-h`.

Thus every nonzero limit lies in exactly one of the two torus strata
`x0<-h` (interior) or `x0=-h` (wall).  The constant arc `u=v=0` has
identically zero restriction.

The tempting shortcut

`E_bad=x0+x1+x2+h-(m0+m1+m2+m3)`

is false: at `r=s=w=x0=1`, `x1=x2=0`, it gives `-1`, while the correct
formula gives `1`.

## Residue branches and leading planes

Write `A,B,C` for the last three source coordinates and `e=(1,0,0,0)`.
The four exhaustive residue branches and their distinguished row `K0` are:

| branch | residue condition | `K0` |
|---|---|---|
| `r<s` | `w=r`, leading residues `pi`; includes `v=0` | `pi*(C-c1*A)` |
| `s<r` | `w=s`, leading residues `theta`; includes `u=0` | `theta*(c2*B-C)` |
| equal, no cancellation | `r=s=w=h`, `pi*theta*(pi-theta)!=0` | `-pi*c1*A+theta*c2*B+(pi-theta)*C` |
| equal, higher cancellation | `r=s=h`, `pi=theta!=0`, `w>h`; includes `u=v` | `pi*(-c1*A+c2*B)` |

For every branch,

```
U1=<e,c1*A+C>,  U2=<e,c2*B+C>,  U3=<e,c1*A+c2*B>.
```

In the interior `U0=<e,K0>`.  On the wall, in Plucker order
`01,02,03,12,13,23`, the exact raw `U0` coordinates are

```
r<s:                (-pi*c0*c1, 0,              pi*c0,         -c1*c2, c1, -c2)
s<r:                (0,           theta*c0*c2,  -theta*c0,     -c1*c2, c1, -c2)
equal no cancel:    (-pi*c0*c1, theta*c0*c2, (pi-theta)*c0,    -c1*c2, c1, -c2)
equal higher:       (-pi*c0*c1, pi*c0*c2,       0,              -c1*c2, c1, -c2).
```

The four pure Segre rows are pointwise `(K0,e,e,e)`.  Only the `1111`
coefficient is nonzero.  The replay checks the exact coefficient and every
pair rank by explicit minors.

## Complete 16-chart machine atlas

The JSON certificate fixes the chart order and expected pair profiles; the
replay emits each chart with raw `U0`, both rows of every leading plane, pure
kernel rows, pure-tensor support, exact rank witnesses, and placement.  In pair
order `(01,02,03,12,13,23)`, the eight profiles at `(0,1)` are:

| branch | interior | wall |
|---|---|---|
| `r<s` | `(2,3,3,3,3,3)` | `(3,4,4,3,3,3)` |
| `s<r` | `(3,2,3,3,3,3)` | `(4,3,4,3,3,3)` |
| equal no cancel | `(3,3,3,3,3,3)` | `(4,4,4,3,3,3)` |
| equal higher | `(3,3,2,3,3,3)` | `(4,4,3,3,3,3)` |

The other eight charts follow by source `diag(1,-1,-1,1)` and swapping modes
1 and 2.  Equivalently, profiles exchange `01<->02` and `13<->23`, while

`(a,b,c,d,e,f) -> (-a,-b,c,d,-e,-f)`

on raw `U0` Plucker coordinates.  This is an exact centre isomorphism, not a
numerical resemblance.

For the equal/no-cancellation interior chart, a naive `03` rank witness can
contain the accidental factor `(pi+theta)`.  The replay instead uses rows
`(0,2,3)`, columns `(1,2,3)`, whose determinant is

`-c1^2*c2*(pi-theta)^2`.

Hence there is no hidden rank drop at `pi+theta=0`.

## Placement and pointwise H31/H22 boundary

All charts remain in the component-20 closure by construction.

- Every interior chart has `e in U0`, hence lies in the component-18
  common-singleton closure.  The `r<s`, `s<r`, and equal/higher-cancellation
  interiors also have a rank-2 support-one pair and lie in the component-15
  support-one-secant closure.  The equal/no-cancellation interior is only
  certified here for components 20 and 18.
- Every wall chart has `e notin U0`; all pair ranks are at least 3, while
  modes 1,2,3 have common kernel `e` and their three mutual pair matrices have
  rank 3 with the unique `e*e` relation.  These lie in the component-16
  directed-triangle closure, not the component-18 common-singleton family.

The component labels are not used in the obstruction.  Pointwise, the pure
rows are `(K0,e,e,e)`.  After any H31 deletion and extension, the three `e`
rows occupy at most two columns, so Hall's condition kills the all-alpha
diagonal for every deletion, marking, source unit, residue, and extension.
The same three rows occupy at most two columns under both weighted H22 maps
`D01` and `D23`, including all homogeneous weights and endpoints.  Therefore
no displayed chart has an H31 binary neighbour, and neither H22 direction can
be binary.

The construction was independently reconstructed and is now `VERIFIED` in
this diagonal scope; its discovery label remains `CANDIDATE`.  This is not a
classification of arbitrary source changes and not a solution of the global
Krenn-Gu conjecture.  See
[`COMPONENT20_INTRINSIC_ZERO_DIAGONAL_DVR_ATLAS_VERIFICATION.md`](COMPONENT20_INTRINSIC_ZERO_DIAGONAL_DVR_ATLAS_VERIFICATION.md).
