# Component 19 weighted `H22` on `q=phi` — VERIFIED

```yaml
role: construction
date_utc: 2026-08-01T15:45:15Z
git_commit: 3738e5a0d2fb94658a80808c0ff60eee3173eb56
claim_label: VERIFIED
discovery_claim_label: CANDIDATE
scope: finite divisor q=phi on its exact nonzero all-pair-open locus p*phi!=0
inputs: paths and SHA-256 hashes emitted by replay
method: regular intrinsic basis, exact permanents/pair minors, finite/infinity shared incidence, parameter-aware elimination
command: uv run --with sympy python claims/p5/h22/component19-q-eq-phi-special-divisor/derive_p5_h22_component19_q_eq_phi_special_divisor_obstruction_candidate.py
outputs: this report, its JSON certificate, and the standalone replay
limitations: independently verified on the stated open; finite opposite-plane chart only; no global conclusion
```

## Frozen result

**VERIFIED:** the component-19 weighted-`H22` fibre is empty on

`q=phi,   p*phi != 0`.

The calculation starts from the specialized planes and a regular intrinsic
basis.  It never substitutes into the generic `H22` ideal and never divides
by `q-phi`.

## Regular pure basis and exact open set

On `q=phi`, reconstruct

```
U0=<Abar+pB, Bbar+phi B>,
U1=<B,A>,
U2=<Bbar,A>,
U3=<Abar,B+phi Bbar>.
```

Use the denominator-free row-swap basis

```
alpha0=Bbar+phi B,  beta0=Abar+pB,
alpha1=B,           beta1=A,
alpha2=Bbar,        beta2=A,
alpha3=Abar,        beta3=B+phi Bbar.
```

The mode-zero change from the displayed `U0` rows has determinant `-1`.
Thus it remains regular everywhere on this affine chart.  After every affine
marking `betai -> betai+hi alphai`, exact permanent expansion gives only

`T1111=4p`.

The pure point is therefore nonzero and intrinsically unique when `p!=0`.
Direct squarefree pair minors, reconstructed after imposing `q=phi`, give

`(rank01,rank02,rank03,rank12,rank13,rank23)=(4,4,3,3,3,3)`

with fixed witnesses

`8p*phi, 8p, 4p^2, 4, -4, 4phi`.

Hence the exact nonzero all-pair-open locus is `p*phi!=0`.  There are no
hidden exclusions at `phi=+1` or `phi=-1`.

At `p=0`, the pure coefficient vanishes.  At `phi=0` with `p!=0`, the pure
coefficient remains nonzero, but edge `23` has rank exactly two; a fixed
two-minor equals `2`.  Thus `phi=0` is honestly outside the all-pair-open
locus rather than silently inverted.

## Complete projective weighted incidence

For finite weights `[lambda:1]`, build

```
D01(z,e)=(lambda*z0+z1,z2,z3,e),
D23(z,e)=(z0,z1,lambda*z2+z3,e).
```

The `[1:0]` maps are reconstructed separately.  In every calculation the
same four affine markings and eight-coordinate extension are retained.
Both beta diagonals are explicitly saturated as nonzero.  The required
disjunction `A01!=0 or A23!=0` is exhausted by normalizing each orientation
in turn, so the both-binary overlap is included.

Direct bidirectional elimination over `Q(p,phi)` returns the unit ideal for
each individual binary direction on both projective weight charts:

```
D01 binary, finite:    <1>
D01 binary, infinity:  <1>
D23 binary, finite:    <1>
D23 binary, infinity:  <1>.
```

The complete shared calculations are also performed rather than inferred:

```
shared A01, finite:    <1>
shared A01, infinity:  <1>
shared A23, finite:    <1>
shared A23, infinity:  <1>.
```

Thus no marking, finite slope, weight endpoint, or shared extension survives
on the function field.

## Parameter-aware boundary audit

To expose every parameter factor hidden by the function field, the replay
repeats all eight systems over `Q[p,phi]`, retaining `p,phi` during
elimination.  It finds

```
D01 binary projection closure, finite and infinity:
  <h3,h2,h0,phi>

D23 binary projection, finite and infinity:
  <1>

all four shared orientation projections:
  <1>.
```

Therefore the only individual-binary parameter warning is supported on
`phi=0`, already excluded because edge `23` has rank two.  Even there, both
shared orientations are unit ideals.  This records the false lead without
promoting a projection-closure point to an actual lift.

No broad search, parameter grid, finite-field inference, generic-ideal
specialization, or denominator-divergent marking is used.  The discovery
label remains `CANDIDATE`, but the frozen statement was independently
reconstructed and is now `VERIFIED` on the stated open.  See
[`P5_H22_COMPONENT19_Q_EQUALS_PHI_OBSTRUCTION_VERIFICATION.md`](../component19-q-equals-phi/P5_H22_COMPONENT19_Q_EQUALS_PHI_OBSTRUCTION_VERIFICATION.md).
Projective opposite-plane boundaries and the global Krenn-Gu problem remain
unresolved.
