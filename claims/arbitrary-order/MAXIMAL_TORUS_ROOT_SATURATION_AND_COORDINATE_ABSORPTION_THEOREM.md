# Maximal torus-root saturation and coordinate absorption theorem

## Status

This is an exact global structural reduction over `C` for every hypothetical
ternary Krenn--Gu witness at even order `n>=6`.

Choose a maximum-cardinality set of fully supported local vectors whose
internal evaluated edges all vanish.  The theorem proves pointwise that every
outside vertex is then a blocker for at least one colour.  Either the maximum
has one root, in which case every physical edge block is a single matrix
monomial and a forbidden coefficient requires additional word-compatible
matchings whose symmetric differences contain alternating cycles, or it has
at least two roots and the original tensor equality becomes one exact
blocker-admissible principal-hafnian-deck identity.

The theorem also absorbs the formerly open coordinate-monomial branch of the
two-residual cell: promoting one residual root turns the other residual into
a blocker and produces two overlapping surplus-two blocker identities.
This is absorption into the deeper-blocker branch, not an exclusion.

The unsynchronized surplus-two identities, higher surplus, and the monomial
cancellation branch remain open.  No complete proof or counterexample is
claimed; the global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Maximum torus-root configurations

Let `Omega` be the vertex set and let every local space be `C^3`.  Write
`B_uv` for the physical bilinear block on the edge `{u,v}`.  A **torus-root
configuration** is a pair

```text
(R,(x_i)_(i in R)),

R subset Omega,        x_i in (C^*)^3,
B_ij(x_i,x_j)=0        for all distinct i,j in R.     (1)
```

Choose such a configuration with maximum cardinality `r=|R|`.  This means
maximum over both the vertex set and all choices of its torus vectors, not
merely inclusion-maximal for one fixed choice.  Every singleton is a
configuration, so `r>=1`.

### Lemma 1 (the maximum root set is proper)

One has `R != Omega`.

### Proof

Suppose instead that `R=Omega`.  Leave one vertex `v` open and contract every
other vertex against its `x_i`.  In any perfect matching, `v` meets one root
`j`; the other `n-2>=4` roots contain an internal matching edge, whose value
is zero by (1).  Hence the contracted graph tensor is the zero covector at
`v`.

The contracted GHZ covector has coordinate-`c` component

```text
product_(i in Omega-{v}) x_i[c],                      (2)
```

which is nonzero for every `c`.  This contradicts the tensor equality.
Notice that scalar evaluation at all the `x_i` would not suffice: three
nonzero complex GHZ products could cancel.  The open-slot argument proves the
required covector contradiction.

For each outside vertex `u`, define

```text
a_(i,u)(z)=B_iu(x_i,z),
A_u=span{a_(i,u):i in R} subset (C^3)^*,
K_u=A_u^perp,
B_c={u in Omega-R:e_c^* belongs to A_u}.              (3)
```

The root slot in `a_(i,u)` is filled by `x_i` irrespective of the numerical
order of the vertex labels.  This is the blocker convention used throughout
the owning arbitrary-order claims.

### Theorem 2 (pointwise maximal-root saturation)

Every outside vertex blocks at least one colour:

```text
Omega-R = B_0 union B_1 union B_2.                    (4)
```

### Proof

Suppose `u` belongs to no `B_c`.  Then `K_u` is nonzero: otherwise
`A_u=(C^3)^*` contains every coordinate covector.  Moreover

```text
K_u subset ker(e_c^*)  iff  e_c^* belongs to A_u,     (5)
```

so `K_u` is contained in none of the three coordinate hyperplanes.  The
three proper subspaces `K_u intersect ker(e_c^*)` cannot cover `K_u` over the
infinite field `C`.  Choose

```text
z_u in K_u intersect (C^*)^3.                         (6)
```

Every evaluated edge from an old root to `u` vanishes, so adjoining
`(u,z_u)` produces a larger torus-root configuration.  This contradicts the
maximum-cardinality choice.

This is a pointwise statement at the hypothetical witness.  It uses no
generic fiber, closure, specialization, or projective-to-torus inference.

## 2. The saturated principal-hafnian layer

Assume now that `r>=2`, and put

```text
B=Omega-R,          |B|=r+s,
s=n-2r.                                                (7)
```

Every root coordinate is nonzero, so the blocker lower bound in
[`MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md`](MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md)
applies separately to all three colours:

```text
|B_c|>=r.                                             (8)
```

In particular `|B|>=r`, so `s>=0`; since `n` is even, `s` is even.

There are in fact at least five outside modes.  Choose any root pair.  The
pointwise
[`FOUR_BLOCKER_IDEAL_OBSTRUCTION.md`](FOUR_BLOCKER_IDEAL_OBSTRUCTION.md)
supplies five distinct blockers outside that pair.  No other root `j` is one
of these pair-blockers: its torus vector `x_j` lies in both pair kernels, so
membership of any `e_c^*` in the two-row span would force `x_j[c]=0`.
The five blockers therefore lie in `B`.  Hence

```text
|B|>=5,
r=2  => s>=4,
r=3 or 4 => s>=2,
s=0 => r>=5.                                         (9)
```

Only the pointwise five-blocker statement is used.  No rank hypothesis on an
internal physical root block is inserted.

For `u in B`, leave `z_u` free and write the root-incidence column

```text
H_u[i,-]=B_iu(x_i,-),          i in R.                (10)
```

For an `r`-set `T subset B`, let `P_r(H_u:u in T)` be the permanent tensor of
the `r x r` root-incidence matrix.  For an even set `S subset B`, let `H_S`
be the physical perfect-matching tensor of the graph induced by `S`, with
`H_empty=1`.

### Theorem 3 (maximal-root principal-hafnian identity)

The original tensor equality contracts exactly to

```text
sum_(S subset B, |S|=s)
  H_S tensor P_r(H_u:u in B-S)
 = sum_(c=0)^2 X_c product_(u in B) z_u[c],           (11)

X_c=product_(i in R) x_i[c] != 0.
```

Thus every witness with `r>=2` supplies one complete physical principal
hafnian layer at the fixed order `s`, with all members coming from the same
outside block graph.

### Proof

Contract the roots against their `x_i` and classify a perfect matching by the
outside vertices used by the roots.  An internal root edge has value zero, so
the roots must match injectively to an `r`-set `B-S`.  Their bijections give
the permanent tensor `P_r`.  The unused set `S` has size `|B|-r=s` and is
perfectly matched internally, giving `H_S`.  Conversely one root bijection
and one perfect matching of `S` reconstruct one perfect matching of `Omega`.
The correspondence preserves products and multiplicities, proving (11).
The contracted GHZ tensor supplies its displayed right side.

This matching partition is the `Q=empty` specialization of the bookkeeping
in
[`TWO_PORT_SEVEN_BLOCKER_REDUCTION.md`](TWO_PORT_SEVEN_BLOCKER_REDUCTION.md)
and is compatible with
[`MIXED_ROOT_DELETION_FILTRATION_AND_HERALD_FREE_PAIR_NO_GO.md`](MIXED_ROOT_DELETION_FILTRATION_AND_HERALD_FREE_PAIR_NO_GO.md).
The new step is that maximum-cardinality saturation forces the formula for
every hypothetical witness on the `r>=2` branch.  Equation (11) is a complete
fixed-order layer, not the complete even tower exposed by the separate
balanced half-sensor theorem.

The first three surplus levels are

```text
s=0:  P_r(H_u:u in B) = weighted Delta_3;

s=2:  sum_(u<v in B)
        B_uv tensor P_r(H_w:w in B-{u,v})
      = weighted Delta_3;

s>=4: one higher physical principal-hafnian layer.    (12)
```

The direct pair blocks in the `s=2` line are not automatically common
two-row permanental channels.

### Incidence and corank bounds

Put

```text
I_u={c:e_c^* belongs to A_u},
t_j=number of u in B with |I_u|=j,       j=1,2,3.     (13)
```

Saturation makes `t_1+t_2+t_3=r+s`, while (8) gives

```text
t_1+2t_2+3t_3=sum_u |I_u|>=3r.                       (14)
```

Elementary elimination yields

```text
2t_1+t_2<=3s,
t_3-t_1>=r-2s.                                       (15)
```

The row span of `H_u` is `A_u`, and the coordinate covectors in `I_u` are
independent.  Therefore

```text
sum_(u in B) (3-rank H_u)
 <= sum_u (3-|I_u|)
 =2t_1+t_2
 <=3s.                                               (16)
```

