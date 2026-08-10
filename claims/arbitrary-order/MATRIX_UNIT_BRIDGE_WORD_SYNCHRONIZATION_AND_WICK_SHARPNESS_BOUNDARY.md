# Matrix-unit bridge word synchronization and Wick sharpness boundary

## Status

This note proves an exact sharpness boundary for the `r=1` matrix-unit
branch over `C`.  The binary bridge-square and ternary bridge-hexagon
promotions do not preserve the endpoint word: every endpoint in the promoted
block changes colour.  A complete six-vertex graph with one
nonzero matrix unit on every physical pair then shows that global parity,
all mixed-word cancellations, and the relevant full rigid-head Wick towers
and anchored-cut equations still do not repair the binary-square word
change.  A second complete six-vertex relay shows that even all three pure
target coefficients together with fully active pure-edge cofactors do not
force a word-preserving diagonal rematching.  Neither gadget realizes a
ternary bridge hexagon.

The example realizes `+/- e_a^(star tensor 6)`, not `Delta_(6,3)`.  Its pure
`b` coefficient and its third-colour coefficient are zero.  It is therefore
not a Krenn--Gu witness or counterexample.  The exact conclusion is that any
word-synchronizing argument needs information beyond the parity,
mixed-word-cancellation, and Wick equations used here.  Simultaneous
pure-support/cofactor activation alone is also insufficient.  The relay
identifies the exact remaining support target: higher mixed identities would
have to force perfect matchings in the pure graphs induced on the word
shores (equivalently, their Tutte inequalities), or supply some different
global mechanism.  This is a target, not an exhaustive route theorem.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Local bridge normalization necessarily changes the word

Work in the one-matrix-unit branch.  A physical pair has one nonzero unit,
so it cannot carry two different diagonal labels.

### Theorem 1 (binary square word flip)

Under the hypotheses of the imported bridge-square theorem, let `a!=b` and
suppose its selected matching contains two offdiagonal edges

```text
u_1(a)--v_1(b),       u_2(a)--v_2(b).                 (1)
```

On the no-deeper branch, the bridge-square theorem forces

```text
u_1u_2=(b,b),         v_1v_2=(a,a).                   (2)
```

Replacing (1) by (2) changes the word at all four vertices:

```text
(u_1,u_2,v_1,v_2):   (a,a,b,b) -> (b,b,a,a).         (3)
```

There is no diagonal perfect matching on these four vertices inducing the
word on the left.  Such a matching would have to pair the two `a` positions
and the two `b` positions, requiring

```text
u_1u_2=(a,a),         v_1v_2=(b,b),                   (4)
```

which is incompatible with the unique units in (2).  Either of the other
pairings joins an `a` position to a `b` position and therefore cannot induce
the original word using diagonal edges.

### Theorem 2 (ternary hexagon word flip)

Under the hypotheses of the imported ternary bridge-hexagon theorem, write
the three selected offdiagonal types as

```text
u_0(0)--u_1(1),
v_0(0)--v_2(2),
w_1(1)--w_2(2).                                      (5)
```

The no-deeper hexagon promotion is

```text
u_1v_2=(0,0),
u_0w_2=(1,1),
v_0w_1=(2,2).                                        (6)
```

Again every endpoint changes colour.  The unique diagonal matching on
exactly these six endpoints that could preserve the word in (5) instead
requires

```text
u_0v_0=(0,0),
u_1w_1=(1,1),
v_2w_2=(2,2).                                        (7)
```

None of (7) is supplied by (6).  Thus the forced hexagon promotion itself
cannot preserve the word.  A word-preserving diagonal upgrade on exactly
these six endpoints would have to prove the three additional units (7).
Any alternative would require a different rematching, possibly outside the
block.  Neither conclusion follows from the bridge hexagon.

## 2. A complete six-vertex sharpness gadget

Use colours `a=0`, `b=1`; colour `2` will be absent.  Put

```text
U={u_1,u_2,x,y},       V={v_1,v_2}.                   (8)
```

Every `U--V` pair has label `a` at its `U` endpoint and `b` at its `V`
endpoint.  With rows indexed by `v_1,v_2` and columns by `u_1,u_2,x,y`, its
weight matrix is

