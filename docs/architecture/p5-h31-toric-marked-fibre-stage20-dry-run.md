# P5 H31 toric marked fibre - Stage 20 exact migration dry run

Status: **APPROVED FOR AN EXACT FROZEN BATCH under the repository-owner
standing delegation dated 2026-08-08. No move has yet been executed.**

> **Scientific status will not change.** The global Krenn-Gu conjecture
> remains **UNRESOLVED**. This review resolves filesystem ownership only. It
> does not extend the first-component toric result to the projective interior,
> a second or further component, component exhaustiveness, weighted `H22`,
> `P5 -> Delta3`, or the global prize problem.

## Review authority and audited baseline

- Exact merged baseline:
  `0c368f1f0b1467ccb2ab2e57517ce742aa2bf9ec`.
- Branch: `codex/stage20-h31-toric-marked-fibre-migration`.
- Actual mapping reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.
- Delegated-review test: routine, non-ambiguous, evidence-backed exact layout
  mapping; no scientific status/scope decision, ambiguous proof-boundary
  decision, or owner-preference architecture choice is required.
- Batch ID to freeze: `p5-h31-toric-marked-fibre-stage20`.
- Approval-time raw Windows-checkout manifest SHA-256:
  `1398c2c84219d32cd26c50e68d4315f448a84d3cee8723cdb1a068bf0e566d30`.
- Canonical mapping SHA-256:
  `48c99b929b824d4cf5709406aa846beb4a3f47cf18f570e936910ee9408621a2`.

The manifest hash is informational approval-time provenance over raw CRLF
checkout bytes. The canonical mapping hash is the portable authority for the
reviewed old-to-new pairs.

All three records are currently `review_required` with medium classifier
confidence. Classifier confidence is proposal evidence only. Approval comes
from independent proof-topology/status and mechanical/consumer audits and
applies only to the mapping below.

## Exact three-file mapping

All three files move flat into `claims/p5/h31/toric-marked-fibre/`.

| role | source | destination |
|---|---|---|
| theorem | `P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md` | `claims/p5/h31/toric-marked-fibre/P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md` |
| characteristic-zero primary | `verify_p5_h31_toric_marked_fibre_obstruction.py` | `claims/p5/h31/toric-marked-fibre/verify_p5_h31_toric_marked_fibre_obstruction.py` |
| modular audit | `audit_p5_h31_toric_marked_fibre_obstruction.py` | `claims/p5/h31/toric-marked-fibre/audit_p5_h31_toric_marked_fibre_obstruction.py` |

Every source is tracked grandfathered root debt, every destination is absent,
and the durable classifier and generated manifest contain exactly these
source-to-destination pairs. There are no selected duplicate sources or
destinations, destination collisions, double moves, overlap cycles, or
package-name collisions.

The exact baseline Git blobs are:

| source | Git blob |
|---|---|
| `P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md` | `f6e7ccccf1a2f4dc7a2273fe7db35993084e6b76` |
| `audit_p5_h31_toric_marked_fibre_obstruction.py` | `c47068780b92e2f2e40d1a24882a440ba1535855` |
| `verify_p5_h31_toric_marked_fibre_obstruction.py` | `8707cd9f08a79dcdfd31a0b1ad7c0dbd0fad5b7e` |

## Proof-obligation ownership

The selected triple is one complete first-component toric-boundary proof
leaf:

```text
P4 first pure-rank-two component toric faces + exact Segre slice reduction
  -> 5 genuine divisor orbits + 4 genuine edge orbits
  -> 21 base-orbit/orientation cases
  -> 17 pure-direction types / 39 direction-orientation types
  -> both first-plane charts, every row shift, every binary extension
  -> 78 characteristic-zero projection/ledger runs
  -> 78 selected-obstruction unit ideals with 438 transverse products
  => the complete marked H31 fibre on the genuine toric base boundary
     of the first/known component is empty

projective interior, second/further components, exhaustiveness,
P5 -> Delta3, weighted H22, gluing, and global remain outside this leaf
```

The internal `E=0` divisor and projective first-plane interior boundary are
separately owned results. They are not members needed to prove this toric
leaf. The selected theorem owns exactly the displayed toric orbit cover; it
is not a generic whole-component theorem.

Evidence roles remain distinct:

- the theorem and primary give the exact characteristic-zero unit-ideal
  obstruction;
- the primary reconstructs the first-component toric/Segre data and all 78
  projection plus 78 selected-obstruction runs;
- the `F5/F7` audit does not import the primary and independently computes
  modular kernels, projective extension directions, and marked-minor tests;
- the audit nevertheless shares `toric_cases` / `marked_rows`, reused modular
  marked-basis primitives, and hard-coded projection/certificate-selection
  data, so independence is claimed only downstream of that shared
  construction/data layer; and
