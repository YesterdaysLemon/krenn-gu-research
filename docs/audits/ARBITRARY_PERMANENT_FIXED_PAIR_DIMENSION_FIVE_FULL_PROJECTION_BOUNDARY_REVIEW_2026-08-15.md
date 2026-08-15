# Hostile review of the fixed pair-dimension-five full-projection boundary

## Verdict and provenance

**PASS, with the stated fixed-pair and characteristic-zero scope.**  No
mathematical or implementation blocker survived hostile review.  For the
specific two local colour frames displayed in the theorem, an actual weighted
restriction `P_6 -> Delta_3` cannot have rank three in all eight maps

```text
Phi_k|L_t,        k in {1,2}, t in {2,3,4,5}.
```

Equivalently, at least one of those eight projected ranks is at most two.  The
result is pointwise and exact.  It does not classify all pair-product spaces
of dimension five, normalize an arbitrary equality-five pair to this frame,
or exclude the remaining low-projection locus.  Consequently unrestricted
`P_6 -> Delta_3`, arbitrary-order permanent nonrestriction, and the global
Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_DIMENSION_FIVE_FULL_PROJECTION_BOUNDARY.md
  verify_arbitrary_permanent_fixed_pair_dimension_five_full_projection_boundary.py
  audit_arbitrary_permanent_fixed_pair_dimension_five_full_projection_boundary.py
```

The theorem was first reconstructed independently from the fixed vectors and
then compared line by line with the written proof.  The review separately
recomputed the square-free products, complement quartics, hyperplane-product
lemma, all sixteen common-factor cells, and all 729 coefficients of the
sharpness fixture.  Three precision issues found during review were corrected:
the stripped scope of the one-dimensional annihilator was made explicit, the
`x_4x_5` extraction in the sixteen-cell calculation was typed correctly, and
the fixture was no longer described as failing a formal hypothesis that
Theorem 3 does not have.

## 1. Dependency and proof-topology audit

The earlier
`ARBITRARY_PERMANENT_COTWO_PRODUCT_SENSOR_CORANK_TWO_STRENGTHENING_THEOREM.md`
is a contextual predecessor: it proves that dimension five is the universal
lower boundary for a two-mode product space in a hypothetical restriction.
The new proof does not import its difficult equality-four classification.  It
directly verifies that the displayed fixed pair has dimension five and then
uses the standard square-free/permanent dictionary pointwise.

Nor does the proof import the global fourth-order permanent-subrank theorem.
It proves the narrower hyperplane-zero lemma that it needs.  Thus the logical
spine of the new result is:

```text
fixed product table
  -> two factored mixed-radical quartics
  -> full pair-mixed tensor zeros
  -> common omitted factor for each quartic
  -> one of sixteen common-kernel cells
  -> complementary pure pairing rank at most two
  -> contradiction with three nonzero diagonal outputs.
```

No generic point, Zariski closure, orbit-closure specialization, or finite
case-cover assertion enters this implication.  It is a pointwise theorem for
one fixed coordinate pair.

## 2. Independent reconstruction of the fixed algebra

In the edge order `(01,02,03,12,13,23)`, direct multiplication in
`Z_6=K[x_0,...,x_5]/(x_i^2)` gives

```text
u_i v_j = [[d_0,m_1,m_1],
           [m_2,d_1,m_2],
           [m_2,m_1,d_2]],
```

where

```text
m_1=(0,1,-1,0, 0,-1),    m_2=(0,0,0,1,-1,-1),
d_0=(1,1, 0,0,-1,-1),    d_1=(1,0,-1,1, 0,-1),
d_2=(0,0, 0,0, 0,-2).
```

These five vectors are independent in characteristic zero; one explicit
five-by-five minor is `-4`.  Hence `dim B=5`, while
`M=span(m_1,m_2)` has dimension two.  Inside the stripped six-dimensional
quadratic space on variables `0,1,2,3`, the unique ordinary relation is

```text
q_02+q_03+q_12+q_13=0.
```

The review also checked the distinction between that stripped annihilator and
the full degree-four annihilator of `B` in `Z_6`.  Under the perfect
edge/complement pairing, the latter has dimension ten and is

```text
span{x_S : |S|=4 and {4,5} is not a subset of S}
  direct-sum K x_4x_5(x_0+x_1)(x_2+x_3).
