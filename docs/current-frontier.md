# Current frontier of the Krenn–Gu conjecture programme

## Status, scope, and authority

The global Krenn–Gu conjecture is **UNRESOLVED**. No complete
characteristic-zero proof and no exact counterexample to the original global
statement is known in this repository.

This is the canonical maintained research map. Its initial consolidation was
reconstructed through PR #82 at merged commit
`367eef49e5917a0f71594dce4c18a608850cdd6a`; subsequent owning advances are
incorporated here as committed. Owning theorem documents are authoritative for
proofs, assumptions, and evidence. This page records how those claims fit
together; it does not replace them or strengthen their scope.
The [theorem ledger](../catalog/theorem-ledger.json) is a partial claim/evidence
index, not the proof graph, and its empty `dependencies` arrays mean “not
recorded.”

Except where an owner says otherwise, the live symbolic trunk below is over
`C` or characteristic zero. Generic/function-field theorems do not include
excluded divisors, projective boundaries, or arbitrary points without a proved
specialization argument.

For even `n >= 6` and `d >= 3`, the conjecture asks whether block matrices
`W_ij in C^(d x d)` can satisfy

```text
T_W(a_1,...,a_n)
  = sum_(perfect matchings M) product_({i,j} in M) W_ij[a_i,a_j]
  = sum_(c=0)^(d-1) product_v 1_(a_v=c).
```

The programme concentrates on the ternary restriction. Every local P5, P6,
or P7 result remains only a local proof leaf until a theorem extracts and
glues that leaf from every hypothetical global witness.

## Live proof topology

Arrows are typed. A `boundary` arrow names a surviving obligation; it is not a
proof of the target. A `specialization` arrow applies only under the owner's
hypotheses.

```mermaid
flowchart TD
  G0["Hypothetical complex witness<br/>global conjecture UNRESOLVED"]

  S1["Balanced complete-deck sensor<br/>PROVED reduction"]
  S2["Full-sensor rational lift and Wick gate<br/>OPEN"]
  S3["All balanced partitions rank-drop<br/>OPEN on witness locus"]

  M1["Maximum torus-root split<br/>PROVED reduction"]
  M2["r >= 2 fixed-surplus layer<br/>PROVED reduction"]
  PR["Weighted permanent restriction family<br/>OPEN at arbitrary order"]
  O1["Fixed-layer truncation and nonobservability<br/>PROVED boundary"]
  O2["Two-open detector and q=0 star gauge<br/>PROVED boundary"]
  O2P["Projective single-open consecutive lift<br/>PROVED conditional reduction"]
  O2M["Minimum q=0, r=3 row replacement<br/>TWO-OPEN DETECTED conditionally"]
  O2T["q=0, r=4 locally transverse cell<br/>AT LEAST ONE DETECTOR conditionally"]
  O2F["Complete aligned q=0, r=4 cell<br/>AT LEAST ONE DETECTOR conditionally"]
  O2V["q=0, r=5 good-companion activity stratum<br/>AT LEAST ONE DETECTOR conditionally"]
  O2A["q=0, r=5 all-companion root-transverse stratum<br/>AT LEAST ONE DETECTOR conditionally"]
  O2C["Complete locally transverse q=0, r=5 cell<br/>AT LEAST ONE DETECTOR conditionally"]
  O3["q=0 r=5 local-dependence boundary; q=0 r>=6;<br/>q>=1 or unfactorized detector OPEN"]

  U1["r = 1 complete matrix units<br/>PROVED normal form"]
  U2["At-most-four-port response<br/>k = 1, 2, 3 remain OPEN"]
  U3["Globally rigid colour system<br/>CONDITIONAL"]
  U4["Three-block primitive and dual bridges<br/>PROVED"]
  U5["Primitive-alone closure<br/>REFUTED ROUTE"]
  U6["Cross parity, bridges, rigid-head Wick<br/>PROVED reduction"]
  U7["Word-shore Tutte or global rematching<br/>OPEN"]
  U8["Proper flag propagation<br/>OPEN"]
  D1["Deeper blocker branch<br/>OPEN"]

  A1["Simultaneous balanced all-bridge<br/>CONDITIONAL branch"]
  A2["Degree <= 4 excluded;<br/>degree >= 5 OPEN"]

  P5["Local P5 component programme<br/>PARTIAL / boundary-limited"]
  P7["Committed local P7 incidence<br/>criterion proved, outcome OPEN"]
  GL["Universal extraction, synchronization,<br/>and local-to-global gluing OPEN"]
  C2["Automatic characteristic-two lift<br/>REFUTED as a general route"]

  G0 -->|universal reduction| S1
  S1 -->|boundary| S2
  S1 -->|boundary| S3

  G0 -->|universal reduction| M1
  M1 -->|case r >= 2| M2
  M1 -->|case r = 1| U1
  S1 -->|premise| O1
  M2 -->|premise| O1
  O1 -->|residual refinement| O2
  O2 -->|aligned projective branch| O2P
  O2P -->|permanent reduction| PR
  O2P -->|minimum Hall cell| O2M
  O2P -->|transverse next cell| O2T
  O2P -->|complete four-cell closure| O2F
  O2P -->|five-cell collective transport| O2V
  O2P -->|five-cell pair collision| O2A
  O2P -->|complete transverse five-cell| O2C
  O2T -. strict special case .-> O2F
  O2V -. strict overlapping stratum .-> O2C
  O2A -. strict overlapping stratum .-> O2C
  O2F -->|larger-cell boundary| O3
  O2C -->|local-dependence boundary| O3
  O2 -->|boundary| O3
  M2 -->|zero-surplus specialization| PR

  U1 -->|reduction| U2
  U2 -->|specialization| U3
  U3 -->|premise| U4
  U4 -. primitive alone insufficient .-> U5
  U1 -->|premise| U6
  U2 -->|premise| U6
  U6 -->|exact erasure| M2
  U6 -->|boundary| U7
  U2 -->|boundary| U8
  U2 -->|boundary| D1
  U6 -->|boundary| D1
  U2 -->|simultaneous full flags| A1
  A1 -->|residual refinement| A2

  PR -->|local specialization only| P5
  PR -->|local specialization only| P7
  P5 -->|open gluing obligation| GL
  P7 -->|open gluing obligation| GL
  S2 -->|global section obligation| GL
  G0 -. route boundary .-> C2
```

