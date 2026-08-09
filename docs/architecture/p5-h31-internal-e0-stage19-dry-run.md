# P5 H31 internal `E=0` marked fibre - Stage 19 exact migration dry run

Status: **APPROVED FOR AN EXACT FROZEN BATCH under the repository-owner
standing delegation dated 2026-08-08. No move has yet been executed.**

> **Scientific status will not change.** The global Krenn-Gu conjecture
> remains **UNRESOLVED**. This review resolves filesystem ownership only. It
> does not extend the exact internal-divisor result to another divisor or
> component, close weighted `H22`, prove `P5 -> Delta3`, or turn the modular
> audit into the characteristic-zero proof.

## Review authority and baseline

- Exact merged baseline:
  `d7433d7aad1fb6fa0ae26d711b93c8fd54ee80aa`.
- Branch: `codex/stage19-h31-internal-e0-migration`.
- Actual mapping reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.
- Delegated-review test: routine, non-ambiguous, evidence-backed exact layout
  mapping; no scientific status/scope decision, genuinely ambiguous
  proof-boundary decision, or owner-preference architecture choice is needed.
- Batch ID to freeze: `p5-h31-internal-e0-stage19`.
- Approval-time manifest SHA-256:
  `823a73851bc880704a392ebc279cffb21f552ebe1b945dd73e731e9485879adc`.
- Canonical mapping SHA-256:
  `0a345a2e89974d1e7f8b026cd568d1da6ecec62b0337412b9cc9a35c7edecd6a`.

The approval-time manifest SHA is informational and hashes the raw Windows
checkout bytes. The canonical mapping hash is the portable, authoritative
binding of the reviewed old-to-new pairs.

All three records are currently `review_required` with medium classifier
confidence. Classifier confidence is proposal evidence only. Approval comes
from the independent proof-topology, evidence-semantics, documentation, and
mechanical audits and applies only to the mapping below.

## Exact three-file mapping

All three files move flat into
`claims/p5/h31/internal-e0-marked-fibre/`.

| role | source | destination |
|---|---|---|
| theorem | `P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md` | `claims/p5/h31/internal-e0-marked-fibre/P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md` |
| primary | `verify_p5_h31_internal_e0_marked_fibre.py` | `claims/p5/h31/internal-e0-marked-fibre/verify_p5_h31_internal_e0_marked_fibre.py` |
| modular audit | `audit_p5_h31_internal_e0_marked_fibre.py` | `claims/p5/h31/internal-e0-marked-fibre/audit_p5_h31_internal_e0_marked_fibre.py` |

Every source is tracked grandfathered root debt, every destination is absent,
and the durable classifier and generated manifest contain exactly these
source-to-destination pairs. There are no selected destination collisions,
duplicate sources or destinations, double moves, overlap cycles, or
package-name collisions.

All three working-tree source blobs equal the exact baseline Git blobs:

| source | Git blob |
|---|---|
| `P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md` | `1168bd201c15a3fa2db07f5dd09a4890d4bbb6cd` |
| `audit_p5_h31_internal_e0_marked_fibre.py` | `abc0caadc2f10eb572b835684e96ec1def4e6db7` |
| `verify_p5_h31_internal_e0_marked_fibre.py` | `dd97026693496cf3c28ba926c3fe1e31681588f8` |

## Proof-obligation ownership

The selected triple is one complete divisor-scoped proof leaf:

```text
P4 pure-rank-two toric facet + Segre slice reduction (stay P4-owned)
  -> internal E=0 facet of the first pure-compression component
  -> 2 reduced Segre directions x q in {0,2,3} x 2 first-plane charts
  -> 12 exact saturated projections and 24 projection components
  -> 29-chart exact atlas: 27 ordinary residual charts,
     one closure-artifact chart, and one coupled selected-minor unit ideal
  => every marked H31 fibre on that internal divisor is excluded

other divisor/component families stay separately owned;
weighted H22, broader unclosed boundaries/exhaustiveness,
P5 -> Delta3, gluing, and global remain open as stated by their owners
```

The theorem covers every marking on this one divisor: both pure directions,
all three all-rank distinguished coordinates, both projective first-plane
charts, every kernel-row shift, and every binary extension direction. It is
not a generic theorem for a whole component and does not own the other
divisor closures used in the later first-component synthesis.

Evidence axes remain separate:

- the theorem and primary give the exact characteristic-zero obstruction;
- the primary reconstructs all twelve projections and the 29-chart exact
  atlas, including its closure-artifact and coupled-unit-ideal charts;
- the audit does not import the primary and independently enumerates modular
  kernels, projective extension directions, and selected minors over `F5`
  and `F7`;
- the audit nevertheless shares `toric_cases` / `marked_rows` from the root
  generator and hardcodes the displayed projection bases, while its modular
  kernel, extension, and minor route is separate; its independence is claimed
  only downstream of that shared toric/marked-row and projection-data layer;
  and
- finite-field enumeration is QA, not the characteristic-zero proof.

No selected theorem, primary, or audit has a curated theorem-ledger entry.
Migration adds no entry and changes no mathematical status, assumptions,
scope, evidence role, lifecycle, or global-status field.

## Explicit exclusions and pre-existing prose debt

The following remain separately owned:

- `derive_p5_h31_toric_marked_fibre_elimination.py`, which also serves the
  genuine toric-boundary sibling;
- `p5_high_coordinate_tree_chart_cegar.py`,
  `verify_p5_h31_marked_basis_open_branch.py`, and
  `audit_p5_h31_marked_basis_fibre_classification.py`, which are shared root
  utilities;
- the P4 toric-boundary theorem and Segre reduction under `claims/p4/`;
- the finite-family, component-chart, first-plane-infinity, toric-boundary,
  and rank-one-gate H31 obligations for the first component;
- the diagonal-quadric and later component families;
- weighted `H22`, component exhaustiveness outside the statements already
  proved elsewhere, `P5 -> Delta3`, arbitrary-order gluing, and the global
  conjecture.

The selected theorem and marked-basis classification contain pre-existing
checkpoint prose saying that only one rational marked fibre on the second
component had been excluded. The P4 toric-boundary theorem likewise leaves
the second component's generic marked fibre and further-component existence
open. The high-coordinate frontier, root README, and diagonal-quadric
outer-boundary closure instead record complete second-component marked-H31
closure. This is a pre-existing status/provenance conflict outside the
internal-`E=0` theorem's actual scope. Stage 19 does not adjudicate those
artifacts by recency, reopen or promote either statement, or use the disputed
sentence as an input. It preserves the selected theorem byte-identically in
the pure move and leaves final conflict adjudication to a focused
scientific-status audit. The primary's `additional_components_closed: false`
is scope-local: this verifier proves no additional-component result.

## Mechanical repair surface

Both moved Python executables currently derive `ROOT` from their source
directory and import root modules before any bootstrap. After the pure move:

- both install the shared `krenn_gu.bootstrap` before root-module imports;
- `REPO_ROOT, HERE = bootstrap(__file__)` supplies stable ownership;
- `THEOREM`, and the audit's `PRIMARY`, resolve from `HERE`;
- the primary's P4 toric theorem, Segre reduction, shared generator, and
  imported root utilities resolve through `REPO_ROOT`; and
- the audit's shared generator and marked-basis imports resolve through
  `REPO_ROOT`.

Exactly one staying Python consumer needs one operational path retarget:
`verify_p5_high_coordinate_partial_frontier.py` must point its internal-`E=0`
dependency at the new destination. No staying importer or subprocess caller
of either selected module exists.

The deterministic link rewrites also change the bytes of three evidence
documents that staying scripts hash as inputs: the P4 toric-boundary theorem,
the marked-basis classification, and the high-coordinate frontier. Those are
hash/provenance ripples rather than import-path repairs, but their primary and
audit consumers must be included in the staged replay audit rather than
treated as untouched evidence.

A read-only virtual post-move simulation predicts exactly seven Markdown-link
rewrites and two fenced replay-command rewrites across six Markdown files,
with zero ambiguities and zero theorem-ledger relocations:

- one link each in `P5_ALTERNATIVE_STRATEGY_MAP.md`,
  `P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md`,
  `P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`, and the root `README.md`;
- two links in the P4 toric-boundary theorem;
- the moved theorem's P4 link plus both replay commands.

Because two rewritten documents are already ledger-backed, deterministic
hash maintenance must refresh four existing fields while preserving their
statuses and all other semantics:

- the three root-README entries (`open`, `verified_generic`, `partial`) from
  `2d2c48d2364b4b34` to projected `0a2bdc3d8f298425`; and
- the verified high-coordinate frontier entry from `a254bb28a2f2440c` to
  projected `438f42c953f13628`.

