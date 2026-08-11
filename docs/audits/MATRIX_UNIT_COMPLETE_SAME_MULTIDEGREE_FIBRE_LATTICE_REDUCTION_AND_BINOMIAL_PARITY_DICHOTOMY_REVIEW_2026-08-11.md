# Hostile review: complete same-multidegree fibre-lattice reduction

Date: 2026-08-11

Reviewed artifact:

[`../../claims/arbitrary-order/MATRIX_UNIT_COMPLETE_SAME_MULTIDEGREE_FIBRE_LATTICE_REDUCTION_AND_BINOMIAL_PARITY_DICHOTOMY_THEOREM.md`](../../claims/arbitrary-order/MATRIX_UNIT_COMPLETE_SAME_MULTIDEGREE_FIBRE_LATTICE_REDUCTION_AND_BINOMIAL_PARITY_DICHOTOMY_THEOREM.md)

Review disposition: **PASS at the stated arbitrary-order reduction scope**.

This review does not change the global status.  The Krenn--Gu conjecture
remains **UNRESOLVED**.

## 1. Claim under review

The artifact does not claim a global matrix-unit exclusion.  Its claimed
advance is the following exact reduction for one complete mixed
same-multidegree block on a fixed complete nonzero `r=1` matrix-unit label
support:

1. divide each nonempty matching-fibre equation by one invertible reference
   matching monomial;
2. place every normalized equation in the group algebra of the lattice of
   within-fibre matching differences;
3. descend unit-ideal and holonomy-elimination questions faithfully to that
   group algebra;
4. classify the special case in which every nonempty fibre is binomial by
   integer-kernel sign parity.

Singleton fibres give a unit.  In an all-binomial block, an odd signed
dependency gives a unit, while a parity-consistent block is proper and gives
exactly the existing cycle sign equation in the selected holonomy.  Aggregate
fibres remain open.

## 2. Adversarial questions and findings

### 2.1 Is the normalization merely a specialization?

No.  For each nonempty fibre,

```text
C_chi=lambda^(M_chi) f_chi
```

is an identity in the full physical Laurent ring.  The removed factor is a
unit precisely because the theorem stays on the complete nonzero physical
torus.  No amplitude is assigned a value and no matching term is dropped.

### 2.2 Does the difference lattice depend on the reference matching?

No.  Changing the reference translates every exponent in that fibre by one
within-fibre difference.  The generated lattice is unchanged and the
normalized polynomial is multiplied by a Laurent monomial from that same
lattice.  The ideal in the group algebra is therefore unchanged.

### 2.3 Does freeness fail for a nonsaturated sublattice?

No.  For any subgroup `L <= Z^E`, not only a saturated one, the ambient group
algebra splits as a direct sum of rank-one copies of `k[L]` indexed by the
set of cosets `Z^E/L`.  Torsion in the quotient changes multiplication among
chosen representatives but does not destroy the module basis.  Thus the
extension is free and faithful, and extension-contraction of the normalized
ideal is exact.

This point is load-bearing.  Replacing it by a claim that `L` is a direct
summand would be false in examples such as `2Z <= Z`; the theorem makes no
such claim.

### 2.4 Is the holonomy-elimination equality justified?

Yes.  The holonomy exponent is a sum of ratios of matchings inside the cycle
fibres, so it lies in the within-fibre lattice.  Therefore both the normalized
ideal and `H-X^z` lie in the zero-coset summand after adjoining `H`.  The same
free-module contraction applies before intersecting with `k[H]`.

In the parity-consistent all-binomial branch, the quotient is nonzero and
`H` equals the base-field scalar `(-1)^m`.  Hence the kernel of the map from
`k[H]` is exactly `H-(-1)^m`, not merely an ideal containing that polynomial.

### 2.5 Does parity consistency really imply the binomial ideal is proper?

Yes.  If every integer kernel relation has even sign parity, the transported
sign is a well-defined character on the generated lattice.  Evaluating each
group monomial at that character annihilates every normalized binomial and
sends `1` to `1`.  This gives a direct properness certificate in `k[L]`.

