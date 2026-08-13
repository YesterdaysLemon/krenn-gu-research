# Hostile review of the balanced root-quadric basepoint bridge

## Verdict and provenance

**PASS, as a scoped proof-DAG corollary and fixed-gauge sharpness result.**
The owning document proves three compatible statements:

1. the all-cross permanent is the complete residue modulo the ideal generated
   by all diagonal root quadrics on one balanced shore;
2. a fully target-supported common zero of those quadrics exposes an exact
   `P_m -> Delta_3` restriction; and
3. all-balanced rank drop does not force such a zero in an arbitrarily
   prescribed common root gauge.

The permanent extraction in item 2 is not presented as new.  It is the
zero-surplus interface already present in the maximal torus-root theorem.
The new live edge is that a common nondegenerate root quadric supplies a
fully supported conic point and therefore routes the whole common-quadric
shore to the permanent restriction family.  This excludes `m=3,4` by existing
exact permanent results and leaves `m>=5` open at `PR`.

Citrine packaged the claim; Amber and Saffron performed adversarial
fresh-reader checks inside the Codex team.  This is durable automated review,
not independent human peer review.  The phrase "independent audit" below
refers specifically to implementation independence of the no-import replay.

Reviewed package:

```text
claims/arbitrary-order/
  BALANCED_ROOT_QUADRIC_BASEPOINT_PERMANENT_RESTRICTION_AND_GAUGE_SHARPNESS_THEOREM.md
  verify_balanced_root_quadric_basepoint_permanent_restriction_and_gauge_sharpness.py
  audit_balanced_root_quadric_basepoint_permanent_restriction_and_gauge_sharpness.py
```

The global Krenn--Gu conjecture remains **UNRESOLVED**.

The theorem explicitly assumes shore size `m>=2`.  This is necessary already
for the phrase "concise weighted `Delta_3`": with only one nonroot mode the
three displayed target summands combine into a single covector.  All
Krenn--Gu applications have `m>=3`.

## 1. The matching partition has the correct balanced multiplicities

Fix `r` internal root edges.  They use `2r` roots, leaving `m-2r` roots to
cross.  Those cross edges use `m-2r` nonroots, leaving exactly `2r` nonroots,
which must form `r` internal edges.  Thus the two internal shore matchings
have equal size.  Conversely, choosing those two matchings and one bijection
between the remaining vertices determines exactly one perfect matching.

The `r=0` sector is therefore the unsigned `m x m` permanent with coefficient
one.  Every `r>=1` sector contains at least one generator of the root ideal.
No deck multiplier, determinant sign, or combinatorial factorial is missing
from the displayed identity.

Both new scripts reconstruct this classification independently.  The primary
keeps symbolic edge labels and compares the killed contraction with a direct
permanent through `m=5`; the audit counts the surviving bijections through
`m=6`.

## 2. Ideal membership is not confused with a common zero

The residue equations hold for the ideal

```text
I_R=(b_ij:i<j in R)
```

without any claim that `I_R` is principal, proper, radical, or has a
projective basepoint.  Evaluating the congruence at a point is used only after
a common projective zero is separately assumed or constructed.

This distinction is load-bearing.  The exact eight-vertex fixture has six
root quadrics forming a basis of all ternary quadrics in the prescribed
gauge, so `I_R=(x_0,x_1,x_2)^2` and its projective base locus is empty.  The
document therefore does not promote ideal membership alone into a pointwise
permanent identity.

## 3. Full target support is exactly the concision gate

At a common zero, putting `x_i=A_i^{-1}x` into every root kills every internal
root edge.  Equal shore sizes then force all remaining edges to cross, and
the full graph contraction is the local pullback of `P_m`.

The GHZ contraction has weights

```text
X_c=product_i e_(i,c)^*(x_i).
```

The proof assumes every one of these root coordinates is nonzero, so all
three weights are nonzero and the diagonal target is concise.  It does not
infer concision from a point on a coordinate boundary.  One invertible local
diagonal rescaling normalizes the weights; no illegal global scalar division
or target-stabilizer assumption is hidden.

The maps in the owning document have the correct direction for multilinear
forms: each nonroot local space maps to the `m` root-incidence coordinates,
and the permanent form is pulled back.  Dually this is the standard tensor
restriction convention used by the permanent packages.

## 4. The conjecture-range extraction is credited to the existing theorem

For `m>=3`, a fully supported pairwise-zero root half has cardinality `n/2`.
The multi-star theorem already forbids a larger root set.  Hence this half is
a maximum torus-root set, its outside set has zero surplus, and Theorem 3 of
the maximal torus-root package, whose stated scope is `n>=6`, specializes to

