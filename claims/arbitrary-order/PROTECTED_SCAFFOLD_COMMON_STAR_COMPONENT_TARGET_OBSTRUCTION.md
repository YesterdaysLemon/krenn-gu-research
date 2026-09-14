# Common-star obstruction from global component targets

## Status and scope

The source identities and obstructions below have direct proofs over C
and were independently reviewed, including the unique-port extension, on
2026-09-14. The
[independent review](../../docs/audits/PROTECTED_SCAFFOLD_COMMON_STAR_REVIEW_2026-09-14.md)
records exact physical replays and the cycle, triangle, and multiple-label
controls. No Lean formalization is supplied.

This result rejects a declared construction route for the
[Q4 parent](../../docs/strategy/scaffold-q4-parent-attempt-2026-09-14.md):
common-star pair gadgets on a triangle-free component graph, and gadgets
with at most one edge in each ordered color port even when triangles are
present. It is not a normal-form theorem for arbitrary hollow fillings and
does not prove Q4.
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

## Remaining Q4 boundary

Together the two obstructions require both triangles and the specified
local port repetition in any common-star filling satisfying the global
component targets. They give necessary conditions, not a sufficiency
claim. Both use literal component-constant sources, which are supplied by
Q4, and make no normal-form assertion about arbitrary hollow fillings.

This closes the proposed triangle-free common-star construction route
and its extension to arbitrary triangles with unique ordered ports. It
does not eliminate common-star arrays with interacting triangles and
repeated ports, classify general protected fillings, or resolve the
all-k Q4 parent.
