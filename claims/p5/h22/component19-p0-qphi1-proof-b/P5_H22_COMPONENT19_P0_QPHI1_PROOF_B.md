# Component 19 ordinary `p=0`, `q*phi=1` proof B

```yaml
role: proof_b
date_utc: 2026-08-01T16:23:09Z
git_commit: 27e0d4beb3323a7496607c684726aa09dbfe02bb
claim_label: VERIFIED
discovery_claim_label: DERIVED
scope: ordinary component-19 p=0 fibre on q*phi=1 and phi^2!=1
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  derive_p5_h22_component19_p0_ordinary_open_proof_b.py: 098e7f3ed19999f8e2445125ae4d5413eca2049c150845b734f8ac508c75f311
method: regular p0 basis, exact finite/infinity contractions, complete linear kernels, and fixed one-marked minors
command: uv run --with sympy python claims/p5/h22/component19-p0-qphi1-proof-b/derive_p5_h22_component19_p0_qphi1_proof_b.py
outputs: replay stdout gives final path and sha256 pairs
limitations: ordinary fibre only; phi=+/-1 zero endpoints and projectivized directions are excluded; no valuative, closure, arbitrary-order, or global claim
```

## Result

Put `q=1/phi` and assume `phi^2!=1`.  The ordinary restricted tensor is
nonzero, all six pair-product maps have rank three, and the weighted `H22`
fibre is empty.  This is a parameter-divisor theorem, not a closure theorem.

No construction-agent compatibility-divisor artifact was inspected.

## Regular ordinary chart

At `p=0` use the nonsingular intrinsic bases

```text
(alpha0,beta0)=(Abar,Bbar+B/phi),
(alpha1,beta1)=(B,A),
(alpha2,beta2)=(Bbar,A),
(alpha3,beta3)=(Abar,B+phi*Bbar).
```

The only nonzero pure coefficient is

```text
T_1111=4*(1/phi-phi).
```

Thus the tensor is ordinary and nonzero precisely away from the retained
endpoints `phi^2=1`.  Fixed three-minors, together with vanishing of every
four-minor, give pair profile `(3,3,3,3,3,3)`.

## Shared-orientation classification

Write a finite common orientation as `[lambda:1]`.  Since the `D01`
all-alpha coefficient vanishes identically, `D23` must be the binary side.
On its all-alpha open, the `0001` and `1000` equations force
`h0=h3=0`.

If `lambda!=1`, the two first `D01` mixed equations force
`C2=phi*C1`.  The `D23` all-alpha coefficient is then

```text
-2*C1*((phi+1)*lambda+phi-1),
```

so `C1` and the displayed linear factor are nonzero.  Two further `D01`
equations, after removing the common `lambda+1`, are

```text
C1*(phi^2-1)-phi*D0-D3=0,
C1*(phi^2-1)+phi*D0+D3=0.
```

They contradict `C1*(phi^2-1)!=0` unless `lambda=-1`.  At `lambda=-1`
the remaining equations force

```text
h=(0,0,0,0),
C=(0,c,phi*c,0),
D=(u,0,0,v).
```

This is the complete three-dimensional extension kernel, but its `D01`
all-beta coefficient is zero.  Hence it is not a genuine weighted `H22`
point.

The only finite genuine candidate orientation is therefore `lambda=1`.
The complete equations give

```text
h=(0,0,t,0),
C=(0,c,-phi*c,0),
D=(u,v,0,c*(phi^2-1)-phi*u).
```

A fixed rank-five coefficient minor is

```text
-1024*(phi-1)^2*(phi+1)^2/phi^3,
```

and the three displayed parameter vectors lie in the kernel, proving
completeness.  The three surviving diagonal coefficients are

```text
B01=-4*(phi^2-1)*(phi*c*t+v)/phi,
A23=4*phi*c,
B23=4*c*(phi^2-1)/phi.
```

Consequently genuineness is exactly `c*G!=0`, where `G=phi*c*t+v`.

At the shared infinity orientation, the same all-alpha open forces
`C2=phi*C1` and `C1!=0`.  The two displayed opposite-sign equations occur
without a `lambda+1` factor, immediately contradicting `phi^2!=1`.
Thus the infinity fibre is empty.

## Fixed rank obstruction

For the genuine `lambda=1` kernel, two `D01` one-marked four-minors are

```text
mode 0, rows (1,3,5,7):
  128*c*phi*(phi^2-1)*G*(phi*u-c*(phi^2-1)),

mode 3, rows (4,5,6,7):
  -128*c*u*(phi^2-1)*G/phi^2.
```

If both one-marked maps had target-local rank at most three, both minors
would vanish.  On `c*G*(phi^2-1)!=0`, the mode-three minor forces `u=0`;
the mode-zero minor then forces `c*(phi^2-1)=0`, a contradiction.  Hence
every genuine extension is obstructed.

## Preserved endpoints and evidence boundary

At `phi=+1` or `phi=-1` one also has `q=phi`, so the ordinary restricted
tensor itself is zero.  Those zero endpoints, their transverse or
projectivized directions, and all valuative fibres remain `UNKNOWN` here.
A separate no-import audit reconstructed the theorem and promoted it to
`VERIFIED`; its discovery label remains `DERIVED`.
