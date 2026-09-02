# Adversarial review: all-diagonal weighted Bogdanov, degree-four exclusion

Date: 2026-09-01

Reviewed package:

- `claims/arbitrary-order/ALL_DIAGONAL_WEIGHTED_BOGDANOV_MAXIMUM_DEGREE_FOUR_EXCLUSION_THEOREM.md`
- `claims/arbitrary-order/verify_all_diagonal_weighted_bogdanov_maximum_degree_four_exclusion.py`
- `claims/arbitrary-order/audit_all_diagonal_weighted_bogdanov_maximum_degree_four_exclusion.py`

## Independence disclosure

Written by the same agent (Claude) that wrote the theorem and both scripts,
in the same session.  This is an adversarial self-review, not an independent
audit in the sense of `AGENTS.md` section 5.  A second reviewer has not
examined the package; that absence is recorded rather than papered over.

## Verdict

**PASS as a scoped exact theorem in the all-diagonal branch.**  Every
all-diagonal witness has `Delta(D) >= 5`.  It is not a proof of the
conjecture, does not touch bichromatic entries, and does not close the
all-diagonal branch.

## 1. Attacks on the setting

*Is (F) really exact?*  With diagonal blocks a matching monomial is nonzero
only if every edge joins equal colours, so the sum over matchings splits over
the colour classes into a product of principal hafnians, with odd classes
giving zero.  The primary checks all `3^6` words on random rational blocks;
the audit repeats this with complex floating point and einsum.

*Does (H2) with two parts cover `A = e`?*  Yes: `(e, V - e, empty)` is an
ordered partition into even parts not all in one class since `n >= 4`.

## 2. Attacks on the proof

*Step 3.*  The bound `deg_(E_c) <= 2` needs the three `E_c` disjoint **as
sets of pairs**, which is exactly what exclusivity gives (a pair active in
two colours would carry nonzero weight in both).  Checked.

*Step 4.*  The score argument uses that nonactive pairs have score zero by
definition, so Laplace at a vertex sums only over its active pairs.  Correct.

*Step 5.*  The claimed four distinct `D`-neighbours: the two cycle
neighbours are distinct pairs in `E_c`; the active partners in the other two
colours are pairs in `E_d` and `E_e`, disjoint from `E_c` and from each
other.  So all four pairs are distinct and `deg_D = 4` is saturated.  Then
`supp(Z^c) subset D` and exclusivity leave only the two cycle neighbours as
colour-`c` neighbours.  The conclusion "`U` is a union of components of
`supp(Z^c)`" and the factorization `f_c(V) = haf(Z^c[U]) haf(Z^c[V - U])`
are standard.  The audit exhibits odd components killing the total hafnian
on random instances.

*Step 7.*  A cycle vertex is on no cycle of another colour because its other
two `E`-degrees are one.  Non-cycle vertices meet at most one `H` edge.  So
`R` has maximum degree one.  Checked against the degree patterns
`(1,1,1)` and `(2,1,1)`.

*Step 9.*  The noncancellation lemma is the same matrix fact used by the
all-bridge degree-four exclusion; both scripts check it, the audit against
the explicit path/cycle factorization formula.

*Step 10.*  Bogdanov's theorem is used only for a simple cubic graph that is
the disjoint union of three perfect matchings.  Both scripts verify it
exhaustively for `n = 6, 8`; the general statement is imported through the
repository's existing citation.  The word induced by `F` is non-constant
because `F` uses at least two colours, and each nonempty class has a perfect
matching inside `supp(Z^c)`, so Step 9 makes every factor nonzero.

## 3. What the theorem does not say

It does not bound the degree of general witnesses.  It does not identify the
all-diagonal branch with the all-bridge branch; the proof route is the same in
outline but the even-cycle input is different (component factorization here,
normal-type bit flips there).  The degree-five case is genuinely open and the
document names the three places where the argument breaks.

## 4. Evidence

Both scripts share no code.  Runtimes are a few seconds each.  Outputs go to
the untracked `tmp/` directory.  The fast-verifier set in `check_hygiene.py`
was not extended.
