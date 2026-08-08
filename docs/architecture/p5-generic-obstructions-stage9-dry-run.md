# Stage 9 dry-run — P5 component-level generic H31/H22 obstruction migration

Status: **dry-run / pre-execution**.  This document freezes the Stage 9
selection analysis, ownership decisions, dependency topology, exact
mapping, and projections.  Measured values are labeled *measured*;
everything about post-execution state is labeled *projected*.

> No theorem claim, assumption, scope, proof status, provenance status,
> or global-resolution status changes as a result of this migration.
> The global Krenn–Gu conjecture remains UNRESOLVED.

## Measured baseline

- Starting merged `main` SHA: `4ee0cdcb580a4b94c730e977c7f24ac1892dfa9c`
  (PR #37, the Stage 8.5 agent-operations documentation merge).
- Stage 8.5 prerequisite verified on merged `main`: `AGENTS.md`,
  `docs/proof-obligation-architecture.md`,
  `docs/formalization-interface.md`,
  `docs/architecture/layout-migration-runbook.md`,
  `docs/architecture/agent-operations-documentation-pass.md`,
  `docs/architecture/layout-migration-stage8-report.md`, and the
  Stage 8 artifacts (`catalog/batches/p4-rank-two-triangle-stage8.json`,
  the Stage 8 spine under `claims/p4/`) all present before any Stage 9
  work.
- Branch: `layout-migration-stage9-p5-generic-obstructions`.
- Root entries at baseline (*measured*, `git ls-tree --name-only HEAD`):
  **2,134** = 2,133 Stage 8 final + 1 (`AGENTS.md` added by Stage 8.5;
  verified as the only root-level addition between `3404991` and
  `4ee0cdc`).
- Baseline validation floor (*measured*, all green on the baseline):
  `check_hygiene.py` (provenance 239/239, manifest summary consistent,
  5 fast verifiers pass); `tests.test_migration_tools` 117 tests OK;
  `test_fourteen_vertex_cycle_cover_lattice.py` 14 tests OK;
  `rewrite_links.py` idempotent (0 links / 0 commands / 0 ledger
  updates / 0 ambiguities); `git diff --exit-code` clean.
- Environment: Windows 11, Python 3.13.14, sympy 1.14.0; Singular is
  **not** on the Windows PATH — Singular 4.3.2 is available through WSL
  (`wsl.exe --exec /usr/bin/Singular`), the same manual-replay
  convention used in Stage 3 (`hygiene` reports "Singular: not on PATH
  (manual replays only)").

## Fresh-agent documentation audit (in progress; final version in the
Stage 9 report)

Friction recorded so far (full schema fields in the final report):

1. **"Every executable member" vs "every practical live verifier/audit".**
   The runbook says "replay every practical moved verifier and
   independent audit"; the Stage 9 prompt says the same.  Neither states
   that a `.py` batch member is *not automatically* a theorem replay
   obligation (exploration scripts are not).  First preflight attempt
   launched a blanket serial replay of all 47 scripts with a permissive
   timeout; the owner interrupted and required an explicit role
   inventory (primary verifier / independent audit / support /
   exploration) with ledger-derived runtime guidance.  Classification:
   borderline C (stable migration rule, weakly missing) — the runbook's
   phrase "verifier and independent audit" is role-specific, but the
   distinction from auxiliary/exploration executables is only implicit.
2. **Singular invocation conventions are undocumented.**  Four distinct
   conventions coexist in the selected layer: shared
   `singular_command_with_timeout` helper (6 scripts), self-contained
   WSL-aware `("wsl.exe", ..., "/usr/bin/Singular")` tuples (23),
   direct PATH `["Singular", "-q"]` (2 — both coincident-support
   verifiers), and no Singular (26).  The ledger records
   `external_binaries: ['Singular >= 4.3']` but not which convention a
   script uses, so replayability on a given machine required inspecting
   every script.  Classification: B/E (family/script-specific state;
   belongs in stage reports, not permanent docs).
3. **A ledger `verified_generic` entry did not imply a currently
   runnable verifier.**  The equal-support-sixfold H31 verifier was
   already broken before Stage 9 (stale `P4_EQUAL_SUPPORT_SIXFOLD_
   PURE_COMPONENT.md` root-path constant left behind by the Stage 3
   component move).  Nothing in the ledger, the classifier, or the
   Stage 3 report flagged the regression.  Discovered only by
   preflight.  Classification: E (mutable state, recorded here) — this
   is exactly the failure mode that mandatory preflight exists to
   catch.
4. Root-count arithmetic across documentation stages required noting
   that Stage 8.5 added `AGENTS.md` at root (+1 entry vs the Stage 8
   final 2,133).  The Stage 8 report's table does not predict later
   additions; the delta was measured directly from Git.  Classification:
   A (adequate docs; measured from the authoritative source).

## Candidate inspection list — include / exclude / defer

Inspection source: every root `P5_H31_*` / `P5_H22_*` document and
companion script (`git ls-files`), cross-checked against
`catalog/theorem-ledger.json` statuses and per-script import/link
scans.  Classifier confidence played **no** role in selection.

### Included (28 packages, 86 files)

All included packages satisfy: ledger `verified_generic` for the
generic component theorem; complete doc + primary verifier +
independent audit on disk (one documented exception below); imports
only root-shared utilities, already-migrated P4 modules, or batch
siblings; all markdown links either move together or point at
stable root / already-migrated targets; preflight replay green
(57/57 executables, see replay plan).

| underlying P4 family | H31 package | H22 package | pairing note |
|---|---|---|---|
| all-rank-one triangle (component 9) | include (4 files: triple + modular explore) | include (3) | symmetric pair |
| coincident support (component 10) | include (3) | include (3) | symmetric pair; both verifiers use the direct-`["Singular"]` convention (WSL replay verified) |
| coincident-support rank-one star (star classification) | include (3) | — | H31 only; no H22 generic theorem exists for this family (asymmetry recorded, not manufactured) |
| common-kernel vertical triangle | include (3) | — | H31 only; the H22 side is a `_CANDIDATE`/`_VERIFICATION` pair, not a live generic theorem — deferred by the candidate rule |
| common singleton (component 18) | include (3) | include (3) | symmetric pair |
| directed zero-divisor triangle components (shared machinery family) | include (3) | include (3) | symmetric pair; P4 dependency `verify_p4_directed_zero_divisor_triangle_components` stays shared at root |
| disjoint mixed star (component 8) | include (3) | already migrated (pilot) | H31-only by construction: the H22 package is the pilot under `claims/p5/h22/disjoint-mixed-star/` |
| disjoint secant (pair geometry) | include (3) | include (3) | symmetric pair; H22 verifier imports its H31 sibling (batch-internal edge) |
| eisenstein norm | include (3) | include (3) | symmetric pair |
| equal-support common factor | include (3) | include (3) | symmetric pair; P4 doc `P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md` stays at root (not yet migrated — staying-root dependency) |
| full-support tangent (pair geometry) | include (3) | include (3) | symmetric pair |
| mixed orientation (component 6) | include (3) | include (3) | symmetric pair; P4 dependency already migrated (`claims/p4/components/mixed-orientation`) |
| six-dimensional (component 7) | include (3) | include (3) | symmetric pair; P4 dependency already migrated |
| transverse common factor | include (3) | include (3) | symmetric pair |
| two-rank-two-spoke mixed star | include (3) | include (3) | symmetric pair; P4 dependency already migrated (`claims/p4/classifications/star/two-rank-two-spoke-mixed-star-component`) |
| diagonal quadric (component 2) | — | include (4: triple + superseded working note) | H22 only this stage: the H31 side (`P5_H31_DIAGONAL_QUADRIC_ELLIPTIC_GENERIC_OBSTRUCTION.md`) owns a 10-file elliptic boundary forest (marked-fibre, T2/T3 divisor, genus-two, coordinate charts) and is inseparable from it at generic-core granularity — deferred as one unit |

Supporting-file asymmetries preserved exactly:

- **equal-support-sixfold: DEFERRED both sides.**  Its two generic docs
  are ledger `verified_generic`, but both verifiers are **broken
  pre-move**: `verify_p5_h31_equal_support_sixfold_component_generic_
  obstruction.py` raises `FileNotFoundError` for
  `P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md` (moved to
  `claims/p4/components/equal-support-sixfold/` in Stage 3; the
  verifier still walks parents looking for the root file).  Diagnosis:
  pre-existing stale path constant — not mathematical failure, not
  environment.  Rule applied: a selected live package that cannot
  replay cleanly for a non-environmental reason is deferred, and
  migration does not repair mathematics-adjacent path semantics in a
  preflight phase.  Neither sixfold package nor its audit-less state is
  touched by Stage 9.
- **equal-support-sixfold audit absence** (no independent audit exists
  on disk; ledger `independent_audit: null`) is moot while deferred but
  recorded for Stage 10.
- `P5_H22_DIAGONAL_QUADRIC_WORKING_NOTE.md` (classifier
  `review_required`, status SUPERSEDED EXPLORATORY) moves **with** its
  owning generic package, matching the pilot precedent (the disjoint
  mixed-star working note moved with its package).  It is explicitly
  historical, not theorem material.

### Excluded (not Stage 9 material)

- `common-active-binary-triangle` (both sides): prompt-flagged; the
  H31 generic doc is a single node with a **large descendant boundary
  tree** (special divisor, intrinsic boundary, normalized affine,
  p+q boundary/infinity-endpoint/exceptional-lower-pair, plus a
  `derive_..._candidate` dependency and a 33-importer candidate
  derivation module).  Not separable at generic-core granularity.
- `embedded-p3` (both sides): generic docs link five (H31) / three
  (H22) boundary-obstruction documents (projective closure, rank-one
  collapse, rank-two-line, r-zero, support-two) that are the package's
  own evidence chain; moving the generic core without them would strand
  same-theorem evidence.
- `common-center-kernel-star`: the H31 generic theorem is clean but is
  imported by 7 staying root H22 boundary scripts of the same family;
  its generic-vs-boundary ownership is one package-level decision and
  belongs to a later stage with the whole family.
- `unequal-complement-common-kernel`, `unequal-endpoint-inward-star`,
  `one-three-components` (H22): generic docs exist and are
  `verified_generic`, but each is imported by staying root scripts
  (`one-three` H31 is also imported by the staying H22 verifier) and
  the families have open boundary-recursion consumers; deferred to keep
  this stage's consumer repair surface bounded.
- `first-rank-two` (H22 only): clean imports but its independent audit
  imports `audit_p5_h31_marked_basis_fibre_classification` (root),
  and the family's P4 anchor is the pair-geometry pure-rank-two
  theorem; deferred to Stage 10 with the remaining pair-geometry
  generics.
- `split-center-mixed-star` (both sides): the H22 verifier imports the
  root-staying `derive_p5_h22_common_active_binary_triangle_...
  _candidate` module; deferred so Stage 9 does not create a
  claims→root dependency on a candidate-derivation script.
- All `*_CANDIDATE*`, `*_PARTIAL*`, `*_VERIFICATION.md`-only families,
  component19/component23 divisor trees, the elliptic-end/marked-fibre
  charts, the P5 frontier documents (`P5_HIGH_COORDINATE_PARTIAL_
  FRONTIER.md`, `P5_DELTA3_OBLIGATION_LEDGER.md`,
  `P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md`), and every non-H31/H22
  root P5 file: excluded by the default-exclusion rules (candidate/
  partial/frontier/pointwise-recursion), never promoted by confidence.

### Deferred to Stage 10+ (inspected, eligible, out of scope now)

one-three, split-center-mixed-star, first-rank-two (see exclusions for
the exact remaining edge), common-center-kernel-star, embedded-p3,
common-active-binary-triangle, unequal-complement-common-kernel,
unequal-endpoint-inward-star, diagonal-quadric-elliptic (H31, with its
forest), equal-support-sixfold (after path-constant repair is decided
as its own non-migration work item), and the H22-only
`COMMON_CENTER_KERNEL_STAR_COMPONENT_R_ZERO_DIVISOR_GENERIC_OBSTRUCTION`
(the boundary-recursion side of that family).

## H31/H22 pairing table

| family | H31 | H22 | Stage 9 shape |
|---|---|---|---|
| all-rank-one-triangle | in | in | pair |
| coincident-support | in | in | pair |
| coincident-support-rank-one-star | in | absent (no live H22 theorem) | H31-only, recorded |
| common-kernel-vertical-triangle | in | candidate-only | H31-only, recorded |
| common-singleton | in | in | pair |
| diagonal-quadric | deferred (elliptic forest) | in | H22-only, recorded |
| directed-zero-divisor-triangle-components | in | in | pair |
| disjoint-mixed-star | in | pilot-migrated | H31-only, recorded |
| disjoint-secant | in | in | pair |
| eisenstein-norm | in | in | pair |
| equal-support-common-factor | in | in | pair |
| full-support-tangent | in | in | pair |
| mixed-orientation | in | in | pair |
| six-dimensional | in | in | pair |
| transverse-common-factor | in | in | pair |
| two-rank-two-spoke-mixed-star | in | in | pair |

12 symmetric pairs, 3 recorded H31-only cases, 1 recorded H22-only
case, 1 pilot-already-migrated counterpart.  No manufactured symmetry.

## Generic-vs-boundary ownership decisions

Every selected generic document was read for its own scope statement.
Each states explicitly that it is a generic/function-field (or dense-
open) theorem and lists what it does **not** close (special/projective
fibres, weighted slopes, divisor boundaries, the global step).  The
two same-spine links that point at staying root documents
(`P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`,
`P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md`) are cross-references from
generic docs to root-staying frontier/atlas docs — they re-anchor
upward after the move and establish no ownership.  No selected package
leaves same-theorem evidence at root: the only generic docs with
boundary links (embedded-p3, common-active-binary-triangle) were
excluded above for exactly that reason.

## Dependency topology

```text
P4 (already migrated, stable anchors)
    claims/p4/components/all-rank-one-triangle
    claims/p4/components/disjoint-mixed-star
    claims/p4/components/mixed-orientation
    claims/p4/components/six-dimensional
    claims/p4/classifications/star/two-rank-two-spoke-mixed-star-component
    claims/p4/classifications/star/coincident-support-rank-one-star
    claims/p4/classifications/pair-geometry/disjoint-secant-lower-pair
    claims/p4/classifications/pair-geometry/full-support-tangent-pair
    claims/p4/classifications/triangle-211/split-center-mixed-star-211 (H31 doc link only)
        |
        v   (P4 -> P5 generic edges; imports via expose_claim_package
             or bare root import)
P5 generic layer (this batch)
    h31/<family>  <----H31/H22 sibling---->  h22/<family>
    intra-batch sibling imports:
        h22/disjoint-secant -> h31/disjoint-secant (verifier+audit)
        h22/disjoint-secant audit -> h22/directed-zero-divisor audit
        h22/full-support-tangent -> h31/full-support-tangent + h31 marked basis
    shared root utilities (STAY, consumed by moved scripts):
        verify_p5_h31_marked_basis_open_branch  (frontier)
        p5_high_coordinate_tree_chart_cegar     (frontier)
        verify_p4_directed_zero_divisor_triangle_components (shared P4 machinery)
        krenn_gu.bootstrap                      (src package)
    staying-root P4 docs referenced by moving docs:
        P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md
        P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md
        P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md
        P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md
        P4_COMMON_SINGLETON_COMPONENT.md + analyze_p4_common_singleton_local_dimension
        P4_DIRECTED_ZERO_DIVISOR_TRIANGLE_COMPONENTS.md
        P4_INOUT_PATH_STRATUM_WORKING_NOTE.md
    downstream boundary/frontier consumers staying at root (Commit D
    repair surface, sampled post-move):
        verify/audit_p5_h22_first_rank_two_...  (imports moving mixed-orientation)
        verify/audit_p5_h22_one_three_components_... (imports moving mixed-orientation)
        research_snapshots/2026-08-04-p5-delta3-obligation-ledger/scripts/*
            (4 scripts import moving h31 all-rank-one-triangle verifier)
```

Edge categories present: `P4 -> P5 generic`, `H31/H22 sibling`,
`shared utility (staying)`, `already-migrated dependency`,
`staying-root dependency`, `frontier consumer (staying)`,
`historical-only (the superseded diagonal-quadric working note)`.
Generic → boundary-descendant edges: **none inside the batch** (the
families that have them were deferred).

## Exact mapping (frozen candidate table)

86 members, 28 packages.  Destinations are the classifier's
`proposed_path` values; human ownership review found **zero** records
requiring refinement (verified record-for-record: manifest
`new_path` equals classification `proposed_path` for all 86; no
confidence promotion, no status change in this commit).

Source-family/status arithmetic (*measured*):

```text
members by starting manifest status:
    proposed_high_confidence   84
    review_required             2   (the diagonal-quadric working note,
                                     the all-rank-one-triangle explore script)
members by category:            29 claim documents, 56 scripts,
                                1 exploration script
members by spine:               h31: 44 files / 15 packages
                                h22: 42 files / 13 packages
```

The full 86-row old→new table lives in
`catalog/batches/p5-generic-obstructions-stage9.json` (Commit B); the
dry-run does not duplicate it to avoid drift between two sources of
truth.  All 86 sources verified: tracked at root, present in the
manifest, status != moved, destination unoccupied, no duplicate
sources/destinations.

## Replay plan (measured preflight results)

Mandatory preflight = every practical selected live primary verifier
and independent audit (28 + 28), plus the family exploration script
(replayed once for completeness; classified exploration, not
theorem-grade).  Ledger `expected_runtime` guidance used for timeout
sizing (H31 "minutes", H22 "minutes-hours").  Scheduling: pure-sympy
jobs at parallelism 2, Singular-touching jobs strictly serial,
direct-`Singular` scripts in WSL.

- **57/57 green.**  28 primary verifiers, 28 independent audits,
  1 exploration script, all rc=0.  Observed runtimes 0.1 s – 303.2 s;
  the two WSL-only coincident-support verifiers: 43.8 s (H31) and
  298.8 s (H22) — consistent with the ledger's "minutes" /
  "minutes-hours" guidance.
- Pre-move failure investigated and resolved as **environmental
  convention, not mathematics**: both coincident-support verifiers use
  direct `["Singular", "-q"]` (Windows PATH), failing with
  `WinError 2` outside WSL; in the established WSL Singular 4.3.2
  environment both pass with `status: pass` output and consistent
  theorem hashes.
- One family **deferred on preflight evidence**: equal-support-sixfold
  (both sides) — stale root path constant, broken since the Stage 3
  component move; deferral, not repair (see candidate table).
- No generated solver artifacts are tracked: these verifiers write to
  `tmp/` (gitignored) or stdout only.

Post-move replay will repeat the same 57-executable mandatory set from
the new package paths, plus clean-subprocess import checks for the
staying-root consumers listed in the dependency topology.

## Projections (not measured until execution)

```text
root entries:                2,134  ->  2,048   (−86)
manifest moved:                239  ->    325   (+86)
stale paths enforced:          239  ->    325   (+86)
proposed_high_confidence:      361  ->    277   (−84)
review_required:             1,415  ->  1,413   (−2)
unclassified:                  348  ->    348   (unchanged)
```

Per-source-family arithmetic: 84 members originate in
`proposed_high_confidence` and 2 in `review_required`; naive
subtraction from a single bucket would be wrong.  All 86 members start
at root, so the root decrease equals the member count (86).

## What this stage deliberately does NOT do

No divisor/boundary recursion, no exceptional fibres, no pointwise
closure, no common-center-kernel-star / common-active-binary-triangle /
embedded-p3 families, no frontier documents, no legacy evacuation, no
P6/P7, no proof-DAG schema, no mathematical change.  The migrated
layer is described only as "migrated component-level generic H31/H22
obstruction packages".
