# All-bridge all-degree localized pure-cancellation and bipartite-core reduction

## Status and exact scope

This is an exact arbitrary-order theorem over characteristic zero in the
simultaneous three-colour balanced all-bridge branch.  It separates two facts
that do not require a saturated-support degree bound from the genuinely
degree-five refinements proved previously.

First, every hypothetical witness in this branch has a proper supported pure
hafnian cancellation in at least one of the following active-deck-localized
forms:

1. an inactive selected-edge complement;
2. one side of a selected-matching-component/complement cut; or
3. one side of a Hamiltonian-chord-arc/complement cut.

This trichotomy holds at **all** saturated degrees.  The alternatives are
exhaustive but are not asserted to be mutually exclusive as the selected
perfect matchings vary.

Second, a globally least supported pure cancellation has a connected
matching-covered core which is bipartite at **all** saturated degrees.  If
that core has cyclomatic rank `beta`, then its perfect-matching polytope has
affine dimension `beta`, it has at least `beta+1` distinct perfect matchings,
and every core degree is at most `beta+1`.  At a branch vertex of degree `d`,

```text
d <= beta       implies a nonzero aggregate cofactor port;
a sparse port fan implies d=N=beta+1,                 (A)
```

where `N` is the number of core perfect matchings.  Rank one is exactly an
even cycle, while rank two is exactly a closed all-odd theta with three
perfect matchings.  More generally, the one-open-port theta profile from the
abstract port theorem cannot occur inside an all-bridge least core.

These are structural reductions, not exclusions.  None of the three
localized cancellations, the even-cycle core, the all-odd theta core, or the
higher-rank aggregate/sparse alternatives is proved impossible here.  The
separate deeper-blocker branch and universal extraction/gluing remain open.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Inherited identities and notation

Let `V` have even size `n>=6`.  For each colour `c in {0,1,2}`, let `Z^c`
be the hollow symmetric matrix of saturated colour-`c` diagonal entries and
put

```text
D={ij : Z^c_ij!=0 for at least one c}.                 (1)
```

For an edge `f={i,j}`, define its global pair-deletion cofactor and active
score by

```text
C_f^c=haf(Z^c[V-{i,j}]),
s_f^c=Z_f^c C_f^c,
E_c={f : s_f^c!=0},
H=D-(E_0 union E_1 union E_2).                         (2)
```

The inherited all-bridge identities are

```text
haf(Z^c[V])=1,                                         (3)

haf(Z^c[A]) haf(Z^d[V-A])=0                            (4)
```

for distinct colours `c,d` and every nonempty proper even `A subset V`, and

```text
sum_(j!=i) s_{ij}^c=1                                  (5)
```

at every vertex `i` and colour `c`.  Consequently every `E_c` spans `V`
with positive minimum degree.  The three physical active edge sets are
pairwise disjoint.  More strongly, if an edge is active in colour `c`, then
its saturated entries and global pair-deletion cofactors in both other
colours vanish.

Every nonzero edge of `Z^c` flips the two normal-type bits other than `b_c`.
Thus either fixed non-`c` bit gives a global bipartition of
`support(Z^c)`.  Finally, the maximum-degree-four exclusion supplies the
degree-free fact

```text
Delta(D)>=5                                             (6)
```

for every hypothetical witness in this all-bridge branch.

## 2. The all-degree active-matching trichotomy

### 2.1 No active perfect matching

Fix a colour `c` for which `E_c` has no graph-theoretic perfect matching.
By (3), `Z^c[V]` has at least one nonzero perfect-matching monomial.  The
following statement has strong quantifiers: for **every** such matching `M`
and **every** edge

```text
f in M-E_c,
```

one has `Z_f^c!=0` and `s_f^c=0`, hence

```text
C_f^c=haf(Z^c[V-f])=0.                                 (7)
```

Here and below `V-f` means deletion of both endpoints.  The matching `M-f`
is a nonzero supported perfect matching on `V-f`, so (7) is a proper
supported pure cancellation.  Applying (4) to the two-point set `f` in both
other colours gives

