# Layout migration Stages 27-29 reviewed plan

Status: **STAGE 27 COMPLETE AND VALIDATED; STAGES 28-29 REMAIN REVIEWED,
UNFROZEN, AND UNEXECUTED.**

The global Krenn-Gu conjecture remains **UNRESOLVED**. This plan changes
filesystem and executable-path ownership and corrects stale ledger mappings
for already-documented evidence carriers. It does not change an underlying
theorem, scope, lifecycle, evidence role, finite-case quantifier,
formalization status, or global status.

In this plan, an exact size, set, or hash refers to migration membership or
identity, and a complete N-file subtree or forest refers to ownership closure.
Neither term asserts mathematical case-cover completeness unless that is
stated explicitly.

## Live base and target

This review was performed on clean `main` at:

```text
commit: d6189369104002268530476d64a2fbbd168ebf5c
tree:   1853517f3712781b29321f5508ef8785491ba5f8
```

The measured root has 1,953 files and 9 directories, or 1,962 entries.
GitHub's repository-contents response returns only 1,000 entries at this
commit. To put the root strictly below that cap, at least 963 root files (and
hence entries) must leave root. The reviewed plan moves 964 distinct root
files:

| stage | exact members | projected root entries | projected grandfathered debt |
|---|---:|---:|---:|
| current | 0 | 1,962 | 1,946 |
| 27 | 587 | 1,375 | 1,359 |
| 28 | 201 | 1,174 | 1,158 |
| 29 | 176 | 998 | 982 |

The three sets are pairwise disjoint. Their canonical aggregate mapping hash
at the reviewed base is:

```text
d5f60ec990e841cd33fd3267ab429928dc41439cfb95663f1aea659cbc3ad02d
```

Each stage will still be frozen separately against its actual post-merge base
commit and tree. A later stage may have different source blobs because an
earlier fixed-point link rewrite can legitimately re-anchor links in a
staying document. The old-path/new-path mapping hash is independent of that
expected source-byte change.

## Review method and corrections

Filesystem/classifier topology, executable/provenance topology, and
mathematical proof-obligation topology were reconstructed independently.
Three independent review roles were used:

| review | surface | result |
|---|---|---|
| root inventory | exact membership, catalog state, collisions, hashes, root arithmetic | exact 587/201/176 disjoint plan; 998-entry projection |
| proof forest | theorem/evidence ownership, lifecycle, scope, four owner conflicts | accepted selected families; rejected conflict-bearing and misowned alternatives |
| consumer graph | imports, path literals, subprocesses, hashes, staying consumers | Stage 27 bounded; Stages 28-29 are Tier-2 high-repair but mechanically executable without helper extraction |

Adversarial review changed the initial proposal materially:

1. A classifier-wide arbitrary-order batch was rejected. It would have split
   evidence packages and consumed a misowned Component20 conflict surface.
2. The complete 42-file `ROOT_M7` subtree was kept together. Two primary
   verifiers initially proposed for `src/krenn_gu` were corrected to claim
   ownership.
3. Three directly read arbitrary-order antecedent triples were added so moved
   primaries do not leave executable theorem dependencies at root.
4. Component21, Component23, embedded-P3, marked-basis/H31, high-coordinate,
   weighted-`p+q`, Component20, Branch B, and partial-legacy alternatives were
   rejected.
5. Three apparently standalone tools were found to have 62 inbound import
   edges from 61 distinct importer files and were removed from the taper.
6. A replacement tool was found to overlap the finite set and was
   deduplicated. A disjoint replacement restored a one-file margin beyond the
   minimum strictly-below-cap reduction.
7. The finite/P4 and P5 stages were classified as Tier-2 path migrations,
   not pure-move tranches. Their repair surfaces are explicit validation
   obligations rather than reasons to rerun mathematics.

## Stage 27: high-order symbolic forest and minimal tool taper

Exact size: **587**.

Canonical mapping SHA-256:

```text
cc379f4cf74ebb7c8ffbf428e8a68acca6f18703e3f5e95d70183f2f5887f7b0
```

