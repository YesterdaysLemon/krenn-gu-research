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
- more sharply, any nonzero decomposable restriction of the order-four
  permanent tensor through rank-at-least-two local maps has rank two in
  at least two modes.  The two rare `q5_311` deletions therefore force
  either one shared rank-drop mode with three common source rows on a
  line, or disjoint `2+2` rank-drop sets partitioning the four modes.
- the shared rank-drop case is impossible: contracting both rare slices
  along their exceptional rows exposes the same residual `P_3`, but
  forces it into two independent target-colour pure lines.  Hence only
  the disjoint `2+2` partition remains.
- the disjoint `2+2` case is impossible as well: its four common-row
  `P_3` contractions obey an all-zero/all-pure plane theorem, and both
  alternatives contradict nonvanishing of the rare slices.  Therefore
  the complete normalized `q5_311` branch is excluded over `C`.
- this rank-two boundary is sharp: an exact five-parameter family with
  all four local maps of rank two sends `P_4` to a nonzero pure tensor.
  Consequently the two rare deletions must be coupled; neither can be
  excluded in isolation.
- the closure of that family is a generically smooth
  five-dimensional irreducible component of the pure rank-two
  compression locus.  An exact incidence Jacobian has rank 15 in 20
  variables, while the family tangent map has rank five.  This
  identifies a component but does not classify other components or its
  all-rank-two boundary.
- a second five-dimensional pure rank-two component now exists.
  Viewing `P_4` as the Frobenius form of the squarefree complete
  intersection turns exceptional plane pairs into annihilator lines on
  diagonal quadrics.  A radical-plane normal form is governed by an
  irreducible `(3,3)` hypersurface in `P^2 x P^2`; an exact quadratic
  tangent-cone certificate proves component status.  A
  diagonal-quadric jump invariant separates it from every symmetry
  translate of the first component.
- the diagonal-quadric map has now exposed three further
  five-dimensional components.  On the `1+3` radical-plane stratum,
  the remaining pure condition is the split cubic
  `(D-G-S+T)(D+G-S-T)(D+G+S+T)`.  Exact smooth incidence
  certificates prove that all three factors give components.  Their
  generic `(2+2,1+3)` jump signatures are `(1,1),(0,2),(0,1)`,
  distinct from the earlier signatures `(2,1),(1,0)`.  Thus at least
  five symmetry-inequivalent pure rank-two components exist; this is
  not yet an exhaustive classification.
- the apparent common-smooth-quadric continuation does not create a
  sixth component.  After normalizing the quadric, its four annihilator
  lines have only the spinor ruling patterns `LLLL`, `LLLR`, and
  `LLRR`.  Exact characteristic-zero saturation proves that `LLLL`
  has no nonzero pure restriction and that the other two pure loci are
  only one-dimensional before restoring the diagonal source torus.
  More sharply, every mixed-ruling solution has a block annihilator
  line.  Hence a component-sized continuation must use the `2+2` or
  `1+3` jump geometry already exposed by the diagonal-quadric map.
- the generic directed radical-star stratum is now classified, not
  merely sampled.  A rank-one exceptional relation is a zero product
  in the squarefree complete intersection and therefore lives on a
  source-coordinate pair.  Two such relations pointing away from a
  common mode force either a `2+2` or `1+3` radical plane.  Dense
  normal forms then recover exactly the irreducible second component
  in the `2+2` case and the three split-cubic components in the `1+3`
  case.  No additional component occurs on this stratum; mixed edge
  orientations, triangle geometry, and lower pair-rank boundaries
  remain.
- the exact rank-two pair-image boundary now has a computation-free
  pencil classification.  Its projective kernel is a line in the
  `2 x 2` Segre quadric ambient space.  The line cannot be a Segre
  ruling because every nonzero degree-one element of the squarefree
  algebra has annihilator dimension at most one.  A secant kernel
  forces the existing `2+2` or `1+3` block centers; a tangent kernel
  forces coincident planes through one coordinate line (and the
  transverse generator must use at least two other coordinates).
  Thus a single rank-two exceptional pair has no third kernel type,
  although compatibility of several such pencils and the exceptional
  triangle remain open:
  [`P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md`](P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md).
- the all-rank-two-relation triangle now has an intrinsic symbolic
  holonomy.  Off the trivial-holonomy divisor, three Borel row shifts
  remove the constant relation terms, all six mixed triple products
  vanish, and each cross-product has the opposite local plane as its
  full degree-one annihilator.  Its symmetric zero-diagonal
  catalecticant has rank two, so it is a weighted cut: `1+3` or
  `2+2`, with the latter governed by one tetrad.  This reduces the
  nonresonant triangle to cyclic cut compatibility:
  [`P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md`](P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md).
- the full-support all-`1+3` part of that cyclic problem is now empty.
  A triangle cut has only an internal factorization or a fully
  supported sign-reflection factorization.  Since every opposite
  annihilator plane lies in a coordinate hyperplane, only the internal
  sheet is possible.  The three singleton labels must coincide;
  otherwise the planes collapse into a coordinate two-plane.  With a
  common label the restriction is an embedded pure `P_3`, whose perfect
  pairing forces all three alleged rank-three pair images to have rank
  at most two.  Thus no new component occurs there; `2+2` cycles,
  proper cut-support boundaries, and the resonant divisor remained at
  that checkpoint:
  [`P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md).
- every full-support `2+2` bridge is now impossible as well.  Writing
  it as `q=ab` across two binary blocks, every factorization of `q`
  contains the anchor `a` or `b`.  Its annihilator is
  `span(a_bar,b_bar)`, but every plane with a rank-three product and a
  unique rank-two relation against that annihilator is a crossed graph
  `span(alpha*a+tau*b_bar,-tau*a_bar+beta*b)` with `tau!=0`; such a
  plane contains neither anchor.  The bridge therefore cannot factor.
  Combining both cut theorems empties the full-support nonresonant
  triangle.  At that checkpoint, proper cut-support boundaries and
  the resonant holonomy divisor remained:
  [`P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md).
