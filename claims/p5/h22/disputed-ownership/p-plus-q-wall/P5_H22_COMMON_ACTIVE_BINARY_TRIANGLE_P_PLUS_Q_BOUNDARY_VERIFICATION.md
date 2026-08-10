# Independent verification of the weighted-`H22` `p+q=0` wall obstruction

```yaml
role: verifier
date_utc: 2026-08-01T12:25:17Z
git_commit: e64e3e9ac673e372eb3ecea955934df93ccc90c6
claim_label: VERIFIED
scope: weighted H22 on the complete nine-stratum diagonal-source-torus DVR p+q=0 wall of component twenty
inputs:
  P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md: 667611de1e8bd08dd8c1a5b3b3c431ab57df523f834828c4258d881833b9ee82
  verify_p4_common_active_binary_triangle_p_plus_q_boundary.py: 7273548fb0de4b1f36c05fdc8c184ed68e5633a9f3d290b28bc999d3abd3b371
  audit_p4_common_active_binary_triangle_p_plus_q_boundary.py: 78916f2ecde1ff5428c846ddf3621b934c6c9c7ca3714440177a5c2dc30fa56b
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_PARTIAL.md: abb78c5c92990eb7cabf3538f4231aac489bdb1a79d19fa3ac1a9981f5dfab28
  audit_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial.py: 059b932257ee63f26aa6abbbb2c80014646aa2038c4f3c2997e7581d9bb29499
  audit_p5_h22_common_active_binary_triangle_p_plus_q_b_full_infinity_finite_pair_verifier.py: 1566300e0d007f66b18ac0889a22e2fd9f451601641ea1b9c8392d1814f0046b
  audit_p5_h22_common_active_binary_triangle_p_plus_q_generic_d01_infinity_b_drop.py: 50e6b8015e4bb709c6fbba14188978cdfa1739266f4a5184b81e06d9bae46ff7
  audit_p5_h22_common_active_binary_triangle_p_plus_q_exceptional_fibres_independent.py: 87fd76d0779149d48604e20f4a7be6f6af0731bfb6b874e5cd85b22a9770a290
  audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_candidate_verifier.py: 0319d7144dc00599d4e8179bb0ab986927b7258f516503194c6f440e48ec97ad
  audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_integration_verifier.py: da28f9dd7e34ff2712e38eecdb154a21f4ac4157bfcac911813be39755b79273
  audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_compatibility_obstruction_verifier.py: 052830c0e8347d964fb213c932f79c67d004702fbb0f4dcbd098ad91957a4471
  derive_p5_h22_embedded_p3_component_r_zero_boundary_obstruction.py: b7667f8d89bddb991319bbb0c4248b966f1b085a01640ec55ee6832c6b966355
  audit_p5_h22_embedded_p3_component_r_zero_boundary_independent.py: a23103cfe9fc3a5a065e8734fe225dcd54373f7c47e2021de38950b76c1c94b3
  audit_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_verifier.py: 5c851665189354c5afac5db4d5a3380a6d8a824767d86f1646a3a83af7cbcc5e
  audit_p5_h22_p_plus_q_diagonal_dvr_coverage.py: 803577222c9ebae932581a6166514e469045e72ef7e4e0ecbd9d6944704ab1bb
  derive_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_obstruction_candidate.py: 5fb47169c683c0dc0e0b1c917c59f51d0399d27e77dc420f4d3567ffb0a2613d
  audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_independent.py: 49435463b5d198839d0005a75a4dedd3c5e8902070533c21d5017722dd26641b
  p5_h22_p_plus_q_diagonal_dvr_coverage.json: 874272d3d86ec635f1a0bd854b7078b8f91a2323aa1f7ebfb219406680549a6e
  p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_certificate.json: a77c1ba350cb9cc0f0ca8ee0c7177657c6aabf02272ba2a9904bffa8ff834a7f
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md: 52168b35b43c40c483919c8fa1dd37e7c147cae5f331320d8656bf6a1ed309a9
  verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_obstruction.py: e005093b4736e1154bd1abe28e0c5046b3acf5427daa7d6df919b67b3444ff97
method: fresh Z3 real-linear partition proof, exact ledger/certificate comparison, and direct subprocess replay of every cited mathematical verifier without importing the primary aggregate verifier
command: uv run --with z3-solver python audit_p5_h22_common_active_binary_triangle_p_plus_q_boundary_obstruction.py
outputs:
  audit_p5_h22_common_active_binary_triangle_p_plus_q_boundary_obstruction.py: 5c5ebd204d436d544d810f1567a04eb701b89eeb759975022397d77fd36f4973
limitations: diagonal source tori only; no full embedded-P3 projective closure, non-diagonal or arbitrary GL4 source changes, arbitrary-order reduction, component exhaustiveness, prize graph, or global claim
```

