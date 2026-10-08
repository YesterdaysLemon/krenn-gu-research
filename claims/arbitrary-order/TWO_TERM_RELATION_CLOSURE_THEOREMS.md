# Two-term relation closure: grid, odd cycle, completeness, inertness

## Status

**Proved for every even order n, over C (Theorems A and B over every field of
characteristic not two).**  These are conditional implications and scope
statements about the repository's "row-space" / transported-binomial
mechanism.  None of them excludes a witness without explicit support premises,
none is an occurrence theorem, and none changes the frontier.  Theorems A and
B are division-free sharpenings of mechanisms already in the repository (the
full-word quotient grid of
[source-cancellation-mechanisms](../../docs/strategy/source-cancellation-mechanisms-2026-09-13.md)
and its coloured-slot parity clauses); Theorems C and D are new scope
statements.  No independent audit and no Lean formalization exist.  The global
Krenn–Gu conjecture remains **UNRESOLVED**.

## Setting

Three colours, even `n`, blocks `W_ij in C^{3x3}` with `W_ji = W_ij^T`, and
`T_W(w) = sum_M m_M(w)` over perfect matchings `M` of `K_n`, where
`m_M(w) = prod_{ij in M} W_ij[w_i, w_j]`.  A witness has `T_W = Delta`
(value 1 on the three constant words, 0 on every mixed word).  A *support* is
a set `S` of physical entries assumed nonzero, all other entries zero.  At a
word `w`, a matching is *live* if all its entries lie in `S`; the *fibre* of
`w` is the set of live matchings.  On the torus `(C^*)^S` the fibre equation
reads `sum_{M live} X^{m_M(w)} = delta_w`.

**BL closure.**  For a support `S`, the full-word binomial-linear closure
`BL(S)` maintains a lattice `Lambda` of exponent vectors `r` with known values
`X^r = c(r)`, and repeats: (i) replace every live monomial by `c * Y_[class]`,
classes being cosets of `Lambda`, with `Y_0 = 1` the constant class; (ii) take
the rational row space of all fibre equations; (iii) a consequence `Y = 0` is a
contradiction, and a consequence `Y_u = c Y_v` is inserted into `Lambda`
(a lattice relation with value `!= 1` on the zero vector is a contradiction).
It stops when no new relation appears.  Implementation:
`tools/explore/binomial_linear_closure.py` (integer Hermite insertion, exact
rational row reduction with python-flint).  The recursive variant used in the
eight-vertex programme adds induced coefficients `T_{W[A]}(w)` as further torus
variables and their Laplace identities as further rows.

## Theorem A (two-matching grid, division-free)

Let `P, Q` be disjoint nonempty vertex sets and `R` the rest.  Fix a word `c`
on `R`, colourings `alpha_0, alpha_1` of `P` and `beta_0, beta_1` of `Q`, and
put `w_ab = (alpha_a on P, beta_b on Q, c on R)`.  Let `M != N` be perfect
matchings with no edge of `M union N` joining `P` to `Q`, and assume every
other perfect matching has a vanishing monomial at all four words `w_ab`.
Then, with `x_a` (resp. `u_b`) the product of the factors of `M`-edges not
meeting `Q` (resp. meeting `Q`) at `w_ab`, and `y_a, v_b` likewise for `N`,

```text
T(w_ab) = x_a u_b + y_a v_b,
T(w_00) x_1 u_1 = T(w_00)T(w_11) - x_0 u_0 T(w_11) - T(w_01)T(w_10)
                  + x_0 u_1 T(w_10) + x_1 u_0 T(w_01).
```

Hence `T(w_01) = T(w_10) = T(w_11) = 0` implies
`T(w_00) m_M(w_11) = T(w_00) m_N(w_11) = 0` (and the same for the two cross
products `x_1 v_1`, `y_1 u_1`).  In particular, if `w_00` is constant, the
other three words are mixed, and **one** of `m_M(w_11)`, `m_N(w_11)` is
nonzero, there is no witness.

*Proof.*  An `M`-edge not meeting `Q` has endpoints in `P union R`, so its
factor depends only on `a`; an edge meeting `Q` has no endpoint in `P`, so its
factor depends only on `b`.  The displayed identity is a polynomial identity in
eight variables (expand both sides).  If the three mixed corners vanish the
right side vanishes.  Ideal membership of the other three products is checked
by the verifier.  ∎

The repository's ratio form `rho(w_00)rho(w_11) = rho(w_01)rho(w_10)` assumed
all eight corner monomials nonzero; Theorem A needs one.  The cost is the
explicit zero premises making each corner fibre exactly `{M, N}`.

## Theorem B (odd opposite-ratio cycle)

Let `a != b` be vertices with colours `alpha, beta`, and `s_1, ..., s_k`
(`k` odd, indices mod `k`) slots `s_t = (v_t, gamma_t)` with
`v_t notin {a, b}`.  Put `A_t = W_{a v_t}[alpha, gamma_t]`,
`B_t = W_{b v_t}[beta, gamma_t]`, `p_t = A_t B_{t+1} + A_{t+1} B_t`.  Then

```text
sum_{t=1}^k (-1)^(t+1) p_t prod_{j notin {t,t+1}} B_j = 2 A_1 prod_{j != 1} B_j,
```

