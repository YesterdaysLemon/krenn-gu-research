# Layout migration Stages 17-19 program audit

Status: **PASS WITH NON-BLOCKING GOVERNANCE AND SCIENTIFIC-PROVENANCE
DEBT.** No defect in Stages 17, 18, or 19 blocks unrelated continued layout
migration.

The global Krenn-Gu conjecture remains **UNRESOLVED**. This is a read-only
program audit of three merged layout stages. It does not promote a claim,
choose between conflicting scientific artifacts, change an evidence status,
or authorize status-consuming use of a disputed statement.

## Audit boundary and method

- Pre-Stage-17 merged baseline:
  `7873c2026423af32dea6055fdee557ceebfcbe20`.
- Audited merged main:
  `e6de41759c35ba6f267953723dbbc72480e69003`.
- Audited stages:
  - Stage 17: complete H31 rank-one-gate obstruction forest;
  - Stage 18: complete diagonal-source-torus `p+q=0` marked-H31 wall; and
  - Stage 19: internal-`E=0` marked-H31 divisor leaf.

Independent read-only mechanical/governance and semantic/status passes
reconstructed Git/PR lineage, frozen mappings, pure moves, manifest and root
arithmetic, path repairs, ledger changes, navigation, proof-obligation
topology, audit-independence claims, status boundaries, CI, and current
hygiene. A separate serial hygiene replay closed an overlapping Windows
`__pycache__` atomic-write race; the race was validation-process contention,
not a repository failure.

## Exact lineage and frozen transactions

