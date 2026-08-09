# Layout migration report — Stage 13 (split-center mixed-star H22)

Status: **the exact Stage 13 migration transaction is complete locally and
ready for a fresh merge-gate review.**  One coherent three-file claim package
left repository root: its theorem document, exact Singular-backed primary
verifier, and existing no-import exact-rational audit.

> **Scientific status did not change.**  The theorem remains a generic
> function-field obstruction.  It covers every finite `[lambda:1]` weight and
> `[1:0]`, while special component-parameter divisor fibres and projective
> component-boundary fibres remain open.  The audit corroborates selected
> exact-rational witnesses and does not replace the generic proof.  The global
> Krenn–Gu conjecture remains **UNRESOLVED**.

## Provenance anchors

- Exact merged baseline: `8acb404de48871f5fbc8d3b852434e886c3c2049`.
- Branch: `codex/stage13-split-center-migration`.
- Frozen batch commit: `1822359b173d5c33aa01bfcbdecb7fe02b99f00b`.
- Pure move commit: `142173063c2e8ad02ffd05d9c28dd1d86963ff76`.
- Mechanical repair commit: `22aa9d911ea9bcde3c2d76d00078ea6c43eae01d`.
- Ownership audit:
  [`p5-candidate-helper-ownership-stage12.md`](p5-candidate-helper-ownership-stage12.md).
- Exact-commit dry run:
  [`p5-h22-split-center-stage13-dry-run.md`](p5-h22-split-center-stage13-dry-run.md).
- Frozen batch: `catalog/batches/p5-h22-split-center-stage13.json`:
  - approved by the repository owner with the exact words
    `Approved exactly as listed`;
  - base SHA: `8acb404de48871f5fbc8d3b852434e886c3c2049`;
  - member count: 3;
  - mapping SHA-256:
    `fd1d3e4163068b2e0e16f6e6161a52f822a4d02acd74bdd5e80e5bc6ba341154`;
  - approval-time manifest SHA-256:
    `3d254459159bd136f4d2e9cc4c6d1fcbd75384c5548fa1059df4b1e7edbf40d3`.

The owner also delegated future evidence-backed layout mapping decisions to
the lead agent.  That standing delegation does not authorize mathematical
status or scope changes, ambiguous owner-taste architecture, destructive
history changes, or bypass of a frozen exact batch and required review.

## Selected package and exclusions

The exact package is:

| role | destination |
|---|---|
| theorem | `claims/p5/h22/split-center-mixed-star/P5_H22_SPLIT_CENTER_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` |
| primary verifier | `claims/p5/h22/split-center-mixed-star/verify_p5_h22_split_center_mixed_star_component_generic_obstruction.py` |
| independent audit | `claims/p5/h22/split-center-mixed-star/audit_p5_h22_split_center_mixed_star_component_generic_obstruction.py` |

The candidate-housed four-source weighted-H22 construction helper, marked
basis helper, H31 sibling, component-boundary files, and special-fibre work did
not move.  Stage 12 established that the selected claim package has coherent
ownership while the reusable helper still has mixed ownership and 39 direct
import consumers.

## Pure-move acceptance

Against the pure move commit's direct parent:

- all three exact sources are absent and all three destinations are present;
- every destination blob is byte-identical to its source-parent blob;
- Git records all three moves as `R100`;
- the only non-rename change is the mechanical manifest transaction;
- each selected manifest record is `moved` and names
  `p5-h22-split-center-stage13` as `executed_batch`;
- no theorem prose or executable content changed in the pure move commit.

Recorded source/destination blob identities:

| role | Git blob |
|---|---|
| theorem | `c8eed302f89c10faf71a56d547b9842cdef12d73` |
| audit | `07bcb2c0747e62bea5710d8ed3b298ffe21d00e6` |
| primary | `cbfe839b95a8832b2956c814b8a320d9e14d5f62` |

Observed post-move arithmetic:

| measure | before | after |
|---|---:|---:|
| manifest `moved` | 350 | 353 |
| manifest `proposed_high_confidence` | 252 | 249 |
| manifest `review_required` | 1,413 | 1,413 |
| measured root files | 2,014 | 2,011 |
| measured root directories | 9 | 9 |
| measured root entries | 2,023 | 2,020 |
| grandfathered root debt | 2,007 | 2,004 |
| enforceable retired paths | 350 | 353 |

