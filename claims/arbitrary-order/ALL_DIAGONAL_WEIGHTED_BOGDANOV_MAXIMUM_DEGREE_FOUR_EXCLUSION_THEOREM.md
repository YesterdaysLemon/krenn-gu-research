# All-diagonal weighted Bogdanov: even active cycles and maximum-degree-four exclusion

## Status

This is an exact arbitrary-order theorem over `C` in the **all-diagonal
branch**: every edge block is a diagonal matrix, equivalently every edge is
monochromatic with an arbitrary complex weight.  It proves that no
all-diagonal witness has maximum support degree at most four.  It is not a
proof of the Krenn--Gu conjecture, it does not apply to blocks with
bichromatic entries, and it is not the repository's simultaneous balanced
all-bridge branch (whose normal form has off-diagonal singleton killers).
The global conjecture remains **UNRESOLVED**.

The theorem was written to settle the first lemma named in the
[fibre-exact targets brief](../../docs/strategy/fibre-exact-targets-2026-09-01.md):
whether active colour-`c` cycles are even when all blocks are diagonal.  They
are, for a reason simpler than the normal-type bit flips used in the
all-bridge lane, and the rest of the degree-four argument then transfers
with a shorter ending.

## Setting

Let `V` have even size `n >= 6`.  An **all-diagonal witness** is a triple of
hollow symmetric complex matrices `Z^0, Z^1, Z^2` on `V` whose diagonal
blocks `W_ij = diag(Z^0_ij, Z^1_ij, Z^2_ij)` satisfy `T_W = Delta_n`.  For
even `A subset V` write `f_c(A) = haf(Z^c[A])`, with `f_c(empty) = 1`, and
for a word `a` let `V_c(a) = {v : a_v = c}`.  Because every edge is
monochromatic, a perfect matching contributes to the word `a` only if each of
its edges joins two vertices of the same colour, so

```text
T_W(a) = f_0(V_0(a)) f_1(V_1(a)) f_2(V_2(a)),                              (F)
```

where an odd class makes its factor zero.  Hence `T_W = Delta_n` is exactly

```text
(H1)  f_c(V) = 1                                   for c = 0,1,2;
(H2)  f_0(V_0) f_1(V_1) f_2(V_2) = 0               for every ordered partition
                                                   of V into even parts that
                                                   does not put all of V in
                                                   one part.
```

(H2) with two parts reads `f_c(A) f_d(V - A) = 0` for `c != d` and every
even `A` with `empty != A != V`.  This is the complex-weight form of the
problem Bogdanov solved for positive weights, hence "weighted Bogdanov".

Notation.  `D` is the simple graph of pairs `{i,j}` with `Z^c_ij != 0` for at
least one `c`.  For a pair `e = {i,j}` the colour-`c` **cofactor** is
`C^c_e = f_c(V - e)`, the **score** is `s^c_e = Z^c_e C^c_e`, and `e` is
**active in colour `c`** when `s^c_e != 0`; `E_c` is the graph of such pairs.

## Theorem

**Theorem 1 (active structure).**  In every all-diagonal witness:

1. (Laplace) for every vertex `v` and colour `c`, `sum_(u != v) s^c_(vu) = 1`,
   so `E_c` has minimum degree at least one;
2. (exclusivity) if `e` is active in colour `c` then `Z^d_e = 0` and
   `C^d_e = 0` for both `d != c`; in particular `E_0, E_1, E_2` are pairwise
   disjoint and `D` has minimum degree at least three;
3. (even active cycles) if `Delta(D) <= 4`, every cycle of `E_c` is a
   connected component of the support graph of `Z^c` and has even length.

**Theorem 2 (degree-four exclusion).**  No all-diagonal witness has
`Delta(D) <= 4`.  Equivalently, every all-diagonal witness has a vertex
incident with at least five pairs carrying a nonzero weight in some colour.

The border families of the GHZ closure theorem are all-diagonal and cubic
(`Delta(D) = 3`); Theorem 2 confirms that none of them is an exact witness,
as the closure theorem already asserted from the six-vertex exclusion.

## Proof

Throughout, (F) is used only in the form (H1), (H2).

*Step 1 (Laplace).*  Expanding `f_c(V) = 1` along `v` gives
`sum_u Z^c_(vu) f_c(V - {v,u}) = 1`, which is item 1.

