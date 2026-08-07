# Stage 4 dry-run: remaining high-confidence P4 pure-component packages

Generated before execution, from the tree at the Stage 4 starting
SHA `1d96829` (merged `main` including PR #31, tagged
`stage4-start`).

Approval artifact: `catalog/batches/p4-components-stage4.json`
(produced with this report).  Approval:

```text
YesterdaysLemon (repository owner), Stage 4 P4 component migration instruction
```

applies only to the exact generated mappings recorded in that batch
file; it does not approve other P4 files or later batches.

## Scope and stop-condition verdict

All six remaining high-confidence P4 `*_PURE_COMPONENT` triples were
verified against current `main`:

- every theorem document, verifier, and audit exists at the root;
- every manifest record is `proposed_high_confidence` with confidence
  `high` and destination
  `claims/p4/components/<family>/<same filename>`;
- ownership is unambiguous in all six cases (exact-stem triple, no
  shared verifier inside a triple);
- no candidate required mathematical refactoring to move;
- the dependency chain mixed-orientation → disjoint-mixed-star →
  all-rank-one-triangle → P5 consumers closes inside this batch plus
  already-repaired consumers.

**No package is excluded. Batch: 6 packages / 18 files** (target hit;
well under the 30-file ceiling; minimum of 4 exceeded).

## Package summary

| package | theorem | verifier | audit | ownership confidence | verifier runtime | audit runtime | external binaries |
|---|---|---|---|---|---|---|---|
| all-rank-one-triangle | P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md | verify_p4_all_rank_one_triangle_pure_component.py | audit_p4_all_rank_one_triangle_pure_component.py | high | ~2 s (pure sympy; pre-move replay rc=0) | ~3 s (pure sympy) | none |
| diagonal-quadric | P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md | verify_p4_diagonal_quadric_pure_component.py | audit_p4_diagonal_quadric_pure_component.py | high | ~2 s (pure sympy; pre-move replay rc=0) | ~1 s (pure sympy) | none |
| embedded-p3 | P4_EMBEDDED_P3_PURE_COMPONENT.md | verify_p4_embedded_p3_pure_component.py | audit_p4_embedded_p3_pure_component.py | high | ~2 s (pure sympy; pre-move replay rc=0) | ~1 s (pure sympy) | none |
| mixed-orientation | P4_MIXED_ORIENTATION_PURE_COMPONENT.md | verify_p4_mixed_orientation_pure_component.py | audit_p4_mixed_orientation_pure_component.py | high | Singular ds decomposition, 300 s fail-closed timeout (WSL fallback) | ~3 s (pure sympy, modular) | Singular (verifier only) |
| single-word-quadrilateral | P4_SINGLE_WORD_QUADRILATERAL_PURE_COMPONENT.md | verify_p4_single_word_quadrilateral_pure_component.py | audit_p4_single_word_quadrilateral_pure_component.py | high | one Singular ds slice, 3600 s fail-closed timeout; NO native-Windows fallback — replayed under WSL python | two modular Singular slices, 900 s each; NO native-Windows fallback — replayed under WSL python | Singular (verifier + audit) |
| six-dimensional | P4_SIX_DIMENSIONAL_PURE_COMPONENT.md | verify_p4_six_dimensional_pure_component.py | audit_p4_six_dimensional_pure_component.py | high | ~2 s (pure sympy; pre-move replay rc=0) | ~1 s (pure sympy) | none |

Pre-move baselines (run from root on `stage4-start`): all-rank-one
triangle, diagonal-quadric, embedded-p3, six-dimensional verifiers
exit 0 in ~2 s each; mixed-orientation and single-word-quadrilateral
pre-move baselines are recorded in the Stage 4 report.

## File mapping (exact, 18 moves)

