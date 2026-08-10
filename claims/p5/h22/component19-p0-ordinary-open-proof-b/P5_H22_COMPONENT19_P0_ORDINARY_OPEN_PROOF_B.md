---
role: proof_b
date_utc: 2026-08-01T16:02:32Z
git_commit: 7a3eea50e311a163765750fa5f22f9d2b5c1b98e
claim_label: VERIFIED
discovery_claim_label: DERIVED
scope: ordinary component-19 p=0 boundary on q*phi*(q-phi)!=0
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: regular replacement basis, subset-algebra permanents, fixed pair and kernel minors, direct finite/infinity compatibility, complete kernel vectors, and complete one-marked four-minor generators
command: uv run --with sympy python derive_p5_h22_component19_p0_ordinary_open_proof_b.py
outputs:
  derive_p5_h22_component19_p0_ordinary_open_proof_b.py: sha256 emitted by replay JSON
  P5_H22_COMPONENT19_P0_ORDINARY_OPEN_PROOF_B.md: sha256 emitted by replay JSON
limitations: obstruction-open theorem only; no closure across listed rank-safe loci; q=0 is not all-pair-open, phi=0 is outside the component torus, and q=phi projectivized directions are deferred
---

# Component 19 on the ordinary `p=0` boundary: proof B

## Result and evidence boundary

The ordinary `p=0` restriction is not identically zero.  On

```text
q*phi*(q-phi) != 0
```

it is nonzero and all-pair-open.  Away from the compatibility divisor
`phi*q=1`, its complete shared finite incidence has a single branch and a
three-dimensional extension kernel.  Two complete one-marked minor
generators give an exact obstruction open.

In particular, the weighted-`H22` fibre is empty on the principal parameter
open

```text
q*phi*(q-phi)*(q^2-1)*(phi^2-1)*((q*phi)^2-1) != 0.
```

The special rank-safe divisors listed below remain `UNKNOWN`; this report does
not infer their closure from the proved open.  A separate no-import audit
independently reconstructed the theorem, so it is now `VERIFIED`; its
discovery label remains `DERIVED`.

## Regular ordinary basis and tensor

At `p=0`, use the original two rows of `U0` in the intrinsic order

```text
alpha0=Abar,       beta0=Bbar+qB.
```

Together with

```text
alpha1=B,      beta1=A,
alpha2=Bbar,   beta2=A,
alpha3=Abar,   beta3=B+phi Bbar,
```

this is regular even though the generic function-field basis has collapsed.
Direct squarefree multiplication gives exactly

```text
T_w=0 for w!=1111,       T_1111=4*(q-phi).
```

Thus the apparent zero obtained by retaining only the generic `4p` diagonal
is a basis artifact whenever `q!=phi`.

## Pair strata

On `q*phi*(q-phi)!=0`, fixed minors and all larger-minor checks give

```text
phi*q!=1:   (3,3,4,3,3,3),
phi*q=1:    (3,3,3,3,3,3).
```

The fixed rank-three witnesses for `01` and `02` are both `4q`; those for
`13` and `23` are `4phi`.  The `03` rank-four witness off `phi*q=1` is
`-8*(q-phi)*(phi*q-1)`.  On `phi*q=1`, its rank-three witness is

```text
4*(phi-1)*(phi+1)^2/phi.
```

This is nonzero because `q=1/phi` and `q!=phi` imply `phi^2!=1`.

## Complete compatibility off `phi*q=1`

The all-alpha `D01` diagonal vanishes identically at finite and infinite
weights, so `D01` cannot be the binary side.  Put

```text
L=C1*(lambda-1)+C2*(lambda+1).
```

For the `D01`-pure, `D23`-binary orientation,

```text
A23=-2L,
T23_0001=-2*h3*L,
T23_1000=-2*h0*L.
```

The genuine condition `A23!=0` forces `h0=h3=0`.  Two `D01` pure equations
are

```text
-2*(lambda-1)*(phi*C1-C2)=0,
 2*(lambda-1)*(-C1+q*C2)=0.
```

If `lambda!=1`, their determinant is `phi*q-1`; hence off that divisor they
contradict `L!=0`.  Therefore `lambda=1`.  The remaining equations force
`h1=0` and leave `h2=t` free.  At infinity the analogous equations force
`phi*q=1`, so there is no infinity branch off that divisor.

The complete finite branch is

```text
lambda=1,       h=(0,0,t,0).
```

Its combined 29-by-8 unwanted-coefficient matrix has rank exactly five.  A
fixed five-minor is `-1024*q*(q-phi)^2`, and the complete kernel is

```text
vX=(0,-1/r,phi/r,0; 1,0,0,0),
vY=(0,0,0,0;         0,1,0,0),
vZ=(0,-q/r,1/r,0;    0,0,0,1),
r=q-phi.
```

## Genuine locus and exact obstruction open

Write the extension as `X*vX+Y*vY+Z*vZ` and define

```text
F=phi*X+Z,
G=(q-phi)*Y-t*F,
H=X+q*Z.
```

The three genuine diagonals are

```text
B01=4G,       A23=-4F/(q-phi),       B23=4H.
```

Thus the common genuine locus is exactly `F*G*H!=0`.

All mode-zero one-marked `4 x 4` minors are zero or signs of

```text
M0=64*Z*(phi^2-1)*(2*phi*X+(phi*q+1)*Z)*G/(q-phi)^2,
```

and all mode-three four-minors are zero or signs of

```text
M3=-64*X*(q^2-1)*((phi*q+1)*X+2*q*Z)*G/(q-phi)^2.
```

Therefore the exact certified obstruction open is

```text
F*G*H != 0  and  (M0 != 0 or M3 != 0).
```

On this union a one-marked map has rank four, contradicting the required
rank-at-most-three target-local factorization.

For the simpler parameter-only theorem, suppose additionally that
`q^2`, `phi^2`, and `(q*phi)^2` are all different from one.  If both residual
linear factors vanished with `X*Z!=0`, their coefficient determinant would be

```text
-(phi*q-1)^2,
```

which is nonzero.  The cases `X=0` or `Z=0` would instead force
`phi*q=-1`.  Hence at least one of `M0,M3` is nonzero throughout every
genuine extension on the principal parameter open stated above.

On the finer divisor `q*phi=-1`, the same formulas already certify every
genuine extension with `X*Z!=0`; only the axis cases `X*Z=0` remain
`UNKNOWN` here.

## Explicit `UNKNOWN` and deferred loci

No closure claim is made for:

- `q=+1` or `q=-1`;
- `phi=+1` or `phi=-1`;
- the compatibility divisor `q*phi=1`, including all its intersections;
- `q*phi=-1` with `X*Z=0` on the rank-safe genuine locus;
- any other simultaneous `M0=M3=0` extension sublocus.

The ordinary sublocus `q=phi` has zero restricted tensor.  Its transverse or
projectivized tensor directions are deliberately deferred and are not mixed
with the ordinary nonzero fibre in this report.  Likewise `q=0` is not
all-pair-open here, while `phi=0` lies outside the component parameter torus.
