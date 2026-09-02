# AP-prime at maximum degree four: path-cycle reduction and common-perfect-matching exclusion

## Status

This document proves two exact, arbitrary-order statements about the
support abstraction (AP') of the all-diagonal Krenn–Gu branch:

1. if the union of its three support graphs has maximum degree at most four,
   then each support graph is a disjoint union of even paths and even cycles,
   with all cross-colour overlap confined to one residual partial matching;
2. two maximum-degree-two support graphs in an AP' model cannot share a
   perfect matching.

These are a **proved reduction** and a **proved obstruction** for every even
order at least six.  They do not prove that AP' is unsatisfiable at maximum
degree four.  The missing orientation/blocker implication is stated exactly
below.  They do not improve the already stronger weighted-witness exclusion
at maximum degree four from WB1, and they say nothing about bichromatic
blocks.  The global Krenn–Gu conjecture remains **UNRESOLVED**.

The proofs are human, exact, support-only arguments.  The primary verifier
and the independently represented audit are bounded corroborating checks,
not the proofs.

## Parent-theorem checkpoint

The parent attacked in this sprint was:

> **AP' has no model at every even order at least six.**

Its upstream supply is the exact bridge in
[WB2](ALL_DIAGONAL_SUPPORT_LEVEL_WEIGHTED_BOGDANOV_FINITE_EXCLUSION_THEOREM.md):
every all-diagonal witness gives an AP' model.  Its named downstream consumer
is the all-diagonal parent in
[the fibre-exact targets brief](../../docs/strategy/fibre-exact-targets-2026-09-01.md):
an all-order AP' exclusion would force every genuine witness to have a
bichromatic block.  That consumer remains thin, so this was a scoped branch
sprint, not a claim of global resolution-first closure.

The run synthesized the accessibility/exclusivity mechanism of WB1 with the
support-only forcing mechanism of WB2.  It tested that synthesis against the
finite AP' frontier, shared residual edges, pairwise matching collisions,
the need for all three colours, and fixed cycle-orientation failures.  The
result is the exact reduction and obstruction below, followed by one sharper
remaining lemma.  No third sibling refinement is proposed.

## 1. The support abstraction

Let \(V\) have even cardinality \(n\ge 6\).  For each colour
\(c\in\{0,1,2\}\), an AP' model has a graph \(G_c\) on \(V\) and a family
\(\mathcal S_c\) of even subsets satisfying:

- the empty set and \(V\) belong to \(\mathcal S_c\), and its two-element
  members are exactly the edges of \(G_c\);
- **(L)** if \(A\in\mathcal S_c\) and \(v\in A\), some edge \(vu\) of \(G_c[A]\)
  has \(A-\{v,u\}\in\mathcal S_c\);
- **(S)** every \(G_c[A]\), for \(A\in\mathcal S_c\), has a perfect matching;
- **(F)** if \(G_c[A]\) has exactly one perfect matching, then
  \(A\in\mathcal S_c\);
- **(H2)** no ordered partition \(V=A_0\sqcup A_1\sqcup A_2\) into even
  classes, at least two nonempty, has \(A_c\in\mathcal S_c\) for every colour.

Write \(D=G_0\cup G_1\cup G_2\) for the simple union graph.

## 2. The degree-four support reduction

For each colour define its **top-active graph**

\[
E_c=\{uv\in E(G_c):V-\{u,v\}\in\mathcal S_c\}.
\]

### Theorem 1

If an AP' model satisfies \(\Delta(D)\le 4\), then:

1. every \(E_c\) spans \(V\) and has minimum degree at least one;
2. the \(E_c\) are pairwise edge-disjoint, and no edge of \(E_c\) belongs to
   another support graph;
3. \(H=D-(E_0\cup E_1\cup E_2)\) is a partial matching and
   \(G_c\subseteq E_c\cup H\) for every colour;
4. every \(G_c\) has maximum degree at most two and is a disjoint union of
   even paths and even cycles;
5. the unique perfect-matching edge incident with each vertex in an even
   path component belongs to \(E_c\).  Thus path choices are fixed and
   private; only even-cycle orientations can collide through \(H\).

### Proof

Apply (L) to \(V\in\mathcal S_c\) at each vertex.  It supplies an incident
edge \(uv\in G_c\) whose complementary set is in \(\mathcal S_c\), so
\(\delta(E_c)\ge1\).

If \(uv\in E_c\), then both \(V-\{u,v\}\) and \(\{u,v\}\) lie in
\(\mathcal S_c\).  If the same edge belonged to \(G_d\), for \(d\ne c\),
then \(\{u,v\}\in\mathcal S_d\).  Assigning the complement to colour \(c\),
the pair to colour \(d\), and the empty set to the third colour contradicts
the two-part case of (H2).  This proves active-edge exclusivity.

At every vertex there is now at least one distinct incident edge from each of
\(E_0,E_1,E_2\).  Since \(\Delta(D)\le4\), at most one further edge is
incident there.  Hence the residual \(H\) has maximum degree at most one.
An edge of \(G_c\) cannot lie in \(E_d\) for \(d\ne c\), so it lies in
\(E_c\cup H\).  At a vertex of \(E_c\)-degree two there is no residual
incidence; at a vertex of \(E_c\)-degree one there is at most one.  Therefore
\(\Delta(G_c)\le2\).

By (S) applied to \(V\), each \(G_c\) has a perfect matching.  Its components
are consequently even paths or even cycles.  Finally, if \(uv\in E_c\), then
\(G_c[V-\{u,v\}]\) is matchable by (S).  In an even path component, deleting
the endpoints of an edge leaves a matchable remainder exactly when that edge
is in the path's unique perfect matching.  Since (L) supplies an incident
top-active edge at every path vertex, all of the unique path-matching edges
are top-active.  Active-edge exclusivity makes them private.  ∎

### Why this is not WB1

The reduction above uses only AP'.  WB1 goes further for actual weighted
witnesses: it uses numerical Laplace scores to collapse its active
components and a weight-level noncancellation lemma before applying
Bogdanov's matching theorem.  Those numerical data are absent from AP', and
the witness-to-AP' bridge is one-way.  Therefore WB1 does **not** by itself
prove AP' unsatisfiable under \(\Delta(D)\le4\).

## 3. Common-perfect-matching exclusion

### Theorem 2

In any AP' model, two support graphs of maximum degree at most two cannot
share a perfect matching.

In particular, under Theorem 1, the perfect-matching sets of \(G_c\) and
\(G_d\) are disjoint whenever \(c\ne d\).

### Proof

Suppose \(G_c\) and \(G_d\) share a perfect matching \(R\).  Contract the
edges of \(R\) to a set \(X\) of matching atoms.  Because each graph has
maximum degree at most two, every component is an \(R\)-alternating path or
an \(R\)-alternating cycle.

Let \(\mathcal C\) be the family of subsets of \(X\) arising from the cycle
components of \(G_c\), and define \(\mathcal D\) from \(G_d\).  Within each
family the blocks are pairwise disjoint, and every block has size at least
two.

We claim there is a nonempty proper subset \(Y\subset X\) such that

\[
C\nsubseteq Y\quad(C\in\mathcal C),
\qquad
Y\cap D\ne\varnothing\quad(D\in\mathcal D).
\]

Choose one representative from each \(D\)-block while giving every
\(C\)-block capacity \(|C|-1\); atoms outside all \(C\)-blocks have capacity
one.  For any subfamily \(\mathcal J\subseteq\mathcal D\), put
\(U=\bigcup\mathcal J\).  Since the \(D\)-blocks are disjoint and have size
at least two, \(|U|\ge2|\mathcal J|\).  The available capacity in \(U\) is
\(|U|-q\), where \(q\) is the number of \(C\)-blocks contained wholly in
\(U\).  Those blocks are disjoint and have size at least two, so
\(q\le |U|/2\).  Hence the available capacity is at least
\(|U|/2\ge|\mathcal J|\).  Capacitated Hall therefore supplies the
representatives; take them for \(Y\).

If \(\mathcal D\) is empty, take any singleton for \(Y\).  In every case
\(Y\) is nonempty and proper: a selected representative set omits at least
one atom from every nonempty \(D\)-block, while a singleton cannot contain a
\(C\)-block.

Let \(A\subset V\) be the endpoints of the \(R\)-edges represented by \(Y\).
The restriction \(R[A]\) is the unique perfect matching of \(G_c[A]\).
Indeed, a second perfect matching would have symmetric difference with
\(R[A]\) containing an alternating cycle, necessarily an entire cycle
component of \(G_c\), but \(Y\) contains no \(\mathcal C\)-block.

Similarly, \(R[V-A]\) is the unique perfect matching of \(G_d[V-A]\):
because \(Y\) meets every \(\mathcal D\)-block, the complement contains none
of them in full.  Both shores are nonempty.  By (F),
\(A\in\mathcal S_c\) and \(V-A\in\mathcal S_d\), contradicting the two-part
case of (H2).  ∎

## 4. Exact sharpness controls

These controls test the synthesis rather than strengthen the theorem.

### Pairwise-disjoint support matchings are not automatic

On vertices \(0,\ldots,7\), let \(h=67\),

\[
\begin{aligned}
E_0&=\{03,15,27,46\},\\
E_1&=\{02,13,17,26,34,45\},\\
E_2&=\{04,07,12,35,56\},\qquad G_c=E_c\cup\{h\}.
\end{aligned}
\]

Each \(G_c\) has a unique perfect matching, but those of \(G_1\) and \(G_2\)
both use \(67\).  Thus one cannot begin by arbitrarily selecting a
pairwise-disjoint triple.  The same supports are already excluded by the
two-part partition

\[
\{0,3\}\sqcup\{1,2,4,5,6,7\},
\]

whose first shore is uniquely matchable in \(G_0\) and second shore is
uniquely matchable in \(G_1\).

### The third colour is genuinely needed

On vertices \(0,\ldots,9\), take

\[
\begin{aligned}
R&=\{01,23,45,67,89\},\\
P_0&=\{02,13,46,59,78\},\\
P_1&=\{03,12,47,58,69\},\\
P_2&=\{04,16,28,39,57\}.
\end{aligned}
\]

The cubic graph \(P_0\cup P_1\cup P_2\) has exactly eight perfect
matchings: three monochromatic, two bichromatic matchings each blocked by a
complete same-colour cycle of \(R\cup P_c\), and three trichromatic
cycle-avoiding matchings.  Therefore pairwise reasoning is insufficient;
the final step really can require all three colours.

### A fixed cycle orientation is insufficient

On twelve vertices let

\[
\begin{aligned}
R={}&\{01,23,45,67,89,10\,11\},\\
P_0={}&\{06,17,29,3\,10,48,5\,11\},\\
P_1={}&\{07,16,2\,11,34,59,8\,10\},\\
P_2={}&\{05,12,38,46,7\,10,9\,11\}.
\end{aligned}
\]

The cubic union has exactly nine perfect matchings, and every one contains a
complete selected same-colour cycle block.  This refutes the assertion that
every fixed disjoint triple \(P_0,P_1,P_2\) has a cycle-avoiding mixed
matching.  It is not an AP' model: the proper shore
\(\{0,1,2,3\}\) and its complement are uniquely matchable in two colours.
Nor does it refute existential matching choice: replacing \(P_0\) by \(R\)
admits

\[
\{01,2\,11,38,46,59,7\,10\},
\]

which is mixed and avoids every complete cycle block.

The primary verifier independently enumerates all matching tables quoted in
this section.

## 5. The exact remaining implication

Theorem 1 turns support-perfect-matching choice into a 2-SAT problem.  Each
even support cycle contributes one Boolean variable choosing an alternating
orientation; path choices are fixed.  A shared edge of the residual partial
matching \(H\) contributes a clause forbidding the two orientations that
would both select it.  Call the formula \(\Phi\).

For a satisfying choice \(x\), write

\[
K_x=P_0(x)\cup P_1(x)\cup P_2(x)
\]

and, for every support cycle \(C\) of colour \(c\), define its selected block

\[
B_{c,C}(x)=P_c(x)\cap E(C).
\]

The remaining parent implication is precisely:

> If there is no proper two-colour partition whose two induced support
> graphs have unique perfect matchings, then \(\Phi\) is satisfiable and some
> satisfying choice \(x\) has a nonmonochromatic perfect matching of \(K_x\)
> containing no whole block \(B_{c,C}(x)\).

There are two load-bearing gaps:

1. turn an unsatisfiable implication cycle in \(\Phi\) into a proper
   two-colour uniquely-matchable partition; and
2. when \(\Phi\) is satisfiable, choose its orientations jointly with the
   cycle-avoiding Bogdanov matching.

The twelve-vertex control proves that the quantifier over \(x\) must be
existential.  Proving this dichotomy would close AP' under
\(\Delta(D)\le4\); it would still not close AP' at higher degree.

## Verification

```text
python claims/arbitrary-order/verify_all_diagonal_support_level_maximum_degree_four_reduction_and_common_perfect_matching_exclusion.py
python claims/arbitrary-order/audit_all_diagonal_support_level_maximum_degree_four_reduction_and_common_perfect_matching_exclusion.py
```

The primary exhausts all \(51^2=2601\) ordered pairs of maximum-degree-two
graphs containing one fixed perfect matching on six vertices.  It constructs
the Hall shore and counts the induced perfect matchings exactly.  It also
replays the eight-, ten-, and twelve-vertex sharpness controls.

The audit uses no graph representation.  It enumerates every ordered pair of
disjoint cycle-block families through six matching atoms and constructs the
selector with an independent capacitated max-flow implementation.  Both
scripts run in a few seconds.  Their scope is bounded; the written Hall and
symmetric-difference argument is the arbitrary-order proof.

## Boundary

- AP' under \(\Delta(D)\le4\) remains open.
- Full AP' at every even order remains conjectural.
- WB1's weighted-witness theorem remains valid and strictly stronger on its
  actual-witness scope; no converse to the WB2 bridge is asserted.
- The finite \(n=10\) searches from this sprint are separate computational
  evidence and are not used in either theorem.
- The all-diagonal branch, every bichromatic branch, and the global
  conjecture remain unresolved.