## Mechanical repair

The migration rewriter updated the root README link, the handoff link and two
replay commands, and the existing ledger entry.  Explicit repairs then:

- changed all four theorem replay/lint/compile commands to root-relative
  forward-slash destination paths;
- added the package and its two root shared dependencies to the H22 index;
- corrected the H22 index's blanket weight-slope wording;
- recorded claim-package metadata and all three legacy paths in the ledger;
- refreshed the moved theorem's staged-index document hash; and
- refreshed the three ledger entries whose document is the changed root
  README.

No assertion, algebra, solver strategy, coefficient domain, evidence role,
status, or lifecycle field changed.  Two consecutive final rewriter passes
reported zero links, zero replay commands, zero touched files, and no
ambiguities.

## Mandatory post-move replay

Both commands ran from repository root under Windows Python 3.13.14, SymPy
1.14.0, and `uv` 0.11.8.  The primary used WSL `/usr/bin/Singular` 4.3.2 as
its external exact backend.

| role | result | script elapsed | wall elapsed |
|---|---|---:|---:|
| primary | pass; four projections, six branch unit ideals, both direction orbits empty, generic weighted H22 fibre empty; special fibres/global result false | 120.514 s | 122.123 s |
| audit | pass; seven exact-rational witnesses, including both rational roots of the quadratic branch; generic proof not replaced | 0.556 s | 1.941 s |

The primary reports `finite_field_proof_used: false`,
`special_component_fibres_closed: false`, and
`global_conjecture_resolved: false`.  The audit reports
`generic_function_field_proof_replaced: false` and
`global_conjecture_resolved: false`.  Replays created no tracked output
change.

## Validation floor

The index-complete candidate tree passes:

- Ruff and `py_compile` for both moved executables;
- `check_hygiene.py`: 1,698 Python files compile, all 800 Markdown files have
  resolving local links, all 86 ledger document hashes match, no new root
  debt exists, and all 353 retired paths and batch-provenance records pass;
- all 143 migration-tool tests;
- all 14 fourteen-vertex cycle-cover lattice tests;
- two-pass migration-rewriter fixed point; and
- clean index and working-tree diff checks.

## Three-stage program audit

Three read-only auditors reviewed exact merged baseline `8acb404` before the
move.  They found no policy weakening, classifier/manifest dumping, batch
bypass, new root debt, status erosion, or CI regression across Stages 11.5,
12, and the Stage 13 dry run.  Exact merged-main CI run `31285329687` was
green.  The scientific referee independently confirmed the split-center
weight scope, the global `UNRESOLVED` boundary, and the audit's corroborative
role.

The audit recorded two non-blocking pre-existing correctness debts for
separate follow-up:

1. `audit_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py`
   still assigns a retired root P4 verifier path, then executes only its
   `.name`.  Hygiene does not currently propagate assigned `Path` constants
   into later `.name` subprocess calls.  The full dependency replay therefore
   fails before any Stage 13 change.
2. The already-migrated
   `claims/p4/classifications/triangle-211/common-active-binary-triangle/analyze_p4_common_active_binary_triangle_local_dimension.py`
   imports a root module before calling shared bootstrap.  It is the only
   such migrated claim-package defect found by the audit's AST scan.

Neither file is a Stage 13 batch member or consumer of a moved Stage 13
executable.  They do not block this migration, but they should be repaired in
a bounded Tier-2 correctness stage before the next migration family.

The audit also preserved the Stage 12 evidence-semantics debt: four related
shared-construction audits use broader `independent`/`no-import` wording than
their actual downstream-only independence warrants.  No such wording occurs
in the genuinely no-import split-center audit moved here.

## Merge gate and stop condition

Stage 13 requires a fresh read-only adversarial review of the final branch,
exact-head CI, a fresh merge base, no unresolved consequential review, and a
normal exact-head merge.  The global conjecture remains **UNRESOLVED**.

This stage stops at the exact three-file package.  It does not extract either
shared helper, enter special-fibre or boundary work, repair the two unrelated
program-audit defects, or infer approval from classifier confidence.
