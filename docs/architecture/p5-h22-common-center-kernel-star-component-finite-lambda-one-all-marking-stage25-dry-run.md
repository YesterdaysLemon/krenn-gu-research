# P5 H22 component-23 finite lambda-one all-marking - Stage 25 exact migration dry run

Status: **APPROVED FOR AN EXACT FROZEN BATCH under the repository-owner
standing delegation dated 2026-08-08. No move has yet been executed.**

> **Scientific status will not change.** This review approves filesystem
> ownership only. The selected theorem remains an exact characteristic-zero
> function-field obstruction for the finite `lambda=1` slice and every
> affine marking at the generic common-center-kernel-star component point.
> It is not a pointwise statement on special component fibres and does not by
> itself prove the whole generic finite fibre, special or projective fibres,
> arbitrary-order gluing, or the global conjecture. The global Krenn-Gu
> conjecture remains **UNRESOLVED**.

## Review authority and exact baseline

- Exact clean baseline:
  `6bff7b460c3e04ae0538ba38553b5f51bbf4fd7d`.
- Baseline tree:
  `acf015de9139f7717c745ca3d8d5870fce13bcfd`.
- Branch:
  `codex/stage25-h22-finite-lambda-one-all-marking-migration`.
- Actual mapping reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.
- Delegated-review test: routine, non-ambiguous, evidence-backed exact layout
  mapping; no scientific-status decision, ambiguous proof-boundary choice,
  or owner-preference architecture decision is required.
- Batch ID to freeze:
  `p5-h22-finite-lambda-one-all-marking-stage25`.
- Corrected classifier raw Windows-checkout SHA-256:
  `f4e9dba9f245b9bfe9eea71a24940f71b6d4dc7b6bc5ff23269f8d74a28b75ce`.
- Approval-time manifest raw Windows-checkout SHA-256:
  `25b051239004b967c7bbb00017462b8daad63e55947549e11b66ba70c2d8d1e2`.
- Canonical mapping SHA-256:
  `611abb78c553a124a4cf02308950ec5ace6c9f5f1e2e727ece7f043f3b1f59ba`.

The catalog contains exactly these three family records. Each remains
medium-confidence `review_required`; classifier confidence is proposal
evidence, not review authority. All three sources are tracked grandfathered
root debt, every destination is absent, and the exact mapping has no source
or destination duplicate, case-folded collision, double move, overlap cycle,
or package-name collision.

The simulated executor output for this exact batch has:

- normalized-LF manifest SHA-256
  `857e9a1aaae23354af7631926aaa85291cd9142c4afb99d2a3a317b24a8976c2`;
- raw CRLF manifest SHA-256
  `3039028bf9609ccbf47a9e1d22a27e17bc0b2c7aed325c755e7dfebd6f913b38`;
  and
- Git blob `eb2d446278cc72976b73799c2de47de5446453a6`.

These projections are valid only for the exact batch ID, base, and three
old-to-new pairs below.

## Exact three-file mapping

All three files move flat into
`claims/p5/h22/common-center-kernel-star-component-finite-lambda-one-all-marking/`.

| role | source | destination |
|---|---|---|
| theorem | `P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_LAMBDA_ONE_ALL_MARKING_OBSTRUCTION.md` | `claims/p5/h22/common-center-kernel-star-component-finite-lambda-one-all-marking/P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_LAMBDA_ONE_ALL_MARKING_OBSTRUCTION.md` |
| exact-ℚ specialization audit | `audit_p5_h22_common_center_kernel_star_component_finite_lambda_one_all_marking_obstruction.py` | `claims/p5/h22/common-center-kernel-star-component-finite-lambda-one-all-marking/audit_p5_h22_common_center_kernel_star_component_finite_lambda_one_all_marking_obstruction.py` |
| characteristic-zero primary | `verify_p5_h22_common_center_kernel_star_component_finite_lambda_one_all_marking_obstruction.py` | `claims/p5/h22/common-center-kernel-star-component-finite-lambda-one-all-marking/verify_p5_h22_common_center_kernel_star_component_finite_lambda_one_all_marking_obstruction.py` |

The frozen source identities are:

