# Layout migration Stage 23 report

Status: **SUBSTANTIVE MIGRATION COMPLETE ON BRANCH; AWAITING FINAL REPORT
REVIEW AND MERGE.**

The global Krenn-Gu conjecture remains **UNRESOLVED**. Stage 23 changes
filesystem ownership, replay paths, navigation, and mechanically derived hash
metadata. It does not promote a displayed canonical marked-row obstruction to
a complete marked fibre, a first-plane divisor result to an entire projective
boundary or whole-component theorem, or any local obstruction to
`P5 -> Delta3`, gluing, or the global conjecture.

## Exact reviewed transaction

- Audited baseline:
  `97abc5f2c0cedc3707d0c97b85382df8d1747d74`.
- Branch: `codex/stage23-h31-component-fiber-infinity-migration`.
- Dry-run approval commit:
  `5235190c6542cb3b0ddb4dc98b90ce86606bd338`.
- Frozen-batch commit:
  `d5bb6dd46a58a8715d33f64b46d774054bbe3fc7`.
- Pure-move commit:
  `df9c657a38eb811805e1a86d0e7506a57ea00e13`.
- Package/path repair and navigation commit:
  `df34337e56fb006cd2025ab2ca80f4c4614c66ab`.
- Substantive tree:
  `cb86677366f19df76aa73046487e8b343221ce3b`.
- Batch ID: `p5-h31-component-fiber-infinity-stage23`.
- Canonical mapping SHA-256:
  `3874be216b1210251aea1150fa655e7ea5bde0c035df0d8c9d51d18b0d57a454`.
- Approval-time raw Windows-checkout manifest SHA-256:
  `c6c5b192a13da3016fe4d70f784c8cc7991b471e26c119eeec5b8a8d36f1dc36`.
- Corrected classifier raw Windows-checkout SHA-256:
  `8561e714ce1aafe77a9d274cc62feb756ba9b7335c8cc1cf920641f89f22c397`.
- Actual mapping reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.

The approval-manifest hash is platform-specific informational provenance.
The canonical mapping hash is the portable authority for the exact three
old-to-new pairs. The approved ownership analysis is recorded in
[`p5-h31-component-fiber-infinity-stage23-dry-run.md`](p5-h31-component-fiber-infinity-stage23-dry-run.md),
and the executable batch is frozen in
[`catalog/batches/p5-h31-component-fiber-infinity-stage23.json`](../../catalog/batches/p5-h31-component-fiber-infinity-stage23.json).

## Moved proof-obligation boundary

The exact theorem/primary/audit triple moved flat into
`claims/p5/h31/component-fiber-infinity/`:

1. `P5_H31_COMPONENT_FIBER_INFINITY_OBSTRUCTION.md`;
2. `verify_p5_h31_component_fiber_infinity.py`; and
3. `audit_p5_h31_component_fiber_infinity.py`.

The frozen source blobs were:

| role | Git blob |
|---|---|
| theorem | `9de3e9dfb61cf6904f1b2169e45eb56a680ea2cf` |
| primary | `3adfdde02c912df1775fd440374a321c231c1fdf` |
| modular audit | `565cd8e720336c6743f04a4f5864e755b9d95960` |

The selected claim is an exact characteristic-zero obstruction on the first
known pure-rank-two component's first-plane Schubert divisor
`Delta_0(01)=0`, restricted to the locus where the other three selected
preferred Pluecker coordinates remain nonzero. It uses the displayed
canonical marked-row normal form with `H,N != 0`, `E` arbitrary,
`(A,D)!=(0,0)`, and all four distinguished-source orientations
`q=0,1,2,3`.

Its exact boundary is:

```text
first known pure-rank-two component
  -> first-plane Schubert divisor Delta_0(01)=0
  -> other three selected preferred Pluecker coordinates remain nonzero
  -> H,N != 0; E arbitrary; projective direction (A,D)!=(0,0)
  -> displayed canonical marked-row normal form
  -> four exhaustive symbolic parameter cases
  -> all q=0,1,2,3 distinguished-source orientations
  -> exact mixed-kernel and marked-minor contradictions
  => those selected canonical marked sections do not lift to H31

arbitrary kernel-row shifts, the complete marked-basis fibre, the rest of
the projective boundary, the finite chart, second/further components, H22,
P5 -> Delta3, gluing, and global remain outside this leaf
```

