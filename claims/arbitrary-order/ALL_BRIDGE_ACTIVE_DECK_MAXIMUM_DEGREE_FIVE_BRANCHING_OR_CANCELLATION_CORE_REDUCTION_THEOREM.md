# All-bridge active-deck degree-five cut reduction and full-support degree-eight boundary

## Status

This is an exact arbitrary-order theorem over characteristic zero in the
simultaneous three-colour balanced all-bridge branch.  Let `D` be the physical
graph of saturated diagonal entries and let `G` be the full essential support
skeleton.  It proves two distinct conclusions.

First, without imposing a degree bound,

```text
deg_G(v) >= deg_D(v)+3       for every vertex v.       (A)
```

The existing maximum-degree-four exclusion gives `Delta(D)>=5`.  Therefore

```text
Delta(G)>=8,                n>=10.                    (B)
```

In particular, every simultaneous balanced all-bridge support of maximum
full-support degree at most seven is excluded.

Second, if a hypothetical witness satisfies

```text
Delta(D) <= 5,                                        (1)
```

then the already proved maximum-degree-four exclusion makes
`Delta(D)=5`.  Every such system has a proper supported pure hafnian
cancellation in at least one of the following active-deck-localized forms:

1. **inactive-selected-edge complement:** some `E_c` has no perfect matching;
   a nonzero full colour-`c` matching contains an inactive edge `f`, and
   `haf(Z^c[V-f])=0` although the remaining matching supports `V-f`.  A
   minimal deficient shore further forces two vertex-disjoint inactive repair
   edges whose pair-deletion cofactors vanish in all three colours;
2. **selected-matching-component/complement:** every `E_c` has a perfect
   matching, and some selected pair `P_c union P_d` is disconnected; or
3. **Hamiltonian-chord-arc/complement:** every selected pair is Hamiltonian,
   and a residual saturated edge is a proper chord.

In the last two forms the mixed-cut identity forces one of the two displayed
supported factors to vanish.  For a fixed selected matching triple, the
component and Hamiltonian alternatives are exhaustive, but different choices
of the `P_c` need not give the same form.

The universal zero-layer theorem already forces a proper supported pure
cancellation for **every** all-bridge witness, independently of (1).  The
existing abstract least-cancellation theorem refines any globally least such
cancellation into a primitive single cycle or a connected branching core.
Those are inherited universal exits, not new degree-five alternatives, and
the globally least core need not be one of the cuts localized here.  Under
`Delta(D)=5`, however, that core is additionally bipartite and subcubic.  It
is therefore exactly an even cycle/binomial, a cyclomatic-rank-two closed
all-odd theta/trinomial, or a core of rank at least three with at least four
cubic vertices.

The degree-five result is a structural reduction, not an exclusion.  None of
the three localized cancellation forms is proved impossible.  All three
displayed least-core strata, `Delta(D)>=6`, and the separate deeper-blocker
branch remain open.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

The later
[`ALL_BRIDGE_ACTIVE_DECK_ALL_DEGREE_LOCALIZED_PURE_CANCELLATION_AND_BIPARTITE_CORE_REDUCTION_THEOREM.md`](ALL_BRIDGE_ACTIVE_DECK_ALL_DEGREE_LOCALIZED_PURE_CANCELLATION_AND_BIPARTITE_CORE_REDUCTION_THEOREM.md)
shows that Sections 3--4 actually localize one of the same three supported
cancellations at every saturated degree.  It also separates degree-free
least-core bipartiteness and the rank-one/rank-two classification from the
genuinely degree-five subcubic and typed-site conclusions owned here.

## 1. Inherited identities and notation

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
disjoint, and an edge active in colour `c` carries no saturated entry of
either other colour.

An important quantifier boundary is worth making explicit.  Every active
edge belongs to at least one nonzero perfect-matching monomial of `Z^c`,
because both its entry and complementary cofactor are nonzero.  This does
**not** say that the other edges of that monomial are active: their cofactor
sums may cancel.  Thus it does not imply that `E_c` contains a perfect
matching.

Put

```text
H = D - (E_0 union E_1 union E_2),
a_c(v) = deg_(E_c)(v),
h(v) = deg_H(v).                                      (7)
```

