# Independent verification: component 19 ordinary `p=0` weighted-`H22` open

```yaml
role: verifier
date_utc: 2026-08-01T16:12:20Z
git_commit: 7a3eea50e311a163765750fa5f22f9d2b5c1b98e
claim_label: VERIFIED
scope: ordinary finite component-19 p=0 weighted-H22 obstruction on q*phi*(q-phi)*(q^2-1)*(phi^2-1)*((q*phi)^2-1)!=0, with finite and infinite weight charts
inputs:
  - P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md sha256=ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: independent regular-basis reconstruction; exact pair ranks; bidirectional shared-incidence elimination over Q(q,phi); complete 28x8 kernel frame; exact one-marked minors; function-field saturation and explicit linear-factor case certificate
command: uv run --with sympy python claims/p5/h22/component19-p0-ordinary-obstruction-open/audit_p5_h22_component19_p0_ordinary_obstruction_open.py
outputs:
  - audit_p5_h22_component19_p0_ordinary_obstruction_open.py sha256=a225c1f5e2c9a333448c95ffa999bebd4e685b9407fcfe488d798efdd8a73e75
  - P5_H22_COMPONENT19_P0_ORDINARY_OBSTRUCTION_OPEN_VERIFICATION.md
limitations: q=+/-1, phi=+/-1, q*phi=1, the genuine axes on q*phi=-1, and the zero/projective base q=phi remain UNKNOWN; q=0 and phi=0 are outside the all-pair-open component chart; no arbitrary-order or global Krenn-Gu conclusion is made
```

## Verdict

The frozen ordinary `p=0` weighted-`H22` obstruction-open theorem is
**VERIFIED** on

```text
q*phi*(q-phi)*(q^2-1)*(phi^2-1)*((q*phi)^2-1) != 0.
```

No `p=0` construction, candidate, proof-B, or certificate artifact was read,
imported, or executed.

## Regular pure basis and pair geometry

Use the regular mode-zero basis

```text
alpha0=A_bar,
beta0=B_bar+qB.
```

Together with the component theorem's unchanged modes 1--3, the only nonzero
restriction coefficient is

```text
T_1111=4(q-phi).
```

Thus this ordinary theorem requires `r=q-phi!=0`.  On `q*phi*r!=0`, every pair
has rank at least three.  Off `q*phi=1`, the profile is

```text
(3,3,4,3,3,3).
```

The fixed edge-`03` maximal minor is

```text
-8(q-phi)(phi*q-1).
```

On `q*phi=1`, with `q!=phi`, that edge drops to rank three and the profile is

```text
(3,3,3,3,3,3).
```

Fixed rank-three witnesses on edges `01,02,12,13,23` are respectively

```text
4q, -4, -4, -4, 4phi.
```

## Exact shared incidence

Both shared orientations were projected in the finite and projective-infinity
weight charts over `Q(q,phi)`, eliminating all eight extension coordinates and
the normalization/inverse variable.  Every equality was checked in both ideal
containment directions.

The exact results are

```text
finite, D01-normalized shared orientation: (1),

finite, D23-normalized shared orientation:
<lambda-1,h3,h1,h0>,

infinity, D01-normalized shared orientation: (1),
infinity, D23-normalized shared orientation: (1).
```

Hence the only generic shared finite marking branch is

```text
lambda=1, h=(0,0,t,0),
```

and the shared projective-infinity incidence is empty.

## Complete shared kernel

Write `r=q-phi` and order extensions as
`(x0,x1,x2,x3;y0,y1,y2,y3)`.  The stacked `28 x 8` mixed matrix on the shared
finite branch has kernel

```text
z=X*vX+Y*vY+Z*vZ,

vX=(0,-1/r,phi/r,0; 1,0,0,0),
vY=(0,0,0,0; 0,1,0,0),
vZ=(0,-q/r,1/r,0; 0,0,0,1).
```

Rows `(2,9,10,12,15)` and columns `(0,1,2,3,6)` have determinant

```text
-1024*q*r^2.
```

Therefore the mixed rank is five and this three-frame is complete on
`q*r!=0`, including `t=0`.

Put

```text
F=phi*X+Z,
G=rY-tF,
H=X+qZ.
```

The four diagonal forms `(A01,B01,A23,B23)` are exactly

```text
(0, 4G, -4F/r, 4H).
```

The complete nonforced/genuine open on this kernel is consequently

```text
F*G*H != 0.
```

## Complete fixed-minor obstruction

Two independently reconstructed one-marked determinants are

```text
M0 = det(D01 mode 0, rows 1357)
   = 64*Z*(phi^2-1)*(2phi*X+(phi*q+1)Z)*G/r^2,

M3 = det(D01 mode 3, rows 4567)
   = -64*X*(q^2-1)*((phi*q+1)X+2qZ)*G/r^2.
```

On the stated parameter open and `FGH!=0`, these two determinants cannot both
vanish.  Indeed, after removing required units, their equations are

```text
Z*(2phi*X+(phi*q+1)Z)=0,
X*((phi*q+1)X+2qZ)=0.
```

If `X=0` or `Z=0`, the other equation and `phi*q+1!=0` force both to vanish,
contradicting `F*H!=0`.  If `X*Z!=0`, the two remaining linear forms have
determinant

```text
-(phi*q-1)^2,
```

which is nonzero on the open.  Thus at least one one-marked map has rank four,
excluding a ternary weighted-`H22` lift.  A separate exact saturation by
`F*G*H` returns the unit ideal and corroborates this case certificate.

## Honest exceptional frontier

- `q=+/-1`: `M3` loses its fixed coefficient; UNKNOWN.
- `phi=+/-1`: `M0` loses its fixed coefficient; UNKNOWN.
- `q*phi=1`: the linear-form determinant vanishes and the shared incidence may
  specialize; UNKNOWN despite the ordinary pair profile remaining all-three.
- `q*phi=-1`: away from `X=0` and `Z=0`, the displayed minors still obstruct.
  On either axis, both selected minors vanish while `F,H,G` can remain nonzero;
  those genuine axis subloci are UNKNOWN.
- `q=phi`: the ordinary restriction is zero.  Its projectivized normal
  directions and valuative arcs are a separate problem; UNKNOWN here.
- `q=0` or `phi=0`: at least one pair drops below rank three, so these are not
  in the all-pair-open ordinary theorem.

No exceptional divisor is promoted by continuity from the verified open.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/component19-p0-ordinary-obstruction-open/audit_p5_h22_component19_p0_ordinary_obstruction_open.py
```

Expected final markers:

```text
P0_ORDINARY_H22_OPEN_VERIFIED
EXCEPTIONAL_AXES_STATUS_UNKNOWN
```
