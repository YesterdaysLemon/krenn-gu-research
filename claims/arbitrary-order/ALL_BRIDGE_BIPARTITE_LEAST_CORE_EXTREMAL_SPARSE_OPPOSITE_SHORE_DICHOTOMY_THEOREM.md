# All-bridge bipartite least-core extremal-sparse opposite-shore dichotomy

## Status

This is an exact arbitrary-order reduction over characteristic zero in the
simultaneous balanced all-bridge branch.  It starts with the globally least
supported pure hafnian cancellation and its connected bipartite
matching-covered first-cofactor core from the preceding all-degree theorem.

Suppose that this core has an **extremal sparse branch site** `v`.  If `beta`
is the cyclomatic rank and `N` is the number of core perfect matchings, this
means

```text
deg(v)=N=beta+1,                                      (A)
```

and every matching port at `v` is a singleton.  Then the shore containing
`v` has no other branch site.  The opposite shore has exactly one of two
forms:

1. it also has one extremal degree-`beta+1` site, and the whole core is a
   subdivision of `Theta_(beta+1)` into internally disjoint odd routes; or
2. it has between two and `beta-1` branch sites, every one of degree at most
   `beta`, and every one carries a nonzero multi-monomial aggregate cofactor
   port.

The sparse site also forces the pointwise support bounds

```text
deg_D(v)>=beta+3,       deg_G(v)>=beta+6,              (B)
```

where `D` is the physical saturated-diagonal graph and `G` is the full
essential support skeleton.

At `beta=3`, the two alternatives have exact suppressed route kernels:

```text
four odd routes between two quartic sites;

or

two odd routes from one sparse quartic site to each of two cubic sites,
plus one even route between those cubic sites.          (C)
```

Both cubic sites in the second form have nonzero aggregate ports.  In
particular, a rank-three sparse site belongs to the `Delta(D)>=6` branch, not
to the degree-five subcubic branch.

This is a structural reduction, not an exclusion.  Both alternatives occur
as exact characteristic-zero least scalar residuals.  Moreover,
`N=beta+1` by itself does **not** imply a sparse site or a theta: a weighted
`K_(3,3)-e` is an exact least residual with `beta=3,N=4` and four cubic branch
sites.  None of the scalar controls below is a simultaneous three-colour
all-bridge witness.  Aggregate-port control, extremal sparse-fan exclusion,
the separate deeper-blocker branch, and universal extraction/gluing remain
open.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Imported least core and notation

Let `e` be a colour and let `S` be globally least, over all colours and all
nonempty proper even shores, such that

```text
haf(Z^e[S])=0
and support(Z^e[S]) has a perfect matching.            (1)
```

For `ij subset S`, put

```text
B_ij=Z^e_ij haf(Z^e[S-{i,j}]),
A={ij subset S:B_ij!=0}.                               (2)
```

The imported least-core theorem gives the exact identity between `A` and the
union of all support perfect matchings on `S`.  In particular, `A` is
connected and matching-covered, every edge of `A` is allowed, and

```text
delta(A)>=2.                                           (3)
```

The all-bridge saturated bit flips make `A` bipartite.  Write its shores as
`U,W`, each of size `m`, and put

```text
beta=|E(A)|-|S|+1,
N=#PM(A).                                              (4)
```

The all-degree matching-polytope theorem supplies

```text
sum_(u in U)(deg(u)-2)
 =sum_(w in W)(deg(w)-2)=beta-1,                       (5)

N>=beta+1.                                             (6)
```

At any branch vertex `x`, the imported port theorem partitions the `N`
perfect matchings into the `deg(x)` nonempty incident-edge ports.  Every port
sum is the nonzero restricted first cofactor on that incident edge.  Hence

```text
N=deg(x)  => every port at x is one monomial;

N>deg(x)  => some port at x has at least two monomials
              and a nonzero total.                    (7)
```

Assume from now on that `v in U` is an extremal sparse branch site.  Thus
(A) holds.  Since `deg(v)>=3`, one has `beta>=2`.

