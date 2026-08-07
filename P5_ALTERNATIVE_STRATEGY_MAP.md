# Alternative routes for the remaining P5 obstruction

## Status

The global Krenn--Gu conjecture remains unresolved.  This note records
routes that can replace or guide support-by-support Gröbner calculations
in the remaining attempt to prove that the order-five permanent tensor
does not restrict to `Delta_3`.

The complete exact-three-coordinate branch is now excluded, with no
bound on how many of its ten non-coordinate cells are partial.  The
deletion-stable spanning-tree cover in
`P5_EXACT_THREE_COORDINATE_TREE_CHART_OBSTRUCTION.md` replaces the
remaining layer-by-layer search.

For context, the next layer would have contained

```text
2 * 6^5 * binomial(10,3) * 3^3 = 50,388,480
```

labelled exact-three-partial supports across both shapes, and deeper
layers grow further.  The chart theorem covers them all at once.  The
remaining `P_5` problem is now the structurally distinct branch in
which some local map has four coordinate rows of multiplicity `3+1`
or `2+2` and one partial row supplying the missing target coordinate.
The earlier three-type high-coordinate partition omitted these two
families; the exact correction is in
`P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md`.

## Route A: sparse-resultant cores

One exact-two `C4+C6` support has a five-equation Laurent contradiction:

```text
22001, 22002, 22200, 22201, 22202.
```

The full support system has 205 mixed equations, but these five reduce
to the two-branch identity in
`P5_FIVE_EQUATION_LAURENT_CORE.md`.  This is evidence that the large
Gröbner bases may be discovering much smaller sparse resultants.

A term-count screen found 55 exact-two supports with the same
`(9,8,9,8,9)` five-equation rectangle profile: 29 of shape `C4+C6` and
26 of shape `C10`.  A five-second probe certified six of the 29
`C4+C6` systems directly; 23 timed out.  A timeout here is not a
survivor, because deleting equations can make a Gröbner calculation
harder.  Term counts alone also do not prove that two cores are related
by a Laurent change of variables.

A monomial-hypergraph refinement separates those 55 supports into 32
classes.  Only the original support is identical to the proved core
under a plain variable relabelling.  Thus a reusable theorem needs
genuine Laurent/gauge transformations or several different sparse
identities; the term-count rectangle is not itself the lemma.

The next useful test is therefore structural, not another longer batch:

1. encode each five-polynomial system as a monomial-incidence
   hypergraph;
2. quotient by variable relabelling and torus gauge transformations;
3. recover a symbolic resultant identity for each resulting class;
4. translate each identity back into a support-local forbidden pattern.

If a small number of forbidden patterns covers the exact-three layer,
the computational theorem can become a human-scale lemma.

The first exact-three `C10` extraction is substantially stronger than
the exact-two seed.  Catalogue orbit 384 has 193 mixed equations, but an
exact lift certificate uses no saturation equation and minimizes to ten
mixed coefficients whose affine ideal is already the unit ideal.  Those
ten equations have a short hand reduction ending in
`2*t*(a+s)=0` while earlier equations force both factors nonzero.  See
`P5_C10_TEN_EQUATION_AFFINE_CORE.md`.

The first transport test falsifies the coarsest version of that motif
idea.  The 15 catalogue cases sharing orbit 384's canonical coordinate
backbone and missing-colour geometry split into 11 affine unit ideals
and four affine non-unit ideals.  Geometry therefore does not determine
the core.  The next experiment is to quotient the coefficient
monomial-incidence systems themselves and to record whether each
contradiction is affine or needs Laurent saturation.  See
`probe_p5_c10_joint_affine_class.py`.

A finer algebraic pattern already has substantial coverage.  If three
forbidden coefficients have the form

```text
P=1+m*A,  Q=1+m*B,  R=A+B,
```

then `P+Q-m*R=2`, an immediate characteristic-zero contradiction.  An
independent bitmask scan finds this binary fork in exactly 1,328 of the
11,751 audited `C10` orbits, and the original generator symbolically
replays all 1,328 identities.  This needs neither saturation nor pure
nonzero assumptions.  See `P5_C10_BINARY_FORK_OBSTRUCTION.md`.

The first sparse-resultant generalization is complete.  The
four-polynomial template

```text
P=1+m*A,  X=A+B,  Y=A+C,  Z=B+C
```

gives `2P-mX-mY+mZ=2`.  It occurs in 604 catalogue orbits, 113 of
which are not binary-fork hits.  The two exact rules therefore exclude
1,441 `C10` orbits in union and leave 10,310 undecided by these sparse
templates.  The original generator replays all 113 new identities.
See `P5_C10_TRIANGLE_OBSTRUCTION.md`.

The next step is no longer template guessing by geometry: enumerate
short monomial-linear relations directly in the sparse coefficient
vector matroid, then cluster the resulting exact certificates.

The first five-edge odd-cycle scan adds 74 orbits beyond the
fork/triangle union.  If

```text
Ei=Ai+A(i+1)  for a five-cycle,
P=1+m*A0,
```

then the alternating edge sum is `2*A0`, so the six coefficients give
`2P-m(E0-E1+E2-E3+E4)=2`.  The three sparse rules now exclude 1,515
`C10` orbits in union and leave 10,236 undecided by these rules.  The
original generator replays all 74 new identities.  See
`P5_C10_ODD_CYCLE5_OBSTRUCTION.md`.

An exhaustive general search for anchored four-coefficient relations
of the form `2P-mX-mY+mZ=2` added no orbit beyond the fork/triangle
union.  Thus the next useful matroid layers are seven-cycles and
relations with at least five non-anchor coefficients, not further
rephrasings of the four-coefficient case.

A complementary degree-zero coefficient-vector scan is broader than
any one fixed template, but it does not subsume the monomial-multiplier
rules above.  Sparse Gaussian elimination followed by rational
reconstruction finds exact identities

```text
sum(q_i*F_i)=1
```

in at least 1,523 `C10` orbits.  It adds 175 orbits beyond the three
named sparse rules, making the certified union 1,690 and leaving 10,061
not covered by these certificates.  Every modular hit reconstructs
over the rationals, and the original generator replays all 175 new
identities.  Modular misses are not treated as rational
non-membership proofs.  A seven-cycle probe adds only one orbit beyond
the named rules, and that orbit is already in this scalar-span closure.
See
`P5_C10_SCALAR_SPAN_OBSTRUCTION.md`.

The degree-one Macaulay span generated by `F_i` and `u_j*F_i` is now
complete as a certificate-discovery pass over the 10,061 cases left by
those rules.  It finds 1,960 modular hits; every one reconstructs to an
exact rational identity and replays through the original generator.
The certified union is therefore 3,650, leaving 8,101 cases not covered
by these layers.  Modular misses are not rational non-membership proofs.
See `P5_C10_DEGREE_ONE_MACAULAY_OBSTRUCTION.md`.

Naively extending the same dictionary elimination to degree two is not
sustainable.  A guarded probe on one degree-one miss processed 13,194
of roughly 57,600 rows in 120 seconds and accumulated 1,669,740 basis
nonzeros without a decision.  The next algebraic implementation should
use sparse-core extraction, F4-style elimination, or black-box
finite-field linear algebra rather than scaling that prototype.

## Route B: symmetry-broken exact-k SAT

The support constraints, local projective-signature catalogue,
source-pair quotas, pure-permanent requirement, and
no-unique-mixed-permanent condition are Boolean before any coefficient
algebra is attempted.  They can therefore be enumerated directly in a
symmetry-broken SAT model.

`enumerate_p5_exact_k_partial_supports.py` implements this route.  It
adds an exact cardinality constraint to the existing local-signature
CNF and blocks only canonical fixed-shape supports.  This avoids
building a Python set containing all 50,388,480 labelled exact-three
supports.  Every run checkpoints and stops before host-available memory
falls below 20 percent.

This remains a finite search, but it is sustainable enough to produce a
small survivor catalogue on which Routes A and C can learn structural
certificates.  The exact-three runs completed with:

```text
C4+C6:  5,993 support-semantic survivor orbits
C10:   11,751 support-semantic survivor orbits
total: 17,744 support-semantic survivor orbits.
```

The `C4+C6` catalogue is no longer exploratory.  An independent packed
regeneration of all 25,194,240 labelled exact-three supports agrees
exactly on its 5,993 final orbits, and exact characteristic-zero
unit-ideal calculations exclude all of them.  See
`P5_EXACT_THREE_C4C6_BOUNDARY_OBSTRUCTION.md`.

The `C10` catalogue is independently audited as well.  A second
packed-array regeneration of all 25,194,240 labelled supports agrees
exactly on all 11,751 final orbits; see
`P5_EXACT_THREE_C10_CENSUS.md`.  Exact characteristic-zero Singular
calculations return the unit ideal directly for all 11,751 support-only
systems.  Together with the 5,993-case `C4+C6` result, this closes the
complete exact-three-partial layer; see
`P5_EXACT_THREE_C10_BOUNDARY_OBSTRUCTION.md`.