Over an arbitrary characteristic-zero base field this proves properness but
need not give a rational physical-torus point.  The theorem correctly claims
an actual full torus point only over `C`, where the lattice character extends
to `Z^E` by choosing roots in a Smith basis.  An earlier draft risk would have
been to conflate these two statements; the reviewed text keeps them separate.

### 2.6 Are the binomial coefficients really both one?

Yes at the polynomial level used here.  Each physical edge has one fixed
matrix-unit label pair and one Laurent amplitude variable.  Each compatible
perfect matching contributes the product of its edge variables with
coefficient one.  Numerical signs and phases belong to the values of those
variables, not to extra polynomial coefficients.  The theorem would require
modification for an edge carrying a sum of several matrix units, which is
outside the stated `r=1` branch.

### 2.7 Is every word in the chosen block a zero target?

Yes because the multidegree is explicitly mixed.  Pure multidegrees are
excluded from the theorem's target-zero block.  Empty fibres contribute the
tautology zero and are retained in the definition of completeness.

### 2.8 Does the theorem prove transport reachability between all words?

No, and it does not use such reachability.  The target tensor independently
requires every mixed word coefficient in the block to vanish.  Same
multidegree remains only a grading for the bridge dynamics.  The theorem is
an algebraic complete-block result, not a graph-connectivity assertion.

### 2.9 Is the signed-lattice theorem being duplicated or silently promoted?

The integer-kernel parity criterion predates this checkpoint.  The new
document cites it explicitly and restates the short argument only so the
matrix-unit specialization and holonomy equality are auditable in place.
The new mathematical content is the complete-fibre normalization, faithful
group-algebra descent, and exact connection to the live `U7` block.

### 2.10 Does this close the requested unit-or-syzygy obligation?

Only partially.  It completely decides singleton and all-binomial complete
blocks, but it does not force either condition from arbitrary active-cycle
response data.  Any fibre of size at least three remains an aggregate
polynomial in the smaller group algebra.  The canonical frontier must retain
that aggregate obligation, along with cross-multiplicity, pure-cofactor, and
deeper-blocker exits.

## 3. Evidence review

The primary verifier:

- imports the established fixed `U7D` table and exact Smith-form lattice
  implementation;
- reconstructs all complete block fibres matching-first;
- checks every nonempty fibre normalization at two nonzero rational
  assignments;
- recovers the singleton unit and the three active-cycle relation rows;
- checks saturated and nonsaturated consistent and inconsistent signed
  systems; and
- audits a nonsaturated group-algebra coset decomposition.

The independent verifier:

- imports no repository module;
- reconstructs each of the 70 words separately by target-constrained
  recursion;
- uses different reference choices and rational assignments;
- certifies full integer kernels through explicit unimodular domain bases and
  independent rational-rank arithmetic;
- rebuilds the active cycle and its endpoint-character-zero holonomy; and
- audits a skew nonsaturated sublattice rather than the primary diagonal
  example.

The two scripts are genuinely separate implementations.  Their finite
checks do not prove the universal claims; those claims rest on the written
group-algebra and parity arguments.

## 4. Boundary attacks

The following changes would invalidate or require altering the theorem and
are correctly excluded:

- characteristic two, where `1=-1` is not a contradiction;
- zero physical amplitudes, where reference matching monomials need not be
  units;
- an edge carrying multiple matrix units rather than one fixed unit;
- a pure word multidegree, whose target coefficient is nonzero rather than
  zero;
- a sampled or selected subset of a fibre instead of every compatible
  matching;
- a holonomy exponent outside the within-fibre lattice; or
- claiming a base-field torus point over a non-algebraically-closed field
  solely from properness.

No such scope extension appears in the reviewed artifact.

## 5. Verdict and live frontier

The proof is accepted as an exact characteristic-zero arbitrary-order
reduction.  It strengthens the live `U7C -> U7` edge as follows:

```text
complete same-degree singleton      -> unit;
complete all-binomial odd parity    -> unit;
complete all-binomial consistent    -> exactly H=(-1)^m, no stronger P(H);
complete aggregate block            -> reduced to k[L_mu], still open.
```

It does not exclude an arbitrary active cycle, the complete nonzero `r=1`
matrix-unit branch, or the global conjecture.  No counterexample is produced.
The global Krenn--Gu status remains **UNRESOLVED**.
