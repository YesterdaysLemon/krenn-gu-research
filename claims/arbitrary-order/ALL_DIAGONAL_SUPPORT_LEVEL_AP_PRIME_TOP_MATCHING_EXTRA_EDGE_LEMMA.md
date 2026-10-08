# AP' extra-edge sub-lemma: widow-chain Hamiltonicity, the CGI core, and a locality obstruction

Date: 2026-10-08.

## Status

This document attacks one sub-lemma of the top-matching lemma of
[WB4](ALL_DIAGONAL_SUPPORT_LEVEL_AP_PRIME_BRANCHING_LEMMA_AND_PARENT_ATTEMPT.md)
(Section 7 there; the started argument is WB4 Section 8.3 on the branch
`claude/ap-prime-top-matching-20261008`).  **The sub-lemma is not proved at any
order beyond those where AP' itself has no model** (`n = 6, 8` by WB2,
`n = 10` by the WB4 certificate, where it holds vacuously).  The exact content
is:

1. **Proposition 1 (reduction):** if one colour's support graph is a perfect
   matching `M_0`, its family is exactly the family of `M_0`-unions and (H2)
   becomes a two-colour condition relative to `M_0`.  Proved.
2. **Lemma 2 (widow chains are Hamiltonian):** in that situation every
   widow-first Laplace chain of colour 1 or 2 removes a perfect matching `N`
   with `M_0 ∪ N` a Hamiltonian cycle, and the removed sets are arcs of that
   cycle.  Proved at every even order; it completes the WB4 Section 8.3
   observation and does not use the top-matching hypothesis.
3. **Proposition 3 (the CGI core):** the uniform case of the sub-lemma is
   *equivalent* to the imported nonmonochromatic-perfect-matching theorem of
   Chandran, Gajjala and Illickan for three-edge-coloured cubic graphs.  So
   every proof of the sub-lemma proves or imports that theorem.  Lemma 2 alone
   closes the uniform case when `n ≡ 2 (mod 4)`.  Proved.
4. **Theorem 4 (locality obstruction):** the axioms that suffice for the fast
   solver refutations at `n <= 10` (Laplace accessibility only at `V` and at
   its children, forcing only on sets of size at most four, full (H2), the
   top-matching hypothesis, and `G_0 = M_0`) have models at `n = 160, 162` and
   at every even `n >= 12640`.  Proved, with an exact girth check by the
   companion verifier.  The short `n <= 10` refutations therefore do not lift.
