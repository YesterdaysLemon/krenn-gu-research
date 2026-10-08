# Adversarial review: three-edge-cut form of the GHZ closure face criterion (Proposition E)

Date: 2026-10-08

Reviewed package (not edited by this review):

- `claims/arbitrary-order/GHZ_CLOSURE_FACE_THREE_EDGE_CUT_CRITERION_AND_UPSTREAM_CROSSCHECK.md`,
  Section 1 (Proposition E) and Section 3, at branch
  `claude/openai-math-face-crosscheck-20261007`, commit `a46423f3`
- `claims/arbitrary-order/verify_ghz_closure_three_edge_cut_face_criterion.py`

Section 2 of the note (the external Lean development) is out of scope and was
not examined.

## Independence disclosure

This is a same-day agent review: it was written on 2026-10-08, one day after
the note (dated 2026-10-07), by a Claude agent in a separate session that did
not write the note.  I do not know whether the note's author is the same model
family, so it should not be counted as an independent audit in the sense of
`AGENTS.md` section 5, and no human mathematician has read the proof.  The
supplementary computations below were written for this review and differ in
route from the primary verifier (linear-programming tests over enumerated
perfect matchings, random graphs, no use of the primary verifier's cut
enumerator), but they are floating-point LP checks on finite instances, they
are a test and not a proof, and the scripts were not committed.  The global
Krenn--Gu conjecture remains **UNRESOLVED**; nothing here changes any status.

## Verdict

**PASS.**  I found no mathematical gap in Proposition E items 1 to 6, in the
derivation (E1)/(E2) from Edmonds' theorem, in the equivalence
(i) <=> (ii) <=> (iii) <=> (iv), or in the Edmonds-free non-face certificate
of Section 3.  The evidence boundary the note declares (elementary:
items 1, 2, 3, 5 and (iv) => (ii) => (i), (ii) => (iii); Edmonds-dependent:
(i) => (ii), (iii) => (ii), (ii) => (iv) and item 6) matches what I found when
I traced each step.  There are four small presentational or scope points,
listed in "Findings", none of which invalidates a stated claim.

## Verdicts by attack

### (a) Item 1: parity and the single crossing of each colour class — PASS

`3|U| = 2e(U) + |delta(U)|` gives `|delta(U)| = |U| (mod 2)`, so a three-edge
cut has an odd shore.  A perfect matching `N` satisfies
`|U| = 2|N cap E(U)| + |N cap delta(U)|`, so `|N cap delta(U)|` is odd, hence 1
or 3.  The three colour classes partition `E(G)` (proper colouring of a cubic
graph, each vertex sees all three colours), hence partition the three edges of
`delta(U)`; each class is a perfect matching and so takes an odd, hence
positive, number of them; three positive odd numbers summing to 3 are all 1.
Each step is correct and uses only the stated hypotheses.  The verifier
asserts both statements on every nontrivial cut of every instance
(stars are trivially crossed once by any perfect matching).

### (b) Item 2: affine independence and `dim L = 3m - r` — PASS

`L = { y : y(D) = 1 for all D in C }` with `C` including the vertex stars is
the right affine space: the stars are exactly the equations
`y(delta(v)) = 1` that define the perfect-matching face of the matching
polytope, so omitting them would change both `L` and the identification with
the minimal face.  `L` is nonempty (it contains `x`), so the solution space
of the consistent system has dimension `3m - rank = 3m - r`.  The three
colour-class indicator vectors lie in `L` by item 1, are nonzero with disjoint
supports, hence linearly and so affinely independent; `3m - r >= 2`.  Correct.
The verifier confirms `r <= 3m - 2` on all 13 instances.

### (c) Item 3: potential `nu(e) = m k(e) - K` — PASS (algebra verified)

