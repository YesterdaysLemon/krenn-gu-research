# Layout migration Stage 24 report

Status: **SUBSTANTIVE MIGRATION COMPLETE ON BRANCH; AWAITING
REPORT-INCLUSIVE VALIDATION, FINAL REFEREES, AND MERGE.**

The global Krenn-Gu conjecture remains **UNRESOLVED**. Stage 24 changes
filesystem ownership, replay paths, navigation, and mechanically derived hash
metadata. It does not promote one complete divisor fibre to the rest of the
projective boundary, the finite chart, a whole-component theorem, component
exhaustiveness, weighted `H22`, `P5 -> Delta3`, gluing, or the global
conjecture.

## Exact reviewed transaction

- Merged-main baseline:
  `28b3ff93fb27e890d647544882b00f96be2c4cec`.
- Generator-ownership correction:
  `26f7a48817de6f9e4b435966dc836c5a03e9a5bb`.
- Branch:
  `codex/stage24-h31-component-fibre-infinity-marked-fibre-migration`.
- Dry-run approval commit:
  `e6be08259da18c37ffdb3fd6bd098f9a46f39364`.
- Frozen-batch commit:
  `10322073e55df2265a0aaa606ba0ef9be48aa36b`.
- Pure-move commit:
  `cd0b8256e05998a107bc0f5649599465ee50ce4b`.
- Package/path repair and navigation commit:
  `37de804fc74dd4813ed3b66853d26b8944e7bd35`.
- Substantive tree:
  `8e2cb0df95582b2c5887f94abfb3087f9179fbaf`.
- Batch ID:
  `p5-h31-component-fibre-infinity-marked-fibre-stage24`.
- Canonical mapping SHA-256:
  `103e5de3343c1271841a84cfa79903c9d9e8c6f2c318adc8325c3b8cd1a3ace1`.
- Corrected classifier raw Windows-checkout SHA-256:
  `9e7d6057c5ebf3699028de874e24dd3dce92cd876b279707ee492efd5cc4fbb0`.
- Approval-time manifest raw Windows-checkout SHA-256:
  `0cc191a112b2cda2a525939b1a6ca7749c617478c58a914a3c6e3951fa2f24a8`.
- Actual mapping reviewer:
  `Codex (exact mapping reviewer under repository-owner standing delegation
  dated 2026-08-08)`.
