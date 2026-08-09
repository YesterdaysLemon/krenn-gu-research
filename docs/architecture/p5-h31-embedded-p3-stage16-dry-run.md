# P5 H31 embedded-P3 — Stage 16 exact migration dry run

Status: **APPROVED FOR AN EXACT FROZEN BATCH under the repository-owner
standing delegation dated 2026-08-08.  No move has yet been executed.**

> **Scientific status will not change.**  The global Krenn–Gu conjecture
> remains **UNRESOLVED**.  This review resolves filesystem ownership only; it
> does not promote a theorem, enlarge a scope, reinterpret an audit, or close
> any H22 obligation.

## Review authority and baseline

- Exact merged baseline:
  `2eda840131e73e699a99b58efb190d5eaf1023c1`.
- Branch: `codex/stage16-h31-embedded-p3-migration`.
- Actual mapping reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.
- Delegated-review test: routine, non-ambiguous, evidence-backed exact layout
  mapping; no scientific status/scope decision, genuinely ambiguous
  proof-boundary decision, or owner-preference architecture choice is needed.
- Batch ID to freeze: `p5-h31-embedded-p3-stage16`.
- Approval-time manifest SHA-256:
  `16ff7b355d83890b1acb321b994eecbfb2f83ac2f5a87c0e7cf2fba127e345b9`.
- Canonical mapping SHA-256:
  `db3bf4cc6309334ffc2a9983456f8674d9df5f22c3f921c969bcc4af414d5fb7`.

Classifier confidence is recorded below as proposal evidence only.  It is not
the approval basis.  Approval comes from the independent ownership/topology
review and applies only to the exact mapping in this document.

## Exact 15-file mapping

Every destination has prefix `claims/p5/h31/embedded-p3/` and preserves the
source basename.

| role | source | pre-execution status / confidence |
|---|---|---|
| theorem | `P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md` | `proposed_high_confidence` / high |
| primary | `verify_p5_h31_embedded_p3_component_generic_obstruction.py` | `proposed_high_confidence` / high |
| audit | `audit_p5_h31_embedded_p3_component_generic_obstruction.py` | `proposed_high_confidence` / high |
| theorem | `P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md` | `review_required` / medium |
| primary | `verify_p5_h31_embedded_p3_component_normalized_boundary.py` | `review_required` / medium |
| audit | `audit_p5_h31_embedded_p3_component_normalized_boundary.py` | `review_required` / medium |
| theorem | `P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md` | `review_required` / medium |
| primary | `verify_p5_h31_embedded_p3_component_support_two_boundary.py` | `review_required` / medium |
| audit | `audit_p5_h31_embedded_p3_component_support_two_boundary.py` | `review_required` / medium |
| theorem | `P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md` | `review_required` / medium |
| primary | `verify_p5_h31_embedded_p3_component_r_zero_boundary.py` | `review_required` / medium |
| audit | `audit_p5_h31_embedded_p3_component_r_zero_boundary.py` | `review_required` / medium |
| theorem | `P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md` | `review_required` / medium |
| primary | `verify_p5_h31_embedded_p3_component_projective_closure.py` | `review_required` / medium |
| audit | `audit_p5_h31_embedded_p3_component_projective_closure.py` | `review_required` / medium |

The destination directory is absent, every source is tracked root debt, and
the manifest contains exactly these 15 source-to-destination pairs.

## Proof-obligation ownership

The H31 files form one asymmetric but complete closure forest:

```text
P4 embedded-P3 component anchor (already migrated; stays)
  -> dense generic H31 obstruction
  -> normalized A*B*r != 0 chart
       + support-two A=0, B!=0 divisor
       + r=0, A*B!=0 divisor
       => complete affine B!=0 family
  -> projective symmetry/case-union closure
       consumes normalized + support-two + r=0
       => full nonzero embedded-P3 component H31 fibre empty
```

The projective theorem explicitly consumes all three boundary children and
proves their chart union exhaustive.  No H31 embedded-P3 obligation child is
left at root.  The already-migrated P4 component is an upstream anchor; the
common-active wall, H22 program, and high-coordinate synthesis are downstream
or sibling consumers, not package-owned descendants.

Evidence axes remain distinct:

- the curated ledger indexes only the generic triple as `verified_generic`;
- the owning H31 documents record the normalized, divisor, and projective
  characteristic-zero conclusions at their stated scopes;
- the five audits are modular corroboration, not the characteristic-zero
  proof; and
- pure-component exhaustiveness and global resolution remain false.

