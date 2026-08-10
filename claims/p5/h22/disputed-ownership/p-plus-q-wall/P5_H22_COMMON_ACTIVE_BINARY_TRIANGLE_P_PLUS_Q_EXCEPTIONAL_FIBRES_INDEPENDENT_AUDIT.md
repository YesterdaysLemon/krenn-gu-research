# Independent audit of the exceptional weighted-`H22` obstruction

## Verdict

**VERIFIED**, restricted to the exceptional `a=0,-1` diagonal-DVR fibres
and the actual lower-pair baseline/wall residue families claimed in
`P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_FIBRES_OBSTRUCTION.md`.
The verdict is conditional on the cited verified `P4` residue classification.

The verifier imports neither the candidate primary, its reconstruction
helper, nor its existing audit.  It builds the planes and every permanent
matrix through a separate subset-DP implementation.

No claim is made for other centres, non-diagonal source transformations,
arbitrary-order gluing, or the global Krenn--Gu conjecture.

## What was attacked

The independent replay checks:

1. the direct `a=0,-1` orientations and their sole pure coefficients;
2. all eight direct finite/infinite `D01` projections and all four parametric
   lower-pair projections by bidirectional characteristic-zero elimination;
3. every actual direct marking line, with complete kernels and fixed
   mode-three minors;
4. the finite endpoint `r=0` on all four direct charts and `r=-lambda` on
   both `B_full` centres by direct complete-kernel rebuilds;
5. baseline and `gamma!=0` wall kernels at finite slope and infinity for
   each of

   ```text
   generic x^2!=y^2, x=0, x=y, x=-y, y=0, x=y=0;
   ```

6. lower-pair diagonal-zero fibres `r=0`, `rt+1=0`, and, on the wall,
   `gamma r+1=0`, separately on every residue stratum;
7. the fixed one-marked minors and their projective `c^3` scaling;
8. the `a=-1` lower-mode/source-sign symmetry and the exact residue map
   `x=(pi-theta)/2`, `y=(pi+theta)/2`.

## Direct exceptional charts

The exact projections have the claimed geometric marking lines

```text
a=0:  h=(0,t,0,0),
a=-1: h=(0,0,t,0).                                  (1)
```

All eight generic finite/infinite kernel calculations reproduce the claimed
ranks, complete nullspaces, diagonals, and fixed mode-three minors.  On the
finite chart, `r=0` has `A=0` on the entire rebuilt kernel for all four
direct fibres.  Direct reconstruction at `r=-lambda` gives `B=0` on the
whole `B_full` kernel at both centres; in particular it confirms rather than
specializes the singular `a=-1` frame.

Thus every projective `D01` slope is covered: finite nonzero slopes by the
fixed minors or direct diagonal-zero rebuild, `r=0` directly, and the
infinity endpoint independently.

## Lower-pair families

The parametric projections over `Q[x,y]` and `Q[x,y,gamma,gamma^-1]` are
exactly

```text
baseline finite/infinity: <h3,h2,h1>,
wall finite:              <h3,h2,h1>,
wall infinity:            <h3,h2,h1,h0>.            (2)
```

The audit does not infer the special residue fibres merely from (2).  It
rebuilds all fourteen mixed rows and complete kernels at every listed
specialization.  The ranks remain six at finite generic slope, five at
infinity, and the fixed mode-one `0137` minors reproduce the claimed
diagonal products.  All direct special-slope kernels have the asserted
identically zero diagonal.

The residue identities

```text
x^2-y^2=-pi theta,
-2y=-(pi+theta)=-Delta                               (3)
```

verify the `x=+/-y`, generic, `y=0`, and origin routing, including the
compulsory last-plane Pluecker coordinate.  The wall computations retain
`gamma` symbolically and explicitly invert it in the projection audit.

## Symmetry and limitations

Swapping the lower tensor modes only permutes permanent rows.  Under the
source sign `e -> -e`, finite `D01` is reparametrized by `r -> -r`; the
infinity contraction changes only by an invertible target-column sign.
This verifies the stated `a=-1` transport without assuming the conclusion.

No finite field, parameter grid, random sample, or broad maximal-minor scan
is used.  Projection ideals remain closures; every geometric branch and
singular slope used in the verdict has a direct complete-kernel check.

The first independent projection replay stopped immediately because the
Singular program used `R` for both the ring and a reduction ideal.  That
identifier collision produced no mathematical evidence.  Renaming the ideal
to `Right` allowed the complete audit to run; the failure is retained here
rather than omitted.

## Run report

```yaml
role: verifier
date_utc: 2026-08-01T10:55:00Z
git_commit: a0764e34b14d56ec76471f646755c067e8cb9ff2
claim_label: VERIFIED
scope: exceptional a=0,-1 direct and actual lower-pair baseline/wall D01 fibres on the verified p+q=0 diagonal-DVR boundary
inputs:
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_FIBRES_OBSTRUCTION.md: 9a496917de3939751ebf434c6403030be6a7822cffcdfa50afd772df30c574c5
  verify_p5_h22_common_active_binary_triangle_p_plus_q_exceptional_fibres_obstruction.py: aa1dc1ff7bd1a0200b3503c3da30f69bacee08e89d6de935b0369cbd24fbbcda
method: independent subset-DP permanents, 12 exact projections, direct complete kernels, fixed minors, symmetry and residue exhaustion
command: uv run --with sympy python claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_common_active_binary_triangle_p_plus_q_exceptional_fibres_independent.py
outputs: this report and its audit script, with sha256 values emitted at replay
limitations: conditional on verified P4 residue classification; no other centres, non-diagonal transformations, arbitrary-order gluing, or global result
```

Replay with

```text
uv run --with sympy python \
  claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_common_active_binary_triangle_p_plus_q_exceptional_fibres_independent.py
```
