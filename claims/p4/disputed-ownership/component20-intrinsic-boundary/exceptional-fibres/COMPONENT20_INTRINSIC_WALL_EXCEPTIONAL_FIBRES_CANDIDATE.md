# Candidate classification of component twenty's intrinsic-wall exceptions

```yaml
role: construction
date_utc: 2026-08-01T13:58:12Z
git_commit: 00c3574f854e1f86cb8ec2304645204479c3f75e
claim_label: VERIFIED
discovery_claim_label: CANDIDATE
scope: normalized-affine component-twenty intrinsic-wall exceptions (p,q)=(0,1),(-1,0),(-1/2,1/2), including the compactified Segre-direction P1 over the first two zero restrictions; fixed-source straight intrinsic limit only at the half point
inputs:
  P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md: dcaae5365f5e2072e798c2ee52dea47c0d5c48f073ed7553ae5f758e9830f0b2
  P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION.md: ddd3dd8a441db26e6a0fa238842c56ed369133151944a203acc66e3d4bd4ad51
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION_CANDIDATE.md: 62abdc4004a01cc1045ae4ecaf5fe282913b8d817d1f870333653db1e82cf772
  P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md: 667611de1e8bd08dd8c1a5b3b3c431ab57df523f834828c4258d881833b9ee82
  P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md: 04c9498887d2bc3faf16f195f5d7b58a6f901432b4f06b8d508717da6c6ae14a
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md: 52168b35b43c40c483919c8fa1dd37e7c147cae5f331320d8656bf6a1ed309a9
  P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md: eb5a8fb528a9c367ec059a06a5630cbcb533be5c49a4ecd1ee8148cac6644b32
method: direct Grassmann-plane reconstruction, exact squarefree permanents and pair ranks, first-order coefficient-map compactification, and characteristic-zero elimination with the Segre-chart coordinate retained polynomially
command: uv run --with sympy python claims/p4/disputed-ownership/component20-intrinsic-boundary/exceptional-fibres/derive_component20_intrinsic_wall_exceptional_fibres_candidate.py
outputs:
  derive_component20_intrinsic_wall_exceptional_fibres_candidate.py: hash reported by replay
  component20_intrinsic_wall_exceptional_fibres_certificate.json: hash reported by replay
  COMPONENT20_INTRINSIC_WALL_EXCEPTIONAL_FIBRES_CANDIDATE.md: hash reported by replay
limitations: verified after a fresh no-import reconstruction; compactified P1 claims concern normalized-affine Segre incidence over zero restrictions rather than actual nonzero-P4 fibres; p=-1/2 covers only the straight fixed-source intrinsic limit and does not reopen or supersede the verified finite-k and k=0 p+q atlas; no mixed source-torus limits, component-parameter infinity, arbitrary GL4 degeneration, P4 exhaustiveness, arbitrary-order reduction, prize graph, or global Krenn-Gu claim
```

## Outcome

**VERIFIED after a fresh independent no-import reconstruction:** none of the
three exceptional plane tuples is an actual nonzero-`P4` fibre.  The points
`p=0,-1` are regular component-twenty
Grassmann fibres with zero restriction and a full compactified `P1` of
limiting Segre directions.  Every direction on those two `P1` fibres has
empty marked-`H31` and shared weighted-`H22` incidence.  The straight
fixed-source `p=-1/2` limit is instead a zero-tensor rank-two-pair edge at
`k=infinity`, distinct from the already verified nonzero half-centre atlas.

The independent verifier reconstructed the planes, graph closure, all
incidence systems, the half-centre edge, and the component-fifteen arc before
comparing the discovery artifacts.

## The two regular zero restrictions

On `q=p+1`, the actual normalized mode-zero rows are

```text
r0=-A+B,
r1=p(p+1)/(2p+1)e-(2p+1)A+C.                      (1)
```

At `p=0` and `p=-1`, (1) is regular.  Direct reconstruction of all four
planes gives

```text
p=0,q=1:
 U0=< -A+B, -A+C>, U1=<e,A+C>, U2=<e,B+C>, U3=<e+A+B,e>;

p=-1,q=0:
 U0=< -A+B,  A+C>, U1=<e,C-B>, U2=<e,C-A>, U3=<e+A+B,e>.  (2)
```

Every one of the sixteen squarefree permanent coefficients vanishes at both
points.  Exact pair matrices have profile

```text
(3,3,3,3,3,3).                                    (3)
```

Thus these are zero restrictions in the component-twenty closure, not
nonzero pure-`P4` fibres and not lower-pair points.

## Why the compactified fibre is a full `P1`

Before the zero specialization, the only two coefficients in the actual
`(r0,r1)` basis are

```text
(T0111,T1111)=(2(p-q+1),-2q(q-1)).                 (4)
```

Their Jacobians with respect to `(p,q)` have determinants

```text
-4 at (0,1),       +4 at (-1,0).                  (5)
```

Hence every first-order projective coefficient direction `[a:b]` occurs.
Exact realizing arcs are

```text
(0,1):   p=(a-b)t/2,       q=1-bt/2,
(-1,0):  p=-1+(a+b)t/2,    q=bt/2.                (6)
```

Modes one through three retain their common active rows.  In mode zero the
kernel of direction `[a:b]` is

