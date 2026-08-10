# Component 19 ordinary `p=0, phi=+/-1` weighted-`H22` obstruction — CANDIDATE

```yaml
role: construction
date_utc: 2026-08-01T16:53:36Z
git_commit: 565e1a39cf34228c8bf3fe598eab9485720c175d
claim_label: CANDIDATE
scope: component 19 finite ordinary p=0, phi in {+1,-1}, q*(q^2-1)!=0
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md: 7d817f91a5a24512e092dca125258ad5a3753bbb97b6199ad2b6c202c9d91965
method: direct sign-specialized finite incidence elimination, exact shared frame, complete individual one-marked classification, full two-contraction stacks, and third-colour diagonal obstruction
command: uv run --with sympy python claims/p5/h22/component19-p0-phi-pm-one-ordinary/derive_p5_h22_component19_p0_phi_pm_one_ordinary_obstruction_candidate.py
outputs: this report, its JSON certificate, and the bounded standalone replay
limitations: construction result pending independent verification; finite projective-weight chart only; all listed parameter intersections excluded
```

## Frozen result

For each `s=+1,-1`, the component-19 weighted-`H22` fibre is **CANDIDATE
empty** on

```text
p=0,  phi=s,  q*(q^2-1)!=0.                       (1)
```

This is exactly the requested ordinary open.  When `phi=+/-1`, the excluded
conditions `q=phi`, `q=+/-1`, and `q*phi=+/-1` are all contained in
`q^2=1`; `q=0` is the remaining excluded intersection.

## Ordinary tensor and pair profile

Use the regular basis

```text
alpha=(Abar,B,Bbar,Abar),
beta =(Bbar+qB,A,A,B+s Bbar).
```

The only pure coefficient is

`T1111=4(q-s)`.

On (1), the exact pair profile is `(3,3,4,3,3,3)`.  The edge-`03`
rank-four witness is

`-8*s*(q-s)^2`.

Thus no ordinary zero or pair-rank boundary is silently included.

## Complete finite shared incidence

The four normalized incidence systems are reconstructed independently for
both signs over `Q(q)`.  Each sign gives exactly

```text
D01 binary:   <1>
D23 binary:   <h3,h0,h1*h2>
shared A01:   <1>
shared A23:   <lambda-1,h3,h1,h0>.
```

Therefore the complete finite shared branch is

```text
[lambda:1]=[1:1],  h=(0,0,t,0).                   (2)
```

Put `r=q-s`.  Its combined mixed matrix has rank five, with fixed determinant

`-1024*q*r^2`.

The complete kernel is

```text
vX=(0,-1/r,s/r,0; 1,0,0,0),
vY=(0,0,0,0;       0,1,0,0),
vZ=(0,-q/r,1/r,0;  0,0,0,1).
```

For `z=XvX+YvY+ZvZ`, define

```text
F=sX+Z,
G=rY-tF,
H=X+qZ.
```

The binary diagonals are

```text
A01=0,  B01=4G,
A23=-4F/r,  B23=4H,
```

so the exact genuine condition is `F*G*H!=0`.

## Complete individual one-marked survivor locus

Two fixed projected minors are

```text
D23 mode 2, rows 0237:  64*Y^2*H,
D01 mode 3, rows 4567:
  -64*X*(q^2-1)*((s*q+1)X+2qZ)*G/r^2.
```

On the genuine open (1), rank at most three in every individual map first
forces `Y=0`; then `G=-tF` forces `t!=0`.  The second minor gives the exact
union

```text
Axis: X=Y=0, Z*t!=0;
Line: Y=0, (s*q+1)X+2qZ=0, X*t!=0.                (3)
```

Direct substitution proves sufficiency for the individual rank conditions.
On both pieces, for either sign, the mode-order profiles are

```text
D01: (3,1,1,3),
D23: (3,3,3,3).
```

## Full target-local compatibility

Use the full five-coordinate contraction rows

```text
q01=(1,1,0,0,0),
q23=(0,0,1,1,0).
```

### The line

Parameterize the line in (3) by

```text
X=2qK,  Y=0,  Z=-(s*q+1)K.
```

At mode three, stack the full `D01` and `D23` one-third-row maps.  Rows
`(5,6,7,8,14)` and all five columns have determinant

```text
-512*s*K^4*q^2*t*(q^2-1).                         (4)
```

It is nonzero everywhere on (1), including the formerly suspicious point
`q=-2s`.  Hence the line has no shared third target row at mode three.

### The axis

On `z=K vZ`, every full `D01/D23` stack has rank exactly four.  The replay
records a nonzero fixed four-minor and a complete one-dimensional kernel for
each mode and each sign.

However, all four kernel generators satisfy

```text
gamma_i[0]=gamma_i[1]=0.                           (5)
```

The normalized `H22` colours identify `alpha=E1`, `beta=E2`, and the missing
row `gamma=E0`.  The `D01` contraction must have nonzero `E0^4` coefficient
`lambda0`.  Equation (5) gives directly

```text
per(q01,gamma0,gamma1,gamma2,gamma3)=0,            (6)
```

because four gamma rows occupy only coordinates `2,3,4`.  Thus the axis
passes every individual and stacked rank test but fails the required third
colour diagonal.  It is not an actual `H22` lift.

Equations (4) and (6) exhaust (3), proving the candidate obstruction on the
whole finite open (1).  No finite-field inference or broad parameter search
is used.  Projective weights, `q=0`, `q=+/-1`, other component boundaries,
arbitrary-order reduction, and the global Krenn--Gu conjecture remain outside
scope.
