# All-bridge active-deck maximum-degree-five branching or cancellation-core reduction

## Status

This is an exact arbitrary-order reduction over characteristic zero in the
simultaneous three-colour balanced all-bridge branch.  Let `D` be the physical
graph of saturated diagonal entries.  If a hypothetical witness satisfies

```text
Delta(D) <= 5,                                        (1)
```

then the already proved maximum-degree-four exclusion makes
`Delta(D)=5`, and at least one of the following three exits occurs:

1. **active branching:** some colour active-deck graph `E_c` has a vertex of
   degree three;
2. **primitive pure cancellation cycle:** every `E_c` is nonbranching, and a
   least proper supported pure-colour hafnian cancellation has active
   cofactor graph equal to one even cycle; or
3. **pure branching cancellation core:** every `E_c` is nonbranching, and a
   least proper supported pure-colour hafnian cancellation has a connected
   matching-covered active cofactor graph of cyclomatic rank at least two.

In the last branch, the core has either a vertex of degree at least four or
at least two vertices of degree at least three.  At every vertex of saturated
degree five, the full essential support skeleton has degree at least eight.

This is a structural reduction, not an exclusion.  None of the three exits is
closed here, the separate deeper-blocker branch is untouched, and the global
Krenn--Gu conjecture remains **UNRESOLVED**.

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

If some `a_c(v)=3`, the first exit in the status statement holds.  For the
rest of the proof assume

```text
Delta(E_c) <= 2 for every c.                          (12)
```

## 3. Nonbranching active decks and the degree-two residual

Under (12), every component of `E_c` is a path or a cycle.  At an endpoint
of a path, (6) forces the unique incident active score to be one.  If the
path continued through the next vertex, its other active score would have to
be zero, contradicting activity.  Hence every path component is `K_2`.

Every cycle component is even because its edges flip a fixed normal bit.
Choose one alternating half of each cycle together with every `K_2` to form
a perfect matching `P_c`; let `Q_c` be the other alternating half.  Then

```text
E_c = P_c disjoint-union Q_c,                         (13)
```

where `P_c` is perfect and `Q_c` is a partial matching.  The three `P_c` are
pairwise physically edge-disjoint.

Define the physical residual

```text
R = H union Q_0 union Q_1 union Q_2.                  (14)
```

The table (9) shows that `Delta(R)<=2`.  The possible labels at a residual
degree-two vertex are exactly

```text
H H,          H Q_c,          Q_c Q_d  (c!=d).        (15)
```

There cannot be two incident `Q_c` edges because `Q_c` is a matching.
Conversely, the three cases in (15) correspond respectively to the local
types `(1,1,1;2)`, `(2,1,1;1)`, and `(2,2,1;0)`.

The maximum-degree-four theorem already excludes `Delta(D)<=4`.  Thus (1)
forces a vertex of degree five, and (10), (12) show that this vertex has
residual degree two.  In particular, `R` is nonempty and cannot be a partial
matching.  This is the exact first place where the old decomposition fails.

Active exclusivity also gives, for every colour,

```text
support(Z^c) = P_c union R_c,
R_c = Q_c union {e in H : Z_e^c != 0} subset R.       (16)
```

Here the union is physically edge-disjoint.  Indeed, `E_c=P_c` disjoint
union `Q_c`, the three active graphs are pairwise edge-disjoint, and `H` is
disjoint from all of them.  If `Z_e^c!=0` and `e` is active in some colour
`d`, exclusivity forces `d=c`, so `e in E_c`; otherwise `e` is inactive in
every colour and belongs to `H`.

Unlike the degree-four residual, `R_c` may have degree two.  The
partial-matching noncancellation lemma therefore cannot be invoked.

## 4. The mixed cuts force a proper pure cancellation

Fix the matchings `P_c` from (13).  We prove that some proper nonempty even
set `S subset V` has

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
alternating cycle.  Choose an edge `r in R`.  Since `R subset D`, choose a
colour `c` with `Z_r^c!=0`, and choose `d!=c`; let `k` be the third colour.
The edge `r` belongs to none of the `P_e`.  If it lies in `Q_e subset E_e`,
active exclusivity forces `e=c`; if it lies in `H`, the conclusion is
immediate from the definition.  In either case `r in R_c`.

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
matching.  This proves (17) in every nonbranching case.

