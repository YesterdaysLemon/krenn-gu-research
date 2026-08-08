# Stage 10 dry-run — deferred generic recovery and bounded P5 migration

Status: **approved scope reconstructed; blocker repair complete; exact batch not
yet frozen or executed.**

This dry-run separates three questions that must not be collapsed:

1. can a package replay in the current tree;
2. what scientific evidence the package actually has; and
3. whether its generic core is separable enough to migrate now.

No theorem, assumption, scope, proof status, divisor status, or global status
changes here. The global Krenn–Gu conjecture remains **UNRESOLVED**.

## Baseline and source hierarchy

Measured on 2026-08-08:

- GitHub PR #38 is merged, with merge commit
  `5db0fd317a1b77aaa3003a16b0cde9be89d9c568`.
- Fresh local `main` and `origin/main` both resolved to that SHA; there were no
  intervening commits.
- Stage 10 branch: `layout-migration-stage10-deferred-generics`.
- Pre-change validation passed: `check_hygiene.py`, 117 migration-tool tests,
  14 fourteen-vertex tests, link rewriter fixed point, and clean diff.
- Stage 10 repair commit:
  `943920421515282653cd6831b9d7b6cfa002e060`.
- Measured Git root-tree entries after the repair: **2,048**.

The current `AGENTS.md`, migration runbook, proof-obligation architecture,
formalization interface, Stage 9 report, classifier, moved-path manifest,
theorem ledger, and Stage 9 batch were read first. Older Stage 3–8 reports were
not consumed wholesale. Historical evidence below was retrieved only for the
specific equal-support path chronology and earlier ownership decisions.

## Delegation ledger

Subagents were read-only. Their results were evidence; the lead performed all
writes, replay decisions, package selection, and integration.

| task | agent | why delegated | surface inspected | compact result | confidence | lead spot-check | usefulness |
|---|---|---|---|---|---|---|---|
| equal-support archaeology | `equal_support_archaeology` | broad evidence/provenance reconstruction with a crisp two-package target | two P5 docs/primaries, P4 package/audit, ledger, classifier, Git chronology, consumers | two live primaries, no P5 audits; exact stale-path cause; no boundary forest | high | yes: constants, ledger, P4 audit scope, failures, full replays | high; avoided reconstructing the full history |
| stale-path/provenance audit | `stale_path_audit` | scan executable constants and staying consumers without mixing in fixes | all proposed packages, 32 staying executable consumers, prior moved P4/P5 dependencies | only equal-support blocked pre-move; exact post-move repair surface and one unrelated candidate debt item | high | yes: selected constants, import lists, frontier hashes | high; exact locations made the audit directly actionable |
| deferred-family classification | `deferred_family_classifier` | compare many nuclei across ledger/prose/topology | ten deferred nuclei, ledger, classifier, theorem prose, imports | conservative 25-file / 9-package generic-only slice | high except common-center ownership medium-high | yes: selected ledger entries, mappings, and decisive imports | medium-high; substantially reduced broad reading |

The lead did not reproduce each worker's broad search. Consequential evidence
was checked at the cited files/symbols, then replayed or recomputed directly.

## Pre-migration blocker repair

### Failure and chronology

Before repair, both equal-support P5 primaries resolved `ROOT` to the repository
root but attempted to hash:

```text
P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md
verify_p4_equal_support_sixfold_pure_component.py
```

Both root paths were absent. The live files are under
`claims/p4/components/equal-support-sixfold/`. Direct import/provenance probes
for H31 and H22 each returned rc=1 with `FileNotFoundError`; no verifier body or
output write was triggered.

Git chronology shows that the P5 constants were authored in `41404fa` while the
P4 files were still at root. Stage 3 pure-moved the P4 package in `69ed945`; its
repair commit `fd4836a` updated the P5 Markdown links but not these executable
constants. The defect therefore predates Stage 10 and was independently
observed again in Stage 9.

### Repair classification and content

Classification: **stale path constants left by an earlier migration**.

Repair commit `9439204` changed only four path-constant lines:

- H31 `COMPONENT` and `COMPONENT_PRIMARY`;
- H22 `COMPONENT` and `COMPONENT_PRIMARY`.

