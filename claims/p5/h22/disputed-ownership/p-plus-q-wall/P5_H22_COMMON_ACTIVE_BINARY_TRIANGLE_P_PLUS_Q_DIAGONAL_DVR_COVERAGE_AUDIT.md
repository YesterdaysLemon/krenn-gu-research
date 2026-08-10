# Coverage audit for weighted `H22` on the diagonal-DVR `p+q=0` wall

```yaml
role: literature
date_utc: 2026-08-01T11:53:14Z
git_commit: 7b32d942f49043ea433f35aaf10aa7be3af13210
claim_label: UNKNOWN
scope: every actual stratum in the verified diagonal-source-torus p+q=0 valuative boundary of component 20
inputs:
  P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md: 667611de1e8bd08dd8c1a5b3b3c431ab57df523f834828c4258d881833b9ee82
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_PARTIAL.md: abb78c5c92990eb7cabf3538f4231aac489bdb1a79d19fa3ac1a9981f5dfab28
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_GENERIC_D01_INFINITY_OBSTRUCTION.md: 60afe02d4327ec93770f29bc4de8bad2592053257bf021a3c45084306508aa90
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_B_FULL_INFINITY_FINITE_PAIR_VERIFICATION.md: 67427504ed7f78eee119b73f88c1c045ad7a2927556f8b8eb97e8668dc5536df
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_GENERIC_D01_INFINITY_B_DROP_AUDIT.md: 34f7cb79ac6f62e7f770bea8de34a27b83dfc59a1df91616b54fc728d8d83773
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_FIBRES_INDEPENDENT_AUDIT.md: 2a66c7a87b903167a213644fd198bdcab3b0909539014f0df7e8aa6855212138
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_INDEPENDENT_VERIFICATION.md: 5ac8f47b5d7d6cbfc5867630e57ab63ef1ed8772009a7146326c1994d6805b98
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_COMPATIBILITY_OBSTRUCTION_VERIFICATION.md: 6419b739f275abe528f3c30a3b5fdd8af1d19e4fc94914c3c87b3522db0e8774
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_INTEGRATION_VERIFICATION.md: 101563d2edc322ada1428d5261952a29452c01eae1d2ff068913214326c139eb
  P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md: dfc2ca99ac668605b54a08b2a4dfb48f74abba97ae2ecc405121d21b8e7f3f4a
  P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md: baf5531740cfd77207f31cf8e1de2b5b838701cbcae5ec778667e6e7f712d15e
  P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md: 7ae8c19e5a43ac7af2cac35892af59130555ab509495d5280745aad114eed056
  P5_H22_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_VERIFICATION.md: b83ddbe1e1f928dd18b9914c2c3433e612e315096888023a343af62ddf52c5c7
  P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_VERIFICATION.md: 55ccdd6cbce892a1171a71f0bbb5e8c04241cb269c98ac797dbdf85e96f4f38b
  P5_H22_EMBEDDED_P3_COMPONENT_R_ZERO_T_NONZERO_WEIGHT_ENDPOINTS_VERIFICATION.md: 8e4cbe9b66bd1e53f374ef36e9fd257b410014297d9760cdf5472598f505d838
  audit_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_verifier.py: 5c851665189354c5afac5db4d5a3380a6d8a824767d86f1646a3a83af7cbcc5e
method: source-to-stratum coverage map, exact support-mask calculation for actual embedded-P3 arcs, frozen-byte audit, and replay of the new endpoint verifier
command: |
  uv run --with sympy python claims/p5/h22/embedded-p3/audit_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_verifier.py
  python claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_p_plus_q_diagonal_dvr_coverage.py
outputs:
  p5_h22_p_plus_q_diagonal_dvr_coverage.json: 874272d3d86ec635f1a0bd854b7078b8f91a2323aa1f7ebfb219406680549a6e
  audit_p5_h22_p_plus_q_diagonal_dvr_coverage.py: 803577222c9ebae932581a6166514e469045e72ef7e4e0ecbd9d6944704ab1bb
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_DIAGONAL_DVR_COVERAGE_AUDIT.md: hash reported by the coverage audit consumer
limitations: dependency audit rather than a replay of every cited theorem; restricted to diagonal source tori; normal-mask-6 matching/projective transport, arbitrary-order reduction, and the global Krenn-Gu conjecture remain UNKNOWN
```

## Verdict

The whole diagonal-DVR `p+q=0` weighted-`H22` wall remains **UNKNOWN**.
Six of the nine aggregate arc strata have scoped characteristic-zero
certificates.  The remaining three are exactly the nonexceptional strata
routed by the `P4` classification to the embedded-`P3` support-two closure.

The newly verified `r0=0,t0!=0` homogeneous weight endpoints complete the
previously missing endpoints on the standard normalized free-plane divisor.
They do **not** close the actual wall.  Every open wall family has normal
support mask 6, and the independent projective audit already showed that
mask 6 cannot be moved into the certified standard chart while simultaneously
preserving the ordered `01|23` matching and its shared homogeneous weight.

## Exhaustive stratum map

