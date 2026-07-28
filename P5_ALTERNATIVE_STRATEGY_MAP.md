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
remaining `P_5` problem is now the structurally distinct branch in which
some local map has four or five coordinate rows.

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
Therefore the `d=n` formal proof does not bypass the remaining problem:
in the three-colour regime it reduces exactly to the need to propagate
blocker surplus across several roots.  The useful next experiment is to
apply the contraction at two or three roots simultaneously and express
the resulting compatibility as a Grassmannian incidence condition,
linking this route to Route C without choosing row-support charts.

## Priority

1. enumerate and learn sparse obstructions for the exact-four-partial
   layer without materializing all labelled supports;
2. formulate the simultaneous-root version of Route G in Grassmannian
   coordinates;
3. test the four-channel selector and cut-rank formulation from Route F;
4. learn and prove sparse forbidden patterns with Route A;
5. use Route C if the survivor supports fall into few Grassmannian
   matroid strata;
6. keep Route E as a source of identities, but require a
   postselection-only elimination before investing in it.

Route D's homogeneous degree-six scalar separator has been ruled out
exactly, and the full covariant ideal is empty through degree five.
Revisit this route only with a degree-six-or-higher non-invariant module
or a specific higher-degree invariant construction.  A full degree-six
covariant calculation is much larger than the eleven-dimensional
scalar-invariant slice and should not displace the support and
Grassmannian routes without a sharper representation-theoretic target.