## Node key

| ID | Live node and exact status | Owning theorem or programme document |
|---|---|---|
| `G0` | Original global conjecture: **UNRESOLVED** | [Problem statement](../README.md#the-conjecture) |
| `S1` | Balanced complete even deck and full-sensor/rank-drop dichotomy: **proved reduction** | [Balanced half-sensor theorem](../claims/arbitrary-order/BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md) |
| `S2` | Pole-free normalized projective lift satisfying all Wick equations: **open** | [Balanced half-sensor theorem, exact frontier](../claims/arbitrary-order/BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md#6-exact-frontier) |
| `S3` | Exclusion of all-balanced rank drop inside the hypothetical-witness locus: **open**; properness is proved only in ambient block-graph space | [Balanced half-sensor theorem](../claims/arbitrary-order/BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md#3-the-proper-closed-all-balanced-boundary) |
| `M1` | Maximum torus-root saturation and `r=1` / `r>=2` split: **proved universal reduction** | [Maximal torus-root theorem](../claims/arbitrary-order/MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md) |
| `M2` | One complete fixed-surplus physical hafnian layer; coordinate two-residual absorption: **proved reduction, not exclusion** | [Maximal torus-root theorem](../claims/arbitrary-order/MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md#2-the-saturated-principal-hafnian-layer) |
| `PR` | Weighted `P_t -> Delta_3` restriction family: **extracted at zero surplus and on the conditional consecutive-lift branch; arbitrary-order exclusion open**. The live `t=6` / P6 restriction remains inside this node; the three-excess notes address only the first strict-support layer, not arbitrary support. | [Maximal-root extraction](../claims/arbitrary-order/MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md#2-the-saturated-principal-hafnian-layer), [consecutive single-open lift](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_SINGLE_OPEN_CONSECUTIVE_PERMANENT_LIFT_AND_COMPANION_FRAME_THEOREM.md), [P6 package index](../claims/p6/README.md), [three-excess port boundary](../claims/arbitrary-order/ARBITRARY_PERMANENT_THREE_EXCESS_PORT_PERMUTATION_THEOREM.md), and [conformal Birkhoff boundary](../claims/arbitrary-order/ARBITRARY_PERMANENT_THREE_EXCESS_CONFORMAL_BIRKHOFF_REDUCTION.md) |
| `O1` | Contracted truncation, same-fibre rank nonobservability, and single-open absorption: **proved structural boundary** | [Balanced fixed-surplus theorem](../claims/arbitrary-order/BALANCED_FIXED_SURPLUS_TRUNCATION_FIBRE_NONOBSERVABILITY_AND_TRANSVERSE_ABSORPTION_THEOREM.md) |
| `O2` | Complete two-open equation and conditional `q=0` tensor-preserving star gauge: **proved boundary** | [Two-open gauge theorem](../claims/arbitrary-order/BALANCED_TWO_OPEN_ROOT_GAUGE_DETECTOR_AND_STAR_INVISIBILITY_BOUNDARY.md) |
| `O2P` | On the aligned common-two-row, projectively constant branch, the complete single-open identity is a consecutive `P_(m+1)` restriction and its old-root companions form an exact rank-two diagonal quotient frame: **proved conditional reduction** | [Consecutive single-open lift](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_SINGLE_OPEN_CONSECUTIVE_PERMANENT_LIFT_AND_COMPANION_FRAME_THEOREM.md) |
| `O2M` | In the minimum aligned projective cell `q=0,r=3`, the lifted row quotas force `P_3(a,a,b)!=0`, so every nonzero absorption direction at either non-aligned root is **detected by the complete two-open tensor**; this is not a witness exclusion | [Lifted minimum-cell detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_ROW_QUOTAS_AND_MINIMAL_CELL_TWO_OPEN_DETECTOR_THEOREM.md) |
| `O2T` | In the aligned projective `q=0,r=4` cell, local independence of `a_u,b_u` at all four outside modes makes `h -> P_4(h,a,a,b)` injective; a companion-basis deletion then gives **at least one nonzero two-open detector**. This remains a verified strict special case of `O2F`. | [Transverse four-cell detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_TRANSVERSE_FOUR_CELL_TWO_OPEN_DETECTOR_THEOREM.md) |
| `O2F` | In the full aligned projective `q=0,r=4` cell, collision quotients plus Hall incidence reduce invisibility to a common outside `a/b` zero; recolouring and local concision exclude it. Hence **at least one nonzero two-open detector** always exists, and all three do when the companions are pairwise independent. This is not a witness exclusion. | [Complete four-cell detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_FOUR_CELL_TWO_OPEN_DETECTOR_THEOREM.md) |
| `O2V` | In aligned projective `q=0,r=5`, the four companion equations form an exact symmetric `XL=0` system. Away from a zero companion or balanced `2+2` projective split, modewise three-activity forces **at least one nonzero two-open detector**. Local `a/b` transversality implies activity. This is conditional detection, not full-cell closure or witness exclusion. | [Five-cell collective detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_COLLECTIVE_COMPANION_AND_ACTIVITY_DETECTOR_THEOREM.md) |
| `O2A` | In locally transverse aligned projective `q=0,r=5`, common-kernel contraction makes a doubly transverse root's five-mode pair-collision map injective. If at most one root is not doubly transverse, all six pair tensors are nonzero, and the rank-two companion zero-edge lemma gives **at least one detector for every companion frame**. This is not witness exclusion. | [Five-cell all-companion pair detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_FIVE_CELL_PAIR_COLLISION_AND_ALL_COMPANION_DETECTOR_THEOREM.md) |
| `O2C` | In every locally transverse aligned projective `q=0,r=5` cell, weak-root common-kernel trapping plus the exhaustive good/zero/balanced companion split forces a local-concision contradiction if all four collective tensors vanish. Hence **at least one nonzero two-open detector** exists for every companion frame and every root quotient-support pattern. This is not full-cell closure or witness exclusion. | [Complete transverse five-cell detector](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_TRANSVERSE_FIVE_CELL_TWO_OPEN_DETECTOR_THEOREM.md) |
| `O3` | In aligned projective `q=0,r=5`, the remaining detector boundary is local dependence of some outside `a_u,b_u` pair. Every `q=0,r>=6` cell, every `q>=1` cell, and every unfactorized outside graph is also **open**. | [Complete transverse five-cell boundary](../claims/arbitrary-order/PROJECTIVELY_CONSTANT_LIFT_COMPLETE_TRANSVERSE_FIVE_CELL_TWO_OPEN_DETECTOR_THEOREM.md#5-exact-residual-boundary) and [two-open exact boundary](../claims/arbitrary-order/BALANCED_TWO_OPEN_ROOT_GAUGE_DETECTOR_AND_STAR_INVISIBILITY_BOUNDARY.md#6-exact-boundary) |
| `U1` | Complete nonzero one-matrix-unit blocks and forbidden-word cancellation: **proved normal form; exclusion open** | [Maximal-root one branch](../claims/arbitrary-order/MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md#3-the-maximum-one-monomial-branch) |
| `U2` | Globally minimum forbidden word has at most four deviations; exact finite-port response and partial bridges: **proved reduction**. The `k=1`, `k=2`, and `k=3` cells all remain unexcluded; only `k=4` forces rigidity in the base colour. | [Four-switch theorem](../claims/arbitrary-order/MATRIX_UNIT_FOUR_SWITCH_MINIMAL_PORT_AND_PARTIAL_BRIDGE_REDUCTION_THEOREM.md) |
| `U3` | Globally rigid colour factors into a pure hafnian and binary tensor: **proved conditionally; rigidity not forced** | [Rigid-colour boundary](../claims/arbitrary-order/RIGID_COLOUR_COFACTOR_ANNIHILATION_AND_BACKBONE_CANCELLATION_BOUNDARY.md) |
| `U4` | Bi-null cuts, three-block primitive, and dual quadratic bridges: **proved; arbitrary-order exclusion open** | [Rigid primitive theorem](../claims/arbitrary-order/RIGID_COLOUR_THREE_BLOCK_BINARY_PRIMITIVE_AND_QUADRATIC_BRIDGE_THEOREM.md) |
| `U5` | “The primitive alone contradicts the tensor”: **refuted route** for every even order at least eight | [Primitive sharpness theorem](../claims/arbitrary-order/RIGID_COLOUR_THREE_BLOCK_PRIMITIVE_SHARPNESS_AND_DUAL_BRIDGE_COMPLETION_OBSTRUCTION.md) |
| `U6` | Cross-parity erasure, bridge/deeper entry, rigid-head Wick tower, and pseudoforest normal form: **proved reduction** | [Cross-parity theorem](../claims/arbitrary-order/MATRIX_UNIT_CROSS_PARITY_ERASURE_RIGID_HEAD_WICK_AND_BRIDGE_CORE_REDUCTION_THEOREM.md) |
| `U7` | Higher mixed identities force word-shore perfect matchings/Tutte inequalities, or another word-preserving rematching: **open** | [Word-synchronization boundary](../claims/arbitrary-order/MATRIX_UNIT_BRIDGE_WORD_SYNCHRONIZATION_AND_WICK_SHARPNESS_BOUNDARY.md#4-fully-active-pure-cofactors-still-do-not-synchronize-the-word) |
| `U8` | Proper nonempty colour-nonrigidity sets propagate to all vertices: **open** | [Four-switch partial-bridge theorem](../claims/arbitrary-order/MATRIX_UNIT_FOUR_SWITCH_MINIMAL_PORT_AND_PARTIAL_BRIDGE_REDUCTION_THEOREM.md#5-partial-bridge-systems) |
| `D1` | Deeper double-star/multi-star blocker branch: **open**. Its blocker alternatives are pointwise after shrinking to a dense constructible stratum; no uniform blocker pair is proved on the whole component. | [Double-star lemma](../claims/arbitrary-order/DOUBLE_STAR_ANNIHILATION_LEMMA.md) and [multi-star factorization](../claims/arbitrary-order/MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md) |
| `A1` | Simultaneous balanced all-bridge system: **proved conditional branch**, not universal extraction | [Three-colour balanced bridge intersection](../claims/arbitrary-order/THREE_COLOUR_BALANCED_BRIDGE_INTERSECTION_THEOREM.md) |
| `A2` | Saturated-diagonal maximum degree at most four: **excluded**; `Delta(D)>=5` remains **open** | [Cubic exclusion](../claims/arbitrary-order/ALL_BRIDGE_ACTIVE_DECK_EXCLUSIVITY_AND_CUBIC_DIAGONAL_EXCLUSION.md) and [degree-four exclusion](../claims/arbitrary-order/ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FOUR_EXCLUSION.md) |
| `P5` | Local `P5 -> Delta_3` component programme: **partial, generic and boundary-limited** | [P5 package index](../claims/p5/README.md) and [obligation ledger](../claims/p5/frontier/P5_DELTA3_OBLIGATION_LEDGER.md) |
| `P7` | One committed legal sensor/incidence pullback: criterion **proved**, algebra outcome **open** | [Committed P7 criterion](../claims/p7/COMMITTED_LEGAL_SENSOR_ORDERED_SECANT_FACTOR_CHOW_NORM_AND_BOUNDARY_TRAP_CRITERION.md) |
| `GL` | Universal extraction, cross-chart/depth synchronization, and local-to-global gluing: **open** | [Top two-port observability boundary](../claims/arbitrary-order/GRAPH_EXTRACTION_TOP_TWO_PORT_SYNCHRONIZATION_OBSERVABILITY_BOUNDARY.md) |
| `C2` | Automatic reduction of arbitrary characteristic-zero solutions to the pinned `F_2` argument: **refuted as a general lemma** | [Characteristic-two route boundary](../claims/arbitrary-order/CHARACTERISTIC_TWO_CONTRACTION_LIFT_OBSTRUCTION.md) |

## Typed-edge table

| Source | Relationship | Target | Exact meaning |
|---|---|---|---|
| `G0` | reduction | `S1` | Every hypothetical ternary witness has a balanced-sensor dichotomy. |
| `S1` | boundary obligation | `S2`, `S3` | Neither full-sensor globalization nor witness-locus rank-drop is excluded. |
| `G0` | reduction | `M1` | Maximum-cardinality torus roots give a pointwise exhaustive split. |
| `M1` | case coverage | `M2`, `U1` | The two cases are `r>=2` and `r=1`; neither is excluded by the split. |
| `S1` + `M2` | mathematical premises | `O1` | Rebalancing the fixed layer exposes a truncated contracted sensor. |
| `O1` | residual refinement | `O2` | A second open root gives the exact next detector equation. |
| `O2` | specialization | `O2P` | If the outside two-row factorization is aligned with root `j` and its open shore is projectively constant, the whole single-open equation lifts the fixed `P_m` layer to `P_(m+1)`. |
| `O2P` | reduction | `PR` | The synchronized projective branch is reduced to the same arbitrary weighted-permanent restriction family; no permanent nonrestriction theorem is inferred. |
| `O2P` | conditional cell closure | `O2M` | The repeated-row Hall quotas and adjacent pure/mixed equations close row-replacement vanishing only in the minimum `q=0,r=3` cell; they do not exclude a witness there. |
| `O2P` | conditional cell closure | `O2T` | In `q=0,r=4`, local `a/b` transversality plus a surviving companion basis forces at least one nonzero row-replacement detector; transversality is not derived and no witness is excluded. |
| `O2P` | conditional cell closure | `O2F` | Collision quotients, Hall incidence, recolouring, and local concision close every local-dependence boundary in aligned projective `q=0,r=4`; no witness is excluded. |
| `O2P` | conditional stratum detector | `O2V` | In `q=0,r=5`, the collective companion matrix and deletion activity force at least one nonzero detector away from the two classified companion exceptions; neither activity nor good companions is universal. |
| `O2P` | conditional stratum detector | `O2A` | In locally transverse `q=0,r=5`, pair-collision injectivity and the companion zero-edge lemma cover every companion frame when at most one root has quotient support at most one. |
| `O2P` | conditional cell closure | `O2C` | In locally transverse `q=0,r=5`, weak-root trapping and the exhaustive companion split close every root quotient-support pattern; no witness is excluded. |
| `O2T` | strict special case | `O2F` | The earlier local-transversality proof remains valid but its extra hypothesis is no longer needed for four-cell detection. |
| `O2V` | strict overlapping stratum | `O2C` | Good companion frames with deletion activity are a strict subcase of the complete locally transverse five-cell detector. |
| `O2A` | strict overlapping stratum | `O2C` | Frames with at most one quotient-sparse root are a strict subcase of the complete locally transverse five-cell detector. |
| `O2F` | boundary obligation | `O3` | Four-cell closure does not automatically transport to larger aligned cells, positive surplus, or the unfactorized branch. |
| `O2C` | boundary obligation | `O3` | The complete transverse result does not derive local `a/b` independence and does not transport automatically to larger aligned cells, positive surplus, or the unfactorized branch. |
| `O2` | boundary obligation | `O3` | The tight star refutes an automatic detector; higher/unfactorized data are needed. |
| `M2` | specialization | `PR` | Zero surplus yields a tight weighted permanent restriction at arbitrary `r>=5`; it is not reduced to P7. |
| `U1` | reduction | `U2` | Matrix-unit cancellation reduces to an at-most-four-port response. |
| `U2` | specialization | `U3` | Only the globally rigid-colour cell enters the deletion-deck factorization. |
| `U3` | mathematical premise | `U4` | Rigid factorization yields the primitive and dual bridges. |
| `U4` | refutation of argument | `U5` | The primitive alone cannot close arbitrary order. |
| `U1` + `U2` | mathematical premises | `U6` | Parity and bridge structure refine the one-root branch. |
| `U6` | reduction | `M2` | Exact erasure may produce a different realization with at least two roots. |
| `U6` | boundary obligation | `U7` | Bridge normalization changes the exact word; synchronization remains missing. |
| `U2` | boundary obligation | `U8` | Full flags have consequences, but proper nonempty flag sets remain. |
| `U2`, `U6` | boundary obligation | `D1` | Both reductions retain the deeper-blocker alternative. |
| `U2` | specialization | `A1` | Simultaneous full flags for all colours enter all-bridge, absent deeper blockers. |
| `A1` | residual refinement | `A2` | PRs #72–#73 close degree at most four only. |
| `PR` | specialization | `P5`, `P7` | These are two separately developed local lanes. The still-open `r=6` / P6 restriction remains in `PR`, and arbitrary `r>=8` is not reduced to any of these ranks. |
| `P5`, `P7` | open gluing obligation | `GL` | Even complete local exclusions require a theorem connecting every global witness to them. |
| `S2` | open gluing obligation | `GL` | A rational pointwise lift must extend to one physical block graph and satisfy all Wick relations. |
| `G0` | refutation of argument | `C2` | Good reduction to the prime field is not automatic, and the source theorem's local correspondence remains pending. |

## Smallest positive next obligations

These are positive theorems or exact decisions that would advance a surviving
branch. They are not an instruction to begin all of them at once.

1. **Zero-surplus permanent restrictions.** Decide the live `P_6 -> Delta_3`
   restriction, and exclude `P_r -> Delta_3` for every `r>=8` at every legal
   support size, or prove an exact reduction to ranks that are already closed.
   The committed P7 sensor and the exactly-three-excess support normal forms
   are not exhaustive arbitrary-r theorems.

2. **Word-shore forcing.** Prove from higher mixed coefficients that each pure
   support graph induced on the actual word shore satisfies Tutte's condition,
   or construct another exact word-preserving global rematching. Global pure
   matchings and fully active pure cofactors are insufficient.

3. **Remaining larger/unfactorized detector.** On the aligned projectively
   constant branch, close the local-`a/b`-dependence boundary in `q=0,r=5`;
   the entire locally transverse cell is now detected.  Then treat
   `q=0,r>=6` or `q>=1`, or prove a legal selector separating the replacement
   tensors. Outside that branch, produce an exact nonzero selector or
   otherwise exclude the unfactorized high-surplus cell.  The existing cell
   detectors do not exclude a witness.

4. **First remaining all-bridge degree.** Exclude or structurally reduce
   `Delta(D)=5`. This does not address the separate deeper-blocker branch.

5. **Component 22 isolated complement.** Close the finite-`D23` cell
   `H=f2=f8=0`, `rho(rho+1)!=0`, `2h3+s!=0`, and keep it distinct from the
   remaining `f2=0` residual. See the [slope-intersection owner](../claims/p5/h22/unequal-complement-common-kernel-component-d23-f2-f8-h3-slope-intersection/P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_F2_F8_H3_SLOPE_INTERSECTION_OBSTRUCTION.md)
   and [two-minor partial owner](../claims/p5/h22/unequal-complement-common-kernel-component-d23-h1-nonzero-two-minor-factor-cover-partial/P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_D23_H1_NONZERO_TWO_MINOR_FACTOR_COVER_PARTIAL_OBSTRUCTION.md).

6. **P4-B3 semantic/composition audit.** Audit the nonzero-pure-factor, symmetry,
   inclusion, and lower-pair quantifiers in the
   [P4 all-pair-rank reduction](../claims/p4/classifications/P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md).
   The owner asserts a 25-component exhaustiveness theorem; the independent
   acceptance of those load-bearing quantifiers remains open. Script replay is
   not a substitute for that review.

7. **Committed P7 calculation.** Materialize the residual equations, pull back
   the factor equations, justify properness/finiteness where used, and decide
   `A_good`; proceed to `A_gen^star` only if the criterion requires it. A result
   on this fixed sensor would still need `GL`.

Component 25 is not a closed shortcut: its finite-`D23` three-branch cover is
not an exclusion, and finite-`D01`, special fibres, and projective boundaries
remain open.

Within the `r=1` route, the minimum-word cells `k=1`, `k=2`, and `k=3`
remain distinct positive obligations. The port theorem packages their exact
responses; it does not collapse them into the globally rigid `k=4` cell.

## Refuted or insufficient proof routes

| Route | Exact finding | Owner |
|---|---|---|
| Automatic characteristic-zero to `F_2` reduction | Refuted as a general lemma; good reduction and prime-field residue are not forced | [Characteristic-two boundary](../claims/arbitrary-order/CHARACTERISTIC_TWO_CONTRACTION_LIFT_OBSTRUCTION.md) |
| Fixed surplus determines balanced-sensor rank | False: one fixed-layer fibre can contain deficient and full uncontracted shores | [Fixed-surplus nonobservability](../claims/arbitrary-order/BALANCED_FIXED_SURPLUS_TRUNCATION_FIBRE_NONOBSERVABILITY_AND_TRANSVERSE_ABSORPTION_THEOREM.md) |
| The first two-open equation always detects the affine gauge | False on a conditional tight `q=0` outside-star cell | [Two-open star invisibility](../claims/arbitrary-order/BALANCED_TWO_OPEN_ROOT_GAUGE_DETECTOR_AND_STAR_INVISIBILITY_BOUNDARY.md) |
| Primitive or pure scalar hafnian pencils close the rigid branch | False at arbitrary order; mixed deletion and completion coupling remain essential | [Primitive sharpness](../claims/arbitrary-order/RIGID_COLOUR_THREE_BLOCK_PRIMITIVE_SHARPNESS_AND_DUAL_BRIDGE_COMPLETION_OBSTRUCTION.md) |
| Bogdanov-backbone cancellation alone contradicts equality | False: all selected backbone mixed words can cancel while other words fail | [Rigid-colour cancellation boundary](../claims/arbitrary-order/RIGID_COLOUR_COFACTOR_ANNIHILATION_AND_BACKBONE_CANCELLATION_BOUNDARY.md) |
| Bridge normalization, parity/Wick, or fully active pure cofactors synchronize the exact word | False; exact six-vertex countermechanisms isolate the word-shore condition | [Word-synchronization boundary](../claims/arbitrary-order/MATRIX_UNIT_BRIDGE_WORD_SYNCHRONIZATION_AND_WICK_SHARPNESS_BOUNDARY.md) |
| One fixed P7 survivor or incidence result globalizes automatically | False as an inference: one still needs physical edge descent, all Wick equations, and universal extraction | [Balanced sensor Wick gate](../claims/arbitrary-order/BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md) |

These are refutations of arguments, not counterexamples to the Krenn–Gu
conjecture.

## Evidence, disagreements, and maintenance

- The P4 owner asserts a 25-component exhaustiveness theorem. The programme
  retains P4-B3 as a human semantic/composition audit of its load-bearing
  quantifiers. This is an audit-acceptance gap, not an automatic mathematical
  contradiction and not permission to call the cover either unproved or fully
  audited without qualification.
- Several P5 results are generic/function-field or divisor-specific. Package
  colocation, a component count, or a finite certificate does not close their
  special and projective boundaries.
- The external characteristic-two Lean project is source-inspected candidate
  evidence here; local build replay and statement correspondence remain
  pending. The local algebraic route obstruction is independent of accepting
  that external formalization.
- `primary_verifier` and `independent_audit` are evidence roles, not
  mathematical premises. Bounded checks do not prove arbitrary-order prose.
- Any PR that changes a node, edge, open leaf, route refutation, or local/global
  scope on this page must update it. A PR that changes mathematical claims but
  leaves this live frontier unchanged must explicitly state why no frontier
  update is needed. The owning claim document must change when the theorem
  itself changes.

The detailed reconstruction, reviewer disagreements, relocation inventory,
and PR #72–#82 evidence are in the
[programme proof-topology audit](audits/PROGRAMME_PROOF_TOPOLOGY_AUDIT_2026-08-10.md).
The superseded chronology remains available in the
[2026-08-05 frontier snapshot](history/current-frontier-stabilization-snapshot-2026-08-05.md)
and [2026-08-10 handoff](history/handoffs/SYMBOLIC_PROGRAM_HANDOFF_2026-08-10.md).