For a perfect matching `N` (`|N| = m`):
`nu(N) = m sum_{e in N} k(e) - m K`, and
`sum_{e in N} k(e) = sum_{D in C*} |N cap D|` by exchanging the order of
summation, while `K = sum_{D in C*} 1`.  So
`nu(N) = m sum_{D in C*} (|N cap D| - 1)`.  By item 1 each summand is 0 or 2,
all vanish iff `N in F`, and otherwise `nu(N) >= 2m`.  The identity holds for
any finite family of cuts, so it does not depend on `C*` being exhaustive; the
exhaustiveness of `C*` matters only for identifying the zero set with `F`
(for which stars contribute 0 anyway).  The zero set of a functional that is
nonnegative on the vertices of `P(G)` is a face whose vertices are the vertices
where it vanishes; `x` lies in it because the colour classes lie in `F`.  The
verifier checks `nu = 0` on the colour classes and `min nu >= 2m` on extra
matchings; the minimum is exactly `2m` (6, 8, 10, 12, 14, 16 for
`n = 6, ..., 16`), so the stated gap is sharp on the canonical family.

### (d) Derivation of (E1) and (E2) from Edmonds' theorem — PASS

- (E1).  The perfect-matching polytope is the face of Edmonds' matching
  polytope on which all star inequalities are equalities (the face of a
  polytope cut out by making a set of valid inequalities tight; its vertices
  are the matching-polytope vertices with every star tight, i.e. the perfect
  matchings).  On that face `sum_{v in S} y(delta(v)) = |S|` gives
  `|S| = 2 y(E(S)) + y(delta(S))`, so `y(E(S)) <= (|S|-1)/2` is equivalent to
  `y(delta(S)) >= 1`.  Correct.
- "No nonnegativity constraint is tight at `x`": `x_e = 1/3 > 0`.  Justified.
- Tight odd-set constraints at `x`: `x(delta(S)) = |delta(S)|/3`.  This is at
  least 1 for every odd `S` because `x` is a convex combination of perfect
  matchings, each of which meets the odd set's cut; it equals 1 iff
  `|delta(S)| = 3`.  So the tight odd-set constraints are exactly the
  equations `y(D) = 1` for the three-edge cuts `D` with shore of size at least
  3 (and, by complementation, at most `2m - 3`).
- "Every three-edge cut comes from an odd set": by item 1 each
  `D = delta(U)` has `|U|` odd, and `2m - |U|` is then odd as well; if
  `|U| = 1` (or `2m-1`) it is a star equation, already among the equalities;
  otherwise it is an Edmonds odd-set constraint.  Justified.  The note's
  phrase "arises from an odd set" is correct but compressed; the star case is
  the reason stars must be in `C`.
- (E2).  The minimal face of a polyhedron containing a point is obtained by
  setting to equality exactly the constraints tight at the point, for any
  finite inequality description (a face containing the point is a nonnegative
  combination of constraints, all of which must be tight at the point).
  Since `x` satisfies every other inequality strictly, a neighbourhood of `x`
  in the affine solution set of the tight equations lies in the polytope, so
  the affine hull of `F_x` is the whole solution set `L`.  Hence
  `dim F_x = 3m - r`, and the vertices of `F_x` are the perfect matchings
  satisfying all `y(D) = 1`, i.e. `F`.  Correct.

The cited statement of Edmonds' theorem (nonnegativity, star, and odd-set
inequalities `y(E(S)) <= r` for `|S| = 2r+1`, `r >= 1`, give exactly the
matching polytope) is the standard one.  `catalog/literature/sources.json`
records honestly that only the statement was read from a scanned page and the
proof was not.

### (e) `(iv) => (ii)` through the coordinates `lambda_c` — PASS

If `r = 3m - 2` then `dim L = 2` and `L` contains three affinely independent
points, so `L` is their affine hull.  For `N in F`, `chi_N in L` (because
`chi_N(D) = |N cap D| = 1`), so `chi_N = sum_c lambda_c chi_{M_c}` with
`sum lambda_c = 1`.  The classes partition `E(G)`, so the coordinate on an
edge of `M_c` is `lambda_c`; being a 0/1 coordinate it forces each
`lambda_c in {0,1}` with exactly one equal to 1, so `N` is a colour class.
Correct and elementary.

