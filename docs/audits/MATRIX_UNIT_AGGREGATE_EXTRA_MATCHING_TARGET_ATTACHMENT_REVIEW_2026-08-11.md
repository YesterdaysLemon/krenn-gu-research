# Hostile review: aggregate extra-matching target attachment

Date: 2026-08-11

Reviewed artifact:

[`../../claims/arbitrary-order/MATRIX_UNIT_AGGREGATE_EXTRA_MATCHING_TARGET_ATTACHMENT_THEOREM.md`](../../claims/arbitrary-order/MATRIX_UNIT_AGGREGATE_EXTRA_MATCHING_TARGET_ATTACHMENT_THEOREM.md)

Review disposition: **PASS at the stated offdiagonal-extra attachment,
shortest-cycle boundary, and fixed-family sharpness scope**.

The Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Exact obligation under review

`U7J` proves

```text
H=(-1)^m product_i(1+A_i)
```

for aggregate active-cycle fibres, but does not relate the extra matching
terms to target equations away from the selected cycle.  The pure-side node
`U7I` separately classifies a least cancelling shore as a primitive cycle,
sparse conformal fan, or nonzero aggregate port.  No theorem connected those
two structures.

The reviewed checkpoint claims:

1. a zero residual shore of one offdiagonal extra matching contains a
   **conformally minimal** connected matching-covered residual;
2. every matching term of its primitive-cycle/fan/aggregate-port relation
   extends by fixed edges into the same mixed target fibre, preserving exact
   incidence differences;
3. if the source shores are nonzero, bridge normalization gives the deeper
   branch, the same pure attachment at the bridge word, or an active complete
   target equation;
4. on a shortest transport cycle, an active bridge word is outside the cycle
   or is the selected successor; and
5. the parallel-successor survivor is exact and sharp even with all three
   pure target coefficients one.

The theorem explicitly leaves purely diagonal aggregate excess, universal
unit forcing, the deeper branch, and the global conjecture open.

## 2. Adversarial proof checks

### 2.1 Does a conformally minimal residual always exist?

Yes.  The original cancelling shore `S` is itself admissible: it has zero
hafnian and a support perfect matching supplied by the extra full matching,
while its complement in itself has the empty perfect matching.  A
least-cardinality admissible subset therefore exists in the finite shore.

### 2.2 Is conformal minimality really enough for the allowed-core identity?

Yes.  If an allowed edge `uv` had zero complementary hafnian, then
`R-{u,v}` would still have a support perfect matching.  Its complement in the
original shore would be matchable by the fixed matching on `S-R` together
with `uv`.  It would be a smaller conformally admissible zero, a
contradiction.  Thus every allowed edge has nonzero first cofactor.

The converse is standard and exact: a nonzero first cofactor contains a
support complement matching, so adjoining its edge gives a full matching.
No numerical genericity is used.

### 2.3 Does connectedness follow under the weaker minimality?

Yes.  Perfect matchings factor across components of the allowed graph.  If
the full hafnian is zero, one component hafnian is zero.  Every other
component and the fixed matching on `S-R` supplies a matching of its
complement in `S`, so a vanishing proper component would again contradict
conformal minimality.

Support edges that occur in no full perfect matching do not affect the
factorization.  If a cross-component edge did occur in a perfect matching,
it would be allowed and would join the components.

### 2.4 Why is minimum degree at least two?

The allowed graph covers every vertex because it contains a perfect
matching.  Every allowed incident edge has nonzero first cofactor.  Hafnian
Laplace expansion at a vertex sums those cofactors to the zero residual.  A
single nonzero term cannot sum to zero, so degree one is impossible.

### 2.5 Are the imported pure normal forms used within their hypotheses?

Yes.  The reviewed proof reconstructs exactly the properties used in the
owning `U7H`/`U7I` arguments: the active graph equals the allowed graph, is
connected and matching-covered, has minimum degree at least two, and every
allowed-edge cofactor is nonzero.  The subsequent alternating-cycle,
port-partition, singleton-port fan, and aggregate-port arguments are purely
matching-theoretic.  No global least-residual claim is imported silently.

Characteristic two is excluded from the signed relation interpretation, as
in the owning port theorem.  The matrix-unit application is over `C`.

### 2.6 Is the pure-to-mixed attachment only physical-variable overlap?