## 5. Least cancellation core

Section 4 proves that the following family is nonempty.  Among **all** pairs
`(e,S)` such that `e` is a colour, `S` is a nonempty proper even subset of
`V`, `support(Z^e[S])` has a perfect matching, and `haf(Z^e[S])=0`, choose
one with `|S|` least.  This is global minimality inside the three pure
matrices, not merely minimality among the particular cuts selected in
Section 4.  For `ij subset S`, put

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

Because `support(Z^e[S]) subset D[S]`, the core also has maximum degree at
most five.  These are respectively the primitive-cycle and branching-core
exits in the status statement.

## 6. Sharp exact controls

The following controls delimit what the inherited local identities can prove.
They are **not** all-bridge witnesses.

### 6.1 A balanced active graph need not have a perfect matching

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
perfect matching.  Its whole support is bipartite and can be assigned the
single-colour normal-bit flip.  This proves that hafnian normalization,
Laplace scores, and one-colour bit compatibility cannot eliminate the active
branching exit.  The matrix is not claimed to satisfy the simultaneous
three-colour mixed cuts.

### 6.2 Maximum-degree-two residuals can cancel exactly

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

### 6.3 Mixed cuts are indispensable

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

## 7. Full-support density at a degree-five vertex

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

In particular, every vertex with `deg_D(v)=5` has `deg_G(v)>=8`; since the
graph is simple and `n` is even, this also forces `n>=10`.  This also
explains why the earlier maximum-full-support-degree-five obstruction does
not close the present boundary: it bounds `G`, whereas (1) bounds only the
saturated graph `D`.

## 8. Dependencies, checks, and exact boundary

The load-bearing inherited results are:

1. [`ALL_BRIDGE_ACTIVE_DECK_EXCLUSIVITY_AND_CUBIC_DIAGONAL_EXCLUSION.md`](ALL_BRIDGE_ACTIVE_DECK_EXCLUSIVITY_AND_CUBIC_DIAGONAL_EXCLUSION.md): score-one identities, active exclusivity, and the saturated graph;
2. [`ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FOUR_EXCLUSION.md`](ALL_BRIDGE_ACTIVE_DECK_MAXIMUM_DEGREE_FOUR_EXCLUSION.md): exclusion of `Delta(D)<=4` and the Hamiltonian chord construction;
3. [`UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md`](UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md): saturated bit-flip characterization;
4. [`HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md`](HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md): mixed complementary-product equation (4);
5. [`MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md`](MATRIX_UNIT_MINIMAL_PURE_COFACTOR_MATCHING_COVERED_CORE_AND_SINGLE_CYCLE_THEOREM.md): the abstract least-cancellation core theorem; and
6. [`FIVE_REGULAR_BALANCED_BRIDGE_DIAGONAL_BACKBONE.md`](FIVE_REGULAR_BALANCED_BRIDGE_DIAGONAL_BACKBONE.md): only its pre-degree-assumption derivation of the three distinct off-diagonal singleton killers, used for (27).

Focused exact checks:

```text
python claims/arbitrary-order/verify_all_bridge_active_deck_maximum_degree_five_branching_or_cancellation_core_reduction.py
python claims/arbitrary-order/audit_all_bridge_active_deck_maximum_degree_five_branching_or_cancellation_core_reduction.py
```

The primary script checks the degree table, residual labels, Hamiltonian chord
interface, both scalar controls, and the typed eight-vertex control by exact
matching enumeration.  The independent audit shares no imports with it and
uses a separate bitmask hafnian recurrence and graph routines.  These bounded
programs verify the displayed finite interfaces; the written arbitrary-order
argument is the proof.

```text
simultaneous all-bridge Delta(D)<=4:                  EXCLUDED;
simultaneous all-bridge Delta(D)=5:
  active branching or least pure cancellation core: PROVED REDUCTION;
active branching exit:                               OPEN;
primitive pure cancellation-cycle exit:              OPEN;
pure branching cancellation-core exit:               OPEN;
deeper-blocker branch:                                OPEN;
universal extraction/gluing:                         NOT PROVED;
global Krenn--Gu conjecture:                         UNRESOLVED.
```
