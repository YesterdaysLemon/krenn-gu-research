# Stage 7 dry-run: P4 pair-geometry classification/boundary spine

Generated before execution, from the tree at the Stage 7 starting
SHA `22b674e` (merged `main` including PR #34 / Stage 6), branch
`layout-migration-stage7-p4-pair-geometry`, plus the Stage 7
machinery-fix commit `8e36cc5` (shared replay grammar: uv-wrapper
continuation form; suite 107 → 112).

Approval artifact: `catalog/batches/p4-pair-geometry-stage7.json`
(produced after this report).  Approval:

```text
YesterdaysLemon (repository owner), Stage 7 P4 pair-geometry classification/boundary migration instruction
```

applies only to the exact generated mappings recorded in that batch
file.  It does not authorize all remaining `p4/classifications`, all
`p4/boundaries`, P5 lower-pair/tangent/secant claims, global
pair-rank machinery, legacy files, or future batches.

## Baseline (measured at `22b674e`, before any Stage 7 change)

```text
starting main SHA               22b674e0d4f5fad8c4c1a2fc5eef4c8a1cd2785a
root entries                    2207
manifest moved                  165
proposed_high_confidence        361
review_required                 1489
unclassified                    348
remaining p4/classifications    83
remaining p4/boundaries         73
stale enforced                  165 (3 full-path, 162 root-to-package)
migration-tool tests            107  (112 after the grammar fix commit)
ledger entries                  85
markdown files                  773
python files compiled           1698
```

## Scope and stop-condition verdict

**Batch: 12 packages / 42 files** (10 classification packages = 36
files, 2 boundary packages = 6 files; preferred range 10–16 packages,
35–55 files — hit on both; hard ceiling 65 not approached).

The pure-rank-two cluster resolves to **Outcome A** (one mathematical
package with canonical/closure/reduction documents plus a toric
boundary subclaim in the existing `boundaries/` subpackage); see the
dedicated section below.

## Candidate review

| seed | classifier family | decision | rationale |
|---|---|---|---|
| P4_RANK_ONE_PAIR_OBSTRUCTION | p4/boundaries | **include** (reassign → classifications) | closes pair-image ranks 0/1; structural theorem, not a boundary inclusion; complete triple |
| P4_RANK_TWO_PAIR_KERNEL_GEOMETRY | p4/boundaries | **include** (reassign → classifications) | secant/tangent kernel dichotomy structural theorem; verifier present; **no independent audit exists** — the doc states the verifier is a tiny exact replay, not a proof substitute; intentional documented state |
| P4_DISJOINT_SECANT_LOWER_PAIR_COMPONENT | p4/classifications | **include** | component 15 theorem; complete triple |
| P4_OVERLAPPING_SECANT_LOWER_PAIR_CLASSIFICATION | p4/classifications | **include** | overlapping secant stratum = known sixfold; complete triple; cross-spine dep on `claims/p4/components/six-dimensional` (stays) |
| P4_FULL_SUPPORT_TANGENT_PAIR_COMPONENT | p4/classifications | **include** | component 14 theorem; complete triple |
| P4_TANGENT_RANK_TWO_PAIR_PURITY_CLASSIFICATION | p4/classifications | **include** | tangent rank-two pair classification; complete triple |
| P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION | p4/classifications | **include** | **corollary document only** — its stated replay is the union of the eight sibling pair-geometry scripts (all in this batch); no dedicated verifier/audit exists; intentional documented state |
| P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION | p4/boundaries | **include** (stays boundary) | explicit boundary theorem (support-one secants lie in the disjoint-secant closure); complete triple; classifier category confirmed by review |
| P4_SUPPORT_TWO_TANGENT_FLAG_BOUNDARY_INCLUSION | p4/boundaries | **include** (stays boundary) | explicit boundary theorem (support-two tangent flags lie on the sixfold); complete triple |
| P4_PURE_RANK_TWO_COMPONENT_THEOREM | p4/classifications | **include** (pure-rank-two package) | canonical component theorem; verifier/audit use the short stem `verify_p4_pure_rank_two_component.py` / `audit_…_component.py` (sole referrers) |
| P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE | p4/classifications | **include** (pure-rank-two package) | chart closure of the same component; complete triple |
| P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY | p4/classifications | **include** (pure-rank-two package, `boundaries/` subpackage) | toric boundary fan **subclaim** of the same component; its own doc links the Segre reduction; boundary-flavored but pair-geometry-owned |
| P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION | p4/classifications | **include** (pure-rank-two package) | Segre slice reduction; complete triple under the short stem |
| P4_DECOMPOSABLE_RANK_TWO_FAMILY | p4/boundaries | **include** (reassign → classifications) | five-parameter family construction feeding the pure-rank-two component theorem; structural theorem; complete triple |
| P4_DECOMPOSABLE_RESTRICTION_RANK_DROP | p4/boundaries | **include** (reassign → classifications) | rank-drop tensor theorem; structural theorem; complete triple |
| P4_MARKED_DELTA2_SLICE_CLASSIFICATION | p4/classifications | **DEFER** | q4_211 marked boundary (`P_4 -> Delta_2`), consumed by `P5_Q4_211_*` claims; not pair-geometry-owned |
| P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION | p4/classifications | **DEFER** | companion of the delta2 slice; same q4_211 boundary population |
| P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION | p4/classifications | **DEFER** | five primes of the mixed-orientation normal form; owned by the already-migrated `claims/p4/components/mixed-orientation` family |

### Default exclusions honored

- `P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION` (+ verify/audit) —
  **shared/global** machinery spanning stars, triangles, pair
  geometry; stays at root (its `RESOLUTION_PACKAGES` list is repointed
  in Commit D).
- `verify_p4_directed_zero_divisor_triangle_components`,
  `verify_p4_common_singleton_component` — shared machinery, stay
  (the singleton's migration-aware resolver needs no repair).
- P5 consumers (H22/H31 first-rank-two, disjoint-secant,
  full-support-tangent, toric-marked-fibre, q5_311, component23
  lower-pair endpoints, etc.) — downstream, stay.
- Withdrawn/superseded rank-two artifacts — legacy bucket, not
  touched.

## Exact package inventory

| package (slug) | category | canonical claim | other owned claims | verifiers | audits | support | destination |
|---|---|---|---|---|---|---|---|
| rank-one-pair-obstruction | classifications | P4_RANK_ONE_PAIR_OBSTRUCTION.md | — | verify_p4_rank_one_pair_obstruction.py | audit_… | none | claims/p4/classifications/pair-geometry/rank-one-pair-obstruction/ |
| rank-two-pair-kernel-geometry | classifications | P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md | — | verify_p4_rank_two_pair_kernel_geometry.py | **none (documented)** | none | claims/p4/classifications/pair-geometry/rank-two-pair-kernel-geometry/ |
| disjoint-secant-lower-pair | classifications | P4_DISJOINT_SECANT_LOWER_PAIR_COMPONENT.md | — | complete triple | | none | claims/p4/classifications/pair-geometry/disjoint-secant-lower-pair/ |
| overlapping-secant-lower-pair | classifications | P4_OVERLAPPING_SECANT_LOWER_PAIR_CLASSIFICATION.md | — | complete triple | | none | claims/p4/classifications/pair-geometry/overlapping-secant-lower-pair/ |
| full-support-tangent-pair | classifications | P4_FULL_SUPPORT_TANGENT_PAIR_COMPONENT.md | — | complete triple | | none | claims/p4/classifications/pair-geometry/full-support-tangent-pair/ |
| tangent-rank-two-pair-purity | classifications | P4_TANGENT_RANK_TWO_PAIR_PURITY_CLASSIFICATION.md | — | complete triple | | none | claims/p4/classifications/pair-geometry/tangent-rank-two-pair-purity/ |
| decomposable-rank-two-family | classifications | P4_DECOMPOSABLE_RANK_TWO_FAMILY.md | — | complete triple | | none | claims/p4/classifications/pair-geometry/decomposable-rank-two-family/ |
| decomposable-restriction-rank-drop | classifications | P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md | — | complete triple | | none | claims/p4/classifications/pair-geometry/decomposable-restriction-rank-drop/ |
| lower-pair-rank-exhaustion | classifications | P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md | — | **corollary doc only** (replay = union of 8 sibling scripts) | | none | claims/p4/classifications/pair-geometry/lower-pair-rank-exhaustion/ |
| pure-rank-two | classifications | P4_PURE_RANK_TWO_COMPONENT_THEOREM.md | CHART_CLOSURE (closure), TORIC_SLICE_SEGRE_REDUCTION (reduction), TORIC_BOUNDARY (boundary subclaim, `boundaries/` subpackage) | verify_p4_pure_rank_two_component.py, …_chart_closure.py, …_toric_slice_segre.py, …_toric_boundary.py | corresponding 4 audits | none | claims/p4/classifications/pair-geometry/pure-rank-two/ (+ boundaries/) |
| support-one-secant | boundaries | P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md | — | complete triple | | none | claims/p4/boundaries/pair-geometry/support-one-secant/ |
| support-two-tangent-flag | boundaries | P4_SUPPORT_TWO_TANGENT_FLAG_BOUNDARY_INCLUSION.md | — | complete triple | | none | claims/p4/boundaries/pair-geometry/support-two-tangent-flag/ |

Shared dependencies that stay: the three global/shared machinery
scripts above; `claims/p4/components/six-dimensional` and
`claims/p4/components/diagonal-quadric` docs (cross-spine, already
migrated); root-resident docs referenced by moving verifiers (root
docs such as `P4_FIRST_COMPONENT_APOLAR_TRIANGLE_NORMAL_FORM.md`
stay).

Downstream consumers (stay): `derive_p5_h31_toric_marked_fibre_elimination.py`
(bare import → `expose_claim_package` repair),
`verify_p4_common_active_binary_triangle_p_plus_q_boundary.py`
(subprocess-replays six selected verifiers — path repair),
four component20 candidates, four already-migrated component/star
verifiers hashing pure-rank-two/lower-pair docs, and the P5 H22/H31
consumer family listed below.

## Pure-rank-two cluster — ownership resolution (Outcome A)

The four documents form one connected component narrative:

```text
P4_PURE_RANK_TWO_COMPONENT_THEOREM          canonical: 5-dim component of the
                                            decomposable rank-two family closure
        ├── P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE
        │       closure certificate of the same component chart
        ├── P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY
        │       boundary fan subclaim (toric threefold boundary)
        └── P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION
                reduction subclaim closing the 21 divisor orientations
```

Each subclaim carries its own verifier + audit with independent
implementations, so provenance stays per-executable.  The toric
boundary is boundary-flavored but is **owned by this component's
geometry** (no other classification consumes it as its own boundary),
so it goes into the package's `boundaries/` subpackage exactly as the
Stage 1 pilot established for the P5 disjoint-mixed-star component.
The existing metadata model already expresses this
(`claim_package` from the manifest family; `subpackage: boundaries`;
`proof_variant: canonical` for root-level non-working-note docs);
**no metadata-model extension was needed**.

## Dependency graph

### Intra-batch edges

- **Python imports: none** (full regex scan of all 27 scripts).
- Doc cross-references (path constants inside moving verifiers):

```text
verify_p4_pure_rank_two_component            -> P4_DECOMPOSABLE_RANK_TWO_FAMILY.md (moves)
verify_p4_pure_rank_two_component_chart_closure -> P4_PURE_RANK_TWO_COMPONENT_THEOREM.md (moves)
verify_p4_pure_rank_two_toric_slice_segre    -> P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md (moves)
verify_p4_pure_rank_two_component_toric_boundary
    -> P5_H31_* root docs (stay; REPO_ROOT constants)
```

### Cross-spine P4 (already migrated, stay)

```text
claims/p4/components/six-dimensional         <- overlapping secant + support-two flag
claims/p4/components/diagonal-quadric        <- pure-rank-two theorem + toric boundary docs
claims/p4/classifications/star/no-double-endpoint-star-1110-collision
                                             <- hashes LOWER_PAIR exhaustion doc (moves)
```

### Shared root (stay)

```text
verify_p4_all_pair_rank_exceptional_graph_reduction.py   (RESOLUTION_PACKAGES repair)
verify_p4_common_active_binary_triangle_p_plus_q_boundary.py
    (subprocess-replays 6 moving verifiers: CLASSIFICATION_VERIFIERS paths)
verify_p4_common_singleton_component.py      (migration-aware resolver; no repair)
verify_p4_diagonal_quadric_one_three_components.py (path constant)
branch_invariants_and_sieve.py               (prose comment only)
4x component20 audit/derive candidates       (hash/path constants)
```

### P5 downstream (stay)

```text
derive_p5_h31_toric_marked_fibre_elimination.py   BARE IMPORT -> expose_claim_package
verify_p5_h31_toric_marked_fibre_obstruction.py
verify_p5_h31_internal_e0_marked_fibre.py
verify_p5_h31_{marked_basis_fibre_classification, marked_basis_open_branch,
               rank_two_component_orbit, known_rank_two_family_obstruction,
               component_chart_boundary, component_chart_boundary_marked_fibre,
               component_fiber_infinity, component_fibre_infinity_marked_fibre}.py
verify_p5_h22_first_rank_two_component_generic_obstruction.py
verify_p5_high_coordinate_partial_frontier.py
verify_p5_q5_311_exclusion.py, verify_p5_two_singleton_coordinate_obstruction.py
```

### Ledger

Zero ledger entries reference any of the 42 moving files.  No
repoints; hash refresh only for ledger docs whose content changes
during rewrites.

## Mapping (exact, 42 moves)

| old path | new path |
|---|---|
| P4_DECOMPOSABLE_RANK_TWO_FAMILY.md | claims/p4/classifications/pair-geometry/decomposable-rank-two-family/P4_DECOMPOSABLE_RANK_TWO_FAMILY.md |
| audit_p4_decomposable_rank_two_family.py | claims/p4/classifications/pair-geometry/decomposable-rank-two-family/audit_p4_decomposable_rank_two_family.py |
| verify_p4_decomposable_rank_two_family.py | claims/p4/classifications/pair-geometry/decomposable-rank-two-family/verify_p4_decomposable_rank_two_family.py |
| P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md | claims/p4/classifications/pair-geometry/decomposable-restriction-rank-drop/P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md |
| audit_p4_decomposable_restriction_rank_drop.py | claims/p4/classifications/pair-geometry/decomposable-restriction-rank-drop/audit_p4_decomposable_restriction_rank_drop.py |
| verify_p4_decomposable_restriction_rank_drop.py | claims/p4/classifications/pair-geometry/decomposable-restriction-rank-drop/verify_p4_decomposable_restriction_rank_drop.py |
| P4_DISJOINT_SECANT_LOWER_PAIR_COMPONENT.md | claims/p4/classifications/pair-geometry/disjoint-secant-lower-pair/P4_DISJOINT_SECANT_LOWER_PAIR_COMPONENT.md |
| audit_p4_disjoint_secant_lower_pair_component.py | claims/p4/classifications/pair-geometry/disjoint-secant-lower-pair/audit_p4_disjoint_secant_lower_pair_component.py |
| verify_p4_disjoint_secant_lower_pair_component.py | claims/p4/classifications/pair-geometry/disjoint-secant-lower-pair/verify_p4_disjoint_secant_lower_pair_component.py |
| P4_FULL_SUPPORT_TANGENT_PAIR_COMPONENT.md | claims/p4/classifications/pair-geometry/full-support-tangent-pair/P4_FULL_SUPPORT_TANGENT_PAIR_COMPONENT.md |
| audit_p4_full_support_tangent_pair_component.py | claims/p4/classifications/pair-geometry/full-support-tangent-pair/audit_p4_full_support_tangent_pair_component.py |
| verify_p4_full_support_tangent_pair_component.py | claims/p4/classifications/pair-geometry/full-support-tangent-pair/verify_p4_full_support_tangent_pair_component.py |
| P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md | claims/p4/classifications/pair-geometry/lower-pair-rank-exhaustion/P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md |
| P4_OVERLAPPING_SECANT_LOWER_PAIR_CLASSIFICATION.md | claims/p4/classifications/pair-geometry/overlapping-secant-lower-pair/P4_OVERLAPPING_SECANT_LOWER_PAIR_CLASSIFICATION.md |
| audit_p4_overlapping_secant_lower_pair_classification.py | claims/p4/classifications/pair-geometry/overlapping-secant-lower-pair/audit_p4_overlapping_secant_lower_pair_classification.py |
| verify_p4_overlapping_secant_lower_pair_classification.py | claims/p4/classifications/pair-geometry/overlapping-secant-lower-pair/verify_p4_overlapping_secant_lower_pair_classification.py |
| P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md | claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md |
| audit_p4_pure_rank_two_component_chart_closure.py | claims/p4/classifications/pair-geometry/pure-rank-two/audit_p4_pure_rank_two_component_chart_closure.py |
| verify_p4_pure_rank_two_component_chart_closure.py | claims/p4/classifications/pair-geometry/pure-rank-two/verify_p4_pure_rank_two_component_chart_closure.py |
| P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md | claims/p4/classifications/pair-geometry/pure-rank-two/boundaries/P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md |
| audit_p4_pure_rank_two_component_toric_boundary.py | claims/p4/classifications/pair-geometry/pure-rank-two/boundaries/audit_p4_pure_rank_two_component_toric_boundary.py |
| verify_p4_pure_rank_two_component_toric_boundary.py | claims/p4/classifications/pair-geometry/pure-rank-two/boundaries/verify_p4_pure_rank_two_component_toric_boundary.py |
| P4_PURE_RANK_TWO_COMPONENT_THEOREM.md | claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_THEOREM.md |
| audit_p4_pure_rank_two_component.py | claims/p4/classifications/pair-geometry/pure-rank-two/audit_p4_pure_rank_two_component.py |
| verify_p4_pure_rank_two_component.py | claims/p4/classifications/pair-geometry/pure-rank-two/verify_p4_pure_rank_two_component.py |
| P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md | claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md |
| audit_p4_pure_rank_two_toric_slice_segre.py | claims/p4/classifications/pair-geometry/pure-rank-two/audit_p4_pure_rank_two_toric_slice_segre.py |
| verify_p4_pure_rank_two_toric_slice_segre.py | claims/p4/classifications/pair-geometry/pure-rank-two/verify_p4_pure_rank_two_toric_slice_segre.py |
| P4_RANK_ONE_PAIR_OBSTRUCTION.md | claims/p4/classifications/pair-geometry/rank-one-pair-obstruction/P4_RANK_ONE_PAIR_OBSTRUCTION.md |
| audit_p4_rank_one_pair_obstruction.py | claims/p4/classifications/pair-geometry/rank-one-pair-obstruction/audit_p4_rank_one_pair_obstruction.py |
| verify_p4_rank_one_pair_obstruction.py | claims/p4/classifications/pair-geometry/rank-one-pair-obstruction/verify_p4_rank_one_pair_obstruction.py |
| P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md | claims/p4/classifications/pair-geometry/rank-two-pair-kernel-geometry/P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md |
| verify_p4_rank_two_pair_kernel_geometry.py | claims/p4/classifications/pair-geometry/rank-two-pair-kernel-geometry/verify_p4_rank_two_pair_kernel_geometry.py |
| P4_TANGENT_RANK_TWO_PAIR_PURITY_CLASSIFICATION.md | claims/p4/classifications/pair-geometry/tangent-rank-two-pair-purity/P4_TANGENT_RANK_TWO_PAIR_PURITY_CLASSIFICATION.md |
| audit_p4_tangent_rank_two_pair_purity_classification.py | claims/p4/classifications/pair-geometry/tangent-rank-two-pair-purity/audit_p4_tangent_rank_two_pair_purity_classification.py |
| verify_p4_tangent_rank_two_pair_purity_classification.py | claims/p4/classifications/pair-geometry/tangent-rank-two-pair-purity/verify_p4_tangent_rank_two_pair_purity_classification.py |
| P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md | claims/p4/boundaries/pair-geometry/support-one-secant/P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md |
| audit_p4_support_one_secant_boundary_inclusion.py | claims/p4/boundaries/pair-geometry/support-one-secant/audit_p4_support_one_secant_boundary_inclusion.py |
| verify_p4_support_one_secant_boundary_inclusion.py | claims/p4/boundaries/pair-geometry/support-one-secant/verify_p4_support_one_secant_boundary_inclusion.py |
| P4_SUPPORT_TWO_TANGENT_FLAG_BOUNDARY_INCLUSION.md | claims/p4/boundaries/pair-geometry/support-two-tangent-flag/P4_SUPPORT_TWO_TANGENT_FLAG_BOUNDARY_INCLUSION.md |
| audit_p4_support_two_tangent_flag_boundary_inclusion.py | claims/p4/boundaries/pair-geometry/support-two-tangent-flag/audit_p4_support_two_tangent_flag_boundary_inclusion.py |
| verify_p4_support_two_tangent_flag_boundary_inclusion.py | claims/p4/boundaries/pair-geometry/support-two-tangent-flag/verify_p4_support_two_tangent_flag_boundary_inclusion.py |

## Classification refinement (durable, rebuild-safe)

For the 42 selected records, `catalog/layout-classification.json` —
the durable source — was edited:

```text
claim_family:  p4/boundaries (19 records) | p4/classifications (23)
           ->  p4/classifications/pair-geometry/<slug>   (36 records)
               p4/boundaries/pair-geometry/<slug>        (6 records)
proposed_path: -> matching claims/... destinations (the 3 pure-rank-two
               toric-boundary files gain the boundaries/ subpackage)
evidence:      + "stage7_human_review: P4 pair-geometry spine package"
               (11 records additionally carry the boundary->
               classification reassignment marker: the three records
               each of rank-one-pair-obstruction,
               decomposable-rank-two-family, and
               decomposable-restriction-rank-drop, plus the two
               rank-two-pair-kernel-geometry records — each document's
               status states it is a structural component/rank theorem,
               not a boundary inclusion)
```

`build_manifest.py` was then run normally.  Verified against the
committed manifest:

- **42 records changed**, all `review_required -> review_required`
  (no status promotion; confidence untouched);
- all **165 already-moved records byte-identical**, `executed_batch`
  preserved 165/165;
- counts unchanged (moved 165, proposed 361, review 1489,
  projected_root_if_moved_only 2207);
- no record outside the selection changed;
- **cross-category arithmetic**: 19 members originate in
  `p4/boundaries` and 23 in `p4/classifications`; the post-move
  family populations are therefore 83 − 23 = 60 remaining
  `p4/classifications` proposals and 73 − 19 = 54 remaining
  `p4/boundaries` proposals (naive total subtraction would be wrong).

## Projections (expected, measured after execution)

| measure | projection |
|---|---|
| package count | 12 (10 classifications + 2 boundaries) |
| member count | 42 (36 + 6) |
| starting-status composition | 42 review_required; 0 high-confidence |
| destination collisions | none |
| source/destination cycles | none |
| expected root-entry decrease | −42 (2,207 → 2,165; all sources are root files) |
| expected stale-path increase | +42 (165 → 207; all basename-preserving root→package) |
| manifest-state transitions | moved 165 → 207; review_required 1489 → 1447; proposed 361 unchanged; projected_root_if_moved_only 2207 → 2165 |
| ledger entries affected | 0 repointed; hash refresh only for touched ledger docs |
| links/commands likely affected | inbound links ≈ 53 across ~30 staying docs; 42 replay commands inside moving docs (incl. 15 in the exhaustion corollary and the first uv-continuation form); plus README/handoff fences |

## Preflight replayability (all performed pre-freeze, rc=0, from repo root)

| script class | result |
|---|---|
| 27 scripts (all sympy-only; no external solvers in the batch) | all rc=0, ≤3.8 s each |

No extreme runtimes; all replays practical for this PR.  Outputs land
in `tmp/` (gitignored).  Manual Windows replay; no Singular/msolve/
SAT required by any selected package.

## Machinery note

Stage 7 discovered one genuine grammar gap before freezing:
`uv run --with sympy \` + next-line `python script.py` (used by the
kernel-geometry doc) was not a recognized continuation form.  Fixed
narrowly in the shared grammar (`LAUNCHER_UV_CONTINUATION`, commit
`8e36cc5`) with 5 regression tests; rewriter and stale scanner share
the fix through `match_replay`.  No other machinery change.