## 2. Exact local degree table

Assume (1).  Pairwise active exclusivity and positive active degree give

```text
a_0(v)+a_1(v)+a_2(v)+h(v) = deg_D(v) <= 5,
a_c(v) >= 1.                                          (8)
```

Therefore every `E_c` is subcubic and `H` has maximum degree two.  Up to a
permutation of colours, the complete list of local possibilities is

```text
(a_0,a_1,a_2;h) =
  (1,1,1;h),  h=0,1,2;
  (2,1,1;h),  h=0,1;
  (3,1,1;0);
  (2,2,1;0).                                          (9)
```

At a vertex of saturated degree five, these specialize to

```text
(1,1,1;2), (2,1,1;1), (3,1,1;0), (2,2,1;0).          (10)
```

Each connected component of every `E_c` is balanced bipartite.  Indeed, a
colour-`c` active edge flips both normal bits different from `b_c`, so either
fixed one of those bits bipartitions the component.  If its shores are `L,R`,
sum (6) over `L` and over `R`.  Each edge score is counted once in either
sum, and hence

```text
|L| = sum_(e in E_c[L,R]) s_e^c = |R|.               (11)
```

Characteristic zero converts equality of the field elements `|L|*1` and
`|R|*1` into equality of the integer shore sizes.  Balancedness alone does
not force Hall's condition because the nonzero scores need not have one
sign; Section 6 gives a sharp exact control.

## 3. The active-matching dichotomy

Fix a colour `c`.  If `E_c` has no graph-theoretic perfect matching, choose
any nonzero full perfect-matching monomial `M` of `Z^c`; one exists because
`haf(Z^c[V])=1`.  Then `M` is not contained in `E_c`.  For every
`f in M-E_c`,

```text
Z_f^c != 0,             s_f^c = Z_f^c C_f^c = 0,
```

so the field property gives

```text
haf(Z^c[V-f]) = C_f^c = 0.                            (12)
```

Here `V-f` means deletion of both endpoints.  The matching `M-f` is a
nonzero supported perfect matching on this nonempty proper even set.  Thus
(12) is the first localized cancellation form.  Moreover, the two-point
mixed cuts give `Z_f^c C_f^d=0` for `d!=c`, so

```text
C_f^0=C_f^1=C_f^2=0.                                  (13)
```

This no-perfect-matching lemma does not require (1).

There is a sharper simultaneous interface in this first form.  Use either
fixed non-`c` normal bit to give the global bipartition `U,W` of
`support(Z^c)`, and hence of `E_c`.
Choose an inclusion-minimal Hall-deficient set `X subset U` for the whole
active graph, and put `T=N_(E_c)(X)`.  Minimality gives

```text
|X|=|T|+1.                                             (13a)
```

Indeed, deleting any `x in X` leaves a nondeficient set, forcing
`|T|>=|X|-1`; deficiency gives the reverse inequality.  Every `t in T` has
at least two neighbours in `X`, since otherwise deleting its unique neighbour
would leave a smaller deficient set.  Each active component is balanced by
(11), so `X` cannot be a union of entire components.  Hence the active
boundary

```text
F=E_c[T,U-X]
```

is nonempty.  Summing (6) first over `X` and then over `T` gives

```text
sum_(f in F) s_f^c = |T|-|X| = -1.                    (13b)
```

Choose `e={y,t} in F` and a nonzero matching monomial in its complementary
cofactor.  Let `a` count its edges from `X` to `T-{t}`, let `b` count its
edges from `X` to `W-T`, and let `q` count its edges from `U-X-{y}` to
`T-{t}`.  Matching the two shores gives

```text
a+b=|X|,        a+q=|T|-1=|X|-2,
b=q+2 >=2.                                             (13c)
```

Thus the complementary matching contains at least two vertex-disjoint
colour-`c` support edges from `X` to `W-T`.  They are not active in colour
`c` by the definition of `T`; active exclusivity prevents them from being
active in either other colour.  Hence they lie in `H`.  For every such repair
edge `f`, its nonzero colour-`c` entry and inactivity give `C_f^c=0`, while
the two oriented mixed cuts give

