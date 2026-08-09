# P5 H22 finite lambda-zero all-marking Stage 26 dry run

Status: **APPROVED FOR THE EXACT FROZEN BATCH BELOW under the repository
owner's standing delegation dated 2026-08-08.**

The global Krenn-Gu conjecture remains **UNRESOLVED**. This approval changes
filesystem ownership only. It does not promote the selected branch verifier,
its exact specialization audit, any shared implementation provider, or the
later component synthesis beyond their existing mathematical scopes.

## Exact approval boundary

- Base HEAD: `cd97b313b021e26ad6391fbb7a1cf08db958f8e6`.
- Base tree: `b0bbe20fac33caed29f20b7da17b4236cdbb0b10`.
- Batch ID: `p5-h22-finite-lambda-zero-all-marking-stage26`.
- Canonical mapping SHA-256:
  `06622ad9c8ab149021fd4d3a5c412327db4a28cd2f210d339418d118a7e85131`.
- Approval-time manifest raw Windows-checkout SHA-256:
  `3039028bf9609ccbf47a9e1d22a27e17bc0b2c7aed325c755e7dfebd6f913b38`.
- Classifier raw Windows-checkout SHA-256:
  `f4e9dba9f245b9bfe9eea71a24940f71b6d4dc7b6bc5ff23269f8d74a28b75ce`.
- Reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.

The exact approved mapping is:

```text
P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_LAMBDA_ZERO_ALL_MARKING_OBSTRUCTION.md
-> claims/p5/h22/common-center-kernel-star-component-finite-lambda-zero-all-marking/P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_LAMBDA_ZERO_ALL_MARKING_OBSTRUCTION.md

audit_p5_h22_common_center_kernel_star_component_finite_lambda_zero_all_marking_obstruction.py
-> claims/p5/h22/common-center-kernel-star-component-finite-lambda-zero-all-marking/audit_p5_h22_common_center_kernel_star_component_finite_lambda_zero_all_marking_obstruction.py

verify_p5_h22_common_center_kernel_star_component_finite_lambda_zero_all_marking_obstruction.py
-> claims/p5/h22/common-center-kernel-star-component-finite-lambda-zero-all-marking/verify_p5_h22_common_center_kernel_star_component_finite_lambda_zero_all_marking_obstruction.py
```

All three classifier and manifest records agree on one `claim_document`, two
`claim_script` artifacts, the family
`p5/h22/common-center-kernel-star-component-finite-lambda-zero-all-marking`,
medium confidence, and current status `review_required`. All sources are
tracked exactly once. The destination directory and all three destinations
are absent, including case-folded checks. Collision, double-move, and overlap
cycle reports are empty.

The frozen source identities are:

| artifact | normalized-LF SHA-256 | raw Windows-checkout SHA-256 | Git blob |
|---|---|---|---|
| theorem | `6a0c5e816059e6b84fba11f2525af85c9c7689553f8fbd35381c459ab68e368c` | `d5385f6f16d86144489ce44b8ac1016406844925232879ab9a296510cfe4461b` | `d8f968fa09d070f68e5f29b2d31ab937a4ca13e9` |
| audit | `1dc85a9043e7ea0bea539bbf443f564f8c4f26f182553c7c2423fd9dbc4ee379` | `2578f945c278906eb74ed5812dbac5e5be28e644865a7fbb6981acd2b4794f81` | `6c27df8efc96e45459806b256341aff074cc68df` |
| primary | `e9d7439a05751d5774cf303fa37470c84907f065bc823e2788fe94dd18a7cfca` | `430df38f85d9aafe7f09c88447ed745933335c68a6b3816d32a47f2f297b82d4` | `699333d0e738c4fba28a2ff744c14fdafc3a1f8b` |

Classifier confidence is proposal evidence, not approval. The exact mapping
was separately reviewed along filesystem, executable/provenance, and
mathematical proof-obligation axes. All three reviews agree on this bounded
theorem/primary/audit leaf, so no owner-level scientific or architectural
choice is required.

