# Weighted-`H22` obstruction on the `p+q=0` boundary of component twenty

## Status

**VERIFIED after a fresh independent aggregate audit.**  The exact
characteristic-zero certificates cited below obstruct weighted `H22` on all
nine actual strata in the independently verified diagonal-source-torus DVR
classification of the `p+q=0` boundary.  The no-import aggregate replay is
recorded in
`P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_VERIFICATION.md`.

This is a theorem only about the diagonal-DVR wall classified in
`P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md`.  It does not close the
full projective embedded-`P3` component, non-diagonal or arbitrary `GL4`
source changes, the arbitrary-order local-to-global reduction, or the global
Krenn--Gu conjecture.

## Exhaustive stratum integration

The pre-closure coverage audit froze nine aggregate arc strata.  Six already
had verified certificates, and exactly three actual embedded-`P3` mask-6
strata remained.  The direct mask-6 theorem now closes those twelve flag
instances without projective transport.

| Actual arc stratum | Exact route | Weighted-`H22` certificate |
| --- | --- | --- |
| generic finite, `y=0,x0=d` | `B_full` | finite and infinite `D01` obstruction |
| generic finite, `y=0,x0>d` | `B_drop` | finite and infinite `D01` obstruction |
| generic finite, `-d<=y<0` | actual embedded `P3`, four mask-6 flags | both all-alpha diagonals vanish |
| `a=0,-1`, all actual finite residues | direct charts and component 15 | exceptional-fibre `D01` obstruction |
| `a=-1/2`, `y=0` | replacement family | homogeneous Hall obstruction |
| `a=-1/2`, `y<0` | actual embedded `P3`, four mask-6 flags | both all-alpha diagonals vanish |
| infinity, `-d<=y<-r` | actual embedded `P3`, four mask-6 flags | both all-alpha diagonals vanish |
| infinity, `y=-r,x0>d-2r` | component-14 off-wall endpoint | slope forcing plus compatibility obstruction |
| infinity, `y=-r,x0=d-2r` | component-14 on-wall endpoint | complete projective `D01` obstruction |

The exact dependency map before the mask-6 theorem is
`p5_h22_p_plus_q_diagonal_dvr_coverage.json`.  Its three `UNKNOWN` identifiers
are exactly the three identifiers in
`p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_certificate.json`.
That certificate enumerates four actual flags for each identifier, and the
independent mask-6 verifier reconstructs every flag from the raw valuation
formulas.

## Evidence boundaries retained

- The original component-14 endpoint analysis is `REFUTED` only in its
  stronger assertion that every genuine `D23,r=1/2` survivor has rank exactly
  three.  The exact rank-two subfamily does not change the survivor cover;
  later independent slope-forcing and compatibility certificates close the
  endpoint.
- The original embedded-`P3` full-divisor transport is `REFUTED` at the two
  homogeneous weight endpoints.  Separate original-coordinate certificates
  close those endpoints and verify the standard-chart `r0=0` divisor.
- The overstrong full projective embedded-`P3` closure remains `UNKNOWN` on
  unrelated normal-mask, Grassmann-pivot, and orientation-endpoint strata.
  The wall theorem needs only the actual mask-6 atlas, which is reconstructed
  directly.
- No finite-field computation, parameter grid, broad graph search, or timeout
  is used as proof.

## Focused replay

```text
uv run --with sympy python verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_obstruction.py
uv run --with z3-solver python audit_p5_h22_common_active_binary_triangle_p_plus_q_boundary_obstruction.py

uv run --with sympy python audit_p5_h22_p_plus_q_diagonal_dvr_coverage.py
uv run --with sympy python derive_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_obstruction_candidate.py
uv run --with sympy python audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_independent.py

uv run --with sympy python derive_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_candidate.py
uv run --with sympy python audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_integration_verifier.py
uv run --with sympy python audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_compatibility_obstruction_verifier.py
```

The primary and independent aggregate verifiers emit complete run reports
with current hashes, the nine-stratum status map, the twelve mask-6 flags, and
all limitations.