The remaining implications also check out.  `(ii) => (iii)`: `x` is the
barycentre of the triangle, a relative interior point; a face of `P(G)`
containing it meets the triangle in a face of the triangle containing a
relative interior point, hence contains the triangle, and the triangle is
itself a face containing `x`, so it is `F_x`.  `(i) => (ii)`: the same
argument shows the face of (i) equals `F_x`, whose vertex set is `F` by (E2).
`(iii) => (ii)`: `dim L = 2` by (E2) is (iv), then `(iv) => (ii)`.
`(ii) => (iv)`: `dim F_x = 2 = 3m - r` by `(ii) => (iii)` and (E2).  Item 5
needs only item 3 (every law with marginals `1/3` is supported on a face
containing `x`, hence on `F`).  Item 6 is correct as stated; its "fourth
perfect matching implies a nontrivial three-edge cut" uses `(i) => (ii)`,
which the evidence-boundary paragraph correctly lists as Edmonds-dependent.

### (f) Section 3: a second proper three-edge-colouring certifies "not a face" without Edmonds — PASS

If `{M_0, M_1, M_2}` were the vertex set of a face `Phi`, then `x`, the
barycentre, lies in `Phi`.  A second proper three-edge-colouring
`{M'_0, M'_1, M'_2}` has the same barycentre `x`, which is a convex
combination with positive weights of the vertices `chi_{M'_c}` of `P(H)`; a
face containing a point contains every vertex in any convex decomposition of
it, so every `M'_c` would be one of `M_0, M_1, M_2`.  The `M'_c` are
pairwise disjoint and cover `E(H)`, so they would be the same partition.  So
any second colouring that is a different partition (equivalently, one with a
class outside `{M_0, M_1, M_2}`) refutes the face property, using only the
definition of a face.  The verifier's search for the second colouring takes
two disjoint perfect matchings both outside the original classes whose
complement is a perfect matching, which does give a different partition.  It
finds one on K_{3,3}, the cube, and both WP1 fixtures.

The weaker supporting statement "the minimal face of `x` is all of `P(H)`"
does use (E2), hence Edmonds.  I confirmed it by a route that does not use
Edmonds (below), so this is a note on provenance, not a defect.

## Verifier

`python claims/arbitrary-order/verify_ghz_closure_three_edge_cut_face_criterion.py`
exits 0 and prints `VERIFIED` (about 9 s wall-clock here, not 5 s).  It does
check what the document says it checks:

- items 1 to 3 and the sharp gap `2m` on the canonical family `n = 4, ..., 16`,
  with `K = m - 2` nontrivial cuts and `r = 3m - 2`;
- `dim aff(F) = 3m - r` on every instance (a computational test of the
  dimension statement in (E2));
- the equivalence of `F = colour classes`, `r = 3m - 2` and `dim aff(F) = 2`
  on every instance;
- the table of Section 3 (`|V|, |E|`, 30 and 160 perfect matchings, no
  nontrivial cut, `dim aff F = dim P`, 27/24 and 157/56 extra-matching counts,
  the latter via the sibling bridge verifier's `build_h`, `h_pm_to_word`,
  `q_vector`, which I did not re-derive).

Points about its scope, none contradicting the note's own sentence "It replays
the displayed finite instances only; the written argument is the proof":

1. The output field `colour_classes_form_face` is computed as
   `set(F) == set(classes)`, i.e. condition (ii), not condition (i).  Condition
   (i) is nevertheless settled on every instance by an elementary certificate:
   the explicit potential with gap at least `2m` for the positive cases, and the
   second colouring for the negative ones.  The Edmonds-dependent direction
   (i) => (ii) is therefore never tested against a face-membership oracle.
2. All four negative instances (K_{3,3}, cube, two WP1 fixtures) have no
   nontrivial three-edge cut.  No instance combines a nontrivial cut with
   `F` strictly larger than the colour classes, so the interaction of the
   cut system with a failing face is untested by the repository's verifier.
3. Condition (iii) is tested only through `dim aff(F)`, using the note's own
   vertex-set claim for `F_x`; the minimal face of `x` is not computed
   independently.  Items 5 and 6 are not tested.
4. It is the primary verifier only; there is no independent audit script, as the
   note says.

## Supplementary independent test (this review)

To close points 1 to 3, I wrote a separate script (kept out of the repository)
with a different route: random simple cubic graphs from the pairing model on
`n = 6, 8, 10, 12, 14` vertices, up to two proper three-edge-colourings each,
all perfect matchings, all three-edge cuts by exhaustive shore enumeration, and
for each case