| old path | new path |
|---|---|
| P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md | claims/p4/components/all-rank-one-triangle/P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md |
| P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md | claims/p4/components/diagonal-quadric/P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md |
| P4_EMBEDDED_P3_PURE_COMPONENT.md | claims/p4/components/embedded-p3/P4_EMBEDDED_P3_PURE_COMPONENT.md |
| P4_MIXED_ORIENTATION_PURE_COMPONENT.md | claims/p4/components/mixed-orientation/P4_MIXED_ORIENTATION_PURE_COMPONENT.md |
| P4_SINGLE_WORD_QUADRILATERAL_PURE_COMPONENT.md | claims/p4/components/single-word-quadrilateral/P4_SINGLE_WORD_QUADRILATERAL_PURE_COMPONENT.md |
| P4_SIX_DIMENSIONAL_PURE_COMPONENT.md | claims/p4/components/six-dimensional/P4_SIX_DIMENSIONAL_PURE_COMPONENT.md |
| verify_p4_all_rank_one_triangle_pure_component.py | claims/p4/components/all-rank-one-triangle/verify_p4_all_rank_one_triangle_pure_component.py |
| verify_p4_diagonal_quadric_pure_component.py | claims/p4/components/diagonal-quadric/verify_p4_diagonal_quadric_pure_component.py |
| verify_p4_embedded_p3_pure_component.py | claims/p4/components/embedded-p3/verify_p4_embedded_p3_pure_component.py |
| verify_p4_mixed_orientation_pure_component.py | claims/p4/components/mixed-orientation/verify_p4_mixed_orientation_pure_component.py |
| verify_p4_single_word_quadrilateral_pure_component.py | claims/p4/components/single-word-quadrilateral/verify_p4_single_word_quadrilateral_pure_component.py |
| verify_p4_six_dimensional_pure_component.py | claims/p4/components/six-dimensional/verify_p4_six_dimensional_pure_component.py |
| audit_p4_all_rank_one_triangle_pure_component.py | claims/p4/components/all-rank-one-triangle/audit_p4_all_rank_one_triangle_pure_component.py |
| audit_p4_diagonal_quadric_pure_component.py | claims/p4/components/diagonal-quadric/audit_p4_diagonal_quadric_pure_component.py |
| audit_p4_embedded_p3_pure_component.py | claims/p4/components/embedded-p3/audit_p4_embedded_p3_pure_component.py |
| audit_p4_mixed_orientation_pure_component.py | claims/p4/components/mixed-orientation/audit_p4_mixed_orientation_pure_component.py |
| audit_p4_single_word_quadrilateral_pure_component.py | claims/p4/components/single-word-quadrilateral/audit_p4_single_word_quadrilateral_pure_component.py |
| audit_p4_six_dimensional_pure_component.py | claims/p4/components/six-dimensional/audit_p4_six_dimensional_pure_component.py |

## Dependency summary

### The dependency chain this batch must keep usable

```text
verify_p4_mixed_orientation_pure_component   (moving: mixed-orientation)
        ^ imported by
verify_p4_disjoint_mixed_star_pure_component (moved Stage 3: disjoint-mixed-star)
        ^ imported by
verify_p4_all_rank_one_triangle_pure_component (moving: all-rank-one-triangle)
        ^ guarded-imported by
verify_p5_h22_all_rank_one_triangle_..._generic_obstruction.py (stays at root)
verify_p5_h31_all_rank_one_triangle_..._generic_obstruction.py (stays at root)
```

Every arrow is preserved by the shared import helper
`krenn_gu.bootstrap.expose_claim_package` (added in Stage 4 Commit A):
each bare-name importer exposes the moved package directory through the
helper instead of a per-importer `sys.path` shim.

### Per moved Python script

