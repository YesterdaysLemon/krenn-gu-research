# Component 19 weighted `H22` on `p=0, q*phi=1` — VERIFIED

```yaml
role: construction
date_utc: 2026-08-01T16:21:18Z
git_commit: 27e0d4beb3323a7496607c684726aa09dbfe02bb
claim_label: VERIFIED
discovery_claim_label: CANDIDATE
scope: finite ordinary divisor p=0, q*phi=1, phi^2!=1
inputs:
  P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md: ce333e8605b78e17c2e6b7cfe91fd369e89afe0d3aed65c7df35f82fee319634
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_VERIFICATION.md: f414f67a9605b231b6a9737ce9a23ffa9a00eb0336630161d136ea1e25c4f4ae
  NEXT_INSTANCE_HANDOFF_2026-07-31.md: 1464b39b99ada4035600b711c903876b6ec3ed7b23800f4b2ea3e56dbe868487
method: direct Q(phi) reconstruction, exact permanents and pair minors, complete finite/infinity elimination, shared-kernel basis, and two fixed one-marked minors
command: uv run --with sympy python claims/p5/h22/component19-p0-qphi-one-ordinary/derive_p5_h22_component19_p0_qphi_one_ordinary_obstruction_candidate.py
outputs: this report, its JSON certificate, and the bounded standalone replay
limitations: construction result only; phi=+1,-1 zero endpoints and projective/valuative boundaries excluded
```

## Frozen result

**VERIFIED:** the component-19 weighted-`H22` fibre is empty on

`p=0,  q*phi=1,  phi^2!=1`.

This is a direct calculation over `Q(phi)`.  It does not specialize the
generic ordinary-`p=0` branch as proof.

## Direct regular basis and exact ordinary locus

On `q=1/phi`, multiply the original mode-zero beta row by the field unit
`phi`.  The resulting denominator-free basis is

```
alpha=(Abar,B,Bbar,Abar),
beta =(B+phi Bbar,A,A,B+phi Bbar).
```

The mode-zero basis change has determinant `phi`.  After every affine marking,
the exact permanent expansion has only

`T1111=4(1-phi^2)`.

Thus the tensor is nonzero for `phi^2!=1`; `phi!=0` is automatic from
`q*phi=1`.  Every squarefree pair-product matrix has rank exactly three.
Fixed three-minors are

```
edge 01:  4phi
edge 02:  4phi
edge 03:  4(phi-1)(phi+1)^2
edge 12: -4
edge 13:  4phi
edge 23:  4phi
```

and all six matrices have every four-minor equal to zero.  Hence the pair
profile is exactly `(3,3,3,3,3,3)` throughout the stated ordinary locus.

## Complete finite/infinity incidence

All binary and shared orientations are rebuilt from the specialized basis.
Bidirectional exact elimination over `Q(phi)` gives

```
D01 binary, finite:     <1>
D01 binary, infinity:   <1>
D23 binary, finite:     <h3,h0,h1*h2>
D23 binary, infinity:   <h3,h0,h1*h2>
shared A01, finite:     <1>
shared A01, infinity:   <1>
shared A23, finite:     <lambda-1,h3,h1,h0>
shared A23, infinity:   <1>
```

Therefore the only shared branch is finite:

`[lambda:1]=[1:1],  h=(0,0,t,0)`.

## Complete shared kernel and fixed obstruction

The combined `D01/D23` mixed matrix has rank five.  Rows
`(2,9,10,12,15)` and columns `(0,1,2,3,6)` give determinant

`-1024(phi-1)^2(phi+1)^2`.

Its complete three-dimensional kernel is

```
z=(0, (C+E)/(phi^2-1), -phi(C+E)/(phi^2-1), 0; C,D,0,E).
```

Set

```
S=C+E,
G=(phi^2-1)D+phi*t*S.
```

The binary diagonals are

```
A01=0,  B01=-4G,
A23=4phi*S/(phi^2-1),  B23=4S.
```

Thus a genuine shared binary lift requires `S*G!=0`.  Two fixed four-minors
of the `D01` one-marked maps are

```
mode 0, rows (1,3,5,7): -128 E*phi*S*G/(phi^2-1),
mode 3, rows (4,5,6,7): -128 C*phi*S*G/(phi^2-1).
```

On the stated locus and the genuine branch, requiring both one-marked maps
to have rank at most three forces `E=0` and `C=0`.  This contradicts
`S=C+E!=0`.  No shared marking or extension survives, so no full-stack
argument is needed.

The endpoints `phi=+1,-1` have `q=phi` and `T1111=0`; they are separate zero
fibres, not ordinary points covered here.  No finite-field computation,
broad brute force, or global Krenn–Gu inference is used.  A separate no-import
audit reconstructed the complete genuine incidence, caught and repaired an
intermediate missing-`B01` saturation in its own audit, and promoted the
frozen theorem to `VERIFIED`; the discovery label remains `CANDIDATE`.  See
[`P5_H22_COMPONENT19_P0_QPHI_ONE_INDEPENDENT_VERIFICATION.md`](../component19-p0-qphi-one-independent/P5_H22_COMPONENT19_P0_QPHI_ONE_INDEPENDENT_VERIFICATION.md).