## Exact mathematical scope

The selected triple is an exact characteristic-zero case-coverage leaf over
the generic component field

```text
K = Q(r,t).
```

It covers component 23, the finite homogeneous-weight chart at `lambda=0`,
every affine marking `h0,h1,h2,h3`, and the shared `D01/D23`
mixed-extension system. It is not a pointwise theorem on special
component-parameter divisors, a projective marking or weight theorem, the
whole generic finite fibre by itself, component exhaustiveness,
arbitrary-order gluing, or global resolution.

The theorem is load-bearingly dependent on the earlier dense-open
supplement. That predecessor proves that the relevant cross-contraction
minor at `lambda=0` is associated over `K` to

```text
h2*h3*H0,

H0 = (4*r^2 - 2*r*t - 2*r + 2*t^2 + 2*t - 4)*h3
     - r^2 - r*t + r - t + 2.
```

Thus full rank already holds away from `h2*h3*H0=0`. The selected primary
does not recompute that determinant cover. It closes exactly the three
residual branches

```text
h2=0, h3=0, H0=0.
```

On every branch the 28 shared mixed rows generate the full free rank-eight
module; both module inclusions and all four diagonal reductions are checked.
On `H0=0`, solving for `h3` is legal in `Q(r,t)` because the displayed
coefficient is a nonzero element and hence a unit in that function field.
Combining the three branch certificates with the prior factor cover closes
the complete `lambda=0` all-affine-marking slice at the generic component
point.

The special parameter divisor where that coefficient specializes to zero is
outside the generic function-field quantifier. Stage 26 must not turn this
into pointwise special-fibre coverage.

The proof-obligation lineage is:

```text
old partial theorem
  -> dense-open supplement
       residual refinement: lambda=0 requires h2*h3*H0=0
       complete lambda=-1 slice
  -> selected lambda=0 leaf
       mathematical dependency on the prior factor cover
       case coverage by h2=0, h3=0, H0=0
  -> separately moved lambda=1 leaf
  -> ordinary F=0,h2=0 leaf
  -> later ordinary-residual theorem
       consumes lambda=0,1,-1 plus ordinary branches
  => complete generic finite all-marking fibre
  + prior infinity theorem
  => generic weighted-H22 closure at the generic component point
```

The selected triple and dense-open supplement originated together in
`49750bedfeb42d31d9ea621a6d22691f33004acb`. The selected primary later
received only the Stage 10 import repair in
`c93a5c6828c01ebb216b54046a3a5ef8796638de`. The terminal
ordinary-residual theorem was added later in
`9efab43eea3696d7f6f49edb09f0968788bb5929`.

Consequently, the selected theorem's residual `UNKNOWN` prose and its
`generic_finite_all_markings_closed: false` field are truthful chronological,
leaf-local statements. The later ordinary-residual theorem's generic finite
closure is also truthful. Migration must preserve both rather than silently
"correcting" either one.

## Evidence roles and ownership

The primary is the characteristic-zero branch proof replay. It imports:

- `build_model` from a candidate-named model builder;
- `coefficient_row` and `singular_command` from the old partial verifier; and
- `rows` and `shifted` from the migrated H31 component provider.

These are shared construction, serialization, launcher, and row
parametrization dependencies. Their candidate, partial, or H31 theorem
statuses are not mathematical premises and are not promoted by code reuse or
proximity.

The audit imports no repository module. It independently reconstructs the
component rows, projections, permanents, mixed rows, and three residual branch
modules over exact `Q` at `(r,t)=(2,4)`, using the `H0`-branch
specialization `h3=3/8`. It shares Singular standard-basis and reduction machinery.
It does not re-verify the earlier factor cover and is neither an independent
generic `Q(r,t)` proof nor a complete independent audit of the selected
theorem. Its independence is limited to exact-Q branch-module corroboration.

