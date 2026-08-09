# P5 H31 complete component-chart-boundary marked fibre - Stage 23 deferred candidate audit

Status: **BLOCKED — NOT APPROVED FOR A FROZEN BATCH. The exact filesystem
ownership is clear, but the selected theorem and primary disagree on the
certificate-stratum count. No move has been executed.**

> **Scientific status will not change.** The global Krenn-Gu conjecture
> remains **UNRESOLVED**. This review resolves filesystem ownership only. It
> does not turn one divisor-scoped complete marked fibre into a generic or
> whole-component theorem, component exhaustiveness, `P5 -> Delta3`, gluing,
> or a global result.

## Review authority and corrected baseline

- Exact corrected baseline:
  `025ee3c41372907c6f69ff8066ce3d884164bd08`.
- Branch: `codex/stage23-h31-component-chart-boundary-marked-fibre-migration`.
- Actual mapping reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.
- Delegated-review test for filesystem ownership: routine, non-ambiguous, and
  evidence-backed. Batch execution is nevertheless blocked because resolving
  the scientific theorem/verifier contradiction is outside that delegation.
- Candidate batch ID, not to be frozen while this audit is blocked:
  `p5-h31-component-chart-boundary-marked-fibre-stage23`.
- Candidate-review raw Windows-checkout manifest SHA-256:
  `c6c5b192a13da3016fe4d70f784c8cc7991b471e26c119eeec5b8a8d36f1dc36`.
- Canonical mapping SHA-256:
  `9d9c85b5dc89958ea0127f6ed5f7fe8000b060294e17966a70321a36b709f39e`.

The manifest hash is informational candidate-review provenance over raw CRLF
checkout bytes. The canonical mapping hash is the portable authority for the
reviewed old-to-new pairs.

The original classifier routed the generator to `tools/explore` solely from
its `derive_` prefix. That split was mechanically consistent but contradicted
the actual proof boundary: the theorem names the generator as its regeneration
command; the primary is its only Python importer, imports `rows`, `singular`,
and `singular_program`, and hashes the file as a dependency. Commit
`025ee3c` therefore makes the one routine ownership correction before this
candidate review:

- generator category `tool_script -> claim_script`;
- family `null -> p5/h31/component-chart-boundary-marked-fibre`;
- destination `tools/explore/... -> claims/p5/h31/component-chart-boundary-marked-fibre/...`;
- family count `3 -> 4`, `tool_script 211 -> 210`, and
  `claim_script 1071 -> 1072`; and
- generated destination counts `claims 1761 -> 1762`, `tools 210 -> 209`.

The correction changes no classifier confidence or migration status. The
corrected classifier raw SHA-256 is
`8561e714ce1aafe77a9d274cc62feb756ba9b7335c8cc1cf920641f89f22c397`;
the corrected manifest record remains `review_required` with medium
confidence. Hygiene and all 152 migration-tool tests passed on the complete
candidate index before the correction commit. Classifier confidence remains
proposal evidence only. The topology and mechanical audits establish the
exact ownership below, but scientific execution approval is withheld by the
theorem/verifier contradiction.

## Exact four-file mapping

All four files move flat into
`claims/p5/h31/component-chart-boundary-marked-fibre/`.

| role | source | destination |
|---|---|---|
| theorem | `P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md` | `claims/p5/h31/component-chart-boundary-marked-fibre/P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md` |
| characteristic-zero primary | `verify_p5_h31_component_chart_boundary_marked_fibre.py` | `claims/p5/h31/component-chart-boundary-marked-fibre/verify_p5_h31_component_chart_boundary_marked_fibre.py` |
| modular audit | `audit_p5_h31_component_chart_boundary_marked_fibre.py` | `claims/p5/h31/component-chart-boundary-marked-fibre/audit_p5_h31_component_chart_boundary_marked_fibre.py` |
| exact elimination generator | `derive_p5_h31_chart_boundary_marked_fibre_elimination.py` | `claims/p5/h31/component-chart-boundary-marked-fibre/derive_p5_h31_chart_boundary_marked_fibre_elimination.py` |

