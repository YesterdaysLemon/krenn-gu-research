# Full four-minority sources do not force common-star resource alignment

## Status and exact parent

This is an exact countercontrol to the resource-supply implication RCS,
over Q(sqrt(3)), inside the one-label common-star construction. It is
**not** a counterexample to CSQ4 or Krenn--Gu. Its explicit mixed component
word has amplitude 2^(-360), whereas the target is zero. The global
Krenn--Gu conjecture remains **UNRESOLVED**.

Use precisely the physical arrays, actual factors and source conventions
in [PSCS](PROTECTED_SCAFFOLD_COMMON_STAR_COMPONENT_TARGET_OBSTRUCTION.md):
protected unit K4 components, a simple component graph, one unequal
endpoint-color label per component edge, and one nonzero center factor A
and one nonzero selected-leaf factor B on that gadget. All other crossing
entries vanish. The state graph H has vertices (component,color), with
each gadget joining its two endpoint states and carrying q=AB.

Write S1 for every singleton-component target, S2 for every double-
component target, including equal changed colors, and U4 for **every full
physical source equation** at Hamming distance at most four from a constant
word. The attempted implication was

```
RCS: S1 + S2 + U4 imply that H is a disjoint union of
     complete tripartite components.
```

A hypothetical CSQ4 witness supplies this antecedent. The intended consumer
was PSCS's complete-resource cycle exclusion (14). The explicit finite
array below refutes RCS with all actual weights retained. It leaves a
strictly weaker supply question, because the new binary-resource consumer
(15) in PSCS needs complete bicliques for only one pair of colors.

The [independent review](../../docs/audits/COMMON_STAR_RESOURCE_ALIGNMENT_REVIEW_2026-09-14.md)
audits the source-family classification, exact construction and physical
replay. No Lean formalization or external solver is used. The universal
U4 statement follows from the matching proof below, not enumeration of
the enormous set of physical words.

## Exhaustive crossing classification through four minorities

Fix a background color c. Every crossing edge in a supported physical
perfect matching consumes at least one minority vertex, by hollowness.
There are therefore at most four crossing edges. Their multigraph on K4
components has even degree at every vertex, since uncrossed physical
vertices must be matched internally.

Crossing degree four is impossible with at most four crossing edges.
Its other endpoints would be either one degree-four component, requiring
four edges on a pair that has only two, or two degree-two components.
The latter requires two doubled gadgets, both using the first component's
unique center. Thus every used component has crossing degree two, and
the crossing multigraph is a union of cycles, allowing doubled edges.

At a used component there are exactly two possible local types:

- **AB:** the center and one leaf cross. If the crossed leaf is the
  color-y leaf, the remaining protected edge forces the other two leaves
  to color y as well. All three leaves are y; the center may differ.
- **BB:** two distinct leaves cross, in their own distinct colors. The
  remaining center and third leaf have the third color. This costs two
  minorities if the third color is c and three otherwise.

There is no AA type, since the center can be used only once. Now exhaust
the cycles allowed by the bound:

1. A doubled edge uses both factors of one gadget. Both endpoint K4s are
   monochromatic in different colors. At most four minorities allows
   exactly one whole changed component and no further crossing cycle.
2. A triangle has either no A edges, costing at least six minorities,
   or one A edge and two B edges. The latter has one BB component w.
   If w's remaining color is not c, its crossed color-c leaf forces a
   non-c leaf triple at a neighboring AB component, already costing six.
   Hence w's crossed leaves have the two other colors d,e. The two AB
   leaf triples must be c, or the cost is at least five. Their A edge has
   unequal endpoint colors, so one or both centers are minorities. These
   are the three- and four-minority ABB triangle families.
3. A four-cycle with no A edges costs at least eight minorities. With
   one A edge its two BB components cost at least four, and at least one
   A endpoint is another minority. With two A edges those edges are
   disjoint; each of the two disjoint B edges forces a non-c leaf triple
   at one endpoint, costing at least six.
