---
role: proof_b
date_utc: 2026-08-01T15:39:05Z
git_commit: 7dc8acbc6186f84c6c9d78cab4f7be5c46e727cf
claim_label: VERIFIED
discovery_claim_label: DERIVED
scope: component 19 weighted H22 on q=0, phi=+1 and phi=-1, p!=0
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  P5_H22_COMPONENT19_Q0_SPECIAL_DIVISOR_PROOF_B.md: 86b70a49969bf7e71bf0e50b90ae2927463f6c6fde3eb7e498e3b51e9e4a6c56
  derive_p5_h22_component19_q0_special_divisor_proof_b.py: 782ec5fed5fb93fc6cc6c222206ce3e009647c8a38b72c2cb321bcab00a40fc8
method: fresh endpoint squarefree permanents, direct finite/infinity contractions, structural orientation split, complete kernel vectors plus fixed rank minors, and fixed one-marked minors
command: uv run --with sympy python claims/p5/h22/component19-q0-phi-endpoints-proof-b/derive_p5_h22_component19_q0_phi_endpoints_proof_b.py
outputs:
  derive_p5_h22_component19_q0_phi_endpoints_proof_b.py: sha256 emitted by replay JSON
  P5_H22_COMPONENT19_Q0_PHI_ENDPOINTS_PROOF_B.md: sha256 emitted by replay JSON
limitations: p=0 is the zero-tensor/lower boundary and is excluded; no other projective component boundaries, arbitrary-order reduction, component exhaustiveness, prize graph, or global conclusion
---

# Component 19 at `q=0`, `phi=+/-1`: proof B

## Result

For each sign `epsilon=phi in {+1,-1}` and `p!=0`, the specialized component
is nonzero and all-pair-open with profile

```text
(3,4,4,3,3,3).
```

The complete weighted-`H22` fibre is empty.  The finite shared branch is
still uniquely

```text
lambda=1,       h=(epsilon,0,t,0),
```

the infinity branch is empty, and the reversed binary/pure orientation is
also empty.  This closes the two rank-jump endpoints left open by the
special-divisor proof.  A separate no-import audit independently reconstructed
both signs, so this claim is now `VERIFIED`; its discovery label remains
`DERIVED`.

## Endpoint planes and pair ranks

The proof reconstructs

```text
alpha0=-epsilon*(Abar+pB)-pBbar,   beta0=Abar+pB,
alpha1=B,                          beta1=A,
alpha2=Bbar,                       beta2=A,
alpha3=Abar,                       beta3=B+epsilon*Bbar.
```

Direct squarefree multiplication gives only `T1111=4p`.  Fixed pair minors
give `(3,4,4,3,3,3)` separately at both signs; all larger minors on the four
rank-three edges vanish identically.

## Completeness of the shared marking

For the orientation in which `D01` is pure and `D23` is binary, write

```text
L=C1*(lambda-1)+C2*(lambda+1).
```

The all-alpha `D23` diagonal and two mixed coefficients are

```text
A23=2*epsilon*L,
T23_0001=2*h3*epsilon*L,
T23_1000=2*(epsilon*h0-1)*L.
```

On `A23!=0`, these force `h3=0` and `h0=epsilon`.  Two `D01` equations then
force `lambda=1`: otherwise they give `C1=C2=0`, contradicting `L!=0`.
At `lambda=1`, `L=2C2`, and `T23_0100=4*epsilon*C2*h1` forces `h1=0`.
Thus `h2=t` is the only free marking coordinate.

At infinity, the same first two equations force `h3=0,h0=epsilon`, after
which the two direct `D01` equations give

```text
C1=0,       C1-epsilon*C2=0.
```

This contradicts the required nonzero `C1+C2`; hence there is no infinity
branch.

For the reversed orientation, normalize the `D01` all-alpha open by
`C1-epsilon*C2=1`.  Its mixed equations force

```text
h0=epsilon, h3=-1/p, C1=0, C2=-epsilon.
```

The `D23` pure equation is then `A23=-2*(lambda+1)`, so it forces
`lambda=-1`.  At that weight the remaining `D01` mixed equations force
`D1=D2=h1=0`, and the all-beta `D01` diagonal is zero.  Thus it is not
genuinely binary.  At infinity the `D23` all-alpha coefficient is the
nonzero constant `-2`, contradicting purity directly.

## Complete endpoint kernels

On the unique finite branch, the combined 29-by-8 unwanted-coefficient
matrix has rank exactly five.  A fixed five-minor is

```text
rows (2,3,11,13,16), columns (0,1,2,3,6): 1024*p^3.
```

Its complete kernel is

```text
vC=(0,-1/p,epsilon/p,0; 1,0,0,0),
vD=(0,0,0,0;             0,1,0,0),
vE=(epsilon*p,0,-epsilon,0; 0,0,0,1).
```

Write the extension as `C*vC+D*vD+E*vE`, and put

```text
F=C-pE,       G=pD-epsilon*tF.
```

The three genuine diagonals are

```text
B01=4G,       A23=4F/p,       B23=4C.
```

Therefore the complete genuine locus is exactly

```text
C*F*G != 0.
```

## Fixed rank-four obstruction

For mode three of the `D01` contraction, rows `(2,3,4,7)` of the one-marked
matrix have determinant

```text
-64*epsilon*C*p*G^2.
```

Thus at `phi=+1` the minor is `-64*C*p*(pD-t(C-pE))^2`, while at `phi=-1`
it is `+64*C*p*(pD+t(C-pE))^2`.  It is nonzero throughout the genuine locus,
so the one-marked map has rank four.  This contradicts the rank-at-most-three
target-local factorization required by a ternary weighted-`H22` lift.

The only adjacent failure retained here is `p=0`: then `T1111=4p` vanishes,
so this is a zero-tensor/lower boundary rather than a point of the nonzero
all-pair-open endpoint family.
