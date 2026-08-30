# Four-`K5` rank-degeneracy component ledger (working note)

## Status and boundary

**Candidate parent-level argument under hostile review.  Not a theorem.**

This note records a proposed completion of the rank-degeneracy obligation
left open by the
[four-`K5` support-Segre generic-rank census](EIGHT_VERTEX_FOUR_FIVE_SET_PENCIL_SUPPORT_SEGRE_GENERIC_RANK_CENSUS_THEOREM.md).
It separates the mathematical reductions from the current finite evidence so
that neither is silently promoted.

The proposed conclusion is the componentwise envelope inequality

```text
Delta + c_rank + sum_(i<j) r_ij >= 20,                         (1)
```

for the four induced `K5` charts on a fixed labelled common `K4`.  The present
evidence identifies seven candidate equality-component orbits originating at
generic predecessor value at most `22` and gives one full balanced sensor on
each.  A complementary-ruling correction initially exposed a possible
predecessor-`23` equality pattern.  The targeted exact pass now eliminates
that pattern in all `8,882` canonical `q=23` systems: the only eighteen systems
surviving its partition tests have support-forced, hence codimension-zero,
line conditions at both proposed active vertices.  Thus the seven-orbit list
is again a candidate exhaustive list, but only conditional on the charge
argument under hostile review and the pinned finite audits.  Before that review
is complete, (1), the equality classification, and the resulting `B_all` cut
are all **candidate**.

Nothing here proves compatibility among the seventy choices of a four-chart
pencil, imposes every remaining GHZ target equation, excludes a witness, or
resolves Krenn--Gu.  The global conjecture remains **UNRESOLVED**.  Because
this is not an accepted frontier change, `docs/current-frontier.md` is not
changed by this working note.

## 1. Exact obligation inherited from the generic census

Fix one feasible selector/exact-partition system from the predecessor.  At
common vertex `i`, write its distinct partition blocks as `B`, with coordinate
supports

```text
U_(i,B) subset k^3.                                           (2)
```

The exact-partition root base is the open distinct-point locus in

```text
X_i = product_B P(U_(i,B)).                                   (3)
```

Partition coarsenings are not hidden boundary events: they are separate exact
partition systems in the predecessor's exhaustive fifteen-state census.

At an edge `ij`, repeated partition-block pairs are deduplicated.  There are
at most four distinct decomposable evaluation points

```text
x_(i,B_i(t)) tensor x_(j,B_j(t)).                             (4)
```

The predecessor computes their generic rank `rho_ij`.  On a locally closed
root component `Z` inside the exact-partition base, let their actual generic
rank be `r_ij`, and let `c_rank=codim(Z)`.  Equation (1) is precisely the
missing bound.

## 2. Minimal circuits of at most four decomposable tensors

The proposed exhaustion uses the following elementary characteristic-zero
lemma.

Let `a_t tensor b_t`, `t in T`, be distinct projective decomposable tensors
with `|T|<=4`.

1. Two distinct tensors are independent.
2. Three are dependent exactly when they lie on a ruling line of the Segre
   variety: one factor is fixed and the other three factor points span a
   two-dimensional vector space.
3. If four form a minimal circuit, put
   `r=dim span{a_t}` and `s=dim span{b_t}`.  A full-support relation gives
   orthogonal row spaces in `k^4`, hence `r+s<=4`.  Minimality leaves
   `(r,s)=(1,3),(2,2),(3,1)`.  The `(1,3)` and `(3,1)` cases are fixed-factor
   span relations.  In the `(2,2)` case the four Segre points lie in a plane
   section of the smooth quadric `P^1 x P^1`.  That section is either an
   irreducible `(1,1)` conic, giving the labelled cross-ratio divisor when all
   endpoint factors are distinct, or the union of one ruling of each type.
   In the reducible case a minimal four-circuit can have complementary
   repeated factor pairs (for example `a_0=a_1` and `b_2=b_3`).

For item 2, a projective line meeting the Segre variety in three points lies
in every defining quadric and hence is a Segre ruling.  For item 3, if `A`
and `B` are the two factor matrices and `D` is the nonzero diagonal of
relation coefficients, then

```text
A D B^T = 0,                                                  (5)
```

