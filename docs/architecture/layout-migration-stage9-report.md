# Layout migration report — Stage 9 (P5 component-level generic H31/H22 obstruction spine)

Status: **the first large-scale P5 generic-obstruction migration is
complete.**  Twenty-eight component-level generic packages (86 files)
moved from the repository root into `claims/p5/h31/<family>/` and
`claims/p5/h22/<family>/`.  Every migrated package is a ledger
`verified_generic` generic/function-field theorem with its claim
document, primary verifier, and independent audit moved as one unit.

> No theorem claim, assumption, scope, proof status, provenance
> status, or global-resolution status changed as a result of this
> migration.  Generic theorems remain generic; excluded divisors
> remain excluded.  The global Krenn–Gu conjecture remains
> UNRESOLVED.

## Provenance anchors

- Starting merged `main` SHA: `4ee0cdc` (PR #37, Stage 8.5 merge).
  Stage 8.5 verified present before any Stage 9 work (AGENTS.md,
  proof-obligation architecture, formalization interface, migration
  runbook, agent-operations pass, Stage 8 report and batch).
- Baseline root entries: **2,134** = Stage 8 final 2,133 + `AGENTS.md`
  added at root by Stage 8.5 (measured as the only root-level addition
  between `3404991` and `4ee0cdc`).
- Branch: `layout-migration-stage9-p5-generic-obstructions`.
- Commits: A `cd9a37c` (dry-run + zero-refinement classifier pass),
  B `d0527b8` (frozen batch), C `2b15668` (pure git-mv),
  D `7c13b15` (mechanical repairs), E (navigation, ledger hashes, this
  report).
- Batch: `p5-generic-obstructions-stage9`, artifact
  `catalog/batches/p5-generic-obstructions-stage9.json`:
  - approved_by: "YesterdaysLemon (repository owner), Stage 9 P5
    component-level generic H31/H22 obstruction migration
    instruction";
  - approved_at: 2026-08-07;
  - base_sha: `cd9a37c` (Stage 9 commit A);
  - mandatory mapping_sha256:
    `68d20c08b987c2465395ec485647dc37c958d8400a8d05dede37559256a47f23`;
  - member_count: **86**.
- Pure-move commit: `2b15668`; R100 count **86 / 86** (measured
  against the direct parent; the only non-rename change in that commit
  is the manifest status flip).

## What moved

28 packages: 15 H31 + 13 H22 (46 + 40 files).  Pairing by underlying
P4 family — 12 symmetric pairs plus 4 recorded asymmetries:

| shape | families |
|---|---|
| H31+H22 pair | all-rank-one-triangle, coincident-support, common-singleton, directed-zero-divisor-triangle-components, disjoint-secant, eisenstein-norm, equal-support-common-factor, full-support-tangent, mixed-orientation, six-dimensional, transverse-common-factor, two-rank-two-spoke-mixed-star |
| H31 only | coincident-support-rank-one-star, common-kernel-vertical-triangle (no live H22 counterpart exists), disjoint-mixed-star (H22 side is the pilot package) |
| H22 only | diagonal-quadric (H31 elliptic side inseparable from its boundary forest; deferred) |

Supporting-file asymmetries preserved: the all-rank-one-triangle
modular **exploration** script moved with its package (classified
exploration, not theorem evidence), and the superseded
diagonal-quadric working note moved with its owning generic package
(same precedent as the pilot's working note).

## Classifier refinement

**Zero records required refinement.**  All 86 members' classifier
destinations already matched human ownership review
(record-for-record: manifest `new_path` == classification
`proposed_path`); `build_manifest.py` regeneration was proven
byte-identical before Commit A.  Source-family/status arithmetic
(measured): 84 `proposed_high_confidence` + 2 `review_required`
members; no confidence promotion, no status change.  This is the
second stage (after Stage 8) where the flat classifier's package
bucketing agreed fully with human review.

## Root-count accounting (observed)

| Moment | Root entries |
|---|---|
| Stage 8 final (`3404991`) | 2,133 |
| Stage 8.5 merge / Stage 9 start (`4ee0cdc`) | 2,134 (+AGENTS.md) |
| after pure Stage 9 moves (`2b15668`) | 2,048 |
| final PR head | 2,048 |

Manifest tallies (observed, executor-produced):

```text
stage9_files_moved                    86
stage9_root_entries_removed           86
cumulative_moved_entries              325   (239 + 86)
stale_paths_enforced (after)          325   (239 + 86)
remaining_proposed_high_confidence    277   (361 - 84)
remaining_review_required             1413  (1415 - 2)
remaining_unclassified                348   (unchanged)
```

## Dependency topology and repair surface

Moved-script conventions (mechanical, Stage 3/4 canonical pattern):

- 35 moved scripts converted to
  `REPO_ROOT, HERE = bootstrap(__file__)` with `ROOT = REPO_ROOT`
  aliasing so pre-move repo-root path constants keep their meaning;
  same-package theorem/script constants re-pointed to `HERE`.
- Two pre-bootstrapped verifiers (disjoint-mixed-star H31,
  two-rank-two-spoke H31) had `expose_claim_package` passed the
  script's own directory — wrong once the script left root; rewired
  to `REPO_ROOT`.
- Intra-batch sibling imports (disjoint-secant ↔ full-support-tangent,
  disjoint-secant audit → directed-zero-divisor audit) resolved via
  `expose_claim_package`.
- Shared root utilities (`verify_p5_h31_marked_basis_open_branch`,
  `p5_high_coordinate_tree_chart_cegar`,
  `verify_p4_directed_zero_divisor_triangle_components`) stayed at
  root; already-migrated P4 anchors referenced by link/exposure only.

Staying consumers repaired (all verified import-clean and sampled
green in execution):

- 4 root H22 consumers importing moved mixed-orientation
  (first-rank-two + one-three-components verify/audit);
- 10 pilot disjoint-mixed-star package scripts importing the moved
  H31 sibling (audits, boundary audits, explore, one boundary
  verifier);
- 4 `research_snapshots/2026-08-04-p5-delta3-obligation-ledger`
  scripts importing the moved all-rank-one-triangle H31 verifier;
- 13 staying scripts whose string constants named moved files
  (frontier verifier, common-singleton P4 component verifier, 8
  candidate derivations, dense-marking verifier, common-active-binary
  infinity-endpoint verifier, tenth-component snapshot script).

Pre-existing debt found and handled honestly: the frontier verifier
`verify_p5_high_coordinate_partial_frontier.py` carried two stale
constants **from the Stage 3/pilot moves**
(`P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`,
`P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`); both
repointed in the same mechanical pass.  A repo-wide scan found further
stale constants in staying root scripts referencing files moved in
Stages 3–7 (e.g. diagonal-quadric and six-dimensional consumers, the
equal-support-sixfold verifiers); those are pre-existing and out of
Stage 9 scope — recorded here and in the friction audit for a future
repair pass.

## Link and command rewrites

- Rewriter pass 1 (post pure move): 133 links + 74 replay commands
  across 46 files, 28 ledger entries re-pointed, 0 ambiguities.
- Pass 2 (post Python repairs): 53 links + 58 replay commands across
  34 files, 0 ambiguities.
- Pass 3: **fixed point — 0 links, 0 commands, 0 touched files,
  0 ambiguities**.
- No theorem prose changed: diffs contain only link targets, fenced
  command paths, path constants, and import/repair blocks.

## Replay results (role-separated accounting)

Mandatory set = every practical moved **live primary verifier** (28)
and every **independent audit** (28).  Exploration scripts are
optional smoke tests and are accounted separately.  Support/dependency
correctness was established through the owning verifiers/audits plus a
faithful script-dir-only import probe of all 57 moved scripts and 18
repaired consumers (75/75 clean).

| class | pre-move (preflight) | post-move |
|---|---|---|
| primary verifiers | 28/28 rc=0 (0.5–303.2 s) | 28/28 rc=0 (0.5–315.9 s) |
| independent audits | 28/28 rc=0 (0.1–239.8 s) | 28/28 rc=0 (0.1–241.7 s) |
| exploration smoke (optional) | 1/1 rc=0 (7.3 s) | 1/1 rc=0 (7.4 s) |

Environment: native Windows Python 3.13.14, sympy 1.14.0.  Singular is
not on the Windows PATH; Singular 4.3.2 was used through WSL for the
two direct-`["Singular"]` coincident-support verifiers (299 s / 45 s),
the established Stage 3 manual-replay convention.  The other
Singular-touching scripts are self-wsl-aware and ran from Windows.
No verifier or audit was claimed without execution; the 56 mandatory
verifier/audit replays wrote only to gitignored `tmp/` or stdout.
One optional downstream smoke test was an exception: it wrote a tracked
snapshot JSON and later required restoration (see Post-review
corrections).

Downstream sampling (post-move, executed): three pilot
disjoint-mixed-star boundary audits (rc=0, census outputs intact),
the frontier verifier (rc=0 after the Stage 9 constant repoints), and
obligation-ledger snapshot scripts.  One snapshot script
(`retry_frame_q2_extraction.py`) exited rc=0 but recorded
`timeout_null` — an inconclusive result that its caller wrongly logged
as green; the tracked JSON it overwrote was restored (see Post-review
corrections).

## Preflight finding deferred a family

**equal-support-sixfold (both sides) was deferred.**  Its two generic
docs are ledger `verified_generic`, but both verifiers fail pre-move
with `FileNotFoundError` on
`P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md` — a stale root-path
constant left behind by the Stage 3 component move (the verifier still
walks parents looking for the file at root).  Diagnosis: pre-existing
breakage, non-environmental.  Per the selection rule, a live package
that cannot replay cleanly for a non-environmental reason is deferred;
migration does not repair it.  Neither package nor its audit-less
state (ledger `independent_audit: null`) was touched.

## Ledger

- **28 entries re-pointed** mechanically by the rewriter (document,
  primary_verifier, independent_audit paths + `claim_package` +
  `legacy_paths` for every moved generic theorem).
- **35 committed-blob hashes refreshed** mechanically for documents
  whose content changed during reference rewrites (28 moved theorem
  docs, README.md, the frontier doc, four obligation-ledger snapshot
  scripts, and others).  All 85 ledger hashes validate; every
  `status` field is byte-identical to pre-migration; `global_status`
  remains **UNRESOLVED**.
- No entries added: the ledger remains curated and partial; no generic
  entry was transformed into a pointwise one.

## Navigation

Created `claims/p5/README.md`, `claims/p5/h31/README.md`, and
`claims/p5/h22/README.md`.  They state explicitly that Stage 9
migrated **component-level generic** packages, pair H31/H22 siblings
by underlying P4 family, record the four asymmetries, and distinguish
the migrated generic layer from the pointwise boundary/divisor
closures that remain elsewhere.  No exhaustiveness is implied.

## Machinery behavior

Stage 9 required **no migration-machinery change** — executor,
batch contract, rewriter, and replay-command grammar all handled the
larger batch without modification (the preferred outcome for a
ramp-up stage).  All Python repairs used the shared
`bootstrap`/`expose_claim_package` helpers; no per-importer shims and
no package-specific path hacks were added.

## CI bookkeeping

Per the established convention: the substantive-head `workflow_dispatch`
run ID and the exact substantive-head SHA are recorded here, and the
final PR-triggered workflow must pass hygiene, migration tests,
14-vertex tests, and the rewriter fixed-point check on the resulting
PR head.

- Substantive head dispatch
  [31239784636](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31239784636)
  passed (**success**) on the exact substantive head
  `3f88a68e85b950c3d6ed58bdf659bc479a5f0fca`.  No migration machinery,
  theorem claim, or batch mapping changed as a result.

## Validation floor

On the final head: `check_hygiene.py` all green (ledger 85/85 hashes,
provenance 325/325, stale paths 325 enforced, markdown links resolve,
5 fast verifiers pass, candidate-index completeness precondition
green); `tests.test_migration_tools` 117 tests OK;
`test_fourteen_vertex_cycle_cover_lattice.py` 14 tests OK; rewriter
idempotent (second pass 0/0/0/0).  Root: 2,134 → 2,048.

## Post-review corrections

Independent review found two integrity defects after the first
bookkeeping head.  Both were narrow migration/process errors, not
mathematics.  Corrected in a single post-review correction commit;
the pure-move history was not rewritten.

### Defect 1: accidental tracked scientific-output mutation

Downstream sampling executed
`research_snapshots/2026-08-04-p5-delta3-obligation-ledger/scripts/retry_frame_q2_extraction.py`
as a smoke test.  That script writes its tracked ledger JSON even when
its computation is inconclusive and exits rc=0 after recording
`timeout_null`.  The replay therefore overwrote the committed
successful result (`strategy_a_slimgb`, 0.6 s, generator
`p^2*q^3-p^2*q+p*q^2+p*q`, factors `1, p, q, q+1, p*q-p+1`) with a
`timeout_null` record.

- The execution was reported as rc=0 "green"; that was wrong —
  `timeout_null` is inconclusive and rc=0 is not a semantic success
  criterion for output-writing exploration/support scripts.
- The JSON was restored byte-for-byte to the Stage 9 base blob
  `8ef250728c039de5ad0470d32de45f2346caffdd` (verified by blob-hash
  comparison against `4ee0cdc`).
- The earlier statement that generated solver outputs went only to
  gitignored `tmp/` or stdout was **incorrect**: it held for all 56
  mandatory verifier/audit replays, but not for this optional snapshot
  smoke test.
- A full `git diff 4ee0cdc..HEAD` scan confirmed no other tracked
  result/certificate/snapshot artifact was mutated as a replay side
  effect; the JSON above was the sole computational-output change in
  the whole Stage 9 diff.

### Defect 2: silent stale provenance dependency (fail-open)

`claims/p5/h22/all-rank-one-triangle/verify_p5_h22_all_rank_one_triangle_component_generic_obstruction.py`
still defined `H31_THEOREM` at the repository root after Stage 9 moved
the file, and its dependency inventory is guarded by `if path.exists()`
— the stale path therefore silently dropped the H31 dependency while
the verifier returned rc=0.  The earlier import probe could not catch
this because fail-open `.exists()` paths are never exercised at import
time.

- Repaired mechanically to
  `claims/p5/h31/all-rank-one-triangle/P5_H31_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`;
  theorem logic untouched.
- Replayed post-repair: rc=0, `verified: true`, and the dependency map
  again contains
  `P5_H31_ALL_RANK_ONE_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`
  hashed from its new location.
- The same systematic scan found one more Stage-9-broken executable
  dependency: `claims/p4/components/disjoint-mixed-star/verify_p4_disjoint_mixed_star_pure_component.py`
  hashes the same moved H31 theorem in an **unguarded** dependency map
  (would crash loudly); repointed and replayed green with the
  dependency present.
- All other 78 basename occurrences were classified: same-package
  `HERE /` references, already-repointed `claims/...` constants,
  docstring prose, and two legitimate JSON status fields naming the
  companion theorem by display name.  No other executable root-relative
  reference to a Stage-9-moved path remains.
- Other successful verifier/audit replays were preserved, not rerun
  (no other executable was materially affected).

### Process lessons recorded

Both defects exposed stable migration rules, now added to the
migration runbook (section 8, "Replay and repository-state hygiene"
and "Stale optional-dependency audit"): replay must not silently dirty
tracked state; check `git status` after replay tiers; output-writing
snapshot scripts need a sandbox or explicit intent; rc=0 is not
semantic success for scripts that encode inconclusive results; and
moved-path scans must cover fail-open `.exists()` provenance
constants, which an import probe cannot catch.

### First corrected substantive head

Because executable code changed, the correction commit is a new
substantive head with its own `workflow_dispatch`; the final
PR-triggered CI must pass on the exact final head (recorded below).

- Corrected substantive head dispatch
  [31240609202](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31240609202)
  passed (**success**) on the exact corrected substantive head
  `bffa91832e6fa5cddb1555c61b5e278b90904d18`.  No migration machinery,
  theorem claim, or batch mapping changed as a result.

### Final independent merge-gate correction

The final independent merge-gate review compared every Python
docstring changed between the Stage 9 base and the candidate head.  It
found one further mechanical-repair defect:

- Commit D had inserted an eleven-line bootstrap block *inside* the
  module docstring of
  `claims/p5/h31/coincident-support/audit_p5_h31_coincident_support_component_generic_obstruction.py`.
  The text was inert at runtime, so import and replay probes could not
  detect it, but it corrupted the independent audit's explanatory
  prose.  The injected text was removed, restoring that docstring to
  the Stage 9 base text; no executable or mathematical logic changed.
- The same review corrected a transposed dry-run inventory split:
  the frozen batch contains 46 H31 files and 40 H22 files, not 44 and
  42.  The total (86), package counts (15 and 13), mapping, and catalog
  arithmetic were already correct.

The affected independent audit was replayed after the correction.  A
new authoritative validation floor and exact-head PR CI are required;
their run identifiers belong in PR #38 metadata rather than another
report-only bookkeeping commit.


## Fresh-agent documentation audit

This stage was executed by a fresh agent from the Stage 9 prompt plus
the committed repository only.  Friction log (schema fields
condensed):

1. **"Every executable member" vs "every practical live
   verifier/audit".**  The runbook's "replay every practical moved
   verifier and independent audit" does not say that a `.py` batch
   member is not automatically a theorem replay obligation.  First
   preflight attempt launched a blanket serial replay of all scripts;
   the owner required an explicit role inventory with ledger-derived
   runtime guidance and conservative Singular scheduling.
   Classification: **C** (stable migration rule, weakly missing).
   No permanent-doc change made: the runbook's wording is
   role-specific and the gap is in interpretation, not in a missing
   correctness rule; recorded as a recommendation instead.
2. **Singular invocation conventions are undocumented.**  Four
   conventions coexist in this layer (shared helper, self-contained
   WSL tuple, direct `["Singular"]`, none).  The ledger records
   `external_binaries: ['Singular >= 4.3']` but not the convention,
   so replayability required per-script inspection.  Classification:
   **E** (mutable script-specific state) — belongs in stage reports,
   not permanent docs.
3. **Ledger `verified_generic` did not imply a currently runnable
   verifier.**  equal-support-sixfold was broken since Stage 3 and
   nothing flagged it.  Discovered only by mandatory preflight —
   exactly the failure mode preflight exists to catch.
   Classification: **E** (mutable state).
4. **Stale path constants from earlier stages.**  The frontier
   verifier and several root consumers carried Stage 3–7 stale
   constants; Stage 9 repaired only its own breakage plus the two
   frontier constants it re-touched.  Classification: **C** (a stable
   rule would be: "when a batch moves a file, repair every staying
   script constant that names it").  The runbook's mechanical-repair
   list already covers "path constants"; the gap is that prior stages
   missed some.  No permanent-doc change; recorded as a
   recommendation.
5. Root arithmetic across documentation stages (Stage 8.5 added
   `AGENTS.md` at root): answered directly from Git history.
   Classification: **A** (docs adequate; measured from the
   authoritative source).

**Could Stage 9 be executed safely from the Stage 9 prompt plus the
committed repository alone?  Yes.**  Every operational question —
approval model, artifact authority, batch contract, executor usage,
rewriter conventions, replay expectations, ledger semantics, stop
conditions — was answered by AGENTS.md, the runbook, and the current
catalogs without asking the owner.  The only owner interactions were
the Stage 9 instruction itself and two process corrections (replay
role accounting), which are refinements to execution style rather
than missing institutional knowledge.  Scientific judgments (which
families are separable, which are entangled) were made from the
documents' own status sections and import graphs, exactly as the
runbook prescribes.

**Did Stage 8.5 documentation reduce historical reconstruction?
Yes.**  Prior stages' reports were consulted only for the replay
convention precedent (Stage 3 WSL Singular) and the consumer-repair
pattern (Stages 6/7); no old report was needed to understand any
current invariant.

**Permanent documentation changes.**  The initial friction audit made
no permanent edits (no friction item met all four threshold criteria).
However, the post-review corrections exposed two genuinely stable
migration rules — replay repository-state hygiene and fail-open
optional-dependency auditing — that were added to the migration
runbook (section 8).  These are permanent policy, not Stage 9 state.

## Selected / excluded / deferred

- **Selected:** 28 live generic packages (86 files), listed above.
- **Deferred (inspected, eligible later):** one-three,
  split-center-mixed-star, first-rank-two, common-center-kernel-star,
  embedded-p3, common-active-binary-triangle,
  unequal-complement-common-kernel, unequal-endpoint-inward-star,
  diagonal-quadric-elliptic (H31 forest), equal-support-sixfold
  (after its path-constant breakage is repaired as a separate
  non-migration work item).
- **Excluded:** all `*_CANDIDATE*` / `*_PARTIAL*` / verification-only
  prose, component19/21/23 divisor trees, the elliptic-end and
  marked-fibre chart families, P5 frontier documents, Q4_211/Q5_*
  programmes, legacy, P6/P7.
- **Already migrated elsewhere:** pilot `claims/p5/h22/disjoint-mixed-star/`
  and the Stages 3–8 P4 spines.

## Stop condition

This PR does not begin P5 divisor recursion, exceptional fibres,
pointwise closure, common-center-kernel-star or
common-active-binary-triangle migration, remaining P4 cleanup, legacy
evacuation, proof-DAG schema design, or any new mathematics.  Stage 9
proves the migration system can move a broad horizontal P5 layer —
86 files across 28 packages — while keeping generic scope honest and
every verifier/audit reproducible.

> No theorem claim, assumption, scope, proof status, provenance
> status, or global-resolution status changed as a result of this
> migration.  The global Krenn–Gu conjecture remains UNRESOLVED.