The primary is the characteristic-zero proof replay: it reconstructs the
plane normal form, permanent coefficients, every mixed-kernel survivor case,
and the six displayed marked-minor certificates. The audit imports neither
the primary nor any scientific/computational repository helper. Its sole
repository import is path-only `krenn_gu.bootstrap`; it separately implements
dynamic-programming permanents, modular kernels, and projective extensions
over `F5/F7`. The audit is modular QA only, not the characteristic-zero proof.

The primary's historical
`remaining_known_component_geometry="Delta_1(12)*Delta_2(12)*Delta_3(03)=0"`
field remains unchanged. It does not reopen the later toric
closure recorded by current theorem prose. Correcting that historical output
field would be separate owner-gated scientific-output work, not migration.

The later
`P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md` family adds
arbitrary kernel-row shifts and the complete marked basis on the same plane
locus. Its theorem, primary, audit, and uniquely consumed elimination
generator remain together at repository root as grandfathered debt pending a
separately reviewed four-file batch. The selected canonical theorem remains a
live narrower result; it is neither withdrawn nor superseded. No selected
artifact has a curated theorem-ledger entry or formal counterpart, and Stage
23 adds neither.

## Preserved conflicts and deferred family

Stage 23 neither consumes nor adjudicates the pre-existing P4 attribution
conflict between the internal `E=0` description and the Stage 22 canonical
chart-boundary leaf's `D=0,a!=0` description. Intersections of the internal
`E=0` and genuine toric packages with this first-plane divisor are covered by
this selected triple only for its displayed canonical marking; the sibling
packages separately own complete marked-fibre coverage on their own scoped
intersections.

The broader first/second-component provenance conflict also remains
unadjudicated and owner-gated. Stage 23 makes no claim about the second
diagonal-quadric component, further components, or component exhaustiveness.

A distinct proposed four-file
`component-chart-boundary-marked-fibre` family remains deferred. Its theorem
says fourteen certificate strata while its primary constructs, asserts, and
reports sixteen. That claimed-proof/verifier contradiction is recorded in
[`p5-h31-component-chart-boundary-marked-fibre-stage23-dry-run.md`](p5-h31-component-chart-boundary-marked-fibre-stage23-dry-run.md).
Its theorem, primary, audit, and generator remain at repository root with
`review_required` manifest status; no batch was frozen. Stage 23 does not
promote, repair, dismiss, or combine that blocked family with the selected
first-plane canonical triple.

## Pure move and mechanical repairs

Against its direct parent, the pure-move commit contains exactly three
`R100` moves plus the corresponding manifest transaction. Scientific bytes
are identical across the move. The manifest changes only the selected three
records from `review_required` to `moved`, records the exact executed batch,
and updates deterministic summary fields:

- moved: `398 -> 401`;
- review-required: `1,375 -> 1,372`;
- proposed-high-confidence: `242` unchanged;
- moved-only root projection: `1,974 -> 1,971`;
- moved-plus-high-confidence root projection: `1,732 -> 1,729`; and
- all-classified root projection: `357` unchanged.

After the move, both selected executables install the shared
`krenn_gu.bootstrap` machinery before repository use. The theorem and sibling
primary resolve through `HERE`; the P4 chart, Stage 22 canonical dependency,
and ignored generated JSON resolve through `REPO_ROOT`. Exactly three staying
primaries retarget the selected theorem path:

1. the P4 toric-boundary primary;
2. the complete first-plane marked-fibre successor primary; and
3. the high-coordinate frontier primary.

No staying importer or subprocess caller targets either selected executable.
The executable edits are path/bootstrap-only; no mathematical algorithm,
case, assertion, output/status field, or evidence role changes.

