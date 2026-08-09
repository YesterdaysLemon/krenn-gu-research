# P5 H31 complete first-plane Schubert-infinity marked fibre - Stage 24 exact migration dry run

Status: **APPROVED FOR AN EXACT FROZEN BATCH under the repository-owner
standing delegation dated 2026-08-08. No move has yet been executed.**

> **Scientific status will not change.** The global Krenn-Gu conjecture
> remains **UNRESOLVED**. This review resolves filesystem ownership only. It
> does not promote one complete divisor fibre to an entire projective
> boundary, a generic or whole-component theorem, component exhaustiveness,
> `P5 -> Delta3`, gluing, or a global result.

## Review authority and corrected baseline

- Exact clean corrected baseline:
  `26f7a48817de6f9e4b435966dc836c5a03e9a5bb`.
- Branch:
  `codex/stage24-h31-component-fibre-infinity-marked-fibre-migration`.
- Actual mapping reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.
- Delegated-review test: routine, non-ambiguous, evidence-backed exact layout
  mapping; no scientific-status decision, ambiguous proof-boundary decision,
  or owner-preference architecture choice is required.
- Batch ID to freeze:
  `p5-h31-component-fibre-infinity-marked-fibre-stage24`.
- Corrected classifier raw Windows-checkout SHA-256:
  `9e7d6057c5ebf3699028de874e24dd3dce92cd876b279707ee492efd5cc4fbb0`.
- Approval-time manifest raw Windows-checkout SHA-256:
  `0cc191a112b2cda2a525939b1a6ca7749c617478c58a914a3c6e3951fa2f24a8`.
- Canonical mapping SHA-256:
  `103e5de3343c1271841a84cfa79903c9d9e8c6f2c318adc8325c3b8cd1a3ace1`.

The two catalog hashes pin the raw corrected checkout used for review. The
canonical mapping hash is the portable authority for the reviewed old-to-new
pairs. All four manifest records remain `review_required` with medium
classifier confidence. Confidence is proposal evidence only; approval comes
from the independent topology, status, consumer, and mechanical reviews and
applies only to this exact four-file mapping.

The original classifier sent the generator to `tools/explore` solely because
of its `derive_` prefix. That mechanical route split one proof leaf: the
theorem names the generator as its regeneration command, the primary is its
only Python importer, and the primary hashes it as a dependency. Commit
`26f7a488` made the exact ownership correction before this review:

- generator category `tool_script -> claim_script`;
- family `null -> p5/h31/component-fibre-infinity-marked-fibre`;
- destination `tools/explore/... ->
  claims/p5/h31/component-fibre-infinity-marked-fibre/...`;
- family count `3 -> 4`, `tool_script 210 -> 209`, and
  `claim_script 1072 -> 1073`; and
- generated destination counts `claims 1762 -> 1763` and
  `tools 209 -> 208`.

The correction changes no confidence or manifest status. Classified and
manifest records remain 2,015; confidence totals remain 1,179 medium, 426
low, and 410 high. It changes no theorem, verifier, audit, generator,
navigation, lifecycle, or scientific-status byte.

## Exact four-file mapping

All four files move flat into
`claims/p5/h31/component-fibre-infinity-marked-fibre/`.

| role | source | destination |
|---|---|---|
| theorem | `P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md` | `claims/p5/h31/component-fibre-infinity-marked-fibre/P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md` |
| characteristic-zero primary | `verify_p5_h31_component_fibre_infinity_marked_fibre.py` | `claims/p5/h31/component-fibre-infinity-marked-fibre/verify_p5_h31_component_fibre_infinity_marked_fibre.py` |
| modular audit | `audit_p5_h31_component_fibre_infinity_marked_fibre.py` | `claims/p5/h31/component-fibre-infinity-marked-fibre/audit_p5_h31_component_fibre_infinity_marked_fibre.py` |
| exact elimination generator | `derive_p5_h31_fibre_infinity_marked_fibre_elimination.py` | `claims/p5/h31/component-fibre-infinity-marked-fibre/derive_p5_h31_fibre_infinity_marked_fibre_elimination.py` |

Every source is tracked grandfathered root debt, every destination is absent,
and the corrected classifier and generated manifest contain exactly these
pairs. There are no duplicate sources or destinations, case-folded
destination collisions, double moves, overlap cycles, or package-name
collisions.