Every source is tracked grandfathered root debt, every destination is absent,
and the corrected durable classifier and generated manifest contain exactly
these pairs. There are no duplicate sources or destinations, case-folded
destination collisions, double moves, overlap cycles, or package-name
collisions.

| source | Git blob | raw Windows-checkout SHA-256 |
|---|---|---|
| theorem | `73ade81380b483a81f52ebda4f14443f815ebb32` | `b560311b0b2afa84fea55b659a7cbe448ee9f8cedde77aa48b5f7db3ee82209f` |
| audit | `799b2c1098910bd10596f359ae88f384fbd3a229` | `6ad60659b87debf59a65fc40aaf09772663477bd413189eaf23b58d725ec0bf2` |
| generator | `b2ed4c8096d22da626141922a5df926fac853d43` | `ed8b3e711a3db1bb3bcf7870cfe36f6fb18f760d188bdef04dfbd326b667a345` |
| primary | `0366d5a7233ba3f4fcc1427b66b7a72d17c44330` | `a320497a50b4ae5b9b64e6943b12e2296b2a922dadb1bfd5b010c1635e3ef6d7` |

## Proof-obligation ownership and exact scope

The selected package is one complete, separable divisor-scoped proof leaf:

```text
first known pure-rank-two component
  -> one nonzero all-rank-two divisor in the preferred chart, D=0 and a!=0
  -> A*H*N != 0 with R arbitrary
  -> bijective source/row action normalizes H=N=1 and retains A!=0
  -> every divisor plane tuple and every kernel-row shift
  -> every q=0,1,2,3 and binary Delta2 extension direction
  -> exact characteristic-zero elimination plus selected-minor cover
  => the complete marked-basis fibre on this divisor is empty

first-plane infinity, internal E=0, toric/projective interior,
second/further components, H22, P5 -> Delta3, gluing, and global
remain outside this leaf
```

The exact scope description is:

> An exact characteristic-zero, divisor-scoped complete marked-basis-fibre
> obstruction on the one nonzero all-rank-two divisor in the preferred
> four-Grassmannian chart of the first known pure-rank-two component. Before
> normalization `A*H*N != 0`, with `R` arbitrary; the source/row action
> bijectively normalizes `H=N=1`, retains `A!=0`, and preserves all four
> row-shift parameters. It quantifies over every divisor plane tuple, every
> kernel-row shift, all `q=0,1,2,3`, and every binary `Delta2` extension
> direction.

It is not generic, a whole-component theorem, component-closure evidence, or
component exhaustiveness. It strictly strengthens the live Stage 22 canonical
marked-row checkpoint in `claims/p5/h31/component-chart-boundary/` by adding
all kernel-row shifts and the complete marked-basis fibre. That predecessor is
neither withdrawn nor superseded.

The P4 chart closure and Stage 22 canonical theorem remain separately owned
upstream evidence. Shared root helpers
`p5_high_coordinate_tree_chart_cegar.py`,
`verify_p5_h31_marked_basis_open_branch.py`, and
`audit_p5_h31_marked_basis_fibre_classification.py` remain root-owned because
they have broader consumers. No other Python executable imports the selected
generator.

No selected artifact has a curated theorem-ledger entry or formal
counterpart. Migration adds no entry and changes no mathematical status,
assumption, quantifier, scope, lifecycle, evidence role, or global-status
field.

## Preserved conflicts and evidence boundaries

Two pre-existing scientific/provenance conflicts remain explicit and are not
adjudicated by this move.

First, the P4 toric-boundary prose attributes the earlier canonical theorem
to internal `E=0`, while the P4 chart-closure source and this successor identify
the selected nonzero divisor as `D=0,a!=0`; this successor treats internal
`E=0` separately. Migration neither infers equivalence nor endorses or corrects
that prose edge.

