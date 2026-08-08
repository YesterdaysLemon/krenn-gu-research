# Stage 11 P5 proof-obligation and boundary topology reconnaissance

Status: **documentation-only reconnaissance; no scientific status change**

Baseline inspected: `main` at `920c79621d1901ae41d5fc91e46ae0ed1c7ce44a`, the merge commit for PR #39 (Stage 10).

This report reconstructs the remaining P5 surface after the Stage 9--10 generic-package migrations. It is not a move manifest, proof-DAG schema, theorem correction, or claim promotion. The global conjecture remains **UNRESOLVED**.

## 1. Executive finding

The remaining root-level P5 material is not primarily a backlog of independent

```text
theorem + verifier + audit
```

triples. It is a mixed forest containing:

- distributed closures in which several divisor or residual theorems jointly discharge one generic obligation;
- generic theorems with substantial specialization, projective-boundary, or exceptional-fibre debt;
- exact partial case trees whose closed children and open residuals must remain distinguishable;
- primary verifiers, audits, shared row/model builders, and provenance aggregators whose executable ownership differs from mathematical ownership;
- candidate, refuted, superseded, and exploratory artifacts retained as scientific lineage; and
- frontier syntheses that aggregate local results without proving the global frontier closed.

At the inspected baseline, a conservative root-level filename filter (`P5_`, `verify_p5_`, `audit_p5_`, `derive_p5_`, `check_p5_`, `explore_p5_`, `generate_p5_`, or `p5_`) finds 789 tracked entries: 281 Markdown files, 489 Python files, 17 JSON files, and 2 C++ files. This is a layout count, not a count of claims or proof obligations. Exact-prefix counts also undercount families whose descendants use component numbers or boundary names rather than the generic theorem prefix.

The central architectural conclusion is therefore:

> A future P5 ownership or proof-graph decision must reconstruct filesystem/classification, executable/provenance, and mathematical proof-obligation topology separately. The three graphs often overlap, but they do not coincide.

The topology is clear enough for a next design step, but the next step should be an evidence/ledger semantics pass. It is not yet safe to derive a machine-readable proof DAG from imports, hashes, filenames, or the current ledger `dependencies` field.

## 2. Baseline and scope

The investigation verified:

- local `main`, `origin/main`, and the PR #39 merge commit all resolved to `920c79621d1901ae41d5fc91e46ae0ed1c7ce44a` before documentation work began;
- the working tree was clean;
- `git fetch --prune` and a fast-forward-only pull found no intervening change;
- PR #39 was merged on 2026-08-08 and is the current Stage 10 baseline; and
- no later commit altered the P5 topology before this reconnaissance.

The authoritative first-pass sources were `AGENTS.md`, the layout-migration runbook, the proof-obligation and formalization interfaces, the Stage 9--10 reports and dry run, the three catalogs, and the P5/H31/H22 README surfaces named in the Stage 11 instructions. Older migration history was consulted only where a current ownership or dependency question required it.

No theorem, verifier, audit, ledger, certificate, snapshot, result, classifier, moved-path record, or scientific status was changed.

## 3. Three-graph verdict

The three-graph hypothesis survived systematic testing and is useful, provided it is treated as a separation of concerns rather than three views expected to agree.

### 3.1 Graph A: filesystem and classification

This graph answers where an artifact currently lives and where the classifier proposes it should live. It is useful for transactions, path rewrites, ownership review, and finding likely families.

It is not a proof graph. Examples:

- The component-23 generic H22 closure is spread across an old `PARTIAL` root and later `DENSE_OPEN`, special-value, ordinary-divisor, and residual files. The filenames record discovery order, not the final case-union theorem.
- The diagonal-quadric H31 closure includes middle-coordinate, end-coordinate, normalization, and outer-boundary files that a generic-theorem prefix count misses.
- The classifier itself identifies shared-library candidates with 81, 44, 39, 17, and 12 consumers. Proposed destination and current executable ownership are therefore already known to diverge.

### 3.2 Graph B: executable and provenance

This graph answers what code imports, calls, exposes, hashes, or replays. It is essential for replayability and migration impact analysis.

It is not automatically a mathematical dependency graph. Examples:

