# GHZ closure face criterion: three-edge-cut form, an external formalization, and a refuted WP1 route

Date: 2026-10-07.

## Status

This note is a companion to the
[GHZ closure theorem](GHZ_CLOSURE_MATCHING_POLYTOPE_FACE_ASYMPTOTIC_REALIZABILITY_THEOREM.md).
It changes no statement of that theorem and no other claim.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

It records three separate things, with separate evidence:

1. **Proposition E** (Section 1): an exact combinatorial form of the face
   hypothesis of Theorem A in terms of three-edge cuts.  The sufficiency
   directions are proved here from first principles.  The necessity
   directions import Edmonds' matching-polytope theorem.  Written proof; no
   independent review; no formalization.
2. **An external Lean development** (Section 2) that states the graph-theoretic
   content of Theorem B.  Its statements were read at a pinned commit.  It
   was **not built or kernel-checked here**, and its publisher lists its
   review status as unchecked.  Nothing in this repository depends on it.
3. **A mechanism refutation** (Section 3): the minimal face of the all-`1/3`
   point gives no information about the extra matchings of the WP1 cubic
   graph on the two fixtures of the protected pair-gadget bridge.  Exact
   finite computation on two instances; not a branch exclusion.

## 1. The three-edge-cut form of the face hypothesis

### Setting

Let `G` be a simple cubic graph on `2m >= 4` vertices with a proper
three-edge-colouring.  Its colour classes `M_0, M_1, M_2` are perfect
matchings and partition `E(G)`, and `|E(G)| = 3m`.  Write `P(G)` for the
perfect-matching polytope in `R^(E(G))`, `x` for the all-`1/3` point (the
barycentre of the three colour classes), and `chi_N` for the incidence
vector of an edge set `N`.

A **three-edge cut** is a set `delta(U)` of exactly three edges, where `U` is
a vertex set and `delta(U)` is the set of edges with exactly one end in `U`.
The vertex stars are three-edge cuts; a three-edge cut is **nontrivial** when,
as an edge set, it is not a vertex star (for connected `G` this means
`1 < |U| < 2m - 1`; for disconnected `G` the same edge set may be `delta(U)`
for several `U`, and it is the edge set that matters).  Let

```text
C     = the set of all three-edge cuts of G,
C*    = the set of nontrivial ones,          K = |C*|,
k(e)  = the number of members of C* containing the edge e,
r     = the rank of the vectors chi_D, D in C,
F     = { perfect matchings N of G : |N cap D| = 1 for every D in C }.
```

Vertex stars impose nothing on a perfect matching, so `F` is equally the set
of perfect matchings crossing every member of `C*` exactly once.

### Statement

**Proposition E.**  In the setting above:

1. Every `D = delta(U)` in `C` has `|U|` odd.  Every perfect matching meets
   `D` in one or three edges, and each colour class meets it in exactly one.
2. `r <= 3m - 2`.
3. The integer edge function `nu(e) = m k(e) - K` satisfies

   ```text
   nu(N) = m * sum_(D in C*) (|N cap D| - 1)    for every perfect matching N,
   ```

   so `nu(N) = 0` for `N in F` and `nu(N) >= 2m` for every other perfect
   matching.  Consequently `conv{chi_N : N in F}` is a face of `P(G)` that
   contains `x` and has vertex set `F`.
4. The following are equivalent.

   ```text
   (i)    {M_0, M_1, M_2} is the vertex set of a face of P(G)
          (equivalently, condition (3) of Theorem A holds for some nu);
   (ii)   F = {M_0, M_1, M_2};
   (iii)  the minimal face F_x of P(G) containing x has dimension two;
   (iv)   r = 3m - 2.
   ```

   When they hold, `nu(e) = m k(e) - K` is an explicit potential for
   Theorem A, and `F_x` is the triangle on the three colour classes.
5. When the conditions of item 4 hold, the uniform law on
   `{M_0, M_1, M_2}` is the only probability law on the perfect matchings of
   `G` whose edge marginals are all `1/3`.
6. If `C*` is empty, then `F` is the set of all perfect matchings of `G`,
   and the conditions of item 4 hold if and only if `G` has exactly three
   perfect matchings.  In particular a graph `G` to which Theorem A applies
   and which has a fourth perfect matching has a nontrivial three-edge cut.