No outside Python file imports the selected primary or audit. Neither has a
subprocess or hash consumer. The later ordinary-residual theorem and root
README are semantic consumers only. No selected artifact has a curated
theorem-ledger entry or recorded Lean/formal counterpart; Stage 26 adds none.

The frozen staying provider blobs are:

| provider | Git blob |
|---|---|
| candidate model builder | `a0aa17900c5e52330cdec720e81a9fa193e1980e` |
| partial coefficient/Singular provider | `8723bea6d00c58fbd87bb5fdeb4699d37f029a38` |
| migrated H31 row provider | `64ef8957937af9c71162f3142f39617a83167ab9` |
| dense-open premise primary | `f07c1ace19afed23a7da619c75ca820cb9505da1` |
| dense-open theorem | `2febc95fd2f1182965ec2408b3114358d512c8df` |
| shared bootstrap helper | `2e63e926ea4295af7b6d4fa18e24e26e7ef92324` |

Stage 26 neither consumes nor adjudicates the owner-gated H31
chart-boundary marked-fibre family whose theorem says fourteen certificate
strata while its primary constructs and reports sixteen. It also excludes
known weighted-H22 status conflicts and broader first/second-component
provenance questions. Those remain outside this mapping.

## Baseline replay evidence

An initial capture wrapper attempted to use
`ProcessStartInfo.ArgumentList`, which is unavailable in the Windows
PowerShell/.NET environment. The wrapper failed before `Process.Start`; zero
scientific processes began. That prelaunch-only failure is preserved at:

```text
C:\Users\Yeste\.codex\run-artifacts\stage26-baseline-cd97b313b021e26ad6391fbb7a1cf08db958f8e6-20260809T160643Z
```

It is an infrastructure record, not theorem evidence and not a failed
verifier or solver run.

A separately authorized corrected capture then used direct `uv` invocation
and ran the three intended executables exactly once each, strictly serially,
with no retry, priority change, or process intervention:

| executable | elapsed seconds | stdout SHA-256 | result |
|---|---:|---|---|
| selected `Q(r,t)` lambda-zero primary | 15.1499832 | `82a2f4f35afa63ca69b0000e002ed5d0d9916b558fd231055e5647d37c972004` | rc=0, empty stderr, one JSON object |
| selected exact-Q specialization audit | 6.7623319 | `0ef8123b3dc8c1305793d509e471f6167fc6af11f494af609965412043cf4c23` | rc=0, empty stderr, one JSON object |
| staying dense-open premise primary | 10.5731619 | `aa0c198261388168d8306ba383aa8c055e5bba9df324aa8832c0c4119277c95f` | rc=0, empty stderr, one JSON object |

The corrected evidence is preserved at:

```text
C:\Users\Yeste\.codex\run-artifacts\stage26-baseline-cd97b313b021e26ad6391fbb7a1cf08db958f8e6-20260809T160643Z-corrected
```

Offline assertions matched all exact schemas and ten source/dependency blobs,
proved `H|lambda=0 = H0`, and confirmed the intended composition: the prior
`h2*h3*H0` cover plus the three full-module branches closes only the
`lambda=0` slice. The audit remained exact-Q at `(2,4)` and audit-only;
generic-finite, finite-field-proof, and global-resolution fields stayed
false. The scripts created no JSON output. Only ignored bytecode appeared,
and HEAD, index, and worktree remained clean at `cd97b313`.

## Pure-move arithmetic

The simulated post-executor manifest for executed batch
`p5-h22-finite-lambda-zero-all-marking-stage26` has:

- normalized-LF SHA-256:
  `e07f1b187f3b99c15ca5204cef1cae65ccb2b95c92ce13ff388cb633dd02c5dc`;
- raw CRLF SHA-256:
  `6282ad5ac80fac671f117cd2d1d2226ee91f90e49eeac824a169a43e99e03385`;
