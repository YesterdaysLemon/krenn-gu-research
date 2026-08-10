# Independent verification of the component-twenty generic weighted-`H22` obstruction

```yaml
role: verifier
date_utc: 2026-08-01T13:20:36Z
git_commit: f089d5bc9f9a9f0c3550d6e0f9ca2686a8fb55f4
claim_label: VERIFIED
scope: generic weighted H22 fibre of component twenty over Q(p,q); the p+q=0 wall and all other special/projective fibres are excluded
inputs:
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md: 49149b81ad2a50982d69f03d6e391808ced2beaddff0115f0c86039dd361c823
  derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py: 6d2b36e7a7c8452c02c4a006dde2a2a9c47351bb06cffbe10d19bc8a06790de6
  p5_h22_common_active_binary_triangle_component_generic_certificate.json: 5d70e08b54d8c0d945190019e7b4279bee874a0db966d938553c6f892730e6fc
  P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md: dcaae5365f5e2072e798c2ee52dea47c0d5c48f073ed7553ae5f758e9830f0b2
  verify_p4_common_active_binary_triangle_component.py: 8b5c6892ccf3e48eb1a5d7f1946cb8b9c7617b7b38047c18c1e50bb7f5db244a
  P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md: 73596e624c6a6e093b861b5c366582cd4b61bc39197d01690f295c9e7194722c
  verify_p5_h31_common_active_binary_triangle_component_generic_obstruction.py: d31d0a6255501839ac0d3024882bdd6e328b464fe90cd0dc799dd970dff5a1b5
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md: 52168b35b43c40c483919c8fa1dd37e7c147cae5f331320d8656bf6a1ed309a9
method: fresh subset-DP permanents and five bounded characteristic-zero Singular projections for one shared marking, homogeneous weight, and extension vector
command: uv run --with sympy python audit_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py
outputs:
  audit_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py: f0ea62d6a5e35729ba23b163fefd8aecfb6dd61dc99b2991d7d1e10aeca330bb
limitations: generic function field only; separately verified p+q=0 diagonal-DVR wall not used; no other special/projective fibres, P4 component exhaustiveness, arbitrary-order local-to-global reduction, prize graph, or global Krenn-Gu conclusion
```

## Verdict

**VERIFIED.**  A fresh verifier reconstructs the pure normal form, checks the
complete binary-orientation cover, proves the individual finite `D01`
projection in both ideal directions, and returns unit ideals for every shared
finite and infinity orientation.  The generic marked weighted-`H22` fibre of
component twenty is empty over `Q(p,q)`.

The separately verified `p+q=0` diagonal-DVR wall is not part of this proof.
No other special parameter divisor or projective component-boundary fibre is
classified here.

## Pure normal form

With `s=p-q+1`, the verifier independently rebuilds

```text
alpha0=-p(p+1)A+q(q-1)B+sC,
beta0 =-s e-(p+q)A+(p+q)B,

alpha1=e,              beta1=(p+1)A+(q-1)B+C,
alpha2=e,              beta2=pA+qB+C,
alpha3=e+A+B,          beta3=e.
```

A subset-dynamic-program permanent calculation gives

```text
T_w=0 for w!=1111,
T_1111=2(p+q)(p-q+1),
```

before and after every affine marking `beta_i -> beta_i+h_i alpha_i`.
The coefficient is nonzero at the generic point.  The exact `P4` component
and generic `H31` dependency replays both pass.

## Exhaustive shared orientation split

Both weighted contractions use one marking `h`, one homogeneous weight, and
one eight-coordinate extension vector `z`.  A weighted-`H22` point requires

```text
M01 z=M23 z=0,
B01 z != 0,
B23 z != 0,
A01 z != 0 or A23 z != 0.
```

The two beta diagonals are the required nonzero pure coefficients.  The final
disjunction expresses that at least one neighbour is genuinely binary.
Consequently, on each projective weight chart, the complete incidence is
covered by exactly two normalized orientations:

```text
A01=1, with B01 and B23 inverted;
A23=1, with B23 and B01 inverted.
```

The contractions are homogeneous linear in the same `z`.  Scaling `z` by the
inverse of the chosen nonzero alpha diagonal justifies either normalization
without changing the shared marking or projective weight.  The inverse
variables explicitly saturate both beta diagonals.  Thus no zero-diagonal or
normalization branch is silently discarded.

## Exact finite `D01` necessary projection

On `[lambda:1]`, first consider only a genuinely binary `D01`: impose its
fourteen mixed equations, normalize `A01=1`, invert `B01`, and eliminate the
extension and inverse coordinate.  Independent bidirectional standard-basis
reduction gives exactly

```text
<h3,h0,F>,
```

where

```text
F = lambda h1 h2 q(q-1)
  + lambda h1 p q(p+1)
  + lambda h2 p(p+1)(q-1)
  + h1 p q(p+q)
  + h2(p+q)(p+1)(q-1)
  + lambda p q(p+1)(q-1).
```

This is scheme-theoretic ideal equality, not merely equality of radicals or
sampled points.

The staged proof uses this projection only as a necessary condition.  Every
actual shared point in the `A01` orientation projects into
`h0=h3=F=0`.  After substituting `h0=h3=0`, the verifier reimposes `F=0`, both
full mixed systems, the `A01=1` normalization, and both beta inversions on the
same extension vector.  Eliminating that restricted shared system gives

```text
finite shared A01 orientation: <1>.
```

Projection closure cannot create a gap here.  Even if `<h3,h0,F>` contained
extra non-liftable closure points, the second unit calculation excludes the
entire closed locus, a superset of all actual shared points.  Sufficiency of
the individual D01 projection is neither assumed nor needed.

## Remaining finite and endpoint orientations

The opposite finite orientation is reconstructed directly, without the
staging step:

```text
finite shared A23 orientation: <1>.
```

The finite chart includes `[0:1]` at `lambda=0`.  At the remaining projective
endpoint `[1:0]`, the verifier rebuilds both direct contraction maps and gets

```text
infinity shared A01 orientation: <1>,
infinity shared A23 orientation: <1>.
```

These four shared unit ideals exhaust both binary orientations on all of
`P1`.  All use the same marking and extension vector; no direction-wise
survivors are combined after the fact.

## Saturation, denominators, and retained timeout

Every contracted coefficient is homogeneous linear in the extension vector,
and all diagonal nonvanishing conditions are represented by explicit inverse
equations.  The eliminations run over `Q(p,q)`, so their only parameter
localization is the stated generic function field.  Divisors such as `p+q=0`
and `p-q+1=0` are special fibres outside the theorem, not denominator cases
filled by this calculation.

The earlier unrestricted individual finite `D23` projection timed out at
120 seconds.  The independent verifier does not rerun it and does not use the
timeout, partial output, or absence of a result as evidence.  The direct
shared `A23` unit calculation is bounded and sufficient.

## Evidence boundary and replay

The proof is exact in characteristic zero.  No finite-field sample, parameter
grid, broad minor enumeration, timeout, or solver exit code is proof.  The
verified `p+q=0` diagonal-DVR wall remains a separate theorem; other
special/projective fibres, pure-`P4` component exhaustiveness, the
arbitrary-order local-to-global reduction, a prize graph, and the global
Krenn–Gu conjecture remain open.

```text
uv run --with sympy python claims/p5/h22/common-active-binary-triangle-component-generic/audit_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py
uv run --with ruff ruff check audit_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py
python -m py_compile audit_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py
python -m json.tool p5_h22_common_active_binary_triangle_component_generic_certificate.json
git diff --check
```

The verifier emits current hashes for this report, itself, the candidate
artifacts, and every theorem dependency.