They now address the existing Stage 3 P4 package. Algebra, assertions, solver
strategy, timeouts, coefficient domain, theorem prose, status, and output
semantics are unchanged. The remaining obsolete `find_root()` sentinel and the
H22 same-directory companion path are post-move mechanical obligations; they
are not needed while the files remain at root.

### Pre/post repair replay

Pre-repair path probes: H31 rc=1; H22 rc=1; both exact
`FileNotFoundError` on the P4 theorem path.

Post-repair full primary replays used:

```text
host: native Windows 11 checkout
guest: WSL Ubuntu
working directory: /mnt/c/Users/Yeste/OneDrive/Documents/open-graph-theory-with-prize
Python: 3.12.3
SymPy: 1.14.0
Singular: 4.3.2
```

| package | command script | wall seconds | rc | semantic result |
|---|---|---:|---:|---|
| H31 equal-support-sixfold | `verify_p5_h31_equal_support_sixfold_component_generic_obstruction.py` | 13.25 | 0 | `verified=true`, generic fibre empty; complete boundary, global H31/H22, and global conjecture remain false/open |
| H22 equal-support-sixfold | `verify_p5_h22_equal_support_sixfold_component_generic_obstruction.py` | 48.52 | 0 | `verified=true`, generic H22 fibre empty and generic-point slope coverage true; global H22 and global conjecture remain false/open |

Both outputs went to ignored `tmp/` JSON files. `git status --short` and
`git diff` showed no tracked mutation after each tier.

## Equal-support evidence structure

The two equal-support packages are not evidentially symmetrical with the Stage
9 packages.

| package | ledger status | primary | P5 independent audit | upstream P4 evidence | migration decision |
|---|---|---|---|---|---|
| H31 equal-support-sixfold | `verified_generic` | present and replayed | none; `audit_provenance: none_exists` | P4 theorem, primary, and independent P4 audit | include with explicit evidence debt |
| H22 equal-support-sixfold | `verified_generic` | present and replayed | none; `audit_provenance: none_exists` | same P4 package; H22 also hashes the H31 theorem | include with explicit evidence debt |

The P4 audit is genuinely independent for the **P4 component theorem**. It is
not an audit of either P5 obstruction and explicitly does not claim generic H31
or weighted H22 exclusion. No audit was created in Stage 10.

Two evidence debts remain recorded, not repaired:

- the ledger dependency arrays are empty although the primaries hash real P4
  dependencies, and H22 hashes the H31 theorem;
- the equal-support ledger assumption summaries are coarser than, and partly in
  tension with, the theorem/verifier descriptions of closed interior strata and
  special slopes.

Changing those scientific summaries requires a dedicated evidence review, not
a layout-migration edit. The classifier's two false “verify/audit triple”
evidence strings are corrected in this stage to “theorem/primary pair; no P5
independent audit exists”; ownership, confidence, and destinations are
unchanged.

## Deferred-family inventory