## 2. Shore excess is exhausted at the sparse site

The contribution of `v` to the `U`-shore excess in (5) is

```text
deg(v)-2=(beta+1)-2=beta-1.                            (8)
```

It consumes the entire shore excess.  Every other summand in (5) is
nonnegative by (3), so

```text
deg(u)=2       for every u in U-{v}.                   (9)
```

Let `w_1,...,w_r` be the branch vertices on `W`, and write

```text
epsilon_i=deg(w_i)-2>=1.                               (10)
```

The opposite-shore identity in (5) becomes

```text
epsilon_1+...+epsilon_r=beta-1.                        (11)
```

In particular,

```text
1<=r<=beta-1.                                         (12)
```

This elementary partition is the source of the dichotomy.  The route
conclusion in the one-part case also needs the following exact graph fact.

## 3. A nontrivial matching-covered graph has no cut vertex

### Lemma 1

The core `A` is 2-vertex-connected.

### Proof

The branch site `v` has degree at least three, so `A` is not the two-vertex
single-edge graph.  Suppose that a vertex `x` were a cut vertex, and let
`C_1,...,C_t`, `t>=2`, be the components of `A-x`.  Connectivity gives an
edge `xy_i` from `x` into every `C_i`.

Every edge of a matching-covered graph belongs to a perfect matching.  Fix
`i` and choose a perfect matching containing `xy_i`.  Inside that matching,
`C_i-y_i` is matched internally, while every `C_j`, `j!=i`, is matched
internally.  Therefore

```text
|C_i| is odd,
|C_j| is even for every j!=i.                          (13)
```

Repeating the argument with an allowed edge from `x` into `C_j` makes
`|C_j|` odd and `|C_i|` even, a contradiction.  Thus `A` has no cut vertex.
QED.

This proof uses matching-coveredness, not merely the existence of one perfect
matching.  It will exclude a degree-two path which leaves and returns to the
same branch vertex.

## 4. Extremal sparse opposite-shore dichotomy

### Theorem 2

Exactly one of the following holds.

#### I. Two extremal sites and an odd multi-theta

One has `r=1`.  The unique opposite-shore branch vertex `w` satisfies

```text
deg(w)=beta+1=N.                                      (14)
```

Every other vertex of `A` has degree two, and `A` is the union of exactly
`beta+1` internally vertex-disjoint odd `v`--`w` paths.  Equivalently, `A`
is a subdivision of `Theta_(beta+1)`.  Every port at both `v` and `w` is a
singleton.

#### II. One sparse shore and several aggregate sites

One has

```text
2<=r<=beta-1.                                         (15)
```

For every opposite-shore branch vertex `w_i`,

```text
3<=deg(w_i)<=beta,                                    (16)
```

and at least one incident port at `w_i` contains two or more matching
monomials with nonzero total.

### Proof

If `r=1`, equations (10)--(11) give

```text
deg(w_1)-2=beta-1,
```

which is (14).  Equations (9) and (11) say that `v,w_1` are the only branch
vertices.

Suppress every maximal path whose internal vertices have degree two.  A
closed component consisting only of degree-two vertices is impossible by
connectedness.  Every resulting route therefore has branch vertices as its
endpoints.  Lemma 1 forbids a route which leaves and returns to `v` or which
leaves and returns to `w_1`: the internal vertices of such a route would be
separated from the other branch vertex by deleting its endpoint.  Hence every
route joins `v` to `w_1`.

There are `deg(v)=beta+1` such internally disjoint routes.  Since `v in U`
and `w_1 in W`, every route has odd length.  This proves the multi-theta
description.  Finally, the `N=deg(w_1)` nonempty ports at `w_1` partition
`N` matchings, so they are all singletons by (7).

Now suppose `r>=2`.  Since the other `r-1` positive parts in (11) consume at
least `r-1`,

```text
epsilon_i<=beta-r,
deg(w_i)=epsilon_i+2<=beta-r+2<=beta.                  (17)
```

