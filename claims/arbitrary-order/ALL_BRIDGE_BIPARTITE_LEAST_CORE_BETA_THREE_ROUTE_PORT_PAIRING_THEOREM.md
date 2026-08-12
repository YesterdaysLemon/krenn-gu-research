# All-bridge bipartite least-core beta-three route-port pairing theorem

## Status and exact scope

This is an exact characteristic-zero refinement of the rank-three extremal-
sparse branch in the simultaneous balanced all-bridge reduction.  Let
`(e,S)` be globally least, over all colours and all nonempty proper even
shores supporting a pure cancellation, and let `A` be its connected
bipartite matching-covered first-cofactor core.  Assume

```text
beta(A)=3
```

and that `A` has an extremal sparse quartic site `v`.  The preceding
opposite-shore theorem then gives exactly the `Q/Q` or `Q/C^2` suppressed
route kernel and exactly four perfect matchings.

This theorem identifies the matching ports at the two ends of every route.
On an odd route the endpoint ports are the same set.  On an even route they
are disjoint complementary sets.  Consequently:

1. in the `Q/Q` kernel, each odd route pairs the same singleton port at the
   two quartic sites, and the two endpoint port contributions are the same
   nonzero full perfect-matching monomial;
2. in the `Q/C^2` kernel, the four odd routes pair four singleton ports, while
   the unique even route has complementary doubleton endpoint ports.  Those
   two doubleton port contributions are nonzero and exact negatives.

The word **contribution** is load-bearing.  For a core edge `f=ab`, the port
quantity is

```text
C_f=z_f haf(Z^e[S-{a,b}]),
```

including the edge weight `z_f`.  No equality or negation of the bare
deletion hafnians is asserted.

This is a pure least-core refinement, not an exclusion.  It does not attach
either paired port to a mixed target fibre, prove algebraic independence,
produce a simultaneous all-bridge witness, or resolve the global conjecture.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Imported core and weighted port notation

Write

```text
h(T)=haf(Z^e[T]),             h(empty)=1,
h(S)=0,
```

although `support(Z^e[S])` has a perfect matching.  For `f=ab subset S`, put

```text
z_f=Z^e_ab,
C_f=z_f h(S-{a,b}),
A={f subset S:C_f!=0}.                                (1)
```

The least-core theorem identifies `A` with the union of all support perfect
matchings on `S`.  Thus its perfect matchings are exactly the support perfect
matchings contributing to `h(S)`.  For `M in PM(A)`, define its nonzero full
matching monomial

```text
lambda(M)=product_(f in M) z_f.                        (2)
```

At a vertex `p` and an incident core edge `f`, write

```text
P(p,f)={M in PM(A):f in M}.                            (3)
```

The imported U7I port theorem gives the exact identities

```text
C_f=sum_(M in P(p,f)) lambda(M) !=0,                  (4)

{P(p,f):f incident with p} partitions PM(A).          (5)
```

Equation (4) is independent of which endpoint of `f` is used to name its
port.  It is a full-matching identity: multiplication by `z_f` adjoins `f`
to every complementary matching in the deletion hafnian.

The imported A4 theorem supplies

```text
N=#PM(A)=4,          deg_A(v)=4,                       (6)
```

and exactly one of the `Q/Q` and `Q/C^2` route kernels described below.

## 2. Route-state lemma

Suppress the maximal paths whose internal vertices have degree two.  Let

```text
R=(r_0,r_1,...,r_l)
```

be one resulting route, with branch endpoints `p=r_0` and `q=r_l`.  Its
endpoint edges are

```text
f_p(R)=r_0r_1,              f_q(R)=r_(l-1)r_l.         (7)
```

When `l=1`, these are two endpoint incidences of the same physical edge; all
paired-port conclusions below are then tautological at that route.

### Lemma 1 (route endpoint states)

For every `M in PM(A)`:

1. if `l` is odd, then `M` uses both endpoint edges of `R` or neither;
2. if `l` is even, then `M` uses exactly one endpoint edge of `R`.

Consequently,