The support enumeration has now been replaced by an all-layer cover.
For each coordinate backbone, SAT produces an uncovered support and a
spanning tree inside it.  A full-closure coefficient ideal saturates
only the three pure coefficients, so every non-tree entry may vanish.
A unit ideal therefore excludes every descendant support containing
that tree.  Deletion minimization leaves 401 `C10` and 411 `C4+C6`
charts.  Global symmetry-broken CNFs using those clauses are UNSAT, and
their DRAT traces replay independently.  See
`P5_EXACT_THREE_COORDINATE_TREE_CHART_OBSTRUCTION.md`.

Their raw supports now have a concrete structural quotient.  Forgetting
the coordinate backbone leaves only 17 uncoloured partial-cell
geometries, or 66 geometries after recording the missing colours.  The
pair of a coordinate-backbone class and a missing-colour geometry has
2,675 observed values across all 17,744 survivors.  See
`P5_EXACT_THREE_MOTIF_QUOTIENT.md`.  This makes a motif-level Laurent
identity search substantially smaller than the support catalogue while
preserving an explicit fallback refinement.

## Route C: Grassmannian and Pluecker elimination

A proposed restriction consists of five surjective maps

```text
A_i : C^5 -> C^3.
```

Before choosing target bases, each map determines a two-plane
`ker(A_i)` in `Gr(2,5)`.  The current row-support language is a chartwise
description of these five Grassmannian points.  Replacing matrix entries
by Pluecker coordinates has three potential advantages:

- the rank-three condition is built in;
- changes of target basis disappear;
- the five local coordinate-plane incidence conditions become
  Schubert-type conditions.

The concrete experiment is to rewrite the pair-cover and
source-subset Hall hierarchy as incidences among five points of
`Gr(2,5)`, then eliminate against the Pluecker quadrics.  A resulting
empty intersection would close all support charts at once.  Even a
nonempty intersection would stratify the remaining charts by matroid,
which is a more invariant classifier than raw zero patterns.

## Route D: tensor invariants

The desired statement is

```text
(A_1 tensor ... tensor A_5) P_5 != Delta_3.
```

Thus a polynomial on `3 x 3 x 3 x 3 x 3` tensors that vanishes on every
restriction of `P_5` but not on `Delta_3` would be a one-line global P5
obstruction.

The full covariant search has an exact low-degree floor.  The
multiplicity-free decomposition of
`Sym^2((C^3) tensor power 5)` has sixteen irreducible
`GL(3)^5` modules, indexed by even subsets of exterior-square factors.
An isolated pair of source permutations proves that the restriction
pullback is nonzero, hence injective, on every module.  Therefore the
`P_5` restriction image has no nonzero quadratic equations at all.
The proof map is `P5_NO_QUADRATIC_RESTRICTION_EQUATIONS.md`.

Degree three has nontrivial multiplicity spaces, but it is now closed
as well.  Exact Schur--Weyl character arithmetic reduces all 147
ordered cubic module tuples to thirteen type-count representatives.
Deterministic matrix-unit contractions of three copies of `P_5` have
full multiplicity rank in every representative; nonzero minors modulo
five certify the ranks over characteristic zero.  Therefore the full
cubic pullback is injective and the restriction image has no cubic
equations.  See `P5_NO_CUBIC_RESTRICTION_EQUATIONS.md`.

Degree four is now closed by the same principle with a compiled exact
contraction.  The 839 ordered nonzero `S_4` module tuples reduce to 44
mode-symmetry representatives with multiplicity at most ten.  Every
representative has full rank modulo five, and the complete Schur
dimension sum is the 148,897,035-dimensional quartic space.  Hence the
quartic pullback is injective over characteristic zero.  The proof map
is `P5_NO_QUARTIC_RESTRICTION_EQUATIONS.md`.

Degree five is closed as well.  The five target partitions produce
2,955 ordered nonzero module tuples, reduced by mode symmetry to 115
representatives with multiplicity at most 61.  A compiled five-copy
subset contraction reaches full multiplicity rank in every block over
`F_7`; the complete Schur-dimension sum is 7,355,513,529.  Since 120 is
invertible modulo seven, the modular rank witnesses lift to
characteristic zero.  Thus the full quintic pullback is injective.  See
`P5_NO_QUINTIC_RESTRICTION_EQUATIONS.md`.

The obvious degree-three determinant contraction cannot work.  It uses
one alternating epsilon tensor in each of five modes; swapping two of
the three tensor copies changes its sign by `(-1)^5`, while a
degree-three polynomial is symmetric in those copies.  The contraction
is therefore identically zero.  Degree six, using two epsilon tensors
per mode, is the first natural invariant search space.

A naive 30-index degree-six contraction is computationally unsuitable,
but the symmetry-reduced search space is small.  Exact Young
seminormal-form character arithmetic verifies that the `S_6`
representation of shape `(2,2,2)` has dimension five and that

```text
dimension (([2,2,2]) tensor power 5)^(S_6) = 11.
```

Thus there are only eleven degree-six scalar invariants to test.
`analyze_p5_degree_six_invariant_space.py` checks the Coxeter relations,
the complete `S_6` character table, character orthogonality, and the
11-dimensional multiplicity.

That remaining test is now exact and negative.  Eleven explicit
epsilon-pair contractions have a generic evaluation minor with
determinant `1 mod 5`, so they form a basis.  Their pullbacks along
explicit local restrictions of `P_5` have an evaluation minor with
determinant `2 mod 5`.  The pullback is therefore injective: no nonzero
degree-six `SL(3)^5` scalar invariant vanishes on every `P_5`
restriction.  This closes the simple degree-six separator route, though
it does not exclude higher-degree invariant relations or non-invariant
equations.  The exact proof map is
`P5_DEGREE_SIX_INVARIANT_PULLBACK.md`.

## Route E: Fourier charge and Gaussian moments

Applying the three-point Fourier transform in every target mode sends
`Delta_3` to the charge-conservation tensor

```text
1[k_1 + ... + k_5 = 0 mod 3].
```

This turns three isolated diagonal coefficients into one affine
`Z_3` hyperplane and may expose a convolution or character-sum identity
for the permanent tensor.  It is worth testing whether the five local
maps can satisfy this charge law without support enumeration.

The original graph tensor is also the squarefree, one-photon-per-party
sector of an exponential quadratic form, so Wick/hafnian identities are
available.  The caution is that standard Gaussian recurrences couple
different photon-number sectors, while the conjecture constrains only
one postselected sector.  A useful identity must eliminate the
unobserved sectors; otherwise this language is only a reformulation.

The root-of-unity block selector in
[`ROOT_OF_UNITY_BLOCK_PERMANENT_SELECTOR.md`](ROOT_OF_UNITY_BLOCK_PERMANENT_SELECTOR.md)
now supplies one exact postselection-safe filter.  In the commuting
square-zero algebra it cancels every permanent term selecting rows from
more than one prescribed block while retaining every within-block minor
sum with a nonzero coefficient.  This does not solve the target Fourier
charge equations, but it replaces the Gaussian-sector concern by a finite
legality question: can the selector's constant columns be realized by
legal contractions of the graph tensor?

## Route F: herald promotion and matching-tensor cut rank

The exact rational `n=6, k=4, d=4` Question-2 construction posted by
`@speaktoevil` supplies a concrete positive model with two fixed red
heralds.  Its 17-mode support actually carries a complete
eight-parameter family; see `Q2_N6_K4_D4_CONSTRUCTION.md`.

The first attempted promotion to Question 1 fails for a structural
reason.  If the four-output block has monochromatic amplitudes `A_i` and
the herald pair receives colour-channel weights `H_j`, the coefficients
of

```text
(i,i,i,i,j,j)
```

form the outer-product matrix `A_i H_j`.  On the three non-red colours
it has rank one, whereas the corresponding Question-1 target submatrix
has rank three.  On the concrete support every off-diagonal entry is
represented by a unique perfect matching, so no cancellation is
available.

This suggests measuring the matching tensor's flattening rank across
small vertex cuts.  For any proposed counterexample, the target
`Delta_d` has cut rank `d` across every nontrivial partition.  A graph
decomposition that exposes fewer than `d` independent partial-matching
interface states is therefore impossible.  The useful next theorem
would bound that interface rank in terms of a separator, matching width,
or a finite set of crossing-matching states.  Conversely, a constructive
search should explicitly create at least `d` nonseparable interface
channels, rather than adding more parallel colours to a rank-one herald
edge.

The counterexample-oriented version is a selector-gadget search: combine
several colour-permuted heralded modules so that exactly one branch is
active and their rank-one slices sum to the diagonal.  The main hazard
is that taking a union of graph gadgets introduces cross-matchings; a
valid selector must cancel those cross terms exactly.  This is a
different search space from raw support enumeration and gives an
immediate falsifiable target: a four-channel selector for the verified
Question-2 module.