*Step 2 (exclusivity).*  Let `e` be active in colour `c` and `d != c`.
Apply (H2) with two parts to `A = e` and to `A = V - e`:

```text
Z^c_e f_d(V - e) = 0,        f_c(V - e) Z^d_e = 0.
```

Both `Z^c_e` and `C^c_e = f_c(V - e)` are nonzero, so `C^d_e = 0` and
`Z^d_e = 0`.  A pair active in two colours would need a nonzero weight in
each, so the `E_c` are pairwise disjoint; with item 1 this gives three
distinct incident pairs at every vertex, so `deg_D >= 3`.

Assume from now on that `Delta(D) <= 4`.

*Step 3 (degrees).*  Each `E_c` has degree at least one at every vertex and
the three are disjoint subgraphs of `D`, so every vertex has `E_c`-degree one
or two, and the `E_c`-degree triple is a permutation of `(1,1,1)` or
`(2,1,1)`.  Thus every `E_c` is a disjoint union of paths and cycles.

*Step 4 (path components are single edges).*  Let a path component of `E_c`
have at least two edges and let `v` be an endpoint with active edge `e_1`.
Nonactive pairs have score zero, so Step 1 at `v` gives `s(e_1) = 1`.  At the
next vertex, of `E_c`-degree two, Step 1 gives `s(e_1) + s(e_2) = 1`, hence
`s(e_2) = 0`, contradicting activity.  So every path component is a single
edge, of score one.

*Step 5 (even cycles; Theorem 1, item 3).*  Let `C` be a cycle component of
`E_c` with vertex set `U`.  A vertex `v in U` has `E_c`-degree two, hence
`E_d`- and `E_e`-degree one for the other colours and `D`-degree exactly four.
Its four `D`-neighbours are its two cycle neighbours and its active partners
`p_d(v), p_e(v)`; these are four distinct vertices because the `E`-graphs are
pairwise disjoint as sets of pairs.  By exclusivity `Z^c_(v p_d(v)) =
Z^c_(v p_e(v)) = 0`, and `supp(Z^c) subset D`.  Therefore the colour-`c`
neighbours of `v` are exactly its two cycle neighbours.  Consequently
`Z^c[U]` is the cycle `C` itself, with no chords, and there is no colour-`c`
pair between `U` and `V - U`: `U` is a union of connected components of
`supp(Z^c)`.  The hafnian factorizes over components,

```text
f_c(V) = haf(Z^c[U]) haf(Z^c[V - U]).
```

If `|U|` were odd the first factor would vanish, contradicting (H1).  So
every active cycle is even.  (The same factorization shows directly that for
`e in C`, `C^c_e = haf(Z^c[U - e]) haf(Z^c[V - U])`, the first factor being
the unique matching of a path.)

*Step 6 (a perfect matching inside each `E_c`).*  Let `P_c` consist of the
single-edge components of `E_c` together with alternate edges of every
(even) cycle component, and let `Q_c` be the remaining alternate edges.  Then
`P_c` is a perfect matching of `V` and `E_c = P_c + Q_c`.

*Step 7 (the residual is a partial matching).*  Put
`H = D - (E_0 + E_1 + E_2)`.  A vertex on an `E_c`-cycle already has
`D`-degree four, so it meets no edge of `H`, and it lies on no cycle of
another colour.  A vertex on no cycle has `E`-degrees `(1,1,1)` and meets at
most one edge of `H`.  Hence `R = H + Q_0 + Q_1 + Q_2` has maximum degree
one, and `R` is edge-disjoint from every `P_c`.

*Step 8 (support of `Z^c`).*  `supp(Z^c) subset D`, and exclusivity kills
`Z^c` on `E_d` and `E_e`.  Hence `supp(Z^c) subset E_c + H = P_c + Q_c + H`,
so

```text
supp(Z^c) = P_c + R_c,     R_c = Q_c + {h in H : Z^c_h != 0} subset R,
```

with `P_c` perfect, `R_c` a partial matching, the two edge-disjoint, and all
weights on them nonzero.

