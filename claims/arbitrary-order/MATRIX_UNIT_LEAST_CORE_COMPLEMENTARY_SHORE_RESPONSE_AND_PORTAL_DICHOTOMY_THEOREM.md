# Matrix-unit least-core complementary-shore response and portal dichotomy

## Status and exact scope

This is an exact arbitrary-order reduction over characteristic zero in the
simultaneous balanced all-bridge specialization of the `r=1` matrix-unit
branch.  It starts with the globally least supported pure hafnian
cancellation and its connected bipartite matching-covered first-cofactor core
from the all-degree theorem.

Three complementary interfaces are proved.

1. Every allowed edge of the least core exposes a nonzero deletion cofactor.
   The mixed-cut identity then forces a zero hafnian on the shore obtained by
   adjoining that edge's endpoints to the complementary vertex set, in each
   of the other two colours.  If one of those zero shores is support-matchable,
   global leastness gives the exact size landing

   ```text
   2|S| <= n+2,
   ```

   and a conformally minimal pure relation on the response shore embeds
   termwise in one mixed target fibre.
2. Across every core edge, the two endpoint neighbour sets in either other
   active-deck graph are nonempty and disjoint.  This gives a response-shore
   matching whenever both endpoints have exterior active neighbours and the
   remainder of the complement is matchable.  It does **not** force those
   neighbours outside the least shore: the active colour's own normal bit is
   free.  In a co-two exterior with `|S|>=6`, the vertices having an exterior
   active neighbour therefore form only an independent set in the core.
3. In the original colour, either the complement of the least shore is
   matchable and the least relation completes termwise into the pure target
   fibre, or every full matching crosses the cut.  A full matching with the
   minimum number of crossing edges then determines a balanced finite portal.
   Alternating-path switching proves that every nonempty union of its induced
   portal pairs has an unmatchable image on the complementary side.

The first interface turns the inherited mixed-cut product into an edgewise
family indexed by the entire allowed core.  The second proves the exact
active-neighbour separation while recording why active degree alone does not
supply exterior portals.  The third records the exact support obstruction
when same-colour conformal completion fails.  These interfaces do not force a
response shore to be matchable, exclude the co-two exterior, bound the number
of portals by two, produce a target-lattice unit, exclude an aggregate port,
or close the deeper-blocker branch.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

No graph-family enumeration or search is used.  The arbitrary-order proof is
the hafnian product identity, global leastness, and matching switches along
alternating paths.

## 1. Imported all-bridge data

Let `V` have even size `n>=6`.  For each colour `c in {0,1,2}`, let `Z^c`
be the hollow symmetric saturated-diagonal matrix and write

```text
h_c(T)=haf(Z^c[T]),          h_c(empty)=1.             (1)
```

The simultaneous balanced all-bridge branch supplies

```text
h_c(V)=1                                                     (2)
```

for every colour and the mixed complementary-product identity

```text
h_c(T) h_d(V-T)=0                                           (3)
```

for distinct colours `c,d` and every nonempty proper even `T subset V`.
Every support graph `support(Z^c)` is bipartite, with its bipartition fixed by
either normal-type bit different from `c`.

Choose globally, over all colours and all nonempty proper even shores, a pair
`(e,S)` of minimum `|S|` such that

```text
h_e(S)=0,
support(Z^e[S]) has a perfect matching.                     (4)
```

Put

```text
C=V-S.                                                       (5)
```

For every pair `f={i,j} subset S`, define

```text
B_f=Z_f^e h_e(S-f),
A={f subset S:B_f!=0}.                                      (6)
```

The imported least-core theorem says that `A` is exactly the union of all
support perfect matchings on `S`.  It is connected, matching-covered, and
bipartite.  In particular, every `f in A` is allowed and satisfies

```text
Z_f^e!=0,             h_e(S-f)!=0.                          (7)
```

Also `|S|>=4`, because a supported two-vertex hafnian cannot vanish.

## 2. Edgewise complementary-shore response

### Theorem 1 (allowed-edge response family)

For every allowed core edge `f in A` and every other colour `d!=e`, put

```text
T_(d,f)=C union f.                                          (8)
```

Then

```text
h_d(T_(d,f))=0.                                             (9)
```

Exactly one of the following support alternatives holds for each pair
`(d,f)`.

