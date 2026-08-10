# No-import verification of component 19 at `p=0`, `phi=+/-1`

```yaml
role: verifier
date_utc: 2026-08-01T16:55:29Z
git_commit: abf206ec29175b0df6dc5b5149efcb6790f3e9fa
claim_label: VERIFIED
scope: component 19 ordinary p=0,phi=e for e=+1,-1 over Q(q), with q*(q^2-1)!=0
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: fresh regular-basis permanents, direct finite/infinity incidence, complete shared kernel, exhaustive individual four-minors, and fixed full-target stacked minors
command: uv run --with sympy python claims/p5/h22/component19-p0-phi-endpoints-no-import/audit_p5_h22_component19_p0_phi_endpoints_no_import.py
outputs: replay stdout gives final path and sha256 pairs
limitations: ordinary phi endpoints on q*(q^2-1)!=0 only; q=0,+/-1, projectivized, valuative, closure, arbitrary-order, and global claims excluded
```

## Verdict

**VERIFIED on the frozen open.**  For each `e=+1,-1`, exactly two genuine
families survive every individual one-marked rank test.  Both fail the
necessary shared target-local condition by a fixed nonzero mode-one stacked
four-minor.

The audit does not read or import any construction-side `phi`-endpoint
artifact.  It reconstructs the component directly from
`P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md` and the regular `p=0`
basis.

## Parameter open and complete shared incidence

Fix `phi=e`, `e^2=1`, over `Q(q)`, and assume

```text
q*(q^2-1) != 0.                                   (1)
```

This already implies `q!=e`, `q!=-e`, and `e*q-1!=0`; the factors `q-e`
and `e*q-1=e*(q-e)` are redundant on (1).  The regular basis is

```text
(alpha0,beta0)=(Abar,Bbar+q*B),
(alpha1,beta1)=(B,A),
(alpha2,beta2)=(Bbar,A),
(alpha3,beta3)=(Abar,B+e*Bbar).
```

Its only pure coefficient is `T_1111=4*(q-e)`, which is nonzero on (1).

On the finite `D23` all-alpha open, the mixed equations force
`h0=h3=0`.  If `lambda!=1`, the two `D01` equations in `(C1,C2)` have
determinant `e*q-1`, forcing `C1=C2=0` and contradicting that open.  Hence
`lambda=1`.  The remaining equations give the complete shared branch

```text
h=(0,0,t,0),
C=(0,-H/(q-e),F/(q-e),0),
D=(X,Y,0,Z),

F=e*X+Z,
G=(q-e)*Y-t*F,
H=X+q*Z.
```

A fixed coefficient five-minor is `-1024*q*(q-e)^2`; the three displayed
parameter vectors lie in the kernel, proving completeness.  The diagonals
are

```text
B01=4*G,       A23=-4*F/(q-e),       B23=4*H,
```

so genuineness is exactly `F*G*H!=0`.

At shared orientation infinity, the same invertible two-equation system
occurs without the `lambda-1` factor.  It forces `C1=C2=0`, contradicting the
`D23` all-alpha open.  The infinity fibre is empty.

## Complete individual-rank survivor locus

The audit builds all eight full-target `8 x 5` one-marked maps and checks
every `4 x 4` minor.  Six maps have all four-minors identically zero.  The
only possibly rank-four maps are these.

For `D01`, mode three, every nonzero four-minor is, up to sign,

```text
M01=-64*X*(q^2-1)*L*G/(q-e)^2,
L=(e*q+1)*X+2*q*Z.                                (2)
```

For `D23`, mode two, all four-minors vanish after `Y=0`, while rows
`(0,2,3,7)`, columns `(0,1,2,4)` give

```text
M23=64*Y^2*H.                                     (3)
```

On the genuine locus and (1), equations (2)--(3) say that all individual
one-marked ranks are at most three exactly when

```text
Y=0,       X*L=0.
```

Thus the complete individual-rank survivor locus consists of precisely

```text
Family A: X=Y=0,                         Z*t!=0;

Family B: Y=0,
          Z=-(e*q+1)*X/(2*q),            X*t!=0.  (4)
```

The units in (1) make the inequalities in (4) exactly the remaining
`F*G*H!=0` conditions.

## Shared target-local obstruction

For a full target row `y=(y0,y1,y2,y3,y4)`, the two slice restrictions are

```text
rho01(y)=(y0+y1,y2,y3,y4),
rho23(y)=(y0,y1,y2+y3,y4).
```

Let `N01_i,N23_i` be the corresponding full-target one-marked maps.  A
common ternary target-local factorization requires

```text
rank stack(N01_i,N23_i) <= 3                      (5)
```

for every mode `i`.

Order both eight-row blocks by `000,...,111`, put `D01` first, and use target
columns `0,...,4`.  At mode one, stacked rows `(7,8,9,15)` and columns
`(0,1,2,3)` give, uniformly in `e`,

```text
Family A: -64*Z^4*q/(q-e)^2,
Family B:   4*X^4*(q-e)^2/q^3.                   (6)
```

Both are nonzero under (1) and (4).  Every survivor therefore has stacked
rank at least four at mode one and violates (5).  No genuine shared ternary
weighted-`H22` lift remains on the frozen open.

The excluded point `q=e` is the zero tensor and compatibility divisor.  At
`q=-e`, the factor `q^2-1` in (2) vanishes and the individual-rank survivor
locus enlarges, so that intersection is explicitly not claimed here.  The
lower-pair boundary `q=0`, all projectivized or valuative directions, closure,
arbitrary-order reduction, and the global conjecture remain outside scope.
