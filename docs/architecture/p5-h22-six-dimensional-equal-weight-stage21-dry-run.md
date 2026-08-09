# P5 H22 six-dimensional equal-weight leaf - Stage 21 exact migration dry run

Status: **APPROVED FOR AN EXACT FROZEN BATCH under the repository-owner
standing delegation dated 2026-08-08. No move has yet been executed.**

> **Scientific status will not change.** The global Krenn-Gu conjecture
> remains **UNRESOLVED**. This review resolves filesystem ownership only. It
> does not promote an equal-weight function-field obstruction to pointwise
> closure of the full geometric divisor, close other weight or parameter
> boundaries, prove all weighted `H22` empty, or settle the global problem.

## Review authority and audited baseline

- Exact merged baseline:
  `7352a0615ae1bfbccb118a1a0ec2d725ea432ff1`.
- Branch: `codex/stage21-h22-sixdim-equal-weight-migration`.
- Actual mapping reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.
- Delegated-review test: routine, non-ambiguous, evidence-backed exact layout
  mapping; no scientific status/scope decision, ambiguous proof-boundary
  decision, or owner-preference architecture choice is required.
- Batch ID to freeze: `p5-h22-six-dimensional-equal-weight-stage21`.
- Approval-time raw Windows-checkout manifest SHA-256:
  `3b82e4fec1304eea532dd7f88eb816c55d0048ea50a2fc2c18ecb13402b9c181`.
- Canonical mapping SHA-256:
  `f7427206126ecc290b0a926c1731eb5eb557aca7d784547d4c64df2dc2b41cf0`.

The manifest hash is informational approval-time provenance over raw CRLF
checkout bytes. The canonical mapping hash is the portable authority for the
reviewed old-to-new pairs.

The theorem record is currently `proposed_high_confidence` with high
classifier confidence. The two script records are `review_required` with
medium confidence. Classifier confidence is proposal evidence only. Approval
comes from independent proof-topology/status and mechanical/consumer audits
and applies only to the exact mapping below.

## Exact three-file mapping

All three files move flat into the existing
`claims/p5/h22/six-dimensional/` package.

| role | source | destination |
|---|---|---|
| theorem | `P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md` | `claims/p5/h22/six-dimensional/P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md` |
| characteristic-zero primary | `verify_p5_h22_six_dimensional_equal_weight_binary_obstruction.py` | `claims/p5/h22/six-dimensional/verify_p5_h22_six_dimensional_equal_weight_binary_obstruction.py` |
| modular audit | `audit_p5_h22_six_dimensional_equal_weight_binary_obstruction.py` | `claims/p5/h22/six-dimensional/audit_p5_h22_six_dimensional_equal_weight_binary_obstruction.py` |

Every source is tracked grandfathered root debt, every destination is absent,
and the durable classifier and generated manifest contain exactly these
source-to-destination pairs. There are no selected duplicate sources or
destinations, case-folded destination collisions, double moves, overlap
cycles, or package-name collisions.

The exact baseline source identities are:

| source | Git blob | raw Windows-checkout SHA-256 |
|---|---|---|
| theorem | `3c5e8c88dab90ca2c8d6d17c9e45249ba207d02d` | `1c940a703d6406c8af03bcbfbfec9d903b5afcdf529d368f598d2bd1884672ff` |
| audit | `b9a477a53818bbda85d4458e279edce6dc34d8ae` | `dd51fb009384737636d1146902174ecbfd45aa7923bb308f0f6ae35f49dbb8e2` |
| primary | `bbe942bf8f1e19a6da8543b32d1762f67d236169` | `f26c47ce85070c965ee607cb5647a754cc856c4369754cb7e492a9cdc5938e84` |

## Proof-obligation ownership and exact scope

The selected triple is one complete, separable binary-incidence proof leaf:

```text
generic point of the six-dimensional P4 component over C(s,d,u,v)
  -> every nonzero marked basis on the displayed function-field chart
  -> equal source weight r=1
  -> diagonal contractions D01 and D23
  -> 14 mixed binary equations plus two nonzero diagonals
  -> both exact saturated projections are the unit ideal
  => neither diagonal admits a binary Delta2 neighbour on this chart
  => the equal-weight r=1 binary H22 incidence is empty at that generic point

opposite and coupled slopes, parameter/projective boundaries,
pointwise divisor closure, all H22, gluing, and global remain outside
```

The mandatory scope description is:

> The selected theorem is an exact characteristic-zero binary-incidence
> obstruction at the **generic component function-field normal-form point**
> `K=C(s,d,u,v)` after the equal-weight normalization `r=1`. It covers every
> marked basis and fifth-coordinate extension at that generic point. It is
> **not a pointwise theorem for the full geometric `r=1` divisor**.

The four affine marking parameters exhaust marked bases over the displayed
function-field normal form; they do not quantify over every specialization of
the component parameters.

The migrated generic six-dimensional theorem identifies setting `r=1` early
as the valid exceptional equal-weight calculation. The boundary-divisor atlas
lists this theorem as the `r=1` binary certificate and separately leaves
component-parameter and projective boundaries open. Stage 21 reads that
shorthand only at the generic component function-field normal-form point; it
does not promote it to pointwise closure of the full geometric `r=1` divisor.