```text
Z_f^c C_f^d=0        for d!=c.
```

Since `Z_f^c!=0`, every such inactive selected edge satisfies

```text
C_f^0=C_f^1=C_f^2=0.                                  (8)
```

No degree hypothesis is used in (7)--(8).

### 2.2 An arbitrary selected active triple has residual support

Suppose instead that every `E_c` has a perfect matching.  Choose an
arbitrary triple

```text
P_c subset E_c,       c=0,1,2.                         (9)
```

Active exclusivity makes these three matchings physically edge-disjoint.
Let

```text
R_P=D-(P_0 union P_1 union P_2).                       (10)
```

The selected triple uses exactly three incident physical edges at every
vertex.  At a vertex whose `D`-degree is at least five, supplied by (6), at
least two incident edges remain in `R_P`.  Therefore

```text
R_P is nonempty                                        (11)
```

for every choice in (9).  No upper bound on `Delta(D)` is used.

### 2.3 Disconnected selected pairs

For any distinct `c,d`, the graph `P_c union P_d` is a spanning disjoint
union of alternating even cycles.  If it is disconnected, let `A` be the
vertex set of any one of its components.  Then `A` and `V-A` are nonempty
proper even sets; both selected matchings restrict to perfect matchings on
each union of components.  In particular, `P_c` supports `Z^c[A]` and
`P_d` supports `Z^d[V-A]`.  Equation (4) forces at least one of

```text
haf(Z^c[A]),          haf(Z^d[V-A])                    (12)
```

to vanish despite its displayed supported matching.

Thus, for every selected triple, every disconnected pair, and every
component of that pair, the component/complement cut supplies one supported
pure cancellation.  The identity does not identify in advance which of the
two supported factors in (12) vanishes.

### 2.4 Hamiltonian selected pairs

It remains, for the fixed triple (9), to suppose that all three graphs
`P_c union P_d` are Hamiltonian alternating cycles.  Choose arbitrarily

```text
r in R_P,
c with Z_r^c!=0,
d!=c,
```

and let `k` be the third colour.  Every edge of the Hamiltonian cycle
`P_c union P_d` flips `b_k`, and the saturated colour-`c` chord `r` does as
well.  Its endpoints are therefore in opposite classes of that cycle, so
both Hamiltonian arcs between them have odd length.

Exactly one of the two arcs starts and ends with `P_d` edges.  Its length is
not one: otherwise `r` is the same physical edge as a `P_d` edge.  Its length
is not `n-1`: otherwise the complementary one-edge arc makes `r` the same
physical edge as a `P_c` edge.  Both contradict `r in R_P`.  Let `A` be the
vertex set of the selected arc.  Then

1. the `P_d` edges on the arc perfectly match `A`;
2. `r` together with the intervening `P_c` edges is a colour-`c` supported
   perfect matching of `A`; and
3. `P_d` perfectly matches `V-A`.

The set `A` is nonempty, proper, and even.  Equation (4) forces one of

```text
haf(Z^c[A]),          haf(Z^d[V-A])                    (13)
```

to vanish despite its supported matching.

This conclusion holds for every `r`, every saturated support colour of `r`,
and either choice of the other colour.  For a fixed selected triple, the
disconnected-pair case and the all-pairs-Hamiltonian case are exhaustive.
Different selected triples may realize different forms, so no global
exclusivity is claimed.

Equations (7), (12), and (13) prove the announced all-degree localized
trichotomy.

## 3. The degree-free Hall-repair interface

There is a sharper consequence in the no-active-perfect-matching case.  Fix
a colour `c` as in Section 2.1 and use either fixed non-`c` bit to write the
global bipartition of `support(Z^c)` as `U,W`.  Choose any
inclusion-minimal Hall-deficient set `X subset U` for `E_c`, and put

```text
T=N_(E_c)(X).
```

Minimality gives

```text
|X|=|T|+1.                                             (14)
```

Indeed, deleting any `x in X` leaves a nondeficient set and gives
`|T|>=|X|-1`, while deficiency gives the reverse inequality.  The same
minimality shows that every `t in T` has at least two neighbours in `X`.