5. **Lemma 5 (conditional closure):** an "arc lemma" for one colour
   (every `N`-ended arc of one widow cycle lies in that colour's family)
   implies the sub-lemma, and in fact the stronger statement that no colour's
   support graph is a perfect matching, at every order `n ≡ 2 (mod 4)`.
   Proved; the arc lemma itself is open and is the sharpest next lemma this
   attempt identifies.

Outcome type: an exact obstruction plus an honest stall point (deliverables
(ii) and (iii) of the task), not a proof.  The all-diagonal branch and the
global Krenn–Gu conjecture remain **UNRESOLVED**.

## Setting

An AP' model on an even vertex set `V`, `|V| = n >= 6`, consists of graphs
`G_c` and families `S_c` of even subsets of `V`, `c ∈ {0, 1, 2}`, with

- (a) `∅, V ∈ S_c`, and the two-element members of `S_c` are exactly the edges
  of `G_c`;
- (L) if `A ∈ S_c` and `v ∈ A`, some `u ∈ A` has `vu ∈ G_c` and
  `A − {v, u} ∈ S_c`;
- (S) every `A ∈ S_c` has a perfect matching in `G_c[A]`;
- (F) if `G_c[A]` has exactly one perfect matching then `A ∈ S_c`;
- (H2) no ordered partition `V = A_0 ⊔ A_1 ⊔ A_2` into even classes, at least
  two nonempty, has `A_c ∈ S_c` for every `c`.

`E_c = {e ∈ G_c : V − e ∈ S_c}` is the top-active graph.  WB3/WB4 facts used:
every `E_c` has minimum degree at least one, and `E_c ∩ G_d = ∅` for `c ≠ d`.

**Target sub-lemma.**  If every `E_c` is a perfect matching `M_c` (so the
`M_c` are pairwise disjoint, `M_c ⊆ G_c`, and `G_c ∩ M_d = ∅` for `d ≠ c`),
then no colour has `G_c = M_c`.

**Stronger candidate (PM).**  No AP' model has a colour whose support graph is
a perfect matching.  (PM) implies the sub-lemma.  The solver data in Section 6
show the top-matching hypothesis plays no visible role at `n <= 10`.

## 1. Proposition 1 (reduction to a two-colour problem)

**Proposition 1.**  Let an AP' model have `G_0 = M_0`, a perfect matching.
Then `S_0` is the family of `M_0`-unions, and (H2) is equivalent to

> (R) there is no partition `V = U ⊔ A_1 ⊔ A_2` with `U` an `M_0`-union,
> `A_1 ∈ S_1`, `A_2 ∈ S_2`, and at least two of the three classes nonempty.

Consequently:

- (i) no proper nonempty `M_0`-union lies in `S_1` or in `S_2`;
- (ii) `G_1 ∩ M_0 = G_2 ∩ M_0 = ∅`;
- (iii) for disjoint nonempty `A_1 ∈ S_1`, `A_2 ∈ S_2`, the union `A_1 ∪ A_2`
  is not an `M_0`-union.

*Proof.*  A set with a perfect matching in `G_0 = M_0` is an `M_0`-union and
its perfect matching is unique, so (S) and (F) give `S_0 = {M_0-unions}`.
Then (H2) is (R).  (i) is (R) with `A_d = ∅` for the other colour `d` and
`U = V − A_c`.  (ii): an edge `e ∈ M_0 ∩ G_c` lies in `S_c` by (a) and is a
proper nonempty `M_0`-union since `n >= 4`.  (iii) is (R) with
`U = V − (A_1 ∪ A_2)`.  ∎

For `A ⊆ V` write `∂A` for the vertices of `A` whose `M_0`-partner is outside
`A`; `|∂A|` is even when `|A|` is, and (i) says `|∂A| >= 2` for every proper
nonempty `A ∈ S_1 ∪ S_2`.

## 2. Lemma 2 (widow chains are Hamiltonian)

Fix `c ∈ {1, 2}` and `ab ∈ E_c`.  A **widow-first chain** of colour `c` is a
sequence `V = A_0 ⊃ A_1 = V − ab ⊃ A_2 ⊃ ... ⊃ A_{n/2} = ∅` of members of
`S_c` in which, for `j >= 1`, `A_{j+1} = A_j − {w, u}` is a supported Laplace
child of `A_j` at a vertex `w ∈ ∂A_j` (a *widow*: its `M_0`-partner has been
removed).  By (L) such a chain exists for every choice of widows, as long as
`∂A_j ≠ ∅` for `A_j ≠ ∅`, which (i) guarantees.

**Lemma 2.**  In a model with `G_0 = M_0`, let `e_1 = ab, e_2, ..., e_{n/2}`
be the removed edges of a widow-first chain of colour `c` and
`B_j = V − A_j`.  Then

1. for `1 <= j <= n/2 − 1`, `B_j` is the vertex set of a path of
   `M_0 ∪ {e_1, ..., e_j}` whose two end edges are chain edges, and its two
   endpoints form the set `W_j` of vertices of `B_j` whose `M_0`-partners lie
   outside `B_j`; so `B_j − W_j` is an `M_0`-union, `|W_j| = 2`, and
   `∂A_j` is the set of `M_0`-partners of `W_j`;
2. `N = {e_1, ..., e_{n/2}}` is a perfect matching of `G_c` and `M_0 ∪ N` is
   a Hamiltonian cycle;
3. for `1 <= j <= n/2 − 1`, `W_j` is not an edge of `G_d` (`d ≠ c`), and more
   generally no member of `S_d` contains `W_j`, avoids `A_j`, and has `∂`
   equal to `W_j`.

*Proof.*  `N ∩ M_0 = ∅` by Proposition 1(ii), and `N` covers `V` because the
chain ends at `∅`.

(1) by induction on `j`.  For `j = 1`, `B_1 = {a, b}` and `ab ∉ M_0`, so the
claim holds with `W_1 = {a, b}`.  Suppose it holds for `j <= n/2 − 2`, with
path endpoints `W_j = {y, z}` and widows `y', z'` (their `M_0`-partners).  The
chain removes a widow, say `y'`, together with a partner `u ∈ A_j`.  If
`u = z'`, then `B_{j+1} = B_j ∪ {y', z'}` is an `M_0`-union and
`A_{j+1} = V − B_{j+1}` is a proper nonempty `M_0`-union in `S_c` (it is
nonempty because `j + 1 <= n/2 − 1`), contradicting (i).  So `u ≠ z'`, and
`u' ∉ B_j` (the only removed vertices whose partners remain are `y, z`, whose
partners are `y', z' ≠ u`).  The path extends by the `M_0`-edge `y y'` and the
chain edge `y' u`; its endpoints become `z` and `u`, and `W_{j+1} = {z, u}`.

(2) At `j = n/2 − 1` the remaining set `A_j` has two vertices, which must be
the two widows `y', z'` because `|∂A_j| = 2`; the last chain edge is `y'z'`.
The path `B_j` from `y` to `z`, the `M_0`-edges `yy'` and `zz'`, and the edge
`y'z'` form a Hamiltonian cycle `M_0 ∪ N`.

(3) Let `D ∈ S_d` with `W_j ⊆ D ⊆ B_j` and `D − W_j` an `M_0`-union.  Then
`A_j ∈ S_c` and `D ∈ S_d` are disjoint and nonempty and
`A_j ∪ D = V − (B_j − D)` is an `M_0`-union (because `B_j − D` is the
`M_0`-union part of `B_j` minus an `M_0`-union), contradicting
Proposition 1(iii).  `D = W_j` is the case `W_j ∈ G_d`.  ∎

Lemma 2 says the arcs `B_j` of the Hamiltonian cycle `C = M_0 ∪ N` (and
their complements `A_j`, also arcs of `C` with chain end edges) are the only
sets it places in `S_c`.  The cycle `C` depends on the widow choices, because
the partners chosen by (L) may depend on the history.

## 3. Proposition 3 (the uniform case is the CGI theorem)

Call a model **uniform** if `G_c` is a perfect matching for every `c`.

**Proposition 3.**  Let `K` be a simple cubic graph on `n >= 6` vertices whose
edge set is the disjoint union of three perfect matchings `M_0, M_1, M_2`.
Put `G_c = M_c` and `S_c = {M_c-unions}`.  This is an AP' model (with every
`E_c = M_c` a perfect matching and every `G_c = M_c`) if and only if `K` has
exactly three perfect matchings.  Every uniform AP' model arises this way.

