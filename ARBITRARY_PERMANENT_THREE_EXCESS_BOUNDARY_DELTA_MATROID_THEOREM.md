# Boundary matching delta-matroid and elementary-pair descent

## Status

**Exact support theorem, with an exact weighted response formula.**  No
support family is enumerated.  The theorem applies to every order at once.

For a conformal bipartite exterior, the terminal sets that it can cover form
an even matching delta-matroid.  Moreover, every nonempty realizable boundary
sector contains a realizable elementary sector consisting of one core mode
and one core source.  Consequently the entire question of whether *any*
nonempty boundary sector exists compresses to a bipartite link graph on
mode-source pairs.

This is a support compression, not a cancellation theorem.  The weighted
elementary response is a permanental-cofactor contraction.  Its entries can
cancel over characteristic zero, and neither delta-matroid exchange nor the
formula below supplies Pfaffian/Wick identities for these physical
permanental amplitudes.

## Boundary graph and feasible terminal sets

Write the bipartition of the full support graph as

```text
modes:    A disjoint union R,
sources:  P disjoint union Q.
```

The core terminals are `T=A disjoint union P`; the exterior vertices are
`I=R disjoint union Q`.  Delete the core edges `A-P` and retain exactly the
boundary graph

```text
Gamma=(R-Q) union (A-Q) union (R-P).                 (1)
```

For `U subseteq T`, call `U` **feasible** when the induced graph
`Gamma[I union U]` has a perfect matching.  Thus `U` is the set of core
vertices covered through the exterior.  Let

```text
F(Gamma)={U subseteq T : Gamma[I union U] has a perfect matching}. (2)
```

Exterior conformality is exactly `emptyset in F(Gamma)`.

## Theorem 1: symmetric exchange

For any graph `Gamma`, the feasible family `F(Gamma)` satisfies symmetric
exchange:

```text
U,V in F(Gamma), x in U triangle V
  => there is y in U triangle V, y != x,
     with U triangle {x,y} in F(Gamma).              (3)
```

All feasible sets have one parity.  Provided `F(Gamma)` is nonempty, this
makes `(T,F(Gamma))` an even delta-matroid.  In the application nonemptiness
is automatic because exterior conformality makes the empty set feasible.

### Proof

Choose perfect matchings `M_U` of `Gamma[I union U]` and `M_V` of
`Gamma[I union V]`.  In the symmetric-difference graph `M_U triangle M_V`,
every exterior vertex has degree zero or two.  Its degree-one vertices are
exactly the terminals in `U triangle V`.

The component containing `x` is therefore an alternating path with another
endpoint `y in U triangle V`, necessarily distinct from `x`.  Toggle the
edges of this path in `M_U`.  At an endpoint belonging to `U\V`, its
`M_U` edge is removed; at an endpoint belonging to `V\U`, its `M_V` edge is
added.  Every interior vertex remains matched once.  The resulting matching
is perfect on

```text
I union (U triangle {x,y}),                           (4)
```

which proves (3).  The endpoints come in pairs, so all feasible-set sizes
have the same parity.  This proof is purely combinatorial and invokes no
finite census.  It is the terminal-set specialization of Bouchet's matching
delta-matroid construction [1].

## Theorem 2: bipartite balance and elementary-pair descent

Assume `Gamma` has the bipartition in (1), `|R|=|Q|`, and its exterior is
conformal.  Then every feasible set is balanced:

```text
|U intersect A|=|U intersect P|.                     (5)
```

Every nonempty `U in F(Gamma)` contains a two-element feasible subset

```text
{a_i,p_j} in F(Gamma).                               (6)
```

### Proof

A perfect matching of `Gamma[I union U]` equates the sizes of its two
bipartition shores:

```text
|R|+|U intersect A| = |Q|+|U intersect P|.
```

Since `|R|=|Q|`, this is (5).

Now compare a nonempty feasible `U` with the feasible empty set in (3).
For any `x in U`, exchange gives distinct `x,y in U` such that
`U\{x,y}` is feasible.  Balance before and after deletion forces one of
`x,y` to lie in `A` and the other in `P`.  Repeat.  Feasible sets shrink by
one mode-source pair until a feasible set of size two remains.  It is a
subset of the original `U` and has the form (6).

Define the **elementary boundary link graph**

```text
L_Gamma subseteq A times P,
(a_i,p_j) in L_Gamma iff {a_i,p_j} in F(Gamma).       (7)
```

Then

```text
F(Gamma)={emptyset}
  iff L_Gamma has no edges.                          (8)
```

Thus no search through sectors of sizes four, six, or higher is needed to
prove exterior decoupling: it is enough to eliminate every elementary link.
The theorem does not say that an arbitrary prescribed pair inside `U` is
feasible; it says that at least one pair survives the descent.

## Theorem 3: alternating reachability computes the link graph

Fix one conformal exterior matching

```text
M_0={r_k-q_k : 1<=k<=n},                             (9)
```

after relabelling `R,Q`.  Contract every edge of `M_0` to a vertex `v_k`
and construct a directed graph with arcs

```text
a_i -> v_k   when a_i-q_k is an edge,
v_k -> v_l   when r_k-q_l is an edge outside M_0,
v_k -> p_j   when r_k-p_j is an edge.               (10)
```

Then

```text
(a_i,p_j) in L_Gamma
  iff there is a directed path a_i -> ... -> p_j.   (11)
```

### Proof