Reviewed-base canonical source identity SHA-256 uses dictionaries of the exact
form `{"old_path": old, "new_path": new, "git_blob": index_oid}`, sorted by
`(old_path, new_path)` and serialized with sorted keys and compact JSON
separators:

```text
b644cf42195fe50215f33bc5dbf39917bc316cea3e3d01c9b4c443cb710801aa
```

Destination totals are:

```text
claims/arbitrary-order  352
claims/p7               183
claims/p6                39
tools/generate           10
tools/explore             3
```

### The 522-file core

- every current manifest `p7` member: 183;
- every current manifest `p6` member: 39;
- 92 classifier triples whose theorem, primary, and audit are all current
  arbitrary-order manifest members: 276;
- three supplemental theorem/primary/audit packages: 9;
- the six initially omitted `ROOT_M7` members, making its subtree exactly 42;
- three load-bearing arbitrary-order antecedent triples: 9.

The supplemental packages are:

- `ARBITRARY_ORDER_HAFNIAN_EULER_HESSIAN_CHANNEL_UNMIXING_AND_SINGULAR_DISCRIMINANT`;
- `EXACT_THREE_BLOCKER_PERMANENT_RANK_LEMMA`;
- `FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION`.

The Hessian unmixing theorem is characteristic-zero but conditional on legal
response-jet exposure that the current P7 forest does not supply. The
exact-three-blocker package is a structural reduction, and its F5 audit is
corroborating rather than a second characteristic-zero proof. The fourth-order
subrank package covers only the tight P4 endpoint; its F5 audit has the same
qualification.

The directly read antecedents are:

- `TWO_PORT_SEVEN_BLOCKER_REDUCTION`;
- `ODD_RESIDUAL_PORT_PERMANENT_EXTRACTION`;
- `ONE_NONBLOCKER_SURPLUS_PERMANENT_EXTRACTION`.

The two-port theorem reduces to three overlapping P5 systems whose
synchronization remains open. Odd-residual-port is the configured general
bridge. One-nonblocker-surplus is its narrower special case, but is not
lifecycle-marked as superseded.

The two corrected `ROOT_M7` primary mappings are:

```text
verify_root_m7_endpoint_legal_certificate_hitting_minimum_two_exclusion.py
verify_root_m7_one_edge_a10_shared_pure_mixed_factor_obstruction.py
```

Both go to `claims/arbitrary-order/`, not `src/krenn_gu/`. Their only bare
import consumers are sibling `ROOT_M7` claim verifiers, and the complete
42-file subtree moves together.

That 42-file completeness is ownership closure only. The relative
fourth-incidence shell excludes 908 supports, not all
`binomial(104,4) = 4,598,126` supports. Arbitrary P7/local-to-global remains
**UNKNOWN**, and the global conjecture remains **UNRESOLVED**.

### Eleven additional exact arbitrary-order triples

- `FIVE_ROOT_NO_TORUS_CODIMENSION_TWO_THEOREM`;
- `FOUR_RESIDUAL_EVEN_WICK_TOWER_AND_P6_SYNCHRONIZATION_THEOREM`;
- `HAFNIAN_CONVOLUTION_SPLIT_LEMMA`;
- `MULTI_STAR_BLOCKER_FACTORISATION_LEMMA`;
- `RESIDUAL_HAFNIAN_COMMON_COFACTOR_GRAM_THEOREM`;
- `RESIDUAL_HAFNIAN_HESSIAN_KNESER_ETALE_AND_JET_INTEGRABILITY_THEOREM`;
- `RESPONSE_JETS_AS_PRINCIPAL_DELETION_DECKS_AND_ROOT_PARITY_LEGALITY_THEOREM`;
- `THREE_COLOUR_BALANCED_BRIDGE_INTERSECTION_THEOREM`;
- `THREE_COLOUR_BLOCKER_UNION_LEMMA`;
- `THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM`;
- `UNIVERSAL_FIVE_BLOCKER_DIVISIBILITY_LEMMA`.