1. `support(Z^d[T_(d,f)])` has no perfect matching.
2. It has a perfect matching.  Then `T_(d,f)` is a supported pure
   cancellation and

   ```text
   |S| <= |T_(d,f)|=n-|S|+2,
   2|S| <= n+2.                                            (10)
   ```

   Moreover, there is a conformally minimal supported pure `d`-relation
   inside `T_(d,f)` which embeds termwise in the complete mixed target fibre
   whose word is `d` on `T_(d,f)` and `e` on `S-f`.

Consequently, if

```text
2|S|>n+2,                                                  (11)
```

then every one of the `2|E(A)|` response shores in (8) is support-
unmatchable.  At equality in (10), any supported response shore is itself a
globally least-size cancellation.

### Proof

Fix `f in A`.  The set `S-f` is nonempty, proper, and even: `|S|>=4`, while
`S` is a proper subset of `V`.  Apply (3) with

```text
c=e,            T=S-f.
```

Its complementary shore is

```text
V-(S-f)=C union f=T_(d,f).
```

Thus

```text
h_e(S-f) h_d(C union f)=0.                                (12)
```

The first factor is nonzero by (7).  Since the coefficient field is a field,
(9) follows.

If the support on `T_(d,f)` has a perfect matching, then (9) makes it an
eligible supported zero in the global minimization which selected `S`.
Therefore `|S|<=|T_(d,f)|`, which is exactly (10).  If (11) holds, this
alternative is impossible for every `d,f`.

For the attachment statement, assume the response shore is supported.  Call
an even `R subset T_(d,f)` conformally admissible when

```text
h_d(R)=0;
support(Z^d[R]) has a perfect matching;
support(Z^d[T_(d,f)-R]) has a perfect matching.             (13)
```

The full set `T_(d,f)` is admissible, using the empty matching on its
complement.  Choose an admissible `R` of least size.  The imported
conformally minimal theorem makes its first-cofactor graph connected and
matching-covered and gives its primitive-cycle / sparse-fan / nonzero-
aggregate-port trichotomy.

Fix a support perfect matching `Q` on `T_(d,f)-R`.  Since `h_e(S-f)!=0`, fix
a nonzero support perfect matching `P` on `S-f`.  For every support perfect
matching `M` on `R`,

```text
M_hat=M union Q union P                                  (14)
```

is a full physical matching.  All such unions induce the same word: colour
`d` on `T_(d,f)` and colour `e` on `S-f`.  Their weights satisfy

```text
sum_M lambda(M_hat)
  =lambda(Q)lambda(P) h_d(R)=0,                           (15)
```

and for any two residual matchings `M,N`,

```text
1_(M_hat)-1_(N_hat)=1_M-1_N.                              (16)
```

This proves the exact termwise attachment and preservation of matching-
exponent differences.  It is a cancelling diagonal subrelation inside the
complete mixed fibre; offdiagonal terms elsewhere in that fibre need not be
absent.

Global leastness also gives `|R|>=|S|`, while `R subset T_(d,f)`.  At equality
in (10), these inequalities force `R=T_(d,f)`, proving the last claim.  QED.

## 3. Active-neighbour separation and the exterior-portal boundary

The response zeros in Theorem 1 are algebraic.  Active-score positivity adds
one exact local restriction, but it does not by itself support a response
shore.

### Theorem 2 (separation and conditional exterior portal)

Fix `d!=e` and let `k` be the third colour.  For every core edge `xy in A`,

```text
N_(E_d)(x) intersect N_(E_d)(y)=empty.                    (17)
```

Both neighbour sets are nonempty.  If there are exterior vertices

```text
r_x in N_(E_d)(x) intersect C,
r_y in N_(E_d)(y) intersect C,                            (18)
```

then `r_x!=r_y`, and the two active edges form a nonzero colour-`d` support
matching on `{x,y,r_x,r_y}`.  If the remaining support on

```text
C-{r_x,r_y}                                               (19)
```

has a colour-`d` perfect matching, then `C union {x,y}` is a supported
response shore and every conclusion of Theorem 1 applies.

Suppose in particular that `|C|=2` and `|S|>=6`.  Define

```text
P_d={x in S:N_(E_d)(x) intersect C is nonempty}.          (20)
```

Then `P_d` is an independent set in the least core `A`.  Thus the co-two
exterior is not excluded: every core edge must merely have at least one
endpoint whose colour-`d` active neighbours all remain in `S`, for each
`d!=e`.

### Proof

