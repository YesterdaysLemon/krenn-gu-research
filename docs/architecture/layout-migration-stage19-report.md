# Layout migration Stage 19 report

Status: **SUBSTANTIVE MIGRATION COMPLETE ON BRANCH; AWAITING FINAL
EXACT-CANDIDATE REVIEW AND MERGE.**

The global Krenn-Gu conjecture remains **UNRESOLVED**. Stage 19 changes
filesystem ownership, replay paths, navigation, and mechanically derived
hash metadata only. It does not promote a claim, extend the internal-divisor
theorem to another divisor or component, close weighted `H22`, prove
component exhaustiveness or `P5 -> Delta3`, or turn modular corroboration
into the characteristic-zero proof.

## Exact reviewed transaction

- Merged baseline:
  `d7433d7aad1fb6fa0ae26d711b93c8fd54ee80aa`.
- Branch: `codex/stage19-h31-internal-e0-migration`.
- Dry-run approval commit:
  `39e64eb3c340445702ef7257c83de42517003193`.
- Frozen-batch commit:
  `15eaf05d165a3e30adc980e8c3a6346017df46f5`.
- Pure-move commit:
  `b2c27889bde2a92c15a0b2df99cc479e0fd8ba6f`.
- Substantive repair commit:
  `d36180c0a35c6ad0603c40511a6a0a478013e53a`.
- Substantive tree:
  `91daf3ef8ed28467c36282c28722e5741ec9db40`.
- Batch ID: `p5-h31-internal-e0-stage19`.
- Mapping SHA-256:
  `0a345a2e89974d1e7f8b026cd568d1da6ecec62b0337412b9cc9a35c7edecd6a`.
- Approval-time raw Windows-checkout manifest SHA-256:
  `823a73851bc880704a392ebc279cffb21f552ebe1b945dd73e731e9485879adc`.
- Actual mapping reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.

The approval-manifest hash is platform-specific and informational. The
canonical mapping hash is the portable authority for the three old-to-new
pairs. The approved ownership analysis is recorded in
[`p5-h31-internal-e0-stage19-dry-run.md`](p5-h31-internal-e0-stage19-dry-run.md),
and the executable batch is frozen in
[`catalog/batches/p5-h31-internal-e0-stage19.json`](../../catalog/batches/p5-h31-internal-e0-stage19.json).

## Moved proof-obligation boundary

The exact theorem/primary/audit triple moved flat to
`claims/p5/h31/internal-e0-marked-fibre/`:

1. `P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md`;
2. `verify_p5_h31_internal_e0_marked_fibre.py`; and
3. `audit_p5_h31_internal_e0_marked_fibre.py`.

Its ownership topology is:

```text
P4 pure-rank-two toric facet + Segre slice reduction (stay P4-owned)
  -> internal E=0 facet of the first pure-compression component
  -> 2 reduced Segre directions x q in {0,2,3} x 2 first-plane charts
  -> 12 exact saturated projections and 24 projection components
  -> 29-chart exact atlas: 27 ordinary residual charts,
     one closure-artifact chart, and one coupled selected-minor unit ideal
  => every marked H31 fibre on this internal divisor is excluded

other divisor/component families stay separately owned;
weighted H22, broader unclosed boundaries/exhaustiveness,
P5 -> Delta3, gluing, and global remain open as stated by their owners
```

The characteristic-zero primary covers every marking on this one divisor:
both pure directions, all three all-rank distinguished coordinates, both
projective first-plane charts, every kernel-row shift, and every genuine
binary extension direction. It is neither a generic result nor a complete
component package.

Evidence roles remain distinct:

- the theorem and primary own the exact characteristic-zero obstruction;
- the primary reconstructs all 12 projections and the 29-chart atlas,
  including the closure-artifact and coupled-unit-ideal charts;
- the `F5/F7` audit does not import the primary and independently implements
  its modular kernel, projective-extension, and selected-minor route;
- the audit nevertheless shares `toric_cases` / `marked_rows` and copied
  projection data, so independence is claimed only downstream of that
  shared construction layer; and
- finite-field enumeration is QA, not the characteristic-zero proof.

No selected artifact has a curated theorem-ledger entry. Stage 19 adds no
entry and changes no mathematical status, assumption, scope, evidence role,
lifecycle, or global-status field.

## Explicit exclusions and pre-existing status-provenance conflict

Stage 19 does not move or decide:

- the shared toric generator, high-coordinate tree helper, marked-basis
  constructors, solver wrapper, or modular helper modules;