Their 22 currently unclassified named primary/audit carriers move with their
theorems. A finite or combinatorial audit remains corroborating when the
written theorem is characteristic-zero; colocation does not promote it into
an independent characteristic-zero proof.

Three superficially similar triples are excluded:

- `FIVE_ROW_PROJECTIVE_INCIDENCE_LEMMA` is P5-owned;
- `FIVE_ROOT_DIAGONAL_TARGET_INCIDENCE_SCHUBERT_DUALITY_AND_COFACTOR_LINE_THEOREM`
  is P7 full-sensor/Schubert-boundary-owned;
- `UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM` depends on the still-valid
  symmetry/sign-table part of the partially withdrawn
  `SIX_PERMUTED_POTENTIALS_LEMMA` lineage. Its older finite residual
  applications are withdrawn. Both remain at root to keep that mixed
  lifecycle coherent; this is not a live theorem relying on a withdrawn step.

### Nineteen asymmetric-evidence leaves

The following exact membership set moves to `claims/arbitrary-order/`:

```text
ADJACENT_PORT_DETERMINANT_TRANSPORT_LEMMA.md
verify_adjacent_port_determinant_transport_lemma.py
DOUBLE_STAR_ANNIHILATION_LEMMA.md
EVEN_CYCLE_FEASIBLE_SET_EXPANSION.md
verify_even_cycle_feasible_set_expansion.py
FIVE_ROOT_ZERO_COUPLING_INTERSECTION_LEMMA.md
verify_five_root_zero_coupling_intersection.py
FULL_COLOUR_SUPPORT_ORBIT_LEMMA.md
INTEGER_SIGNED_LATTICE_TRANSPORT_THEOREM.md
verify_integer_signed_lattice_transport.py
MINIMAL_SINGLETON_CIRCUIT_RECTANGLE_THEOREM.md
verify_minimal_singleton_circuit_rectangle_theorem.py
ODD_FULL_FACTOR_ONE_TERM_THEOREM.md
verify_odd_full_factor_one_term_mechanism.py
PARTIAL_MINIMAL_SINGLETON_CIRCUIT_DICHOTOMY.md
verify_partial_minimal_singleton_circuit_dichotomy.py
RECIPROCAL_PORT_ORIENTATION_CORRECTION.md
verify_reciprocal_port_orientation.py
THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md
```

Evidence asymmetry is intentional: six documents have no separate replay,
and the remainder have one named replay rather than a primary plus an
independent audit. `PARTIAL_*` remains partial;
`RECIPROCAL_PORT_ORIENTATION_CORRECTION` remains a correction, with older
finite artifacts still withdrawn.

### Thirteen non-claim tools

The selected tools retain their existing classifier destinations:

```text
tools/explore/analyze_dimacs_extension_clause_core.py
tools/explore/explore_twelve_vertex_complement_matching_chains.py
tools/explore/extract_fourteen_vertex_transport_residuals.py

tools/generate/augment_degree3_anchor_reciprocal_dichotomy.py
tools/generate/augment_degree3_pure_tensor_support.py
tools/generate/augment_dimacs.py
tools/generate/augment_fourteen_vertex_rule_cnf_with_partial_circuit_supports.py
tools/generate/condition_dimacs_on_selector_set.py
tools/generate/reorient_fourteen_vertex_minimum_activity_certificates.py
tools/generate/retrofit_fourteen_vertex_c4_c4_c6_chain_minimum_certificates.py
tools/generate/solve_dimacs_pysat.py
tools/generate/materialize_verified_dimacs_clause_set.py
tools/generate/augment_fourteen_vertex_rule_cnf_with_binomial_support_closures.py
```

These are non-claim support tools and do not by themselves discharge a
theorem obligation. The last augmenter has a pre-existing provenance
weakness: its mandatory-unit `--verified-support` route records but does not
compare an immutable stored hash for the referenced partial-analysis bytes.
The immediate staying caller still performs its verifier/generator/audit
sequence. This weakness is preserved and reported; the move does not upgrade
the route into a durable certificate chain.