- Git blob: `51be6e3ec279ff23b9aa784810f33251147950f3`.

Only the selected three records may change from `review_required` to
`moved`, gain the exact `executed_batch`, and contribute to deterministic
summary arithmetic:

| measure | before | after |
|---|---:|---:|
| total records | 2,015 | 2,015 |
| moved | 408 | 411 |
| proposed high-confidence | 242 | 242 |
| review-required | 1,365 | 1,362 |
| unclassified | 348 | 348 |
| moved-only root projection | 1,964 | 1,961 |
| high-confidence root projection | 1,722 | 1,719 |
| all-classified root projection | 357 | 357 |
| measured root files | 1,956 | 1,953 |
| root directories | 9 | 9 |
| root entries | 1,965 | 1,962 |
| allowlisted root files | 7 | 7 |
| grandfathered root debt | 1,949 | 1,946 |
| new root debt | 0 | 0 |
| retired/provenance paths | 408 | 411 |
| tracked files under `claims/` | 412 | 415 |
| H22 package directories | 19 | 20 |
| H31 package directories | 31 | 31 |

The frozen root baseline remains 2,363 files plus 3 directories. The
classifier's inherited all-migration estimate remains 356, separate from the
manifest all-classified projection 357.

## Deterministic rewrite and ledger forecast

The first post-move rewriter pass must return exactly:

```text
links_rewritten=2
commands_rewritten=4
files_touched=3
ambiguous=[]
ledger_entries_updated=0
```

The three files are:

1. the moved theorem, with two selected primary/audit replay commands;
2. `docs/NEXT_INSTANCE_HANDOFF_2026-07-31.md`, with the theorem link and two
   replay commands; and
3. root `README.md`, with the selected theorem link.

The dense-open replay command in the moved theorem remains root-relative
because that premise executable stays at root. Historical Stage 10 and Stage
25 code-span basenames remain unchanged. The second pass must be a `0/0/0`
fixed point with empty ambiguity.

The moved theorem's dense-open predecessor is inline code and therefore
outside the rewriter. Convert only that reference into an ordinary Markdown
link targeting:

```text
../../../../P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_ALL_MARKING_DENSE_OPEN_SUPPLEMENT.md
```

Projected identities are:

| file/state | normalized-LF SHA-256 | raw CRLF SHA-256 | Git blob |
|---|---|---|---|
| theorem, rewriter only | `2dc16269e7f9fb9128761abb8a6e91a2863360cc6ca5e50fcd9c946b59e9a5f9` | `e5b9c610892301f3e6b83946ae33c1e79af938b7b780fce5ff6383a299b82dc3` | `353ae82f49c218e6bc04ac876ea05ac3eae0fa3b` |
| theorem, final manual link | `0d4f2d89f9d11359dc594a065617263688e7119a99d516dffcaa9933d91f85d3` | `ea0f8e4c183b43cd45cdb185595786b368361092b1336d19ec81a34d26041107` | `b671074e302ffe6a633b1e12d85e036d7d36a118` |
| historical handoff | `ddbcca43fdeeb06b3deb74cfdc7ee74ec24ebd880c856706c5d925a47875998f` | `ad5aa58c272d44a5020c6f0c9b940b9e329e71c3eb202ecbc00fe134ae6e8d70` | `8e91a6e22ed256f2a044183f904b530b5f9f3f01` |
| root README | `a0cf89174c320e7b77a14f94c6322755bd9db8613ebacb8b17c8138049fd5b03` | `94b3cb6e7993e80f78a13ada5fdd01a90a29906bfa269eebb7899cc27126db51` | `e61df8bc5436bf469fdb48ea8c78925a71c27e2b` |
| theorem ledger | `a79f86dc6c4bc6d7c0530087a6197f1d3ce63e27d4042d19d800a62d2891d79b` | `37543b72237304232805b4c4922ef4a69a91d0fe107ac64c10e13a6937657d9f` | `ccf02d807c05ba565f4b4a0c9894e4fa7f77d825` |