- modular enumeration is QA, not the characteristic-zero proof.

No selected artifact has a curated theorem-ledger entry. Migration adds no
entry and changes no mathematical status, assumptions, scope, evidence role,
lifecycle, or global-status field.

## Conflict boundary and explicit exclusions

The selected theorem and its P4 toric-boundary input contain checkpoint-era
prose saying that a second diagonal-quadric or further components remain
open. Other synthesis artifacts record conflicting closure language. Both
sides substantially originate in commit `60a885ca`; recency cannot resolve
the conflict. The combined Stages 17-19 audit records the exact provenance in
[`layout-migration-stages17-19-program-audit.md`](layout-migration-stages17-19-program-audit.md).

That conflict does not block this mapping:

- the proof consumes only first-component toric/Segre geometry;
- disputed second-component sentences are not mathematical premises;
- whole-document hashes are provenance, not a specialization or status edge;
- the pure move preserves all three blobs; and
- repair changes only paths, commands, navigation, and mechanically derived
  hashes.

Stage 20 neither endorses, reopens, nor promotes either side of the broader
conflict. The primary's `additional_components_closed: false` is scope-local:
this verifier establishes no additional-component theorem.

The following remain separately owned:

- `derive_p5_h31_toric_marked_fibre_elimination.py`, which also serves the
  migrated internal-`E=0` primary and audit;
- the shared high-coordinate, marked-basis-primary, and marked-basis-audit
  helpers;
- the P4 component, toric-boundary, and Segre theorems and their replays;
- the projective interior and internal-`E=0` packages;
- second/further components and component exhaustiveness;
- weighted `H22`, `P5 -> Delta3`, arbitrary-order gluing, and global work.

## Mechanical repair surface

Both selected scripts currently derive `ROOT` from repository root and import
root modules before any bootstrap. After the pure move:

- both install shared `krenn_gu.bootstrap` before bare root imports;
- `REPO_ROOT, HERE = bootstrap(__file__)` supplies stable ownership;
- the selected theorem and the audit's sibling primary resolve from `HERE`;
- P4 toric/Segre documents, the shared generator, and shared root helpers
  resolve through `REPO_ROOT`; and
- emitted replay commands use full destination-relative paths.

Exactly one staying Python consumer needs one operational retarget:
`verify_p5_high_coordinate_partial_frontier.py` must point its toric theorem
dependency at the destination. No staying module importer or subprocess
caller targets either selected script name.

The deterministic virtual post-move rewriter predicts exactly 11
Markdown-link rewrites and two fenced replay-command rewrites across ten
Markdown files, with zero ambiguities and zero theorem-ledger relocations.
The selected theorem receives two reanchored P4 links and two full replay
commands. Staying rewrites touch the root README, alternative strategy map,
component-fibre-infinity document, marked-basis classification/open
documents, high-coordinate frontier, and the migrated P4 component,
toric-slice, and toric-boundary documents.

Four existing ledger hashes must refresh mechanically while all statuses and
semantic fields remain fixed:

- the three root-README entries from `0a2bdc3d8f298425` to projected
  `8b8d7ee9a4cfe4ac`; and
- the verified high-coordinate entry from `438f42c953f13628` to projected
  `56b23fe36b5d97d8`.

Navigation must add a distinct non-generic toric marked-fibre section to
`claims/p5/h31/README.md`, record the batch/mapping hash and shared-helper
boundary, and update H31 package directories from 27 to 28. Parent P5
navigation must add the scoped fifth exception without implying a complete
component theorem.

## Projected transitions

| measure | before | after |
|---|---:|---:|
| manifest `moved` | 389 | 392 |
| manifest `proposed_high_confidence` | 243 | 243 |
| manifest `review_required` | 1,383 | 1,380 |
| moved-only manifest root projection | 1,983 | 1,980 |
| high-confidence manifest root projection | 1,740 | 1,737 |
| all-classified manifest root projection | 357 | 357 |
| measured root files | 1,975 | 1,972 |
| measured root directories | 9 | 9 |
| measured root entries | 1,984 | 1,981 |
| grandfathered root debt | 1,968 | 1,965 |
| enforceable retired paths | 389 | 392 |

The move creates no top-level directory and changes no root baseline or
end-state allowlist.

## Exact baseline replay

Fresh serial replay on exact audited main passed once per executable. The
first valid JSON results were preserved; no solver rerun was triggered by a
post-parse assertion.

The characteristic-zero primary returned rc=0 and empty stderr in 201.639
seconds (emitted elapsed 200.751 seconds):

- 17 direction types, 39 orientation types, and 21 base-orbit cases;
- two charts;
- 78 projection/ledger and 78 selected-obstruction runs;
- 18 binary-empty orientation/chart runs and 438 selected products;
- all binary extensions excluded and genuine toric marked fibre closed;
- projective interior boundary false;
- additional components false; and
- global false.