Second, and blocking for execution, the selected theorem says its components split into fourteen
elementary certificate strata and later refers to a fourteen-row certificate
ledger. The primary's `certificate_strata()` contains sixteen `Stratum`
records and explicitly asserts and reports `16`. The theorem's separate phrase
“fourteen mixed binary coefficients” is a different count. The modular audit
does not settle this characteristic-zero stratum cardinality. Stage 23
preserves both artifacts verbatim, does not claim complete fact-for-fact
theorem/verifier agreement, and leaves reconciliation to a separate
owner-gated scientific/provenance correction. Because the repository contract
requires a stop when a claimed proof contradicts its verifier, clear
filesystem ownership does not authorize freezing or executing this batch.
Both artifacts nevertheless
agree on assumptions, elimination ideals, the selected-minor obstruction,
scope, and the conservative conclusion, so the mismatch does not make
filesystem ownership ambiguous.

The primary is the characteristic-zero proof replay. The audit imports
neither the primary nor the generator; it duplicates the family rows and uses
shared finite-field audit primitives to perform separate `F5/F7` modular row
reduction, projective-extension enumeration, and direct-minor QA. Its
independence is downstream of the shared theorem-specified normal form, and
the modular census is QA only, not the characteristic-zero proof or an
end-to-end independent derivation. The generator is proof-producing support,
not independent evidence.

The following remain separately owned and retain their own recorded statuses:

- first-plane infinity, internal `E=0`, and toric/projective interior;
- the finite chart, second diagonal-quadric and further components;
- component exhaustiveness, weighted `H22`, and `P5 -> Delta3`;
- arbitrary-order/local-to-global gluing and the global conjecture.

The broader first/second-component status-provenance conflict remains
unconsumed. Scope-local false fields must not downgrade separately proved
results.

## Mechanical repair and deterministic rewrite surface

After the pure move, all three selected Python executables install the shared
bootstrap before repository imports:

- `REPO_ROOT, HERE = bootstrap(__file__)` supplies stable path ownership;
- the primary resolves its theorem and generator through `HERE`, and the P4
  chart plus canonical predecessor through `REPO_ROOT`;
- the audit resolves theorem and primary through `HERE`, while bootstrap
  exposes its staying root finite-field helper;
- the generator uses bootstrap to expose both staying root helpers; and
- the sole staying operational consumer,
  `verify_p5_high_coordinate_partial_frontier.py`, retargets its theorem path.

All three selected executables remain stdout-only. No module importer or
subprocess caller outside the selected primary targets the selected generator,
primary, or audit.

The deterministic virtual post-move rewriter predicts exactly **eight
Markdown links and three fenced replay commands across eight Markdown files**,
with zero ambiguity and zero ledger relocation. The touched files are the
moved theorem, Stage 22 canonical theorem, P4 pure-rank-two component theorem,
alternative-strategy map, marked-basis classification, marked-basis open
branch, high-coordinate frontier, and root README. Stage 22 reports and
`docs/research-notes.md` are historical provenance and remain unchanged. The
second pass must be a `0/0/0` fixed point.

Projected normalized-LF hashes include:

- moved theorem:
  `c81bfd32f6e5e2d145570980b2b3cc4ceaf9645cf477142186013b61fdec3ade`;
- canonical predecessor:
  `225df2c26fa54b0a112151b5da9845805dc11e304f865b66710dd643afdb67f4`;
- P4 component theorem:
  `6e9322f9be09280c007ce1066d217c28470bc3ed01c527b889202acc034a6387`;
- marked-basis classification/open:
  `8705c8c50a260a4f7682510135a0550090870e8ffac064279e32b270f13ed628`
  and `6f2884e1623bf7afc1c9db9434a4cdd023004be9453197a4ab3666d8bef590b5`;
