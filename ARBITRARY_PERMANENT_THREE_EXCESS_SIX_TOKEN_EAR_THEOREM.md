# The three-excess support has a six-token ear budget

## Status

**Exact arbitrary-order combinatorial theorem.**  Let `G` be the physical
support graph of a minimal restriction

```text
P_m -> Delta_3
```

with support exactly `3m+3`.  The previous support and minimality theorems
make `G` a connected bipartite matching-covered graph on `m+m` vertices,
with minimum degree at least three.

Starting from any conformal cycle, Hetyei's bipartite ear theorem gives an
odd-ear decomposition of `G`.  In every such decomposition, each vertex has
one mandatory later endpoint occurrence and there are exactly six further
endpoint occurrences in the whole graph: three on the mode side and three
on the source side.  These six surplus occurrences are exactly the six
degree-excess incidences over cubicity.

This converts an arbitrary-length matching-covered support into a causal
schedule with a constant replay budget.  It does not by itself exclude the
`3m+3` layer or prove the Krenn--Gu conjecture.

The support and matching-covered inputs are proved in
[`ARBITRARY_PERMANENT_THREE_M_PLUS_TWO_SUPPORT_BOUND.md`](ARBITRARY_PERMANENT_THREE_M_PLUS_TWO_SUPPORT_BOUND.md)
and
[`ARBITRARY_PERMANENT_THREE_EXCESS_CONFORMAL_BIRKHOFF_REDUCTION.md`](ARBITRARY_PERMANENT_THREE_EXCESS_CONFORMAL_BIRKHOFF_REDUCTION.md).

## Literature input