| nucleus | classification | Stage 10 treatment | evidence-based reason |
|---|---|---|---|
| equal-support-sixfold | `PATH_DEBT`, `EVIDENCE_DEBT`, then `READY_GENERIC` | include H31 and H22 pairs | blocker repaired; both primaries replay; no P5 audits, explicitly recorded |
| common-active-binary-triangle | H31 `BOUNDARY_INSEPARABLE`; H22 `CANDIDATE_ONLY`, `PATH_DEBT`, `EVIDENCE_DEBT` | defer | H31 classifier family owns a 21-file descendant tree; H22 is absent from the ledger and its audit still targets a moved P4 root path |
| embedded-p3 | `BOUNDARY_INSEPARABLE` | defer both sides | generic documents route into same-theorem boundary/closure evidence chains (15 H31 + 20 H22 files) |
| common-center-kernel-star | H31 `READY_GENERIC`; H22 `SCIENTIFICALLY_PARTIAL` | include H31 triple only | H31 generic triple is separable; H22 root theorem is explicitly partial |
| unequal-complement/common-kernel | H31 `READY_GENERIC`; H22 `SCIENTIFICALLY_PARTIAL` / boundary recursion | include H31 triple only | exact three-file H31 package; H22 D01/D23 recursion remains at root |
| unequal-endpoint/inward-star | H31 `READY_GENERIC`; H22 `BOUNDARY_INSEPARABLE`, `SCIENTIFICALLY_PARTIAL`, `TOO_LARGE_FOR_STAGE10` | include H31 triple only | exact three-file H31 core; large H22 branch/divisor tree remains |
| diagonal-quadric-elliptic | `BOUNDARY_INSEPARABLE` | defer | primary hashes boundary theorem paths and the generic prose consumes a ten-file elliptic forest |
| one-three-components | `READY_GENERIC` | include H31 and H22 triples | both ledger live/audited; H22-to-H31 edges become batch-internal |
| split-center-mixed-star | H31 `READY_GENERIC`; H22 `SHARED_DEPENDENCY_UNCLEAR`, `EVIDENCE_DEBT` | include H31 triple only | H22 primary imports load-bearing model/project functions from a common-active candidate derivation |
| first-rank-two | `READY_GENERIC` | include H22 triple only | live audited generic theorem; boundary/divisors excluded and stay at root |

This is deliberately smaller than the preferred Stage 10 size. Expanding it to
40 files would require laundering a boundary forest, candidate-derived helper,
or partial recursion into the generic live spine.

## Selected packages and replay roles

Selected: **9 packages / 25 files**.

| side/family | theorem | primary verifier | independent audit | members |
|---|---|---|---|---:|
| H31 equal-support-sixfold | yes | yes | none exists | 2 |
| H22 equal-support-sixfold | yes | yes | none exists | 2 |
| H31 common-center-kernel-star | yes | yes | yes | 3 |
| H31 unequal-complement-common-kernel | yes | yes | yes | 3 |
| H31 unequal-endpoint-inward-star | yes | yes | yes | 3 |
| H31 one-three | yes | yes | yes | 3 |
| H22 one-three-components | yes | yes | yes | 3 |
| H31 split-center-mixed-star | yes | yes | yes | 3 |
| H22 first-rank-two | yes | yes | yes | 3 |

Executable role inventory:

```text
primary_verifier:    9
independent_audit:   7
support_dependency: 0 batch members (shared dependencies stay shared)
optional_exploration: 0
generator:           0
other:               0
mandatory replays:  16
```

No candidate, partial, boundary, divisor, exceptional-fibre, exploration, or
generator file is selected.

## Measured pre-move scientific replay

Exact command form for every row:

```text
wsl.exe --exec bash --noprofile --norc -lc "cd '/mnt/c/Users/Yeste/OneDrive/Documents/open-graph-theory-with-prize' && python3 '<script>'"
```

All commands used the environment recorded above. Wall times are measured.

| role | script | seconds | rc | semantic result |
|---|---|---:|---:|---|
| primary | `verify_p5_h31_equal_support_sixfold_component_generic_obstruction.py` | 13.25 | 0 | generic H31 true; boundary/global false |
| primary | `verify_p5_h22_equal_support_sixfold_component_generic_obstruction.py` | 48.52 | 0 | generic H22 true; global false |
| primary | `verify_p5_h31_common_center_kernel_star_component_generic_obstruction.py` | 16.20 | 0 | generic H31 true; H22/global false |
| primary | `verify_p5_h31_one_three_component_generic_obstruction.py` | 38.79 | 0 | three generic H31 fibres excluded; boundaries/global false |
| primary | `verify_p5_h22_one_three_components_generic_obstruction.py` | 23.87 | 0 | three generic weighted H22 fibres empty; divisors/boundaries/global false |
| primary | `verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction.py` | 43.45 | 0 | generic H31 true; global false |
| primary | `verify_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction.py` | 7.91 | 0 | generic H31 true; pivot/special boundaries/global false |
| primary | `verify_p5_h31_split_center_mixed_star_component_generic_obstruction.py` | 14.84 | 0 | generic H31 true; H22/global false |
| primary | `verify_p5_h22_first_rank_two_component_generic_obstruction.py` | 27.40 | 0 | first component generic H22 true; divisors/boundary/global false |
| audit | `audit_p5_h31_common_center_kernel_star_component_generic_obstruction.py` | 4.08 | 0 | audit completed; finite-field proof not used; global false |
| audit | `audit_p5_h31_one_three_component_generic_obstruction.py` | 5.13 | 0 | `audited=true`, independent of primary imports |
| audit | `audit_p5_h22_one_three_components_generic_obstruction.py` | 47.44 | 0 | `audited=true`, independent; finite-field results corroborative only |
| audit | `audit_p5_h31_unequal_complement_common_kernel_component_generic_obstruction.py` | 1.19 | 0 | audit completed; finite-field proof not used; global false |
| audit | `audit_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction.py` | 6.46 | 0 | generic H31 replayed; pivot boundary false; global false |
| audit | `audit_p5_h31_split_center_mixed_star_component_generic_obstruction.py` | 2.01 | 0 | characteristic-zero proof not replaced; finite-field proof not used |
| audit | `audit_p5_h22_first_rank_two_component_generic_obstruction.py` | 8.14 | 0 | `audited=true`, independent; finite-field results corroborative only |