- the P4 toric-boundary theorem and Segre reduction;
- the finite-family, nonzero-chart, infinity, toric-boundary, or rank-one-gate
  siblings of the first H31 component;
- the diagonal-quadric or later-component families;
- weighted `H22`, component exhaustiveness beyond separately proved
  statements, `P5 -> Delta3`, arbitrary-order gluing, or the global
  conjecture.

The selected theorem and marked-basis classification contain older prose
saying that only one rational marked fibre on the second component had been
excluded. The P4 toric-boundary theorem likewise leaves that component's
generic marked fibre and further-component existence open. The
high-coordinate frontier, root README, and diagonal-quadric outer-boundary
closure instead record complete second-component marked-H31 closure. This is
a pre-existing status/provenance conflict outside the internal-`E=0`
theorem's scope.

Stage 19 does not adjudicate those artifacts by recency, reopen or promote
either statement, or use the disputed prose as a premise. The pure move
preserved the selected theorem blob exactly; the later theorem-document hunk
changes only a link and replay commands. Focused scientific-status review,
not layout migration, owns final conflict adjudication. The primary's
`additional_components_closed: false` remains scope-local: this verifier
proves no additional-component result.

## Pure-move acceptance

Against the pure-move commit's direct parent:

- exactly three source paths disappear and three destinations appear;
- all three moves are `R100`, and every destination Git blob equals the
  source-parent blob frozen by the batch;
- the only non-rename change is `catalog/moved-paths.json`;
- exactly the three selected `review_required` records become `moved` and
  gain `executed_batch: p5-h31-internal-e0-stage19`;
- no other manifest record or non-count metadata changes; and
- collision, double-move, and overlap-cycle counts remain zero.

The frozen source blobs are:

| artifact | Git blob |
|---|---|
| theorem | `1168bd201c15a3fa2db07f5dd09a4890d4bbb6cd` |
| modular audit | `abc0caadc2f10eb572b835684e96ec1def4e6db7` |
| characteristic-zero primary | `dd97026693496cf3c28ba926c3fe1e31681588f8` |

Observed arithmetic:

| measure | before | after |
|---|---:|---:|
| manifest `moved` | 386 | 389 |
| manifest `proposed_high_confidence` | 243 | 243 |
| manifest `review_required` | 1,386 | 1,383 |
| moved-only manifest root projection | 1,986 | 1,983 |
| high-confidence manifest root projection | 1,743 | 1,740 |
| all-classified manifest root projection | 357 | 357 |
| measured root files | 1,978 | 1,975 |
| measured root directories | 9 | 9 |
| measured root entries | 1,987 | 1,984 |
| grandfathered root debt | 1,971 | 1,968 |
| enforceable retired paths | 386 | 389 |

There are zero new root-debt paths. The frozen root baseline and end-state
allowlist are unchanged.

## Mechanical repair

Both moved executables now install the shared `krenn_gu.bootstrap` machinery
before any root-helper import. Package-owned theorem and primary paths use
`HERE`; the P4 inputs, shared generator, and root imports use `REPO_ROOT`.
The staying `verify_p5_high_coordinate_partial_frontier.py` received the
single required dependency-path retarget. No staying module imports or
subprocess callers required repair.

The deterministic rewriter made exactly seven Markdown-link changes and two
fenced replay-command changes across six Markdown files, with zero
ambiguities and zero ledger relocations. Its second pass is a `0/0/0` fixed
point. Navigation records 27 H31 package directories and labels this package
as divisor-scoped, non-generic, and not a complete-component package.

Four existing ledger hashes changed mechanically while every status and
other semantic field remained fixed:

- the three root-README entries changed from `2d2c48d2364b4b34` to
  `0a2bdc3d8f298425`; and
- the verified high-coordinate frontier entry changed from
  `a254bb28a2f2440c` to `438f42c953f13628`.

The rewriter also changed links in the P4 toric-boundary theorem,
marked-basis classification, and high-coordinate frontier. Their executable
hash consumers were therefore included in the replay matrix even where no
Python path changed.

## Exact committed-head replay

The two moved executables and the directly edited high-coordinate primary
ran from repository root by relative path and from a fresh foreign working
directory by absolute path at exact substantive head
`d36180c0a35c6ad0603c40511a6a0a478013e53a`. Each emitted one JSON object and
empty stderr. The moved primary pairs agree after removing only its volatile
`elapsed_seconds`; the audit and high-coordinate pairs agree exactly.