- Thirty-nine scripts directly import utilities from `derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py`. Most import `build_model`; the consumers span five filename groups, with the common-center and component-23 groups belonging to the same mathematical component family.
- A common-center `k=infinity` boundary verifier imports the unequal-complement H31 `component_rows` normal form. Its theorem explicitly says the generic component-22 theorem cannot be specialized to prove that boundary. This is shared implementation, not logical reliance on that generic theorem.
- `verify_p5_high_coordinate_partial_frontier.py` hashes 62 documents while explicitly leaving `P5_to_Delta3_resolved` and the global conjecture false. It is a provenance/frontier consumer, not a 62-premise proof of closure.
- A common-active H22 wall audit replays live premises, a superseded partial that must remain `UNKNOWN`, a historical artifact that must remain `REFUTED`, and a corroborating route that is explicitly not the proof route. A subprocess inventory is therefore semantically heterogeneous.

### 3.3 Graph C: mathematical proof obligations

This graph answers which mathematical claims, transformations, case covers, specializations, boundaries, and evidence relationships actually support a conclusion.

It contains structures absent from ordinary import graphs:

- exhaustive unions of normalized, support-two, and `r=0` cases for embedded-P3 H31 projective closure;
- a later residual theorem that consumes earlier dense-open and special-divisor results to close the component-23 generic H22 fibre;
- generic-to-divisor and divisor-to-exceptional-fibre descent;
- symmetry transfers between boundary charts;
- refutations of attempted arguments while the target obligation remains open;
- audits and corroboration that support confidence but are not mathematical premises; and
- frontier aggregation that records consequences without closing every upstream or downstream branch.

### 3.4 Where the graphs agree and diverge

They agree most closely for compact, self-contained packages such as the split-center H22 generic theorem. They diverge strongly for distributed boundary forests, shared implementation hubs, and evidence aggregators.

The divergence is often legitimate. It becomes risky when a migration or status inference silently substitutes one graph for another. In particular:

- filename proximity is evidence of likely family membership, not proof ownership;
- an import is evidence of an executable edge, not necessarily a theorem premise;
- a hash records provenance or replay scope until theorem prose establishes logical use; and
- a common mathematical owner does not imply that all code belongs in the same directory.

## 4. Provisional edge taxonomy

The following taxonomy is supported across several inspected families. It is conceptual; it does not freeze future schema field names.

| Edge | Meaning | Representative evidence |
|---|---|---|
| `LOGICAL_DEPENDENCY` | Claim B requires claim A as a mathematical premise. | Unequal-complement H22 D01 uses the verified H31 deletion-one theorem at weight infinity. |
| `REDUCTION_DEPENDENCY` | A proved transformation replaces one obligation with another precise obligation. | The high-coordinate frontier reduces a P5 obstruction to H31/H22 targets without closing them. |
| `CASE_COVERAGE` | Children jointly exhaust a stated case split. No child alone proves the parent. | Embedded-P3 H31 projective closure; component-23 finite H22 generic closure. |
| `SPECIALIZATION` | A generic/function-field result descends to a locus under proved specialization hypotheses. | Divisor-generic results followed by separately justified special-value fibres. |
| `BOUNDARY_DESCENDANT` | A divisor, fibre, projective chart, or endpoint remains after the generic result. | Embedded-P3 H22 projective coverage after normalized affine closure. |
| `RESIDUAL_REFINEMENT` | A partial factor or minor cover narrows the live residual obligation. | Unequal-complement D23 `h1!=0` factor tree and terminal `h2=0` closure. |
| `SYMMETRY_TRANSFER` | A proved involution or relabelling transports a closed chart to another chart. | Common-center transfers between `r=0` and `t=0` boundary pieces. |
| `PRIMARY_EVIDENCE` | A theorem is checked or replayed by its primary verifier. | The ordinary theorem/verifier pair in a compact generic package. |
| `PROVENANCE_DEPENDENCY` | An artifact hashes or records another artifact to pin evidence or lineage. | Equal-support H22 hashes P4 and H31 companions. |
| `EXECUTABLE_DEPENDENCY` | One program imports, calls, or subprocesses another. | Split-center H22 imports model helpers and H31 row constructors. |
| `SHARED_IMPLEMENTATION` | Claims use common machinery without one claim implying another. | The 39-consumer candidate-housed `build_model` utility. |
| `AUDIT_EDGE` | A distinct audit checks a claim or evidence package. It is not a mathematical premise. | Split-center's exact-rational no-import audit. |
| `CORROBORATION` | A computation supports confidence but is explicitly not the proof route. | Embedded-P3 finite-field checks and the common-active wall's alternate `r=0` chart. |
| `FRONTIER_CONSUMER` | A synthesis incorporates a local result into a broader open frontier. | The high-coordinate partial frontier's broad dependency/hashing surface. |
| `REFUTATION_OF_ARGUMENT` | Evidence invalidates an attempted route without deciding the target theorem. | The withdrawn unequal-endpoint Branch B coefficient-splitting argument. |
| `HISTORICAL_OR_SUPERSEDED` | An artifact preserves exploration or lineage but is not proof-active. | The superseded common-active partial and the diagonal point seed after subsumption. |