- the proper cut-support boundary is now empty too.  Every nonzero
  proper cut is either one edge or a two-edge star.  A one-edge
  annihilator forces every rank-two-relation partner into the same
  coordinate plane, making the product rank at most one.  A two-edge
  star and both its partners lie in one coordinate hyperplane, turning
  the restriction into an embedded `P_3`; perfect pairing makes every
  alleged rank-three pair have rank at most two.  Consequently the
  complete nonresonant all-rank-two-relation triangle is empty.  Only
  the trivial-holonomy resonant divisor remains:
  [`P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md).
- the resonant divisor is now an affine-holonomy problem.  After
  normalizing projective transport, the relations are
  `A_ij*y_i*y_j+y_i*x_j-x_i*y_j=0` and the residual gauge invariant is
  `delta=A_12+A_23-A_13`.  If `delta!=0`, all kernel-rich triple
  products vanish and the three one-kernel products coincide, giving
  a tangent-Segre first jet; the three kernel-pair products are
  rank-two cuts.  If `delta=0`, all triple products depend only on
  Hamming weight and factor through `Sym^3(C^2) -> R_3`, with its
  first three coefficients compressed to a plane.  These two small
  incidences, not the original plane equations, are the remaining
  triangle frontier:
  [`P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md`](P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md).
- the nonzero additive-holonomy branch is empty.  Its tangent-Segre
  first jet makes the three kernel-pair products into nonzero
  rank-two cuts with the opposite planes as annihilators.  Proper
  supports descend to a rank-deficient partner; a full `2+2` cut
  contradicts the anchor/crossed-graph lemma; and three full `1+3`
  cuts force a common coordinate hyperplane and hence an embedded
  pure `P_3`, where perfect pairing makes every pair image have rank
  at most two.  The triangle frontier is therefore reduced to the
  flat synchronized binary cubic `Omega=delta=0`:
  [`P4_RESONANT_NONZERO_ADDITIVE_HOLONOMY_OBSTRUCTION.md`](P4_RESONANT_NONZERO_ADDITIVE_HOLONOMY_OBSTRUCTION.md).
- the flat synchronized binary cubic is now classified completely.
  A generic row-pair is a four-point configuration on `P^1`;
  synchronization turns its partners into an adjugate pencil, and a
  third-compound factorization contradicts the purity flag.  On the
  collision boundary, zero columns descend to pure `P_3`, `2+1+1`
  collisions kill the active cube, and `1+3` collisions drop the pair
  rank.  The sole survivor is the balanced `2+2` family
  `U0=<a_bar,b_bar>, U1=<a,b>, U2=<a,b+s*a_bar>,
  U3=<a,b+t*a_bar>` with pure coefficient `-4(s+t)`.  Its plane locus
  has dimension at most four, below the five-dimensional minimum for
  a nonzero pure-incidence component.  Thus the complete
  all-rank-two-relation triangle cannot be the generic graph of a new
  component:
  [`P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md`](P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md),
  [`P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION.md`](P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION.md).
- a star of three rank-two exceptional relations is impossible too.
  Tree gauge synchronizes all three leaves with the center.  For a
  generic four-point center the leaves lie on its adjugate pencil,
  whose pair-rank-drop graph is a matching of three disjoint edges;
  two leaves therefore close a forbidden generic triangle.  Zero,
  `2+1+1`, and `1+3` center collisions respectively give a zero
  restriction, a zero active cube, or pair rank at most two.  On the
  remaining balanced `2+2` collision, one forbidden coefficient is
  the constant `4`.  Hence an all-pair-rank-at-least-three missing
  component must use a rank-one relation or a genuinely mixed
  rank-one/rank-two selection:
  [`P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md`](P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md).
- a rank-three exceptional triangle cannot have relation-rank pattern
  `(2,2,1)`.  Gauge the two rank-two edges into a synchronization
  `V`.  Generic and `2+1+1` centers automatically synchronize the
  leaves with each other, contradicting the rank-one third relation.
  The balanced `2+2` center reduces the issue to the degree-one
  annihilator of a leaf kernel: it is either zero or the line
  `C*a_bar`, and the other leaf never contains that line.  Thus a
  remaining generic mixed triangle has at most one rank-two edge:
  [`P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md`](P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md).
- a mixed zero-product orientation produces a sixth
  symmetry-inequivalent component.  The normalized rank-two
  contraction condition is a `3 x 4` determinantal problem whose
  radical splits into five linear primes.  One prime gives the explicit
  pure family
  `T_0000=2q(d+p+q)`; its diagonal-torus orbit has a rank-five family
  tangent and a smooth rank-fifteen incidence certificate.  Although
  its coarse jump signature `(0,1)` matches `L_3`, its three rank-one
  exceptional relations have sorted pure-kernel endpoint indegrees
  `(2,1,0,0)`, rather than `(1,1,1,0)`.  Thus at least six component
  orbits exist.
- the mixed-orientation component's complete marked `H31` fibre is
  empty at its generic point.  Function-field projection leaves four
  rational marking sheets across distinguished coordinates two and
  three; every extension on those sheets has an exact all-extension
  determinant proportional to the two required binary diagonals, and
  two pure transverse entries are nonzero.  Its special parameter and
  projective boundaries remain open.
- one lower-pair-rank determinantal prime is not another isolated
  fivefold: it lies inside a generically smooth rational
  six-dimensional component.  In apolar coordinates its only
  coefficients are
  `T_1010=2(1-b(a+c))` and `T_1110=2(1-e(a+c))`.
  The diagonal-source family tangent has rank six and the
  Segre-incidence Jacobian has rank fourteen.  Its generic pair profile
  is `(4,3,2,4,4,3)`, placing it on the rank-two-edge boundary omitted
  by the radical-star classification.  Dimension separates it from
  the six known fivefolds, raising the certified lower bound to seven
  component orbits.
- the six-dimensional component's generic marked `H31` fibre is empty
  as well.  The apolar change
  `s=a+c,u=1-sb,v=1-se` reduces the problem to four parameters.
  Distinguished coordinate one has only the pure reconstruction
  kernel and no binary neighbour; each other coordinate has one
  rational marking, excluded by a three-minor Fitting certificate.
  The new component's special parameter/projective boundary remains
  open.
- the same component now has the first orbit-generic `H22`
  obstruction.  Restoring the missing source-torus slope is essential:
  the weighted `01` diagonal has unit binary projection, while the
  weighted `23` diagonal has one rational marking pencil and a
  two-dimensional extension kernel.  One kernel line has both
  diagonals zero; every genuine direction is excluded from a ternary
  lift by the mode-zero `0127/0137` Fitting ideal.  The equal-weight
  calculation survives as a useful exceptional boundary certificate,
  but the generic theorem uses the full weighted pencil.  Its slope and
  parameter divisors and the rest of `H22` remain open.
- the mixed-orientation fivefold now has a generic weighted `H22`
  obstruction as well.  For the weighted `01` pencil, a hierarchical
  projective-kernel cover proves that the `14 x 8` mixed matrix has
  full column rank at every marking.  The weighted `23` projection is
  contained in three explicit marking closures; on each, saturation
  by the two required diagonals and two mode-three minors gives the
  unit ideal.  Thus every genuine binary survivor has marked rank four.
  Its parameter/slope divisors and projective boundary remain open;
  the other known component orbits are tracked separately below.
- the three split-cubic `1+3` components are now generically excluded
  from weighted `H22`.  All three weighted `01` projections are unit,
  and `L_3` is unit in the `23` direction as well.  The remaining
  `L_1` projection consists of two rational sheets, while `L_2` is
  covered by three affine lines.  On all five survivor closures, the
  same mode-zero `0247` marked minor gives a saturated unit ideal.
  Generic weighted `H22` incidence is therefore empty on five of the
  seven certified component orbits; their boundaries remain, and the
  two earlier rank-two components are tracked below.
- the first rank-two component is now generically excluded from
  weighted `H22`.  Its `01` mixed matrix is everywhere injective by an
  eight-chart projective-kernel cover.  Its exact `23` projection has
  two sheets, killed respectively by the mode-two `0147` and `0137`
  marked minors.  Six of seven certified component orbits are now
  generically closed at this checkpoint.
- the diagonal-quadric component is now generically excluded from
  weighted `H22` as well.  In fixed binary coordinates, its extension
  image is an eight-plane and every marked binary target lies in the
  join of a Segre fourfold with its all-beta point.  At one exact
  rational interior fibre, fifteen Segre charts are unit; the last is
  only the zero-vector base point, and its blow-up exceptional
  five-space is linearly disjoint from the extension plane.  Properness
  transports this empty projective fibre to the generic point.  Thus
  all seven certified component orbits are generically closed, while
  component exhaustiveness and special parameter/slope divisors remain:
  [`P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md).
- a disjoint-support mixed star supplies an eighth certified
  pure-`P_4` component orbit.  Normalize its three rank-one
  zero-product supports to `{01,01,23}`.  The pure condition is the
  irreducible hypersurface
  `a^2*b*f*phi^2+a^2*f^2-b^2*f^2+b^2*phi^2-b*f-1=0`;
  its diagonal-source family tangent has rank five and the universal
  Segre-incidence Jacobian has rank fifteen.  Support disjointness
  separates it from the overlapping mixed component:
  [`P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`](P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md).
  Its generic marked `H31` fibre is now empty.  Exact function-field
  projection leaves no genuine marking for source coordinates zero
  and one and one marking each for coordinates two and three; on both
  survivors a mode-zero minor is
  `+/-f*(b*f+1)*(1-a^2*f^2)/(a^2*f+b)*A*B^2`, so every genuine binary
  extension has rank four:
  [`P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).
  Its generic weighted `H22` incidence is now empty as well.  Passing
  first to the Fitting rank locus turns `D_23^r` into the marking line
  `t_1=t_2=t_3=0` and `D_01^r` into an exact degree-five scheme over
  the component field.  The relation `t_1*t_2=0`, two further factored
  cover relations, and one- or two-minor ternary obstructions close all
  five markings:
  [`P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).
  The equal- and opposite-weight slope divisors are now closed more
  strongly at the binary level: at `r=1` the mixed kernel forces the
  first diagonal to vanish, while at `r=-1` it forces the second:
  [`P5_H22_DISJOINT_MIXED_STAR_EQUAL_OPPOSITE_WEIGHT_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_EQUAL_OPPOSITE_WEIGHT_OBSTRUCTION.md).
  Factoring the component equation closes twelve further generic
  parameter/coordinate branches with twenty-four exact Fitting ideals:
  [`P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md).
  The remaining visible coupled coefficient in the degree-five cover
  is also closed; its `D_01` obstruction moves to mode one while its
  `D_23` obstruction stays in mode zero:
  [`P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md).
- an embedded pure-`P_3` suspension supplies a ninth certified
  pure-`P_4` component orbit.  Three local planes lie in one
  source-coordinate hyperplane and form one of the exact pure-`P_3`
  sign charts; the fourth plane freely supplies the missing
  coordinate.  The six-parameter family has only
  `T_0010=-2/B,T_0110=-2A/B`.  Its family tangent has rank six and a
  `14 x 14` Segre-incidence minor is `114688/2187`, proving component
  status.  Its generic pair profile `(4,4,4,2,2,2)` separates it from
  the previous six-dimensional component and all seven fivefolds:
  [`P4_EMBEDDED_P3_PURE_COMPONENT.md`](P4_EMBEDDED_P3_PURE_COMPONENT.md).
  Its generic marked `H31` fibre is empty already at the binary level.
  The embedded `P_3` turns source-coordinate-zero extension into a
  six-column apolar insertion map.  Its rank-drop support is exactly
  three signed projective lines plus three coordinate points; on a
  generic projected mode-zero line, every possible kernel kills the
  required all-alpha diagonal:
  [`P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md).
  The generic weighted `H22` fibre is empty at binary level too:
  `D_23^r` has a structural zero diagonal, while `D_01^r` is the same
  insertion arrangement on a slope-dependent projective line:
  [`P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md).
  The nine exceptional `H31` insertion points are now closed on the
  entire normalized affine chart.  Exact truncated-Segre relations
  leave five binary survivor families; four fail small one-marked
  covers, while the deepest rank-three point fails a constant stacked
  determinant `8`:
  [`P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md).
  The weighted `H22` boundary is now closed whenever its projected
  mode-zero image is still a line.  Four arrangement strata leave six
  binary marked families; factored one-marked covers exclude them,
  with constant stacked determinants `8` and `-8` at the two deepest
  rank-three points:
  [`P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md`](P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md).
  The rank-one projection collapse is now empty at binary compatibility
  too.  The other required marked slice becomes an insertion pencil
  with singular fibres only at `S=+/-1`; their kernels kill,
  respectively, its pure diagonal and the first slice's alpha
  diagonal:
  [`P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md`](P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md).
  Thus its full normalized weighted `H22` chart is closed; the omitted
  normalization/projective boundary remains open.
