# Component 19 `q*phi=-1` homogeneous weight-at-infinity obstruction - CANDIDATE

```yaml
role: construction
date_utc: 2026-08-01T17:11:13Z
git_commit: 17a4054ebe42316dd3c9f2bf8839c656520625ed
claim_label: CANDIDATE
scope: component 19 at p=0, q=-1/phi in the homogeneous weight [1:0] chart on phi*(phi^2+1)!=0, including phi=+/-1
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: direct denominator-free divisor reconstruction, exact mixed-coefficient syzygy, and bounded elimination audits
command: uv run --with sympy python claims/p5/h22/component19-p0-qphi-minus-one-weight-infinity/derive_p5_h22_component19_p0_qphi_minus_one_weight_infinity_obstruction_candidate.py
outputs:
  - P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_WEIGHT_INFINITY_OBSTRUCTION_CANDIDATE.md
  - p5_h22_component19_p0_qphi_minus_one_weight_infinity_certificate.json
  - derive_p5_h22_component19_p0_qphi_minus_one_weight_infinity_obstruction_candidate.py
limitations: construction result pending independent verification; only this homogeneous weight chart and parameter open are covered
```

## Frozen result

**CANDIDATE:** the genuine shared binary incidence in the homogeneous
weight-at-infinity chart is empty on

```text
p=0, q=-1/phi, phi*(phi^2+1)!=0.
```

Consequently there is no actual weighted-`H22` target compatibility to solve
in this chart: the shared extension already fails at the binary mixed stage.
This includes the crossings `phi=1` and `phi=-1`.

## Direct ordinary-open reconstruction

Use the four-coordinate rows

```text
A=(1,1,0,0),   Abar=(1,-1,0,0),
B=(0,0,1,1),   Bbar=(0,0,1,-1).
```

On `q=-1/phi`, take the regular plane bases

```text
alpha=(Abar, B, Bbar, Abar),
beta =(phi*Bbar-B, A, A, B+phi*Bbar).
```

The mode-zero beta row has been multiplied by `phi`; this is an invertible
basis change with determinant `phi` on the exact open, not a specialization
argument.  After replacing each `beta_i` by `beta_i+h_i*alpha_i`, the only
nonzero pure coefficient is

```text
T1111=-4*(phi^2+1).
```

Fixed square-free pair minors give profile `(3,3,4,3,3,3)` in pair order
`01,02,03,12,13,23`, with witnesses

```text
01: -4*phi
02: -4*phi
03: -16*phi*(phi^2+1)
12: -4
13:  4*phi
23:  4*phi.
```

Thus the exact ordinary all-pair-open condition is
`phi*(phi^2+1)!=0`; in particular, `phi=+/-1` is ordinary and must not be
discarded.

## Direct homogeneous-weight contractions

At homogeneous weight `[1:0]`, the two five-coordinate contraction rows are

```text
D01=(0,1,0,0,0),
D23=(0,0,0,1,0).
```

Let `x0,...,x3` be the alpha extension coordinates and `x4,...,x7` the beta
extension coordinates.  Direct permanent expansion gives the two desired
binary alpha diagonals and two `D01` mixed coefficients

```text
A01 = 0,
A23 = -2*(x1+x2),
m1 = coeff_D01(0001) = -2*(phi*x1-x2),
m2 = coeff_D01(1000) = -2*(phi*x1+x2).
```

The decisive identity is

```text
A23=((1-phi)/(2*phi))*m1+((1+phi)/(2*phi))*m2.
```

It is valid throughout `phi!=0`.  Therefore the shared `A01` orientation is
impossible because `A01` vanishes identically, while the shared `A23`
orientation is impossible because `A23` lies in the required `D01` mixed
ideal.  This contradiction precedes every beta-diagonal or ternary target
condition.

At the two crossings the same identity specializes directly to

```text
phi= 1: A23=m2,
phi=-1: A23=-m1.
```

No division by `phi^2-1` occurs.

## Bounded elimination audit

Independent of the displayed hand proof, exact elimination over `Q(phi)`
returns

```text
D01 binary incidence: <1>
D23 binary incidence: <h3,h0,h1*h2>
shared A01 incidence: <1>
shared A23 incidence: <1>.
```

A second audit over `Q[phi]`, saturated by
`phi*(phi^2+1)`, returns the unit ideal for both shared orientations.  The
standalone replay checks equality of each projected ideal in both directions.
These are small symbolic audits, not finite-field computations or a broad
search.

## Boundary

The conclusion is only for the homogeneous weight `[1:0]` chart on the stated
ordinary open.  The finite weight chart is not invoked as proof.  The points
`phi^2=-1` are zero-tensor points, and `phi=0` is unavailable under
`q=-1/phi`; other component boundaries, other components, the arbitrary-order
reduction, and the global Krenn-Gu conjecture remain outside scope.
