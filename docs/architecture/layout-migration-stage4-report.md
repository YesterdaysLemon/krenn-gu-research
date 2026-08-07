# Layout migration report — Stage 4 (P4 component packages, six families)

Status: **the high-confidence P4 pure-component package set is
complete.**  Six full theorem packages (theorem + primary verifier +
independent audit each) moved from the repository root into
`claims/p4/components/`, joining the three Stage 3 packages — nine
migrated standalone pure-component packages total.  Provenance,
replayability, links, ledger integrity, and Git history preserved; the
Stage 3 executor fix (automatic manifest-summary recomputation) proven
under real execution.

> No theorem claim, assumption, scope, provenance status, or
> global-resolution status changed as a result of this migration. The
> global Krenn–Gu conjecture remains **UNRESOLVED**.

## Provenance anchors

- Starting main SHA: `1d96829` (merged main including PR #31), tagged
  `stage4-start`.
- Branch: `layout-migration-stage4-p4-components`.
- Batch: `p4-components-stage4`, artifact
  `catalog/batches/p4-components-stage4.json`:
  - approved_by: "YesterdaysLemon (repository owner), Stage 4 P4
    component migration instruction";
  - approved_at: 2026-08-06;
  - base_sha: `1025f88` (Stage 4 commit A1);
  - informational manifest_sha256 recorded;
  - **mandatory** canonical mapping_sha256:
    `5833e9f2e17fce64c03563093d76e870065ea49190a96e567ec06538d37c6f91`;
  - member_count: **18**.
- Packages: all-rank-one-triangle, diagonal-quadric, embedded-p3,
  mixed-orientation, single-word-quadrilateral, six-dimensional.
  **No exclusions** — all six triples verified present, unambiguous,
  and replayable; the desired minimum of 4 and the target of 6 were
  both met.
- Pure-move commit: `42a65a3`; R100 count: **18 / 18** (every moved
  file recorded by Git as a 100%-similarity rename — history
  preserved, no content change).

## Root-count accounting (observed)

| Moment | Root entries |
|---|---|
| 1. original pre-migration root (`pre-layout-migration-v1`) | **2,366** |
| 2. Stage 4 starting `main` (`1d96829`) | **2,319** |
| 3. immediately after pure Stage 4 moves (`42a65a3`) | **2,301** |
| 4. final PR head | **2,301** |

Moments 3 and 4 are equal because everything added after the pure move
(dry-run report, batch artifact, this report) is nested under
`docs/` or `catalog/`.

Manifest tallies (observed, produced by the executor itself):

```text
stage4_files_moved                    18
stage4_root_entries_removed           18
cumulative_moved_entries              71
stale_paths_enforced (after)          71   (53 before + 18 = 71 ✓)
remaining_proposed_high_confidence    361
remaining_review_required             1583
remaining_unclassified                348
```

## Executor acceptance test (Step 11) — real-world proof

Immediately after the executor ran (before any rebuild), the manifest
already carried:

```text
counts.moved                        53 + 18 = 71        ✓
counts.proposed_high_confidence    379 - 18 = 361       ✓
counts.review_required             1583 (unchanged)     ✓
projected_root_if_moved_only       2319 - 18 = 2301     ✓
```

`finalize_execution` re-derived every summary number from the records
inside the rollback-safe transaction; no manual rebuild was needed at
any point in Stage 4.  This is the Stage 3 executor fix passing its
first real multi-package execution.

## The dependency chain (Step 13 acceptance)

Stage 4's central objective — proving the chain survives multiple
package relocations:

```text
mixed-orientation (moves)
      ↑ imported by
disjoint-mixed-star (moved Stage 3)
      ↑ imported by
all-rank-one-triangle (moves)
      ↑ guarded-imported by
verify_p5_h22/h31_all_rank_one_triangle_… (stay at root)
```

- The moved DMS verifier now exposes the moving mixed-orientation
  package via the shared helper; the moving AROT verifier exposes both
  the DMS and MO packages.
- The two root P5 AROT verifiers keep their fail-open
  `if COMPONENT_PRIMARY.exists():` guards, with the expose call inside
  the guard so absence still degrades gracefully.
- Clean-subprocess acceptance (fresh interpreter, only the repo root on
  `sys.path`): MO verifier imports; DMS verifier imports MO; AROT
  verifier imports DMS + MO; the H31 AROT guarded import resolves and
  reconstructs the component family (4 planes).  All pass.

## Import-shim debt (Step 7) — resolved narrowly

Stage 3 left five per-importer `sys.path` shims for the moved
disjoint-mixed-star package (one root H31 script + the four moved H22
scripts).  Stage 4 consolidated them into ONE shared helper,
`krenn_gu.bootstrap.expose_claim_package(repo_root, rel)`:

- lives in the existing `src/krenn_gu/bootstrap.py`;
- validates the package directory exists (loud `FileNotFoundError`);
- repository-relative path only (absolute/`..`-escaping paths refused
  with `ValueError`, including the Windows `PurePath` absoluteness
  quirk — regression-tested);
- contains the `sys.path` mutation in one place; idempotent;
- no `.git` dependency; hyphenated directories stay hyphenated; claim
  directories are NOT turned into Python packages.

Five tests added (`ExposeClaimPackageTests`); migration-tool suite grew
76 → 81 tests.  No Stage 3-style one-off shim was added in Stage 4 —
every new bare-name import (DMS→MO, AROT→DMS/MO, P5 AROT guards) goes
through the helper.

### Pre-existing debt found and fixed

`verify_p4_common_singleton_component.py` was **already broken on
`stage4-start`**: its fragment inventory read the Stage-3-moved
disjoint-mixed-star verifier from the root (`FileNotFoundError`).  It
escaped hygiene because it is not a fast verifier.  Fixed in commit A1
with a manifest-aware path resolver (tries root, then the executed-move
map); inventory verified passing before any Stage 4 move.

## Link and import rewrites

- Rewriter first pass: 67 links re-anchored across 39 files, 10 fenced
  replay commands repointed, 0 ambiguities.  Second pass: **0 links, 0
  commands, 0 ambiguities** (idempotent).
- Machinery gap (recorded, fixed manually): the rewriter's replay
  matcher only covers single-line `python <file>.py` fences.  Three
  docs needed manual repairs: the embedded-p3 `uv run --with sympy`
  form, the mixed-orientation continuation line, and the Stage 3
  leftover continuation lines in the moved DMS theorem doc (4 commands
  total).  Same gap applies to the bare-basename stale scanner; the
  manual repairs keep the tree stale-clean.  No broad rewriter
  redesign — recorded as deferred debt.
- Python: 34 `.py` files changed in commit C (12 moved Stage-4 scripts
  switched to the centralized bootstrap; 3 Stage-3-moved scripts
  repointed to the moving packages; 19 staying consumers — P5
  H22/H31 AROT/MO/DQ/six-dimensional verifiers, the high-coordinate
  frontier, three P4 classification scripts — repointed their doc and
  primary-script constants).  All moved scripts' path constants
  existence-checked; all chain imports tested in clean subprocesses.
- No theorem prose changed (verified by diff: only link targets and
  fenced command paths).

## Replay results (Step 14)

Post-migration replays from the new locations (working directory:
repository root; outputs in `tmp/`, untracked):

| Package | Verifier | Audit |
|---|---|---|
| all-rank-one-triangle | **verified=true** (pure sympy, ~3 s) | audited=true, independent=true (~2 s) |
| diagonal-quadric | **verified=true** (pure sympy, ~2 s) | audited=true, independent=true (~1 s) |
| embedded-p3 | **verified=true** (pure sympy, ~1 s) | audited=true, independent=true (<1 s) |
| mixed-orientation | **verified=true** (Singular via WSL fallback, ~8 s) | audited=true, independent=true (~3 s) |
| single-word-quadrilateral | **verified=true** (Singular ds slice, run under WSL python, 438 s) | audited=true, independent=true (~1 s) |
| six-dimensional | **verified=true** (pure sympy, ~2 s) | audited=true, independent=true (<1 s) |

The moved DMS verifier (Stage 3, content changed only by the MO expose
line + constant) replayed `verified=true` (~3 s); the unchanged DMS
audit replayed `audited=true, independent=true` (~3 s).  External
binary: Singular 4.3.2 in WSL (native `Singular` not on the Windows
PATH).  No verifier claimed without execution.

Pre-move baselines: AROT, DQ, EP3, six-dimensional verifiers exit 0
(~2 s each); MO verifier exit 0 (~7 s).  The SWQ verifier/audit
pre-move baseline exceeded the background-job time cap before emitting
output and is recorded as not completed pre-move; the post-move replay
is the evidence.

## Ledger (Step 16)

- No theorem-ledger entry references any of the 18 moved files (the
  ledger is a curated partial index centered on the P5 generic-fibre
  claims).  0 entries repointed; no entries were fabricated.
- 13 committed-blob hash fields refreshed (11 unique docs whose content
  changed during reference rewrites: README.md ×3 entries,
  P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md, and the eight P5
  H22/H31 theorem docs linked from the moved packages).  All 85 ledger
  hashes validate.

## Stale-reference enforcement (Step 18)

Enforced old paths increased from 53 to **71** (53 + 18 = 71 ✓; 3
full-path, 68 root-to-package).  Zero stale references outside
provenance.  Checked root markdown links, `docs/` links, already-migrated
H22 and Stage 3 P4 packages, P5 H31/H22 downstream scripts, replay
commands, the ledger, workflow comments, and Python string paths.

## Machinery behavior

- **Executor summary recomputation worked without rebuilding** — the
  exact Step-11 numbers above were produced by `finalize_execution`
  inside the transaction; `check_hygiene.py [11]` agrees.
- **Rollback was NOT invoked** — no mid-batch failure.
- **Migration-tool bugs found:** one pre-existing consumer breakage
  from Stage 3 (common-singleton inventory; fixed narrowly + documented
  above) and the replay-fence matcher gap (documented, manual repair).
  No defect in the executor, contract validator, or summary
  recomputation.
- **New regression tests:** 5 (ExposeClaimPackageTests).  No executor
  regression test was needed (none was broken).

## Validation floor (Step 21)

On the final head: `check_hygiene.py` all green (1,697 files compile;
all markdown links resolve; ledger 85/85 hashes; provenance 71/71;
stale paths 71 enforced, none present; portability clean; 5 fast
verifiers pass).  81 migration-tool tests OK.
`test_fourteen_vertex_cycle_cover_lattice.py` OK (14 tests).  Rewriter
idempotent (second pass 0/0/0).  CI run __CI_RUN__ on the exact final
head __FINAL_SHA__.

## Deferred debt (for Stage 5)

1. The replay-fence matcher in `rewrite_links.py` does not cover
   continuation-line (`python \` + filename) or `uv run` command
   forms; the matching stale-bare-reference scanner has the same
   blind spot.  Both were repaired manually this stage; a narrow
   rewriter extension is Stage 5 material.
2. The large `claims/p4/classifications/` population (medium/low
   confidence) remains at root — a different ownership problem,
   explicitly out of scope here.
3. `verify_p4_common_singleton_component.py`'s fragment inventory
   still scans nine root scripts that may move in later stages; its
   manifest-aware resolver already handles those moves without edits.

## Stop condition

This PR does not begin the classification-family evacuation.  Stage 4
proves the workflow scales to a moderate multi-package dependency batch
(18 files, six packages, one cross-package import chain) with frozen
approval, exact provenance, automatic summary maintenance, and full
replayability.

> No theorem claim, assumption, scope, provenance status, or
> global-resolution status changed as a result of this migration. The
> global Krenn–Gu conjecture remains **UNRESOLVED**.