### Stage 27 executable repairs

The source set has zero inbound Python imports and zero internal
cross-destination imports. Five outbound imports come from two selected leaf
verifiers and are preserved by the shared bootstrap with root imports:

- `verify_integer_signed_lattice_transport.py`: four root helpers;
- `verify_odd_full_factor_one_term_mechanism.py`:
  `explore_random_even_cycle_forks.py`.

A post-plan folded-AST scan also found 18 selected scripts that construct a
co-moving theorem path as `Path(<root basename>)`. They need package-local
`HERE` paths after the move. This selected-to-selected same-package path
surface was absent from the initial external-path scan; it changes the repair
inventory, not the 587-file mapping or proof boundary.

Four selected arbitrary-order verifiers require final `REPO_ROOT` paths to
one P7 primary and three P6 theorem documents. Staying consumers include the
four `FAST_VERIFIERS` entries in `check_hygiene.py`, two P5 pair-signature
loaders, one `Containerfile` example, and these exact additional executable
surfaces:

- six finite scripts whose CLI defaults read
  `THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md`:
  `analyze_ten_vertex_degree_six_kotzig_port_survivors.py`,
  `analyze_ten_vertex_permuted_potential_survivors.py`,
  `audit_ten_vertex_degree_six_kotzig_ports.py`,
  `audit_ten_vertex_permuted_potential_survivors.py`,
  `explore_ten_vertex_degree_six_kotzig_ports.py`, and
  `scout_twelve_vertex_six_potential_cells.py`;
- `run_fourteen_vertex_mandatory_unit_binomial_cegar.py`, with one subprocess
  argv path to the moved binomial-support augmenter;
- `run_fourteen_vertex_symmetry_binomial_cegar.py`, with three more argv paths
  assembled from adjacent string literals and therefore invisible to a plain
  full-basename text scan.

The Stage 27 dry run must freeze the line-exact repair inventory before the
batch is approved.

The curated ledger has two stale evidence mappings in this forest. Exact
Three Blocker and Support-four P5 contraction each explicitly name a primary
and distinct finite-field audit in the owning document, while the ledger says
one or both carriers do not exist. Stage 27 will record or retain both primary
paths with `script_is_the_verifier` provenance and both audit paths with
`independent_modular_audit` provenance, with an explicit scope wall: the
audits independently reconstruct only their finite-field formula/coefficient
layers and are corroborating evidence, not second characteristic-zero proofs.
Mathematical status and scope remain unchanged.

## Stage 28: bounded finite forest plus conflict-free P4 packages

Exact size: **201**.

Canonical mapping SHA-256:

```text
2715a521e40f5ad6815af2044af1b1c075bf1cf29de81b076c4de239db5cf9a6
```

### Finite 133

Select all 49 current claim documents in the five finite families and every
current-root Python carrier named by them, for 84 carriers:

```text
claims/finite/n14  70
claims/finite/n08  28
claims/finite/n10  15
claims/finite/n12   5
claims/finite/n06   2
tools/explore       6
tools/generate      4
src/krenn_gu        3
```

Existing mappings are retained for 16 classified carriers. Each of 68
currently unclassified carriers has one unique owning finite destination.
No finite theorem is promoted beyond its stated order, support, orbit,
selector, connectivity, equality, or conditioned-CNF hypotheses. A finite
survivor is not a counterexample, and no sampling run becomes exhaustive.

Finite-subset canonical mapping SHA-256:

```text
09206352818278ce66e9112ea6045ca34e0df12365c8caf84c08c16eb4439d30
```

### P4 safe 68

Select each current P4 document whose named current-root Python evidence
stays in P4, plus that evidence, then remove the exact common-active
weighted-`p+q` triple. The resulting 68 files comprise 50 classification
members and 18 boundary members.

P4-subset canonical mapping SHA-256:

```text
70cdd782d78c47f1ae0f7deaaf9a1178c578df88a60bdd8c40ecad6b056b4295
```

