# All-bridge active-deck maximum-degree-four exclusion

## Status

This is an exact arbitrary-order theorem over characteristic zero in the
simultaneous three-colour balanced all-bridge branch.  Let `D` be the physical
graph of saturated diagonal entries.  The theorem proves

```text
Delta(D) >= 5.                                        (1)
```

It strengthens the cubic-diagonal exclusion without imposing a bound on the
full support skeleton.  It does not apply to the separate deeper-blocker
branch, prove a universal extraction into the all-bridge branch, or resolve
the global Krenn--Gu conjecture.

## Inherited identities

Let `V` have even size `n>=6`.  For each colour `c in {0,1,2}`, let `Z^c`
be the symmetric matrix of saturated colour-`c` diagonal entries, and put

```text
D = {ij : Z^c_ij != 0 for at least one c}.             (2)
```

The all-bridge zero-layer and mixed-cut theorems give

```text
haf(Z^c[V]) = 1,                                      (3)

haf(Z^c[A]) haf(Z^d[V-A]) = 0                         (4)
```

for distinct colours `c,d` and every nonempty proper even subset `A` of
`V`.  Every saturated colour-`c` edge flips the two normal-type bits other
than `b_c`.

For an edge `e={i,j}`, define

```text
C_e^c = haf(Z^c[V-{i,j}]),
s_e^c = Z_e^c C_e^c,
E_c = {e : s_e^c != 0}.                               (5)
```

The active-deck theorem gives

```text
sum_(j!=i) s_{ij}^c = 1                               (6)
```

at every vertex and colour.  Hence every `E_c` spans `V` with positive
minimum degree.  The three physical edge sets `E_0,E_1,E_2` are pairwise
disjoint, and an edge active in colour `c` carries no saturated diagonal
entry of either other colour.

## A noncancellation lemma for two matchings

### Lemma

Let a weighted graph `G` be the edge-disjoint union of

1. a perfect matching `P`, all of whose weights are nonzero; and
2. a partial matching `R`, all of whose weights are nonzero.

If

```text
haf(G[V]) != 0,                                       (7)
```

then every principal induced subgraph `G[A]` which has a perfect matching
satisfies

```text
haf(G[A]) != 0.                                       (8)
```

### Proof

Every connected component of `P union R` is an alternating path or an even
alternating cycle.  Because `P` is perfect, a path component has even order,
starts and ends with `P`, and has the unique perfect matching supplied by its
`P`-edges.  A cycle component has exactly its two alternating perfect
matchings.  Therefore the full hafnian factors as

```text
product_(path K) product_(e in P intersect K) w_e
times
product_(cycle K)
  (product_(e in P intersect K) w_e
   + product_(e in R intersect K) w_e).               (9)
```

All path products are nonzero.  Condition (7) says that every displayed
cycle factor is nonzero as well.

An induced subgraph of a path or cycle is a disjoint union of paths, except
that selecting a whole cycle leaves that cycle component intact.  If the
induced subgraph has a perfect matching, each of its path components has even
order and a unique matching with nonzero product.  Each whole cycle
component contributes the already nonzero factor from (9).  Multiplying the
component hafnians proves (8).  No positivity or genericity is used.

## Degree-four reduction to matching pairs

Assume for contradiction that

```text
Delta(D) <= 4.                                       (10)
```

Since the three `E_c` are edge-disjoint and each has positive degree at every
vertex,

```text
1 <= deg_(E_c)(v) <= 2,
sum_c deg_(E_c)(v) <= 4.                              (11)
```

Thus each `E_c` is a union of paths and cycles.  Fix one colour and abbreviate
`s_e=s_e^c`.  At an endpoint of a path, (6) has only one nonzero summand, so
its incident active edge has score one.  If the path continued through the
next vertex, (6) there would read

```text
1 + s_f = 1,
```

forcing the next active score `s_f` to vanish.  Hence every path component is
just `K_2`.

Every cycle component is even: its colour-`c` edges all flip each of the two
normal-type bits other than `b_c`, so the cycle is bipartite with respect to
either bit.  Choose a perfect matching `P_c` of `E_c` by taking each
`K_2` and one alternating half of every cycle.  Let `Q_c` be the other
alternating half of the cycles.  Thus

```text
E_c = P_c disjoint-union Q_c,                         (12)
```

where `P_c` is perfect and `Q_c` is partial.

Put

```text
H = D - (E_0 union E_1 union E_2).                    (13)
```

