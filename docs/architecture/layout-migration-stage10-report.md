# Layout migration report — Stage 10 (deferred generic recovery and bounded P5 migration)

Status: **the Stage 10 recovery and migration transaction is complete and
ready for an independent merge-gate review.**  One pre-existing operational
blocker was repaired in a separate commit, then nine live generic packages
(25 files) were moved into the P5 claim spine.  The batch contains nine
theorem documents, nine primary verifiers, and seven existing independent
audits.

> **Scientific status did not change.**  Generic theorems remain generic;
> special divisors, projective boundaries, exceptional fibres, pointwise
> closure, and the global Krenn--Gu conjecture remain open where they were
> open before Stage 10.  In particular, the two equal-support-sixfold P5
> packages have primary verifiers but no P5 independent audits.

## Provenance anchors

- Stage 9 baseline: merge commit
  `5db0fd317a1b77aaa3003a16b0cde9be89d9c568`, verified as the merge of PR
  #38 and as both local and remote `main` before the Stage 10 branch was
  created.  There were no intervening main commits.
- Branch: `layout-migration-stage10-deferred-generics`.
- Preflight repair (R):
  `943920421515282653cd6831b9d7b6cfa002e060`.
- Inventory, classifier correction, and dry-run (A):
  `45a2bcde25d1a3318581fd7102100a25b8f8a1ec`.
- Frozen batch (B): `c9e7c94904e77c1ad8849e0eb7df048823602be2`.
- Pure move (C): `c9b354fe0905aa465ef38553c657c86e849d807e`.
- Mechanical repair (D):
  `c93a5c6828c01ebb216b54046a3a5ef8796638de`.
- Dry-run: [`p5-deferred-generics-stage10-dry-run.md`](p5-deferred-generics-stage10-dry-run.md).
- Frozen batch: `catalog/batches/p5-deferred-generics-stage10.json`:
  - approved_by: "YesterdaysLemon (repository owner), Stage 10 deferred
    generic P5 migration instruction";
  - base_sha: `45a2bcde25d1a3318581fd7102100a25b8f8a1ec`;
  - member_count: 25;
  - mapping_sha256:
    `e39d17c3ed855ef5a1342560ebf61e9b313246142f24af23940bc3ff8af472db`;
  - approval-time manifest_sha256:
    `6c4314b2f2762f0affc5fe48ad60b7220620c06e3a9beae36365afefaf640e35`.

Approval applies only to this exact mapping.  It does not approve the
remaining P5 boundary, divisor, partial, or candidate work.

## Preflight operational repair

Both root equal-support-sixfold primaries failed before any Stage 10 move:

```text
verify_p5_h31_equal_support_sixfold_component_generic_obstruction.py  rc=1 FileNotFoundError
verify_p5_h22_equal_support_sixfold_component_generic_obstruction.py  rc=1 FileNotFoundError
```

The scripts still named the P4 theorem and primary at repository-root paths,
while the actual P4 package had moved to
`claims/p4/components/equal-support-sixfold/` in Stage 3.  Git history and
blame established that the bad constants predated Stage 10; the Stage 9 report
had independently recorded the same failures.

Commit R changed only the four stale constants.  No assertion, algebra,
solver strategy, coefficient domain, theorem prose, or status changed.  The
pre-move repaired replays then returned rc=0:

| primary | seconds | semantic result |
|---|---:|---|
| equal-support H31 | 13.25 | generic marked H31 excluded; complete boundary, H31 census, and global result false |
| equal-support H22 | 48.52 | generic weighted H22 excluded with no generic open slope divisor; full H22/global result false |

The repair produced ignored `tmp/` output only and left tracked state clean.

## Equal-support evidence structure

The H31 and H22 ledger records each name a theorem and primary verifier and
explicitly record `independent_audit: null` / `none_exists`.  No exact-name P5
audit exists.  The audit in the P4 equal-support package audits the P4
component theorem only and explicitly does not establish the P5 H31 or H22
obstruction.

Stage 10 therefore migrated each equal-support side as an honest
theorem/primary pair.  It did not create evidence, claim symmetry with Stage 9
triples, or promote scientific confidence.  The classifier's two inaccurate
"verify/audit triple" descriptions were corrected to describe the actual
primary-only pairs; ownership, confidence, status, and destinations were
unchanged.

## Bounded delegation result

Three read-only agents were used; the lead remained the sole decision-maker
and writer.

