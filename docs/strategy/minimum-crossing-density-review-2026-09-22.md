# Minimum crossing density: model-review brief

The global Krenn--Gu conjecture remains **UNRESOLVED**. This checkpoint
proves an all-order density obstruction inside the protected unit-K4
scaffold, over complex weights.

**Result:** a hypothetical full GHZ source on k>=2 protected components
must have strictly more than 6k supported crossing scalar entries. Entries
with different color labels on the same physical edge are counted separately.
All crossings are hollow; protected internal entries have unit weights.

The proof has five steps:

1. Each singleton macro cancellation needs at least two entries of each
   ordered component/color/background type. Double counting gives m>=6k.
   At equality every such pair is a bijection between protected edges in
   two components, and its two actual weights multiply to -1.
2. The resulting literal graph F has vertices (component,color), degree
   two, and one neighbor of each other color. Macro targets force only
   three constant independent transversals. Each color-pair permutation
   must be one cycle. A triangle yields an explicit mixed transversal by
   coloring two arcs of one such cycle, so F has no triangles.
3. Two-exception macro words then force every reused resource to have both
   foreign-color neighbors in one physical component: a hidden overlap.
4. An unaligned hidden overlap has a unique one-pair matching. An aligned
   one has the unique mixed word `0000|1222|0000|...`, with coefficient
   `-x/z` and global paired-depth vector `(2,2k-1,2k-2)`. All exterior
   crossings are disabled by their literal colors. Both cases contradict
   the full source.
5. Every resource allocation is therefore split. This is exactly the
   complete protected-edge pairing already excluded by the published
   cubic matching theorem PSCG.

The intermediate normal form needs only WP2: the macro targets plus all
mixed coefficients of minimum paired depth at most two. The final cubic
theorem supplies a mixed word with no depth bound, so **this does not
exclude WP2 or WP1 alone**. In particular, the hidden witness has depth two,
outside WP1. No degeneration of a denser source to equality is proved.

The imported premise is PSCG's use of Kothari--Lee--Lucchesi--da Silva,
Theorem 2.4 on graphs with exactly three perfect matchings; its provenance
and hypotheses are already recorded with PSCG. No new external theorem is
introduced in this checkpoint.

Independent separate-agent review checked the written all-order chain.
Portable exact replays cover all 496 two-entry singleton supports on three
K4s, 11,618 explicit triangle witnesses, and 768 complete arrays testing
both hidden orientations with nontrivial exterior gadgets. Those finite
checks corroborate the proof; they do not establish its unbounded scope.
No Lean or independent human-referee claim is made.

For adversarial review, concentrate on the two incidence counts, the
directed arc construction, whole-array isolation of the hidden word,
and exact transfer to the complete-pair theorem. A flaw in any of these
would break the density result. Denser protected sources and the reduction
from arbitrary conjecture witnesses to this scaffold remain open.

- [Owning proof](../../claims/arbitrary-order/PROTECTED_MINIMUM_CROSSING_DENSITY_EXCLUSION.md)
- [Independent review](../audits/PROTECTED_MINIMUM_CROSSING_DENSITY_REVIEW_2026-09-22.md)
- [Cubic matching dependency](../../claims/arbitrary-order/PROTECTED_PAIR_GADGET_CUBIC_MATCHING_EXCLUSION.md)
- [Current frontier](../current-frontier.md), node PSMD