Two refinements were required beyond the initial Stage 11 list. `RESIDUAL_REFINEMENT` captures exact partial factor trees without pretending that every child is a boundary divisor. `REFUTATION_OF_ARGUMENT` distinguishes refuting a proof route from refuting the target claim. `SYMMETRY_TRANSFER` is also worth making explicit because it can discharge a chart only when the transport itself is proved.

Edge type and node status are orthogonal. A candidate or historical node may have executable or provenance edges without becoming a live logical premise. An audit may be strong evidence while remaining outside the mathematical premise chain.

## 5. Major family maps

These maps identify mathematical cohesion, not proposed move batches. File lists are intentionally restricted to load-bearing surfaces.

### 5.1 Embedded-P3

```text
H31 generic
  -> normalized boundary
  -> support-two boundary
  -> r=0 boundary
  -> projective case-union closure
  => entire embedded-P3 component closed for H31

H22 generic
  -> rank-two projected-line boundary
  -> rank-one collapse
  -> normalized affine closure
  -> r0=0 attempted transport [refuted]
       -> independently repaired t0!=0 endpoints
  -> projective coverage [still open]
       normal-mask + Grassmann-pivot + orientation endpoint strata
```

- Root claim: the P4 embedded-P3 component has H31 and H22 obstruction programs.
- Generic H31 core: theorem, primary, and audit; status verified at the generic point.
- H31 closure: `P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md` explicitly consumes the normalized, support-two, and `r=0` children. These are inseparable pieces of the same projective closure.
- H22 closure: generic/rank-two/rank-one results close the normalized affine chart. The old full `r0=0` projective transport is refuted; exact endpoint work repairs only the stated missing strata.
- Frontier consumer: the component-20 `p+q` wall uses the actual embedded mask-6 atlas, not a nonexistent full H22 projective closure.
- Open obligation: exact H22 projective coverage listed above.
- Migration cohesion: **H31 high; H22 medium-high**. The H31 forest is a genuine whole-family closure. H22 must preserve both refuted lineage and live projective debt.

### 5.2 Common-active binary triangle (component 20)

```text
H31 generic
  -> normalized affine + special divisors
  -> intrinsic wall
       -> exceptional zero bases / diagonal atlases
  -> p+q wall aggregate
       -> exceptional lower pair
       -> infinity endpoints
       -> embedded-P3 H31 closure

H22 generic [candidate-named, independently verified]
  -> intrinsic wall + exceptional fibres
  -> p+q wall aggregate
       -> nine-stratum case cover
       -> superseded partial / refuted route retained as history
  -> other parameter and projective boundaries [open]
```

- Root claim: common-active binary-triangle P4 component.
- H31 generic core and main boundary packages are verified, but the wall aggregates depend on real cross-component case coverage.
- H22 generic and intrinsic documents retain candidate names from discovery; current theorem/audit prose records independent verification. Names do not determine present epistemic status.
- Same-theorem structure: both `p+q` wall aggregates consume multiple child strata. Their subprocess inventories also preserve non-live history, so executable inputs must be typed before use as proof edges.
- Open obligations: other H22 special parameter/projective fibres and non-diagonal/source compactification limits.
- Migration cohesion: **medium-high**. Individual wall closures are cohesive; the entire family has shared and cross-component ownership.

### 5.3 Common-center-kernel-star H22 (component 23)

```text
old PARTIAL checkpoint
  -> dense-open supplement
       -> lambda=-1
  -> lambda=0
  -> lambda=1
  -> F-h2=0 ordinary divisor
  -> ordinary residual theorem
  => complete generic finite fibre
  + previously closed infinity fibre
  => complete generic weighted H22 fibre at the generic component point

boundary descendants
  -> r=0 / t=0 charts
  -> s=1, k=infinity line
  -> s=0, rt=1 face
  -> s=0, k=infinity projective corner surface
  -> wider source-torus / ambient degenerations [open]
```

- The root `P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_PARTIAL.md` honestly records an earlier unknown checkpoint.
- The later `...FINITE_ORDINARY_RESIDUAL_OBSTRUCTION.md` explicitly consumes the dense-open and special-divisor results and states the generic finite closure. The current P5 README synthesis records the same closure.
- This is the clearest example of one proof obligation distributed across files whose individual names/status headers cannot be read in isolation.
- Boundary descendants contain many exact children, but source-torus compactification and arbitrary ambient/Grassmann degenerations remain open.
- Executable mismatch: at least one common-center boundary reuses unequal-complement row machinery while explicitly denying specialization of the imported generic theorem.
- Migration cohesion: **high mathematical cohesion, medium readiness**. The exact member surface is large and an old partial root cannot move alone.