There is now a concrete first cancellation gadget for this test.  The
`b=t=d=s=2` root-of-unity selector gives

```text
per [[u,v,1,1], [w,z,1,1], [p,q,2,-2], [r,s,2,-2]]
  = -8(uz+vw)+2(ps+qr),
```

so every matching mixing the two variable row blocks disappears.  The
general block theorem is replayed over characteristic zero and audited
independently over `Q` and `Q(omega)`.  The isolated seed now also has an exact
eight-vertex loopless symmetric lift: all 105 full graph matchings are
included, exactly 24 bipartite terms survive, and the constant columns arise
from ordinary fixed `d=4` herald modes.  See
[`ROOT_OF_UNITY_SELECTOR_SYMMETRIC_HAFNIAN_LIFT.md`](ROOT_OF_UNITY_SELECTOR_SYMMETRIC_HAFNIAN_LIFT.md).

The resulting boundary is sharper.  If the entire left side is fixed, every
completion on the four live right modes is a local restriction of `P_4`, so
the exact subrank-two theorem rules out `Delta_3`.  The next Route-F experiment
must keep additional left modes live while composing the selector with the
17-mode Question-2 support and must check all residual and cross-module
matchings.  Neither that composition nor herald removal is proved.

## Route G: dual hyperplane annihilation