Every connected component of `E_c` is balanced bipartite: summing (5) over
its two shores gives equality of their cardinalities in characteristic zero.
Consequently `X` cannot be a union of whole active components.  The active
boundary

```text
F=E_c[T,U-X]                                           (15)
```

is nonempty.  Summing (5) first over `X` and then over `T` gives the exact
signed boundary identity

```text
sum_(e in F) s_e^c=|T|-|X|=-1.                         (16)
```

Now choose any `e={y,t} in F`, with `y in U-X` and `t in T`, and any nonzero
perfect-matching monomial in `C_e^c`.  Such a monomial exists because `e` is
active.  In that complementary matching let

```text
a = # edges from X to T-{t},
b = # edges from X to W-T,
q = # edges from U-X-{y} to T-{t}.
```

Matching the two shores yields

```text
a+b=|X|,
a+q=|T|-1=|X|-2,
b=q+2>=2.                                              (17)
```

Thus every such complementary matching contains at least two
vertex-disjoint repair edges from `X` to `W-T`.  Each repair edge `f` carries
a nonzero colour-`c` entry but is not active in colour `c`, by the definition
of `T`.  Active exclusivity prevents it from being active in either other
colour, so `f in H`.  Its inactivity and the two oriented two-point mixed
cuts give

```text
C_f^0=C_f^1=C_f^2=0.                                  (18)
```

The existence, vertex-disjointness, and common global cofactor zeros in
(17)--(18) are degree-free.  Under the additional hypothesis
`Delta(D)<=5`, every repair endpoint has `h>=1`; together with positive
active degree in the other two colours this prevents active degree three in
any colour.  Only this endpoint-degree consequence uses degree five.

The signed six-vertex double-star from the preceding degree-five theorem has
`q=0,b=2`.  It proves that (17) is sharp at the one-colour interface.  That
control is not a simultaneous three-colour all-bridge witness and does not
show that (18) is globally realizable.

## 4. The globally least core is bipartite at every degree

The universal saturated zero-layer theorem gives a nonmonochromatic
matching whose nonempty colour shores satisfy

```text
product_c haf(Z^c[V_c])=0,                             (19)
```

while each nonempty factor contains a nonzero supported matching monomial.
Hence there is at least one pair `(e,S)` such that

```text
empty != S proper-subset V,
|S| is even,
haf(Z^e[S])=0,
support(Z^e[S]) has a perfect matching.                (20)
```

Choose such a pair globally over all three colours and all eligible shores
with `|S|` least.  For `ij subset S`, put

```text
B_ij=Z^e_ij haf(Z^e[S-{i,j}]),
A_S={ij subset S : B_ij!=0}.                           (21)
```

The imported least-supported scalar cofactor theorem proves that `A_S`

1. is exactly the union of all support perfect matchings on `S`;
2. is connected and matching-covered;
3. has minimum degree at least two; and
4. is either one even cycle or a connected branching exchange core.

Every edge of `A_S` lies in `support(Z^e[S])`.  Every saturated colour-`e`
edge flips either fixed non-`e` bit, so that bit bipartitions the whole graph
`support(Z^e)`.  Therefore

```text
A_S is bipartite                                        (22)
```

without any degree assumption.  The previous degree-five proof bundled
bipartiteness with subcubicity; only subcubicity requires the degree bound.

## 5. Shore excess and the perfect-matching polytope

Let `U_S,W_S` be the bipartition of `A_S`, let each shore have size `m`, and
write

```text
beta=|E(A_S)|-|S|+1,
N=# perfect matchings of A_S.                          (23)
```

The shore sizes are equal because `A_S` has a perfect matching.  Since every
core degree is at least two,

```text
sum_(u in U_S)(deg(u)-2)
 =sum_(w in W_S)(deg(w)-2)
 =|E(A_S)|-2m=beta-1.                                  (24)
```

This is the exact shore-excess identity.  Every summand is a nonnegative
integer, so at every core vertex