### 5.4 Unequal-complement common-kernel H22 (component 22)

```text
D01 orbit
  -> finite orbit closed
  -> infinity via H31 deletion-one theorem
  => D01 closed

D23 orbit [partial]
  -> h1=0 factor branches and residuals closed
  -> rho=0 / rho=-1 subcases closed
  -> h1!=0 factor tree
       -> H=h2=0 terminal closure
       -> selected factor intersections
       -> remaining factors [open]
```

- Root claim: generic weighted H22 fibre for the unequal-complement component.
- D01 is a complete case with an explicit H31 logical dependency at infinity.
- D23 is an exact partial case tree. The `h2=0` terminal result is load-bearing inside a larger cover but does not close its sibling factors.
- Candidate/shared implementation: several primaries and six audits reuse the candidate-housed `build_model` and H31 row constructors. That does not by itself weaken theorem status, but it narrows the audits' implementation independence and creates ownership risk.
- Open obligations: the remaining `h1!=0` D23 chart plus special component-parameter and projective/source/ambient charts.
- Migration cohesion: **high cohesion, low readiness** because evidence maturity remains partial and implementation ownership is shared.

### 5.5 Unequal-endpoint inward-star H22 (component 25)

```text
weight infinity + dense finite D01 [closed]

remaining finite D01
  -> A branch residual forest
  -> B branch residual forest
       -> old descent-only generic obstruction [withdrawn]
       -> corrected full-field generic-weight theorem
       -> T=0 / H=0 / N=0 and sparse-cover descendants

finite D23 [partial]
  -> lambda=1 all-marking slice closed
  -> other branches open

projective g=0 forest [partial]
  -> several sign sheets, generic D23 and k=0 closed
  -> special weights, D23 infinity, s=0, other charts open
```

- Root claim: the generic H22 obstruction on the component.
- Evidence maturity: a large exact partial forest, not a completed family theorem.
- Historical edge: the old Branch B coefficient-splitting route is explicitly withdrawn and unused by the corrected full-field theorem.
- Metadata conflict: `catalog/theorem-ledger.json` nevertheless labels that withdrawn document `verified_generic`, records no primary/audit, and points to the current matching document hash. The document says `WITHDRAWN AS A GENERIC OBSTRUCTION; VERIFIED IDENTITIES ONLY`; its primary and audit emit identities-only success and deny generic emptiness. This is committed metadata inconsistency, not worktree drift and not evidence that the live corrected route uses the withdrawn step.
- Open obligations: displayed finite D23 residuals, special/projective fibres, and remaining projective charts.
- Migration cohesion: **high intended cohesion, very low readiness** because boundary complexity is extreme and the ledger contains a direct status/evidence contradiction.

### 5.6 Diagonal-quadric elliptic H31

```text
slice / curve layer
  -> C/H marked curve
  -> E marked curve
  -> H=0 ruling
  -> pure-direction factored slice

elliptic generic theorem
  -> middle-coordinate dense chart
  -> end-coordinate dense chart
  -> genus-two exception
  -> t2=x and t3=1 divisors
  -> pivot complement
  -> normalization boundary rxD=0
  -> outer ABF=0 boundary
  => entire presently known diagonal-quadric component closed for H31
```

- The generic theorem also orchestrates later regular-chart closure.
- The outer-boundary theorem consumes the normalized affine work and concludes closure of the entire presently known component, including its projective parameter boundary.
- The isolated rational-point seed is subsumed by the E-curve theorem and belongs in historical/corroborative topology, not as a separate live premise.
- Remaining research concerns possible additional P4 components and H22, not an unclosed H31 boundary of this known component.
- Migration cohesion: **high; evidence maturity high; readiness medium-high** as a future whole-family unit. A generic triple alone would strand same-theorem descendants.

### 5.7 Split-center mixed-star H22 (component 24)

```text
generic H22 theorem
  -> D01 finite + infinity
  -> D23 finite + infinity
  => generic weighted fibre closed

special component/projective fibres [excluded and open]
```