| Actual arc stratum | `P4` route | Weighted-`H22` status | Exact certificate or gap |
| --- | --- | --- | --- |
| Generic finite centre, `y=0,x0=d` | `B_full` | `VERIFIED` | finite `D01` certificate plus independent `D01`-infinity replay |
| Generic finite centre, `y=0,x0>d` | `B_drop` | `VERIFIED` | finite `D01` certificate plus independent `S1/S2` `D01`-infinity replay |
| Generic finite centre, `-d<=y<0,x0>=d` | embedded `P3`, all four `(eps_x,eps_y)` faces | `UNKNOWN` | actual normal mask 6; matching/shared-weight projective transport absent |
| `a=0,-1`, every direct `y=0` and realized lower-pair `y<0` residue family | direct exceptional / component 15 | `VERIFIED` | independent audit covers all finite/infinite `D01` slopes, baseline/wall residues, and special diagonal-zero slopes |
| Half centre `a=-1/2`, `y=0`, both `x0=d` and `x0>d` | replacement family | `VERIFIED` | homogeneous Hall-support obstruction |
| Half centre `a=-1/2`, `-d<=y<0,x0>=d` | embedded `P3`, all four `(eps_x,eps_y)` faces | `UNKNOWN` | same actual mask-6 projective/matching gap |
| Infinity, `-d<=y<-r,x0>=d-2r` | embedded `P3`, four `(eps_x,eps_l)` faces with `eps_u=0` | `UNKNOWN` | same actual mask-6 projective/matching gap |
| Infinity, `y=-r,x0>d-2r` | component-14 off-wall `gamma=0` endpoint | `VERIFIED` | infinity branches, finite-slope integration to `D23,r=0`, and compatibility obstruction |
| Infinity, `y=-r,x0=d-2r` | component-14 on-wall `gamma=2` endpoint | `VERIFIED` | direct finite/infinite `D01` obstruction and empty `D23` infinity |

The component-14 base audit is `REFUTED` overall because its claim that every
genuine `D23,r=1/2` kernel has rank exactly three is false.  This map uses
only its explicitly verified endpoint tensors, marking projections, on-wall
obstruction, and projective infinity subclaims, together with the later
independently verified compatibility and integration steps.

## Why the actual embedded strata are mask 6

For every generic, half-centre, and infinity lower-pair arc routed to the
embedded component, the last three planes have the form

```text
U1=U2=<e,c1 A-c2 B>,       U3=<e,c1 A+c2 B>,       c1 c2 != 0.
```

In the common hyperplane basis `(e,A,B)`, choose normals

```text
n1=(0,c2,c1),
n2=(0,-c2,-c1),
n3=(0,-c2,c1).
```

They are exactly the sign-rectangle presentation

```text
n1=(C,A,B), n2=(C,-A,-B), n3=(C,-A,B)
```

at

```text
[C:A:B]=[0:c2:c1].
```

Since `c1*c2!=0`, this is support mask 6, not the full-support normal chart
used by the normalized affine and `r0=0` free-plane theorems.  The coverage
audit reconstructs these annihilating normals directly.

## Effect of the new endpoint verification

The exact replay

```text
uv run --with sympy python \
  claims/p5/h22/embedded-p3/audit_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_verifier.py
```

returned `status: pass`, `claim_label: VERIFIED`, and
`both_endpoint_fibres_obstructed: true`.  Its frozen report hash is
`8e4cbe9b66bd1e53f374ef36e9fd257b410014297d9760cdf5472598f505d838`;
the replay script hash is
`5c851665189354c5afac5db4d5a3380a6d8a824767d86f1646a3a83af7cbcc5e`.
It uses no finite-field computation as proof.

Together with the independently supported `t0=0` corner and the invertibly
rebalanced `t0!=0,rho*sigma!=0` transport, this fills the `r0=0` divisor in
the standard normalized normal chart.  It does not repair either of the
separate failures found by the projective-closure audit:

1. support mask 6 has no certified chart change preserving the `01|23`
   matching;
2. the shared ordered homogeneous weight must also be transported at both
   projective endpoints.

No coefficientwise atlas map from all actual mask-6 arc free planes to a
certified weighted chart exists in the current files.  Even if individual
planes happen to meet a normalized subchart, that has not been exhausted or
certified stratum by stratum.

## Exact closure criterion

Closing only the newly isolated free-plane endpoint fibres does **not** close
the diagonal-DVR wall.  A genuinely full projective embedded-`P3`
weighted-`H22` theorem would close all remaining wall strata, provided it
does one of the following without changing the problem:

- proves the obstruction directly on normal support mask 6 for arbitrary
  actual free planes and every homogeneous shared weight; or
- gives an exact atlas transport from mask 6 to a certified chart that
  preserves the ordered `01|23` matching, the common weight including both
  endpoints, markings, extensions, and genuineness.

Once that is supplied, the table above has no other unmapped diagonal-DVR
stratum.  This remains only a local order-five wall statement: arbitrary
source `GL4`, arbitrary-order local-to-global reduction, component
exhaustiveness, and the global Krenn--Gu conjecture are outside scope.

## Coverage replay

```text
python claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_p_plus_q_diagonal_dvr_coverage.py
```

The replay checks all 16 frozen dependency hashes and status markers, checks
the nine-stratum ledger with exactly six `VERIFIED` and three `UNKNOWN`
entries, reconstructs the actual normal support mask 6, and emits the
machine-readable result.  It is a dependency/coverage audit, not a substitute
for the cited characteristic-zero mathematical verifiers.