```text
deg(v)<=beta+1.                                        (25)
```

### 5.1 Exact matching-polytope description

In the real edge-coordinate space of `A_S`, define

```text
Q={x>=0 : sum_(f incident with v) x_f=1 for every v}.  (26)
```

Then `Q` is exactly the convex hull of the incidence vectors of the perfect
matchings of `A_S`.

To see this without an integrality assumption, take `x in Q` and consider
its positive-support bipartite graph.  For every `Y subset U_S`,

```text
|Y|=sum_(u in Y)sum_(uw) x_uw
    <=sum_(w in N(Y))sum_(uw) x_uw=|N(Y)|.
```

Hall's theorem supplies a perfect matching `M` in the positive support.  Put
`epsilon=min_(f in M)x_f`.  If `epsilon=1`, the vertex equations force
`x=1_M`.  Otherwise

```text
x'=(x-epsilon 1_M)/(1-epsilon) in Q,
```

and at least one positive edge disappears.  Iteration terminates and writes
`x` as a convex combination of perfect-matching incidence vectors.  The
reverse inclusion is immediate.

The unsigned vertex-edge incidence matrix of a connected bipartite graph on
`2m` vertices has rank `2m-1`: a row dependence has coefficients satisfying
`alpha_u+alpha_w=0` on every edge, and connectedness leaves only the one
dependence which is constant on `U_S` and its negative on `W_S`.  Hence the
affine solution space of the vertex equations in (26) has dimension

```text
|E(A_S)|-(2m-1)=beta.                                  (27)
```

There is no hidden lower-dimensional face.  Since `A_S` is
matching-covered, the average of all its perfect-matching incidence vectors
is strictly positive on every edge.  It is therefore a relative-interior
point of (26), so

```text
dim Aff(Q)=beta.                                       (28)
```

A polytope of affine dimension `beta` needs at least `beta+1` points in any
convex generating set.  Consequently

```text
N>=beta+1.                                             (29)
```

This uses ordinary real convex geometry only on the finite incidence
vectors.  It does not change the characteristic-zero field of the hafnian
weights and introduces no unproved integrality premise.

### 5.2 Aggregate ports are forced below extremal degree

At a branch vertex `v`, put `d=deg_(A_S)(v)>=3`.  The imported cofactor-port
theorem partitions all `N` perfect matchings into the `d` nonempty incident
edge ports.  Every port sum is a nonzero restricted first cofactor.  If
`N=d`, every port is a singleton and the site is a sparse conformal `d`-fan.
If `N>d`, at least one port contains two or more matching monomials and its
aggregate remains nonzero.

Combining (25) and (29) gives the exact refinement

```text
d<=beta      => N>=beta+1>d => nonzero aggregate port;

sparse at v  => N=d and beta+1<=N=d<=beta+1
             => d=N=beta+1.                           (30)
```

Thus a sparse site can occur only at the extremal degree and matching count.
If `d=beta+1` but `N>beta+1`, an aggregate port still occurs.  The conclusion
is sitewise: a core can have an extremal sparse site and a lower-degree
aggregate site.

## 6. Degree-free rank strata and theta parity

### 6.1 Rank one

If `beta=1`, both shore excesses in (24) vanish.  Every core vertex has
degree two.  Connectedness makes `A_S` one even cycle.  It has exactly two
perfect matchings, and least-support minimality gives the inherited primitive
signed Laurent binomial relation.

### 6.2 Rank two

If `beta=2`, each shore in (24) has total excess one.  Hence exactly one
vertex in `U_S` and exactly one vertex in `W_S` has degree three, and every
other vertex has degree two.

The connected matching-covered core has no bridge.  Indeed, a bridge is
either in no perfect matching, contrary to matching-coveredness, or in every
perfect matching; in the latter case no other edge incident with either
endpoint can be allowed, contrary to minimum degree two.  Suppressing maximal
degree-two paths therefore gives three parallel routes between the two cubic
vertices.  The cubic vertices lie in opposite bipartition shores, so all
three routes have odd length.  Thus