| executable | root | foreign | preserved result |
|---|---:|---:|---|
| internal-`E=0` primary | 104.444 s | 96.618 s | 12 projections, 24 components, 29 charts, coupled unit ideal true; known divisor true; additional/global false |
| internal-`E=0` modular audit | 30.334 s | 31.256 s | `F5/F7`, 3,976 points, 58,280 extensions, 747,552 minor tests; known divisor true; global false |
| high-coordinate primary | 0.785 s | 0.818 s | internal `E=0`, first component, and second component true; `P5 -> Delta3`/global false |

Ten additional hash/provenance consumers replayed semantically from root:

| executable | runtime | preserved result |
|---|---:|---|
| P4 toric-boundary primary | 0.407 s | verified; 21 gate-excluded / 23 all-rank; H31/P5/global false |
| P4 toric-boundary independent audit | 0.371 s | independent replay; same 21/23 split |
| P4 toric-slice Segre verifier | 1.426 s | 21 residual orientation pairs; H31/P5/global false |
| H31 toric marked-fibre primary | 154.1 s | 17 direction types, 39 orientation types, 78 projection and 78 selected-obstruction runs, 18 binary-empty runs, 438 products; genuine toric fibre true; other boundaries/components/global false |
| marked-basis classification primary | 15.116 s | verified; finite known-family fibre true; projective/additional/global false |
| marked-basis no-import audit | 2.835 s | `F5/F7`, 426 markings, 6,234 directions, 4,498 extensions, 32 closure artifacts rejected |
| high-coordinate independent audit | 3.546 s | 6,495 catalogue / 1,680 high / 1,170 excluded / 510 frontier; P5/global false |
| H22 mask-6 independent audit | 1.082 s | all 12 actual diagonal-DVR wall flags obstructed; exact scoped status `VERIFIED`; global false |
| component-19 `phi=+/-1` derivation | 14.963 s | exact open-domain checks pass; result remains `CANDIDATE`; global excluded |
| component-19 `q phi=-1` axes derivation | 3.670 s | two axes and higher obstruction true; actual lift false; result remains `CANDIDATE` |

All expected theorem/dependency hash changes propagated consistently; every
executable blob in the ten-consumer set remained unchanged. Tracked
certificate hashes remain historical provenance and were not rewritten.
Replays left no tracked or staged drift.

The complete H31 toric replay above returned rc=0, empty stderr, and valid
JSON before a post-parse wrapper rejected an incorrect provisional
`binary_empty == 78` assertion. Source and emitted tables give the correct
split `18` binary-empty / `438` selected products. A later redundant wrapper
run under concurrent load reached one worker's 240-second limit, and a
separate redundant outer harness also exceeded its deadline. Those are run
outcomes, not contrary evidence; they neither replace nor negate the
successful complete replay. Exact process checks left no replay, WSL, or
Singular workers alive.

Native Singular is absent. The existing WSL Singular 4.3.2 fallback passed
the exact eliminations. `python-sat` is required by the shared marked-basis
surface; both moved modules pass isolated foreign-CWD imports under
`uv run --with sympy --with python-sat python -I`.

## Validation and publication boundary

The clean substantive head passes:

- workflow-dispatch hygiene run
  [31296961362](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31296961362)
  at the exact substantive SHA, including every repository job;
- `check_hygiene.py`: 1,698 Python files compile, all 810 pre-report Markdown
  files have resolving local links, all 86 ledger hashes match, root debt is
  `1,968 grandfathered / 0 new`, and all 389 retired-path/provenance records
  pass;
- all 152 migration-tool tests;
- all 14 fourteen-vertex cycle-cover lattice tests;
- targeted Ruff fatal/error checks and byte compilation for the three
  directly affected Python files;
- the complete 13-executable replay matrix and three root/foreign pairs;
- two isolated moved-module import probes;
- rewriter fixed point; and
- clean index/worktree diff checks.

Adding this report raises the final Markdown count from 810 to 811. The final
documentation candidate must rerun the index-complete floor, receive fresh
Tier-2 semantic/status and mechanical/bypass referee passes, and pass final
exact-head PR CI before a normal guarded merge.

## Stop boundary

Stage 19 stops at the exact internal-`E=0` marked-H31 divisor leaf of the
first pure-compression component. Other divisors and components remain
separately owned; the older-versus-later second-component prose conflict
remains an explicit focused-audit obligation. Weighted `H22`, broader
component exhaustiveness, `P5 -> Delta3`, local-to-global gluing, and all
global work remain separate. The global Krenn-Gu conjecture remains
**UNRESOLVED**.