- high-coordinate frontier:
  `65cb23c8d9a2bb316d11c32a8f3bd3e64150f39a83ddb5af1cdcfb392424bcfa`;
  and
- root README:
  `d9a6577ae27a2976d60f6559536644b149044b80ef2e8f0bbeaa3219fb9abefe`.

Exactly four existing ledger hashes refresh mechanically:

- verified high-coordinate frontier -> `65cb23c8d9a2bb31`; and
- the three root-README entries -> `d9a6577ae27a2976`, retaining statuses
  `open`, `verified_generic`, and `partial`.

All other ledger fields remain byte-for-byte fixed. Navigation adds a
separately labelled complete marked-fibre strengthening on the same nonzero
chart divisor to `claims/p5/h31/README.md`, changes the scoped-exception count
from six to seven, records the Stage 23 batch/mapping hash, and explicitly says
this is not a whole-component theorem. Parent P5 navigation mirrors the scope
and changes the H31 package-directory count from 29 to 30.

## Projected transitions

| measure | before | after |
|---|---:|---:|
| manifest `moved` | 398 | 402 |
| manifest `proposed_high_confidence` | 242 | 242 |
| manifest `review_required` | 1,375 | 1,371 |
| moved-only manifest root projection | 1,974 | 1,970 |
| high-confidence manifest root projection | 1,732 | 1,728 |
| all-classified manifest root projection | 357 | 357 |
| measured root files | 1,966 | 1,962 |
| measured root directories | 9 | 9 |
| measured root entries | 1,975 | 1,971 |
| grandfathered root debt | 1,959 | 1,955 |
| new root debt | 0 | 0 |
| enforceable retired/provenance paths | 398 | 402 |

The move creates one approved nested H31 package directory, increasing the
H31 package count from 29 to 30, and changes no root baseline or end-state
allowlist.

## Exact baseline evidence

The selected primary and audit bytes at the corrected baseline are unchanged
from the Stage 22 acceptance matrix. That serial replay preserved rc=0,
empty-stderr, valid-JSON results from repository root and, for the primary, a
fresh foreign working directory.

The characteristic-zero primary reported:

- `verified: true`, field `characteristic zero`, normalization
  `H=N=1 with bijective shift action`;
- four projection/ledger runs and **sixteen** exact factor-certificate records;
- all extension residual covers and the complete chart-boundary marked fibre
  excluded true; and
- projective first-plane boundary, internal `E=0`, additional components, and
  global resolution false.

The root/foreign primary objects agreed after removing only their measured
`elapsed_seconds` values (12.517 and 10.763 seconds in that matrix). The
modular audit passed in 2.017 seconds with four orientations, 614 projection
points, 5,400 binary extensions, the complete divisor fibre excluded true,
and global false. Those facts are replay evidence for current bytes, not a
resolution of the fourteen-versus-sixteen theorem/verifier prose conflict.

## Acceptance matrix required after a separate reconciliation

Use
`uv run --quiet --python 3.13 --with sympy --with python-sat python`,
strictly serial, and preserve every first output before assertions. A wrapper
or post-parse error must not trigger an automatic expensive rerun or become
theorem evidence. External-Singular jobs use the established fail-closed WSL
route on Windows and must not overlap.

The complete recursive closure is **25 unique executables and 35
invocations**:

1. Run the moved primary, moved audit, and staying high-coordinate primary
   from both repository root and fresh foreign working directories by absolute
   path: six JSON invocations.