```text
       u_1  u_2   x   y
v_1     1   -1   1   1
v_2     1    1  -1   1.                              (9)
```

The edge inside `V` is

```text
v_1v_2=(a,a), weight 1.                               (10)
```

The six edges inside `U` are

```text
u_1u_2=(b,b), weight  1,      xy=(b,b), weight  1,
u_1x  =(b,b), weight  1,      u_2y=(b,b), weight -1,
u_1y  =(a,a), weight  1,      u_2x=(a,a), weight -1.  (11)
```

Equations (9)--(11) specify all fifteen physical pairs, and every weight is
nonzero.

### Theorem 3 (exact tensor and parity)

The graph in (8)--(11) satisfies

```text
T_W=-e_a^(star tensor 6).                             (12)
```

In particular every matching has colour-count parity `000`, and every mixed
coefficient is exactly zero.

### Proof

A perfect matching crosses `U|V` in zero or two edges, because `|V|=2`.
Every cross edge is of type `{a,b}`, so every induced word has even `a` and
`b` counts and zero third-colour count.

In the zero-cross sector, the edge `v_1v_2` is forced.  The three perfect
matchings of `U` are

```text
u_1u_2 | xy,         weight  1, word bbbb,
u_1x   | u_2y,       weight -1, word bbbb,
u_1y   | u_2x,       weight -1, word aaaa.            (13)
```

The first two cancel, and the third contributes `-e_a^(star tensor 6)`.

In the two-cross sector, leave one pair `e` of `U` internally matched.  The
two vertices of `V` match bijectively to the complementary two columns of
(9), so the coefficient is the weight of `e` times the corresponding
`2 x 2` permanent.  The complements of the four `b`-edges give

```text
per(F_[x,y])=0,
per(F_[u_1,u_2])=0,
per(F_[u_2,y])=0,
per(F_[u_1,x])=0.                                    (14)
```

For the two `a`-edges,

```text
weight(u_1y) per(F_[u_2,x]) =  2,
weight(u_2x) per(F_[u_1,y]) = -2.                    (15)
```

They induce the same word--`a` on `U` and `b` on `V`--and cancel.  Hence the
entire two-cross sector is zero, proving (12).

Multiplying every edge incident with one fixed vertex by `-1` multiplies
every perfect-matching term by `-1`.  This vertex gauge converts (12) to
`+e_a^(star tensor 6)` without changing labels, support, or any vanishing
coefficient.

### Corollary 4 (the two cancellations are wordwise and separate)

The matching

```text
u_1v_1 | u_2v_2 | xy                                  (16)
```

has word `(a,a,b,b,b,b)` in the vertex order
`(u_1,u_2,v_1,v_2,x,y)` and weight `1`.  It cancels with

```text
u_1v_2 | u_2v_1 | xy,        weight -1.              (17)
```

Its bridge normalization

```text
u_1u_2 | v_1v_2 | xy                                  (18)
```

has the different word `(b,b,a,a,b,b)` and weight `1`.  That coefficient
cancels separately against

```text
u_1x | u_2y | v_1v_2,        weight -1.              (19)
```

Thus exact wordwise cancellation does not identify a matching with its
bridge normalization.

## 3. Maximum-root and rigid-head properties

### Theorem 5 (maximum torus-root number one)

The graph (8)--(11) has maximum torus-root number `r=1`.

### Proof

Every pair block is one nonzero matrix monomial.  On two fully supported
local vectors its value is the product of two nonzero coordinates and a
nonzero edge weight, hence is nonzero.  No two vertices can be zero-coupled.
Every singleton is a torus-root configuration, so the maximum is exactly
one.

For colour `a`, the nonrigidity tails and rigid heads are

```text
S_a=V,                 R_a=U.                         (20)
```

For colour `b`, they are

```text
S_b=U,                 R_b=V.                         (21)
```

Indeed, every cross edge points from `V` to `U` as an `a`-flag and from `U`
to `V` as a `b`-flag.  There are no other cross-colour units.

### Theorem 6 (full relevant Wick towers and anchored cuts)

For `(c,d)=(a,b)` and `(b,a)`, every nonempty rigid-head subset obeys the
all-order identity

