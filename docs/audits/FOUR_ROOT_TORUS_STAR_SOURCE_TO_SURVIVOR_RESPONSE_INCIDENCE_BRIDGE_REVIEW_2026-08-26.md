# Review: source-to-survivor response-incidence bridge

Date: 2026-08-26

## Verdict

Accept `GLD81` as an **exact forward source-interface bridge and conditional
principal-open exclusion** for the named root-order-four, surplus-two,
fully-supported, rank-three, nonisotropic maximal-star source branch.

An actual GHZ graph presentation on that branch supplies one physical raw
coefficient vector and one legal `17 x 3` lift satisfying the complete
denominator-free incidence used by `GLD80`.  Thus `GLD80` excludes this
physical source branch whenever at least one induced normalized survivor
frame lies in its principal open `D(delta)`.

The theorem does not compute `delta`, cover `V(delta)`, prove source
integrability of arbitrary nuisance tensors, exhaust other components or
gauges, force the named source branch, or resolve Krenn--Gu.  The global
conjecture remains **UNRESOLVED**.

## Proof bridge audited

The source coefficient and response equations are both partitions of the
same ten-mode perfect-matching formula.

1. Maximum-root zeroes remove every matching containing a root--root edge.
   Each of the remaining `360` matchings pairs all four roots outside and
   therefore contains exactly one outside--outside edge.  The fifteen such
   edge classes give the physical `1+24+54=79` raw coordinates and
   `b alpha=T(F)`.
2. Partitioning those same matchings by the neighbor of `q_0` gives thirteen
   constant response coordinates and four root-response coordinates.  Every
   physical local response factors through this complete `17`-coordinate
   domain.  This is not a claim that a three-dimensional local response map
   has rank `17`.
3. For the fixed-coordinate GHZ target, the three vectors
   `y_c=z_0[c]e_(q_0,c)` produce exactly the three demanded diagonal
   summands.  Their incident-edge evaluations form the physical lift `L`.
4. The `GLD80` port-frame intertwiners then send
   `beta=S_F alpha` and `L'=J_F L` to the literal-diagonal incidence.  No
   converse source-integrability claim is used.

The raw-coordinate convention was checked explicitly.  A physical
`q_0`--port edge leaves `q_1` in the complementary root permanent and is the
`h_eta` family; a `q_1`--port edge similarly belongs to `h_xi`.

## Hostile-review repairs

The first review rejected a broad covariance sentence.  Root and residual
normalizations are not contained in the `GLD80` matrix `J_F`.  The accepted
proof instead rebuilds the physical nuisance map, response map, raw vector,
and incident-evaluation map after canonical normalization.

For root gauges `x_i |-> d_i x_i`, with `d=product_i d_i`, the constant
response block scales by `d`, the `i`-th root column by `d/d_i`, and its
physical incident coordinate by `d_i`.  Every response term and the
grade-zero contraction therefore scale by the same `d`.  For residual gauges
`(z_0,z_1) |-> (a z_0,c z_1)`, the four raw blocks scale by
`(ac,a,c,1)`, while both the grade-zero coefficient and response at `a y`
against `c z_1` scale by `ac`.

Only after this rebuilt physical presentation is formed does the proof use
the exact `GLD80` covariance

```text
U_F b=b_F S_F,
U_F D_q0(alpha)=D'_(q0,F)(S_F alpha)J_F.
```

The orientation `L'=J_F L` is load-bearing and was rechecked.  Arbitrary GHZ
stabilizers are not asserted to preserve the source interface.  A permutation
or diagonal rescaling of the three displayed summands merely right-multiplies
both `R` and `L` by the same invertible monomial matrix.

Further repairs fixed the target-coordinate convention, restated the
weighted-matching source model, recorded the `h_eta/h_xi` crosswalk, replaced
ambiguous “17 directions” language, and restricted the residual list to a
proof-tree cover relative to the named root-order-four program.

## Computational evidence

The primary verifier replays the complete `GLD80` interface and
principal-open theorem, enumerates all `945` perfect matchings, checks the
`360` surviving matchings and fifteen raw-edge classes, verifies the
`h_eta/h_xi` complementary labels, checks the `13+4=17` response partition,
and replays exact target and gauge scaling identities.

The standard-library no-import audit independently reconstructs the finite
matching partition using a bitmask recurrence, checks the complementary
residual labels, the complete response-label census, and exact target and
source-gauge scalings.  The arbitrary-source quantifier and the multilinear
coefficient equalities are carried by the written matching proof.  The audit
does not independently reconstruct every symbolic `GLD70` column or the
upstream `GLD80` intertwiners.

## Load-bearing limits and successor

The source branch hypotheses remain assumptions: lower port rank, fewer base
survivors, the maximal triangle, residual-coordinate boundaries, isotropic
slopes, other survivor gauges/components, `V(delta)`, and other root/surplus
profiles remain open.

The highest-value successor is an explicit strict-closure image computation
over the survivor base: exhibit a certified `delta` nonzero at `GLD72`, or a
finite named Fitting/divisor cover, while retaining projective saturation,
rank-drop fibres, chart determinants, and every zero denominator as a residual
branch.  `GLD81` then immediately promotes that survivor exclusion to the
named physical source branch.