```text
C_f^0=C_f^1=C_f^2=0.                                  (13d)
```

Under (1), every endpoint of these repair edges has `h>=1`, so none can have
active degree three in any colour.  The double-star in Section 6.1 attains
`b=2`, showing that this two-repair conclusion is sharp at the one-colour
interface.

It remains to suppose every `E_c` has a perfect matching.  Choose

```text
P_c subset E_c                                          (14)
```

for all three colours.  Active exclusivity makes these matchings pairwise
physically edge-disjoint.  Put

```text
R_P = D - (P_0 union P_1 union P_2).                  (15)
```

At every vertex, the selected triple uses exactly three distinct saturated
edges, and hence

```text
deg_(R_P)(v)=deg_D(v)-3 <=2.                           (16)
```

The maximum-degree-four theorem and (1) supply a vertex of `D`-degree five;
`R_P` has degree two there and is nonempty.  Notice that this argument does
not require `Delta(E_c)<=2`: an active graph may branch and still contain the
selected matching.

## 4. Selected-pair mixed cuts locate a proper pure cancellation

Using the `P_c` from (14), we prove that some proper nonempty even set
`S subset V` has

```text
haf(Z^e[S]) = 0                                      (17)
```

for some colour `e`, although `support(Z^e[S])` has a perfect matching.

First suppose that `P_c union P_d` is disconnected for some distinct
colours `c,d`.  It is a spanning disjoint union of alternating even cycles.
Let `A` be the vertex set of one component.  Then `P_c` matches `A`, while
`P_d` matches `V-A`.  Both sets are nonempty, proper, and even.  Equation
(4) forces at least one of

```text
haf(Z^c[A]),       haf(Z^d[V-A])                      (18)
```

to vanish, and the relevant matching proves supportedness.  This gives
(17).

It remains to suppose that every `P_c union P_d` is one Hamiltonian
alternating cycle.  Choose an edge `r in R_P`.  Since `R_P subset D`, choose a
colour `c` with `Z_r^c!=0`, and choose `d!=c`; let `k` be the third colour.
The edge `r` belongs to none of the `P_e`.

Every edge of the Hamiltonian cycle `P_c union P_d` flips `b_k`, and the
saturated colour-`c` chord `r` does as well.  Hence both Hamiltonian arcs
between its endpoints have odd length.  Exactly one arc starts and ends with
`P_d` edges.  Its length is neither one nor `n-1`, since either alternative
would make `r` a physical edge of `P_d` or `P_c`.  Let `A` be the vertex set
of this arc.  Then

1. the `P_d` edges on the arc match `A`;
2. the chord `r` together with the intervening `P_c` edges is a
   colour-`c` supported perfect matching of `A`; and
3. `P_d` matches `V-A`.

The set `A` is nonempty, proper, and even.  The mixed cut (4) again forces
one of `haf(Z^c[A])` and `haf(Z^d[V-A])` to vanish despite its supported
matching.  This proves (17) whenever all active graphs have perfect
matchings.  Together with Section 3, the three localized forms are exhaustive
under (1).

## 5. Universal least cancellation core (inherited)

The universal saturated zero-layer theorem already proves, without a degree
bound, that the following family is nonempty.  Its nonmonochromatic matching
`F` gives a nonzero matching monomial to every nonempty colour shore in

```text
product_c haf(Z^c[V_c])=0.
```

At least one factor therefore vanishes on a nonempty proper even shore while
its support has a perfect matching.  Sections 3--4 supply additional
localizations, scoped here under the degree-five hypothesis, to an inactive
selected-edge complement, a selected-matching component/complement, or a
Hamiltonian chord-arc/complement cut.  The later all-degree owner proves that
these localization arguments themselves need no upper-degree bound.

Among **all** pairs `(e,S)` such that `e` is a colour, `S` is a nonempty
proper even subset of `V`, `support(Z^e[S])` has a perfect matching, and
`haf(Z^e[S])=0`, choose one with `|S|` least.  This is global minimality
inside the three pure matrices, not merely minimality among the particular
cuts selected in Section 4.  For `ij subset S`, put