```text
0 = sum_(J subset T, |T-J| even)
      haf(Z^c[T-J])
      sum_(injections phi:J->S_c)
        product_(r in J) F_(phi(r),r)^(d,c)
        haf(Z^d[Omega-(T union phi(J))]).              (22)
```

For every proper `T subsetneq R_c`, one also has

```text
haf(Z^c[S_c union T]) haf(Z^d[R_c-T])=0.              (23)
```

For `c in {a,b}` and `d=2`, the corresponding Wick equations vanish
termwise.  No anchored-cut claim is made with `c=2`, because its required
nonempty tail-set hypothesis fails in this gadget.

### Proof

The matching partition behind (22) is reversible: a `c`-head either pairs
internally through `Z^c` or injects into a distinct tail through a flag, and
the residue is pure `d`.  Thus its right side is exactly the coefficient of
the word equal to `c` on `T` and `d` elsewhere.  That word is mixed, so (12)
makes the coefficient zero.  The same rigid-head prohibition separates the
two shores in (23), making its product the coefficient of another mixed
word; it is zero by (12).  When `c in {a,b}` and `d=2`, no unit carries the
residual colour, so every displayed Wick summand is zero where required.

In particular, the square (16) uses the bridge alternative for both colours:
`v_1v_2=(a,a)` for the two `a`-tails and `u_1u_2=(b,b)` for the two
`b`-tails.  The exact Wick equations permit the permanent cancellation
(16)--(17), while the anchored-cut equation permits the independent pure
hafnian cancellation (18)--(19).  Neither equation synchronizes the words.

## 4. Fully active pure cofactors still do not synchronize the word

Use vertices `1,...,6`, colours `a=0`, `b=1`, `c=2`, and the selected word

```text
omega=(a,a,b,b,c,c).                                  (24)
```

Put weight `+1` on every edge except `16`, which has weight `-1`.  The three
pure support graphs are the unique perfect matchings

```text
M_a={34,15,26},
M_b={12,36,45},
M_c={56,14,23}.                                       (25)
```

Assign the remaining six physical pairs, with labels written in the displayed
endpoint order, by

```text
13=(a,b),   24=(a,b),   16=(a,c),
35=(b,c),   25=(b,a),   46=(c,a).                    (26)
```

Equations (25)--(26) specify all fifteen pairs by nonzero matrix units.

### Theorem 7 (pure-active relay countermechanism)

The graph (25)--(26) has all three pure coefficients equal to `1`.  Every
pure edge has complementary pure hafnian `1`, so every vertex is met by an
active pure edge of every colour.  Nevertheless the coefficient of `omega`
has exactly the two terms

```text
F=13|24|56,       weight +1,
G=16|24|35,       weight -1,                          (27)
```

and is zero, while no diagonal matching induces `omega`.

### Proof

Each graph in (25) is a single weight-one perfect matching, proving the pure
coefficient assertion.  Deleting any one of its edges leaves its other two
edges, so every displayed pure-edge cofactor is also `1`.

For `omega`, vertex `2` can use only `24`, so that edge is forced.  The
remaining eligible graph on `{1,3,5,6}` is the four-cycle

```text
1--3--5--6--1.
```

Its two perfect matchings are exactly the residual parts of `F` and `G`.
Their products are `+1` and `-1`, proving the cancellation and its
exhaustiveness.

A diagonal matching inducing `omega` would have to use

```text
12=(a,a),       34=(b,b),       56=(c,c).             (28)
```

But the unique units on `12` and `34` are respectively `(b,b)` and `(a,a)`.
Thus the promoted bridge edges are fully pure-cofactor-active but have the
wrong colours for the selected word.  The cancellation is instead relayed
through the external four-cycle.  As every pair block is a nonzero matrix
unit, the same torus argument as Theorem 5 gives maximum root number `1`.

This is still not a Krenn--Gu witness.  For example, `15|24|36` is the
unique matching inducing

```text
(a,a,b,b,a,b),                                        (29)
```

and contributes `+1` to that forbidden coefficient.

### Corollary 8 (the exact word-conformal matching obligation)

