# Stage 6 dry-run: P4 star / mixed-star classification spine

Generated before execution, from the tree at the Stage 6 starting
SHA `a342d12` (merged `main` including PR #33 / Stage 5), branch
`layout-migration-stage6-p4-star-classifications`.

Approval artifact: `catalog/batches/p4-star-stage6.json` (produced
after this report).  Approval:

```text
YesterdaysLemon (repository owner), Stage 6 P4 star/mixed-star classification migration instruction
```

applies only to the exact generated mappings recorded in that batch
file.  It does not approve all remaining P4 classification files, all
files containing STAR, P4 boundaries generally, P5 claims, research
snapshots, global classification machinery, or future batches.

## Scope and stop-condition verdict

Every candidate seed named in the Stage 6 instruction was verified
against current `main`.  All 13 seeds exist as complete
claim/verifier/audit triples; the inventory adds four more complete
star-classification triples (`coincident_support_star_reverse`,
`disjoint_mixed_star_affine`, `disjoint_mixed_star_projective`,
`two_rank_two_spoke_mixed_star_classification`) discovered through
the classifier's `p4/classifications` family.

**Batch: 17 packages / 51 files** (17 complete triples; preferred
range 15–22 packages, 50–75 files — hit on both).  Hard ceiling 90
not approached.  No owned support scripts: no candidate verifier has
a sole-importer support module (the only cross-script Python import
among candidates is the P5 consumer of
`verify_p4_two_rank_two_spoke_mixed_star_component`, which stays at
root).

## Selection decisions

| package (slug) | classifier family/confidence | decision | rationale |
|---|---|---|---|
| all-center-kernel-star-111-obstruction | p4/boundaries, medium/low | **include** | seed; doc states it excludes one star `(1,1,1)` orientation from the last open all-pair cell — star-cell-specific obstruction; complete triple; replay ≤1 s |
| all-double-endpoint-star-111-obstruction | p4/boundaries, medium/low | **include** | seed; same star-cell ownership rationale; complete triple; replay ≤1 s |
| coincident-support-rank-one-star | p4/classifications, medium/low | **include** | seed (as `P4_RADICAL_STAR_COMPONENT_CLASSIFICATION`'s sibling star component theorem, component 21); complete triple; replay ~3 s; four P5 consumers stay at root |
| coincident-support-star-reverse | p4/classifications, medium/low | **include** | reverse classification of the coincident-support star orientation; complete triple; replay ~1 s; referenced by two selected 111 verifiers (intra-batch doc link only) |
| common-center-kernel-star-211 | p4/classifications, medium/low | **include** | seed; complete triple; replay ~4 s |
| disjoint-mixed-star-affine | p4/classifications, medium/low | **include** | affine stratum exhaustion of the rank-one disjoint mixed star; depends on already-migrated `claims/p4/components/disjoint-mixed-star` (cross-spine dependency, not moved again); complete triple; replay ~1 s |
| disjoint-mixed-star-projective | p4/classifications, medium/low | **include** | projective exhaustion closing the stratum; same cross-spine dependency; complete triple; replay ~1 s |
| equal-endpoint-inward-star-211-obstruction | p4/boundaries, medium/low | **include** | seed; doc: closes the two-inward frontier of the star `(2,1,1)` cell together with the already-migrated unequal-endpoint complete theorem — star-specific; complete triple; replay ~2 s |
| mixed-endpoint-star-111-complete | p4/classifications, medium/low | **include** | seed; complete triple; replay ~1 s |
| no-double-endpoint-star-1110-collision | p4/classifications, medium/low | **include** | seed; Singular required (exact radical replay); WSL fallback present; replay ~8 s |
| one-double-endpoint-star-111 | p4/classifications, medium/low | **include** | seed; Singular required; WSL fallback; replay ~3 s |
| radical-star | p4/classifications, medium/low | **include** | seed; generic radical-star classification doc hashed by four already-migrated component verifiers and two staying frontier scripts — cross-reference density, not ownership: they reference it, it does not belong to them; complete triple; replay ~1 s |
| rank-two-relation-star-obstruction | p4/boundaries, medium/low | **include** | seed; star-tree-gauge obstruction repaired after the withdrawn overstrong attempt; complete triple; replay ~1 s |
| two-double-endpoint-star-111-complete | p4/classifications, medium/low | **include** | seed; verifier hashes the already-migrated triple-kernel doc (cross-spine constant); complete triple; replay ~2 s |
| two-rank-two-spoke-mixed-star-classification | p4/classifications, medium/low | **include** | complete triple; replay ~2 s; slug keeps `-classification` to avoid destination collision with the component package |
| two-rank-two-spoke-mixed-star-component | p4/classifications, medium/low | **include** | seed; complete triple; replay ~3 s; one staying P5 verifier imports it (bare import repaired via `expose_claim_package` in Commit D) |
| unequal-endpoint-inward-star-211 | p4/classifications, medium/low | **include** | seed (as `..._211_COMPONENT`); complete triple; replay ~3 s; linked from the already-migrated Stage 5 `unequal-endpoint-inward-star-211-complete` package doc (link re-anchored, not moved) |

The medium/low classifier confidence is retained as-is; Stage 6's
human review resolved *ownership* (package membership, nested
destination, triple completeness), which is what the batch approval
records.  No confidence field is promoted.

## Ownership classification of related-but-separate files

| file(s) | role | disposition |
|---|---|---|
| `P4_RANK_TWO_RELATION_STAR_OBSTRUCTION_WITHDRAWN_OVERSTRONG.{md}` + verify/audit | historical_snapshot / withdrawn | **EXCLUDE** — classifier already proposes `claims/legacy/` (high confidence, `proposed_high_confidence`); the withdrawn artifact stays at root until a dedicated legacy batch; the selected obstruction package does not import it |
| `verify_p4_directed_zero_divisor_triangle_components.py` | shared_dependency | stays at root (Stage 5 precedent: 6 importers across 4 families) |
| `verify_p4_common_singleton_component.py` | shared_dependency | stays; its `PROFILE_SOURCE_FRAGMENTS` table names `verify_p4_two_rank_two_spoke_mixed_star_component.py`, but resolution goes through `_fragment_source_path` → `catalog/moved-paths.json` (already migration-aware; no repair needed) |
| `verify_p4_all_pair_rank_exceptional_graph_reduction.py` | shared_dependency / atlas | stays; 8 selected docs named in its `RESOLUTION_PACKAGES` tuple — Commit D path repair |
| P5 H22/H31 star-consumer scripts and docs (coincident-support, two-rank-two-spoke, unequal-endpoint families) | downstream_consumer | stay at root; path constants / one bare import repaired in Commit D |
| `claims/p4/components/*` verifiers hashing `P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md` | boundary_owned_elsewhere (component packages) | already migrated; their `REPO_ROOT /` constants repaired in Commit D |
| `branch_ambient_certificates.py` | working_note | stays; prose mention only |
| `claims/p4/components/disjoint-mixed-star/` package | boundary_owned_elsewhere | Stage 3/4 migrated component; inbound links re-anchored, not moved |
| `claims/p4/classifications/triangle-211/{mixed-center-star-211-complete, split-center-mixed-star-211, unequal-endpoint-inward-star-211-complete}` | already_migrated_elsewhere | Stage 5 packages; **not moved again**; linked from the new star README as cross-spine dependencies |

## Classification refinement (durable, rebuild-safe)

For the 51 selected records, `catalog/layout-classification.json` —
the durable source — was edited:

```text
claim_family:  p4/boundaries (12 records) | p4/classifications (39)
           ->  p4/classifications/star/<package-slug>
proposed_path: claims/p4/boundaries/<file> | claims/p4/classifications/<file>
           ->  claims/p4/classifications/star/<package-slug>/<file>
evidence:      + "stage6_human_review: P4 star/mixed-star classification spine package"
```

`build_manifest.py` was then run normally.  Verified against the
committed manifest:

- **51 records changed**, all `review_required -> review_required`
  (no status promotion);
- all **114 already-moved records byte-identical**, `executed_batch`
  preserved 114/114;
- counts unchanged (moved 114, proposed 361, review 1540,
  projected_root_if_moved_only 2258);
- no record outside the selection changed;
- the 4 refined `p4/boundaries` records are accounted for separately
  in the root arithmetic below (family reassignment, not a
  classifications-bucket subtraction).

## File mapping (exact, 51 moves)

| old path | new path |
|---|---|
| P4_ALL_CENTER_KERNEL_STAR_111_OBSTRUCTION.md | claims/p4/classifications/star/all-center-kernel-star-111-obstruction/P4_ALL_CENTER_KERNEL_STAR_111_OBSTRUCTION.md |
| verify_p4_all_center_kernel_star_111_obstruction.py | claims/p4/classifications/star/all-center-kernel-star-111-obstruction/verify_p4_all_center_kernel_star_111_obstruction.py |
| audit_p4_all_center_kernel_star_111_obstruction.py | claims/p4/classifications/star/all-center-kernel-star-111-obstruction/audit_p4_all_center_kernel_star_111_obstruction.py |
| P4_ALL_DOUBLE_ENDPOINT_STAR_111_OBSTRUCTION.md | claims/p4/classifications/star/all-double-endpoint-star-111-obstruction/P4_ALL_DOUBLE_ENDPOINT_STAR_111_OBSTRUCTION.md |
| verify_p4_all_double_endpoint_star_111_obstruction.py | claims/p4/classifications/star/all-double-endpoint-star-111-obstruction/verify_p4_all_double_endpoint_star_111_obstruction.py |
| audit_p4_all_double_endpoint_star_111_obstruction.py | claims/p4/classifications/star/all-double-endpoint-star-111-obstruction/audit_p4_all_double_endpoint_star_111_obstruction.py |
| P4_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT.md | claims/p4/classifications/star/coincident-support-rank-one-star/P4_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT.md |
| verify_p4_coincident_support_rank_one_star_component.py | claims/p4/classifications/star/coincident-support-rank-one-star/verify_p4_coincident_support_rank_one_star_component.py |
| audit_p4_coincident_support_rank_one_star_component.py | claims/p4/classifications/star/coincident-support-rank-one-star/audit_p4_coincident_support_rank_one_star_component.py |
| P4_COINCIDENT_SUPPORT_STAR_REVERSE_CLASSIFICATION.md | claims/p4/classifications/star/coincident-support-star-reverse/P4_COINCIDENT_SUPPORT_STAR_REVERSE_CLASSIFICATION.md |
| verify_p4_coincident_support_star_reverse_classification.py | claims/p4/classifications/star/coincident-support-star-reverse/verify_p4_coincident_support_star_reverse_classification.py |
| audit_p4_coincident_support_star_reverse_classification.py | claims/p4/classifications/star/coincident-support-star-reverse/audit_p4_coincident_support_star_reverse_classification.py |
| P4_COMMON_CENTER_KERNEL_STAR_211_COMPONENT.md | claims/p4/classifications/star/common-center-kernel-star-211/P4_COMMON_CENTER_KERNEL_STAR_211_COMPONENT.md |
| verify_p4_common_center_kernel_star_211_component.py | claims/p4/classifications/star/common-center-kernel-star-211/verify_p4_common_center_kernel_star_211_component.py |
| audit_p4_common_center_kernel_star_211_component.py | claims/p4/classifications/star/common-center-kernel-star-211/audit_p4_common_center_kernel_star_211_component.py |
| P4_DISJOINT_MIXED_STAR_AFFINE_CLASSIFICATION.md | claims/p4/classifications/star/disjoint-mixed-star-affine/P4_DISJOINT_MIXED_STAR_AFFINE_CLASSIFICATION.md |
| verify_p4_disjoint_mixed_star_affine_classification.py | claims/p4/classifications/star/disjoint-mixed-star-affine/verify_p4_disjoint_mixed_star_affine_classification.py |
| audit_p4_disjoint_mixed_star_affine_classification.py | claims/p4/classifications/star/disjoint-mixed-star-affine/audit_p4_disjoint_mixed_star_affine_classification.py |
| P4_DISJOINT_MIXED_STAR_PROJECTIVE_CLASSIFICATION.md | claims/p4/classifications/star/disjoint-mixed-star-projective/P4_DISJOINT_MIXED_STAR_PROJECTIVE_CLASSIFICATION.md |
| verify_p4_disjoint_mixed_star_projective_classification.py | claims/p4/classifications/star/disjoint-mixed-star-projective/verify_p4_disjoint_mixed_star_projective_classification.py |
| audit_p4_disjoint_mixed_star_projective_classification.py | claims/p4/classifications/star/disjoint-mixed-star-projective/audit_p4_disjoint_mixed_star_projective_classification.py |
| P4_EQUAL_ENDPOINT_INWARD_STAR_211_OBSTRUCTION.md | claims/p4/classifications/star/equal-endpoint-inward-star-211-obstruction/P4_EQUAL_ENDPOINT_INWARD_STAR_211_OBSTRUCTION.md |
| verify_p4_equal_endpoint_inward_star_211_obstruction.py | claims/p4/classifications/star/equal-endpoint-inward-star-211-obstruction/verify_p4_equal_endpoint_inward_star_211_obstruction.py |
| audit_p4_equal_endpoint_inward_star_211_obstruction.py | claims/p4/classifications/star/equal-endpoint-inward-star-211-obstruction/audit_p4_equal_endpoint_inward_star_211_obstruction.py |
| P4_MIXED_ENDPOINT_STAR_111_COMPLETE_CLASSIFICATION.md | claims/p4/classifications/star/mixed-endpoint-star-111-complete/P4_MIXED_ENDPOINT_STAR_111_COMPLETE_CLASSIFICATION.md |
| verify_p4_mixed_endpoint_star_111_complete_classification.py | claims/p4/classifications/star/mixed-endpoint-star-111-complete/verify_p4_mixed_endpoint_star_111_complete_classification.py |
| audit_p4_mixed_endpoint_star_111_complete_classification.py | claims/p4/classifications/star/mixed-endpoint-star-111-complete/audit_p4_mixed_endpoint_star_111_complete_classification.py |
| P4_NO_DOUBLE_ENDPOINT_STAR_1110_COLLISION_CLASSIFICATION.md | claims/p4/classifications/star/no-double-endpoint-star-1110-collision/P4_NO_DOUBLE_ENDPOINT_STAR_1110_COLLISION_CLASSIFICATION.md |
| verify_p4_no_double_endpoint_star_1110_collision_classification.py | claims/p4/classifications/star/no-double-endpoint-star-1110-collision/verify_p4_no_double_endpoint_star_1110_collision_classification.py |
| audit_p4_no_double_endpoint_star_1110_collision_classification.py | claims/p4/classifications/star/no-double-endpoint-star-1110-collision/audit_p4_no_double_endpoint_star_1110_collision_classification.py |
| P4_ONE_DOUBLE_ENDPOINT_STAR_111_CLASSIFICATION.md | claims/p4/classifications/star/one-double-endpoint-star-111/P4_ONE_DOUBLE_ENDPOINT_STAR_111_CLASSIFICATION.md |
| verify_p4_one_double_endpoint_star_111_classification.py | claims/p4/classifications/star/one-double-endpoint-star-111/verify_p4_one_double_endpoint_star_111_classification.py |
| audit_p4_one_double_endpoint_star_111_classification.py | claims/p4/classifications/star/one-double-endpoint-star-111/audit_p4_one_double_endpoint_star_111_classification.py |
| P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md | claims/p4/classifications/star/radical-star/P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md |
| verify_p4_radical_star_component_classification.py | claims/p4/classifications/star/radical-star/verify_p4_radical_star_component_classification.py |
| audit_p4_radical_star_component_classification.py | claims/p4/classifications/star/radical-star/audit_p4_radical_star_component_classification.py |
| P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md | claims/p4/classifications/star/rank-two-relation-star-obstruction/P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md |
| verify_p4_rank_two_relation_star_obstruction.py | claims/p4/classifications/star/rank-two-relation-star-obstruction/verify_p4_rank_two_relation_star_obstruction.py |
| audit_p4_rank_two_relation_star_obstruction.py | claims/p4/classifications/star/rank-two-relation-star-obstruction/audit_p4_rank_two_relation_star_obstruction.py |
| P4_TWO_DOUBLE_ENDPOINT_STAR_111_COMPLETE_CLASSIFICATION.md | claims/p4/classifications/star/two-double-endpoint-star-111-complete/P4_TWO_DOUBLE_ENDPOINT_STAR_111_COMPLETE_CLASSIFICATION.md |
| verify_p4_two_double_endpoint_star_111_complete_classification.py | claims/p4/classifications/star/two-double-endpoint-star-111-complete/verify_p4_two_double_endpoint_star_111_complete_classification.py |
| audit_p4_two_double_endpoint_star_111_complete_classification.py | claims/p4/classifications/star/two-double-endpoint-star-111-complete/audit_p4_two_double_endpoint_star_111_complete_classification.py |
| P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md | claims/p4/classifications/star/two-rank-two-spoke-mixed-star-classification/P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md |
| verify_p4_two_rank_two_spoke_mixed_star_classification.py | claims/p4/classifications/star/two-rank-two-spoke-mixed-star-classification/verify_p4_two_rank_two_spoke_mixed_star_classification.py |
| audit_p4_two_rank_two_spoke_mixed_star_classification.py | claims/p4/classifications/star/two-rank-two-spoke-mixed-star-classification/audit_p4_two_rank_two_spoke_mixed_star_classification.py |
| P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md | claims/p4/classifications/star/two-rank-two-spoke-mixed-star-component/P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md |
| verify_p4_two_rank_two_spoke_mixed_star_component.py | claims/p4/classifications/star/two-rank-two-spoke-mixed-star-component/verify_p4_two_rank_two_spoke_mixed_star_component.py |
| audit_p4_two_rank_two_spoke_mixed_star_component.py | claims/p4/classifications/star/two-rank-two-spoke-mixed-star-component/audit_p4_two_rank_two_spoke_mixed_star_component.py |
| P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPONENT.md | claims/p4/classifications/star/unequal-endpoint-inward-star-211/P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPONENT.md |
| verify_p4_unequal_endpoint_inward_star_211_component.py | claims/p4/classifications/star/unequal-endpoint-inward-star-211/verify_p4_unequal_endpoint_inward_star_211_component.py |
| audit_p4_unequal_endpoint_inward_star_211_component.py | claims/p4/classifications/star/unequal-endpoint-inward-star-211/audit_p4_unequal_endpoint_inward_star_211_component.py |

## Dependency summary

### Intra-batch chains

Zero Python imports between selected modules (verified by a full
regex scan of all 51 scripts).  The only intra-batch couplings are
verifier path-constant references to *documents* of sibling selected
packages (all resolve through repo-root-relative constants after the
move):

```text
verify_p4_mixed_endpoint_star_111_complete_classification
    references  P4_DISJOINT_MIXED_STAR_PROJECTIVE_CLASSIFICATION.md (moves)
verify_p4_no_double_endpoint_star_1110_collision_classification
    references  P4_COINCIDENT_SUPPORT_STAR_REVERSE_CLASSIFICATION.md (moves)
    references  P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md (moves)
verify_p4_two_double_endpoint_star_111_complete_classification
    references  P4_COINCIDENT_SUPPORT_STAR_REVERSE_CLASSIFICATION.md (moves)
```

### Cross-spine dependencies on already-migrated packages (STAY put)

```text
claims/p4/components/disjoint-mixed-star/          (Stage 3/4)
    inbound links from both disjoint-mixed-star-* packages
claims/p4/components/{all-rank-one-triangle, six-dimensional,
                      mixed-orientation, diagonal-quadric}/
    hash/reference P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md (moves)
claims/p4/classifications/triangle-211/triple-kernel-rank-one-triangle/
    hashed by verify_p4_two_double_endpoint_star_111_complete_classification
claims/p4/classifications/triangle-211/unequal-endpoint-inward-star-211-complete/
    links P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPONENT.md (moves)
claims/p4/classifications/triangle-211/cyclic-rank-one-triangle-support/
    links P4_DISJOINT_MIXED_STAR_PROJECTIVE_CLASSIFICATION.md (moves)
```

None of these already-migrated packages is relocated.

### Staying root consumers repaired in Commit D (path constants)

```text
verify_p4_all_pair_rank_exceptional_graph_reduction.py   (8 selected docs in RESOLUTION_PACKAGES)
audit_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py   (hashes coincident-support doc+verifier)
verify_p5_component21_pq_zero_normal_blowup_transfer_obstruction.py  (P4_PRIMARY constant)
audit_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py  (P4_SCRIPT constant)
derive_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py (COMPONENT constant)
verify_p5_h31_coincident_support_rank_one_star_component_generic_obstruction.py (COMPONENT constant)
verify_p5_h22_two_rank_two_spoke_mixed_star_component_generic_obstruction.py    (COMPONENT constant)
verify_p5_h22_two_rank_two_spoke_mixed_star_dense_marking_obstruction.py        (COMPONENT constant)
verify_p5_high_coordinate_partial_frontier.py          (radical-star doc in SOURCES tuple)
verify_p5_h31_two_rank_two_spoke_mixed_star_component_generic_obstruction.py    (BARE IMPORT: expose_claim_package)
claims/p4/components/all-rank-one-triangle/verify_p4_all_rank_one_triangle_pure_component.py      (REPO_ROOT constant)
claims/p4/components/disjoint-mixed-star/verify_p4_disjoint_mixed_star_pure_component.py          (REPO_ROOT constant)
claims/p4/components/mixed-orientation/verify_p4_mixed_orientation_pure_component.py              (REPO_ROOT constant)
claims/p4/components/six-dimensional/verify_p4_six_dimensional_pure_component.py                  (REPO_ROOT constant)
```

`verify_p4_common_singleton_component.py` needs **no** repair: its
fragment-source resolver consults `catalog/moved-paths.json` and
finds the moved
`verify_p4_two_rank_two_spoke_mixed_star_component.py`
automatically.

### Moving scripts needing REPO_ROOT repair (Commit D)

Verifiers whose `ROOT = Path(__file__).parent` constants point at
root-resident documents after the move (switched to the centralized
bootstrap, siblings via `HERE`, root-resident docs and `tmp/` via
`REPO_ROOT`):

```text
verify_p4_radical_star_component_classification.py
verify_p4_mixed_endpoint_star_111_complete_classification.py
verify_p4_two_double_endpoint_star_111_complete_classification.py
verify_p4_no_double_endpoint_star_1110_collision_classification.py
audit_p4_radical_star_component_classification.py
audit_p4_coincident_support_star_reverse_classification.py
audit_p4_common_center_kernel_star_211_component.py
```

(The audits' package-local references survive the move unchanged;
only their `ROOT = parent` idiom is re-anchored for consistency with
the established bootstrap pattern where they also write to `tmp/`.)

### Replay commands affected

34 replay fences inside the 17 moving docs (17 verifiers + 17
audits; `uv run --with sympy python` single-line forms plus one
continuation-line `python \` + filename pair in the radical-star
doc — all covered by the shared grammar), plus fences outside the
batch in README and handoff docs (handled by the same rewriter).

### Preflight replayability (all performed pre-freeze, rc=0, from repo root)

| script class | result |
|---|---|
| 15 sympy-only packages (30 scripts) | all rc=0, ≤3.4 s each |
| one-double-endpoint verifier (Singular exact radical, WSL fallback) | rc=0, 2.4 s |
| one-double-endpoint audit | rc=0, 0.7 s |
| no-double-endpoint-collision verifier (Singular, WSL) | rc=0, 6.3 s |
| no-double-endpoint-collision audit | rc=0, 1.4 s |

Singular 4.3.2 executed via WSL (`/usr/bin/Singular`); no native
Windows Singular on PATH.  No extreme runtimes; all replays
practical for this PR.  Outputs land in `tmp/` (gitignored).

### Ledger references

Zero ledger entries reference any of the 51 moving files (the ledger
is a curated partial index centered on the P5 H22/H31 claims, which
stay).  No repoints; hash refresh only for ledger docs whose content
changes during rewrites (README.md expected).  No entries fabricated.

## Integrity summary

| measure | value |
|---|---|
| member count | 51 |
| package count | 17 (all complete triples) |
| confidence composition | all 51 members review_required (17 medium docs, 34 low claim_scripts); 0 high-confidence; no promotions |
| destination collisions | none (17 new package directories) |
| source/destination cycles | none |
| expected stale-path count increase | +51 (all root→package basename-preserving; 114 → 165) |
| expected root-entry decrease | −51 (2,258 → 2,207; all 51 sources are root files) |
| ledger entries affected | 0 repointed; hash refresh only for touched ledger docs |
| manifest summary expectations | moved 114 → 165; review_required 1540 → 1489; proposed_high_confidence 361 (unchanged); projected_root_if_moved_only 2258 → 2207 (executor recomputes, no rebuild) |
| source classifier records refined | 51 (39 from p4/classifications, 12 from p4/boundaries — the boundary reassignment is a human ownership decision recorded by approval, accounted separately from the classifications-bucket remainder) |

## Exclusions

| candidate | decision | reason |
|---|---|---|
| P4_RANK_TWO_RELATION_STAR_OBSTRUCTION_WITHDRAWN_OVERSTRONG (+verify/audit) | exclude | withdrawn historical artifact; classifier proposes `claims/legacy/` (high confidence); belongs to a dedicated legacy batch, not the star classification spine; the selected obstruction package does not import it |
| P5 H22/H31 star-consumer population | out of scope | downstream consumers; P5 migration is a later stage |
| remaining `claims/p4/classifications` records (122 − 39 = 83 after refinement) | out of scope | other families / unreviewed; Stage 7+ |
| remaining `claims/p4/boundaries` population (minus the 12 refined) | out of scope | boundary claims not star-owned |
| shared machinery (directed-zero-divisor, common-singleton, all-pair-rank reducer) | stays | shared_dependency / atlas roles |

## Cross-package acceptance note

This batch moves 17 complete triples with zero intra-batch Python
imports, two Singular-dependent packages, three moving verifiers
that reference sibling moving docs, one staying P5 verifier with a
bare import of a moving module, and four already-migrated
cross-spine families (components + triangle-211) that must remain
stable while their links/constants are repaired.  The rewriter's
second pass must report 0/0/0, and the h31 two-rank-two-spoke bare
import must resolve from a clean checkout after Commit D.