This proves (15)--(16).  But `N=beta+1`, so

```text
N>deg(w_i)
```

at every one of these sites.  The nonzero port partition (7), applied
separately at every `w_i`, forces a multi-monomial port with nonzero total at
each site.  No independence or disjointness between those aggregate ports is
asserted.  QED.

## 5. Saturated- and full-support degree landing

The `beta+1` core edges incident with `v` all lie in
`support(Z^e)`.  Let `d,k` be the other two colours.  Active exclusivity makes
`support(Z^e)` physically disjoint from `E_d union E_k`, and the two active
graphs `E_d,E_k` are physically disjoint from each other.  Their score-one
identities give positive degree at every vertex.  Thus, in addition to the
`beta+1` core edges, `v` has at least one distinct saturated edge from each
of `E_d,E_k`.  Therefore

```text
deg_D(v)>=beta+1+1+1=beta+3.                           (18)
```

The unconditional full-support inequality from the degree-five/full-support
owner is

```text
deg_G(x)>=deg_D(x)+3       for every vertex x.          (19)
```

Applying it at `v` proves

```text
deg_G(v)>=beta+6.                                      (20)
```

These are lower bounds, not exact degrees.  They use no maximum-degree
hypothesis.  In particular, at `beta=3` the sparse site satisfies

```text
deg_D(v)>=6,       deg_G(v)>=9.                        (21)
```

Thus the rank-three extremal sparse case is absent from the degree-five
subcubic core classification.

## 6. Rank-three sparse-site normal form

Assume `beta=3`.  Each shore has excess two.  The sparse site `v` has degree
four and exhausts the excess on its shore.

### Corollary 3

Exactly one of the following route kernels occurs after suppressing maximal
degree-two paths.

1. **`Q/Q` kernel.**  The opposite shore has one quartic site `w`.  The
   kernel consists of four parallel `v`--`w` routes.  All four routes are
   odd, `N=4`, and both quartic sites are sparse.
2. **`Q/C^2` kernel.**  The opposite shore has two cubic sites `x,y`.  If
   `a,b,c` are respectively the numbers of routes from `v` to `x`, from `v`
   to `y`, and from `x` to `y`, then

   ```text
   a+b=4,
   a+c=3,
   b+c=3,                                             (22)
   ```

   and hence

   ```text
   (a,b,c)=(2,2,1).                                   (23)
   ```

   The four routes incident with `v` and an opposite-shore branch site are
   odd.  The route between `x,y`, which lie on the same shore, is even.
   Again `N=4`; `v` is sparse, while both cubic sites have a nonzero
   aggregate port.

### Proof

Equation (11) partitions `beta-1=2`.  Its only positive partitions are `2`
and `1+1`.  The first is Theorem 2.I with four routes.  The second gives two
cubic sites.  Lemma 1 again rules out a suppressed route from a branch vertex
back to itself, so every route has two distinct branch endpoints.  The three
degree equations are exactly (22), whose unique nonnegative solution is
(23).  Route parity follows from the fixed bipartition.  The port conclusions
are Theorem 2.  QED.

The `Q/C^2` conclusion gives two aggregate sites, but it does not say that
their aggregate ports are different, algebraically independent, or coupled
to two different mixed target equations.

## 7. Complete rank-three suppressed-kernel census

The sparse-site corollary is only part of the rank-three topology.  The
following finite census is included to delimit the hypothesis and to prevent
the false inference `N=beta+1 => sparse theta`.

At `beta=3`, equation (5) says that each shore has one of the two degree
patterns

```text
Q:    one degree-four vertex and all other vertices degree two;
C^2:  two degree-three vertices and all other vertices degree two. (24)
```

Suppress maximal degree-two paths.  A route between opposite shores has odd
length; a route between branch vertices on the same shore has even length.
A perfect matching restricts on an odd route to one of the endpoint states
`00,11`, and on an even route to one of `10,01`.  Conversely, an assignment
of route states which covers every branch vertex exactly once extends
uniquely along all routes to a perfect matching of `A`.