Evidence boundary inside the proposition: items 1, 2, 3, 5, and the
implications `(iv) => (ii) => (i)` and `(ii) => (iii)` of item 4 are proved
below without any imported result.  The implications `(i) => (ii)`,
`(iii) => (ii)` and `(ii) => (iv)`, and item 6, use Edmonds' theorem.

### Proof

*Item 1.*  Summing degrees over `U` gives `3|U| = 2 e(U) + |delta(U)|`, where
`e(U)` counts edges inside `U`.  So `|delta(U)|` and `|U|` have the same
parity, and `|delta(U)| = 3` forces `|U|` odd.  A perfect matching `N` covers
the odd set `U`, so `|N cap delta(U)|` is odd, hence one or three.  The three
colour classes partition the three edges of `delta(U)` and each takes at
least one, so each takes exactly one.

*Item 2.*  By item 1 the three vectors `chi_(M_c)` lie in the affine space
`L = { y : y(D) = 1 for every D in C }`, whose dimension is `3m - r`.  They
are affinely independent, because they are nonzero with disjoint supports.
Hence `3m - r >= 2`.

*Item 3.*  A perfect matching has `m` edges, so

```text
nu(N) = m * sum_(e in N) k(e) - m K = m * sum_(D in C*) |N cap D| - m K
      = m * sum_(D in C*) (|N cap D| - 1).
```

By item 1 every summand is `0` or `2`, and all vanish exactly when `N in F`.
The linear functional `y -> sum_e nu(e) y_e` is therefore nonnegative on the
vertices of `P(G)` and vanishes exactly on `F`; its zero set on `P(G)` is a
face with vertex set `F`.  It contains each `chi_(M_c)` by item 1, hence `x`.

*Item 4, the implications that need no import.*

`(ii) => (i)`: item 3 with `F = {M_0, M_1, M_2}`.  The potential `nu` is the
one required by condition (3) of Theorem A, with gap `2m >= 1`.

`(ii) => (iii)`: under (ii) the face of item 3 is the triangle on the three
colour classes, and `x` is its barycentre, a relative interior point.  A face
containing a relative interior point of another face contains that face, so
the triangle is the minimal face `F_x`, of dimension two.

`(iv) => (ii)`: if `r = 3m - 2` then `L` has dimension two and is the affine
hull of the three colour classes.  Let `N in F`.  Then `chi_N in L`, so
`chi_N = sum_c lambda_c chi_(M_c)` with `sum_c lambda_c = 1`.  Since the
classes partition `E(G)`, the coordinate of the right side on an edge of
`M_c` is `lambda_c`, so each `lambda_c` is `0` or `1`, exactly one is `1`,
and `N` is a colour class.

*Edmonds' theorem and the tight system at `x`.*  Edmonds proved that the
matching polytope of a graph is the solution set of nonnegativity, the star
inequalities `y(delta(v)) <= 1`, and `y(E(S)) <= (|S|-1)/2` for every odd
vertex set `S` with `|S| >= 3`, where `E(S)` is the set of edges inside `S`.
`P(G)` is the face of that polytope on which every star inequality is tight.
On that face, summing the star equations over `S` gives
`|S| = 2 y(E(S)) + y(delta(S))`, so the odd-set inequality is equivalent to
`y(delta(S)) >= 1`.  Therefore

```text
P(G) = { y >= 0 : y(delta(v)) = 1 for all v, y(delta(S)) >= 1 for all odd S }.   (E1)
```

At `x` no nonnegativity constraint is tight, and `x(delta(S)) = |delta(S)|/3`
equals `1` exactly when `delta(S)` is a three-edge cut.  By item 1 every
three-edge cut arises from an odd set.  So the constraints of (E1) tight at
`x` are exactly the equations `y(D) = 1`, `D in C`.  The minimal face of a
polyhedron at a point is cut out by the constraints tight at that point, and
its affine hull is the solution set of those tight equations, because the
point satisfies every other inequality strictly.  Hence

```text
F_x = { y in P(G) : y(D) = 1 for every D in C },    vertex set F,
dim F_x = dim L = 3m - r.                                                        (E2)
```

*Item 4, the implications that use (E2).*

