# Layout migration Stages 20-26 program audit and handoff

Status: **PASS WITH NON-BLOCKING GOVERNANCE AND SCIENTIFIC-PROVENANCE
DEBT. MIGRATION PAUSED AFTER STAGE 26.**

The global Krenn-Gu conjecture remains **UNRESOLVED**. This is a post-merge,
read-only audit and operating handoff for Stages 20-26. It does not promote a
claim, reconcile scientific conflicts, authorize Stage 27, or change an
evidence status. Repository-owner direction is to stop migration exploration
at this boundary.

## Audited boundary

- Pre-Stage-20 merged baseline: `0c368f1f0b1467ccb2ab2e57517ce742aa2bf9ec`.
- Stage-26 final PR head: `aaa3d8a3958057e88f2663b305192e4f403393e8`.
- Stage-26 merge and audited main: `8be5a11730aa7fccb34224e1c108ea658e57fc07`.
- Stage-26 substantive head: `3e501cbe36a6133d02afe85ff68eaf1bf097a9a7`.

Independent semantic/status and mechanical/provenance reviews reconstructed
the frozen mappings, pure moves, root-debt arithmetic, repair surfaces,
replay evidence, ledger invariants, PR lineage, CI, cleanup boundary, and
current Git state. Every Stage 20-26 merge is a normal two-parent merge whose
tree equals the reviewed final branch-head tree. The first-parent merge chain
is uninterrupted.

## Exact stage ledger

