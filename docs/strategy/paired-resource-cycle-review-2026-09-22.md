# Paired-resource cycle theorem: model-review brief

The global Krenn--Gu conjecture remains **UNRESOLVED**. This checkpoint
proves a broader construction-family exclusion and supplies an elementary
alternative to an external theorem used in two earlier exclusions.

Take any three protected perfect matchings on the same finite physical
vertex set, with arbitrary nonzero complex weights. Partition their
colored edges into pairs of different colors. Add crossings only within
each resulting two-by-two state block, forbid physical selfloops, and
require every crossing block to contain a perfect matching. Blocks may
have two, three or four crossings; protected resources may overlap
physically. No K4 scaffold is needed.

**Theorem:** some mixed physical word has exactly one supported perfect
matching, so its coefficient cannot vanish.

Proof: fix a base color a. Draw u->v whenever the a-mate of u has a
supported crossing to a foreign-colored state at v. Positive outdegree
gives a directed cycle, possibly a one-vertex loop. Change the pure a-word
at each cycle vertex to its incoming arc's foreign color. A block with
r cycle vertices on its a-resource selects exactly 2-r base states and
r foreign states. The partition of colored resources prevents arrivals
from another block. For r=0,1,2 the selected states have exactly one
edge, respectively protected/crossing/protected. Other blocks are empty.
Thus the whole word has a unique matching with nonzero product weight.
A proper cycle leaves color a outside. A spanning cycle gives half of
each foreign color, because there are |V|/4 blocks of each color-pair type.

This covers the earlier two-crossing complete-pair family and extends it
to denser blocks and overlapping resources. It removes the need for the
imported three-perfect-matchings classification in the sparse-crossing
and strict minimum-density full-source exclusions. Their earlier cubic
correspondence and imported proof remain valid.

The missing parent step is **full-source supply of a suitable resource
structure**. A state crossing-degree bound of two alone does not provide
the paired blocks. Macro equations can involve indispensable four-crossing
terms and entries invisible to every macro word. No arbitrary-witness
reduction, general degree-two exclusion, or WP1/WP2 exclusion is claimed.

For adversarial review, check the converse excluding foreign arrivals from
other blocks, physical overlaps and auxiliary loops, the spanning-cycle
color count, and the exact consumer hypotheses. Two separate agents reviewed
the proof. Exact portable replays check 4,872 four-vertex configurations and
15 nonbipartite twelve-vertex dense-block cases; these are corroboration,
not the all-order proof. No Lean or human-referee claim is made.

- [Full proof](../../claims/arbitrary-order/PAIRED_RESOURCE_DIRECTED_CYCLE_EXCLUSION.md)
- [Independent review](../audits/PAIRED_RESOURCE_CYCLE_REVIEW_2026-09-22.md)
- [Current frontier](../current-frontier.md), node PRDC