Every edge of `E_d` has a nonzero saturated colour-`d` entry and therefore
flips the normal bit `b_k`.  A core edge is a saturated colour-`e` edge and
also flips `b_k`.  If a vertex `r` belonged to both neighbour sets in (17),
then the two colour-`d` edges would give

```text
b_k(r)=1-b_k(x)=1-b_k(y),                                (21)
```

so `b_k(x)=b_k(y)`, contradicting the colour-`e` transition on `xy`.  This
proves (17).  The active-score identity makes every `E_d` spanning with
positive minimum degree, proving nonemptiness of the two full neighbour sets.

If the exterior neighbours in (18) exist, (17) makes them distinct.  Deck
activity includes `Z^d_(x r_x)!=0` and `Z^d_(y r_y)!=0`.  Adjoining a matching
on (19) therefore makes `C union {x,y}` support-matchable in colour `d`, and
Theorem 1 applies.

When `|C|=2`, two adjacent vertices of `P_d` would have distinct exterior
active neighbours by (17), hence would use both vertices of `C`.  The empty
matching completes their two active edges to a support perfect matching on
the four-set `C union {x,y}`.  Theorem 1 makes that four-set a supported pure
zero.  For `|S|>=6` this contradicts the global minimality of `S`.  Therefore
`P_d` is independent.  QED.

### The own-bit freedom is load-bearing

For a saturated colour-`c` transition, the two bits other than `b_c` must
flip, but the value of `b_c` at the other endpoint is unrestricted.  Hence,
although

```text
q=b_d xor b_k                                             (22)
```

is constant along the connected colour-`e` core, a colour-`d` edge need not
flip `q`: it flips `b_k` but may also flip its own bit `b_d`.  For example,
with `e=0,d=1,k=2`, the colour-`d` transition

```text
000 -> 111                                                (23)
```

flips the required bits `b_0,b_2`, also flips `b_1`, and preserves
`b_1 xor b_2`.  Thus no conclusion

```text
N_(E_d)(x) subset C
```

is available.  Opposite-colour active edges may remain inside `S`, and
neither active degree nor (17) excludes a co-two exterior.  This explicit
boundary prevents the conditional portal in (18)--(19) from being promoted
to an unconditional one.

## 4. Same-colour completion or a minimum-crossing portal

The response theorem uses the two colours other than `e`.  There is a
separate exact dichotomy in colour `e` itself.

### Theorem 3 (conformal completion / portal obstruction)

Exactly one of the following holds.

#### I. Same-colour conformal completion

The support on `C` has a perfect matching `Q`.  Then every support perfect
matching `N` of the least core completes to the full pure-`e` target fibre as

```text
N_hat=N union Q.                                         (26)
```

The map is injective,

```text
sum_N lambda(N_hat)=lambda(Q)h_e(S)=0,                    (27)
```

and all matching-exponent differences are preserved.

#### II. A balanced minimum-crossing portal

The support on `C` has no perfect matching.  Since `h_e(V)=1`, the full
support graph `support(Z^e)` has at least one perfect matching.  Choose one,
`M`, with the minimum number `k` of edges crossing the cut `(S,C)`.  Then

```text
k>=2 is even.                                             (28)
```

Let `P subset S` and `Q subset C` be the endpoints of the crossing edges and
write the unique decomposition

```text
M=R union X union L,                                      (29)
```

where `R` matches `S-P`, `L` matches `C-Q`, and `X` is the crossing matching
from `P` to `Q`.  If `U,W` are the two bipartition shores of the global
colour-`e` support, then

```text
|P intersect U|=|P intersect W|=k/2.                     (30)
```

For every perfect matching `N` of the least core, delete common edges from
`N union R`.  The remaining components are alternating even cycles and
exactly `k/2` vertex-disjoint odd alternating paths whose endpoint pairs
partition `P`.  Call this path family `Pi_N`.

For any nonempty subfamily `J subset Pi_N`, let `P_J` be the union of its
endpoint pairs and put

```text
Q_J=X(P_J).                                               (31)
```

Then

```text
support(Z^e[Q_J]) has no perfect matching.                (32)
```

In particular, the two complementary portal endpoints associated with each
individual path are not joined by a colour-`e` support edge.  If an allowed
core edge `f` has both endpoints in `P`, choose a core perfect matching
containing `f`.  The edge `f` is then a one-edge member of `Pi_N`, and the
corresponding pair `X(f)` is absent from `support(Z^e)`.

### Proof