and for even `k` the same alternating sum is identically zero.  Consequently,
if for each `t` some mixed word `w_t` (colours `alpha, beta, gamma_t,
gamma_{t+1}` at `a, b, v_t, v_{t+1}`) has `T(w_t) = C_t p_t` identically under
the zero premises, then
`2 A_1 prod_{j != 1} B_j prod_t C_t` lies in the span of the `T(w_t)` with
polynomial coefficients, so a witness needs one of these factors to vanish
(characteristic not two).  The natural cofactor is
`C_t = T_{W[V - {a,b,v_t,v_{t+1}}]}`, when every other two-open term of
`w_t` vanishes.

*Proof.*  On the torus `p_t / (B_t B_{t+1}) = tau_t + tau_{t+1}` with
`tau = A/B`; the alternating sum of `tau_t + tau_{t+1}` around a cycle
telescopes to `2 tau_1` for odd `k` and to `0` for even `k`.  Clearing the
denominators gives the displayed polynomial identity, which the verifier also
expands for `k = 3, 5, 7, 9`.  ∎

## Theorem C (BL is complete on binomial supports)

Call `S` a *binomial support* if every mixed word has 0 or 2 live matchings and
every constant word has exactly one.  For such `S` at any even order `n`, the
following are equivalent:

1. there is a witness with support exactly `S`;
2. `BL(S)` ends without contradiction;
3. there are no integers `k_w` (mixed two-term words `w`, live matchings
   `M_w, N_w`) and `k_c` (colours) with
   `sum_w k_w (m_{M_w} - m_{N_w}) + sum_c k_c m_c = 0` and `sum_w k_w` odd,
   where `m_c` is the exponent vector of the unique live matching of the
   constant word of colour `c`.

*Proof.*  On `(C^*)^S` the target system is exactly the binomial system
`X^{m_{M_w} - m_{N_w}} = -1`, `X^{m_c} = 1`; words with no live matching hold
automatically.  Let `Lambda` be the lattice spanned by the exponent rows.
(3) says that the assignment `row -> (-1 or 1)` extends to a well-defined
homomorphism `sigma: Lambda -> C^*`.  If it does, `C^*` is divisible, hence an
injective abelian group, so `sigma` extends to `Z^S -> C^*`, i.e. to a point
`X` of the torus solving every equation; this gives (1).  Conversely a witness
makes `sigma(r) = X^r` well defined.  For (2): the closure's first round
inserts every binomial row; Hermite insertion performs unimodular operations
on the generating set, so a relation `sum k_i r_i = 0` with odd sign reaches the
zero vector with value `-1` and is reported, while if `sigma` is well defined
every later deduction is valid on the solution `X` and no contradiction can
arise.  ∎

So, restricted to binomial supports, the Krenn–Gu conjecture at order `n` is
equivalent to the purely combinatorial statement that every binomial support
satisfying the single-term conditions carries an odd sign circuit (3).

## Theorem D (BL is inert on two-term-free supports)

Suppose every mixed word has 0 or at least 3 live matchings and every constant
word has at least one.  Then `BL(S)` ends after at most two rounds with no
contradiction, and its only binomials are `X^{m_c} = 1` for the colours whose
constant word has a single live matching.

*Proof.*  A monomial `m_M(w)` determines `w` (each vertex lies in one edge,
whose entry records its colour) and `M`; so distinct (word, matching) pairs
give distinct monomials, and each fibre row owns its monomial columns, sharing
only `Y_0`.  A vector of the row space restricted to the columns owned by `w`
is `lambda_w (1, ..., 1)`.  A consequence with one nonzero coordinate, or with
two coordinates outside the span of the single-term constant rows, would need
some row with at most two nonzero entries in total; mixed rows have at least
three, constant rows with two or more live matchings have at least three
(including `Y_0`).  So round one inserts only `X^{m_c} = 1`.  These `m_c` have
pairwise disjoint supports (colour-`c` entries), so no lattice relation arises,
and `m - m' in Lambda` for distinct matching monomials forces `{m, m'}` to be
two of the `m_c` (coefficients of a disjoint-support combination lie in
`{-1, 0, 1}`, and `m superset m_c` forces `m = m_c` by cardinality).  Round two
therefore only replaces those monomials by `Y_0`, which changes nothing else.  ∎

The full support (every entry nonzero) satisfies the hypothesis at every
order `n >= 4`, since each fibre has `(n-1)!! >= 3` live matchings.  The
recursive variant is not covered by Theorem D: a vertex expansion of an
induced coefficient can have two live terms even when every full fibre has
three or more.

## Boundary

- Theorems A–D are about relations among values of supported terms; none
  supplies its premises from a hypothetical witness.  No occurrence statement
  is proved.
- Theorem C covers only supports whose fibres all have at most two live
  matchings with one-term constant fibres; with a two-term constant fibre the
  remaining equation `X^m + X^{m'} = 1` is not binomial and only one-sided
  tests are claimed.
- Theorem D is a no-go for the *full-word* closure; it does not bound the
  recursive closure, Groebner-type reasoning, or the killer theorem (which the
  full support violates).
- The six-vertex consequences (the 27-entry pattern and the 51-entry
  survivor) are recorded in
  [the attempt note](../../docs/strategy/row-space-all-orders-attempt-2026-10-08.md)
  with their own verifiers.

## Verification

```text
python claims/arbitrary-order/verify_two_term_relation_closure_theorems.py
```

The verifier replays the displayed identities of A and B, the ideal
memberships in A, and the distinct-monomial lemma behind D at `n = 4, 6, 8`.
It does not replay the proofs of C and D, which are the arguments above.
Primary verifier only; no independent audit exists.
