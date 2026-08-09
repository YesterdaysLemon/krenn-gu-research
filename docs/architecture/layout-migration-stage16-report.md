# Layout migration report — Stage 16 (H31 embedded-P3 closure)

Status: **the exact Stage 16 migration transaction is complete locally and
ready for fresh Tier-2 merge-gate review.**  One coherent 15-file proof
forest left repository root: five theorem documents, their five exact
characteristic-zero primary verifiers, and five independent modular audits.

> **Scientific status did not change.**  The generic ledger node remains
> `verified_generic`.  Its three affine descendants and projective case-union
> theorem retain their stated scopes, and the audits remain corroborative
> finite-field evidence rather than replacements for the characteristic-zero
> proofs.  No claim about all pure components, the separate weighted-H22
> embedded-P3 programme, or the global problem was added.  The global
> Krenn-Gu conjecture remains **UNRESOLVED**.

## Provenance anchors

- Exact merged baseline: `2eda840131e73e699a99b58efb190d5eaf1023c1`.
- Branch: `codex/stage16-h31-embedded-p3-migration`.
- Corrected dry-run commit:
  `9827defc5e618db0d4ae0f11eead523a890f4860`.
- Frozen batch commit:
  `1e0558ccfc9028b638a4469ac54aa53f6ada973a`.
- Pure move commit:
  `fad6bd52213508195746a9a1867fe1ae4c184ac7`.
- Mechanical repair commit:
  `ad86ccc089e332de3faccdc862edcb83a0c37dda`.
- Exact-commit dry run:
  [`p5-h31-embedded-p3-stage16-dry-run.md`](p5-h31-embedded-p3-stage16-dry-run.md).
- Frozen batch: `catalog/batches/p5-h31-embedded-p3-stage16.json`:
  - reviewer: `Codex (exact mapping reviewer under repository-owner standing
    delegation dated 2026-08-08)`;
  - base SHA: `2eda840131e73e699a99b58efb190d5eaf1023c1`;
  - member count: 15;
  - mapping SHA-256:
    `db3bf4cc6309334ffc2a9983456f8674d9df5f22c3f921c969bcc4af414d5fb7`;
  - approval-time manifest SHA-256:
    `16ff7b355d83890b1acb321b994eecbfb2f83ac2f5a87c0e7cf2fba127e345b9`.

Three independent pre-execution scouts separately reconstructed the
proof-obligation topology, replayed the mathematics, and simulated the
mechanical transaction.  All three found the mapping routine,
evidence-backed, and non-ambiguous under the repository owner's standing
delegation.  Classifier confidence was used only as proposal evidence.

## Selected closure forest and exclusions

All 15 files moved to `claims/p5/h31/embedded-p3/`:

| scope | theorem family | primary | audit |
|---|---|---|---|
| dense generic point | `GENERIC_OBSTRUCTION` | exact SymPy verifier | independent modular audit |
| normalized `A B r != 0` chart | `NORMALIZED_BOUNDARY_OBSTRUCTION` | exact SymPy verifier | independent modular audit |
| support-two `A=0, B!=0` divisor | `SUPPORT_TWO_BOUNDARY_OBSTRUCTION` | exact SymPy verifier | independent modular audit |
| `r=0, A B!=0` divisor and affine `B!=0` closure | `R_ZERO_BOUNDARY_OBSTRUCTION` | exact SymPy verifier | independent modular audit |
| full projective ninth component | `PROJECTIVE_CLOSURE_OBSTRUCTION` | exact SymPy verifier | independent modular audit |

The ownership topology is:

```text
generic dense open
  -> normalized A B r != 0 chart
       + support-two A=0, B!=0 divisor
       + r=0, A B!=0 divisor
       => complete affine B!=0 family
  -> projective symmetry and case-union closure
       consumes normalized + support-two + r=0
       => whole projective ninth-component H31 fibre empty
```

The projective theorem explicitly consumes all three boundary children, so
moving only the generic triple would split one proof obligation.  No other
tracked H31 embedded-P3 theorem, primary, or audit was found.

Explicitly excluded:

- the separately owned weighted-H22 embedded-P3 forest, whose historical
  refuted/UNKNOWN lineage and open projective coverage remain at root;
- the already migrated P4 embedded-P3 component package, which is upstream;
- `verify_p5_h31_marked_basis_open_branch.py`, a high-fanout shared helper;
- common-active and high-coordinate files, which consume this forest but do
  not belong to it; and
- architecture reports and historical provenance records.

## Pure-move acceptance

Against the pure move commit's direct parent:

- all 15 exact sources are absent and all 15 destinations are present;
- every destination blob is byte-identical to its source-parent blob;
- Git records all 15 moves as `R100`;
- the only non-rename change is the deterministic manifest transaction;
- every selected manifest record is `moved` and names
  `p5-h31-embedded-p3-stage16` as `executed_batch`; and
- no theorem prose, assertion, algebra, or executable content changed.

Observed arithmetic:

| measure | before | after |
|---|---:|---:|
| manifest `moved` | 353 | 368 |
| manifest `proposed_high_confidence` | 249 | 246 |
| manifest `review_required` | 1,413 | 1,401 |
| measured root files | 2,011 | 1,996 |
| measured root directories | 9 | 9 |
| measured root entries | 2,020 | 2,005 |
| grandfathered root debt | 2,004 | 1,989 |
| enforceable retired paths | 353 | 368 |

There are zero new root-debt paths, destination collisions, double moves, or
overlap cycles.

## Mechanical repair

The migration rewriter made exactly 21 Markdown-link rewrites and 11 fenced
replay-command rewrites across 14 Markdown files, plus one theorem-ledger
path relocation.  A second pass was a fixed point with zero ambiguities.

Explicit repairs then:

- placed shared bootstrap before repository imports in all ten moved Python
  executables and used `HERE` for co-located evidence;
- moved the four load-bearing root/co-moved imports below bootstrap and used
  `REPO_ROOT` for the generic verifier's P4 anchor;
- updated exactly 19 operational path bindings in nine staying consumers;
- preserved frozen historical hashes and prose while updating only active
  paths and replay commands;
- added the five-triple closure forest to the P5/H31 navigation and recorded
  its asymmetry from the still-open H22 programme;
- retained the generic ledger status, assumptions, scope, and audit role;
- corrected only that entry's runtime metadata from an inapplicable Singular
  requirement to `seconds-to-minutes (sympy)` with no external binary; and
- refreshed staged-blob hashes for the moved generic theorem and six other
  ledger entries whose documents received deterministic link rewrites.

No evidence status, lifecycle state, theorem quantifier, domain, assumption,
or global-resolution field changed.

## Exact package replay

Each moved executable ran once from repository root by relative destination
path and once from a fresh foreign working directory by absolute path under
Python 3.13.14 and SymPy 1.14.0.  For every script, the two parsed JSON
objects were exactly equal.

| family | primary, two-run wall | audit, two-run wall | required semantic result |
|---|---:|---:|---|
| generic | 10.647 s | 5.726 s | generic H31 empty; boundary/census/global false |
| normalized | 3.505 s | 0.606 s | complete normalized chart empty; projective/global false |
| support-two | 4.115 s | 0.601 s | `A=0, B!=0` fibre empty; remaining projective/global false |
| `r=0` | 14.303 s | 0.835 s | divisor and affine `B!=0` family empty; global false |
| projective | 1.617 s | 0.570 s | whole projective ninth-component H31 fibre empty; census/global false |

All ten report `verified: true` and `global_problem_resolved: false`.
Every audit additionally reports `finite_field_audit_is_theorem: false`.

## Staying-consumer replay

Nine root-owned consumers were replayed after their path constants changed:

| consumer | wall | semantic result |
|---|---:|---|
| H22 generic primary | 1.077 s | generic weighted fibre empty; slope/global false |
| H22 rank-two primary | 2.039 s | rank-two line closed; rank-one/projective/global false |
| H22 `r=0` derivation | 9.086 s | aggregate VERIFIED only after the separate endpoint theorem |
| historical H22 `r=0` audit | 2.520 s | original full-divisor route remains REFUTED; endpoints remain historically UNKNOWN |
| endpoint construction | 1.142 s | exactly both homogeneous endpoints VERIFIED |
| endpoint independent audit | 11.526 s | both endpoints and both exact H31 subprocess replays pass |
| common-active wall primary | 12.671 s | stated diagonal-DVR H31 wall closed; H22/global false |
| common-active wall audit | 5.383 s | independent wall replay; primary not imported; H22/global false |
| high-coordinate frontier | 0.850 s | aggregate verified; `P5_to_Delta3_resolved=false`; global false |

The historical REFUTED result is preserved rather than rewritten by the later
endpoint repair.  Replays created no tracked-output change.

## Validation floor

The index-complete candidate tree passes:

- Ruff and byte compilation for all 19 changed or consuming executables;
- isolated `python -I` import probes for the same 19 files from a foreign
  working directory under the declared SymPy environment;
- `check_hygiene.py`: 1,698 Python files compile, all 804 Markdown files have
  resolving local links, all 86 ledger hashes match, the root-debt ratchet is
  `1,989 grandfathered / 0 new`, and all 368 retired-path and batch-provenance
  records pass;
- all 152 migration-tool tests;
- all 14 fourteen-vertex cycle-cover lattice tests;
- migration-rewriter fixed point; and
- clean staged-candidate and working-tree diff checks.

## Merge gate and stop condition

This Tier-2 migration requires two fresh read-only exact-head referees:
semantic/status review and mechanical/bypass review.  It also requires
exact-head CI, a fresh merge base, no consequential unresolved review, and a
normal exact-head merge.

This stage stops at the H31 embedded-P3 closure forest.  It does not migrate
the H22 sibling forest, extract the marked-basis helper, classify every pure
component, close unrelated boundaries, or make a global claim.  The global
Krenn-Gu conjecture remains **UNRESOLVED**.
