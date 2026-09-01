# GHZ closure theorem: matching-polytope faces give asymptotic realizability

## Status

This is an exact arbitrary-order theorem over `C` about the *closure* of the
set of perfect-matching tensors.  It is a **structural no-go for a whole
class of proof routes**, not a counterexample and not a proof of the
Krenn--Gu conjecture.  It changes no existing claim.  The global conjecture
remains **UNRESOLVED**.

Informally: for every even `n >= 4` the ternary GHZ tensor is a *limit* of
perfect-matching tensors `T_W` with all blocks monochromatic matrix units,
even though (for `n >= 6`) the conjecture says it is never *equal* to one.
Consequently no polynomial identity, rank bound, flattening bound, or any
other condition that is closed under limits of the tensor `T_W` alone can
separate the GHZ tensor from the hafnian image.  Every valid proof must use
the exact fibre `T_W = Delta`, that is, structure of `W` itself (such as the
exact zero columns of the killer theorem), and any numerical search whose
cost tends to zero along diverging weights has found nothing.

## Setting

For even `n` and blocks `W_ij in C^(3 x 3)` (`i<j`), write

```text
T_W(a_1,...,a_n) = sum_(perfect matchings M of K_n) product_({i,j} in M) W_ij[a_i,a_j],
Delta_n(a)      = 1 if a_1 = ... = a_n, else 0.
```

Let `Phi_n : W -> T_W` be the (polynomial) matching-tensor map and
`Im(Phi_n) subset (C^3)^(tensor n)` its image.  For a graph `G` on the
vertex set `[n]` with a proper three-edge-colouring `kappa : E(G) -> {0,1,2}`
and a function `nu : E(G) -> Z`, define the one-parameter family

```text
W_e(eps) = eps^(nu(e)) e_(kappa(e)) e_(kappa(e))^T   for e in E(G),
W_e(eps) = 0                                          for e not in E(G).      (1)
```

Every block is a monochromatic matrix unit, so a perfect matching `M` of `G`
contributes only to the word `chi_M` in which every vertex receives the colour
of its `M`-edge:

```text
T_(W(eps))(a) = sum_(M in PM(G), chi_M = a) eps^(nu(M)),    nu(M) = sum_(e in M) nu(e).   (2)
```

## Theorem

**Theorem A (face criterion).**  Let `G` be a cubic graph on `n` vertices
with a proper three-edge-colouring whose colour classes `M_0,M_1,M_2` are
perfect matchings.  Suppose `nu : E(G) -> Z` satisfies

```text
nu(M_c) = 0            for c = 0,1,2,
nu(M)   >= 1           for every other perfect matching M of G.             (3)
```

Then the family (1) satisfies, identically in `eps`,

```text
T_(W(eps)) = Delta_n + eps R(eps),                                          (4)
```

where `R(eps)` is a tensor with polynomial entries in `eps` supported on
non-constant words.  In particular `T_(W(eps)) -> Delta_n` as `eps -> 0`, and
`Delta_n` lies in the Euclidean closure, hence in the Zariski closure, of
`Im(Phi_n)`.  Condition (3) holds for some `nu` if and only if
`{M_0,M_1,M_2}` is the vertex set of a face of the perfect-matching polytope
of `G`.

**Theorem B (existence for every even order).**  For every even `n >= 4`
there is a cubic graph `G_n` on `n` vertices with a proper three-edge-colouring
and an integer potential `nu_n` satisfying (3).  Explicitly, `G_4 = K_4` with
its three perfect matchings as colour classes and `nu_4 = 0`, and `G_(n+2)`
is obtained from `G_n` by replacing one vertex by a triangle (truncation).
Hence

```text
Delta_n in closure(Im(Phi_n))    for every even n >= 4.                     (5)
```

**Corollary C (no tensor-level separation).**  Let `P` be any polynomial on
`(C^3)^(tensor n)` with `P(T_W) = 0` for all `W`, or more generally any
subset `Z subset (C^3)^(tensor n)` closed in the Euclidean topology with
`Im(Phi_n) subset Z`.  Then `P(Delta_n) = 0`, respectively `Delta_n in Z`.
No such condition can exclude a Krenn--Gu witness.  In particular, upper
bounds on flattening ranks, slice ranks, border ranks, or on any other
lower-semicontinuous invariant of `T_W`, and every identity in the ideal of
the hafnian image, are automatically satisfied by `Delta_n`.