The root README SHA16 becomes `a0cf89174c320e7b`. Replace exactly the three
existing README-backed ledger values `e088b31ea75020ac` with that value. The
ledger remains 86 entries. The three statuses stay `open`,
`verified_generic`, and `partial`; all other fields remain unchanged. No
selected-theorem ledger entry is added.

Navigation must:

- change the H22 package count from 19 to 20;
- record the Stage 26 batch and mapping hash;
- add a separately labelled generic-parameter `lambda=0` all-affine-marking
  leaf while retaining the `lambda=1` leaf;
- name the dense-open factor cover as its mathematical premise;
- name the ordinary-residual theorem as its later semantic consumer;
- state the exact-Q `(2,4)` audit limitation;
- exclude both moved finite-weight leaves from "not migrated" wording;
- keep the generic core and remaining boundary forest at root; and
- keep the global status `UNRESOLVED`.

No package README is required. Exact navigation README hashes must be
recorded after the approved prose is materialized.

## Python portability repair

The moved primary must mirror the corrected Stage 25 pattern:

- place stdlib `sys`/`Path` and shared bootstrap before every repository
  import;
- bind `REPO_ROOT, _ = bootstrap(__file__)`;
- expose `claims/p5/h31/common-center-kernel-star`;
- delay the H31 provider, candidate builder, and partial provider imports with
  scoped `E402` suppressions;
- add no unused `HERE`, theorem, or path constant; and
- preserve every equation, branch order, three 120-second solver calls,
  assertion, and JSON field.

The approved exact materialization is projected to:

- normalized-LF SHA-256:
  `ccc9e14059649b9e6918e020373eba205799d6ad5ec2e4eb3bad2212d0456ba7`;
- raw CRLF SHA-256:
  `265d20b8033fd896343698c1cc1c1418d3b051a751edad302046d0c0e5a6a35e`;
- Git blob: `c4cc602476092872443960dc8089df5746c0dd99`.

The moved audit remains free of repository imports. Add only stdlib `shutil`
and a local launcher that prefers native `Singular -q`, then uses
`wsl.exe --exec /usr/bin/Singular -q`, and otherwise fails clearly. Preserve
its equations, branch order, three 90-second solver calls, assertions, and
JSON. With standard top-level spacing, the approved materialization is:

- normalized-LF SHA-256:
  `c818b712e74699fece78aceb0d7dab75a9c2133956db30dbbcd33a36abf7c5bb`;
- raw CRLF SHA-256:
  `5ef00dcf46f54fc03772ca3bd99fee07798bb5b9b81129dbb68b6d219d832e7f`;
- Git blob: `afe0f29c0a4599c20ea2ebfb7240a9967253a541`.

The expected repair commit changes exactly eight files:

```text
README.md
catalog/theorem-ledger.json
claims/p5/README.md
claims/p5/h22/README.md
claims/p5/h22/common-center-kernel-star-component-finite-lambda-zero-all-marking/P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_LAMBDA_ZERO_ALL_MARKING_OBSTRUCTION.md
claims/p5/h22/common-center-kernel-star-component-finite-lambda-zero-all-marking/audit_p5_h22_common_center_kernel_star_component_finite_lambda_zero_all_marking_obstruction.py
claims/p5/h22/common-center-kernel-star-component-finite-lambda-zero-all-marking/verify_p5_h22_common_center_kernel_star_component_finite_lambda_zero_all_marking_obstruction.py
docs/NEXT_INSTANCE_HANDOFF_2026-07-31.md
```

No mathematics or status field may change in that repair.

## Post-move acceptance matrix

The minimum complete scientific closure is exactly three unique executables
and five strictly serial invocations:

1. staying dense-open primary once from repository root, as the
   dependency-integrity row;
2. moved lambda-zero primary from repository root;
3. moved lambda-zero primary by absolute path from a fresh foreign CWD;
4. moved audit from repository root; and
5. moved audit by absolute path from another fresh foreign CWD.

