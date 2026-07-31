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
- at least ten inequivalent components of the pure rank-two
  `P_4`-compression variety.  Generic `H31` and generic weighted
  `H22` fibres are empty on the nine components known before the new
  two-rank-two-spoke mixed star; its marked fibres are unclassified.  The
  complete marked projective
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

The flat branch crosses into three classical neighboring subjects,
but with a crucial marked-point refinement.  Purity fixes a kernel
line, so the relevant moduli problem is four affine ratios modulo the
affine group, not four unmarked points modulo full `PGL_2`.
Synchronization still makes every other row-pair lie in a
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

An earlier collision compactification used full `PGL_2` and therefore
moved this marked kernel line.  Its claimed complete triangle
classification, the star theorem depending on it, and the
balanced-chart part of the mixed `(2,2,1)` theorem were withdrawn:
[`P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION_WITHDRAWN_OVERSTRONG.md`](P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION_WITHDRAWN_OVERSTRONG.md),
[`P4_RANK_TWO_RELATION_STAR_OBSTRUCTION_WITHDRAWN_OVERSTRONG.md`](P4_RANK_TWO_RELATION_STAR_OBSTRUCTION_WITHDRAWN_OVERSTRONG.md),
[`P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION_WITHDRAWN_PENDING_BOREL_AUDIT.md`](P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION_WITHDRAWN_PENDING_BOREL_AUDIT.md).
Their pencil-matching and annihilator calculations remain useful local
lemmas, connected respectively to bounded-normal-rank pencils
([De Teran--Dopico--Landsberg](https://arxiv.org/abs/1606.02574))
and Lefschetz behavior of monomial complete intersections
([Phuong--Tran](https://arxiv.org/abs/2211.13548)), but they do not
by themselves support the advertised global scopes.  Corrected marked
replacements for all three now appear below.

Keeping the marked kernel instead yields the true generic normal form

```text
y=(1,1,1,1),       x=(0,1,p,q).
```

Its synchronizer is again a two-dimensional pencil, now over the
two-dimensional affine-ratio moduli.  The binary-cubic coefficient
matrix has a common biquadratic cofactor `F`; purity forces `F=0`,
all `3 x 3` minors then vanish, and three small `K,J` minors prevent
the compressed span from becoming a line.  This repairs the generic
theorem without moving the flag:
[`P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md`](P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md).
The one-kernel-zero otherwise-distinct chart remains valid as a
separate boundary theorem:
[`P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md`](P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md).

The projective pencil closure over the distinct-ratio center is now exact:
[`P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md`](P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md).
With one partner at infinity, the pure binary-cubic incidence is the union
of three rational curves.  In the marked affine ratios
`(r_0,r_1,r_2,r_3)=(0,1,p,q)`, they are precisely

```text
r_0+r_3=r_1+r_2,       r_0+r_2=r_1+r_3,       r_0+r_1=r_2+r_3.
```

Thus the missing sheet is indexed by the three perfect matchings of four
points and detects exactly a failure of the weak Sidon condition (distinct
sums of disjoint pairs).  This additive-combinatorial formulation is
invariant under the legal affine gauge and explains the three factors
before elimination.  The standard distinct-pair-sum language appears, for
example, in Lee,
[On Sidon sets in a random set of vectors](https://arxiv.org/abs/1405.4227).

The more consequential identity is the bridge back to pencil geometry:
on each additive-parallelogram curve, the product image of the infinite
partner with its finite neighbor has rank exactly two.  Hence every pure
point leaves the all-rank-three-relation triangle and lands on the
Segre/Kronecker seam classified by the pair-kernel theorem.  With both
partners at infinity, two incompatible confluent minors make the pure sheet
empty.  The review found the separate ingredients--Sidon collisions,
osculating binary forms, and bounded-rank pencil closures--but not this
specific implication among them.

The full-support collision strata now have an equally small foreign
description:
[`P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION.md`](P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION.md).
For `2+1+1` and `3+1`, the synchronizer remains a pencil but its point at
infinity is a rank-one local map.  Every admissible partner keeps one common
active row, whose squarefree cube vanishes because its support has size at
most two.  This is a zero-divisor argument in the Artinian complete
intersection, not an incidence elimination.

For `2+2`, the synchronizer jumps to a projective plane.  Multiplication
induces a degenerate alternating form with the center as its radical, so
mutually synchronized triples are exactly projective lines through that
radical.  This is the elementary three-dimensional edge of projective
symplectic/c-polar geometry; compare Prazmowska--Prazmowski--Zynel,
[Projective symplectic geometry on regular subspaces](https://arxiv.org/abs/1203.2053).
On each such line, purity leaves four signed points.  All four have a
rank-two noncentral pair and hence cross immediately into the
Segre/Kronecker boundary.  Projective endpoints are empty.  Combining the
presymplectic collision theorem with the finite/projective distinct-ratio
theorems excludes every full-kernel-support flat rank-three-relation
triangle.  Only smaller kernel supports remain in that branch.

The smaller supports change the conclusion from obstruction to
classification:
[`P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md`](P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md).
After zero-column descent to `P_3`, the kernel-support stratification has
only one survivor.  On complementary binary blocks choose opposite
zero-product directions `a,a_bar` and `b,b_bar`.  Then

```text
U_0=span(b_bar,a_bar),
U_i=span(a,b+alpha_i a_bar),
```

and the restriction has the single coefficient
`-4(sum alpha_i)x_0x_1x_2x_3`.  Every leaf pair has image rank three and its
unique relation has matrix rank two.  Conversely, the corrected Borel
support analysis proves that every such exceptional triangle has this
form.

This is the cleanest payoff so far from crossing specializations.  The
affine-holonomy language reduces to a binary cubic; presymplectic geometry
classifies its synchronizer jumps; the Frobenius annihilator pairing forces
the fourth plane; and the remaining polynomial is merely the first
elementary symmetric function of three line parameters.  The resulting
annihilator-line normal form was not found in the neighboring pencil,
symplectic, binary-form, or Lefschetz sources.  A previously displayed
two-parameter balanced family was only the `alpha_i=0` slice seen after an
illegal full-row normalization; the new theorem recovers the complete
three-parameter marked family without moving a kernel line.

That corrected survivor is now the valid input to a repaired star theorem:
[`P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md`](P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md).
The adjugate-pencil rank-drop graph is a matching of three edges, so three
leaves over a four-distinct center contain a rank-three pair; the corrected
triangle then forces a support-two kernel, contradicting a support-three or
support-four center.  The genuinely new chart is the full-support `2+2`
presymplectic plane.  Center-leaf rank three makes every radical coefficient
nonzero, after which two kernel-marked permanent words are `-4E` and
`-4(E-1)`.  They cannot both vanish.  The support-two charts close by the
constant annihilator product `a^2b^2=4X_0X_1X_2X_3`.

This illustrates why the neighboring subjects must be used in sequence:
Kronecker roots control which leaves can be paired, the corrected
binary-cubic theorem identifies that pair, presymplectic geometry handles
the dimension jump, and the Artinian annihilator product supplies the final
constant.  None of the literature sources alone states the star
obstruction in this marked squarefree setting.

The mixed `(2,2,1)` triangle is now repaired by one further translation:
[`P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md`](P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md).
Two rank-two edges put both leaves in the center's synchronizer variety.  All
ordinary two-dimensional pencils are totally isotropic, so their leaf edge
already has an alternating, coefficient-rank-two relation.  The only new
case is the full-support `2+2` collision, where the synchronizer is the
three-dimensional presymplectic space described above.

In marked coordinates the alternating pairing of two leaves is

```text
Delta=r_2s_3-r_3s_2.
```

Four product-image Pluecker coordinates are `Delta` times two signed pairs.
On the rank-drop locus, assuming `Delta!=0` makes the signed differences
force `r_2+r_3=s_2+s_3=0`, hence `Delta=0`, a contradiction.  Thus every
rank-three leaf pair on this locus lies on an isotropic line through the
radical, and its unique relation is the nonsingular alternating matrix.

This is a small instance of a general principle in projective symplectic
geometry: rank conditions on product images can force incidence with the
radical before one solves the ambient equations.  The neighboring literature
supplies the polar-space language, while the squarefree pair-image minors
make the radical incidence exact here.  The review found no source stating
this marked `(2,2,1)` obstruction.  The remaining graph-theoretic boundary is
not this pattern but triangles with only one rank-two edge, other mixed-star
patterns, and lower pair-image ranks.

The first of those “other” mixed stars is not an obstruction but a new
component:
[`P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md`](P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md).
Two rank-two spokes again place two leaves in the full-support `2+2`
synchronizer plane.  A star requires their presymplectic determinant to be
nonzero, the opposite of the triangle rank-drop condition above.  A third
rank-one spoke pins its pure kernel to the complementary binary annihilator.
The fifteen purity equations then reduce to one nonzero coefficient and the
rational law

```text
d=(1+st)/(s+t).
```

The Cayley transformation `c(z)=(z-1)/(z+1)` conjugates this to

```text
c(d)=c(s)c(t).
```

So the surviving compatibility surface is a toric multiplication graph, not
an unexplained determinantal residue.  Its five-dimensional diagonal-source
orbit is smooth on the universal Segre incidence at `(s,t)=(2,3)`, proving a
tenth component orbit.  The use of a radical alternating form places the
construction near projective symplectic geometry.  For the broader neighboring
language of degenerate alternating-form flag geometry, compare Boos,
Cerulli Irelli, Fang, and Fourier,
[Linear degenerate symplectic flag varieties](https://arxiv.org/abs/2405.02739).
That literature does not state the squarefree permanent component or its
`(2,2,1)` relation-rank invariant.

The reverse normal-form calculation is now complete as well:
[`P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md`](P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md).
The ordinary Kronecker pencils are totally isotropic and cannot give a star
with full leaf-pair rank.  In the full-support presymplectic chart, four
linear syzygies among the purity coefficients force the signs `r_1=-r_2=1`
and the Cayley product law.  In the only other dimension-jump chart, the
squarefree annihilator pairing forces the fourth plane to
`span(a_bar,b_bar)`, where the center-pair image has rank two.  Thus the
toric family is the entire dense `{1,2,2}` star stratum, not just a component
inside it.  This exact passage from Kronecker type to presymplectic radical to
torus group law is the classification mechanism absent from the neighboring
literatures when considered separately.

The final remaining generic graph shape already contains the repository's
first component, but its old coordinates obscured that fact.  The new apolar
normal form is
[`P4_FIRST_COMPONENT_APOLAR_TRIANGLE_NORMAL_FORM.md`](P4_FIRST_COMPONENT_APOLAR_TRIANGLE_NORMAL_FORM.md).
Two overlapping binary zero products and one synchronized edge reduce the
triangle to a factorization of a fixed three-term squarefree quadratic.  Its
dense factorization has only one apparent parameter, removed by the unused
source-coordinate torus.  Of the eight triple products, only the all-kernel
and all-active covectors survive.  The opposite plane is therefore a point of

```text
Gr(2,ker(all-kernel covector))=Gr(2,3)=P^2.
```

This is a concrete Macaulay-duality/apolarity description of the first
component: a fixed triangle, an apolar projective-plane fibre, and the source
torus.  It is adjacent to the higher-Hessian characterization of Lefschetz
elements in Artinian Gorenstein algebras by Maeno--Watanabe
([arXiv:0903.3581](https://arxiv.org/abs/0903.3581)), but the exact
squarefree-quadratic factorization and exceptional-graph interpretation are
specific to this problem.  Other Borel orientations of the `{1,1,2}` triangle
remain to be compared with known star and lower-rank component closures.

The crossed Borel orientation of that triangle is now classified on the
whole genuine support-two stratum:
[`P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md`](P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md).
A binary zero product is an opposite signed pair
`(X_i+X_j)(X_i-X_j)=0`; its support is an edge `{i,j}` of `K_4`.  The six
supports therefore form the octahedron `J(4,2)=L(K_4)`, or equivalently the
support shadow of the `D_4` root arrangement.  Equality, opposition, and
adjacency of two octahedron vertices give the complete support trichotomy.
Equal labels force a coordinate-hyperplane Schubert boundary.  Opposite
labels turn the remaining factorization into a rank-one `K_(2,2)` block and
force either an anchor plane collapse or a second pair relation.  Adjacent
labels turn it into a triangle-supported quadratic whose unique dense
factorization is the fixed apolar component.

There is a useful matrix-completion reformulation.  Multiplication of
degree-one vectors `u,v` records the off-diagonal part of
`uv^T+vu^T`; the free diagonal is exactly the squarefree quotient.  The
three support branches are free-diagonal completions of weighted adjacency
matrices supported on `K_2`, `K_(2,2)`, and `K_3`.  Kiraly, Theran, and
Tomioka develop the local algebraic-matroid view of low-rank completion
([arXiv:1211.4116](https://arxiv.org/abs/1211.4116)), while Bernstein,
Blekherman, and Lee study symmetric completion ranks determined by graph
patterns ([arXiv:1909.06593](https://arxiv.org/abs/1909.06593)).  Their
frameworks explain why the observation graph should matter; neither contains
the marked squarefree factorization or its Borel orientation.

The same binary pairs are homogeneous zero divisors in an Artinian algebra.
Kustin, Striuli, and Vraciu obtain Hilbert-function restrictions from exact
pairs ([arXiv:1304.0411](https://arxiv.org/abs/1304.0411)).  Here the stronger
degree-one annihilator bound decorates each pair by a `D_4` support label.
Combining that finite incidence geometry with low-rank completion and then
Macaulay duality is what produces the classification.  This synthesis seems
stronger for the present local problem than any one neighboring
specialization by itself.

The equal-support common-factor orbit then gives the opposite answer: it is
not obstructed but component-sized.  Its exact normal form and smoothness
certificate are in
[`P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md`](P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md).
The shared pair `a a_bar=0` gives the two-periodic complex

```text
... -> R --a_bar--> R --a--> R --a_bar--> R -> ...,
```

and the rank-two edge becomes the affine synchronization law
`x_2-x_1 in Ann(a)=(a_bar)`.  This leaves a genuine translation modulus.
Holm's construction of totally reflexive modules from exact zero-divisor
pairs ([arXiv:1002.0419](https://arxiv.org/abs/1002.0419)) is the nearest
homological language, while Tran--Skoldberg compute Hochschild cohomology for
square-free monomial complete intersections
([arXiv:1806.07802](https://arxiv.org/abs/1806.07802)).  Neither predicts the
permanent family.  Here the one-dimensional kernel-cubic span has a `P^2`
apolar opposite-plane fibre; adjoining the affine synchronization parameter
and source torus produces a smooth sixfold.  This raises the certified
component lower bound to eleven.

The tenth component's generic `H31` obstruction adds a module-theoretic
translation:
[`P5_H31_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).
The four marking parameters form an affine chart on `(P^1)^4`; the two
diagonal coefficient rows are opposite decomposable vertices of the binary
Segre tensor cube.  A binary neighbor would be an intersection of the
eight-dimensional extension image with the corresponding moving secant.

Instead of eliminating that incidence or stratifying all its maximal-minor
divisors, regard the fourteen mixed rows as a polynomial submodule of a free
rank-eight module over `C(s,t)[h0,h1,h2,h3]`.  For every deleted coordinate,
the all-alpha diagonal has zero class in the cokernel while the all-beta
diagonal has nonzero class.  This one syzygy statement excludes every marking
simultaneously.  It is the module-level refinement of the standard Fitting
presentation formalism in the
[Stacks Project, Section 15.8](https://stacks.math.columbia.edu/tag/07Z6).

The Segre-secant viewpoint is adjacent to the catalecticant/flattening
technology surveyed and developed by Landsberg--Ottaviani
([arXiv:1012.3563](https://arxiv.org/abs/1012.3563)); the squarefree
annihilator viewpoint remains adjacent to Maeno--Watanabe's higher-Hessian
Lefschetz criterion.  Neither neighboring literature states the present
uniform cokernel identity.  The useful synthesis is: toric normalization
first, Segre incidence second, polynomial-module membership last.  It closes
the entire generic marked fibre without graph enumeration or a ternary-rank
calculation.

The weighted continuation of the tenth component adds a useful caution to
that translation:
[`P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_DENSE_MARKING_OBSTRUCTION.md`](P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_DENSE_MARKING_OBSTRUCTION.md).
The Cayley map polynomializes the torus multiplication graph, but the
Hadamard block coordinates `(a,a_bar,b,b_bar)` do not preserve the
squarefree permanent.  The correct calculation uses the toric coordinates
for the planes while pulling the Frobenius top form back to the original
coordinate axes.  Once those roles are separated, the two weighted mixed
matrices have compact factored rank-eight pivots on a dense open.

This is precisely where the apolar and toric literatures complement rather
than replace each other: toric geometry supplies the natural parameter chart,
while Artinian-Gorenstein duality fixes the multilinear functional that is
allowed to move.  Polynomial row modules then prove complete marking-fibre
emptiness at three rational component points.  The remaining generic marking
divisors are a concrete kernel-sheaf/Fitting problem, not evidence for a
weighted lift.

The eleventh component shows that the module translation becomes still
sharper when the exceptional triangle is built from an exact zero-divisor
pair.  Its generic marked `H31` theorem is
[`P5_H31_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md).
Over the full marking ring `C(p,q,r)[h0,h1,h2,h3]`, the all-kernel diagonal
row lies in the mixed row module for every deleted coordinate, whereas the
all-active diagonal has nonzero normal form.  For the two shared-support
deletions the first row is literally zero; for the other two it is a short
combination of standard-basis summands in the reduced module.

This is a small but useful strengthening of the usual determinantal
language.  Maximal minors locate rank-drop divisors and Fitting ideals record
supports, but an explicit row-module inclusion proves vanishing on every
kernel fibre at once, including marking divisors where those minors vanish.
The neighboring homological picture of exact zero divisors explains why the
presentation simplifies; the Segre picture identifies exactly which two
cokernel classes matter.  Their combination closes all eleven certified
components generically for `H31` without elimination, sampling, or a ternary
rank test.

The weighted `H22` continuation answers that question more directly than
expected:
[`P5_H22_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md).
After arbitrary diagonal source scaling and an arbitrary homogeneous merge
of `X0,X1`, the repeated kernel rows `a,a` are supported only on the merged
and fifth target channels.  They saturate that two-channel cut.  The remaining
rows are forced onto `X2,X3`, where the residual permanent is

```text
per [[p t2,p t3],[t2,-t3]]=0.
```

This is the annihilation `(X2+X3)(X2-X3)=0` seen in three neighboring
languages: an exact-zero-divisor pair in the squarefree complete
intersection, orthogonality of the trivial and sign characters of `C2`, and
a zero transfer across a two-channel tensor-network cut.  The homological
language predicts persistence of the annihilator block; the matching
language explains why a weighted projection cannot route around it.  The
result is stronger than a Fitting obstruction: one required binary diagonal
vanishes before the fourteen mixed equations are even imposed, for every
marking and every weighted slope.

Thus the eleventh component is generically closed for both marked types.  At
this checkpoint ten of the eleven certified components were generically
closed for weighted `H22`; the tenth component's marking divisors remained.

Those divisors are now closed by a translation from marked decompositions to
a fixed-vertex Segre join:
[`P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).
If `C_w` are the canonical binary tensor coordinates and the active rows move
by `beta_i -> beta_i+h_i alpha_i`, then every coordinate except the free
all-active `C_1111` must satisfy

```text
C_S C_empty^(|S|-1)=product_(i in S) C_{i},
2 <= |S| <= 3.
```

This is a Boolean rank-one toric array: six quadrics and four cubics, with no
marking variables.  The larger neighboring object is the secant-line variety
of a Segre product.  Landsberg--Manivel develop equations for Segre secants
([arXiv:math/0311388](https://arxiv.org/abs/math/0311388)); Raicu proves that
secant-line ideals of Segre--Veronese varieties are generated by cubic
flattening minors ([arXiv:1011.5867](https://arxiv.org/abs/1011.5867)), noting
the parallel motivations from algebraic statistics and phylogenetics.

Here the fixed first summand makes the incidence smaller and more elementary
than the full secant.  Projecting away the opposite diagonal produces the
toric equations above.  On the tenth component's weighted `23` extension
space, their exact function-field ideal is `(1)`.  Three binomials already
exclude the open pivot branch through the factor `2(u-1)(v-1)`; the full
canonical system closes its boundary.  This replaces the intractable generic
marking-module normal form by an invariant eleven-generator certificate and
closes all eleven certified components generically for both marked types.

The next common-factor sheet is controlled by a different classical binary
geometry:
[`P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md`](P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md).
For two complementary-block linear forms `s=uX2+vX3` and
`t=pX2+qX3`, the determinant `Q=uq-vp` cuts out the diagonal in
`P^1 x P^1`, whereas the squarefree polar pairing `A=uq+vp` cuts out the
graph of the exact-zero-divisor involution.  The four maximal minors of the
kernel-rich cubic multiplication map split into these two `(1,1)` divisors
and two coordinate-polar sheets.  This converts a permanent apolarity
condition into incidence between the diagonal and the graph of an involution
on the binary projective line.

Abdesselam--Chipalkatti study quadratic-form-induced involutions on binary
forms through compound transvectants
([arXiv:1008.3117](https://arxiv.org/abs/1008.3117)).  Kustin--Striuli--Vraciu
study exact pairs of homogeneous zero divisors
([arXiv:1304.0411](https://arxiv.org/abs/1304.0411)), and Shafiei proves
degree-two generation results for apolar ideals of generic permanents
([arXiv:1212.0515](https://arxiv.org/abs/1212.0515)).  Those are the three
neighboring specializations: binary invariant theory supplies the
involution, commutative algebra supplies the annihilator line, and apolarity
supplies the opposite plane.  None alone predicts the transverse
five-edge graph or the permanent component.

On the transverse sheet the exact point has pair profile
`(3,3,4,3,3,3)` and all four three-mode kernel-rich cubic spans have rank
two.  Fourteen regular incidence equations leave one excess tangent, but the
omitted equation has exact transverse leading term `12h^2`.  The tangent is
therefore obstructed and the displayed five-dimensional family closure is a
component.  Its sorted pair profile `(3,3,3,3,3,4)` separates it from all
eight earlier fivefolds; dimension separates the three earlier sixfolds.
The certified lower bound is therefore twelve components.  This reopens the
generic marked-fibre frontier:
the eleven components known before this binary-polarity discovery remain
generically closed for `H31/H22`, while the twelfth component's weighted
fibre was not yet classified at that checkpoint.

The twelfth component's `H31` side is now closed by the same module language
that succeeded on the tenth and eleventh components:
[`P5_H31_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md).
The exact-pair block makes the first two all-kernel diagonals identically
zero.  The other two are supported in four standard-basis summands of the
mixed presentation module.  Polynomial row reduction over the entire
marking ring gives module sizes `(7,7,8,8)` and retains the all-active
cokernel class in every deletion.

This is stronger than a generic determinantal rank calculation: it proves
one diagonal vanishes on every kernel fibre simultaneously, including every
marking divisor.  The binary-polarity geometry from the component theorem
and the Fitting-module viewpoint therefore dovetail exactly.  All twelve
certified pure components are now generically closed for `H31`; the new
generic known-component frontier is its weighted `H22` fibre.

That weighted fibre collapses to the polarity involution itself:
[`P5_H22_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md).
The repeated rows `a,a` saturate the merged/fifth channels.  The residual
two-channel matrix has rows `(-t2,k*t3)` and `(t2,k*t3)`, so its permanent
vanishes.  Equivalently,

```text
(-X2+kX3)(X2+kX3)=0
```

in the squarefree binary block.  Thus the quadratic involution from binary
invariant theory, the exact-zero-divisor pair from commutative algebra, and a
zero tensor-network transfer are literally the same certificate after the
weighted projection.  All twelve certified components are now generically
closed for both marked types.  The live frontier returns to component
exhaustiveness and special parameter/projective boundaries.

The same binary polarity also closes the dense common-kernel `YY` chart of
the remaining `(2,1,1)` exceptional triangle:
[`P4_COMMON_KERNEL_YY_211_TRIANGLE_OBSTRUCTION.md`](P4_COMMON_KERNEL_YY_211_TRIANGLE_OBSTRUCTION.md).
Here the neighboring theories do more than supply terminology.  The
rank-two cubic-span condition factors through the symmetric squarefree
pairing `A=uq+vp` and determinant pairing `Q=uq-vp`.  In the dense torus its
four minors force `A=0`, so the two complementary forms are an exact pair of
linear zero divisors.  The remaining equations remove the last component in
the common-kernel direction, and the all-active cubic becomes an explicit
linear combination of two kernel-rich cubics.

This is a small bridge between three literatures.  Abdesselam--Chipalkatti's
quadratic-form-induced involutions explain why `A=0` is naturally a graph in
`P^1 x P^1`, not an accidental bilinear factor
([arXiv:1008.3117](https://arxiv.org/abs/1008.3117)).
Kustin--Striuli--Vraciu study the Hilbert-function constraints imposed by
exact pairs of homogeneous zero divisors in standard graded Artinian rings
([arXiv:1304.0411](https://arxiv.org/abs/1304.0411)).  Shafiei's apolar study
of generic determinants and permanents explains the cubic-annihilator side
of the translation
([arXiv:1212.0515](https://arxiv.org/abs/1212.0515)).  None of these papers
states the graph obstruction: the new content is that the permanent
triangle's minors force the exact-pair sheet, on which the desired active
class collapses into the mixed apolar span.

The mixed `YX` common-kernel orientation reduces to a still smaller
factorization scheme:
[`P4_COMMON_KERNEL_YX_211_FACTORISATION_OBSTRUCTION.md`](P4_COMMON_KERNEL_YX_211_FACTORISATION_OBSTRUCTION.md).
The synchronization law becomes `b*d=a^2`.  Looking only at off-diagonal
coefficients makes this a symmetric rank-two matrix-completion problem with
one prescribed edge.  Its determinant split is complete: the rigid branch
has binary factors and pair-image rank one; the singular branch consists of
reflected factors `B+s`, `B-s`, where squarefreeness forces `s^2=0`.  That
reflection creates a second independent pair relation, so the image rank is
at most two.  The desired unique-relation rank-three edge cannot occur.

The exact-zero-divisor literature supplies the ambient Artinian
factorization language, but the point useful here is more elementary and
stronger for this stratum: the support graph of a factorization of one
squarefree edge is rigid enough to manufacture an extra tensor relation.
This closes the whole genuine support-two `YX` orientation, including the
coordinate-ray boundary, without primary decomposition or point search.

The final active/active common-kernel orientation crosses into arithmetic
geometry rather than collapsing:
[`P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md`](P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md).
Its four normalized parameters satisfy

```text
N(alpha,gamma)=N(r+beta,beta),
N(x,y)=x^2+x*y+y^2.
```

Thus the cubic apolarity condition is an equality of Eisenstein norms.  Over
the quadratic splitting field it becomes `UV=ST`, the rank-one determinant
defining the Segre quadric `P^1 x P^1`.  On the nonzero-norm chart the same
equation says that the ratio of the two Eisenstein elements belongs to a
norm-one torus.  Modern work on norm-one tori studies their compactifications,
rationality, and arithmetic obstructions in vastly greater generality; see
Hoshi--Kanai--Yamasaki
([arXiv:1910.01469](https://arxiv.org/abs/1910.01469)).  The present quadratic
case needs only the elementary Hilbert-90 parameterization, but that language
reveals why the parameter surface is rational and doubly ruled.

The graph-theoretic consequence is new: on this norm quadric the unwanted
permanent coefficient is `-4F` and the all-active coefficient is the constant
`4`.  The projective quadric contributes two moduli and the source torus
three; exact tangent/incidence ranks `5/15` prove that their closure is a
five-dimensional component.  The support-octahedron label and purity
incidence separate it from all twelve earlier orbits.  Consequently the
literature-guided translation has not merely simplified an obstruction; it
has exposed a thirteenth component and reopened the generic marked-fibre
frontier.

The `H31` side of that reopened frontier is now closed by combining the
quadric's rationality with presentation-module geometry:
[`P5_H31_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md).
Projection from a rational point gives a dominant two-parameter chart of the
norm quadric, so the extension problem lives over the honest rational
function field `C(u,v)`, without an algebraic coefficient extension.  In the
full four-variable marking ring, the all-kernel binary diagonal belongs to
the fourteen-row mixed module for every coordinate deletion, while the
all-active diagonal retains a nonzero cokernel class.

This is a useful division of labor between the neighboring theories: norm-
form geometry rationalizes the component field, and commutative algebra
turns the simultaneous marking problem into four row-module inclusions.
The reduced module sizes `(10,10,10,10)` and exact rank jumps
`(7,7,7,7)->(8,8,8,8)` replace pointwise determinant tests.  All thirteen
known components are therefore generically closed for `H31`; the weighted
`H22` fibre of the Eisenstein component is the remaining generic known-
component question.
