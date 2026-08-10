# Verified weighted-`H22` obstruction on every actual diagonal-DVR mask-6 stratum

Discovery run report (before independent verification):

```yaml
role: construction
date_utc: 2026-08-01T11:57:25Z
git_commit: 28cb33964950b9caee96ee0ca8ee8e047d3f4d3c
claim_label: CANDIDATE
scope: weighted H22 on every actual normal-support mask-6 embedded-P3 stratum of the diagonal-DVR p+q=0 wall
inputs:
  p5_h22_p_plus_q_diagonal_dvr_coverage.json: 874272d3d86ec635f1a0bd854b7078b8f91a2323aa1f7ebfb219406680549a6e
  P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md: 667611de1e8bd08dd8c1a5b3b3c431ab57df523f834828c4258d881833b9ee82
  P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md: dfc2ca99ac668605b54a08b2a4dfb48f74abba97ae2ecc405121d21b8e7f3f4a
method: exact characteristic-zero permanent reconstruction in original wall coordinates with the standard 01|23 matching and shared homogeneous weight
command: uv run --with sympy python derive_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_obstruction_candidate.py
outputs:
  derive_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_obstruction_candidate.py: hash reported by replay
  p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_certificate.json: hash reported by replay
  P5_H22_P_PLUS_Q_DIAGONAL_DVR_MASK6_ACTUAL_FREE_PLANES_OBSTRUCTION_CANDIDATE.md: hash reported by replay
limitations: fresh independent replay pending; restricted to the three actual mask-6 diagonal-DVR aggregate strata and their twelve flags; no claim about other projective embedded-P3 points, arbitrary-order local-to-global reduction, component exhaustiveness, a prize graph, or the global Krenn-Gu conjecture
```

## Frozen result

**VERIFIED after a fresh no-import replay:** every actual mask-6 embedded-`P3`
free plane on the verified diagonal-DVR wall has a direct structural
weighted-`H22` obstruction.  The proof uses the original wall coordinates,
the standard `01|23` matching, and one shared homogeneous weight.  It does not
use the refuted projective-chart transport.

Write the source coordinates as `(e,A,B,C)` and put

```text
L=c1 A-c2 B,             M=c1 A+c2 B,             c1*c2 != 0.
```

Every actual open stratum in the frozen coverage ledger has

```text
U1=U2=<e,L>,             U3=<e,M>,
U0=<L,C+xi e+upsilon M>.                              (1)
```

The twelve actual flag instances are:

| aggregate stratum | `xi` | `upsilon` | flags |
| --- | --- | --- | --- |
| finite generic, negative `y` | `eps_x eta` | `-eps_y Delta/2` | all four `(eps_x,eps_y)` |
| finite half-centre, negative `y` | `-eps_x k` | `-eps_y Delta/2` | all four `(eps_x,eps_y)` |
| infinity, `y<-r` | `eps_x kappa` | `-eps_l Delta/2` | all four `(eps_x,eps_l)`, with `eps_u=0` |

The flagged coefficients are nonzero when their flag is one.  The obstruction
below is independent of `xi,upsilon`, so it covers every instance uniformly,
including their intersections.

## Pure restriction and marking orientation

In the wall's natural orientation take

```text
alpha=(L,e,e,e),
beta =(C+xi e+upsilon M,L,L,M).                     (2)
```

Direct order-four permanent expansion has the sole nonzero coefficient

```text
T_1110=-2 c1 c2.                                    (3)
```

Because `c1*c2!=0`, this is projectively the advertised `T_1110=-2` pure
restriction.  To use the standard all-beta marking convention, swap the two
basis vectors inside `U3` only:

```text
alpha=(L,e,e,M),
beta =(C+xi e+upsilon M,L,L,e).                     (4)
```

Then the sole coefficient is `T_1111=-2c1c2`.  The internal plane-basis swap
does not permute source coordinates, tensor modes, the `01|23` matching, or
the homogeneous weight.  Arbitrary markings

```text
beta_i -> beta_i+h_i alpha_i
```

leave (4) pure all-beta and do not change the transverse alpha rows.

## Direct homogeneous contractions

For the shared weight `[rho:sigma]`, reconstruct exactly

```text
D01(z,f)=(rho z0+sigma z1,z2,z3,f),
D23(z,f)=(z0,z1,rho z2+sigma z3,f).                 (5)
```

The four `D01` alpha rows have zero retained `C` target coordinate.  Their
all-alpha matrix therefore has a literal zero column for every independent
extension:

```text
A01=0.                                               (6)
```

For `D23`, the source parts of the alpha rows are

```text
(0,c1,-rho c2), (1,0,0), (1,0,0), (0,c1,rho c2).
```

Expanding the all-alpha permanent along the independent extension column,
the four three-row cofactors are exactly

```text
(0,0,0,0).                                          (7)
```

The middle two vanish because the two `e` rows compete for one target
coordinate; in the other two cofactors the `L/M` contributions cancel.
Hence

```text
A23=0                                                (8)
```

identically in `rho,sigma,c1,c2,xi,upsilon`, all markings, and all extension
coordinates.

A genuine binary `Delta2` image needs both complementary all-alpha and
all-beta diagonal coefficients nonzero.  Equations (6) and (8) show that
neither weighted direction can be binary.  Since an `H22` local map requires
at least one binary direction, no weighted-`H22` pair survives.

This includes `[rho:sigma]=[0:1]`, `[1:0]`, and the open weight torus directly;
there is no affine slope division or endpoint transport.

## Evidence boundary

- The calculation is exact over characteristic zero and uses no grid or
  finite-field audit as proof.
- The machine-readable certificate enumerates all three aggregate unknown
  ledger strata and all twelve actual flags.
- The earlier projective transport remains refuted and is not repaired or
  invoked here.  This candidate instead proves only the actual wall atlas.
- The fresh verifier reconstructs the raw valuation flags, plane atlas, pure
  orientations, and both homogeneous diagonal identities without importing
  the construction script.  Its report is
  `P5_H22_P_PLUS_Q_DIAGONAL_DVR_MASK6_ACTUAL_FREE_PLANES_INDEPENDENT_VERIFICATION.md`.
- No arbitrary-order, component-exhaustiveness, prize-graph, or global
  Krenn--Gu conclusion is made.

## Replay

```text
uv run --with sympy python claims/p5/h22/disputed-ownership/p-plus-q-wall/derive_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_obstruction_candidate.py

uv run --with sympy python claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_independent.py
```

The standalone script verifies the ledger routing, all twelve flags, both
pure-coordinate orientations, arbitrary markings, both homogeneous
contractions, and all eight extension cofactors.  It then prints exact hashes
and limitations.