so `row(A)` is orthogonal to `D row(B)`.  In the all-distinct `(2,2)` chart,
the determinant of the four columns `(1,b_t,a_t,a_t b_t)` is the single
labelled cross-ratio equation.  If a factor repeats, the plane contains its
ruling line; the residual plane-section ruling gives the complementary repeat
pattern above.

The repeat pairs of a reducible ruling-pair circuit are fixed by the two exact
endpoint partitions.  If both endpoint spans are already two-dimensional,
the circuit is present in the predecessor's generic rank `rho_ij`.  More
generally, a three-block partition of type `0012` has generic span three; a
line event lowers it to two.  Complementary repeated pairs such as `0012` and
`0122`, together with line events at both endpoints, then create a new
active--active ruling-pair circuit inside the fixed exact-partition stratum.

Consequently a rank decrease inside a fixed exact-partition stratum can only
come from:

- a collinear triple of distinct block points at one common vertex;
- all four distinct block points lying on one projective line (the
  intersection of two distinct triple events is included here); or
- a complementary-ruling joint circuit between two line-valued three-block
  vertices whose repeated chart pairs are complementary; or
- a labelled cross-ratio equality between two four-distinct line-valued
  vertices.

Structural fixed-factor and complementary-ruling circuits may already lower
`rho_ij`; the event ledger begins from that exact predecessor rank and charges
only a further decrease inside the fixed stratum.  The joint ruling event in
the preceding bullet is required precisely when the complementary repeat
pattern is structural but its two endpoint line conditions are not.

Each edge loses **at most one** relative to its predecessor rank.  Indeed, the
deduplicated edge set contains at most four distinct projective Segre points.
Two distinct points are independent.  The only possible loss of at least two
would therefore be `rho_ij=4` specializing to rank at most two.  Rank one is
impossible, while rank two would put at least three distinct Segre points on a
projective line.  Such a line is a Segre ruling, so one endpoint factor is
fixed on the entire deduplicated edge set.  That fixed block-pair pattern is
structural in the exact partitions, and its predecessor rank is already at
most three, contradicting `rho_ij=4`.  This proves the claimed one-step bound
without a numerical genericity assumption.

No numerical rank observation is used to enlarge the circuit list or prove
the one-step bound.

## 3. Coordinate-support line strata and their codimension

For a set `S` of three distinct blocks, or all four blocks, impose that their
points lie in the vector plane `H_n=ker(n)`.  Stratify the projective normal
`[n]` by its exact nonzero coordinate mask `N subset {0,1,2}`.  Put

```text
epsilon_(B,N) = 1 if U_(i,B) has a coordinate in N, else 0.
```

On the normal-support torus `P(k^N)^torus`, the vector-bundle rank is constant:

```text
dim(U_(i,B) intersect H_n)
  = dim U_(i,B) - epsilon_(B,N).                               (6)
```

The incidence stratum therefore has dimension

```text
(|N|-1)
+ sum_(B in S) (dim(U_(i,B) intersect H_n)-1)
+ sum_(B not in S) (dim U_(i,B)-1).                            (7)
```

After removing coincident block points and requiring the selected points to
span `H_n`, it is irreducible.  Projection to (3) is injective because three
distinct collinear points determine their line.  Thus (7) gives the exact
locally closed codimension.  Every line has one exact normal support, so these
strata exhaust the collinearity locus.  A non-automatic event has codimension
at least one.

If two different three-block events occur among four distinct blocks, the
triples share two distinct points and determine the same line.  The correct
stratum is the single four-block line stratum; its codimension is charged
once, not as the sum of two triple events.

## 4. Cross-ratio maps are dominant on every feasible coordinate stratum

On a four-distinct line stratum, at least one point moves freely on the line.
Indeed, if no point were free, every support would be a coordinate point or a
coordinate plane meeting the line in one point.  Repeated coordinate planes
would give repeated points, and there are only three coordinate planes.  If
one or two coordinate points are prescribed, the line-through-point
conditions make the remaining coordinate-plane intersections repeat one of
those points unless one support contains the whole line, which is precisely a
free point.  Four distinct points are therefore impossible without a free
factor.

For a fixed labelled block, containing the event line is a closed condition on
the irreducible exact-normal-support base.  The finitely many such conditions
cover that base by the preceding argument, so one labelled block contains the
line throughout the stratum.  Choose it as the free point.  After forgetting
that point but retaining the line, the other three labelled points, and the
remaining support data (an irreducible parameter space `Y`), the cross-ratio
map on the free-point fibre is a fractional-linear isomorphism

