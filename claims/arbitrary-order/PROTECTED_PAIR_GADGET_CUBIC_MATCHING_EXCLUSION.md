# Protected sparse crossings and the cubic matching obstruction

Date: 2026-09-22.

Status: proved over C by the argument below, with an explicit imported
matching theorem and a completed independent mathematical audit. An
[elementary directed-cycle proof](PAIRED_RESOURCE_DIRECTED_CYCLE_EXCLUSION.md)
now supplies an independently reviewed alternative for the full-family
exclusion, including a broader paired-block family. The cubic correspondence
and imported proof below remain valid; the import is no longer necessary
for the exclusion. No Lean
formalization is supplied. The Krenn--Gu conjecture remains **UNRESOLVED**.

This is a complete construction-family exclusion and an exact interface for
the weighted one-pair parent WP1. It is not a normal form for arbitrary
protected arrays. The definitions of the protected scaffold and of the
physical coefficient T_W are those of
[PSMR](PROTECTED_SCAFFOLD_MINORITY_CYCLE_AND_RESOURCE_BOUNDARY.md).

Section 5 also proves a macro-driven normal form: with **at most one
supported crossing entry per physical vertex/color state**, the singleton
macro targets force the complete pairing in Section 1. Consequently this
entire sparse-crossing class is excluded from the full source. The result
still supplies no paired-minority-depth bound and does not exclude WP1.

## 1. Exact family and parent

Take k>=2 protected unit K4 components. Their six colored edges are the two
edges in each of

```text
M_0={01,23}, M_1={02,13}, M_2={03,12}.
```

Partition all 6k protected colored edges into 3k unordered pairs. Every pair
must join edges of different colors in different physical components. If a
pair comprises e={u_1,u_2} of color a and f={v_1,v_2} of color b, choose a
bijection between e and f and add the corresponding two crossing entries
of color (a,b), with arbitrary nonzero complex weights alpha and beta.
There are no other crossing entries. Reverse physical orientation transposes
the color matrix, as usual.

Call this a **complete protected-edge pairing**. Each physical vertex/color
state (v,c) belongs to its unique protected M_c edge, and therefore to one
gadget. Consequently different gadgets never prescribe the same scalar
entry. No bipartition of the components, uniform port allocation, simplicity
of a component projection, or six-layer description is required.

The earlier
[PSFD construction](PROTECTED_SCAFFOLD_FIXED_MINORITY_DEPTH_NO_GO.md)
is a specialization. Its complementary pair allocation pairs every protected
edge exactly once and sets alpha beta=-1 in every gadget.

**Theorem.** Every complete protected-edge pairing with all crossing weights
nonzero has a mixed physical word with exactly one supported perfect matching.
Its coefficient is nonzero. Hence no array in this family realizes the full
GHZ source, over C and at any permitted order.

The present proof does not bound the paired-minority depth of that word.
WP1 requires all macro targets and all mixed min_c q_c<=1 coefficients to
vanish, where q_c counts complete minority M_c pairs. Its restriction to
this family remains a separate question after the full-source exclusion.

## 2. The complete state graph and local coefficients

Replace each physical vertex v by its three states (v,0),(v,1),(v,2).
Include the supported scalar edges between states. A protected edge has
weight one; the two crossings of a gadget have weights alpha,beta.

Every state has exactly one protected neighbor and one crossing neighbor.
For one gadget these four states form a C4: its two protected edges are
opposite, and its two crossings are opposite. Since states belong to unique
gadgets, the entire state graph is a disjoint union of these C4s.

A physical word selects exactly one state at each physical vertex. Its
literal scalar graph is the induced graph on these selected states. Its
matching sum factors over the gadgets, with these exhaustive local cases:

| Selected states in one gadget | Local coefficient |
| --- | --- |
| none | 1 |
| an adjacent pair | the weight of their single edge |
| an opposite pair, or an odd number | 0 |
| all four | 1+alpha beta |

In particular, a word selecting only empty gadgets and adjacent pairs has
exactly one supported matching, with nonzero product weight. This assertion
does not assume alpha beta=-1. When that product is -1 for every gadget,
these are exactly the nonzero words: every fully selected C4 cancels.

## 3. A cubic graph encoding the surviving words

For each state C4, let P and Q be its bipartition classes. Each class contains
one state of color a and one of color b. Introduce two auxiliary vertices
p_g,q_g joined by an edge. Join p_g to the two physical vertices underlying
P and q_g to those underlying Q. Do this for every gadget; retain the
original physical vertices but none of their original edges. Denote the
resulting unweighted graph by H.

