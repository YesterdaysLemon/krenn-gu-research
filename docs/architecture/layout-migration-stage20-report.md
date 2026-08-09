# Layout migration Stage 20 report

Status: **SUBSTANTIVE MIGRATION COMPLETE ON BRANCH; AWAITING FINAL
EXACT-CANDIDATE REVIEW AND MERGE.**

The global Krenn-Gu conjecture remains **UNRESOLVED**.  Stage 20 changes
filesystem ownership, replay paths, navigation, and mechanically derived
hash metadata only.  It does not promote a claim, extend the toric-boundary
theorem to the projective interior or another component, close weighted
`H22`, prove component exhaustiveness or `P5 -> Delta3`, or turn modular
corroboration into the characteristic-zero proof.

## Exact reviewed transaction

- Merged baseline:
  `0c368f1f0b1467ccb2ab2e57517ce742aa2bf9ec`.
- Branch: `codex/stage20-h31-toric-marked-fibre-migration`.
- Dry-run approval commit:
  `3eaa084ceb132824a37f1bc764d4b023b31d1c51`.
- Frozen-batch commit:
  `6efa6050c66aa4e1a71709d7041523e2f1230dc9`.
- Pure-move commit:
  `d9477c432f78decd8fd98cf4f6c71c69b589ef5f`.
- Substantive repair commit:
  `f113eb7cc98401d478e4f58839f3038d3c2e126b`.
- Substantive tree:
  `d0fa752b73c1c65c32b6fed027cbf5fc3bab58bc`.
- Batch ID: `p5-h31-toric-marked-fibre-stage20`.
- Mapping SHA-256:
  `48c99b929b824d4cf5709406aa846beb4a3f47cf18f570e936910ee9408621a2`.
- Approval-time raw Windows-checkout manifest SHA-256:
  `1398c2c84219d32cd26c50e68d4315f448a84d3cee8723cdb1a068bf0e566d30`.
- Actual mapping reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.

The approval-manifest hash is platform-specific and informational.  The
canonical mapping hash is the portable authority for the three old-to-new
pairs.  The approved ownership analysis is recorded in
[`p5-h31-toric-marked-fibre-stage20-dry-run.md`](p5-h31-toric-marked-fibre-stage20-dry-run.md),
and the executable batch is frozen in
[`catalog/batches/p5-h31-toric-marked-fibre-stage20.json`](../../catalog/batches/p5-h31-toric-marked-fibre-stage20.json).

## Moved proof-obligation boundary

The exact theorem/primary/audit triple moved flat to
`claims/p5/h31/toric-marked-fibre/`:

1. `P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md`;
2. `verify_p5_h31_toric_marked_fibre_obstruction.py`; and
3. `audit_p5_h31_toric_marked_fibre_obstruction.py`.

Its ownership topology is:

```text
P4 first pure-rank-two component toric fan + exact Segre slice (stay P4-owned)
  -> 21 genuine toric base-orbit/orientation cases
  -> 17 pure-direction types and 39 direction/orientation types
  -> both first-plane charts, every row shift, every binary extension
  -> 78 characteristic-zero projection/ledger runs
  -> 78 selected-obstruction unit ideals with 438 products
  => the complete marked H31 fibre over this genuine toric base boundary
     of the first/known component is empty

projective interior, second/further components, component exhaustiveness,
weighted H22, P5 -> Delta3, gluing, and global remain outside this leaf
```

Evidence roles remain distinct:

- the theorem and primary own the exact characteristic-zero obstruction;
- the primary reconstructs the toric/Segre data and all 156 exact runs;
- the `F5/F7` audit does not import the primary and independently computes
  modular kernels, projective extension directions, and marked-minor tests;
- the audit nevertheless shares `toric_cases` / `marked_rows`, reused
  modular marked-basis primitives, and hard-coded
  projection/certificate-selection data, so independence is claimed only
  downstream of that shared construction/data layer; and