In particular at least `max(0,r-2s)` outside modes are triple, rank-three
blockers.  These conclusions are for `r>=2`.

## 3. The maximum-one monomial branch

Suppose `r=1`.  If an edge block `B_uv` had a zero at a pair of torus vectors,
those two vertices would form a torus-root configuration, contradicting
maximality.  Hence every bilinear polynomial `B_uv(x,y)` is zero-free on
`(C^*)^3 x (C^*)^3`.

In the Laurent coordinate ring

```text
C[x_0,x_0^(-1),...,x_2,x_2^(-1),
  y_0,y_0^(-1),...,y_2,y_2^(-1)],                    (17)
```

the weak Nullstellensatz makes a zero-free regular function a unit.  Laurent
units are scalar monomials, and bilinearity forces

```text
B_uv(x,y)=lambda_uv x[a_uv] y[b_uv],
lambda_uv != 0.                                      (18)
```

Thus every physical block has exactly one nonzero matrix entry.

For each target colour `c`, its nonzero pure coefficient supplies a perfect
matching `M_c` all of whose entries are `(c,c)`.  The three selected matchings
are physically edge-disjoint, because one matrix-unit block cannot support
two different diagonal labels.  The nonmonochromatic-matching theorem used
in
[`UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md`](UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md)
gives a nonmonochromatic perfect matching `F` in their three-coloured union
when `n>4`.

The matching `F` has a compatible nonconstant vertex word and a nonzero
coefficient monomial.  The target coefficient of that word is zero, so at
least one further compatible physical perfect matching must contribute and
the complete coefficient sum must cancel.  For any such second matching
`F'`, the nonempty symmetric difference `F triangle F'` is a union of
word-preserving alternating even cycles.

This is an exact cancellation obligation, not a contradiction and not a
claim of two-term cancellation.  It does not place the witness in the
stronger simultaneous balanced all-bridge normal form without another
theorem.

## 4. Coordinate two-residual absorption

Now start from the exact two-residual cell of
[`TWO_RESIDUAL_NONBLOCKER_TWO_PORT_FACTORISATION.md`](TWO_RESIDUAL_NONBLOCKER_TWO_PORT_FACTORISATION.md):

```text
|R|=r>=2,      |B|=r+2,      Q={q0,q1},              (19)
```

where the roots are fully supported and pairwise zero-coupled, `B` is the
entire blocker union, and `q0,q1` block no colour.  Put

```text
K_j=intersection_(i in R) ker B_(i,qj)(x_i,-),
beta=B_(q0,q1) restricted to K_0 x K_1.              (20)
```

Both kernels contain torus vectors.  When `r=2`, the four vertices in `B`
would be the complete blocker union for a fully supported zero root pair,
contradicting the pointwise five-blocker theorem.  Hence every surviving cell
under the stated `r>=2` hypothesis has `r>=3`.

### Theorem 4 (noncoordinate two-root promotion)

If `beta` is not a nonzero coordinate monomial, including `beta=0`, choose
torus vectors `z_j in K_j` with

```text
beta(z_0,z_1)=0.                                      (21)
```

Then `R union {q0,q1}` is a torus-root configuration.  The old blockers
remain blockers because their root-row spans only grow.  The new root set and
the outside set `B` both have size `r+2`, so the tight matching identity is

```text
P_(r+2) -> weighted Delta_3.                          (22)
```

This is the existing torus-zero extraction, now expressed as root promotion.
For original `r=3,4,5` it gives `P_5,P_6,P_7`, respectively.  It remains a
restriction, not a nonrestriction theorem.

### Theorem 5 (coordinate one-root absorption)

Suppose instead that, on the two kernel spaces,

```text
beta(z_0,z_1)=kappa z_0[c] z_1[d],    kappa!=0.       (23)
```

Choose any torus `z_0 in K_0`, promote `q0`, and put

```text
g=B_(q0,q1)(z_0,-),
A'_1=A_(q1)+span(g),
K'_1=(A'_1)^perp.                                    (24)
```

On `K_1`, equation (23) says

```text
g=kappa z_0[c] e_d^*.                                (25)
```

Thus `g-kappa z_0[c]e_d^*` lies in `K_1^perp=A_(q1)`, and the nonzero scalar
gives

```text
e_d^* belongs to A'_1.                               (26)
```

The old nonblocker hypothesis says `e_d^*|K_1` is nonzero.  Consequently