Every physical vertex has three incident edges, one for each of its states.
Every auxiliary vertex has two physical neighbors and its auxiliary partner.
Thus H is cubic. It is simple: the four physical vertices of each gadget are
distinct, and different gadgets have different auxiliary vertices.

Color each physical-auxiliary edge by its physical state color, and color
the auxiliary edge by the third color outside {a,b}. Each vertex now sees
all three colors exactly once. Therefore H has a specified proper
three-edge-coloring, whose color classes C_0,C_1,C_2 are perfect matchings.

H is triangle-free. Physical vertices are independent and the auxiliary
subgraph is a matching. A remaining possible triangle would require one
physical vertex adjacent to both auxiliaries of the same gadget, which
cannot happen because its four ports are distinct and partitioned by P,Q.

A perfect matching N of H has precisely two local choices at a gadget:

1. use p_g q_g, selecting no physical state there; or
2. match each auxiliary to one physical neighbor, selecting an adjacent
   pair of states of the original C4.

Each physical vertex is matched once, so N chooses one color at that vertex.
This gives a physical word having a unique original matching by Section 2.
Conversely such an empty/adjacent-pair word fixes its matching N: a selected
state fixes its spoke, and an unused gadget fixes its auxiliary edge.
For all nonzero weights this is a bijection between PM(H) and the
empty/adjacent-pair words, and hence an injection into nonzero physical
coefficients. It is injective on words, not merely on original matching
terms. Under alpha beta=-1 its image is all nonzero physical coefficients.

The three pure words are exactly C_0,C_1,C_2. At a gadget incident with color
c, the pure word selects its protected color-c pair and the two color-c
spokes. At a gadget whose endpoint colors omit c, it selects no states and
uses the color-c auxiliary edge. Thus no additional matching can map to a
pure word.

## 4. Imported matching theorem and full-source exclusion

We use the following external result with its hypotheses intact:

> A connected matching-covered graph has exactly three perfect matchings
> precisely when it is a bi-subdivision of Theta or K4.

