# Stage 3 dry-run: P4 component packages

Generated before execution, from the tree at `stage3-start`
(`295a875`, merged main including PR #30).

Approval artifact: `catalog/batches/p4-components-stage3.json`
(produced with this report in Commit A).

## Packages (3) and exact moves (9)

### Package 1 — disjoint-mixed-star

| old path | new path |
|---|---|
| P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md | claims/p4/components/disjoint-mixed-star/P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md |
| verify_p4_disjoint_mixed_star_pure_component.py | claims/p4/components/disjoint-mixed-star/verify_p4_disjoint_mixed_star_pure_component.py |
| audit_p4_disjoint_mixed_star_pure_component.py | claims/p4/components/disjoint-mixed-star/audit_p4_disjoint_mixed_star_pure_component.py |

### Package 2 — split-pair

| old path | new path |
|---|---|
| P4_SPLIT_PAIR_PURE_COMPONENT.md | claims/p4/components/split-pair/P4_SPLIT_PAIR_PURE_COMPONENT.md |
| verify_p4_split_pair_pure_component.py | claims/p4/components/split-pair/verify_p4_split_pair_pure_component.py |
| audit_p4_split_pair_pure_component.py | claims/p4/components/split-pair/audit_p4_split_pair_pure_component.py |

### Package 3 — equal-support-sixfold

| old path | new path |
|---|---|
| P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md | claims/p4/components/equal-support-sixfold/P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md |
| verify_p4_equal_support_sixfold_pure_component.py | claims/p4/components/equal-support-sixfold/verify_p4_equal_support_sixfold_pure_component.py |
| audit_p4_equal_support_sixfold_pure_component.py | claims/p4/components/equal-support-sixfold/audit_p4_equal_support_sixfold_pure_component.py |

## Per-file reference profile

| file | classification | inbound md | python importers | replay refs | outbound refs to staying files |
|---|---|---|---|---|---|
| P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md | owned_by_package | 13 | 0 | 0 | — |
| verify_p4_disjoint_mixed_star_pure_component.py | owned_by_package | 0 | 6 | 0 | 4 docs + 1 module |
| audit_p4_disjoint_mixed_star_pure_component.py | owned_by_package | 0 | 0 | 0 | 0 |
| P4_SPLIT_PAIR_PURE_COMPONENT.md | owned_by_package | 3 | 0 | 0 | — |
| verify_p4_split_pair_pure_component.py | owned_by_package | 0 | 0 | 0 | 0 |
| audit_p4_split_pair_pure_component.py | owned_by_package | 0 | 0 | 0 | 0 |
| P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md | owned_by_package | 4 | 0 | 0 | — |
| verify_p4_equal_support_sixfold_pure_component.py | owned_by_package | 0 | 0 | 0 | 0 |
| audit_p4_equal_support_sixfold_pure_component.py | owned_by_package | 0 | 0 | 0 | 0 |

### Inbound markdown links (to theorem docs)

- disjoint-mixed-star (13): P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md,
  P4_DISJOINT_MIXED_STAR_AFFINE_CLASSIFICATION.md,
  P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md,
  P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md,
  P4_SIX_DIMENSIONAL_PURE_COMPONENT.md, P5_ALTERNATIVE_STRATEGY_MAP.md,
  P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md,
  P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md,
  P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md, README.md, and the three
  already-migrated H22 package docs (canonical theorem, working note,
  alternate theorem).
- split-pair (3): P4_INOUT_PATH_STRATUM_WORKING_NOTE.md,
  P4_SINGLE_WORD_QUADRILATERAL_PURE_COMPONENT.md, README.md.
- equal-support-sixfold (4): P4_INOUT_PATH_STRATUM_WORKING_NOTE.md,
  P5_H22_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md,
  P5_H31_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md,
  README.md.

### Python importers (of the disjoint-mixed-star verifier; the only
imported moved module)

- claims/p5/h22/disjoint-mixed-star/verify_..._component_generic_obstruction.py
- claims/p5/h22/disjoint-mixed-star/boundaries/verify_..._af_aphi_...py
- claims/p5/h22/disjoint-mixed-star/boundaries/verify_..._coupled_slope_...py
- claims/p5/h22/disjoint-mixed-star/boundaries/verify_..._torus_quotient.py
- verify_p4_all_rank_one_triangle_pure_component.py
- verify_p5_h31_disjoint_mixed_star_component_generic_obstruction.py

The four already-migrated H22 scripts (the canonical H22 verifier and
the three boundary scripts above) import via the centralized bootstrap
(repo root on sys.path), which keeps resolving after the P4 move.  The
two root scripts (`verify_p4_all_rank_one_triangle_pure_component.py`,
`verify_p5_h31_disjoint_mixed_star_component_generic_obstruction.py`)
import bare module names; they are repaired in Commit C.

Repair mechanism (accurate): because the imported P4 module itself
moved out of the repo root, each importer inserts an explicit
repo-relative `sys.path` entry pointing at the moved package directory
(`claims/p4/components/disjoint-mixed-star`) before the bare-name
import, and repoints the component-doc / primary-script constants to
the package path.  This is a per-importer shim, not the centralized
bootstrap helper itself (which discovers the repo root but does not
know package directories).  Avoiding proliferation of these shims is
Stage 4 debt: if a clean single mechanism emerges (e.g. a package
registry in the bootstrap), the shims should be consolidated then.

### Outbound refs from the disjoint-mixed-star verifier to files that
stay in place

- `P4_MIXED_ORIENTATION_PURE_COMPONENT.md` (doc)
- `P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md` (doc)
- `P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md` (doc)
- `P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md` (doc)
- `verify_p4_mixed_orientation_pure_component` (module import)

Repaired in Commit C: the moved verifier switches to the centralized
bootstrap, uses `HERE` for its own package files and `REPO_ROOT` for
the root-resident files above (which stay in place).

## Shared dependencies deliberately left in place

- `verify_p4_mixed_orientation_pure_component.py` — imported by the
  disjoint-mixed-star verifier AND by the deferred
  all-rank-one-triangle verifier; shared, stays at root (it does not
  independently belong to either package).
- The four root docs referenced by the disjoint-mixed-star verifier
  (above) — global P4/P5 material, not owned by this batch.

## Ambiguous files deliberately excluded

- **P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT** package (doc + verifier +
  audit): its verifier imports the disjoint-mixed-star verifier (a
  moving package) AND is itself imported by two P5 H31/H22 verifiers
  at the root.  That cross-package Python dependency is ambiguous
  enough under the Stage 3 constraints to defer to Stage 4, where it
  can be handled together with its importers.  Excluded from this
  batch; recorded here.

## Ledger references

No theorem-ledger entry currently references any of the three theorem
docs (the ledger is a curated partial index; the P4 component packages
were not yet mapped).  `update_ledger` will therefore repoint 0 ledger
entries for this batch; the moved files' provenance lives in the
manifest's `executed_batch` record.

## Collision and cycle status

- destination collisions: **none**;
- source/destination overlap cycles: **none** (no moved file is the
  destination of another move).

## Batch summary

- member count: **9**;
- package count: **3**;
- files moved: 9 (3 docs, 3 verifiers, 3 audits);
- expected root count after the move: 2,328 − 9 = **2,319**;
- stale-enforcement count expected after: 44 + 9 = **53**.

## Cross-package acceptance note

The disjoint-mixed-star package is imported by the already-migrated
`claims/p5/h22/disjoint-mixed-star/` package.  Stage 3 therefore
exercises the supported case: an already-migrated source whose target
moves in a later stage.  The rewriter's second pass must report
0/0/0.