```

The corrected theorem wording does not conflate these two spaces.

Complementing the two mixed vectors gives exactly

```text
F_1=x_1x_4x_5(x_3-x_2-x_0),
F_2=x_0x_4x_5(x_3-x_2-x_1).
```

Because the four factors in each display have disjoint coordinate supports,
their ordinary factorization and their square-free four-linear polarization
agree without hidden repeated-variable terms.  The review checked this
identity on all coordinate inputs as well as symbolically.

## 3. The four-hyperplane zero lemma

Let `H_alpha,H_beta` be hyperplanes of a four-space and let
`A_(alpha,beta)` be the span of their square-free quadratic products.  Its
annihilator is the space of symmetric zero-diagonal forms vanishing on
`H_alpha x H_beta`.

If the normals are independent, such a form kills their common two-plane and
descends to a symmetric form on a two-dimensional quotient.  The
zero-diagonal condition rules out a three-dimensional annihilator, so the
product space has dimension at least four.  If the normals are proportional,
every annihilating symmetric form is

```text
alpha tensor z + z tensor alpha.
```

In characteristic different from two, its zero diagonal forces `z_i=0` on
the support of `alpha`.  Therefore

```text
dim A_(alpha,alpha)=2+|supp(alpha)|.
```

Every hyperplane-product space consequently has dimension at least three,
with equality exactly for two copies of one coordinate hyperplane.

If the four-variable permanent vanishes on
`H_0 x H_1 x H_2 x H_3`, the two pair-product spaces for `01|23` are
orthogonal under the perfect edge-complement pairing.  Their dimensions sum
to at most six, so both dimensions are exactly three.  Each pair is therefore
a repeated coordinate hyperplane.  Coordinate-hyperplane product spaces are
self-orthogonal, and unequal ones are not mutually orthogonal, forcing the
same omitted coordinate in all four modes.

As independent falsification, referee-side exhaustive calculations over
`F_3` and `F_5` found exactly four zero configurations: the four common
coordinate hyperplanes.  The checked projective sets had respectively 40 and
156 normals.  The independent repository audit separately checks all 12,246
unordered hyperplane pairs over `F_5` and finds dimension three in exactly the
four coordinate cases.  These finite checks support the formulas; the written
linear-algebra argument proves the characteristic-zero lemma.

## 4. Exact quantifier bridge and sixteen-cell obstruction

For an actual diagonal restriction, every coefficient whose first two colours
differ is zero.  Since `m_1` and `m_2` occur as such fixed pair products, this
is the vanishing of each entire pulled-back four-linear tensor, not merely a
selection of Hamming-near coefficients.  If all eight projected ranks were
three, the four images under each `Phi_k` would be hyperplanes.  The preceding
lemma then supplies one factor

```text
phi in {x_1,x_4,x_5,ell_1},
psi in {x_0,x_4,x_5,ell_2}
```

that vanishes on every `L_t`.  The choice is common to all four complementary
modes for each quartic.  Shared factors such as `x_4` or `x_5`, including the
codimension-one cases `phi=psi`, are retained rather than silently discarded.

The complementary quartics of the three diagonal pair products are

```text
D_0=x_4x_5(x_1+x_2)(x_3-x_0),
D_1=x_4x_5(x_0+x_2)(x_3-x_1),
D_2=-2x_0x_1x_4x_5.
```

The sixteen common-kernel cells have exact pairing ranks

```text
                     psi
              x_0   x_4   x_5   ell_2
phi  x_1       1     0     0      2
     x_4       0     0     0      0
     x_5       0     0     0      0
     ell_1     2     0     0      2.