| source | Git blob | frozen raw SHA-256 |
|---|---|---|
| theorem | `f1e632a06283b316469c4735bd6ffc72acc45436` | `ace531fdb3240c10cc1a74e14235a177bd2c68766acaa63aca8c45de429f035c` |
| primary | `03eaacb2daf5df572e0e3cf6f62e8233961583a9` | `3dc62b644474c0b9d41d74d4b99ac1e588268f58bdc0f4292765fb42ed2d7d34` |
| audit | `660fc27c5ced8b9b4f957c9f00b12ebe71ec52ea` | `320c2f2820ac818bfdfc63c3e4cfd229c6371f6a6412055cf42ba5b3c059d16a` |
| generator | `9f2f1ddf68ff6e583713f30168833d1f94fdf9d5` | `5a905ec64ae26083b898be8f6941300503c1d3681540aac0dac3dd4b81df3f2a` |

## Proof-obligation ownership and exact scope

The four artifacts are one complete, separable divisor-scoped proof leaf:

```text
first known pure-rank-two component
  -> first-plane Schubert-infinity divisor outside the finite chart
  -> H,N != 0; E arbitrary; projective direction (A,D)!=(0,0)
  -> bijective source/row action normalizes H=N=1
  -> every marking is a_i+t_i b_i for arbitrary t in C^4
  -> every distinguished source coordinate q=0,1,2,3
  -> every binary Delta_2 extension with both diagonals nonzero
  -> fourteen mixed equations and exact saturated elimination over Q
  -> 21 minimal projection components split into 25 rational charts
  -> 18 two-dimensional and 7 three-dimensional mixed kernels
  -> 154 selected nonzero residual products generate the required unit ideals
  -> an injective neighbouring marked map plus a transverse pure coordinate
  => the third target row vanishes, contradicting target rank three
  => the complete marked-basis fibre on this first-plane divisor is empty

other projective-boundary loci, the whole internal E=0 divisor,
the finite chart, second/further components, H22, component exhaustiveness,
P5 -> Delta3, gluing, and global resolution remain outside this leaf
```

The exact scope description is:

> An exact characteristic-zero obstruction for the complete marked-basis
> fibre on the known first pure-rank-two component's first-plane
> Schubert-infinity divisor, with `H,N != 0`, `E` arbitrary,
> `(A,D)!=(0,0)`, every plane tuple on that locus, every kernel-row shift,
> all four distinguished-source orientations, and every binary `Delta_2`
> extension direction with both diagonal coefficients nonzero.

The primary verifies the normalization and permanent identities, runs all
four exact absolute projections, checks all 21 minimal components and 25
residual-cover charts, and proves the characteristic-zero unit ideals. Its
report must retain:

- `verified: true` and field `characteristic zero`;
- `projection_runs: 4`, `minimal_projection_components: 21`, and
  `exact_residual_cover_strata: 25`;
- kernel histogram `2:18, 3:7` and 154 selected nonzero products;
- all binary extensions excluded and the complete first-plane infinity
  marked fibre excluded true; and
- internal-`E=0` marked-fibre closure, additional components, and global
  resolution false.

The internal-`E=0` field concerns the separate whole divisor. Its false value
does not deny the `E=0` intersection already included in this first-plane
leaf. The theorem's statement that internal `E=0` was later closed is
external lineage, not a scope expansion of this package.

## Live canonical predecessor and evidence roles

The migrated `claims/p5/h31/component-fiber-infinity/` triple is the live,
narrower canonical-section predecessor. It excludes the displayed canonical
marked rows on the same first-plane locus. This Stage 24 successor adds all
kernel-row shifts and the complete marked-basis fibre. The predecessor remains
live; it is neither withdrawn nor superseded, and its theorem, verifier,
audit, status, and package ownership remain separate.

The P4 pure-rank-two component theorem is separately owned upstream plane
geometry. The uniquely consumed generator belongs here because it constructs
the four saturated projection programs used by the primary and is named by
the theorem as the regeneration route. It is proof-producing support, not
independent evidence.

The finite-field audit imports neither this primary nor this generator. It
duplicates the family rows and projection equations, then exhausts the exact
projection loci over `F5` and `F7`, reconstructs modular mixed kernels,
enumerates every projective binary extension direction, and directly tests
the selected minors. It reports:

- `F5`: 351 projection points, 29 projection-closure artifacts, 3,096
  binary extensions, and 5,188 selected-minor tests;
- `F7`: 703 / 43 / 11,700 / 19,014; and
- totals 1,054 / 72 / 14,796 / 24,202, four orientations, complete
  first-plane marked fibre true, and global false.