```text
P_m=weighted Delta_3.
```

The direct balanced matching proof is included for clarity, but the status
section explicitly calls the conjecture-range result a new proof-DAG edge
rather than a new extraction theorem.  This avoids double-counting an existing
mathematical advance.  The optional `m=2` statement lies outside that package
and follows directly from the new matching proof; its impossibility is then
the elementary local-rank comparison.

## 5. The conic-avoidance argument is absolute and finite

A nondegenerate ternary quadratic is absolutely irreducible in characteristic
zero, so its projective zero set is a smooth conic.  Every pulled-back target
coordinate is a nonzero linear form because each root identification is an
isomorphism.  No line contains the conic; each line therefore removes only a
finite intersection.  Finitely many such lines cannot cover the conic.

The chosen point kills every scalar multiple `rho_ij Q`, including a zero
root quadratic, and avoids all `3m` coordinate hyperplanes.  No assumption
that the root-to-nonroot cross blocks are separable, conformal, invertible, or
nonzero is inserted.

## 6. The low-order conclusions use the correct monotone invariant

At `m=3`, concision forces the three local maps on `P_3` to have rank three.
They are square and hence invertible, so tensor rank is preserved.  The exact
rank-four `P_3` theorem contradicts the rank-three diagonal target.

At `m=4`, the imported theorem states that the subrank of `P_4` is exactly
two.  This directly forbids a concise three-term diagonal restriction.  The
argument does not try to use ordinary tensor rank in a direction where local
maps could decrease it.

No analogous exclusion is claimed for `m>=5`; those orders are routed to the
live permanent restriction problem.

## 7. The rational sharpness table is exact but gauge-scoped

For the eight matrices `G_i`, direct exact calculation gives

```text
det(G_i)=(1,1,-1,1,-1,-1,1,1/54),
det(W_ij) in {-1,-1/54,1/54,1},
pure coefficients=(1,1,1),
T_W(00111111)=-1.
```

The six fixed-gauge root quadrics have coefficient determinant `-1`.
Therefore the table really has complete support, invertible blocks,
normalized pure terms, and empty fixed-gauge base locus, and it really is not
a witness.

The all-cut rank bound is not inferred from a sample.  Exact conjugation gives

```text
G_i^(-T) W_ij G_j^(-1)=I_3
```

on all 28 edges, putting the graph inside the already proved nondegenerate
common-quadratic orbit.  The existing covariance theorem then proves the
rank-at-most-seven statement for every contraction point and every balanced
cut.

This same conjugation is the essential caveat: the fixture is latently
common-quadric.  It refutes a basepoint inference only for prescribed
same-vector root identifications.  It neither refutes nor tests an
existential theorem allowing independent root gauges or arbitrary root
vectors.

## 8. Computational independence and replay meaning

The primary verifier uses SymPy symbolic expressions, permutation permanents,
matrix inverses, and exact rational graph coefficients.  The no-import audit
uses only the standard library, `Fraction`, separate perfect-matching
recursion, recursive determinants, and hand-written Gaussian inversion.  It
extends the matching census one order beyond the primary.

The two scripts share the displayed mathematical fixture, as they must, but
do not share implementation code, algebra systems, or matrix routines.  They
audit bounded constants and conventions.  The arbitrary-order result is the
written matching partition, conic geometry, and imported permanent theorems.

## 9. Acceptance boundary

The accepted live update is

```text
root-ideal residue on one balanced shore:              PROVED;
fully supported root-ideal basepoint => PR:             PROVED;
common nondegenerate root quadric => PR:                PROVED;
common-root-quadric shore for m=3,4:                    EXCLUDED;
common-root-quadric shore for m>=5:                     OPEN AT PR;
all-balanced rank drop => fixed-gauge basepoint:        FALSE;
all-balanced rank drop => latent synchronization:       NOT PROVED;
arbitrary all-balanced witness locus:                   OPEN;
global conjecture:                                      UNRESOLVED.
```

## Strongest fresh-referee objection

The easiest overstatement is: `the six fixed-gauge quadrics have no common
zero, so the graph has no torus-root half.`  That is false.  The graph is a
vertex-gauge common-quadratic model and acquires a conic of fully supported
root tuples after the displayed independent gauges.  The owning theorem and
frontier retain this distinction, which is why the fixture is accepted as a
fixed-gauge route warning rather than an S3 counterexample.