```

This table was rederived without the primary implementation.  Any row or
column involving `x_4` or `x_5` kills all three `D_i`.  In the four remaining
cells:

- `(x_1,x_0)` has `D_2=0` and `D_0=D_1`, hence rank one;
- `(x_1,ell_2)` and `(ell_1,x_0)` have `D_2=0`, hence rank at most two; and
- `(ell_1,ell_2)` forces `x_0=x_1`, while
  `D_0-D_1=x_4x_5(x_1-x_0)(x_2+x_3)`, hence rank at most two.

The generated product-space calculation shows that the displayed upper bounds
are the exact ambient cell ranks.  No assumption that the four `L_t` are
equal is used: their products merely lie in the common-kernel product space.

Conversely, the three constant-colour complementary products evaluate on
`d_0,d_1,d_2` as a diagonal matrix with three nonzero entries.  Their induced
functionals on `B` are therefore independent.  Rank at most two versus rank
at least three is the required contradiction.  This step uses precisely the
nonzero diagonal-output hypothesis; zero pure blocks are not admitted or
silently divided away.

## 5. Characteristic boundary

The theorem correctly claims characteristic zero.  The linear-algebra proof
in fact uses invertibility of two at its visible critical points, but the
review does not promote the statement to a broader field scope.

Characteristic two is a genuine failure mode, not a cosmetic exclusion:

- the displayed five-vector basis drops from rank five to rank three;
- `d_2=-2x_2x_3` becomes zero;
- the order-four permanent equals the determinant, so its restriction to four
  copies of any three-dimensional hyperplane vanishes, not only coordinate
  hyperplanes; and
- all three sharpness weights `(-4,8,-2)` become zero.

Thus neither the equality-five premise, the hyperplane classification, nor
the nonzero-pure sharpness claim survives unchanged in characteristic two.

## 6. Sharpness fixture and its exact limitation

The six-mode fixture was recomputed by direct `6!` permanent enumeration for
all `3^6=729` colour words.  Every local frame has ambient rank three, while
the two projection profiles on modes `2,3,4,5` are

```text
Phi_1: (3,3,3,1),       Phi_2: (2,2,2,2).
```

Exactly 18 coefficients are nonzero and 711 are zero.  All
`6*3^4=486` words with unequal first-pair colours vanish, all 36 Hamming-one
neighbours of the monochromatic code vanish, and the three pure coefficients
are `(-4,8,-2)`.  With Hamming distance defined as minimum distance to
`{000000,111111,222222}`, the surviving mixed words consist of nine words in
shell two and six in shell three.  The middle three-mode support is exactly a
colour-permuted copy of the six-term `P_3` permanent support.  The canonical
all-word serialization has SHA-256

```text
1360041C9A60D4451F58F18B978DFB30C86B707BB4FC7C860D7573D4686A7DA8.
```

This fixture is not a restriction to `Delta_3`: its fifteen Hamming-two or
Hamming-three coefficients are explicit nonzero violations.  It proves only
that full pair-mixed zeros, nonzero pure outputs, Hamming-one zeros, and
ambient local rank three do not eliminate the low-projection residual.  It
does not show that Hamming-two information is necessary in the all-eight-
ranks-three case, which the theorem already excludes using the full
pair-mixed tensors.

## 7. Computational independence and replay

The primary verifier uses SymPy, a sparse square-free subset algebra,
symbolically generated common kernels, and generated fourth product powers.
It checks both quartic tensors on all `2*6^4=2,592` coordinate entries,
constructs every one of the sixteen cells, and computes the fixture's 729
coefficients by subset multiplication.

The independent audit imports neither the primary module nor SymPy.  It uses
`Fraction` Gaussian elimination, separately hard-coded residual quadratic
bases, bit-mask quartic multiplication, exhaustive projective hyperplane-pair
enumeration over `F_5`, and direct 720-permutation evaluation of every fixture
coefficient.  The two implementations agree on the product table, quartics,
sixteen-cell ranks, projection profiles, full coefficient support, Hamming
ledger, colour-permuted `P_3` support, and serialization hash.

Focused final replay passed:

```text
new primary verifier:                         PASS;
new independent no-import audit:             PASS;
new py_compile:                              PASS;
new Ruff check:                              PASS;
corank-two predecessor primary/audit:        PASS/PASS;
product-sensor predecessor primary/audit:    PASS/PASS.
```

The finite scripts replay coordinate identities and provide independent
falsification.  The written hyperplane and rank arguments, not the bounded
finite-field audits alone, prove the theorem.

## 8. Novelty and remaining obligations

A focused search of reviewed `origin/main` at `4efbbd2` found no copy of this
fixed pair, its two quartic projections, its full-projection obstruction, or
its sharpness fixture.  This establishes repository novelty relative to that
base; it is not a claim of external literature priority.  The package sits on
the corank-two predecessor commit `4a3a098`.

Accepted scoped boundary:

```text
displayed fixed pair has dim B=5:                         PROVED;
actual extension has a rank-at-most-two Phi_k|L_t:        PROVED;
all eight full-projection ranks for this fixed pair:      EXCLUDED;
sharp partial-equation model in low-projection residual:  EXACT;
classification of all dim(B_ab)=5 pair orbits:            NOT PROVIDED;
normalization of arbitrary equality-five pair:            NOT PROVIDED;
low-projection residual:                                  OPEN;
unrestricted P_6 -> Delta_3:                              UNKNOWN;
arbitrary-order permanent nonrestriction:                 UNKNOWN;
global Krenn--Gu conjecture:                               UNRESOLVED.
```

Any integration that treats this theorem as a new live frontier node must
update the canonical frontier/navigation artifacts under the repository
contract.  This hostile-review document does not itself broaden the theorem's
scope or discharge those integration obligations.

## Final reviewed hashes

```text
theorem:
727F39246FA64C899D1F51377FCB3C58640174C044510F727C796C888798F7C2

primary verifier:
7975FF892EE6A1FC4CB0CA12FA02D426AD25E60FBCB9AA88CF2874D605B600B0

independent audit:
AF66CD5BA787B80BC96F5C33316DC0A6CEAA7233DAC4B8D2D48159884E2A6C2B
```