- condition (i) by an LP over edge weights `c` with `c(M_j) = 0` and
  `c(N) >= 1` for every other perfect matching `N`;
- the vertex set of the minimal face of `x` by, for each perfect matching `N`,
  an LP maximising `p_N` over probability laws with all edge marginals `1/3`
  (the minimal face's vertices are exactly the matchings that occur in some
  decomposition of `x`); its dimension is the rank of the differences;
- `r` by exact rank (sympy), `F` by direct enumeration.

Result (run through `tools/research/run_bounded.py`, 246 coloured graphs, all
connected, no mismatch): conditions (i), (ii), (iii), (iv) agree on every case;
the vertex set of the true minimal face equals `F`; `dim F_x = 3m - r`;
`r <= 3m - 2` always.  The cases split as 96 positive (all with nontrivial
cuts), 108 with nontrivial cuts and `F` strictly larger than the three classes
(the combination the primary verifier does not cover), and 42 with no
nontrivial cut and more than three perfect matchings.  A hand-built
disconnected check (`K_4 + K_4`, `K_4 + prism`) also agreed with Proposition E,
with the equivalence failing on both sides as expected.  I also re-ran the two
WP1 fixtures of Section 3 through the bridge verifier's `build_h` with the same
LP tests: for the 20-vertex and 30-vertex graphs the colour classes are not a
face and the minimal face of `x` has all 30 and 160 perfect matchings with
`dim F_x = dim P(H) = 10` and `15`.  These are floating-point LP outcomes on
finite instances; they test the statements and do not prove them.

## Findings (all minor; no claim is invalidated)

1. **Definition of `C*` for disconnected graphs.**  The note does not assume `G`
   connected.  "Nontrivial" is defined through the shore size
   (`1 < |U| < 2m - 1`), but for disconnected `G` the star `delta(v)` also equals
   `delta(U)` for `U` = `{v}` plus a whole component, which would count as
   nontrivial by the shore definition and as trivial by the edge-set definition.
   For connected `G`, `delta(U) = delta(U')` forces `U'` to be `U` or its
   complement, so counting cuts as edge sets (as the verifier does, giving
   `K = 1` for the prism) is unambiguous.  The proposition is true in both
   readings (the identity of item 3 holds for any finite family of cuts, and
   the rest does not use connectivity; I confirmed this on the two disconnected
   examples), but `K` is a priori ambiguous.  Suggested wording: define `C*` as
   the set of three-edge cuts, as edge sets, that are not vertex stars.
2. **"Special case of the OpenAI bound."**  The statement that item 2 is the
   special case `|supp y| - dim F_y <= 3m - 2` at `y = x` identifies
   `dim F_x` with `3m - r`, which is (E2) and hence needs Edmonds.  Item 2 as
   an inequality on `r` is elementary, as stated; only the packaging as
   a statement about the dimension of a minimal face imports Edmonds.  The
   note's boundary paragraph says this is a special case "proved in item 2", which
   is slightly stronger than what item 2 alone gives.
3. **Beyond the reviewed items: the Theorem B paragraph.**  "Its extra matchings
   are exactly the matchings that cross some truncation cut three times"
   needs every nontrivial three-edge cut of `G_n` to be a truncation cut.
   For `n <= 16` this follows from `K = m - 2`, the number of truncations, if
   the truncation cuts are distinct; for general `n` it is an induction that is
   not written in the note.  The set of extras is correctly characterised by
   Proposition E as the matchings crossing some nontrivial cut three times.
   Not a defect of Proposition E.
4. **Section 3 provenance.**  "The minimal face of `x` is the whole polytope"
   (hence "filters no perfect matching") uses (E2).  An Edmonds-free certificate
   would be an exact rational decomposition of `x` with all perfect matchings
   in the support.  Not needed for the note's conclusion that the colour
   classes are not a face, which has its own elementary certificate.

## Frontier consequence

None.  This review changes no mathematical claim, status, scope, or reduction
edge, so `docs/current-frontier.md` is unchanged.  Proposition E remains a
written proof with an Edmonds import for the necessity directions, a primary
verifier replaying finite instances, and this same-day agent review; it has no
formalization and no independent audit script.  Nothing in the review bears on
the global Krenn--Gu status, which remains **UNRESOLVED**.
