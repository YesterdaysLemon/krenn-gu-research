# Symbolic translation and literature frontier (2 August 2026)

## Scope

This review starts from the current exact frontier, not from a new support
search:

- every `P_m -> Delta_3` restriction has at least `3m+3` nonzero row cells;
- the eliminated `3m+2` equality layer reduced to a bipartite negative-gain
  cancellation graph on two exceptional sources;
- the five-root cell gives coloured quotient-minor equations, but common
  tangent edges do not force a rank-two hidden pair;
- scalar overlay identities are surjective and therefore cannot obstruct the
  cell by themselves.

The goal is to identify mathematical translations that preserve the exact
complex cancellations.  Positive-weight, numerical, finite-field, border,
and asymptotic statements are not silently promoted to proofs of the original
characteristic-zero exact restriction problem.

The strict permanent bound has one immediate transfer that should be kept
separate from the speculative translations below.  Whenever the proved
root--blocker lemmas extract `P_m -> Delta_3`, their active cell support is at
least `3m+3`.  In the one-port case this gives
`I(R,B)+p>=3r+6`, and the graph-only sufficient contradiction
`e_G(R,B)+e_G(B,Q)<=3r+5`.  The exact sharp targets are therefore 17, 20,
and conditionally 23 cells for extracted `P_5`, `P_6`, and `P_7` systems.
Forcing one of those sparse extractions globally is still open.  See
`GRAPH_EXTRACTION_STRICT_SUPPORT_TRANSFER_COROLLARY.md`.

## 1. Gain graphs and a new multi-backbone gluing diagram

### Existing theory

In a gain graph, oriented edges carry elements of a group, reversal inverts
the gain, and a cycle is balanced when its gain product is the identity.
Zaslavsky's foundational biased-graph theory organizes these balanced cycles
and the associated matroids:

- Thomas Zaslavsky, *Biased graphs. I. Bias, balance, and gains*, JCTB 47
  (1989),
  [doi:10.1016/0095-8956(89)90063-4](https://doi.org/10.1016/0095-8956(89)90063-4).

### Exact translation obtained here

At `3m+2` equality, let `p_1,p_2` be the exceptional sources and define

```text
g_(i,c)=r_(i,p_2)[c]/r_(i,p_1)[c].
```

Every cancellable mixed backbone matching gives an edge between two
mode--colour states and forces `g_u/g_v=-1`.  Thus the cancellation graph is
an all-negative gain graph and must be bipartite.  This is proved in
`ARBITRARY_PERMANENT_EQUALITY_NEGATIVE_GAIN_GRAPH_THEOREM.md`.

### Exact no-go for one backbone

For a fixed triple `H=M_0 union M_1 union M_2`, every incident state `(i,c)`
has a canonical side: the pure edge of `M_c` at mode `i` ends at either
`p_1` or `p_2`.  Every cancellation edge joins the two sides.  Thus the
fixed-backbone gain graph is combinatorially bipartite before the ratio
equations are used.  An exchange complex whose attaching loops are already
walks in that graph adds no new odd-holonomy obstruction.

### New theory to build: the multi-backbone gain diagram

Let the objects be all triples `(M_0,M_1,M_2)` of pure matchings, with an
elementary transition when one matching changes along one alternating cycle.
Attach to each object its fixed-backbone cancellation graph.  Identify a
vertex `(i,c)` across all objects because its physical ratio `g_(i,c)` is
independent of the chosen matching.  The resulting colimit graph is
`Gamma^*` from
`ARBITRARY_PERMANENT_EQUALITY_NEGATIVE_GAIN_GRAPH_THEOREM.md`.

Each fibre is bipartite, but the colimit need not be: a state may lie on the
`p_1` side in one pure matching and the `p_2` side in another.  Every edge in
the colimit still has gain `-1`, so a hypothetical restriction requires the
whole colimit to be bipartite.

The pure-matching cube theorem makes the diagram finite in structure at
every order: every switch is an exceptional-source four-cycle, and at most
two colours can switch.  Thus the object set is a face of `{0,1}^k`, `k<=2`,
with at most four objects.  The two-switch case is confined to co-located
noncoordinate excess cells.  This is a theorem about the choice space, not
permission to enumerate the mixed matchings inside those objects.

The zero-dimensional face is now impossible.  If every colour has a unique
pure matching, full colour eligibility has a unique-matching triangular
form with at most two nonmatching edges.  Rectangle cancellation makes the
sets of colours used by mixed matchings at the two exceptional sources
disjoint.  It also forces each pair of pure colour matchings to form one
Hamilton cycle: every multi-component two-factor produces either a mixed
matching with the same terminal colour or two complementary mixed matchings
whose cross partners create a pure switch.  Bogdanov supplies a mixed
matching, so one exceptional-source colour set is a singleton.  A nonforced
edge of that colour is a chord of the Hamilton cycle formed by the other two
colours; extending the chord to a perfect matching contradicts the singleton
port rule.  Hence every equality survivor has one or two switches.

This packages the remaining equality problem into one exact combinatorial
claim:

```text
Do alternating-cycle transitions among all pure matchings force an odd
cycle after their ratio-state vertices are identified?
```

This is the highest-priority arbitrary-order route.  It uses matching
exchange between backbones; it does not repeat the already exhausted
single-backbone odd-cycle argument.

The backbone-colouring glue theorem gives a complete descent formulation.
Its vertices are connected components of the fixed-backbone graphs; shared
ratio states label overlap edges by the xor of the two canonical side
assignments.  The colimit is bipartite exactly when this `F_2` overlap graph
is balanced.  A one-switch straddling pair gives an immediate unbalanced
two-cycle.

The one-switch cut normal-form theorem first sharpened that target.  The nonzero
pure switch binomial forbids every nonmonochromatic matching in either
selected backbone that uses both switch edges.  After deleting the switch
core, the common residual backbone has a unique perfect matching; its
alternating dependency digraph is therefore acyclic and its biadjacency
support triangular.  In the two-fibre
component-incidence graph, the only nonzero overlap labels are the two
switch states.  Equality holds at the gluing level exactly when those two
marked edges belong to the cut space: both are bridges, or they are a
two-edge series cut.  A straddling pair is only the smallest violating cycle.
Abstract bridge and series-pair models survive this cut-space test.

The full permanent backbone now excludes them by a different transfer.  In
the one-switch branch, component selection forces every pair of selected
pure matchings to be one alternating Hamilton cycle.  The exceptional edges
of a nonswitch colour are therefore two chords of the Hamilton cycle formed
by the other colours.  Extending each chord to a mixed perfect matching and
applying two-source localization forces both cross cells, producing a second
pure matching of the nonswitch colour.  Hence the one-switch branch is empty
at every order.  This is a perfect-one-factorization obstruction rather than
a gain-holonomy obstruction.

This is a direct transfer from unique-perfect-matching theory and the
Dulmage--Mendelsohn viewpoint, but the marked cut condition is specific to
the permanent cancellation local system.  See Kotzig's 1959
[unique-matching record](https://eudml.org/doc/29879) and Dulmage--Mendelsohn,
[*Coverings of Bipartite Graphs*](https://doi.org/10.4153/CJM-1958-052-0).

The two-switch branch has a complementary local invariant.  Its two
noncoordinate excess rows are co-located at one mode and the equality ledger
leaves exactly one coordinate row there.  Localization forces that row to
have the third colour, so local concision makes the switch-colour `2 x 2`
minor nonzero.  In gain coordinates, `g_(a,c)!=g_(a,d)`.  Path parity then
separates the two same-mode switch states whenever they have the same source
side, and also separates each switch state from its mandatory partner in
every fibre.  Therefore the most local candidate pair cannot straddle; a
ratio state away from the common excess mode is essential.  Cross-colour
pairs at `b_c,b_d` remain open.

This also marks the exact limit of two nearby imported theories.  The excess
plane lies in `Gr(2,3)`, which has no quadratic Pluecker equation.  The two
known switch rectangles admit one coherent edge signing, so there is no
two-rectangle Pfaffian obstruction.  Adding the third row pair would obstruct
one common determinant signing, but that orientation failure is not a
contradiction in the bosonic permanent system.  Matchgate identities would
additionally require a full deletion-closed boundary signature.
Cai--Gorenstein and Bravyi explain that signature-level hypothesis; the
present alternate backbones do not satisfy it automatically.

The direct mixed-backbone route to the third switch-mode rectangle is now
reduced exactly to Hall completion.  Delete the common excess mode, both
degree-four switch modes, and the three sources they occupy.  The remaining
graph is switch-independent.  A perfect matching completes the desired mixed
word and forces its rectangle equation.  If no matching exists, a minimal
deficient set has deficit one; its two
switch-colour matchings form one alternating path plus cycles, and its shore
has cut signature `(1,1,1)` or `(1,1,3)`.  An explicit six-mode support with
the five-edge signature satisfies the complete degree ledger, local ranks,
pure-switch classification, and every source-subset Hall quota.  It is not a
mixed-coefficient solution, but proves that these structural conditions do
not force completion.  It does not rule out deriving the same rectangle
indirectly from other mixed equations.

This is the appropriate tight-cut translation: contract a connected shore
while retaining its three or five boundary port values, and seek a boundary
coefficient identity incompatible with the diagonal target.  The three-edge
signature is now excluded exactly.  Its two switch-colour ports occupy the
same outside source, so full-support Laplace expansion has only two distinct
complement minors and flattening rank at most two.  The corresponding
nontrivial flattening of `Delta_3` has rank three.  The five-edge signature
is now excluded by a separate boundary-state argument.  Defect-one balance
forces an internal Kempe pairing bit; a pure switch toggles the exterior bit
while preserving the interior.  Choosing the aligned backbone gives a
one-cycle flip whose mixed monomial lacks its localized two-source cross
partner.  Thus no no-completion shore survives, and the residual perfect
matching and cross-colour port rectangle are forced at every order.  The
shore interior remains symbolic throughout; no census of supports is used.

The remaining two-switch branch is now excluded without further scalar gain
algebra.  Select the two switch matchings so that their common excess mode
`a` goes to opposite exceptional sources.  Their two-factor contains the
path `p_1--a--p_2`.  Any other component would allow a mixed component
selection using both selected switch edges, so switch-core rigidity makes
the factor Hamilton.  The two exceptional edges of the nonswitch colour are
then Hamilton chords.  Their two mixed extensions force both cross cells and
create a forbidden pure switch in that colour.  This closes all equality
strata and sharpens the support bound from `3m+2` to `3m+3`.

## 2. Toric ideals and matching-exchange binomials

### Existing theory

Perfect matchings become monomials, and their symmetric differences decompose
into even cycles.  Toric ideals record when two products of matching monomials
have the same incidence vector.  Recent work relates generator degrees for
matching-polytope toric ideals to edge colourings of bipartite multigraphs:

- Mori, Motomura, Ohsugi, and Tsuchiya, *Toric ideal of matching polytopes and
  edge colorings*, [arXiv:2501.19209](https://arxiv.org/abs/2501.19209).

The nearby matroid version asks whether toric relations are generated by
quadratic symmetric exchanges; see Lasoń,
[*On the toric ideals of matroids of a fixed rank*](https://arxiv.org/abs/1601.08199).

### Safe transfer

The equality equation `AD+BC=0` is a signed exchange binomial.  After choosing
one sign gauge, its exponent difference is exactly the four-cycle lattice
move `AD-BC`.  Thus the **exponents** live in a matching toric ideal while the
**coefficient signs** live in the gain local system of Section 1.

Neither structure alone is enough:

- the toric ideal forgets the required plus sign;
- the gain graph forgets which exchange cycles are generated by actual
  perfect matchings.

Together they suggest a rigorous target: compute a symbolic presentation of
the exchange lattice of the three chosen pure matchings, then prove that the
`-1` character on its rectangle generators is not trivial on the relation
lattice.  One odd relation in that lattice is exactly the desired
contradiction.  This is a lattice-rank/Smith-normal-form theorem in symbols,
not a census of matchings.

### Exact three-excess port reduction

The strict support theorem makes `3m+3` the first remaining layer.  Choose
the mandatory `3m`-cell coordinate cover.  The three excess cells have two
or three exceptional source endpoints: one endpoint is impossible because
Bogdanov supplies a mixed backbone matching and an alternating cancellation
cycle needs two new source endpoints.

Exceptional-source localization then collapses every coefficient of a word
induced by the selected backbone exactly.  Relative to its backbone matching
`F`, every other term for the same word agrees outside the exceptional
sources and permutes their `F`-preimage modes.  There can be only one exchange
cycle, so the change is a transposition or a three-cycle.  After the common
arbitrary-order interior monomial is factored, the full coefficient is

```text
W_F per(X),          X of size 2 x 2 or 3 x 3.
```

Thus the matching-toric boundary of a mixed backbone word has at most the six
elements of `S_3`.  Pure words are sharper.  A colour-eligibility graph has
only three cells beyond its chosen matching.  After contraction these are at
most three loopless dependency arcs, which contain at most one directed
cycle.  Hence every colour has at most two pure matchings, related by one
alternating four- or six-cycle, and the pure backbones form a Boolean cube of
dimension at most three and size at most eight.  This is stronger than a
bounded search claim: it is an exact quotient of every backbone-induced
coefficient by its common interior plus a dependency-digraph classification
of all pure choices.

The new obstruction is also sharp.  A `3 x 3` permanent may vanish while a
distinguished row has no cross entry, because the complementary two ports
transpose and cancel with that row fixed.  For a chord row `s`, the fixed-row
channel is

```text
X_(s,s) per(X_(hat s,hat s)).
```

Nonvanishing of that complementary `2 x 2` permanent forces a cross arc out
of `s`.  If this holds for all three chord rows, a directed two- or
three-cycle of forced arcs gives a second pure matching.  The precise next
problem is therefore to exclude the fixed-port bypass rectangles, not to
enumerate the six permutations.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_PORT_PERMUTATION_THEOREM.md`.

### Matching-covered and `B_3` phase translations

At exact support `3m+3`, the physical support graph is matching-covered.  An
edge in no perfect matching could be deleted without changing the
polynomial, contradicting the strict support theorem.  A disconnected
support would factor across components and have flattening rank one, whereas
the corresponding nontrivial flattening of `Delta_3` has rank three.

De Carvalho and Little's quoted general theorem implies that any three
prescribed edges of a matching-covered graph lie in a conformal subgraph
formed from at most two alternating circuits.  Their sharper three-edge
corollary says the carrier is an induced circuit, an even subdivision of
`Theta`, or an even subdivision of one of nine `K_4`-generated graphs.
Bipartiteness excludes the last family because every member retains an odd
circuit.
Hence the excess cells lie in a conformal even circuit or theta subdivision,
with exactly two or three internal perfect matchings; see [*Matching Covered
Graphs with Three Removable
Classes*](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v21i2p13).
This is the correct even bipartite analogue of the tempting factor-critical
ear translation.

For a three-source backbone word, normalize the three transposition
monomials to `a,b,c` and the oriented three-cycle monomials to `u,v`.  The
complete coefficient and its toric circuit are

```text
1+a+b+c+u+v=0,       uv=abc.
```

The multiplicative equation is exactly the unique cubic circuit of the
`3 x 3` Birkhoff polytope described by Haase and Paffenholz in
[*Groebner Bases for Transportation
Polytopes*](https://arxiv.org/abs/math/0607194).  The three complementary
fixed-row channels are `1+c,1+b,1+a`.  Setting `a=b=c=-1` leaves the
consistent equations `u+v=2`, `uv=-1`, realized over `C` by a full-support
port matrix with `u,v=1+sqrt(2),1-sqrt(2)`.  Hence even simultaneous
vanishing of all three channels cannot be excluded inside one port
coefficient.

The invented next object is a proposed phase-decorated `B_3` exchange
complex: glue one additive/toric phase variety for every backbone-induced
mixed word and identify shared physical row-cell factors across the Boolean
pure-backbone cube.  To incorporate the conformal cycle/theta theorem, its
definition still needs carrier-selection data recording how that theorem's
matching meets each pure backbone.  The intended object retains both complex
phases and global matching reuse; either ingredient alone is insufficient.

## 3. Determinantal ideals, Grassmannians, and a cofactor quiver

### Existing theory

The visible condition that two quotient cofactors are proportional is the
rank-one determinantal variety, cut out by `2 x 2` minors.  Across many linked
linear maps, quiver semi-invariants provide systematic determinantal
equations.  Schofield and Van den Bergh prove that, in characteristic zero,
determinantal semi-invariants span the semi-invariant functions for acyclic
quivers:

- Schofield and Van den Bergh, *Semi-invariants of quivers for arbitrary
  dimension vectors*, [arXiv:math/9907174](https://arxiv.org/abs/math/9907174).

Symmetric quivers add Pfaffian semi-invariants on skew-symmetric arrows; see
Aragona, [*Semi-invariants of Symmetric Quivers*](https://arxiv.org/abs/1006.4378).

### Exact translation obtained here

For every active root deletion `k`, the pair

```text
(bar C_k,bar E_k)
```

is a two-row matrix of rank at most one.  Its minors are the quotient-wedge
invariants.  At least two sectors are active, yielding five degree-eight
products without naming them.

### Proposed theory: a bound deletion-depth cofactor quiver

Make one vertex for each quotient cofactor space at each deletion depth.
Edge-contraction maps and root/end-point expansions become arrows; the
five hidden-pair equations become rank constraints on five two-arrow
Kronecker fragments.  Common root-edge parameters impose relations between
arrows, so this is a **bound/constrained** representation variety, not
automatically the ordinary acyclic quiver space covered by the cited
semi-invariant theorem.

The proof program must first define the group action and relations and check
whether the resulting quiver is acyclic, or instead work with the more
general map-of-projectives formulation.  Only then is it legitimate to seek
a determinantal semi-invariant that vanishes on the legal shared-edge image
and is nonzero on the prescribed lower-jet frame.  Schofield theory suggests
candidate forms; it does not guarantee such a separator here.

This remains preferable to eliminating all edge weights if a separator can
be found.  One semi-invariant could certify incompatibility uniformly over an
entire component, as the repository's row-module certificates already do in
lower-order cells.

The tangent counterfamily sharply specifies the missing data: a determinant
built only from `h_k,q_k,g_t` cannot work.  At least one actual complementary
blocker cofactor value must enter.

## 4. Matchgates, spinors, and delta-matroids: a conditional local tool

### Existing theory

Cai and Gorenstein prove that the matchgate identities are necessary and
sufficient for planar matchgate signatures:

- Cai and Gorenstein, *Matchgates Revisited*,
  [arXiv:1303.6729](https://arxiv.org/abs/1303.6729).

Tropical Wick relations and even delta-matroids describe the support-side
spinor analogue; see Rincón,
[*Isotropical Linear Spaces and Valuated Delta-Matroids*](https://arxiv.org/abs/1004.4950).

### Proven non-transfer and remaining use

Generic bosonic principal hafnians cannot be changed into principal
Pfaffians by a fixed edge signing from six vertices onward, and complex
cancellation can destroy delta-matroid support.  Those exclusions are proved
in `BOSONIC_HAFNIAN_SPINOR_NO_TRANSFER.md`.

Therefore no global Grassmann--Plücker identity may be imported.  A narrower
conditional route remains legitimate: if the equality/gain analysis forces a
coherent sub-Pfaffian representation across the entire relevant
boundary-deletion family, with compatible signs, then matchgate identities
apply on that chart.  A Pfaffian orientation computing one full matching sum
is not enough.  The proof obligation is to derive the coherent family from
the permanent hypotheses; planarity is one sufficient route, but cannot be
assumed.

Priority: medium.  It may close a rigid equality subcase, but it is not a
universal bosonic theory.

## 5. Tensor subrank, invariant theory, and orbit closure

### Existing theory

Ordinary tensor subrank is exactly the largest diagonal tensor obtainable by
independent local linear maps.  Christandl, Fawzi, Ta, and Zuiddam study the
distinct symmetric version, where the same map is used on every leg, and its
relation to ordinary/asymptotic subrank:

- *Symmetric Subrank of Tensors and Applications*,
  [arXiv:2104.01130](https://arxiv.org/abs/2104.01130).

Entanglement polytopes turn covariants into local spectral witnesses for
orbit closures:

- Walter, Doran, Gross, and Christandl, *Entanglement Polytopes*,
  [arXiv:1208.0365](https://arxiv.org/abs/1208.0365).

Tensor-network state spaces can be nonclosed, so exact image membership and
border membership must be separated:

- Landsberg, Qi, and Ye, *On the geometry of tensor network states*,
  [arXiv:1105.4449](https://arxiv.org/abs/1105.4449).

Geometric-complexity work also warns that coarse moment-polytope or
`SL`-representation data can be too weak for orbit-closure lower bounds:

- Bürgisser and Ikenmeyer, *Geometric Complexity Theory and Tensor Rank*,
  [arXiv:1011.1350](https://arxiv.org/abs/1011.1350).

### Safe transfer

`P_m -> Delta_3` is an exact ordinary-subrank restriction, not a symmetric,
border, or asymptotic statement.  Local concision and Hall
quotas resemble moment-polytope inequalities, but the sharp `3m+2` survivor
shows that such inequalities are not enough.  The useful next objects are
explicit covariants or nonlinear flattenings that:

```text
vanish on every legal hafnian/permanent restriction image,
but do not vanish on Delta_3.
```

The coloured quotient minors are not yet such covariants or separators.
They are coordinate-dependent determinantal equations on one uniform-axis
lower-jet chart, derived using the `Delta_3` target; no `GL`-equivariance or
nonvanishing target evaluation has been proved.  The bound-cofactor-quiver
program asks whether they can be combined into a genuine separator without
passing to border or asymptotic rank.  Symmetric/asymptotic subrank
functionals remain orientation, not proof certificates for this exact
finite problem.

## 6. Bosonic Gaussian moments, apolarity, and cumulant sheaves

### Existing theory

Hafnians are transversal moments of a formal centered Gaussian family, and
Gaussian moment parametrizations form algebraic moment varieties.  Useful
entry points are:

- Hamilton et al., *Gaussian Boson Sampling*,
  [arXiv:1612.01199](https://arxiv.org/abs/1612.01199);
- Améndola, Faugère, and Sturmfels, *Moment Varieties of Gaussian Mixtures*,
  [arXiv:1510.04654](https://arxiv.org/abs/1510.04654).

### Exact repository transfer

In the vertex-exclusive square-zero algebra, the full family of partial
matching tensors is

```text
M=exp(Q),                 log M=Q.
```

Thus all connected cumulants above degree two vanish **for the full
partition-closed partial-moment family in which proper blocker subsets are
retained and core vertices may split or delete**.  A shell of complementary
cofactors retaining one common blocker core need not be log-quadratic after
coefficient extraction.  The current lower-frame theorem does not force the
required family, and the scalar hidden overlay is surjective.  This is proved in
`BLOCK_SQUARE_ZERO_WICK_COMPLETION_THEOREM.md` and
`ROOT_M7_HIROTA_HIDDEN_OVERLAY_SURJECTIVITY_NOGO.md`.

### Proposed analogy: a deletion-cumulant gluing obstruction

Regard known cofactor values on the subset lattice as prospective local
sections.  A legal graph should give compatible log-quadratic completions on
partition-closed windows.  This resembles a Čech obstruction, but is not yet
a sheaf or a defined cohomology class: restriction maps, the gauge/torsor
structure on nonunique completions, and gauge-independent overlap differences
must all be constructed.

A rigorous program is:

1. choose partition-closed windows that allow proper core subsets;
2. define their completion spaces and restriction maps;
3. quotient the nonuniqueness by an explicit gauge action;
4. only then define and test an overlap obstruction against the `Delta_3`
   frame.

The scalar-surjectivity theorem says one window has zero obstruction.  The
first possible class must be coloured and use at least two overlapping root
deletions, matching the quotient-wedge result.

Priority: high after the cofactor quiver is written, because the quiver
arrows provide the overlap maps this sheaf needs.

## 7. Tropical, stable, and Lorentzian methods: degeneration only

### Existing theory

Lorentzian polynomials have M-convex support and strong Hodge-type
inequalities; see Brändén and Huh,
[*Lorentzian polynomials*](https://arxiv.org/abs/1902.03719).  Valuated
delta-matroids give the tropical spinor-side exchange theory in Rincón's
paper cited above.

### Boundary

The Krenn--Gu weights are arbitrary complex numbers.  Positivity,
real-stability, negative dependence, and Lorentzian inequalities do not
survive arbitrary destructive interference.  The support of nonzero complex
principal hafnians is not even always a delta-matroid.

These tools become legitimate only after a proved one-parameter degeneration
in which a unique leading term is selected and the `Delta_3` restriction is
preserved after compensating local scalings.  This suggests combining
Hilbert--Mumford one-parameter subgroups with matching valuations.  The hard
lemma is existence of a useful nontrivial degeneration of an arbitrary exact
hypothetical solution.  Without that lemma, tropical or Lorentzian output is
not evidence about the original complex cancellation problem.

Priority: exploratory, but fully symbolic.

## Ranked proof program

1. **Phase-decorated `B_3` exchange complex.**  Define the missing incidence
   alignment between the conformal cycle/theta matching and the
   at-most-eight pure backbones, then glue the exact additive and cubic toric
   equations.  A single coefficient cannot exclude simultaneous bypasses.
2. **Deletion-depth cofactor quiver.**  Build one cross-sector
   semi-invariant using actual lower cofactor values.  The tangent
   counterfamily rules out weaker candidates in advance.
3. **Coloured deletion-cumulant compatibility.**  Use two overlapping root
   windows to turn quotient minors into a global log-quadratic obstruction.
4. **Conditional Pfaffian chart.**  Apply matchgate identities only if a
   support-specific orientation is forced.
5. **GIT/tropical degeneration.**  Seek a one-parameter initial form that
   preserves the exact diagonal restriction; do not substitute asymptotic or
   border statements.

## Current status wall

```text
new arbitrary-order exclusion:    all 3m+2 equality faces impossible;
new arbitrary-order theorem:      support >=3m+3 and S_3 port normal form;
new exact local invariant:        additive/toric B_3 phase variety;
new exact route exclusion:        one coefficient permits all bypasses;
highest-priority invented object: phase-decorated B_3 exchange complex;
highest-priority literature tool: conformal cores + Birkhoff circuit;
full proof or counterexample:      NOT YET;
global Krenn--Gu conjecture:       UNRESOLVED.
```