The degree count (11) makes `H` a physical matching.  A vertex on an
`E_c`-cycle already has active degree `2+1+1=4`, so no edge of `H` meets it.
Cycle-vertex sets belonging to different colours are disjoint, since two
active degrees of two would leave no room for the positive degree of the
third active graph.  Consequently

```text
R = H union Q_0 union Q_1 union Q_2                  (14)
```

is a physical partial matching, edge-disjoint from all three `P_c`.

Active exclusivity kills every colour-`c` entry on `E_d` for `d!=c`.  Thus
any colour-`c` support edge outside `E_c` lies in `H`.  Hence

```text
support(Z^c) = P_c union R_c,                         (15)

R_c = Q_c union {h in H : Z_h^c != 0} subset R.
```

Equation (3) and the lemma now imply:

> every principal subgraph of `Z^c` which has a perfect matching has
> nonzero hafnian.                                    (16)

## Pairwise Hamiltonicity

Fix distinct colours `c,d`.  The edge-disjoint perfect matchings
`P_c,P_d` form a spanning disjoint union of alternating even cycles.  If
there were more than one component, let `A` be the vertex set of one cycle.
Then `P_c` matches `A` and `P_d` matches `V-A`.  Statement (16) gives

```text
haf(Z^c[A]) != 0,
haf(Z^d[V-A]) != 0,
```

contradicting (4).  Therefore

```text
P_c union P_d is one Hamiltonian alternating cycle    (17)
```

for every pair of colours.

## A Hamiltonian chord excludes every residual edge

Suppose that `r in R_c` for some colour `c`, and choose another colour `d`.
Let `k` be the third colour.  Every edge of the Hamiltonian cycle
`P_c union P_d` flips `b_k`.  The saturated colour-`c` edge `r` also flips
`b_k`.  Its endpoints are therefore in opposite classes of this Hamiltonian
bipartition, so both Hamiltonian arcs between them have odd length.

Exactly one arc starts and ends with `P_d`-edges.  It cannot have length one,
because then `r` would be that `P_d`-edge.  It cannot have length `n-1`,
because then the complementary one-edge arc would be the `P_c`-edge with the
same endpoints as `r`.  Both alternatives contradict the physical
edge-disjointness of `R` from every `P_c`.  The selected arc therefore has
length between three and `n-3`.

Let `A` be its vertex set.  The `P_d`-edges on the arc perfectly match `A`.
The chord `r` together with the intervening `P_c`-edges is a perfect matching
of `A` supported by `Z^c`.  Because `A` is a union of `P_d`-edges, `P_d` also
matches `V-A`.  The set `A` is nonempty, proper, and even.  Applying (16) on
both sides gives

```text
haf(Z^c[A]) != 0,
haf(Z^d[V-A]) != 0,
```

again contradicting (4).  Thus

```text
R_c is empty for every c.                             (18)
```

Every edge of `R` lies in `D` and hence supports at least one saturated
colour.  Equation (18) forces `R` itself to be empty.  Then all `Q_c` and `H`
are empty, so

```text
D = P_0 union P_1 union P_2
```

is cubic.  This contradicts the previously proved cubic saturated-diagonal
exclusion.  Assumption (10) is impossible, proving (1).

## Dependencies, checks, and exact boundary

The load-bearing inherited results are:

1. [`ALL_BRIDGE_ACTIVE_DECK_EXCLUSIVITY_AND_CUBIC_DIAGONAL_EXCLUSION.md`](ALL_BRIDGE_ACTIVE_DECK_EXCLUSIVITY_AND_CUBIC_DIAGONAL_EXCLUSION.md): the Laplace identity, active exclusivity, and cubic exclusion;
2. [`UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md`](UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md): the saturated bit-flip characterization and zero-layer matrices; and
3. [`HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md`](HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md): the mixed complementary-product identity.

Focused bounded checks:

```text
python claims/arbitrary-order/verify_all_bridge_active_deck_maximum_degree_four_exclusion.py
python claims/arbitrary-order/audit_all_bridge_active_deck_maximum_degree_four_exclusion.py
```

They check the path-score reduction, the two-matching noncancellation lemma,
the Hamiltonian arc construction, and the local degree bookkeeping behind the
degree-four decomposition.  The written characteristic-zero argument above
is the proof; the bounded programs are supporting checks rather than an
exhaustive graph cover.

```text
simultaneous all-bridge Delta(D)<=4: EXCLUDED;
simultaneous all-bridge Delta(D)>=5: UNKNOWN;
deeper-blocker branch:               UNKNOWN;
universal extraction/gluing:         NOT PROVED;
global Krenn--Gu conjecture:          UNRESOLVED.
```