No.  Fixing a complement matching `C` and all outer edges `K` sends every
residual matching `M` to `K union C union M` in one mixed fibre.  For any two
terms, the common incidence vector cancels:

```text
1_(K union C union M)-1_(K union C union N)=1_M-1_N.
```

The relation's exact exponent characters therefore occur inside the mixed
fibre lattice.  The common nonzero monomial also factors from the weighted
sum.  This is stronger than saying the constructions reuse edge variables.

### 2.7 Is the embedded pure subrelation a universal target-ideal generator?

No, and the artifact says so.  The shore hafnian is zero at the hypothetical
witness on the selected cancellation branch.  Its extended sub-sum is an
exact branch equation and a termwise part of the complete fibre.  The proof
does not claim that this subpolynomial belongs to the target ideal at every
point of the fixed label-support torus.

This boundary is important: the attachment alone does not make the global
target ideal a unit.

### 2.8 Is every extra matching covered?

Only every extra matching with a **nonempty offdiagonal core**, exactly as
stated.  Purely diagonal extra matchings do not enter bridge normalization
and remain a separate aggregate-excess branch.  The theorem does not infer
that every aggregate fibre contains an offdiagonal extra.

### 2.9 Why is the source/deeper/target decision exhaustive?

For `X=E union P_0 union P_1 union P_2`, either some residual shore hafnian
vanishes or all are nonzero.  The first case gives source attachment.  In the
second, `E` is cofactor-active and the imported square/hexagon theorem gives
deeper data or a nonzero diagonal bridge matching.

At the bridge word, either its diagonal aggregate is zero or nonzero.  A zero
product contains a zero shore with an explicit nonzero matching term and
gives target attachment.  A nonzero product, together with the complete
mixed target equation, forces equal-and-opposite nonzero offdiagonal
response.  There is no omitted scalar case.

### 2.10 Does the target word remain mixed?

Yes.  Bridge normalization preserves all three colour multiplicities.  It
changes a nonempty endpoint set, but the original active word is mixed, so
the target word remains mixed and its GHZ coefficient is required to vanish.

### 2.11 Is shortest-cycle minimality used correctly?

Yes.  An extra active arc from `chi_i` to another vertex `chi_j` of the
selected cycle, followed by the selected path from `chi_j` back to `chi_i`,
is a directed cycle.  It is shorter unless `j=i+1` cyclically.  The bridge
word cannot equal `chi_i` because the nonempty core changes every bridge
endpoint.  Thus the only on-cycle survivor is the selected successor.

The proof does not claim that an outside target eventually gives a shorter
cycle or a unit.

### 2.12 Does parallel transport force cross-fibre lattice overlap?

No.  The exact within-fibre vectors are

```text
u=1_X-1_F,
v=1_Y-1_G.
```

The sharpness family has `Y=G`, hence `v=0` while `u` is a nonzero primitive
four-cycle difference.  The successor fibre contributes no new direction
from this rectangle.  This refutes the stronger inference despite literal
reuse of the same physical matching.

### 2.13 Is the ten-vertex table complete and locally concise?

Yes.  The table assigns one nonzero matrix unit to all `45` physical pairs.
At every endpoint, the incident labels are exactly `{0,1,2}`.  The excluded
parameter divisors `t=0` and `1+t=0` are exactly those making the extra edge
weight or selected edge weight zero.

The primary verifier checks the set of all 45 pairs and every local label
set.  The independent audit rebuilds the literal table separately and makes
the same checks.

### 2.14 Are the `3/2/2` fibres complete?

Yes.  Both checkers enumerate all `9!!=945` perfect matchings.  The first
cycle word has exactly the selected outgoing term of weight `-(1+t)`, the
parallel extra of weight `t`, and the incoming diagonal term of weight one.
The other two fibres are the displayed `1,-1` binomials.  Their sums vanish
identically.

The custom-polynomial no-import audit groups all matchings by their full
ten-label words and confirms that these are the only identically zero
nonempty fibres of the family.

### 2.15 Are the pure target equations actually satisfied?

Yes.  Each constant word has exactly one compatible matching, and each has
weight one:

```text
0^10: 09|17|26|38|45,
1^10: 08|19|23|46|57,
2^10: 05|16|28|39|47.
```

