# Degree-two source parent: model-review brief

The global Krenn--Gu conjecture remains **UNRESOLVED**. This checkpoint
attacks full-source exclusion on k>=2 protected K4 components with hollow
complex crossings and at most two crossings per vertex/color state. It
does not assume arbitrary witnesses have this form. Color regularity below
means exactly one crossing to each foreign color, a stronger hypothesis.

**Main reduction (ASSR).** In the additional all-split class, every
protected resource maps bijectively to a whole foreign resource. Full-source
rows force all binary physical transition permutations to be Hamiltonian,
the resource graph to be one cycle C_(6k), and every normalized crossing-pair
product to equal -1. A switched-cycle coefficient is exactly its nonzero
baseline weight times the factors (1+sigma) at fully occupied transition
squares. One-resource switches force every sigma=-1.

Hamilton parity makes the resource cycle's endpoint twist odd. A single
diagonal state gauge therefore removes all complex weight parameters:
protected rungs become +1 and crossing pairs (+1,-1). It preserves every
zero coefficient and the three pure coefficients. Every physical word
leaves at least 2k resources empty, cutting the ladder into paths. A word
has nonzero coefficient exactly when each path has:

1. an even number of singly occupied resources;
2. correct forced endpoint transport between consecutive singleton pairs;
3. no remaining full run of length 2 modulo 3.

The last rule follows from Z_0=Z_1=1 and Z_m=Z_(m-1)-Z_(m-2).
**The missing theorem is existence of a mixed physical transversal satisfying
these conditions.** The physical K4 incidence cannot be rearranged freely.

**C8 source transport (PSDT).** Retaining the complete two/four-crossing
singleton expansion, a C8 cancellation forces the opposite foreground
layer to split into two pair gadgets of product -1. A q1 word forces at
least one repair resource to leave a one-component C8 target. Escape does
not automatically iterate. An exact two-component array satisfies all 486
reciprocal one-component/background specifications (477 distinct words),
yet fails 195 full-source rows. Thus those local rows alone cannot close the
parent. A separate three-component control passes all81 local rows with
one cancelling pair and two orphan targets in each foreground layer.
Thus complete split/C8 classification itself needs a global supplier.
Non-color-regular distributions also remain outside these reductions.

**Conditional consumer (RSTC).** Resource-simple blocks containing at most
one protected resource per color are excluded when opposite-endpoint exits
have adjacent targets. Directed-cycle balance then gives a mixed unique
matching. Endpoint supply alone cannot furnish even one such good cycle:
an exact hollow three-K4 control has every base-color cycle bad, although
317 other mixed words have unique matchings. This is a route obstruction,
not a counterexample to the conjecture.

Independent agents checked the written implications. Exact companions
corroborate the controls, 94,208 switched-cycle words, all 6,561 words of a
nontrivial gauge example, and 1,007,769 path cases. Finite checks do not
supply the all-order quantifiers. No external theorem, Lean verification,
or independent human refereeing is claimed.

Review priorities: missing matching sectors in the switched coefficient;
physical overlaps; global gauge closure and pure normalization; forced
singleton pairing; and, above all, the remaining mixed-transversal
existence problem. The three routes are not an exhaustive degree-two cover.

- [All-split reduction and exact path criterion](../../claims/arbitrary-order/COLOR_REGULAR_ALL_SPLIT_SOURCE_REDUCTION.md)
- [Source transport and q1 escape](../../claims/arbitrary-order/DEGREE_TWO_SOURCE_TRANSPORT_AND_LOCAL_BOUNDARY.md)
- [Transition-closed exclusion and route controls](../../claims/arbitrary-order/RESOURCE_SIMPLE_TRANSITION_CLOSED_EXCLUSION.md)
- [All-split audit](../audits/ALL_SPLIT_SOURCE_REDUCTION_REVIEW_2026-09-22.md)
- [Source audit](../audits/DEGREE_TWO_SOURCE_TRANSPORT_REVIEW_2026-09-22.md)
- [Block audit](../audits/RESOURCE_SIMPLE_TRANSITION_REVIEW_2026-09-22.md)
- [Current frontier](../current-frontier.md), nodes ASSR, PSDT and RSTC
