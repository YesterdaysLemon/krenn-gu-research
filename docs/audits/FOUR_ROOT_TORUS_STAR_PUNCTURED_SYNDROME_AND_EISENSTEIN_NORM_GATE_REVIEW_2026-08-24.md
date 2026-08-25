# Hostile review: four-root torus-star punctured syndrome gate

Date: 2026-08-24

## Verdict

**Accept at the declared parent-theorem and boundary-control scope.**  The
package gives a useful structural reduction of the one fixed torus-star
space from `GLD70`, proves its complete characteristic-zero one-word syndrome
dichotomy, derives exact low-degree necessary gates, and records a
load-bearing counterexample to pairwise syndrome independence.

It does not prove the determinant-safe three-word statement, the fixed-star
GHZ exclusion, or any graph-level contradiction.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Reviewed artifacts:

- [`FOUR_ROOT_TORUS_STAR_PUNCTURED_SYNDROME_AND_EISENSTEIN_NORM_GATE_THEOREM.md`](../../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_PUNCTURED_SYNDROME_AND_EISENSTEIN_NORM_GATE_THEOREM.md);
- [`verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py`](../../claims/arbitrary-order/verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py);
- [`audit_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py`](../../claims/arbitrary-order/audit_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py);
- [`generate_four_root_torus_star_punctured_syndrome_singular_atlas.py`](../../claims/arbitrary-order/generate_four_root_torus_star_punctured_syndrome_singular_atlas.py);
- the owning [`GLD70` theorem](../../claims/arbitrary-order/FOUR_ROOT_COMPLETE_Q_LAYER_SECANT_BOUNDARY_TRAP_AND_TORUS_STAR_COMPRESSION_THEOREM.md).

## 1. Exact scope under review

`GLD70` reduces every fully supported rank-two maximal torus star to one
fixed `44`-dimensional nuisance space `N_star` inside the `81`-dimensional
four-qutrit tensor space.  Its remaining strong question is whether

```text
N_star intersect GHZ_3 = empty.
```

The reviewed package does not answer that question.  It removes the exact
`21`-dimensional pair layer, represents the `23`-dimensional quotient by a
`37`-dimensional annihilator in a `60`-coordinate punctured ambient space,
and asks whether every three-word syndrome dependency has singular centre.

This is a parent reformulation of the fixed-space problem.  It is not another
targetwise selector theorem, and it obeys the repository rule against a
third sibling theorem without a serious parent-theorem attempt.

## 2. Puncture and dimension audit

The pair layer is supported exactly on tensor coordinates for which at least
two of the three leaf indices are `2`.  There are seven such leaf words and
three centre coordinates.  The primary verifier checks that the `54` raw pair
columns vanish on the complementary `60` coordinates and have rank `21` on
the erased `21` coordinates.

After puncturing, the `Q+residual` columns have rank `23`; the complete raw
map still has rank `44`.  Hence the punctured kernel is exactly the pair
layer, not merely a `21`-dimensional subspace with an unproved identification.

The no-import audit reconstructs the fixed ports and all `79` columns from
the permanent using a subset dynamic program and reversed layer and label
orders.  It independently returns

```text
pair rank / erased rank / punctured quotient / full rank = 21/21/23/44.
```

Its root-slice codimensions are independently `4,4,6`.

## 3. One-word theorem audit

The erasure classification is elementary: a leaf product has no coordinate
with at most one index `2` exactly when at least two factors are the `e_2`
axis.  Outside that locus, at least two leaves have a nonzero binary
coordinate.  Leaf permutation symmetry therefore reduces the projective
cover to

```text
2*2*3*3=36
```

charts: binary pivots on two leaves, an arbitrary pivot on the third leaf,
and an arbitrary centre pivot.

The primary verifier pins `37` sparse integer annihilator rows, checks exact
rank `37`, checks exact annihilation of a reconstructed `44`-column nuisance
basis, checks that the relations vanish on the erased coordinates, and
checks all six leaf permutations preserve the nuisance space.  It then runs
exact SymPy Groebner bases over the characteristic-zero coefficient domain.
Every one of the `36` chart ideals contains a nonzero constant.

A separate Singular 4.3.2 calculation retained all three choices of the two
binary-visible leaves instead of invoking symmetry.  The committed generator
reconstructs the pinned equations and streams the exact rational `108`-chart
program to the second CAS.  Its current generated program has SHA-256

```text
a86c4fbdf6e149f04af06b78147f62e8b465e64b9595a2de3a643b01aa6f04f4
```

and reported:

```text
ATLAS_COUNTS
108
108
DONE
```