## Verdict

**VERIFIED.**  The nine-stratum list is an exact, disjoint, exhaustive split of
the already verified diagonal-DVR `P4` wall, and every row now has an
independently replayed characteristic-zero weighted-`H22` obstruction.  The
fresh audit imports neither the primary aggregate verifier nor its result.

This proves only that the marked weighted-`H22` fibre is empty on the stated
diagonal-source-torus `p+q=0` wall.  It does not prove a full projective
embedded-`P3` theorem, close any non-diagonal fibre, establish an
arbitrary-order local-to-global reduction, or resolve the Krenn--Gu conjecture.

## Independent nine-stratum exhaustion

The verifier rebuilds the four mutually exclusive centre types from the exact
`P4` valuation conditions and asks Z3 over the reals to prove both coverage and
pairwise disjointness.  It also asks for a witness to every branch, so an empty
cell cannot make the partition pass.

| Centre type | Exact branches | Count |
| --- | --- | ---: |
| finite generic | `y=0,x0=d`; `y=0,x0>d`; `y<0` | 3 |
| finite exceptional `a=0,-1` | the common exact residue schema | 1 |
| finite half-centre `a=-1/2` | `y=0`; `y<0` | 2 |
| infinity | `y<-r`; `y=-r,x0>d-2r`; `y=-r,x0=d-2r` | 3 |

Thus the aggregate count is exactly `3+1+2+3=9`.  The row identifiers,
parameter conditions, and `P4` routes agree coefficient-for-coefficient with
the frozen coverage ledger.  The primary and independent `P4` classification
replays both return `VERIFIED`.

## Six previously closed rows

The audit reruns the actual scripts supporting the historical six-row cover:

- generic `B_full` and `B_drop`: the partial finite-direction certificates and
  separate no-import infinity replays return `VERIFIED`;
- `a=0,-1`: the independent exceptional-fibre audit returns `VERIFIED` for all
  direct and realized lower-pair residue families;
- `a=-1/2,y=0`: the homogeneous Hall obstruction returns `VERIFIED` at both
  projective weight endpoints and on the interior;
- component-14 infinity off-wall: the finite-slope integration and compatibility
  obstruction both return `VERIFIED`;
- component-14 infinity on-wall: the direct endpoint obstruction remains
  verified.

The first component-14 endpoint report remains honestly labelled `REFUTED`
because one stronger exact-rank assertion is false.  Its output confirms that
the survivor boundary did not change.  The aggregate uses only its retained
factor cover and on-wall result together with the two later independent
compatibility verifiers.

## Exact closure of the three historical gaps

The historical coverage replay returns exactly these three `UNKNOWN` ids:

```text
finite_generic_negative_y_embedded_p3
finite_half_centre_negative_y_embedded_p3
infinity_lower_pair_embedded_p3
```

They are exactly the three family ids in the independently verified mask-6
certificate.  For each family the audit checks the full flag square
`(0,0),(1,0),(0,1),(1,1)`, giving twelve actual flags with no duplicates.
The no-import mask-6 replay reconstructs the original wall coordinates and
returns

```text
D01 all-alpha diagonal = 0,
D23 all-alpha diagonal = 0
```

for arbitrary homogeneous weight, including `[0:1]` and `[1:0]`, arbitrary
markings, and independent extensions.  It uses no projective normal-chart
transport.  Consequently the old three-row `UNKNOWN` set is replaced exactly,
not enlarged or inferred from a broader projective statement.

The combined standard-chart `r0=0` divisor theorem also replays as `VERIFIED`,
while retaining the `REFUTED` label on its original endpoint transport proof.
That divisor is not needed for the actual wall closure: the twelve mask-6 flags
are handled directly.  The unrelated full embedded-`P3` projective problem
therefore remains `UNKNOWN` without leaving an actual diagonal-wall gap.

## Replay and QA

```text
uv run --with z3-solver python claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_common_active_binary_triangle_p_plus_q_boundary_obstruction.py
uv run --with ruff ruff check audit_p5_h22_common_active_binary_triangle_p_plus_q_boundary_obstruction.py
python -m py_compile audit_p5_h22_common_active_binary_triangle_p_plus_q_boundary_obstruction.py
git diff --check
```

The verifier emits current hashes for this report, itself, the aggregate draft,
the primary aggregate script, and every independently replayed dependency.
No finite-field computation, bounded parameter grid, broad brute force, or
timeout is used as proof.
