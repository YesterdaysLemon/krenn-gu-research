# Complete pair gadgets: cubic matching review brief

The global Krenn--Gu conjecture remains **UNRESOLVED**. This checkpoint
excludes an entire protected construction family and gives an exact graph
form of its remaining weighted one-pair question.

Take k protected unit K4s. Pair all 6k protected colored edges, each with an
edge of a different color in another K4. Join the endpoints of each pair
by either bijection, with two arbitrary nonzero complex weights. Add no
other crossings. No component bipartition or uniform port allocation is
assumed. The existing PSFD high-girth construction lies in this family.

**Theorem:** every such array has a mixed physical word with exactly one
supported perfect matching, hence nonzero amplitude. It cannot be a full
GHZ source, at any order and for any permitted nonzero weights.

The proof replaces each vertex by its three color states. These partition
into disjoint four-cycles. Replacing each four-cycle's two bipartition
classes by auxiliary vertices gives a simple triangle-free cubic graph H
with a proper three-edge-coloring. Its perfect matchings biject with words
selecting only zero or two adjacent states in each gadget. Every such word
has one original matching. The three color-class matchings give exactly
the three pure words.

The imported Theorem 2.4 of Kothari, Lee, Lucchesi and da Silva,
[*Cubic graphs, S-minors and conformal minors*, arXiv:2606.04173v1](https://arxiv.org/html/2606.04173v1#S2.SS1),
says a connected matching-covered graph with exactly three perfect
matchings is a bi-subdivision of Theta or K4. Applied componentwise,
cubicity, simplicity and triangle-freeness exclude both possibilities.
An additional matching supplies the required mixed word.

**Exact remaining boundary:** if the two crossing weights in each gadget
multiply to -1, H's matchings biject with *all* nonzero source words.
The WP1 system in this family therefore asks whether every non-color-class
matching can avoid both (i) component-constant words and (ii) words with
min_c q_c<=1, where q_c counts complete minority M_c pairs. The matching
count theorem supplies no q bound. Forcing an extra matching in either
class would exclude WP1 here; this checkpoint does not do so. Arbitrary
protected arrays need not have this gadget decomposition, and no reduction
of arbitrary conjecture witnesses to the protected scaffold is supplied.

The written proof passed independent mathematical review. Two portable
exact reconstructions use different enumeration routes. Controls cover
two K4s, a three-K4 nonbipartite component graph, and the weight boundary:
160 unique-matching words remain when arbitrary weights increase the total
number of nonzero words to 281. These are checks of the correspondence,
not a finite proof of the all-order theorem. No Lean or human review claim.

For adversarial review, check the state partition, word-level injectivity,
componentwise application of the imported theorem, and the distinction
between a mixed matching and a low-paired-depth mixed matching.

- [Owning proof and two replay commands](../../claims/arbitrary-order/PROTECTED_PAIR_GADGET_CUBIC_MATCHING_EXCLUSION.md)
- [Independent audit](../audits/PROTECTED_PAIR_GADGET_CUBIC_REVIEW_2026-09-22.md)
- [Current frontier](../current-frontier.md), node PSCG
- [Earlier fixed-cutoff parent checkpoint](low-minority-parent-review-2026-09-22.md)
