# Krenn--Gu literature and translation review (30 July 2026)

## Scope and evidence boundary

This review concerns the complex-weighted monochromatic quantum-graph
equation, not only ordinary edge-colourings with no cancellation.  The
target is

```text
T_W(a_1,...,a_n)
 = sum_(perfect matchings M)
     product_({i,j} in M) W_ij[a_i,a_j]
 = Delta_(n,d).
```

The global statement for even `n>=6,d>=3` remains open.  No source below
contains either a global counterexample or a global nonexistence proof.

## Primary problem and physics sources

1. Krenn, Gu, and Zeilinger,
   [Quantum Experiments and Graphs: Multiparty States as Coherent
   Superpositions of Perfect Matchings](https://arxiv.org/abs/1705.06646)
   (2017), identifies graph edges with pair sources and perfect
   matchings with coherent state terms.  This is the origin of the
   hafnian/matching-tensor formulation.
2. Krenn, Gu, and Soltész,
   [Questions on the Structure of Perfect Matchings inspired by Quantum
   Physics](https://arxiv.org/abs/1902.06023) (2019), gives the
   graph-theoretic inherited-colouring formulation and the original
   family of open questions.
3. Krenn's maintained
   [problem page](https://mariokrenn.wordpress.com/graph-theory-question/)
   records the prize problem and later public updates.  It is useful for
   provenance, but theorem claims here are checked against papers or
   proof artifacts where possible.

## Published combinatorial frontier

1. Chandran and Gajjala,
   [Edge-coloured graphs with only monochromatic perfect matchings and
   their connection to quantum
   physics](https://arxiv.org/abs/2202.05562) (2022/2023), classifies the
   cancellation-free `PMValid` colouring problem.  Its support
   structure is relevant, but arbitrary complex destructive
   interference is strictly more general.
2. Chandran, Gajjala, and Illickan,
   [Krenn--Gu conjecture for sparse
   graphs](https://arxiv.org/abs/2407.00303) (MFCS 2024), proves the
   conjecture for skeletons of vertex connectivity at most two and for
   cubic graphs, and shows a minimal counterexample must be
   four-connected.
3. The current Google DeepMind
   [`MonochromaticQuantumGraph.lean`](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/Paper/MonochromaticQuantumGraph.lean)
   formalizes the exact complete-graph equation system.  As checked on
   30 July 2026, its public registry still labels the complex
   `(n,d)=(6,3)`, `(8,3)`, and general even-order statements as open,
   while recording the `d=n` obstruction as solved.

## Results in this repository that go beyond that published frontier

Subject to the repository's exact replay artifacts and still needing
external mathematical review, the strongest additional claims are:

- exact complex nonexistence for six vertices and therefore every
  `d>=3` by colour restriction;
- several exact eight- and ten-vertex support/skeleton exclusions;
- arbitrary-order blocker, balanced-bridge, and reciprocal-port
  obstruction theorems;
- a complete exact-three-coordinate obstruction for
  `P_5 -> Delta_3`;
- exact exclusions of normalized `q5_311`, `q5_221`, and `q4_211`;
- at least nine inequivalent components of the pure rank-two
  `P_4`-compression variety.  Generic `H31` and generic weighted
  `H22` fibres are empty on all nine.  The complete marked projective
  `H31` fibre of the embedded-`P_3` ninth component is empty, while its
  weighted `H22` obstruction currently covers the full normalized
  affine chart rather than every projective boundary.  On the eighth
  component the equal-
  and opposite-weight `H22` fibres are additionally empty already at
  the binary-incidence level, twelve generic parameter/coordinate
  branches are empty by exact Fitting ideals, and the principal
  coupled slope-parameter divisor is empty by a cross-mode minor.  An
  intrinsic maximal-minor content calculation further closes the four
  rational sheets `af=+/-1,a phi=+/-1`; on those sheets the `D_23`
  binary incidence itself is generically empty.  A second intrinsic
  content ledger closes the compactified slope endpoint `r=0`: `D_01`
  fails already at binary level, while the rank-six `D_23` degeneration
  fails a two-minor marked-rank test.  Normalizing a further coefficient
  divisor exposes a new irreducible quadratic component branch; full
  unsplit Fitting ideals exclude both weighted directions there.
  Three further rational slope graphs are excluded by six unsplit
  identities; one graph has a genuine mode-zero degeneration repaired
  by a fixed mode-one minor.  An exact source-torus quotient reduces
  the dense component base to a two-dimensional surface while
  preserving both weighted slopes.

The first item is stronger than the currently cited paper frontier and
than the status labels in the current public formal-conjectures file.
It should therefore be presented as a repository computer-assisted
theorem, not silently attributed to those authors and not treated as a
peer-reviewed global result.

## Translating the problem into other mathematical languages

| Original surface | Translated object | Tool exposed |
|---|---|---|
| coherent sum over perfect matchings | coloured hafnian / matching tensor | tensor contractions, flattenings, subrank |
| one photon in each spatial mode | projected bosonic Gaussian state / transversal Wick moment | Gaussian moment identities and hafnian geometry |
| local colour changes | `GL(d)^n` tensor restriction | representation theory and invariant/covariant modules |
| deleted roots and blockers | restrictions of permanent tensors `P_k` | apolarity, Frobenius algebras, zero-product geometry |
| existence of a binary neighbour | rank drop of a `14 x 8` matrix | determinantal varieties and Fitting ideals |
| pure tensor target | Segre variety | secants, tangents, incidence geometry |
| local two-planes | points of `Gr(2,4)` | Plücker coordinates and matroid strata |
| support cancellations | binomial/toric relations | lattice ideals and circuit elimination |
| several simultaneous roots | multihomogeneous zero loci in products of projective planes | Chow rings and intersection numbers |
| blocker allocation | transversal problem | Hall-type and matroid-intersection inequalities |
| mode/colour symmetry | finite group action | orbit normal forms and equivariant stratification |
| rank-two pair image | line meeting the `2 x 2` rank-one Segre quadric | Kronecker pencils, secant/tangent normal forms |
| triangle of rank-two pair relations | `PGL_2` connection plus degree-two catalecticants | holonomy, tetrads, and weighted cuts |
| three full-support `1+3` bridges | singleton cut labels plus coordinate-hyperplane intersections | factorization sheets, cut compatibility, perfect pairing |
| a full-support `2+2` bridge | two hyperbolic binary planes | anchor sheets versus crossed-graph partners |
| a proper cut support | coordinate Schubert incidence | suspension to `P_3` and Poincare pairing |
| trivial projective triangle holonomy | affine local system on a cycle | additive cohomology, tangent jets, binary cubics |

The determinantal step used in the new `H22` theorem is standard Fitting
geometry: rank-drop loci are cut out by minors, and the construction is
stable under base change.  See the Stacks Project,
[Fitting ideals, Section 15.8](https://stacks.math.columbia.edu/tag/07Z6).

The tensor-subrank translation also has a mature algebraic-complexity
literature.  Useful orientation includes Kopparty--Moshkovitz--Zuiddam,
[Geometric rank of tensors and subrank of matrix
multiplication](https://arxiv.org/abs/2002.09472), and
Derksen--Makam--Zuiddam,
[Subrank and Optimal Reduction of Scalar Multiplications to Generic
Tensors](https://arxiv.org/abs/2205.15168).  Those papers do not solve
the Krenn--Gu restriction problem, but their monotonicity and
rank-variety viewpoint is the right language for turning local
permanent restrictions into invariant obstructions.

Two further translations are especially relevant to the present
frontier.

First, Wick's theorem identifies the coloured matching tensor with a
block-transversal moment of a centered formal Gaussian family:

```text
T_W(a_1,...,a_n)
 = E[X_(1,a_1) ... X_(n,a_n)],

E[X_(i,c) X_(j,e)] = W_ij[c,e].
```

Equivalently it is the one-photon-per-spatial-mode sector of a bosonic
Gaussian state.  Hamilton et al.,
[Gaussian Boson Sampling](https://arxiv.org/abs/1612.01199), establish
the direct Gaussian-output/hafnian correspondence.  This recasts the
prize problem as an intersection between a projected Gaussian moment
variety and the `GL(d)^n` orbit of the diagonal (GHZ) tensor.  The
identification is algebraic: arbitrary complex edge weights need not
be a positive covariance matrix.  Gaussian positivity arguments
therefore do not apply automatically, but Wick recurrences, moment
varieties, and invariant theory do.

Second, the unclassified rank-two pair boundary is a matrix-pencil
problem.  De Teran--Dopico--Landsberg,
[An explicit description of the irreducible components of the set of
matrix pencils with bounded normal
rank](https://arxiv.org/abs/1606.02574), organize bounded-normal-rank
pencils by Kronecker type.  De Seguins Pazzis,
[Large spaces of bounded rank matrices
revisited](https://arxiv.org/abs/1507.05375), supplies the broader
compression-space viewpoint.  Most directly, the February 2026 paper
of Bernardi--Gesmundo,
[Triangular tensor networks, pencils of matrices and
beyond](https://arxiv.org/abs/2602.15114), characterizes
low-physical-dimension triangle networks by Kronecker invariants and
extracts equations from coincident-root and determinantal geometry.
That paper does not treat the squarefree permanent restriction here,
but its organizing language matches the repository's remaining
exceptional triangle almost exactly.

The cut output has a second neighboring literature.  Sturmfels and
Sullivant,
[Toric geometry of cuts and splits](https://arxiv.org/abs/math/0606683),
organize graph cuts and split systems by toric relations.  Cohen and
Orlik,
[Arrangements and local systems](https://arxiv.org/abs/math/9907117),
relate multiplicative local-system behavior to resonance loci of
arrangements.  Neither paper contains the repository's obstruction,
but together they suggest separating discrete cut labels from the
holonomy divisor.  That separation yields
[`P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md):
a full `1+3` bridge factors either internally or by a fully supported
sign reflection.  Coordinate-hyperplane annihilators exclude the
reflection sheet, force all three singleton labels to agree, and then
the perfect `R_2 x R_1 -> R_3` pairing drops the alleged rank-three
triangle to the embedded-`P_3` boundary.

The complementary `2+2` calculation uses the same bounded-rank pencil
language more literally.  A full cut `q=ab` has an anchor in every
linear factorization, while every rank-three partner of
`Ann(q)=span(a_bar,b_bar)` is an off-diagonal graph avoiding both
anchors.  Their incidence is empty:
[`P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md).
Combined with the `1+3` theorem, this empties the entire full-support
nonresonant triangle.  The support boundary itself has only one-edge
and two-edge normal forms.  The first collapses the partner product to
rank one; the second transports one coordinate hyperplane around the
triangle and suspends a pure `P_3`, whose Poincare pairing forces rank
at most two:
[`P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md).
Thus the complete nonresonant triangle is empty, leaving only trivial
holonomy.

That remaining divisor has a second, affine holonomy.  Normalized edge
relations carry constants `A_ij`, changed by vertex potentials, and
their unique cohomology class is
`delta=A_12+A_23-A_13`.  A nonzero class produces a
tangent-Segre tensor and a cyclic system of kernel cuts; the zero
class synchronizes the local bases and factors multiplication through
`Sym^3(C^2) -> R_3`:
[`P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md`](P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md).
This is where arrangement local systems, tangent developables, and
binary-form geometry meet the squarefree permanent problem.

This translation already gives a new exact repository theorem:
[`P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md`](P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md).
For a pair of local two-planes whose product image has rank two, the
projective kernel is a line in `P^3`.  The rank-one relations form the
Segre quadric.  The kernel line cannot be a ruling because a nonzero
linear form in the squarefree algebra has annihilator dimension at
most one.  Its only possibilities are therefore a secant, forcing a
`2+2` or `1+3` block center, or a tangent, forcing coincident planes
through a coordinate line.  Tangency at a genuine two-coordinate
zero product would make the pair-image rank one and is therefore
excluded.

## What the review changes strategically

The published graph-theoretic papers extract strong consequences from
support and connectivity, but they do not classify cancellation
varieties over `C`.  The repository's most productive symbolic route
has instead been:

```text
matching graph
 -> hafnian tensor
 -> deleted permanent restriction
 -> squarefree apolar algebra
 -> Grassmann/Fitting incidence
 -> a few exact minors.
```

The new weighted `H22` theorem is a clean example.  A broad
extension-variable elimination had timed out.  Passing first to the
Fitting scheme of the mixed matrix turns one direction into a line and
the other into a degree-five scheme; three factor charts and two small
minors then finish the generic component.

The next high-value translation is not a larger graph search.  It is a
Kronecker classification of the three compatible pair pencils in the
remaining exceptional triangle, followed by the global classification
of the pure `P_4` compression variety as an orbit/degeneracy-locus
theorem in `Gr(2,4)^4`.  Coincident-root loci from triangular tensor
networks and Gaussian/Wick covariants are the two most promising
sources of symbolic equations.  A simultaneous-root Grassmannian
formulation of the blocker hierarchy remains the arbitrary-order
follow-up.

That triangle translation has now produced a second exact reduction:
[`P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md`](P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md).
The three rank-two relation matrices carry a multiplicative
projective holonomy.  Away from the trivial-holonomy divisor, basis
shifts remove their three constant terms and force all six mixed
triple products to vanish.  The three surviving cross-products have
rank-two zero-diagonal catalecticants and therefore lie on
`1+3`/`2+2` cut strata.  The `2+2` equation is a tetrad, connecting
the residual compatibility problem to algebraic statistics and trek
separation rather than to a larger permanent ideal.

Following the common `1+3` cut instead of discarding the pair-rank
drop exposes a ninth component:
[`P4_EMBEDDED_P3_PURE_COMPONENT.md`](P4_EMBEDDED_P3_PURE_COMPONENT.md).
It is the one-coordinate suspension of the already classified pure
`P_3` sign chart.  The construction is six-dimensional and a rational
rank-fourteen Segre-incidence certificate proves that its closure is
a component.  Its pair-rank multiset `{2,2,2,4,4,4}` separates it
from the earlier six-dimensional component.  This is a concrete
example of a lower-rank boundary carrying more geometry than the
dense stratum that led to it.

Its generic marked `H31` fibre then collapses through a second
cross-specialty translation:
[`P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md).
The squarefree algebra is an Artinian Gorenstein complete
intersection, so the extension map is a first variation of
multiplication and its exceptional directions form a Lefschetz-style
degeneracy locus.  The relevant `7 x 6` presentation is even more
rigid than a generic determinantal matrix: its maximal minors have
support equal to three signed projective lines plus three coordinate
points.  At a generic point of each line, the sole syzygy is one of
the pure-`P_3` factor covectors and therefore annihilates the required
all-alpha diagonal.  This gives a binary-level obstruction for every
marking over the generic component point.

The closest literature neighbors are the characterization of
Lefschetz elements in Artinian Gorenstein algebras by higher Hessians
([Maeno--Watanabe](https://arxiv.org/abs/0903.3581)) and the conversion
of arrangement ideals into combinatorially controlled subspace
arrangements and syzygies
([Denham--Steiner](https://arxiv.org/abs/2112.13462)).  Neither result
is imported as a black box; together they suggest the successful
order of operations: find the Fitting support and its kernel sheaf
before eliminating marking variables.

The weighted `H22` fibre needs no new elimination:
[`P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md).
One weighted diagonal map preserves the suspended coordinate and hence
has an identically zero all-alpha coefficient.  The other merely
moves the projected mode-zero line from
`P span((1,S,U),(0,1,T))` to
`P span((1,S,U),(r,1,T))`.  Its intersection with the same
arrangement is controlled by nine point-line determinants.  Thus the
kernel-sheaf calculation closes both generic marked types on the
ninth component and raises the generic `H31/H22` closure count from
eight to all nine currently known component orbits.

The insertion arrangement also makes its own boundary tractable:
[`P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md).
At its nine singular/projective points, exact kernel vectors replace
elimination.  Requiring the second slice to be diagonal is just a
truncated `2 x 2 x 2` Segre test; its three quadratic relations factor
into signed lines.  Only five binary families survive.  Four have
transverse one-marked rank four, and the unique rank-three/rank-three
point is killed by a stacked determinant `8`.  This closes the entire
normalized `H31` chart and illustrates the broader strategy:
degeneracy support first, kernel sheaf second, compatibility last.

The weighted boundary confirms that this order is not merely generic:
[`P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md`](P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md).
Intersecting the moving projected line with the arrangement leaves
four symbolic strata and six marked families.  Their obstructions are
factor covers by tiny one-marked determinants, except at two deepest
points where the appropriate object is a stacked source map with
constant determinants `8` and `-8`.  This is naturally read as a
kernel-sheaf gluing problem: local Fitting generators may vanish while
two source directions still generate the full fibre.

The qualitatively different collapse `rS=1,T=rU` is now closed too:
[`P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md`](P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md).
Instead of taking a non-flat limit of the first line arrangement, use
the second marked contraction required by `H22`.  It becomes a
`7 x 6` matrix pencil with maximal minors supported only at
`S=+/-1`.  At one Kronecker-type singular fibre the kernel annihilates
the required pure coefficient; at the other it has no alpha-extension
direction and annihilates the first slice's diagonal.  This matches
the invariant-first philosophy of basis-free matrix-pencil reduction
([Verdier](https://arxiv.org/abs/1205.1138)) and minimal pencil ranks
([Goulart--Comon](https://arxiv.org/abs/1712.05742)): identify the
singular fibres and kernel covectors before solving coordinates.  The
payoff here is a full normalized-chart theorem, not merely a generic
or rank-two statement.

The first omitted normalization divisor is now closed in the same
language:
[`P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md).
On `A=0`, `B!=0`, the pure sign chart loses one support coordinate and
the insertion presentation acquires a zero row.  Its Fitting support
nevertheless has only one genuine branch, `rho=-Cp`.  The branch is
generically excluded by a one-marked determinant; at its coordinate
endpoint the third root contraction leaves the covector `(C+1)X`, so
only the pencil resonance `C=-1` survives.  That fibre splits into
two invariant kernel types and closes by small factor covers, one
stacked determinant, and a fixed coefficient `4`.  This is a useful
warning from matrix-pencil theory: the residual source-torus scalar
is Kronecker data, not a normalization nuisance, and setting it to
one would hide the only resonance.  The result closes this support-two
divisor, but not by itself the other mode-zero-plane chart or the
projective compactification.

The complementary mode-zero-plane chart is now closed in
[`P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md).
Its open `t!=0` part is transported to the normalized theorem by the
signed source permutation `X_2'=-X_3,X_3'=-X_2`.  At the genuine
corner `r=t=0`, the insertion tensor is a first variation of the
rank-one `P_3` restriction.  Binary diagonality asks that tangent
tensor to meet the secant line through `AAA,BBB`; the resulting mixed
determinant is three signed planes times one residual multiaffine
factor.  This is exactly the sort of tangent--secant translation
suggested by the rank stratification of tangential Segre varieties
([Ballico--Bernardi](https://arxiv.org/abs/1210.7976)) and the broader
secant/tensor dictionary
([Bernardi et al.](https://arxiv.org/abs/1812.10267)).

The geometry does more than rename an elimination.  The three signed
planes have a single nongenuine kernel until a `6 x 5` Fitting
presentation drops rank; its maximal minors split into only nine
families.  The residual sheet has a three-minor cover, and its five
singular base points leave nine sparse families.  Thus the whole
affine `B!=0` ninth-component chart is now empty for `H31`.

Finally, the apparent projective boundary disappears after using the
correct compactification:
[`P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md).
The absolute sign-rectangle normal is a point `[C:A:B] in P^2`.
Support-one points are zero restrictions.  Every support-two or
support-three point has two nonzero coordinates, which source symmetry
moves into the already closed chart `C'B'!=0`.  This is the
oriented-matroid/toric support viewpoint anticipated by the
second-hypersimplex dictionary
([Herrmann--Joswig](https://arxiv.org/abs/0804.2897)): glue Pluecker
charts by support, not by taking limits of inverse pivot variables.
Consequently the ninth component is now closed in full for `H31`.

The same “translate before eliminate” principle now closes the
nonzero additive-holonomy part of the resonant rank-two triangle:
[`P4_RESONANT_NONZERO_ADDITIVE_HOLONOMY_OBSTRUCTION.md`](P4_RESONANT_NONZERO_ADDITIVE_HOLONOMY_OBSTRUCTION.md).
The affine connection first becomes a tangent-Segre jet; its three
kernel-pair products then become cut quadrics.  The obstruction is
not a tangent-rank calculation by itself.  It passes through the
classification of squarefree cut supports, the anchor geometry of
`2+2` quadrics, and finally the Frobenius perfect pairing of the
three-variable squarefree complete intersection.  This closes the
tangent branch and leaves only the flat synchronized binary cubic.

The flat branch crosses into three classical neighboring subjects.
First, its generic row-pair is a labelled four-point configuration on
`P1`, so projective normalization leaves one cross-ratio.  Second,
synchronization makes every other row-pair lie in a
two-dimensional matrix pencil.  Treating the missing affine sheets as
genuine pencil-closure strata follows the bundle/closure viewpoint of
[De Teran--Dopico](https://arxiv.org/abs/2204.10237), rather than
discarding them as bad coordinates.  Third, the Hamming-weight
products `Y,K,J,X` are the osculating coefficient flag of a binary
cubic.  This sits next to classical binary-cubic equivalence
([Cremona](https://arxiv.org/abs/2212.02120)), osculating Veronese
geometry
([Bernardi--Catalisano--Gimigliano--Ida](https://arxiv.org/abs/0807.2455)),
and determinantal/catalecticant descriptions of Veronese secants
([Buczynska--Buczynski](https://arxiv.org/abs/1012.3563)).

The repository-specific payoff is the exact identity

```text
C_3([Y K J X])=8F N:
```

the compression minor forces `F=0`, after which every cofactor
vanishes although `X` is required to escape the compressed plane.
The projective pencil sheets obey smaller versions of the same
identity.  A targeted review found the surrounding languages above,
but not this particular squarefree-permanent cofactor factorization.

The collision compactification then needs no elimination.  Zero
columns descend to `P3`; the `2+1+1` collision kills the active cube;
the `1+3` split drops the pair rank; and the balanced `2+2` split gives
the sole canonical survivor.  Its source-torus orbit has dimension at
most four, below the five-dimensional minimum for a nonzero
pure-incidence component.  Thus the complete rank-two-relation
triangle is no longer a possible generic missing-component graph:
[`P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md`](P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md),
[`P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION.md`](P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION.md).

The same pencil has a second use: it closes a star of rank-two
relations in
[`P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md`](P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md).
The relevant object is not a large permanent ideal but the
rank-drop graph on the pencil parameter line.  Its three Kronecker
degeneracy pairs are disjoint, so the graph is a matching; three
leaves necessarily contain a rank-three pair and close the forbidden
triangle.  This is a concrete instance of the bounded-normal-rank
pencil organization developed by
[De Teran--Dopico--Landsberg](https://arxiv.org/abs/1606.02574).
On the balanced collision, even that language collapses to one
intersection-number calculation: the forbidden coefficient is
`a^2b^2=4`.

The next mixed triangle is controlled not by another pencil
classification but by the annihilator of a linear form in the
squarefree complete intersection:
[`P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md`](P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md).
Two rank-two edges again create a synchronization pencil.  On the
only nonautomatic `2+2` collision, a full-support kernel row has zero
linear annihilator, while a two-supported row has one annihilator
line that misses the other leaf plane.  This is the smallest-degree
shadow of the Lefschetz behavior of characteristic-zero monomial
complete intersections; for the broader theorem see
[Phuong--Tran](https://arxiv.org/abs/2211.13548).  Here the exact
support-sensitive statement is elementary and stronger for the local
incidence: it excludes relation-rank pattern `(2,2,1)` outright.