```text
g notin A_(q1),
dim A'_1=dim A_(q1)+1,
K'_1=K_1 intersect ker(e_d^*),
dim K'_1=dim K_1-1.                                  (27)
```

In particular, if `K_1` is a line then `K'_1=0` and `q1` becomes a triple,
rank-three blocker.  All old blockers persist.  Relative to the promoted
root set and outside blocker set

```text
R'=R union {q0},      B'=B union {q1},
|R'|=r+1,             |B'|=r+3=|R'|+2,              (28)
```

the exact full tensor is therefore the physical, generally unfactorized

```text
Lambda_(r+1,2)
 = sum_(u<v in B')
     B_uv tensor P_(r+1)(H'_w:w in B'-{u,v})
 = weighted Delta_3.                                 (29)
```

Here `H'` is the incidence matrix of the promoted root set.  Thus `Lambda`
is only a name for the displayed physical principal two-vertex layer, not an
assumption that its direct blocks factor through two common rows.

Choose separately a fresh torus vector in the **original** `K_1` and promote
`q1` instead.  The symmetric argument gives a second overlapping
`Lambda_(r+1,2)` identity on `B union {q0}`.  It is not an iteration from the
shrunken kernel `K'_1`: that kernel lies in `ker(e_d^*)` and has no torus
point.

The derivation of (15) uses only full outside blocker saturation and the
multi-star lower bound, not maximality itself.  It therefore applies to
either promoted cell.  Its new root count is `r+1` and its surplus is two, so

```text
t_3-t_1>=r-3,          2t_1+t_2<=6.                  (30)
```

Thus an original five-root coordinate cell yields two overlapping
`Lambda_(6,2)` identities, each with at least two triple blockers.

The resulting low-root staircase is

```text
original r     noncoordinate branch     coordinate branch
3              P_5                      Lambda_(4,2)
4              P_6                      Lambda_(5,2)
5              P_7                      Lambda_(6,2).              (31)
```

## 5. Exact frontier and provenance

The synchronization obstruction is real.  In the surplus-two identity, the
pair cofactor is a direct physical block `B_uv`, which can have rank three.
A common two-row channel `a_u b_v+b_u a_v` has rank at most two.  The exact
top-observability analysis in
[`GRAPH_EXTRACTION_TOP_TWO_PORT_SYNCHRONIZATION_OBSERVABILITY_BOUNDARY.md`](GRAPH_EXTRACTION_TOP_TWO_PORT_SYNCHRONIZATION_OBSERVABILITY_BOUNDARY.md)
does not force the former to be the latter.  The full diagonal aggregate may
impose additional relations, but no current theorem proves the required
synchronization.

```text
maximum torus-root set is pointwise blocker-saturated: PROVED;
universal r=1 versus saturated-deck dichotomy:          PROVED;
fixed surplus-s principal-hafnian layer:                PROVED;
five-outside-mode and incidence/corank bounds:          PROVED for r>=2;
r=1 one-matrix-unit classification:                     PROVED;
r=1 forbidden-word cancellation obligation:            PROVED, NOT EXCLUDED;
noncoordinate two-residual root promotion:              EXACT, EXISTING BRIDGE;
coordinate one-root absorption into Lambda_(r+1,2):     PROVED;
two overlapping promoted identities:                    PROVED;
surplus-two synchronization:                            UNKNOWN;
higher-surplus exclusion:                               UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

The genuinely new global mechanism is maximum-root saturation and its
unconditional trigger of the existing matching ledger.  The blocker lower
bounds, two-residual torus-zero dichotomy, noncoordinate permanent
extraction, and Bogdanov matching input retain their prior provenance.

## Focused checks

Run from repository root:

```text
python claims/arbitrary-order/verify_maximal_torus_root_saturation_and_coordinate_absorption.py
python claims/arbitrary-order/audit_maximal_torus_root_saturation_and_coordinate_absorption.py
```

The primary check compares the fixed-surplus matching formula as an exact
sparse polynomial through ten vertices, checks the incidence inequalities,
and checks rational coordinate-promotion charts.  The independent no-import
audit constructs the labelled matching bijection directly and uses a separate
exact row-reduction implementation for the promotion kernels.  These bounded
checks audit indexing and linear algebra only.  The arbitrary-order proofs
are the written maximum-root, matching-bijection, and duality arguments above.