The deterministic rewriter changed exactly five Markdown links and two
fenced replay commands across four Markdown files, with zero ambiguity and
zero ledger relocation. Its second pass is a `0/0/0` fixed point. Navigation
now records 30 H31 package directories, raises the explicitly scoped
exception count from six to seven, and labels this package as a canonical
first-plane Schubert-infinity section, never as generic, complete-marked-
fibre, whole-component, or component-exhaustiveness evidence.

The theorem ledger changes exactly four `document_sha256_16` values:

- the verified high-coordinate entry now uses `8da5855890f720c3`; and
- the three README-backed entries now use `3ad0a357fa8df313`, retaining
  statuses `open`, `verified_generic`, and `partial`.

Every other ledger field is unchanged, including the global
**UNRESOLVED** field.

Observed end-of-substantive-stage arithmetic is:

| measure | before | after |
|---|---:|---:|
| measured root files | 1,966 | 1,963 |
| measured root directories | 9 | 9 |
| measured root entries | 1,975 | 1,972 |
| grandfathered root debt | 1,959 | 1,956 |
| new root debt | 0 | 0 |
| enforceable retired/provenance paths | 398 | 401 |

The frozen root baseline and exact end-state allowlist are unchanged.

## Scientific replay matrix

The complete recursive affected-consumer closure is 11 unique executables
and 16 scientific invocations. Every row ran exactly once and strictly
serially through
`uv run --quiet --python 3.13 --with sympy --with python-sat python`.
Rows 1--16 all returned rc=0, empty stderr, and one valid JSON object.

The five directly affected executables ran from repository root and by
absolute path from a fresh foreign working directory:

| rows | executable | root s | foreign s | preserved semantic boundary |
|---|---|---:|---:|---|
| 1--2 | moved canonical primary | 9.074 | 3.054 | field `C`; `Delta_0(01)=0`; six certificates; all four orientations true; H31/P5/global false |
| 3--4 | moved modular audit | 94.592 | 95.672 | no primary import; exact `F5/F7` census; zero successful lifts; modular QA only |
| 5--6 | P4 toric-boundary primary | 1.016 | 1.029 | 44 divisor/orientation pairs = 21 gate + 23 all-rank; H31/P5/global false |
| 7--8 | complete first-plane marked-fibre successor primary | 25.189 | 22.192 | 21 components, 25 residual charts, 154 products; complete scoped fibre true; whole internal-`E=0`, additional-component, and global false |
| 9--10 | high-coordinate primary | 2.043 | 2.054 | existing frontier census and dependency hashes; P5/global false |

The moved primary, moved audit, P4 primary, and high-coordinate pairs are
byte-identical. The complete-successor objects are equal after removing only
their measured `elapsed_seconds` values, `21.999` versus `19.949`. All five
pairs carry current source/theorem/dependency hashes, and every foreign
directory remained empty.

The six root-only consumers also passed:

| row | executable | elapsed s | preserved boundary |
|---|---|---:|---|
| 11 | P4 toric-boundary audit | 1.016 | independently reconstructed 28 lattice points, 12 facets, and the 21/23 split |
| 12 | complete first-plane marked-fibre audit | 4.062 | `F5`: 351 projection points, 29 closure artifacts, 3,096 extensions; `F7`: 703/43/11,700; 24,202 total minor tests; modular QA, global false |
| 13 | high-coordinate audit | 4.038 | census 6,495 / 1,680 / 1,170 / 510; P5/global false |
| 14 | H22 actual mask-6 independent audit | 2.015 | all 12 scoped flags obstructed; label remains `VERIFIED`; global false |
| 15 | component-19 `phi=+/-1` derivation | 15.122 | construction checks pass; label remains `CANDIDATE` |
| 16 | component-19 `qphi=-1` axes derivation | 4.054 | higher obstruction true and actual lift false; label remains `CANDIDATE` |

The moved modular audit retained exactly:

- `F5`: 1,920 boundary parameter points, 17,408 projective binary
  extensions, all 17,408 marked-injective, and zero successful lifts; and
- `F7`: 12,096 / 160,704 / 160,704 / 0.

