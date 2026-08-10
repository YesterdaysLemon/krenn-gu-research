# Component 19 zero base: valuative finite cover - CANDIDATE

```yaml
role: construction
date_utc: 2026-08-01T18:08:21Z
git_commit: a3d47ed7d9debeaa9ae55c225c71e39ddd6d0116
claim_label: CANDIDATE
scope: all characteristic-zero DVR/Puiseux arcs through component-19 Z0 inside the displayed finite component chart, with nonzero generic restriction and phi a unit
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  P5_H22_COMPONENT19_P0_FINITE_ORDINARY_AGGREGATE_VERIFICATION.md: ebb4bc46e06b99d4d21e0dff96a35fb071d48dfeceeb926cb4b2643fdeeddbc3
  P5_H22_COMPONENT19_Q_EQUALS_PHI_OBSTRUCTION_VERIFICATION.md: 77bad167798b52ca6d623ded47d346255023a13f4122f672ffc485dff9c70f50
  P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_VERIFICATION.md: 43e714b95f8a092bee9bf3b9259916a66bf7e8ae5984b63bf259d7e41aa4f440
method: exact p-chart blow-up rows, parameter-aware shared projections, complete diagonal/weight covers, explicit hidden-divisor and endpoint kernels, and fixed target-local minors
command: uv run --with sympy python claims/p5/h22/component19-zero-base-valuative-finite-cover/derive_p5_h22_component19_zero_base_valuative_finite_cover_candidate.py
outputs:
  - P5_H22_COMPONENT19_ZERO_BASE_VALUATIVE_FINITE_COVER_CANDIDATE.md
  - p5_h22_component19_zero_base_valuative_finite_cover_certificate.json
  - derive_p5_h22_component19_zero_base_valuative_finite_cover_candidate.py
limitations: construction result pending independent verification; no source/projective/ambient-chart, multi-parameter, arbitrary-local-map, local-to-global, or global claim
```

## Frozen result

**CANDIDATE:** no characteristic-zero one-parameter formal DVR or Puiseux arc
through the component-19 zero base `Z0={p=0,q=phi}`, with nonzero generic
restriction inside the displayed finite component chart and `phi` a unit,
admits the tested weighted-`H22` lift.

This is an exact fraction-field finite-cover argument.  It does not invoke
properness, specialize a generic result to a boundary, or use a finite-field
audit.  Every hypothetical formal lift supplies a point over its Laurent or
Puiseux fraction field; that field-valued point is eliminated in one of the
cases below.  Poles in markings, extension coordinates, inverse diagonals,
the homogeneous weight coordinate, and the blow-up ratio are therefore
allowed rather than silently excluded.

## Exact blow-up frame

Put

```text
d=q-phi,  p=z,  d=z*n.
```

For the original mode-zero rows

```text
v=Abar+pB,
u=Bbar+qB,
```

the determinant-one frame used throughout the `p!=0` chart is exactly

```text
alpha0 = u-n*v = Bbar+phi*B-n*Abar,
beta0  = v       = Abar+z*B.
```

No limit or first-order truncation is involved.  The markings are then added
as `beta_i -> beta_i+h_i*alpha_i` in all four modes.

## Exhaustive field-valued partition

Write `d=q-phi`.  A nonzero generic restriction falls into exactly one of:

1. `p=0,d!=0`: the verified `p=0` finite ordinary aggregate applies; near
   `Z0`, `q=phi+d` remains a unit.
2. `d=0,p!=0`: the verified `q=phi` divisor obstruction applies.
3. `p*d!=0,phi^2!=1`: use the exact `p=z,d=z*n` atlas below.
4. `p*d!=0,phi=+1` or `phi=-1`: use the two direct endpoint atlases below.

This partition is over the generic fraction field.  It therefore also covers
arbitrary ramification and unequal positive orders of `p` and `d`: the ratio
`n=d/p` may have any nonzero Laurent/Puiseux value.

## Parameter-aware shared projection atlas

Every genuine shared weighted-`H22` point lies in at least one of the four
diagonal opens

```text
(A01,B01,A23), (A01,B01,B23),
(A23,B23,A01), (A23,B23,B01).
```

The replay constructs both `D01` and `D23` mixed systems from the exact rows,
uses both homogeneous weight charts (`[lambda:1]` and `[1:0]`), normalizes one
chosen diagonal, and saturates the other two plus `z*n*phi`.  It performs the
eight characteristic-zero eliminations while retaining `h0,...,h3`, `n`,
`phi`, `z`, and finite `lambda`.

At weight infinity all four projected ideals are the unit ideal.  At finite
weight the first two opens are unit.  The reverse opens have exactly two
surviving projected branches:

```text
(A23,B23,A01):
  lambda=-1, h1=h2=h3=0, h0*n=1,
  n*phi*z+phi^2-1=0.

(A23,B23,B01):
  lambda=1, h1=h3=0, h0*n=1,
  h2 free.
```

The first branch is the hidden divisor `q*phi=1`; it would be missed by an
elimination performed only over the generic parameter function field.

## Target-local obstruction on the generic finite branches

On the `lambda=1` branch away from `phi^2=1`, the combined mixed matrix has
rank six.  A nonzero rank witness is

```text
4096*n*phi*z^2*(phi-1)*(phi+1).
```

Its kernel has basis

```text
(0,-1/z,phi/z,0; 1,0,0,0),
(0,0,0,0;        0,1,0,0).
```

For coefficients `C,D`, the genuine shared open is

```text
C*n*phi*(z*D-phi*h2*C) != 0.
```

On precisely that open, the fixed `D01`, mode-3, full one-marked map has the
nonzero minor

```text
-64*C*(z*D-phi*h2*C)^2/z.
```

On the hidden `q*phi=1`, `lambda=-1` branch, the combined mixed matrix has
rank five, witnessed by

```text
-1024*n*phi^3.
```

Its three displayed kernel vectors and diagonal formulas are replayed in the
certificate.  The genuine shared open is

```text
c0*n*(phi^2-1)*(c1*n*phi+c2) != 0,
```

and the fixed `D23`, mode-3, full one-marked map has the nonzero minor

```text
-64*c0^2*(c1*n*phi+c2)/phi^3.
```

Thus both surviving generic shared-projection branches are target-locally
obstructed.

## Endpoint atlases `phi=+/-1`

The endpoint computation is performed directly, not obtained by setting
`phi^2=1` in a localized generic certificate.  For each sign, the replay
checks

```text
2 homogeneous weight charts x 4 diagonal opens = 8 systems.
```

All infinity systems and the first three finite opens are unit.  The only
surviving shared projection has

```text
lambda=1, h1=h3=0, h0*n=1.
```

The combined mixed rank is five, with witness

```text
-1024*epsilon*n*z^2,  epsilon in {+1,-1}.
```

With kernel coefficients `X,Y,Z`, define

```text
F=X*n+epsilon*Z,
G=Y*n*z-epsilon*h2*F,
H=F+Z*n*z.
```

The genuine shared open is `F*G*H!=0`.  The fixed `D23`, mode-3, full
one-marked map has minor

```text
-64*F^2*H/(n^2*z^2),
```

so the endpoint branch is target-locally obstructed for both signs.

## Exact boundary

This candidate closes one-parameter characteristic-zero DVR/Puiseux arcs only
inside the displayed finite component chart, with a nonzero generic
restriction and `phi` a unit.  It does **not** cover multi-parameter arcs,
source/projective or omitted Grassmann charts, approaches through an ambient
component, `phi=0`, arbitrary local maps, the arbitrary-order local-to-global
reduction, or the global Krenn-Gu conjecture.  Those remain **UNKNOWN**.
