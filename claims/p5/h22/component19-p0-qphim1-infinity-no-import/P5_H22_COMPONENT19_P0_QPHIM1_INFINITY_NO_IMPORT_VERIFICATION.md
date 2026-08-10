# No-import verification of the `p=0`, `q*phi=-1` infinity chart

```yaml
role: verifier
date_utc: 2026-08-01T17:04:12Z
git_commit: c15a3bb67d9aa130b95a9d6bffc994d1a26c379f
claim_label: VERIFIED
scope: component 19 ordinary p=0,q*phi=-1 shared weight-at-infinity chart on phi*(phi^2+1)!=0
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: fresh regular p0 basis, direct infinity contractions, saturated mixed-coefficient identity, and direct phi=+/-1 endpoint replay
command: uv run --with sympy python claims/p5/h22/component19-p0-qphim1-infinity-no-import/audit_p5_h22_component19_p0_qphim1_infinity_no_import.py
outputs: replay stdout gives final path and sha256 pairs
limitations: ordinary weight-at-infinity chart only; phi=0, phi^2=-1 zero tensor, finite weight, projectivized, valuative, closure, arbitrary-order, and global claims excluded
```

## Verdict

**VERIFIED empty.**  The shared weight-at-infinity chart has no genuine
binary incidence, hence no full target-local ternary weighted-`H22` lift.
This includes the ordinary points `phi=+1` and `phi=-1`.

The audit reads no new infinity construction artifact.  It reconstructs the
chart directly from `P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md`.

## Ordinary tensor and infinity contractions

Put `q=-1/phi` in the regular `p=0` basis

```text
(alpha0,beta0)=(Abar,Bbar-B/phi),
(alpha1,beta1)=(B,A),
(alpha2,beta2)=(Bbar,A),
(alpha3,beta3)=(Abar,B+phi*Bbar).
```

The only pure coefficient is

```text
T_1111=-4*(phi^2+1)/phi.
```

Thus `phi*(phi^2+1)!=0` is exactly the ordinary nonzero parameter open.
The shared weight-at-infinity restrictions of a full row
`y=(y0,y1,y2,y3,y4)` are

```text
rho01_infinity(y)=(y0,y2,y3,y4),
rho23_infinity(y)=(y0,y1,y2,y4).
```

The `D01` all-alpha diagonal is identically zero, so `D01` can only be the
pure side and `D23` must be binary.  Its required all-alpha diagonal is

```text
A23=-2*(C1+C2).                                   (1)
```

On the `A23` open, its adjacent mixed coefficients also force `h0=h3=0`,
but the contradiction below does not need those marking equations.

## Complete incidence obstruction

Two `D01` mixed coefficients are

```text
m1=T01_0001=-2*(phi*C1-C2),
m2=T01_1000= 2*(-C1-C2/phi).                      (2)
```

Their coefficient determinant in `(C1,C2)` is

```text
q*phi-1=-2,
```

a characteristic-zero unit.  Equivalently, after inverting the standing
unit `2*phi`, direct expansion gives the exact ideal identity

```text
A23=((1-phi)/(2*phi))*m1 + ((1+phi)/2)*m2.        (3)
```

Every mixed solution has `m1=m2=0`; equation (3) then gives `A23=0`,
contradicting the required binary diagonal.  Consequently the saturated
genuine shared incidence is empty.  There is no extension kernel on which
all required diagonals are nonzero.

At `phi=+1`, identity (3) specializes to `A23=m2`.  At `phi=-1`, it
specializes to `A23=-m1`.  Therefore neither ordinary endpoint is lost by a
division or generic-only argument.

## Target-local boundary

Full target-local compatibility is tested only after a genuine shared binary
incidence exists.  Here that incidence scheme is empty on the required
diagonal open, so there is no survivor whose stacked one-marked maps need a
rank test.  The target-local fibre is therefore empty for the stronger,
incidence-level reason above.

The excluded divisor `phi^2=-1` has `q=phi` and zero ordinary tensor.  Its
projectivized or transverse directions, `phi=0`, finite-weight charts,
valuative fibres, closure, arbitrary-order reduction, and the global
conjecture remain outside scope.
