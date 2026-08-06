# Layout migration report — pilot (disjoint mixed-star weighted H22)

Status: **pilot complete; bulk migration not started.**  The global
Krenn–Gu conjecture remains **UNRESOLVED**.  This migration moves and
re-anchors files only; no theorem claim was added, removed, promoted,
or reworded.

## Provenance anchors

- Starting commit: `f6d2cc4` (tag `pre-layout-migration-v1`, the
  merged stabilization pass).
- Pilot commits on `layout-migration-pilot`:
  - `34fc7ea` inventory, classification, manifest tooling;
  - `8421072` infrastructure (ledger move to `catalog/`, warning-mode
    root enforcement, `src/krenn_gu/paths.py`);
  - `7731a54` tooling fixes (pilot layout, executor);
  - `a6b8bbb` **pure `git mv`** of the 35 pilot files;
  - `457494d` reference/path rewrites;
  - final commit: ledger hash refresh + this report.
- Machine-readable record: `catalog/moved-paths.json` (every move with
  old path, new path, reason, status).

## Scope of this PR

Per the migration plan, this PR contains only:

1. repository inventory and classification;
2. proposed architecture encoded in `catalog/moved-paths.json`;
3. migration tooling (`tools/migration/`);
4. root-layout enforcement in **warning-only** mode
   (`KG_LAYOUT_STRICT=1` switches it to failing);
5. the complete disjoint mixed-star H22 pilot migration;
6. this validation report.

The bulk root evacuation follows in later PRs after review.

## Root counts

| Measure | Before | After pilot |
|---|---|---|
| root-level files | 2,363 | 2,327 |
| root-level directories | 3 | 8 |
| total root entries (GitHub listing) | 2,366 | 2,335 |

GitHub still truncates at 1,000 entries; the pilot was never expected
to fix that — the bulk evacuation will.  The target remains fewer than
30 entries at the end of the full migration (manifest estimate for the
full classified set: 360 entries, i.e. the 348 unclassified files plus
fixed entries decide the remainder — those need human classification
decisions, recorded in `catalog/unclassified-files.json`).

## Files moved (35, all `R100` renames)

```text
claims/p5/h22/disjoint-mixed-star/
  P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md
  verify_p5_h22_disjoint_mixed_star_component_generic_obstruction.py
  audit_p5_h22_disjoint_mixed_star_component_generic_obstruction.py
  P5_H22_DISJOINT_MIXED_STAR_WORKING_NOTE.md
  explore_p5_h22_disjoint_mixed_star_modular.py
claims/p5/h22/disjoint-mixed-star/alternate/
  P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION_ALTERNATE.md
  verify_p5_h22_disjoint_mixed_star_component_generic_obstruction_alternate.py
  audit_p5_h22_disjoint_mixed_star_component_generic_obstruction_alternate.py
claims/p5/h22/disjoint-mixed-star/boundaries/
  9 boundary theorem docs + their verify/audit scripts
  + verify_..._slope_r1_binary_obstruction.py
  + verify_..._slope_rm1_binary_obstruction.py
  + P5_H22_DISJOINT_MIXED_STAR_CERTIFICATE_DIVISOR_FRONTIER.md
```

Git recorded all 35 as `R100` (100% similarity) renames, so history
follow-through is preserved for every file.

## Links rewritten

- `tools/migration/rewrite_links.py` re-anchored **117 markdown links**
  (72 in the first pass, 45 after a targeted rerun for intra-package
  links) and **4 fenced replay commands** across **27 file edits**,
  zero ambiguous targets.  URL fragments preserved; external URLs
  untouched; code blocks untouched except documented replay lines.
- Post-rewrite link check: **all 757 markdown files, every local link
  resolves** (checker step [3]).
- The remaining mentions of the old filenames outside
  `catalog/moved-paths.json` are non-link prose and code-fence file
  lists; a scripted sweep confirms **zero broken path references** to
  any moved basename.

## Ledger entries changed

Five entries in `catalog/theorem-ledger.json` were repointed:

| Entry | Change |
|---|---|
| Generic weighted H22 fibre empty: disjoint mixed star | document/verifier/audit → package paths |
| Eighth-component weighted H22 closure — canonical | same, plus `claim_package`, `legacy_paths` |
| Eighth-component weighted H22 closure — alternate | same |
| Eighth-component boundary closures (atlas entry) | atlas doc unchanged; atlas scripts moved (no ledger script refs) |
| Eighth-component torus quotient | document → boundaries path |

All entries gained `claim_package` and `legacy_paths` where moved;
committed-blob hashes recomputed (85/85 validate); **status,
assumptions, and provenance fields untouched** — no status upgraded or
downgraded.

## Imports that required refactoring

- The 23 moved Python scripts replaced
  `ROOT = Path(__file__).resolve().parent` with an explicit `HERE` +
  discovered `REPO_ROOT` (the repo's established find-root pattern).
  Sibling package docs resolve via `HERE`; root-level dependencies
  (the P4 component doc, `tmp/`) via `REPO_ROOT`; root-module imports
  get `REPO_ROOT` on `sys.path`; `boundaries/` scripts additionally
  expose the package root for the canonical verifier they import.
- Two snapshot scripts
  (`research_snapshots/2026-08-04-p5-h22-slope-divisor-closures/scripts/verify_p5_h22_disjoint_mixed_star_slope_divisor_symbolic_fitting.py`
  and `..._special_slope_reduced_fitting.py`) import the moved
  canonical verifier; both got the package path appended to their
  existing `sys.path` bootstrap.
- No new `sys.path` hacks were invented: the pattern is the same one
  already used by the obligation-ledger scripts and four root
  verifiers.
- All 23 moved scripts compile **and import** from a clean checkout
  (subprocess-tested).

## Commands that changed

Replay commands now run from the repository root:

```text
python claims/p5/h22/disjoint-mixed-star/verify_p5_h22_disjoint_mixed_star_component_generic_obstruction.py
python claims/p5/h22/disjoint-mixed-star/audit_p5_h22_disjoint_mixed_star_component_generic_obstruction.py
python claims/p5/h22/disjoint-mixed-star/alternate/verify_p5_h22_disjoint_mixed_star_component_generic_obstruction_alternate.py
python claims/p5/h22/disjoint-mixed-star/alternate/audit_p5_h22_disjoint_mixed_star_component_generic_obstruction_alternate.py
```

The ledger's replay-command documentation and the docs' fenced
commands were rewritten to match.

## Verifiers and audits replayed

| Artifact | Result |
|---|---|
| canonical audit (`audit_..._component_generic_obstruction.py`) | **passed** from the new location (86 s) |
| alternate audit (`alternate/audit_..._alternate.py`) | **passed** from the new location (168 s); `independent_of_primary_imports: true` |
| canonical verifier (`verify_..._component_generic_obstruction.py`) | **replayed clean under WSL with Singular 4.3.2, ~108 s: `verified: true`, EXIT_CODE=0** |
| alternate verifier | not replayed this session (already replayed pre-migration, 1,327 s; script content unchanged except path bootstrap — hash in the ledger) |
| boundary verifiers/audits | not replayed (hours of Singular each); all import-tested |
| the two snapshot scripts importing the canonical verifier | import-tested only |

## Tests not replayed (candid)

- The SAT/DRAT finite-certificate chains (kissat/glucose/drat-trim not
  installed here); unchanged by this migration.
- All boundary verifiers (Singular-heavy); only compiled and
  import-tested.
- The alternate verifier end-to-end (content-identical to its
  pre-migration replay except the path bootstrap; the committed-blob
  hash is in the ledger).

## Structural problems the pilot exposed (and the fixes)

1. **`ROOT = parent` constants break on any depth change.**  Every
   moved script assumed it lived at the repository root.  Fixed with
   the established `_repo_root()` discovery pattern; future package
   moves get the same treatment via tooling.
2. **Cross-package imports are position-sensitive.**  Moved modules
   imported by root and snapshot scripts needed `sys.path` updates in
   exactly two places (found by a repo-wide importer scan, not by
   hand-picking).
3. **A blanket revert of a failed automated patch silently rolled back
   earlier good rewrites** (intra-package markdown links).  The
   link-checker caught it; lesson recorded: validation must run after
   every commit, and reverts must be scoped by path.

## Unclassified files

**348** root files remain unclassified (`catalog/unclassified-files.json`).
The largest groups: 276 orphan `verify_*` scripts whose documents are
not at the root or not named by the exact-stem pairing rule, 164
`audit_*` siblings of those, and 54 prose documents from the P6/P7
transfer track with no family prefix.  Each needs an explicit human
decision before the bulk evacuation; none was guessed.

## Explicit statement

No theorem claim changed.  The global conjecture remains UNRESOLVED.
Candidate, withdrawn, exploratory, and superseded entries keep their
labels; the alternate proof remains an independent alternate, not a
replacement.
## Review pass 1 fixes (machinery hardening)

The pilot was accepted; the review required the reusable machinery to be
trustworthy at repository scale before the bulk migration.  All seven
items were addressed; the 35-file pilot itself was not redone.

### 1. Replay claim corrected

The summary wording no longer says "all replayed".  Accurate statement:
**35 files moved; the canonical verifier and both independent audits
were replayed from the new locations; the alternate verifier and all
boundary verifiers/audits were compile- and import-tested only.**

### 2. True pre-migration base

`inventory_layout.py` gained `--ref` and now inspects any git ref via
git objects (`ls-tree`/`show`), reading content at that ref and
resolving links textually against the tracked set.  The inventory and
manifest were regenerated from `pre-layout-migration-v1` (`f6d2cc4`),
so the starting commit, the 2,363 root files / 2,366 entries counts,
and every downstream figure agree across the inventory, manifest, PR
body, and this report.  The `THEOREM_LEDGER.json ->
catalog/theorem-ledger.json` relocation is a first-class manifest
entry, so every move appears in the manifest.

### 3. Confidence-gated executable batches

Manifest statuses are now `moved` / `pilot` / `approved` /
`review_required`.  Only high-confidence classifications auto-approve;
medium/low stay `review_required` proposals.  `execute_moves.py`
refuses `review_required`.  Current split: 36 moved, 369 approved,
1,610 review_required, 348 unclassified.  Projected root counts are
reported per gate: approved-only 1,967, review-also-approved 357,
with-unclassified 705.

### 4. Final-destination validation and rollback

`build_manifest.py` computes the FINAL destination (base proposal, then
pilot-layout transformation, then normalization) and validates
uniqueness, double-moves, and source/destination overlap cycles on that
final value (`validate_records`, also unit-tested).  `execute_moves.py`
independently re-verifies unique sources/destinations, overlap cycles,
parent-path validity, and manifest health; it executes in deterministic
order and, on ANY failure, rolls back the moves performed in that
invocation in reverse order and writes `catalog/recovery-<ts>.json`
without touching the manifest.

### 5. Rewriter repair + test suite in CI

The rewriter's manifest lookup and relative-path calculation now use the
NORMALIZED resolved path, and an existence-based guard makes it
idempotent (two consecutive runs rewrite 0 links).  Reference-style
definitions, image links, and fenced replay commands with arguments are
handled; duplicate replay basenames are reported and skipped.
`tests/test_migration_tools.py` (27 tests) covers the full review
checklist and runs as a dedicated CI step against a synthetic post-move
fixture tree.

### 6. Manifest-aware stale-path enforcement

`check_hygiene.py` rejects moved old paths in tracked
`.md/.py/.yml/.yaml/.sh/.json` files, except in the provenance allowlist
(catalog migration files, audit reports, migration report/inventory,
`tools/migration/`, migration tests).  JSON hits are checked
structurally so `legacy_paths` fields are exempt.  Root-file moves that
keep their filename are ambiguous and not enforced; sub-path moves and
renamed-away root files are.

### 7. Consolidated import/path strategy

The duplicated `_repo_root()`/`sys.path.insert()` blocks were replaced
by one helper, `src/krenn_gu/bootstrap.py`.  `find_repo_root()` walks
upward to a repository MARKER file (`Containerfile`,
`requirements.lock.txt`, `catalog/theorem-ledger.json`) — not `.git` —
so it works in clean checkouts and source archives.  Every moved script
shares the identical header; `claim_package` is the package root and
`alternate`/`boundaries` are recorded via `proof_variant`/`subpackage`
fields.
