# Layout migration report — pilot (disjoint mixed-star weighted H22)

Status: **pilot complete; bulk migration not started.**  The global
Krenn–Gu conjecture remains **UNRESOLVED**.  This migration moves and
re-anchors files only; no theorem claim was added, removed, promoted,
or reworded.

## Provenance anchors

- Starting state: tag `pre-layout-migration-v1` (commit `f6d2cc4`,
  the merged stabilization pass).  The inventory and manifest are
  built from this ref via `git ls-tree`/`git show`, so every count in
  this report is measured against the true pre-migration tree.
- Pilot commits on `layout-migration-pilot`:
  - `34fc7ea` inventory, classification, manifest tooling;
  - `8421072` infrastructure (ledger move to `catalog/`, root-layout
    enforcement, shared path module);
  - `7731a54` tooling fixes (pilot layout, executor);
  - `a6b8bbb` **pure `git mv`** of the 35 pilot files;
  - `457494d` reference/path rewrites;
  - `823256b` validation, report, final hashes;
  - `fce2c3c` consolidated import/path strategy;
  - `b175a9b` true-base inventory and confidence gating;
  - `da43490` rewriter repair and the 27-test suite;
  - `65f4288` manifest-aware stale-path enforcement;
  - `8107d1a` ledger `proof_variant`/`subpackage` fields;
  - `b519f4b` review-pass report update;
  - final commit: count corrections, batch approval model,
    context-aware stale references, real hash-update tests.
- Machine-readable record: `catalog/moved-paths.json` (every move
  with old path, new path, reason, status, confidence); the ledger
  relocation itself is entry number 36, so no tracked source is
  missing from the manifest.
- The pilot's approval record:
  `catalog/batches/p5-h22-disjoint-mixed-star-pilot.json`.

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

Three distinct moments, all measured from git objects:

| Moment | Root files | Root dirs | Entries |
|---|---|---|---|
| Before migration (tag `f6d2cc4`) | 2,363 | 3 | **2,366** |
| Immediately after the 35 pure moves (`a6b8bbb`) | 2,327 | 8 | **2,335** |
| Final PR head | 2,327 | 9 | **2,336** |

The post-move count is net −31 relative to the tag: −36 root files
(35 pilot files + the ledger) and +5 top-level directories that the
migration infrastructure created (`claims/`, `catalog/`, `docs/`,
`src/`, `tools/`).  The final head adds exactly one more entry: the
`tests/` directory holding the migration test suite.  GitHub still
truncates at 1,000 entries; only the bulk evacuation fixes that.

Projected root entries after future batches (unclassified files are
not members of any move set, so every projection already leaves them
at the root):

- moved-only (today): 2,336;
- if all 369 high-confidence proposals were batched and executed:
  1,967;
- if all 2,015 classified proposals were batched and executed: 357 —
  composed of the 348 unclassified files plus retained root files and
  the fixed entry-point/directory set.

## Files moved (35 pilot + 1 ledger, all `R100` renames)