The modular audit returned rc=0 and empty stderr in 69.267 seconds:

| field | `F5` | `F7` | total |
|---|---:|---:|---:|
| projection points | 3,738 | 9,326 | 13,064 |
| projection-closure artifacts | 170 | 350 | 520 |
| binary extensions | 46,976 | 225,648 | 272,624 |
| marked-minor tests | 51,008 | 240,168 | 291,176 |

Its global field remains false. Native Singular is absent; the existing WSL
Singular 4.3.2 fallback completed the characteristic-zero elimination.

## Post-move acceptance matrix

Use a checked schema-aware assertion manifest and preserve each first rc=0,
empty-stderr, valid-JSON output before semantic assertions. A wrapper error
must not automatically launch an expensive solver rerun or become
mathematical evidence.

Run the moved primary and audit from repository root by destination-relative
path and from a fresh foreign working directory by absolute path under
`uv run --with sympy --with python-sat python -I`. Compare each pair exactly,
removing only the primary's volatile `elapsed_seconds`. Require the exact
counts and conservative false fields above. Run the staying high-coordinate
primary from root and foreign CWD and preserve its current scientific fields.

Rewritten evidence-document bytes create a 27-executable hash/provenance
matrix. Replay all of the following, using disposable copies for scripts that
write ignored or tracked outputs:

1. moved toric marked-fibre primary;
2. moved toric marked-fibre audit;
3. `claims/p4/classifications/pair-geometry/pure-rank-two/boundaries/verify_p4_pure_rank_two_component_toric_boundary.py`;
4. `claims/p4/classifications/pair-geometry/pure-rank-two/boundaries/audit_p4_pure_rank_two_component_toric_boundary.py`;
5. `claims/p4/classifications/pair-geometry/pure-rank-two/verify_p4_pure_rank_two_toric_slice_segre.py`;
6. `claims/p4/classifications/pair-geometry/pure-rank-two/audit_p4_pure_rank_two_toric_slice_segre.py`;
7. `claims/p4/classifications/pair-geometry/pure-rank-two/verify_p4_pure_rank_two_component.py`;
8. `claims/p4/classifications/pair-geometry/pure-rank-two/audit_p4_pure_rank_two_component.py`;
9. `claims/p4/classifications/pair-geometry/pure-rank-two/verify_p4_pure_rank_two_component_chart_closure.py`;
10. `claims/p4/components/diagonal-quadric/verify_p4_diagonal_quadric_pure_component.py`;
11. `claims/p4/components/mixed-orientation/verify_p4_mixed_orientation_pure_component.py`;
12. `verify_p4_diagonal_quadric_one_three_components.py`;
13. `verify_p5_h31_component_fiber_infinity.py`;
14. `audit_p5_h31_component_fiber_infinity.py`;
15. `verify_p5_h31_component_fibre_infinity_marked_fibre.py`;
16. `verify_p5_h31_marked_basis_open_branch.py`;
17. `audit_p5_h31_marked_basis_open_branch.py`;
18. `verify_p5_h31_marked_basis_fibre_classification.py`;
19. `audit_p5_h31_marked_basis_fibre_classification.py`;
20. `verify_p5_h31_rank_two_component_orbit.py`;
21. `claims/p5/h31/internal-e0-marked-fibre/verify_p5_h31_internal_e0_marked_fibre.py`;
22. `verify_p5_high_coordinate_partial_frontier.py`;
23. `audit_p5_high_coordinate_partial_frontier.py`;
24. `claims/p5/h22/first-rank-two/verify_p5_h22_first_rank_two_component_generic_obstruction.py`;
25. `audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_independent.py`;
26. `derive_p5_h22_component19_p0_phi_pm_one_ordinary_obstruction_candidate.py`; and
27. `derive_p5_h22_component19_p0_qphi_minus_one_axes_compatibility_obstruction.py`.

Expected theorem/dependency/self hashes may change mechanically. Mathematical
scope fields must not. The component-19 derivations remain `CANDIDATE`; P4,
H31, H22, `P5 -> Delta3`, and global fields retain their current exact
boundaries. Historical tracked certificate hashes do not refresh merely
because a linked synthesis document moved. Require no tracked output drift.

Both moved modules must also pass isolated foreign-CWD import probes with
`sympy + python-sat`. The current root scripts fail isolated import before
bootstrap; that is the known mechanical defect being repaired, not a
scientific failure. Confirm targeted Ruff/byte compilation, rewriter fixed
point, the index-complete validation floor, exact-head CI, and fresh semantic
plus mechanical final referees before a normal exact-head guarded merge.

The global Krenn-Gu conjecture remains **UNRESOLVED**.