| stage | PR | base | final branch head | merge | reviewed/merged tree | batch members |
|---|---:|---|---|---|---|---:|
| 17 | [#48](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/pull/48) | `7873c202` | `3678a96e` | `fb87d7c3` | `6c399aa068fee7710aa0aad6bcc31d2a32ef29e9` | 9 |
| 18 | [#49](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/pull/49) | `fb87d7c3` | `c9cfe526` | `d7433d7a` | `503574915f1e797a5823e8fa33afea48366b5847` | 9 |
| 19 | [#50](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/pull/50) | `d7433d7a` | `6e51d36b` | `e6de4175` | `309352bcbd0d90e0197ae25865f3cb39c20ec30d` | 3 |

Every merge has exactly the expected base and reviewed-head parents, and
every merge tree equals its reviewed branch-head tree. The three branch
histories are each linear five-commit sequences: exact dry-run approval,
frozen batch, pure move, mechanical repair, and final report.

All three batch Git blobs are unchanged from their freeze commits. Their
canonical mapping hashes independently reproduce:

| stage | batch | mapping SHA-256 |
|---|---|---|
| 17 | `p5-h31-single-gate-stage17` | `7525f91818132db42c0104a366f873441118befe50c0ffcf9d676fe1c765c6a0` |
| 18 | `p5-h31-common-active-p-plus-q-stage18` | `7595460669d3e45b4a5c12924f846d02e3dddf36385822a577b2826aebcb04d9` |
| 19 | `p5-h31-internal-e0-stage19` | `0a345a2e89974d1e7f8b026cd568d1da6ecec62b0337412b9cc9a35c7edecd6a` |

Each batch names Codex as the actual reviewer under the repository-owner
standing delegation dated 2026-08-08. Current batch/manifest validation and
executed-provenance validation report zero problems. The recorded
approval-manifest hashes match the raw CRLF approval checkouts and are
correctly described as informational; the canonical mapping hashes are the
portable mapping authority.

## Pure-move and root-exit accounting

The three pure commits contain exactly 9 + 9 + 3 `R100` moves and one
`catalog/moved-paths.json` transaction apiece. Every destination blob equals
its source-parent blob. No theorem statement, proof computation, or status
changed in a pure move.

Manifest transitions are exact:

- Stage 17: nine `review_required -> moved` records;
- Stage 18: three `proposed_high_confidence -> moved` and six
  `review_required -> moved` records; and
- Stage 19: three `review_required -> moved` records.

Every unselected record and non-count manifest field is invariant. Final
counts are `moved=389`, `proposed_high_confidence=243`, and
`review_required=1383`, with zero collisions, double moves, or overlap
cycles.

| boundary | root files | root dirs | grandfathered debt | retired paths |
|---|---:|---:|---:|---:|
| before Stage 17 | 1,996 | 9 | 1,989 | 368 |
| after Stage 17 | 1,987 | 9 | 1,980 | 377 |
| after Stage 18 | 1,978 | 9 | 1,971 | 386 |
| after Stage 19 | 1,975 | 9 | 1,968 | 389 |

The program removes 21 grandfathered root paths, creates no new root debt or
top-level directory, and leaves the frozen root universe, end-state
allowlist, classifier, contracts, migration tooling, tests, and workflow
unchanged.

## Scientific and evidence-semantics invariants

No cross-stage ownership collision or silent scope promotion was found:

- Stage 17 exhausts only the stated rank-one-gate dichotomy. Its P3 result
  remains a reduction, the two children remain characteristic-zero
  obstructions, and the all-rank-two/global branches remain open.
- Stage 18 closes only the stated diagonal-source-torus `p+q=0` marked-H31
  wall. Its P4 arc and embedded-P3 inputs remain separately owned, and the
  other 12 common-active files remain separate.
- Stage 19 closes only the internal-`E=0` marked-H31 divisor leaf. It remains
  non-generic and is not a whole-component theorem.

Audit independence is represented accurately. Stage 17's later modular
audits share helpers from its P3 audit; Stage 18's infinity pair shares the
marked-matrix construction; and Stage 19's `F5/F7` audit is independent only
downstream of shared toric-case/marked-row construction and copied projection
data. Every finite-field audit remains QA rather than a characteristic-zero
proof.

Across all 86 theorem-ledger entries, only the mechanically recomputed hashes
of the three root-README entries and the high-coordinate frontier changed.
All statuses, assumptions, lifecycle fields, evidence roles, and dependency
semantics remain fixed. Ledger completeness remains `partial_curated`, and
`global_status` remains `UNRESOLVED`.

## Durable final-referee traceability

The individual stage reports were committed before their final merge-gate
reviews and therefore still describe final review as pending. GitHub has no
formal reviews or comments on PRs #48-#50. The task-history verdicts are
backfilled here against the exact trees they reviewed:

| stage | exact final tree | semantic/status referee | mechanical/bypass referee |
|---|---|---|---|
| 17 | `6c399aa068fee7710aa0aad6bcc31d2a32ef29e9` | PASS | PASS |
| 18 | `503574915f1e797a5823e8fa33afea48366b5847` | PASS WITH NON-BLOCKING pre-existing lifecycle prose debt | PASS |
| 19 | `309352bcbd0d90e0197ae25865f3cb39c20ec30d` | PASS | PASS after correcting the report aggregate from 76 to 438 selected products |

Future stages should make this trace durable before merge, either through a
final report-only update that records the exact reviewed tree and both
verdicts, followed by a lightweight superseding review, or through durable PR
comments that name the roles, exact tree, and verdicts.

## Validation and CI

Every substantive head, final PR head, and merged-main head passed the
repository workflow:

| stage | substantive | final PR | merged main |
|---|---|---|---|
| 17 | [31292423869](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31292423869) | [31292977118](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31292977118) | [31293012022](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31293012022) |
| 18 | [31294646401](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31294646401) | [31295177744](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31295177744) | [31295209576](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31295209576) |
| 19 | [31296961362](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31296961362) | [31297632794](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31297632794) | [31297667281](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31297667281) |

Current merged main independently passes hygiene: 1,698 Python files compile,
811 Markdown files have resolving links, all 86 ledger hashes match, root
debt is `1,968 grandfathered / 0 new`, all 389 retired-path/provenance records
pass, and all five fast verifiers pass.

## Non-blocking scientific-provenance debt

### Second-component H31 conflict

Open-language appears in:

- `claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_THEOREM.md`;
- `P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md`;
- `claims/p4/classifications/pair-geometry/pure-rank-two/boundaries/P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md`; and
- the moved internal-`E=0` theorem.

Complete-closure language appears in the root README, high-coordinate
frontier, and diagonal-quadric outer-boundary theorem. Much of both sides
originates in the same commit `60a885ca`; recency cannot adjudicate the
conflict. Stages 17 and 19 correctly report it and do not use the disputed
broader claim as a premise.

### Weighted-H22 status sentence in the Stage 18 aggregate

The moved H31 aggregate theorem
`claims/p5/h31/common-active-binary-triangle/P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md`
still says weighted H22 on that wall remains open. The dedicated root
`P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md` and
root README instead label that same diagonal-DVR wall `VERIFIED`. The Stage
18 report correctly treats H22 as separately verified, so this stale sentence
does not invalidate the H31 mapping. It remains a focused scientific-status
reconciliation obligation.

### Stage 19 navigation wording

`claims/p5/h31/README.md` identifies the Stage 19 audit's shared
toric/marked-row construction but omits that it also copies the displayed
projection equations. The Stage 19 report contains the full limitation, and
the README still labels the audit modular QA. This is nonblocking wording
debt, not an independence or status promotion.

These conflicts are owner-gated for status-consuming migration, proof-graph
use, or scientific prose harmonization. Unrelated filesystem migration may
continue. A mapping touching one of these families is routine only when its
ownership and status boundary can be established without choosing a side;
otherwise it must stop for focused provenance/evidence review.

## Replay-process hardening

The underlying Stage 17-19 executables passed their required matrices, but
ad hoc wrappers caused avoidable noise: Stage 18 initially asserted the wrong
nested field, while Stage 19 initially confused a program/category count with
the emitted 438-product aggregate and launched redundant expensive reruns.
One redundant Stage 19 worker then reached its time limit under contention.
None was mathematical evidence.

Future expensive replay plans should use a checked, schema-aware assertion
manifest and preserve the first rc=0, empty-stderr, valid-JSON result before
post-parse assertions. A wrapper mistake must not automatically trigger a
solver rerun or be described as a verifier failure.

## Program verdict

Stages 17-19 preserve exact mappings, proof-boundary ownership, evidence
roles, scientific statuses, and the root-debt ratchet. The identified debt is
explicit and nonblocking for unrelated layout work. The next stage may
proceed under the standing delegation only within a fresh bounded dry run and
must not consume either disputed scientific family without focused review.
The global Krenn-Gu conjecture remains **UNRESOLVED**.