In case I, (26)--(27) follow by disjoint union and multiplicativity of
matching weights.  The completed relation is a zero subrelation inside the
pure coefficient `h_e(V)=1`; other full pure matchings compensate it, so no
contradiction follows.

Assume case II.  A matching crosses any even vertex set in an even number of
edges.  Since a zero-crossing full matching would restrict to a perfect
matching on `C`, minimality and unmatchability give (28).

The global colour-`e` support is bipartite.  The least core has a perfect
matching, so `S` contains equally many vertices of `U` and `W`.  The partial
matching `R` matches all of `S-P` internally.  Equality of the unmatched
bipartition counts gives (30).

Fix a core perfect matching `N`.  In the symmetric difference of `N` and
the partial matching `R`, every vertex of `S-P` has degree zero or two and
every vertex of `P` has degree one.  Hence the nontrivial components are
alternating cycles and paths pairing the vertices of `P`.  Every path starts
and ends with an edge of `N`, so it has odd length and joins opposite
bipartition shores.  This proves the asserted decomposition.

Suppose, contrary to (32), that a nonempty `Q_J` has a support perfect
matching `Y`.  Starting from `M`, perform the following simultaneous switch:

1. remove the `R`-edges on every path in `J`;
2. remove the `X`-edges incident with `P_J`;
3. add the `N`-edges on every path in `J`; and
4. add the matching `Y` on `Q_J`.

Alternation keeps all internal path vertices matched.  The added `N`-edges
match the vertices of `P_J` internally in `S`, while `Y` matches their former
partners internally in `C`.  Every other edge of `M` is unchanged.  The
result is therefore a full support perfect matching with

```text
k-|P_J| < k                                               (33)
```

crossing edges, contradicting the choice of `M`.  Thus (32) holds.

If `f subset P` is an allowed core edge, matching-coveredness supplies a core
perfect matching `N` containing it.  No edge of `R` meets `P`, so `f` is a
one-edge alternating path in `Pi_N`.  Applying (32) to that path proves the
last assertion.  QED.

## 5. Other-colour portal trigger

The edgewise response family becomes active as soon as a full matching of
another colour crosses the least shore through one allowed pair.

### Corollary 4 (zero-portal or aligned two-portal attachment)

Fix `d!=e` and a full support perfect matching `K` of `Z^d[V]`, which exists
because `h_d(V)=1`.

1. If `K` has no edge crossing `(S,C)`, its restriction to `C` completes the
   original least relation on `S` termwise into the mixed target word which
   is `e` on `S` and `d` on `C`.
2. If `K` has exactly two crossing edges and their two endpoints in `S` form
   an allowed core edge `f in A`, then `K|_(C union f)` is a support perfect
   matching of `T_(d,f)`.  Theorem 1 supplies the response zero, the size
   bound (10), and the conformally minimal mixed-fibre attachment (14)--(16).
3. Otherwise this argument stops at a multiportal or nonaligned two-portal
   boundary: the crossing number is at least four, or the two endpoints in
   `S` do not form an allowed edge of the least core.

### Proof

Every full matching crosses the even set `S` an even number of times.  In the
zero-crossing case, its restriction to `C` is a fixed support matching and
the same multiplicative proof as (27), with two different colours on the two
shores, gives the attachment.

In the two-crossing case, all vertices of `S-f` are matched internally by
`K`; the two vertices of `f` are matched across to `C`; and every remaining
vertex of `C` is matched internally.  Thus the edges of `K` contained in
`C union f` form a perfect matching of that response shore.  Theorem 1
applies.  The final alternative is the exhaustive complement of the first
two cases.  QED.

The corollary does not say that an arbitrary full or active matching has at
most two portals or that a two-portal endpoint pair must be allowed.  Those
are the nearest open support-theoretic obligations.

## 6. Exact proof-topology consequence

The new decision surface is

```text
globally least all-bridge pure core (e,S)
    -> every allowed f and d!=e:
         h_d((V-S) union f)=0

         -> supported response shore
              -> 2|S|<=n+2
              -> conformally minimal cycle / fan / aggregate relation
                 attached termwise in one mixed target fibre;

         -> unsupported response shore
              -> exact support obstruction;

    -> every core edge xy and d!=e:
         N_(E_d)(x) and N_(E_d)(y) are nonempty and disjoint
         -> if both have exterior neighbours and the remainder is matchable:
              supported response shore as above
         -> if |V-S|=2 and |S|>=6:
              exterior-neighbour vertices form an independent set in A
              (co-two exterior remains open);

    -> colour-e complement matchable
         -> original least relation completes into the pure target fibre;

    -> colour-e complement unmatchable
         -> balanced minimum-crossing portal
         -> every induced nonempty portal-pair union is unmatchable.
```

