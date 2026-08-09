# Layout migration Stage 28 report

Status: **MOVE AND REPAIR COMPLETE; LOCAL VALIDATION PASS; PUBLICATION AND CI
PENDING.**

The global Krenn-Gu conjecture remains **UNRESOLVED**. Stage 28 changes
filesystem ownership, executable paths, navigation, and mechanically derived
catalog/ledger path metadata. It does not change a theorem, quantifier,
finite-case bound, lifecycle, evidence role, formalization status, owner-gated
conflict, or global status.

The repair checkpoint is index-complete and locally validated. Publication,
hosted CI, and merge remain pending and are not inferred from local results.

## Known transaction checkpoints

| role | commit |
|---|---|
| reviewed dry run and catalog refinement | `ed5bd1a03fe124baf13b427830f2cec10b92c985` |
| frozen exact batch | `ade5d5be1d607b1e145387abccc03625ec5ecdb3` |
| pure Stage 28 moves | `ed8dc6a01664858f3a24de3fc28e02f0c1661c58` |
| migration-aware link/command rewrite checkpoint | `d25cd2ad357827370baae5cfaaffd695a7573cd3` |
| final import/path/provenance repair | `da48c9ac1bd60c804b141e0f970deb5740d539ae` |
| validated repair tree before this evidence-only report pin | `50a2a33fca0a94e35baa1a486da58b01ae0699c0` |

Reviewed merged-main base:
`5726180037986d27b9e445ee058e6c221b6d2d03`, tree
`07195d8c8720901f31fe35b5d037f01bf04d1b0f`.

Batch: [`finite-p4-stage28`](../../catalog/batches/finite-p4-stage28.json).
The batch contains exactly 201 root-to-package moves.

## Exact mapping identity

| subset | documents | carriers | members | mapping SHA-256 | source-identity SHA-256 |
|---|---:|---:|---:|---|---|
| finite | 49 | 84 | 133 | `09206352818278ce66e9112ea6045ca34e0df12365c8caf84c08c16eb4439d30` | `25d1c183c59efeb142285db366c33437d1aafb19ac5b2309a873f990861f4fe9` |
| P4 safe | 24 | 44 | 68 | `70cdd782d78c47f1ae0f7deaaf9a1178c578df88a60bdd8c40ecad6b056b4295` | `018ecc42523b69ca8bc6dc9131aece536a3bc3f04d4f20183f5fb5df83870db4` |
| aggregate | 73 | 128 | 201 | `2715a521e40f5ad6815af2044af1b1c075bf1cf29de81b076c4de239db5cf9a6` | `d64ecf0b34d83efbd24d9cef24841e17719c427159f07b5eea7dcc5fdb776871` |

The portable run-local mapping artifact has SHA-256
`a2fc55c46ac5806c87888e43fbe15a8f5a6e08fea77b139dec8012701d67d433`.
The freeze-time moved-paths manifest has SHA-256
`1b44664f26a50b310e3f4a984fef0e50449017ee7ccd434c8b3ac450ae4d5a32`.

The pure-move checkpoint contains exactly 201 `R100` pairs. Every destination
blob equals its frozen source blob. The only accompanying mutation is the
executor-owned moved-paths state for exactly those 201 records.

## Root projection

The live root immediately after the pure move contains 1,165 tracked files
and nine directories: **1,174 entries**, with **1,158** grandfathered debt
entries. This is the live-tree count; the historical manifest projection is
one lower because retained `AGENTS.md` lies outside the classifier universe.

## Scientific and ledger boundary

The finite packages remain restricted to their stated vertex order, support,
factor type, orbit, selector, connectivity, equality, and conditioned-CNF
hypotheses. A finite survivor is not a counterexample, and a bounded or
sampled computation is not promoted to exhaustive case coverage. The
order-twelve Kotzig-port package remains finite regression evidence subsumed
by the separate Stage 27 arbitrary-order theorem. The order-fourteen ledger
frontier remains `partial`.

The P4 packages retain their component, boundary, obstruction, reduction,
and lifecycle scopes. The first-component apolar record remains a dense P4
normal form only. The all-pair-rank record stops at pure-P4 component
exhaustiveness and does not close marked H31/H22 special fibres, the
`P5 -> Delta_3` reduction, or the global conjecture.

Zero-based theorem-ledger entries 5-10 and 66 retain their scientific and
evidence fields:

- entries 5-9: `verified_finite`, null single-script primary/audit mappings,
  and `historical_certificate_chain` provenance;
- entry 10: `partial`, with its three order-fourteen families incomplete;
- entry 66: `verified_generic` within the all-pair-rank reduction and
  source/mode symmetry, mapped primary, null independent audit,
  `not_yet_mapped` audit provenance, and live `BOTTLENECK B3` quantifier
  review.

