# Independent verification: component 19 `p=0`, `q*phi=1`

```yaml
role: verifier
date_utc: 2026-08-01T16:27:43Z
git_commit: 27e0d4beb3323a7496607c684726aa09dbfe02bb
claim_label: VERIFIED
scope: complete ordinary weighted-H22 obstruction at p=0, q*phi=1, phi^2!=1, including both genuine shared finite orientations and projective infinity
inputs:
  - P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md sha256=ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: independent specialized-basis reconstruction; exact shared-orientation elimination over Q(phi) with both D23 diagonals and required D01 pure diagonal inverted; complete kernel and fixed-minor obstruction; separate phi=+/-1 audit
command: uv run --with sympy python audit_p5_h22_component19_p0_qphi_equals_one.py
outputs:
  - audit_p5_h22_component19_p0_qphi_equals_one.py sha256=60c9be43261e5172a95b8dfb5cf36d07e21ee8c4a0582401a8d503317a66d640
  - P5_H22_COMPONENT19_P0_QPHI_ONE_INDEPENDENT_VERIFICATION.md
limitations: phi=+/-1 are zero lower-pair endpoints and remain outside the ordinary nonzero theorem; no arbitrary-order or global Krenn-Gu conclusion is made
```

## Verdict

The frozen `p=0`, `q*phi=1`, `phi^2!=1` weighted-`H22` obstruction is
**VERIFIED**.

An intermediate audit initially retained a `lambda=-1` component after
inverting only the two `D23` diagonals.  That was an incomplete genuineness
test: the required `D01` pure diagonal `B01` vanishes identically there.  After
also inverting `B01`, the exact projection contains only the claimed
`lambda=1` branch.  The earlier survivor/refutation interpretation is
withdrawn.

No `q*phi=1` construction, proof-B, or certificate artifact was inspected.

## Specialized ordinary geometry

Put `q=1/phi` and scale the ordinary mode-zero beta row by `phi`.  The regular
specialized basis satisfies

```text
beta0=beta3=B+phi*B_bar.
```

The only nonzero pure coefficient is

```text
T_1111=4(1-phi^2),
```

and the pair profile is

```text
(3,3,3,3,3,3)
```

on `phi^2!=1`.

## Exact genuine shared incidence

For each shared orientation, the audit imposes both mixed systems, normalizes
the chosen all-alpha diagonal, inverts its all-beta diagonal, and also inverts
the other required pure all-beta diagonal.  With that complete genuineness
saturation, the exact projected ideals are

```text
finite A01 orientation: (1),

finite A23 orientation:
<lambda-1,h3,h1,h0>,

infinity A01 orientation: (1),
infinity A23 orientation: (1).
```

Thus the only genuine shared finite branch is

```text
lambda=1, h=(0,0,t,0),
```

and all projective-infinity orientations are empty.

The apparent unsaturated component

```text
lambda=-1, h=0
```

has diagonals

```text
(A01,B01,A23,B23)=(0,0,4P/phi,-4phi*(C+E)).
```

Although it can be `D23`-binary, `B01=0` identically, so it is not a genuine
shared weighted-`H22` incidence and is correctly removed by the repaired
saturation.

## Complete kernel and fixed obstruction

Let `delta=phi^2-1`.  On the genuine finite branch the complete mixed kernel is

```text
z=C*vC+D*vD+E*vE,

vC=(0,1/delta,-phi/delta,0;1,0,0,0),
vD=(0,0,0,0;0,1,0,0),
vE=(0,1/delta,-phi/delta,0;0,0,0,1).
```

Rows `(2,9,10,12,15)` and columns `(0,1,2,3,6)` have determinant

```text
-1024*(phi^2-1)^2.
```

Hence the stacked matrix has rank five and the frame is complete.

Put

```text
S=C+E,
G=(phi^2-1)D+phi*t*S.
```

The diagonals `(A01,B01,A23,B23)` are exactly

```text
(0,-4G,4phi*S/(phi^2-1),4S),
```

so the genuine open is `S*G!=0`.

The fixed one-marked determinants are

```text
M0 = det(D01 mode 0, rows 1357)
   = -128*E*phi*S*G/(phi^2-1),

M3 = det(D01 mode 3, rows 4567)
   = -128*C*phi*S*G/(phi^2-1).
```

If both vanish on the genuine open, then `C=E=0`, contradicting `S!=0`.
An independent exact saturation by `S*G` returns the unit ideal.  Therefore
every genuine shared extension has a rank-four one-marked map and cannot lift
to weighted `H22`.

## Zero endpoints

At `phi=+1` and `phi=-1`, the pure coefficient is zero and the pair profile is

```text
(3,3,2,3,3,3).
```

They are zero lower-pair endpoints, not limits silently included in the
verified ordinary theorem.

## Replay

```powershell
uv run --with sympy python audit_p5_h22_component19_p0_qphi_equals_one.py
```

Expected final markers:

```text
P0_QPHI_ONE_FULL_OBSTRUCTION_VERIFIED
LAMBDA_MINUS_ONE_NONGENUINE_COMPONENT_DISCARDED
PHI_PLUS_MINUS_ONE_ZERO_ENDPOINTS_EXCLUDED
```