2. Run the following 21 JSON consumers once from repository root:
   - `audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_independent.py`;
   - `audit_p5_h31_marked_basis_fibre_classification.py`;
   - `audit_p5_h31_marked_basis_open_branch.py`;
   - `audit_p5_high_coordinate_partial_frontier.py`;
   - `claims/p4/classifications/pair-geometry/pure-rank-two/audit_p4_pure_rank_two_component.py`;
   - `claims/p4/classifications/pair-geometry/pure-rank-two/boundaries/verify_p4_pure_rank_two_component_toric_boundary.py`;
   - `claims/p4/classifications/pair-geometry/pure-rank-two/verify_p4_pure_rank_two_component.py`;
   - `claims/p4/classifications/pair-geometry/pure-rank-two/verify_p4_pure_rank_two_component_chart_closure.py`;
   - `claims/p4/components/diagonal-quadric/verify_p4_diagonal_quadric_pure_component.py`;
   - `claims/p4/components/mixed-orientation/verify_p4_mixed_orientation_pure_component.py`;
   - `claims/p5/h22/first-rank-two/verify_p5_h22_first_rank_two_component_generic_obstruction.py`;
   - `claims/p5/h31/component-chart-boundary/audit_p5_h31_component_chart_boundary.py`;
   - `claims/p5/h31/component-chart-boundary/verify_p5_h31_component_chart_boundary.py`;
   - `derive_p5_h22_component19_p0_phi_pm_one_ordinary_obstruction_candidate.py`;
   - `derive_p5_h22_component19_p0_qphi_minus_one_axes_compatibility_obstruction.py`;
   - `verify_p4_diagonal_quadric_one_three_components.py`;
   - `verify_p5_h31_component_fiber_infinity.py`;
   - `verify_p5_h31_component_fibre_infinity_marked_fibre.py`;
   - `verify_p5_h31_marked_basis_fibre_classification.py`;
   - `verify_p5_h31_marked_basis_open_branch.py`; and
   - `verify_p5_h31_rank_two_component_orbit.py`.
3. Run the moved generator without `--run` for every `q=0,1,2,3` from both
   root and foreign CWD and compare the eight deterministic Singular programs
   exactly. The primary already submits all four generated programs to
   Singular and verifies their exact projection bases, so duplicate generator
   `--run` calls are unnecessary.

Exactly 18 closure executables write only ignored repository-`tmp/` JSON and
seven are stdout-only; none writes a tracked output. The selected primary,
audit, and generator are stdout-only.

Require:

- moved-primary root/foreign equality after removing only
  `elapsed_seconds`, with four projection runs, **16** reported certificate
  records, complete divisor fibre true, and projective/internal/additional/
  global false;
- moved-audit byte equality, four orientations, 614 projection points, 5,400
  extensions, modular-QA scope, and global false;
- all eight generator programs equal across CWDs and all selected dependency
  hashes current;
- high-coordinate census 6,495 / 1,680 / 1,170 / 510, mask-6 `VERIFIED`,
  both component-19 derivations `CANDIDATE`, and P5/global false;
- canonical predecessor, P4 component, marked-basis, first-plane, and
  rank-two-orbit consumers preserve their existing exact scopes, statuses,
  counts, and conservative global fields;
- every emitted theorem, primary, source, and dependency hash matches current
  bytes; and
- every generated file remains ignored, all foreign directories stay empty,
  and no tracked output drifts.

If a separate authorized scientific/provenance audit reconciles the blocking
count and a fresh mapping review again authorizes the batch, all three moved
modules must pass isolated foreign-CWD import probes. Confirm
targeted Ruff and byte compilation, rewriter fixed point, the index-complete
validation floor, exact-head CI, and fresh semantic plus mechanical final
referees before a normal head-guarded merge.

## Stop boundary

This candidate stops before batch freeze or execution. A separate
owner-gated scientific/provenance audit must reconcile the fourteen-versus-
sixteen certificate-cardinality conflict before this package can be reviewed
again for migration. The P4 attribution conflict, first-plane infinity,
internal `E=0`, toric/projective interior, later components, component
exhaustiveness, weighted `H22`, `P5 -> Delta3`, local-to-global gluing, and
global resolution also remain outside this candidate.

The global Krenn-Gu conjecture remains **UNRESOLVED**.
