# Dry-run report: navigation-docs-phase2

Generated before execution, from the tree at base SHA
`081c54b1a344` (branch `layout-migration-phase2`).

Approval artifact: `catalog/batches/navigation-docs-phase2.json`
(`mapping_sha256 b981092ec090fca6…`).

## Mappings (8)

| old path | new path | inbound md links | outbound links | replay cmds | ledger entries |
|---|---|---|---|---|---|
| ASTRA_MATHEMATICS_TRANSFER_STRATEGY.md | docs/ASTRA_MATHEMATICS_TRANSFER_STRATEGY.md | 1 | 4 | 10 | 1 |
| CURRENT_FRONTIER.md | docs/current-frontier.md | 2 | 17 | 0 | 0 |
| LITERATURE_REVIEW_2026-07-30.md | docs/LITERATURE_REVIEW_2026-07-30.md | 0 | 60 | 0 | 0 |
| MERGE_AUDIT_REPORT.md | docs/audits/MERGE_AUDIT_REPORT.md | 3 | 0 | 0 | 0 |
| NEXT_INSTANCE_HANDOFF_2026-07-31.md | docs/NEXT_INSTANCE_HANDOFF_2026-07-31.md | 3 | 240 | 68 | 0 |
| RESEARCH_NOTES.md | docs/research-notes.md | 1 | 11 | 30 | 0 |
| STABILIZATION_AUDIT_REPORT.md | docs/audits/STABILIZATION_AUDIT_REPORT.md | 2 | 10 | 0 | 0 |
| SYMBOLIC_TRANSLATION_LITERATURE_FRONTIER_2026-08-02.md | docs/SYMBOLIC_TRANSLATION_LITERATURE_FRONTIER_2026-08-02.md | 1 | 0 | 0 | 1 |

## Collision status

None. All eight destinations are distinct and unoccupied.

## Affected ledger entries

Two entries reference moved documents and will have their `document`
paths repointed with recomputed committed-blob hashes:

- "Transfer track: root-of-unity selector, hafnian lift, quotient
  catalogue" (ASTRA_MATHEMATICS_TRANSFER_STRATEGY.md)
- "P6/P7 symbolic reductions (ARBITRARY_PERMANENT_* family)"
  (SYMBOLIC_TRANSLATION_LITERATURE_FRONTIER_2026-08-02.md)

## Affected Python imports

None (no Python module is moved). Two derive scripts read
`NEXT_INSTANCE_HANDOFF_2026-07-31.md` as an `INPUTS` member whose
SHA-256 is recorded in their output certificates:

- derive_p5_h22_component19_p0_ordinary_boundary_candidate.py
- derive_p5_h22_component19_p0_qphi_one_ordinary_obstruction_candidate.py

Their `INPUTS` path constants are updated in the reference-rewrite
commit. The certificate hash recorded by these scripts is computed at
run time against the file content, which is unchanged by the move, so
no mathematical content drifts.

## Affected replay commands

`RESEARCH_NOTES.md`, `NEXT_INSTANCE_HANDOFF_2026-07-31.md`, and
`ASTRA_MATHEMATICS_TRANSFER_STRATEGY.md` contain fenced `python …`
command lines. The migration-aware rewriter handles fenced replay
commands; after the rewrite pass a second rewriter run must report
zero changes (idempotency gate).

## Ambiguities

None. `SPARSE_RESULTANT_CORES_ATTACK_PLAN.md` and
`GRASSMANNIAN_PLUECKER_ATTACK_PLAN.md` were on the candidate list but
no longer exist on current main (stale classification entries), so
they were removed from the batch rather than guessed.

## Provenance expectations after execution

- the 8 manifest entries flip to `status: moved` with
  `executed_batch: navigation-docs-phase2`;
- stale-path enforcement gains 8 executed old paths (all root moves
  keeping their basename except CURRENT_FRONTIER.md and
  RESEARCH_NOTES.md, which are renamed by their destination);
- the hygiene provenance invariant requires every moved entry's batch
  file to freeze its exact mapping.
