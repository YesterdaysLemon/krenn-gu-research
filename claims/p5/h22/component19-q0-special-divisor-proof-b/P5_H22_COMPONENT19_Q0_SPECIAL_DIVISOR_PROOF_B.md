---
role: proof_b
date_utc: 2026-08-01T15:29:47Z
git_commit: 6e6e02ad34c8462f2fc08087ee6fc73e3e543f28
claim_label: VERIFIED
discovery_claim_label: DERIVED
scope: component 19 weighted H22 on q=0 with p*phi*(phi^2-1)!=0
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_VERIFICATION.md: 43e714b95f8a092bee9bf3b9259916a66bf7e8ae5984b63bf259d7e41aa4f440
  P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md: da64a3ee55d5dfa361a70cb771196f76f93d13b3d61df358442a22e1e72de1a8
method: fresh subset-algebra permanents, fixed pair minors, direct finite/infinity contractions, structural case splits, and fixed extension and one-marked minors; no Groebner basis
command: uv run --with sympy python claims/p5/h22/component19-q0-special-divisor-proof-b/derive_p5_h22_component19_q0_special_divisor_proof_b.py
outputs:
  derive_p5_h22_component19_q0_special_divisor_proof_b.py: sha256 emitted by replay JSON
  P5_H22_COMPONENT19_Q0_SPECIAL_DIVISOR_PROOF_B.md: sha256 emitted by replay JSON
limitations: phi=+/-1 rank-jump endpoints are recorded but not closed; no other parameter/projective boundaries, arbitrary-order reduction, component exhaustiveness, prize graph, or global conclusion
---

# Component 19, `q=0`, weighted `H22`: proof B

## Result

Over `Q(p,phi)` with

```text
p*phi*(phi^2-1) != 0,
```

the `q=0` family is nonzero and all-pair-open, with pair profile

```text
(3,4,4,3,3,3).
```

The complete finite shared incidence has the unique marking branch

```text
lambda=1,       h=(1/phi,0,t,0).
```

There is no shared infinity branch.  On the finite branch the shared
extension kernel is two-dimensional, but its genuine open has a fixed
rank-four one-marked minor.  Hence the weighted `H22` fibre is empty on the
stated divisor.  This was independently reconstructed by the separate
no-import audit and is now `VERIFIED`; its discovery label remains `DERIVED`.

## Specialized planes and pure basis

Put

```text
A=X0+X1,  Abar=X0-X1,  B=X2+X3,  Bbar=X2-X3.
```

At `q=0`, orient the planes as

```text
alpha0=-phi*(Abar+pB)-p*Bbar,   beta0=Abar+pB,
alpha1=B,                        beta1=A,
alpha2=Bbar,                     beta2=A,
alpha3=Abar,                     beta3=B+phi*Bbar.
```

The change from the displayed component basis of `U0` has determinant `p`,
so it is valid on the stated open.  Direct squarefree multiplication gives

```text
T_w=0 for w!=1111,       T_1111=4p.
```

Fixed minors, with all larger minors checked to vanish when the asserted
rank is three, give pair profile `(3,4,4,3,3,3)`.  In particular the exterior
rank-three edge `01` has witness `-4*p^2*phi`; the exterior rank-four edges
`02,03` have witnesses `8*p^3` and `-8*p^2*phi`.

## Direct contraction setup

Mark `beta_i` by `beta_i+h_i*alpha_i`, and append independent extension
coordinates `C_i,D_i` to these marked rows.  On the finite chart use

```text
D01(z,x)=(lambda*z0+z1,z2,z3,x),
D23(z,x)=(z0,z1,lambda*z2+z3,x).
```

The infinity maps are constructed directly by retaining respectively `z0`
and `z2`; they are not obtained by taking a leading coefficient of a finite
Groebner basis.

## Why `D01` cannot be the binary side

For finite weight, let `K=C1-phi*C2`.  The all-alpha `D01` diagonal is

```text
A01=2*p*K*(lambda-1).
```

On its genuine open, scale `K=1`.  The mixed equations `1000` and `0001`
give

