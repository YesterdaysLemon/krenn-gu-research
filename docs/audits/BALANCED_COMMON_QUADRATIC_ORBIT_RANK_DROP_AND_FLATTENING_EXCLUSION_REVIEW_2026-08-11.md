# Hostile review of the common-quadratic all-rank-drop exclusion

## Verdict and provenance

**PASS, with the residual boundary kept explicit.**  The owning theorem
proves two independent statements about the vertex-gauge common-quadratic
stratum:

1. from `n=8` onward it lies in every balanced rank-drop locus; and
2. for every Krenn--Gu order `n>=6` it is disjoint from the ternary GHZ
   witness equations by a flattening-rank mismatch.

The proof does not classify `B_all`, force a hypothetical witness into this
stratum, or exclude nonsynchronized edge blocks.  The global conjecture
remains **UNRESOLVED**.

Reviewed candidate:

```text
claims/arbitrary-order/
  BALANCED_COMMON_QUADRATIC_ORBIT_RANK_DROP_AND_FLATTENING_EXCLUSION_THEOREM.md
```

The review reconstructed the mathematics from the written definitions, then
compared the primary SymPy route with the no-import standard-library audit.
The scripts support constants and conventions; they are not the
arbitrary-order proof.

## 1. The synchronization hypothesis is substantive

The theorem assumes one three-dimensional space `V`, one symmetric bilinear
form `q`, and one isomorphism `A_u:L_u -> V` per vertex such that

```text
W_uv(x_u,x_v)=q(A_u x_u,A_v x_v)
```

for **every** incident pair.  The same `A_u` must work simultaneously on all
edges at `u`.  It is not enough that each individual invertible `3 x 3` edge
matrix can be reduced to the identity by a pair of edge-dependent changes of
basis; that observation would be vacuous and would not imply the theorem's
sensor covariance or flattening normal form.

The proof and frontier wording retain this as a synchronized stratum.  No
inference from all-balanced rank drop to common-quadratic synchronization is
made.

## 2. Local gauges are not claimed to preserve GHZ

A possible invalid argument would transform the edge blocks to `q`, silently
declare that GHZ is unchanged, and compare coordinate coefficients.  The
owning proof does not do this.  It uses

```text
T_W=(tensor_u A_u^*) H_(2m,q)
```

and only the invariance of bipartite matrix rank under invertible row and
column transformations.  GHZ itself is kept in its original coordinate
bases and has flattening rank three in every nontrivial cut.  Therefore the
independent local gauges need not lie in the GHZ stabilizer.

This also explains why the new result is stronger than checking one explicit
mixed coefficient of the diagonal representative: an arbitrary local change
of basis can destroy coordinate-word sparsity but cannot change flattening
rank.

## 3. Balanced-sensor covariance is pointwise and surjective

For a fixed cut, every root slot in every companion term is pulled back by
the same invertible root map assigned to that slot.  This gives a common
invertible transformation of the sensor's row space, not a different
transformation for each column.

At a contracted nonroot `u`, replacing `z_u` by `A_u z_u` is bijective because
`A_u` is an isomorphism.  Hence a rank bound for every transformed contraction
point is exactly a rank bound for every original contraction point.  The
argument proves identical rank functions under reparametrization; it does
not infer generic rank from one sample.

## 4. Polarization and the common-quadratic subspace

After uniformization, root-slot permutation symmetry is genuine because the
same **symmetric** form `q` occurs on every root-root and root-nonroot edge.
Characteristic-zero polarization therefore recovers the root tensor from its
repeated-root polynomial.

For every companion except the all-cross column, at least one root-root edge
remains.  Its repeated-root factor is `Q(x)=q(x,x)`, so all such columns lie
in

```text
Q Sym^(m-2)(V^*).
```

For nonzero `Q`, polynomial multiplication is injective and this space has
dimension `binomial(m,2)`.  Adding one all-cross column gives the stated
upper bound.  If `Q=0`, symmetry and characteristic zero force `q=0`, making
the bound only easier.  No division by `Q`, nondegeneracy assumption, or
generic contraction is hidden in the rank-drop proof.

At `m=3`, the bound equals four and does not imply rank drop.  The theorem
starts its `B_all` conclusion at `m=4` exactly.

## 5. The six-column flattening certificate is complete

For nondegenerate symmetric `q`, scalar extension and congruence reduce it to
the coordinate dot product without changing rank.  Symmetry of the first two
slots gives the upper bound six.

Three right words with one repeated colour give three diagonal left columns.
After removing the common nonzero factor `(2m-3)!!`, their matrix has diagonal
`2m-1` and off-diagonal `1`.  Its eigenvalues are `2m-2` (twice) and `2m+1`,
all nonzero in characteristic zero.

For each colour pair, a right word with those two colours occurring once and
the remaining colour occurring `2m-4` times isolates the corresponding
symmetric off-diagonal direction with coefficient `(2m-5)!!`.  The six
directions are independent, proving exact rank six rather than only a lower
bound.

The GHZ comparison has rank exactly three because its three pure left tensors
and three pure right tensors are separately independent.  This is a tensor
flattening statement, not a sampled coordinate-coefficient heuristic.

## 6. Degenerate forms and local concision

When `rank(q)<3`, every first-slot covector of the graph tensor lies in the
first-factor image of `q`.  The one-vertex flattening rank is therefore at
most `rank(q)<3`, while GHZ has local rank three.  This covers the degenerate
and zero forms without trying to apply the six-rank calculation to them.

Conversely, nondegenerate `q` gives one-vertex rank three (also checked in
both scripts), so the nondegenerate common-form orbit is locally concise and
has invertible blocks.  The exclusion is not caused by a hidden local-rank
failure there.

## 7. Computational independence and replay meaning

The primary verifier:

- compares all 729 six-vertex coordinate words with the double-factorial
  formula;
- constructs full exact two-flattenings through eight vertices with SymPy;
- verifies the six selected columns and GHZ rank separately;
- builds symmetric companion polynomials and checks ranks through `m=6`; and
- checks one-flattening ranks for diagonal forms of ranks one, two, and three.

The independent audit imports no code from the primary and uses:

- its own recursive matching generator;
- exact `Fraction` row reduction;
- only the six certificate right words, evaluated by direct matching rather
  than the coefficient formula; and
- direct enumeration of crossing roots, bijections, internal root matchings,
  and edge colours before collapsing to sparse diagonal polynomials.

The routes differ in representation and rank implementation.  Their bounded
agreement supports the displayed constants.  Neither script proves the
arbitrary-order theorem by enumeration.

## 8. Acceptance and residual boundary

The accepted proof-topology change is narrow:

```text
common-quadratic local-GL orbit subset B_all:          PROVED for n>=8;
that orbit intersect ternary GHZ witness equations:    EMPTY for n>=6;
arbitrary B_all graph is common-quadratic:              NOT PROVED;
nonsynchronized B_all witness intersection:             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

This justifies a new scoped `S3Q` node and a refinement of the surviving
`S3` obligation.  It does not justify deleting `S3`, changing the global
status, or treating invertibility, local concision, or complete support as a
classification theorem.

## Strongest fresh-referee objection

The most dangerous reading is that “every edge can be put in identity form”
implies the simultaneous representation (1).  It does not: the endpoint
change at a vertex must be shared by all incident edges.  The theorem is
valid precisely because it states and preserves that global synchronization
hypothesis.  The remaining nonsynchronized all-rank-drop locus is still the
load-bearing open branch.