```text
line minus the other three points  -->  M_(0,4).
```

Conversely the labelled cross ratio recovers the free point.  Thus the
incidence stratum is birational (indeed, after this standard labelled
trivialization, isomorphic) to `Y x M_(0,4)`, with cross ratio the second
projection; this is stronger than mere dominance.  For `k` such strata, their
equal-cross-ratio fibre product is birational to

```text
(product_j Y_j) x M_(0,4),
```

and is therefore irreducible of codimension exactly `k-1`.  Its closure is
the unique equality component meeting the chosen dense opens.  There is no
unordered/anharmonic splitting here: the four chart labels fix the order.
Coincident-point boundaries belong to coarser exact partitions.

As a finite check on this argument, every feasible four-singleton coordinate
support tuple and every normal-support event type was enumerated.  All `3,052`
cross-ratio-eligible types produced two distinct lifted values modulo
`1,000,003`; no constant type appeared.  This is supporting finite evidence,
not a substitute for the preceding characteristic-zero argument.

## 5. The subset-incidence and global charge lemmas

Call a vertex **active** when a non-automatic triple or four-block line event
is imposed there.  A fixed-factor rank loss on edge `ij` contains a
three-point circuit (or its four-point fixed-factor span version).  If the
event is at `i`, the relevant three chart labels lie in three distinct blocks
at `i`, while the same three labels lie in one block at `j`.  Therefore that
block of `Pi_j` has size at least three, so `Pi_j` has at most two blocks.
Vertex `j` cannot itself carry a collinearity event among three distinct
blocks.  This is the exact chart-subset incidence statement; it does not infer
compatibility merely from the total block count.

There is one separate ruling mechanism.  A line-valued three-block vertex has
one repeated chart pair `P`.  Two such vertices create a reducible ruling-pair
circuit exactly when their repeated pairs are complementary.  This includes
both active--active edges and edges from an active ruling vertex to a
three-block vertex that was already structurally line-valued.  A
structural--structural circuit is already present in `rho_ij` and is not a new
loss.

Let `r` be the number of ruling-active vertices and `u` the number of
non-active structurally line-valued three-block vertices.  For complementary
pair type `ell=1,2,3`, let `x_ell,y_ell` be the active counts on its two sides
and `X_ell,Y_ell` the structural counts.  The exact number of new ruling edges
is bounded by

```text
R(r,u) = max sum_ell (x_ell y_ell + x_ell Y_ell + y_ell X_ell),
sum_ell(x_ell+y_ell)=r,  sum_ell(X_ell+Y_ell)=u.               (8)
```

Only `r+u<=4` is relevant.  The elementary integer maximum is

```text
          u=0  u=1  u=2  u=3  u=4
r=0        0    0    0    0    0
r=1        0    1    2    3
r=2        1    2    4
r=3        2    4
r=4        4.                                                (9)
```

This table is also a direct enumeration of the six possible repeated-pair
labels; it does not add the incompatible maxima of active--active and
active--structural subgraphs separately.  Explicitly, for `r=1` all `u`
structural labels can complement the active label.  For `r=2`, equal active
labels give `2u`, complementary active labels give `1+u`, and all other labels
give at most `u`, yielding `1,2,4` for `u=0,1,2`.  For `(r,u)=(3,0),(4,0)` the
complete-bipartite maximum is `2,4`; with `(3,1)`, active multiplicities
`2+1` across a complementary pair give two active--active plus two
active--structural edges, and no label can meet more.  These are every
remaining entry because `r+u<=4`.  Multiple overlapping triple events at one
four-block vertex remain consolidated into the single stronger four-block
line stratum of Section 3.

Every further edge loss is at most one by the circuit lemma.  Let

- `a` be the number of active vertices;
- `r` be the number of ruling-active three-block vertices;
- `u` be the number of structurally line-valued non-active three-block
  vertices;
- `f` be the number of active four-distinct line vertices;
- `s` be the number of non-active vertices already generically line-valued
  with four distinct blocks;
- `p` be the number of passive vertices capable of receiving a fixed-factor
  circuit.