| task | inspected surface | compact result | confidence | lead spot-check | usefulness |
|---|---|---|---|---|---|
| equal-support archaeology | both P5 theorems/primaries, ledger, P4 evidence, history, consumers | reconstructed stale-path chronology and proved that no P5 audit exists | high | yes: paths, ledger, history, and full replays | high |
| stale-path/provenance audit | selected executables, moved P4/P5 dependencies, 31 import consumers, frontier paths | isolated the pre-move blocker and exact post-move repair surface; recorded unrelated candidate debt without cleaning it | high | yes: every consequential path and consumer class | high |
| deferred-family classification | listed Stage 9 deferred families, theorem prose, ledger, evidence roles, boundary ownership | identified a conservative 25-file / 9-package generic-only slice | medium-high | yes: every included package and each exclusion class | medium-high |

The agents materially reduced primary-context burden: broad searches returned
exact locations and compact inventories, after which the lead inspected the
consequential evidence rather than reproducing each broad search.  No agent
edited repository files, froze the batch, or made scientific-status decisions.

## Selected packages and roles

| side | package | members | evidence structure |
|---|---|---:|---|
| H31 | equal-support-sixfold | 2 | theorem + primary; no P5 audit exists |
| H22 | equal-support-sixfold | 2 | theorem + primary; no P5 audit exists |
| H31 | common-center-kernel-star | 3 | theorem + primary + independent audit |
| H31 | unequal-complement-common-kernel | 3 | theorem + primary + independent audit |
| H31 | unequal-endpoint-inward-star | 3 | theorem + primary + independent audit |
| H31 | one-three | 3 | theorem + primary + independent audit |
| H22 | one-three-components | 3 | theorem + primary + independent audit |
| H31 | split-center-mixed-star | 3 | theorem + primary + independent audit |
| H22 | first-rank-two | 3 | theorem + primary + independent audit |

Role totals are 9 `primary_verifier`, 7 `independent_audit`, and 9 theorem
documents.  No support dependency, optional exploration, generator,
candidate, boundary, or partial file moved.

## Deferred-family disposition

- `common-active-binary-triangle`: H31 boundary-inseparable; H22 remains a
  candidate with path and evidence debt.
- `embedded-p3`: both generic documents remain joined to same-theorem
  boundary/closure chains.
- common-center H22: scientifically partial.
- unequal-complement H22: partial D01/D23 boundary recursion.
- unequal-endpoint H22: partial, boundary-inseparable, and too large for this
  stage.
- diagonal-quadric elliptic H31: its primary and prose consume a ten-file
  elliptic boundary forest.
- split-center H22: load-bearing imports from a common-active candidate
  derivation make the evidence boundary unclear.

These are deferrals, not demotions.  No pointwise divisor or boundary recursion
entered the P5 generic spine.

## Pure-move acceptance

Against commit C's direct parent:

- all 25 exact sources were absent and all 25 destinations present;
- every destination's index blob matched its source-parent blob;
- all eligible renames were `R100` and all moved-member numstats were `0/0`;
- all 1,990 unselected manifest records were unchanged;
- the manifest transaction recorded all 25 members as `moved` with the frozen
  Stage 10 batch as `executed_batch`;
- no scientific prose or executable repair was mixed into C.

Observed manifest arithmetic after C:

| state | count |
|---|---:|
| moved | 350 |
| proposed | 252 |
| review | 1,413 |
| unclassified | 348 |
| moved-only root projection | 2,022 |

The actual indexed root-entry count fell from 2,048 to 2,023.  The one-entry
difference from the projection is the committed `AGENTS.md`, which is outside
the classifier universe.

## Mechanical repair and staying consumers

The shared migration machinery rewrote 34 Markdown links and 24 fenced replay
commands across 17 files on its first pass.  The final fixed point was:

```text
links_rewritten: 0
replay_rewritten: 0
files_touched: 0
ambiguities: []
```

Moved executables received only bootstrap, package exposure, and relocated
theorem/verifier/P4 paths.  Sixteen moved executable docstrings were compared
to C and were identical.  Every watched `THEOREM`, `PRIMARY`, `COMPONENT`,
`COMPONENT_PRIMARY`, `COMPANION`, and `CANONICAL_PRIMARY` path resolved.

Thirty-one staying root H22 scripts import one of four moved H31 modules:
7 common-center, 12 unequal-complement, 11 unequal-endpoint, and 1 split-center.
Each is byte-for-byte its C version plus one exact shared
`bootstrap`/`expose_claim_package` block.  All 31 imported successfully in
fresh WSL subprocesses.  The staying high-coordinate frontier received three
path-only theorem updates.

## Mandatory post-move replay