- Publication surface:
  [pull request #56](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/pull/56).

The two catalog hashes are checkout-specific provenance. The canonical
mapping hash is the portable authority for the exact four old-to-new pairs.
The approved ownership analysis is recorded in
[`p5-h31-component-fibre-infinity-marked-fibre-stage24-dry-run.md`](p5-h31-component-fibre-infinity-marked-fibre-stage24-dry-run.md),
and the executable batch is frozen in
[`catalog/batches/p5-h31-component-fibre-infinity-marked-fibre-stage24.json`](../../catalog/batches/p5-h31-component-fibre-infinity-marked-fibre-stage24.json).

## Corrected generator ownership

The original classifier routed
`derive_p5_h31_fibre_infinity_marked_fibre_elimination.py` to
`tools/explore/` solely from its `derive_` prefix. That split a single proof
leaf: the theorem names this generator as its regeneration command, the
primary is its only Python importer, and the primary pins its hash.

Commit `26f7a488` corrected only catalog ownership:

- category `tool_script -> claim_script`;
- claim family `null -> p5/h31/component-fibre-infinity-marked-fibre`;
- destination `tools/explore/... ->
  claims/p5/h31/component-fibre-infinity-marked-fibre/...`;
- family size `3 -> 4`;
- `tool_script 210 -> 209` and `claim_script 1072 -> 1073`; and
- generated destination counts `claims 1762 -> 1763` and
  `tools 209 -> 208`.

The correction changed neither medium classifier confidence nor
`review_required` manifest status, and changed no theorem, verifier, audit,
generator, navigation, lifecycle, or scientific-status byte. Approval came
from the separate proof-topology, status, consumer, and mechanical reviews,
not classifier confidence.

## Moved proof-obligation boundary

The exact theorem/primary/audit/generator family moved flat into
`claims/p5/h31/component-fibre-infinity-marked-fibre/`:

1. `P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md`;
2. `verify_p5_h31_component_fibre_infinity_marked_fibre.py`;
3. `audit_p5_h31_component_fibre_infinity_marked_fibre.py`; and
4. `derive_p5_h31_fibre_infinity_marked_fibre_elimination.py`.

The frozen source identities were:

| role | Git blob | raw Windows-checkout SHA-256 |
|---|---|---|
| theorem | `f1e632a06283b316469c4735bd6ffc72acc45436` | `ace531fdb3240c10cc1a74e14235a177bd2c68766acaa63aca8c45de429f035c` |
| characteristic-zero primary | `03eaacb2daf5df572e0e3cf6f62e8233961583a9` | `3dc62b644474c0b9d41d74d4b99ac1e588268f58bdc0f4292765fb42ed2d7d34` |
| modular audit | `660fc27c5ced8b9b4f957c9f00b12ebe71ec52ea` | `320c2f2820ac818bfdfc63c3e4cfd229c6371f6a6412055cf42ba5b3c059d16a` |
| exact elimination generator | `9f2f1ddf68ff6e583713f30168833d1f94fdf9d5` | `5a905ec64ae26083b898be8f6941300503c1d3681540aac0dac3dd4b81df3f2a` |

The four artifacts are one complete, separable divisor-scoped proof leaf:

```text
first known pure-rank-two component
  -> first-plane Schubert-infinity divisor outside the finite chart
  -> H,N != 0; E arbitrary; projective direction (A,D)!=(0,0)
  -> bijective row action normalizes H=N=1
  -> every marking a_i+t_i b_i for arbitrary t in C^4
  -> every distinguished-source coordinate q=0,1,2,3
  -> every binary Delta_2 extension with both diagonals nonzero
  -> fourteen mixed equations and exact saturated elimination over Q
  -> 21 minimal projection components split into 25 rational charts
  -> kernel dimensions 2:18 and 3:7
  -> 154 selected nonzero residual products generate the unit ideals
  -> rank-three contradiction
  => the complete marked-basis fibre on this first-plane divisor is empty

the rest of the projective boundary, the finite chart, the whole internal
E=0 divisor, second/further components, H22, component exhaustiveness,
P5 -> Delta3, gluing, and global resolution remain outside this leaf
```

The primary is the characteristic-zero proof replay. It reconstructs the
normalization and permanent identities, runs all four exact absolute
projections, checks all 21 minimal components and 25 residual-cover charts,
and proves all characteristic-zero unit ideals. It retains `verified: true`,
the `4/21/25`, `2:18,3:7`, and 154-product counts, complete first-plane fibre
true, and whole internal-`E=0`, additional-component, and global fields false.
Those false fields are scope boundaries; they do not deny the `E=0`
intersection included in this first-plane leaf or downgrade separately proved
sibling results.

The exact generator is proof-producing support, not independent evidence. It
constructs the four saturated projection programs consumed by the primary.
The modular audit imports neither this primary nor this generator and uses a
different finite-field enumeration route over `F5/F7`. It is independent of
the family primary and characteristic-zero proof route, but not hermetically
implementation-independent: it imports eight computational primitives from
the staying `audit_p5_h31_marked_basis_fibre_classification.py`. Its role is
modular QA; the characteristic-zero residual-cover ideals remain the proof.

The migrated `claims/p5/h31/component-fiber-infinity/` triple remains the
live narrower canonical-section predecessor. This Stage 24 successor adds all
kernel-row shifts and the complete marked-basis fibre on the same plane
locus. The predecessor is neither withdrawn nor superseded. No selected
artifact has a curated theorem-ledger entry or formal counterpart, and Stage
24 adds neither.

## Preserved conflicts and exclusions

Stage 24 neither consumes nor adjudicates the separate root
`P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md` four-file
family. Its theorem says fourteen certificate strata while its primary
constructs, asserts, and reports sixteen. That claimed-proof/verifier
contradiction remains owner-gated. The fourteen mixed equations in this
selected family are a different count; its 21-component, 25-chart proof has
no corresponding cardinality conflict.

The pre-existing P4 attribution conflict between the whole internal `E=0`
description and the separate nonzero chart divisor `D=0,a!=0` remains
unadjudicated. A migrated link or replay cannot validate that prose edge. The
broader first/second-component status-provenance conflict likewise remains
owner-gated and unconsumed.

This package does not close the rest of the first component's projective
boundary, its finite chart, the whole internal `E=0` divisor by itself, the
second diagonal-quadric or any further component, component exhaustiveness,
weighted `H22`, `P5 -> Delta3`, arbitrary-order/local-to-global gluing, the
prize graph, or the global conjecture.

## Pure move and mechanical repair

Against its direct parent, commit `cd0b8256` contains exactly four `R100`
moves plus the corresponding manifest transaction. Scientific bytes are
identical across the move. The manifest changes only the four selected
records from `review_required` to `moved`, records the frozen batch, and
updates deterministic summary fields:

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

The frozen root baseline and exact end-state allowlist are unchanged.

Commit `37de804` repairs exactly 13 files. The selected primary, audit, and
generator install shared bootstrap before repository imports; use `HERE` for
package-owned theorem/sibling paths and `REPO_ROOT` for staying dependencies
and ignored outputs; and preserve their mathematical algorithms, cases,
assertions, and status fields. The sole staying operational consumer,
`verify_p5_high_coordinate_partial_frontier.py`, retargets the moved theorem
dependency. No outside module imports the selected primary, audit, or
generator, and the selected primary remains the generator's sole importer.

Within the 13-file repair, the deterministic rewriter changes exactly six
Markdown links and three fenced replay commands across six Markdown files:
the moved theorem, canonical predecessor theorem, alternative-strategy map,
high-coordinate frontier, marked-basis classification, and root README. It
has zero ambiguity and zero ledger relocation, and its second pass is a
`0/0/0` fixed point.

The other repair surfaces are the three selected executable repairs, the one
staying high-coordinate consumer retarget, the theorem ledger, and two
navigation files. Exactly four existing ledger hashes refresh mechanically:

- verified high-coordinate frontier -> `cb1f3200d27f9855`; and
- the three root-README entries -> `0e3e92ffbdb54440`, retaining statuses
  `open`, `verified_generic`, and `partial`.

All other ledger fields remain unchanged. Navigation adds
`component-fibre-infinity-marked-fibre/` as the eighth scoped H31 exception,
records 31 H31 package directories, states the complete first-plane
Schubert-infinity scope and shared-helper audit limitation, and preserves
`component-fiber-infinity/` as the separate live canonical predecessor. It
does not imply projective-boundary, whole-component, or component-exhaustive
closure.

The post-repair raw SHA-256 values of the moved package are:

| artifact | SHA-256 |
|---|---|
| theorem | `09e07a378f1b8cba14aedddf7c7efcffdfdfdd5af808d38bbbe4e5b6b47770e4` |
| primary | `a758f5b2452977f3c265bab38ca88b5153d9e47459c004e74c006a9273465e05` |
| audit | `0837798730ac2aa5cc04ccf72855cc857d056724759814c9b2d2f152905eb626` |
| generator | `753885002c5a335c2db2c9a368409ddf216f3ccfea15a056e5539e5ffeab8085` |

## Scientific replay matrix

The complete affected closure is 14 unique executables and 24 scientific
invocations: 13 JSON executables in 16 invocations, plus eight deterministic
text invocations of the moved generator. Every invocation ran exactly once,
strictly serially, through
`uv run --quiet --python 3.13 --with sympy --with python-sat python`.
All 24 returned rc=0 with empty stderr. The selected primary and the
component-19 `phi=+/-1` derivation used their established WSL/Singular routes
without overlap.

The three paired JSON executables ran from repository root and by absolute
path from a fresh foreign working directory:

| rows | executable | root s | foreign s | preserved assertion |
|---|---|---:|---:|---|
| 1--2 | moved characteristic-zero primary | 31.566 | 21.858 | objects equal after removing only `elapsed_seconds`; internal values 23.618/20.317; exact 4/21/25, `2:18,3:7`, 154; complete scoped fibre true; internal-`E=0`/additional/global false |
| 3--4 | moved modular audit | 3.219 | 3.211 | byte-exact; four orientations; exact `F5/F7` and total census; modular QA, global false |
| 5--6 | staying high-coordinate primary | 1.369 | 1.461 | byte-exact; census 6,495 / 1,680 / 1,170 / 510; `P5 -> Delta3` and global false |

The ten root-only JSON executables also passed:

| row | executable | elapsed s | preserved assertion |
|---|---|---:|---|
| 7 | canonical predecessor primary | 2.752 | field `C`; `Delta_0(01)=0`; `[H,N]`; `(A,D)!=(0,0)`; six certificates; all four orientations true; H31/P5/global false |
| 8 | canonical predecessor audit | 95.224 | `F5` 1,920/17,408/17,408/0 and `F7` 12,096/160,704/160,704/0; zero ambient maps and Grassmannians |
| 9 | P4 toric-boundary primary | 0.837 | 28 lattice points, 12 facets, 11 genuine divisors, 44 pairs = 21 gate + 23 all-rank; H31/P5/global false |
| 10 | P4 toric-boundary audit | 0.909 | independent 28/12 and 21/23 reconstruction; zero ambient maps and Grassmannians |
| 11 | marked-basis classification primary | 12.474 | 20 certificate strata; finite known-family fibre true; projective boundary, additional components, and global false |
| 12 | marked-basis classification audit | 2.181 | 426 markings, 6,234 kernel directions, 4,498 extensions, 32 rejected `L=0` artifacts; zero ambient maps and Grassmannians |
| 13 | high-coordinate audit | 3.365 | independent 6,495 / 1,680 / 1,170 / 510 census; P5/global false |
| 14 | H22 actual mask-6 audit | 1.187 | all 12 scoped flags obstructed; label remains `VERIFIED`; global false |
| 15 | component-19 `phi=+/-1` derivation | 16.687 | construction checks pass; label remains `CANDIDATE` |
| 16 | component-19 `qphi=-1` axes derivation | 3.542 | actual lift false and higher obstruction true; label remains `CANDIDATE` |

The moved audit retained exactly:

- `F5`: 351 projection points, 29 projection-closure artifacts, 3,096
  binary extensions, and 5,188 selected-minor tests;
- `F7`: 703 / 43 / 11,700 / 19,014; and
- totals 1,054 / 72 / 14,796 / 24,202.

For each `q=0,1,2,3`, the moved generator ran from root and a fresh foreign
CWD with `--components` and without `--run`. These no-run calls printed
deterministic Singular programs but did not invoke Singular:

| rows | q | root s | foreign s | byte-exact stdout SHA-256 |
|---|---:|---:|---:|---|
| 17--18 | 0 | 1.488 | 1.549 | `d185832bbb01b47bee13a62753f9e169fffa4b4da097828f0548f7db77b2c294` |
| 19--20 | 1 | 1.725 | 1.854 | `56c8f13d0ed12a30cac7c46dcab31fb0def6a221f4d2e5d2dc64def9952c28de` |
| 21--22 | 2 | 1.684 | 1.584 | `4d9e8d2dbab41f7420b6428e9e07ef0c46c79d9325002e4b36bb1ab4a29e078a` |
| 23--24 | 3 | 1.492 | 1.510 | `e48880ca0533df259769fd4ee7f7f520398709dbbb360d814c01cb79389e0088` |

All 16 JSON captures parsed. Every one of 115 emitted theorem, primary,
source, generator, input, output, and dependency hash assertions matched the
current bytes of 89 uniquely named repository files. The four selected root
paths are absent. Exactly eight JSON executables wrote only ignored,
untracked repository-`tmp/` files, and each generated object parse-matched its
preserved stdout. Five JSON executables were stdout-only; the generator was
one stdout-text executable; no executable wrote tracked output. The seven
matrix foreign directories remained empty, and the tracked/index tree did not
drift.

Every first stdout, stderr, rc, timing, argument vector, and SHA-256 is
preserved outside the repository at
`C:\Users\Yeste\.codex\run-artifacts\stage24-20260809T133353Z`.

## Isolated import probes and non-evidence tooling record

The import-only probes were separate from the 24-invocation matrix. Each used
a robust stdin wrapper from its own fresh foreign directory and executed
exactly once:

| row | moved module | elapsed s | result |
|---|---|---:|---|
| 25 | primary | 1.989 | rc=0, empty stderr, `IMPORT_OK`, empty foreign directory |
| 26 | audit | 0.430 | rc=0, empty stderr, `IMPORT_OK`, empty foreign directory |
| 27 | generator | 1.046 | rc=0, empty stderr, `IMPORT_OK`, empty foreign directory |

Before row 1, an initial preflight compared the full HEAD hash to the supplied
short pin and stopped before creating a run artifact or launching a process.
The corrected preflight established the exact full head; this was not a
scientific invocation or replay.

After all 27 preserved results existed, the first read-only offline assertion
aggregation stopped at predecessor certificate counting because Windows
PowerShell strict mode did not expose `.PSObject.Properties.Count`. It
launched no Python, Singular, verifier, audit, generator, or import process.
The corrected read-only parser consumed the same preserved artifacts and
passed 246 checks with zero failures. This parser event is neither a failed
scientific run nor theorem evidence, and no scientific invocation was
automatically rerun.

## Validation and publication boundary

At substantive head
`37de804fc74dd4813ed3b66853d26b8944e7bd35` and tree
`8e2cb0df95582b2c5887f94abfb3087f9179fbaf`, the complete pre-report local
index floor passed:

- `check_hygiene.py`: all 1,698 Python files compile, all 822 pre-report
  Markdown files have resolving local links, all 86 ledger hashes match,
  root is 1,959 files + 9 directories = 1,968 entries, root debt is
  `1,952 grandfathered / 0 new`, and all 405 retired-path/provenance records
  pass;
- all 152 migration-tool tests;
- all 14 fourteen-vertex cycle-cover lattice tests;
- deterministic rewriter fixed point `0/0/0`; and
- clean tracked/index diff checks after the replay matrix.

Pre-report pull-request run
[`31316983114`](https://github.com/YesterdaysLemon/open-graph-theory-with-prize/actions/runs/31316983114)
succeeded at the exact substantive head, including hygiene, migration tests,
the self-contained lattice module, and rewrite closure.

Adding this report raises the Markdown count from 822 to 823. The
report-inclusive index floor, fresh Tier-2 semantic/status and
mechanical/provenance/bypass referee passes, and final exact-head pull-request
CI remain pending publication gates. Stage 24 is not merge-ready until those
gates pass on the unchanged reviewed report candidate, followed by the normal
head-guarded merge.

## Stop boundary

Stage 24 stops at the complete marked-basis fibre on the first-plane
Schubert-infinity divisor of the first known pure-rank-two component. It does
not execute or repair the blocked chart-boundary fourteen-versus-sixteen
family, adjudicate the P4 or broader component-provenance conflicts, or
extend the theorem to the rest of the projective boundary, the finite chart,
a second or further component, component exhaustiveness, weighted `H22`,
`P5 -> Delta3`, local-to-global gluing, or global resolution.

The global Krenn-Gu conjecture remains **UNRESOLVED**.