All 16 mandatory replays were semantically green. Sequential measured wall time
was **308.68 seconds**. Eight scripts wrote ignored JSON beneath `tmp/`; the
other eight emitted JSON to stdout only. No selected replay wrote a tracked
result, certificate, or snapshot. `git status --short` and `git diff` were clean
after primary, audit, and semantic-inspection tiers.

## Generic versus boundary ownership

The selected package unit is exactly:

```text
generic theorem
+ primary verifier
+ existing independent audit when one exists
```

Shared marked-basis helpers, already-migrated P4 component theorems, and
already-migrated mixed-orientation packages remain shared. Staying boundary
consumers are repaired to import the moved generic package; their ownership does
not follow the import edge.

Left behind explicitly:

- common-active candidate and boundary tree;
- embedded-P3 closure chains;
- common-center H22 partial/divisor recursion;
- unequal-complement H22 D01/D23 recursion;
- unequal-endpoint H22 branch/divisor tree;
- diagonal-quadric elliptic boundary forest;
- split-center H22 theorem with candidate-derived helper;
- every special fibre, exceptional locus, pointwise closure, and frontier
  synthesis file.

## Dependency and consumer topology

Batch-internal edges:

- H22 equal-support hashes the H31 equal-support theorem;
- H22 one-three imports the H31 one-three primary;
- H22 one-three audit imports the H31 one-three audit.

Previously moved dependencies:

- equal-support uses `claims/p4/components/equal-support-sixfold/`;
- first-rank-two uses the migrated pure-rank-two P4 theorem and the migrated
  H22 mixed-orientation package.

Root-shared dependencies stay shared:

- `p5_high_coordinate_tree_chart_cegar.py`;
- marked-basis open/fibre helpers;
- the root P4 diagonal-quadric one-three component package, which remains
  outside this P5 batch.

Staying executable repair surface: **32 files**.

- 7 common-center H22 importers;
- 12 unequal-complement H22 importers;
- 11 unequal-endpoint H22 importers;
- 1 split-center H22 importer;
- `verify_p5_high_coordinate_partial_frontier.py`, with three hard provenance
  paths naming the moving H31/H22 one-three and H22 first-rank-two theorems.

The 31 importers are exact-name imports of one of the four moving H31 modules.
They will receive `bootstrap`/`expose_claim_package` repair only; no boundary
file moves and no algebra changes. The frontier verifier receives path-only
constant updates and must replay afterward.

Exact importer inventory:

```text
# common-center (7)
verify_p5_h22_common_center_kernel_star_component_finite_all_marking_dense_open_supplement.py
verify_p5_h22_common_center_kernel_star_component_finite_lambda_one_all_marking_obstruction.py
verify_p5_h22_common_center_kernel_star_component_finite_lambda_zero_all_marking_obstruction.py
verify_p5_h22_common_center_kernel_star_component_finite_ordinary_F_h2_zero_obstruction.py
verify_p5_h22_common_center_kernel_star_component_finite_ordinary_residual_obstruction.py
verify_p5_h22_common_center_kernel_star_component_partial.py
verify_p5_h22_common_center_kernel_star_component_r_t_divisor_symmetry_transfer.py

# unequal-complement (12)
audit_p5_h22_unequal_complement_common_kernel_component_d23_f2_f7_intersection_obstruction.py
audit_p5_h22_unequal_complement_common_kernel_component_d23_f2_f8_h3_slope_intersection_obstruction.py
audit_p5_h22_unequal_complement_common_kernel_component_d23_h1_nonzero_h2_zero_partial_closure.py
audit_p5_h22_unequal_complement_common_kernel_component_d23_h2_zero_six_by_six_terminal_reduction.py
audit_p5_h22_unequal_complement_common_kernel_component_d23_h2_zero_terminal_complete_obstruction.py
audit_p5_h22_unequal_complement_common_kernel_component_d23_h2r1_residual_obstruction.py
verify_p5_h22_common_center_kernel_star_component_k_infinity_all_pair_boundary_obstruction.py
verify_p5_h22_unequal_complement_common_kernel_component_d01_pair_orbit_obstruction.py
verify_p5_h22_unequal_complement_common_kernel_component_d23_h0_nonzero_residual_cofactor_open_obstruction.py
verify_p5_h22_unequal_complement_common_kernel_component_d23_h0_zero_residual_obstruction.py
verify_p5_h22_unequal_complement_common_kernel_component_d23_pair_orbit_partial_obstruction.py
verify_p5_h22_unequal_complement_common_kernel_component_survivor_reconnaissance.py

# unequal-endpoint (11)
verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a.py
verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a_exceptional_divisor.py
verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a_exceptional_divisor_generic_obstruction.py
verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a_exceptional_divisor_ternary_false_positive.py
verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a_exceptional_weights.py
verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a_univariate.py
verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_lambda_minus_one.py
verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_residual.py
verify_p5_h22_unequal_endpoint_inward_star_component_finite_d23_factor_cover.py
verify_p5_h22_unequal_endpoint_inward_star_component_finite_d23_lambda_one.py
verify_p5_h22_unequal_endpoint_inward_star_component_partial.py

# split-center (1)
verify_p5_h22_split_center_mixed_star_component_generic_obstruction.py
```

## Pre-approval stale-path audit

Measured findings:

- equal-support was the only selected pre-move blocker, repaired in `9439204`;
- no selected dependency/hash inventory is guarded by fail-open `.exists()`;
- selected `.exists()` uses are bootstrap discovery plus the equal-support
  sentinel that must be replaced after the move;
- all other selected P4/theorem dependencies currently resolve;
- H31/H22 one-three, first-rank-two, and equal-support have known package-local
  constants that become invalid only after moving;
- the 32 staying consumers above are the complete selected exact-name import
  and hard-provenance surface found by the audit.

Unrelated debt is deferred: the unselected common-active H22 candidate audit
still targets the obsolete root P4 common-active verifier. Stage 10 does not
repair it.

## Exact proposed mappings

All 25 source records are currently `proposed_high_confidence`, confidence
`high`. Classifier confidence is not approval.