```text
beta=2 => A_S is one closed all-odd theta.              (31)
```

It has exactly three perfect matchings, one for each route chosen to match
both cubic endpoints.  Their three nonzero monomials sum to zero.  No proper
nonempty subsum can vanish, since the remaining nonzero monomial would then
also vanish.  The least relation is therefore an exact support-minimal
trinomial, and

```text
N=3=beta+1.                                            (32)
```

No degree bound on `D` is used in either rank stratum.

### 6.3 The one-open-port theta is impossible in all-bridge cores

At any branch vertex and for any fixed core perfect matching `P`, choose any
two non-`P` exits.  The imported conformal-theta theorem constructs a theta
subdivision in `A_S`.  Abstractly its path parities are either

```text
odd/odd/odd,
odd/even/even.                                         (33)
```

The second profile contains two odd cycles, each formed by the odd path and
one even base arc.  It certifies a nonbipartite core.  Equation (22) excludes
it.  Therefore every two-exit theta carrier in an all-bridge least core is a
closed all-odd theta.  Its theta edge set has exactly three internal perfect
matchings and is matching-covered.

This last statement concerns the theta carrier.  It does **not** say that a
higher-rank core has only three perfect matchings or that the carrier is an
induced subgraph.  The generic one-open-port sharpness fixture remains valid
for the abstract port theorem; it simply lies outside the bipartite
all-bridge specialization.

## 7. What remains special to saturated degree five

Assume now `Delta(D)<=5`.  The inherited bound (6) makes
`Delta(D)=5`, and the preceding degree-five theorem supplies the following
additional conclusions.

1. The complete active/inactive local degree table has total degree at most
   five, and for every selected triple (9),
   `deg_(R_P)(v)=deg_D(v)-3<=2`.
2. At endpoints of the Hall repair edges in Section 3, no active colour can
   have degree three.
3. If `e` is the colour of the globally least core and `d,k` are the other
   colours, active exclusivity makes `support(Z^e)` disjoint from
   `E_d union E_k`.  Positive active degree then gives

   ```text
   deg_(support(Z^e))(v)
      <=deg_D(v)-deg_(E_d)(v)-deg_(E_k)(v)<=3.          (34)
   ```

   Hence the least core is subcubic in addition to being bipartite.
4. All core degrees are two or three.  If `t` is the number of cubic core
   vertices, handshaking gives

   ```text
   t=2(beta-1).                                        (35)
   ```

   Thus `beta>=3` gives at least four cubic sites.
5. At each cubic colour-`e` core site, five physically distinct saturated
   edges are forced: the three core edges and one incident edge from each of
   `E_d,E_k`.  The exact distinguished-colour local type is

   ```text
   (a_e,a_d,a_k;h)
      =(1,1,1;2), (2,1,1;1), or (3,1,1;0).             (36)
   ```

   The `3-a_e` core edges outside `E_e` lie in `H`, carry colour `e`, and
   have all three **global** pair-deletion cofactors zero, although their
   restricted least-core coefficients in (21) are nonzero.

The unconditional three off-diagonal singleton killers further give
`deg_G(v)>=deg_D(v)+3`; hence every cubic degree-five core site has full
support degree at least eight.  These degree-five conclusions remain valid
but are not inputs to the all-degree trichotomy, bipartiteness, polytope
dimension, or rank-one/rank-two classification.

## 8. Inherited results, new consequences, and exact boundary

The load-bearing inherited results are:

1. [`ALL_BRIDGE_ACTIVE_DECK_EXCLUSIVITY_AND_CUBIC_DIAGONAL_EXCLUSION.md`](ALL_BRIDGE_ACTIVE_DECK_EXCLUSIVITY_AND_CUBIC_DIAGONAL_EXCLUSION.md):
   score-one identities, active exclusivity, and active support;
2. [`ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FOUR_EXCLUSION.md`](ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FOUR_EXCLUSION.md):
   the unconditional `Delta(D)>=5` bound;
3. [`UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md`](UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md):
   the saturated bit-flip characterization and existence of a supported pure
   cancellation;