This is independent of the family primary and characteristic-zero
SymPy/Singular proof route, but it is not hermetically implementation-
independent: it imports eight computational primitives from the staying root
`audit_p5_h31_marked_basis_fibre_classification.py`. Safe wording is
"independent of the family primary and characteristic-zero proof route, with
shared finite-field helper implementation." The modular enumeration is QA;
the characteristic-zero residual-cover ideals are the proof.

No selected artifact has a curated theorem-ledger entry or formal
counterpart. Migration adds none and changes no assumption, quantifier,
scope, lifecycle state, evidence role, or global-status field.

## Preserved conflicts and explicit exclusions

The separate root
`P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md` four-file
family remains blocked and is not a Stage 24 member. Its theorem says fourteen
certificate strata while its primary constructs, asserts, and reports
sixteen. That claimed-proof/verifier contradiction remains owner-gated. In
this selected theorem, the number fourteen instead counts mixed binary
coefficients; its distinct 21-component, 25-chart proof has no corresponding
cardinality conflict. Stage 24 neither consumes nor adjudicates the blocked
family.

The pre-existing P4 attribution conflict between internal `E=0` and the
separate nonzero chart divisor `D=0,a!=0` also remains unadjudicated. P4 is
upstream plane geometry, not part of this batch, and a rewritten link or
replay cannot validate or endorse that prose edge. The broader first/second-
component status-provenance conflict likewise remains owner-gated and
unconsumed.

This package does not close:

- the rest of the first component's projective boundary or its finite chart;
- the whole internal `E=0` divisor or genuine toric siblings by itself;
- the second diagonal-quadric or any further pure-compression component;
- component exhaustiveness or weighted `H22`;
- `P5 -> Delta3`, arbitrary-order/local-to-global gluing, or the prize graph;
  or
- the global conjecture.

Scope-local false fields must not downgrade separately proved sibling results,
and later prose must not promote this divisor leaf to a whole-component
closure.

## Mechanical repair and deterministic rewrite surface

After the pure move, all three selected Python executables install the shared
bootstrap before repository imports:

- `REPO_ROOT, HERE = bootstrap(__file__)` supplies stable repository and
  package ownership without `.git` discovery for the audit and generator;
- the primary uses `bootstrap(__file__, also=["."])` before its sibling
  generator import, resolves theorem and generator through `HERE`, and
  resolves the canonical predecessor and P4 theorem through `REPO_ROOT`;
- the audit resolves theorem and primary through `HERE`, while bootstrap
  exposes the staying shared finite-field helper;
- the generator uses bootstrap before importing the two staying root helpers;
  and
- the sole staying operational consumer,
  `verify_p5_high_coordinate_partial_frontier.py`, retargets its theorem
  dependency to the new package path.

No outside Python module imports the selected primary, audit, or generator.
The selected primary is the generator's sole importer. All three selected
executables remain stdout-only; the move creates no durable or tracked
solver output.

The deterministic virtual post-move rewriter predicts exactly **six Markdown
links and three fenced replay commands across six Markdown files**, with zero
ambiguity and zero ledger relocation. It touches:

1. the moved theorem;
2. the canonical predecessor theorem;
3. `P5_ALTERNATIVE_STRATEGY_MAP.md`;
4. `P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`;
5. `P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md`; and
6. root `README.md`.

Historical architecture reports and `docs/research-notes.md` remain unchanged.
The second rewriter pass must be a `0/0/0` fixed point.

The exact virtual post-move simulation projects these normalized-LF hashes:

- moved theorem:
  `d87e81fedcc68795e7352c7c9a64f5a172ddc912bc919d522876bd08ee904c3f`;
- canonical predecessor:
  `2cf8f5979c3384f79efda1a5f580774870f05456bc55834280fb0ed6df204871`;
- alternative-strategy map:
  `3be8f7d6fac7c8363a0c11851fffb6c5839cb9d2e64ea5f532373280c7a2b623`;
- high-coordinate frontier:
  `cb1f3200d27f9855ae52b5b729ab43bd9c73a561f0e17ccbbbef7229557f388a`;
- marked-basis classification:
  `152c70a08f22bb593e6c984f46e073395030be1cd429229aa4eaba879adbc25a`;
  and
- root README:
  `0e3e92ffbdb5444017f10b2ef50841b48e8c589bc08b93916f93abec50143b34`.