**Corollary D (numerical searches).**  For every even `n >= 4` the infimum
over `W` of every continuous loss `L(T_W - Delta_n)` with `L(0)=0` is zero,
attained only in the limit of unbounded weights when `n >= 6` (conditionally
on the conjecture; unconditionally at `n = 6` by the six-vertex exclusion).
A cost tending to zero is therefore not evidence for a witness unless the
weights stay bounded in some vertex gauge.

## Proof

### Theorem A

Let `M` be a perfect matching of `G` inducing a constant word `c^n`.  Every
edge of `M` then has colour `c`, so `M subset M_c`; since both are perfect
matchings, `M = M_c`.  Conversely `M_c` induces `c^n`.  Hence by (2)

```text
T_(W(eps))(c^n) = eps^(nu(M_c)) = 1     for every eps,
```

using the first line of (3).  Every other perfect matching induces a
non-constant word and has `nu(M) >= 1`, so each non-constant coefficient
`T_(W(eps))(a) = sum eps^(nu(M))` is a polynomial in `eps` with zero constant
term.  This is (4), and the limit statement follows because the entries of
`R` are polynomials.  A Euclidean limit of points of `Im(Phi_n)` lies in the
Zariski closure of `Im(Phi_n)` because polynomials are continuous.

For the face statement: the perfect-matching polytope of `G` is the convex
hull of the incidence vectors of its perfect matchings, and these vectors are
exactly its vertices.  A set `S` of vertices of a polytope is the vertex set of
a face if and only if some linear functional attains its minimum over the
polytope exactly on `S`.  For `S={M_0,M_1,M_2}` such a functional, shifted
to have minimum zero and scaled to be integral with gap at least one, is
precisely a potential `nu` satisfying (3), and conversely.  (The integrality
scaling uses that a rational functional can be chosen, since the polytope is
rational.)

### Theorem B

*Truncation.*  Let `G` be cubic with a proper three-edge-colouring `kappa`
whose classes are perfect matchings, let `v` be a vertex with incident edges
`v u_c` of colour `c` (`c=0,1,2`), and let `nu` satisfy (3) for `G`.  Define
`G'` by deleting `v`, adding three new vertices `t_0,t_1,t_2`, and adding the
edges

```text
u_c t_c        with colour c,                 (attachment edges)
t_a t_b        with colour 3-a-b,   a<b.      (triangle edges)
```

At `t_c` the three incident colours are `c`, `3-c-a = b`, and `3-c-b = a`,
so the colouring is proper, and every colour class `M'_c = M_c - v u_c
+ u_c t_c + t_a t_b` is again a perfect matching.

*Perfect matchings of `G'`.*  A perfect matching of `G'` uses either one or
three attachment edges: with none, the three triangle vertices cannot be
matched among themselves; with two, the remaining triangle vertex has no free
partner.  If it uses exactly `u_c t_c`, it must contain `t_a t_b`, and its
remaining edges form a perfect matching of `G - v - u_c`; adding `v u_c`
gives a perfect matching `M` of `G`, and this correspondence
`M -> M - v u_c + u_c t_c + t_a t_b` is a bijection between perfect matchings
of `G` and perfect matchings of `G'` with one attachment edge.  If it uses
all three attachment edges, its remaining edges form a perfect matching `N`
of `G - N[v]`, where `N[v] = {v,u_0,u_1,u_2}`; conversely every such `N`
extends uniquely.

*Potential.*  Fix an integer `A >= 1` and put

```text
nu'(u_c t_c) = nu(v u_c) + A,
nu'(t_a t_b) = -A,
nu'(e)       = nu(e)          for every other edge.
```

A lifted matching satisfies `nu'(M') = nu(M) - nu(v u_c) + (nu(v u_c) + A)
- A = nu(M)`.  Hence `nu'(M'_c) = 0` and every lifted extra matching keeps
`nu' >= 1`.  A three-attachment matching has

```text
nu' = 3A + sum_c nu(v u_c) + nu(N) >= 1
```

as soon as `A >= (1 - sum_c nu(v u_c) - min_N nu(N))/3`, where the minimum
is over perfect matchings `N` of `G - N[v]` (vacuous if there are none).
Thus `nu'` satisfies (3) for `G'`.

*Induction.*  `K_4` with colour classes its three perfect matchings has no
other perfect matching, so `nu = 0` satisfies (3).  Truncating any vertex
gives the triangular prism on six vertices, and iterating gives cubic graphs
`G_n` for every even `n >= 4` together with potentials `nu_n` satisfying
(3).  Theorem A then gives (5).