The public Lean proof of the `d=n` family in
[`MonochromaticQuantumGraph.lean`](https://github.com/google-deepmind/formal-conjectures/blob/af88acbf9da0f26e3e934743a819e986e02f6875/FormalConjectures/Paper/MonochromaticQuantumGraph.lean)
gives a useful coordinate-free view of the hard branch.  Fix a root
vertex `r`, set its test vector to the all-ones vector, and for each
other vertex `u` define the covector

```text
A_u(b) = sum_a W_ru(a,b).
```

Choosing `v_u in ker(A_u)` kills every matching term at its edge
incident with `r`.  A witness would therefore force

```text
sum_c product_(u != r) v_u(c) = 0
```

for every product of those hyperplanes.  Equivalently, if
`q_u : C^d -> C^d/<A_u>` denotes the dual quotient, then

```text
(tensor_(u != r) q_u) Delta_d = 0.                 (G1)
```

The Lean proof rules this out when `d=n` by an elementary
colour-versus-neighbour pigeonhole construction.  Restricting a
hypothetical larger-colour witness to any `n` colours gives the same
obstruction for `d>=n`.  The prize regime `3<=d<n` is exactly where that
counting step stops.

For `d=3`, however, the failure of the contraction has a sharp
classification.  If all `q_u` have rank at least two, then

```text
sum_(c=1)^3 tensor_u q_u(e_c) = 0
```

implies that all three decomposable summands vanish separately.  Indeed,
if all three were nonzero, a three-term dependence among pure tensors
would make the three factors collinear in all but at most one mode,
contradicting rank at least two in another mode.  If one summand
vanished, the other two would have proportional factors in every mode;
at a mode killing the first summand this would again make the quotient
rank at most one.  The remaining cases are immediate.

Thus `(G1)` holds exactly when, for each target colour `c`, some neighbour
has

```text
A_u a nonzero multiple of e_c^*.
```

These are precisely the three coordinate blockers exposed by the
double-star and multi-star arguments elsewhere in this repository.
One neighbour cannot serve two colours, so every root has at least three
distinct blockers for this all-ones contraction.

The two-root divisibility route sharpens the local geometry further.
Around any rank-three root edge it freezes five blocker choices.  For
each choice, the two complementary-column ranks are either both at most
one, or a rank-two pair forces the opposite pair to be exactly zero.  If
one entire incident block is full rank, the opposite block is a nonzero
one-sided killer.  In particular, the two incident blocks at a frozen
blocker cannot both be full rank.

Therefore the `d=n` formal proof does not bypass the remaining problem:
in the three-colour regime it reduces exactly to the need to propagate
blocker surplus across several roots.  The useful next experiment is to
apply the contraction at two or three roots simultaneously and express
the resulting compatibility as a Grassmannian incidence condition,
linking this route to Route C without choosing row-support charts.

## Route H: simultaneous deleted-permanent rank drops

The two rare `q5_311` colours replace the full five-mode problem by two
different deleted-row restrictions of `P_4`.  A new flattening theorem
shows that a nonzero decomposable `P_4` restriction has at most two
rank-three local maps.  Each rare deletion therefore forces at least
two rank drops among the same four maps.

The rank-drop theorem first leaves two incidence types:

```text
shared mode:
  the three common source rows span one line;

disjoint modes:
  two drops for the first deletion and the complementary two
  for the second.
```

The shared branch is now excluded exactly.  Contracting the two deleted
slices in the shared mode along their exceptional rare rows produces
the same residual `P_3`, but the two identities require it to lie in
independent pure target-colour lines.  Therefore the two drop sets are
necessarily a disjoint `2+2` partition.

The disjoint branch is now excluded too.  Its four common-row maps all
have rank two.  Contracting the four non-drop incidences produces four
`P_3` restrictions, each zero or pure.  The four-plane sign theorem says
they are either all zero or all nonzero.  The zero case kills a common
source row in every mode and hence kills the rare slices; the nonzero
case forces one non-drop contraction to vanish after another places its
pure factor in that mode's common image plane.

Thus Route H gives an exact arbitrary-chart exclusion of the complete
normalized `q5_311` branch.  The earlier rare-slice CEGAR cores remain
useful as independent finite evidence but are no longer the proof
frontier.

The rank-drop bound is sharp: an exact five-parameter family of four
rank-two maps sends `P_4` to a nonzero pure tensor.  This rules out the
coarser strategy of forbidding a single rank-at-least-two compression.
The useful invariant couples both deletions.  The zero and nonzero
`P_3` classifications, including the six two-parameter projective sign
charts, supply exactly the missing disjoint-branch compatibility.

For normalized `q5_221`, the same contraction exposes three embedded
copies of `P_4` with independent hyperplane normals.  Every normal is
contained in at least two of the four remaining row spaces.  The
singleton colour is distinguished, so selecting two incidences per
normal gives nine marked types over six uncoloured multigraphs, not six
fully symmetric types.

At a multiply incident mode, cross-contraction produces one of six
explicit sign-related `P_3` tensors.  Its residual map in another mode
has rank

```text
3-dim(U_i intersect J_cd^perp),
```

so a two-dimensional intersection is a genuine rank-one boundary and
must be separated before applying the existing `P_3` classification.
The first three exact marked boundaries are nevertheless closed: the
two multiplicity-two colours cannot have the same exact drop pair.  A
singleton drop at either shared endpoint supplies a common-normal mode;
the two cross residuals then force both outside maps to kill
`e_0+e_1` and `e_2+e_3`, contradicting the exact majority drop sets.
If the singleton pair is complementary, the paired-majority mode forces
a nonzero residual normal to contain `z`, while a singleton-drop mode
forces the same normal to omit `z`.  The rank-one exceptions imply a
zero residual that makes a singleton-drop map kill `z`, also
impossible.

The singleton-doubled double-plus-adjacent exact type is also excluded.
Its shared endpoint contains all three normals.  The first `Q_20`
residual fixes the adjacent and outside plane normals as the two
support-two sign variants.  The second `Q_20` residual has one possible
rank-one exception, which makes both `Q_12,Q_21` impossible despite the
local cross-scalar lemma.  After removing that exception, the two
possible signs at the doubled endpoint force either a rank-three
`J_21` map or incompatible `J_12` normal support.

The disjoint version is excluded as well.  Its first nonzero `Q_20`
forces both modes on the disjoint majority edge to kill `y_+`.  The
`AB|CD` complement pairing then leaves only a `K_0` plane at one
doubled endpoint; a contracted nondegenerate `P_2` leaves `K_1` at the
other.  In the colour-one slice, `y_+` is forced uniquely into `K_1`,
leaving a residual `P_3` with forbidden rank profile `322`.

The complete exact triangle type is now excluded without an exhaustive
search.  Repeated `h_2` contraction gives two chiralities.  In the
first, full-support normal transport removes the apparent rank-one
exceptions; in the second, the only rank-one gates land in the wrong
target colours.  The cross-scalar alternative then contradicts the
nonzero decomposable-`P_3` classification in both cases.

The exact star is excluded by a simultaneous-slice argument.  At its
all-normal centre, the cross scalars form an invertible zero-diagonal
`3 x 3` matrix, forcing one of two directed three-cycles of nonzero
residuals.  Either cycle fixes three leaf factor directions and makes
a forbidden mixed coefficient of the colour-two `P_4` slice equal to
`-4` times nonzero scalars.

Both marked paths are now excluded analytically.  At a marked end, the
cross-residual pencil has two rank-one gates.  The nonzero `Q_02`
branch is killed by the `AC|BD` complement pairing and a required versus
forbidden coefficient pair.  In the remaining branch, rank one at `A`
makes the required colour-one coefficient vanish, while rank two
forces a different mixed colour-one coefficient to be nonzero.

For a marked middle, repeated `h_2` contraction gives two target-support
chiralities.  Interpreting residual plane normals as the kernel lines
`K_i intersect J_cd` turns the overlap into a Grassmannian incidence
obstruction.  One chirality puts all three `Q_12` normals in a
two-vertex slice of the `P_3` sign rectangle; the other produces a
support-one `Q_21` normal.  Thus all nine exact minimal marked types are
closed.  At this intermediate stage the extra-containment strata
remained open; the monotone cover theorems below close them.

The extra-containment poset has now been reduced without searching row
spaces.  Every nonminimal incidence pattern contains a seven-incidence
cover of the minimal layer, and there are fourteen such marked cover
orbits.  Nine contain a mode with fixed kernel
`span(u_0,u_1)`; five have degree profile `2,2,2,1` and lie entirely on
the three pair-incidence Schubert divisors.  Proving monotone
obstructions for the cover layer would exclude normalized `q5_221`.

Squarefree apolarity now supplies a monotone theorem that the
distinguished normal has multiplicity exactly two.  It excludes the six
covers `#0--#4,#9`, including every higher-incidence stratum above
them.  The triangle, repeated-majority-pair, and block-apolar rectangle
arguments exclude exact covers `#12,#8,#13`, respectively, but not
their monotone boundaries.  The three-edge dependency obstruction also
closes the two-all-normal cover `#5` monotonically.  A directed-cycle
factor-line theorem closes the all-normal-partner covers `#6,#11`
monotonically: the difficult orientation forces `Q_20,Q_01,Q_12`, and
its rank-one and rank-two boundaries both identify two differently
coloured local factor lines.  The same directed-cycle method closes
the remaining fixed-kernel covers `#7,#10`.

Only two eighth-incidence orbits remain above the exact-only covers
`#8,#12,#13`.  One is excluded because a nonzero `Q_02` chart cannot
have all three normals in the common-coordinate slice.  In the other,
the remaining orientation double-contracts `T_2` to
`Sym(h_0,h_1)` through two injective maps, preserving bilinear rank two
and contradicting a pure target product.  Thus the complete normalized
`q5_221` branch is excluded over `C`.

## Route I: the closed `q4_211` simultaneous diagonal pencil

The `q4_211` subbranch was not merely another support cover.  Normalize
its distinguished mode to

```text
u_0=(a,1,1,0,0),
u_1=(b,0,0,1,0),
u_2=(c,0,0,0,1),
```

with at least two of `a,b,c` nonzero.  If `Phi(z)` denotes contraction
of `P_5` by `z` followed by the other four maps, then a `q4_211`
solution requires

```text
Phi(u_c)=lambda_c e_c^4.
```

Thus `Phi` maps the whole three-plane `span(u_0,u_1,u_2)`
isomorphically to the diagonal tensor plane.  After projecting away
the three diagonal target words, the resulting `78 x 5` contraction
matrix must have rank at most two.

This is a determinantal/Terracini-type condition rather than a
coefficient-support search.  The source-coordinate-zero section is the
projective support-four pencil

```text
a t_0+b t_1+c t_2=0.
```

For `abc != 0`, its three boundary points are exactly one support-two
and two support-three contractions mapping to the three two-colour
diagonal boundaries.  The singleton contractions also give two
embedded `P_4` tensors, hence two selected rank-drop edges on four
modes: parallel, adjacent, or disjoint.

The known positive support-four family lies outside the required
degeneracy locus.  Its off-diagonal rank is exactly four at every
parameter point, proved by a two-variable minor elimination, so its
kernel is only one-dimensional.  It cannot be deformed within that
family into `q4_211`.

Two of the three incidence types now have specialization-specific
reductions.  On `bc != 0`, a two-dimensional diagonal matrix pencil
shows that a parallel pair always acquires a third common incidence;
the apparent nonzero-residual exception is excluded by quotienting an
embedded `P_4`.  At a common mode, the two cross residuals form another
`P_4`: one cross scalar forces the new normal `(0,0,0,c,b)`, while two
nonzero scalars give a marked `P_4 -> Delta_2` restriction.  Its
all-rank-two slice family is excluded by a rank-four
complement-pairing flattening.  Its rank-one boundary has exactly two
alternating gates and two determinant strata; a triple-normal
contraction excludes the transverse lift and a double-normal `P_3`
sign chart excludes the tangent lift.  Thus only the separate one-cross
fourth-normal incidence survives adjacent.  There `n` pulls back only
from target colour zero.  A simultaneous zero/pure pair of `P_3`
residuals forces one whole opposite normal pencil, while the polarized
binary cubic on the pure-slice pencil has roots exactly
`h_2,n,u_1` or `h_1,n,u_2`, modulo double-normal and common-kernel
gates.  A second, nondegenerate direction conic fixes the two remaining
direction lines; compatibility with the binary cubic removes its free
polar core.  The second-common and double-normal alternatives reduce
away, leaving a full direction plane or a common `e_1+e_2` kernel.
The former has an impossible repeated-direction target colour.  In the
latter, binary polarity and the paired `P_3(w_-),P_3(w_+)` charts force
one vector simultaneously onto target colours zero and two.  Hence
adjacent incidence is empty on `abc != 0`.  On the same stratum, the
exact disjoint type turns the nondegenerate doubled-colour
quadratic into a projective polarity.
The four cross edges form a `K_(2,2)` orthogonality system, forcing one
normal pair to share the source kernel `span(e_1+e_2)`.  Kernel
propagation leaves only `(s,s,s,s)` or `(s,s,d,s)`; both are
impossible, so exact disjoint incidence is excluded.

Parallel incidence reselects as adjacent, so these cases exhaust the
two singleton-normal containment sets.  The complete normalized
`q4_211` branch is therefore excluded on `abc != 0`.  The `a=0`,
`b=0`, and `c=0` faces are now excluded by their separate
Grassmannian, ternary-Segre, and coordinate-normal arguments.  Its
zero-row closure is covered by the two-singleton theorem.  Thus Route I
is complete and supplies techniques for the new frontier rather than
an open case.

## Route J: the `H31/H22` marked-deletion frontier

The surviving high-coordinate rows are

```text
H31: e_0,e_0,e_0,e_1,a e_0+b e_1+c e_2,  bc!=0;
H22: e_0,e_0,e_1,e_1,a e_0+b e_1+c e_2,  c!=0,
                                             (a,b)!=(0,0).
```

In `H31`, two coordinate contractions are embedded copies of `P_4`
sharing three source rows: one maps to a pure tensor and the other to
`Delta_2`.  In `H22`, the contractions with normals
`e_0^*-e_1^*`, `e_2^*-e_3^*`, and `e_4^*` are three embedded copies of
`P_4`; one maps pure, the other two map pure or to the same-colour
`Delta_2` boundary, and at least one is genuinely `Delta_2`.

The natural continuation is an incidence classification for a marked
`P_4 -> Delta_2` compression coupled to a neighbouring pure deletion.
Pair-image Grassmannians and the existing all-rank-two/alternating-gate
normal forms should be used before any ambient-map enumeration.  The
known five-parameter all-rank-two pure family is a dense chart in a
generically smooth five-dimensional **plane** component.  The first
mixed-matrix theorems excluded only displayed marked row sections, not
the full marked-basis fibres over those planes.

The component-completeness question now has a decisive negative answer.
In the squarefree Frobenius algebra

```text
C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2),
```

exceptional pair images become pairs of annihilator lines on diagonal
quadrics.  A radical-plane normal form yields a second
five-dimensional component, parametrized before diagonal-source orbit
by an irreducible `(3,3)` hypersurface in `P^2 x P^2`:

- [`P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md`](claims/p4/components/diagonal-quadric/P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md)

At one rational point of this component, exact marked projection leaves
only two markings, one for each of `q=0,3`; a uniform
`-8u(u-2v)^2` marked minor excludes every genuine extension.  This is
a complete point fibre:

- [`P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md)

The obstruction has now been globalized along the nonzero part of the
rational curve `A=B=E=F=H=1, C=c`.  Projection over `Q(c)` and exact
special fibres at `c=0,1` classify every marking for every `c!=-1`;
a separate relative elimination over `Q[c]`, saturated by `c+1`,
certifies that these are the only specialization jumps.
In each survivor kernel, a one-marked determinant is forced nonzero by
the two binary diagonal conditions:

- [`P5_H31_DIAGONAL_QUADRIC_CURVE_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_CURVE_MARKED_FIBRE_OBSTRUCTION.md)

A transverse curve `A=B=F=H=1,C=0,E=e` is also closed for every
`e in C`.  It contains the former isolated point at `e=2`, intersects
the first curve at `e=1,c=0`, and has only the relative projection
jumps `e=0,+/-1`:

- [`P5_H31_DIAGONAL_QUADRIC_E_CURVE_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_E_CURVE_MARKED_FIBRE_OBSTRUCTION.md)

The pure-factor-direction curve `C=-1,E=e` is closed in its natural
marking chart as well.  The slice equation

```text
C(C+1)(1-E^2)=0
```

and the source symmetry `E=-1 <-> E=1` then show that the complete
nonzero slice `A=B=F=H=1` is excluded:

- [`P5_H31_DIAGONAL_QUADRIC_PURE_DIRECTION_CURVE_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_PURE_DIRECTION_CURVE_MARKED_FIBRE_OBSTRUCTION.md)

The full discrete source/mode orbit of this slice is closed as well.
For example, `(0 1)(2 3)` on source coordinates and `1<->2` on modes
sends the `C=c` line to `A=B=C=E=F=1,H=h`.

The interior slice `A=B=F=1,H=0` is closed too.  Its equation
`(CE-1)(CE+1)=0` consists of two rational rulings exchanged by
`X_0<->X_3`.  A saturated relative projection on one ruling closes two
uniform survivor kernels and the sole `e=+/-1` jumps:

- [`P5_H31_DIAGONAL_QUADRIC_H0_RULING_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_H0_RULING_MARKED_FIBRE_OBSTRUCTION.md)

The normalized component has now been reframed globally on a dense
open set.  With

```text
U=C+H, S=1+CH, T=H+CE^2,
```

its equation is the conic-bundle determinant `S^2-UT`.  Setting
`r=S/U`, `x=1-rH`, and `Y=rEx` gives

```text
Y^2=x[(1-r^2)x^2+(3r^2-2)x+(r^2-1)^2].
```

Exact projection over the elliptic function field gives the unit ideal
for all four distinguished coordinates, uniformly in every marking.
Thus the generic marked fibre is empty.  The `H=0` rulings above become
the two sections `(1,+/-r^2)`, while the factored `H=1` slice is
supported over `r=1` or the birational base locus.  The minimal
resolution is an elliptic K3 with reducible-fibre root rank 17; the
known section is non-torsion, so Shioda--Tate gives Picard number 20
and Mordell--Weil group `Z + Z/2`:

- [`P5_H31_DIAGONAL_QUADRIC_ELLIPTIC_GENERIC_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_ELLIPTIC_GENERIC_OBSTRUCTION.md)

This is a dense-open theorem, not yet a complete-component theorem.
It reduces the remaining task to a proper divisor and boundary
classification.

The first divisor-support chart is now exact.  For `q=1,2`, quotienting
the universal mixed-kernel line turns the problem into a rank-six
determinantal locus.  A small pivot and bordered-minor compatibility
force every extra kernel on that chart onto the already-closed `H=0`
section or pure-direction/singular-fibre strata:

- [`P5_H31_ELLIPTIC_MIDDLE_COORDINATE_RANK_DROP.md`](P5_H31_ELLIPTIC_MIDDLE_COORDINATE_RANK_DROP.md)

For `q=0,3`, the canonical universal kernels are small as well.  One
bordered quotient minor proves full rank off the marking divisors
`t2=x,t3=1` and the standard geometric factors:

- [`P5_H31_ELLIPTIC_END_COORDINATE_FULL_RANK_CHART.md`](P5_H31_ELLIPTIC_END_COORDINATE_FULL_RANK_CHART.md)

On the deepest `q=0,3` intersections `t2=x,t3=1`, two-minor
compatibility leaves conjugate residual trisections.  Their common
normalization is a smooth genus-two curve, where each marking is unique
but two further full-rank minors have coprime residual factors.  Thus
both apparent curves are empty:

- [`P5_H31_ELLIPTIC_END_GENUS_TWO_EXCEPTION_OBSTRUCTION.md`](P5_H31_ELLIPTIC_END_GENUS_TWO_EXCEPTION_OBSTRUCTION.md)

The same genus-two model closes the complete regular `t2=x` divisor.
After the first rank conditions force `t1,t0`, two residual minors have
a one-variable resultant with only one regular quadratic exception; a
third minor is nonzero there:

- [`P5_H31_ELLIPTIC_END_T2_DIVISOR_OBSTRUCTION.md`](P5_H31_ELLIPTIC_END_T2_DIVISOR_OBSTRUCTION.md)

The complete regular `t3=1` divisor is now closed too.  The apparent
quadratic marking cover splits over the elliptic function field; its
two branches are forced onto the same genus-two normalization.
Univariate branch/sheet gcds leave only a finite algebraic set, where
exact mixed-kernel and binary-diagonal ranks exclude every lift:

- [`P5_H31_ELLIPTIC_END_T3_DIVISOR_OBSTRUCTION.md`](P5_H31_ELLIPTIC_END_T3_DIVISOR_OBSTRUCTION.md)

The middle-pivot complement is now closed as well.  A four-factor
Fitting cover eliminates its three marking divisors, while two adapted
minors close the regular `Y=0` two-torsion slice:

- [`P5_H31_ELLIPTIC_MIDDLE_COORDINATE_PIVOT_COMPLEMENT.md`](P5_H31_ELLIPTIC_MIDDLE_COORDINATE_PIVOT_COMPLEMENT.md)

Thus every regular elliptic-chart marking is excluded.  The
elliptic-normalization boundary is closed too: it reduces to the known
factorized/base-locus strata and two rational `r=0` curves, both
excluded by relative projection and a uniform all-extension marked
minor:

- [`P5_H31_DIAGONAL_QUADRIC_NORMALIZATION_BOUNDARY_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_NORMALIZATION_BOUNDARY_OBSTRUCTION.md)

The complete normalized affine slice `A=B=F=1` is therefore empty.
The outer projective/gauge boundary `A B F=0` is now empty as well.
Its coordinate surfaces form four curve types under a diagonal-source
torus and one source/mode involution, while `B=0` contributes one
rational conic.  Exact relative projection classifies every survivor;
one-marked minors close all transverse cases, and the sole deepest
edge direction has stacked determinant `128p`:

- [`P5_H31_DIAGONAL_QUADRIC_OUTER_BOUNDARY_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_OUTER_BOUNDARY_OBSTRUCTION.md)

This distinction is witnessed on the open `L!=0` stratum: shifting the
pure-colour rows by

```text
(-1/Q,0,L/(1+LQ),0)
```

produces a genuine binary `Delta_2` extension over the same plane
tuple.  Its marked determinant

```text
8(1+LQ)^2(1+(C+L)Q)
```

still excludes the ternary lift.  The ensuing determinantal
classification now closes the full affine Borel fibre over every
finite family member.  It finds the complete constructible survivor
table, including three isolated markings on `C=-L/2`, and excludes
every extension in every survivor kernel:

- [`P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md`](P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md)

The preferred-chart and toric plane closures remain useful base
geometry: the toric face lattice has only 21 Segre-capable all-rank
plane/orientation pairs.  The complete marked incidence now excludes
all 21, including both pure directions of every secant, both
first-plane charts, and every binary extension direction:

- [`P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md)

The mixed rank profiles are now closed.  A unique primary gate with
rank-two common-plane partners reduces to a marked `P_3` chart and four
projective line strata; their ternary lifts fail by transverse kernels
or one deepest `1122` coefficient.  A further common-plane rank drop
creates a secondary gate.  Its common data is a `P_3 -> Delta_2`
subtensor, and pair-image polarity leaves only two zero-product support
strata, both excluded by the same one-marked/mixed-colour mechanism.

Thus the marked-basis bundles of the first two components are closed.
The diagonal-quadric map has since produced three further
five-dimensional component orbits.  On the `1+3` radical-plane
stratum, the pure condition is the split cubic

```text
(D-G-S+T)(D+G-S-T)(D+G+S+T).
```

Exact smooth-point certificates distinguish its three components from
each other and from the earlier two by their generic `2+2/1+3`
diagonal-quadric jump counts.  Their generic marked fibres are empty:
function-field projection leaves no binary neighbour on one branch,
and on the other two every survivor has a one-marked determinant
`A^2B/c(S,D,G)`.  Their parameter/projective boundaries remain, and
the resulting five-component checkpoint was not exhaustive:

- [`P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md`](P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md)
- [`P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md)

The common-smooth-diagonal-quadric branch is now structurally closed
away from the block-line base locus.  After normalization to a smooth
quadric, the two spinor rulings reduce four annihilator lines to the
three patterns `LLLL`, `LLLR`, and `LLRR`.  Exact saturation makes the
first nonzero-pure locus empty and the other two only one-dimensional;
inverting every block discriminant `s_i(s_i^4-1)` makes all three unit
ideals.  Therefore this semisimple branch cannot contain a new
five-dimensional component:

- [`P4_COMMON_SMOOTH_DIAGONAL_QUADRIC_OBSTRUCTION.md`](P4_COMMON_SMOOTH_DIAGONAL_QUADRIC_OBSTRUCTION.md)

The generic directed radical-star block locus is classified as well.
Rank-one exceptional relations are coordinate-pair zero products.
Two of them pointing away from a common mode force a `2+2` or `1+3`
double-contraction radical.  Exhaustive dense normal forms recover
exactly the irreducible second component and the three split-cubic
components, with no further component on this stratum:

- [`P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md`](claims/p4/classifications/star/radical-star/P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md)

The rank-two-relation triangle has also become discrete.  Away from
trivial holonomy, its three bridge catalecticants are weighted
`1+3`/`2+2` cuts.  The full-support all-`1+3` case is now impossible:
the bridge factorization has an internal sheet and a fully supported
reflection sheet; coordinate-hyperplane annihilators exclude the
latter, and cyclic compatibility forces one common singleton.  The
result is an embedded pure `P_3`, whose perfect pairing drops the
three pair ranks from three to at most two:

- [`P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md`](claims/p4/classifications/rank-two-triangle/nonresonant/cut-reduction/P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md)
- [`P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md`](claims/p4/boundaries/rank-two-triangle/nonresonant/one-three/P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md)

A second hyperbolic-block argument excludes every full-support
`2+2` bridge.  Such a bridge is `q=ab`, and every factorization
contains the anchor `a` or `b`.  But a rank-three partner of
`Ann(q)=span(a_bar,b_bar)` has crossed-graph form with nonzero
off-diagonal coupling and contains neither anchor:

- [`P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md`](claims/p4/boundaries/rank-two-triangle/nonresonant/two-two/P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md)

The proper bridge-support boundary is now closed as well.  A nonzero
proper cut has one edge or is a two-edge star.  The former forces its
partner back into a coordinate two-plane and product rank one; the
latter puts all three triangle planes in one coordinate hyperplane,
where the pure-`P_3` pairing forces pair rank at most two:

- [`P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md`](claims/p4/boundaries/rank-two-triangle/nonresonant/degenerate-cut/P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md)

The complete nonresonant triangle is therefore empty.  Only the
resonant holonomy divisor remains.

The latter is now organized by an additive affine holonomy

```text
delta=A_12+A_23-A_13.
```

For `delta!=0`, the `R_3`-valued triple tensor is
`J(yxx+xyx+xxy)+Xxxx`, a tangent-Segre first jet, and the three
kernel-pair products form a cyclic cut system.  For `delta=0`, the
three local bases synchronize and multiplication factors through a
binary cubic `Sym^3(C^2) -> R_3`; purity compresses its first three
coefficients to a plane while the fourth escapes:

- [`P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md`](claims/p4/classifications/rank-two-triangle/resonant/affine-holonomy-reduction/P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md)

The complementary mixed zero-product orientation produces a sixth
component.  Its normalized kernel contractions form a `3 x 4`
determinantal matrix with five linear minimal primes.  One prime gives
an explicit pure family with a smooth five-dimensional
diagonal-source orbit.  A directed pure-kernel endpoint invariant
separates it from the three split-cubic branches despite the shared
coarse jump signature `(0,1)`:

- [`P4_MIXED_ORIENTATION_PURE_COMPONENT.md`](claims/p4/components/mixed-orientation/P4_MIXED_ORIENTATION_PURE_COMPONENT.md)

Its generic marked `H31` fibre is empty.  Function-field projection
leaves four rational sheets, and exact all-extension determinants plus
pure transverse entries exclude all of them:

- [`P5_H31_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md)

The lower-pair-rank boundary contains a seventh component orbit, now
of dimension six.  In its apolar normal form only

```text
T_1010=2(1-b(a+c)),   T_1110=2(1-e(a+c))
```

survive.  A rank-six family map and rank-fourteen smooth
Segre-incidence certificate prove component status.  Its generic pair
profile is `(4,3,2,4,4,3)`:

- [`P4_SIX_DIMENSIONAL_PURE_COMPONENT.md`](claims/p4/components/six-dimensional/P4_SIX_DIMENSIONAL_PURE_COMPONENT.md)

This component's generic marked fibre is empty as well.  The variables
`s=a+c,u=1-sb,v=1-se` expose a pure reconstruction kernel for one
distinguished coordinate.  The other three coordinates have one
rational marking each, all excluded by three-minor Fitting
certificates:

- [`P5_H31_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md)

For `H22`, retaining the residual source-torus slope gives a complete
generic component obstruction.  The weighted `01` pencil has no binary
neighbor.  The weighted `23` pencil has one rational marking sheet and
a two-dimensional extension kernel, but every genuine direction makes
one of two mode-zero marked minors nonzero:

- [`P5_H22_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md)

The mixed-orientation fivefold has a second generic weighted `H22`
obstruction.  The weighted `01` pencil is killed by an exact
hierarchical cover of the projective extension kernel: after the
mode-two/three extension coordinates vanish, four residual charts
close the remaining `P^3`.  For the weighted `23` pencil, five
low-degree eliminated marking relations give a three-closure cover,
and the mode-three `0267/0467` Fitting ideal is unit on every closure:

- [`P5_H22_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md)

The three split-cubic `1+3` branches give a unified third transport.
All weighted `01` projections and the `L_3` weighted `23` projection
are unit.  The remaining `L_1` scheme has two rational sheets and the
`L_2` scheme has three line closures; the same mode-zero `0247` minor
has saturated unit ideal on all five:

- [`P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md`](P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md)

The first rank-two component gives a fourth transport.  Its weighted
`01` mixed matrix is injective for every marking by an eight-chart
projective-kernel cover.  Its exact weighted `23` projection has two
rational sheets.  The mode-two `0147` minor excludes the first and the
`0137` minor excludes the second:

- [`P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md)

At equal source weights, both pencils are already empty at binary
level; in the second pencil, two mixed coefficient rows alone force the
contradiction:

- [`P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md`](P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md)

The weighted theorems show why that specialization was insufficient.
The diagonal-quadric component supplies the final generic transport.
In fixed coefficient coordinates, its extension image is an
eight-plane and marked binary targets lie in the join of a Segre
fourfold with its all-beta point.  One rational fibre is projectively
empty in both weighted directions: fifteen standard charts are unit,
the last gives only the zero-vector base point, and the exceptional
tangent five-space is disjoint.  Properness proves generic emptiness:

- [`P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md)

Thus the seven previously certified component orbits are generically
closed for weighted `H22`.  A disjoint-support mixed star has since
produced an eighth five-dimensional component.  Its normalized pure
condition is one irreducible cubic hypersurface, and exact rank-five
family/rank-fifteen incidence certificates prove component status:

- [`P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`](claims/p4/components/disjoint-mixed-star/P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md)

Its generic marked `H31` fibre is now empty.  Function-field
projection gives unit ideals for source coordinates zero and one and
one marking each for coordinates two and three.  On both surviving
markings the same `0137` minor is `+/-R*A*B^2`, with
`R=f*(bf+1)*(1-a^2*f^2)/(a^2*f+b)`, excluding every genuine binary
extension:

- [`P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md)

Its generic weighted `H22` incidence is now empty.  The mixed-matrix
Fitting locus is one marking line for `D_23^r` and an exact degree-five
scheme for `D_01^r`; a three-chart factor cover and one- or two-minor
ternary obstructions close every genuine binary direction:

- [`P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](claims/p5/h22/disjoint-mixed-star/P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md)

At the special slopes `r=1` and `r=-1`, the entire binary incidence is
empty: the mixed kernel lies in the first diagonal hyperplane at equal
weight and in the second at opposite weight:

- [`P5_H22_DISJOINT_MIXED_STAR_EQUAL_OPPOSITE_WEIGHT_OBSTRUCTION.md`](claims/p5/h22/disjoint-mixed-star/boundaries/P5_H22_DISJOINT_MIXED_STAR_EQUAL_OPPOSITE_WEIGHT_OBSTRUCTION.md)

Factoring the component relation on its coordinate and pivot divisors
produces twelve generic rank-two branches.  Twenty-four exact Fitting
ideals close them.  The last visible coupled coefficient in the
degree-five marking cover is also closed by switching the `D_01`
obstruction from local mode zero to mode one:

- [`P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md`](claims/p5/h22/disjoint-mixed-star/boundaries/P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md)
- [`P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md`](claims/p5/h22/disjoint-mixed-star/boundaries/P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md)

Other hidden coefficient divisors and component boundaries remain.
The embedded pure-`P_3` suspension has since proved that the earlier
eight-component list was incomplete and raised the lower bound to
nine.  Its generic marked `H31` fibre is now empty: deleting source
coordinate zero gives a six-column apolar insertion map whose
rank-drop support is three signed lines plus three points, and every
generic line kernel kills the all-alpha diagonal:

- [`P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md)

Restoring the weighted source-torus slope preserves this symbolic
reduction.  The `D_23` direction has an identically zero all-alpha
diagonal, while `D_01` is the same insertion arrangement on a
slope-dependent line.  Hence its generic weighted `H22` fibre is also
empty:

- [`P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md)

The nine exceptional `H31` insertion points are now classified
exactly.  Truncated Segre relations leave five binary families.  Four
are excluded by tiny neighboring one-marked covers; at the deepest
point every neighboring map has rank three, but the stacked
pure/neighbouring map has constant determinant `8`:

- [`P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md)

The analogous weighted boundary is also closed whenever the
slope-dependent projected mode-zero image is a genuine line.  Four
arrangement strata give six binary marked families; small factored
one-marked covers exclude them, with stacked determinants `8` and
`-8` at the two deepest points:

- [`P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md`](P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md)

The rank-one collapse `rS=1,T=rU` is now closed by switching to the
other required marked contraction.  Its complementary insertion
pencil is injective away from `S=+/-1`; at those two fibres its kernel
kills the `D_23` pure diagonal or the `D_01` alpha diagonal:

- [`P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md`](P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md)

One part of the ninth component's omitted normalization boundary is
now closed.  On `A=0`, `B!=0`, the support-three sign chart degenerates
to support two and the `H31` insertion map becomes a singular matrix
pencil.  A Fitting factor forces its exceptional line, generic
one-marked rank closes the line, and the unique resonance `C=-1` is
killed by a stacked determinant and the constant third-contraction
coefficient `4`:

- [`P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md)

The complementary `r=0`, `A B!=0` divisor is now closed as well.
Its `t!=0` part is the normalized chart after a signed source
permutation.  At `r=t=0`, the mixed insertion determinant is three
signed planes times one tangent--Segre factor.  Fitting ideals split
the boundary into four zero-coordinate branches, nine signed-sheet
second drops, and nine deepest families, all excluded by tiny
one-marked covers:

- [`P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md)

The apparent projective compactification is now closed too.  Write the
homogeneous absolute normal as `[C:A:B]`.  Support-one points give the
zero pure restriction; every support-two or support-three point can
be source-permuted into a closed chart with `C'B'!=0`:

- [`P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md)

Thus the ninth component is closed in full for `H31`; exhaustiveness
of the new component list remains open.  The earlier modular pattern and
timed-out broad route remain as provenance:

- [`P5_H22_DISJOINT_MIXED_STAR_WORKING_NOTE.md`](claims/p5/h22/disjoint-mixed-star/P5_H22_DISJOINT_MIXED_STAR_WORKING_NOTE.md)

The later two-rank-two-spoke mixed star gives a tenth component.  Its complete
marked-basis fibre over the generic component point is now empty for `H31`.
For each deleted coordinate, the all-alpha diagonal functional belongs to the
row module of the fourteen mixed extension functionals over
`C(s,t)[h0,h1,h2,h3]`; consequently every mixed-zero extension has zero first
diagonal.  Explicit global syzygy lines retain the nonzero all-beta diagonal,
so this is an asymmetric cokernel statement rather than collapse of the
extension map:

- [`P5_H31_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md)

Its weighted `H22` analysis first reached a dense-open symbolic checkpoint.
Cayley parameters turn the component law into `d=(1+uv)/(1-uv)` and give one
factored rank-eight mixed minor in each weighted direction.  Both binary
extensions are therefore empty on a dense open of the combined
component/slope/marking space.  At `(s,t)=(2,3),(3,5),(5,7)`, exact row-module
normal forms equal the full free rank-eight module for every marking and
slope.  The selected determinantal divisors were left open at that checkpoint:

- [`P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_DENSE_MARKING_OBSTRUCTION.md`](P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_DENSE_MARKING_OBSTRUCTION.md)

They are now closed by changing from marking coordinates to the fixed-vertex
Segre join:

- [`P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md)

On the nonzero all-kernel chart, the fifteen coordinates other than the free
all-active coordinate form a Boolean rank-one array.  Its six quadratic and
four cubic toric binomials eliminate all four Borel markings intrinsically.
After substitution of the eight weighted `23` extension entries, the ideal is
`(1)` over `C(u,v,rho)`.  Off one linear pivot divisor, three binomials already
give the visible contradiction `2(u-1)(v-1)=0`; the full natural toric ideal
closes the divisor.  The complete generic weighted fibre is empty.

The first component's one-rank-two-edge triangle now has a reverse support
classification on its crossed Borel orientation.  Genuine binary zero
products are labeled by the six two-subsets of the source coordinates, hence
by the octahedron `J(4,2)=L(K_4)`.  The three support orbits have exact and
very different outcomes:

```text
equal labels       -> all triangle planes lie in a coordinate hyperplane,
disjoint labels    -> a plane collapses or an exceptional pair rank drops,
one-point overlap  -> the unique dense orbit is the first apolar component.
```

The disjoint case is the rank-one `K_(2,2)` matrix-completion identity
`det[u,u']det[v',v]=0`; the overlap case is a signed-reflection
factorization of a triangle-supported quadratic.  This closes every support
collision in that orientation without Gröbner elimination:

- [`P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md`](claims/p4/classifications/triangle-211/crossed-211-triangle-support/P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md)

The remaining generic triangle work is no longer an undifferentiated
support problem.  It is confined to common-factor/radical Borel
orientations and support-one or lower-pair-rank boundaries.

The first common-factor branch is now a new component rather than a boundary
obstruction:

- [`P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md`](P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md)

Two leaf kernel rows share the exact zero divisor `a`, while their rank-one
edges share the active common-mode row `a_bar`.  The rank-two edge reduces to
`x_2-x_1 in (a_bar)`, leaving one affine translation parameter `r`.  Its
rank-one cubic apolar space leaves a `P^2` opposite-plane fibre.  Together
with the source torus, the family has dimension six; exact minors `3/128`
and `-9/2` certify a smooth incidence point.  The sorted pair profile
`(3,3,3,4,4,4)` distinguishes it from the earlier six-dimensional
component.  The certified lower bound is now eleven component orbits, and
its complete generic marked `H31` fibre is now empty:

- [`P5_H31_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md)

For each deleted coordinate, the all-kernel binary diagonal belongs to the
row module of the fourteen mixed rows over
`C(p,q,r)[h0,h1,h2,h3]`.  The all-active diagonal has nonzero cokernel class.
This is simultaneous in all markings; the exact-zero-divisor block makes two
all-kernel rows vanish identically and puts the other two visibly in a free
summand of the mixed module.  All eleven certified components are therefore
generically closed for `H31`.

The same component's generic weighted `H22` fibre is empty for a still more
structural reason:

- [`P5_H22_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md)

For the weighted `01` projection, two identical-support kernel rows can only
occupy the merged and fifth target channels.  The other two rows are forced
onto the `X2,X3` channels, where their permanent is
`p*t2*(-t3)+p*t3*t2=0`.  This is the exact-zero-divisor identity
`b*b_bar=0` exposed by a two-channel tensor cut.  It is homogeneous in the
merge weights and source scalings, so it closes every marking and weighted
slope without mixed equations.  Together with the fixed-vertex theorem for
the tenth component, all eleven certified components are now generically
closed for weighted `H22` as well as `H31`.  The eleventh component's special
pure-factor degenerations and projective boundary remain open.

The residual common-factor orientation has now crossed the component
boundary a second time:

- [`P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md`](P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md)

Write the complementary binary parts of the synchronized active row and the
common kernel as `s=uX2+vX3` and `t=pX2+qX3`.  The three-cubic apolar
condition factors through

```text
A=<s,t>=u*q+v*p,       Q=[s,t]=u*q-v*p.
```

The diagonal `Q=0` and split-polar graph `A=0` lead back to the eleventh
component or its `q=0` boundary.  On `AQ!=0`, the remaining equations force
the common kernel's first binary block onto a single coordinate.  One exact
sheet has only `T_1111=-4` and graph profile `(3,3,4,3,3,3)`.  Its source-
torus closure supplies five tangent directions at `(r,k)=(-4/3,2)`, while
the universal Segre incidence has rank fourteen.  Solving fourteen regular
equations along the excess tangent makes the omitted equation begin with
`12h^2`, so the sixth direction is obstructed and the five-dimensional
family closure is a component.  Its sorted pair profile
`(3,3,3,3,3,4)` differs from all eight earlier fivefolds, while dimension
separates the three earlier sixfolds.  This raises the certified component
lower bound to twelve.

The displayed two-parameter sheet is a dense normal form.  Its complete
generic marked `H31` fibre is now empty:

- [`P5_H31_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md)

Over `C(r,k)[h0,h1,h2,h3]`, the all-kernel binary diagonal belongs to the
fourteen-row mixed module for all four deleted coordinates, while the
all-active diagonal has nonzero cokernel class.  The reduced module sizes are
`(7,7,8,8)`.  Thus all twelve certified components are generically closed for
`H31`.  At this stage the new component's weighted `H22` fibre remained open;
the former statement that all known components were generically closed for
both types was a historical eleven-component checkpoint.

That last generic fibre is now closed by the binary-polarity cut:

- [`P5_H22_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md)

The repeated kernel rows `a,a` consume the merged and fifth channels in the
weighted `01` neighbor.  The remaining two rows restrict to

```text
(-t2,k*t3),       (t2,k*t3),
```

whose permanent is identically zero.  This is the exact pair
`(-X2+kX3)(X2+kX3)=0`, homogeneous in every merge weight, source scaling,
extension entry, and marking.  Hence all twelve certified components are now
generically closed for both `H31` and weighted `H22`.

The dense common-kernel/kernel-leaf orientation of the exceptional
`(2,1,1)` triangle is also empty:

- [`P4_COMMON_KERNEL_YY_211_TRIANGLE_OBSTRUCTION.md`](P4_COMMON_KERNEL_YY_211_TRIANGLE_OBSTRUCTION.md)

After synchronizing the exact pair, the seven kernel-containing cubics span
three columns `C0,C1,C2`.  If

```text
A=u*q+v*p,       Q=u*q-v*p,
```

their four maximal minors factor as

```text
8q*u*v*A,
8p*u*v*A,
4Q(E-2gamma*u*v),
4Q(E+2gamma*u*v).
```

On the dense binary torus, rank at most two forces `A=0` and `gamma=0`.
The first equation is the graph of the squarefree binary polarity, or
equivalently an exact zero-divisor relation `s*t=0`.  On that graph the
all-active cubic satisfies

```text
X=delta*C2-beta*(beta+r)*C0.
```

Thus it dies in every apolar quotient that kills the kernel-rich columns.
This closes the dense `YY` Borel orientation without enumerating graphs.
The mixed `YX` orientation is stronger still:

- [`P4_COMMON_KERNEL_YX_211_FACTORISATION_OBSTRUCTION.md`](P4_COMMON_KERNEL_YX_211_FACTORISATION_OBSTRUCTION.md)

Its synchronization equation is the factorization `b*d=a^2`.  A two-by-two
determinant `Delta` separates two branches.  If `Delta!=0`, both factors are
binary and the pair image has rank one.  If `Delta=0`, the factors are
reflections `B+s` and `lambda*(B-s)` with `s^2=0`; then

```text
lambda^(-1)*a*d+a*b-(b0+b1)*a^2=0
```

is a second pair relation.  The image has rank at most two, so no rank-three
`YX` edge exists anywhere on the genuine support-two exact-pair stratum.
Only the active `XX`, support-one common-zero-divisor, and lower-pair-rank
strata remain from this common-kernel split.

The active `XX` orientation is not empty.  It is controlled by an Eisenstein
norm quadric and supplies a thirteenth component:

- [`P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md`](P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md)

With `N(x,y)=x^2+xy+y^2`, the entire purity condition is

```text
N(alpha,gamma)=N(r+beta,beta).
```

After adjoining a primitive cube root of unity this is the determinant
`UV-ST=0`, so its projectivization is `P^1 x P^1`.  The affine radial
direction is already a block source scaling; the quadric contributes two
directions and the diagonal source torus contributes three.  At
`(alpha,beta,r,gamma)=(2,1,1,1)`, the exact family and incidence minors are
`1/864` and `-2/81`, giving a smooth five-dimensional component.  Its pure
restriction is identically `4*x0*x1*x2*x3` on the quadric.

The new component has the same coarse triangle profile as the first apolar
fivefold, but its two rank-one support labels coincide rather than being
adjacent in `J(4,2)`.  It has the same unmarked exact-pair support as the
eleventh component, but dimension and the reversed kernel/active incidence
separate them.  The certified component lower bound is now thirteen.  The
new component's generic `H31/H22` fibres are open at this checkpoint, so the
former twelve-component generic-closure theorem is now historical.

The thirteenth component's complete generic marked `H31` fibre is now empty:

- [`P5_H31_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md)

Projecting the norm quadric rationally from `(2,1,1,1)` gives the dominant
function-field chart `C(u,v)`.  Over
`C(u,v)[h0,h1,h2,h3]`, every deleted-coordinate mixed module satisfies

```text
A_j in Row(M_j),       B_j notin Row(M_j),
reduced module sizes (10,10,10,10).
```

At a generic rational chart point, the mixed ranks `(7,7,7,7)` are unchanged
by the all-kernel row and rise to `(8,8,8,8)` after adjoining the all-active
row.  Hence all thirteen certified components are generically closed for
`H31`.  Only the new weighted `H22` generic fibre remains before the earlier
known-component closure statement is restored at count thirteen.

That weighted fibre is now closed scheme-theoretically:

- [`P5_H22_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md)

For the weighted `01` neighbor, let `I_mix` be the ideal of the fourteen
mixed coefficients and `A,B` the two diagonal coefficients.  Over the full
ring

```text
C(u,v)[rho,h0,h1,h2,h3,x0,...,x3,y0,...,y3]
```

one exact reduction gives

```text
A*B in I_mix.
```

The reduced basis has size `48`.  This retains every special finite slope:
the mixed extension scheme is contained in `V(A) union V(B)` even where the
individual row-module obstruction switches branches.  The homogeneous
infinite-slope chart has the same product membership, with basis size `10`.
Thus all thirteen certified components are generically closed for both
`H31` and weighted `H22`.

The double-support-one boundary of the `(2,1,1)` triangle is now reduced
without elimination:

- [`P4_SUPPORT_ONE_211_TRIANGLE_REDUCTION.md`](P4_SUPPORT_ONE_211_TRIANGLE_REDUCTION.md)

Since `Ann_R1(X_i)=C X_i`, common-factor support-one orientations have leaf
pair-image rank at most two.  In the crossed orientation, distinct support
lines reduce the synchronizer to `p*q=X0*X1`.  Its only rank-three branch is

```text
p=P+s,       q=lambda*(P-s),       s^2=0.
```

The squarefree equation `s^2=0` forces one complementary coordinate, so all
three triangle planes lie in a coordinate `P^2`.  The Frobenius--Kunneth
decomposition then factors the four-mode tensor as a missing-coordinate
functional times a `P3` tensor.  Every pure survivor belongs to the embedded-
`P3` component.  The remaining support boundary has exactly one support-one
and one genuine support-two rank-one edge.

The earlier
quadratic-function-field experiments and their null outcomes remain
recorded as provenance:

- [`P5_H22_DIAGONAL_QUADRIC_WORKING_NOTE.md`](P5_H22_DIAGONAL_QUADRIC_WORKING_NOTE.md)

The five primes in the mixed determinantal chart are exhausted: they
map to the sixth component, the six-dimensional component, `L_2`, and
`L_1`, with no further orbit:

- [`P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md`](P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md)

The
nonzero preferred-chart divisor, first-plane Schubert boundary, and
internal `E=0` divisor of the first component are closed at complete
marked-fibre level:

- [`P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md)
- [`P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md)
- [`P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md)

## Priority

1. use the now-exhaustive twenty-five-component `P_4` ledger to close the
   explicit weighted-`H22` residuals on components twenty-two, twenty-three,
   and twenty-five, then the remaining special/projective fibres on
   components nineteen through twenty-five;
2. algebraically lift only the nonredundant high-overlap part of the
   six-blocker quotient catalogue.  Local maximal-overlap incidence is now
   exhausted in both exchanged-root coupling cases, and the exact global
   identity puts the endpoint `P_6` tensors in a rank-one GHZ hypercube.  Attack
   its companion cofactor corners; at order twelve these become synchronized
   rational `P_6` curves, while higher orders retain residual vertices.  Then
   move to five shared blockers or different ports;
3. compose the now-legal heralded symmetric lift of the root-of-unity
   four-row seed with the Question-2 module while keeping additional left
   modes live.  The fixed-left architecture is already excluded by
   `subrank(P_4)=2`;
4. formulate the simultaneous-root version of Route G in Grassmannian
   coordinates when the quotient lift exposes a small realizability stratum;
5. if the coupled selector survives all residual matchings and herald
   removal, test the four-channel selector and cut-rank formulation from
   Route F;
6. learn and prove sparse forbidden patterns with Route A;
7. use Route C if the survivor supports fall into few Grassmannian
   matroid strata;
8. use Route E only through exact matching-sector identities; do not infer
   anything from Gaussian recurrences involving unobserved sectors.

Route D's homogeneous degree-six scalar separator has been ruled out
exactly, and the full covariant ideal is empty through degree five.
Revisit this route only with a degree-six-or-higher non-invariant module
or a specific higher-degree invariant construction.  A full degree-six
covariant calculation is much larger than the eleven-dimensional
scalar-invariant slice and should not displace the support and
Grassmannian routes without a sharper representation-theoretic target.