```text
catalog/theorem-ledger.json            (was THEOREM_LEDGER.json)
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

Git recorded all 35 pilot moves as `R100` (100% similarity) renames,
so history follow-through is preserved for every file.

## Links rewritten

`tools/migration/rewrite_links.py` re-anchored **117 markdown links**
and **4 fenced replay commands** across 27 file edits, zero ambiguous
targets.  Inline links, reference-style definitions, image links,
fragments, and fenced commands with arguments are all handled; the
rewriter resolves each target against the source's *written* location,
normalizes before the manifest lookup, and is idempotent (an
existence guard leaves already-correct links untouched — two
consecutive runs rewrite nothing).  Post-rewrite check: all 758
markdown files' local links resolve.  Remaining old-filename mentions
outside the manifest are non-link prose and code-fence file lists; a
scripted sweep confirms zero broken path references to any moved
basename.

## Ledger entries changed

Five entries in `catalog/theorem-ledger.json` were repointed to the
package paths and gained `claim_package` (always the package root),
`proof_variant` (`canonical`/`alternate`), `subpackage`
(`null`/`alternate`/`boundaries`), and `legacy_paths`; committed-blob
hashes recomputed (85/85 validate).  **Status, assumptions, and
provenance fields untouched** — nothing upgraded or downgraded.

## Import/path strategy

One strategy, documented in `src/krenn_gu/bootstrap.py`: every moved
script shares the same header — a self-locating `src/` insertion and
one `bootstrap(__file__)` call that returns `(REPO_ROOT, HERE)` and
installs `sys.path`.  Root discovery walks upward to a repository
MARKER file (`Containerfile`, `requirements.lock.txt`,
`catalog/theorem-ledger.json`), **not** `.git`, so it works from clean
checkouts and source archives alike.  (The pilot's first iteration
used per-script `_repo_root()` helpers; review pass 1 consolidated
them into this single module.)  `boundaries/` scripts pass
`also=[".."]` to reach the package-root verifier they import; the two
snapshot scripts importing the moved canonical verifier got the
package path appended to their existing bootstrap.  All 23 moved
scripts compile and import from a clean checkout.

## Commands that changed

Replay commands now run from the repository root:

```text
python claims/p5/h22/disjoint-mixed-star/verify_p5_h22_disjoint_mixed_star_component_generic_obstruction.py
python claims/p5/h22/disjoint-mixed-star/audit_p5_h22_disjoint_mixed_star_component_generic_obstruction.py
python claims/p5/h22/disjoint-mixed-star/alternate/verify_p5_h22_disjoint_mixed_star_component_generic_obstruction_alternate.py
python claims/p5/h22/disjoint-mixed-star/alternate/audit_p5_h22_disjoint_mixed_star_component_generic_obstruction_alternate.py
```

Ledger replay documentation and the docs' fenced commands were
rewritten to match.

## Approval model and the manifest status vocabulary

Classifier confidence is not operational approval.  Manifest statuses:

- `moved` — executed (records `executed_batch`);
- `pilot` — the executed pilot batch;
- `proposed_high_confidence` — the classifier's high-confidence
  proposals; NOT executable on their own;
- `review_required` — medium/low-confidence proposals.

`execute_moves.py` requires `--batch-id` (a committed file under
`catalog/batches/`) or `--batch-file`; there is no mode that sweeps a
status class across the repository.  Every batch file records
`approved_by`, `approved_at`, `base_sha`, and the exact member list.
Current split: 36 moved / 369 proposed_high_confidence / 1,610
review_required / 348 unclassified.

## Enforcement

`check_hygiene.py` enforces the migration durably:

- **stale paths** (executed moves only): full old paths are rejected
  in tracked `.md/.py/.yml/.yaml/.sh/.json` outside the provenance
  allowlist; the 35 root-to-package moves that kept their filename are
  enforced context-aware — markdown links in root documents, fenced
  replay commands, python subprocess/command strings, and shell/yaml
  command references — while the same basename remains valid inside
  the destination package.  Planned-but-unexecuted moves are not
  enforced (they are still correctly at their old paths);
- **root layout** (warning-only during the migration): allowlist,
  <30-entry target, forbidden `P4_*/P5_*/verify_*` root patterns;
- the migration tool suite (39 tests) runs in CI.

## Verifiers and audits replayed

| Artifact | Result |
|---|---|
| canonical audit (`audit_..._component_generic_obstruction.py`) | **passed** from the new location (86 s) |
| alternate audit (`alternate/audit_..._alternate.py`) | **passed** from the new location (168 s); `independent_of_primary_imports: true` |
| canonical verifier (`verify_..._component_generic_obstruction.py`) | **replayed clean under WSL with Singular 4.3.2, ~108 s: `verified: true`, EXIT_CODE=0** |
| alternate verifier | not replayed after the move (already replayed pre-migration, 1,327 s; content unchanged except the path bootstrap) |
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
   moved script assumed it lived at the repository root.  The first
   fix used per-script `_repo_root()` discovery; review pass 1 then
   consolidated everything into the single `src/krenn_gu/bootstrap.py`
   helper with marker-file (not `.git`) root discovery.
2. **Cross-package imports are position-sensitive.**  Moved modules
   imported by root and snapshot scripts needed `sys.path` updates in
   exactly two places (found by a repo-wide importer scan, not by
   hand-picking).
3. **A blanket revert of a failed automated patch silently rolled back
   earlier good rewrites** (intra-package markdown links).  The
   link-checker caught it; lesson recorded: validation must run after
   every commit, and reverts must be scoped by path.
4. **The rewriter was not idempotent**: re-running re-anchored
   already-correct relative links.  Fixed with an existence-based
   guard and a normalized-path manifest lookup; proved by tests and by
   two consecutive zero-rewrite runs on the real tree.
5. **Confidence was conflated with approval**: the first manifest made
   all high-confidence entries executable via `--status approved`.
   Replaced by the batch-file model above.
6. **Stale enforcement originally skipped root-to-package moves** that
   kept their filename (35 of 36 executed moves).  Now covered by
   context-aware reference scanning restricted to executed moves.
7. **Projected root counts double-counted the unclassified files.**
   Corrected; the manifest carries an explicit note that every
   projection already leaves them at the root.

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