- all five minimal primes in the mixed `3 x 4` determinantal chart are
  now identified.  Two are the sixth component, one is a subfamily of
  the six-dimensional component, and the remaining two are explicit
  source/mode symmetry charts of `L_2` and `L_1`.  Thus this dense
  mixed zero-product chart produces no further component within that
  chart; the disjoint-support eighth component lies outside it.
- the complete marked `H31` fibre over the generic point of each of
  those three new components is empty.  Function-field projection
  leaves no binary `Delta_2` neighbour on one component and only two
  rational marking families on the other two.  On every survivor, a
  one-marked determinant is exactly `A^2 B` divided by a nonzero
  parameter factor, where `A,B` are the two required binary diagonals.
  The parameter divisors and projective boundaries remain open.
- a restriction of `P_3` to three rank-at-least-two source subspaces is
  zero exactly when all three subspaces are the same coordinate plane.
- every nonzero decomposable `P_3` restriction through
  rank-at-least-two maps has rank profile `222` and belongs to six
  explicit two-parameter projective sign charts.
- in normalized `q5_221`, the three target-colour contractions are
  embedded copies of `P_4` on hyperplanes with independent normals.
  Their rank drops give nine singleton-marked minimal incidence types
  over six uncoloured three-edge multigraphs.
- if the two multiplicity-two colours in normalized `q5_221` have the
  same exact two-mode rank-drop set, the cross-contraction pencil gives
  incompatible `P_3` normal supports.  The drop sets therefore cannot
  coincide, excluding three exact marked incidence boundaries.
- the exact singleton-doubled double-plus-adjacent `q5_221` type is
  impossible as well.  Its all-normal mode fixes a support-two `P_3`
  sign pair, and both possible signs at the doubled endpoint contradict
  a second cross residual.
- the singleton-doubled double-plus-disjoint exact type is impossible.
  Its residual sign chart, `AB|CD` complement pairing, a nondegenerate
  `P_2` contraction, and a final forbidden `P_3` rank profile reduce
  the only surviving planes to a contradiction.
- the complete exact triangle incidence type in normalized `q5_221` is
  impossible.  One chirality closes by full-support normal transport;
  in the other, the only rank-one gates land in the wrong target
  colours.  Both force `Q_01=Q_10=0`, contradicting their local
  cross-scalar alternative.  The same proof also excludes both marked
  exact seven-incidence extensions obtained by adding one normal at the
  fourth mode.
- the exact `q5_221` star type is impossible.  Its all-normal centre
  turns the cross scalars into an invertible zero-diagonal matrix and
  forces a directed residual cycle.  Either cycle makes a mixed
  coefficient of the colour-two `P_4` slice nonzero.
- both exact marked `q5_221` path types are impossible.  The marked-end
  proof couples the cross-residual rank-one gates to two forced
  permanent coefficients.  The marked-middle proof recasts residual
  normals as intersections of two-dimensional kernels with residual
  three-spaces and obtains a sign-rectangle incidence contradiction.
  All nine exact minimal marked incidence types are therefore closed.
  The later monotone theorems below close their extra-containment
  strata.
- exact seven-incidence cover `#8` is impossible.  Two simultaneous
  cross-contraction channels first force three residual rank-one gates;
  their multilinear normal form makes one forbidden `T_0` coefficient
  force `f=0`, while the required pure `T_2` coefficient is a nonzero
  scalar times `f`.  This is symbolic invariant theory, not a map
  search, and it does not yet close the monotone boundary of the cover.
- the distinguished normal in normalized `q5_221` occurs in exactly
  two modes.  A double apolar contraction and one nonzero `Q_12`
  residual rule out three incidences without any absence assumptions.
  This closes six of the fourteen seven-incidence covers monotonically.
- exact cover `#13`, the final untreated no-fixed-kernel stratum, is
  impossible.  Its support-two `P_3` chart kills the required `T_2`
  coefficient through `Perm_2(h_1,u_1)=0`; its full-support chart is
  excluded by a four-corner apolar rectangle identity.
- monotone cover `#5` is impossible.  Its two all-normal modes leave
  three rank-one bilinear equations through the other two modes.
  Colouring the three forced dependency edges by two endpoints makes
  one endpoint have rank at most two, contradicting its rank three.
- monotone covers `#6,#11` are impossible.  The nontrivial orientation
  of their all-normal mode forces the directed residual cycle
  `Q_20,Q_01,Q_12`; its rank-one and rank-two partner strata both make
  two differently coloured residuals share one local factor line.
- the remaining fixed-kernel covers `#7,#10` and the two exceptional
  eighth-incidence no-fixed-kernel boundaries are impossible.  Hence
  the complete normalized `q5_221` branch is excluded over `C`.
- normalized `q4_211` is a simultaneous tensor-pencil problem.  Its
  four remaining maps would have to send a three-plane of contractions
  isomorphically to the diagonal tensor three-plane, forcing the
  associated `78 x 5` off-diagonal contraction matrix to have rank at
  most two.
- the known positive support-four construction cannot supply those
  four maps.  Its off-diagonal matrix has rank four and a
  one-dimensional kernel, and exact two-variable elimination proves
  rank four at every point of its published two-parameter family.
- on `bc != 0`, the parallel singleton-normal incidence type always
  acquires a third common mode.  A diagonal matrix-pencil lemma handles
  the zero residual, while a quotient of an embedded `P_4` excludes
  the only apparent nonzero-residual kernel boundary.
- at a common-normal mode on `bc != 0`, the two cross residuals form an
  order-four permanent pencil.  One nonzero cross scalar forces a new
  normal `(0,0,0,c,b)` at another mode; two nonzero scalars give a
  marked sharp restriction `P_4 -> Delta_2`.
- the marked `P_4 -> Delta_2` boundary has an exact two-slice
  classification.  Its all-rank-two family is incompatible with the
  adjacent `h_1,h_2` incidences because a `2|2` complement-pairing
  flattening has rank at least four.  Every rank-one slice has exactly
  two alternating gates and one of two determinant normal forms.  The
  transverse lift contradicts the triple-`n` contraction; the tangent
  lift contradicts a double-`n` decomposable-`P_3` sign chart.  Thus
  the full two-cross marked boundary is empty, and only the separate
  one-cross fourth-normal incidence remains adjacent.  In that last
  branch `n` pulls back only from target colour zero, a zero/pure pair
  of `P_3` residuals forces one whole opposite normal pencil into a
  remaining row space, and a polarized binary cubic confines the
  other pencil to the three lines `h_2,n,u_1` or `h_1,n,u_2`, modulo
  explicit double-normal and common-kernel gates.  The same branch
  exposes a nondegenerate direction conic: its two direction lines are
  forced to `{u_2,c u_1-bu_2}` or `{u_1,c u_1-bu_2}`.  Compatibility
  with the binary cubic removes the free polar core.  A second-common
  mode is impossible and every double-normal gate is absorbed, leaving
  only a full direction plane or a common `e_1+e_2` kernel.  The
  direction-plane gate has the wrong target colour in a repeated
  `P_3` contraction.  Binary polarity propagates the common-kernel gate
  to the pattern `A:s,Y:d,D:s`; the nonzero `P_3(w_-)` and zero
  `P_3(w_+)` charts then force `L_C(s)` simultaneously to have and not
  have a target-colour-zero component.  Thus adjacent one-cross
  incidence is empty on `abc != 0`.
- on `abc != 0`, the exact disjoint type is a conic-polarity problem.
  All four maps have rank two on one ternary quadratic support, and the
  resulting `K_(2,2)` polarity equations force one normal pair to share
  the kernel `span(e_1+e_2)`.  Repeated-normal contractions propagate
  the kernel and leave only `(s,s,s,s)` or `(s,s,d,s)`; the former kills
  the doubled-colour-zero coefficient and the latter forces
  incompatible `h_2,n` target colours.  Thus exact disjoint incidence
  is excluded.
- parallel incidence reselects as adjacent, so the preceding adjacent
  and disjoint theorems exhaust every pair of singleton-normal
  containment sets.  Therefore normalized `q4_211` is excluded over
  `C` on the open stratum `abc != 0`.
- the three `q4_211` parameter faces are excluded as well.  The
  `b=0,c=0` faces reduce to coordinate-normal polar systems.  On
  `a=0`, adjacent incidence is a complete-quadrangle degeneracy locus
  in `Gr(2,4)`, while exact disjoint incidence reduces to a ternary
  `P_3` sign obstruction.  The zero-row closure is excluded by the
  two-singleton theorem.  Hence the complete partial `q4_211` branch is
  excluded over `C`.
- the `q5_311` argument actually proves a stronger two-singleton
  theorem: any local map with two target coordinates supported on two
  distinct singleton source rows is impossible.  This also excludes
  the zero-row `q4_211` closure and one partial `3+1` family.
