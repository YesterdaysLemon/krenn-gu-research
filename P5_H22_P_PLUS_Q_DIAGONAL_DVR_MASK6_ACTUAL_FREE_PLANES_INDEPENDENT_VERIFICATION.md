# Independent verification of the actual diagonal-DVR mask-6 obstruction

```yaml
role: verifier
date_utc: 2026-08-01T12:05:45Z
git_commit: 28cb33964950b9caee96ee0ca8ee8e047d3f4d3c
claim_label: VERIFIED
scope: weighted H22 on the twelve actual normal-support mask-6 embedded-P3 flags of the diagonal-DVR p+q=0 wall
inputs:
  P5_H22_P_PLUS_Q_DIAGONAL_DVR_MASK6_ACTUAL_FREE_PLANES_OBSTRUCTION_CANDIDATE.md: cc0cae9efc70c60acb458449526915104459bac7435a599e5bb54c9802cf7605
  derive_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_obstruction_candidate.py: 5fb47169c683c0dc0e0b1c917c59f51d0399d27e77dc420f4d3567ffb0a2613d
  p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_certificate.json: a77c1ba350cb9cc0f0ca8ee0c7177657c6aabf02272ba2a9904bffa8ff834a7f
  p5_h22_p_plus_q_diagonal_dvr_coverage.json: 874272d3d86ec635f1a0bd854b7078b8f91a2323aa1f7ebfb219406680549a6e
  P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md: 667611de1e8bd08dd8c1a5b3b3c431ab57df523f834828c4258d881833b9ee82
  P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md: dfc2ca99ac668605b54a08b2a4dfb48f74abba97ae2ecc405121d21b8e7f3f4a
  P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md: 7d817f91a5a24512e092dca125258ad5a3753bbb97b6199ad2b6c202c9d91965
method: no-import reconstruction from raw wall excess and leading formulas, explicit witnesses for all twelve flags, independent permanent expansion, and homogeneous all-alpha cofactor identities
command: uv run --with sympy python audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_independent.py
outputs:
  audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_independent.py: hash reported by replay
  P5_H22_P_PLUS_Q_DIAGONAL_DVR_MASK6_ACTUAL_FREE_PLANES_INDEPENDENT_VERIFICATION.md: hash reported by replay
limitations: restricted to the twelve actual flags in the verified diagonal-source-torus p+q=0 wall atlas and the standard 01|23 matching; no arbitrary GL4 source changes, component exhaustiveness, arbitrary-order reduction, prize graph, or global Krenn-Gu conclusion
```

## Verdict

**VERIFIED for the frozen actual-wall claim.**  The verifier imports no
construction code.  It reconstructs the three flag families from the raw
mode-zero wedge formulas, exhibits an admissible valuation witness for every
one of the twelve flags, rebuilds both pure-coordinate orientations, and
computes the two homogeneous all-alpha diagonals with independent extension
coordinates.

The result concerns the actual diagonal-source-torus wall atlas only.  It does
not promote the global conjecture or an arbitrary projective embedded-`P3`
closure theorem.

## Reconstructed twelve-flag atlas

Use source coordinates `(e,A,B,C)` and nonzero `c1,c2,Delta`.  Set

```text
L=c1 A-c2 B,                  M=c1 A+c2 B.
```

Starting from the raw factored mode-zero wedge, the independent calculation
divides by the common leading scalar in each of the three source regimes and
recovers the coefficient tables

```text
generic:  (-eta c1, eta c2, *, -Delta c1c2, c1, -c2),
half:     ( k c1,  -k c2, *, -Delta c1c2, c1, -c2),
infinity: (-kappa c1,kappa c2,*, -Delta c1c2,c1,-c2).
```

The starred `03` coefficient never survives on the strict lower-pair strata.
The exact excesses are

```text
generic:  (x0-d,x0-d,x0-d-y,d+y,0,0),
half:     (x0-d,x0-d,h+x0-d-y,d+y,0,0),
infinity: (x0-d+2r,x0-d+2r,x0-d+r-y,d+y,0,0).
```

For the generic and half-centre families, explicit witnesses with `d=2`,
`y=-2` or `-1`, and `x0=2` or `3` realize every
`(eps_x,eps_y) in {0,1}^2`.  For infinity, `r=-1,d=2`, `y=-2` or `0`, and
`x0=4` or `5` realize every `(eps_x,eps_l)`.  The strict condition `y<-r`
forces `eps_u=0` in all four cases.  Hence the twelve flags are actual, not a
projection closure or formal Boolean enlargement.

