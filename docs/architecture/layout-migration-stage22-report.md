# Layout migration Stage 22 report

Status: **SUBSTANTIVE MIGRATION COMPLETE ON BRANCH; AWAITING FINAL
EXACT-CANDIDATE REVIEW AND MERGE.**

The global Krenn-Gu conjecture remains **UNRESOLVED**. Stage 22 changes
filesystem ownership, replay paths, navigation, and mechanically derived hash
metadata. It does not promote a canonical marked-row section to a complete
marked fibre, a divisor result to a whole-component result, or any local
obstruction to `P5 -> Delta3` or the global conjecture.

## Exact reviewed transaction

- Merged baseline:
  `2040f9ff6ce077908eae83d3ce40e7cb8254fd39`.
- Branch: `codex/stage22-h31-component-chart-boundary-migration`.
- Dry-run approval commit:
  `5460a134ad8d618ad5c2d52d21eea58dc6acf29d`.
- Frozen-batch commit:
  `406c3bb8d3a4934f4cb199fbfb8a1db05df8f7c7`.
- Pure-move commit:
  `2eac482376c8047236f6ae53a4a74699c93def0b`.
- Package/path repair commit:
  `b267b097a51a6901facbec7d7a75d2e2269e7832`.
- Bootstrap-spacing normalization commit:
  `35697e22e5e7312f934fc7775df8386f80597c0a`.
- Substantive tree:
  `e116b077781d6da901005d5fcc2d073d1dc373ed`.
- Batch ID: `p5-h31-component-chart-boundary-stage22`.
- Mapping SHA-256:
  `7130acd031ab499906c6c463298292de459ce7a60eac566a35986d40d3763837`.
- Approval-time raw Windows-checkout manifest SHA-256:
  `bd9b23bc2dbe624f646c27d665394917ec6afc1ac8ad0c71eb9e92ad0c667d91`.
- Actual mapping reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.

The approval-manifest hash is platform-specific and informational. The
canonical mapping hash is the portable authority for the three old-to-new
pairs. The approved ownership analysis is recorded in
[`p5-h31-component-chart-boundary-stage22-dry-run.md`](p5-h31-component-chart-boundary-stage22-dry-run.md),
and the executable batch is frozen in
[`catalog/batches/p5-h31-component-chart-boundary-stage22.json`](../../catalog/batches/p5-h31-component-chart-boundary-stage22.json).

## Moved proof-obligation boundary

The exact theorem/primary/audit triple moved flat into
`claims/p5/h31/component-chart-boundary/`:

1. `P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md`;
2. `verify_p5_h31_component_chart_boundary.py`; and
3. `audit_p5_h31_component_chart_boundary.py`.

The selected claim is an exact characteristic-zero obstruction for the
displayed canonical marked-row normal form on the nonzero all-rank-two
preferred-chart divisor of the first known pure-rank-two component. Its
parameters satisfy `A H N != 0`, `R` is arbitrary, and it covers the four
distinguished-source orientations `q=0,1,2,3`.

Its exact boundary is:

```text
first known pure-rank-two component
  -> nonzero preferred-chart divisor
  -> displayed canonical marked-row normal form, A H N != 0, R arbitrary
  -> all q=0,1,2,3 distinguished-source orientations
  -> exact rank, collision, and R=0 degeneracy checks over characteristic 0
  => those four canonical marked sections are excluded

arbitrary kernel-row shifts, the complete marked-basis fibre, first-plane
infinity, internal E=0, toric/projective interior, second/further components,
H22, P5 -> Delta3, gluing, and global remain outside this leaf
```

The primary is the characteristic-zero proof replay. The audit imports no
primary or scientific/computational repository helper; its only repository
import is the path-only shared `krenn_gu.bootstrap`. It separately implements
dynamic-programming permanents and modular row reduction over `F5/F7`. Its
exhaustive modular census is QA only, not the characteristic-zero proof.