| moved script | imports | importers | shared dependencies | downstream consumers (stay put) |
|---|---|---|---|---|
| verify_p4_all_rank_one_triangle_pure_component.py | verify_p4_disjoint_mixed_star_pure_component (moved S3); verify_p4_mixed_orientation_pure_component (moving in THIS batch) | verify_p5_h22_all_rank_one_triangle_...py (guarded); verify_p5_h31_all_rank_one_triangle_...py (guarded) | — | the two P5 AROT verifiers: COMPONENT doc + COMPONENT_PRIMARY constants |
| audit_p4_all_rank_one_triangle_pure_component.py | none (stdlib + sympy; independent) | none | — | — |
| verify_p4_diagonal_quadric_pure_component.py | none | none | hashes P4_PURE_RANK_TWO_COMPONENT_THEOREM.md, P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md (stay at root) | verify_p5_h31_diagonal_quadric_component_point.py, ..._curve_marked_fibre.py (COMPONENT + COMPONENT_PRIMARY hashes); 7 more H31 DQ scripts hash the COMPONENT doc |
| audit_p4_diagonal_quadric_pure_component.py | none (independent) | none | — | — |
| verify_p4_embedded_p3_pure_component.py | none | none | hashes P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md (stays) | verify_p5_h22/h31_embedded_p3_component_generic_obstruction.py (COMPONENT doc constants) |
| audit_p4_embedded_p3_pure_component.py | none (independent, modular) | none | — | — |
| verify_p4_mixed_orientation_pure_component.py | none (stdlib + sympy + Singular subprocess) | verify_p4_disjoint_mixed_star_pure_component (moved S3); verify_p4_all_rank_one_triangle_pure_component (moving) | hashes four root classification docs | verify_p5_h31_mixed_orientation_...py (COMPONENT_PRIMARY hash); verify_p4_common_singleton_component.py fragment scan (repaired Commit A via manifest-aware resolver) |
| audit_p4_mixed_orientation_pure_component.py | none (independent, modular) | none | — | — |
| verify_p4_single_word_quadrilateral_pure_component.py | none | none | hashes P4_INOUT_PATH_STRATUM_WORKING_NOTE.md (stays) + snapshot README (research_snapshots/, historical, untouched) | none |
| audit_p4_single_word_quadrilateral_pure_component.py | none (independent) | none | — | none |
| verify_p4_six_dimensional_pure_component.py | none | none | hashes P4_MIXED_ORIENTATION doc (moving in this batch → HERE-relative), P4_RADICAL_STAR_...md (stays) | verify_p5_h22_six_dimensional_..._generic.py, ..._equal_weight_binary.py, verify_p5_h31_six_dimensional_...py (COMPONENT + COMPONENT_PRIMARY hashes) |
| audit_p4_six_dimensional_pure_component.py | none (independent) | none | — | — |

### Python consumers repaired in Commit C (staying files)

Constants pointing at moved files (doc hashes / existence guards /
guarded imports) are repointed to `claims/p4/components/<family>/`:

```text
verify_p5_h22_all_rank_one_triangle_component_generic_obstruction.py
verify_p5_h31_all_rank_one_triangle_component_generic_obstruction.py
verify_p5_h31_mixed_orientation_component_generic_obstruction.py
verify_p5_h31_diagonal_quadric_component_point.py
verify_p5_h31_diagonal_quadric_curve_marked_fibre.py
verify_p5_h31_diagonal_quadric_e_curve_marked_fibre.py
verify_p5_h31_diagonal_quadric_elliptic_generic.py
verify_p5_h31_diagonal_quadric_h0_ruling.py
verify_p5_h31_diagonal_quadric_outer_boundary.py
verify_p5_h31_diagonal_quadric_pure_direction_curve.py
verify_p5_h22_six_dimensional_component_generic_obstruction.py
verify_p5_h22_six_dimensional_equal_weight_binary_obstruction.py
verify_p5_h31_six_dimensional_component_generic_obstruction.py
verify_p5_h22_diagonal_quadric_component_generic_obstruction.py
verify_p5_h22_mixed_orientation_component_generic_obstruction.py
verify_p5_h22_embedded_p3_component_generic_obstruction.py
verify_p5_h31_embedded_p3_component_generic_obstruction.py
verify_p5_high_coordinate_partial_frontier.py
verify_p4_diagonal_quadric_one_three_components.py
verify_p4_mixed_determinantal_prime_classification.py
verify_p4_radical_star_component_classification.py
```

Already repaired in Commit A:

- `verify_p4_common_singleton_component.py` — its fragment inventory
  was broken on `stage4-start` itself (it read the Stage-3-moved
  disjoint-mixed-star verifier from root); fixed with a
  manifest-aware path resolver before any Stage 4 move.
- The five Stage 3 per-importer `sys.path` shims for the moved
  disjoint-mixed-star package (one root H31 script + four moved H22
  scripts) now call `expose_claim_package`.

### Markdown inbound links (to the six theorem docs)

49 links across 39 root/claims docs (plus 2 historical text mentions
in `docs/research-notes.md`, which are prose, not links, and stay):