An ear of a subgraph is an odd path whose endpoints lie in the subgraph and
whose internal vertices do not.  The bipartite ear-decomposition theorem,
attributed to Hetyei, says that every conformal cycle of a bipartite
matching-covered graph extends to a sequence obtained by adding one odd ear
at a time.  A modern statement is Theorem 1.2 of Dalwadi, Pause, Diwan, and
Kothari,
[*Planar cycle-extendable graphs*](https://dmtcs.episciences.org/15655/pdf).
Mallik, Diwan, and Kothari also use the same theorem in their study of
[*Extremal minimal bipartite matching covered graphs*](https://arxiv.org/abs/2404.06445).

Only the ear theorem is imported.  The six-token identity below is the new
translation specific to the exact `3m+3` permanent-support boundary.

## Ear accounting

Fix a conformal even cycle `C` and an ear decomposition

```text
C=G_0 subset G_1 subset ... subset G_t=G,
G_j=G_(j-1) union P_j,                              (1)
```

where every `P_j` is an odd path.  If `ell_j` is the number of edges of
`P_j`, it introduces `ell_j-1` internal vertices.  Therefore each ear raises
`|E|-|V|` by one.  Since the initial cycle has equally many edges and
vertices,

```text
t=|E(G)|-|V(G)|=(3m+3)-2m=m+3.                    (2)
```

Every vertex is born with degree two: initial vertices have their two cycle
edges, while every later vertex is internal to its birth ear.  Let `h(v)` be
the number of later ears having `v` as an endpoint, counting all ears for an
initial-cycle vertex and only post-birth ears for a later vertex.  Edge
disjointness of the construction gives the exact identity

```text
deg_G(v)=2+h(v).                                    (3)
```

Minimum degree three forces `h(v)>=1` for every one of the `2m` vertices.
On the other hand, every ear has two endpoints, so

```text
sum_v h(v)=2t=2m+6.                                (4)
```

Define the replay or surplus token count

```text
s(v)=h(v)-1=deg_G(v)-3.                             (5)
```

Equations (2)--(5) prove

```text
s(v)>=0,                 sum_v s(v)=6.              (6)
```

Equivalently, mark the first post-birth endpoint use of every vertex as its
mandatory token.  Across the entire decomposition there are exactly six
endpoint slots that revisit a vertex after that first use.  No enumeration
of ears, matchings, supports, or graphs is involved.

## Three tokens on each bipartition shore

Every odd path in a bipartite graph has endpoints in opposite shores.
Consequently each of the `t=m+3` ears contributes one endpoint occurrence to
each shore.  Each shore has `m` vertices and therefore consumes `m`
mandatory first-use tokens.  Hence

```text
sum_(v in modes)   s(v)=3,
sum_(v in sources) s(v)=3.                          (7)
```

This is also the degree identity

```text
sum_(v in one shore) (deg_G(v)-3)
   = |E(G)|-3m=3.                                   (8)
```

Thus the positive degree excess on either shore has only the partitions

```text
3,             2+1,             1+1+1.             (9)
```

In particular, at most three modes and at most three sources can have degree
greater than three.  On the source shore, the mandatory `3m` coordinate
cover has degree exactly three at every source.  Hence source replay
multiplicity is precisely incidence with the three excess cells.

There is an important asymmetry.  The mandatory cover need not have degree
three at every mode.  If `B` is that cover and `h_E(i)` is the number of
excess cells at mode `i`, then only

```text
s(i)=deg_G(i)-3=h_E(i)+deg_B(i)-3                   (10)
```

is automatic.  Mode replay vertices need not be the mode endpoints of the
excess cells.

## Alignment with the conformal cycle/theta carrier

The previous three-edge theorem puts the three excess cells in a conformal
induced even cycle or in an even subdivision of a three-edge theta.  In the
cycle case, that carrier itself may be used as `G_0` in (1).

In the theta case, its three branch paths are odd.  Any two form an even
cycle, and the internal vertices of the third path have a perfect matching;
together with the matching outside the conformal theta, this makes the
chosen cycle conformal in `G`.  It may therefore be used as `G_0`.  The
third path is a legal odd ear of that cycle.  The theorem does **not** claim
that an arbitrary ear extension must choose it as the first ear.

The new causal formulation is therefore compatible with both conformal
carriers:

```text
one first endpoint use per physical vertex,
three replay endpoints on the mode shore,
three replay endpoints on the source shore.         (11)
```

The source replay vertices are exactly the exceptional sources of the
three-excess port theorem.  The mode replay vertices record degree surplus,
not necessarily the modes carrying excess cells.  Any proposed
incidence-alignment lemma between the conformal carrier and the pure-backbone
cube must respect this asymmetry and fit inside these six replay events.

## Immediate structural consequences

1. The final ear has length one.  Otherwise one of its internal vertices is
   born with degree two and has no later ear in which to become an endpoint,
   contradicting minimum degree three.
2. After selecting one first endpoint occurrence for every vertex, only six
   endpoint incidences remain.  Thus every attempt to propagate port labels
   through an ear sequence may branch or revisit an already activated
   vertex only six times in total, three times per shore.
3. The token locations do not depend on the chosen ear decomposition:
   `s(v)=deg_G(v)-3`.  Only the temporal placement of the mandatory and
   replay endpoint occurrences changes.

Items 1--3 are exact, but they are a resource theorem rather than an
exclusion theorem.  A long chain of first-use ears can still exist.

The later replay/exchange theorem excludes the source partition `3`, proves
the sharp five-sector odd closure, and gives unbounded structural families in
which the token budget does not force coloured carrier alignment.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_REPLAY_EXCHANGE_CLOSURE_THEOREM.md`.

## Proof target exposed

The conformal--Birkhoff reduction left one missing incidence statement: an
alignment between a conformal matching and the at-most-eight pure
backbones.  The six-token theorem replaces an arbitrary-order search by the
following sharper symbolic target.

```text
Show that transporting the three exceptional ports from their conformal
cycle/theta carrier through any cubic-first odd-ear schedule either

  (a) forces more than three replay endpoints on one shore, or
  (b) creates a same-word cube face with noncommuting S_3 port transport, or
  (c) isolates a mixed coefficient with no cancellation partner.
```

None of (a)--(c) is proved here.  In particular, six replay tokens can be
distributed consistently as `3`, `2+1`, or `1+1+1` on each shore.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_three_excess_six_token_ear_theorem.py
python audit_arbitrary_permanent_three_excess_six_token_ear_theorem.py
```

The primary verifier checks the affine ear, endpoint, degree, and shore
identities symbolically and verifies the three partitions of the shore
budget.  The independent no-import audit reconstructs the ledger from
coefficient pairs and checks the final-ear consequence.  These scripts
audit the arithmetic; the arbitrary-order proof is equations (1)--(8) plus
Hetyei's theorem.

## Boundary

```text
matching-covered support at exactly 3m+3:     PROVED PREVIOUSLY;
odd-ear count from any conformal cycle:       m+3;
post-birth endpoint slots:                    2m+6;
mandatory first-use slots:                    2m;
surplus/replay endpoint slots:                EXACTLY 6;
surplus split by bipartition:                 EXACTLY 3+3;
forced nonabelian holonomy or isolation:      NOT PROVED;
exclusion of support 3m+3:                    NOT PROVED;
global Krenn--Gu conjecture:                  UNRESOLVED.
```
