# Independent audit of the state-C4 cubic bridge

Date: 2026-09-22

## Verdict

**PASS.**  The state-gadget to cubic-graph translation is exact, and the
claimed perfect-matching consequence follows from the precise hypotheses of
Kothari--Lee--Lucchesi--Nunes da Silva, Theorem 2.4.  The proof applies to a
broader protected-edge pairing family: pair all `6k` protected colored edges,
requiring the two edges in each pair to have different colors and lie in
different K4 components, and join their endpoints by any bijection with two
nonzero crossing factors.  With no other crossings, every such filling has a
mixed physical word with a unique supported perfect matching.  Consequently
no such filling is a full source.  The bipartite six-layer allocation is a
special case; no shore, layer, or uniform local-allocation hypothesis is used.

The theorem does **not** bound the paired-minority depth of the extra word.
It therefore does not exclude WP1: the fourth matching may map to a word with
`min_c q_c>=2`.  No global Krenn--Gu conclusion or arbitrary-filling
normal form follows.

## 1. Exact state decomposition and general family

Each protected K4 has six colored protected edges, two in every `M_c`.  For a
fixed color `c`, `M_c` covers all four physical vertices once.  Consequently,
over all protected colored edges, every physical color state `(v,c)` occurs
exactly once.

Partition these `6k` colored edges into `3k` unordered pairs.  Require the two
edges in a pair to have distinct colors `a!=b` and to belong to distinct K4
components.  Choose either endpoint bijection between them and add the two
corresponding nonzero crossing entries; add no other crossing entries.  The
color and component restrictions make every crossing entry hollow.  Since
the colored protected edges partition the states, different gadgets cannot
duplicate a scalar state edge.

For every paired-edge gadget `g=(a,b)`, the four relevant
physical color states form a `C4` with two protected edges and the two
allocated crossing edges.  The protected-edge pairing partitions all states
`(v,c)` among these gadgets: each physical vertex has one state of each color,
and each state belongs to exactly one gadget.  This is the only global
allocation property used below.

For a physical color word `w`, select `(v,w_v)` at every physical vertex.
Because the state gadgets are disjoint, its compatible scalar graph is the
disjoint union of the subgraphs induced in the individual `C4`s.

If each crossing-pair product is `-1`, the local coefficient is:

| selected states in a gadget | local coefficient |
| --- | --- |
| 0 | `1` |
| 1 or 3 | `0` |
| 2 adjacent | the single selected edge weight, nonzero |
| 2 opposite | `0` |
| 4 | `1 + (crossing product) = 0` |

Hence the global coefficient is nonzero exactly when every gadget selects
zero states or two adjacent states.  Such a word has one and only one
physical scalar matching.  Without the product `-1` premise, every word of
this zero/two-adjacent form still has that unique nonzero matching; only the
converse characterization of all nonzero words is lost.

## 2. Auxiliary cubic graph and matching bijection

Use the bipartition `P_g,Q_g` of each state `C4`.  Each class contains one
`a`-state and one `b`-state.  Construct `H` with:

* one node for every physical vertex;
* two auxiliary nodes `P_g,Q_g` for every gadget;
* a spoke from an auxiliary class to the physical owner of each of its two
  states; and
* the internal edge `P_g Q_g`.

Color a spoke by its state color and color `P_gQ_g` by the third color not in
`{a,b}`.

Every perfect matching of `H` behaves in one of two ways at a gadget:

1. it uses `P_gQ_g`, selecting no state; or
2. it omits `P_gQ_g` and uses one spoke at each auxiliary vertex, selecting
   one state in each `C4` bipartition class, hence two adjacent states.

At each physical node the matching chooses exactly one of the three state
spokes, so it defines a color word.  Conversely a zero/two-adjacent word
forces the internal edge or the two spokes at every gadget.  These maps are
inverse.  Thus

```text
PM(H)  <->  words selecting 0 or 2 adjacent states in every gadget.       (1)
```

The word determines the matching, so (1) is injective even when the crossing
products are arbitrary nonzero values.  Each image word has exactly one
physical scalar matching and therefore a nonzero coefficient.

## 3. Structure of H

The advertised graph properties are literal in the general paired-edge
family.

* A physical node has its three state spokes, one of each color.
* An auxiliary node has its `a`-spoke, its `b`-spoke, and the internally
  matched third-color edge.

Therefore `H` is cubic and properly 3-edge-colored; each color class is a
perfect matching.  All physical nodes form an independent set and all
auxiliary-auxiliary edges form a matching.  A triangle would consequently
have to use `P_gQ_g` and a physical node adjacent to both auxiliaries.  The
four gadget states have four distinct physical owners, so this cannot occur.
The same fact prevents parallel spokes; distinct gadgets have distinct
auxiliary nodes.  Thus `H` is simple and triangle-free.

For every connected component `C` of `H`, the restriction of each color class
is a perfect matching of `C`.  Every edge lies in its own color-class matching,
so `C` is matching covered in the source paper's sense.

## 4. Primary theorem and exact application

The primary source is:

