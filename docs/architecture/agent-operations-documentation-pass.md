# Agent operations and proof-architecture documentation pass (Stage 8.5)

Documentation and scientific-operations architecture pass — not a
layout-migration stage and not a mathematical research stage.

The global Krenn–Gu conjecture remains **UNRESOLVED**.

## Provenance

```text
starting main SHA:   3404991ac9eca65e1fe0aa5acd7e3e71f4640194
                     (PR #36 / Stage 8 merge commit)
branch:              agent-operations-proof-architecture
inspection date:     2026-08-07
```

Stage 8 merge verified before any work: rank-two-triangle
classification/boundary packages, the Stage 8 batch, dry-run, report,
and the candidate-index-completeness invariant in `check_hygiene.py`
all present on merged `main`.

## Documents created

- `AGENTS.md` — durable agent operating contract: context
  reconstruction from committed evidence, mandatory scientific-status
  distinctions, multi-axis evidence, certificate discharge pattern,
  independent-verification rules, Lean semantics, research/software/
  migration modes, candidate-tree validation, stop conditions.
- `docs/proof-obligation-architecture.md` — how analytic arguments,
  reductions, computational certificates, independent audits, and
  formal methods compose into a proof DAG; the R/X/E/C/Z/A
  certificate discharge rule; evidence classes as orthogonal modes;
  generic-to-pointwise closure; withdrawn-lineage rules; status-change
  gate.
- `docs/formalization-interface.md` — interface to the external Lean
  development, including the pinned-commit inspection record and the
  L0–L5 formalization milestones.
- `docs/architecture/layout-migration-runbook.md` — the stable
  migration procedure extracted from Stages 1–8 (allowed to become
  historical after migration finishes).

## Navigation files touched

- `README.md` — one short "Working with the research repository"
  section linking the four documents (three `catalog/theorem-ledger.json`
  hash fields refreshed for the changed README; no ledger entry
  created, repointed, or status-changed).

No `CONTRIBUTING.md`, `CITATION.cff`, or `docs/index.md` exists in
this repository, so no edits were made there.

## External Lean repository inspected

```text
repository:       KitaKen1/monochromatic-quantum-graphs-lean
inspected commit: d3ed1892ef181f5f5f5d61d9b5817f05b53a6675
Lean version:     v4.27.0 (lean/); v4.33.0-rc1 (lean4web/)
mathlib:          mathlib4 a3a10db0e9d66acbebf76c5e6a135066525ac900
FC dependency:    google-deepmind/formal-conjectures
                  f7349f32ba6df6e7b7baf77467a3c6c7777a634d (pinned)
```

Inspection was read-only (shallow clone + source/README review); no
Lean build was run.  Facts established:

- central theorem
  `QuantumLean.eqSystem_no_solution_ge6_ge3_int` — the integer-weight
  no-solution obstruction for even N ≥ 6, D ≥ 3;
- twelve Formal-Conjectures wrapper theorems with a per-wrapper
  `#print axioms` audit module;
- no `sorry`/`sorryAx` admissions and no project-specific `axiom`
  declarations in the repository-owned Lean proof sources of either
  edition; the pinned Formal Conjectures dependency intentionally
  contains open catalogue declarations using `answer(sorry)` — what
  matters for the completed wrappers is their actual axiom dependency
  footprints; the project's own README records the expected axiom
  closure as `propext`, `Classical.choice`, `Quot.sound` (ordinary
  foundational assumptions), excluding `sorryAx`,
  `Lean.ofReduceBool`, `Lean.trustCompiler` — recorded as the
  project's claim, with a fresh build as the decisive confirmation;
- the N=4 base case uses committed CNF/LRAT certificates checked by
  mathlib's `lrat_proof` elaborator, so the SAT producer is not
  trusted by the kernel.

**Correspondence status: pending audit.**  The external project is
recorded as a candidate external formalization; its integer-weight
statement is not yet audited against this repository's formulations,
and no definitional equivalence or formal closure of this
repository's obligations is claimed.  At this high-level pass no
project-specific axiom/admission concerns were found (none present
in the repository-owned sources; the pending item is build-level
confirmation of the wrapper axiom footprints), but that finding
inherits the pending-correspondence caveat.

## Non-interference confirmation

- No theorem document, proof text, verifier, audit, or certificate
  data changed.
- No migration mapping, batch artifact, manifest, or classification
  record changed.
- The only tracked-content edits outside new documentation are the
  README navigation section and the three README-hash ledger
  refreshes.

## Validation

Candidate tree staged (`git add -A`) before authoritative validation,
per the index-completeness invariant:

```text
python check_hygiene.py                          -> all checks passed
python -m unittest tests.test_migration_tools    -> 117 tests OK
python -m unittest tests.test_fourteen_vertex_cycle_cover_lattice
                                                 -> 14 tests OK
python tools/migration/rewrite_links.py          -> 0/0/0/0
git diff --exit-code                             -> clean
```

All local Markdown links in the new documents resolve.  No scientific
verifier/audit replay was required or performed: no scientific
content or executable research code changed.

CI bookkeeping (per the established convention): the substantive-head
workflow dispatch [31223729630](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31223729630)
passed (**success**) on the exact substantive head
`db8427b13ec33747caf39fd60e4560104def2d95`; the subsequent report-fill
bookkeeping commit carries its own PR CI run, recorded on the PR.
The final PR-triggered workflow must pass hygiene, migration tests,
14-vertex tests, and the rewriter fixed-point check on the resulting
PR head.

A focused documentation-only precision pass (proof-or-counterexample
resolution rule, counterexample audit route, LRAT trust model,
axiom-wording qualification) followed as new substantive head
`3d07613d22f5658725e1927d1adb652eb8fb36c3`; its dispatch
[31224934066](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31224934066)
passed (**success**) on that exact head.  One subsequent report-only
bookkeeping commit carries its own PR CI run, recorded on the PR.

## Stop condition

No Stage 9, no Lean formalization project, no proof-obligation JSON
schema, no legacy evacuation, and no new mathematics were begun.

> No theorem claim, assumption, scope, proof status, provenance
> status, or global-resolution status changed as a result of this
> documentation pass.  The global Krenn–Gu conjecture remains
> UNRESOLVED.