| role | Git blob | raw Windows-checkout SHA-256 |
|---|---|---|
| theorem | `1074a957b3a6d50d137ff3f92f2756f268b873f9` | `0963088f40499e4372a600b7a69eea6182375a439dd8da194475f4a02b65016d` |
| audit | `e43c41f06c803a1ed9090577788a83cb1fd3558f` | `5763de5079ce4330f95a46248e20f81765325857d8db55eeda7a999321e2b0ef` |
| primary | `3a3cfb661c15a00bf0618fa48672db6760f4a698` | `299e1f784659b57ca0dd7a79be3842ede51c2dd6cf23c744f52224845b6a98f7` |

The theorem, primary, and audit were introduced together in commit
`49750bedfeb42d31d9ea621a6d22691f33004acb`. The primary later received only
the Stage 10 operational import repair for the migrated H31 row provider.

## Exact proof-obligation scope

The selected triple is one complete, separable case-coverage leaf:

```text
common-center-kernel-star component 23 at its generic parameter point
  -> coefficient field K = Q(r,t)
  -> finite homogeneous-weight chart with lambda=1
  -> every affine marking (h0,h1,h2,h3)
  -> D01 and D23 binary contractions
  -> their 28 shared mixed coefficient rows
  -> exact bidirectional module equality
       M = <e1,e2,e3,e4,e6,e7,e8>
  -> A01, A23, B01 in M; B23 not in M
  -> every shared mixed kernel has B01=0
  -> genuine weighted H22 requires inherited all-beta support,
       hence B01 and B23 both nonzero
  => contradiction
  => the complete finite lambda=1 all-affine-marking fibre is empty

other finite weights, special/projective component parameters, wider
source-torus or ambient degenerations, component exhaustiveness,
arbitrary-order gluing, and the global conjecture remain outside this leaf
```

The field `Q(r,t)` makes this a generic-component function-field result. It
does not silently quantify over parameter specializations where generic
denominators vanish. “Every affine marking” quantifies the four marking
variables on this generic `lambda=1` slice; it does not mean every
projective marking chart or every special component fibre.

The primary must retain exactly:

- `status: pass`, `field: Q(r,t)`, `component: 23`, and direction
  `finite lambda=1 all markings`;
- `claim_label: VERIFIED_EMPTY`;
- mixed module `e1,e2,e3,e4,e6,e7,e8` and bidirectional equality true;
- diagonal membership in reported order `A01,A23,B01,B23` equal to
  `[true,true,true,false]`;
- `lambda_one_all_markings_closed: true`;
- `generic_finite_all_markings_closed: false`;
- the two displayed residual descriptions inherited from the dense-open
  checkpoint;
- `finite_field_proof_used: false`; and
- `global_conjecture_resolved: false`.

## Case-union lineage and chronological fields

The selected leaf is load-bearing inside a later case union, but that does
not make the whole component-23 forest one filesystem package:

```text
old PARTIAL checkpoint
  -> dense-open supplement
       -> also closes lambda=-1
  -> lambda=0 all-marking sibling
  -> selected lambda=1 all-marking leaf
  -> F=0,h2=0 ordinary branch
  -> final ordinary residual theorem
  => complete generic finite fibre
  + the earlier infinity theorem
  => complete generic weighted H22 fibre at the generic component point

separate boundary descendants
  -> r=0 / t=0 charts
  -> projective and source-torus faces
  -> wider ambient or Grassmann degenerations remain open
```

The staying
`P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_ORDINARY_RESIDUAL_OBSTRUCTION.md`
explicitly consumes the complete `lambda=0,1,-1` slices and closes the later
generic finite case union. Root README records that current synthesis. The
selected theorem's earlier residual-`UNKNOWN` prose and its primary's
`generic_finite_all_markings_closed: false` field truthfully describe what
this leaf alone did at that chronological checkpoint. They do not downgrade
the later terminal theorem. Migration preserves those bytes and records the
later edge in navigation; it does not rewrite scientific history.

The Stage 11 topology warning against moving the old partial/generic core in
isolation does not block this completed terminal slice. The selected leaf is
complete at its stated `lambda=1` scope, while its predecessor and successor
edges can cross package boundaries without changing their mathematics.

## Evidence roles and shared providers