This strictly strengthens the earlier `U7J` sharpness family, whose pure
coefficients were all zero.  It still does not satisfy the full mixed target.

### 2.16 Is the claimed completion minimality global?

No.  It is correctly limited to completing the fixed eight-vertex parallel
`3/2/2` template.  On those eight vertices, every `22` edge must avoid all
cycle terms.  The eight unused pairs have vertex `2` and vertex `4` both
forced to neighbour `7`, so they contain no perfect matching.  The pure-2
anchor cannot be restored at order eight without changing the template.

Order must remain even, so two new vertices are necessary; the ten-vertex
table proves they are sufficient.  No global smallest-support claim is made.

### 2.17 Is the holonomy elimination exact?

Yes.  The selected subsystem is

```text
1+x+t=0,
Hx-1=0.
```

It maps to `Q(t)` by `x=-(1+t)` and `H=-1/(1+t)`.  A nonzero Laurent
polynomial in `H` cannot vanish after substituting this nonconstant
transcendental rational function.  The three pure equations are satisfied
identically throughout the same one-parameter family, so adjoining them
cannot create an `H`-only polynomial on this family.

The primary checker finds no `H`-only polynomial in the exact lexicographic
basis.  The independent audit verifies the triangular independence of
`(-1)^k(1+t)^(d-k)` through degree eight with its own rational row reduction;
the written distinct-degree argument covers every degree.

### 2.18 Is the family an apparent counterexample?

No.  The mixed word `0011111122` has the unique compatible matching

```text
01|23|46|57|89
```

of weight one.  Its target-zero equation is a Laurent unit.  Thus the full
target ideal of this fixed support is `(1)`, and the table transparently
fails the original target tensor.

This is both a safety check and useful evidence: in this family an equation
outside the cycle does exactly supply the desired unit, but the theorem does
not generalize that occurrence without proof.

## 3. Evidence independence

The primary verifier uses:

- recursive first-vertex matching enumeration;
- exact SymPy polynomial/rational arithmetic;
- all `945` physical perfect matchings;
- exact pure-shore hafnians and endpoint characters;
- a lexicographic Groebner check;
- conformally minimal cycle, `K_4` fan, and `K_(3,3)` aggregate fixtures; and
- an explicit unused-edge perfect-matching obstruction at order eight.

The independent audit imports neither the primary verifier nor SymPy.  It
uses:

- 45-bit physical edge masks;
- custom exact coefficient-tuple addition and multiplication;
- a separate last-vertex pure-matching recursion;
- different numerical weights for all three conformal residual fixtures;
- exact Gaussian rank of triangular substitution matrices; and
- a separately hard-coded order-eight unused graph.

The two scripts share only the mathematical table and the claims they must
check.  Their matching representations, polynomial implementations, pure
fixtures, and elimination audits are distinct.

The arbitrary-order statements are the written conformal-minimality,
termwise-completion, bridge, target-equation, and shortest-cycle proofs.  The
finite scripts audit mechanisms and sharpness; they are not an exhaustive
arbitrary-order support census.

## 4. Remaining boundary

The checkpoint leaves open:

- aggregate cycle fibres whose extra terms are all diagonal;
- whether an attached primitive cycle or fan/port relation forces an odd
  dependency, unit, or killed quotient sheet;
- whether every outside active target equation yields useful non-direct
  cross-multiplicity overlap;
- parallel successor pairs when the two successor terms are distinct;
- forced singleton or other unit certificates for arbitrary supports;
- the deeper-blocker branch;
- exclusion of the complete nonzero `r=1` matrix-unit branch; and
- the global conjecture.

Physical-variable overlap, cycle length, and pure-anchor normalization alone
remain insufficient.

## 5. Verdict

The theorem is accepted as an exact offdiagonal-extra attachment result and
as a sharp correction to the stronger shortest-cycle proposal.  It genuinely
couples conformally minimal pure residual characters to mixed response when a
source or bridge shore cancels.  Otherwise it forces deeper data or another
active complete target equation, with the exact parallel-successor survivor
isolated.

The ten-vertex family validates that survivor at the pure-anchor level and is
independently excluded by a singleton mixed equation.  No complete proof or
counterexample follows.

The global Krenn--Gu conjecture remains **UNRESOLVED**.