- the earlier claim that `q4_211,q5_311,q5_221` exhaust the
  high-coordinate branch was false.  The exact 6,495-signature census
  has 1,680 high-coordinate signatures; current theorems exclude
  1,170.  The remaining 510 form two partial-row families `H31` and
  `H22`, coupling one pure `P_4` deletion to one or two sharp
  `P_4 -> Delta_2` deletions.  This is the current `P_5` frontier, not
  a proof or counterexample.
- the complete marked-basis fibre over every finite member of the
  five-parameter all-rank-two family is now classified and excluded
  from `H31`.  Kernel-row shifts genuinely change the neighbouring
  `Delta_2` equations: a dense shifted branch has a binary extension,
  and three isolated `q=1` markings occur on `C=-L/2`.  Exact
  all-extension marked-minor covers exclude every survivor ternarily.
  This statement concerns the first component; its projective
  boundary is handled by the subsequent complete-fibre theorems.
- the exact closure of each known component inside its preferred
  Grassmann chart has one additional nonzero boundary divisor.  The
  canonical marked section of that divisor is impossible in all four
  orientations.  The toric plane boundary has 12 divisors, 26 edges,
  and 16 vertices; exact Segre intersection leaves only 21 all-rank
  plane/orientation pairs.  Their complete marked-basis fibres are now
  excluded: 17 pure-direction types, both first-plane charts, all row
  shifts, and all binary extension directions reduce to selected
  marked-minor unit ideals.
- the nonzero divisor outside the finite five-parameter family but
  inside the preferred component chart is now excluded at complete
  marked-fibre level.  An exact source action reduces its full bundle
  to four shifts; four saturated projection ideals and 16
  all-extension residual-factor strata exclude every orientation.
- the first-plane Schubert line at infinity is now excluded at complete
  marked-fibre level.  Its four saturated projection closures have 21
  minimal components; a 25-chart characteristic-zero residual cover
  excludes every row shift and binary extension direction.
- the internal `E=0` divisor is now excluded at complete marked-fibre
  level as well.  Its two Segre directions, three all-rank
  orientations, and both first-plane charts reduce to 24 projection
  components and a 29-chart exact residual atlas.  Consequently the
  full marked fibre of the known pure-compression component is closed.
- every `H31` pure/`Delta_2` pencil with a rank-one pair on the pure
  hyperplane is impossible.  The rank-two common-plane branch reduces
  to four projective line strata; the remaining secondary-gate branch
  becomes a `P_3 -> Delta_2` pair-image polarity with only two support
  types.  Transverse one-marked kernels and deepest mixed-colour
  coefficients exclude all of them.
- at one rational point of the second diagonal-quadric component, the
  complete marked fibre is excluded.  Exact binary projection leaves
  no marking for `q=1,2` and one marking for each of `q=0,3`; every
  extension in the two survivor kernels has injective marked minor
  `-8u(u-2v)^2`.
- more strongly, every marked fibre on the nonzero rational curve
  `A=B=E=F=H=1, C=c!=-1` in that component is excluded.  Exact
  relative projection over `Q[c]`, saturated by `c+1`, proves that
  `c=0,1` are the only jump fibres.  Their kernels and the
  function-field kernels reduce every genuine binary extension to a
  factored nonzero one-marked minor.  The `H31` remainder is therefore
  the complement and boundary of that curve in the second component,
  plus any still further pure-`P_4` components.
- a transverse rational curve `A=B=F=H=1,C=0,E=e` is excluded for
  every `e in C` as well.  It contains the former isolated point at
  `e=2` and meets the first curve at `e=1,c=0`.  Its exact relative
  projection has only the jumps `e=0,+/-1`, all closed by binary-
  diagonal factorizations of selected marked minors.  Thus the
  second-component remainder is more precisely the complement and
  boundary of these two curves.
- the pure-factor-direction curve `C=-1,E=e` is excluded too.  On the
  common slice `A=B=F=H=1`, the component equation is exactly
  `C(C+1)(1-E^2)=0`; the fourth branch `E=-1` is source-symmetric to
  the closed `E=1` branch.  Therefore every nonzero marked fibre on
  this complete factored slice and its full source/mode symmetry orbit
  is excluded from `H31`.  That orbit includes the transverse
  `A=B=C=E=F=1,H=h` line.
- a second complete slice is closed in the component interior.  On
  `A=B=F=1,H=0`, the equation is `(CE-1)(CE+1)=0`; exact relative
  projection excludes the `CE=1` ruling, and `X_0<->X_3` exchanges it
  with `CE=-1`.  Hence every nonzero marked fibre on this slice and
  its source/mode orbit is excluded.
- generically, the second component is excluded as well.  On
  `A=B=F=1`, its six-term equation is the rank-one conic bundle
  `S^2=UT`.  A birational change of variables gives the elliptic
  surface
  `Y^2=x((1-r^2)x^2+(3r^2-2)x+(r^2-1)^2)`.
  Exact saturated projection over its function field returns the unit
  ideal for all four distinguished coordinates and every marking.
  Thus the binary-survivor projection is a proper closed subset of the
  second component.  The minimal resolution is an elliptic K3 with
  fibres `I4+2I6+2I1+I0*`; Shioda--Tate and the non-torsion `H=0`
  section give Picard number 20 and Mordell--Weil group
  `Z + Z/2`.  For the middle distinguished coordinates, quotienting a
  universal mixed-kernel line and factoring bordered minors proves that
  a dense rank-drop chart contains no new survivor curve: it collapses
  to the closed `H=0`, pure-direction, or singular-fibre loci.  The
  end-coordinate quotient is also full rank off the two explicit
  marking divisors `t2=x,t3=1`.  On their deepest intersection for both
  `q=0,3`, compatibility cuts out a conjugate pair of smooth genus-two
  residual trisections; each unique candidate marking is excluded by
  two coprime full-rank minors.  Pulling the whole `t2=x` divisor back
  to the same genus-two normalization closes it for both endpoints by
  a univariate resultant and one final quadratic-exception minor.  On
  `t3=1`, the apparent marking cover splits over the elliptic function
  field.  Its two branches are forced onto that same genus-two curve;
  univariate gcds and exact binary-diagonal ranks at the finite
  exceptions close both sheets.  Thus every regular end-coordinate
  marking is excluded.  For the middle coordinates, a second
  Fitting-ideal cover closes all three missing pivot divisors and the
  regular `Y=0` two-torsion slice.  Therefore every marked fibre in the
  regular elliptic chart is excluded for all four distinguished
  coordinates.  The inverse-map boundary reduces to the closed
  `H=+/-1` and base-locus strata plus two rational `r=0` curves.
  Relative marked-fibre projection and a uniform marked minor close both
  curves, including their projective endpoints.  Thus the complete
  normalized affine slice `A=B=F=1` is excluded.  The outer
  projective/gauge boundary `A B F=0` is now closed too.  Its seven
  coordinate surfaces reduce under a diagonal-source torus and one
  source/mode involution to four rational curves, while `B=0` leaves
  one rational conic.  Exact relative projections classify every
  binary survivor.  Factored one-marked minors exclude all but one
  deepest edge direction, and there a stacked `5 x 5` minor is
  `128p`.  Therefore the complete marked fibre of the second known
  pure-compression component is empty.
- for any five selected vertices, their ten pairwise bilinear
  zero-coupling equations have a simultaneous projective solution over
  `C`; the intersection number is 24.  The solution is not yet
  guaranteed to avoid the 15 coordinate hyperplanes.
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
- the complete exact-three-partial layer is impossible over `C`.
  Independent fixed-shape regenerations reduce the two halves to 5,993
  `C4+C6` and 11,751 `C10` support-semantic survivor orbits.  Exact
  characteristic-zero support-only calculations return the unit ideal
  for all 17,744 systems.  Thus any remaining exact-three-coordinate
  model has at least four partial non-coordinate cells.
- in fact, the entire exact-three-coordinate branch is impossible over
  `C`, with no bound on the number of partial cells.  A deletion-stable
  spanning-tree chart cover reduces all lower supports to 812 exact
  rational unit-ideal certificates across 200 viable coordinate
  backbones.  Two global CNFs are UNSAT under CaDiCaL and Glucose, and
  both Kissat DRAT traces are independently accepted by `drat-trim`.
  Therefore any hypothetical `P_5 -> Delta_3` restriction has a local
  map with at least four coordinate rows.
- one of those `C10` orbits already has a ten-mixed-coefficient affine
  contradiction, needing neither the saturation equation nor a pure
  nonzero assumption.  Its 15-member coarse motif class splits into 11
  affine unit ideals and four affine non-unit ideals, so the proof
  template requires a finer monomial-incidence invariant.
- a three-equation binary-fork identity `P+Q-mR=2` gives an exact affine
  contradiction in 1,328 of the 11,751 `C10` orbits.  Every hit is
  independently regenerated and symbolically replayed; the rule uses
  neither saturation nor pure-amplitude nonzero assumptions.
- a four-equation triangle identity `2P-mX-mY+mZ=2` adds 113 new `C10`
  orbits beyond the fork.  The two sparse rules exclude 1,441 orbits in
  union and leave 10,310 undecided by these templates.
- a five-edge odd-cycle identity adds 74 more `C10` orbits.  The three
  sparse rules exclude 1,515 orbits in union and leave 10,236
  undecided by these templates.