The primary uses the three providers below to obtain the generic component
rows and marking shifts and to construct and serialize both binary models,
the 28 mixed rows, and four diagonal rows. It then asks Singular to check both
module inclusions and all four membership results over
`Q(r,t)[h0,h1,h2,h3]`. Its three repository providers stay outside this
package:

1. `build_model` from
   `derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py`;
2. `coefficient_row` and `singular_command` from
   `verify_p5_h22_common_center_kernel_star_component_partial.py`; and
3. `rows` and `shifted` from the migrated
   `claims/p5/h31/common-center-kernel-star/` primary.

These are construction, serialization, launcher, and row-parameterization
providers. The candidate-bearing filename of the first provider does not
promote its candidate claim, and reuse of the H31 implementation does not use
the H31 obstruction conclusion as a premise. The selected theorem's
mathematical predecessor is the common-center partial/dense-open lineage,
not the unrelated status of shared implementation containers.

No outside Python module imports the selected primary or audit. There is no
subprocess or hash consumer of either executable, no selected theorem-ledger
entry, and no formal counterpart. The staying ordinary-residual theorem is a
semantic downstream consumer only; no downstream executable is load-bearing
solely because of this move.

The audit imports no repository module. It independently reconstructs, over
exact `Q` at `(r,t)=(2,4)`, the component rows, marking shifts, projections,
permanents, coefficient vectors, mixed module, and diagonal rows. It obtains
the same seven generators and `[true,true,true,false]` membership pattern.
Safe evidence wording is:

> No-repository-import exact-Q corroboration at `(r,t)=(2,4)`, independently
> reconstructing the rows, projections, permanents, and module input. It
> shares Singular standard-basis/reduction machinery and is not an
> independent generic `Q(r,t)` proof.

The audit must retain:

- `status: pass`, `field: Q`, and specialization `r=2,t=4`;
- `independent_no_repository_imports: true`;
- the same mixed module, bidirectional equality, and membership vector;
- `audit_only_not_generic_proof: true`;
- `finite_field_proof_used: false`;
- `generic_finite_all_markings_closed: false`; and
- `global_conjecture_resolved: false`.

The theorem's statement that no rational specialization is used in the proof
refers to the characteristic-zero generic primary. The audit specialization
is exact QA and must not be presented as proof of the generic theorem.

## Preserved conflicts and explicit exclusions

The selected theorem's residual-`UNKNOWN` sentence is chronological
provenance debt, not an owner-gated migration blocker. Editing it into a
current whole-family synthesis would be separate scientific-status work and
is excluded from the move. The root README link repair below records existing
case-union evidence without changing any theorem statement.

The component-23 family retains open special/projective/source-torus and
ambient-degeneration obligations. Separate boundary files may reuse row
machinery from other components while explicitly denying theorem
specialization; those ownership and evidence questions are not consumed or
adjudicated here. Stage 25 neither migrates the old partial theorem,
dense-open supplement, `lambda=0` sibling, ordinary branches, nor any
component-23 boundary descendant.

No candidate-labelled provider becomes verified evidence by proximity or
import. No generic field is replaced by the audit point `(2,4)`. No false or
open field is promoted, no ledger entry is created for the selected theorem,
and no claim is made about full pointwise component coverage, component
exhaustiveness, `P5 -> Delta3`, arbitrary-order/local-to-global gluing, the
prize graph, or global resolution.

## Mechanical repair and deterministic rewrite surface

After the pure move, the primary must place the standard `sys`/`Path`
bootstrap before every repository import. It uses
`REPO_ROOT, HERE = bootstrap(__file__)`, retains
`expose_claim_package(REPO_ROOT, "claims/p5/h31/common-center-kernel-star")`,
and imports both staying root providers and the migrated H31 provider only
after path setup, with scoped `E402` suppressions. It does not need
`also=["."]` because it has no selected sibling import. This is an
operational import-order repair only; no row, equation, module assertion,
timeout, output field, or mathematical algorithm changes.

The audit remains free of repository imports. Its only portability repair is
to add stdlib `shutil` and a local launcher that chooses native
`Singular -q` first, uses `wsl.exe --exec /usr/bin/Singular -q` on Windows
when native Singular is unavailable, and fails clearly if neither exists. It
must not import a repository launcher. Its 90-second timeout, equations,
assertions, and JSON remain unchanged. The primary retains the provider
launcher's native/WSL choice and 120-second timeout.

