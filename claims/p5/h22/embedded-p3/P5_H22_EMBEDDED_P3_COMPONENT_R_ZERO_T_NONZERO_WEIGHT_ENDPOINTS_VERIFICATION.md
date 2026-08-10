# Independent verification of the two `t0 != 0` weighted-`H22` endpoints

```yaml
role: verifier
date_utc: 2026-08-01T11:47:57Z
git_commit: b563d842bdde4d05d3dfd0a845f8b4ed3b6c74bc
claim_label: VERIFIED
scope: embedded-P3 free-plane r0=0, t0!=0 weighted-H22 fibres at [rho:sigma]=[0:1] and [1:0]
inputs:
  P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_ENDPOINTS_OBSTRUCTION_CANDIDATE.md: 71bf270bdf74fe756b89a130fcb64c3eacddd5f28cdc5c9c8ed9a4386c1a9ac7
  derive_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_obstruction_candidate.py: a8f1afa1223d859b75368d405ccf4bd152c7f335541fb747f42c4a4a6fbd5705
  P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md: 3471170831a745c05f2fb2f462719b42ad643da49d4ffe5f3ea56ffd07bfd9a1
  verify_p5_h31_embedded_p3_component_r_zero_boundary.py: c0a9069d8d4cc0522e592a797eacd1fd092f932655b712ceac1c4261c2ee5c10
  P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md: 3d1914a582f3d38baa6fa182c77774acdb598c1fd884d266afbb23c483c7c8e7
  verify_p5_h31_embedded_p3_component_normalized_boundary.py: 4b7b09f8e3a56a5f5c70e20cc6d2024afc36c2c5afd93ce1d7b4362fa480577f
method: fresh no-import original-coordinate permanent reconstruction, exact signed-swap and normalization transport, and separate characteristic-zero H31 theorem replays
command: uv run --with sympy python claims/p5/h22/embedded-p3/audit_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_verifier.py
outputs:
  audit_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_verifier.py: hash reported by replay
  P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_ENDPOINTS_VERIFICATION.md: hash reported by replay
limitations: exactly the two stated t0!=0 homogeneous endpoints on this embedded-P3 r0=0 chart; the weight-zero conclusion depends on the separately replayed exact H31 theorem; no component-exhaustiveness, arbitrary-order, prize-graph, or global Krenn-Gu claim
```

## Verdict

**VERIFIED for the frozen endpoint claim.**  The audit imports neither the
construction script nor its functions.  It rebuilds all four endpoint
contractions from the original four planes, with independent symbolic marking
and extension coordinates, and checks all sixteen permanent coefficients when
transporting the only nontrivial direction to the exact `H31` chart.

This is not a statement about the whole weighted-`H22` frontier.  It closes
only the two homogeneous weight endpoints on the chart

```text
r0=0,                    t0 != 0.
```

## Original-coordinate endpoint audit

The verifier starts from

```text
alpha0=(0,1,S,U),              beta0=(1,0,0,t0),
alpha1=(0,-1,1,0),             beta1=(0,-1,0,1),
alpha2=(0, 1,0,1),             beta2=(0, 1,1,0),
alpha3=(0, 0,1,1),             beta3=(0,-1,0,1),
```

and uses arbitrary markings `betai+hi alphai`.  The alpha and beta extensions
are eight independent symbols in each weighted direction.

At `[rho:sigma]=[1:0]`, the two contractions are

```text
D01(z,e)=(z0,z2,z3,e),
D23(z,e)=(z0,z1,z2,e).
```

All four alpha rows have `z0=0`.  The all-alpha permanent therefore has a zero
target column in both contractions, and the audit obtains identically

```text
A01=0,                    A23=0.
```

Neither contraction can have the two nonzero diagonals of a genuine binary
slice.  Since weighted `H22` requires at least one of these two marked slices
to be binary, the endpoint is empty.

At `[rho:sigma]=[0:1]`,

```text
D01(z,e)=(z1,z2,z3,e),
D23(z,e)=(z0,z1,z3,e).
```

The same zero-column argument gives `A23=0`, so `D23` cannot be binary.  The
audit then verifies, including all eight extension coordinates, all sixteen
coefficients, and both diagonals, that `D01` is literally deletion zero before
normalization.  Thus any weighted-`H22` point would contain the deletion-zero
binary slice required by the corresponding `H31` subproblem.

## Exact `t0 != 0` transport

The audit does not reuse the invalid full-`H22` shared-weight transport.  It
first records that the signed source swap

```text
P:(x0,x1,x2,x3) -> (x0,x1,-x3,-x2)
```

acts on the two pencils by

```text
D01^[rho:sigma] -> D01^[rho:sigma]
D23^[rho:sigma] -> D23^[sigma:rho]
```

up to signed target-coordinate permutations.  In particular, `D23` exchanges
the two endpoints.  This is exactly why the earlier common-weight `H22`
transport could not close them.

For the direction-local deletion-zero `H31` dependency, however, only `D01`
is used, and that direction is preserved.  Put `r'=-t0`.  After the signed
swap, interchange old modes one and two and scale source coordinate zero by
`r'`.  The transformed planes are the normalized embedded-`P3` planes with

```text
(S',U',T')=(-U,-S,0),
```

and the marking change is

```text
(h0,h1,h2,h3) -> (h0/r',h2,h1,-1-h3).
```

Its Jacobian is `1/r'`.  The corresponding extension change has Jacobian
`-1/r'`.  Both are invertible exactly under the frozen assumption
`t0!=0`.  The verifier checks the precise row rescalings and, for every binary
word, the resulting nonzero coefficient rescaling.  In particular,

```text
A_normalized=-A_original,
B_normalized=B_original/r'.
```

Hence genuine deletion-zero binary points are carried bijectively to the full
normalized chart; no marking family, extension direction, or diagonal endpoint
is lost.

## Replayed `H31` dependency

The verifier runs both exact characteristic-zero theorem scripts in fresh
subprocesses and checks their frozen theorem hashes and conclusions:

- the normalized chart has exactly five classified binary-survivor marking
  families, all excluded by its one-marked covers or deepest stacked
  determinant `8`;
- the `r=0` boundary theorem reports the exact signed transport to the
  normalized chart and verifies its own boundary family cover.

No finite-field audit is used as proof.  Therefore deletion-zero `D01` cannot
be the binary member of a local lift at `[0:1]`.  Since `D23` cannot be binary
there, the endpoint is empty.

## Projective and boundary ledger

- Replacing `[rho:sigma]` by `[kappa rho:kappa sigma]`, `kappa!=0`, is checked
  to be a nonzero monomial target rescaling in each direction.  Thus the two
  representative endpoint calculations are projectively well defined.
- The arguments are uniform in all `S,U` and all markings.  No generic
  `S,U` factor is divided out.
- The only division is by `r'=-t0`, exactly matching the stated open condition
  `t0!=0`.  The intersection `t0=0` is outside this claim and is handled by the
  separate corner theorem.
- The two weight endpoints are distinct points of the projective weight line.
  Their exchange in `D23` is explicitly recorded rather than treated as an
  intersection or silently identified.
- No grid, finite field, or broad brute-force search enters the proof.
- The global Krenn--Gu conjecture remains unresolved.

## Replay

```text
uv run --with sympy python claims/p5/h22/embedded-p3/audit_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_verifier.py
```

The JSON output must report `status: pass`, `claim_label: VERIFIED`, both
endpoint fibres obstructed, the complete signed-swap/normalization ledger, and
successful exact replays of both `H31` dependencies.