For any matrix-unit graph and any word `chi`, put
`V_d={v:chi(v)=d}` and let `G_d` be the pure-`d` support graph.  A diagonal
matching inducing `chi` exists if and only if every induced graph
`G_d[V_d]` has a perfect matching.  Equivalently, by
[Tutte's one-factor theorem](https://doi.org/10.1112/jlms/s1-22.2.107),
each shore must satisfy

```text
odd_components(G_d[V_d]-X) <= |X|   for every X subset V_d.          (30)
```

Indeed, a diagonal matching never crosses between two word shores, so it
restricts to one perfect matching in every `G_d[V_d]`; conversely the union
of those shore matchings is diagonal and induces `chi`.

The global pure matchings in (25) do not imply these induced conditions.
For `omega`, both `G_a[{1,2}]` and `G_b[{3,4}]` are edgeless two-vertex
graphs.  Their active global pure matchings export those vertices through
the third shore.  Thus full pure activation supplies alternating-cycle
routing, not the word-conformal Tutte inequalities.

## 5. Scope and load-bearing boundary

The first gadget is not a Krenn--Gu witness.  Equation (12) gives

```text
[T_W]_(a,a,a,a,a,a)=-1,
[T_W]_(b,b,b,b,b,b)=0,
[T_W]_(2,2,2,2,2,2)=0.                               (31)
```

After the vertex gauge, the first coefficient is `+1`, but the other two
remain zero.  Structurally, a pure-`b` matching cannot cover `V`: the edge
inside `V` is pure `a`, while every edge from `V` to `U` has label `a` at
its `U` endpoint.  No edge uses colour `2`.

The bridge square/hexagon and rigid-head Wick identities are imported from
[`MATRIX_UNIT_CROSS_PARITY_ERASURE_RIGID_HEAD_WICK_AND_BRIDGE_CORE_REDUCTION_THEOREM.md`](MATRIX_UNIT_CROSS_PARITY_ERASURE_RIGID_HEAD_WICK_AND_BRIDGE_CORE_REDUCTION_THEOREM.md).
The local word-flip obstruction, both complete six-vertex sharpness gadgets,
and the word-conformal matching formulation are new here.

```text
local square/hexagon normalization preserves word: FALSE;
complete all-nonzero matrix-unit sharpness gadget:  PROVED;
gadget realizes ternary bridge-hex sharpness:       FALSE;
maximum torus-root number of the gadget:            EXACTLY ONE;
all matching parity sectors:                        000;
all mixed coefficients:                             ZERO EXACTLY;
relevant rigid-head Wick towers and cuts:           SATISFIED EXACTLY;
first gadget has simultaneous pure targets:         FALSE;
second gadget has all pure targets/cofactors active: TRUE EXACTLY;
second gadget has word-preserving diagonal relay:    FALSE;
either gadget is a Krenn-Gu witness:                 FALSE;
parity plus mixed-word/Wick equations alone sync:   REFUTED;
pure-support/cofactor activation alone syncs:        REFUTED;
higher mixed identities force word-shore Tutte:     UNKNOWN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

## Focused check

Run from repository root:

```text
python claims/arbitrary-order/verify_matrix_unit_bridge_word_synchronization_and_wick_sharpness.py
python claims/arbitrary-order/audit_matrix_unit_bridge_word_synchronization_and_wick_sharpness.py
```

The checker directly enumerates the fifteen perfect matchings in each
six-vertex gadget.  It verifies the first edge table, both wordwise
cancellations, the exact tensor and gauge, parity, the `S_a/R_a` and
`S_b/R_b` sets, and every subset in the displayed Wick and anchored-cut
equations.  It separately verifies the relay's three pure coefficients,
all pure-edge cofactors, exhaustive two-term selected-word cancellation,
absence of a diagonal word matching, and an explicit nonzero forbidden
coefficient.  These are bounded exact convention and falsification checks.
The universal local obstruction and arbitrary-subset Wick partition, and
the word-shore equivalence, are the written proofs above.

The independent audit does not import the primary checker.  It uses a
word-indexed bitmask dynamic program over all `3^6` assignments and a
separate pure-hafnian cache.  It reconstructs the relay table, pure targets
and cofactors, near-monochromatic active-deck rows, the exhaustive selected
coefficient, absence of a diagonal rematching, and an explicit failing
coefficient.  It remains bounded evidence for the displayed six-vertex
countermechanism, not a proof of the arbitrary-order statements or a global
counterexample.