```text
B_ij = Z^e_ij haf(Z^e[S-{i,j}]),
A_S = {ij subset S : B_ij != 0}.                      (19)
```

The abstract scalar part of
[`MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md`](MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md)
applies to `Z^e[S]`.  Its proof uses only least supported hafnian
cancellation over a field of characteristic different from two.  It gives:

1. `A_S` is exactly the union of all perfect matchings of the support on
   `S`;
2. `A_S` is connected and matching-covered, with minimum degree at least
   two; and
3. exactly one of the following holds:

   - `A_S` is one even cycle, with exactly two nonzero matching monomials
     whose sum is zero and hence one primitive signed Laurent binomial; or
   - `A_S` has cyclomatic rank at least two, at least three perfect
     matchings, and either one vertex of degree at least four or at least two
     vertices of degree at least three.

Under assumption (1), the core is bipartite and subcubic.  To see the degree
bound, let `d,k` be the other two colours.  Active exclusivity makes
`support(Z^e)` physically disjoint from `E_d union E_k`; those two active
graphs are physically disjoint and have positive degree at every vertex.
Consequently

```text
deg_(support(Z^e))(v)
  <= deg_D(v)-deg_(E_d)(v)-deg_(E_k)(v) <= 5-1-1=3.   (19a)
```

Every saturated colour-`e` edge flips both normal bits other than `b_e`, so
either fixed one of those bits bipartitions `support(Z^e)`.  Since `A_S` is a subgraph of its
restriction to `S`, the same conclusions hold for the least core.

Write

```text
beta=|E(A_S)|-|S|+1,
t=#{v in S : deg_(A_S)(v)=3}.                         (19b)
```

All core degrees are two or three, so handshaking gives

```text
t=sum_(v in S)(deg(v)-2)=2(beta-1).                   (19c)
```

For `beta=1`, this recovers the even-cycle/binomial case.  If `beta=2`, then
exactly two vertices are cubic.  A connected matching-covered core has no
bridge: a bridge lies in every perfect matching when its deletion leaves odd
shores, while any other incident edge at either endpoint would then be
allowed by matching-coveredness but could occur in no perfect matching.
Suppressing maximal degree-two paths therefore gives three parallel routes
between the two cubic vertices.  Bipartiteness makes their lengths have one
common parity, and

```text
|S|=ell_1+ell_2+ell_3-1
```

is even, so all three route lengths are odd.  This is a closed all-odd theta.
It has exactly three perfect matchings, one for each choice of the route that
matches both cubic endpoints.  Their three nonzero monomials sum to zero; no
proper nonempty subsum can vanish, since the remaining nonzero monomial would
then also have to vanish.  Hence the relation is an exact support-minimal
trinomial cancellation.  Finally `beta>=3` gives
`t=2(beta-1)>=4` cubic vertices.

Every cubic vertex `v` of the least colour-`e` core has an exact simultaneous
label.  Its three incident core edges lie in `support(Z^e)`.  Active
exclusivity makes them disjoint from `E_d union E_k`, while positive active
degree supplies one further incident edge from each of those two graphs.
These five edges are physically distinct.  Assumption (1) therefore forces

```text
deg_D(v)=5,              deg_(support(Z^e))(v)=3.       (19d)
```

The five-edge exhaustion also shows that every incident `E_e` edge, which
carries colour `e`, is one of the three core-support edges.  Thus, writing
`a_e=deg_(E_e)(v)`, the distinguished-colour local type is exactly one of

```text
(a_e,a_d,a_k;h)=(1,1,1;2), (2,1,1;1), (3,1,1;0).      (19e)
```

In particular `(2,2,1;0)` never hosts a cubic site of any pure least core.
The `3-a_e` core edges outside `E_e` lie in `H`, carry a nonzero colour-`e`
entry, and have

```text
C_f^0=C_f^1=C_f^2=0.                                  (19f)
```

Indeed, inactivity and `Z_f^e!=0` give `C_f^e=0`; for each `d!=e`, the
oriented two-point mixed cut gives `Z_f^e C_f^d=0`, hence `C_f^d=0`.
Here these are the **global** pair-deletion cofactors on `V`; the restricted
least-core coefficient `B_f^e` on `S` is nonzero.  Thus a rank-two theta has
two full-support sites of degree at least eight, while `beta>=3` has at least
`2(beta-1)>=4` such sites by (27) below.

