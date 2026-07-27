# Krenn-Gu prize conjecture research

## Status

**UNRESOLVED globally.**  This repository does not yet contain a proof or
counterexample for all even `n >= 6` and `d >= 3`.

Separately, the repository now contains an exact rational positive
Question-2 witness for [`n=6, k=4, d=4`](Q2_N6_K4_D4_CONSTRUCTION.md).
It has two red heralds and therefore is not a Question-1 counterexample.
PyTheus already established existence at these parameters; the
Twitter/X-thread witness recorded here has different support and much
simpler rational weights.  It was posted by
[`@speaktoevil`](https://x.com/speaktoevil/status/2080655946825818276);
this repository makes no priority claim.

It does contain independently replayed computer-assisted theorems that
strictly advance the finite frontier:

- no six-vertex complex witness for `d >= 3`;
- no eight-vertex, three-colour witness with a 4-regular skeleton;
- no eight-vertex, three-colour witness whose essential skeleton has a
  degree-four vertex and at most 17 edges;
- no eight-vertex, three-colour, exact-18- or exact-19-edge witness with a
  degree-three vertex;
- no 84-entry witness on a 5-regular, exact-20-edge eight-vertex skeleton;
- no member of the 7,938-labelled-support full-2-factor/singleton
  macro-family on any 5-regular eight-vertex skeleton;
- no 105-entry witness on a 5-regular, exact-25-edge ten-vertex skeleton.
- at every even order, no 4-regular witness in the simultaneous
  three-colour balanced all-bridge boundary.
- at every even order, no witness of maximum support degree at most five
  in the simultaneous three-colour balanced all-bridge boundary.
- at every even order, no witness in the pairwise-disjoint
  exact-degree-six Kotzig/reciprocal-port boundary.
- throughout the simultaneous balanced all-bridge branch, every remaining
  witness is forced onto a saturated monochromatic-diagonal zero layer
  with a genuine alternating-cycle cancellation.
- at every even order, any zero-coupled set of `r >= 2` root vectors
  requires at least `r` outside blockers; equality forces a nonzero
  root--blocker permanent, a pure residual matching tensor, and no
  mixed-colour coefficient in the full root--blocker tensor.
- for three fully supported zero-coupled roots with exactly three
  blockers, the residual kernel restriction loses at least one of the
  other two coordinate products.
- the order-four permanent tensor has exact subrank two over `C`; in
  particular, four fully supported zero-coupled roots require at least
  five blocker vertices in total.
- every contraction of the order-five permanent tensor by a vector of
  coordinate support at most three has subrank at most two over `C`;
  the support-three case has exact subrank two.
- in sharp contrast, every support-four contraction of the order-five
  permanent tensor has subrank at least three; an explicit integer
  restriction produces `12 Delta_3`.
- the full local-restriction image of the order-five permanent tensor
  has no nonzero defining equations of degree at most five; its
  degree-six `SL(3)^5` scalar-invariant pullback is also injective.
- every local map in a hypothetical restriction `P_5 -> Delta_3` must
  contain a nonzero source-coordinate row supported on a single target
  colour.
- the five rows of each such local map fall into three exact projective
  strata: at least two coordinate rows, a one-coordinate line type, or
  a one-coordinate rigid complete-quadrangle type.
- those five local maps cannot all have the rigid complete-quadrangle
  type; at least one must be line-type or have two coordinate rows.
- every source-row pair spans a target coordinate plane in at least one
  mode; consequently some local map has two coordinate rows or has the
  axial `4+1` support form `four two-colour rows + one third-colour row`.
- more generally, for every source subset of size `s=2,3,4` and every
  target colour, its row span contains that coordinate covector in at
  least `s` of the five modes.
- for every individual source row and every target colour, one of the
  five local maps has that row proportional to the corresponding
  coordinate covector; hence at least 15 of the 25 local rows are
  coordinate, and some local map has at least three coordinate rows.
- every complex five-row support/pair-incidence signature satisfying the
  local coordinate-pair condition belongs to an explicit
  6,495-pattern catalogue; the 303 apparent patterns outside it all
  force local rank at most two.
- if every local map has at most three coordinate rows, then every map
  has exactly three and the ten non-coordinate cells form either one
  `C10` or a disjoint `C4+C6` in the mode--source bipartite graph.
- the entire all-full part of that exact-three-coordinate boundary is
  impossible over `C`: an exhaustive `6^5`-per-shape orbit census gives
  226 support orbits, complex-valid pair quotas exclude 213, a prior
  theorem excludes three, and exact unit-ideal calculations exclude all
  198 viable signature tuples on the remaining ten.
- the entire exact-one-partial part of that boundary is also impossible
  over `C`: 466,560 labelled supports give 5,676 symmetry orbits; local
  validity and pair quotas reduce these to 319, and exact support-only
  unit-ideal calculations exclude every survivor.
- the entire exact-two-partial part is impossible over `C` as well:
  6,298,560 labelled supports give 76,098 symmetry orbits; local
  validity, pair quotas, and direct support semantics reduce these to
  3,308, and exact support-only unit-ideal calculations exclude every
  survivor.  Hence any remaining exact-three-coordinate model has at
  least three partial non-coordinate rows.
- in the `C4+C6` half of the exact-three-partial layer, all 5,993
  support-semantic survivor orbits have exact support-only coefficient
  ideals equal to the unit ideal.  Thus any remaining `C4+C6`
  exact-three-coordinate model has at least four partial cells.
- in the `C10` half of the same layer, an independent regeneration of
  all 25,194,240 labelled supports agrees exactly with the
  symmetry-broken SAT catalogue on 11,751 support-semantic survivor
  orbits.  Their algebraic exclusion is still in progress.
- every fully supported zero-coupled root pair requires at least five
  distinct outside blockers across the three colours.
- for every rank-at-least-two root edge, five fixed outside
  vertex--colour pairs have blocker determinants that are scalar
  multiples of the root-edge equation; a rank-three root edge therefore
  forces five one-sided complementary-colour compressions, at least
  three at the same endpoint.
- on eight or ten vertices, no witness exists anywhere in the
  simultaneous balanced all-bridge branch, without a support-degree
  bound.
- on twelve vertices, no simultaneous balanced all-bridge witness has
  the complementary normal-type profile `6 x 000 + 6 x 111`.
- for every even `n >= 8`, no equality-architecture witness whose full
  2-factor consists entirely of odd cycles.
- for every `n = 4k+2`, no equality-architecture witness whose full
  factor is a single spanning cycle `C_n`;
- no order-14 equality-architecture witness whose full factor is
  `C3+C3+C4+C4`, `C3+C3+C8`, `C3+C4+C7`, `C3+C5+C6`,
  `C4+C5+C5`, or `C14`.
- within the remaining order-14 `C4+C10` equality family, 365 of 425
  pinned first-factor orbits are excluded.  The 60 not excluded by the
  current certificates are `3--28`, `58--63`, `70--75`, `102--105`,
  `112--113`, `121`, `124`, `153`, `156`, `164`, `170--174`,
  `176--177`, `248`, `251--252`, and `255`.
- within the remaining order-14 `C6+C8` equality family, 292 of 328
  pinned first-factor orbits are excluded under the explicit hypothesis
  that the support skeleton has vertex connectivity at least three.  The
  36 not excluded are `17--40`, `46`, `53`, `145--150`, `156`, `163`,
  `168`, and `183`.  This is the connectivity regime relevant to a
  minimal counterexample, which is known to be 4-connected.
- within the remaining order-14 `C4+C4+C6` equality family, 67 of 93
  pinned first-factor orbits are excluded under the same explicit
  minimum-connectivity-three hypothesis.  The 26 not excluded are
  `9--11`, `13--16`, `22`, `36--41`, `45--51`, `54--55`, `57`, `63`,
  and `68`.  The aggregate certificates are globally reconstructed and
  their DRAT proofs are independently replayed.

The current public problem statement and the July 2026 formalization still
list the hard `d=3<n` general case as open:

- <https://mariokrenn.wordpress.com/graph-theory-question/>
- <https://github.com/google-deepmind/formal-conjectures/blob/af88acbf9da0f26e3e934743a819e986e02f6875/FormalConjectures/Paper/MonochromaticQuantumGraph.lean>
- <https://arxiv.org/abs/2407.00303>

## Active work-in-progress snapshot

The current `P_5 -> Delta_3` coordinate-support CEGAR machinery and frozen
ledgers are published in
[`research_snapshots/2026-07-27-p5-coordinate-cegar/`](research_snapshots/2026-07-27-p5-coordinate-cegar/README.md).
That snapshot is deliberately labeled exploratory: its active ledgers are
not complete branch certificates and do not change the global
**UNRESOLVED** status above.

The snapshot's non-unimodular Laurent failure has since been reproduced and
closed on three actual determinant-`2` strata. Two Singular algorithms and
an independent `msolve` conversion all certify the unit ideal, while a
focused semantic audit replays the resulting clauses exactly. The packaged
evidence is in
[`nonunimodular_boundary/`](research_snapshots/2026-07-27-p5-coordinate-cegar/nonunimodular_boundary/README.md).

The proper-colour all-full part of the exact-three-coordinate boundary is
also closed on its three support orbits. Exact Singular and `msolve`
certificates, plus a semantic coefficient verifier and independent orbit
census, are in
[`all_full_tricolour_boundary/`](research_snapshots/2026-07-27-p5-coordinate-cegar/all_full_tricolour_boundary/README.md).

The proper-colour hypothesis has now been removed.  The complete all-full
layer has 226 support orbits: pair-incidence quotas exclude 213, the prior
proper theorem excludes three, and exact coefficient ideals exclude all
198 viable signature tuples on the remaining ten.  The full audit,
regenerators, and solver replay package are in
[`all_full_boundary/`](research_snapshots/2026-07-27-p5-coordinate-cegar/all_full_boundary/README.md).

The next support layer is now closed too.  Among the ten non-coordinate
cells, no exact-three-coordinate restriction can have exactly one
two-colour cell and nine full cells.  An exhaustive audit reduces 5,676
support orbits to 319 viable supports, and exact support-only coefficient
ideals exclude all 319.  The replay package is in
[`one_partial_boundary/`](research_snapshots/2026-07-27-p5-coordinate-cegar/one_partial_boundary/README.md).
Combined with the all-full theorem, this forces at least two partial cells
in the remaining exact-three-coordinate branch.

The exact-two layer is now closed as well.  An independent packed-array
audit reconstructs all 6,298,560 labelled supports and 76,098 symmetry
orbits.  Local validity, the 30 pair Hall quotas, and direct support
semantics leave 3,308 supports.  Exact support-only coefficient ideals
exclude all 3,308: 3,307 directly and one through an exactly equivalent
split saturation.  The replay package is in
[`two_partial_boundary/`](research_snapshots/2026-07-27-p5-coordinate-cegar/two_partial_boundary/README.md).
Together with the preceding layers, this forces at least three partial
cells in the remaining exact-three-coordinate branch.

The ongoing exact-three search now uses a symmetry-broken SAT enumerator
instead of materializing its 50,388,480 labelled supports.  The structural
alternatives and their concrete go/no-go tests are recorded in
[`P5_ALTERNATIVE_STRATEGY_MAP.md`](P5_ALTERNATIVE_STRATEGY_MAP.md).
The `C10` half has now been independently regenerated and agrees exactly
with the 11,751-case SAT catalogue; the packaged census is in
[`three_partial_c10_audit/`](research_snapshots/2026-07-27-p5-coordinate-cegar/three_partial_c10_audit/README.md).
This is an exact census checkpoint, not yet an algebraic exclusion.

## Problem

For even `n`, `d` colours, and a complex `d x d` block `W_ij` on every
unordered vertex pair, define

```text
T_W(a_1,...,a_n)
  = sum over perfect matchings M
      product over {i,j} in M of W_ij[a_i,a_j].
```

The conjecture says that

```text
T_W != sum_(c=1)^d e_c tensor ... tensor e_c
```

for `n >= 6`, `d >= 3`.  Restriction to any three colours makes `d=3`
the essential remaining case.

## Authoritative certificate maps

- [`SIX_VERTEX_CERTIFICATE.md`](SIX_VERTEX_CERTIFICATE.md)
- [`EIGHT_VERTEX_4REGULAR_CERTIFICATE.md`](EIGHT_VERTEX_4REGULAR_CERTIFICATE.md)
- [`EIGHT_VERTEX_DEGREE4_FRONTIER.md`](EIGHT_VERTEX_DEGREE4_FRONTIER.md)
- [`EIGHT_VERTEX_16EDGE_CERTIFICATE.md`](EIGHT_VERTEX_16EDGE_CERTIFICATE.md)
- [`EIGHT_VERTEX_17EDGE_CERTIFICATE.md`](EIGHT_VERTEX_17EDGE_CERTIFICATE.md)
- [`EIGHT_VERTEX_DEGREE3_E19_CERTIFICATE.md`](EIGHT_VERTEX_DEGREE3_E19_CERTIFICATE.md)
- [`EIGHT_VERTEX_ENTRY84_BOUNDARY.md`](EIGHT_VERTEX_ENTRY84_BOUNDARY.md)
- [`EIGHT_VERTEX_DOUBLE_C4_FAMILY_CERTIFICATE.md`](EIGHT_VERTEX_DOUBLE_C4_FAMILY_CERTIFICATE.md)
- [`EIGHT_VERTEX_FULL_SINGLETON_FAMILY_CERTIFICATE.md`](EIGHT_VERTEX_FULL_SINGLETON_FAMILY_CERTIFICATE.md)
- [`ODD_FULL_FACTOR_ONE_TERM_THEOREM.md`](ODD_FULL_FACTOR_ONE_TERM_THEOREM.md)
- [`SINGLE_EVEN_CYCLE_RECTANGLE_THEOREM.md`](SINGLE_EVEN_CYCLE_RECTANGLE_THEOREM.md)
- [`FOURTEEN_VERTEX_ONE_EXTRA_CYCLE_LEMMA.md`](FOURTEEN_VERTEX_ONE_EXTRA_CYCLE_LEMMA.md)
- [`EVEN_CYCLE_FEASIBLE_SET_EXPANSION.md`](EVEN_CYCLE_FEASIBLE_SET_EXPANSION.md)
- [`MINIMAL_SINGLETON_CIRCUIT_RECTANGLE_THEOREM.md`](MINIMAL_SINGLETON_CIRCUIT_RECTANGLE_THEOREM.md)
- [`PARTIAL_MINIMAL_SINGLETON_CIRCUIT_DICHOTOMY.md`](PARTIAL_MINIMAL_SINGLETON_CIRCUIT_DICHOTOMY.md)
- [`ADJACENT_PORT_DETERMINANT_TRANSPORT_LEMMA.md`](ADJACENT_PORT_DETERMINANT_TRANSPORT_LEMMA.md)
- [`THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md`](THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md)
- [`DOUBLE_STAR_ANNIHILATION_LEMMA.md`](DOUBLE_STAR_ANNIHILATION_LEMMA.md)
- [`MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md`](MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md)
- [`EXACT_THREE_BLOCKER_PERMANENT_RANK_LEMMA.md`](EXACT_THREE_BLOCKER_PERMANENT_RANK_LEMMA.md)
- [`FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md`](FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md)
- [`SUPPORT_THREE_P5_CONTRACTION_SUBRANK.md`](SUPPORT_THREE_P5_CONTRACTION_SUBRANK.md)
- [`SUPPORT_FOUR_P5_CONTRACTION_RESTRICTION.md`](SUPPORT_FOUR_P5_CONTRACTION_RESTRICTION.md)
- [`FIVE_ROW_PROJECTIVE_INCIDENCE_LEMMA.md`](FIVE_ROW_PROJECTIVE_INCIDENCE_LEMMA.md)
- [`FIVE_ROW_PROJECTIVE_NORMAL_FORMS.md`](FIVE_ROW_PROJECTIVE_NORMAL_FORMS.md)
- [`ALL_QUADRANGLE_P5_OBSTRUCTION.md`](ALL_QUADRANGLE_P5_OBSTRUCTION.md)
- [`P5_COORDINATE_PLANE_PAIR_COVER.md`](P5_COORDINATE_PLANE_PAIR_COVER.md)
- [`P5_KERNEL_HALL_HIERARCHY.md`](P5_KERNEL_HALL_HIERARCHY.md)
- [`P5_SOURCE_ROW_TRICOLOUR_COVER.md`](P5_SOURCE_ROW_TRICOLOUR_COVER.md)
- [`P5_PAIR_SIGNATURE_CATALOGUE_COVERAGE.md`](P5_PAIR_SIGNATURE_CATALOGUE_COVERAGE.md)
- [`P5_THREE_COORDINATE_CYCLE_DICHOTOMY.md`](P5_THREE_COORDINATE_CYCLE_DICHOTOMY.md)
- [`P5_ALL_FULL_TRICOLOUR_OBSTRUCTION.md`](P5_ALL_FULL_TRICOLOUR_OBSTRUCTION.md)
- [`P5_ALL_FULL_BOUNDARY_OBSTRUCTION.md`](P5_ALL_FULL_BOUNDARY_OBSTRUCTION.md)
- [`P5_ONE_PARTIAL_BOUNDARY_OBSTRUCTION.md`](P5_ONE_PARTIAL_BOUNDARY_OBSTRUCTION.md)
- [`P5_EXACT_TWO_PARTIAL_BOUNDARY_OBSTRUCTION.md`](P5_EXACT_TWO_PARTIAL_BOUNDARY_OBSTRUCTION.md)
- [`P5_EXACT_THREE_C4C6_BOUNDARY_OBSTRUCTION.md`](P5_EXACT_THREE_C4C6_BOUNDARY_OBSTRUCTION.md)
- [`P5_EXACT_THREE_C10_CENSUS.md`](P5_EXACT_THREE_C10_CENSUS.md)
- [`P5_EXACT_THREE_MOTIF_QUOTIENT.md`](P5_EXACT_THREE_MOTIF_QUOTIENT.md)
- [`P5_FIVE_EQUATION_LAURENT_CORE.md`](P5_FIVE_EQUATION_LAURENT_CORE.md)
- [`P5_NO_QUADRATIC_RESTRICTION_EQUATIONS.md`](P5_NO_QUADRATIC_RESTRICTION_EQUATIONS.md)
- [`P5_NO_CUBIC_RESTRICTION_EQUATIONS.md`](P5_NO_CUBIC_RESTRICTION_EQUATIONS.md)
- [`P5_NO_QUARTIC_RESTRICTION_EQUATIONS.md`](P5_NO_QUARTIC_RESTRICTION_EQUATIONS.md)
- [`P5_NO_QUINTIC_RESTRICTION_EQUATIONS.md`](P5_NO_QUINTIC_RESTRICTION_EQUATIONS.md)
- [`P5_DEGREE_SIX_INVARIANT_PULLBACK.md`](P5_DEGREE_SIX_INVARIANT_PULLBACK.md)
- [`P5_ALTERNATIVE_STRATEGY_MAP.md`](P5_ALTERNATIVE_STRATEGY_MAP.md)
- [`THREE_COLOUR_BLOCKER_UNION_LEMMA.md`](THREE_COLOUR_BLOCKER_UNION_LEMMA.md)
- [`FOUR_BLOCKER_IDEAL_OBSTRUCTION.md`](FOUR_BLOCKER_IDEAL_OBSTRUCTION.md)
- [`UNIVERSAL_FIVE_BLOCKER_DIVISIBILITY_LEMMA.md`](UNIVERSAL_FIVE_BLOCKER_DIVISIBILITY_LEMMA.md)
- [`THREE_COLOUR_BALANCED_BRIDGE_INTERSECTION_THEOREM.md`](THREE_COLOUR_BALANCED_BRIDGE_INTERSECTION_THEOREM.md)
- [`FOUR_REGULAR_BALANCED_BRIDGE_OBSTRUCTION.md`](FOUR_REGULAR_BALANCED_BRIDGE_OBSTRUCTION.md)
- [`FIVE_REGULAR_BALANCED_BRIDGE_DIAGONAL_BACKBONE.md`](FIVE_REGULAR_BALANCED_BRIDGE_DIAGONAL_BACKBONE.md)
- [`THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md`](THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md)
- [`RECIPROCAL_PORT_ORIENTATION_CORRECTION.md`](RECIPROCAL_PORT_ORIENTATION_CORRECTION.md)
- [`ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`](ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md)
- [`UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md`](UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md)
- [`EIGHT_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md`](EIGHT_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md)
- [`TEN_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md`](TEN_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md)
- [`TWELVE_VERTEX_COMPLEMENT_PROFILE_SET_TREE_OBSTRUCTION.md`](TWELVE_VERTEX_COMPLEMENT_PROFILE_SET_TREE_OBSTRUCTION.md)
- [`FULL_ADMISSIBLE_POTENTIAL_CONE_LEMMA.md`](FULL_ADMISSIBLE_POTENTIAL_CONE_LEMMA.md)
- [`TWELVE_VERTEX_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`](TWELVE_VERTEX_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md)
- [`INTEGER_SIGNED_LATTICE_TRANSPORT_THEOREM.md`](INTEGER_SIGNED_LATTICE_TRANSPORT_THEOREM.md)
- [`PARTIAL_CIRCUIT_BINOMIAL_CLOSURE_LEMMA.md`](PARTIAL_CIRCUIT_BINOMIAL_CLOSURE_LEMMA.md)
- [`PINNED_FACTOR_SUPPORT_SYMMETRY_LEMMA.md`](PINNED_FACTOR_SUPPORT_SYMMETRY_LEMMA.md)
- [`FULL_COLOUR_SUPPORT_ORBIT_LEMMA.md`](FULL_COLOUR_SUPPORT_ORBIT_LEMMA.md)
- [`COLOUR_SYMMETRIC_FACTOR_ORBIT_TRANSFER_LEMMA.md`](COLOUR_SYMMETRIC_FACTOR_ORBIT_TRANSFER_LEMMA.md)
- [`FOURTEEN_VERTEX_MINIMAL_CIRCUIT_FRONTIERS_CERTIFICATE.md`](FOURTEEN_VERTEX_MINIMAL_CIRCUIT_FRONTIERS_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_NO_ONE_TERM_SUPPORT.md`](FOURTEEN_VERTEX_NO_ONE_TERM_SUPPORT.md)
- [`MATCHING_FORK_TRANSPORT_LEMMA.md`](MATCHING_FORK_TRANSPORT_LEMMA.md)
- [`FOURTEEN_VERTEX_C3_C4_C7_FAMILY_CERTIFICATE.md`](FOURTEEN_VERTEX_C3_C4_C7_FAMILY_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C3_C5_C6_FAMILY_CERTIFICATE.md`](FOURTEEN_VERTEX_C3_C5_C6_FAMILY_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C3_C3_C8_FAMILY_CERTIFICATE.md`](FOURTEEN_VERTEX_C3_C3_C8_FAMILY_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C3_C3_C4_C4_FAMILY_CERTIFICATE.md`](FOURTEEN_VERTEX_C3_C3_C4_C4_FAMILY_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C4_C5_C5_FAMILY_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C5_C5_FAMILY_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C4_C10_ORBIT0_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C10_ORBIT0_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C4_C10_ORBIT1_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C10_ORBIT1_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C6_C8_ORBITS0_2_CERTIFICATE.md`](FOURTEEN_VERTEX_C6_C8_ORBITS0_2_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C6_C8_108_ORBITS_CERTIFICATE.md`](FOURTEEN_VERTEX_C6_C8_108_ORBITS_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C6_C8_117_ORBITS_CERTIFICATE.md`](FOURTEEN_VERTEX_C6_C8_117_ORBITS_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C6_C8_118_ORBITS_CERTIFICATE.md`](FOURTEEN_VERTEX_C6_C8_118_ORBITS_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C6_C8_119_ORBITS_CERTIFICATE.md`](FOURTEEN_VERTEX_C6_C8_119_ORBITS_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C6_C8_121_ORBITS_KAPPA3_CERTIFICATE.md`](FOURTEEN_VERTEX_C6_C8_121_ORBITS_KAPPA3_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C6_C8_122_ORBITS_KAPPA3_CERTIFICATE.md`](FOURTEEN_VERTEX_C6_C8_122_ORBITS_KAPPA3_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C6_C8_123_ORBITS_KAPPA3_CERTIFICATE.md`](FOURTEEN_VERTEX_C6_C8_123_ORBITS_KAPPA3_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C6_C8_124_ORBITS_KAPPA3_CERTIFICATE.md`](FOURTEEN_VERTEX_C6_C8_124_ORBITS_KAPPA3_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C6_C8_125_ORBITS_KAPPA3_CERTIFICATE.md`](FOURTEEN_VERTEX_C6_C8_125_ORBITS_KAPPA3_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C6_C8_130_ORBITS_KAPPA3_CERTIFICATE.md`](FOURTEEN_VERTEX_C6_C8_130_ORBITS_KAPPA3_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C4_C4_C6_ORBIT2_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_ORBIT2_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C4_C4_C6_ORBIT3_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_ORBIT3_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C4_C4_C6_ORBIT5_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_ORBIT5_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C4_C4_C6_ORBIT6_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_ORBIT6_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C4_C4_C6_ORBIT7_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_ORBIT7_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C4_C4_C6_ORBIT8_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_ORBIT8_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C4_C4_C6_ORBIT8_PARTIAL_BINOMIAL_SUPPORT_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_ORBIT8_PARTIAL_BINOMIAL_SUPPORT_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C4_C4_C6_ORBIT44_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_ORBIT44_CERTIFICATE.md)
- [`FOURTEEN_VERTEX_C4_C4_C6_61_ORBITS_KAPPA3_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_61_ORBITS_KAPPA3_CERTIFICATE.md)
- [`TEN_VERTEX_C4_C6_SUPPORT_CERTIFICATE.md`](TEN_VERTEX_C4_C6_SUPPORT_CERTIFICATE.md)
- [`TEN_VERTEX_C4_C6_FAMILY_CERTIFICATE.md`](TEN_VERTEX_C4_C6_FAMILY_CERTIFICATE.md)
- [`TEN_VERTEX_C10_EQUALITY_CERTIFICATE.md`](TEN_VERTEX_C10_EQUALITY_CERTIFICATE.md)
- [`TEN_VERTEX_ODD_FACTOR_EQUALITY_CERTIFICATE.md`](TEN_VERTEX_ODD_FACTOR_EQUALITY_CERTIFICATE.md)
- [`TEN_VERTEX_FIVE_REGULAR_EQUALITY_BOUNDARY.md`](TEN_VERTEX_FIVE_REGULAR_EQUALITY_BOUNDARY.md)
- [`RESEARCH_NOTES.md`](RESEARCH_NOTES.md)

Each theorem-level claim requires:

1. exact reconstruction of every algebraic or elementary learned conflict;
2. exhaustive regeneration of the relevant unlabeled skeleton/role
   catalogue;
3. byte-checked selector-CNF compilation;
4. an independent SAT decision;
5. independent DRAT replay returning `s VERIFIED`;
6. a final SHA-256 hash-chain audit.

## One-command theorem audits

With the bundled dependencies on `PYTHONPATH`, run:

```text
python verify_q2_n6_k4_d4_construction.py
PYTHONPATH=tmp/python_deps python verify_q2_n6_k4_d4_family.py
PYTHONPATH=tmp/python_deps python verify_q2_herald_promotion_rank_barrier.py
python verify_six_vertex_final.py
python verify_eight_vertex_4regular.py
python verify_eight_vertex_16edge.py
python verify_eight_vertex_degree4_e17.py
python verify_eight_vertex_degree3_e19.py
python verify_eight_vertex_entry84_boundary.py
python verify_five_regular_double_c4_singleton_family.py
python verify_five_regular_full_singleton_family.py
python verify_unary_cycle_relation_family.py
python verify_eight_vertex_three_amplitude_forks.py
python verify_ten_vertex_equality_factor_lattice.py
python verify_ten_vertex_equality_factor_lattice_final.py
python verify_ten_vertex_three_amplitude_certificate.py
python verify_ten_vertex_c4_c6_equality_family.py
python verify_ten_vertex_c10_equality_family.py --certificates tmp/ten_vertex_c10_equality_support_transport_final2.json
python verify_ten_vertex_five_regular_equality_boundary.py
python verify_odd_full_factor_one_term_mechanism.py
python verify_minimal_singleton_circuit_rectangle_theorem.py
python verify_partial_minimal_singleton_circuit_dichotomy.py
python verify_adjacent_port_determinant_transport_lemma.py
python verify_three_colour_balanced_bridge_intersection.py
python audit_three_colour_balanced_bridge_intersection.py
python verify_four_regular_balanced_bridge_obstruction.py
python audit_four_regular_balanced_bridge_obstruction.py
python verify_five_regular_balanced_bridge_diagonal_backbone.py
python audit_five_regular_balanced_bridge_diagonal_backbone.py
python verify_three_colour_diagonal_matching_balance.py
python audit_three_colour_diagonal_matching_balance.py
python verify_reciprocal_port_orientation.py
python verify_arbitrary_order_degree_six_kotzig_port_obstruction.py
python audit_arbitrary_order_degree_six_kotzig_port_obstruction.py
python verify_universal_saturated_diagonal_zero_layer.py
python audit_universal_saturated_diagonal_zero_layer.py
python verify_multi_star_blocker_factorisation.py
python audit_multi_star_blocker_factorisation.py
python verify_exact_three_blocker_permanent_rank.py
python audit_exact_three_blocker_permanent_rank.py
python verify_fourth_order_permanent_subrank.py
python audit_fourth_order_permanent_subrank.py
python verify_support_three_p5_contraction_subrank.py
python audit_support_three_p5_contraction_subrank.py
python verify_support_four_p5_contraction_restriction.py
python audit_support_four_p5_contraction_restriction.py
python verify_five_row_projective_incidence.py
python audit_five_row_projective_incidence.py
python verify_five_row_projective_normal_forms.py
python audit_five_row_projective_normal_forms.py
python verify_all_quadrangle_p5_obstruction.py
python audit_all_quadrangle_p5_obstruction.py
python verify_p5_coordinate_plane_pair_cover.py
python audit_p5_coordinate_plane_pair_cover.py
python verify_p5_kernel_hall_hierarchy.py
python audit_p5_kernel_hall_hierarchy.py
python verify_p5_source_row_tricolour_cover.py
python audit_p5_source_row_tricolour_cover.py
PYTHONPATH=tmp/python_deps python verify_p5_exact_three_c4c6_boundary_obstruction.py
PYTHONPATH=tmp/python_deps python verify_p5_exact_three_c10_audit.py
python verify_three_colour_blocker_union.py
python audit_three_colour_blocker_union.py
python verify_four_blocker_ideal_obstruction.py
python audit_four_blocker_ideal_obstruction.py
PYTHONPATH=tmp/python_deps python certify_eight_vertex_balanced_set_trees.py
PYTHONPATH=tmp/python_deps python audit_eight_vertex_balanced_set_trees.py
PYTHONPATH=tmp/python_deps python certify_ten_vertex_balanced_set_trees.py
PYTHONPATH=tmp/python_deps python audit_ten_vertex_balanced_set_trees.py
PYTHONPATH=tmp/python_deps python certify_twelve_vertex_complement_profile.py
PYTHONPATH=tmp/python_deps python audit_twelve_vertex_complement_profile.py
python verify_full_admissible_potential_cone.py
python audit_full_admissible_potential_cone.py
python audit_twelve_vertex_port_cell_orbits.py
python compare_twelve_vertex_six_potential_orbit_audit.py
python verify_integer_signed_lattice_transport.py
python verify_fourteen_vertex_partial_circuit_binomial_branch.py tmp/fourteen_vertex_c4_c4_c6_orbit8_partial_binomial_closure_all22_r2.json --output tmp/fourteen_vertex_c4_c4_c6_orbit8_partial_binomial_closure_all22_r2_verified.json
python verify_fourteen_vertex_partial_circuit_binomial_selection_chain.py tmp/fourteen_vertex_c4_c4_c6_orbit8_partial_binomial_selection_cegar_minimal_v5.json --output tmp/fourteen_vertex_c4_c4_c6_orbit8_partial_binomial_selection_cegar_minimal_v5_verified.json
python verify_fourteen_vertex_binomial_support_closure_augmentation.py tmp/fourteen_vertex_c4_c4_c6_orbit8_binomial1_augmentation.json --output tmp/fourteen_vertex_c4_c4_c6_orbit8_binomial1_augmentation_verified.json
python verify_fourteen_vertex_partial_circuit_binomial_selection_chain.py tmp/fourteen_vertex_c4_c4_c6_orbit8_support2_partial_binomial_selection_cegar.json --output tmp/fourteen_vertex_c4_c4_c6_orbit8_support2_partial_binomial_selection_cegar_verified.json
python verify_fourteen_vertex_binomial_support_closure_augmentation.py tmp/fourteen_vertex_c4_c4_c6_orbit8_binomial2_augmentation.json --output tmp/fourteen_vertex_c4_c4_c6_orbit8_binomial2_augmentation_verified.json
python verify_fourteen_vertex_minimal_circuit_frontiers.py
python verify_fourteen_vertex_no_one_term_support.py
python verify_fourteen_vertex_binomial_trinomial.py
python certify_fourteen_vertex_matching_fork.py tmp/fourteen_vertex_direct_free_search_p500000_multiswitch.json
python verify_fourteen_vertex_cancellation_transport.py tmp/fourteen_vertex_direct_free_search_p500000_multiswitch.json tmp/fourteen_vertex_matching_fork_p500000_multiswitch.json --output tmp/fourteen_vertex_matching_fork_p500000_multiswitch_verified.json
python certify_fourteen_vertex_c3_c4_c7_family.py
python verify_fourteen_vertex_c3_c4_c7_family.py
python verify_fourteen_vertex_c3_c5_c6_family.py
python verify_fourteen_vertex_c3_c3_c8_family.py
python verify_fourteen_vertex_c3_c3_c4_c4_family.py
python verify_fourteen_vertex_c4_c5_c5_family.py
python verify_fourteen_vertex_c14_rectangle_theorem.py
python verify_fourteen_vertex_c4_10_orbit0.py
python verify_fourteen_vertex_c4_10_orbit1.py
python verify_fourteen_vertex_c6_8_130_orbits_kappa3.py
python verify_fourteen_vertex_c4_c4_c6_orbit2.py
python verify_fourteen_vertex_c4_c4_c6_orbit3.py
python verify_fourteen_vertex_c4_c4_c6_orbit5.py
python verify_fourteen_vertex_c4_c4_c6_orbit6.py
python verify_fourteen_vertex_c4_c4_c6_orbit7.py
python verify_fourteen_vertex_c4_c4_c6_orbit8.py
python verify_fourteen_vertex_c4_c4_c6_orbit44_core24.py
python verify_fourteen_vertex_c4_c4_c6_58_orbits.py
python -m unittest -v test_search_witness.py
python -m unittest -v test_fourteen_vertex_two_even_cycle_rule_sat.py test_fourteen_vertex_minimum_activity_certificate.py
```

The current regression suite has 53 tests.  The final audit JSON for every
claimed theorem must contain `"verified": true`.

The `tmp/` directory contains large pinned CNFs and proof traces.  Some DRAT
files are hundreds of megabytes; do not replace them with solver summaries,
because the raw proof and its independent replay are part of the evidence
contract.

## Current continuation

The active computational frontiers are:

- exact 18 edges with a degree-four vertex;
- exact 20 edges in the normalized same-colour and different-colour
  reciprocal-killer branches, now with at most 83 supported entries in the
  5-regular slice.

The main analytic tools now include:

- distinct rank-one generic killers and diagonal anchors;
- complete local killer flags;
- degree-three singleton stars;
- degree-four monochromatic singletons;
- the degree-five singleton-or-swap normal form;
- the exact-20 entry bound and equality-diagonal forcing theorem;
- cancellation transport between adjacent colourings;
- the two-monomial rectangle obstruction;
- the singleton-exchange rectangle motif;
- odd signed triangles of two-monomial amplitudes;
- signed binomial-lattice/partial-character certificates;
- double-star blockers and the simultaneous balanced-bridge
  eight-type classification;
- multi-star blocker surplus and exact pure-minor factorisation;
- the exact three-blocker permanent-tensor rank obstruction;
- the exact order-four permanent-subrank obstruction;
- the support-at-most-three `P_5` contraction subrank obstruction;
- the explicit support-four `P_5` contraction restriction to `Delta_3`;
- the five-row projective incidence/singleton-row lemma;
- the three-colour five-vertex blocker-union lower bound;
- four- and eight-term affine Laurent-cube factor choices with exact lattice
  CEGAR;
- exact Laurent and rational linear-monomial fallback certificates.

The former four-blocker boundary is now excluded at every even order.
After restricting every nonblocker to the simultaneous kernel of the two
root covectors, the four free blocker modes satisfy an identity in the
ideal generated by their six root-pair forms.  The tight span
classification leaves only the incidence types `0,0,12,12`,
`0,01,12,12`, and `01,01,02,02`.  Each type has an explicit common zero
of all six generators at which one nonzero GHZ diagonal term survives.
This contradiction raises the arbitrary-order lower bound to five
distinct blockers.  The symbolic verifier and an independent 544-case
`F_5` audit are documented in
[`FOUR_BLOCKER_IDEAL_OBSTRUCTION.md`](FOUR_BLOCKER_IDEAL_OBSTRUCTION.md).

Promoting a simultaneous-kernel vertex to a third root now has a sharp
equality obstruction.  With exactly three blockers, their root--blocker
tensor is a local image of the order-three `3 x 3` permanent tensor.
If all three residual coordinate products remained active, all three
local maps would be invertible.  The permanent tensor has tensor rank
four—its three-dimensional slice space contains no nonzero rank-one
matrix—whereas the resulting three-term diagonal has rank three.  Hence
some other residual coordinate product must vanish.  The proof and an
independent `F_5` slice audit are in
[`EXACT_THREE_BLOCKER_PERMANENT_RANK_LEMMA.md`](EXACT_THREE_BLOCKER_PERMANENT_RANK_LEMMA.md).

The next fully tight endpoint is also impossible.  The order-four
permanent tensor cannot restrict to a concise three-colour diagonal
tensor.  Every local map in such a restriction would select a hyperplane
of `C^4`.  Factoring each `2|2` flattening through the six-dimensional
space of unordered coordinate pairs shows that flattening rank three
forces at least three selected hyperplanes to coincide, with a common
normal supported on at most two coordinates.  Support one destroys
conciseness.  In the support-two case the remaining three-mode slice
space is

```text
l * span{mn, l n, l m},
```

which contains no nonzero decomposable tensor, while a diagonal
three-colour slice space contains three.  An alternating eight-cycle
gives the matching lower bound two, so the subrank is exactly two.
Consequently four fully supported zero-coupled roots cannot have a
four-vertex total blocker union.  The symbolic reconstruction and an
independent audit of all 24,336 ordered hyperplane-normal pairs over
`F_5` are in
[`FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md`](FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md).

The first genuinely new contraction of the order-five permanent tensor
is now also excluded.  A support-three contraction is the quartic
`a b q`, where `q` is a nondegenerate ternary quadratic.  In a
hypothetical restriction to `Delta_3`, the common kernels of the
pullbacks of `a,b` must consist only of target vectors with a zero
coordinate; contracting any full-support vector there would produce
the forbidden restriction `P_3 -> Delta_3`.  Restricting complementary
pairs of those kernels then forces their coordinatewise-product spaces
to be at most one-dimensional and to match the rank and row spaces of
the corresponding `a,b` pair form.  The nine possible line/plane kernel
types give 6,561 cases and no survivor; an independent `F_5` audit
checks 104,976 actual kernel quadruples.  This proves exact subrank two
for support three and the upper bound two for every support-at-most-three
contraction.  The remaining `P_5` boundary is a five-row projective
incidence condition, not another unconstrained numerical search.  See
[`SUPPORT_THREE_P5_CONTRACTION_SUBRANK.md`](SUPPORT_THREE_P5_CONTRACTION_SUBRANK.md).

The support-three boundary is sharp.  For the canonical support-four
contraction by `(1,1,1,1,0)`, four explicit integer `5 x 3` maps send
the resulting quartic to `12 Delta_3`.  The construction belongs to a
two-parameter family and all full support-four contractions are
equivalent by coordinate scaling.  Exact expansion checks all 81 target
coefficients, and independent `F_5` and `F_7` audits replay the integer
point and the family.  This positive restriction is not a restriction
of `P_5` itself, but it proves that the tempting support-four extension
of the contraction obstruction is false.  See
[`SUPPORT_FOUR_P5_CONTRACTION_RESTRICTION.md`](SUPPORT_FOUR_P5_CONTRACTION_RESTRICTION.md).

The surviving `P_5` maps nevertheless have a forced zero pattern.
Intersecting a local three-plane with any source coordinate
three-plane and applying the support-at-most-three theorem shows that
the span of every pair of its five row covectors contains a target
coordinate covector.  Five non-coordinate projective points with this
property would colour every edge of `K_5` by one of three coordinate
points and make every triangle rainbow, which is impossible at a
degree-four vertex.  Hence every local map has a nonzero singleton row.
There are 68 singleton-placement orbits after source, mode, and colour
symmetry.  The exact proof and an independent census of 376,992
five-point multisets over `F_5` are in
[`FIVE_ROW_PROJECTIVE_INCIDENCE_LEMMA.md`](FIVE_ROW_PROJECTIVE_INCIDENCE_LEMMA.md).

The forced singleton has a short exact geometric refinement.  If it is
the only coordinate row, the other four projective rows either lie on
one coordinate-bearing line or form a complete quadrangle whose three
diagonal points are exactly the target coordinate points.  The latter
is rigid up to diagonal rescaling, with representatives
`(1,1,1),(-1,1,1),(1,-1,1),(1,1,-1)`.  In the line case a target vector
of support at most two maps to a source vector of support exactly one.
Thus every hypothetical local map belongs to one of only three
geometric strata: at least two coordinate rows, line type, or rigid
quadrangle type.  An independent `F_5` census classifies all 2,556
spanning pair-incidence configurations.  See
[`FIVE_ROW_PROJECTIVE_NORMAL_FORMS.md`](FIVE_ROW_PROJECTIVE_NORMAL_FORMS.md).

The rigid branch cannot occur in all five modes.  For any fixed pair of
source rows, a quadrangle map has a common-kernel vector supported on
exactly two target colours.  Among five such vectors, four share a
surviving colour.  Evaluating the alleged diagonal restriction on those
four vectors and the corresponding coordinate vector in the fifth mode
is nonzero.  The source permanent is zero, because four modes avoid the
same two source coordinates and cannot be injected into the remaining
three.  This exact pigeonhole obstruction forces at least one mode into
the line or multiple-coordinate stratum.  See
[`ALL_QUADRANGLE_P5_OBSTRUCTION.md`](ALL_QUADRANGLE_P5_OBSTRUCTION.md).

The same four-mode evaluation gives a stronger ten-pair cover.  For a
fixed source pair, the five common kernels have nonempty active-colour
sets of size at most two.  No colour can be active in four modes, so an
incidence count forces one kernel to be a coordinate line; dually, that
mode's two rows span a coordinate plane.  This holds for all ten source
pairs.  A quadrangle map covers none of them, and a non-axial line map
covers at most one.  Hence every hypothetical restriction contains
either a map with at least two coordinate rows or an axial `4+1` map
with four two-colour rows and one row on the third colour.  See
[`P5_COORDINATE_PLANE_PAIR_COVER.md`](P5_COORDINATE_PLANE_PAIR_COVER.md).

The evaluation obstruction extends to a Hall hierarchy.  If `s` source
coordinates are forbidden, then `6-s` selected modes cannot be injected
into the remaining `5-s` coordinates.  Isolating one target colour in
the other modes proves that this colour can remain active in the common
kernel of those rows in at most `5-s` modes.  Dually, every fixed target
coordinate covector lies in the corresponding row span in at least
`s` modes, for `s=2,3,4`.  This adds simultaneous pair, triple, and
four-row quotas to the surviving axial and multiple-coordinate cases.
See [`P5_KERNEL_HALL_HIERARCHY.md`](P5_KERNEL_HALL_HIERARCHY.md).

The singleton boundary, where the Hall evaluation has no spare mode,
has a stronger tensor-level solution.  Fixing one source row and
restricting all five local inputs to its row kernels makes the source
permanent identically zero.  The target becomes a sum of three
decomposable tensors.  A three-term rank-one dependence can vary in at
most one tensor mode, whereas the three restricted coordinate
functionals span a space of dimension at least two in every mode.
Therefore the three colour terms must be killed separately.  For every
source row and every target colour, some local map has exactly that
coordinate row.  This forces at least 15 coordinate rows among the 25
local rows and at least three in one mode.  An independent `F_3` audit
checks all 8,568 zero-or-projective five-row multisets and 34,272
nonzero coefficient cases.  See
[`P5_SOURCE_ROW_TRICOLOUR_COVER.md`](P5_SOURCE_ROW_TRICOLOUR_COVER.md).

The finite local signature catalogue now has an exact coverage theorem
over `C`.  An abstract Boolean encoding retains only zero/nonzero row
supports, the ten coordinate-pair incidences, projective plane closure,
and necessary rank conditions.  After blocking the 6,495 signatures
listed by an `F_5` enumeration, exactly 303 patterns remain.  In every
one, all ten row pairs contain the same coordinate point; this forces
every triple of rows to be dependent and the local map to have rank at
most two.  The 303 patterns form eight `S_5 x S_3` orbits.  The final
150-variable, 9,099-clause CNF is UNSAT, and its 3,349,683-byte DRAT
proof passes independent forward replay.  Thus the finite field is only
an enumeration device: every relevant complex support/pair signature is
covered.  Higher-subset incidences and coefficient realizability are
not imported.  See
[`P5_PAIR_SIGNATURE_CATALOGUE_COVERAGE.md`](P5_PAIR_SIGNATURE_CATALOGUE_COVERAGE.md).

The saturated 15-coordinate-row boundary has a two-shape
classification.  If no mode has four coordinate rows, all five modes
must have exactly three, and every source-row/target-colour requirement
occurs exactly once.  Each mode and each source then has exactly two
non-coordinate cells.  Their mode--source incidence graph is
2-regular and bipartite on ten vertices, so it is either `C10` or
`C4+C6`.  Independent enumerations find 2,040 labelled graphs: 1,440
of the first type and 600 of the second.  See
[`P5_THREE_COORDINATE_CYCLE_DICHOTOMY.md`](P5_THREE_COORDINATE_CYCLE_DICHOTOMY.md).

Intersecting the balanced all-bridge normal form for all three colours gives
an exact arbitrary-order reduction.  Every edge block has at most four
potentially nonzero entries.  Rank three occurs exactly between
complementary endpoint types, permitted primary singletons are reciprocal,
and at support degree four the neighbourhood consists of one diagonal
complement-type anchor plus three reciprocal singleton killers.  Two
independent 64-case reconstructions have SHA-256
`c99df4a42d4f4066ebf05ad78ce7cd4f74ec9b2479a41049f0ce4606756a4820`
and
`41015b2cd28cacec7f61639efcda1af31ac3a0984e5caa16191cde823ab79944`.
See
[`THREE_COLOUR_BALANCED_BRIDGE_INTERSECTION_THEOREM.md`](THREE_COLOUR_BALANCED_BRIDGE_INTERSECTION_THEOREM.md).

The 4-regular part of that boundary is now excluded at every even order.
Contracting the forced diagonal-anchor perfect matching turns the other
edges into reciprocal singleton ports.  For any fixed background colour,
at least half of the one-anchor-pair colour perturbations contain no
compatible alternating cycle.  The anchor matching is then the unique
matching for a forbidden nonconstant colouring, so its nonzero monomial
cannot cancel.  The local type reconstruction and all 4,096 contracted
order-six port configurations pass two independent audits, one using
alternating cycles and one directly enumerating 73,728 compatible
perfect-matching instances; see
[`FOUR_REGULAR_BALANCED_BRIDGE_OBSTRUCTION.md`](FOUR_REGULAR_BALANCED_BRIDGE_OBSTRUCTION.md).
This arbitrary-order theorem is now subsumed by the
maximum-degree-five result below; the deeper-blocker branch remains
separate.

The entire maximum-degree-five boundary is now excluded at every even
order.  The three coordinate-primary killers at each vertex are distinct
off-diagonal singleton blocks, so diagonal entries can occur on at most
the other two incident support edges.  Yet every monochromatic target
amplitude supplies a perfect matching in those diagonal edges.  Their
union is therefore a disjoint collection of even paths and even cycles.
Paths have a forced all-three-colour matching.  On a cycle, the three
colour matchings choose the two alternating parities; even in the `2+1`
split, an exact eight-type finite-state argument forces every
majority-parity edge to join complementary normal types.  Consequently
there is always a spanning complementary-type anchor matching whose
edges carry at least two nonzero diagonals.  Relative to any such anchor,
an independent 32-state automaton for each pair of colours has eight
strong components, all monochromatic.  Thus every alternating cycle in a
supported pair-constant two-colour colouring is monochromatic, and the
complete amplitude factors exactly into the principal hafnians of its
two colour classes.  This needs no anchor-weight support assumption and
forces every anchor-pair-deleted principal hafnian to vanish in all three
colours, despite every full principal hafnian equalling one.

Cancellation is eliminated by the degree-two backbone itself.  On a
proper selection of anchor pairs, each diagonal component breaks into
paths whose unique perfect matching is the selected anchor edges.  On a
whole component, the factor is nonzero because the full monochromatic
hafnian is one.  Since every anchor edge supports at least two of three
colours, a nonconstant two-colour list assignment always exists and makes
both factors nonzero, contradicting its target coefficient zero.  Two
independent reconstructions are documented in
[`FIVE_REGULAR_BALANCED_BRIDGE_DIAGONAL_BACKBONE.md`](FIVE_REGULAR_BALANCED_BRIDGE_DIAGONAL_BACKBONE.md).
Every remaining simultaneous all-bridge case contains a support vertex of
degree at least six; the deeper-blocker branch is also separate.

At the resulting degree-three diagonal boundary, choosing one nonzero
monochromatic perfect matching per colour forces a further arbitrary-order
balance.  Each of the three normal-type bits is one on exactly half the
vertices.  Colour-0 matching edges flip bits 1 and 2, colour-1 edges flip
bits 0 and 2, and colour-2 edges flip bits 0 and 1.  Any edge shared by
two matchings is therefore complementary-type; if the matchings are
pairwise disjoint, their union is a rigid properly three-edge-coloured
cubic graph.  More generally, relative to any of the three matchings,
every pair-constant two-colour amplitude factors.  Deleting a
colour-`a` matching edge therefore forces the principal hafnian cofactor
of each other colour to vanish.  All nine 64-state automata have only
monochromatic strong components, and the same is true of all three
96-state automata using the full colour set.  Thus every pair-constant
three-colour amplitude factors into its principal-hafnian classes.  At
the exact cubic diagonal boundary, pairwise-disjoint chosen matchings
would consequently have no extra diagonal colours and every pairwise
union would have to be one Hamiltonian cycle: the residual graph is a
cubic perfect one-factorization.  Every diagonal block then collapses
further to its forced own-colour diagonal plus at most one optional
off-diagonal, and that optional unit is itself a reciprocal port
transition.  In the exact support-degree-six case, the support is
therefore the union of this at-most-two-unit cubic diagonal graph and a
one-unit cubic reciprocal-port graph, with at most `9n/2` matrix units in
  total.

A port-orientation audit found that the older finite programs had paired
target tasks correctly but then emitted those task labels as physical
half-colours.  The physical unit is obtained by swapping the paired target
labels and must independently survive the balanced-bridge table.  Of 96
reciprocal local target transitions, exactly 72 are physically admissible.
An integer type potential is zero on every forced diagonal transition and
strictly positive on every permitted optional diagonal transition and on
all 72 physical port transitions.  The correction is documented in
[`RECIPROCAL_PORT_ORIENTATION_CORRECTION.md`](RECIPROCAL_PORT_ORIENTATION_CORRECTION.md).

That corrected sign table yields a simple arbitrary-order contradiction.
The properly three-edge-coloured cubic diagonal graph has three differently
coloured monochromatic perfect matchings.  Bogdanov's theorem supplies a
nonmonochromatic perfect matching when `n>4`.  Its forced own-colour units
have total potential zero.  Every optional diagonal unit and every
physical port unit has positive potential, so no competing monomial for
the induced colouring can use one.  The proper edge-colouring makes the
forced matching unique, leaving a nonzero coefficient where the target
requires zero.  This excludes the complete pairwise-disjoint
exact-degree-six branch for every even `n >= 6`; see
[`ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`](ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md).

Corrected finite replays provide regressions rather than the proof.  At
orders eight, ten, and twelve they respectively find `0`, `374,544`, and
`51,168` admissible representative port covers.  Every order-ten and
order-twelve cover is already contradicted by the identity potential
(indeed every order-twelve cover succeeds under all six rays), with zero
residuals.  The old 72-cover, 547,434-cover, 15,478,610-cover, and
395-residual records are explicitly retained only as withdrawn historical
calculations.  The former state-lift cycle-fibre proposal and the old
order-fourteen port scouts used the same mistaken physical-state
convention and are withdrawn.

The remaining all-bridge targets are the overlapping selected-matching
branch and support degree at least seven.  The separate deeper-blocker
branch also remains open.

There is now a degree-free reduction on both all-bridge targets.  The sum
of the six permuted potentials is nonnegative on all 180 allowed local
units, with exact edge values `0`, `10`, and `20`; its 48 zero units are
precisely the saturated monochromatic diagonals.  Bogdanov's theorem
therefore supplies a nonmonochromatic zero-layer matching in every
hypothetical all-bridge witness.  Its forbidden coefficient can cancel
only against other saturated-diagonal matchings, so at least one
monochromatic alternating even cycle is forced.  In particular, every
edge shared by two selected colour matchings forces a remote
same-colour alternating cycle in each corresponding cofactor.  The
complete statement and independent table audit are in
[`UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md`](UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md).

Actual principal hafnian families obey more than the vertex-wise
set-tree axiom.  The coefficientwise convolution identity

```text
sum_(|A|=2k) haf(L[A]) haf(L[V-A])
  = binomial(n/2,k) haf(L)
```

forces every nonzero principal hafnian to have a nonzero complementary
split at every even size.  This arbitrary-order representability
constraint is proved and independently enumerated through order 12 in
[`HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md`](HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md).
Combined with the vanishing of every mixed complementary product, it
also forces a colour-exclusive cut at each size: both same-colour
factors are nonzero while the corresponding factor pair for either
other colour contains a zero.  At size two, every colour therefore has
an exclusive saturated edge whose own edge and complementary cofactor
are nonzero, while both other-colour edge/cofactor products vanish.

On eight vertices, the zero-layer reduction closes completely.  For each
colour, the nonzero principal hafnians form a set tree whose member
subsets obey two exact normal-bit balance equations.  Bit balance gives
57 normal-type multiplicity profiles.  A corrected distinct-colour
incompatibility encoding excludes 55 profiles; its one SAT cube orbit
consists of the two parity profiles.  In that orbit each colour graph
splits into two `K_2,2` components.  The resulting exact 24-variable,
72-clause support CNF excludes all weighted realizations, and an
independent audit tests all `7^6 = 117,649` component-support products
with zero survivors.  Both DRAT proofs replay successfully.  See
[`EIGHT_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md`](EIGHT_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md).

The same set-tree theorem closes order ten.  Its 104 balanced normal-type
profiles form 10 orbits under independent bit flips and coordinate
permutations.  All 10 orbit formulas are UNSAT in two independent
encodings and solvers.  Kissat's corrected 122,539-clause UNSAT proof is
independently replayed by `drat-trim`; see
[`TEN_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md`](TEN_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md).

At order twelve, the corrected set-tree plus all-size convolution system
now excludes the complementary profile `6 x 000 + 6 x 111`.  After fixing
one exposed matching, an exact stabilizer recursion reduces the second
tree's 120 hard partner chains to 16 canonical leaves.  The combined
81,227-variable, 209,442-clause selector CNF is UNSAT; its 70,573,433-byte
DRAT proof passes a forward `drat-trim` replay, and an independently
generated Glucose audit also finds all 17 branches UNSAT.  This is one
profile, not a complete order-twelve theorem; see
[`TWELVE_VERTEX_COMPLEMENT_PROFILE_SET_TREE_OBSTRUCTION.md`](TWELVE_VERTEX_COMPLEMENT_PROFILE_SET_TREE_OBSTRUCTION.md).

A pinned census of 123 dense 20-edge support models found an elementary
rectangle in every model.  In that enumeration order each model also had a
particularly rigid singleton-exchange certificate.  Deliberately forbidding
mixed singleton perfect matchings then produced two new SAT supports; one
has no singleton perfect matching at all, but it still has a
nonzero-target two-monomial rectangle.  Thus the singleton motif is not
universal even in the relaxation, while the broader rectangle obstruction
survived that audited census.  The later deliberately binomial-free search
below did find supports that avoid it.  The arbitrary-`n` task is now to
force the wider disjunctive signed-character calculus, or exhibit an exactly
verified support that avoids that too.

The signed-lattice abstraction unifies the two-monomial elementary
cancellation rules and many transport instances.  Two-term forbidden
amplitudes assign the value `-1` to exponent
differences.  An inconsistent lattice sign, an isolated nonzero monomial
class in a forbidden amplitude, or complete cancellation of a required
monochromatic amplitude is an exact contradiction.  It independently
certifies all 146 Laurent cubes in the older six-vertex residual and every
one of 193 distinct dense eight-vertex support models in the current
combined pinned census.  The modes split into 124 isolated forbidden
classes, 44 required amplitudes annihilated by their signed classes, and 25
inconsistent sign characters.  This remains finite evidence: the missing
global theorem is that an arbitrary hypothetical support must expose such a
signed class.

A separate toric reduction now puts any hypothetical witness into a sharper
normal form.  Repeated vertex-colour rescaling and a finite `t -> 0` limit
produce a support-minimal witness.  The Gordan--Stiemke alternative then
forces strictly positive weights on every supported matrix entry such that
the weighted degree of lifted vertex `(v,c)` depends only on `c`, not on
`v`.  Adding supported monochromatic perfect matchings equalizes the three
degrees, so the lifted support graph has a strictly positive fractional
perfect matching.  We call this a balanced support.  Exact replay of the
same 193-model census classifies 78 supports as further degenerable and 115
as already balanced.  Thus a global proof may assume balance from the
outset, although balance alone is not yet a contradiction.

The first deliberately **binomial-free** dense support has now sharpened
the algebraic frontier.  It is a balanced exact-20-edge support with 84
selected entries: eight full `3 x 3` blocks and twelve diagonal singleton
blocks.  Every forbidden amplitude has between four and seven active
matching monomials, so it has no two-term, odd-binomial-triangle, or direct
signed-lattice certificate.  This disproves the exploratory hypothesis
that every dense support must expose a literal two-term amplitude; it is
still only a support-relaxation model, not a complex witness.

The stratum itself is nevertheless impossible over `C`.  Each of its 5,648
four-term forbidden amplitudes is a Laurent parallelogram and factors into
a choice between two signed binomial relations.  There are 160 distinct
relations.  Exact signed-lattice reduction turns 13 factor branches into
isolated nonzero classes in five-term forbidden amplitudes.  The resulting
160-variable, 5,661-clause CNF is UNSAT under CaDiCaL 1.9.5, and its DRAT
proof independently replays as `s VERIFIED`.  The exact reconstruction and
replay are in
`tmp/eight_vertex_no_binomial_same_e20_factor_lattice_verified.json`.
After blocking that support, the resumed search found a second
non-isomorphic balanced 84-entry arrangement.  The same engine closes all
5,240 of its four-term factor choices with 72 exact lattice no-goods; its
5,312-clause CNF and independent DRAT replay are audited in
`tmp/eight_vertex_no_binomial_same_e20_factor_lattice_02_verified.json`.
This new factor-lattice mechanism reaches supports that the earlier direct
binomial census cannot see, but it has not yet been proved universal.

The two survivors expose a common finite architecture: eight full blocks
form a spanning 2-factor, while the complementary cubic graph is
partitioned into three perfect matchings that become twelve diagonal
singleton blocks.  Exhausting every possible 2-factor removes the initially
observed double-`C4` assumption.  Across all three 5-regular skeleton types
there are 753 spanning 2-factors, 1,323 one-factorizations up to global
colour assignment, 7,938 labelled supports, and 86 graph/colour orbits.

Exactly 1,086 supports—the 181 factorizations whose full factor is
`C4+C4`—are binomial-free.  Their 23 orbits are closed by four-term factor
choices.  Every other support has a literal two-term forbidden amplitude;
all 63 remaining orbits close in one direct signed-lattice branch.  Across
all 86 certificates there are 183,673 relations, 313,813 factor clauses,
and 1,441 exact lattice no-goods.  Every final CNF is UNSAT and every
CaDiCaL proof independently replays as `s VERIFIED`.

The 23 hard orbits now have a simpler direct replay as well.  Each contains
one four-term amplitude forcing one of two alternating-cycle relations, and
two five-term amplitudes that separately rule out those relations by two
paired cancellations plus one surviving monomial.  Therefore only three
amplitudes per orbit are needed.  The direct verifier covers all 1,086
labelled binomial-free supports through the audited orbit catalogue; the
corresponding 23 tiny redundant DRAT traces total 6,574 bytes.

`verify_five_regular_full_singleton_family.py` independently reconstructs
the three skeleton types, all 753 factors, 1,323 colour-unlabelled
factorizations, 7,938 labelled supports, 86 orbits, model assignments,
amplitude activities, semantic lattice conflicts, artifact hashes, and
audit coverage.  The aggregate audit is
`tmp/eight_vertex_five_regular_full_singleton_family_verified.json`
(SHA-256
`add0fb4e6cb8aca04a1a143e87a5383db28a86f9e276aa1ad1a3bbdd6490499a`).

The entry-count theorem now proves that every 84-entry support in the
5-regular exact-20 branch has precisely this architecture.  Combining the
support-level equality proof with the 7,938-support certificate excludes the
entire 84-entry boundary.  It does not force this architecture below 84
entries; the remaining 5-regular exact-20 boundary has at most 83 entries.
See [`EIGHT_VERTEX_ENTRY84_BOUNDARY.md`](EIGHT_VERTEX_ENTRY84_BOUNDARY.md).

The same equality architecture exists for larger even `n`.  A first
ten-vertex test has expanded to the complete `C4+C6` equality family.
Fixing the full factor leaves 446,592 colour-unlabelled factorizations and
4,903 symmetry orbits, representing 101,287,065,600 labelled coloured
supports.  Every orbit has a direct three-amplitude fork: a four-term
factorization forces one of two alternating-cycle relations, while two
five-term amplitudes rule out the alternatives by paired cancellations with
one surviving nonzero monomial.  The independent audit verifies the
catalogue, orbit coverage, activities, Laurent pairings, and survivors.
This does not cover the other ten-vertex full-factor types or arbitrary
supports.  See
[`TEN_VERTEX_C4_C6_FAMILY_CERTIFICATE.md`](TEN_VERTEX_C4_C6_FAMILY_CERTIFICATE.md).

The earlier one-support factor-lattice/DRAT proof remains as a redundant
cross-check in
[`TEN_VERTEX_C4_C6_SUPPORT_CERTIFICATE.md`](TEN_VERTEX_C4_C6_SUPPORT_CERTIFICATE.md).

All three ten-vertex odd-component equality families are now closed as well.
There are 5,558 `C3+C7`, 2,536 `C5+C5`, and 906 `C3+C3+C4` orbits, and
every support has a forbidden colouring with exactly one active nonzero
matching monomial.  Independent orbit and activity audits cover
186,216,226,560 labelled coloured supports.  See
[`TEN_VERTEX_ODD_FACTOR_EQUALITY_CERTIFICATE.md`](TEN_VERTEX_ODD_FACTOR_EQUALITY_CERTIFICATE.md).

The remaining `C10` equality family is closed by a different direct motif.
Three forbidden binomial amplitudes impose signed Laurent relations whose
exact combination forces cancellation of two terms in a forbidden
trinomial, leaving its third supported monomial nonzero.  The independent
audit replays this transport identity on all 23,204 support orbits,
representing 491,794,208,640 labelled coloured supports.  See
[`TEN_VERTEX_C10_EQUALITY_CERTIFICATE.md`](TEN_VERTEX_C10_EQUALITY_CERTIFICATE.md).

These five cycle types exhaust every spanning 2-factor on ten vertices.
Combining their audits with the entry-count and diagonal-singleton equality
theorem excludes the complete 105-entry, 5-regular exact-25 boundary:
37,107 support orbits and 779,297,500,800 labelled coloured supports.  A
hypothetical witness in that branch has at most 104 entries.  This is still
a finite boundary theorem, not a global proof.  See
[`TEN_VERTEX_FIVE_REGULAR_EQUALITY_BOUNDARY.md`](TEN_VERTEX_FIVE_REGULAR_EQUALITY_BOUNDARY.md).

The one-term mechanism is not merely finite for all-odd full factors.
At every even order `n >= 8`, choose a skeleton perfect matching with the
fewest singleton edges and activate exactly its singleton part.  Minimality
and the oddness of every full cycle make that perfect matching unique.
The only endpoint case is discharged by the lower bound on perfect
matchings in bridgeless cubic graphs, which supplies a mixed-colour
singleton matching.  This proves the arbitrary-order all-odd equality
family impossible.  See
[`ODD_FULL_FACTOR_ONE_TERM_THEOREM.md`](ODD_FULL_FACTOR_ONE_TERM_THEOREM.md).

The all-odd hypothesis is essential to that proof.  A targeted matching-poset
search found an explicit `C3+C4+C7` equality support at order 14 with no
one-term forbidden amplitude.  An independent verifier reconstructs all
267 skeleton perfect matchings and gives a second active matching for every
possible target: 249 through a proper singleton subset and 18 by flipping
the untouched `C4`.  This refutes only the proposed mixed-factor one-term
extension, not Krenn--Gu.  A stronger test closes this support: a binomial at
equation 118 transports its Laurent relation to two terms of a trinomial at
equation 112, forcing them to cancel and leaving the third monomial nonzero.
This is an exact two-amplitude contradiction for the explicit support, not
the full `C3+C4+C7` family.  See
[`FOURTEEN_VERTEX_NO_ONE_TERM_SUPPORT.md`](FOURTEEN_VERTEX_NO_ONE_TERM_SUPPORT.md).

The repeated order-14 obstruction now has an arbitrary-order analytic
form.  If adding one singleton edge to a singleton matching adds exactly one
perfect matching, while all old perfect matchings use one common full edge
at the changed endpoint, two adjacent exact-activation colourings give an
immediate cancellation contradiction.  The activation construction uses
only the bipartiteness of the union of the other two singleton 1-factors.
This replaces a `3^14` colour scan by a small perfect-matching calculation.
It independently closes four increasingly adversarial `C3+C4+C7` supports,
including the completed 500,000-prefix search candidate whose broader
direct-Laurent score was reduced to two.  See
[`MATCHING_FORK_TRANSPORT_LEMMA.md`](MATCHING_FORK_TRANSPORT_LEMMA.md).

The complete `C3+C4+C7` equality family is now closed as well.  A
deterministic factor classification starts from all 44,226 possible
singleton 1-factors.  One-term subsets remove 35,112 immediately.  The 420
exceptional safe factors form four orbits and cannot be extended to three
colours without one of 168 exact two-edge one-term sets.  The remaining
8,694 factors all send the triangle to the 7-cycle.  A catalogue of 4,368
matching forks reduces these to 3,654 fork-free factors in 18 orbits; only
36 second-factor choices survive, and none admits a third factor.  A
separate bitmask matcher reconstructs the catalogues and all orbit counts,
returning `"verified": true`.  This is a full finite family theorem, but not
the complete order-14 equality boundary or the global conjecture.  See
[`FOURTEEN_VERTEX_C3_C4_C7_FAMILY_CERTIFICATE.md`](FOURTEEN_VERTEX_C3_C4_C7_FAMILY_CERTIFICATE.md).

The `C3+C3+C8` family has a shorter terminal obstruction.  Of 44,250
eligible singleton factors, exact activation counts eliminate 44,064 by a
one-term forbidden amplitude.  The remaining 186 factors are precisely the
Cartesian product of six bijections between the triangles and 31 internal
matchings of `K8-C8`.  Every one preserves the same `6|8` vertex split, so
every candidate skeleton is disconnected.  Matching-tensor coefficients
then factor across the two components.  Required same-colour coefficients
make both component factors nonzero, while assigning different constant
colours to the components gives a forbidden nonzero coefficient.  The
independent audit returns `"verified": true`.  See
[`FOURTEEN_VERTEX_C3_C3_C8_FAMILY_CERTIFICATE.md`](FOURTEEN_VERTEX_C3_C3_C8_FAMILY_CERTIFICATE.md).

The `C3+C3+C4+C4` family is now closed by an exhaustive hybrid
one-term/transport calculation.  Fixing one of 14 admissible first-factor
orbits leaves 2,911,352 size-three-compatible third-factor choices.
Sound one-term matching filters reduce this to 2,863,992 supports, of
which 996 are disconnected and impossible by tensor factorization.  A
pool of 5,039 direct cancellation certificates induces 21,837 replacement
rules and closes all but 394,068 connected candidates.  Four exact shards
give one stable `C4` two-to-three matching fork for each residual support.
The independent verifier regenerates the factor census and filters, replays
all 394,068 witnesses, and reports zero survivors.  See
[`FOURTEEN_VERTEX_C3_C3_C4_C4_FAMILY_CERTIFICATE.md`](FOURTEEN_VERTEX_C3_C3_C4_C4_FAMILY_CERTIFICATE.md).

The `C4+C5+C5` family is also exhausted by the one-term/fork calculus.
Starting from 44,195 singleton factors, exact one-term tests leave 4,495
and size-three matching forks leave 3,295 factors in 13 orbits.  Across
those representatives only four compatible second factors remain.
The exact size-four and size-five fork catalogues leave no compatible
ordered third factor.  An independent verifier semantically replays all
183,800 forks and regenerates the zero-survivor calculation.  See
[`FOURTEEN_VERTEX_C4_C5_C5_FAMILY_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C5_C5_FAMILY_CERTIFICATE.md).

The all-even `C4+C4+C6` family remains open.  The earlier recursive layer
made 61 of its 93 pinned first-factor orbits finite theorems.  Its global
reconstruction replays 5,800 simple sources, 37 audited fixed-support
proofs, 2,357 minimum-activity certificates, the orbit-2 layer, all 2,576
vertex-connectivity-at-least-three quotient cuts, and the orbit-3 layer.
It matches a 324-variable, 1,094,961-clause CNF exactly.  A single
169,361,294-byte DRAT proof excludes 58 selectors at once; a separate
independently reconstructed proof excludes orbit 5, and recursive
certificate-plus-DRAT chains exclude orbits 6 and 7. Together these cover
orbits
`0--7, 12, 17--21, 23--35, 52--53, 58--62, 64--66, 69--92`.
The remaining 32 are
`8--11, 13--16, 22, 36--51, 54--57, 63, 67--68`. See
[`FOURTEEN_VERTEX_C4_C4_C6_61_ORBITS_KAPPA3_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_61_ORBITS_KAPPA3_CERTIFICATE.md).

The later aggregate minimal-circuit frontier excludes four more selectors,
so 65 of 93 are now closed under the same connectivity-at-least-three
hypothesis.  The remaining 28 are
`8--11, 13--16, 22, 36--41, 44--51, 54--55, 57, 63, 68`; see
[`FOURTEEN_VERTEX_MINIMAL_CIRCUIT_FRONTIERS_CERTIFICATE.md`](FOURTEEN_VERTEX_MINIMAL_CIRCUIT_FRONTIERS_CERTIFICATE.md).

A targeted signed-lattice continuation now excludes orbit 8 as well.
Two exact relation-selection supports contribute 160 freshly replayed
branches.  Three further supports close from mandatory unit relations;
the pinned-factor stabilizer and colour-1/2 symmetry expand those three
certificates into 46 fresh support no-goods.  Conditioning the resulting
1,220,641-clause CNF on selector 240 gives an independently replayed
58,902,708-byte DRAT proof.  Thus 66 of 93 selectors are now excluded and
the 27 outside the certificates are
`9--11, 13--16, 22, 36--41, 44--51, 54--55, 57, 63, 68`.  See
[`FOURTEEN_VERTEX_C4_C4_C6_ORBIT8_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_ORBIT8_CERTIFICATE.md).

Colour symmetry now strengthens that frontier in two exact ways.  First,
each of the 66 excluded factor orbits is impossible in any of the three
singleton-colour roles.  The independently reconstructed augmentation adds
115,500 width-seven factor no-goods and leaves 5,696 allowed factors in the
same 27 orbit classes.  Second, a proved support obstruction transports
under all 1,536 full-factor automorphisms and all six colour permutations;
see
[`COLOUR_SYMMETRIC_FACTOR_ORBIT_TRANSFER_LEMMA.md`](COLOUR_SYMMETRIC_FACTOR_ORBIT_TRANSFER_LEMMA.md)
and
[`FULL_COLOUR_SUPPORT_ORBIT_LEMMA.md`](FULL_COLOUR_SUPPORT_ORBIT_LEMMA.md).

The first bounded full-colour orbit-9 continuation certifies 99 support
orbits in total.  Its support closures add 730,368 fresh width-21 no-goods
to the colour-pruned CNF.  Every clause set is independently reconstructed
before entering the incremental solver; ten batched materializations are
then independently replayed byte-for-byte.  The final 2,066,509-clause CNF
has SHA-256
`113d712f100c3d44705ce801f546c419ead18d1b3ab0780b00d7c68058368fc1`.
A fresh assumption audit still finds all 27 remaining selectors SAT,
including orbit 9.  This is an exact finite null result, not an orbit-9
exclusion and not a proof of the complete family.

The analogous full-colour orbit-16 continuation has now certified 300
supports.  Supports 201--300 alone contribute 834,048 fresh symmetry
no-goods; the current 4,706,893-clause checkpoint has SHA-256
`95db7b12bcd7ead4f9076ff973db1cd9c9957c28d83918ce248b5a65c2b68df7`.
A fresh audit still leaves the same 27 selectors SAT.  A separate
orbit-49 support required all 64 inclusion-minimal relation selections
rather than only the mandatory core.  Every branch was freshly replayed,
yielding 9,216 new full-colour symmetry no-goods and the independently
reconstructed 4,716,109-clause checkpoint with SHA-256
`e9482392e9c6568190ba6a1a4cd6c23025e7c8fd5a17fc5ff0c582cf864adb35`.
That audit also leaves all 27 selectors SAT.  These are certified support
exclusions and exact finite null results; the global conjecture remains
unresolved.  Full artifact details and the continuing orbit-49 frontier
are recorded in [`RESEARCH_NOTES.md`](RESEARCH_NOTES.md).

Orbit 44 is now excluded by a much smaller exact boundary.  Under selector
276, the 4,716,109-clause predecessor has exactly 24 factor assignments.
Their 24 width-21 no-goods occur verbatim in two independently replayed
algebraic support-symmetry clause sets, with memberships 8 and 16.  An
independent byte reconstruction appends only those clauses, producing a
4,716,133-clause CNF with SHA-256
`5bea81cd27ae21111f9466c7088694fd3732e1ecae718f0229ef3e08a934cd2b`.
All 93 selector decisions then leave 26 survivors and exclude orbit 44.
Conditioning on selector 276 gives SHA-256
`d1b390a66aee3d748bd12799850fd3a153df8b45872a33f30c2a8f49072a4739`;
Kissat's 192,160,906-byte proof has SHA-256
`26ec2bbc5100d11a4e8b3cc181189c78643ba1563e68688f67869a7c12ba7c0b`
and passes forward `drat-trim`.  A separate end-to-end replay of the
larger original 6,912-clause extension also passes.  Thus 67 of 93
selectors are now excluded and the 26 outside the certificates are
`9--11, 13--16, 22, 36--41, 45--51, 54--55, 57, 63, 68`.  See
[`FOURTEEN_VERTEX_C4_C4_C6_ORBIT44_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_ORBIT44_CERTIFICATE.md).

The factor-CEGAR transport is substantially less brittle than at the
earlier checkpoint.  Guarded-clause core extraction reduces each of 12
independently verified 48,000--79,000-equation fixed-support proofs to the
same eight-clause, seven-relation contradiction needing only 14 colouring
equations.  Their transported clauses have 9--27 literals instead of
roughly 141--153.  Simple-fork analysis now also searches alternate target
equations and adaptively scores 100,000 bases when the first rule is weak;
on the development witness this reduced the activation footprint from 18
edge conditions to 6.  These are finite, independently checked advances,
not yet a `C4+C4+C6` theorem.

The orbit-2, orbit-3, orbit-5, orbit-6, and orbit-7 targeted layers remain separately
replayable.  A four-clause dual-Horn/lattice verifier also gives a second
exact obstruction for one orbit-3 support.  The 61-orbit frontier is a
finite theorem, not a proof of the complete `C4+C4+C6` family.

The earlier two-support orbit-8 development remains documented in
[`FOURTEEN_VERTEX_C4_C4_C6_ORBIT8_PARTIAL_BINOMIAL_SUPPORT_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_ORBIT8_PARTIAL_BINOMIAL_SUPPORT_CERTIFICATE.md);
it is now a predecessor of the complete conditional orbit certificate,
not the active boundary.

The six-vertex pattern layer has also been simplified.  A fresh exhaustive
run gives 145 primitive Laurent units and one rational linear-monomial unit,
with zero Singular fallbacks; Glucose independently replayed all 146 cubes.
The top-level six-vertex audit now uses this stronger chain while retaining
the same final CNF and independently checked DRAT proof.