*Proof.*  (a), (L), (S), (F) hold for the families of unions of a perfect
matching: a set has a perfect matching in `M_c` iff it is an `M_c`-union, and
then that matching is unique; the Laplace child of an `M_c`-union at `v`
removes the `M_c`-edge at `v`.  `E_c = M_c` because `V − e ∈ S_c` exactly for
`e ∈ M_c`.  A
partition violating (H2) gives the perfect matching
`F = ∪_c M_c|A_c` of `K` with at least two colours present, so `F` is a
fourth perfect matching; conversely a perfect matching `F ∉ {M_0, M_1, M_2}`
has at least two nonempty classes `A_c = V(F ∩ M_c)`, each an `M_c`-union.
For the last sentence, in a uniform model (S) and (F) force
`S_c = {G_c-unions}`, and (a) with (H2) forces the three matchings to be
pairwise disjoint (a common edge `e` of `G_c` and `G_d` gives the two-part
partition `(e, V − e)` with `V − e` a `G_d`-union).  ∎

Hence the sub-lemma at order `n` implies that every such `K` on `n` vertices
has a perfect matching other than its three colour classes, which is the
Chandran–Gajjala–Illickan theorem (MFCS 2024, Theorem 1.7) that WB1 and WB4
already import; conversely that theorem proves the uniform case (WB4
Theorem 3, Steps 3–4).  **Any hand proof of the sub-lemma must therefore
contain a proof of that theorem or import it.**

**Corollary 3'.**  The uniform case of the sub-lemma follows from Lemma 2
alone when `n ≡ 2 (mod 4)`.