```text
alpha0=b*r0-a*r1.                                  (7)
```

The complete projective cover used in the replay is

```text
[1:rho]: alpha0=rho*r0-r1, beta0=r0,
[0:1]:   alpha0=r0,        beta0=r1.               (8)
```

The finite-chart coordinate `rho` is retained as a polynomial variable over
`Q`; it is never placed in the coefficient field or inverted.  Thus special
Segre directions are included.

This `P1` is compactified Segre incidence over a zero restriction.  It is
relevant because it records every limiting pure factor direction of the
nonzero component-twenty family, but it does not turn either base tuple into
an actual nonzero-`P4` fibre.

## Compactified marked `H31`

For both base points, both charts in (8), and every deletion `d=0,1,2,3`,
the replay normalizes the all-alpha diagonal, inverts the all-beta diagonal,
and eliminates the eight extension coordinates.  All sixteen exact
projections are

```text
<1>.                                               (9)
```

Thus no marked binary neighbour survives anywhere on either compactified
`P1`.

## Compactified weighted `H22`

The complete shared calculation uses one marking, one homogeneous weight,
and the same eight-coordinate extension in both contractions.  It covers
the finite weight `[lambda:1]`, weight infinity `[1:0]`, and both choices of
which all-alpha diagonal is normalized.  For both base points and both
Segre charts, all sixteen shared projections are

```text
<1>.                                               (10)
```

There are two individual finite-`D01` survivor closures, both on the finite
Segre chart.  Their exact projected ideals are

```text
p=0:
 <h3,h0,
   rho*h1*h2*lambda+(rho-1)*h1*lambda
   +(rho-1)*h1+rho*h2>,

p=-1:
 <h3,h0,
   rho*h1*h2*lambda+(-rho-1)*h2*lambda
   -rho*h1+(-rho-1)*h2>.                           (11)
```

Every other individual binary projection is `<1>`.  Equation (11) must not
be called an `H22` survivor: exact same-extension compatibility with the
opposite direction gives (10), so both closures disappear in the shared
incidence.

## The half point is a separate zero edge

At `p=-1/2,q=1/2`, the denominator in (1) vanishes, so direct substitution is
invalid.  Multiply the actual mode-zero Pluecker vector by `delta=2p+1`:

```text
(p(p+1),-p(p+1),0,delta^2,-delta,delta)
  -> (-1/4,1/4,0,0,0,0).                           (12)
```

This gives the straight fixed-source intrinsic limit

```text
U0=<e,A-B>,
U1=<e,C+(A-B)/2>,
U2=<e,C-(A-B)/2>,
U3=<e,A+B>.                                        (13)
```

Its complete tensor is zero and its pair profile is

```text
(3,3,2,3,3,3).                                    (14)
```

The rank-two `03` kernel is exactly

```text
< e tensor e, (A-B) tensor (A+B) >.                (15)
```

An exact nonzero-pure arc with only `T1100=-2*tau` and pair profile
`(3,4,2,4,3,4)` approaches (13); the support-one secant boundary theorem
places that arc in component fifteen.  Thus (13) is a component-twenty
zero-boundary point lying in the component-fifteen closure.

Surgically, (13) is the `k=infinity` edge of

```text
U0=<A-B,C-k e>.                                    (16)
```

It is not one of the finite-`k` or `k=0` nonzero-`P4` half-centre charts in
the verified `p+q=0` atlas.  Those actual diagonal limits remain complete
and already have verified `H31/H22` obstructions.  No new `H31/H22`
calculation is claimed for the zero edge (13), and no additional blow-up
direction at `k=infinity` is asserted.

## Failure and boundary ledger

- The tempting claim that `p=0,-1` remain nonzero pure fibres is `REFUTED`:
  their full tensors vanish.
- The stronger claim that every individual weighted direction is empty is
  `REFUTED` by (11); shared compatibility, not an individual Hall claim,
  proves (10).
- Treating (13) as a missing finite-`k` half-centre chart is `REFUTED`; it is
  the zero-tensor `k=infinity` edge.
- No finite-field inference, parameter grid, random minor scan, or broad
  brute force is used.
- Mixed source-torus limits, component-parameter infinity, arbitrary `GL4`
  degenerations, component exhaustiveness, arbitrary-order reduction, and
  the global Krenn--Gu conjecture remain outside scope.

## Replay

```text
uv run --with sympy python claims/p4/disputed-ownership/component20-intrinsic-boundary/exceptional-fibres/derive_component20_intrinsic_wall_exceptional_fibres_candidate.py
uv run --with sympy --with z3-solver python claims/p4/disputed-ownership/component20-intrinsic-boundary/exceptional-fibres/audit_component20_intrinsic_wall_exceptional_fibres_candidate.py
```

The standalone replay reconstructs (1)--(16), emits fixed pair-rank witnesses
and kernels, verifies the tangent-direction cover, checks the two ideals in
(11) bidirectionally, and reproduces forty-six unit projections: sixteen
`H31`, fourteen remaining individual weighted-binary, and sixteen shared
`H22`.  The independent audit repeats the complete calculation without
importing the discovery implementation.  Every Singular subprocess has a
fixed 120-second timeout.
