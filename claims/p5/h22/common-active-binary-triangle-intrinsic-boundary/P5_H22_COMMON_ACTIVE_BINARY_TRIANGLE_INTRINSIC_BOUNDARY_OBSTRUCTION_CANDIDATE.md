# Candidate weighted-`H22` obstruction on component twenty's intrinsic wall

```yaml
role: construction
date_utc: 2026-08-01T13:27:10Z
git_commit: 3b23ef9e7803dbf9f3e89684971f8707f2d41d7f
claim_label: VERIFIED
discovery_claim_label: CANDIDATE
scope: weighted H22 over the generic point of component twenty's intrinsic wall q=p+1, over Q(p), excluding p=0,-1,-1/2 and component-parameter infinity
inputs:
  P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION.md: ddd3dd8a441db26e6a0fa238842c56ed369133151944a203acc66e3d4bd4ad51
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md: 49149b81ad2a50982d69f03d6e391808ced2beaddff0115f0c86039dd361c823
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md: 52168b35b43c40c483919c8fa1dd37e7c147cae5f331320d8656bf6a1ed309a9
method: direct replacement-basis reconstruction, exact characteristic-zero permanent expansion, and complete normalized projective elimination of the individual and shared weighted incidences
command: uv run --with sympy python derive_p5_h22_common_active_binary_triangle_intrinsic_boundary_obstruction_candidate.py
outputs:
  derive_p5_h22_common_active_binary_triangle_intrinsic_boundary_obstruction_candidate.py: hash reported by replay
  p5_h22_common_active_binary_triangle_intrinsic_boundary_certificate.json: hash reported by replay
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION_CANDIDATE.md: hash reported by replay
limitations: verified after a fresh no-import replay; only the generic point of q=p+1 is covered; p=0,-1,-1/2, component-parameter infinity, mixed source-torus/projective limits, and every unrelated special fibre remain open here; the verified p+q=0 wall is separate; no pure-P4 exhaustiveness, arbitrary-order local-to-global, prize-graph, or global Krenn-Gu claim
```

## Frozen candidate

**VERIFIED after a fresh independent no-import replay:** the weighted-`H22`
fibre over the generic point of component twenty's intrinsic wall
`p-q+1=0` is empty.  In fact, the exact primary and independent replays give
the stronger result that neither weighted contraction has even an individual
genuine binary incidence at any homogeneous weight.

This is a computation over `K=Q(p)` after setting `q=p+1`.  It excludes
`p=0,-1,-1/2` and component-parameter infinity.  The homogeneous-weight
endpoint `[1:0]` is included.  The verifier reconstructed the replacement
basis and all eight elimination systems without importing the discovery
script or certificate.

## Replacement intrinsic basis

The generic component basis collapses on this wall and is not specialized.
Return directly to the two actual rows of `U0` and use

```text
alpha0=-A+B,
beta0 =p(p+1)/(2p+1)e-(2p+1)A+C,

alpha1=e,          beta1=(p+1)A+pB+C,
alpha2=e,          beta2=pA+(p+1)B+C,
alpha3=e+A+B,      beta3=e.                         (1)
```

Exact permanent expansion leaves only

```text
T1111=-2p(p+1).                                     (2)
```

Thus (1) is a valid pure orientation on the frozen open.  Every affine
marking is `betai -> betai+hi alphai`.

## Complete homogeneous-weight cover

For a common extension vector

```text
z=(x0,x1,x2,x3;y0,y1,y2,y3),                       (3)
```

the finite chart `[lambda:1]` uses

```text
D01(v,e)=(lambda v0+v1,v2,v3,e),
D23(v,e)=(v0,v1,lambda v2+v3,e).                   (4)
```

The direct `[1:0]` endpoint retains `v0` in `D01` and `v2` in `D23`.
For each direction let `M` be the fourteen-row mixed matrix and `A,B` its
two diagonal rows.  Normalize `Az=1`, invert `Bz`, and eliminate `z` and the
inverse.  Exact bidirectional standard-basis reduction gives

```text
finite D01 binary projection:   <1>,
finite D23 binary projection:   <1>,
infinity D01 projection:        <1>,
infinity D23 projection:        <1>.               (5)
```

Consequently there are no individual genuine binary survivors anywhere in
the homogeneous weight line.

## Shared incidence replay

For completeness, the replay also reconstructs the full shared system.  It
uses one marking, one homogeneous weight, and the same vector (3), imposes
both mixed systems and both nonzero beta diagonals, and splits on which
all-alpha diagonal is normalized.  The four exact projections are

```text
finite, D01 binary orientation:   <1>,
finite, D23 binary orientation:   <1>,
infinity, D01 binary orientation: <1>,
infinity, D23 binary orientation: <1>.             (6)
```

The two orientations in (6) cover every weighted-`H22` point because at
least one all-alpha diagonal must be nonzero.  Equations (5)--(6) leave no
survivor scheme.

## Retained failed lead and evidence boundary

The possibility that a non-coordinate weighted merge might restore a binary
incidence, despite the four coordinate-deletion obstructions in the `H31`
wall theorem, is `REFUTED` over `Q(p)` by (5).  There were no timed-out or
partial branches, and no sampled grid or all-minor search was run.

- The discovery-agent conclusion was `CANDIDATE`; it is now `VERIFIED` after
  the fresh no-import replay.
- The excluded points `p=0,-1,-1/2`, component-parameter infinity, and mixed
  source-torus/projective limits remain outside this statement.
- The verified `p+q=0` wall is a separate theorem; its intersection here is
  the excluded point `p=-1/2`.
- No component-exhaustiveness, arbitrary-order, prize-graph, or global
  Krenn--Gu claim is made.

## Replay

```text
uv run --with sympy python claims/p5/h22/common-active-binary-triangle-intrinsic-boundary/derive_p5_h22_common_active_binary_triangle_intrinsic_boundary_obstruction_candidate.py
uv run --with sympy python claims/p5/h22/common-active-binary-triangle-intrinsic-boundary/audit_p5_h22_common_active_binary_triangle_intrinsic_boundary_obstruction_candidate.py
```

The standalone replay reconstructs the replacement basis, verifies (2), and
reproduces all eight unit projections in (5)--(6).  Each Singular subprocess
has a fixed 120-second timeout.  The independent audit repeats the same scope
from a separately implemented subset-DP permanent and elimination pipeline.
