# Independent verification of the embedded-`P3` free-plane `r0=0` weighted-`H22` claim

```yaml
role: verifier
date_utc: 2026-08-01T11:24:20Z
git_commit: 7392ae7e7352a66fc5c42cb017d002043dfd794f
claim_label: REFUTED
scope: full homogeneous weighted-H22 claim on the embedded-P3 free-plane r0=0 divisor
inputs:
  P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION_CANDIDATE.md: 393d088737c3528af220e6536f5f0e0e713387677753d1c6b4695c11c30d9205
  derive_p5_h22_embedded_p3_component_r_zero_boundary_obstruction.py: 7dbeddcdc1238e07938976f51433c5df7a849187350ed363615f436d3ca84cf7
  P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md: 3471170831a745c05f2fb2f462719b42ad643da49d4ffe5f3ea56ffd07bfd9a1
  verify_p5_h31_embedded_p3_component_r_zero_boundary.py: c0a9069d8d4cc0522e592a797eacd1fd092f932655b712ceac1c4261c2ee5c10
method: no-import exact corner elimination, saturated kernels, literal H31-model comparison, and homogeneous-weight transport audit
command: uv run --with sympy python audit_p5_h22_embedded_p3_component_r_zero_boundary_independent.py
outputs:
  audit_p5_h22_embedded_p3_component_r_zero_boundary_independent.py: hash reported by replay
  P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_VERIFICATION.md: hash reported by replay
limitations: the t0=0 corner obstruction is verified, but the full-divisor proof is refuted because the t0 nonzero transport does not cover homogeneous weight endpoints; those endpoint fibres remain UNKNOWN
```

## Verdict

**REFUTED as a proof of the full homogeneous divisor; target UNKNOWN on two
`t0!=0` weight-endpoint fibres.**  The direct `t0=0` corner obstruction is
independently supported over characteristic zero.

The failure is not in the simultaneous corner elimination or its special
kernels.  It is in transporting `t0!=0` to the normalized weighted theorems:
the required source swap preserves the `D01` weight but reverses the `D23`
weight.  Nonzero homogeneous weights can be rebalanced by an invertible
diagonal source scaling; at either endpoint this scaling becomes singular.

## Direct corner replay

At `r0=t0=0`, the audit rebuilt the four planes and both homogeneous
contractions without importing the candidate derivation or the `H31`
verifier.  The exact simultaneous incidence permits a binary `D01` slice and
a nonzero pure all-beta `D23` slice.  It deliberately uses independent
extension vectors as a relaxation; emptiness of that relaxation is a valid
obstruction, while surviving points still require further compatibility.

At weight infinity, bidirectional elimination gives the unit ideal.

For finite weight `r`, independent Singular elimination reproduced all 16
generators in the candidate note exactly.  They split into

```text
r=0:   h0=0, Phi=0,
r=-1:  S=U.
```

No other finite weight survives the relaxed simultaneous incidence.

## The `r=0` dependency is legitimate

At `r=0`,

```text
D01^0(z,e)=(z1,z2,z3,e),
```

which is literally the deletion-zero model in the exact verified `H31`
corner theorem.  The projected ideal also forces `h0=0`, exactly matching
that theorem's forced marking.  Its obstruction is direction-local: every
genuine deletion-zero binary family has a rank-four neighboring marked map
with a nonzero transverse entry.  Consequently it excludes a weighted
`H22` lift before the `D23` row can repair anything.

This dependency is used only after the audit compared the contracted alpha,
beta, coefficient, and extension rows exactly.  It is not an inference that
all `H31` theorems automatically apply to `H22`.

## The `r=-1`, `S=U` branch

For `S=U=s!=0`, the marking is forced to

```text
(h0,h1,h2,h3)=(0,-1,-1,-1/2).
```

Saturation by `s` independently gives the complete `D01` kernel

```text
z3=z5=z6=0,
z1=z0, z2=-z0, z7=z0.
```

Writing its basis coefficients as `(X,Y)`, the audit recovered

```text
A01=4sY,
B01=-2(X+Y),
det N1[0137]=-16s^2Y^2(X+Y).
```

The fixed minor is nonzero whenever the binary slice is genuine.

At `s=0,h0=0`, the complete rank-six kernel has `A01=0`, so it is not
genuine.  At `s=0,h0=1`, the exact marking ideal is

```text
<a*b, a*c, b*(c+1)>,
```

whose three components are the displayed families

```text
(a,b)=(0,0),     (b,c)=(0,0),     (a,c)=(0,-1).
```

For these families, the projected `D01^{-1}` alpha and beta rows are
literally identical to the deletion-zero `H31` singular-base rows: the marked
`beta0` source part is zero, while all other rows already have source
coordinate zero equal to zero.  The exact denominator-free `H31` cover is
therefore a sound dependency here as well.

## The `t0!=0` transport gap

The necessary signed source swap is

```text
P:(x0,x1,x2,x3) -> (x0,x1,-x3,-x2).
```

For a common homogeneous weight `[rho:sigma]`, direct substitution gives

```text
D01 after P: [rho:sigma],
D23 after P: [sigma:rho].
```

Thus the transported pair no longer has the one common weight assumed by
the three cited normalized `H22` theorems.  When `rho*sigma!=0`, the additional
diagonal scaling

```text
diag(1,1,rho^2,sigma^2)
```

rebalances the second contraction to `[rho:sigma]`; it is invertible and
preserves the relevant affine component chart.  This supports the nonendpoint
part of the transport.

At `[rho:sigma]=[0:1]` or `[1:0]`, that scaling is singular.  More
intrinsically, a nonzero diagonal scaling cannot move the zero coefficient
from one endpoint of an ordered pair to the other.  The normalized
dependencies do not cover a pair with weights `[0:1]` and `[1:0]` in its two
directions, and the direct corner infinity elimination applies only at
`t0=0`, not here.

Therefore the claimed homogeneous `t0!=0` transport leaves two explicit
endpoint fibres unproved.

## Evidence boundary

- `t0=0`, finite and infinite weights: independently supported.
- `t0!=0`, `rho*sigma!=0`: transport supported after the additional diagonal
  rebalance.
- `t0!=0`, weights `[0:1]` and `[1:0]`: **UNKNOWN**.
- No finite-field result is used as proof.
- No positive lift is asserted on the uncovered endpoints.
- No component-exhaustiveness, arbitrary-order, or global Krenn--Gu claim is
  made.

Replay:

```text
uv run --with sympy python \
  claims/p5/h22/embedded-p3/audit_p5_h22_embedded_p3_component_r_zero_boundary_independent.py
```