Both executables remain stdout-only. They create no durable or ignored JSON
output and no tracked solver artifact; only ordinary ignored Python bytecode
may arise.

The deterministic post-move rewriter projection is exactly:

- `links_rewritten=1`;
- `commands_rewritten=4`;
- `files_touched=2`;
- ambiguity `0`; and
- second pass `0/0/0`.

The two files are the moved theorem and
`docs/NEXT_INSTANCE_HANDOFF_2026-07-31.md`. The one link is the handoff's
selected-theorem link. The four commands are the primary/audit commands in
the moved theorem and the same two commands in the handoff. The Stage 10
historical importer-inventory basename remains unchanged.

The theorem's dense-supplement reference is inline code and outside the
rewriter's ownership. Repair it to one ordinary Markdown link with label
`P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_ALL_MARKING_DENSE_OPEN_SUPPLEMENT.md`,
target
`../../../../P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_ALL_MARKING_DENSE_OPEN_SUPPLEMENT.md`,
and a trailing period. The label and target are specified separately here so
the pre-move dry run does not itself contain a link to a not-yet-valid
post-move relative path.

Projected normalized-LF hashes are:

| file/state | SHA-256 |
|---|---|
| moved theorem after rewriter only | `a6c3cfd750073bd10a706435f61f1d39701ddebbe5bbd29a57f67a6678bfba56` |
| moved theorem after rewriter plus manual supplement link | `bb666b91513a8694a5b12a10b28b9b58b9162a8f400056be231e748f2e90555e` |
| handoff after rewriter | `1ffca39ec9bf0dc305feef7ec4b1604fe7e0db2b90bcac401996c66fc637ff2b` |

The final moved theorem additionally has raw CRLF SHA-256
`1451a9e458a7b7cafad3c9ebd5db93c061f2d6e0e71f7722f25087e8cb3eecd2`
and Git blob `5f01947d91a4ac51f4ae219e244bf3b1e789dec8`. The handoff additionally has
raw CRLF SHA-256
`439252704667e45faa5e99d9af7da20f6cc8efa2466f95e5fe63c26305f02515`
and Git blob `aba41cd92f70e7c251e1d97c6a74e9f163b4bd5c`.

## Navigation and ledger semantics

Root README already states the later complete generic component-23 weighted
`H22` synthesis but omits direct `lambda=0` and `lambda=1` evidence links.
Between its dense-open link and `F,h2=0` link, insert two ordinary Markdown
link lines. Each line begins with exactly two spaces and ends with a comma.
The first label is
`P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_LAMBDA_ZERO_ALL_MARKING_OBSTRUCTION.md`
with target
`P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_LAMBDA_ZERO_ALL_MARKING_OBSTRUCTION.md`.
The second label is
`P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_LAMBDA_ONE_ALL_MARKING_OBSTRUCTION.md`
with target
`claims/p5/h22/common-center-kernel-star-component-finite-lambda-one-all-marking/P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_LAMBDA_ONE_ALL_MARKING_OBSTRUCTION.md`.
Labels and targets are separated here so the pre-move dry run does not itself
contain a link to the not-yet-created destination.

This is a provenance-completeness repair for the already stated case union,
not a new closure claim. With exactly that two-link insertion and no other
root-README prose edit, projected identities are:

- normalized-LF SHA-256
  `e088b31ea75020ac527e053d684400723076723e8aba6339b1ff8b8476733db0`;
- raw CRLF SHA-256
  `bb8e060dcafcea6d0c646b275811bc9245a4c54fa4854497be5277061a5d2a8b`;
  and
- Git blob `a30a11917d2412ef9548fb3bca239b188806efef`.

The theorem ledger remains at 86 entries and gains no selected-theorem entry.
Exactly the three existing root-README-backed `document_sha256_16` values
change from `0e3e92ffbdb54440` to `e088b31ea75020ac`:

1. `Problem statement: no T_W = GHZ diagonal for even n>=6, d>=3` remains
   `open`;
2. `Component census and exhaustive all-pair-rank reduction (checkpoint)`
   remains `verified_generic`; and