| theorem doc | inbound links |
|---|---|
| P4_ALL_RANK_ONE_TRIANGLE_PURE_COMPONENT.md | 4 (README, P4_INOUT_PATH_STRATUM_WORKING_NOTE, P5_H22_AROT doc, P5_H31_AROT doc) |
| P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md | 13 (README + 12 P4/P5 docs) |
| P4_EMBEDDED_P3_PURE_COMPONENT.md | 10 (README + 5 P4 docs + 2 P5 docs + LITERATURE_REVIEW + moved DMS theorem doc) |
| P4_MIXED_ORIENTATION_PURE_COMPONENT.md | 6 (3 root P4/P5 docs + 2 P5 theorem docs + P4_SIX_DIMENSIONAL which also moves) |
| P4_SINGLE_WORD_QUADRILATERAL_PURE_COMPONENT.md | 3 (README, P4_INOUT_PATH_STRATUM, moved split-pair theorem doc) |
| P4_SIX_DIMENSIONAL_PURE_COMPONENT.md | 13 links in 12 files (README + 8 root docs + 3 P5 docs; P4_OVERLAPPING_SECANT_LOWER_PAIR links twice) |

The rewriter re-anchors these mechanically; the moved theorem docs'
own outbound links (21 total) are re-anchored relative to their new
locations by the same pass.

### Replay commands affected

Each of the six theorem docs fences its own `python verify_…py` /
`python audit_…py` commands (12 commands).  The rewriter repoints
single-line forms; the two continuation-line forms
(`mixed-orientation`, and the Stage 3 `disjoint-mixed-star` leftover)
and the `uv run` form (`embedded-p3`) are repaired manually in
Commit C (see "Machinery gaps").

### Snapshot dependencies

`verify_p4_single_word_quadrilateral_pure_component.py` hashes
`research_snapshots/2026-08-04-p4-exhaustiveness-sweep-census-thirteen/README.md`.
Snapshots are historical provenance and are NOT moved; the constant
switches to REPO_ROOT-relative.

### Ledger references

Zero.  `catalog/theorem-ledger.json` (85 entries, curated partial
index) contains no entry whose `document`, `primary_verifier`, or
`independent_audit` references any of the 18 files.  No entries are
repointed; committed-blob hashes of ledger docs whose content changes
during rewrites (e.g. `README.md`,
`P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`) are refreshed in Commit D.
No six new ledger entries are fabricated.

## Integrity summary

| measure | value |
|---|---|
| member count | 18 |
| package count | 6 |
| destination collisions | none (all six package dirs are new) |
| source/destination cycles | none (no moved file is the destination of another move) |
| expected stale-path count increase | +18 (all root→package basename-preserving moves; 53 → 71) |
| expected root-entry decrease | −18 (2,319 → 2,301; all 18 sources are root files) |
| ledger entries affected | 0 repointed; hash refresh only for touched ledger docs |
| Markdown references affected | 49 inbound links + 21 outbound links in moved docs + 12 replay fences |
| replay commands affected | 12 (six verifiers + six audits) |
| manifest summary expectations | moved 53 → 71; proposed_high_confidence 379 → 361; projected_root_if_moved_only 2,319 → 2,301 (executor recomputes, no rebuild) |

## Exclusions

None of the six candidates is excluded.  Deliberately NOT in this
batch (ownership/scope reasons, unchanged from the manifest):

- all P4 classification families (`claims/p4/classifications/`
  population, medium/low confidence) — Stage 5+ territory;
- `verify_p4_two_rank_two_spoke_mixed_star_component.py` and every
  other non-pure-component P4 verifier — separate ownership;
- the P5 H22/H31 consumer packages that import or hash these P4
  modules — cross-family use is dependency, not ownership; they stay
  at root and are repaired in place;
- research snapshots — historical provenance, never moved.

## Machinery gaps recorded (fixed narrowly in Commit C)

1. The rewriter's `REPLAY_LINE` only matches single-line fenced
   commands; continuation (`python \` / indented filename) and
   `uv run --with sympy python` forms are untouched by the tool.
   Stage 3 left exactly one such leftover (the moved DMS theorem doc).
   Stage 4 repairs those fences manually and records the gap in the
   Stage 4 report.  No broad rewriter redesign.
2. The bare-basename stale scanner likewise covers only single-line
   replay commands; the manual repairs above are what keep the tree
   stale-clean.

## Cross-package acceptance note

This batch moves a module (`verify_p4_mixed_orientation_…`) that an
already-moved package (disjoint-mixed-star) imports, and a module
(`verify_p4_all_rank_one_triangle_…`) that imports the already-moved
package and is guarded-imported by two root P5 verifiers.  The
rewriter's second pass must report 0/0/0, and the full chain must
import from a clean checkout.