*Proof.*  In a uniform model the Laplace partner of every vertex is forced
(`G_1 = M_1`), so the cycle of Lemma 2 for colour 1 is
`C_1 = M_0 ∪ M_1` whatever the widow order, and by choosing the order every
`M_1`-ended arc `B` of `C_1` containing the top edge `ab` occurs as some
`B_j`.  Every `M_1`-edge is top-active, so every proper `M_1`-ended arc
occurs, and by Lemma 2(3) no `M_2`-edge joins the two ends of a proper
`M_1`-ended arc.  Two vertices at odd distance on the even cycle `C_1` are
the ends of exactly one `M_1`-ended arc between them, which is proper unless
they are `M_0`-partners.  So every `M_2`-edge joins vertices at even distance
on `C_1`, i.e. lies inside one of the two colour classes of the bipartite
cycle `C_1`.  Each class has `n/2` vertices, which is odd, so `M_2` cannot be
a perfect matching inside the classes.  ∎

For `n ≡ 0 (mod 4)` the remaining uniform configurations (every `M_2`-chord
of `C_1` at even distance, and symmetrically) are exactly the hard core of the
CGI theorem, which this document does not reprove.

## 4. Theorem 4 (locality obstruction)

Let `Σ_loc(n)` be the following system on `n` vertices:

- colour 0: `G_0 = M_0` is a perfect matching, with all of (a), (L), (S), (F);
- colours 1 and 2: (a) and (S) in full; (L) only for sets `A` with
  `|A| >= n − 2` or `|A| <= 4`; (F) only for sets with `|A| <= 4` or
  `|A| >= n − 4`;
- (H2) in full, and the top-matching hypothesis (every `E_c` a perfect
  matching).

The solver runs of Section 6 show that the weaker system with (L) only at
`|A| >= n − 2` and (F) only at `|A| <= 4` (and no top-matching hypothesis) is
already unsatisfiable at `n = 8` and `n = 10`.

**Theorem 4.**  Let `K` be a simple cubic graph on `n` vertices whose edge set
is the disjoint union of perfect matchings `M_0, N_1, N_2` and whose girth is
at least 10.  Put `m = n/2`, `G_0 = M_0`, `S_0 = {M_0-unions}`, and for
`c = 1, 2`, `G_c = N_c` and

```text
S_c = { unions of k edges of N_c : k ∈ {0, 1, 2, m−2, m−1, m} }.
```

Then `(G_c, S_c)` satisfies `Σ_loc(n)`, every colour has `G_c` equal to its
top-active perfect matching, and in particular the sub-lemma's conclusion
fails for all three colours.  Such graphs exist at `n = 160` and `n = 162`
(explicit, checked by the companion verifier), hence, by disjoint unions, at
every even `n >= 12640`.

*Proof.*  (a), (S), and the top-matching hypothesis are immediate
(`E_c = N_c` because `V − e ∈ S_c` exactly for `e ∈ N_c`).  (L) at a union of
`k` edges with `k ∈ {1, 2, m−1, m}` holds because its children are the unions
of `k − 1` edges, which lie in `S_c`.  (F) at a set of size at most 4 or at
least `n − 4`: in `G_c = N_c` a set with a perfect matching is an `N_c`-union,
of `k <= 2` or `k >= m − 2` edges, so it lies in `S_c`.  Colour 0 satisfies
every axiom as a family of unions.

(H2): a violating partition `(A_0, A_1, A_2)` gives the perfect matching
`F = M_0|A_0 ∪ N_1|A_1 ∪ N_2|A_2` of `K` with `a_c = |F ∩ X_c|`
(`X_0 = M_0`, `X_c = N_c`) satisfying `a_1, a_2 ∈ {0, 1, 2, m−2, m−1, m}` and
`F ∉ {M_0, N_1, N_2}` (two classes are nonempty).  For each `X ∈ {M_0, N_1,
N_2}`, `F Δ X` is a nonempty disjoint union of cycles of `K`, each of length
at least 10, with half of its edges in `F − X`; hence `|F − X| >= 5`, that is,
`a_X <= m − 5`.  Then `a_1, a_2 <= 2`, and `a_0 = m − a_1 − a_2 >= m − 4`,
contradicting `a_0 <= m − 5`.

Existence: the verifier rebuilds two bipartite cubic graphs on `2·80` and
`2·81` vertices, with colour classes `{A_i B_i}`, `{A_i B_{p1(i)}}`,
`{A_i B_{p2(i)}}` from embedded permutations, and checks that each class is a
perfect matching, that the classes are disjoint, and that the girth is
exactly 10.  A disjoint union of such graphs again satisfies the hypotheses,
and since `gcd(80, 81) = 1` every integer `m >= 80·81 − 80 − 81 + 1 = 6320`
is a nonnegative combination of 80 and 81.  ∎