| stage | batch and destination | mapping SHA-256 | files | replay closure | PR head / merge | debt after |
|---|---|---|---:|---|---|---:|
| 20 | `p5-h31-toric-marked-fibre-stage20` -> `claims/p5/h31/toric-marked-fibre/` | `48c99b929b824d4cf5709406aa846beb4a3f47cf18f570e936910ee9408621a2` | 3 | 27 executables / 30 invocations | [#52](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/pull/52) `b89a315d` / `7352a061` | 1,965 |
| 21 | `p5-h22-six-dimensional-equal-weight-stage21` -> existing six-dimensional H22 package | `f7427206126ecc290b0a926c1731eb5eb557aca7d784547d4c64df2dc2b41cf0` | 3 | 11 / 14, then bounded portability closure | [#53](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/pull/53) `80e42c0b` / `2040f9ff` | 1,962 |
| 22 | `p5-h31-component-chart-boundary-stage22` -> `claims/p5/h31/component-chart-boundary/` | `7130acd031ab499906c6c463298292de459ce7a60eac566a35986d40d3763837` | 3 | 16 / 22 plus two imports | [#54](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/pull/54) `5582d262` / `2f52d8fa` | 1,959 |
| 23 | `p5-h31-component-fiber-infinity-stage23` -> `claims/p5/h31/component-fiber-infinity/` | `3874be216b1210251aea1150fa655e7ea5bde0c035df0d8c9d51d18b0d57a454` | 3 | 11 / 16 plus import probes | [#55](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/pull/55) `f5d0bf79` / `28b3ff93` | 1,956 |
| 24 | `p5-h31-component-fibre-infinity-marked-fibre-stage24` -> `claims/p5/h31/component-fibre-infinity-marked-fibre/` | `103e5de3343c1271841a84cfa79903c9d9e8c6f2c318adc8325c3b8cd1a3ace1` | 4 | 14 / 24 plus three imports | [#56](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/pull/56) `c20fd139` / `6bff7b46` | 1,952 |
| 25 | `p5-h22-finite-lambda-one-all-marking-stage25` -> lambda-one H22 package | `611abb78c553a124a4cf02308950ec5ace6c9f5f1e2e727ece7f043f3b1f59ba` | 3 | 2 / 4 plus two imports | [#57](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/pull/57) `604ea750` / `cd97b313` | 1,949 |
| 26 | `p5-h22-finite-lambda-zero-all-marking-stage26` -> lambda-zero H22 package | `06622ad9c8ab149021fd4d3a5c412327db4a28cd2f210d339418d118a7e85131` | 3 | 3 / 5 plus two imports | [#58](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/pull/58) `aaa3d8a3` / `8be5a117` | 1,946 |

The detailed evidence, scope, repair, and replay assertions remain in the
[Stage 20](layout-migration-stage20-report.md),
[Stage 21](layout-migration-stage21-report.md),
[Stage 22](layout-migration-stage22-report.md),
[Stage 23](layout-migration-stage23-report.md),
[Stage 24](layout-migration-stage24-report.md),
[Stage 25](layout-migration-stage25-report.md), and
[Stage 26](layout-migration-stage26-report.md) reports.

Stage 21's original 14-invocation matrix produced 13 successful JSON results
and one native-Singular environment failure. A bounded, transport-only
portability repair then passed the failed primary from root and foreign CWD.
Stage 23 preserved a PowerShell quoting failure that occurred before module
import; the separately authorized corrected import-only probe passed without
rerunning scientific evidence. Neither event was counted as theorem evidence.

## Root-exit and catalog accounting

Stages 20-26 retired 22 grandfathered root files, moved no scientific status,
and created no new root debt.

| boundary | root files | root dirs | grandfathered / new debt | manifest moved | H22 / H31 dirs | `claims/` files |
|---|---:|---:|---:|---:|---:|---:|
| before Stage 20 | 1,975 | 9 | 1,968 / 0 | 389 | 18 / 27 | 393 |
| after Stage 20 | 1,972 | 9 | 1,965 / 0 | 392 | 18 / 28 | 396 |
| after Stage 21 | 1,969 | 9 | 1,962 / 0 | 395 | 18 / 28 | 399 |
| after Stage 22 | 1,966 | 9 | 1,959 / 0 | 398 | 18 / 29 | 402 |
| after Stage 23 | 1,963 | 9 | 1,956 / 0 | 401 | 18 / 30 | 405 |
| after Stage 24 | 1,959 | 9 | 1,952 / 0 | 405 | 18 / 31 | 409 |
| after Stage 25 | 1,956 | 9 | 1,949 / 0 | 408 | 19 / 31 | 412 |
| after Stage 26 | 1,953 | 9 | 1,946 / 0 | 411 | 20 / 31 | 415 |

Current manifest totals are `2,015 = 411 moved + 242
proposed_high_confidence + 1,362 review_required`, with 348 unclassified.
Collision, double-move, and overlap-cycle counts are zero. The curated theorem
ledger remains 86 entries, its completeness remains partial, and its global
status remains `UNRESOLVED`.

## Stage 26 final evidence

The Stage 26 substantive tree `7191c8c2c7d1a5c55cc0a114a4f97557c73a0c3c`
passed the protected five-row scientific matrix exactly once, serially, with
no retry. The dense-open premise ran once; moved primary and audit each passed
from repository root and a fresh foreign CWD with byte-identical pairs. All
five rows returned one JSON object, `rc=0`, and empty stderr. Both isolated
import probes passed. The exact generic-point `Q(r,t)`, finite `lambda=0`,
all-affine-marking scope, the load-bearing prior `h2*h3*H0` factor cover, the
three selected residual branches, and the exact-Q `(2,4)` audit limitation
remain separate. Special/projective fibres and the global conjecture remain
outside this leaf.

The final report-inclusive floor passed with 1,698 Python files, 827 Markdown
files, 86/86 ledger hashes, root debt `1,946 / 0`, 411 provenance records,
152 migration-tool tests, 14 lattice tests, and rewriter fixed point `0/0/0`.
Stage 26 then passed:

- substantive workflow-dispatch run `31325904337`, job `93276122040`, at
  `3e501cbe`;
- exact-final-head pull-request run `31326434844`, job `93277452433`, at
  `aaa3d8a3`; and
- merged-main push run `31326477601`, job `93277560423`, at `8be5a117`.

All were successful on attempt one. The final PR head and merge trees are
identical.

## Overdue program-audit finding

The committed cadence required a program audit every three stages. The last
committed audits cover [Stages 14-16](layout-program-audit-stages14-16.md) and
[Stages 17-19](layout-migration-stages17-19-program-audit.md). The Stage
20-22 window became overdue when Stage 23 began, and the complete Stage 23-25
window also passed without its required committed audit. This document closes
the documentary, read-only audit through Stage 26; it does not retroactively
weaken any individual stage gate.

No evidence of classifier-as-authority use, unapproved batch execution,
collision, double move, overlap cycle, scientific-body mutation during pure
moves, or bypass was found. However, the Stage 20-26 reports retain
pre-merge wording such as "awaiting merge" or "awaiting final CI" after their
PRs merged. Git objects and GitHub run metadata are authoritative. This is
durable report/CI traceability drift, not evidence that a gate was skipped.
Future reports should be generated or finalized from exact post-merge
metadata rather than left at the pre-merge checkpoint.

## Owner-gated scientific conflicts

These conflicts remain explicit stop conditions for any status-consuming
move, proof-graph use, or prose harmonization. This audit does not choose a
side.

1. **H31 chart-boundary marked-fibre 14-vs-16 conflict.** The theorem twice
   describes 14 elementary certificate strata, while the primary contains 16
   `Stratum` records and asserts/reports 16. The separate phrase "fourteen
   mixed binary coefficients" is not a reconciliation, and the modular audit
   does not settle the characteristic-zero count. The theorem, primary,
   audit, and uniquely consumed generator remain root `review_required` debt.
   No batch may freeze until an owner-authorized scientific reconciliation.
2. **P4 internal-`E=0` attribution conflict.** P4 toric-boundary prose assigns
   the earlier canonical theorem to internal `E=0`; P4 chart closure and the
   complete successor instead identify `D=0, a!=0` and treat internal `E=0`
   separately. Executable/hash replay cannot validate that prose edge.
3. **Broader first/second-component provenance conflict.** Several P4,
   marked-basis, toric, and internal-`E=0` artifacts retain open language,
   while the root README, high-coordinate frontier, and diagonal-quadric
   outer-boundary artifacts contain complete-closure language. Much of both
   sides entered in the same historical commit; recency does not adjudicate
   the conflict.
4. **Weighted-H22 `p+q=0` status conflict.** The migrated Stage 18 H31
   aggregate says weighted H22 remains open on the wall, while the dedicated
   H22 theorem and root README label the same diagonal-DVR wall `VERIFIED`.
   Reconciliation is owner-gated; unrelated migrations did not consume it.

Additional nonblocking provenance debt remains: Stage 19 navigation
understates construction copied by its modular audit, and the Stage 25/26
leaf-local `UNKNOWN` or generic-finite-false fields are chronological rather
than contradictions of the later ordinary-residual case-union theorem.
Candidate or partial providers and exact-Q audits remain construction or QA,
not generic theorem evidence.

## Cleanup boundary

The migration program deregistered the 20 clean, merged migration worktrees
identified by the cleanup audit. Nineteen directories are gone; the former
`stages17-19-program-audit` path remains only as an empty, unregistered
residual shell after a prior deletion attempt reportedly encountered an OS
lock. No Git worktree registration or research data remains there. Branch
refs were preserved.

The protected research/theorem worktrees were not modified or removed:

- `astra-math-transfer-review` at `a49b2a56`;
- `astra-math-transfers` at `a49b2a56`;
- `component20-special-h31` at `9720f102`; and
- `local-to-global-bottleneck` at `b6f24b57`.

The temporary worktree used to publish this handoff is also disposable after
its own clean merge. Unrelated worktrees and directories are outside this
program's cleanup authority.

## Throughput improvements for any future resumption

1. Enforce the three-stage program-audit cadence in CI before another batch
   can freeze.
2. Use one schema-aware replay harness with HEAD/tree/source guards, declared
   `uv` dependencies, environment preflight, root/foreign modes, immutable
   stdout/stderr/metadata hashes, and distinct tooling, environment, and
   scientific failure classes. Never auto-rerun a valid scientific row after
   a wrapper or post-parse failure.
3. Treat canonical mapping hashes and Git blob IDs as portable authority.
   Generate normalized and optional raw-CRLF provenance hashes mechanically.
4. Run semantic and mechanical referees concurrently, but serialize Singular,
   expensive solver rows, and cache-writing validation.
5. Generate stage reports and a machine-readable post-merge program ledger
   from frozen batches, Git objects, replay metadata, and CI metadata so final
   head/merge status cannot go stale.
6. When risk and replay closure permit, freeze two to four disjoint routine
   leaves in one exact stage. Preserve package-level mappings and evidence
   boundaries, deduplicate shared consumer replays, and keep root/foreign
   checks for moved executables.
7. Reuse content-addressed replay evidence only under ancestry, immutable
   source, dependency, environment, and schema guards.

The seven stages moved only 22 files, so orchestration and repeated review--not
the pure moves--dominated elapsed time. The improvements above target that
overhead without relaxing scientific or provenance gates.

## Durable resume boundary

Migration exploration is stopped after Stage 26. Do **not** begin Stage 27
from this handoff. If the repository owner later resumes the program, first:

1. confirm clean `main`, current merged-main CI, and protected-worktree state;
2. rerun or explicitly supersede this overdue audit checkpoint;
3. inventory the then-current `1,946` grandfathered root paths rather than
   assuming today's candidates remain valid;
4. keep all four owner-gated conflicts outside routine delegation unless a
   focused scientific review resolves them; and
5. start with a fresh bounded dry run and an exact frozen batch.

Until then, the authoritative state is: 411 executed moves, `1,946 / 0` root
debt, global Krenn-Gu status **UNRESOLVED**, and no Stage 27 authorization.