Explicit exclusions are:

- `P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY` and its two scripts;
- both `P4_COMPONENT20_*_PROOF_B` documents and their conflict carriers;
- `P4_INOUT_PATH_STRATUM_WORKING_NOTE` and its external exploratory tools.

`P4_FIRST_COMPONENT_APOLAR_TRIANGLE_NORMAL_FORM` is included only as its
dense P4 normal form; it explicitly leaves other Borel orientations and
boundaries open and does not consume disputed P5 first/second-component
closure. The selected diagonal-quadric packages state lower bounds or
subcases, not component exhaustiveness. `P4_BOREL_GAUGE_CORRECTION` preserves
the withdrawn lifecycle of its antecedents.

### Stage 28 executable repairs

This is a **Tier-2 high-repair path migration**, not a pure-move tranche.
The exact consumer review found:

- finite: 37 distinct importer-file edits;
- P4: 9 distinct importer-file edits;
- combined: 46 distinct importer files, with no overlap observed;
- 12 actionable staying finite path files with 27 literals;
- 56 staying Python files with 73 P4 path literals.

Shared bootstrap plus exact `expose_claim_package` calls preserve
selected-to-root and claims-directory imports. Imports of the three selected
`src/krenn_gu` providers become qualified package imports; tools/explore
targets receive their exact tool-directory exposure. No helper extraction,
algorithm change, assertion change, or evidence-schema change is required.

One staying Component20 audit constructs `git diff` arguments from
`Path.name`. Its `frozen_component_sources_unchanged()` guard is already false
at the reviewed base against historical commit `f997c...`: three sources moved
with path-only link/command rewrites in earlier stages; the fourth already
received path-only link rewrites and moves in Stage 28. Merely changing the
arguments to repository-relative paths would therefore preserve a false
guard. The Stage 28 freeze must retain the old provenance, establish an exact
post-rewrite source checkpoint/blob set, and compare the four current
repository-relative source blobs to that checkpoint.
A focused test must exercise the repaired guard. This is a bounded
provenance/path repair; it does not consume or adjudicate the excluded
Component20 claim package or rerun its mathematics.

## Stage 29: conflict-free P5 frontier, boundary, and coordinate forest

Exact size: **176**.

Canonical mapping SHA-256:

```text
6577eb9544a8bcc5c20f0c6a204a7248b1db68ec15331d12281e791baccd5d7e
```

Start from current non-moved manifest members in
`p5/frontier`, `p5/boundaries`, and `p5/coordinate-cegar`. Remove the exact
high-coordinate conflict triple. Select a document only when every named
current-root Python carrier is in those families, then select those carriers.
From that intersection:

```text
252
+ 2 omitted C++ primaries
+ 6 omitted q4_211 reduction-triple files
- 66 Component21 files
- 18 Component23 files
= 176
```

The additions are:

- `verify_p5_no_quartic_restriction_equations.cpp`;
- `verify_p5_no_quintic_restriction_equations.cpp`;
- complete triples for `P5_Q4_211_ADJACENT_P4_PENCIL_REDUCTION` and
  `P5_Q4_211_SIMULTANEOUS_PENCIL_REDUCTION`.

This restores the complete 60-file normalized `q4_211` forest. Its P4
marked-Delta2 antecedents have already moved in Stage 28. The complete
49-file normalized `q5_221` forest also moves, with its working-note lifecycle
unchanged.

Complete here means artifact closure within the normalized `q4_211` and
`q5_221` branches. Neither is an exhaustive P5 case cover.

Explicit exclusions include:

- the `P5_HIGH_COORDINATE_PARTIAL_FRONTIER` triple;
- all 22 `P5_COMPONENT21_*` triples;
- all six `P5_COMPONENT23_*` triples;
- every document/carrier whose closure crosses outside the selected
  intersection, including the alternative-strategy, component-boundary,
  high-coordinate-chart, specialization-meta-theorem, and omitted
  q5_311/evidence packages.