Here matching-covered means that every edge belongs to a perfect matching;
Theta has two vertices and three parallel edges. A bi-subdivision inserts
an even number of vertices into each subdivided edge. This is Theorem 2.4,
Section 2.1 of [Kothari, Lee, Lucchesi and da Silva,
*Cubic graphs, S-minors and conformal minors*, arXiv:2606.04173v1](https://arxiv.org/html/2606.04173v1#S2.SS1).
Its statement and proof, and the matching-covered definition, were inspected;
the theorem is an explicit imported proof dependency.

Each connected component of H is matching-covered, because restricting
each color class to that component is a perfect matching. It has at least
three distinct perfect matchings. If it had exactly three, the imported
theorem would make it a bi-subdivision of Theta or K4. Cubicity rules out
every inserted degree-two vertex. Simplicity excludes Theta, and the absence
of triangles excludes K4. Hence every component has at least four perfect
matchings, and H has more than three.

Section 3 now supplies a mixed word with a unique supported original
matching. Its nonzero monomial cannot equal the required mixed coefficient
zero. This proves the stated full-family exclusion. It does not use numerical
search, a finite order bound, or an assumption that H is connected.

## 5. Singleton macro supply forces the pair normal form

Consider a protected unit-K4 array whose crossing support has degree at
most one at every state (v,c). This counts supported scalar entries, not
physical neighboring vertices or ranks of color matrices. Crossings are
hollow and join different protected components, as before.

Assume only that, for each component A, color a, and different background
color c, the component-constant word with color a on A and c everywhere
else has a matching other than its protected matching. Every weighted
macro target implies this support supply: the protected monomial is one,
so a zero coefficient requires another term. We use no independence of
the weights and no cancellations chosen separately for different words.

**Normal-form proposition.** This singleton supply forces a complete
protected-edge pairing. Moreover the two M_a edges in every component A
are paired one to each of the other two colors. In particular every state
has crossing degree exactly one.

To prove it, include all protected edges and supported crossings in the
state graph. Every state has its one protected edge and at most one
crossing. Its components are alternating paths and even cycles. On a
component-constant word the protected edges give a perfect matching P.
Any different matching N has a nonempty symmetric difference with P,
consisting of alternating cycles. Since the state graph has maximum
degree two, each is a complete component of that graph; paths cannot
supply an alternative matching.

Fix A and a. For either other color c, singleton supply therefore gives
a complete state cycle C_c selected by the word a on A, c outside. Collapse
the protected edges of C_c. Each crossing joins different colors, and only
a,c are present, so the protected-edge colors alternate a,c around the
cycle. All its color-a protected edges lie in A and all color-c protected
edges lie outside A.

The two backgrounds give two distinct state cycles: a cycle containing
the first background color cannot be selected by the other singleton
word. They are disjoint and each uses at least one of A's exactly two
color-a protected edges. Thus each uses exactly one. Alternation then
gives exactly one exterior protected edge, so both cycles are C4s. Their
crossings form endpoint bijections. Applying this to every A,a exhausts
all protected edges, proves the pairing, and proves the stated allocation
to the other two colors.

If the singleton macro coefficients actually vanish, every gadget moreover
has alpha beta=-1. After the normal form, the word a on A and c outside
fully selects exactly the gadget assigned to (A,a,c): its other gadget
uses the third color, and an exterior-exterior gadget cannot have both
endpoint colors c. The singleton coefficient is therefore exactly
1+alpha beta. These are the actual shared crossing weights.

**Sparse-crossing corollary.** No protected array with crossing degree at
most one at every state is a full GHZ source, for any k>=2 and arbitrary
complex weights on its supported entries. If singleton supply fails, the
corresponding mixed macro word has exactly its protected term and
coefficient one. If supply holds, the normal-form proposition and Sections
2--4 supply a mixed unique-matching word. Both alternatives contradict the
full target.

This is a conditional support normalization supplied by actual macro
equations under the stated degree bound. It is not a normalization of
arbitrary protected arrays. In particular, the second alternative does
not locate its word at low q; WP1 is reduced to the balanced complete-pair
case, not excluded by this corollary.

## 6. The remaining one-pair matching question

In the cancellation specialization alpha beta=-1, assign to N in PM(H) the
physical word a(N) defined by its spokes. The full weighted one-pair system
is equivalent to these two graph conditions:

* no non-color-class matching induces a component-constant word; and
* no non-color-class matching has min_c q_c(a(N))<=1.

The first is the macro target. The second is the low-paired-depth target.
The three color matchings already supply the pure normalization. This is an
exact reduction, since the source coefficient of every other surviving
word is one nonzero monomial.

The imported theorem supplies an additional matching, but supplies neither
of these properties for its word. A genuinely load-bearing next lemma would
force an extra matching violating one of the two conditions, or provide an
exact graph satisfying both. Counting more matchings alone does not settle
WP1, and the present full-source corollary must not be used as such a proof.

The broader protected source SFULL is still open because a general hollow
array need not have a complete protected-edge pairing. Common-star supports
and arbitrary arrays with several crossings at one vertex/color state are
outside this theorem's hypotheses. No arbitrary-witness reduction or Lean
formalization is supplied.

## 7. Evidence boundary

The state decomposition and auxiliary-graph correspondence are proved above
for the whole family. Finite exact replays check the correspondence and its
weight boundary; they are not an exhaustive proof over graph orders.
The [independent audit](../../docs/audits/PROTECTED_PAIR_GADGET_CUBIC_REVIEW_2026-09-22.md)
checks the family, the word bijection, disconnected graphs, the weight
boundary, and every hypothesis of the imported theorem. It also supplies
a separate word-first reconstruction of the two-K4 correspondence.

Run the three portable exact checks from the repository root:

```text
python claims/arbitrary-order/verify_protected_pair_gadget_cubic_bridge.py
python claims/arbitrary-order/audit_protected_pair_gadget_cubic_bridge.py
python claims/arbitrary-order/audit_protected_state_degree_one_macro_normal_form.py
```

The [primary replay](verify_protected_pair_gadget_cubic_bridge.py) enumerates
physical matching terms and auxiliary matchings separately. A two-K4
control has 30 auxiliary matchings and 30 nonzero words, including 27 mixed
words. A three-K4 control with a nonbipartite component triangle has 160
auxiliary matchings and 160 nonzero words, including 157 mixed words.
Changing its crossing weights to positive nonzero values keeps those 160
unique-matching words but gives 281 nonzero words in total, checking the
injection-versus-bijection distinction.

The [independent replay](audit_protected_pair_gadget_cubic_bridge.py) starts
with a separate port allocation and enumerates all 6561 physical words and
their literal scalar matching graphs. It recovers 30 nonzero words and
30 auxiliary matchings. Neither script imports the other's implementation
or project scientific code. Neither establishes the arbitrary-order
matching theorem computationally or checks a WP1 solution.

A third [standalone replay](audit_protected_state_degree_one_macro_normal_form.py)
switches two crossings while preserving state crossing degree one, merging
two C4s into a C8. Literal physical matching enumeration finds two mixed
singleton macro words with only their protected terms. This is an exact
control of Section 5's supply boundary. Two separate derivations audited
that section's all-order proof, including the at-most-one degree condition
and the product -1 consequence of weighted singleton equations.