```text
l odd:
  P(p,f_p(R))=P(q,f_q(R));                             (8)

l even:
  P(p,f_p(R)) disjoint-union P(q,f_q(R))=PM(A).        (9)
```

### Proof

For `1<=i<=l`, let `t_i` be one when the route edge `r_(i-1)r_i` belongs to
`M`, and zero otherwise.  Every internal route vertex `r_i`,
`1<=i<=l-1`, has degree two in `A` and must be covered exactly once by `M`.
Therefore

```text
t_i+t_(i+1)=1              for 1<=i<=l-1.             (10)
```

The sequence alternates.  Hence `t_l=t_1` when `l` is odd and
`t_l=1-t_1` when `l` is even.  These are precisely the two asserted route
states, and (8)--(9) follow by ranging over all perfect matchings.  QED.

### Corollary 2 (weighted endpoint-port identities)

For an odd route `R`,

```text
C_(f_p(R))=C_(f_q(R))
  =sum_(M in P(p,f_p(R))) lambda(M) !=0.               (11)
```

For an even route `R`,

```text
C_(f_p(R))+C_(f_q(R))
  =sum_(M in PM(A)) lambda(M)
  =h(S)=0,                                             (12)
```

and both summands in (12) are nonzero.

### Proof

For an odd route, substitute the common port set (8) into the U7I identity
(4).  For an even route, substitute the disjoint cover (9).  The perfect
matchings of `A` are exactly the support perfect matchings contributing to
`h(S)`, so their full monomial sum is zero.  Finally, both route endpoint
edges lie in `A`, and (4) makes each corresponding contribution nonzero.
QED.

Equation (11) does not imply

```text
h(S-endpoints(f_p(R)))=h(S-endpoints(f_q(R))).
```

It says only that these bare deletion hafnians become equal after
multiplication by their respective endpoint-edge weights.  The same warning
applies to the negation in (12).

## 3. The `Q/Q` singleton pairing

Assume the A4 kernel is `Q/Q`.  Let `w` be the opposite quartic site and let

```text
R_1,R_2,R_3,R_4
```

be the four internally disjoint odd `v`--`w` routes.  Put

```text
a_i=f_v(R_i),             b_i=f_w(R_i).                (13)
```

### Theorem 3

There are four distinct perfect matchings `M_1,...,M_4` such that, after
indexing by the route selected at `v`,

```text
P(v,a_i)=P(w,b_i)={M_i},                               (14)

C_(a_i)=C_(b_i)=lambda(M_i)!=0                         (15)
```

for every `1<=i<=4`.  The four singleton sets in (14) partition `PM(A)`, and

```text
lambda(M_1)+lambda(M_2)+lambda(M_3)+lambda(M_4)=0.     (16)
```

### Proof

The four nonempty incident ports at the sparse quartic site `v` partition the
four perfect matchings, so each is a singleton and the four singletons are
distinct.  Every route is odd, and Lemma 1 pairs its endpoint port at `v`
with its endpoint port at `w`.  Equation (4) turns the common singleton into
the common nonzero contribution (15).  Summing the four full matching
monomials gives `h(S)=0`, proving (16).  QED.

This proves equality of the two full contributions paired along a route.  It
does not identify the two endpoint edge weights or their bare deletion
hafnians.

## 4. The `Q/C^2` singleton/doubleton pairing

Assume the A4 kernel is `Q/C^2`.  Let `x,y` be the two cubic sites opposite
the sparse quartic site `v`.  Label the two odd routes from `v` to `x` by

```text
R_x1,R_x2,
```

the two odd routes from `v` to `y` by

```text
R_y1,R_y2,
```

and the unique even `x`--`y` route by `E`.  Write

```text
a_xi=f_v(R_xi),       b_xi=f_x(R_xi),
a_yj=f_v(R_yj),       b_yj=f_y(R_yj),                 (17)

g_x=f_x(E),           g_y=f_y(E).                     (18)
```

### Theorem 4

There are four distinct perfect matchings

```text
M_x1,M_x2,M_y1,M_y2
```

such that the four odd routes give the paired singleton ports