If `{a_i,p_j}` is feasible, take an elementary-sector matching `M_1`.
The symmetric difference `M_0 triangle M_1` consists of one alternating
path from `a_i` to `p_j` and possibly disjoint alternating cycles.  Discard
the cycles.  After the `M_0` edges are contracted, the remaining path has
exactly the orientations in (10), proving forward reachability.

Conversely, expand any directed path in (10) by reinserting the contracted
`M_0` edges.  It is an `M_0`-alternating path from `a_i` to `p_j`.  Toggling
that path in `M_0` produces a perfect matching of
`Gamma[I union {a_i,p_j}]`.

Let `B,D,C` be the Boolean adjacency matrices for the three arc types in
(10).  The elementary link matrix is therefore

```text
L_Gamma = B D^* C                                    (12)
```

over the Boolean semiring, where `D^*` is reflexive transitive closure.
Equivalently, `L_Gamma` is empty exactly when a directed cut separates all
boundary entrances from all boundary exits.  This is a reachability
calculation or cut certificate, not a census of higher boundary sectors.

The construction depends on the chosen `M_0`, but the resulting relation
`L_Gamma` does not: (11) identifies it with the intrinsic feasibility
definition (7).

## Theorem 4: weighted elementary response

Let the weighted bipartite adjacency matrix be blocked as

```text
          P   Q
       +---------+
 A     | X   Y   |
 R     | Z   W   |.                                 (13)
       +---------+
```

Rows of `W` are indexed by `R` and columns by `Q`.  Define the unsigned
permanental cofactor transpose

```text
C_per(W)_(q,r)=per(W with row r and column q deleted). (14)
```

The aggregate weight of the elementary sector `{a_i,p_j}` is

```text
E_ij = sum_(q in Q, r in R)
         Y_(i,q) Z_(r,j) per(W_(delete r,delete q))
     = (Y C_per(W) Z)_ij.                           (15)
```

### Proof

An exterior perfect matching covering exactly `a_i,p_j` must choose one
edge `a_i-q`, one edge `r-p_j`, and a perfect matching from
`R\{r}` to `Q\{q}`.  These data are mutually exclusive and exhaustive.
Multiplying their weights and summing proves (11).

Consequently the part of the full block permanent using exactly one pair of
crossing edges is

```text
sum_(i,j) E_ij per(X_(delete i,delete j)).           (16)
```

Higher sectors are governed by higher permanental minors.  Formula (11) is
valid over any commutative ring; in the characteristic-zero application the
weights are commuting linear forms or complex scalars.

## What transfers from the literature, and what does not

Bouchet proved that vertex sets saturated by matchings carry delta-matroid
structure [1].  The alternating-path proof above is included so the exact
version needed here does not depend on importing a black box.

On the fermionic side, principal Pfaffians satisfy quadratic Wick relations,
and their supports/valuations lead to even or valuated delta-matroids; Rincón
develops this spinor-side relationship [2].  The support delta-matroid here
may also be encoded by auxiliary generic skew/Pfaffian coordinates, so
support-level representability consequences are not being denied.  Those
auxiliary signed coordinates are not the physical boundary amplitudes in
(15): the latter use unsigned permanental cofactors and specialized complex
weights.  Therefore no Wick identity or valuation is inferred for `E` or
for the higher physical boundary amplitudes.

References:

1. André Bouchet, “Matchings and delta-matroids,” *Discrete Applied
   Mathematics* 24 (1989), 55–62,
   [doi:10.1016/0166-218X(92)90272-C](https://doi.org/10.1016/0166-218X(92)90272-C).
2. Felipe Rincón, “Isotropical Linear Spaces and Valuated Delta-Matroids,”
   [arXiv:1004.4950](https://arxiv.org/abs/1004.4950).

## Exact consequence for the three-excess program

For every arbitrary-order conformal decomposition already used in the
three-excess reduction, the unknown nonempty boundary convolution has a
support certificate at elementary level.  There are now two sharply
separated first subproblems:

```text
support route:                prove L_Gamma=B D^* C is empty by a cut;
elementary amplitude route:   prove all E=Y C_per(W) Z entries vanish,
                              or their core cofactor images cannot cancel. (17)
```

The support route is combinatorial linkability.  The amplitude route is a
bosonic cofactor problem and may require the apolar/derived flattenings
identified in the literature frontier.  Vanishing of `E_ij` does not imply
absence of the link `(a_i,p_j)`, because distinct exterior matchings can
cancel.  Nor does vanishing of every elementary response decouple the
higher boundary sectors; those higher layers require separate control.

## Scope wall

```text
proved:     all boundary supports obey even symmetric exchange;
proved:     every nonempty conformal sector contains an elementary pair;
proved:     existence of any nonempty sector iff L_Gamma has an edge;
proved:     L_Gamma=B D^* C for any fixed conformal exterior matching;
proved:     E=Y C_per(W) Z is the exact elementary weighted response;
not proved: L_Gamma is empty for every hypothetical restriction;
not proved: elementary aggregates E_ij are nonzero when links exist;
not proved: higher weighted sectors are determined by elementary ones;
not used:   large support enumeration, finite-field search, numerics;
global Krenn--Gu conjecture: UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_arbitrary_permanent_three_excess_boundary_delta_matroid_theorem.py
python audit_arbitrary_permanent_three_excess_boundary_delta_matroid_theorem.py
```

The primary verifier checks the fixed symbolic block-permanent expansion and
the path toggle.  The independent audit uses no algebra package and checks a
separate integer instance plus the descent witness.  Both are proof guards,
not experimental evidence for the universal theorem proved above.
