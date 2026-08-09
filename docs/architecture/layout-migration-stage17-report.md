# Layout migration report — Stage 17 (H31 single-gate forest)

Status: **the exact Stage 17 migration transaction is complete locally and
ready for fresh Tier-2 merge-gate review.**  One coherent nine-file
rank-one-gate obstruction forest left repository root: an exact reduction and
its primary/audit, plus two complementary exact obstruction theorems and their
primaries/audits.

> **Scientific status did not change.**  The reduction remains a reduction,
> not an exclusion theorem.  The two characteristic-zero obstructions jointly
> exclude only H31 pure/Delta2 pencils having a rank-one row pair on the pure
> hyperplane.  The all-rank-two pure-P4 locus, all H31, all H22,
> `P5 -> Delta3`, and the global Krenn–Gu conjecture remain **UNRESOLVED**.

## Provenance anchors

- Exact merged baseline: `7873c2026423af32dea6055fdee557ceebfcbe20`.
- Branch: `codex/stage17-h31-single-gate-migration`.
- Exact-mapping approval commit:
  `36a9a885e7a1868a6f7d9c6fdce72d6f7ec7243a`.
- Frozen batch commit:
  `392bfd3aa7ccc8825f60ca8dd011520af9aed199`.
- Pure move commit:
  `ec1c0a78c3aefe6976e84affb8bb77807668292e`.
- Mechanical repair and substantive head:
  `78016cb7f630a28f7d98de62ac00f69e1d773b7e`.
- Exact dry run:
  [`p5-h31-single-gate-stage17-dry-run.md`](p5-h31-single-gate-stage17-dry-run.md).
- Frozen batch: `catalog/batches/p5-h31-single-gate-stage17.json`:
  - reviewer: `Codex (exact mapping reviewer under repository-owner standing
    delegation dated 2026-08-08)`;
  - base SHA: `7873c2026423af32dea6055fdee557ceebfcbe20`;
  - member count: 9;
  - canonical mapping SHA-256:
    `7525f91818132db42c0104a366f873441118befe50c0ffcf9d676fe1c765c6a0`;
  - informational raw Windows-checkout manifest SHA-256:
    `79a7b498cffcc338ede0ae0ba2528582a9a5eb1ceafa7920c2bda072005335bc`.
- Substantive-head workflow dispatch: run `31292423869`, exact head
  `78016cb7f630a28f7d98de62ac00f69e1d773b7e`, conclusion **success**.

Three independent read-only pre-execution audits reconstructed scientific
topology, evidence semantics, and mechanical/provenance geometry separately.
The semantic and mechanical audits passed the exact mapping.  The
evidence-semantics audit blocked one overbroad dry-run sentence, which was
corrected before approval: the P3 reduction applies only to the rank-two-M
case and does not itself split the entire gate branch.  A reread passed the
corrected report.  Classifier confidence remained proposal evidence only.

## Selected forest and proof boundary

The nine files moved into three sibling claim packages:

| case / role | package | document | primary | audit |
|---|---|---|---|---|
| rank-two-M line-arrangement reduction | `claims/p5/h31/single-gate-p3/` | `P5_H31_SINGLE_GATE_P3_REDUCTION.md` | exact SymPy replay | F5/F7 audit |
| rank-two-M ternary exclusion | `claims/p5/h31/single-gate-rank-two-m-exclusion/` | `P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md` | exact SymPy replay | F5/F7 audit |
| further-rank-drop exclusion | `claims/p5/h31/secondary-gate-exclusion/` | `P5_H31_SECONDARY_GATE_EXCLUSION.md` | exact SymPy replay | F5/F7 audit |

The proof-obligation topology is:

```text
rank-one row pair on the pure hyperplane
  + other three row pairs rank two on M
      -> exact P3/line-arrangement reduction
      -> exact rank-two-M ternary exclusion
  + at least one further rank drop on M
      -> unique secondary gate
      -> exhaustive pair-image support split
      -> exact secondary-gate exclusion
  => every rank-one-pair pure-hyperplane H31 pencil is excluded

all-rank-two pure-P4 H31, all H31, P5 -> Delta3, and global stay open
```

No additional tracked single-gate or secondary-gate claim artifact exists.
The root `P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION` triple remains a shared
upstream owner.  The P4 toric-boundary package, high-coordinate frontier,
Delta3 ledger, component atlas, root README, and research notes are downstream
consumers or navigation/provenance rather than members of this obligation.

Evidence roles remain distinct:

- all three primary verifiers replay exact characteristic-zero identities
  supporting the written proofs over C;
- each F5/F7 audit independently reimplements the calculations of its
  corresponding symbolic primary at the modular arithmetic and row-reduction
  layer and imports no primary verifier;
- the rank-two-M and secondary audits reuse helpers from the P3 audit, so the
  three audits are not mutually no-import independent; and
- every audit explicitly reports
  `finite_field_audit_is_characteristic_zero_proof: false`.

No curated theorem-ledger entry names these three documents.  Stage 17 added
no ledger entry and changed no existing status, assumption, provenance, note,
or global-status field.

## Pure-move acceptance

Against the pure move commit's direct parent:

- all nine exact sources are absent and all nine destinations are present;
- every destination Git blob equals its source-parent blob recorded in the
  dry run;
- Git records all nine moves as `R100`;
- the only non-rename change is the deterministic manifest transaction;
- every selected manifest record is `moved` and names
  `p5-h31-single-gate-stage17` as `executed_batch`; and