4. Two disjoint doubled edges cost at least eight minorities. No other
   nonempty crossing-cycle union fits the bound.

With no crossings, a protected K4 can be matched only when all four of
its vertices have the same color: its two disjoint internal edges belong
to one matching M_c. Thus the only remaining possibilities are a pure word
or a singleton changed component. A pure word has amplitude one, and the
singleton amplitude is exactly 1+sum_v q_uv(d,c).

In particular, **S1 and the absence of incoherent component triangles
imply the entire U4 system**. A component triangle is coherent when its
two incident gadget labels agree at each component. An ABB triangle is
incoherent at its BB component, whose two crossed leaves have different
colors. Coherent triangles need not be absent. This sufficiency uses the
complete classification above; it does not assert S1 alone implies U4.

## An exact noncomplete weighted resource

Let P be the 3-by-3 cyclic permutation matrix with ones at (0,1),(1,2),
(2,0), and J the all-ones matrix. Put

```
t=(sqrt(3)-1)/2,    r=2+sqrt(3),
A=J+((sqrt(3)-3)/2)P,
B=-A^(-T)=((sqrt(3)+3)/3)P-(2/3)J,
Q=A Hadamard B=P-(2/3)J.
```

Direct multiplication gives A B^T=B A^T=-I, Q 1=-1 and Q Q^T=I.
For the three color pairs use the base matrices

```
M_01=A^T,       M_12=A,       M_02=I,
N_ab=-M_ab^(-T),             Q_ab=M_ab Hadamard N_ab.
```

Reverse a color pair by transposing. These orientations matter. A resource
has states (a,p,f), with color a in {0,1,2}, base index p in {0,1,2}, and
clone f in {0,1}. Define z_ab=(1,1) if b is the smaller of the other two
colors and z_ab=(1,r) otherwise. Between states (a,p,f),(b,q,h) put

```
A' = M_ab[p,q] z_ab[f] z_ba[h],
B' = N_ab[p,q] / (2 z_ab[f] z_ba[h]),
q' = Q_ab[p,q]/2.                                  (1)
```

An entry absent from the base support stays absent. All displayed supported
factors are nonzero. The 01 and 12 supports are K_(6,6), while the 02
support is three disjoint K_(2,2)'s. The entire 18-state resource is
connected, with 84 edges; a complete K_(6,6,6) would have 108. Its three
binary partitions therefore do not align into a complete tripartite one.

## Local equations retain both factors

S1 holds because cloning divides each q by two and duplicates its column,
so all opposite-color port sums remain -1. For S2 use the exact PSCS
identity q=2h-xy, with h the common-neighbor sum of q products and x,y
the two differently paired A/B contraction sums.

For same-color states with different base indices, the two contractions
are zero by M N^T=N M^T=-I, and h is zero by Q Q^T=I. For different
clones of the same base index the contractions are -z[f]/z[h] and its
reciprocal, while h=(1/2)sum_q Q[p,q]^2=1/2. Thus xy=2h in both cases.
The same calculation applies to columns.

For two distinct changed colors d,e and the remaining color c, the clone
factor is

```
(1+r)(1+r^(-1))/4=3/2.
```

Consequently the lifted S2 equation is equivalent to the base identity

```
Q_de = 2 Q_dc Q_ce
       -3 (M_dc N_ce) Hadamard (N_dc M_ce).            (2)
```

For de=02 the first product is Q^T Q=I and the two contraction products
are -I, yielding 2I-3I=-I. For de=01 or 12, the identity pair contributes
Q_dc Q_ce=-Q_de and the Hadamard contraction is -Q_de, yielding Q_de.
Transposition handles the reverse orientations. This proves all local
distinct-color S2 entries, including those where the direct edge is absent.
No independent symbol has replaced an actual cofactor or factor.

## A finite, legal physical realization

Take G=SL(2,F5), of order 120. In row-major tuple notation let

```
T_0=(I, (1,1,0,1), (3,2,4,3)),
T_1=(I, (2,4,4,1), (4,2,1,2)).                       (3)
```

