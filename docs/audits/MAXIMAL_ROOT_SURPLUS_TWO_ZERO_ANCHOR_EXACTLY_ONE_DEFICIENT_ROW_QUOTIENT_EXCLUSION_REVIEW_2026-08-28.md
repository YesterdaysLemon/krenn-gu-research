# Hostile review: exactly-one-deficient row-quotient exclusion

## Review target and verdict

Target reviewed:

`claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_EXACTLY_ONE_DEFICIENT_ROW_QUOTIENT_EXCLUSION_THEOREM.md`

**Verdict: PASS for the written mathematical argument, within its stated
scope.**  The theorem matches the repaired same-source proof: zero anchor,
root order three, all six auxiliary labels torus-rigid, and exactly one
deficient joint probe map.  The argument excludes the whole (P=0,1,2)
cover after first excluding (U=\varnothing).  The earlier (P=1) concern
(a row quotient at (n) can leave a one-dimensional quotient in which
colours cancel) is correctly resolved: Section 6 quotients only the pure
axis slot and uses the untouched (n)-coordinate basis, while the scalar
deck/outer-companion rank argument is available directly.

This is a mathematical review only.  The verifier and independent-audit
scripts named in Section 10 were not present in the reviewed working tree,
so executable replay is not claimed here.

## Assumptions and notation checked

The proof consistently uses the complete `GLS61` partial-uncontraction
identity over the ambient polynomial ring, with fraction-field quotients
introduced only after the polynomial identity is established.  The five
labels other than the deficient label (n) are partitioned into injective
pure-probe axes (P) and injective nonaxis labels (U).  The sets

```text
A_n={a : e_(n,a)^*|_(ker J_n) != 0},
E_a={u in U : (k_u)_a is identically zero}
```

are typed correctly.  Pairwise disjointness of the (E_a) uses exactly the
`GLS61` one-zero-coordinate lemma for injective nonaxis labels; no converse
or per-colour upper bound is assumed.

## Earlier (P=1) issue and its repair

The rejected argument was to quotient the deficient (n)-slot and then infer
that a multi-colour diagonal target survives.  A rank-two quotient can allow
colour cancellation, so that inference was not valid.

The current theorem does not make that inference.  For (S=\{n,p\}) in
Section 6 it quotients only the active line at (p).  The sole retained
source term is the (n,p) companion, and it is killed at (p).  The
unquotiented (n)-slot has independent coordinate covectors, so any
surviving colour is separated before any possible one-slot quotient
cancellation.  Equivalently, before quotienting, the companion has the
form

```text
h_(np) (b_n tensor a_p)
```

with scalar (h_(np)); its rank is at most one, whereas two surviving
diagonal colours have rank two.  A single surviving colour would force the
full variable row (a_p) onto a coordinate line, also impossible.  Section
6's conclusion that all three (E)-sets are nonempty is therefore sound.

## Empty-(U) boundary

Section 2 correctly handles (U=\varnothing) separately.  Taking
(S=Bhat) leaves every pair source term meeting a pure-axis label, so the
five active-line quotients kill the source.  The deficient (n)-slot is
untouched and separates the three nonzero target colours.  This does not
require (k_n\neq0), since (n) is open.  Hence (U\neq\varnothing) is
validly established before Lemmas 2--3.

## Supported-colour floor

Lemma 2 is correct.  For (a\in A_n) and (|E_a|\le1), choose (u) so
that (E_a\subseteq\{u\}) and take (S=P\cup\{n,u\}).  Every retained
pair either meets (n) or (P); the former is killed by the row-space
quotient and the latter by an active-line quotient.  The (a)-target has no
contracted (a)-zero factor, survives at (n), at every pure slot, and at
the open (u)-slot.  Evaluation at the (u,a) coordinate isolates it from
all other colours.  This remains valid when (k_n\equiv0), because (n) is
open and no (k_n) factor occurs.

## The “|E|=2” step and deck typing

Lemma 3 is also sound.  If (E_a=\{u,v\}), take
(S=P\cup\{n,u,v\}).  All retained companions are killed except
(g_{uv}): pairs meeting (n) die in the (n)-row quotient and pairs
meeting (P) die at a pure active line.  The complementary factor for
(g_{uv}) has open slots only in (n\cup P), with all remaining (U)-slots
contracted; after quotienting it is the single tensor

```text
Hbar_(uv) in Q_n tensor tensor_(p in P) Q_p.
```

It is not assumed nonzero a priori.  The surviving colour-(a) target is
nonzero, so the equality itself forces both (g_{uv}) and (Hbar_{uv}) to
be nonzero.  All other target colours are killed either by the (n)-row
quotient or by an (E_b\) member outside (S), using Lemma 2 and
disjointness.  Applying a functional nonzero on (Hbar_{uv}) forces
(g_{uv}) to be a scalar multiple of (e_{u,a}^*\otimes e_{v,a}^*).
The `GLS61` same-colour orientation lemma then gives the contradiction.
There is no hidden cancellation between decks because this open set has only
one surviving source pair after the stated quotients.

Consequently (|E_a|\ge3) for every (a\in A_n), exactly as claimed.

## Rank classification

Because the (E_a) are disjoint subsets of the five injective labels,
(|A_n|\le1).  Deficiency makes (K_n\neq0), hence (A_n\neq\varnothing),
so (A_n=\{c\}).  Thus (K_n=Ke_c), (operatorname{rank}J_n=2), and
(\operatorname{row}J_n=\operatorname{span}(e_d^*,e_e^*)).  The exclusions of
rank zero (not rigid), rigid rank one (coordinate-plane kernel), and rigid
rank two with support two are correctly stated.  Since (|E_c|\ge3),
(|U|\ge3), giving (P\le2).