- Root/generic core: compact theorem, primary, and distinct exact-rational no-import audit.
- H31 is a sibling on the same P4 component, not a premise for the H22 theorem merely because code imports H31 row helpers.
- The primary imports `build_model` and `project` from the component-20 candidate derivation. The independent audit reduces status risk but does not remove code-ownership risk.
- Migration cohesion: **high; evidence maturity high at the generic point; represented boundary complexity low; readiness medium** pending neutral ownership of shared implementation.

### 5.8 Consequential evidence anchors

| Family | Exact current evidence anchors |
|---|---|
| Embedded-P3 | `P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md:81-114`; `P5_H22_EMBEDDED_P3_COMPONENT_PROJECTIVE_COVERAGE_BOUNDARY.md:22-41,278-288` |
| Common-active | `P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md:3-28,294-340`; `P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md:3-45` |
| Common-center/component 23 | `P5_H22_COMMON_CENTER_KERNEL_STAR_COMPONENT_FINITE_ORDINARY_RESIDUAL_OBSTRUCTION.md:5-19,92-104`; `README.md:2717-2727` |
| Unequal-complement | `P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D01_PAIR_ORBIT_OBSTRUCTION.md:5-17`; `P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H0_NONZERO_RESIDUAL_SECOND_COFACTOR_COVER_OBSTRUCTION.md:19-30,149-155`; `P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H2_ZERO_TERMINAL_COMPLETE_OBSTRUCTION.md:5-26` |
| Unequal-endpoint | `P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_PARTIAL.md:5-16,147-162`; `P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D01_BRANCH_B_GENERIC_OBSTRUCTION.md:5-19,152-166`; `catalog/theorem-ledger.json:1549-1562` |
| Diagonal-quadric | `P5_H31_DIAGONAL_QUADRIC_ELLIPTIC_GENERIC_OBSTRUCTION.md:336-416`; `P5_H31_DIAGONAL_QUADRIC_OUTER_BOUNDARY_OBSTRUCTION.md:5-22`; `P5_COMPONENT_BOUNDARY_DIVISOR_ATLAS.md:71-75` |
| Split-center | `P5_H22_SPLIT_CENTER_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md:5-20,189-215`; `verify_p5_h22_split_center_mixed_star_component_generic_obstruction.py:14-34`; `audit_p5_h22_split_center_mixed_star_component_generic_obstruction.py:272-278` |

## 6. Same family versus same theorem

Evidence of one distributed theorem or obligation includes explicit continuation language, a parent conclusion whose final boolean/case proof consumes children, and a proved exhaustive union. The strongest inspected examples are:

- embedded-P3 H31 projective closure;
- common-active H31/H22 wall aggregates;
- component-23 generic finite H22 closure; and
- diagonal-quadric regular/projective H31 closure.

By contrast:

- H31 and H22 results on the same P4 component are ordinarily sibling obligations;
- reuse of source rows or weighted-contraction helpers establishes executable sharing, not same-theorem ownership;
- a hash can pin a failed route, refuted artifact, or corroborating calculation; and
- an open residual tree is one intended obligation without yet being one completed theorem.

## 7. Evidence and status map

Status, role, scope, and evidence must remain separate axes.

| Class | Practical meaning in the inspected surface | Examples |
|---|---|---|
| `LIVE_VERIFIED` | Exact claim proved at its stated scope; may still have unclaimed descendants. | Split-center H22 generic; embedded-P3 H31 projective closure. |
| `VERIFIED_GENERIC_WITH_BOUNDARY_DEBT` | Generic/function-field claim is closed while special or projective loci remain. | Embedded-P3 H22; split-center H22. |
| `PARTIAL` | Exact children are closed but case exhaustion, divisors, or charts remain open. It is not merely “weak computation.” | Unequal-complement D23; unequal-endpoint D23/projective forests. |
| `CANDIDATE` | Discovery or epistemic label that must be read with current prose. Candidate-named files can later be verified, refuted, or remain exploratory. | Common-active H22 generic is candidate-named but independently verified. |
| `EXPLORATORY` | Search/reconnaissance without a live theorem conclusion. | Survivor scans and old working notes. |
| `SUPERSEDED` | Retained history replaced by a later route; not proof-active. | Common-active wall partial; diagonal point seed after subsumption. |
| `SHARED_INFRASTRUCTURE` | Reusable implementation whose present filename may suggest one claim owner. | Candidate-housed `build_model`; marked-basis and row-construction hubs. |
| `FRONTIER_SYNTHESIS` | Aggregates closures and open obligations; can contain a verified reduction without closing targets. | High-coordinate partial frontier. |
| `REFUTED_ROUTE` | An argument is invalidated while its target may remain unknown or be proved later by another route. | Unequal-endpoint old Branch B; embedded-P3 overstrong H22 transport. |