- modular enumeration is QA, not the characteristic-zero proof.

No selected artifact has a curated theorem-ledger entry.  Stage 20 adds no
entry and changes no mathematical status, assumption, scope, evidence role,
lifecycle, or global-status field.

## Explicit exclusions and pre-existing status-provenance conflict

Stage 20 does not move or decide:

- the shared toric generator, high-coordinate helper, marked-basis primary,
  marked-basis audit, solver wrapper, or modular helper modules;
- the P4 component, toric-boundary, and Segre theorem packages;
- the projective interior or internal-`E=0` H31 packages;
- a second or further component or component exhaustiveness;
- weighted `H22`, `P5 -> Delta3`, arbitrary-order gluing, or the global
  conjecture.

The selected theorem and its P4 toric-boundary input contain checkpoint-era
prose saying that a second diagonal-quadric or further components remain
open.  Other synthesis artifacts record conflicting second-component closure
language.  Both sides substantially originate in commit `60a885ca`, so
recency cannot adjudicate the conflict.

Stage 20 does not endorse, reopen, or promote either side and does not use
the disputed prose as a premise.  The proof consumes only first-component
toric/Segre geometry.  Whole-document hashes are provenance, not a logical
status edge.  The primary's `additional_components_closed: false` remains
scope-local: this verifier proves no additional-component result.  Focused
scientific-status review, not layout migration, owns final adjudication.

## Pure-move acceptance

Against the pure-move commit's direct parent:

- exactly three source paths disappear and three destinations appear;
- all three moves are `R100`, and every destination Git blob equals the
  source-parent blob frozen by the batch;
- the only non-rename change is `catalog/moved-paths.json`;
- exactly the three selected `review_required` records become `moved` and
  gain `executed_batch: p5-h31-toric-marked-fibre-stage20`;
- no other manifest record or non-count metadata changes; and
- collision, double-move, and overlap-cycle counts remain zero.

The frozen source blobs are:

| artifact | Git blob |
|---|---|
| theorem | `f6e7ccccf1a2f4dc7a2273fe7db35993084e6b76` |
| modular audit | `c47068780b92e2f2e40d1a24882a440ba1535855` |
| characteristic-zero primary | `8707cd9f08a79dcdfd31a0b1ad7c0dbd0fad5b7e` |

Observed arithmetic:

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

There are zero new root-debt paths.  The frozen root baseline and end-state
allowlist are unchanged.

## Mechanical repair

Both moved executables now install the shared `krenn_gu.bootstrap` machinery
before any bare root-helper import.  Package-owned theorem and primary paths
use `HERE`; P4 inputs and the shared generator use `REPO_ROOT`.  The primary's
worker subprocess already re-executes the absolute script path, and Singular
consumes stdin, so no working-directory mutation was needed.  The staying
`verify_p5_high_coordinate_partial_frontier.py` received the single required
dependency-path retarget.  No other operational importer or subprocess
consumer targets either moved script.

The deterministic rewriter made exactly 11 Markdown-link changes and two
fenced replay-command changes across ten Markdown files, with zero
ambiguities and zero ledger relocations.  Its second pass is a `0/0/0` fixed
point.  Navigation records 28 H31 package directories and labels this package
as a first-component toric-boundary leaf, not a generic or complete-component
package.

Four existing ledger hashes changed mechanically while every status and
other semantic field remained fixed:

- the three root-README entries changed from `0a2bdc3d8f298425` to
  `8b8d7ee9a4cfe4ac`; and
- the verified high-coordinate frontier entry changed from
  `438f42c953f13628` to `56b23fe36b5d97d8`.

## Exact committed-head replay

All 27 affected executables ran at exact substantive head
`f113eb7cc98401d478e4f58839f3038d3c2e126b`.  Every successful run emitted
one JSON object and empty stderr, and every reported theorem, primary,
source, dependency, input, and output hash matched current bytes.  Scripts
that write results used only ignored `tmp/` paths; no tracked certificate or
report was refreshed.