## (P=0)

The Section 5 closure is valid.  With (S=\{n\}), there is no retained
source pair and the independent (n)-coordinate basis forces every (E_a)
to be nonempty.  The size count is therefore (3,1,1).  If (E_d=\{u\}),
then (S=\{n,u\}) leaves only the (d)-target, and the four-label
complementary deck is a scalar.  Its nonzero equality forces (g_{nu}) to
be pure ((d,d)).

For an (X)-oriented (u), projecting the (u)-slot off (d) gives

```text
p_n tensor pi_d(q_u)=0.
```

The opposite projection is nonzero because (u) is injective and nonaxis,
so (p_n=0), hence (X_n=0).  From (K_n=Ke_c) and rank two,
(\operatorname{row}Y_n=\operatorname{span}(e_d^*,e_e^*)), while the
remaining pure companion (q_n\otimes p_u) forces that row space into
(Ke_d^*), a contradiction.  The (Y)-orientation is symmetric.

The scalar deck cannot be zero: the target coefficient is a nonzero
polynomial, so the tensor equality forces the deck and companion nonzero.
The argument also covers (k_n\equiv0), since (n) is open and the proof
uses row geometry rather than a cross-product factor.  Zero-shore cases at
(u) would make (u) a pure-probe axis, contrary to (u\in U), so no omitted
boundary remains.

## (P=1)

With (|U|=4), the Section 6 equation (S=\{n,p\}) has one scalar deck
and one outer companion.  Since (|E_c|\ge3), colour (c) is killed; if
either of the other (E)-sets were empty, the corresponding target survives
and the pure-axis quotient plus untouched (n)-basis gives a contradiction.
Thus all three (E)-sets are nonempty, but their disjoint sizes would total
at least (3+1+1>4).  Multi-colour cancellation is unavailable because
the (n)-coordinate basis separates the colours.

## (P=2)

With (|U|=3), the floor gives (E_c=U), and disjointness gives
(E_d=E_e=\varnothing).  In (S=\{n,p,q\}), every source pair meets
(p) or (q) and is killed by the two active-line quotients.  Colour (c)
is killed by the three contracted (U)-cross products; the (d,e) target
terms remain nonzero and are separated by the untouched (n)-coordinate.
Their pure-axis factors survive the quotients.  Hence the target is nonzero
while the source is zero.  This also handles (k_n\equiv0), because (n)
is open.

## Same-source scope and status walls

Every deck in the proof is a contraction of the original physical (H)-tensor
from the same graph.  The proof never substitutes independently selected
local decks, divides by a deck, divides by a cross-product coordinate, or
claims a response/selector/synchronization consequence.  Fraction-field
extension is used only for linear quotients and tensor functionals, with the
polynomial-domain arguments made beforehand.

The theorem therefore supports exactly its stated source-branch conclusion:
the all-six-rigid, zero-anchor, root-order-three exactly-one-deficient branch
is excluded, yielding a deficient-map floor of two.  It does not close the
two-or-more-deficient branches, unique-nonrigid branch, nonzero-anchor or
silent-source branches, higher root orders, response/selector/synchronization
and activity gates, or the global conjecture.

## Independent replay evidence

The primary SymPy verifier and the independent standard-library audit were
rerun from the theorem worktree.  Both exited with code 0 and reported PASS.

Primary command:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py
```

The primary replay reported:

```text
proof_case_total: 2730
supported_E_floor_lt_2: 2190
supported_E_exactly_2_obstruction: 420
P0_ordinary_one_open_failures: 86
P0_singleton_nonsupport_pair_contradiction: 20
P1_active_line_contradiction: 13
P2_active_line_contradiction: 1
survivors: 0
raw_profiles: 18750
raw_support_size_one: 9375
raw_support_size_two: 9375
PASS
```

This includes the open-set/source-survival ledger, the supported
\(|E_a|<2\) floor, the \(|E_a|=2\) pure-companion obstruction, all pure-axis
counts, the rank-two orientation cases, and the raw support-one/support-two
census.  The primary verifier uses SymPy for the displayed exact algebra;
its finite replay is evidence for those ledgers, not a replacement for the
written same-source tensor proof.

Independent command:

```powershell
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py
```

The no-project-import standard-library audit independently reported:

```text
canonical_profile_total: 2730
labelled_colour_copy_total: 8190
row_quotient_floor: 2190
same_colour_pair: 420
p0_missing_other_colour: 86
p0_rank2_companion: 20
p1_all_colour_diagonal: 13
p2_two_colour_diagonal: 1
rank_two_pure_companion_survivors: 0
zero_survivors: 0
PASS
```

Its separate profile split covered support sizes one and two for
\(P=0,1,2,3,4,5\), including \(U=\varnothing\), and its active-line,
two-slot-diagonal, row-quotient, orientation, and rank-two row-space
censuses all completed without survivors.  The audit completed in under a
second and imports no project code or symbolic algebra.

The static checks also passed:

```powershell
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py
```

The replay evidence strengthens the review to final **PASS** for the
theorem's stated scope.  It does not alter the scope walls: the proof still
does not close two-or-more-deficient branches, the unique-nonrigid branch,
nonzero anchors, higher root orders, response/selector/synchronization or
activity gates, or the global conjecture.
