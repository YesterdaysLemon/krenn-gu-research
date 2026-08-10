---
role: proof_b
date_utc: 2026-08-01T15:48:14Z
git_commit: 60b2250e8ce98fa0e787637401686f4edb65d306
claim_label: VERIFIED
discovery_claim_label: DERIVED
scope: component 19 weighted H22 on q=phi with p*phi!=0
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
method: regular intrinsic basis, subset-algebra permanents, fixed pair minors, direct finite/infinity equations, normalized compatibility identities, and a fixed full-rank extension minor
command: uv run --with sympy python claims/p5/h22/component19-q-equals-phi-divisor-proof-b/derive_p5_h22_component19_q_equals_phi_divisor_proof_b.py
outputs:
  derive_p5_h22_component19_q_equals_phi_divisor_proof_b.py: sha256 emitted by replay JSON
  P5_H22_COMPONENT19_Q_EQUALS_PHI_DIVISOR_PROOF_B.md: sha256 emitted by replay JSON
limitations: p=0 is the zero-tensor boundary and phi=0 is outside the component torus; no other projective boundaries, arbitrary-order reduction, component exhaustiveness, prize graph, or global conclusion
---

# Component 19 on `q=phi`: proof B

## Result

On the full nonzero all-pair-open divisor

```text
q=phi,       p*phi != 0,
```

the weighted-`H22` fibre is empty.  One orientation fails because `D23`
has identically zero all-alpha diagonal.  The reverse orientation has one
finite candidate marking and weight when `phi^2!=1`, but its combined
extension matrix has rank eight and zero kernel.  The infinity chart is
empty.  A separate no-import audit independently reconstructed the theorem,
so it is now `VERIFIED`; its discovery label remains `DERIVED`.

## Regular intrinsic basis

The source family specializes to

```text
U0=<Abar+pB, Bbar+phi B>.
```

Instead of dividing by `q-phi`, orient it directly as

```text
alpha0=Bbar+phi B,       beta0=Abar+pB.
```

Together with

```text
alpha1=B,      beta1=A,
alpha2=Bbar,   beta2=A,
alpha3=Abar,   beta3=B+phi Bbar,
```

this is regular on the entire divisor.  Direct squarefree multiplication
gives

```text
T_w=0 for w!=1111,       T_1111=4p.
```

Hence the tensor is nonzero exactly when `p!=0` within the component torus
`phi!=0`.

Fixed pair minors give the exact profile

```text
(4,4,3,3,3,3).
```

In particular, the `03` rank-three witness is `4*p^2`; it remains nonzero
at `phi=+/-1`.  All four rank-three edges have every `4 x 4` minor equal to
zero.  Thus the whole `p*phi!=0` divisor is all-pair-open.

## The `D23`-binary orientation is impossible

For both finite homogeneous weights and the direct infinity map, the
all-alpha `D23` diagonal is identically

```text
A23=0.
```

A genuine binary contraction requires both diagonal coefficients nonzero.
Therefore `D23` can never be the binary side on this divisor.

## Finite reverse orientation

It remains to make `D01` binary and `D23` pure.  Put

```text
K=C1-phi*C2.
```

The all-alpha `D01` diagonal and three mixed coefficients are

```text
A01=-2*K*(lambda-1),
T01_0001=-2*h3*K*(lambda-1),
T01_1000=2*(lambda-1)*(-h0*K+p*C2),
T01_1001|h3=0=2*(lambda-1)*(-phi*C1+C2).
```

On `A01!=0`, scale `K=1`.  These equations force

```text
h3=0,
C2=phi*C1,
C1=1/(1-phi^2),
C2=phi/(1-phi^2),
h0=p*phi/(1-phi^2).
```

Thus no binary branch exists at `phi=+1` or `phi=-1`.  Away from those two
points, `D23` purity forces the unique finite weight

```text
lambda=(1-phi)/(1+phi).
```

The remaining `D23` equations give

```text
C0=C3=D3=0,
D1=h1/(1-phi^2),
D2=phi*h2/(1-phi^2).
```

Two `D01` mixed equations then become

```text
4*h2*phi/(phi+1)=0,
4*h1*phi/(phi+1)=0,
```

so `h1=h2=0`.  The complete candidate marking is therefore

```text
h=(p*phi/(1-phi^2),0,0,0).
```

At this marking, rows `(1,2,3,4,7,10,12,24)` of the combined 29-by-8
unwanted-coefficient matrix have determinant

```text
-131072*p^2*phi^4/(phi+1)^8.
```

This is nonzero on the candidate open, so the complete shared extension
kernel is zero.  Equivalently, after the normalization `K=1`, two remaining
equations demand simultaneously

```text
D0*(1-phi^2)+p=0,
D0*(phi^2-1)+p=0,
```

which is impossible because `p!=0`.

## Infinity and retained boundaries

At infinity, the `D01` all-alpha open again forces

```text
h3=0,       C2=phi*C1.
```

If `phi^2=1`, this contradicts `K!=0`.  Otherwise the `D23` pure equation is

```text
-2*(C1+C2)=-2*C1*(1+phi)=0.
```

For `phi!=-1` this contradicts `K!=0`; at `phi=-1`, `K` was already zero.
Thus the infinity chart is empty.

The excluded `p=0` locus has `T1111=0` and is the zero-tensor boundary.
The value `phi=0` is outside the component's required parameter torus and
meets the separately analyzed `q=0` degeneration; neither is promoted to a
point of this nonzero divisor theorem.