Here `r+f<=a`, and neutral vertices can be omitted when maximizing, so
`a+u+s+p<=4`.  Fixed-factor losses contribute at most `a p`, ruling-pair
losses at most `R(r,u)`, and the active vertex events cost at least `a`.
Line-valued active vertices may also join a cross-ratio class; their event
cost has already been charged once and is not charged again.  Only the `f`
four-distinct active vertices can join the `s` structural four-distinct
vertices.  A largest cross class of size at most `k=f+s` contributes at most

```text
h(k) = 0                                      for k <= 1,
h(k) = binomial(k,2) - (k-1)                 for k >= 2.      (10)
```

after its `k-1` compatibility equations.  Splitting into smaller classes does
not increase this amount.  Thus the total rank-loss-minus-codimension gain is
bounded by

```text
a p - a + R(r,u) + h(f+s),
r+f <= a,                p <= 4-a-u-s.                        (11)
```

Using (9), `h(0),...,h(4)=(0,0,0,1,3)`, and enumerating only
`a=0,1,2,3,4`, the maxima of (11) at fixed `a` are respectively
`3,2,3,2,0`.  Hence the global maximum is three, with exactly two extremal
patterns:

1. `a=r=2`, `p=2`, `u=f=s=0`: two complementary ruling-active vertices,
   two passive vertices, five edge losses, and two vertex-event dimensions;
2. `a=0`, `s=4`, `u=p=0`: four structurally line-valued vertices in one
   cross class.

In the second pattern every pair has generic rank four (the product
description in Section 4 makes equality non-generic), so the predecessor value
is at least `24+Delta>=24`; it finishes at least `21`.  Only the first pattern
could start at generic value `23` and finish at `20`.  Equality forces both
passive vertices to be fully synchronized: each must contain a distinct-block
triple from each of two complementary `2+1+1` partitions, and those two
triples have union all four chart labels.

The targeted exact `q=23` pass records the first failed requirement for every
one of the `8,882` canonical systems.  The counts are

```text
no two complementary 2+1+1 vertices:                    8,832
the other two vertices are not both synchronized:          32
the proposed active line conditions are support-forced:     18
reaches the five-loss check:                                 0
reaches the total-codimension-two check:                     0. (12)
```

For each of the final eighteen records the three active block supports have
structural rank two at both active vertices.  Their points are therefore
already line-valued in the predecessor stratum; imposing collinearity costs
zero and creates no active ruling event.  The per-record certificate pins each
record by its canonical SHA-256 digest and pins the ordered failure ledger by
one aggregate digest.

An independent read-only reconstruction did not read that zero-certificate
script, output, or failure ledger.  Starting from the accepted census
definitions and the pinned near-frontier input, it reproduced the chain as
`8,419` wrong active-count failures plus `413` non-complementary-pair failures,
then a synchronized-passive histogram `0:1, 1:31, 2:18`, followed by zero
non-automatic survivors.  The eighteen terminal records split six each among
active support-plane types `(3,5)`, `(6,5)`, and `(6,3)`; every active
structural rank is exactly two.  The independent canonical digest of the
ordered `8,882` `q=23` records is pinned in Section 8.

Consequently, conditional on the charge lemma, generic `q>=23` remains at
least `21`, and every equality or sub-`20` threat comes from the exactly `547`
canonical predecessor systems with `q<=22`.  The finite conclusion remains
candidate because the mathematical charge and the separate `q<=22` component
reconstruction remain under review.

This charge argument is a principal hostile-review target.  It must not be
cited as proved until the reviewer confirms both the subset-incidence lemma
and the joint use of one line-event cost for passive-edge and cross-ratio
effects.

## 6. Candidate exhaustive finite component ledger

The accepted predecessor was replayed exactly to extract the `547` systems
with generic `q<=22` (`q=20:2`, `q=21:39`, `q=22:506`).  On every system the
event screen enumerated:

- every non-automatic three-block line event;
- every four-block line event;
- every exact normal support;
- products of the four vertex strata; and
- every labelled cross-ratio equivalence relation.

The mixed-ruling-aware replay first checks two hostile `0012|0122` fixtures
directly.  In the active--active fixture, two non-automatic line events lower
generic edge rank four to rank three.  In the active--structural fixture, one
endpoint has a non-automatic line event while the other has masks `(3,3,3)`
and structural rank two; that single event again lowers rank four to three.
The explicit complementary-ruling upper bound is three in both fixtures.  All
base ranks then reproduced the predecessor.  Across the `547` systems, each of
the `6,429`
non-cross-ratio rank-drop cells matched an explicit fixed-factor Segre-circuit
or fixed-factor span upper bound.  There were zero complementary-ruling
rank-drop cells and zero affected records; the run aborts on any unexplained
or accidentally deficient event rank.  The screened minimum was `20`, with
best-value histogram