This is also a **Tier-2 path migration**. The consumer graph found 25
distinct importer files: 8 staying inbound, 15 selected outbound, and 2
internal-cross-only. The 40 import edges are preserved by the same exact
bootstrap/exposure pattern. Remaining repairs are bounded to the
high-coordinate staying consumer, q4 constituent paths, P3/P4 and research
snapshot roots, and pair-signature loaders. No helper extraction or
mathematical replay is required.

## Four owner-gated conflicts excluded from all stages

1. The H31 chart-boundary marked-fibre theorem says 14 certificate strata;
   its primary asserts and reports 16.
2. P4 internal-`E=0` versus chart `D=0,a!=0` attribution is unresolved.
3. First/second-component provenance and closure disagree across marked-basis,
   toric, high-coordinate, outer-boundary, README, and synthesis artifacts.
4. Weighted-H22 `p+q=0` status disagrees between the dedicated root forest
   and migrated aggregate provenance.

Conflict 1 is a genuine theorem/primary contradiction and a repository stop
condition. Conflicts 2-4 are ownership/provenance ambiguities, not adjudicated
mathematical contradictions. No exact counterexample was found.

The Component20 ten-file package, its two P4 proof-B dependencies,
embedded-P3, H31 common-center, Component21/23, Branch B, high-coordinate
triple, and all legacy routing remain outside the reviewed batches. The
legacy exclusion includes all six wholly withdrawn and four partially
withdrawn documents; their evidence is not yet coherently packaged.

## Freeze, execution, and validation contract

For each stage:

1. Start from clean, merged `main` in a fresh isolated worktree.
2. Record the exact base commit, base tree, manifest SHA-256, classifier
   SHA-256, canonical mapping hash, and canonical source identity digest.
3. Refine only the reviewed catalog records, remove newly classified paths
   from `unclassified-files.json`, and obtain separate semantic and
   mechanical review because catalog/policy and bootstrap consumers are
   Tier 2.
4. Commit the dry-run review, then commit an exact batch under
   `catalog/batches/` with the authorized Codex reviewer attribution.
5. Run `execute_moves.py --dry-run`, then execute the exact committed batch
   with `git mv`.
6. Verify every move as R100 before repair and verify source/destination Git
   blob identity against the frozen source records.
7. Apply only the frozen path/import/bootstrap, navigation, ledger, and
   provenance repairs. Do not edit mathematics.
8. Stage the index-complete candidate tree, run the link rewriter to a
   fixed point, and require zero ambiguous rewrites and zero stale executable
   paths.
9. Run no-bytecode syntax checks and an exact import/path smoke matrix for
   every changed importer, path literal, subprocess target, and hash consumer.
   Do not run unrelated theorem calculations.
10. Run the authoritative floor:

```text
git add -A
python check_hygiene.py
python -m unittest -v tests.test_migration_tools
python -m unittest -v test_fourteen_vertex_cycle_cover_lattice.py
python tools/migration/rewrite_links.py
git diff --exit-code
```

11. Obtain a fresh referee, require clean status and exact-head CI, merge,
    verify merged-main CI, and only then base the next stage.

Path/import changes receive focused import or launch probes. Unchanged
scientific sources and frozen computations are reused by blob identity and
ancestry. A wrapper, bootstrap, compiler, or tool failure is infrastructure
evidence and must not trigger solver or brute-force reruns.

## Completion gate

After Stage 29 merges:

- GitHub's contents endpoint must return all 998 root entries rather than the
  1,000-entry cap;
- `main` and `origin/main` must agree and remain clean;
- merged-main CI and the hygiene floor must be green;
- the four conflicts and all excluded packages must remain unadjudicated and
  unmoved, and their mathematical content/status must remain untouched; only
  separately frozen staying-consumer path/provenance repairs are permitted;
- the global Krenn-Gu status must still be **UNRESOLVED**.

At that point root readability is sufficient to pause layout work and return
to the next named symbolic reduction. Remaining root debt is future review
work, not authority for an immediate Stage 30.