The single-cycle/branching-core dichotomy itself is universal and inherited.
Global minimization may select a smaller cancellation than any cut produced
in Sections 3--4, so the least core does not silently inherit that cut's
labels.

## 6. Sharp exact controls

The following controls delimit what the inherited local identities can prove.
They are **not** all-bridge witnesses.

### 6.1 A Hall-deficient active graph exposes the complement cancellation

On vertices `1,...,6`, take one hollow symmetric matrix with

```text
z_12 = -1,
z_13 = z_14 = z_25 = z_26 = z_35 = z_46 = 1,         (20)
```

and all other entries zero.  Its three nonzero matching monomials have
weights `-1,1,1`, so the full hafnian is one.  Its active scores are

```text
s_12 = -1,
s_13 = s_14 = s_25 = s_26 = 1,
s_35 = s_46 = 0.                                     (21)
```

Thus every vertex score sum is one, while the active graph is the balanced
bipartite double-star with degree sequence `(3,3,1,1,1,1)`.  The two leaves
adjacent only to the same centre violate Hall's condition, so it has no
perfect matching.  The three nonzero full matching monomials are

```text
{12,35,46},       {13,25,46},       {14,26,35}.       (21a)
```

Every one contains `35` or `46`, both inactive because its complementary
hafnian is zero; deleting that edge leaves the displayed supported complement
matching.  The whole support is bipartite and can be assigned the
single-colour normal-bit flip.  This is a sharp one-colour model of the first
localized form, not a simultaneous three-colour all-bridge witness.

### 6.2 Active branching can still contain a perfect matching

On a bipartition with three vertices per shore, give all three edges incident
with one shore vertex weight `1/6` and every other `K_(3,3)` edge weight one.
Each of the six perfect matchings has weight `1/6`, so the hafnian is one.
Every edge score is `1/3`, making the active graph all of `K_(3,3)`.  It is
branching but has many perfect matchings and therefore enters Sections 3--4
rather than forming a separate exit.  This too is only a one-colour control.

### 6.3 Maximum-degree-two residuals can cancel exactly

On vertices `1,...,6`, let

```text
P = {15,26,34},
R_0 = {12,13,24,56},                                 (22)
```

give every edge weight one except `z_24=-1`.  Then `P` is a perfect matching,
`Delta(R_0)=2`, the full hafnian is `1+1-1=1`, and every edge of `P` is
active.  Nevertheless

```text
haf(Z[{1,2,3,4}]) = z_12 z_34 + z_13 z_24 = 0.       (23)
```

Therefore the degree-four noncancellation lemma is false if “partial
matching” is replaced merely by “graph of maximum degree two.”

### 6.4 Mixed cuts are indispensable

There is an exact eight-vertex typed support control satisfying monochromatic
normalization, score-one identities, active exclusivity, all saturated
bit-flip rules, the local degree-five pattern `(1,1,1;2)`, and even pairwise
Hamiltonicity of its active matchings.

Assign normal types to vertices `0,...,7` by

```text
000, 011, 101, 110, 110, 101, 001, 010.               (24)
```

Put unit weights on

```text
E_0 = {01,23,45,67},
E_1 = {02,14,36,57},
E_2 = {03,15,27,46},                                  (25)
```

and add the inactive unit edges `04` in colour `2` and `05` in colour `1`.
Each `Z^c` has its displayed `E_c` as the unique full perfect matching and
has hafnian one; the extra edge has zero complementary cofactor.  All three
pairwise unions in (25) are Hamiltonian cycles.  Vertex zero has saturated
degree five.

This control fails the true mixed cut.  For

```text
A = {2,3,6,7},
```

`Z^0[A]` has the unique matching `{23,67}`, while `Z^1[V-A]` has the unique
matching `{05,14}`.  Both hafnians equal one, contradicting (4).  Thus the
mixed-cut step in Section 4 is load-bearing rather than decorative.

## 7. Unconditional full-support degree-eight boundary