*Step 9 (noncancellation).*  Let `G` be the edge-disjoint union of a perfect
matching `P` and a partial matching `R`, all weights nonzero, with
`haf(G[V]) != 0`.  Then every principal subgraph `G[A]` that has a perfect
matching has `haf(G[A]) != 0`.  Indeed the components of `P + R` are
alternating paths, of even order and starting and ending with `P`-edges, and
even alternating cycles; `haf(G[V])` is the product over paths of their
unique matching weight and over cycles of the sum of their two alternating
matching weights, so every cycle factor is nonzero.  An induced subgraph with
a perfect matching consists of even paths, each with a unique nonzero
matching, and whole cycles, each with its nonzero factor.  By (H1) and
Step 8 this applies to every `Z^c`.

*Step 10 (a rainbow word with nonzero coefficient).*  `P_0, P_1, P_2` are
pairwise disjoint perfect matchings of the same vertex set, so
`K = P_0 + P_1 + P_2` is a simple cubic graph properly three-edge-coloured
with perfect-matching colour classes.  Since `n > 4`, Bogdanov's theorem
(Chandran, Gajjala, Illickan, MFCS 2024, Theorem 1.7, already used by the
repository's universal zero-layer theorem) gives a perfect matching `F` of
`K` that is not monochromatic.  Let `V_c = V(F cap P_c)`.  At least two of
the `V_c` are nonempty, each is even, and `Z^c[V_c]` has the perfect matching
`F cap P_c` inside `supp(Z^c)`, so `f_c(V_c) != 0` by Step 9.  By (F) the
coefficient of the non-constant word that colours `V_c` by `c` is
`f_0(V_0) f_1(V_1) f_2(V_2) != 0`, contradicting (H2).  This proves
Theorem 2, and Theorem 1 was proved along the way.  ∎

## What the argument uses, and what breaks at degree five

The proof uses only the Laplace identity, the two- and three-part instances
of (H2), the factorization of hafnians over components, the noncancellation
lemma, and Bogdanov's theorem.  Compared with the all-bridge degree-four
exclusion it needs no normal types, no bit flips, no pairwise Hamiltonicity,
and no Hamiltonian-chord argument: the even-cycle lemma comes from the
component factorization and (H1), and Bogdanov's rainbow matching finishes
directly through (F).

At `Delta(D) = 5` three things fail at once, and the next all-diagonal
lemma must confront them:

1. a vertex may have `E_c`-degree three, so `E_c` is no longer a union of
   paths and cycles and Step 4's score alternation gives only
   `s_1 + s_2 + s_3 = 1`;
2. a vertex on an `E_c`-cycle may carry one residual edge, so `U` need not be
   a union of colour-`c` components and Step 5's factorization fails;
3. consequently `supp(Z^c)` need not be a perfect matching plus a partial
   matching, and the noncancellation lemma of Step 9 no longer applies, so a
   rainbow matching of `P_0 + P_1 + P_2` may induce a word whose factors
   cancel.

Item 3 is the exact point where complex cancellation first has room to act
in the all-diagonal branch.  The natural next statement is: *for an
all-diagonal witness with `Delta(D) = 5`, either some `f_c(V_c(F))` is a
supported pure cancellation for every rainbow `F`, or the witness is
excluded.*

## Scope and boundary

- The theorem is exact over `C` at every even `n >= 6` in the all-diagonal
  branch only.  Any bichromatic entry, however small, leaves its hypotheses.
- It does not bound `Delta(D)` for general witnesses, does not close the
  all-diagonal branch (`Delta(D) >= 5` remains open there), and does not
  change the status of the all-bridge or deeper-blocker branches.
- Bogdanov's theorem is imported through the same citation the repository
  already uses; no other external result is used.

## Verification

```text
python claims/arbitrary-order/verify_all_diagonal_weighted_bogdanov_maximum_degree_four_exclusion.py
python claims/arbitrary-order/audit_all_diagonal_weighted_bogdanov_maximum_degree_four_exclusion.py
```

The primary verifier checks, in exact rational arithmetic, the factorization
(F) on random all-diagonal blocks at `n = 6`, the noncancellation lemma on
random perfect-plus-partial-matching supports at `n = 6, 8`, the vanishing of
`f_c(V)` and of every cycle cofactor when an odd cycle is a colour-`c`
component, the degree bookkeeping of Step 3, and Bogdanov's theorem
exhaustively for all triples of pairwise disjoint perfect matchings of `K_6`
and `K_8`.  The independent audit re-derives each of these with different
algorithms (Laplace-recursion hafnians, bitmask matching enumeration,
explicit component-factorization formulas, and a complex floating-point
control of (F)).  The written argument above is the proof; the programs are
bounded checks of its lemmas.