Every emitted theorem, primary, source, dependency, and input hash matched
current tracked bytes. Exactly six matrix executables write ignored
repository-`tmp/` JSON and five are stdout-only. Generated objects
parse-matched their preserved captures, no foreign working directory gained
an output, and no tracked output drifted.

The full captures and metadata are preserved outside the repository at
`C:\Users\Yeste\.codex\run-artifacts\stage23-20260809T120726Z`.
The complete marked-fibre successor used the established WSL/Singular route
on Windows, and the component-19 `phi=+/-1` derivation used its established
Singular route; strict serialization prevented overlap. No scientific replay
timed out, failed, or was automatically rerun, and no timeout or wrapper
outcome was treated as theorem evidence.

## Isolated import-probe record

Import probes were separate from the 16-row scientific matrix.

Row 17 attempted the moved-primary import from a fresh foreign directory and
returned rc=1 in 0.438 seconds with no stdout and no foreign output. The
PowerShell wrapper stripped required quotes from its generated `python -c`
argument, so Python evaluated `stage23_probe_primary` as an undefined name.
The resulting `NameError` occurred before `spec_from_file_location` could
import the module. This is a preserved pre-import wrapper failure, not a
module failure and not mathematical evidence.

Row 18 independently imported the moved audit in 0.600 seconds and emitted
`IMPORT_OK audit_p5_h31_component_fiber_infinity.py`, with rc=0, empty
stderr, and an empty foreign directory.

After separate authorization, row 19 used a corrected import-only wrapper for
the moved primary. It passed in 1.800 seconds and emitted
`IMPORT_OK verify_p5_h31_component_fiber_infinity.py`, with rc=0, empty
stderr, and an empty foreign directory. Its metadata records:

> Separately authorized corrected import-only probe after preserved row 17
> PowerShell quoting failure before module import.

Row 19 was not an automatic replay of row 17 and did not rerun any scientific
calculation. Together, rows 18 and 19 establish isolated foreign-CWD imports
for both moved modules while preserving row 17's failed-wrapper provenance.

## Validation and publication boundary

At substantive head
`df34337e56fb006cd2025ab2ca80f4c4614c66ab` and tree
`cb86677366f19df76aa73046487e8b343221ce3b`, the exact local
index-complete validation floor passed:

- `check_hygiene.py`: 1,698 Python files compile, all 820 pre-report
  Markdown files have resolving local links, all 86 ledger hashes match,
  root is 1,963 files + 9 directories = 1,972 entries, root debt is
  `1,956 grandfathered / 0 new`, and all 401 retired-path/provenance records
  pass;
- all 152 migration-tool tests;
- all 14 fourteen-vertex cycle-cover lattice tests;
- deterministic rewriter fixed point `0/0/0`;
- targeted Ruff import-order/bootstrap checks (`E402` and `I001`) for both
  moved scripts, with candidate-wide byte compilation supplied by hygiene;
- the preserved row-18 and separately authorized row-19 isolated import
  passes; and
- clean index/worktree diff checks.

Workflow-dispatch run
[`31313475707`](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31313475707)
passed at the exact substantive head, including hygiene, migration tests, the
self-contained lattice module, and rewrite closure.

Adding this report raises the Markdown count from 820 to 821. The final
report candidate must rerun the complete index floor, receive fresh Tier-2
semantic/status and mechanical/provenance/bypass referee passes, and pass
exact-head pull-request CI before a normal guarded merge.

## Stop boundary

Stage 23 stops at the displayed canonical marked-row sections on the first
component's first-plane Schubert-infinity locus. It does not claim arbitrary
kernel-row shifts, the complete marked-basis fibre, the rest of the
projective boundary, the finite chart, the second or further components,
component exhaustiveness, weighted `H22`, `P5 -> Delta3`, local-to-global
gluing, or global resolution. The blocked 14-vs-16 chart-boundary full-family
contradiction and the pre-existing scientific conflicts remain separately
owned and unadjudicated.

The global Krenn-Gu conjecture remains **UNRESOLVED**.