4. [`HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md`](HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md):
   the mixed complementary-product identity;
5. [`MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md`](MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md):
   the abstract least-cancellation core theorem;
6. [`MATRIX_UNIT_MINIMAL_PURE_COFACTOR_PORT_AGGREGATE_AND_CONFORMAL_FAN_REDUCTION_THEOREM.md`](MATRIX_UNIT_MINIMAL_PURE_COFACTOR_PORT_AGGREGATE_AND_CONFORMAL_FAN_REDUCTION_THEOREM.md):
   the port partition, sparse/aggregate dichotomy, and two theta profiles; and
7. [`ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FIVE_BRANCHING_OR_CANCELLATION_CORE_REDUCTION_THEOREM.md`](ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FIVE_BRANCHING_OR_CANCELLATION_CORE_REDUCTION_THEOREM.md):
   the Hall-repair argument, exact controls, and degree-five refinements.

The new content is the all-degree quantifier audit of the localized
trichotomy, the separation of degree-free bipartiteness from degree-five
subcubicity, exclusion of the one-open theta in the all-bridge specialization,
the shore-excess and matching-polytope bounds (24)--(30), and the resulting
degree-free rank-one/rank-two classification.

Exact sharpness controls delimit these conclusions:

- the signed double-star attains the two-repair bound but is only a
  one-colour control;
- an even cycle has `beta=1,N=2`;
- a closed all-odd theta has `beta=2,N=3`;
- the sparse `d`-route all-odd fan has `beta=d-1,N=d`, attaining the extremal
  equality in (30);
- the bipartite aggregate `K_(3,3)` core has `beta=4,N=6` and degree three,
  illustrating the forced aggregate side; and
- the abstract one-open theta is an exact nonbipartite least residual, so
  bipartiteness, not pure-cancellation algebra alone, is load-bearing in its
  all-bridge exclusion.

Focused exact checks:

```text
python -B claims/arbitrary-order/verify_all_bridge_active_deck_all_degree_localized_pure_cancellation_and_bipartite_core.py
python -B claims/arbitrary-order/audit_all_bridge_active_deck_all_degree_localized_pure_cancellation_and_bipartite_core.py
uv run --with ruff ruff check claims/arbitrary-order/verify_all_bridge_active_deck_all_degree_localized_pure_cancellation_and_bipartite_core.py claims/arbitrary-order/audit_all_bridge_active_deck_all_degree_localized_pure_cancellation_and_bipartite_core.py
python -m py_compile claims/arbitrary-order/verify_all_bridge_active_deck_all_degree_localized_pure_cancellation_and_bipartite_core.py claims/arbitrary-order/audit_all_bridge_active_deck_all_degree_localized_pure_cancellation_and_bipartite_core.py
```

The primary program checks the selected-matching component and Hamiltonian
arc interfaces, the Hall count, shore excess, matching-polytope dimensions,
port counts, rank-one/rank-two strata, and sharp controls.  The independent
program reconstructs those finite interfaces without importing the primary
implementation.  These programs check exact finite and combinatorial
interfaces; the written arbitrary-order arguments above are the proof.

```text
all-bridge active-deck localized trichotomy, all Delta(D): PROVED EXHAUSTIVE;
no-active-PM inactive-edge complements/common cofactors:   PROVED;
minimal Hall shore two vertex-disjoint repairs:            PROVED, SHARP;
globally least all-bridge pure core bipartite:              PROVED;
one-open-port theta inside that core:                       EXCLUDED;
matching-polytope dimension beta and N>=beta+1:             PROVED;
d<=beta branch site has a nonzero aggregate port:           PROVED;
sparse branch site only at d=N=beta+1:                      PROVED;
beta=1 even cycle / beta=2 closed all-odd theta:             PROVED;
impossibility of the three localized forms:                 OPEN;
impossibility of all bipartite least-core strata:            OPEN;
deeper-blocker branch:                                      OPEN;
universal extraction/gluing:                                NOT PROVED;
global Krenn--Gu conjecture:                                UNRESOLVED.
```