```text
C1=1-phi*h0,  C2=-h0,
h3=(phi*(phi^2-1)*h0-phi^2)/p.
```

The remaining `1001` equation factors exactly as

```text
-2*(lambda-1)*(phi*h0-1)*((phi^2-1)*h0-phi)=0.
```

Thus there are only two cases.  For `h0=1/phi`, the mixed equations either
force the all-beta diagonal to zero when `lambda=-1`, or, when
`lambda!=-1`, reduce a remaining equation to the nonzero unit multiple
`-2*p*(lambda+1)/phi`.  For `h0=phi/(phi^2-1)`, the paired `0010/1010` and
`0100/1100` equations force `h2=h1=0`; at `lambda=-1` the all-beta diagonal
again vanishes, while otherwise the sum of the normalized `1011` and `1101`
equations is `-4*p*(lambda+1)/(phi^2-1)`, a contradiction.

The direct infinity equations have the same two `h0` cases.  Their analogous
remaining equations reduce to `-2*p/phi` and
`-4*p/(phi^2-1)`.  Hence `D01` is never genuinely binary, at finite or
infinite weight.  Any shared configuration must therefore make `D01` pure
and `D23` binary.

## Complete shared branch

For finite weight define

```text
L=C1*(lambda-1)+C2*(lambda+1).
```

Three directly reconstructed `D23` coefficients are

```text
A23=2*phi*L,
T23_0001=2*h3*phi*L,
T23_1000=2*(phi*h0-1)*L.
```

Thus the genuine condition `A23!=0` forces `h3=0` and `h0=1/phi`.  Then

```text
T01_1000=2*C1*p*(lambda-1)/phi,
T01_0000=2*p*(C1-phi*C2)*(lambda-1).
```

If `lambda!=1`, these force `C1=C2=0`, contradicting `L!=0`.  Therefore
`lambda=1`; now `L=2*C2`, and `T23_0100=4*phi*C2*h1` forces `h1=0`.
No equation restricts `h2=t`.  This proves the stated branch without an
elimination or specialization of the generic theorem.

At infinity, put `L_inf=C1+C2`.  The corresponding three `D23` equations
again force `h3=0,h0=1/phi` on `A23!=0`.  The `D01` equations become

```text
2*p*(C1-phi*C2)=0,       2*p*C1/phi=0,
```

so `C1=C2=0`, contradicting `L_inf!=0`.  The infinity branch is empty.

## Shared kernel and obstruction

On the finite branch, the combined 29-by-8 unwanted-coefficient matrix kills

```text
vC=(0,-1/p,phi/p,0; 1,0,0,0),
vD=(0,0,0,0;             0,1,0,0).
```

Rows `(2,3,5,11,13,16)` and columns `(0,1,2,3,6,7)` have determinant

```text
4096*p^4*phi^2*(phi-1)*(phi+1).
```

Hence these two vectors are the complete kernel on the stated open.  Write
the extension as `C*vC+D*vD`.  Its three genuine diagonals are

```text
B01=4*(pD-phi*tC),
A23=4*C*phi^2/p,
B23=4*C.
```

Thus the common genuine open is exactly

```text
C*(pD-phi*tC) != 0
```

after the standing units are suppressed.  The mode-three `D01` one-marked
matrix has fixed rows `(1,2,5,7)` determinant

```text
-64*C*p*(pD-phi*tC)^2.
```

It is nonzero on the genuine open, so that one-marked map has rank four,
contradicting the rank-at-most-three target-local factorization required by
a ternary weighted-`H22` lift.

## The `phi=+/-1` boundary

No denominator introduced in the plane basis or shared marking uses
`phi^2-1`; only `p` and `phi` are inverted there.  The factor `phi^2-1`
first becomes essential in the complete-kernel minor and the `D01` binary
case split.

At either endpoint the combined branch matrix has rank exactly five: rows
`(2,3,11,13,16)` and columns `(0,1,2,3,6)` have determinant `1024*p^3`, and
the kernel gains the third vector

```text
(p*phi,0,-phi,0; 0,0,0,1).
```

This rank jump is recorded exactly.  The endpoint fibres are not claimed
closed by this report.