The canonical family used by the verifier truncates the vertex of largest
label at every step and takes the smallest admissible `A`.  For the prism
this is `A = 1`: the three rungs receive `eps^1`, the three triangle edges
opposite to them `eps^(-1)`, and the single extra matching (the three rungs)
contributes `eps^3` to one mixed word.

### Corollaries C and D

Corollary C is the continuity statement already used in Theorem A.  For
Corollary D, `L(T_(W(eps)) - Delta_n) -> L(0) = 0` along the family of
Theorem B.  If a bounded sequence of witnesses in some vertex gauge had
cost tending to zero, a convergent subsequence would give an exact witness
by continuity of `Phi_n`; at `n = 6` this contradicts the six-vertex
exclusion, and at general `n >= 6` it contradicts the conjecture.

## Consequences for the programme

1. **Every proof must be fibre-exact.**  The conjecture is the statement
   `Delta_n notin Im(Phi_n)` for `n >= 6`, while `Delta_n in closure(Im(Phi_n))`
   for all `n`.  A proof cannot consist of invariants of `T_W`; it must
   derive structure of `W` from the exact equation, as the column-killer
   theorem, the diagonal-anchor theorem, and the Laplace/Wick identities do.
   Rank-drop, sensor-rank, and flattening arguments are valid only in the
   role they already play in the repository: as consequences of exact
   identities in `W`, never as conditions on `T` alone.

2. **The asymptotic witnesses are exactly Bogdanov-type structures.**  Every
   limiting family in Theorem B is a cubic graph with three monochromatic
   perfect matchings whose extra matchings are suppressed by weights, not
   cancelled.  For `n >= 6` the extra matchings always exist (the cubic
   diagonal exclusion), so `nu` is genuinely nonzero and the weights are
   unbounded in every vertex gauge.  An exact witness would have to achieve
   with cancellation what these families achieve only in the limit.

3. **Numerical evidence.**  Unconstrained complex Levenberg--Marquardt on
   the full `n=6` and `n=8` systems repeatedly drives the least-squares
   cost to `10^-12`--`10^-15` while the largest weights grow to `10^1`--`10^4`;
   in every such run all nonzero blocks are monochromatic matrix units on a
   cubic three-edge-coloured skeleton, with weights spread over several
   orders of magnitude.  These are the families of Theorem A, not witnesses.
   The repository's exploratory optimizer should therefore be read with this
   theorem in mind.

## Boundary

- The theorem says nothing about `Im(Phi_n)` itself; it does not exclude,
  construct, or approximate an exact witness.
- It does not claim that every point of the closure of `Im(Phi_n)` arises
  from a matrix-unit family, nor classify all faces of matching polytopes
  containing three colour classes.
- The `n = 6` unconditional statement in Corollary D depends on the
  repository's six-vertex computer-assisted exclusion; the `n >= 8`
  statement is conditional on the conjecture.
- The literature consulted (Krenn--Gu--Soltesz; Chandran--Gajjala;
  Chandran--Gajjala--Illickan, MFCS 2024; the maintained problem page) treats
  exact realizability only; no statement about closures or limiting families
  was found there, but this novelty assessment is bounded and not a
  literature search of record.

## Verification

```text
python claims/arbitrary-order/verify_ghz_closure_matching_polytope_face_asymptotic_realizability.py
python claims/arbitrary-order/audit_ghz_closure_matching_polytope_face_asymptotic_realizability.py
```

The primary verifier builds the canonical truncation family for
`n = 4,...,16`, enumerates all perfect matchings of each `G_n`, checks the
proper colouring and the perfect-matching colour classes, checks (3)
exactly in integers, and for `n <= 10` expands `T_(W(eps))` symbolically over
all perfect matchings of `K_n` to confirm (4) as a polynomial identity.  The
independent audit rebuilds the family with a different perfect-matching
enumeration, recomputes the potentials, and evaluates the full `3^n` tensor
numerically at `eps = 10^-1, 10^-2, 10^-3` for `n = 6, 8, 10`, confirming
that all constant coefficients equal one to machine precision and that the
largest mixed coefficient scales like `eps^(nu_min)` with the recorded
minimum extra potential.  The written proof above is the theorem; the
programs are exact and numerical supporting checks of the displayed family.