### Proposition 4

Up to swapping shores and relabelling branch vertices within a shore, there
are exactly five matching-covered rank-three route kernels:

| shore types | suppressed route multiplicities | `N` |
|---|---|---:|
| `Q/Q` | four routes between the quartic sites | 4 |
| `Q/C^2` | multiplicities `(2,2,1)` as in (23) | 4 |
| `C^2/C^2` | no same-shore routes; cross multiplicity matrix `[[1,2],[2,1]]` | 5 |
| `C^2/C^2` | one route within each shore and one route on every cross pair; the simple kernel is `K_4` | 4 |
| `C^2/C^2` | one route within each shore and two routes on each edge of one cross perfect matching | 4 |

All cross-shore routes in the table are odd and all same-shore routes are
even.  Consequently every rank-three least bipartite core has

```text
N in {4,5}.                                            (25)
```

Only the first two rows contain an extremal sparse site.  In the last three
rows every branch site is cubic; when `N=4` every cubic site has an aggregate
port, and when `N=5` the same is true a fortiori.

### Proof

The `Q/Q` and `Q/C^2` rows were proved in Corollary 3.  It remains to treat
`C^2/C^2`.  Name the branch vertices `a,b in U` and `x,y in W`.  Put

```text
h_U=# routes a--b,             h_W=# routes x--y,
p=# routes a--x=b--y,          q=# routes a--y=b--x,   (26)
```

where the equalities in the last two expressions are consequences of the
four cubic degree equations.  Those same equations force

```text
h_U=h_W=:h,
h+p+q=3.                                             (27)
```

There are four cases.

- If `h=0`, connectivity excludes `p=0` and `q=0`.  Thus
  `{p,q}={1,2}`.  A perfect matching chooses one route on one of the two
  cross perfect matchings, giving

  ```text
  N=p^2+q^2=5.
  ```

- If `h=1`, then `p+q=2`.  For `(p,q)=(1,1)`, each even same-shore route
  covers one endpoint, and the remaining endpoints can be joined by any one
  of the four cross routes.  Hence `N=4`, giving the simple `K_4` kernel.  For
  `{p,q}={0,2}`, only two of the four orientation pairs of the even routes
  leave endpoints joined by a cross route, but the applicable cross pair has
  multiplicity two.  Again `N=2+2=4`.

- If `h=2`, then `{p,q}={0,1}`.  The two even routes within each shore must
  cover the two branch endpoints between them.  Every cross route is
  therefore in endpoint state `00` in every perfect matching and no edge of
  that route can lie in a perfect matching.  This contradicts the fact that
  `A` is the allowed matching-covered core.

- If `h=3`, then `p=q=0`, and the two shores are disconnected.

The listed kernels are connected, and the displayed route-state choices use
both alternating states needed on every nontrivial route; hence their route
edges are allowed.  This proves completeness and the matching counts.  QED.

The census is a graph theorem about the least core.  It does not say that
every listed route kernel extends to a simultaneous all-bridge target system.

## 8. Exact sharp controls and refuted stronger claims

All controls in this section are hollow symmetric scalar matrices supported
on bipartite graphs.  Their hafnians are the permanents of the displayed
biadjacency matrices.  They prove sharpness of the pure least-residual
topology only.

### 8.1 The four-route sparse branch is nonempty

Take four internally disjoint length-three paths

```text
v--a_i--b_i--w,       1<=i<=4.                         (28)
```

Give every edge weight one except the edge `b_4w`, which has weight `-3`.
There are exactly four perfect matchings, one for each route selected to
match both endpoints, and their weights are

```text
1,1,1,-3.                                             (29)
```

Their sum is zero.  Every proper supported principal hafnian is either one
nonzero monomial or a proper subsum of (29), hence is nonzero.  This is the
inherited `Theta_4` least-residual control and realizes Theorem 2.I.

### 8.2 An exact mixed-shore sparse/aggregate control

Let the bipartition be