* N. Kothari, O. Lee, C. L. Lucchesi, and C. Nunes da Silva,
  [*Cubic graphs, S-minors and conformal minors*, arXiv:2606.04173v1,
  Section 2.1, Theorem 2.4](https://arxiv.org/html/2606.04173v1#S2.SS1).

Theorem 2.4 states that a matching-covered graph has precisely three perfect
matchings if and only if it is a bi-subdivision of `Theta` or `K4`.  The paper
allows parallel edges generally and defines matching covered to include
connectedness; applying it componentwise is therefore necessary and valid.

Each component of `H` already has three distinct perfect matchings from the
proper edge coloring.  If it had exactly three, Theorem 2.4 would make it a
bi-subdivision of `Theta` or `K4`.  A nontrivial bi-subdivision contains
degree-two vertices, impossible in a cubic graph.  The component would thus
be `Theta` itself or `K4` itself.  Simplicity excludes the three-parallel-edge
`Theta`, and triangle-freeness excludes `K4`.  Therefore every component has
at least four perfect matchings, and so does `H`.

The three color-class matchings map under (1) to the three pure physical
words.  Any fourth perfect matching is different from all three and, by the
bijection, maps to a different, hence mixed, color word with one supported
physical matching.  Its coefficient is a product of nonzero factors.

This conclusion does not require crossing-pair product `-1`.  That product is
needed only when one wants all other words containing a fully selected gadget
to cancel and the macro coefficient to factor into `(1-1)` terms.

## 5. Independent literal reconstruction

The [independent replay](../../claims/arbitrary-order/audit_protected_pair_gadget_cubic_bridge.py)
builds an instance of the complete general paired-edge family on
two protected K4 components.  It also realizes the local six-label allocation,
though its component-layer description has repeated component pairs and is
not a simple six-layer macro graph.  The broader paired-edge theorem does not
require component-graph simplicity.

The script independently:

* allocates all 24 physical color states to six disjoint `C4`s;
* constructs the 20-vertex, 30-edge auxiliary graph;
* checks cubicity, simplicity, triangle-freeness, and the proper 3-edge
  coloring;
* enumerates all perfect matchings of `H`;
* enumerates all `3^8=6561` physical words and their scalar perfect matchings;
  and
* verifies the exact PM/word bijection and coefficient rule.

Receipt:

```text
state_gadgets=6 H_vertices=20 H_edges=30
H_perfect_matchings=30 nonzero_words=30
mixed_unique_words=27
proper_3_edge_coloring=PASS simple=PASS triangle_free=PASS
pm_word_bijection_and_coefficients=PASS
N1_CUBIC_BRIDGE_RECONSTRUCTION_PASS
```

Run:

```text
python -X utf8 claims/arbitrary-order/audit_protected_pair_gadget_cubic_bridge.py
```

## Accepted implication and remaining gap

The accepted implication is

```text
all protected colored edges paired across distinct colors and K4s
+ endpoint bijections with two nonzero crossing factors per pair
+ no other crossings
=> some mixed physical word has exactly one matching
=> not a full source (and not unrestricted UPM).                         (2)
```

The complete two-independent-pair product construction is a corollary.  If
each crossing-pair product is `-1`, (1) additionally classifies all nonzero
words.  This condition is exact: since the protected factors are units, a
fully selected state `C4` has coefficient `1+w_1w_2` and cancels precisely
when `w_1w_2=-1`.  Even then, (2) supplies no bound on
`min_c q_c` for the extra matching.  Proving that some fourth matching has
paired depth at most one would exclude WP1 in this family; no such statement
is established here.

## Promotion audit receipt

The candidate owner file was audited line by line at SHA-256
`8B4BC53F3221B55DFDE5CE9706335812963388CCF472B8025252B222495A0AE0`.
No quantifier, disconnected-component, weight, or word-injectivity blocker was
found. In particular, the owner correctly distinguishes the all-weight
injection into nonzero unique-matching coefficients from the
`alpha beta=-1` bijection onto all nonzero coefficients.

The literature registry entry for arXiv:2606.04173v1 records the exact
Theorem 2.4 locator and componentwise correspondence. The registry validator
returned `ok: true` with no errors. The theorem's statement and definitions
were also checked directly in the primary HTML.

The independent reconstruction was replayed from a neutral working directory
outside the repository at script SHA-256
`F78C0879E7BA278DD8B6C5D30A16633CB3D9B3F22E64CD35371425C729241A39`.
It returned `N1_CUBIC_BRIDGE_RECONSTRUCTION_PASS`.

The separately derived [primary replay](../../claims/arbitrary-order/verify_protected_pair_gadget_cubic_bridge.py)
enumerates physical matching terms before grouping by word, while the audit
enumerates all words before building each scalar graph. Its final frozen
script has SHA-256
`D7EBD50CD7B7A0AA670290F2A9023AFB2775407AAF58AFB19BD43AC3AC732AC3`.
It checks the two-K4 allocation, a three-K4 nonbipartite component triangle,
and the arbitrary-nonzero-weight injection boundary. Neither program imports
the other or shared project scientific code. Finite replay independence does
not replace the written all-order proof or the imported graph theorem.

The published owner promotes the reviewed candidate's status and adds
portable evidence links. It also explicitly spells out the all-weight
bijection onto empty/adjacent-pair words already proved in the candidate.
These changes preserve the reviewed mathematical scope.