Use exactly:

```text
uv run --quiet --python 3.13 --with sympy python <script>
```

Do not use `python-sat`. Do not retry, reprioritize, kill, or overlap any
row. Every executable starts Singular three times, so the five-row matrix
contains exactly fifteen non-overlapping Singular subprocesses.

The staying dense-open row must retain:

- exact field `Q(r,t)` and component 23;
- label `VERIFIED_PARTIAL_SUPPLEMENT`;
- certificates `D01_dense_open_minor`,
  `cross_contraction_lambda_zero_minor`, and
  `lambda_minus_one_all_markings_full_module`;
- lambda-minus-one closure true;
- all three chronological residual strings; and
- generic-finite, finite-field-proof, and global-resolution fields false.

The moved primary root/foreign pair must be byte- and object-identical and
retain:

- `status: pass`, `field: Q(r,t)`, component 23;
- direction `finite lambda=0 all markings`;
- label `VERIFIED_EMPTY_WITH_PRIOR_FACTOR_COVER`;
- prior cover `h2*h3*H0=0`;
- branches, in order, `lambda_zero_h2_zero`,
  `lambda_zero_h3_zero`, and `lambda_zero_H_zero`;
- `each_branch_mixed_module_full: true`;
- `lambda_zero_all_markings_closed: true`;
- chronological `generic_finite_all_markings_closed: false`;
- the remaining ordinary residual string unchanged; and
- finite-field-proof and global-resolution fields false.

Acceptance must also check algebraically that the selected `H0` equals the
dense-open predecessor's `H|lambda=0`, and independently check
`H0(2,4,3/8)=0` rather than attributing that derivation to the audit.

The audit root/foreign pair must be byte- and object-identical and retain:

- exact `Q`;
- specialization `r=2`, `t=4`, `H0_solution_h3=3/8`;
- `independent_no_repository_imports: true`;
- branch labels `h2_zero_at_r2_t4`, `h3_zero_at_r2_t4`, and
  `H0_zero_at_r2_t4`;
- `audit_only_not_generic_proof: true`; and
- generic-finite, finite-field-proof, and global-resolution fields false.

Every row must return rc=0, empty stderr, and exactly one JSON object. All
three executables are stdout-only and contain no write API. Require zero
generated JSON, empty foreign directories, and clean tracked/index state.
The dense-open audit, shared providers, and later ordinary-residual theorem
do not belong in the minimum replay closure.

After the five scientific rows, run one isolated foreign-CWD import-only
probe per moved module. Then require targeted Ruff `E402,I001`, source
compilation, rewriter fixed point, the full index-complete validation floor,
exact-head CI, and fresh semantic/status plus mechanical/provenance referees.

## Stop conditions

Stop and report rather than executing or repairing if:

- the base, mapping, source blob, raw hash, destination, or manifest record
  differs from this approval;
- `H0 != H|lambda=0`, the prior factor cover is weakened, or the selected
  primary is presented as proving that cover itself;
- the audit is described as a generic proof or complete factor-cover audit;
- `Q(r,t)` is promoted to pointwise special-fibre coverage;
- candidate, partial, or H31 provider status becomes theorem evidence;
- chronological false/`UNKNOWN` fields are edited or used to downgrade the
  later terminal theorem;
- any equation, branch substitution, module check, timeout, assertion, or
  JSON field changes outside the approved path/launcher repair;
- a selected ledger entry or formalization claim is invented;
- a scientific row fails or a root/foreign pair differs;
- the owner-gated H31 fourteen-versus-sixteen conflict is consumed or edited;
  or
- special/projective fibres, component exhaustiveness, `P5 -> Delta3`,
  arbitrary-order gluing, or global resolution is claimed.

Subject to those exact guards, Stage 26 may freeze and execute without
returning to the repository owner for routine mapping approval.
