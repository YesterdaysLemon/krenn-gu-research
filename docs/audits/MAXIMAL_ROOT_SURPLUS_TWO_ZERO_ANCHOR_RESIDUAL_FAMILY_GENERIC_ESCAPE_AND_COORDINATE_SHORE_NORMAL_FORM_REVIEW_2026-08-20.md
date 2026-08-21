# Hostile review: zero-anchor residual-family generic escape and shore normal forms

## Decision

**Accept as scoped theorem `GLS27`.**  The residual-family argument is a
legitimate source-choice reduction: either a nonempty principal open of
contractions escapes the GLS26 coordinate-shore cover, or the cover holds at
the residual function-field point and has one of the three stated generic
normal forms.  The GLD11 graph exactly realizes the `(2,1)` form off the
witness locus and proves that complete mixed equations remain load-bearing.

This review rejects any claim that GLS27 supplies a legal target row, excludes
the generic cover on a witness, handles the later detector gates, or closes
the strategic node.  The global conjecture remains **UNRESOLVED**.

## 1. Hypothesis and field audit

The package retains one fixed physical `GLS4` pair and probe pair with

```text
h!=0, p!=0, Pi_Q!=0, omega=0.
```

Here `h=H_Q(z_0,z_1)` and `p=p_(A,Q)(z_0,z_1)` are nonzero Laurent
polynomials before specialization; `Pi_Q` is the fixed nonzero complementary-
permanent tensor.  Passing to the
fraction field does not turn a pointwise nonzero value into a universal
identity.  It records the generic residual contraction of this same graph.

The field is infinite because it has characteristic zero.  Therefore a
finite product of nonzero Laurent polynomials has a fully supported
`K`-point where it is nonzero.  This justifies selecting one contraction in a
principal open.  It does not justify a claim about every exceptional fibre,
and the theorem makes no such claim.

## 2. Rank-drop audit

At each shore the generic `3 x 2` incidence matrix has rank one or two.
Nonzero `p` excludes rank zero.  The proof chooses:

- a nonzero generic-rank minor to keep the rank fixed; and
- when a coordinate line is absent, a nonzero augmented minor to preserve
  that absence after specialization.

This is the correct all-rank test.  A single `3 x 3` determinant would be
insufficient on rank-one shores; GLS27 does not make that substitution.

On the cover branch, membership is solved over the function field and all
basis minors and rational denominators are cleared into one nonzero Laurent
factor.  Thus the same colour-to-shore assignment holds on the resulting
open.  Assignment changes and rank drops outside it remain present in the
residual family, but cannot prevent choosing the declared source point.

## 3. Exhaustiveness audit

The function-field coordinate cover either holds or fails.  If it fails, one
of the three colours is absent from both shore spans and persists on a
principal open; GLS26 then gives its pointwise essential-pair conclusion.  If
it holds, choose one accepting shore per colour.  The two branches are
logical complements and no generic fibre is omitted.

The corollary is properly one-way: if every point of `D(hp)` is covered, then
the generic point is covered.  GLS27 does not claim that a generic cover must
extend over every exceptional point.

## 4. Normal-form audit

GLS26 proves that a covered generic rank pair satisfies `d_0+d_1>=3`, while
each rank is at most two.  Therefore only

```text
(1,2), (2,1), (2,2)
```

remain.

For `(1,2)`, the one-dimensional shore must be one coordinate line and the
two-dimensional shore the complementary coordinate plane.  Substitution in
the physical exchange tensor

```text
q=xi_0^0 tensor xi_1^1+xi_0^1 tensor xi_1^0
```

gives a nonzero rank-one cross-axis tensor with zero diagonal.  Nonzero `p`
is used only to exclude `q=0`.

For `(2,2)`, at least one shore contains two coordinate axes and is therefore
a coordinate plane.  The other contains its missing axis and can be written
as that line plus one vector in the complementary plane.  Both residual
covector pairs are bases, and the exchange coefficient matrix is invertible,
so `q` has rank exactly two and its two shore spaces are exactly its left and
right spans.  No coefficient of `q` is normalized.

If both shores are coordinate planes, equal missing colours would leave that
colour uncovered, hence the missing colours are distinct.  This confirms the
last subcase without a hidden genericity assumption.

## 5. Sharp-control audit

In the GLD11 table choose `A={r_0,r_2}` and `Q={q_0,q_1}`.  Direct reading
gives

```text
X_0=span(e_0^*,e_2^*),  X_1=K e_1^*,
q=z_(q_0,0)z_(q_1,1)e_0^* tensor e_1^*,
p=z_(q_0,0)z_(q_1,1),   h=z_(q_0,0)z_(q_1,0).
```

All displayed residual coordinates are torus units.  The injection

```text
r_0-u_0, r_1-u_3, r_2-u_1, r_3-u_2
```

has colour one and proves `Pi_Q!=0`.  The inherited GLD11 theorem supplies
maximum-root maximality, rank-three blockers, pure normalization, the zero
Hamming-one shell, local concision, response nonvanishing, swallowed pure
classes, and the mixed coefficient `1200100020=1`.

The control is not a counterexample because that mixed coefficient violates
the GHZ target.  It proves only that the earlier source/local/pure equations
do not eliminate the generic cover.

## 6. Verification independence

The primary verifier uses SymPy rational-function matrices, separately checks
an escape fixture, the three shore normal forms, the exact GLD11 source
reading, a nonzero `Pi_Q` injection, and the unique mixed coefficient among
the full matching expansion.

The no-import audit uses standard-library `Fraction`, independent Gaussian
elimination, different numeric shore fixtures, and a separate direct reading
of the GLD11 incidence table.  It imports neither the primary verifier nor a
repository mathematics helper.  The scripts audit the finite linear-algebra
and control mechanisms; the arbitrary Laurent-open statement is the written
minor proof.

## 7. Exact scope ledger

```text
generic escape / fixed-cover dichotomy:               ACCEPTED;
rank-one and rank-two shore fibres:                   ACCEPTED;
C12/C21/C22 normal forms:                             ACCEPTED;
GLD11 maximum-root sharpness:                         ACCEPTED;

essential raw pair legal survival:                   OPEN;
complete mixed exclusion of C12/C21/C22:             OPEN;
response, synchronization, activity, downstream:     OPEN;
maximum-root supply/attachment node:                 OPEN;
global Krenn-Gu conjecture:                          UNRESOLVED.
```

Before merge, replay the GLS26 primary/audit and the GLD11 primary/audit,
then run the complete candidate-tree validation contract and exact-head
hosted hygiene.