A future graph should keep candidate, partial, superseded, and refuted nodes visible for lineage, but no such node should become a live proof premise merely through a hash, import, or shared directory.

## 8. Ledger semantics

### 8.1 What the fields mean in practice

The theorem ledger describes itself as `partial_curated`; boundary/divisor certificates are often summarized by atlas entries rather than listed individually. It is a useful index, not an authoritative complete dependency graph.

`dependencies`

- All 85 current entries contain the field.
- All 85 values are empty arrays.
- Empty arrays coexist with explicit logical, provenance, executable, and shared-implementation dependencies.
- Therefore the field currently has no demonstrated semantic contract beyond an unpopulated placeholder. It does not mean “no dependencies,” “complete logical dependencies,” or even “important dependencies.”

Equal-support-sixfold H22 is decisive: its ledger entry has `dependencies: []`, while theorem prose says it uses the H31 gauge and H31 frames for special slopes, explicitly calls an H31 theorem hash a dependency, and its verifier hashes P4 and H31 companions.

`assumptions_and_excluded_divisors`

- Intended as a compact scope summary.
- In practice it is coarse, templated, and sometimes stale relative to theorem prose.
- Equal-support H22 ledger prose says special slopes are excluded while the theorem closes `0`, `+/-1`, and infinity at covered parameter points.
- A common-center `r=0` divisor entry receives generic “slope r transcendental” boilerplate even though the theorem is explicitly on that divisor and instead leaves special `t` points open.

The theorem's current status/scope prose must therefore take precedence.

`status`

- Usually records intended epistemic state at ledger-entry granularity.
- It does not encode scope, evidence independence, or descendant closure.
- The unequal-endpoint Branch B entry is a high-confidence stale contradiction: `verified_generic` in the ledger versus withdrawn/identities-only in the document and both replays.

`primary_verifier` and `verifier_provenance`

- Identify a mapped evidence carrier and its broad form at the ledger entry's granularity.
- They are not logical dependencies.
- A null value does not prove that no related script exists elsewhere in a family.

`independent_audit` and `audit_provenance`

- Identify whether a distinct mapped audit exists, is known absent, or has not been mapped.
- The common `independent_modular_audit` value practically records a mapped distinct script; it is not a reliable literal method label. Split-center's audit is exact-rational, for example.
- Audit edges are evidentiary, not theorem premises. Some “independent” audits share model builders, source rows, or primary orchestration and are independent only in a narrower algorithmic stage.

### 8.2 What `dependencies` should mean before a proof DAG

The current field should not be populated mechanically from imports, hashes, or subprocess lists.

Before any machine-readable proof graph is implemented, repository policy should choose one of two explicit approaches:

1. reserve ledger `dependencies` for typed, direct, live mathematical premises and keep executable/provenance/audit relationships in separate structures; or
2. leave the curated ledger as a claim index and introduce a separate typed proof-obligation graph after its semantics are reviewed.

The second approach is presently safer because the ledger is deliberately partial and coarse-grained. In either approach, direct logical/reduction/case/specialization/boundary edges must be distinguishable from provenance, executable, shared-implementation, audit, corroboration, frontier, and historical edges.

This Stage 11 task does not choose field names, normalize entries, or repair the Branch B inconsistency.

## 9. Candidate-derived dependency contamination

The broadest instance is the component-20 candidate derivation module. Its reusable exports (`WORDS`, `permanent4`, `project`, `build_model`, and `singular_command`) have 39 direct consumers across five naming groups and four mathematical component families. Most consumers use generic weighted-contraction/model infrastructure rather than the candidate theorem conclusion.

Consequences:

- importing these utilities does not automatically downgrade a verified consumer;
- the filename and likely exploratory destination are scientifically misleading for stable shared machinery;
- candidate edits or moves have a large cross-family replay blast radius;
- audits importing the same model/row constructors provide narrower independence than no-import audits; and
- future extraction into neutral infrastructure is plausible, but must preserve exact semantics and is outside Stage 11.

A more serious family-specific example exists in component-21 descendants, where three consumers import code tied more closely to another candidate derivation. That surface deserves separate audit before any refactor.

The architectural rule is not “candidate import implies candidate theorem.” The correct question is whether the imported symbol implements neutral mathematics, encodes a candidate-specific inference, or supplies a load-bearing evidence construction shared with the audit.

## 10. Partial, frontier, and historical semantics

Across the inspected P5 surface, `PARTIAL` most often means that exact subclaims are proved but the parent case cover is incomplete. Typical causes are unresolved divisors, non-exhausted factor branches, missing projective charts, or a proof checkpoint later completed by separate files. It does not generally mean “numerical evidence only.”