```text
P(v,a_xi)=P(x,b_xi)={M_xi}       for i=1,2,
P(v,a_yj)=P(y,b_yj)={M_yj}       for j=1,2,            (19)
```

and hence

```text
C_(a_xi)=C_(b_xi)=lambda(M_xi)!=0,
C_(a_yj)=C_(b_yj)=lambda(M_yj)!=0.                     (20)
```

The endpoint ports of the even route are exactly

```text
P(x,g_x)={M_y1,M_y2},
P(y,g_y)={M_x1,M_x2}.                                  (21)
```

In particular, they are disjoint complementary doubletons, and their full
matching contributions satisfy

```text
C_(g_x)=lambda(M_y1)+lambda(M_y2)!=0,
C_(g_y)=lambda(M_x1)+lambda(M_x2)!=0,                  (22)

C_(g_x)=-C_(g_y).                                      (23)
```

Thus the aggregate port at each cubic site is not merely known to exist: it
is exactly the endpoint port of the unique even route.  The two aggregates
are linked by one exact linear dependence, not proved independent.

### Proof

As in the `Q/Q` case, the four ports at sparse `v` partition four perfect
matchings and therefore give four distinct singletons.  The four `v`-incident
routes are odd, so Lemma 1 pairs their far endpoint ports with those
singletons.  This proves (19), and U7I equation (4) proves (20).

At `x`, the three incident ports are the two singleton ports
`{M_x1},{M_x2}` and the port on `g_x`.  They partition all four matchings, so

```text
P(x,g_x)=PM(A)-{M_x1,M_x2}={M_y1,M_y2}.
```

The same argument at `y` gives the other equality in (21).  Equivalently,
Lemma 1 says directly that the two endpoint ports of the even route are
disjoint and cover `PM(A)`.  They are therefore complementary doubletons.

Substitution into (4) gives (22), including both nonvanishing statements.
Finally, the disjoint union in (21) is all of `PM(A)`, whose full monomial sum
is `h(S)=0`.  This gives (23).  QED.

The exact-negative relation is between

```text
z_(g_x) h(S-endpoints(g_x))
and
z_(g_y) h(S-endpoints(g_y)).
```

It supplies no equality of the bare deletion hafnians and no relation between
the edge weights beyond their displayed weighted product identity.

## 5. Exact scalar controls

The A4 controls sharply realize both port-pairing patterns at pure least-core
level.

### 5.1 Four-route `Q/Q`

Take four length-three routes between two quartic sites.  Give all edge
weights one except the final edge of the fourth route, which has weight
`-3`.  The four perfect matchings select the four odd routes and have full
contributions

```text
1,1,1,-3.
```

At the two ends of each route, the paired singleton port has the same listed
contribution.  Their sum is zero, and every proper supported pure hafnian is
nonzero.  This realizes Theorem 3 as an exact characteristic-zero least
residual.

### 5.2 Eight-vertex `Q/C^2`

Use the A4 bipartite control with rows, in column order
`w_0,w_1,w_2,w_3`,

```text
u_0: 1111,
u_1: 0101,
u_2: 1010,
u_3: 1100,
```

set `z_(u_0w_0)=-3`, and give every other supported edge weight one.  The
four full matching contributions are `-3,1,1,1`.  Suppression gives two odd
routes from `u_0` to each of `w_0,w_1` and the even route
`w_0--u_3--w_1`.  Its endpoint ports have contributions

```text
C_(w_0u_3)=1+1=2,
C_(u_3w_1)=-3+1=-2.                                   (24)
```

The two ports are complementary doubletons, exactly as in Theorem 4.  Every
proper supported pure hafnian is nonzero.  This realizes the pairing and
exact-negative relation while showing that neither is a pure-topological
exclusion.

These controls are hollow symmetric scalar matrices.  They do not provide
the other two colours, the active decks, mixed-cut equations, target
attachment, or a simultaneous all-bridge witness.

## 6. Dependencies and evidence contract

The load-bearing inputs are exactly:

1. [`MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md`](MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md):
   the allowed-core identity and equality between core perfect matchings and
   support perfect matchings of the least residual;