**What the obstruction rules out.**  Any argument for the sub-lemma (or for
(PM)) that uses Laplace accessibility only at `V` and its children, forcing
only for sets of size at most four (or at least `n − 4`), and (H2), cannot
work at all orders: the solver refutations of that system at `n <= 10` rest
on the small order, where every cubic graph has short cycles.  A proof must
use Laplace steps at unbounded depth (as the widow chains of Lemma 2 do) or
forcing for sets of size between 6 and `n − 6`, and by Proposition 3 it must
carry the CGI theorem in the uniform case.  The obstruction does not address
arguments that use full-depth chains: the uniform model on `K` violates (L)
at every union of `m − 2` edges, and under full (L) the families become all
unions, where Proposition 3 applies.

## 5. Lemma 5 (the arc lemma would close `n ≡ 2 (mod 4)`)

For a perfect matching `N ⊆ G_1` with `C = M_0 ∪ N` a Hamiltonian cycle, an
**`N`-ended arc** of `C` is the vertex set of a subpath of `C` whose first and
last edges are in `N`.

> **Arc lemma (open).**  In an AP' model with `G_0 = M_0` there is a perfect
> matching `N ⊆ G_1` such that `M_0 ∪ N` is a Hamiltonian cycle and every
> `N`-ended arc of it lies in `S_1`.

In a uniform model the arc lemma holds (every arc is an `M_1`-union).  Lemma 2
supplies the Hamiltonian cycle and the arcs that avoid the top edge `ab` of
*one* chain; what is missing is the arcs of other chains when partners depend
on the history, and the arcs through `ab`.

**Lemma 5.**  If the arc lemma holds for a model with `G_0 = M_0` and
`n ≡ 2 (mod 4)`, the model violates (H2).  So the arc lemma at such `n`
implies (PM), and hence the sub-lemma, at that order.

*Proof.*  `G_2` has a perfect matching `N_2` (by (S) at `V`).  The cycle
`C = M_0 ∪ N` is bipartite with classes of odd size `n/2`, so some edge
`xy ∈ N_2` joins the two classes, i.e. `x, y` are at odd distance on `C`, and
`xy ∉ M_0` by Proposition 1(ii).  `C − {x, y}` is a union of at most two paths
with an even number of vertices each.  The path `Q` that contains `x'` (the
`M_0`-partner of `x`) starts at `x'` with an `N`-edge, has an odd number of
edges, hence ends with an `N`-edge at a vertex whose next cycle edge is an
`M_0`-edge to `y`; so `Q` runs from `x'` to `y'` and `V(Q)` is an `N`-ended
arc.  The other path `Q'` (empty when `xy ∈ N`) runs from the `N`-neighbour of
`x` to that of `y`, starts and ends with `M_0`-edges, and `V(Q')` is an
`M_0`-union.  The partition `U = V(Q')`, `A_1 = V(Q)`, `A_2 = {x, y}` has
`A_1 ∈ S_1` by the arc lemma, `A_2 ∈ S_2` by (a), at least two nonempty
classes, and `U` an `M_0`-union, contradicting (R).  ∎

For `n ≡ 0 (mod 4)` the arc lemma for one colour leaves exactly the
configuration in which every `G_2`-edge stays inside a class of `C`, the
non-uniform analogue of the CGI hard core.

## 6. Computations (exploratory; not proof)

All runs: CaDiCaL 1.5.3 through `python-sat`, single thread, Windows host,
no symmetry breaking beyond fixing `M_0 = {01, 23, ...}` (sound by
relabelling); wall-clock seconds include encoding.  Script:
`explore_all_diagonal_support_level_ap_prime_matching_colour_relaxations.py`,
which reuses the WB4 encoder.  Relaxation specs are per colour:
`fmax=k` keeps (F) only for `|A| <= k`; `lmin=k` keeps (L) only for
`|A| >= k`.  Every UNSAT entry is evidence at one order only, with no proof
trace, and is vacuous as a statement about AP' models at these orders (AP' has
none); it measures which axioms the refutation needs.