3. `Component twenty-two D23 pencil divisor-by-divisor closure` remains
   `partial`.

The projected whole-ledger normalized-LF SHA-256 is
`d80c4c2fd20e73fa6b0ac52e70bba23664fbafc3d3bd0495c0d6ea1d91e6e39b`,
with raw CRLF SHA-256
`1e40a222ef7986db369edb277dd17f967c9dfde0b0e8abd98c8ac42e4f0306ec`
and Git blob `059947c2e2109feb7fade77211ccf7ad3833b27e`.

`claims/p5/h22/README.md` adds the Stage 25 batch and mapping and labels this
as the scoped generic-parameter `lambda=1` all-affine-marking leaf, outside
the generic package table. Its “Not migrated” wording must distinguish this
moved leaf from the old partial theorem and remaining common-center boundary
forest. `claims/p5/README.md` changes the H22 package-directory count from 18
to 19, records Stage 25 and the same narrow scope, and states that the generic
common-center H22 core remains at root while this leaf moved. These two
manual navigation files are not hash-pinned before their exact wording is
materialized. No package README is required for this three-file leaf.

## Projected transitions

| measure | before | after |
|---|---:|---:|
| total classified records | 2,015 | 2,015 |
| manifest `moved` | 405 | 408 |
| manifest `proposed_high_confidence` | 242 | 242 |
| manifest `review_required` | 1,368 | 1,365 |
| unclassified | 348 | 348 |
| frozen root baseline | 2,363 files + 3 directories = 2,366 | unchanged |
| moved-only manifest root projection | 1,967 | 1,964 |
| high-confidence manifest root projection | 1,725 | 1,722 |
| all-classified manifest root projection | 357 | 357 |
| classifier inherited all-migration estimate | 356 | 356 |
| measured root files | 1,959 | 1,956 |
| measured root directories | 9 | 9 |
| measured root entries | 1,968 | 1,965 |
| allowlisted root files | 7 | 7 |
| grandfathered root debt | 1,952 | 1,949 |
| new root debt | 0 | 0 |
| enforceable retired/provenance paths | 405 | 408 |
| actual tracked files under `claims/` | 409 | 412 |
| H22 package directories | 18 | 19 |
| H31 package directories | 31 | 31 |

The classifier's inherited estimate `356` and manifest's exact projection
`357` are separate existing metrics and must not be silently harmonized. The
move changes no root baseline or exact end-state allowlist.

## Exact pre-move baseline evidence

At clean baseline
`6bff7b460c3e04ae0538ba38553b5f51bbf4fd7d`, the selected primary and audit
ran exactly once each, strictly serially, through:

```powershell
uv run --quiet --python 3.13 --with sympy python <script>
```

No `python-sat` dependency was required. Native Singular was unavailable in
the Windows environment, so the primary used its WSL fallback and the audit
used its then-current direct `wsl.exe --exec /usr/bin/Singular -q` route.

The primary completed in 21.253 seconds with rc=0, empty stderr, one valid
JSON object, and captured-stdout SHA-256
`d822509c388a4f761a1a79b6eed1cc8d2b77e03e8ddca56eb5293e057b4d8c33`.
It reported exactly the `Q(r,t)` scope, seven-generator module,
`[true,true,true,false]` diagonal membership, `VERIFIED_EMPTY` lambda-one
closure, generic-finite false, the two chronological residuals, no
finite-field proof, and global false.

The audit then completed in 11.350 seconds with rc=0, empty stderr, one valid
JSON object, and captured-stdout SHA-256
`a9a9413b5fecec324d73dc73197652e9f23f4fe900a5eda3fc14fc0972ba3669`.
It reported exact `Q`, specialization `(2,4)`, no repository imports, the
same module and diagonal membership, audit-only-not-generic true, no
finite-field proof, generic-finite false, and global false.

Both executables were stdout-only; no tracked or durable ignored result file
was created. Only ignored `__pycache__` directories appeared, and the tracked
worktree remained clean. Every first stdout, stderr, rc, timing, argument
vector, and SHA-256 is preserved outside the repository at:

`C:\Users\Yeste\.codex\run-artifacts\stage25-20260809T142217Z`.

These are pre-move baseline facts for the frozen source bytes, not evidence
for a broader generic finite theorem, special fibre, or global result.