For either other colour, a zero-portal matching enters the first completion
interface, while an aligned two-portal matching enters the edgewise response
interface.  What remains is no longer an unspecified use of the mixed cuts:
one must force support on a response shore, control a multiportal/nonaligned
matching, use the finite portal obstruction family, or exit through the
existing pure/deeper topology.

This result does not identify the globally least core with one of the
active-deck localized cuts.  It does not prove that two edgewise response
families interact non-directly in the target lattice.  Shared physical
variables do not establish such interaction.

## 7. Assumptions and exact boundary

```text
field:                                                   characteristic zero;
physical branch:                                         simultaneous balanced all-bridge;
full pure coefficients h_c(V):                           exactly 1;
mixed complementary-product identity:                    IMPORTED;
globally least supported pure cancellation:               IMPORTED;
least core connected/bipartite/matching-covered:           IMPORTED;
allowed-edge deletion cofactors nonzero:                  IMPORTED;
edgewise opposite-colour response zeros:                  PROVED;
supported-response size bound 2|S|<=n+2:                  PROVED;
supported response gives conformally minimal attachment:  PROVED;
large-shore response family support-unmatchable:           PROVED;
active neighbour sets across every core edge disjoint:     PROVED;
exterior active pair plus remainder matching gives response: PROVED;
co-two exterior-neighbour vertices independent for |S|>=6: PROVED;
opposite-colour active neighbours necessarily leave S:     NOT PROVED;
co-two exterior with |S|>=6 excluded:                       UNKNOWN;
same-colour completion / minimum portal dichotomy:         PROVED;
all induced portal-pair unions support-unmatchable:         PROVED;
zero-/aligned-two-portal other-colour trigger:              PROVED;
some response shore support-matchable:                     UNKNOWN;
every other-colour matching has at most two portals:        UNKNOWN;
every two-portal endpoint pair is allowed:                 UNKNOWN;
portal obstruction forces a target-lattice unit:           UNKNOWN;
aggregate-port or extremal-sparse branch excluded:          UNKNOWN;
localized active-deck cut equals globally least core:       UNKNOWN;
deeper-blocker branch excluded:                             UNKNOWN;
global Krenn--Gu conjecture:                                UNRESOLVED.
```

The attachment statements concern exact cancelling subrelations in complete
target fibres.  They do not assert that those subrelations generate the full
target equations, that the remaining offdiagonal terms vanish, or that a
proper relation is a unit certificate.

## 8. Evidence and replay

Run:

```powershell
python claims/arbitrary-order/verify_matrix_unit_least_core_complementary_shore_response_and_portal_dichotomy.py
python -I claims/arbitrary-order/audit_matrix_unit_least_core_complementary_shore_response_and_portal_dichotomy.py
python -m py_compile claims/arbitrary-order/verify_matrix_unit_least_core_complementary_shore_response_and_portal_dichotomy.py claims/arbitrary-order/audit_matrix_unit_least_core_complementary_shore_response_and_portal_dichotomy.py
uv run --with ruff==0.16.2 ruff check claims/arbitrary-order/verify_matrix_unit_least_core_complementary_shore_response_and_portal_dichotomy.py claims/arbitrary-order/audit_matrix_unit_least_core_complementary_shore_response_and_portal_dichotomy.py
```

The primary verifier uses closed exact `2 x 2` and `3 x 3` permanent formulas
to replay two hand-constructed rational controls: one with same-colour
conformal completion and one with an unmatchable complement and a minimum
two-crossing portal.  It checks the least four-vertex cancellation, all
allowed deletion cofactors, the completed zero subrelation, the nonzero full
coefficient, and both alternating portal paths.  A direct normal-bit table
also keeps both allowed values of the active colour's own bit, verifies the
shared-neighbour separation in (17), and replays the allowed `000 -> 111`
counter-transition to unconditional exterior forcing.

The independent audit imports neither repository code nor the primary
verifier.  It converts the same controls to hollow symmetric matrices and
uses a separate exact hafnian recursion, integer-mask transition sets, and
direct matching-switch checks.
The scripts perform no graph-family enumeration and no witness search.  They
audit the displayed mechanisms and sharpness boundary; the arbitrary-order
result is the proof above.
