# Common-star obstruction from global component targets

## Status and scope

The source identities and obstructions below have direct proofs over C.
The initial triangle-free and unique-port results were reviewed on
2026-09-14. The
[independent review](../../docs/audits/PROTECTED_SCAFFOLD_COMMON_STAR_REVIEW_2026-09-14.md)
records exact physical replays and the cycle, triangle, and multiple-label
controls. No Lean formalization is supplied.
The [two-port review](../../docs/audits/PROTECTED_SCAFFOLD_COMMON_STAR_TWO_PORT_REVIEW_2026-09-14.md)
independently audits the shared-neighbor identity, the source-derived
resource decomposition and the additional global-word contradiction.
The [resource-alignment review](../../docs/audits/COMMON_STAR_RESOURCE_ALIGNMENT_REVIEW_2026-09-14.md)
audits the later binary-resource extension (15). The
[binary-supply review](../../docs/audits/COMMON_STAR_BINARY_SUPPLY_REVIEW_2026-09-14.md)
records the subsequent refutation of its proposed local supply. Earlier reviews pin the
versions they actually inspected, rather than certifying subsequent edits.

This result rejects a declared construction route for the
[Q4 parent](../../docs/strategy/scaffold-q4-parent-attempt-2026-09-14.md):
common-star pair gadgets on a triangle-free component graph, and gadgets
with at most two edges in each ordered color port even when triangles are
present. The latter conclusion uses the full component-constant targets;
singleton and double-component equations alone have an exact control below.
It is not a normal-form theorem for arbitrary hollow fillings and
does not prove Q4.
More generally, the full component target excludes every common-star
array whose state graph splits into complete tripartite resources; the
two-port argument supplies this decomposition in a proved subfamily.
In fact a complete bipartite decomposition for just one color pair is
enough, without any alignment with the other color pairs. Consequently
the full target is impossible if all ports for just one unordered color
pair have size at most two, even with unbounded ports for the other pairs.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

The upstream physical arrays are the
[protected pure-matching scaffolds](PURE_MATCHING_SCAFFOLD_STRUCTURAL_GATE_NO_GO_THEOREM.md).
The
[fixed-minority-depth control](PROTECTED_SCAFFOLD_FIXED_MINORITY_DEPTH_NO_GO.md)
uses a different pair allocation, with two independent matching-pair
resources for each component color. The construction considered here
instead makes the gadgets share one center and one pair for that color.
This distinction changes its source and is used explicitly below.

## Literal physical construction