At `d25cd2a`, moved ledger paths and path-derived package metadata were
committed. The repair candidate refreshes the seven directly moved document
hashes and 18 hash-only link-rewrite consumers against staged Git blobs. All
86 curated document hashes now match. No audit was populated merely because
its carrier co-moved.

## Exclusions and stop conditions

Stage 28 does not select or consume:

- `P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY` or its two scripts;
- either `P4_COMPONENT20_*_PROOF_B` document or its conflict carriers;
- `P4_INOUT_PATH_STRATUM_WORKING_NOTE` or its external exploratory tools;
- the Component20 intrinsic-wall/zero-diagonal package, Component21/23,
  embedded-P3, H31 common-center, Branch B, high-coordinate, or legacy
  routing surfaces.

All four owner-gated conflicts remain unadjudicated:

1. the marked-H31 chart-boundary theorem says 14 certificate strata while its
   primary asserts and reports 16;
2. P4 internal-`E=0` versus chart-`D=0,a!=0` attribution remains ambiguous;
3. first/second-component provenance and closure disagree across marked-basis,
   toric, high-coordinate, outer-boundary, README, and synthesis records;
4. weighted-H22 `p+q=0` status disagrees between the dedicated root forest and
   migrated aggregate provenance.

Conflict 1 remains a repository stop condition. Conflicts 2-4 remain
ownership/provenance ambiguities. Stage 28 found no basis to promote,
adjudicate, or consume any of them.

## Rewriter checkpoint

The migration-aware pass committed at `d25cd2a` rewrites exactly 242 Markdown
links and 221 replay commands across 118 files, with zero ambiguity. Its
second pass is an exact `0/0/0` fixed point. These are path-expression changes,
not theorem edits.

The four Component sources at that checkpoint are:

| source | repository-relative path | checkpoint blob |
|---|---|---|
| Component20 | `claims/p4/classifications/triangle-211/common-active-binary-triangle/P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md` | `eb3d499dc6c39902f9e0053c3280fdc1e1b16464` |
| Component18 | `claims/p4/classifications/P4_COMMON_SINGLETON_COMPONENT.md` | `099c4b8c943a79ecd28d72b5653cf59791bcb6d8` |
| Component15 boundary | `claims/p4/boundaries/pair-geometry/support-one-secant/P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md` | `4d3b26491b1e94d33da89fc52af3f3e31eb18c88` |
| Component16 boundary | `claims/p4/classifications/triangle-211/triple-kernel-rank-one-triangle/P4_TRIPLE_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md` | `358503edee64f8a52136a71e70c5391892dfe6a7` |

Their differences from the historical `f997c...` source anchor are retained as
historical provenance; the Stage 28 differences are path/link/command
rewrites only. The staying Component20 audit now verifies both anchor
ancestries, all eight `commit:path` blobs, and all four full current pathspecs.
Its focused no-main test passes on the live checkpoint and fails after a
nested source mutation in an isolated Git fixture.

## Repair and local validation evidence

The repair remains mechanical and inventory-bounded:

- finite: 78 owned Python files; 37 importers/73 edges; 27 staying path sites;
  94 runtime selected-path sites; one preserved manifest-resolved semantic
  predecessor key;
- P4: 77 owned Python files; nine importers/nine edges; 72 staying sites and
  55 selected records, with semantic basename/theorem keys preserved behind
  the repository-rooted manifest resolver;
- Component20: one staying audit path/provenance repair plus one focused test;
- navigation: six finite READMEs and minimal additions to the three existing
  P4 READMEs.

All 155 inventory-owned Python files compile. Fresh foreign-working-directory
imports pass for finite 78/78 and P4 77/77; the two optional-Z3 P4 imports use
`uv run --with sympy --with z3-solver`. All 82 crossing import edges, 100
staying path records, and 150 selected path/semantic records satisfy their
frozen contracts. No helper extraction or scientific algorithm/assertion edit
was made.

The index-complete local floor passes:

| validation | result |
|---|---|
| `python check_hygiene.py` | PASS: 1,699 Python; 842 Markdown; ledger 86/86; root 1,174/debt 1,158; zero new debt |
| `python -m unittest -v tests.test_migration_tools` | PASS: 152 tests in 11.536 s |
| `python -m unittest -v test_fourteen_vertex_cycle_cover_lattice.py` | PASS: 14 tests in 0.003 s |
| `python -m unittest -v tests.test_component20_source_guard` | PASS: 2 tests in 2.181 s |
| `python tools/migration/rewrite_links.py` | PASS: exact `0/0/0`, zero ambiguity, zero ledger updates |
| `git diff --exit-code` and cached diff check | PASS |

Broad SAT, Singular, sampling, or theorem reruns were neither required nor
performed. The remaining evidence is publication-only: final commit/tree,
remote branch/PR, hosted CI, exact-head merge, and merged-main validation.
