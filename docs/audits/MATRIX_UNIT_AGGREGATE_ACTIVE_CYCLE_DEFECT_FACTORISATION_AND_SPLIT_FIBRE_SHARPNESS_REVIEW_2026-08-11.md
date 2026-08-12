# Hostile review: aggregate active-cycle defects and split fibres

Date: 2026-08-11

Reviewed artifact:

[`../../claims/arbitrary-order/MATRIX_UNIT_AGGREGATE_ACTIVE_CYCLE_DEFECT_FACTORISATION_AND_SPLIT_FIBRE_SHARPNESS_THEOREM.md`](../../claims/arbitrary-order/MATRIX_UNIT_AGGREGATE_ACTIVE_CYCLE_DEFECT_FACTORISATION_AND_SPLIT_FIBRE_SHARPNESS_THEOREM.md)

Review disposition: **PASS at the stated aggregate-cycle recurrence and
selected-subsystem sharpness scope**.

The Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Exact obligation under review

The active-cycle theorem previously split into two cases: all selected fibres
are binomial and force `H=(-1)^m`, or at least one cycle fibre is aggregate.
The aggregate branch had no exact holonomy formula.

The reviewed checkpoint claims:

1. the complete extra matching sum in every cycle fibre defines a
   gauge-invariant normalized defect `A_i`;
2. complete target-zero equations give the arbitrary-order identity
   `H=(-1)^m product_i(1+A_i)`;
3. an aggregate fibre may have `A_i=0` because its nonzero extra terms cancel
   separately, so aggregate combinatorics does not exclude sign holonomy;
4. one complete, locally concise eight-vertex matrix-unit family satisfies
   three complete cycle equations with fibre sizes `5,2,2` and has
   `H=-2/(1+2t)`; and
5. the selected cycle subsystem has zero elimination ideal in
   `Q[H,H^(-1)]`.

The family is explicitly not a Krenn--Gu witness because all three pure
target coefficients are zero.

## 2. Adversarial proof checks

### 2.1 Are all terms of the aggregate fibre included?

Yes.  The definition lists every compatible perfect matching other than the
selected incoming and outgoing matchings.  Equation (8) in the theorem is
the complete mixed target coefficient, not a selected subfibre equation.

The sharpness verifier enumerates all `105` perfect matchings on eight
vertices and recovers exactly five, two, and two compatible terms at the
three cycle words.  The independent audit instead enumerates disjoint
four-edge masks from all 28 physical pairs and obtains the same census.

### 2.2 Is the normalization safe?

Yes.  Each denominator is the weight of the selected outgoing physical
perfect matching `F_i`.  Complete nonzero matrix units make every factor and
therefore the matching monomial nonzero.  The proof never divides by the
aggregate sum `A_i` or assumes that it is nonzero.

### 2.3 Why is each aggregate defect gauge invariant?

Every extra matching and `F_i` induces the same word `chi_i`.  A diagonal
endpoint-coordinate gauge multiplies all of those monomials by the same word
character.  Each ratio and their sum are invariant.  The independent audit
also applies a nontrivial exact power-of-two gauge and recomputes unchanged
defects and holonomy.

### 2.4 Is the sign in the product formula oriented correctly?

Dividing the fibre equation by `lambda(F_i)` gives

```text
lambda(G_(i-1))/lambda(F_i)=-(1+A_i).
```

Multiplication gives `(-1)^m product(1+A_i)`.  Cyclic reindexing changes
`product lambda(G_(i-1))` to `product lambda(G_i)`, which is precisely the
numerator in the established definition of `H`.  No reciprocal was lost.

### 2.5 Why is `1+A_i` nonzero?

The displayed ratio equals `-(1+A_i)`, and both selected matching monomials
are nonzero.  This proves rather than assumes the exceptional-divisor
exclusion.

### 2.6 Can a combinatorially aggregate fibre really have zero defect?

Yes.  In the `t=1/2` specialization, the aggregate fibre has five nonzero
terms.  The selected pair has weights `1,-1`, and the other three have
weights `1/2,-1,1/2`.  Both sub-sums vanish.  Therefore the complete fibre is
aggregate while `A_0=0` and `H=-1=(-1)^3`.

This is not obtained by setting a physical amplitude to zero.

### 2.7 Is every physical pair present in the family?

Yes.  The imported 18 transition edges, four aggregate edges, and six
completion edges are disjoint and total all `binomial(8,2)=28` pairs.  Away
from `t=0` and `1+2t=0`, every weight is nonzero.

### 2.8 Does the completion silently change the cycle fibres?

No.  Each of the six completion edges has an endpoint label different from
the corresponding label of every one of the three cycle words.  It is
therefore incompatible with all three words.  The exhaustive matching
censuses independently confirm that the complete fibre sizes remain
`5,2,2`.