```text
L={u_0,u_1,u_2,u_3},       R={w_0,w_1,w_2,w_3},        (30)
```

and, in the column order `w_0,w_1,w_2,w_3`, take support rows

```text
u_0: 1111,
u_1: 0101,
u_2: 1010,
u_3: 1100.                                            (31)
```

Set `z_(u_0w_0)=-3` and give every other supported edge weight one.  The four
perfect matchings, written as the column selected by each row, are

```text
(0,3,2,1),
(1,3,2,0),
(2,3,0,1),
(3,1,2,0).                                            (32)
```

Only the first uses `u_0w_0`, so their weights are `-3,1,1,1` and the full
hafnian is zero.  Every one of the ten support edges occurs in (32), so the
graph is matching-covered.

For completeness, direct expansion of every proper supported square minor
of the biadjacency matrix gives

| minor size | supported minors | possible nonzero values |
|---:|---:|---|
| `1 x 1` | 10 | `-3,1` |
| `2 x 2` | 25 | `-3,-2,1,2` |
| `3 x 3` | 16 | `-2,-1,1,2` |

Thus all `51` proper supported principal hafnians are nonzero, and the eight
vertices form a least supported cancellation.

The degrees on `L` are `(4,2,2,2)` and those on `R` are `(3,3,2,2)`, so
`beta=10-8+1=3`.  At `u_0`, the four port sums are

```text
-3,1,1,1,                                             (33)
```

and the site is sparse.  At `w_0`, one aggregate port has two monomials and
sum `2`; at `w_1`, one aggregate port has two monomials and sum `-2`.
Suppressing degree-two paths gives two odd routes from `u_0` to each of
`w_0,w_1` and the even route `w_0--u_3--w_1`.  This realizes the
`Q/C^2` alternative and shows that its two aggregate conclusions are sharp.

### 8.3 Equality of matching count does not force a theta

Let `L={u_0,u_1,u_2}`, `R={w_0,w_1,w_2}`, and take `K_(3,3)` with only the
edge `u_2w_2` deleted.  Give `u_0w_0` weight `-3` and every other edge weight
one.  There are exactly four perfect matchings.  The edge `u_0w_0` occurs in
one, so their weights are again `-3,1,1,1` and the full hafnian vanishes.

Every proper supported shore has size `1+1` or `2+2`.  A supported `1 by 1`
minor is a nonzero edge weight.  A supported `2 by 2` permanent which avoids
`-3` is `1` or `2`; one which contains `-3` is `-2` or `1`.  Hence no proper
supported hafnian vanishes.  Every one of the eight support edges belongs to
one of the four full matchings, so this is another exact least
matching-covered residual.

Here

```text
beta=8-6+1=3,       N=4=beta+1,                       (34)
```

but each shore has degree pattern `(3,3,2)`.  There is no degree-four sparse
site, and suppression gives the simple `K_4` row of Proposition 4, not a
four-route theta.  Therefore the tempting implications

```text
N=beta+1 => some sparse site,
N=beta+1 => Theta_(beta+1)                             (35)
```

are both false.  The load-bearing hypothesis of Theorem 2 is the existence
of an extremal sparse **site**, not merely equality in the polytope count.

## 9. Dependencies, evidence, and exact boundary

The load-bearing imported results are exactly:

1. [`MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md`](MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md):
   the allowed-core identity, connectedness, matching-coveredness, and
   minimum degree two;
2. [`MATRIX_UNIT_MINIMAL_PURE_COFACTOR_PORT_AGGREGATE_AND_CONFORMAL_FAN_REDUCTION_THEOREM.md`](MATRIX_UNIT_MINIMAL_PURE_COFACTOR_PORT_AGGREGATE_AND_CONFORMAL_FAN_REDUCTION_THEOREM.md):
   the nonzero port partition and sparse/aggregate alternative;