| n | instance (all with `G_0 = M_0`) | result | s |
|---|---|---|---|
| 6 | full AP' (no top-matching) | UNSAT | 0.0 |
| 8 | full AP' (no top-matching) | UNSAT | 0.1 |
| 10 | full AP' (no top-matching) | UNSAT | 11.1 |
| 10 | full AP' + top-matching | UNSAT | 11.1 |
| 8 | (F) off in colours 1, 2 | SAT | 0.1 |
| 8 | (F) only for `|A| <= 4` in colours 1, 2 | UNSAT | 0.1 |
| 8 | colour 1 without (F), colour 2 (F) for `|A| <= 4` | SAT | 0.1 |
| 8 | both colours `fmax=4, lmin=6` | UNSAT | 0.1 |
| 8 | both colours `fmax=4, lmin=8` (L only at `V`) | SAT | 0.1 |
| 8 | (H2) only for partitions with `min(|A_1|,|A_2|) <= 2` | SAT | 0.1 |
| 8 | (H2) only for partitions with `min(|A_1|,|A_2|) <= 4` | UNSAT | 0.1 |
| 10 | both colours `fmax=4, lmin=8` | UNSAT | 27.1 |
| 10 | both colours `fmax=4, lmin=8`, + top-matching | UNSAT | 28.8 |
| 10 | colour 1 `fmax=4, lmin=10`, colour 2 `fmax=4, lmin=8` | SAT | 0.6 |

Reading.  (1) The top-matching hypothesis is not what makes the WB4
Section 8.2 refutation of `G_0 = M_0` fast: (PM) is refuted as quickly.  (2) At
`n <= 10` forcing on four-sets in both colours and Laplace steps at `V` and its
children in both colours suffice; dropping either side's forcing or second
level makes the relaxation satisfiable.  (3) Theorem 4 shows this local
pattern cannot persist: the same system has models once a girth-10
three-edge-coloured cubic graph fits.  A scratch computation (not reproduced
by the committed script) found a minimal unsatisfiable subset of 103 rainbow,
forcing and Laplace clause groups for the `n = 8` local instance with one
top edge fixed, so even the small-order local refutation is not short.

## Boundary

- The target sub-lemma, (PM), the arc lemma, and the top-matching lemma are
  **open** at every order `n >= 12`; at `n <= 10` they hold only because AP'
  has no model there.
- Lemma 2, Propositions 1 and 3, Corollary 3', Theorem 4 and Lemma 5 are
  proved at every even order stated.  Theorem 4 is an obstruction to a proof
  *method*; it is not a model of AP' and not evidence against the sub-lemma.
  Its models violate (L) at the unions of `m − 2` edges and (F) at sizes
  between 6 and `n − 6`.
- Proposition 3 and Corollary 3' concern uniform models only; the CGI theorem
  is the same external import as WB1 and WB4 (no new import is used here, and
  this document does not reprove it).
- The computations of Section 6 are exploratory and carry no proof traces.
- No independent audit of this document exists.

## Verification

```text
python claims/arbitrary-order/verify_all_diagonal_support_level_ap_prime_extra_edge_locality_obstruction.py
```

Expected: `"result": "PASS"` in under a second.  It rebuilds the two explicit
graphs (`n = 160, 162`), checks exactly that the colour classes are disjoint
perfect matchings and that the girth is 10, and cross-checks the counting
argument of Theorem 4 by a SAT search for a relaxed rainbow partition (UNSAT
for both graphs; SAT for the controls `K_{3,3}` and the cube `Q_3`, which have
girth 4).  The SAT cross-check is a second route, not the proof; the proof of
Theorem 4 is the counting argument, which needs only the exact girth check.

Section 6 rows:

```text
python claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_matching_colour_relaxations.py 8 --relax1 fmax=4,lmin=6 --relax2 fmax=4,lmin=6
python claims/arbitrary-order/explore_all_diagonal_support_level_ap_prime_matching_colour_relaxations.py 10 --relax1 fmax=4,lmin=8 --relax2 fmax=4,lmin=8
```

and the other rows with the flags shown in the table (`--top` adds the
top-matching hypothesis; `--filter onesmall|onesmall4` restricts (H2)).  The
`n = 10` rows take under a minute each; run them under
`tools/research/run_bounded.py`.