Evidence roles remain distinct:

- the theorem and primary give the exact characteristic-zero identities and
  two unit-ideal projections;
- the primary reconstructs the P4 apolar basis, every marked basis, both
  diagonal incidence systems, and their exact eliminations;
- the audit imports no primary implementation and separately implements a
  dynamic-programming permanent, modular nullspace calculation, and exhaustive
  `p^4` marking census over `F5` and `F7`; and
- the audit still uses the same theorem-specified normal form/model and one
  fixed admissible component sample in each field, so independence is claimed
  only downstream of that shared mathematical construction; the finite-field
  census is corroboration only, not the characteristic-zero proof and not
  evidence for excluded slope or parameter boundaries.

No selected artifact has a curated theorem-ledger entry. Migration adds no
entry and changes no mathematical status, assumptions, quantifiers, scope,
evidence role, lifecycle, or global-status field.

## Explicit exclusions and ownership boundary

The following remain outside this leaf and retain the distinct statuses
recorded by their owning artifacts:

- opposite weight `r=-1`;
- the marking-coupled `pr-p+1=0` divisor and the survivor-degeneration
  `ru-r+u-v=0` divisor;
- slope/parameter intersections and every component-parameter or projective
  boundary not covered by the function-field calculation;
- a pointwise theorem over the full equal-weight geometric divisor;
- this theorem makes no claim about other pure components; their existing
  generic, boundary, and open statuses remain unchanged, and component
  exhaustiveness is outside this leaf;
- all weighted `H22`, `P5 -> Delta3`, arbitrary-order gluing, and the global
  conjecture.

The P4 six-dimensional theorem and primary are upstream dependencies and stay
in their existing claim package. The high-coordinate Singular timeout helper
is a 44-consumer root utility and stays at root. No unselected generator,
certificate, theorem child, or proof leaf is uniquely owned by this triple.
The nearby common-center and H31 boundary forests remain separate work.

The two previously recorded scientific-status conflicts are unrelated: this
leaf consumes neither the second-component `H31` status prose nor the
common-active `p+q=0` weighted-`H22` wall. Stage 21 neither adjudicates nor
changes either conflict.

## Mechanical repair surface

Both selected scripts currently derive `ROOT` from repository root. The
primary also imports the root high-coordinate helper before any bootstrap.
After the pure move:

- both scripts install shared `krenn_gu.bootstrap` before root imports;
- `REPO_ROOT, HERE = bootstrap(__file__)` supplies stable ownership;
- the selected theorem and the audit's sibling primary resolve from `HERE`;
- the P4 theorem/primary and high-coordinate helper resolve through
  `REPO_ROOT`; and
- both ignored JSON outputs continue to write under repository `tmp/`, not a
  package-local directory.

Exactly one staying Python consumer needs one operational retarget:
`verify_p5_high_coordinate_partial_frontier.py` must point its selected
theorem dependency at the destination. No staying module importer or
subprocess caller targets either selected script name.

The deterministic virtual post-move rewriter predicts exactly five
Markdown-link rewrites and two fenced replay-command rewrites across five
Markdown files, with zero ambiguities and zero theorem-ledger relocations:

- the moved theorem receives its reanchored P4 link and two full destination
  replay commands;
- `P5_ALTERNATIVE_STRATEGY_MAP.md`;
- `P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`;
- the migrated coincident-support generic theorem; and
- the existing six-dimensional generic theorem.

Three existing ledger hashes must refresh mechanically while every status and
semantic field remains fixed:

- high-coordinate frontier: `56b23fe36b5d97d8` -> projected
  `66ea30eaa865fd66` (`verified` unchanged);
- coincident-support H22 generic: `4c4d8929eb9bb7c7` -> projected
  `ed0df77897f3f9f5` (`verified_generic` unchanged); and
- six-dimensional H22 generic: `72d9943a359888ec` -> projected
  `401808df53fb1a09` (`verified_generic` unchanged).

These are normalized-LF index-blob hashes, not raw CRLF working-tree hashes.
The moved theorem's projected normalized-LF post-rewriter SHA-256 is
`65f049ebbbbcc13444cbc45c125b4999b94842e3a05de018b8d1760e6701048c`.

Navigation must amend `claims/p5/h22/README.md` so it no longer says every
artifact is generic, add a separately labelled six-dimensional equal-weight
function-field normal-form-point section that explicitly says it is not
pointwise closure of the full geometric `r=1` divisor, record the Stage 21
batch/mapping hash, and preserve all other slope and pointwise boundaries.
Parent P5 navigation must add the same scoped H22 exception. The H22
package-directory count remains 18 because the destination already exists.

## Projected transitions

| measure | before | after |
|---|---:|---:|
| manifest `moved` | 392 | 395 |
| manifest `proposed_high_confidence` | 243 | 242 |
| manifest `review_required` | 1,380 | 1,378 |
| moved-only manifest root projection | 1,980 | 1,977 |
| high-confidence manifest root projection | 1,737 | 1,735 |
| all-classified manifest root projection | 357 | 357 |
| measured root files | 1,972 | 1,969 |
| measured root directories | 9 | 9 |
| measured root entries | 1,981 | 1,978 |
| grandfathered root debt | 1,965 | 1,962 |
| new root debt | 0 | 0 |
| enforceable retired/provenance paths | 392 | 395 |