| source | destination |
|---|---|
| `P5_H22_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md` | `claims/p5/h22/equal-support-sixfold/P5_H22_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md` |
| `P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md` | `claims/p5/h22/first-rank-two/P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md` |
| `P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md` | `claims/p5/h22/one-three-components/P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md` |
| `P5_H31_COMMON_CENTER_KERNEL_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | `claims/p5/h31/common-center-kernel-star/P5_H31_COMMON_CENTER_KERNEL_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` |
| `P5_H31_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md` | `claims/p5/h31/equal-support-sixfold/P5_H31_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md` |
| `P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md` | `claims/p5/h31/one-three/P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md` |
| `P5_H31_SPLIT_CENTER_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | `claims/p5/h31/split-center-mixed-star/P5_H31_SPLIT_CENTER_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` |
| `P5_H31_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_GENERIC_OBSTRUCTION.md` | `claims/p5/h31/unequal-complement-common-kernel/P5_H31_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_GENERIC_OBSTRUCTION.md` |
| `P5_H31_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` | `claims/p5/h31/unequal-endpoint-inward-star/P5_H31_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` |
| `audit_p5_h22_first_rank_two_component_generic_obstruction.py` | `claims/p5/h22/first-rank-two/audit_p5_h22_first_rank_two_component_generic_obstruction.py` |
| `audit_p5_h22_one_three_components_generic_obstruction.py` | `claims/p5/h22/one-three-components/audit_p5_h22_one_three_components_generic_obstruction.py` |
| `audit_p5_h31_common_center_kernel_star_component_generic_obstruction.py` | `claims/p5/h31/common-center-kernel-star/audit_p5_h31_common_center_kernel_star_component_generic_obstruction.py` |
| `audit_p5_h31_one_three_component_generic_obstruction.py` | `claims/p5/h31/one-three/audit_p5_h31_one_three_component_generic_obstruction.py` |
| `audit_p5_h31_split_center_mixed_star_component_generic_obstruction.py` | `claims/p5/h31/split-center-mixed-star/audit_p5_h31_split_center_mixed_star_component_generic_obstruction.py` |
| `audit_p5_h31_unequal_complement_common_kernel_component_generic_obstruction.py` | `claims/p5/h31/unequal-complement-common-kernel/audit_p5_h31_unequal_complement_common_kernel_component_generic_obstruction.py` |
| `audit_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction.py` | `claims/p5/h31/unequal-endpoint-inward-star/audit_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction.py` |
| `verify_p5_h22_equal_support_sixfold_component_generic_obstruction.py` | `claims/p5/h22/equal-support-sixfold/verify_p5_h22_equal_support_sixfold_component_generic_obstruction.py` |
| `verify_p5_h22_first_rank_two_component_generic_obstruction.py` | `claims/p5/h22/first-rank-two/verify_p5_h22_first_rank_two_component_generic_obstruction.py` |
| `verify_p5_h22_one_three_components_generic_obstruction.py` | `claims/p5/h22/one-three-components/verify_p5_h22_one_three_components_generic_obstruction.py` |
| `verify_p5_h31_common_center_kernel_star_component_generic_obstruction.py` | `claims/p5/h31/common-center-kernel-star/verify_p5_h31_common_center_kernel_star_component_generic_obstruction.py` |
| `verify_p5_h31_equal_support_sixfold_component_generic_obstruction.py` | `claims/p5/h31/equal-support-sixfold/verify_p5_h31_equal_support_sixfold_component_generic_obstruction.py` |
| `verify_p5_h31_one_three_component_generic_obstruction.py` | `claims/p5/h31/one-three/verify_p5_h31_one_three_component_generic_obstruction.py` |
| `verify_p5_h31_split_center_mixed_star_component_generic_obstruction.py` | `claims/p5/h31/split-center-mixed-star/verify_p5_h31_split_center_mixed_star_component_generic_obstruction.py` |
| `verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction.py` | `claims/p5/h31/unequal-complement-common-kernel/verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction.py` |
| `verify_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction.py` | `claims/p5/h31/unequal-endpoint-inward-star/verify_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction.py` |

Review note: the capitalization in every executable destination must match the
manifest exactly; the frozen batch is authoritative, not this prose table.

Measured canonical mapping SHA-256 for the manifest mappings:

```text
e39d17c3ed855ef5a1342560ebf61e9b313246142f24af23940bc3ff8af472db
```

Measured manifest working-tree SHA-256 before Commit A:

```text
6c4314b2f2762f0affc5fe48ad60b7220620c06e3a9beae36365afefaf640e35
```

## Root projection and catalog arithmetic

Measured before execution:

```text
Git root-tree entries                         2048
manifest moved                                325
manifest proposed_high_confidence             277
manifest review_required                     1413
manifest unclassified                         348
manifest projected_root_if_moved_only         2047
```

Projected after the exact 25 root-file moves:

```text
Git root-tree entries                         2023  (2048 - 25)
manifest moved                                350   (325 + 25)
manifest proposed_high_confidence             252   (277 - 25)
manifest review_required                     1413   (unchanged)
manifest unclassified                         348   (unchanged)
enforced stale paths                          350   (325 + 25)
manifest projected_root_if_moved_only         2022  (2047 - 25)
```

The one-entry difference between the observed Git root and the classifier-era
projection is the post-inventory root addition already documented by Stage 9
(`AGENTS.md`). It remains one before and after this batch.

Classifier refinement is limited to the two equal-support evidence strings.
Regenerating `catalog/moved-paths.json` was byte-identical: previous moved
records, executed-batch provenance, statuses, confidence, destinations, and
summary counts are unchanged.

## Frozen-batch contract (projected)

Artifact:

```text
catalog/batches/p5-deferred-generics-stage10.json
```

Approval string:

```text
YesterdaysLemon (repository owner), Stage 10 deferred generic P5 migration instruction
```

The batch will freeze the exact 25 mappings, Commit A's exact SHA as
`base_sha`, the canonical mapping hash above, the approval-time manifest hash,
and `member_count: 25`. Approval does not extend to any deferred P5 family or
to pointwise/boundary recursion.

## Mechanical repair and replay plan

After the pure move:

1. run the shared link/command rewriter;
2. replace moved-script root discovery with shared `bootstrap`;
3. use package-local `HERE` only for same-package theorem/primary paths;
4. use `REPO_ROOT` or `expose_claim_package` for shared and cross-package
   dependencies;
5. repair all 31 staying importers and the frontier's three hard theorem paths;
6. run the rewriter to a `0 links / 0 commands / 0 files / 0 ambiguities`
   fixed point;
7. replay all 16 mandatory executables from their new paths;
8. clean-subprocess import all moved scripts and all 32 staying consumers;
9. replay the frontier verifier and representative staying boundary consumers;
10. inspect `git status --short` and `git diff` after every tier.

No optional exploration script is a batch member or planned smoke test.

## Tracked-output audit plan

Before each replay tier, record the candidate-tree diff. For every selected
script, preserve its existing output convention:

- ignored `tmp/` JSON for the eight output-writing executables;
- stdout-only JSON for the remaining eight.

After each tier:

```text
git status --short
git diff
```

Any tracked result/certificate/snapshot mutation is a failure unless explicitly
intended, explained, and separately reviewed. rc=0 is never accepted without
reading the semantic JSON booleans.

## Environment and hash-domain requirements

- Native Windows Python is adequate for hygiene/tests but lacks Singular on
  `PATH`.
- Mandatory scientific replay uses WSL Python 3.12.3, SymPy 1.14.0, and Singular
  4.3.2.
- Existing Singular invocation conventions are preserved; no portability
  normalization is authorized.
- Ledger hashes are computed from Git index/committed blob bytes.
- Equal-support working-tree SHA-256 values differ from ledger blob prefixes on
  Windows because of CRLF normalization; this is informational, not corruption.
- Canonical mapping serialization/hash must match exactly in its own domain.

## Documentation and process friction

1. The classifier could describe a theorem/primary pair as a verify/audit
   triple even when the ledger explicitly said `none_exists`. Corrected for the
   two selected equal-support records; no schema change required.
2. Equal-support ledger assumption summaries do not fully match the more
   specific theorem/verifier scope. Recorded as evidence debt; not rewritten by
   migration.
3. Import topology, not filename grouping, exposed 31 staying boundary
   consumers. Exact-name delegated scanning materially reduced lead context.
4. The runbook's index-complete validation order is authoritative: stage first,
   then run `check_hygiene.py`. An initial pre-repair hygiene invocation before
   staging failed only that precondition and was rerun correctly.
5. Singular conventions remain script-specific. This stage records the actual
   environment instead of broadening into portability cleanup.

## Approval boundary and stop condition

Stage 10 proceeds only with the exact 25 mappings above after Commit A is
reviewed and the batch is frozen. It does not begin pointwise divisor recursion,
move boundary descendants, manufacture missing audits, normalize Singular,
repair the common-active candidate, or change the global theorem status.
