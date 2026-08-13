# Self-review: `m=3` common-three-space joint-rank-eight exclusion

## Claim audited

A normalized target-consistent physical `m=3` common shore with singleton
span dimension three cannot have joint cross rank eight.

## Scope checks

- The theorem is characteristic zero; Lemma 1 explicitly uses
  characteristic different from two.
- Rank eight means the physical joint root--nonroot cross-colour map, not the
  full sensor matrix.
- The result is conditional on the common-three-space S2Q stratum and does
  not treat the other pole strata.
- Rank at most seven and all higher orders remain open.
- Global status remains **UNRESOLVED**.

## Adversarial checks

1. **Was full-rank invertibility reused silently?**  No.  Rank eight supplies
   a hyperplane `image H`; the elementary loss-at-most-one inequality is
   substituted explicitly.  The torus-monomial and off-diagonal
   globalization arguments from S2U do not require invertibility.
2. **Why is the exceptional root row full-support?**  Once only `B_23`
   survives, the three physical singleton columns are the three root-1 cross
   vectors tensored with the same root line.  Full sensor rank makes them
   generically independent, so every source projection of the row space is
   nonzero.
3. **Can the regular off-diagonal grid span five dimensions through internal
   three-dimensional source blocks?**  The proof of Lemma 2 retains the full
   source dimensions.  Pure zero-divisor spaces have dimension three, but
   only the displayed `q` row and at most the relevant `p` rows occupy each;
   mixed zero-divisor spaces are one line.  The `2+1` pure pattern is the
   sharp four-dimensional case.
4. **Could a nonzero `C` still give a rank-one exceptional restriction?**
   No.  On the two independent vectors of `R intersect Z`, tensoring by
   nonzero `C` is injective and already has rank two.
5. **Are the two diagonal target covectors truly independent after changing
   source bases?**  Yes.  Source changes do not change the root-output basis.
   The row block has rank three, so the root coordinate rows form a basis of
   `R`; the two surviving target colours select two different dual basis
   covectors.
6. **Does rank seven follow?**  No.  Both inequalities used here become
   equalities at seven: a codimension-two image can hide two root blocks, and
   the zero-grid span bound four can combine with `dim R=3`.  These are
   recorded as live boundaries.

## Failed routes retained

A finite `F_2` probe initially looked as if local concision alone excluded
the sparse equation.  Normalizing a singleton transversal by an arbitrary
root-row basis change does not preserve the two GHZ output covectors.  The
invariant rerun carried both independent covectors, but no finite-field result
was promoted across characteristic.  The proof above instead uses the
covectors basis-free in (26)--(27).

Numerical characteristic-zero least squares approached the sparse equation
only while coefficients diverged and two singular values collapsed.  This
is consistent with a projective boundary and is not used as evidence for the
theorem.

## Evidence independence

The primary uses SymPy normal forms and exact symbolic ranks.  The audit
imports neither SymPy nor the primary script; it implements separate
`Fraction` elimination and independent sharp controls.  Both scripts replay
the case boundaries.  The arbitrary-field proof is the written
zero-divisor classification and derivative argument.