- no theorem prose, assertion, algebra, or executable content changed.

Observed arithmetic:

| measure | before | after |
|---|---:|---:|
| manifest `moved` | 368 | 377 |
| manifest `proposed_high_confidence` | 246 | 246 |
| manifest `review_required` | 1,401 | 1,392 |
| moved-only manifest root projection | 2,004 | 1,995 |
| high-confidence manifest root projection | 1,758 | 1,749 |
| all-classified manifest root projection | 357 | 357 |
| measured root files | 1,996 | 1,987 |
| measured root directories | 9 | 9 |
| measured root entries | 2,005 | 1,996 |
| grandfathered root debt | 1,989 | 1,980 |
| enforceable retired paths | 368 | 377 |

There are zero new root-debt paths, destination collisions, double moves, or
overlap cycles.  The frozen root baseline and end-state allowlist did not
change.

## Mechanical repair

The migration rewriter made exactly 12 Markdown-link rewrites and six fenced
replay-command rewrites across six Markdown files, with zero ambiguities and
zero theorem-ledger relocations.  Its second pass was a fixed point.

Explicit repair then:

- installed shared bootstrap in all six moved executables;
- used package-local `HERE` for each owned theorem and repository `tmp/` for
  ignored replay output;
- kept the P3 classification at its root owner and used full repository paths
  for the moved cross-package reduction, audit, and theorem dependencies;
- exposed `single-gate-p3/` through
  `krenn_gu.bootstrap.expose_claim_package` before the two cross-package audit
  imports, with no one-off path shim;
- repaired the P4 toric-boundary consumer and both single-gate paths in the
  high-coordinate consumer;
- added the three-package rank-one-gate forest to P5/H31 navigation while
  retaining embedded-P3 as the sole complete component-closure forest; and
- refreshed only four existing ledger document hashes after deterministic
  link rewrites changed `README.md` and
  `P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`.

Ruff and byte compilation pass for all eight affected executables.  No
scientific assertion, theorem body, evidence status, or global-resolution
field changed.

## Exact moved-script replay

Each moved executable ran once from repository root by relative destination
path and once from a fresh foreign working directory by absolute path under
Python 3.13.14 and SymPy 1.14.0.  Each run emitted one JSON object; every
root/foreign pair was exactly equal.

| family | primary root / foreign | audit root / foreign | required result |
|---|---:|---:|---|
| P3 reduction | 1.439 / 1.470 s | 2.956 / 2.980 s | reduction verified; H31/P5/global false |
| rank-two-M | 1.216 / 1.196 s | 53.699 / 52.140 s | lift impossible; all-single/H31/P5/global false |
| secondary gate | 1.901 / 1.917 s | 30.200 / 30.582 s | all-single true; all-rank-two/H31/P5/global false |

All six report `verified: true`.  The three audits retain the explicit
not-characteristic-zero-proof field as false.

## Staying-consumer replay

Both staying consumers also ran from repository root and a foreign working
directory with exactly equal parsed JSON:

| consumer | root / foreign | preserved boundary |
|---|---:|---|
| `verify_p5_high_coordinate_partial_frontier.py` | 0.588 / 0.577 s | verified; `P5_to_Delta3_resolved=false`; global false |
| P4 pure-rank-two toric-boundary verifier | 0.237 / 0.224 s | P4 boundary verified; H31/P5/global false |

Replays created no tracked output change.  Isolated foreign-CWD import probes
for all eight affected executables passed 8/8 under
`uv run --with sympy python -I`.  A plain `python -I` probe correctly lacked
user-site SymPy and was replaced by the declared dependency environment; that
environment-only failure required no code change.

## Recorded nonblocking provenance conflict

The staying P4 pure-rank-two component theorem still describes the second
diagonal-quadric generic and boundary fibres as open, while later frontier and
navigation documents describe later closures.  This pre-existing conflict is
outside the single-gate forest.  Stage 17 records it without silently deciding
which scientific provenance is authoritative; a separate focused audit is
required.

## Validation floor

The clean substantive head passes:

- substantive-head workflow dispatch `31292423869` at exact SHA
  `78016cb7f630a28f7d98de62ac00f69e1d773b7e`;
- `check_hygiene.py`: 1,698 Python files compile, all 806 Markdown files have
  resolving local links, all 86 ledger hashes match, root debt is
  `1,980 grandfathered / 0 new`, and all 377 stale-path/provenance records
  pass;
- all 152 migration-tool tests;
- all 14 fourteen-vertex cycle-cover lattice tests;
- Ruff and byte compilation for all eight affected executables;
- 12 moved-script semantic replays, four staying-consumer semantic replays,
  and eight isolated imports;
- migration-rewriter fixed point; and
- clean staged, working-tree, and candidate-index checks.

## Merge gate and stop condition

This Tier-2 migration requires two fresh read-only exact-candidate referees:
one semantic/status review and one mechanical/bypass review.  It also requires
final-head PR CI, a fresh merge base, no consequential unresolved review, and
a normal exact-head merge.

This stage stops at the complete rank-one-gate obstruction forest.  It does
not move the upstream P3 classification, the all-rank-two component forest,
the high-coordinate synthesis, any H22 programme, or the recorded
diagonal-quadric provenance conflict.  The global Krenn–Gu conjecture remains
**UNRESOLVED**.
