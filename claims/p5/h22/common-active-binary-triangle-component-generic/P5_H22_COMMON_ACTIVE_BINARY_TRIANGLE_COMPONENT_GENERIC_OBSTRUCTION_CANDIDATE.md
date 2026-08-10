# Candidate generic weighted-`H22` obstruction for component twenty

```yaml
role: construction
date_utc: 2026-08-01T13:14:31Z
git_commit: f089d5bc9f9a9f0c3550d6e0f9ca2686a8fb55f4
claim_label: VERIFIED
discovery_claim_label: CANDIDATE
scope: generic weighted H22 fibre of component twenty, the common-active binary triangle, over Q(p,q); the p+q=0 wall and every other special parameter divisor are excluded
inputs:
  P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md: dcaae5365f5e2072e798c2ee52dea47c0d5c48f073ed7553ae5f758e9830f0b2
  P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md: 73596e624c6a6e093b861b5c366582cd4b61bc39197d01690f295c9e7194722c
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md: 52168b35b43c40c483919c8fa1dd37e7c147cae5f331320d8656bf6a1ed309a9
method: exact characteristic-zero permanent reconstruction and staged projective elimination for one shared marking, homogeneous weight, and extension vector
command: uv run --with sympy python derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py
outputs:
  derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py: hash reported by replay
  p5_h22_common_active_binary_triangle_component_generic_certificate.json: hash reported by replay
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md: hash reported by replay
limitations: verified after a fresh no-import replay; generic function-field calculation only; the separately verified p+q=0 diagonal-DVR wall is not recomputed or used to fill the generic proof; no claim about other special/projective component fibres, pure-P4 component exhaustiveness, arbitrary-order local-to-global reduction, a prize graph, or the global Krenn-Gu conjecture
```

## Frozen candidate

**VERIFIED after a fresh independent no-import replay:** the generic
weighted-`H22` fibre of component twenty is empty.  The exact primary and
independent replays return the unit ideal in every shared finite/infinity
orientation branch.

The calculation is over the function field `K=Q(p,q)`.  In particular, it
does not overlap the separately verified `p+q=0` diagonal-DVR wall.  Every
other special parameter divisor and projective component-boundary fibre is
also outside this generic statement.  No finite-field inference or parameter
grid is used.

## Intrinsic pure basis

Put `s=p-q+1` and use the component-twenty orientation

```text
alpha0=-p(p+1)A+q(q-1)B+sC,
beta0 =-s e-(p+q)A+(p+q)B,

alpha1=e,              beta1=(p+1)A+(q-1)B+C,
alpha2=e,              beta2=pA+qB+C,
alpha3=e+A+B,          beta3=e.                    (1)
```

Direct permanent expansion gives only

```text
T1111=2(p+q)s.                                      (2)
```

Every affine marking is `betai -> betai+hi alphai`.

## One shared weighted-`H22` system

For a common extension vector

```text
z=(x0,x1,x2,x3;y0,y1,y2,y3),                       (3)
```

the finite homogeneous chart `[lambda:1]` uses

```text
D01(v,e)=(lambda v0+v1,v2,v3,e),
D23(v,e)=(v0,v1,lambda v2+v3,e).                   (4)
```

At `[1:0]`, the direct maps retain `v0` in `D01` and `v2` in
`D23`.  Both directions use the same marking, weight, and vector (3).

Let `M01,M23` be the fourteen mixed-coefficient matrices, and let
`A01,B01,A23,B23` be the all-alpha and all-beta diagonal rows.  A common
weighted-`H22` point satisfies

```text
M01 z=M23 z=0,       B01 z != 0,       B23 z != 0,
(A01 z != 0 or A23 z != 0).                         (5)
```

Thus two normalized orientations cover the complete incidence: normalize
`A01 z=1`, or normalize `A23 z=1`.  The two nonzero beta diagonals are
saturated independently in both branches.

## Staged finite `D01` projection

Before imposing the second contraction, normalize `A01 z=1`, invert
`B01 z`, and eliminate the extension.  Bidirectional standard-basis
reduction gives the exact marking projection

```text
<h3,h0,F>,                                          (6)
```

where

```text
F = lambda*h1*h2*q*(q-1)
  + lambda*h1*p*q*(p+1)
  + lambda*h2*p*(p+1)*(q-1)
  + h1*p*q*(p+q)
  + h2*(p+q)*(p+1)*(q-1)
  + lambda*p*q*(p+1)*(q-1).                        (7)
```

Substitute `h0=h3=0`, impose `F=0`, then add `M23 z=0` and invert
`B23 z` on the same vector.  Exact elimination returns

```text
finite, A01-normalized shared branch: <1>.          (8)
```

This staging loses no common point because (6) is a necessary condition for
every finite point with `A01 z != 0`.

## Remaining projective branches

The opposite finite orientation needs no preliminary projection.  Normalize
`A23 z=1`, invert both beta diagonals, and eliminate the common extension:

```text
finite, A23-normalized shared branch: <1>.          (9)
```

At the homogeneous endpoint `[1:0]`, direct reconstruction gives

```text
infinity, A01-normalized shared branch: <1>,
infinity, A23-normalized shared branch: <1>.       (10)
```

Equations (8)--(10), together with the orientation cover (5), leave no
generic survivor scheme.

## Retained failed route

An initial unrestricted projection of the individual finite `D23` binary
incidence exceeded its fixed 120-second timeout.  It is not evidence and is
not needed by (8)--(10).  No task-related exploration or Singular process
remained afterward.

A bounded fixed-minor reconnaissance on the restricted `D01` locus recovered
`F` as a factor of one rank witness, but additional sampled minors became
large.  That route was abandoned before any broad minor enumeration.  None
of those sampled minors is used in this candidate; the exact staged shared
projections close the incidence directly.

## Evidence boundary

- The construction-agent discovery was `CANDIDATE`; a fresh verifier has now
  independently reconstructed and promoted the exact claim to `VERIFIED`.
- The verified `p+q=0` wall theorem remains separate and is not inferred from
  the function-field calculation.
- No special parameter or projective component-boundary fibre is classified
  here.
- The result makes no component-exhaustiveness, arbitrary-order, prize-graph,
  or global Krenn--Gu claim.

## Replay

```text
uv run --with sympy python claims/p5/h22/common-active-binary-triangle-component-generic/derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py
uv run --with sympy python claims/p5/h22/common-active-binary-triangle-component-generic/audit_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py
```

The standalone replay reconstructs (1)--(4), checks the pure support,
verifies the bidirectional equality in (6), and reproduces the four unit
ideals in (8)--(10).  The independent verifier repeats the argument without
importing the discovery script.  Every Singular subprocess has a 120-second
timeout.