The later complete chart-boundary marked-fibre theorem, primary, audit, and
uniquely consumed elimination generator remain together at repository root
as a distinct successor obligation. Stage 22 neither absorbs nor supersedes
that four-file family. No selected artifact has a curated theorem-ledger
entry, and Stage 22 creates none.

## Preserved scientific conflicts

The P4 toric-boundary prose attributes an internal `E=0` canonical section
to the selected theorem. The P4 chart-closure source identifies the selected
divisor as `D=0, a!=0`, while the later complete marked-fibre theorem treats
internal `E=0` separately. Stage 22 preserves and retargets the P4 link but
does not infer an equivalence, endorse either attribution, or adjudicate the
conflict. Replaying the P4 executable verifies its current hashes and
calculation; it cannot validate that prose edge.

The broader first/second-component status-provenance conflict likewise
remains unconsumed. Any scientific correction to either conflict is a
separate owner-gated status audit, not a layout-migration edit.

## Pure move and mechanical repairs

The pure transaction consists of exactly three `R100` moves plus the
corresponding manifest update. Each source, destination, and working-tree
blob is identical across that commit. The manifest changes only the three
selected records from `review_required` to `moved`, adds their exact
`executed_batch`, and updates deterministic summary fields:

- moved: `395 -> 398`;
- review-required: `1,378 -> 1,375`;
- proposed-high-confidence: `242` unchanged;
- moved-only projection: `1,977 -> 1,974`;
- moved-plus-high-confidence projection: `1,735 -> 1,732`; and
- all-classified projection: `357` unchanged.

After the move, both selected executables use the shared
`krenn_gu.bootstrap` machinery. Package-local theorem/primary paths resolve
through `HERE`; upstream P4/root evidence and ignored `tmp/` output resolve
through `REPO_ROOT`. Exactly four staying primaries retarget their selected
theorem dependency:

1. the P4 toric-boundary verifier;
2. the complete chart-boundary marked-fibre verifier;
3. the canonical first-plane-infinity verifier; and
4. the high-coordinate frontier verifier.

The deterministic rewriter changed exactly eight Markdown links and two
fenced replay commands across five Markdown files, with no ambiguity and no
ledger relocation. The second pass is a fixed point. Navigation now records
29 H31 package directories and labels this package as a canonical-section
divisor leaf, never as generic, complete-marked-fibre, whole-component, or
component-closure evidence.

The theorem ledger changes exactly four `document_sha256_16` values:

- the verified high-coordinate entry now uses `bc51eb1ed19d017e`; and
- the three README-backed entries now use `25c075592c445ed6`.

Their statuses remain `verified`, `open`, `verified_generic`, and `partial`,
respectively. Every other ledger field is unchanged.

## Scientific replay matrix

The full recursive path/hash-consumer closure is 16 unique executables and
22 invocations. Every invocation ran exactly once and strictly serially via
`uv run --quiet --python 3.13 --with sympy --with python-sat python`. Every
run returned rc=0, empty stderr, and one valid JSON object.

The six directly affected executables ran once from repository root and once
by absolute path from a fresh foreign working directory:

| executable | root s | foreign s | result |
|---|---:|---:|---|
| canonical primary | 9.056 | 3.046 | exact characteristic-zero canonical-section obstruction; conservative H31/P5/global false |
| canonical modular audit | 39.262 | 39.315 | `F5/F7` QA; no primary imports |
| P4 toric-boundary primary | 1.026 | 1.025 | 44 pairs = 21 gate-excluded + 23 all-rank; H31/P5/global false |
| complete chart-boundary marked-fibre primary | 15.124 | 13.117 | complete divisor fibre true; projective/internal/additional/global false |
| canonical first-plane-infinity primary | 4.054 | 3.023 | four orientations excluded; whole-H31/P5/global false |
| high-coordinate primary | 2.037 | 2.025 | census 6,495 / 1,680 / 1,170 / 510; P5/global false |

Five pairs are byte-identical. The complete marked-fibre objects are exactly
equal after removing only their measured `elapsed_seconds` values (12.517
versus 10.763). All six foreign directories remained empty.

The ten root-only closure consumers also passed:

| executable | elapsed s | preserved boundary |
|---|---:|---|
| P4 toric-boundary audit | 1.014 | independent 28-point/12-facet and 21/23 split |
| complete chart-boundary marked-fibre audit | 2.017 | four orientations; 614 projection points and 5,400 extensions; modular QA only |
| canonical first-plane-infinity audit | 96.680 | `F5`: 1,920/17,408/17,408/0; `F7`: 12,096/160,704/160,704/0 |
| high-coordinate audit | 4.044 | census unchanged; P5/global false |
| P4 toric-slice Segre primary | 2.025 | orbit counts 12/26/16 and remaining pairs 13+8=21; global false |
| H31 toric marked-fibre primary | 229.683 | 17 directions, 39 orientation types, 21 cases, 78+78 runs, 18 binary-empty, 438 products; global false |
| H31 internal-`E=0` marked-fibre primary | 99.689 | 12 runs, 24 components, 29 charts, coupled unit ideal; additional/global false |
| H22 mask-6 independent audit | 2.028 | `VERIFIED`, all 12 scoped flags obstructed; global false |
| component-19 `phi=+/-1` derivation | 14.106 | remains `CANDIDATE`; global not promoted |
| component-19 `qphi=-1` axes derivation | 4.061 | remains `CANDIDATE`; actual lift false |

Every emitted theorem, primary, source, dependency, input, and output SHA-256
resolved uniquely to and matched current tracked bytes. Exactly nine
generated repository-`tmp/` JSON files parse-match their preserved captures
and remain ignored; seven executables are stdout-only; none writes tracked
output. Both isolated foreign-CWD moved-module import probes returned
`IMPORT_OK` with rc=0 and empty stderr. The final tracked and nonignored
worktree remained clean.

Replay captures and their SHA manifest are preserved outside the repository
at
`C:\Users\Yeste\.codex\run-artifacts\stage22-acceptance-35697e2-20260809T104345Z`.
Native Windows Singular was absent. The complete marked-fibre root/foreign
runs, toric marked-fibre run, and internal-`E=0` run used the shared WSL
`/usr/bin/timeout` plus `/usr/bin/Singular` route; the component-19
`phi=+/-1` run used its separate WSL Singular fallback guarded by Python's
120-second subprocess timeout. All passed; no timeout, failure, wrapper
error, or automatic rerun was treated as theorem evidence.

## Validation and publication boundary

At substantive head `35697e22e5e7312f934fc7775df8386f80597c0a`,
the index-complete validation floor passed:

- `check_hygiene.py`: 1,698 Python files compile, all 817 pre-report Markdown
  files have resolving local links, all 86 ledger hashes match, root is 1,966
  files + 9 directories = 1,975 entries, root debt is
  `1,959 grandfathered / 0 new`, and all 398 retired-path/provenance records
  pass;
- all 152 migration-tool tests;
- all 14 fourteen-vertex cycle-cover lattice tests;
- deterministic rewriter fixed point;
- targeted Ruff fatal/error checks and byte compilation for all six directly
  affected Python files;
- two isolated moved-module foreign-CWD import probes; and
- clean index/worktree diff checks.

Workflow-dispatch run
[`31309927203`](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31309927203)
passed at the exact substantive head, including hygiene, migration tests, the
self-contained lattice module, and rewriter closure.

Adding this report raises the final Markdown count to 818. The final
documentation candidate must rerun the complete index floor, receive fresh
Tier-2 semantic/status and mechanical/provenance/bypass referee passes, and
pass exact-head pull-request CI before a normal guarded merge.

## Stop boundary

Stage 22 stops at the displayed canonical marked-row sections on one nonzero
preferred-chart divisor. The later complete marked-fibre successor remains a
separate four-file proof leaf. First-plane infinity, internal `E=0`, the
toric/projective interior, later components, component exhaustiveness,
weighted `H22`, `P5 -> Delta3`, local-to-global gluing, and global resolution
remain separately owned. The global Krenn-Gu conjecture remains
**UNRESOLVED**.