The two moved executables and the directly retargeted high-coordinate primary
also ran from a fresh foreign working directory by absolute path.  The moved
primary pair agrees after removing only `elapsed_seconds`; the audit and
high-coordinate pairs agree exactly.

| executable | root | foreign | preserved result |
|---|---:|---:|---|
| toric marked-fibre primary | 200.699 s | 156.835 s | 17 direction types, 39 orientation types, 21 base cases, 78 projection + 78 obstruction runs, 18 binary-empty runs, 438 products; toric fibre true; projective/additional/global false |
| toric modular audit | 66.600 s | 66.400 s | `F5/F7`, 13,064 points, 520 closure artifacts, 272,624 extensions, 291,176 minor tests; global false |
| high-coordinate primary | 1.334 s | 1.276 s | census 6,495 / 1,680 / 1,170 / 510; exact existing first/second-component synthesis fields preserved; `P5 -> Delta3`/global false |

The remaining 24 consumer rows replayed semantically from root:

| rows | executables | runtimes | preserved boundary |
|---|---|---|---|
| 3-6 | P4 toric-boundary and toric-slice primary/audit pairs | `<1.5`, `0.637`, `1.736`, `0.652` s | exact toric/Segre surfaces; H31/P5/global false |
| 7-12 | P4 pure component primary/audit, chart closure, diagonal-quadric, mixed-orientation, and one-three component verifiers | `<3.4`, `0.503`, `1.498`, `<3.9`, `9.300`, `<5.0` s | component certificates preserved; all-pure/H31/H22/global remain scoped false where present |
| 13-14 | component-fibre-infinity primary/audit | `2.939`, `95.157` s | four orientations excluded; whole H31/P5/global not promoted |
| 15 | first-plane-infinity marked-fibre primary | `21.642` s | boundary true; internal `E=0`, additional components, global false |
| 16-20 | marked-basis open/classification primary/audit pairs and rank-two orbit verifier | `1.555`, `0.679`, `13.021`, `2.573`, `2.771` s | exact branch/finite-family scopes; projective/additional/H31/P5/global not promoted |
| 21 | internal-`E=0` primary | `106.599` s | 12 projections, 24 components, 29 charts, coupled unit ideal true; additional/global false |
| 23-25 | high-coordinate audit, first-rank-two H22 primary, and H22 mask-6 audit | `3.222`, `37.691`, `1.316` s | census current; generic H22 scoped; actual 12-flag wall `VERIFIED`; all-H22/global false |
| 26-27 | component19 ordinary and residual-axis derivations | `13.618`, `3.559` s | exact construction checks pass; both remain `CANDIDATE` |

Rows 3, 7, 10, and 12 completed with valid first JSON before a post-parse
PowerShell compatibility or handwritten schema assertion was corrected.  The
results were preserved and the scientific executables were not rerun; their
conservative outer-wrapper runtime bounds are reported above.

### Timeout and resource-isolation record

Several preliminary toric-primary attempts and one internal-`E=0` attempt
reached worker or outer-harness timeouts before emitting JSON.  These were run
outcomes only, not contrary evidence.  Inspection found eight orphan-parent,
CPU-bound Python workers that had run continuously since 2026-08-02/03, plus
one current anonymous worker.  No pre-existing or unrelated research process
was killed or modified on disk.

The successful expensive replays used two reversible schedules.  For the
200.699-second root toric-primary result, the eight old workers were assigned
`BelowNormal`, the current anonymous worker was untouched, and the candidate
wrapper and exact child received `High`.  For the later 156.835-second foreign
toric-primary and 106.599-second internal-`E=0` results, the eight old workers
were assigned `Idle`, the current worker `BelowNormal`, and the candidate
wrapper and exact child `High`.  On every normally completed run, each
touched process's original priority was saved and restored in `finally`.