`(i) => (ii)`: if the colour classes are the vertex set of a face, `x` is a
relative interior point of it, so that face is `F_x`, and its vertex set is
`F` by (E2).

`(iii) => (ii)`: by (E2), `dim L = 2`, which is `(iv)`, and `(iv) => (ii)`.

`(ii) => (iv)`: by `(ii) => (iii)` and (E2), `3m - r = 2`.

*Item 5.*  Let `p` be a probability law on perfect matchings with all edge
marginals `1/3`, so `x = sum_N p(N) chi_N`.  The face of item 3 contains `x`,
so it contains `chi_N` whenever `p(N) > 0`; under (ii) such `N` is a colour
class.  The marginal of an edge of `M_c` is then `p(M_c)`, so `p(M_c) = 1/3`.

*Item 6.*  If `C*` is empty, the defining condition of `F` is vacuous.  The
rest is the equivalence `(i) <=> (ii)`.

### Relation to Theorem B and to a published rank bound

The truncation step of Theorem B produces the nontrivial three-edge cut
around the new triangle, and a perfect matching of the truncated graph uses
one or three attachment edges according as it crosses that cut once or three
times.  Proposition E therefore explains the family of Theorem B: a perfect
matching outside the three colour classes crosses some three-edge cut three
times (item 4), and on the canonical family the verifier finds that these
cuts are the truncation cuts for `n <= 16`; the cut-counting potential
`m k(e) - K` is an alternative to the recursive potential of Theorem B.  For the canonical family the verifier
below finds `K = m - 2` nontrivial three-edge cuts and `r = 3m - 2` for
`n = 2m = 4, ..., 16`.

Item 6 shows that the limiting families of Theorem A are confined to cubic
graphs with nontrivial three-edge cuts once a fourth perfect matching is
present.  The closure theorem's Consequence 2 states that a fourth perfect
matching always exists for `n >= 6`; that statement is used here as recorded
there and is not re-proved.

The inequality `r <= 3m - 2` of item 2 is, through (E2) and hence through
Edmonds' theorem, the special case at the all-`1/3` point of a
three-edge-coloured cubic graph of the bound
`|supp y| - dim F_y <= 3m - 2` stated for every point `y` of the
perfect-matching polytope of a loopless multigraph on `2m` vertices in an
OpenAI preprint (Section 2 below).  Item 4 then reads: **Theorem A applies to
`G` exactly when `G` attains equality in that bound at the all-`1/3` point.**
This repository uses only the special case proved in item 2; the general
bound is claimed by its authors and is not imported.

## 2. An external formalization of the graph-theoretic content of Theorem B

Source: the public repository `openai/math` at commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a` (Apache-2.0), namely the preprint
*Entropy and Face Dimension of the Perfect-Matching Polytope* (OpenAI,
2026-09-23) and the Lean files under
`lean/OAI/Combinatorics/MatchingEntropy/`.

Evidence labels, kept separate:

| Label | What it covers here |
|---|---|
| claimed by OpenAI | every theorem of the preprint and every Lean declaration named below |
| statement read here | the declarations and passages listed below, at the pinned commit |
| certificate replayed here | none |
| built and axiom-checked here (2026-10-08) | `OAI.Combinatorics.MatchingEntropy.KleeSharpness` built with Lean 4.34.1 at the pinned commit; `#print axioms` reports only `propext`, `Classical.choice`, `Quot.sound` for `klee_minimal`, `klee_dimension`, `klee_unique_law`, `klee_sharp_face`; the Comparator challenge `TriangleFace` passed a CompareLite comparison (statement identical, 33 challenge-local and 126 library dependencies checked, same three axioms) |
| kernel-checked here | **none**: no `leanchecker` replay of these modules has completed; a replay of the openai/math family-003 modules was still running when this line was written |

The publisher's own catalogue `lean/formalization.yaml` records
`review: status: unchecked`.  The fetched source text of the three Lean files
named below contains no `sorry`, `axiom` or `native_decide` token; that is a
text search of those files only, not of their import closure.  The build and
axiom report above cover the import closure of `KleeSharpness` as compiled;
they are not a kernel replay.

What was read:

- `TriangleExpansion.lean`: `kleeGraph 0` is two vertices joined by three
  labelled parallel edges; `kleeGraph (n+1)` is `triangleExpansion` of
  `kleeGraph n` at the vertex `kleeRoot n`; `kleeUniform n` is the constant
  `1/3`; `kleeTriangle n` is the convex hull of the three colour-class
  indicator vectors.  In `triangleExpansion` an old edge of colour `c` at the
  expanded vertex is reattached to tip `c`, and new edge `i` joins tips `i+1`
  and `i+2` and receives colour `i`.  This is the truncation of Theorem B:
  the triangle edge opposite tip `c` has colour `c`.
- `MinimalFace.lean`: `minimalFace G x` is *defined* as the set of points of
  the polytope that vanish where `x` vanishes and satisfy `cutMass y S = 1`
  for every odd `S` with `cutMass x S = 1`.  It is defined by the tight
  odd-cut system, not as the least face.
- `KleeSharpness.lean`: `klee_minimal` states
  `minimalFace (kleeGraph n) (kleeUniform n) = kleeTriangle n`;
  `klee_dimension` states that its `faceDimension` is two; `klee_unique_law`
  states that the feasible laws at `kleeUniform n` are the single law
  `kleeLaw n`; `klee_sharp_face` bundles these with the count
  `card (KleeE n) - faceDimension = 3 (n+1) - 2`.
- `TriangleExpansion.lean`, `expansion_face`: for a `CubicColoring` and any
  vertex `v`, the extension map identifies `minimalFace` of the expanded
  graph at the extended point with the image of `minimalFace` of the
  original graph.
- `lean/ComparatorChallenges/TriangleFace.lean`, `triangle_expansion_face`:
  the same preservation for a least-face definition (`minFace`, the
  intersection of all convex extreme subsets through the point) at any
  vertex of degree three of a graph with a perfect matching.  The challenge
  file states the theorem with a `sorry` body by design; its solution module
  `OAI.Combinatorics.TriangleFace.Main` was not read.
- `SharpRank.lean`, `sharp_face_rank`: `faceCodimension x + 2 <= 3 m` for a
  point of the polytope of a graph on `2m` vertices, `m > 0`.
- The preprint, Section 1.2, Proposition 2.4, Lemma 5.1 and Proposition 5.2:
  the bound `|supp x| - dim F_x <= 3m - 2`, the triangle-expansion face
  lemma, and the triangular minimal face with its unique law.

Correspondence with this repository, as read:

- `kleeGraph 1` is `K_4` and `kleeGraph (m-1)` has `2m` vertices.  The
  upstream family always expands the image of one fixed root vertex; the
  canonical family of Theorem B truncates the vertex of largest label.  The
  two families need not be isomorphic at a given order.  Theorem B's proof
  truncates an arbitrary vertex, and the upstream `expansion_face` is
  likewise stated at an arbitrary vertex, so the difference does not affect
  the existence statement; it does mean that `klee_minimal` is a statement
  about the upstream family, not about the canonical family checked by this
  repository's verifiers.
- If `klee_minimal` holds, then the three colour classes of `kleeGraph n`
  form a face.  This inference needs no further import: the upstream
  `minimalFace` is the intersection of the polytope with supporting
  hyperplanes of valid inequalities, hence a face, and a triangle that is a
  face has its three vertices as vertex set.  So `klee_minimal`, **if
  accepted**, gives the hypothesis of Theorem A at every even order
  `2(n+1) >= 4`, which is the graph-theoretic content of Theorem B.
- `klee_unique_law` is item 5 of Proposition E for the upstream family.
- Theorem A itself (the identity `T_(W(eps)) = Delta_n + eps R(eps)`), the
  closure statement (5), and Corollaries C and D have **no** upstream
  counterpart.  The formalization status of the closure theorem in this
  repository is unchanged: not formalized.

Prior art.  The preprint attributes the triangle-expansion construction and
the uniqueness of the three-matching partition of these graphs (Klee graphs)
to Cygan, Pilipczuk and Skrekovski (2013), and attributes cubic examples with
exactly three perfect matchings crossing every minimum odd cut once to Abdi,
Cornuejols, Dadush and Dalirrooyfard (2026).  Those two sources were **not
inspected here**; they are unverified leads taken from the preprint's
introduction and Section 5.  They concern the graph family, not the closure
of the hafnian image.  The closure theorem's bounded novelty assessment was
about closures and limiting families; this note does not extend it, and it
should not be read as claiming that the graph-theoretic input of Theorem B
is new.