Let G be a finite simple graph on k>=2 component vertices. Each edge has
exactly one ordered pair of distinct endpoint colors. Orient an edge
e={u,v} for notation and write its label as (d,e'), meaning color d at u
and color e' at v. Reversing the orientation reverses the label. There may
be many incident edges with the same label at a vertex, but there is only
one gadget between any pair of components.

Each component is a protected K4 on local vertices 0,1,2,3, with

```
M_0={01,23}, M_1={02,13}, M_2={03,12},
```

and entire physical matrix E_cc on each edge of M_c. Call vertex 0 the
center and vertex c+1 the color-c leaf. For a component edge labelled
(d,e'), set exactly these two crossing entries nonzero:

```
center_u -- center_v:           color (d,e'), weight a_e;
leaf_(u,d) -- leaf_(v,e'):       color (d,e'), weight b_e.
```

The factor weights a_e,b_e are arbitrary nonzero complex numbers. Put
q_e=a_e b_e. Every other intercomponent entry is zero; reversing a physical
matrix transposes it. In particular the crossing matrices are hollow.
Choosing a different local center by a color-preserving relabelling of a
K4 gives the same construction.

A component-constant word assigns one color to all four physical vertices
of each component. A gadget is compatible with such a word if its ordered
label equals its endpoint component colors. The target is one on the three
globally constant component words and zero on all other component words.

## The exact global source and its forest specialization

Fix a component-constant word x. In a component of color c, the two leaves
other than leaf c have their forced internal M_c edge. Its remaining
center and color-c leaf either match each other internally or both cross
to other components.

Let A_x and B_x be symmetric k-by-k matrices with zero diagonal. On a
compatible component edge e put the center weight a_e in A_x and the leaf
weight b_e in B_x; put zero on every incompatible edge or absent pair.
The full physical source is exactly

```
F(x) = sum_(S subset V(G), |S| even) haf(A_x[S]) haf(B_x[S]). (1)
```

Indeed S is the common set of components whose centers and selected
leaves cross. Their center matching and leaf matching are independent
perfect matchings on that same S. Every other physical factor is a forced
unit edge. This proves (1), with the empty term equal to one.

In general, (1) is not an ordinary matching polynomial: its two matchings
may use different component edges. If the compatible component graph is
a forest, each induced subgraph has at most one perfect matching. To see
this, the symmetric difference of two distinct perfect matchings would
contain a cycle. Consequently, in this forest case only identical center
and leaf matchings survive, and

```
F(x) = sum_(M a matching of the compatible graph) product_(e in M) q_e. (2)
```

Only the specific forest colorings below use (2). No global matching-
polynomial assertion on cyclic compatible graphs is assumed.

## Exact three-source identity at an edge without a triangle

Let uv be a component edge with label (d,e), d!=e, and suppose u and v
have no common neighbor. Let c be the third color. Define these three
component-constant full source coefficients:

```
F_u  : component u has color d, every other component has color c;
F_v  : component v has color e, every other component has color c;
F_uv : u has color d, v has color e, every other component has color c.
```

All three words are mixed when k>=2. Put

```
s_u = sum q_f over edges incident to u labelled (d at u,c at its neighbor);
s_v = sum q_f over edges incident to v labelled (e at v,c at its neighbor).
```

For F_u the compatible graph is the corresponding star at u; for F_v it
is the corresponding star at v. Hence

```
F_u=1+s_u,             F_v=1+s_v.                    (3)
```

For F_uv no edge between two exterior components is compatible, because
both endpoints have color c and every gadget label is hollow. The only
remaining compatible edges are uv and the two stars just described. The
edge uv is absent from each star because it has the single label (d,e),
with c different from both colors. The stars have disjoint exterior
vertices because u and v have no common neighbor.

Thus the compatible graph is a double star, hence a forest. A matching
either uses uv, with contribution q_uv, or chooses independently at most
one edge from each exterior star. Formula (2) therefore gives

```
F_uv=(1+s_u)(1+s_v)+q_uv,
q_uv=F_uv-F_u F_v.                                  (4)
```

Equation (4) is an identity between actual full source coefficients of the
same physical array. It does not replace outside contributions by
independent cofactors. The two exterior star sums are kept until the
source identity cancels them.

## Triangle obstruction

If the component-constant target equations held, all three coefficients
in (4) would be zero. This would give q_uv=0, contrary to the two nonzero
factor weights on the gadget. Consequently, under the component-constant
target equations every nonzero common-star gadget edge must belong to a
triangle of the component graph.

In particular no common-star array on a triangle-free component graph can
satisfy all component-constant targets. If such a graph has an edge, the
preceding argument applies to it. If it has no edges, any nonconstant
component word has its unique protected internal matching of weight one.
This covers arbitrary degrees and repeated labels on distinct edges;
neither regularity nor bipartiteness is needed.

The first two rows in (4) have four physical minorities relative to c.
The third has eight such minorities. Thus Q4 supplies the first two from
its bounded-minority subsystem and the third from its global component
subsystem. In larger orders, the latter row is precisely the additional
source coupling needed by this proof. When k=2 the third row also lies
within four minorities of d or e, which is consistent with the separate
eight-vertex boundary.

The hypotheses cannot be discarded in this argument. A common neighbor
creates a resource collision between the two stars, and cyclic compatible
graphs can have distinct center and leaf matchings in (1). Multiple
different gadgets on the same pair of components also invalidate the
single-label classification used in (3)--(4).

## Ordered ports and a second obstruction with triangles allowed

For distinct colors a,b, define the ordered port (u,a,b) to consist of
the component edges incident to u whose label is color a at u and color
b at the other endpoint. An empty port has no such gadget; a unique port
has one; a repeated port has at least two. These counts concern different
component neighbors, since the component graph is simple and there is
only one label on each edge.

Changing component u from a constant background b to color a gives the
exact full source

```
F_(u:a | b)=1+sum_(f in port(u,a,b)) q_f.              (5)
```

The compatible graph is a star, so (5) follows from (2). This is a mixed
component word. Consequently all component-constant target equations
force every port to be nonempty and every unique port's gadget product
to equal -1.

More locally, orient an edge uv with label (d,e), and let c be the third
color. Suppose the three ports

```
(u,d,e),                 (u,d,c),                 (v,e,c)             (6)
```

are all unique. The first contains uv. Let the other two edges be uU
and vV. The endpoint labels at U and V are c. In particular U!=v and
V!=u: the single label on uv has neither of those endpoint colors.
The three singleton component targets

```
F_(u:d | e)=0,          F_(u:d | c)=0,          F_(v:e | c)=0
```

then imply

```
q_uv=q_uU=q_vV=-1.                                    (7)
```

Consider the full component word with u colored d, v colored e, and every
other component colored c. Its compatible graph has exactly the three
edges uv,uU,vV. Edges between two exterior components are incompatible
because both endpoints are c. No other edge at u or v is compatible by
the uniqueness assumptions in (6).

If U!=V, this graph is a tree. The source is

```
F_uv=(1+q_uU)(1+q_vV)+q_uv=-1.                         (8)
```

If U=V, the compatible graph is a triangle. In (1) only the empty subset
and its three two-vertex subsets can contribute, so

```
F_uv=1+q_uv+q_uU+q_vV=-2.                              (9)
```

Both values contradict the zero target for this mixed word. This proof
uses three singleton component equations and one double-component
equation of the same physical array. It neither assumes a forest in the
triangle case nor drops any exterior matching contribution.

It follows that under all component-constant targets, for every oriented
nonzero gadget uv labelled (d,e), at least one of the three ports in (6)
must be repeated. This statement also applies with the orientation
reversed. In particular, no common-star filling with at most one edge
per ordered port can satisfy all component-constant targets, regardless
of triangles. A missing port already contradicts (5); otherwise every
port is unique and (8)--(9) apply to any edge.

## Shared-neighbor source identity

Fix different components u,v, background color c, and colors d,e different
from c; d=e is allowed. For j outside {u,v}, write

```
A_j=a_uj(d,c), B_j=b_uj(d,c),
C_j=a_vj(e,c), D_j=b_vj(e,c),
s=sum_j A_j B_j, t=sum_j C_j D_j,
h=sum_j A_j B_j C_j D_j,
x=sum_j A_j D_j, y=sum_j B_j C_j.
```

Absent or incompatibly labelled entries are zero. Put q=q_uv(d,e), zero
if that label is absent or d=e. The exact component source is

```
F_(u:d,v:e | c) = (1+s)(1+t)+q+xy-2h.                 (10)
```

Every compatible edge meets u or v, so the common active subset in (1)
has size zero, two or four. The equal center/leaf matchings on four
vertices contribute st-h. The unequal matchings contribute xy-h.
Together with the empty term, the star terms and the central edge, these
give (10). In particular the four-cycle correction is retained.

Assume all singleton and double-component mixed targets. Every singleton
port sum is -1 by (5), including a possible edge to the other distinguished
component. Removing that edge gives

```
1+s=-q_uv(d,c),       1+t=-q_vu(e,c).
```

Their product is zero: the first requires label (d,c) at (u,v), whereas
the second requires (c,e), and d!=c. There is only one label on a
component pair. Thus every double row gives

```
q=2h-xy.                                             (11)
```

There is no small-order exception hidden here. Singleton targets already
force six nonempty ports at each component, hence k>=7 in this simple
one-label construction. For these orders every two-component word used
here is mixed. Orders 2<=k<=6 fail a singleton target.

Use the **state graph** H whose vertices are (u,a), one for each component
and color. A gadget labelled (a,b) joins (u,a) to (v,b), carrying its actual
q product. H is tripartite by color; a state's neighbors in another color
part are exactly its ordered port. There are no edges between different
states of the same physical component.

Two consequences of (11) will be used with their full weighted meaning:

1. Two distinct states of the same color cannot have exactly one common
   neighbor in another color part. If that neighbor is z, then xy=h is
   the product of the two nonzero q values, but q=0 in (11). This would
   give h=0. The assertion also applies after exchanging the two colors.
2. Every state-graph edge has a common neighbor of the third color. With
   no such neighbor, h=x=y=0 would force its q to vanish. If there is
   exactly one such neighbor z, then

```
q_XY=q_XZ q_YZ.                                      (12)
```

These are consequences of actual shared source equations. In particular
(12) is not assumed for triangles with additional common neighbors.

## No singleton port, without bounding other degrees

Suppose state X of color a has unique color-b neighbor Y. If Y had a
second color-a neighbor, that state and X would have exactly one common
color-b neighbor, contrary to consequence 1. Hence Y's color-a port is
also unique, and q_XY=-1.

Let c be the third color. Every edge XZ with Z of color c must belong to
a coherent state triangle. Its only possible color-b neighbor is Y, so
YZ exists. Reversing X,Y proves N_c(X)=N_c(Y). Equation (12) on XZ gives
q_XZ=-q_YZ for every Z in this common set. Summing gives -1=1, because
both color-c port sums are -1. This is impossible over C.

Therefore the singleton and double-component targets force **every
ordered port to contain at least two edges**, regardless of other degrees.

## At most two per port: source-derived resource decomposition

Assume now that every ordered port has at most two edges. The preceding
result makes every port have exactly two. Between any pair of color
parts the state graph is 2-regular. Consequence 1 forces any two row
neighborhoods which intersect to coincide. Thus each connected component
of this bipartite graph is K_(2,2).

At a state X of color a, write its color-b neighbors as Y1,Y2 and its
color-c neighbors as Z1,Z2. Consequence 2 makes the bipartite graph between
these two pairs meet every row and column. Since the full b-c graph is a
disjoint union of K_(2,2)'s, this local 2-by-2 graph is either two disjoint
edges or all four edges. Three edges force the fourth within one block.

In the four-edge case, let X_b be the other color-a neighbor of Y1,Y2.
The edge X_b Y1 needs a color-c common neighbor in {Z1,Z2}. Since color-a
rows have identical or disjoint color-c neighborhoods, X_b has both Z1,Z2
as neighbors. It is therefore also the second color-a neighbor X_c of
Z1,Z2. These six states form a complete K_(2,2,2) component of H: all
their ports are filled and no state-graph edge leaves the component.

In the two-edge case, each edge at X has exactly one common neighbor of
the third color. A neighboring state cannot have the four-edge local
pattern: that would give two common third-color neighbors for the same
edge. Hence each triangle through X has the two-edge pattern at all
three states. Applying (12) cyclically to its three nonzero products
gives q_XY=q_XZ q_YZ, q_XZ=q_XY q_YZ and q_YZ=q_XY q_XZ. Therefore each
product has square one. Every edge at X lies in such a triangle, so its
two q values in a port are both in {1,-1}. Their sum cannot be -1 over C.
This excludes the two-edge local pattern.

Consequently the singleton and double-component equations force H to be
a disjoint union of coherent K_(2,2,2) resources. This is a proved normal
form inside the at-most-two-port common-star family, not an assumed
normal form for general protected arrays.

## Full component target excludes every such resource decomposition

Let R be the number of K_(2,2,2) resources. Each color part of H has k
states and each resource contains two of each color, so k=2R. Pair the
two same-color physical components in each resource. For each color c
this gives a perfect matching P_c on the k physical components: each
component's color-c state occurs in exactly one resource. The six states
in any resource belong to six distinct physical components, since
different-color states of one component cannot be joined by an edge.

The multigraph P_0 union P_1 is a disjoint union of even alternating
cycles; a common matching edge is allowed as a two-cycle. Choose a binary
component coloring using colors 0 and 1 which assigns opposite colors
across every edge of both matchings.

In every resource exactly one color-0 state and one color-1 state are
selected by this component word. No color-2 state is selected. The two
selected states have one compatible gadget between them. Each physical
component selects one state in one resource, so the compatible component
graph consists of R disjoint gadget edges. The exact full source is

```
F(x)=product_(resources r) (1+q_(selected edge of r)).  (13)
```

Each factor is nonzero. The selected edge shares either endpoint's
opposite-color port with one other nonzero gadget q', and q+q'=-1;
therefore 1+q=-q'!=0. The binary coloring is nonconstant since every
P_0 edge has opposite endpoint colors. Equation (13) contradicts its
zero mixed target.

This proves the all-order **at-most-two-port exclusion**, with arbitrary
nonzero complex factor weights and all triangles allowed. Its proof uses
singleton and double-component sources to obtain the resource normal form,
then an additional global component word to contradict the target. It
does not require any non-component-constant minority equation.

## General complete-resource consumer

The final contradiction extends beyond resources of size (2,2,2).
Suppose H is a disjoint union of complete tripartite resources, with
possibly different positive color-part sizes in different resources.
For any resource, summing the singleton q-port normalizations over one
color part and over another counts the same edge sum in two ways.
Their sizes are therefore equal. Write them as (m_r,m_r,m_r).
The no-singleton-port lemma gives m_r>=2 under the singleton and double
targets. Each physical component's three states belong to different
resources: otherwise completeness would give a forbidden edge within
one physical component.

Construct a directed multigraph on resources. For each physical
component u, add an edge from the resource containing (u,0) to the
resource containing (u,1). Every resource has indegree and outdegree
m_r, and there are no loops. A finite nonempty balanced directed graph
contains a simple directed cycle. Start with every component colored 0,
and change to color 1 exactly those components whose directed edges
are on this cycle.

At a resource on the cycle, let X be the color-0 state of its outgoing
cycle edge and Y the color-1 state of its incoming cycle edge. The
selected states are all its color-0 states except X, together with Y.
The compatible graph is a star, so its exact factor is

```
1 + sum_(Z of color 0, Z!=X) q_ZY = -q_XY != 0.      (14)
```

The equality uses Y's complete singleton port normalization. Every
resource off the cycle has no compatible edge and contributes one.
Each physical component selects just one state in one resource, so
these selected graphs are disjoint and the full source is the product
of the factors in (14). It is nonzero. The word is mixed: if there are
R resources then k=sum_r m_r>=2R, while the cycle changes at most R
components and at least one.

Thus **all complete-tripartite resource decompositions are excluded**
under the full component target, at arbitrary resource sizes and
arbitrary complex factors. This is a reusable downstream implication.
The missing upstream statement is a source-derived decomposition for
general larger ports; the theorem above proves it only when every port
has at most two edges. No general decomposition is assumed.

## One binary decomposition is enough

Assume S1 and both types of S2, and fix just one unordered color pair,
say {0,1}. Suppose the bipartite graph H_01 is a disjoint union of complete
bicliques. These binary connected components will be the resources in this
argument; the full tripartite graph H need not split into complete pieces.
S1 ensures every state of colors 0,1 has a neighbor. Summing its actual
q weights by rows and columns balances each biclique as K_(m_r,m_r).
The no-singleton-port lemma, which uses S2 with all three colors, gives
m_r>=2.

A component's states (u,0) and (u,1) belong to different binary resources,
since completeness would otherwise require a forbidden edge between them.
Direct the arc for u from its color-0 resource to its color-1 resource.
This gives a loopless balanced directed multigraph with indegree and
outdegree m_r at resource r. Choose a simple directed cycle and change
exactly its component arcs from baseline color 0 to color 1.

At every resource on the cycle one color-0 state X is removed and one
color-1 state Y is added. The selected compatible graph is a star with
factor

```
1 + sum_(Z of color 0, Z!=X) q_ZY = -q_XY != 0.      (15)
```

No color-2 state is selected anywhere, so all gadgets involving that color
are absent from this full source, regardless of their number or weights.
Each physical component selects one state in one binary resource. Hence
the selected graphs are disjoint, and their physical source factors over
the stars. Off-cycle resources contribute one. The product in (15) is
nonzero, while the word is mixed because its cycle has at most R edges
and k=sum_r m_r>=2R. The full component target is therefore contradicted.

This proves the **binary-resource consumer** for arbitrary complex factors.
It strictly weakens the required structural hypothesis of (14). In
particular, if the ports in just one unordered color pair all have size
at most two, S1/S2 make them exactly two; the same-color S2 prohibition
on one common neighbor makes H_01 a union of K_(2,2)'s. Equation (15)
then excludes the full target, with the other color-pair degrees unbounded.

The [exact alignment countercontrol](PROTECTED_SCAFFOLD_COMMON_STAR_RESOURCE_ALIGNMENT_NO_GO.md)
satisfies S1, S2 and the entire physical U4 system. All its binary graphs
are biclique unions, but their partitions do not align across three colors.
Thus full tripartite alignment does not follow from those inputs; it is
also unnecessary for this consumer. The subsequent
[binary-supply countercontrol](PROTECTED_SCAFFOLD_COMMON_STAR_BINARY_SUPPLY_NO_GO.md)
refutes even the assertion that these inputs force a biclique union for
at least one color pair. The consumer itself remains valid.

## Exact control for the use of the additional global word

The additional global row cannot be omitted. The portable
[repeated-port control](verify_protected_scaffold_common_star_repeated_port_control.py)
constructs k=14 components over Q(sqrt(3)). Index components by
(p,i) in Z/7 x {0,1}, put t=(0,1,3), and label the component edge from
(p,i) to (p+t_b-t_a,j) by (a,b). The six nonzero differences are distinct,
so every component pair has at most one label. Each ordered port has two
edges. For each ordered color pair choose the vector z_ab=(1,1) when b is
the smaller of the other colors, and z_ab=(1,2+sqrt(3)) otherwise. Set

```
a_edge=z_ab[i] z_ba[j],       b_edge=-1/(2 a_edge).
```

The actual 56-vertex physical hafnian and a separate component double-
hafnian evaluation both give the required three constants, 84 singleton
rows and 1092 double rows, including equal changed colors. Their finite
replay corroborates this exact subsystem control; it is not the proof of
the all-order theorem. The alternating fiber word x_(p,i)=i instead has
full component source 2^(-7)=1/128. A separate four-minority word has
source 1/4. Thus this is neither a Q4 model nor a full GHZ witness.

## Remaining Q4 boundary

Any common-star filling satisfying all component targets must have every
port of size at least two. In each of the three unordered color pairs,
at least one port must have size at least three, and at least one connected
binary support component must be noncomplete.
Its state-graph edges must have coherent third-color triangles. These
necessary conditions are not sufficient. The shared-neighbor identity
(10) retains the interference terms which will be needed beyond the
two-port resource decomposition. The weaker binary-resource consumer (15)
closes any larger-port branch with a proved complete decomposition in at
least one color pair. Both tripartite and binary decomposition supply
from S1, S2 and U4 are now refuted by exact controls. A new parent must
retain additional global component equations or a different implication.

The exact parent attempt and its next obstruction are recorded in
[the common-star Q4 parent](../../docs/strategy/common-star-q4-parent-attempt-2026-09-14.md).
General common-star arrays with larger ports, arbitrary protected
fillings, Q4 and the global Krenn--Gu conjecture remain open. No arbitrary
witness-to-common-star reduction is claimed.