```text
20: 5 records
21: 73 records
22: 469 records.                                             (13)
```

There were nine value-`20` event strata in five canonical records.  They
collapse under the declared chart/common-vertex/colour symmetries to the
following seven candidate source orbits.  By the charge bound and the `q=23`
zero-certificate, these are the candidate exhaustive equality list:

| orbit | `Delta` | `c_rank` | ranks `(01,02,03,12,13,23)` | value |
|---|---:|---:|---|---:|
| `A` generic `0000|0123|0123|0123` | 0 | 0 | `(2,3,3,4,4,4)` | 20 |
| `B` generic `0000|0000|0123|0123` | 3 | 0 | `(1,3,3,3,3,4)` | 20 |
| `B` one unrestricted four-block line | 3 | 2 | `(1,2,3,2,3,4)` | 20 |
| `B` two lines, unequal cross ratios | 3 | 4 | `(1,2,2,2,2,4)` | 20 |
| `B` two lines, equal labelled cross ratio | 3 | 5 | `(1,2,2,2,2,3)` | 20 |
| `(2,1)` selector, three synchronized vertices plus one line | 9 | 2 | `(1,1,2,1,2,2)` | 20 |
| injective selector, three synchronized vertices plus one line | 9 | 2 | `(1,1,2,1,2,2)` | 20 |

The one-line `B` source occurs in two symmetric labelled positions; the
three-synchronized `(2,1)` source likewise has symmetric labelled records.
That accounts for nine strata but seven symmetry orbits.

Each listed root source is irreducible: generic sources are products of
projective-support opens; one-line sources are the irreducible incidence
strata of Section 3; the unequal-cross-ratio case is a dense open in a product
of two such strata; and the equal-cross-ratio case is their irreducible fibre
product from Section 4.  On each source the six common-edge evaluation ranks
are constant, so the coefficient incidence is a vector bundle.  At value 20
its total dimension is

```text
(28-Delta-c_rank) + (252-16-sum r_ij) = 244.                 (14)
```

This is a candidate codimension-eight equality ledger.  Its exhaustiveness
depends on the still-unaccepted mathematical charge argument and on the exact
finite `q=23` zero-certificate; it is not promoted merely because both current
computations return the expected result.

The earlier `v4b` output predated explicit complementary-ruling recognition
and is superseded.  The first ruling-aware `v5` replay covered active--active
circuits but did not include the active--structural hostile fixture, so it too
is superseded.  Their aggregate counts happened to agree because no ruling
cell occurs at `q<=22`; only the mixed-ruling-aware `v6` output below supports
that absence.

## 7. Corrected `B_all` fixture evidence

For every known candidate orbit in the table, an exact rational root fixture was
chosen inside the displayed dense stratum.  In particular, every unrestricted
line event now uses

```text
H: x+y+z=0,
```

whose normal has full support `111`; the structural `xy` line in orbit `A`
remains separate.  This corrects an earlier exploratory probe that used the
boundary line `z=0` for unrestricted line components.

For a root fixture, each root-root block is sampled in the exact kernel of its
four chart evaluations.  Each contracted cross covector `h_(i,t)` is sampled
in `(x_i^(t))^perp`, so all sixteen outer-edge evaluations are also imposed.
The resulting balanced `A | A^c` sensor has an exact nonzero `8 x 8` minor.
The seven equality-orbit minors are:

```text
A generic:                         901659762416043994210084799/108900000
B generic:                        -345919614259292012/3375
B one line:                       -11187289987739049817/144000
B two lines, unequal:             -1772405772269592
B two lines, equal:               -245747897116304/375
(2,1) three-sync plus line:        13392112152672
injective three-sync plus line:    1987165331179776.             (15)
```

Equation (15) shows candidate properness on every source in the candidate
exhaustive ledger.  If the charge and finite-exhaustion audits are accepted,
all strata above value `20` already have codimension at least nine, while each
irreducible value-`20` source receives one nonzero `B_all` determinant cut.
Under those still-candidate premises, the fixed-pencil all-balanced locus has
codimension at least nine.  This remains an unaccepted parent-level result,
not an accepted theorem or a seventy-pencil compatibility statement.

