# Independent verification: component 19 `p=0`, `q*phi=-1` axes

```yaml
role: verifier
date_utc: 2026-08-01T16:20:09Z
git_commit: 27e0d4beb3323a7496607c684726aa09dbfe02bb
claim_label: VERIFIED
scope: exact one-marked-rank classification of the genuine X=0 and Z=0 shared-extension axes at p=0, q=-1/phi, phi*(phi^2-1)*(phi^2+1)!=0; actual weighted-H22 existence on residual survivors remains UNKNOWN
inputs:
  - P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md sha256=ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: independent source reconstruction, exact shared-kernel replay, all eight one-marked maps on each axis, fixed rank-four obstruction minors, and exact maximal-rank witnesses on residual subloci
command: uv run --with sympy python audit_p5_h22_component19_p0_qphi_minus_one_axes.py
outputs:
  - audit_p5_h22_component19_p0_qphi_minus_one_axes.py sha256=9485634b18e9c50786b1ae1f5cbd7f06d3ae27bec3cf4052158a49210f546992
  - P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_AXES_VERIFICATION.md
limitations: the two Y=0 survivor subloci pass every one-marked rank condition but no ternary reconstruction or sufficiency theorem was checked; special phi^2=1 and zero-restriction phi^2=-1 points are excluded; special projective-weight incidence was not re-eliminated
```

## Verdict

The two genuine `q*phi=-1` axes are exactly classified by the complete
one-marked rank test.

- Every axis point with `Y!=0` is **VERIFIED obstructed**.
- Each axis has a residual `Y=0`, `t!=0` sublocus that is a **VERIFIED survivor
  of all eight one-marked rank conditions**.
- Existence of an actual weighted-`H22` lift on either residual survivor is
  **UNKNOWN**.

No construction or proof artifact was read or executed.

## Reconstructed frame and open

Set

```text
q=-1/phi,
r=q-phi=-(phi^2+1)/phi,
lambda=1,
h=(0,0,t,0).
```

The finite ordinary calculation requires

```text
phi*(phi^2-1)*(phi^2+1) != 0.
```

The last factor is `r!=0`; when `phi^2=-1`, one is back on the zero base
`q=phi`, not on the ordinary nonzero family.

The verified shared three-frame remains complete.  The fixed rank-five minor
specializes to

```text
1024*(phi^2+1)^2/phi^3.
```

With extension coordinates `(X,Y,Z)`, retain

```text
F=phi*X+Z,
G=rY-tF,
H=X-Z/phi.
```

The relevant open is `F*G*H!=0`.

## Axis `X=0`

Here

```text
F=Z,
H=-Z/phi,
G=rY-tZ,
```

so genuineness requires `Z!=0` and `G!=0`.

For generic `Y`, the exact mode-order rank profiles are

```text
D01 modes 0,1,2,3: (3,1,1,3),
D23 modes 0,1,2,3: (3,3,4,3).
```

The unique rank-four map is `D23` mode two.  Its row-`0127` determinant is

```text
64*Y*Z^2*phi/(phi^2+1).
```

It obstructs every genuine point with `Y!=0`.

On `Y=0`, the open becomes `Z*t!=0`.  The rank-four minor vanishes and the
complete profiles are

```text
D01: (3,1,1,3),
D23: (3,3,3,3).
```

The replay records a nonzero maximal-rank witness for every one of these eight
maps.  Representative witnesses include

```text
D01 mode 0: -16*Z^3*phi^2*t^2/(phi^2+1)^2,
D01 mode 3: -32*Z^2*t*(phi+1)/(phi*(phi^2+1)^2),
D23 mode 2:  16*Z^3*phi/(phi^2+1)^2.
```

Thus `X=Y=0`, `Z*t!=0` is an exact all-one-marked-ranks survivor.

## Axis `Z=0`

Here

```text
F=phi*X,
H=X,
G=rY-phi*tX,
```

so genuineness requires `X!=0` and `G!=0`.

The generic profiles are again

```text
D01: (3,1,1,3),
D23: (3,3,4,3).
```

The `D23` mode-two row-`0127` determinant is

```text
-64*X^2*Y*phi/(phi^2+1),
```

which obstructs every genuine point with `Y!=0`.

On `Y=0`, genuineness becomes `X*t!=0`, and the complete profiles become

```text
D01: (3,1,1,3),
D23: (3,3,3,3).
```

Again every rank is accompanied by an exact nonzero witness.  Representative
ones are

```text
D01 mode 0: -32*X^2*phi^4*t*(phi-1)/(phi^2+1)^2,
D01 mode 3: -16*X^3*phi^2*t^2/(phi^2+1)^2,
D23 mode 2:  16*X^3*phi^2/(phi^2+1)^2.
```

Thus `Z=Y=0`, `X*t!=0` is the second exact all-one-marked-ranks survivor.

## Boundary of the conclusion

Passing all eight rank tests is necessary but was not assumed sufficient for a
ternary weighted-`H22` reconstruction.  The two residual survivors are not
promoted to actual lifts.  Conversely, the `Y!=0` obstruction is complete on
both axes because the displayed rank-four determinant is forced nonzero by the
axis open.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/component19-p0-qphi-minus-one-axes/audit_p5_h22_component19_p0_qphi_minus_one_axes.py
```

Expected final markers:

```text
QPHI_MINUS_ONE_NONAXIS_OBSTRUCTION_VERIFIED
QPHI_MINUS_ONE_Y_ZERO_AXIS_SURVIVORS_VERIFIED
ACTUAL_WEIGHTED_H22_LIFT_STATUS_UNKNOWN
```