Navigation must add this exact scoped non-generic divisor package to
`claims/p5/h31/README.md`, add Stage 19 history, and update the parent P5 H31
directory count from 26 to 27. It must say explicitly that this package is
not the whole first-component forest and does not close other components or
weighted `H22`.

## Projected transitions

| measure | before | after |
|---|---:|---:|
| moved manifest entries | 386 | 389 |
| proposed-high-confidence entries | 243 | 243 |
| review-required entries | 1,386 | 1,383 |
| moved-only manifest root projection | 1,986 | 1,983 |
| high-confidence manifest root projection | 1,743 | 1,740 |
| all-classified manifest root projection | 357 | 357 |
| grandfathered root debt | 1,971 | 1,968 |
| root files | 1,978 | 1,975 |
| root directories | 9 | 9 |
| root entries | 1,987 | 1,984 |
| enforceable retired paths | 386 | 389 |

The move creates no top-level directory and changes no root baseline or
end-state allowlist.

## Baseline replay and acceptance plan

Fresh exact-base replay on 2026-08-08 passed:

- the primary reported `verified: true`, characteristic zero, 12 projection
  runs, 24 projection components, a 29-chart exact atlas (27 ordinary
  residual charts, one projection-closure artifact, and one coupled chart),
  1,172 residual witness products, 32 coupled selected products, and a true
  coupled unit ideal in 107.496 seconds;
- the modular audit reported `verified: true` after 3,976 projection points,
  58,280 binary extensions, and 747,552 selected-minor tests over `F5/F7`;
  and
- `verify_p5_high_coordinate_partial_frontier.py` remained verified while
  retaining `P5_to_Delta3_resolved: false` and
  `global_conjecture_resolved: false`.

After repair, replay both moved executables from repository root by
destination path and from a fresh foreign working directory by absolute
path. Parse one JSON object per run. Remove only the primary's volatile
`elapsed_seconds` and require each root/foreign pair to be otherwise equal.
Require:

- `verified: true` for both;
- two pure directions, orientations `0,2,3`, and two charts;
- 12 projections / 24 components / 29 atlas charts and a true coupled unit
  ideal in the characteristic-zero primary;
- the exact `F5/F7` audit totals above;
- `complete_internal_E0_marked_fibre_excluded: true` and
  `known_component_marked_fibre_excluded: true`; and
- `additional_components_closed: false` in the scope-local primary output
  plus `global: false` in both outputs.

Replay the staying frontier verifier from root and a foreign working
directory. Its self hash and selected dependency hash will change
mechanically, but the two candidate runs must otherwise agree and preserve
the current H31/H22 frontier fields, `P5_to_Delta3_resolved: false`, and
global false. Its ignored `tmp/` output must not create tracked drift.

The complete affected-evidence matrix has 13 executables. Require root and
foreign-CWD normalized-JSON pairs for the two moved scripts and the directly
edited high-coordinate primary. Replay the remaining ten semantically from
repository root (using a disposable copy/sandbox for scripts that write
outputs):

1. P4 toric-boundary primary and audit;
2. `verify_p4_pure_rank_two_toric_slice_segre.py`;
3. `verify_p5_h31_toric_marked_fibre_obstruction.py`;
4. marked-basis classification primary and audit;
5. high-coordinate audit;
6. `audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_independent.py`;
7. `derive_p5_h22_component19_p0_phi_pm_one_ordinary_obstruction_candidate.py`;
8. `derive_p5_h22_component19_p0_qphi_minus_one_axes_compatibility_obstruction.py`.

Their semantic fields must remain fixed while mechanically changed
theorem/dependency hashes update. The two component-19 derivations must remain
`CANDIDATE`. Tracked certificate JSON hashes are historical provenance and
must not be refreshed merely because a linked synthesis document moved. A
mechanically updated live input hash is not a mathematical status change.
After the matrix, require no tracked output drift.

Run isolated foreign-CWD imports for both moved executables under
`uv run --with sympy --with python-sat python -I`. (`python-sat` is required
by the shared marked-basis import surface; a SymPy-only environment is not
sufficient.) Confirm the existing WSL Singular 4.3.2 fallback, compile and
targeted Ruff checks for all three directly affected scripts, the second-pass
rewriter fixed point, the index-complete validation floor, exact-head CI, and
fresh semantic plus mechanical referees before a normal exact-head guarded
merge.

The global Krenn-Gu conjecture remains **UNRESOLVED**.