## Post-move acceptance matrix

The complete affected scientific closure is exactly **two unique
executables and four invocations**:

1. moved primary from repository root;
2. moved primary by absolute path from a fresh foreign CWD;
3. moved audit from repository root; and
4. moved audit by absolute path from a different fresh foreign CWD.

Use
`uv run --quiet --python 3.13 --with sympy python`, strictly serially, and
preserve every first stdout, stderr, rc, timing, argument vector, and JSON
object outside the repository before assertions. Do not automatically rerun
after a wrapper, schema, path, solver, or assertion failure. Do not alter
process priority or kill a running solver. Each scientific invocation starts
Singular once, for four non-overlapping solver subprocesses total.

Require:

- rc=0, empty stderr, and exactly one valid JSON object for every invocation;
- primary root/foreign byte and parsed-object equality, with every exact
  primary field and scope boundary listed above;
- audit root/foreign byte and parsed-object equality, retaining exact `Q`,
  specialization `(2,4)`, `independent_no_repository_imports: true`, and
  `audit_only_not_generic_proof: true`;
- identical seven-generator modules and `[true,true,true,false]` membership
  vectors across both evidence routes, without treating the specialization
  as a generic proof;
- no finite-field-proof or global-resolution field becomes true;
- no provider path is stale and no candidate/shared provider status is
  consumed as theorem evidence;
- both stdout-only executables create zero tracked and zero durable ignored
  JSON outputs;
- both foreign directories remain entirely empty;
- the tracked and index trees remain clean; and
- the pre-move source identities match the frozen pins; the batch, mapping,
  final theorem, handoff, root README, and ledger identities match their
  projected pins; and the newly materialized primary and audit repair
  identities are recorded before replay.

After the four scientific rows, run one isolated import-only probe from a
fresh foreign CWD for each moved module. The two probes are not scientific
replays and are not counted in the four invocations. They must return rc=0,
empty stderr, an explicit import-success marker, and empty foreign
directories. Then run targeted Ruff import-order checks and byte compilation
for both moved scripts.

No provider executable, `lambda=0` sibling, dense-open supplement, or
ordinary-residual executable is load-bearing solely because of the move, so
none belongs in this minimum acceptance closure. The later ordinary-residual
theorem is a semantic consumer and remains untouched.

After acceptance, require the rewriter's `0/0/0` second-pass fixed point, the
index-complete validation floor, exact-head CI, and fresh semantic plus
mechanical final referees before a normal head-guarded merge.

## Stop conditions

Stop rather than freezing, executing, or publishing if:

- the exact mapping, base, source blob, raw hash, or simulated manifest pin
  differs;
- proof ownership expands beyond the exact `lambda=1` all-affine-marking
  function-field leaf;
- `Q(r,t)` is described as pointwise coverage of special component fibres;
- the `(2,4)` audit is described as a generic proof or imports repository
  scientific code;
- a candidate/shared provider is promoted into verified theorem evidence;
- the chronological false/`UNKNOWN` fields are edited, suppressed, or used
  to downgrade the later terminal case-union theorem;
- the primary or audit repair changes equations, modules, assertions,
  timeouts, JSON schema, or any scientific status field beyond the exact
  launcher/path repairs approved above;
- the root README insertion differs from the exact two links without
  recomputing README and ledger hashes;
- any theorem-ledger status changes or a selected-theorem entry is invented;
- root/foreign results differ, a foreign directory gains output, a tracked
  file drifts, or a first run fails; or
- any wording promotes this leaf to generic pointwise component coverage,
  component exhaustiveness, `P5 -> Delta3`, gluing, or global resolution.

## Stop boundary

Stage 25 stops at the complete finite `lambda=1` all-affine-marking fibre
over `Q(r,t)` at the generic common-center-kernel-star component point. It
does not move or adjudicate the surrounding component-23 proof forest,
change the later generic case-union theorem, cover special or projective
component fibres, resolve wider source-torus or ambient degenerations, prove
component exhaustiveness, establish `P5 -> Delta3`, supply arbitrary-order
local-to-global gluing, or solve the prize conjecture.

The global Krenn-Gu conjecture remains **UNRESOLVED**.