A frontier artifact can combine several roles:

- state and verify a reduction;
- aggregate known local closures;
- track unresolved target families;
- pin evidence paths/hashes; and
- explicitly report that a broader consequence remains false or unresolved.

It should not be modeled as an orchestrator whose dependencies are all premises of a completed proof.

Historical, exploratory, superseded, and refuted artifacts should appear in a future graph only with non-live semantics when they are useful for lineage, failed-route protection, or corroboration. Dead hypotheses must not look proof-active. In particular, a `REFUTED` replay can be a successful audit result whose semantic content is preservation of the refutation.

## 11. Comparison with the proof-obligation architecture

The existing R/X/E/C/Z/A discharge model remains sound and useful for certificate-backed leaves:

- `R`: a proved reduction from a mathematical obligation;
- `X`: an exhaustive, deduplicated case set;
- `E`: exact instance generation;
- `C`: a sound exact checker;
- `Z`: accepted certificate/result data; and
- `A`: replayable audit/provenance.

Representative P5 surfaces include the high-coordinate reduction (`R`), exact signature/case censuses (`X`), deterministic exact construction (`E`), verifier semantics (`C`), accepted exact witnesses or pass records (`Z`), and commands/hashes/requirements (`A`). The model correctly insists that certificates do not prove global closure without the bridge and exhaustive cover.

As a whole-repository proof topology, however, R/X/E/C/Z/A is certificate-centric and under-expressive. It does not yet explicitly separate:

- logical from provenance, executable, and shared-implementation dependencies;
- generic claims from specialization and boundary descendants;
- exhaustive case unions from residual refinements;
- symmetry transfers from ordinary implications;
- primary evidence, independent audit, and corroboration;
- live partial/candidate nodes from historical, superseded, and refuted routes; or
- local conclusions from frontier consumers.

The conceptual document should therefore add graph-layer and typed-edge guidance, while retaining R/X/E/C/Z/A as a discharge pattern rather than treating it as the entire P5 proof graph. A schema should wait until ledger and evidence semantics are settled.

## 12. Boundary-family migration readiness

`BOUNDARY_FAMILY_MIGRATION_READY` is a useful review concept if it remains a gate, not a classifier score. A family is ready only when:

1. the mathematical owner and exact live claim surface are known;
2. same-theorem case unions and residual chains are identified;
3. every member's scope and epistemic role are known;
4. logical/reduction/case/specialization/boundary edges are distinguished from executable/provenance/shared/audit edges;
5. candidate, partial, refuted, superseded, and corroborating artifacts are distinguished from live premises;
6. staying frontier and cross-family consumers are known;
7. shared implementation ownership will not be hidden or stranded;
8. the proposed package preserves the actual asymmetric theorem/verifier/audit surface; and
9. no theorem meaning or status must be rewritten merely to make the move coherent.

Provisional family comparison:

| Family | Cohesion | Evidence maturity | Boundary complexity | Future migration readiness |
|---|---|---|---|---|
| Diagonal-quadric elliptic H31 | High | High for presently known component | High but closed | Medium-high as a whole-family unit |
| Embedded-P3 H31 | High | High and projectively closed | Medium-high | Medium-high; keep closure union intact |
| Split-center H22 | High | High at generic point | Low in represented tree; wider boundaries open | Medium; shared helper ownership first |
| Common-center H22 | High | High for generic fibre; mixed wider boundary | Very high | Medium-low; distributed root/children must be frozen together |
| Common-active H31/H22 | Medium-high | High on named generic/wall packages; wider H22 open | High with cross-component consumers | Low-medium; likely subfamily packages, not one flat batch |
| Unequal-complement H22 | High intended obligation | Partial | Very high | Low |
| Unequal-endpoint H22 | High intended obligation | Partial plus one metadata contradiction | Extreme | Very low |

No migration batch is proposed or frozen by this report.

## 13. Ranked architectural and evidence risks