This is an independent computer-algebra route for the unit-ideal step.  The
no-import audit also reconstructs the punctured annihilator modulo `5` and
exhausts all `31^3=29791` projective leaf triples.  It finds exactly

```text
91 pair-erased words of syndrome rank 0;
29700 non-erased words of syndrome rank 3.
```

The finite census is corroborative only.  The characteristic-zero conclusion
comes from the exact rational atlases and the proved projective chart cover.

## 4. Root-slice and norm-gate audit

The six displayed third-root relations are visibly sparse two-term
annihilators.  Direct substitution of the dense leaf chart gives

```text
r(y-x), r(1-xy), q(z-x), q(1-xz), p(z-y), p(1-yz).
```

The primary verifier checks these identities symbolically.  They are only a
slice of the `37` parity checks; the theorem does not promote them to an
equivalent compression.

On the binary cube, every pair-layer column vanishes.  The primary verifier
constructs the unrestricted symbolic `Q+residual` tensor and factors all
three balanced `4 x 4` determinants as the stated products of differences of

```text
s(alpha,beta)=alpha^2-alpha beta+beta^2.
```

The no-import audit directly rebuilds the permanent tensors and agrees at
three unrelated exact rational coefficient assignments, including a zero
`Q` coefficient.  Those evaluations audit conventions; the symbolic primary
calculation is the exact polynomial identity.

The implication from the three products to “at least three of four norms are
equal” is valid over a domain.  The theorem does not identify these nuisance
coefficient differences with syndrome leaf coordinates and does not infer
more than a necessary binary-subcube gate.

## 5. Hostile attacks and rejected strengthenings

### 5.1 One-word rank three implies pairwise rank six

Rejected by an exact characteristic-zero countermodel.  With the leaf frame

```text
[ 1  1  1]
[-1  0  0]
[ 0 -1  0]
```

all columns are non-erased and the frame determinant is `1`, but the second
and third leaf words give a six-column syndrome block of rank `5`.  The
corresponding centre has rank `2`; the full syndrome rank is `8`.  Direct raw
membership, epsilon zero, and balanced ranks `(2,2,2)` replay exactly in both
implementations.

This control is important: a classical minimum-distance or MDS slogan is
false even off the hidden pair layer.

### 5.2 Ten compressed equations suffice on the diagonal leaf locus

Rejected.  During hostile search, a ten-row experimental compression
produced the rational frames

```text
x=(0,1,2),          p=(1/3,95/174,0)
```

and an apparent invertible centre.  The leaf determinant was `-22/29` and
the centre determinant was nonzero, so this was escalated as a potential
exact counterexample.

Full replay against the actual `37`-row syndrome returned rank `9` and seven
nonzero residuals.  Appending its tensor to the raw nuisance basis increased
rank from `44` to `45`.  The tensor itself had nonzero epsilon and balanced
ranks `(3,3,3)`, confirming that the failed membership test—not the GHZ
construction—was the defect.  No counterexample survived.

This episode justifies retaining all coupled parity checks in the live
obligation.

### 5.3 Binary balanced minors define the third secant

Rejected.  The three determinants are necessary restrictions of balanced
flattening minors.  They neither include the other coordinates nor replace
the Strassen equations in the `GLD70` set-theoretic secant description.

### 5.4 A surviving nuisance GHZ tensor would immediately be a graph witness

Rejected exactly as in `GLD70`.  Even a genuine point of
`N_star intersect GHZ_3` would refute this strong fixed-space exclusion, but
would not automatically satisfy the fixed graph target, uncontracted
equations, source consistency, or same-graph integrability.

## 6. Evidence boundary

The package has four distinct evidence layers:

- an exact mathematical puncture and syndrome reformulation;
- an exact computer-assisted characteristic-zero one-word theorem, replayed
  by SymPy and Singular;
- exact symbolic root-slice and Eisenstein determinant identities;
- finite-field and exact-point hostile controls that corroborate conventions
  and refute overstrong variants.

None of these proves the three-word saturation.  Timeouts or failed larger
Groebner attempts used during exploration are not evidence and are not cited
as such.

## 7. Accepted frontier delta

The fixed-star question is no longer best represented as an opaque
`79`-parameter secant saturation.  It now has the following staged form:

1. pair erasure is removed exactly;
2. one non-erased word always consumes three syndrome dimensions;
3. two-word dependencies exist but the certified example is confined to the
   singular-centre boundary;
4. any honest three-word survivor must pass all coupled root-slice checks and
   the equal-Eisenstein-norm divisors;
5. the decisive remaining task is to prove every full-syndrome kernel centre
   singular, or to find and independently validate a genuine invertible-centre
   survivor.

This is meaningful progress toward the universal bridge but not its closure.