The move creates no top-level directory and changes no root baseline or
end-state allowlist.

## Exact baseline replay

The first attempted primary command used `uv run --with sympy` and failed in
1.305 seconds before mathematical computation because the imported shared
helper requires `python-sat`. It returned no JSON and the audit was not
started. This is an environment/dependency failure, not theorem evidence.

One corrected serial replay then used
`uv run --with sympy --with python-sat python` for each selected script. The
first corrected JSON results were preserved; no solver rerun was triggered by
a post-parse assertion.

The characteristic-zero primary returned rc=0 and empty stderr in 53.813
seconds:

- field `C(s,d,u,v)` and pure coefficient `2*s*u`;
- four marking and eight extension parameters;
- fourteen mixed equations per diagonal;
- exact saturated projections `D01=(1)` and `D23=(1)`;
- both binary-`Delta2`-extension-exists flags false;
- equal-weight binary incidence empty true; and
- weighted slopes, generic H22 incidence, component boundaries, all
  components, all H22, and global resolution false.

Those false values are the selected primary's scope-local JSON fields: they
mean only "not established by this verifier." In particular,
`generic_H22_incidence_on_six_dimensional_component_empty: false` does not
contradict or downgrade the separately migrated generic weighted theorem.

The modular audit returned rc=0 and empty stderr in 24.916 seconds:

- `audited` and `independent_of_primary_imports` true;
- 625 `F5` plus 2,401 `F7` markings for each of two diagonals, 6,052 total;
- zero viable binary-`Delta2` markings;
- 3,026 direct `D23` two-row checks;
- both modular incidence fibres empty true; and
- finite-field results explicitly corroborative only.

Both generated JSON files live only under ignored repository `tmp/`. Native
Singular is absent; the established WSL Singular 4.3.2 fallback completed the
exact elimination. The required environment is Python 3.13, SymPy,
`python-sat`, WSL `/usr/bin/timeout`, and Singular.

## Post-move acceptance matrix

Use a checked schema-aware assertion manifest and preserve each first rc=0,
empty-stderr, valid-JSON output before semantic assertions. A wrapper error
must not automatically launch a solver rerun or become mathematical evidence.

Run the moved primary and audit from repository root by destination-relative
path and from a fresh foreign working directory by absolute path under
`uv run --with sympy --with python-sat python -I`. Compare each pair exactly,
normalizing only fields proven volatile by the baseline. Require the exact
scope and conservative false fields above. Run the directly retargeted
high-coordinate primary from root and foreign CWD and preserve its current
scientific fields.

Rewritten evidence-document bytes require replay of the moved pair and every
direct hash/provenance consumer of the changed scientific documents. The
complete closure is exactly these eleven unique scripts:

1. `claims/p5/h22/six-dimensional/verify_p5_h22_six_dimensional_equal_weight_binary_obstruction.py`;
2. `claims/p5/h22/six-dimensional/audit_p5_h22_six_dimensional_equal_weight_binary_obstruction.py`;
3. `claims/p5/h22/six-dimensional/verify_p5_h22_six_dimensional_component_generic_obstruction.py`;
4. `claims/p5/h22/six-dimensional/audit_p5_h22_six_dimensional_component_generic_obstruction.py`;
5. `claims/p5/h22/coincident-support/verify_p5_h22_coincident_support_component_generic_obstruction.py`;
6. `claims/p5/h22/coincident-support/audit_p5_h22_coincident_support_component_generic_obstruction.py`;
7. `verify_p5_high_coordinate_partial_frontier.py`;
8. `audit_p5_high_coordinate_partial_frontier.py`;
9. `audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_independent.py`;
10. `derive_p5_h22_component19_p0_phi_pm_one_ordinary_obstruction_candidate.py`; and
11. `derive_p5_h22_component19_p0_qphi_minus_one_axes_compatibility_obstruction.py`.

The first eight write only ignored `tmp/` JSON plus stdout; the last three are
stdout-only. No executable consumes those ignored JSON outputs. Five dated
tracked provenance artifacts pin an older high-coordinate hash and already
differ from current HEAD; they remain historical and must not be refreshed.

Expected theorem/dependency/self hashes may change mechanically. Mathematical
scope fields must not. The component-19 derivations remain `CANDIDATE`; the
generic theorems remain `verified_generic`; high-coordinate, H22,
`P5 -> Delta3`, and global fields retain their current exact boundaries.
Historical tracked certificate hashes do not refresh merely because a linked
synthesis document changed. Require no tracked output drift.

Both moved modules must pass isolated foreign-CWD import probes with SymPy and
`python-sat`. Confirm targeted Ruff/byte compilation, rewriter fixed point,
the index-complete validation floor, exact-head CI, and fresh semantic plus
mechanical final referees before a normal head-guarded merge.

The global Krenn-Gu conjecture remains **UNRESOLVED**.