3. [`ALL_BRIDGE_ACTIVE_DECK_ALL_DEGREE_LOCALIZED_PURE_CANCELLATION_AND_BIPARTITE_CORE_REDUCTION_THEOREM.md`](ALL_BRIDGE_ACTIVE_DECK_ALL_DEGREE_LOCALIZED_PURE_CANCELLATION_AND_BIPARTITE_CORE_REDUCTION_THEOREM.md):
   global least-core selection, all-bridge bipartiteness, shore excess,
   matching-polytope dimension, `N>=beta+1`, and extremal sparse equality;
   and
4. [`ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FIVE_BRANCHING_OR_CANCELLATION_CORE_REDUCTION_THEOREM.md`](ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FIVE_BRANCHING_OR_CANCELLATION_CORE_REDUCTION_THEOREM.md):
   only its unconditional pointwise inequality `deg_G>=deg_D+3` and the
   degree-five subcubic boundary.

The new proofs are the shore-exhaustion dichotomy, the cut-vertex parity
lemma, the odd multi-theta conclusion, simultaneous aggregate forcing on the
opposite shore, the degree landing (18)--(20), and the complete rank-three
route-kernel census.  No computational result is promoted to an
arbitrary-order claim: the proofs above carry the quantifiers.  The two
finite matrices in Sections 8.2--8.3 are exact sharpness and countermodel
controls, with every relevant matching and proper-minor value displayed.

Focused exact checks for the new interfaces are:

```text
python -B claims/arbitrary-order/verify_all_bridge_bipartite_least_core_extremal_sparse_opposite_shore.py
python -B claims/arbitrary-order/audit_all_bridge_bipartite_least_core_extremal_sparse_opposite_shore.py
```

The primary program exhausts connected bipartite matching-covered graphs
through equal shores `4+4`, checks shore exhaustion, both sparse-shore
alternatives, the rank-three `Q/Q` and `Q/C^2` route kernels and port counts,
all ten nonnegative `C^2/C^2` triples `(h,p,q)` satisfying `h+p+q=3`, and the
resulting `4+4` `C^2/C^2` censuses at `N=4,5`.  It also replays the three
weighted controls in Section 8 and a fixed exact `N=5` `C^2/C^2` least
residual by rational matching enumeration.  The
independent audit imports neither repository code nor the primary verifier;
it uses a separate bitmask/permutation representation, checks 2-connectivity
and the sparse opposite-shore dichotomy throughout the same bounded census,
and independently replays the two non-theta rational controls and every
proper supported minor.

These programs are bounded QA, not an arbitrary-order graph cover.  The
shore-excess, cut-vertex parity, suppression, and port-partition proofs above
carry the arbitrary-order quantifiers.  The controls remain scalar least
residuals rather than simultaneous all-bridge witnesses.

```text
simultaneous balanced all-bridge branch:                    ASSUMED;
globally least supported pure core:                         IMPORTED;
core connected, bipartite, matching-covered, min degree 2: IMPORTED;
extremal sparse site d=N=beta+1:                            ASSUMED;
same-shore branch excess exhausted:                        PROVED;
opposite shore one extremal site / several aggregate sites: PROVED EXHAUSTIVE;
one-site alternative is odd Theta_(beta+1):                PROVED;
deg_D(v)>=beta+3 and deg_G(v)>=beta+6:                      PROVED;
beta=3 sparse route kernels Q/Q or Q/C^2:                   PROVED EXHAUSTIVE;
complete beta=3 route-kernel census and N in {4,5}:         PROVED;
N=beta+1 forces a sparse site or theta:                     REFUTED;
either sparse-shore alternative impossible:                NOT PROVED;
opposite aggregate ports algebraically independent:         NOT PROVED;
aggregate port coupled to mixed response/deeper incidence:  NOT PROVED;
every least core has an extremal sparse site:                NOT PROVED;
localized active-deck cut equals the globally least core:    NOT PROVED;
scalar sharpness control is a complete all-bridge witness:   FALSE / NOT CLAIMED;
deeper-blocker branch:                                      OPEN;
universal extraction/gluing:                               NOT PROVED;
global Krenn--Gu conjecture:                                UNRESOLVED.
```