The migration rewriter may relocate the generic ledger triple and recompute
its document hash, but must retain `status: verified_generic`.  Its stale
runtime/backend metadata is separately verified evidence metadata and may be
corrected from `minutes (sympy + Singular)` / `Singular >= 4.3` to
`seconds-to-minutes (sympy)` / no external binaries; this changes neither
status nor theorem scope.

## Explicit exclusions

The complete H22 embedded-P3 program stays at root.  It is a separate weighted
obligation with refuted `r0=0` lineage, later endpoint repairs, and open
projective coverage.  This includes its generic/rank-two/rank-one triples,
projective-coverage and `r=0` records, endpoint records, and three exploratory
derivations.

Also excluded are the already-migrated P4 embedded-P3 anchor, the shared root
marked-basis helper, common-active p+q wall records, the high-coordinate
frontier, and historical reports/provenance.  Cross-links, imports, hashes,
and subprocess calls do not transfer their ownership into this package.

## Mechanical repair surface

Four moved primaries (generic, normalized, support-two, and `r=0`) import the
shared root marked-basis helper before repository bootstrap.  After the pure
move they must bootstrap first, import shared/root and co-moved siblings after
bootstrap, use `HERE` for co-located theorem files, and use `REPO_ROOT` for the
already-migrated P4 anchor.  The projective primary and all five audits are
local-only.

Nine staying Python consumers require operational paths to the moved
destinations:

1. `verify_p5_h22_embedded_p3_component_generic_obstruction.py`;
2. `verify_p5_h22_embedded_p3_component_rank_two_line_boundary.py`;
3. `derive_p5_h22_embedded_p3_component_r_zero_boundary_obstruction.py`;
4. `audit_p5_h22_embedded_p3_component_r_zero_boundary_independent.py`;
5. `derive_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_obstruction_candidate.py`;
6. `audit_p5_h22_embedded_p3_component_r_zero_t_nonzero_weight_endpoints_verifier.py`;
7. `verify_p5_h31_common_active_binary_triangle_p_plus_q_boundary_obstruction.py`;
8. `audit_p5_h31_common_active_binary_triangle_p_plus_q_boundary_obstruction.py`; and
9. `verify_p5_high_coordinate_partial_frontier.py`.

Frozen H22 output hashes remain historical provenance.  Operational
paths/commands change; recorded historical input hashes do not.

A read-only virtual post-move rewriter simulation predicts 21 Markdown-link
rewrites and 11 fenced replay-command rewrites across 14 Markdown files, plus
relocation of one ledger triple.  Navigation must add this five-triple closure
to `claims/p5/h31/README.md`, remove it from that page's pending list, qualify any
generic-only blanket wording, and update `claims/p5/README.md` counts to H31
`22` and H22 `18`.

## Projected transitions

| measure | before | after |
|---|---:|---:|
| moved manifest entries | 353 | 368 |
| proposed-high-confidence entries | 249 | 246 |
| review-required entries | 1,413 | 1,401 |
| grandfathered root debt | 2,004 | 1,989 |
| root files | 2,011 | 1,996 |
| root entries | 2,020 | 2,005 |

The move creates no new top-level directory and changes no allowlist or debt
baseline.

## Replay and acceptance plan

Replay all five primaries and all five audits from repository root using their
destination paths, then repeat all ten by absolute path from a foreign working
directory.  Baseline package time is about 18.7 seconds.  Acceptance preserves
these exact semantic boundaries:

- generic: generic empty true; component boundary/census/global false;
- normalized: complete normalized chart true; projective/global false;
- support-two: stated `A=0, B!=0` fibre true; remaining/global false;
- `r=0`: divisor and affine `B!=0` family true; projective/global false; and
- projective: whole projective ninth-component H31 fibre empty; component
  census/global false.

Replay all nine staying consumers after repair.  The historical H22 `r=0`
audit must remain `REFUTED`/`UNKNOWN` at its recorded scope, later endpoint
repairs must pass, common-active remains wall-scoped with H22/global false, and
the high-coordinate frontier must retain `P5_to_Delta3_resolved=false` and
`global_conjecture_resolved=false`.

Final acceptance requires pure R100 moves, exact batch provenance, blob
identity, root/manifest arithmetic, no stale operational paths, full hygiene,
all migration and lattice tests, rewrite fixed point, clean exact head, normal
PR CI, and a fresh Tier-2 semantic plus mechanical review because this batch
repairs shared executable paths and ledger evidence metadata.
