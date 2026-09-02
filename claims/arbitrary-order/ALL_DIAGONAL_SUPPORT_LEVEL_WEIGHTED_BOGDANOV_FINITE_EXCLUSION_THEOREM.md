# All-diagonal weighted Bogdanov: support-level abstraction and finite exclusion at n = 6, 8

## Status

This is a **finite computer-assisted exact theorem** in the all-diagonal
branch (every edge block diagonal: monochromatic edges with arbitrary complex
weights) together with an exact **reduction** valid at every even order.  It
proves that no all-diagonal witness exists on eight vertices, and that at
both `n = 6` and `n = 8` the exclusion follows from support-level necessary
conditions alone: which weights are nonzero and which principal hafnians are
nonzero, never their values.  It is not a proof of the Krenn–Gu conjecture,
says nothing about bichromatic entries, and does not settle the all-diagonal
branch at `n >= 10`.  The global conjecture remains **UNRESOLVED**.

Evidence mode: two independent SAT encodings solved by two independent
solvers (CaDiCaL 1.5.3 and Glucose 4.1 through the pinned `python-sat`).  No
DRAT proof trace is recorded, because no proof checker is available on the
reference host; this gap is stated rather than hidden.

## The support abstraction (AP')

Let `n` be even and let `V = {0,...,n-1}`.  A **support model** consists, for
each colour `c in {0,1,2}`, of a graph `G_c` on `V` and a family `S_c` of even
subsets of `V` such that:

- (a) `empty, V in S_c`, and the two-element members of `S_c` are exactly
  the edges of `G_c`;
- (L) *Laplace accessibility*: if `A in S_c` and `v in A`, there is `u in A`
  with `vu in G_c` and `A - {v,u} in S_c`;
- (S) *support*: if `A in S_c` then `G_c[A]` has a perfect matching;
- (F) *forcing*: if `G_c[A]` has exactly one perfect matching then
  `A in S_c`;
- (H2) *rainbow-freeness*: there is no ordered partition `(A_0,A_1,A_2)` of
  `V` into even classes, at least two nonempty, with `A_c in S_c` for all `c`.

**Lemma (bridge).**  Every all-diagonal witness `(Z^0,Z^1,Z^2)` on `V`
yields a support model with `G_c = supp(Z^c)` and
`S_c = {A even : haf(Z^c[A]) != 0}`.

*Proof.*  (a): `haf(Z^c[empty]) = 1`, `haf(Z^c[V]) = 1` by the constant
words, and `haf(Z^c[{u,v}]) = Z^c_(uv)`.  (L): Laplace expansion
`haf(Z^c[A]) = sum_u Z^c_(vu) haf(Z^c[A - {v,u}])`, so a nonzero left side has
a nonzero term.  (S): a hafnian with no perfect matching in its support is an
empty sum.  (F): a hafnian whose support has exactly one perfect matching is
a single nonzero monomial.  (H2): with diagonal blocks every mixed word
factorizes, `T_W(a) = prod_c haf(Z^c[V_c(a)])`, and the target vanishes on
non-constant words.  ∎