Resources are h in G. First consider old components (f,g), f in {0,1},
g in G, whose color-a state belongs to resource g T_fa. The pinned finite
replay checks all 120 resource neighborhoods: their radius-three layers
have sizes 1,6,12,60 without collisions. Thus this bipartite incidence
graph has no cycles of length four or six. Distinct old components share
at most one resource; every triangle of pairwise incident old components
belongs to one resource.

Replace (f,g) by three physical K4 components (p,f,g), p in {0,1,2}.
Its state of color a belongs to g T_fa, occupying local state (a,p,f)
there. Install exactly the supported gadgets (1) in each resource.
Copies of the same old component have equal colors whenever they share a
resource, so no gadget joins them. Different old components share at most
one resource. Hence each physical component pair has at most one gadget
with one unequal label, as required by the construction.

There are 720 physical K4 components, n=2880 vertices and 10080 gadgets.
Every actual component triangle projects to three distinct old components,
lies in one resource, and is coherent. The exact replay also enumerates
all 8640 actual component triangles and checks these properties directly.
S1 and the crossing classification therefore prove every full U4 equation.

For the global S2 bridge, each component-color state belongs to exactly
one resource. Two selected states in different resources have no common
opposite-color neighbor and no direct edge: q=h=x=y=0. In the same
resource, the local equations just proved apply. A selected component's
background state cannot re-enter one of these local sums: the old color
resources at that component are distinct. Removing the other selected
component can delete a background spoke, so the exterior star sums must
not simply be assumed to stay -1. Instead PSCS gives
1+s=-Q_dc[u,v] and 1+t=-Q_ce[u,v]; their product is zero because the
two factors require incompatible labels on the same component pair.
This also holds when the changed colors coincide. Thus the finite array
satisfies all actual S1 and both S2 families, not merely a local block
model with unproved assembly semantics.

Its state graph consists of 120 connected 18-state, 84-edge resources,
each noncomplete. This proves the asserted counterexample to RCS.

## Full target failure and exact replay boundary

Color every clone-zero component 0 and every clone-one component 2. In
each resource the selected graph consists of three disjoint 02 gadgets,
one per base index, each with q=-1/2. Globally these are 360 disjoint
gadgets covering all 720 components. The mixed component source is

```
F=(1-1/2)^360=2^(-360) != 0.                          (4)
```

The literal selected scalar graph on 2880 physical vertices splits into
360 four-cycles and 720 isolated protected edges. Exact hafnian recursion
on these scalar connected components checks (4) and counts 2^360
supported perfect matchings. This is a full physical source replay,
with factorization justified by its actual connected components.

The primary [checker](verify_common_star_resource_alignment_control.py)
reads the tracked [fixture](../../tests/fixtures/common_star_resource_alignment_control.json).
The independent [audit](audit_common_star_resource_alignment_control.py)
reconstructs its algebra and physical incidence separately. The local
72 S1, 180 ordered same-color and 216 ordered distinct-color S2 checks
are finite corroboration. Global S2 uses the proved assembly bridge;
global U4 uses the exhaustive classification and checked triangle property.
Neither checker claims to enumerate all physical U4 words or all 3^720
component words. The displayed failure specifically rules out calling this
array a CSQ4 or global counterexample.

## Sharper remaining implication

RCS is refuted. A full tripartite resource alignment is unnecessary for
the contradiction: PSCS (15) excludes a common-star full target whenever
**one** binary state graph H_ab is a disjoint union of complete bicliques.
S1 balances each biclique and S2 excludes size one; a directed cycle of
binary resources gives a nonzero mixed word using only colors a,b.

The new supply question BS asks whether S1+S2+U4 implies this property for
at least one color pair. The present countercontrol satisfies that weaker
property for all three pairs, so it does not refute BS. BS is open; it
is not inferred from this example or from pairwise neighborhood counts.
The [parent record](../../docs/strategy/common-star-q4-parent-attempt-2026-09-14.md)
tracks this change of implication. Arbitrary protected fillings and an
arbitrary-witness reduction remain separate open obligations.
