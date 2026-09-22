# No fixed minority depth excludes the protected scaffold

Status: proved by the constructive argument below over C. Independent
review has found the argument sound; the separate audit binds the final
artifacts. The verifier supplies exact finite controls, not an exhaustive
check of the arbitrary-depth statement. No Lean formalization is supplied.

This is a proper-subsystem mechanism obstruction, not a full-target source
and not an arbitrary-order scaffold exclusion. The global Krenn--Gu
conjecture remains **UNRESOLVED**.

The later [complete pair-gadget theorem](PROTECTED_PAIR_GADGET_CUBIC_MATCHING_EXCLUSION.md)
excludes the entire complete protected-edge-pairing family containing these
controls from full GHZ, for arbitrary nonzero crossing weights. It supplies
no uniform minority-depth bound and does not change this no-go theorem's
fixed-depth quantifiers.

The upstream family and its structural-gate boundary are owned by the
[pure-matching scaffold theorem](PURE_MATCHING_SCAFFOLD_STRUCTURAL_GATE_NO_GO_THEOREM.md).
The full source is the sum of products of physical edge entries over all
perfect matchings, and its GHZ target is one on the three constant words
and zero on every mixed word. No cofactor is treated as an independent
variable. The
[minority-cycle and exterior-resource theorem](PROTECTED_SCAFFOLD_MINORITY_CYCLE_AND_RESOURCE_BOUNDARY.md)
explains why a literal two-component restriction need not equal a larger
source slice. No reduction of arbitrary sources to this scaffold is assumed.

## Theorem and quantifiers

For every fixed integer r>=0 there exists a finite k>=2 and a protected
n=4k scaffold with all entries in {0,1,-1} such that

```
T_W(a)=delta(a) whenever some color occurs at least n-r times,
```

but some mixed full word has coefficient exactly one. The graph and its
order depend on r. The theorem refutes every fixed-depth minority
parent uniformly in order; it says nothing about a depth that grows with
the order or about one array satisfying all depths simultaneously.

## Labelled component graph and literal physical array

Use a finite simple 6-regular bipartite graph with shores L,R. Its six
edge labels are the ordered distinct color pairs

```
01,02,10,12,20,21,
```

each occurring once at each component vertex. Each graph vertex becomes
a protected K4 on local vertices 0,1,2,3, with

```
M_0={01,23}, M_1={02,13}, M_2={03,12},
```

and physical color matrix E_cc on every edge in M_c. An edge from L to R with
label cd has exactly two nonzero crossing entries of color (c,d), at the
following local row/column positions, with weights +1,-1 in displayed order:

```
01: (2,3),(3,1)       02: (0,3),(1,0)
10: (1,1),(3,0)       12: (0,2),(2,1)
20: (1,3),(2,2)       21: (0,0),(3,2).
```

All other crossing entries are zero. Matrices reverse by transpose.
For any fixed color c at an L component, its labels cd for the two d!=c
use the two disjoint M_c pairs. For any fixed color d at an R component,
its two labels cd use the two disjoint M_d pairs. These assertions follow
directly from the table. Each individual gadget is a bijection between its
allocated endpoint pairs and has crossing-weight product -1.

## Forest lemma for a source matching

Fix a word with at most r minorities relative to a color c, and suppose
one of its full physical matching terms is nonzero. Every crossing physical
edge has different endpoint colors, hence contains a minority vertex.
The matching uses at most r crossing physical edges, and consequently at
most r distinct edges of the component graph.

If that graph has girth greater than r, the graph of used component edges
is a forest. Removing any one of its edges partitions its tree into two
sets of whole K4 components, each containing an even number of vertices.
The number of physical matching edges across this cut is even. The only
used gadget across the cut contains at most two physical crossing entries,
so both must be used.

Thus every used gadget consumes its complete allocated pair at each end.
At a component there are at most two used gadgets. If there are two, their
allocated physical pairs must be disjoint. Edges in different perfect
matchings of K4 always intersect, so the two pairs have the same scaffold
color; all four vertices therefore have that color. If there is only one
used gadget, its complementary internal pair has the same scaffold color,
and again the whole component is monochromatic. A component with no used
gadget has an internal perfect matching, which must be one of M_0,M_1,M_2.
Its two nonzero matrix-unit edges force all four local colors equal. Therefore
every word supporting a nonzero matching in this regime is constant on
every component.

In particular, a non-component-constant word with <=r minorities vanishes
termwise. This argument uses the actual matching, not an effective matrix.

## Exact component-constant amplitude

For a component-constant word, call a gadget available if its two endpoint
component colors equal its ordered label. At a fixed component color, the
at most two available gadgets use disjoint allocated pairs. Thus the
entire scalar graph is a disjoint union of untouched protected edges and
four-vertex gadget cycles. Each gadget has the two matching choices with
weights 1 and -1. Consequently, at every order and without a girth condition,

```
T_W(a) = product_(available gadgets) (1-1).            (1)
```

The empty product is one.

Suppose the word is mixed, with <=r minorities relative to c. Let S be
the non-c components, so 1<=|S|<=r/4. If no gadget were available, each
component v in S, of color d!=c, could follow its unique incident gadget
whose label expects d at v and c at its opposite endpoint. That neighbor
must also belong to S. The resulting directed graph on S has out-degree
one. No edge can be immediately reversed: the first gadget expects c at
its other endpoint, whereas that endpoint's actual color is not c.
A directed cycle therefore gives a simple cycle of length >=3 in the
component graph, with length at most |S|<=r/4. This contradicts girth>r.
There is at least one available gadget, and (1) is zero.

