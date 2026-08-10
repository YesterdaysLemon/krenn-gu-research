# No-import verification of component 19 at `p=0`, `q=+/-1`

```yaml
role: verifier
date_utc: 2026-08-01T16:46:17Z
git_commit: a4adfabf5247c3489544558fd45d7ee62c40b53c
claim_label: VERIFIED
scope: component 19 ordinary p=0,q=e for e=+1,-1 over Q(phi), with phi*(phi^2-1)!=0
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: fresh regular-basis permanents, direct finite/infinity compatibility, complete shared kernel, exhaustive individual four-minors, and fixed full-target stacked minors
command: uv run --with sympy python audit_p5_h22_component19_p0_q_endpoints_no_import.py
outputs: replay stdout gives final path and sha256 pairs
limitations: ordinary q endpoints only; phi=0,+/-1, projectivized, valuative, closure, arbitrary-order, and global claims excluded
```

## Verdict

**VERIFIED.**  For each `e=+1,-1`, exactly two genuine families survive all
individual one-marked rank tests.  Both fail the necessary shared
target-local condition by a fixed nonzero mode-one stacked four-minor.

The audit neither reads nor imports
`explore_p5_h22_component19_p0_q_endpoints.py` or its candidate report.  It
reconstructs the component from
`P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md` and the displayed regular
`p=0` basis.

## Complete shared branch

Fix `q=e`, where `e^2=1`, and assume `phi*(phi^2-1)!=0`.  Then
`e*phi-1!=0`.  In the regular basis

```text
(alpha0,beta0)=(Abar,Bbar+e*B),
(alpha1,beta1)=(B,A),
(alpha2,beta2)=(Bbar,A),
(alpha3,beta3)=(Abar,B+phi*Bbar),
```

the only ordinary pure coefficient is `T_1111=4*(e-phi)`, so it is nonzero.

On the finite `D23` all-alpha open, the mixed equations force
`h0=h3=0`.  If `lambda!=1`, the two `D01` equations have coefficient
determinant `e*phi-1` in `(C1,C2)`, forcing `C1=C2=0` and contradicting that
open.  Thus `lambda=1`.  The remaining equations give

```text
h=(0,0,t,0),
C=(0,-H/(e-phi),F/(e-phi),0),
D=(X,Y,0,Z),

F=phi*X+Z,
G=(e-phi)*Y-t*F,
H=X+e*Z.
```

A fixed coefficient five-minor is `-1024*e*(e-phi)^2`; the three displayed
parameter vectors lie in the kernel, proving that this is the complete
three-dimensional shared extension kernel.  The surviving diagonals are

```text
B01=4*G,       A23=-4*F/(e-phi),       B23=4*H,
```

so genuineness is exactly `F*G*H!=0`.

At shared orientation infinity, the same two `D01` equations occur without
the `lambda-1` factor.  Since `e*phi-1!=0`, they force `C1=C2=0`, contradicting
the `D23` all-alpha open.  The infinity fibre is empty.

## Complete individual-rank survivor locus

The audit builds all eight full-target `8 x 5` one-marked maps and checks
every `4 x 4` minor.  Six maps have every four-minor identically zero.  The
only two that can have rank four are as follows.

For `D01`, mode zero, all nonzero four-minors are equal up to sign to

```text
M01=64*Z*(phi^2-1)*L*G/(e-phi)^2,
L=2*phi*X+(e*phi+1)*Z.                            (1)
```

For `D23`, mode two, every four-minor vanishes after `Y=0`, while the fixed
rows `(0,2,3,7)`, columns `(0,1,2,4)` minor is

```text
M23=64*Y^2*H.                                     (2)
```

On the genuine locus, (2) forces `Y=0`; conversely this kills every `D23`
mode-two four-minor.  Equation (1) then forces `Z*L=0`.  Therefore the
complete individual-rank survivor locus has exactly two genuine families:

```text
Family A: Y=Z=0,                         X*t!=0;

Family B: Y=0,
          X=-(e*phi+1)*Z/(2*phi),        Z*t!=0.   (3)
```

The standing parameter units ensure that the displayed inequalities in (3)
are precisely the remaining `F*G*H!=0` conditions.

## Shared target-local obstruction

For a full target row `y=(y0,y1,y2,y3,y4)`, the two restrictions are

```text
rho01(y)=(y0+y1,y2,y3,y4),
rho23(y)=(y0,y1,y2+y3,y4).
```

Let `N01_i,N23_i` be the corresponding full-target one-marked maps at mode
`i`.  A common ternary target-local factorization requires their two row
spaces to lie in one space of dimension at most three, equivalently

```text
rank stack(N01_i,N23_i) <= 3                      (4)
```

for every mode.

Order each eight-row block by `000,...,111`, put `D01` first, and use target
columns `0,...,4`.  At mode one, stacked rows `(7,8,9,15)` and columns
`(0,1,2,3)` give, uniformly in `e`,

```text
Family A: -64*X^4*phi^3/(phi-e)^2,
Family B:   4*Z^4*(phi-e)^2/phi.                  (5)
```

Both are nonzero under (3) and `phi*(phi^2-1)!=0`.  Hence both complete
individual-rank survivor families have stacked rank at least four and violate
(4).  No genuine shared ternary weighted-`H22` lift survives at either
ordinary `q` endpoint.

This verifies only the frozen endpoint claim.  The excluded parameter
intersections, projectivized or transverse limits, valuative fibres, closure,
arbitrary-order reduction, and the global conjecture remain outside scope.