All rows used the repository root as working directory and this environment:

```text
wsl.exe --cd /mnt/c/Users/Yeste/OneDrive/Documents/open-graph-theory-with-prize --exec python3 <script>
Python 3.12.3; SymPy 1.14.0; Singular 4.3.2
```

| role | package | seconds | rc | semantic result |
|---|---|---:|---:|---|
| primary | H31 equal-support | 9.27 | 0 | generic true; boundary/census/global false |
| primary | H22 equal-support | 48.09 | 0 | generic true and generic slopes closed; full H22/global false |
| primary | H31 common-center | 10.95 | 0 | generic true; H22/global false |
| primary | H31 one-three | 38.83 | 0 | three generic fibres excluded; boundaries/global false |
| primary | H22 one-three | 24.24 | 0 | three generic incidences empty; divisors/boundaries/global false |
| primary | H31 unequal-complement | 43.51 | 0 | generic true; global false |
| primary | H31 unequal-endpoint | 8.19 | 0 | generic true; pivot/special boundaries/global false |
| primary | H31 split-center | 14.80 | 0 | generic true; H22/global false |
| primary | H22 first-rank-two | 28.20 | 0 | generic true; divisors/boundary/global false |
| audit | H31 common-center | 1.08 | 0 | independent no-import rational audit passed |
| audit | H31 one-three | 5.13 | 0 | audited true; independent of primary imports |
| audit | H22 one-three | 47.73 | 0 | audited true; independent; finite-field results corroborative only |
| audit | H31 unequal-complement | 1.36 | 0 | rational audit passed; global false |
| audit | H31 unequal-endpoint | 6.72 | 0 | independent quotient-ring audit passed; boundary/global false |
| audit | H31 split-center | 2.13 | 0 | independent rational audit passed; characteristic-zero proof not replaced |
| audit | H22 first-rank-two | 8.18 | 0 | audited true; independent; finite-field results corroborative only |

All 16 mandatory replays were semantically green.  The final measured table
totals 298.41 seconds.  Equal-support contributes no audit rows because none
exists.

The staying `verify_p5_high_coordinate_partial_frontier.py` replay also passed
(0.79 seconds, rc=0), resolved the moved theorem hashes, and still reported
`P5_to_Delta3_resolved=false` and `global_conjecture_resolved=false`.

## Tracked-output and hash-domain audit

Eight mandatory scripts write JSON below ignored `tmp/`; eight are stdout-only.
The frontier also writes ignored `tmp/p5_high_coordinate_partial_frontier_verified.json`.
`git status --short` and `git diff` were clean after the primary tier, audit
tier, common-center timing confirmation, and frontier replay.  No tracked
result, certificate, or snapshot changed.

Ledger hashes are Git index/blob hashes, not Windows working-tree hashes.  This
avoids false corruption reports caused by CRLF conversion.  The Stage 10 batch
mapping hash uses canonical mapping serialization and was recomputed exactly;
the approval-time manifest hash remains informational provenance.

## Ledger and navigation

- Nine existing ledger entries were repointed to their moved theorem,
  verifier, and existing-audit paths; no entry or status was added.
- `legacy_paths`, claim-package metadata, and proof-variant metadata were
  preserved/generated through the normal rewriter.
- Document hashes were refreshed from the staged Git index after link repair.
- `claims/p5/README.md`, `claims/p5/h31/README.md`, and
  `claims/p5/h22/README.md` now list the recovered packages and state the
  equal-support audit absence explicitly.

## Validation floor

- all changed Python files compile;
- 45 changed/moved/staying Python files import in fresh WSL subprocesses;
- 117 migration-tool tests pass;
- 14 fourteen-vertex lattice tests pass;
- migration rewriter fixed point is exactly 0 links, 0 commands, 0 touched
  files, 0 ambiguities;
- `check_hygiene.py` passes on the complete staged candidate tree;
- batch mapping, manifest arithmetic, moved-only projection, provenance, and
  stale-path checks pass;
- no untracked nonignored file or unstaged tracked change is present in the
  candidate tree.

## CI bookkeeping

The migration workflow is dispatched only after the substantive final report
and navigation commit exists.  Its exact run ID, tested SHA, and conclusion
are recorded by the permitted report-only bookkeeping commit.

## Stop condition

Stage 10 stops at this bounded recovered generic layer.  It does not enter
pointwise divisor/boundary recursion, repair unrelated old stale paths, create
missing audits, normalize Singular invocation style, or advance any theorem
claim.  The branch is intended to be opened as an unmerged PR for a fresh
independent merge-gate review.