Pure words have no available gadget and coefficient one. Combined with the
forest lemma, this proves the required equations through minority depth r
on every labelled graph of girth>r. For r<4 there are no mixed
component-constant words within the depth bound, so that case needs no
availability argument.

## Explicit base graph and explicit full-target failure

Let L_i,R_j be indexed by Z/31. For the labels in the displayed order use
the shifts

```
D=(0,1,3,8,12,18),   L_i -- R_(i+D_label).
```

The 30 ordered nonzero differences of D are exactly the nonzero residues
modulo 31. This proves simplicity and absence of four-cycles; bipartiteness
then gives girth at least six. It has 62 components and n=248 physical
vertices, and already supplies the theorem for r<=5.

Here is an exact mixed component coloring with no available gadget:

```
L: 0100100100100100101001002000000
R: 0000120100100100100201001000000.
```

Read each digit as the color of all four vertices of the corresponding
component. Directly checking the 186 labelled edges gives no endpoint
color pair equal to its edge label. All crossing scalar entries vanish;
the remaining full source has precisely its protected internal matching
of weight one. Thus this word has coefficient one and target zero. There
is no apparent full-target candidate.

## Elementary finite construction of arbitrarily large girth

For r>=1 let B_r consist of words of length at most r in six letters, with
no two consecutive letters equal. Include the empty word. For each letter
l define a permutation s_l of B_r as follows: remove an initial l if
present; otherwise prefix l when the resulting word still lies in B_r;
fix the remaining boundary words. This is an involution. Its non-fixed
pairs are exactly w,lw with |w|<r and w not starting with l.

For every reduced word l_1...l_t with 1<=t<=r, the permutation product
s_(l_1)...s_(l_t), with the rightmost permutation applied first, sends the
empty word to l_1...l_t, so it is not the
identity. Let G be the finite subgroup of Sym(B_r) generated by the six
s_l. This argument proves that G has no nonempty reduced relation of
length at most r; no enumeration of G is needed.

Now take component vertices L_(g,i),R_(g,i), for g in G and i in Z/31.
For each label l add the edge

```
L_(g,i) -- R_(g s_l, i+D_l).
```

It is a finite simple bipartite 6-regular graph, with one edge of each
label at each vertex, and maps to the base graph by forgetting g.
Simplicity also follows from the distinct shifts D_l. At a right vertex
the unique label-l neighbor is L_(g s_l,i-D_l), since s_l is an involution.

A simple cycle of length <=r cannot have equal adjacent labels: there is
only one incident edge of each label. Traversing its G coordinate would
give a nonempty reduced relation among the s_l of that length, a
contradiction. Thus its girth exceeds r. The construction is finite but
potentially very large; it is an existence proof, not a proposed group
enumeration. A finite 6-regular graph contains a cycle, so the component
count exceeds r once its girth does, and in particular n>r. For r=0 the
base graph suffices.

Pull back the base failure coloring by the index i. Every lifted edge has
the same two endpoint colors and label as its base edge. No gadget becomes
available; the mixed full amplitude is still one. This proves the claimed
proper-subsystem boundary at every fixed minority depth.

## Exact replay and independent audit

Run the portable standard-library verifier:

```text
python claims/arbitrary-order/verify_protected_scaffold_fixed_depth_control.py
```

The [finite verifier](verify_protected_scaffold_fixed_depth_control.py)
checks the 62-vertex component graph, its 186 labelled edges and girth six,
all allocation slots and crossing-weight products, and the 744 nonzero
entries of the literal n=248 physical array. It directly computes all three
pure amplitudes, all 372 single-minority-component amplitudes, and the
displayed mixed failure. It also checks the word-ball involutions and
nontrivial products for radii 1,2,3, on sets of sizes 7,37,187.

This is not an exhaustive enumeration of all words through minority depth
four, nor an enumeration of the finite groups at general r. Those
quantifiers are owned by the written proof. The verifier prints its JSON
receipt and writes no files by default. The separate
[independent review](../../docs/audits/PROTECTED_SCAFFOLD_FIXED_DEPTH_REVIEW_2026-09-14.md)
records its derivation checks and finite evidence independently of the
primary verifier.

## The sharper parent Q4 remains open

Define Q4 as follows: for every k>=2, no protected n=4k scaffold satisfies
both all 3^k component-constant target equations and all full source target
equations with at most four minorities relative to some color. These are
equations on the same physical edge array, retaining the exterior resource
contributions. Q4 is an open parent proposition, not a consequence of this
theorem. The present construction fails an explicit component-constant
word, so it does not refute Q4.

For the pair-allocation family used here, equation (1) gives a precise
subproblem. A component coloring avoids a labelled edge when its endpoint
colors do not equal that edge's ordered color pair. The component-constant
target holds exactly when the label-constraint graph has only the three
constant avoiding colorings. This equivalence uses no girth assumption.
It characterizes this constructed family, not arbitrary protected
fillings. Combining those global component equations with the four-minority
resource equations is the next proposed mechanism; no exclusion or
countermodel for Q4 is asserted here.

