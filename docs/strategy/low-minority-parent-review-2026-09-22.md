# Fixed paired-minority parent: review brief

The global Krenn--Gu conjecture is **UNRESOLVED**. This checkpoint closes a
family of proposed support-only proof routes, not the weighted conjecture.

For k protected unit K4s, let q_c count protected color-c pairs whose two
endpoint word colors are both not c. Define P_r as (i) every mixed
component-constant word has a crossing matching as well as its protected
matching, and (ii) no mixed word with min_c q_c<=r has exactly one matching.
A full weighted protected source necessarily supplies every P_r.

**New theorem:** for every fixed r>=1, a finite support satisfying P_r
exists, even with all three whole port graphs acyclic. Therefore no
fixed paired-minority support cutoff can exclude the full source family.

The proof has two parts. In a common-star matching of depth q, at most 3q
components are active. A non-macro matching must project to a component
cycle, so girth>3r hides all non-macro words of depth<=r. Separately, eight
random perfect-matching layers for each of six unequal color labels give
macro rigidity with probability tending to one. A direct short-cycle
factorial-moment and Bonferroni argument gives positive probability of any
fixed girth. Their intersection supplies the finite support. This is an
analytic existence proof, not sampling; graph size can depend on r.

P1 also has an explicit compact witness: 18 K4s on K_(6,12), with twelve
listed permutation columns. A 729-case exact left-color cover proves all
mixed macro assignments have an enabled gadget. A complete local-state
proof excludes every mixed q<=1 word. Both P1 exclusion and DAG-P1 are
therefore refuted concretely.

**Why this does not refute Krenn--Gu:** the accepted PSCS three-source
identity already prevents every triangle-free common-star support from
carrying weights satisfying all macro equations. Counting available terms
loses their shared-weight constraints. Conversely, a separate 72-entry
rational array on three K4s satisfies all macro targets with whole DAGs,
but its one-pair word `1210|1111|1221` has coefficient -1. Each side of this
distinction has an exact control.

The surviving parent **WP1** asks whether one arbitrary hollow protected
array can satisfy both all macro targets and all mixed min-q<=1 zero
equations. Neither control satisfies this conjunction. On common-star
arrays this is precisely the existing CSQ4 parent, so that specialization
is not new progress. Unrestricted all-word UPM, SFULL, legal component
elimination, and arbitrary-witness-to-scaffold supply remain open.

For adversarial review, check the local-state exhaustion, the 3q physical
resource count, the canonical short-cycle overlap argument, and the exact
quantifier order `for each fixed r, there exists a finite support`.
A useful next proof must retain actual coefficients on the same filling,
or use an all-word support condition with a proved order-dependent cover.

- [Owning theorem, explicit columns, full proof, and five replay commands](../../claims/arbitrary-order/PROTECTED_LOW_MINORITY_SUPPORT_COUNTERMODELS.md)
- [Independent mathematical and implementation reviews](../audits/PROTECTED_LOW_MINORITY_PARENT_REVIEW_2026-09-22.md)
- [Current proof topology](../current-frontier.md), nodes PSQ1 and PSPR
- [Earlier source identities and elimination checkpoint](full-source-parent-review-2026-09-22.md)

No Lean formalization or independent human review is claimed.
