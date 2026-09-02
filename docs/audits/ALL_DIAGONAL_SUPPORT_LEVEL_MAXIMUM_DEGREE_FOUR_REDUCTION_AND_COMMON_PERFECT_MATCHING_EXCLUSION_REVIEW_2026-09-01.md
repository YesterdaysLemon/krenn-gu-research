# Adversarial review: AP-prime degree-four reduction and common-perfect-matching exclusion

Date: 2026-09-01

Reviewed package:

- `claims/arbitrary-order/ALL_DIAGONAL_SUPPORT_LEVEL_MAXIMUM_DEGREE_FOUR_REDUCTION_AND_COMMON_PERFECT_MATCHING_EXCLUSION_THEOREM.md`
- `claims/arbitrary-order/verify_all_diagonal_support_level_maximum_degree_four_reduction_and_common_perfect_matching_exclusion.py`
- `claims/arbitrary-order/audit_all_diagonal_support_level_maximum_degree_four_reduction_and_common_perfect_matching_exclusion.py`

## Independence disclosure

Two fresh research agents independently derived and cross-attacked the
common-perfect-matching argument during the same ecology.  One approached it
through graph components and capacitated Hall; the other through disjoint
block families and a network/TU formulation.  The integration review was
performed by the coordinating agent.  This is meaningful same-session
independent-agent review, but not an external audit by an unrelated author.

The primary and audit scripts differ in representation: the primary
enumerates graphs and counts induced perfect matchings, while the audit
enumerates abstract block families and uses an independently implemented
max-flow selector.  Neither script is the all-order proof.

## Verdict

**PASS as an exact arbitrary-order reduction and obstruction.**  Do not
promote it to AP' maximum-degree-four unsatisfiability.  The theorem document
states the remaining orientation/blocker implication, and the global status
remains **UNRESOLVED**.

## 1. Attack on the degree-four reduction

- Top-level (L) really does make every \(E_c\) spanning: it is applied at
  every vertex of \(V\), not merely once per colour.
- Active exclusivity uses only a two-part H2 partition.  If \(uv\in E_c\)
  and \(uv\in G_d\), the complement belongs to \(\mathcal S_c\), the pair
  belongs to \(\mathcal S_d\), and the third shore is empty.
- The three active incidences at a vertex are distinct.  With
  \(\Delta(D)\le4\), the non-active remainder therefore has degree at most
  one, so it is a partial matching.
- An edge of \(G_c\) active in another colour is excluded, proving
  \(G_c\subseteq E_c\cup H\).  The degree-two conclusion follows locally.
- Matchability of \(V\) is supplied by (S), so odd path or cycle components
  cannot occur.
- In an even path, deletion of an edge's endpoints leaves a matchable
  remainder only for an edge of the unique path matching.  This validates
  the fixed/private path assertion.

No weight value, noncancellation claim, or converse bridge is used.

## 2. Attack on the common-matching proof

Contracting a shared perfect matching \(R\) is legitimate because every
maximum-degree-two component containing \(R\) is an alternating path or
cycle.  Alternative perfect matchings differ from \(R\) only on whole cycle
components.

The Hall calculation must charge only a \(C\)-block wholly contained in the
union \(U\) of selected \(D\)-blocks.  Such a block loses one unit of
capacity; a merely intersecting block need not.  The final proof uses this
correct accounting:

\[
|U|\ge2|\mathcal J|,\qquad q\le |U|/2,\qquad
|U|-q\ge|\mathcal J|.
\]

The empty-cycle-family cases preserve two nonempty shores: a singleton works
when the required family is empty, and one representative from each
nonempty required block necessarily omits another atom from that block.

Avoiding every \(G_c\)-cycle block makes the selected shore uniquely
matchable; hitting every \(G_d\)-cycle block makes the complementary shore
uniquely matchable.  Forcing (F) then supplies the exact two H2 memberships.
This proves a contradiction without assuming the shared matching is unique
in either full support graph.

## 3. Attacks on tempting strengthenings

- The eight-vertex control proves that arbitrary support-perfect-matching
  choices need not be pairwise edge-disjoint.
- The ten-vertex control proves that a pairwise argument can miss valid
  three-colour cycle-avoiding matchings.
- The twelve-vertex control refutes cycle avoidance for an arbitrary fixed
  orientation, but not existential orientation choice and not AP' itself.
- Therefore neither the common-matching lemma nor Bogdanov's theorem alone
  closes the reduced problem.

The exact surviving candidate is the two-part-unique-shores versus
existential-orientation-and-cycle-avoiding-matching dichotomy in the theorem.

## 4. Proof-topology correction

The previous WB2 text said WB1 proved AP' unsatisfiable whenever
\(\Delta(D)\le4\).  That inference is unsupported.  WB1 proves the exclusion
for actual weighted witnesses and uses numerical Laplace scores plus a
weight-level noncancellation lemma.  AP' discards those data, and its bridge
from witnesses is one-way.

The corrected topology is:

- WB1: actual all-diagonal witnesses of maximum degree at most four are
  excluded;
- WB2: AP' is excluded at \(n=6,8\) for every degree;
- WB3 (this package): AP' at maximum degree four reduces to even path/cycle
  supports, and the common-perfect-matching subcase is excluded;
- the remaining AP' degree-four dichotomy and full all-order AP' are open.

## 5. Computational evidence

The primary checked all 2,601 ordered graph pairs at \(n=6\), and replayed
the exact sharp controls.  The audit checked all ordered abstract block-family
pairs through six atoms: 25, 225, 2,704, and 41,209 pairs for three through
six atoms.  Both completed successfully.

These checks catch representation, shore-complement, and empty-family
mistakes.  They do not replace the arbitrary-order Hall proof.