Consequently, if (AP') has no model on `V` then there is no all-diagonal
witness on `V`.  The converse fails: a support model need not lift to weights,
so (AP') is strictly weaker than the all-diagonal equations.

## Theorem (finite)

**(AP') has no model for `n = 6` and for `n = 8`.**  Hence there is no
all-diagonal Krenn–Gu witness on six or on eight vertices, and both
exclusions hold at the support level.

The `n = 6` statement is also a consequence of the repository's general
six-vertex exclusion; the `n = 8` statement is new, since the eight-vertex
finite certificates cover sparse skeletons and specific singleton families,
not arbitrary all-diagonal supports (which may have every pair carrying a
weight in some colour).

**Sharpness at `n = 8`.**  Dropping any one of the three non-trivial
ingredients makes (AP') satisfiable:

| dropped ingredient | result | witness model |
|---|---|---|
| three-part rainbow clauses (two-part only) | SAT | three pairwise disjoint perfect matchings, one per colour, on a cubic skeleton: the classical Bogdanov configuration, excluded only by a three-part rainbow |
| forcing (F) | SAT | two colours as perfect matchings, the third an 11-edge graph whose unmatched 4-sets are declared cancelled |
| Laplace (L) | SAT | dense supports whose hafnian families are declared empty above the edge level |

So the exclusion at `n = 8` genuinely uses the interaction of Laplace
accessibility, single-monomial forcing, and three-colour rainbow-freeness,
three support mechanisms also present in the `WB1` setting; none suffices
with the other two removed.  Adding the degree bound `Delta(D) <= 4` also
gives UNSAT at `n = 8`, as it must from the unrestricted finite theorem.
That bounded finite run is not an all-order consequence of `WB1`.

## Conjecture (support-level weighted Bogdanov)

**(AP') has no model for every even `n >= 6`.**

This is a purely combinatorial statement about three graphs and three set
families; no weights appear.  By the bridge lemma it implies the all-diagonal
case of the Krenn–Gu conjecture at every order, and hence that every witness
has a bichromatic entry.  This theorem proves it at `n = 6, 8` for all
degrees.  `WB1` excludes actual weighted witnesses when
`Delta(G_0 + G_1 + G_2) <= 4`, but its numerical score and noncancellation
steps do not transfer through the one-way support bridge.

The later [degree-four support reduction and common-perfect-matching
exclusion](ALL_DIAGONAL_SUPPORT_LEVEL_MAXIMUM_DEGREE_FOUR_REDUCTION_AND_COMMON_PERFECT_MATCHING_EXCLUSION_THEOREM.md)
(`WB3`) proves that an AP' model of maximum degree four has even path/cycle
supports with a residual partial matching, and excludes the subcase where
two supports share a perfect matching.  The remaining orientation/blocker
dichotomy is open.  Thus AP' at maximum degree four, AP' at higher degree,
and the all-order conjecture all remain unresolved.

What a proof must overcome is visible in the sharpness table.  Two colours
alone can satisfy every two-part condition (a Hamiltonian cycle does), so the
argument must use the third colour as Bogdanov did, but with `S_c` in place
of "all unions of matching edges": accessibility descends from `V` through
`G_c`-edges but does not guarantee arbitrary unions, and cancellation is
modelled by the freedom to omit from `S_c` any set whose support has two or
more perfect matchings.

## Verification

```text
python claims/arbitrary-order/verify_all_diagonal_support_level_weighted_bogdanov_finite_exclusion.py
python claims/arbitrary-order/audit_all_diagonal_support_level_weighted_bogdanov_finite_exclusion.py
```

The primary encodes (a), (L), (S), (F), (H1) `V in S_c`, and (H2) with
matching-presence auxiliaries, writes the DIMACS file and records its SHA-256,
solves with CaDiCaL 1.5.3 at `n = 6` and `n = 8` (UNSAT), and reproduces the
three relaxations at `n = 8` (SAT) with their decoded supports.  The
independent audit uses a different encoding (no explicit support clause,
forcing through a cardinality constraint, rainbow clauses from set partitions
rather than colour words) and a different solver, Glucose 4.1, at `n = 6`,
at `n = 8` with `Delta(D) <= 4`, and at `n = 8` unrestricted (all UNSAT).
Expected runtimes on the reference host: about six minutes for the primary
(dominated by the unrestricted `n = 8` instance) and about three minutes for
the audit.  Both write JSON summaries to the untracked `tmp/` directory.

## Boundary

- Finite: `n = 6` and `n = 8` only.  The `n = 10` instances were launched but
  are not part of this theorem.
- All-diagonal only.  The bridge lemma fails as soon as one block has a
  bichromatic entry, because then mixed words no longer factorize.
- Solver-based without a proof trace.  Two independent encodings and solvers
  agree; a DRAT-checked certificate remains an open evidence obligation.
- The conjecture above is a conjecture.  Nothing here changes the global
  status.