## 3. Refuted route: the minimal face does not organize the WP1 extra matchings

**Route tested.**  "In the cubic graph `H` of the
[protected pair-gadget bridge](PROTECTED_PAIR_GADGET_CUBIC_MATCHING_EXCLUSION.md),
use the minimal face of the all-`1/3` point, or the rank and entropy bounds
attached to it, to force an extra perfect matching whose physical word is
component-constant or has `min_c q_c <= 1`."

**Finding.**  On the two fixtures of
`verify_protected_pair_gadget_cubic_bridge.py`, with the proper
three-edge-colouring of `H` carried by its edge data:

| Fixture | `\|V(H)\|` | `\|E(H)\|` | perfect matchings | nontrivial three-edge cuts | `dim aff(F)` | `dim P(H)` | extra matchings | extra matchings that are component-constant or have `min q <= 1` |
|---|---|---|---|---|---|---|---|---|
| two-`K_4` literal table | 20 | 30 | 30 | 0 | 10 | 10 | 27 | 24 |
| three-`K_4` triangle | 30 | 45 | 160 | 0 | 15 | 15 | 157 | 56 |

Neither `H` has a nontrivial three-edge cut.  So `F` is the set of all
perfect matchings; by (E2), which uses Edmonds' theorem, the minimal face of
the all-`1/3` point is the whole polytope `P(H)`; and the three colour
classes do not form a face (this last conclusion is also certified below
without Edmonds' theorem).  The
last conclusion also has a certificate that does not use Edmonds' theorem:
each `H` has a second proper three-edge-colouring, whose three classes
average to the same all-`1/3` point, which is impossible if the original
classes were the vertex set of a face.

**Scope.**  The face of the all-`1/3` point, and any rank, dimension or
entropy bound stated in terms of it, filters no perfect matching on these
instances, so it cannot distinguish the extra matchings in the WP1 target
class from the others.  Such tools supply matching counts and dimensions, not
a bound on the depth vector `q`.  This agrees with the frontier's existing
note that the imported matching-count theorem supplies no such metric
control.  It is a **mechanism refutation on two exact instances**: it is not
a statement about every complete protected-edge pairing, it does not show
that other polyhedral information is useless, and it neither proves nor
refutes WP1.  The target-class counts are properties of these two fixtures
only.

## Boundary

- Proposition E is about simple cubic graphs with a given proper
  three-edge-colouring.  It does not classify the graphs satisfying its
  equivalent conditions, and it says nothing about `Im(Phi_n)`.
- The necessity directions depend on Edmonds' theorem as cited; the
  derivation of (E1) from it is written above.
- No statement of the external Lean development is used as a premise here or
  anywhere in the repository.  Building it and obtaining an axiom report is
  an open evidence task, not a mathematical obligation of any live route.
- Section 3 is two finite instances.  WP1 remains open at general order.
- A same-day adversarial agent review of Proposition E and Section 3 found
  no gap: [review](../../docs/audits/GHZ_CLOSURE_FACE_THREE_EDGE_CUT_CRITERION_REVIEW_2026-10-08.md).
  It is not an external referee report.

## Verification

```text
python claims/arbitrary-order/verify_ghz_closure_three_edge_cut_face_criterion.py
```

The script uses exact integer and rational arithmetic.  It rebuilds the
canonical truncation family for `n = 4, ..., 16` from the closure theorem's
primary verifier, enumerates all three-edge cuts and perfect matchings, and
checks items 1 to 4 of Proposition E on each member, including
`dim aff(F) = 3m - r`, `r = 3m - 2`, and the gap `2m` of the cut-counting
potential.  It checks the same identities on `K_(3,3)` and the cube as
negative controls (no nontrivial three-edge cut, more than three perfect
matchings, a second three-edge-colouring).  It then rebuilds the two WP1
fixtures through `build_h`, `h_pm_to_word` and `q_vector` of the bridge
verifier and reproduces the table of Section 3.  It replays the displayed
finite instances only; the written argument is the proof of Proposition E.
There is no independent audit script.