### Superseded fixture outputs

Two earlier local fixture presentations must not be cited:

1. the first probe sampled the sixteen cross covectors freely and therefore
   omitted `h_(i,t)(x_i^(t))=0`;
2. the next corrected probe enforced those equations but placed unrestricted
   collinear roots on a lower normal-support boundary rather than in the dense
   equality stratum.

The current fixture script enforces every evaluation and uses full-support
line normals.  This explicit supersession is part of the evidence boundary.

## 8. Current reproducible evidence and review gates

The current exploratory artifacts are intentionally ignored under
`.research-runs`; their hashes identify the exact material under review:

```text
kestrel_s3_near_frontier_q22_v1.json
  SHA-256 d5b821a47f8164f56e1254e9400ff1875bab650ce5e64be3a0e191129bed541a

kestrel_s3_near_frontier_q23_v1.json
  SHA-256 3873e085aeb37eff6f9f539bb99433ea05f7f7d414a69758e550644ec37edf75

kestrel_extract_s3_near_frontier_v1.py
  SHA-256 0cf3c84036f06aeb87e4d12edd6984539fec0cc5e00f8c8f29440035b80626ed

kestrel_s3_q23_ruling_zero_certificate_v1.py
  SHA-256 164d77e8730ebd5a86f5d5b71accb6b6b533115146aff33f273b4109f3030452

kestrel_s3_q23_ruling_zero_certificate_v1.json
  SHA-256 9372d1c1103db490241dbe035e87a6c5a8f470342d16ab65a0a8d583009035e4
  ordered failure-ledger SHA-256
  41c3c107ff93d247b1d8ae2575395bbaff43b274cf7ee94c7cb707d034e30b3d

independent read-only q=23 reconstruction
  base commit 638fe92914bd54c84230d9c4c87c39dbfcf0af09
  accepted census Git blob afbd804bf334cca1f3d38f6551022018c904db6a
  canonical ordered q=23-record SHA-256
  608a32c7f8386d193fc2b438576318d9366d59e05c11f22171500b63b9cab926

kestrel_s3_circuit_explained_ledger_v6_mixed_ruling_aware.json
  SHA-256 bd72d00690bd414ffe63267f317256fe77c6fac1a77393515221a5acce3d098e

kestrel_s3_plane_crossratio_screen_v1.py
  SHA-256 596689e797d9109994127d66032c5e1bafa02cdcdc300bc602aeb2e29c74173c

kestrel_s3_crossratio_dominance_v1.py
  SHA-256 502c623be22ea039a4add9db32ec2da66d35f523aa91fccab0b8a076b2dcf665

kestrel_s3_q20_parent_probe_v1.py
  SHA-256 9ac3b5938ebbbebaafb2eef22e451cf42bb7ddca02d36d74a717363f8188d395
```

Before promotion, the following are mandatory:

1. a hostile proof audit of the minimal-circuit, coordinate-incidence,
   cross-ratio-dominance, subset-incidence, and global-charge lemmas;
2. an independent reconstruction of the current nine-stratum/seven-orbit
   `q<=22` ledger (the `8,832/32/18/0` `q=23` chain has passed a separate
   read-only reconstruction);
3. a no-import reconstruction of every dense-component fixture and its
   boundary evaluations/minors;
4. promotion of any accepted verifier/certificate out of `.research-runs`,
   with stable hashes and ordinary repository validation;
5. a live-frontier update only if the candidate result is accepted; and
6. a separate treatment of seventy-pencil compatibility, remaining target
   equations, and witness exclusion.

Until those gates close, the precise status is:

```text
rank-degeneracy envelope (1):                CANDIDATE
q<=22 event screen:                          EXPLORATORY EXACT FINITE EVIDENCE
q=23 complementary-ruling elimination:       EXPLORATORY EXACT; FILTER AUDIT PASSED
seven equality-component orbits:              CANDIDATE EXHAUSTIVE LEDGER
B_all properness on seven sources:            CANDIDATE, FIXTURES VERIFIED
fixed-pencil B_all codimension >=9:           CANDIDATE PARENT-LEVEL RESULT
seventy-pencil compatibility:                 OPEN
eight-vertex witness exclusion:               OPEN
global Krenn--Gu conjecture:                  UNRESOLVED.
```
