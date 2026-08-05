# Verified obstruction for the two `t0 != 0` weighted-`H22` endpoint fibres

Discovery run report (before independent verification):

```yaml
role: construction
date_utc: 2026-08-01T11:35:41Z
git_commit: ab1c3d7f12c47e3a817af86464ab66786b3d9a43
claim_label: CANDIDATE
scope: embedded-P3 free-plane r0=0, t0!=0 weighted-H22 fibres at [rho:sigma]=[0:1] and [1:0]
inputs:
  P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION_CANDIDATE.md: bfe1088d4047cbf3dfacf67562fa15b937d0aed5afcf4d3ac3e1214d510ce232
  P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md: 3471170831a745c05f2fb2f462719b42ad643da49d4ffe5f3ea56ffd07bfd9a1
  verify_p5_h31_embedded_p3_component_r_zero_boundary.py: c0a9069d8d4cc0522e592a797eacd1fd092f932655b712ceac1c4261c2ee5c10
method: exact characteristic-zero reconstruction in original coordinates, structural zero-column obstructions, and coefficientwise identification of D01 at [0:1] with the verified deletion-zero H31 direction
command: |
  uv run --with sympy python verify_p5_h31_embedded_p3_component_r_zero_boundary.py
  uv run --with sympy python derive_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_obstruction_candidate.py
outputs:
  derive_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_obstruction_candidate.py: hash reported by replay
  P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_ENDPOINTS_OBSTRUCTION_CANDIDATE.md: hash reported by replay
limitations: candidate pending fresh independent endpoint replay; the [0:1] conclusion depends on the cited exact H31 theorem; only the two stated endpoint fibres are treated; no component-exhaustiveness, arbitrary-order, prize-graph, or global Krenn-Gu conclusion is made
```

## Frozen claim and status

The two previously `UNKNOWN` homogeneous endpoint fibres on the free-plane
divisor

```text
U0=span((1,0,0,t0),(0,1,S,U)),        t0 != 0,
```

have exact structural obstructions.  This is **VERIFIED** after a fresh
no-import verifier independently reconstructed the endpoint maps, both
marking-weight orientations, and the `H31` dependency.  No grid or
finite-field calculation is used.

Use the original component bases

```text
alpha0=(0,1,S,U),              beta0=(1,0,0,t0),
alpha1=(0,-1,1,0),             beta1=(0,-1,0,1),
alpha2=(0, 1,0,1),             beta2=(0, 1,1,0),
alpha3=(0, 0,1,1),             beta3=(0,-1,0,1),
```

with arbitrary markings `betai -> betai+hi alphai` and arbitrary extension
coordinates.  The homogeneous contractions are reconstructed directly; no
division by either weight is made.

## The endpoint `[rho:sigma]=[1:0]`

Here

```text
D01(z,e)=(z0,z2,z3,e),
D23(z,e)=(z0,z1,z2,e).
```

Every `alphai` has source coordinate zero equal to zero.  Both projected
all-alpha matrices therefore have an identically zero first target column, so

```text
A01=0,                   A23=0
```

identically for all `(S,U,t0)`, markings, and extensions.  A genuine binary
slice requires both its all-alpha and all-beta diagonal coefficients to be
nonzero.  Neither direction can be that binary slice, so a weighted-`H22`
pair is impossible at this endpoint.

## The endpoint `[rho:sigma]=[0:1]`

Now

```text
D01(z,e)=(z1,z2,z3,e),
D23(z,e)=(z0,z1,z3,e).
```

The `D23` all-alpha matrix again has an identically zero first target column,
so `A23=0` for every marking and extension.  Thus `D23` cannot be the genuine
binary member of an `H22` pair; `D01` would have to be binary.

But `D01` is coefficient-for-coefficient exactly the deletion-zero contraction
covered by the exact free-plane `H31` theorem in
`P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md`.  The replay
script checks equality of all projected alpha rows, beta rows, sixteen tensor
coefficients, the fourteen-row mixed matrix, and both diagonal coefficients.

This use of `H31` is direction-local.  Its exact rank/transverse covers say
that a genuine deletion-zero binary family admits no required additional local
row; in particular, the pure `D23` row needed by `H22` cannot repair it.  For
`t0!=0`, the H31 theorem's signed source swap sends deletion zero to deletion
zero followed only by the invertible target map

```text
(y0,y1,y2,e) -> (y0,-y2,-y1,e).
```

There is no second contraction weight in this dependency, so the shared-weight
mismatch that invalidated the earlier full weighted-`H22` transport does not
occur.

## Boundary ledger

- The argument is exact over characteristic zero and uniform in `S,U` and
  nonzero `t0`; it uses neither a generic parameter division nor a finite grid.
- The `[1:0]` conclusion is a direct zero-column obstruction.
- The `[0:1]` conclusion has one explicit dependency: the already verified
  free-plane deletion-zero `H31` theorem and its exact verifier, whose hashes
  are frozen in the run report.
- This note does not alter the independently verified `t0=0` corner, and it
  does not reuse the invalid shared-weight transport for `t0!=0`.
- The fresh verification report is
  `P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_ENDPOINTS_VERIFICATION.md`.

## Replay

```text
uv run --with sympy python derive_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_obstruction_candidate.py

uv run --with sympy python audit_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_verifier.py
```

The script is standalone.  It reconstructs both endpoint contractions from
the original planes, proves the structural all-alpha zeros, checks the literal
deletion-zero model identity, checks the signed-swap target equivalence, and
prints input/output hashes and the remaining limitations.