- rational scalar-span identities `sum(q_i F_i)=1` are certified in at
  least 1,523 `C10` orbits and add 175 beyond the three named rules.
  The combined certificates exclude 1,690 orbits and leave 10,061 not
  covered by these searches.
- degree-one Macaulay identities
  `sum((a_i+sum_j b_ij*u_j)F_i)=1` add 1,960 exact rational
  obstructions.  The certified union excludes 3,650 `C10` orbits and
  leaves 8,101 not explained by these small certificate layers; the
  full saturated calculation excludes them too.
- every fully supported zero-coupled root pair requires at least five
  distinct outside blockers across the three colours.
- for every rank-at-least-two root edge, five fixed outside
  vertex--colour pairs have blocker determinants that are scalar
  multiples of the root-edge equation; a rank-three root edge therefore
  forces five exact zero-or-compression alternatives, at least three
  compressions at the same endpoint.  A full-rank incident leg forces
  the opposite leg to be a nonzero one-sided killer, so both legs at a
  selected blocker cannot be full rank.
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

The exact-three search used a symmetry-broken SAT enumerator instead of
materializing its 50,388,480 labelled supports.  The structural
alternatives and their concrete go/no-go tests are recorded in
[`P5_ALTERNATIVE_STRATEGY_MAP.md`](P5_ALTERNATIVE_STRATEGY_MAP.md).
The `C10` half was independently regenerated and agrees exactly with the
11,751-case SAT catalogue; the packaged census is in
[`three_partial_c10_audit/`](research_snapshots/2026-07-27-p5-coordinate-cegar/three_partial_c10_audit/README.md).
Exact characteristic-zero unit-ideal calculations now exclude every one
of those cases.  Together with the 5,993-case `C4+C6` theorem, this
closes the complete exact-three-partial layer; the compact algebra replay
map is in
[`three_partial_c10_boundary/`](research_snapshots/2026-07-27-p5-coordinate-cegar/three_partial_c10_boundary/README.md).

The layer-by-layer boundary has now been superseded by a complete
deletion-stable cover of the exact-three-coordinate branch.  Across all
200 viable coordinate backbones, 812 spanning-tree charts suffice.  All
812 characteristic-zero ideals replay as unit ideals; the two global
support-cover CNFs have independently replayed DRAT proofs.  The theorem
and package are:

- [`P5_EXACT_THREE_COORDINATE_TREE_CHART_OBSTRUCTION.md`](P5_EXACT_THREE_COORDINATE_TREE_CHART_OBSTRUCTION.md)
- [`research_snapshots/2026-07-27-p5-tree-chart-cover/`](research_snapshots/2026-07-27-p5-tree-chart-cover/README.md)

The remaining `P_5` branch has four or five coordinate rows in at least
one local map.  The arbitrary-order conjecture remains unresolved.

An exploratory high-coordinate chart CEGAR treated the normalized
`q4_211`, `q5_311`, and `q5_221` cases.  Its former assertion that
these three cases partition the whole high-coordinate branch was
incorrect: four coordinate rows can instead have multiplicity `3+1`
or `2+2`, with a partial fifth row supplying the missing target
coordinate.  The chart certificates remain exact for the subcases
they actually cover, but the computation is not a complete
high-coordinate cover.

The analytic theorems below exclude `q5_311`, `q5_221`, and the full
partial `q4_211` parameter family.  A stronger two-singleton theorem
also handles the `q4_211` zero-row closure and 120 partial `3+1`
signatures.  The corrected census and normalized surviving families
are:

- [`P5_TWO_SINGLETON_COORDINATE_OBSTRUCTION.md`](P5_TWO_SINGLETON_COORDINATE_OBSTRUCTION.md)
- [`P5_Q4_211_EXCLUSION_THEOREM.md`](P5_Q4_211_EXCLUSION_THEOREM.md)
- [`P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`](P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md)
- [`P4_PURE_RANK_TWO_COMPONENT_THEOREM.md`](P4_PURE_RANK_TWO_COMPONENT_THEOREM.md)
- [`P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md`](P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md)
- [`P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md`](P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md)
- [`P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md`](P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md)
- [`P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md)
- [`P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md)
- [`P5_H31_DIAGONAL_QUADRIC_CURVE_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_CURVE_MARKED_FIBRE_OBSTRUCTION.md)
- [`P5_H31_DIAGONAL_QUADRIC_E_CURVE_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_E_CURVE_MARKED_FIBRE_OBSTRUCTION.md)
- [`P5_H31_DIAGONAL_QUADRIC_PURE_DIRECTION_CURVE_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_PURE_DIRECTION_CURVE_MARKED_FIBRE_OBSTRUCTION.md)
- [`P5_H31_DIAGONAL_QUADRIC_H0_RULING_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_H0_RULING_MARKED_FIBRE_OBSTRUCTION.md)
- [`P5_H31_DIAGONAL_QUADRIC_ELLIPTIC_GENERIC_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_ELLIPTIC_GENERIC_OBSTRUCTION.md)
- [`P5_H31_ELLIPTIC_MIDDLE_COORDINATE_RANK_DROP.md`](P5_H31_ELLIPTIC_MIDDLE_COORDINATE_RANK_DROP.md)
- [`P5_H31_ELLIPTIC_END_COORDINATE_FULL_RANK_CHART.md`](P5_H31_ELLIPTIC_END_COORDINATE_FULL_RANK_CHART.md)
- [`P5_H31_ELLIPTIC_END_GENUS_TWO_EXCEPTION_OBSTRUCTION.md`](P5_H31_ELLIPTIC_END_GENUS_TWO_EXCEPTION_OBSTRUCTION.md)
- [`P5_H31_ELLIPTIC_END_T2_DIVISOR_OBSTRUCTION.md`](P5_H31_ELLIPTIC_END_T2_DIVISOR_OBSTRUCTION.md)
- [`P5_H31_KNOWN_RANK_TWO_FAMILY_OBSTRUCTION.md`](P5_H31_KNOWN_RANK_TWO_FAMILY_OBSTRUCTION.md)
- [`P5_H31_RANK_TWO_COMPONENT_ORBIT_OBSTRUCTION.md`](P5_H31_RANK_TWO_COMPONENT_ORBIT_OBSTRUCTION.md)
- [`P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md`](P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md)
- [`P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md)
- [`P5_H31_MARKED_BASIS_OPEN_BRANCH.md`](P5_H31_MARKED_BASIS_OPEN_BRANCH.md)
- [`P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md`](P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md)
- [`P5_H31_COMPONENT_FIBER_INFINITY_OBSTRUCTION.md`](P5_H31_COMPONENT_FIBER_INFINITY_OBSTRUCTION.md)
- [`P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md`](P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md)
- [`P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md`](P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md)
- [`P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md)
- [`P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md)
- [`P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md)
- [`P5_H31_SINGLE_GATE_P3_REDUCTION.md`](P5_H31_SINGLE_GATE_P3_REDUCTION.md)
- [`P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md`](P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md)
- [`P5_H31_SECONDARY_GATE_EXCLUSION.md`](P5_H31_SECONDARY_GATE_EXCLUSION.md)
- [`P5_H31_DIAGONAL_QUADRIC_NORMALIZATION_BOUNDARY_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_NORMALIZATION_BOUNDARY_OBSTRUCTION.md)
- [`P5_H31_DIAGONAL_QUADRIC_OUTER_BOUNDARY_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_OUTER_BOUNDARY_OBSTRUCTION.md)
- [`P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md)
- [`P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md)
- [`P5_H22_DISJOINT_MIXED_STAR_EQUAL_OPPOSITE_WEIGHT_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_EQUAL_OPPOSITE_WEIGHT_OBSTRUCTION.md)
- [`P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md)
- [`P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md`](P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md)

Of 1,680 covered local signatures with at least four coordinate rows,
1,170 are excluded immediately by local signature type.  The remaining
510 signatures are exactly `H31` (240) and `H22` (270), but the `H31`
geometry has narrowed further: every rank-one pure-deletion profile is
excluded, and the complete marked-basis fibre over the finite known
family chart has no lift.  Plane geometry reduces the genuine
projective toric boundary to 21 Segre-capable all-rank orientations,
and their complete marked fibres now have no lift either.  The nonzero
preferred-chart divisor, the first-plane Schubert line at infinity,
and the internal `E=0` divisor are closed at complete marked-fibre
level as well.  Thus the complete marked fibre of the known component
is excluded.  A second component is now proved to exist, and its
complete nonzero factored slice `A=B=F=H=1` and all source/mode
symmetry translates are excluded, as are the complete nonzero
`A=B=F=1,H=0` slice and its orbit.  More strongly, a conic-bundle
reparameterization identifies the normalized component birationally
with an elliptic surface, and exact function-field projection excludes
its generic marked fibre in every orientation.  Its first apparent
end-coordinate exception curves are also empty: the conjugate smooth
genus-two trisections on the deepest `q=0,3` marking intersections have
  no rank-drop point.  In fact, both complete regular marking divisors
  `t2=x` and `t3=1` are empty for both endpoints.  A complementary
  middle-coordinate Fitting cover closes the three
  remaining pivot divisors and the regular two-torsion slice.  The two
  residual rational curves on the elliptic-normalization boundary are
  closed by exact relative projection and an all-extension marked
  minor.  Finally, the outer `A B F=0` boundary reduces to four
  coordinate curves and one conic; exact relative projections,
  one-marked minors, and one stacked `5 x 5` certificate close every
  fibre.  Thus the complete marked fibres of the first two
  all-rank-two pure-`P_4` components are excluded from `H31`.
  The cubic diagonal-quadric map has since produced three additional
  symmetry-inequivalent components, bringing the certified lower bound
  to five.  Their generic marked fibres are excluded by exact
  function-field projection and uniform all-extension determinants,
  but their parameter/projective boundaries remain.  A spinor
  calculation on a common smooth diagonal quadric proves that no
  component-sized nonzero-pure family lives away from the block-line
  jump locus; the three ruling patterns reduce to one empty and two
  one-dimensional normalized loci.  The embedded-`P_3` suspension has
  since proved that the eight-component list was incomplete; the
  current nine-component list is still not known to be exhaustive.
  On the eight pure-`P_4` component orbits known before that
  suspension, the generic weighted `H22` incidence is empty.  Six
  earlier proofs combine unit
  binary projections, projective-kernel covers, and one- or two-minor
  ternary Fitting obstructions.  The diagonal-quadric proof instead
  uses an empty projective Segre-join fibre and properness.  On the
  disjoint mixed-star component, exact Fitting minors recover a
  `D_23` line and a degree-five `D_01` marking scheme, then exclude
  every genuine binary direction.  Thus those eight orbits are
  generically closed for both `H31` and weighted `H22`.  The ninth
  orbit is now generically closed for `H31` as well, by a three-line
  apolar insertion arrangement.  Restoring the slope closes its
  generic weighted `H22` fibre by the same arrangement plus one
  structural zero diagonal.  Thus all nine known orbits are now
  generically closed for both marked types.  The ninth orbit's entire
  normalized `H31` chart is closed as well, and its weighted boundary
  is closed on every rank-two projected-line stratum.  The rank-one
  projected-image collapse is now closed by the complementary marked
  contraction too, so its entire normalized weighted chart is empty.
  On the `H31` side, the omitted support-two normalization divisor
  `A=0`, `B!=0` is now empty as well.  Its singular insertion pencil
  has one exceptional line; the only matrix-pencil resonance is
  closed by a stacked determinant and a fixed third-contraction
  coefficient `4`.  The complementary `r=0`, `A B!=0` divisor is now
  closed too: its insertion determinant is three signed planes times
  one tangent--Segre factor, and exact one-marked covers close every
  Fitting stratum.  Thus the ninth orbit's whole affine `B!=0` chart
  is empty for `H31`.  Its projective compactification is now closed
  too: homogeneous normal support `[C:A:B]` either has support one,
  giving the zero restriction, or enters a closed `C'B'!=0` affine
  chart by source symmetry.  Hence the ninth component's complete
  marked `H31` fibre is empty.
  Other component boundaries, slope boundaries, and component exhaustiveness stay open,
  although the eighth component's full equal- and opposite-weight
  slope fibres are now excluded already at the binary level, twelve
  generic parameter/coordinate boundary branches are closed, and the
  principal coupled slope-parameter divisor is closed by a cross-mode
  Fitting obstruction.  An intrinsic content factorization of the
  seven selected `D_23` maximal minors now closes four further rational
  boundary sheets `af=+/-1,a phi=+/-1`; on those sheets the generic
  `D_23` binary incidence is itself empty.  The corresponding `D_01`
  minor/pivot ledger also exposes the compactified endpoint `r=0`.
  There `D_01` fails at binary level, and the rank-six `D_23`
  degeneration fails an unsplit two-minor Fitting obstruction.
  Normalizing the further divisor `a^2 f^2+2bf+1=0` exposes a new
  irreducible quadratic component branch, and full unsplit two-minor
  ideals exclude both weighted directions there as well.  Three
  further rational slope graphs are excluded by six unsplit identities;
  one genuine mode-zero degeneration is repaired by the fixed mode-one
  `0457` minor.  An exact source-torus quotient
  `(a,b,f,phi)~(af,bf,1,phi/f)` reduces the dense component base to a
  two-dimensional surface without changing either weighted slope.
Thus this does not remove the 240 signatures from the fail-closed
census and `P_5 -> Delta_3` remains unresolved.

A stronger finite seed set now removes the gauge-pivot assumptions
entirely on 72 distinct `q5_311` support closures.  The original 34 and
the new 38 closures have zero overlap.  All 72 rational systems freshly
replay as unit ideals through exactly equivalent split saturations.
Their reconstructed branch CNF is still SAT, so this is a strict finite
advance rather than the missing high-coordinate theorem:

- [`research_snapshots/2026-07-28-p5-high-coordinate-zero-forests/`](research_snapshots/2026-07-28-p5-high-coordinate-zero-forests/README.md)
- [`research_snapshots/2026-07-28-p5-q5-311-rare-zero-wave2/`](research_snapshots/2026-07-28-p5-q5-311-rare-zero-wave2/README.md)

The latest stopped continuation transported every exact chart through the
288 branch symmetries and uses a deterministic gauge-tree portfolio to
avoid normalization-dependent Gröbner stalls.  The base 1,380-chart
discovery boundary expands to 336,672 chart-orbit clauses.  Two further
family-learning rounds add 560 exact representatives and six enlarged
family seeds; its last continuation started from 510,198 unique
transported clauses and remained SAT through 360 new records.

The normalized `q5_311` row also exposes two simultaneous deleted-`P_4`
rank-one slices.  Their mixed equations, together with nonvanishing of
all three pure amplitudes, give exact unit ideals on all 300 charts in
one frozen continuation ledger: 298 direct and two split.  No
majority-colour mixed equation is needed.  This identifies a uniform
finite mechanism and a two-chart pure-nonvanishing boundary, not a
completed branch proof.

There is now an analytic reduction behind that finite mechanism.  A
nonzero decomposable `P_4` restriction can have at most two rank-three
local maps.  Hence each rare deletion drops rank in at least two of the
four remaining modes.  The rank-drop theorem first leaves a shared case
or a disjoint `2+2` partition.  The shared case is impossible because
its two exceptional-row contractions expose the same residual `P_3`
but place it in independent target-colour pure lines.  In the disjoint
case, the four common-row `P_3` contractions must be all zero or all
pure, and both alternatives contradict the nonzero rare slices.
Therefore the complete normalized `q5_311` branch is excluded over `C`.
The rank-drop theorem and its 10,880,000-profile finite-field audit
program are in
[`P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md`](P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md).
The primary theorem replay passes; the large finite-field census remains
pending at this checkpoint.
The shared-case obstruction is in
[`P5_Q5_311_SHARED_DROP_OBSTRUCTION.md`](P5_Q5_311_SHARED_DROP_OBSTRUCTION.md).
The complete branch theorem is in
[`P5_Q5_311_EXCLUSION_THEOREM.md`](P5_Q5_311_EXCLUSION_THEOREM.md).

The theorem is sharp.  A symbolic five-parameter family and an
independent exact-integer audit are in
[`P4_DECOMPOSABLE_RANK_TWO_FAMILY.md`](P4_DECOMPOSABLE_RANK_TWO_FAMILY.md).
An exact Grassmann-incidence Jacobian calculation proves that its
closure is a generically smooth five-dimensional component:
[`P4_PURE_RANK_TWO_COMPONENT_THEOREM.md`](P4_PURE_RANK_TWO_COMPONENT_THEOREM.md).
Its preferred-chart closure and unique nonzero internal boundary
divisor are explicit in
[`P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md`](P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md).
This confirms that the remaining target is simultaneous two-deletion
compatibility.  Exact classifications of both zero and nonzero
decomposable `P_3` restrictions through rank-at-least-two maps are in
[`P3_ZERO_HYPERPLANE_PRODUCT_THEOREM.md`](P3_ZERO_HYPERPLANE_PRODUCT_THEOREM.md)
and
[`P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md`](P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md).

The same rank-drop method now gives an exact structural reduction for
normalized `q5_221`.  Its three distinguished-mode contractions are
embedded `P_4` tensors on hyperplanes with independent normals.  Each
normal lies in at least two of the four remaining row spaces.  Because
the singleton colour is distinguished, the correct minimal incidence
list has nine marked types rather than only the six underlying
uncoloured multigraphs.  Cross-contracting at a multiply incident mode
produces one of six explicit sign-related `P_3` tensors; a residual
rank-one gate is recorded explicitly before the `P_3` classification
is used:

- [`P5_Q5_221_HYPERPLANE_INCIDENCE_REDUCTION.md`](P5_Q5_221_HYPERPLANE_INCIDENCE_REDUCTION.md)

Three exact marked incidence boundaries are already closed at once.
The two multiplicity-two colours cannot have the same exact drop pair.
A singleton drop at a shared endpoint makes two cross contractions
force both outside maps to kill `e_0+e_1` and `e_2+e_3`, contradicting
exactness.  If the singleton pair is instead complementary, the
paired-majority mode forces a nonzero residual `P_3` normal to use the
`z` coordinate, while a singleton-drop mode forces the same normal to
omit `z`.  The rank-one exceptions collapse to an impossible zero
residual.  Hence the exact paired-majority pattern is impossible:

- [`P5_Q5_221_PAIRED_MAJORITY_DROP_OBSTRUCTION.md`](P5_Q5_221_PAIRED_MAJORITY_DROP_OBSTRUCTION.md)

This is a strict reduction, not a complete `q5_221` exclusion.  At this
checkpoint, extra rank drops and six remaining minimal marked patterns
still required separate compatibility arguments.

The next exact marked type is closed too.  If the singleton edge is
doubled with one majority edge and the other majority edge is adjacent,
the shared endpoint contains all three normals.  A first `Q_20`
contraction fixes the other two plane normals as the two support-two
sign variants.  Repeating the contraction from the all-normal endpoint
leaves two possible signs at the doubled endpoint; one forces a
rank-three residual and the other forces incompatible normal support.
The only rank-one boundary is rejected by the zero-diagonal
cross-scalar lemma:

- [`P5_Q5_221_MARKED_DOUBLE_ADJACENT_OBSTRUCTION.md`](P5_Q5_221_MARKED_DOUBLE_ADJACENT_OBSTRUCTION.md)

Together, the exact obstruction theorems close four of the nine
marked exact-six-incidence types.  They do not yet cover extra
containments.

The marked double-plus-disjoint type is excluded by a different final
step.  A nonzero `Q_20` first forces both modes on the disjoint majority
edge to kill `e_2+e_3`.  The `AB|CD` complement pairing of `T_2` then
forces one doubled endpoint to have row plane
`span(h_0,u_0)`.  A contracted nondegenerate `P_2` forces the other to
have `span(h_0,u_1)`.  In `T_1`, the factor `e_2+e_3` can then enter
only that second mode, leaving a nonzero pure `P_3` restriction with
rank profile `322`, impossible:

- [`P5_Q5_221_MARKED_DOUBLE_DISJOINT_OBSTRUCTION.md`](P5_Q5_221_MARKED_DOUBLE_DISJOINT_OBSTRUCTION.md)

The complete exact triangle type is now excluded:

- [`P5_Q5_221_TRIANGLE_OBSTRUCTION.md`](P5_Q5_221_TRIANGLE_OBSTRUCTION.md)
- [`P5_Q5_221_TRIANGLE_WORKING_NOTE.md`](P5_Q5_221_TRIANGLE_WORKING_NOTE.md)

Repeated `h_2` contraction splits the triangle into two genuinely
different chiral cases.  In the first, the apparent rank-one exceptions
are inconsistent with the full normal support already forced by the
two nonzero residuals.  In the second, the only rank-one gates have the
wrong target colours, while every other branch has a forbidden
rank-three map or support-one normal.  At this checkpoint, six of the
nine exact minimal types were closed.

The exact star type is excluded too:

- [`P5_Q5_221_STAR_OBSTRUCTION.md`](P5_Q5_221_STAR_OBSTRUCTION.md)

At the all-normal centre, the cross-scalar matrix is invertible with
zero diagonal.  Its determinant is the sum of two directed-cycle
products, so one full residual cycle is nonzero.  The `P_3` sign chart
and its single rank-one gate then force a mixed coefficient of the
colour-two `P_4` slice to be `-4` times nonzero scalars.  Seven of the
nine exact minimal types were closed at this checkpoint.

The two exact marked paths are excluded as well:

- [`P5_Q5_221_MARKED_END_PATH_OBSTRUCTION.md`](P5_Q5_221_MARKED_END_PATH_OBSTRUCTION.md)
- [`P5_Q5_221_MARKED_MIDDLE_PATH_OBSTRUCTION.md`](P5_Q5_221_MARKED_MIDDLE_PATH_OBSTRUCTION.md)

For a marked end, the cross-residual pencil first isolates the two
possible rank-one gates.  A nonzero `Q_02` forces the two opposite
colour-two hyperplanes to kill `u_1`, after which a required
colour-one coefficient and a forbidden colour-two coefficient share
the same nonzero factor.  If `Q_02` vanishes, the remaining `Q_20`
rank-one branch kills the required `T_1` coefficient, while its
rank-two branch forces a forbidden mixed `T_1` coefficient.

For a marked middle, residual plane normals are kernel lines
`K_i intersect J_cd`.  Exact absence of `h_2` identifies the two
overlapping residual lines at each of two modes.  In one chirality all
three `Q_12` normals satisfy the same coordinate equality, impossible
in either a full or support-two `P_3` sign chart.  The other chirality
has a support-one `Q_21` normal.

All nine exact minimal marked types are closed.  The later monotone
theorems below also close every extra-containment stratum.

That remaining boundary has an exact incidence-poset reduction:

- [`P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md`](P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md)

Every extra-containment pattern contains a seven-incidence cover of the
minimal layer.  Up to mode permutations and swapping the two majority
colours, there are exactly fourteen marked covers: nine contain a mode
whose kernel is fixed to `span(u_0,u_1)`, and five have mode-degree
profile `2,2,2,1`.  A complete `q5_221` proof now requires monotone
obstructions on this cover layer.  The distinguished-normal theorem
closes six covers monotonically:

- [`P5_Q5_221_DISTINGUISHED_NORMAL_MULTIPLICITY_THEOREM.md`](P5_Q5_221_DISTINGUISHED_NORMAL_MULTIPLICITY_THEOREM.md)

The strengthened triangle theorem, a two-channel Segre argument, and
a block-apolar rectangle exclude the exact seven-incidence strata of
three further covers:

- [`P5_Q5_221_REPEATED_MAJORITY_PAIR_COVER_OBSTRUCTION.md`](P5_Q5_221_REPEATED_MAJORITY_PAIR_COVER_OBSTRUCTION.md)
- [`P5_Q5_221_COVER_13_OBSTRUCTION.md`](P5_Q5_221_COVER_13_OBSTRUCTION.md)

The two-all-normal theorem closes one further cover:

- [`P5_Q5_221_TWO_ALL_NORMAL_MODES_OBSTRUCTION.md`](P5_Q5_221_TWO_ALL_NORMAL_MODES_OBSTRUCTION.md)

The directed-cycle factor-line theorem closes two more fixed-kernel
covers.  Its second orientation corrects a tempting but false
`Q_21` inference: the all-normal zero-diagonal matrix actually forces
the cycle `Q_20,Q_01,Q_12`.  Both possible ranks at the partner mode
then make two differently coloured residuals share one local factor
line:

- [`P5_Q5_221_H1_PARTNER_ALL_NORMAL_OBSTRUCTION.md`](P5_Q5_221_H1_PARTNER_ALL_NORMAL_OBSTRUCTION.md)

The remaining fixed-kernel theorem closes covers `#7,#10`:

- [`P5_Q5_221_REMAINING_FIXED_KERNEL_OBSTRUCTION.md`](P5_Q5_221_REMAINING_FIXED_KERNEL_OBSTRUCTION.md)

Only two genuine eighth-incidence boundaries survive above the three
exact-only covers.  One has two repeated normal pairs; the other is the
four-cycle of pair-incidence Schubert divisors.  A common-coordinate
`P_3` sign-slice obstruction excludes the first and one orientation of
the second.  The last orientation double-contracts `T_2` to the
rank-two form `Sym(h_0,h_1)` through two injective maps, contradicting
the required pure target product:

- [`P5_Q5_221_FINAL_MONOTONE_BOUNDARY_OBSTRUCTION.md`](P5_Q5_221_FINAL_MONOTONE_BOUNDARY_OBSTRUCTION.md)

Therefore the complete normalized `q5_221` branch is excluded over
`C`.  At that checkpoint the separate normalized `q4_211` branch
remained open.  It is now excluded below, but the corrected `H31/H22`
partial-row frontier still prevents a proof that `P_5 -> Delta_3` is
impossible.

The then-remaining `q4_211` branch has a chart-free
simultaneous-pencil reduction.  In normalized coordinates the distinguished mode pulls the
three target covectors back to

```text
(a,1,1,0,0), (b,0,0,1,0), (c,0,0,0,1),
```

with at least two of `a,b,c` nonzero.  The other four maps would have to
diagonalize their whole three-dimensional span.  On the
source-coordinate-zero slice this becomes a projective line of
support-four contractions whose boundary consists of one support-two
and two support-three `Delta_2` contractions when `abc != 0`.
Equivalently, the `78 x 5` matrix of mixed target coefficients must
have rank at most two, while its diagonal part has rank three on the
kernel.

The published support-four construction is transverse to this
condition: its matrix has rank four, kernel
`span(1,1,1,1,0)`, and diagonal image `(12,12,12)`.  An exact
two-variable elimination proves rank four on every point of its
two-parameter family, not merely at the integer example.  Thus that
positive construction does not lift to `q4_211`; the exceptional
rank-at-most-two degeneracy locus is the new analytic frontier:

- [`P5_Q4_211_SIMULTANEOUS_PENCIL_REDUCTION.md`](P5_Q4_211_SIMULTANEOUS_PENCIL_REDUCTION.md)

The generic parallel singleton-normal incidence type has also been
recast as a two-dimensional diagonal matrix pencil.  When `bc != 0`,
the two complementary maps must both kill `e_1+e_2`.  If their
bilinear residual vanishes, one complementary mode contains both
normals, reducing the type to an adjacent extra-incidence boundary.  If
the residual is nonzero, a second quotient by the forced singleton
image makes one embedded `P_4` residual equal to `-2b e_3^2` or
`-2c e_4^2`, contradicting its required vanishing.  Hence no genuinely
parallel minimal type survives on `bc != 0`; it always has a third
common incidence and can be reselected as adjacent:

- [`P5_Q4_211_PARALLEL_INCIDENCE_KERNEL_REDUCTION.md`](P5_Q4_211_PARALLEL_INCIDENCE_KERNEL_REDUCTION.md)

At a common-normal mode, the two cross residuals also assemble into a
single order-four permanent tensor after quotienting by the local
`span(e_1,e_2)` image.  If one cross scalar vanishes, the
decomposable-`P_4` rank-drop theorem forces a fourth source normal
`(0,0,0,c,b)` into another row space.  If neither vanishes, the tensor
maps to `Delta_2`, leaving a marked sharp-subrank-two boundary:

- [`P5_Q4_211_ADJACENT_P4_PENCIL_REDUCTION.md`](P5_Q4_211_ADJACENT_P4_PENCIL_REDUCTION.md)

That marked boundary is now completely excluded.  When both pure cubic
slices have rank two everywhere, their six singleton rows belong to
one three-parameter family; the adjacent incidences force a flattening
rank at least four instead of two.  Otherwise there is exactly one
gate of each kind at distinct modes.  The resulting transverse and
tangent normal forms are incompatible with, respectively, the
triple-`n` contraction and a double-`n` decomposable-`P_3` sign chart:

- [`P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md`](P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md)
- [`P5_Q4_211_MARKED_DELTA2_PAIR_IMAGE_OBSTRUCTION.md`](P5_Q4_211_MARKED_DELTA2_PAIR_IMAGE_OBSTRUCTION.md)
- [`P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md`](P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md)
- [`P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md`](P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md)
- [`P5_Q4_211_ONE_CROSS_PENCIL_SATURATION_REDUCTION.md`](P5_Q4_211_ONE_CROSS_PENCIL_SATURATION_REDUCTION.md)
- [`P5_Q4_211_ONE_CROSS_DIRECTION_CONIC_REDUCTION.md`](P5_Q4_211_ONE_CROSS_DIRECTION_CONIC_REDUCTION.md)

The generic exact disjoint type has a complementary projective
reduction.  Its mixed double contraction is a nondegenerate ternary
quadratic, and its four cross-pair rank-one equations are polarities
between the four local kernel lines.  Exact disjointness forces all four
restrictions to have rank two.  The resulting `K_(2,2)` polarity system
forces one complete normal pair to share the kernel
`span(e_1+e_2)`.  A kernel-propagation refinement then leaves only
`(s,s,s,s)` and `(s,s,d,s)`.  The former kills the required
doubled-colour-zero coefficient; the latter forces incompatible
`h_2,n` target colours.  Thus exact disjoint incidence is excluded:

- [`P5_Q4_211_DISJOINT_CONIC_POLARITY_REDUCTION.md`](P5_Q4_211_DISJOINT_CONIC_POLARITY_REDUCTION.md)
- [`P5_Q4_211_DISJOINT_EXCLUSION_THEOREM.md`](P5_Q4_211_DISJOINT_EXCLUSION_THEOREM.md)

The three parameter faces are now closed too.  Coordinate-normal
polarity excludes `b=0` and, by colour symmetry, `c=0`.  On `a=0`,
the adjacent branch is a complete-quadrangle degeneracy locus on
`Gr(2,4)` with a nonzero complement-pairing minor, and the exact
disjoint branch reduces to a ternary `P_3` cube with incompatible
antipodal corners.  Together with the two-singleton treatment of the
zero row, this completes `q4_211`:

- [`P5_Q4_211_EXCLUSION_THEOREM.md`](P5_Q4_211_EXCLUSION_THEOREM.md)

This still does not close `P_5`.  The exact corrected high-coordinate
frontier consists of `H31`, where one pure and one `Delta_2` embedded
`P_4` share three source rows, and `H22`, where three embedded `P_4`
contractions share one target colour across their pure/`Delta_2`
images:

- [`P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`](P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md)

The new 38 zero-forest closures are also a stronger stress test of the
rare-slice mechanism.  Direct zero-forest saturation closes 36.  The
remaining two have exact 16-chart and 25-chart support covers using only
the same 160 rare mixed words, all three pure amplitudes, and no lex
symmetry breaking.  All 41 support-chart ideals replay freshly, and both
CaDiCaL and Glucose verify both covers as UNSAT.  This closes those two
finite closures.  Those certificates alone were not a complete
`q5_311` classification; the analytic theorem above now supplies the
complete branch exclusion.

The frozen public packages, exact zero-cell closures, bounded WSL
transport retries, the rejected local-order false lead, retrospective
orbit ranking, exact family enlargement, the rare-slice reduction, and
the ongoing fail-closed search are documented in:

- [`P5_HIGH_COORDINATE_CHART_ORBIT_CEGAR.md`](P5_HIGH_COORDINATE_CHART_ORBIT_CEGAR.md)
- [`P5_Q5_311_RARE_SLICE_REDUCTION.md`](P5_Q5_311_RARE_SLICE_REDUCTION.md)
- [`P5_Q5_311_RARE_AFFINE_CORE.md`](P5_Q5_311_RARE_AFFINE_CORE.md)

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
- [`FIVE_ROOT_ZERO_COUPLING_INTERSECTION_LEMMA.md`](FIVE_ROOT_ZERO_COUPLING_INTERSECTION_LEMMA.md)
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
- [`P5_EXACT_THREE_C10_BOUNDARY_OBSTRUCTION.md`](P5_EXACT_THREE_C10_BOUNDARY_OBSTRUCTION.md)
- [`P5_EXACT_THREE_COORDINATE_TREE_CHART_OBSTRUCTION.md`](P5_EXACT_THREE_COORDINATE_TREE_CHART_OBSTRUCTION.md)
- [`P5_C10_BINARY_FORK_OBSTRUCTION.md`](P5_C10_BINARY_FORK_OBSTRUCTION.md)
- [`P5_C10_TRIANGLE_OBSTRUCTION.md`](P5_C10_TRIANGLE_OBSTRUCTION.md)
- [`P5_C10_ODD_CYCLE5_OBSTRUCTION.md`](P5_C10_ODD_CYCLE5_OBSTRUCTION.md)
- [`P5_C10_SCALAR_SPAN_OBSTRUCTION.md`](P5_C10_SCALAR_SPAN_OBSTRUCTION.md)
- [`P5_C10_DEGREE_ONE_MACAULAY_OBSTRUCTION.md`](P5_C10_DEGREE_ONE_MACAULAY_OBSTRUCTION.md)
- [`P5_C10_TEN_EQUATION_AFFINE_CORE.md`](P5_C10_TEN_EQUATION_AFFINE_CORE.md)
- [`P5_EXACT_THREE_MOTIF_QUOTIENT.md`](P5_EXACT_THREE_MOTIF_QUOTIENT.md)
- [`P5_FIVE_EQUATION_LAURENT_CORE.md`](P5_FIVE_EQUATION_LAURENT_CORE.md)
- [`P5_NO_QUADRATIC_RESTRICTION_EQUATIONS.md`](P5_NO_QUADRATIC_RESTRICTION_EQUATIONS.md)
- [`P5_NO_CUBIC_RESTRICTION_EQUATIONS.md`](P5_NO_CUBIC_RESTRICTION_EQUATIONS.md)
- [`P5_NO_QUARTIC_RESTRICTION_EQUATIONS.md`](P5_NO_QUARTIC_RESTRICTION_EQUATIONS.md)
- [`P5_NO_QUINTIC_RESTRICTION_EQUATIONS.md`](P5_NO_QUINTIC_RESTRICTION_EQUATIONS.md)
- [`P5_DEGREE_SIX_INVARIANT_PULLBACK.md`](P5_DEGREE_SIX_INVARIANT_PULLBACK.md)
- [`P5_Q5_221_TRIANGLE_OBSTRUCTION.md`](P5_Q5_221_TRIANGLE_OBSTRUCTION.md)
- [`P5_Q5_221_STAR_OBSTRUCTION.md`](P5_Q5_221_STAR_OBSTRUCTION.md)
- [`P5_Q5_221_MARKED_END_PATH_OBSTRUCTION.md`](P5_Q5_221_MARKED_END_PATH_OBSTRUCTION.md)
- [`P5_Q5_221_MARKED_MIDDLE_PATH_OBSTRUCTION.md`](P5_Q5_221_MARKED_MIDDLE_PATH_OBSTRUCTION.md)
- [`P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md`](P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md)
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
python verify_five_root_zero_coupling_intersection.py
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
PYTHONPATH=tmp/python_deps python verify_p5_exact_three_c10_boundary_obstruction.py
PYTHONPATH=tmp/python_deps python verify_p5_c10_binary_fork_obstruction.py
PYTHONPATH=tmp/python_deps python verify_p5_c10_triangle_obstruction.py
PYTHONPATH=tmp/python_deps python verify_p5_c10_odd_cycle5_obstruction.py
PYTHONPATH=tmp/python_deps python verify_p5_c10_scalar_span_obstruction.py
PYTHONPATH=tmp/python_deps python verify_p5_c10_degree_one_macaulay_obstruction.py
PYTHONPATH=tmp/python_deps python verify_p5_c10_ten_equation_affine_core.py
PYTHONPATH=tmp/python_deps python probe_p5_c10_joint_affine_class.py
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