Exactly four existing theorem-ledger hashes refresh mechanically:

- verified high-coordinate frontier -> `cb1f3200d27f9855`; and
- the three root-README entries -> `0e3e92ffbdb54440`, retaining statuses
  `open`, `verified_generic`, and `partial`.

All other ledger fields remain byte-for-byte fixed.

Navigation adds `component-fibre-infinity-marked-fibre/` as an eighth scoped
H31 exception, labels it the complete first-plane Schubert-infinity
marked-fibre strengthening, retains `component-fiber-infinity/` as the live
canonical predecessor, and records the Stage 24 batch and mapping hash. Its
audit description must include the shared-helper qualification above. Parent
P5 navigation mirrors the scope, preserves the two packages as separate live
leaves, and changes the H31 package-directory count from 30 to 31. Neither
navigation surface may imply an entire projective-boundary or whole-component
closure.

## Projected transitions

| measure | before | after |
|---|---:|---:|
| manifest `moved` | 401 | 405 |
| manifest `proposed_high_confidence` | 242 | 242 |
| manifest `review_required` | 1,372 | 1,368 |
| moved-only manifest root projection | 1,971 | 1,967 |
| high-confidence manifest root projection | 1,729 | 1,725 |
| all-classified manifest root projection | 357 | 357 |
| measured root files | 1,963 | 1,959 |
| measured root directories | 9 | 9 |
| measured root entries | 1,972 | 1,968 |
| grandfathered root debt | 1,956 | 1,952 |
| new root debt | 0 | 0 |
| enforceable retired/provenance paths | 401 | 405 |
| H31 package directories | 30 | 31 |

The move creates one approved nested H31 package and changes no root baseline
or end-state allowlist.

## Exact prior baseline evidence

No new mathematical replay was run for this dry-run review. The selected
theorem, primary, audit, and generator bytes are unchanged from their replay
in the Stage 23 acceptance matrix at clean committed head
`df34337e56fb006cd2025ab2ca80f4c4614c66ab`; the intervening Stage 24
correction changed only catalog ownership.

In that strictly serial matrix, the selected primary passed once from the
repository root in 25.189 seconds and once from a fresh foreign working
directory in 22.192 seconds, both with rc=0, empty stderr, and valid JSON.
Their objects were identical after removing only `elapsed_seconds` (21.999
and 19.949 seconds). It reported the four projections, 21 components, 25
charts, `2:18,3:7` kernel histogram, 154 products, complete first-plane
marked fibre true, and internal-`E=0`/additional/global false. Its theorem,
canonical predecessor, P4 theorem, and generator hashes all matched then-
current bytes.

The selected audit passed once from root in 4.062 seconds with rc=0, empty
stderr, valid JSON, four orientations, the exact `F5/F7` and total counts
listed above, complete first-plane marked fibre true, and global false. Its
theorem and primary hashes matched. These are prior replay facts for unchanged
scientific bytes, not a new Stage 24 run and not evidence for any excluded
family or broader claim.

## Post-move acceptance matrix

Use
`uv run --quiet --python 3.13 --with sympy --with python-sat python`,
strictly serial, and preserve every first stdout, stderr, rc, timing, and JSON
object outside the repository before assertions. A wrapper or post-parse
failure must not launch an automatic rerun or become theorem evidence. Do not
alter process priority or kill a running solver. The selected primary and the
component-19 `phi=+/-1` derivation use the established fail-closed WSL/Singular
route on Windows and must not overlap.

The complete affected closure is **14 unique executables and 24
invocations**: 13 JSON executables in 16 invocations, plus eight deterministic
text invocations of the one moved generator.

Run these three JSON executables from both repository root and a fresh foreign
working directory by absolute path:

1. moved
   `claims/p5/h31/component-fibre-infinity-marked-fibre/verify_p5_h31_component_fibre_infinity_marked_fibre.py`;
2. moved
   `claims/p5/h31/component-fibre-infinity-marked-fibre/audit_p5_h31_component_fibre_infinity_marked_fibre.py`; and
3. staying `verify_p5_high_coordinate_partial_frontier.py`.

Run these ten JSON executables once from repository root:

4. `claims/p5/h31/component-fiber-infinity/verify_p5_h31_component_fiber_infinity.py`;
5. `claims/p5/h31/component-fiber-infinity/audit_p5_h31_component_fiber_infinity.py`;
6. `claims/p4/classifications/pair-geometry/pure-rank-two/boundaries/verify_p4_pure_rank_two_component_toric_boundary.py`;
7. `claims/p4/classifications/pair-geometry/pure-rank-two/boundaries/audit_p4_pure_rank_two_component_toric_boundary.py`;
8. `verify_p5_h31_marked_basis_fibre_classification.py`;
9. `audit_p5_h31_marked_basis_fibre_classification.py`;
10. `audit_p5_high_coordinate_partial_frontier.py`;
11. `audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_independent.py`;
12. `derive_p5_h22_component19_p0_phi_pm_one_ordinary_obstruction_candidate.py`;
13. `derive_p5_h22_component19_p0_qphi_minus_one_axes_compatibility_obstruction.py`.

For the four values `q=0,1,2,3`, run the moved generator once from repository
root and once from a fresh foreign CWD by absolute path with `--components`
but **without** `--run`. These eight no-run parity calls print deterministic
Singular projection-and-component program text and must not invoke Singular.
Compare each root/foreign `q` pair byte-for-byte. The selected primary already
submits the same four generated programs to Singular and checks their exact
projection bases and minimal components, so separate generator `--run` calls
would be redundant and are excluded from this matrix.

Exactly eight JSON executables write only ignored repository-`tmp/` files:
the canonical predecessor primary/audit, P4 toric primary/audit, marked-basis
classification primary/audit, and high-coordinate primary/audit. Five JSON
executables are stdout-only: the selected primary/audit, mask-6 audit, and two
component-19 derivations. The generator is one stdout-text executable used in
eight invocations. No executable writes tracked output.

Require:

- selected-primary root/foreign objects identical after removing only
  `elapsed_seconds`, with characteristic-zero scope, 4/21/25,
  `2:18,3:7`, 154 products, complete first-plane fibre true, and
  internal-`E=0`/additional/global false;
- selected-audit root/foreign byte equality, four orientations, exact
  `F5` 351/29/3,096/5,188, exact `F7` 703/43/11,700/19,014, exact totals
  1,054/72/14,796/24,202, modular-QA scope, and global false;
- high-coordinate root/foreign byte equality and census
  6,495 / 1,680 / 1,170 / 510, with `P5 -> Delta3` and global false;
- each of the four generator root/foreign text pairs byte-identical, with the
  expected `q` marker and no solver execution or filesystem output;
- the canonical predecessor stays exactly `C`, `Delta_0(01)=0`, `[H,N]`,
  `(A,D)!=(0,0)`, six certificates, all four orientations true, and
  H31/P5/global false; its audit retains exact `F5`
  1,920/17,408/17,408/0 and `F7` 12,096/160,704/160,704/0 counts;
- P4 toric boundary stays 28 lattice points, 12 facets, 11 genuine divisors,
  and 44 divisor/orientation pairs split 21 gate / 23 all-rank, with
  H31/P5/global false;
- marked-basis classification retains its 20 exact certificate strata,
  finite known-family marked-fibre closure true, projective boundary,
  additional components, and global false; its audit retains 426 surviving
  markings, 6,234 projective kernel directions, 4,498 admissible extensions,
  32 rejected `L=0` closure artifacts, and zero ambient maps or
  Grassmannians;
- mask-6 remains `VERIFIED`, both component-19 derivations remain
  `CANDIDATE`, and every global-resolution field remains false where present;
- every emitted theorem, primary, source, generator, input, output, and
  dependency hash matches current bytes, with no stale root path;
- all eight generated JSON files are ignored and untracked, all foreign
  directories are empty, all 16 captured JSON invocation outputs are valid,
  and
  no tracked output drifts; and
- the three moved Python modules pass isolated foreign-CWD import probes.

After the matrix, confirm targeted Ruff and byte compilation, the rewriter's
`0/0/0` second-pass fixed point, the index-complete validation floor, exact-
head CI, and fresh semantic plus mechanical final referees before a normal
head-guarded merge.

## Stop boundary

Stage 24 stops at the complete marked-basis fibre on the first-plane
Schubert-infinity divisor of the first known pure rank-two component. It does
not execute or repair the blocked chart-boundary fourteen-versus-sixteen
family, adjudicate the P4 or broader component-provenance conflicts, or extend
the theorem to the rest of the projective boundary, the finite chart, a
second or further component, component exhaustiveness, weighted `H22`,
`P5 -> Delta3`, local-to-global gluing, or global resolution.

The global Krenn-Gu conjecture remains **UNRESOLVED**.