1. **Unequal-endpoint Branch B ledger contradiction.** A current hashed document and both replays deny the generic theorem that the ledger marks verified.
2. **Semantically empty ledger dependencies.** All entries use `[]`, so downstream tools could mistake absence of data for independence.
3. **Candidate-housed shared infrastructure.** One candidate derivation has 39 direct consumers across five other areas.
4. **Overstated audit independence.** Several audits share model construction, source rows, or primary orchestration; their independence is real only at a narrower stage than filenames may suggest.
5. **Mixed hash/subprocess semantics.** Live premises, provenance, corroboration, superseded checkpoints, and refuted routes occur in the same inventories.
6. **Distributed closure hidden by stale root labels.** Component-23's old `PARTIAL` root is later closed at the generic point by descendants; file-local labels alone can understate current synthesis.
7. **Same-theorem boundary forests can be stranded.** Moving a generic triple alone would misrepresent embedded-P3, common-active wall, component-23, and diagonal H31 closures.
8. **Claim-housed shared libraries blur ownership.** High-consumer verifiers and row/model helpers create cross-package move and replay risk.
9. **Frontier aggregation can be mistaken for proof closure.** Broad dependency/hash maps coexist with explicit unresolved outputs.
10. **Historical/refuted artifacts can become accidentally proof-active.** Untyped graph ingestion would turn preservation checks into theorem premises.

## 14. Recommended next three moves

1. **Evidence/ledger semantics pass (primary).** Under owner review, define the intended contract for status, scope, assumptions, evidence mapping, and direct mathematical dependencies; then resolve known contradictions such as unequal-endpoint Branch B. This is prerequisite work for a trustworthy proof DAG.
2. **Candidate-helper architecture pass.** Audit the 39-consumer model builder and smaller candidate-specific hubs; distinguish neutral reusable mathematics from candidate inferences and document audit-independence boundaries. Do not combine this with scientific refactoring.
3. **One bounded boundary-family packaging dry run.** After the first two moves, test the readiness gate on diagonal-quadric H31 or embedded-P3 H31 as a whole-family inventory. Do not freeze or execute a batch until owner review.

Proof-DAG schema design should follow, not precede, the first move.

## 15. Delegation ledger

Three bounded read-only workers performed broad retrieval. Their conclusions were treated as evidence; the lead independently checked every consequential node used above.

| Task | Worker | Surface inspected | Important findings | Confidence | Lead spot-check | Usefulness |
|---|---|---|---|---|---|---|
| Boundary-family cartography | `boundary_cartographer` | Seven deferred nuclei; theorem prose, current README synthesis, key child evidence | Distributed component-23 closure; H31/H22 embedded divergence; diagonal full-known-component closure; unequal-endpoint status conflict | High on topology; medium-high on exhaustive membership of largest forests | Component-23 terminal theorem/README; embedded closure union; diagonal outer theorem; Branch B lineage | High |
| Executable/provenance audit | `exec_provenance_auditor` | Import AST pass, candidate imports, `expose_claim_package`, hash/subprocess aggregators, classifier hubs, frontier | 39-consumer candidate helper; intentional cross-family imports; mixed input semantics; shared audit construction | High on edges/counts; medium-high on semantic classifications | Classifier hubs; helper definitions/consumers; common-center `k=infinity`; common-active aggregate; frontier outputs | High |
| Ledger/evidence semantics | `semantics_auditor` | All 85 ledger entries; representative theorem, primary, audit, partial, candidate, frontier, historical artifacts | All dependencies empty; assumptions coarse/stale; Branch B contradiction; audit fields are evidence-carrier metadata | High on ledger-wide facts and contradiction | Branch B ledger/document/replays/hash; equal-support H22; split-center audit | High |

Delegation materially reduced primary context load. The highest-value tasks were broad, mechanically bounded surfaces: import/provenance enumeration, ledger-wide field auditing, and first-pass family-tree reconstruction. Ownership, status, policy, and final synthesis remained lead decisions.

## 16. Adversarial self-review and hard stop

The following claims were challenged before promotion:

- **Three graphs:** supported by component-23 distributed closure, common-center cross-family implementation reuse, the 39-consumer candidate helper, mixed aggregate audits, and the frontier hash map. Retained as a durable model.
- **Edge taxonomy:** only distinctions witnessed in multiple artifacts were retained. Names remain provisional for future schema work.
- **Migration readiness:** tested against seven families; it separates compact generic packages, closed whole-family forests, and partial boundary trees without declaring a batch.
- **Ledger dependencies:** the conclusion is ledger-wide (85/85 empty), not an inference from one specimen.
- **Partial/candidate ownership:** current theorem and replay prose, not filenames, control the classifications.
- **Inferred mathematical ownership:** import-only and hash-only edges were not promoted to logical dependencies.

This report intentionally stops before:

- moving boundary files;
- freezing a Stage 12 batch;
- implementing a proof DAG;
- editing ledger semantics or status;
- extracting shared helpers;
- repairing candidate mathematics;
- creating audits; or
- beginning new proof work.

Owner review of this topology is required before any such action.