For each flag the retained Pluecker vector is reconstructed as the wedge

```text
L wedge (C+xi e+upsilon M),
```

with

```text
generic:  xi= eps_x eta,    upsilon=-eps_y Delta/2,
half:     xi=-eps_x k,      upsilon=-eps_y Delta/2,
infinity: xi= eps_x kappa,  upsilon=-eps_l Delta/2.
```

Thus every flag has the uniform plane configuration

```text
U0=<L,C+xi e+upsilon M>,
U1=U2=<e,L>,
U3=<e,M>.
```

The three oriented normals in the `(e,A,B)` hyperplane are

```text
(0,c2,c1), (0,-c2,-c1), (0,-c2,c1).
```

They give `[C:A:B]=[0:c2:c1]`.  Since `c1*c2!=0`, this is exactly normal
support mask `6`.

## Pure tensor and marking orientation

In the wall orientation

```text
alpha=(L,e,e,e),
beta =(C+xi e+upsilon M,L,L,M),
```

an independent expansion of all sixteen permanents gives the sole nonzero
coefficient

```text
T_1110=-2 c1 c2.
```

Swapping the two basis vectors inside `U3`, without permuting modes, source
coordinates, the `01|23` matching, or the weight, gives

```text
alpha=(L,e,e,M),
beta =(C+xi e+upsilon M,L,L,e).
```

After arbitrary shifts `beta_i -> beta_i+h_i alpha_i`, a second complete
sixteen-coefficient expansion has sole support

```text
T_1111=-2 c1 c2.
```

This establishes the standard all-beta pure orientation uniformly, including
all intersections where `xi` or `upsilon` is zero.

## Homogeneous weighted directions

For arbitrary `[rho:sigma]`, use independent alpha-extension coordinates in
the two directions

```text
D01(z,f)=(rho z0+sigma z1,z2,z3,f),
D23(z,f)=(z0,z1,rho z2+sigma z3,f).
```

Every standard alpha row has `C=0`, so the `D01` all-alpha matrix has a
literal zero third target column.  Its four extension-column cofactors and its
diagonal are identically zero.

For `D23`, the four source parts are exactly

```text
(0,c1,-rho c2), (1,0,0), (1,0,0), (0,c1,rho c2).
```

The middle pair competes for one target coordinate.  When either middle row
is omitted, the remaining `L/M` cofactor is
`c1*rho*c2-rho*c2*c1=0`.  All four cofactors therefore vanish, and

```text
A01=A23=0
```

as polynomial identities in `rho,sigma` and all extension coordinates.  The
verifier substitutes both `[0:1]` and `[1:0]` explicitly.  It also checks that
rescaling the projective representative by nonzero `kappa` is only a monomial
target-coordinate rescaling, so no endpoint or projective-scaling case is
lost.

## Why this excludes `H22`

The exact high-coordinate reduction says that the two marked `H22` slices
map to a pure tensor or to `Delta2`, with at least one mapping to `Delta2`.
The embedded-`P3` weighted definition states that a genuine binary `Delta2`
image needs both complementary all-alpha and all-beta coefficients nonzero.

Since both marked directions have all-alpha coefficient zero, neither can be
genuinely binary.  Therefore no weighted-`H22` point exists on any of the
twelve actual mask-6 flags.

## Evidence boundary

- The proof is exact in characteristic zero and uniform in every free-plane
  coefficient and marking.
- No finite-field calculation, grid search, projective normal-chart transport,
  or affine weight division is used.
- Exhaustiveness of the twelve flags is inherited only from the separately
  verified diagonal-DVR `P4` wall classification; the verifier independently
  reconstructs the flags and their source formulas.
- This does not address non-diagonal source changes, arbitrary projective
  embedded-`P3` points, component exhaustiveness, or the arbitrary-order
  local-to-global reduction.
- The global Krenn--Gu conjecture remains unresolved.

## Replay

```text
uv run --with sympy python audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_independent.py
```

The replay must report `status: pass`, `claim_label: VERIFIED`, twelve actual
flags, normal support mask `6`, both homogeneous all-alpha diagonals zero, and
no global conclusion.