A 900-second outer timeout once terminated its wrapper before `finally`.  In
that particular attempt, among pre-existing workers only the eight old
workers had been reprioritized; the current anonymous worker was not touched.
The timed-out candidate wrapper and exact child had separately received
`High`.  The exact candidate child tree was identified by parentage and full
command line and stopped leaf-first.  The eight old workers were inspected at
`BelowNormal` and immediately restored to their original `Normal` priority.
Later successful resource-isolated runs did temporarily assign the current
anonymous worker `BelowNormal`, and its saved original priority was restored
by their normal `finally` paths.  A final read-only process and Git audit
confirmed no candidate, WSL, or Singular orphan and no tracked/index drift.

With these guarded schedules, the unchanged toric primary passed root and
foreign CWD and the unchanged internal-`E=0` primary passed in its historical
runtime envelope.  The initial timeouts neither replace nor negate these
complete first valid results.

Native Singular is absent.  The existing WSL Singular 4.3.2 fallback passed
the exact eliminations.  Python was pinned to 3.13.14 with SymPy 1.14.0 and
`python-sat`; both moved modules also pass isolated foreign-CWD import probes.

## Validation and publication boundary

The clean substantive head passes:

- workflow-dispatch hygiene run
  [31302708919](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31302708919)
  passed at the exact substantive SHA;
- `check_hygiene.py`: 1,698 Python files compile, all 813 pre-report Markdown
  files have resolving local links, all 86 ledger hashes match, root debt is
  `1,965 grandfathered / 0 new`, and all 392 retired-path/provenance records
  pass;
- all 152 migration-tool tests;
- all 14 fourteen-vertex cycle-cover lattice tests;
- targeted Ruff checks and byte compilation for the three directly affected
  Python files;
- the complete 27-executable replay matrix and three required root/foreign
  pairs;
- two isolated moved-module import probes;
- rewriter fixed point; and
- clean index/worktree diff checks.

Adding this report raises the final Markdown count from 813 to 814.  The final
documentation candidate must rerun the index-complete floor, receive fresh
Tier-2 semantic/status and mechanical/bypass referee passes, and pass final
exact-head PR CI before a normal guarded merge.

## Independent final referees

The report candidate at index tree
`73b1aaee70da465d2a70c4dba18160e8b030dd26`, with substantive HEAD
`f113eb7cc98401d478e4f58839f3038d3c2e126b` and staged report blob
`023cbd8e63620895615a8340b06a13e777de45c2`, received two independent
read-only final passes:

- the Tier-2 semantic/status referee returned **PASS**, confirming the exact
  first-component toric-boundary scope, limited audit independence, unchanged
  ledger semantics, unadjudicated second-component conflict, candid timeout
  account, and global **UNRESOLVED** boundary; and
- the mechanical/provenance/bypass referee returned **PASS**, independently
  reproducing the commit chain, batch and approval hashes, three `R100`
  blobs, selected-only manifest transaction, root/debt arithmetic, rewrite
  and ledger surface; reconstructing the complete 27-row consumer matrix and
  auditing its preserved replay evidence; and confirming the exact CI result,
  full local floor, and absence of bypass or candidate drift.

This referee record is the sole report change after that reviewed pin.  A
lightweight read-only superseding check must confirm this append-only delta;
its exact final-tree verdict is recorded durably in the Stage 20 pull-request
review trail without another self-referential report edit.

## Stop boundary

Stage 20 stops at the exact complete marked-`H31` fibre over the genuine toric
base boundary of the first pure-rank-two compression component.  The
projective interior, internal-`E=0` sibling, second and further components,
component exhaustiveness, and the broader conflicting status prose remain
separately owned.  Weighted `H22`, `P5 -> Delta3`, local-to-global gluing, and
all global work remain separate.  The global Krenn-Gu conjecture remains
**UNRESOLVED**.