2. [`MATRIX_UNIT_MINIMAL_PURE_COFACTOR_PORT_AGGREGATE_AND_CONFORMAL_FAN_REDUCTION_THEOREM.md`](MATRIX_UNIT_MINIMAL_PURE_COFACTOR_PORT_AGGREGATE_AND_CONFORMAL_FAN_REDUCTION_THEOREM.md):
   the U7I port partition and the nonzero weighted identity (4);
3. [`ALL_BRIDGE_ACTIVE_DECK_ALL_DEGREE_LOCALIZED_PURE_CANCELLATION_AND_BIPARTITE_CORE_REDUCTION_THEOREM.md`](ALL_BRIDGE_ACTIVE_DECK_ALL_DEGREE_LOCALIZED_PURE_CANCELLATION_AND_BIPARTITE_CORE_REDUCTION_THEOREM.md):
   global least-core selection and all-bridge bipartiteness; and
4. [`ALL_BRIDGE_BIPARTITE_LEAST_CORE_EXTREMAL_SPARSE_OPPOSITE_SHORE_DICHOTOMY_THEOREM.md`](ALL_BRIDGE_BIPARTITE_LEAST_CORE_EXTREMAL_SPARSE_OPPOSITE_SHORE_DICHOTOMY_THEOREM.md):
   `N=4`, the exhaustive `Q/Q` versus `Q/C^2` route kernels, route parities,
   and the two exact scalar controls.

The imported A4 route-state rule is written as the recurrence (10).  The new
content is its explicit composition with the U7I port partition: endpoint
port-set equality/complementarity and the resulting weighted identities
(11)--(12), (14)--(15), and (19)--(23).  Thus this theorem is an exact
`A4 + U7I` interface corollary, not a claim that route parity itself was
previously unknown.

The focused primary verifier is named

```text
claims/arbitrary-order/verify_all_bridge_bipartite_least_core_beta_three_route_port_pairing.py
```

and should enumerate route-state assignments, reconstruct the `Q/Q` and
`Q/C^2` port partitions, and replay both weighted controls using exact
rational matching sums.

The independent audit is named

```text
claims/arbitrary-order/audit_all_bridge_bipartite_least_core_beta_three_route_port_pairing.py
```

and should import neither repository code nor the primary verifier, use a
separate perfect-matching representation, and independently check the four
singleton pairs, complementary even-route doubletons, nonzero endpoint port
sums, and exact negation in the `Q/C^2` control.

Those programs are exact finite QA for the displayed rank-three kernels and
controls.  The written alternating recurrence proves the route-port statement
for arbitrary route lengths; no bounded enumeration carries that quantifier.

## 7. Exact boundary

```text
simultaneous balanced all-bridge branch:                    ASSUMED;
globally least bipartite pure core:                         IMPORTED;
beta=3 extremal sparse quartic site:                        ASSUMED;
Q/Q or Q/C^2 suppressed kernel with N=4:                   IMPORTED EXHAUSTIVE;
odd-route endpoint port sets coincide:                     PROVED;
even-route endpoint ports are disjoint complements:        PROVED;
Q/Q paired ports are equal singleton contributions:        PROVED;
Q/C^2 four odd pairs are singleton contributions:          PROVED;
Q/C^2 even-route endpoint ports are complementary doubletons: PROVED;
Q/C^2 doubleton port sums are nonzero exact negatives:      PROVED;
bare deletion hafnians at paired endpoints equal/opposite:  NOT PROVED / NOT CLAIMED;
paired or aggregate ports algebraically independent:        NOT PROVED / NOT CLAIMED;
paired ports occupy distinct mixed target fibres:           NOT PROVED / NOT CLAIMED;
port pairing implies target attachment or deeper incidence: NOT PROVED;
either Q/Q or Q/C^2 impossible in an all-bridge system:     NOT PROVED;
scalar controls are simultaneous all-bridge witnesses:      FALSE / NOT CLAIMED;
universal extraction/gluing:                                NOT PROVED;
global Krenn--Gu conjecture:                                UNRESOLVED.
```