### 2.9 Is local concision actually checked?

Yes at the matrix-unit label-support level used in the claim.  At each of the
eight vertices, the incident endpoint labels contain `0,1,2`.  Hence the
incident matrix-unit covectors span the three coordinate directions.  This
does not imply the global GHZ target equations, and the theorem does not say
that it does.

### 2.10 Do the three fibre equations vanish identically in the parameter?

Yes.  The two binomial fibres have weights `1,-1`.  The aggregate fibre has
weights

```text
1,x,t,x,t,
x=-(1+2t)/2,
```

whose sum is `1+2x+2t=0`.  The selected bridge products are one and the
selected cross products are `x,-1,-1`, so `H=1/x=-2/(1+2t)`.

### 2.11 Is the zero elimination statement merely based on samples?

No.  The localized selected subsystem is

```text
1+2x+2t=0,
Hx-1=0.
```

It maps to `Q(t)` by `x=-(1+2t)/2` and `H=-2/(1+2t)`.  Since the image of
`H` is a nonconstant rational function of a transcendental parameter, the
map from `Q[H,H^(-1)]` is injective.  Thus the intersection ideal is zero.

The SymPy checker finds no `H`-only element in the exact lexicographic basis.
The no-import audit separately proves triangular independence of the
substituted powers through degree ten.  Those finite ranks audit the written
all-degree injectivity proof; they do not replace it.

### 2.12 Are the localization divisors complete?

For this family, yes.  The new edge `47` has weight `t`, so `t!=0`.  The
selected edge `24` has weight `-(1+2t)/2`, so `1+2t!=0`.  All other weights
are units `1` or `-1`.  The holonomy is consequently nonzero.  No additional
denominator is introduced by the defect formula.

### 2.13 Does zero cycle-subsystem elimination imply the full target ideal is proper?

No.  This was the main scope hazard.  The family satisfies only the three
complete cycle-word target equations.  Its pure coefficients are zero rather
than one, and other mixed target equations are not claimed.  The complete
target ideal could and in this family does reject the table.  The theorem
therefore closes only an aggregate-cycle-only holonomy inference.

### 2.14 Is the family an apparent counterexample requiring escalation?

No.  Exact enumeration shows no compatible matching at any constant word
`0^8,1^8,2^8`; all three required pure coefficients are zero.  It fails the
original target definition transparently and is retained only as a sharpness
mechanism.

### 2.15 What genuinely remains load-bearing?

An additional theorem must constrain the product of the defects or make the
full target ideal a unit.  Possible mechanisms are effective
cross-multiplicity overlap, a forced quotient of free rank at most one whose
every torsion sheet is killed, or a mixed/deeper equation tied to the pure
exit.  Physical-variable overlap by itself is not such a relation.

## 3. Evidence independence

The primary verifier uses recursive perfect matchings, exact SymPy rational
functions, symbolic defect identities, endpoint-character circulation, and
a small lexicographic elimination.  It checks:

- all 28 physical pairs and every local label set;
- the exact complete `5/2/2` cycle fibres;
- the three identically zero coefficient sums;
- `H=-2/(1+2t)` and the defect product;
- split `t=1/2` and nonsplit `t=1` specializations;
- absence of all three pure matching fibres; and
- zero `H`-only polynomial generators in the selected subsystem.

The independent audit imports neither the primary code nor SymPy.  It uses
four-edge subset masks, exact `Fraction` evaluations at four rational
parameters, a separately implemented diagonal gauge, and rational Gaussian
elimination on the triangular substitution matrix.  Its matching-first
representation and elimination route are distinct from the primary
derivation.

The arbitrary-order defect formula is the written complete-fibre division
and telescoping proof.  The finite scripts exactly verify the physical
sharpness family and its selected-subsystem algebra.

## 4. Remaining boundary

The checkpoint leaves open:

- whether the complete target block of every hypothetical witness constrains
  the aggregate-defect product;
- forcing effective cross-multiplicity overlap rather than shared variables;
- forcing global quotient free rank at most one and killing every sheet;
- controlling rank-at-least-two target ideals;
- coupling sparse pure fans or aggregate pure ports to mixed response;
- the deeper-blocker branch;
- exclusion of the complete nonzero `r=1` matrix-unit branch; and
- the global conjecture.

No global status changes follow from the zero selected-subsystem elimination.

## 5. Verdict

The theorem is accepted as an exact arbitrary-order aggregate-cycle normal
form and a complete physical sharpness boundary.  It proves that aggregate
cycle equations alone can leave holonomy algebraically free and that even an
aggregate fibre can retain the binomial sign through an internal split
cancellation.  This removes aggregate-fibre counting as a standalone route
and isolates genuine cross-equation coupling as the next obligation.

The global Krenn--Gu conjecture remains **UNRESOLVED**.
