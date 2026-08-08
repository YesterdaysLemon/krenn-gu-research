# Stage 12 candidate-helper ownership audit

Status: **shared-infrastructure ownership audit; no scientific status change,
file move, or refactor**

Baseline: `main` at
`3ef8d15f799a2acfe0f0d52cd6419556e366cf78` (the merge commit for PR #40).

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Decision

The root script

`derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py`

has two different owners inside one file:

1. component-20 claim/evidence code for the generic weighted-`H22` theorem;
2. neutral four-source weighted-`H22` contraction machinery used by four
   mathematical component families.

The imported machinery does not encode the component-20 pure basis, its
elimination argument, or its theorem conclusion.  In particular, importing
`build_model` is an `implementation_dependency`, not a mathematical premise
from the component-20 claim and not evidence that a consumer is candidate or
exploratory.

The current classifier proposal to move the whole script to `tools/explore/`
is therefore not ownership-correct.  It was inferred only from the `derive_`
prefix.  The file must eventually be tapered into neutral infrastructure and
component-20-owned evidence before its root destination can be approved.

This audit closes the shared-dependency *classification* blocker for the
three-file split-center H22 generic package: that primary consumes neutral
model construction, while its audit independently reconstructs the model.
It does not approve that package's move.  Its exact dry run, replay surface,
frozen mapping, and human approval remain separate required steps.

## 2. Scope and exclusions

This pass followed the three-graph separation in the
[Stage 11 topology](p5-proof-obligation-topology-stage11.md) and the
[evidence-semantics contract](../evidence-semantics-contract.md):

- filesystem/classification;
- executable/provenance; and
- mathematical proof obligations.

It inspected the helper, all direct importers, candidate evidence and hashes,
representative owning theorem/audit prose, bootstrap/path behavior, and the
split-center package that Stage 10 marked `SHARED_DEPENDENCY_UNCLEAR`.

It deliberately did not:

- move, copy, or refactor executable code;
- edit any theorem, verifier, audit, certificate, result, or snapshot;
- change the theorem ledger, classifier, moved-path manifest, hygiene policy,
  or root-debt baseline;
- create or approve a migration batch;
- strengthen an independence claim or scientific status; or
- choose a final shared-module name on the owner's behalf.

The baseline remains 2,007 grandfathered root-debt files and zero new debt.
Stage 12 reduces no root debt; it closes one named ownership blocker.

## 3. Executable census

An AST census finds exactly 39 direct importers.  Their five filename groups
represent four mathematical families because the `component23_*` and
`common_center_kernel_star_*` names are two surfaces of the same component-23
obligation.

| filename group | direct importers | mathematical owner |
|---|---:|---|
| `verify_p5_h22_common_center_kernel_star_*` | 17 | common-center H22 / component 23 |
| `verify_p5_component23_*` and `verify_p5_h22_component23_*` | 8 | common-center H22 / component 23 |
| `*_p5_h22_unequal_complement_common_kernel_*` | 11 | unequal-complement H22 |
| `verify_p5_h22_split_center_mixed_star_*` | 1 | split-center H22 / component 24 |
| `verify_p5_h22_unequal_endpoint_inward_star_*` | 2 | unequal-endpoint H22 |
| **total** | **39** | **four families** |

Of these scripts, 33 are verifier/reconnaissance executables and six are
audit executables.  Twenty-two already bootstrap `src/krenn_gu` and expose a
moved claim package; 17 are still root-local and do neither.  A future shared
module extraction must account for both launch modes rather than assuming
that every root script can already import `krenn_gu`.

The directly imported names are:

| name | importer count | role |
|---|---:|---|
| `build_model` | 36 | neutral weighted-`H22` contraction constructor |
| `project` | 6 | neutral `D01`/`D23`, finite/infinity row projection |
| `WORDS` | 5 | neutral four-bit source-word enumeration |
| `permanent4` | 2 | neutral exact permanent implementation |
| `singular_command` | 1 | neutral runtime/backend discovery, not mathematics |

No importer calls `pure_bases`, `shifted_beta`, `projection_check`,
`projection_certificates`, or `main`.  No direct importer reads the candidate
report, certificate, or component-20 path constants through this module.
The imports use no aliases or wildcards, and no additional dynamic importer,
`runpy` loader, or subprocess caller was found.

## 4. Exact symbol ownership boundary

The script's top-level surface separates as follows.

| symbols | ownership | reason |
|---|---|---|
| `WORDS`, `MIXED`, `PERMUTATIONS3`, `PERMUTATIONS4`, `permanent3`, `permanent4`, `project`, `build_model` | neutral shared implementation | Defined without a component basis or theorem conclusion; they accept caller-supplied rows, extensions, direction, chart, and slope. |
| `singular_command` | neutral runtime plumbing | Selects native or WSL Singular; it carries no claim semantics, but is not conceptually part of the contraction model. |
| `add`, `scale`, `shifted_beta` | mechanically neutral residual helpers | They encode ordinary vector/marking operations, but no cross-family importer requires them; a minimal shared API need not export them. |
| `pure_bases` | component-20 claim construction | Encodes the component-20 basis. |
| `projection_check`, `projection_certificates`, `singular` | component-20 proof/evidence orchestration | Builds the exact eliminations and expected component-20 projected ideals. |
| `ROOT`, `SCRIPT`, `REPORT`, `CERTIFICATE`, `COMPONENT`, `H31`, `H22_WALL`, `sha256`, `git_commit`, `main` | component-20 provenance and replay | Owns paths, hashes, dependency replays, result emission, and the candidate's evidence record. |

The dependency closure of `build_model` is neutral: `project`, `WORDS`,
`MIXED`, `permanent3`, `PERMUTATIONS3`, and SymPy expansion.  It does not
reach any component-20 path, basis, projection certificate, or solver
orchestration.  The analogous closures of `permanent4` and `project` are also
neutral.  This neutrality is scoped to the exact four-source, eight-extension,
four-bit `D01`/`D23` model; it is not an arbitrary-order or local-to-global
constructor.

An exact-arithmetic parity probe compared the shared definitions with the
component-20 no-import audit's independently named `project_row`,
`permanent_by_subsets`, and `contraction_model`.  It passed both directions,
both projective charts, all sixteen coefficients, `project`, and `permanent4`
on deterministic rational data.  This corroborates the source-level boundary;
it is not a replacement for the semantic replays required by a future
extraction.

## 5. Mathematical and lifecycle boundary

The filename contains `candidate`, but the owning component-20 document
records a verified characteristic-zero generic/function-field theorem with
explicit special-divisor and projective exclusions.  The discovery label is
candidate lineage; it is not the current mathematical status of every
correct identity in the file.

Conversely, a consumer's use of the neutral constructor does not inherit the
component-20 theorem.  The four consuming families supply their own row
bases, markings, parameters, and claims.  Their scientific status remains
controlled by their owning documents and evidence, not by this import edge.

The helper is therefore neither wholly `tools/explore` material nor a theorem
premise for 39 consumers.  Moving it wholesale according to the classifier
would hide both the live component-20 evidence role and the shared
implementation role.

## 6. Audit-independence finding

The component-20 generic theorem's own audit is genuinely no-import with
respect to the candidate script: it independently implements subset-DP
permanents, row projection, contraction construction, and Singular
orchestration before checking the candidate artifacts and dependencies.  Its
independence is still scoped: both routes use Singular and the same broad
elimination strategy, and the audit replays rather than re-proves upstream
P4/H31 claims.

Six other audit scripts directly import this helper's `build_model`:

- `audit_p5_h22_unequal_complement_common_kernel_component_d23_f2_f7_intersection_obstruction.py`;
- `audit_p5_h22_unequal_complement_common_kernel_component_d23_f2_f8_h3_slope_intersection_obstruction.py`;
- `audit_p5_h22_unequal_complement_common_kernel_component_d23_h1_nonzero_h2_zero_partial_closure.py`;
- `audit_p5_h22_unequal_complement_common_kernel_component_d23_h2r1_residual_obstruction.py`;
- `audit_p5_h22_unequal_complement_common_kernel_component_d23_h2_zero_six_by_six_terminal_reduction.py`; and
- `audit_p5_h22_unequal_complement_common_kernel_component_d23_h2_zero_terminal_complete_obstruction.py`.

All six also import `component_rows` and `shifted` from the moved
unequal-complement H31 primary.  They are not independent at the source-row
or weighted-contraction construction layers.  Four use explicit Gaussian
elimination downstream of that shared construction while their corresponding
primaries use `DomainMatrix`; the six-by-six terminal script is a distinct
shared-construction replay with substantially the same SymPy checker route;
and the `h2r1` script is exact rational-specialization corroboration, not an
independent audit of the primary's generic coefficient-field elimination.

Four of the six use unqualified `independent` or `no-import` wording in a
docstring or emitted role/method.  Their owning prose usually makes the
narrower intent clearer: they do not import the corresponding H22 primary and
use a different low-level determinant or specialization route.  The durable
interpretation is therefore **shared-construction evidence, independent only
at the stated downstream layer where one exists**, not a fully no-import
rederivation.

This finding does not refute the mathematical claims or force a status
change.  It prevents future metadata, migration reports, or proof graphs from
calling these six audits independent of the shared model/row construction.
Moving that construction into `src/` later will not retroactively increase
their independence.

## 7. Provenance and path consequences

Non-import consumers matter as well:

- the component-20 candidate document records the root replay command and
  script hash;
- the independent verification document pins the candidate script,
  certificate, dependencies, and their hashes;
- the independent audit constructs the candidate script path as a split
  string and hashes/replays its artifacts;
- the layout catalogs carry the unexecuted classifier proposal;
- architecture inventory/history and the continuation handoff name the root
  command.

There is also pre-existing replay debt.  The candidate audit still sets
`P4_SCRIPT` to the retired root path
`verify_p4_common_active_binary_triangle_component.py`, so its complete
dependency replay is not currently path-clean.  Separately, the verification
document records the historical candidate-script hash `6d2b36e7...`, while
the current post-migration-repair script hash is `a7e23c3b...`.  Four
component-19 derivations consume and hash that verification document.  These
facts are provenance constraints, not a reason to rewrite the historical
record in this ownership audit.

A future extraction therefore cannot be validated by import success alone.
It must inspect executable path constants, hashes, report regeneration,
tracked outputs, and the semantic result of every practical replay.  If the
candidate script itself changes to import a neutral module, its pinned hash
and evidence outputs must be deliberately replayed and updated.  If it stays
byte-stable while consumers switch to an extracted implementation, exact
parity and the temporary duplication boundary must be explicit rather than
presented as two independent derivations.

The single `singular_command` consumer is a separate runtime-plumbing edge.
It should not force Singular discovery into a weighted-`H22` mathematics
module merely to make an importer count reach zero.

## 8. Staged continuation

### 8.1 Prefer direct root reduction next

Stage 11 and Stage 11.5 did not reduce debt, and this audit is another
zero-reduction enabling stage.  The governance rule therefore favors a safe
direct reduction over another open-ended policy pass.

The smallest candidate is the split-center H22 generic triple:

```text
P5_H22_SPLIT_CENTER_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h22_split_center_mixed_star_component_generic_obstruction.py
audit_p5_h22_split_center_mixed_star_component_generic_obstruction.py
```

The classifier proposes one coherent destination,
`claims/p5/h22/split-center-mixed-star/`, for all three.  The theorem is
generic with explicit open special/projective boundaries; the primary uses
the neutral model interface identified here; and the audit independently
reconstructs its basis, projections, contractions, and permanent algorithm.

The next stage may therefore perform an owner-reviewed dry run for exactly
this triple.  It must still audit all staying imports/paths, replay the
primary and audit semantically (including Singular requirements), freeze an
exact mapping, and obtain exact human approval.  Nothing in Stage 12 is move
approval.  In particular, the split-center primary currently imports the
root helper before calling `bootstrap`; a moved script must reorder that
import below the standard bootstrap (or target a reviewed neutral module)
rather than relying on root execution path behavior.

### 8.2 Extract shared infrastructure separately

The eventual helper taper should be a Tier 2 shared-infrastructure stage,
separate from a pure migration commit.  Its reviewed design should:

1. define a neutral `src/krenn_gu` contraction interface for `WORDS`,
   `permanent4`, `project`, and `build_model`, including their private
   dependency closure;
2. keep component-20 bases, eliminations, reports, certificates, and
   provenance with the component-20 claim package;
3. handle Singular discovery as runtime infrastructure rather than smuggling
   it into a claim module;
4. repair all 39 direct imports, moving the shared import below bootstrap in
   the existing 22 launchers and adding the standard bootstrap to the other
   17;
5. add exact interface/parity tests and run representative real-repository
   consumers across all four families;
6. replay any changed pinned evidence and inspect tracked outputs; and
7. preserve the six audits' shared-construction independence limitation.

The exact module name and whether the component-20 primary imports it or
retains an explicitly frozen local implementation are owner-reviewed design
choices.  If it imports the neutral interface, it becomes the fortieth
consumer.  No such choice is made by this audit.

### 8.3 Keep other forests deferred

This ownership result does not make common-center/component-23,
unequal-complement, or unequal-endpoint H22 flat-package ready.  They retain
distributed closures, partial/residual trees, evidence-scope distinctions,
or open boundaries recorded in Stage 11.  The component-21 three-consumer
candidate helper is a separate ownership audit.

## 9. Reproducibility and validation

Read-only checks for this audit included:

- exact Git/GitHub/worktree/open-PR reconstruction at the baseline SHA;
- `python check_hygiene.py` (pass; 2,007 grandfathered paths, zero new);
- an AST import census (39 direct importers, exact symbol and family counts);
- exact-string plus split-string provenance/path inspection;
- source-level dependency-closure inspection of every top-level symbol;
- representative theorem, primary, and audit comparison across all four
  consuming families;
- exact rational parity checks against the component-20 no-import audit; and
- confirmation that the split-center audit independently reconstructs the
  imported model surface.

This is a documentation-only ownership result.  It does not substitute for
the candidate-tree validation floor, fresh Tier 2 referees, or exact-head CI
required before integration.

## 10. Hard stop

Stage 12 stops before executable extraction, audit-label repair, a
split-center dry run, a frozen Stage 13 batch, or any scientific edit.

An exact future migration mapping still requires human approval under the
[layout-migration runbook](layout-migration-runbook.md).  The current broad
root-exit goal is not approval for an as-yet-unnamed mapping.