Let `G` be the full essential block-support skeleton and let `D_diag` contain
all edges carrying any diagonal block entry `W_ij[c,c]`.  Then

```text
D subset D_diag subset G.                            (26)
```

Before imposing any maximum-full-support hypothesis, the balanced all-bridge
generic-killer theorem supplies at every vertex three distinct incident
coordinate-primary singleton blocks, one for each target colour.  They are
off-diagonal and therefore lie outside `D_diag`.  Only this unconditional
pre-assumption lemma from the later maximum-full-support theorem is imported
here.  Hence

```text
deg_G(v) >= deg_D(v)+3.                               (27)
```

The maximum-degree-four active-deck theorem already proves `Delta(D)>=5` for
every simultaneous balanced all-bridge witness.  Choose a vertex `v` with
`deg_D(v)>=5`.  Equation (27) gives

```text
Delta(G) >= deg_G(v) >= 8.                            (28)
```

Since `G` is simple and `n` is even, this also forces `n>=10`.  Thus every
all-bridge support of maximum full-support degree at most seven is excluded,
without assuming (1).  This strictly strengthens the old maximum-full-
support-degree-five boundary and subsumes the earlier exact-degree-six
obstruction as an exclusion statement; their internal structural conclusions
and provenance remain separately owned.

## 8. Dependencies, checks, and exact boundary

The load-bearing inherited results are:

1. [`ALL_BRIDGE_ACTIVE_DECK_EXCLUSIVITY_AND_CUBIC_DIAGONAL_EXCLUSION.md`](ALL_BRIDGE_ACTIVE_DECK_EXCLUSIVITY_AND_CUBIC_DIAGONAL_EXCLUSION.md): score-one identities, active exclusivity, and the saturated graph;
2. [`ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FOUR_EXCLUSION.md`](ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FOUR_EXCLUSION.md): exclusion of `Delta(D)<=4` and the Hamiltonian chord construction;
3. [`UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md`](UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md): saturated bit-flip characterization and the universal existence of a proper supported pure cancellation;
4. [`HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md`](HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md): mixed complementary-product equation (4);
5. [`MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md`](MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md): the abstract least-cancellation core theorem; and
6. [`FIVE_REGULAR_BALANCED_BRIDGE_DIAGONAL_BACKBONE.md`](FIVE_REGULAR_BALANCED_BRIDGE_DIAGONAL_BACKBONE.md): only its pre-degree-assumption derivation of the three distinct off-diagonal singleton killers, used for (27).

Focused exact checks:

```text
python claims/arbitrary-order/verify_all_bridge_active_deck_maximum_degree_five_branching_or_cancellation_core_reduction.py
python claims/arbitrary-order/audit_all_bridge_active_deck_maximum_degree_five_branching_or_cancellation_core_reduction.py
```

The primary script checks the degree table, Hall-deficient complement
interface, selected-pair and Hamiltonian-chord interfaces, scalar controls,
least-core rank strata, the typed eight-vertex control, and the degree-eight
full-support arithmetic by exact matching and graph enumeration.
The independent audit shares no imports with it and uses a separate bitmask
hafnian recurrence and graph routines.  These bounded programs verify the
displayed finite interfaces; the written arbitrary-order argument is the
proof.

```text
simultaneous all-bridge Delta(D)<=4:                  EXCLUDED;
simultaneous all-bridge Delta(D)=5 (this theorem):
  inactive-edge complement / selected-pair component /
  Hamiltonian chord-arc localized cancellation:      PROVED EXHAUSTIVE;
same localized trichotomy at every Delta(D):           PROVED LATER;
impossibility of all three localized forms:           OPEN;
Hall-deficient active deck:
  two inactive repairs with common cofactor zeros:   PROVED;
universal least pure cancellation core:
  cycle / rank-2 all-odd theta / rank>=3 core:        PROVED REDUCTION / OPEN;
maximum full-support degree <=7:                      EXCLUDED;
all-bridge even orders n=6,8:                         EXCLUDED;
Delta(D)>=6 exclusion within Delta(G)>=8:              OPEN;
deeper-blocker branch:                                OPEN;
universal extraction/gluing:                         NOT PROVED;
global Krenn--Gu conjecture:                         UNRESOLVED.
```
