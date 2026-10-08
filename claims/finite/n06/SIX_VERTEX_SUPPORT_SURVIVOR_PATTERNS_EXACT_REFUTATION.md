# Six-vertex support-survivor patterns: exact two-term refutations

**Status: exact finite computation at the level of three fixed support
patterns (d = 3, n = 6), with short hand-checkable refutations replayed by
an exact verifier.  This is NOT a new six-vertex theorem.** The six-vertex
exclusion is already recorded, computer-assisted, in
[`SIX_VERTEX_CERTIFICATE.md`](SIX_VERTEX_CERTIFICATE.md); nothing here
changes its scope or evidence.  This note explains *which quantitative
relation* a support-level (zero/nonzero) model lacks, using three patterns
that pass every single-term support test.  The two local lemmas in Section 4
are elementary and hold at every even order. Whether the strengthened
support model they suggest closes any open case is **not** established here.
No independent audit exists.  Global Krenn–Gu status remains
**UNRESOLVED**.

Verifier:
[`verify_six_vertex_support_survivor_patterns.py`](verify_six_vertex_support_survivor_patterns.py)
(sympy, integer/rational arithmetic only).

```text
python claims/finite/n06/verify_six_vertex_support_survivor_patterns.py               # ~3 s
python claims/finite/n06/verify_six_vertex_support_survivor_patterns.py --minimality  # ~45 s
```

## 1. Setting and provenance

Blocks `W_ij` in `C^{3x3}` for `i < j`, with `W_ji = W_ij^T`.  For a word
`a` in `{0,1,2}^6`,

```text
T_W(a) = sum over the 15 perfect matchings M of K_6 of  prod_{ij in M} W_ij[a_i, a_j].
```

A witness has `T_W(a) = 1` on `000000, 111111, 222222` and `0` on the other
726 words.  A *pattern* fixes which entries are nonzero; "`ij: ab`" means
`W_ij[a,b]` (colour `a` at `i`, colour `b` at `j`) is a nonzero unknown, and
every unlisted entry is zero.

The three patterns (27, 41 and 63 nonzero entries; listed verbatim in the
verifier as `P27`, `P41`, `P63`) were supplied by the coordinating agent
from a same-day support-level model run.  That run is not part of this
branch.  It reported that each pattern satisfies Laplace accessibility,
singleton noncancellation, the GHZ zero pattern and the column-killer
theorem.  This note does not re-verify those four filters.  The verifier
re-checks only the two single-term facts visible in the equations: no
forbidden word has exactly one live matching term, and every constant word
has at least one.  The patterns are taken as data; the question here is
only why they are not realisable.

With the pattern fixed, every word equation becomes a sum of distinct
squarefree monomials in the nonzero unknowns, each with coefficient 1.  The
term census reported by the verifier is:

| pattern | nontrivial equations | forbidden words by live-term count | constant words (live terms) |
|---|---|---|---|
| P27 | 38 | 35 x 2 terms | 1, 2, 2 |
| P41 | 85 | 82 x 2 terms | 2, 2, 2 |
| P63 | 729 | 495 x 2, 181 x 3, 37 x 4, 8 x 5, 5 x 6 | 3, 2, 3 |

No forbidden word is a single monomial, so there is **no monomial kill**.
Every refutation must relate the values of at least two terms.

## 2. The calculus and the minimality claims

Work on the torus: all unknowns are nonzero.  A two-term forbidden equation
`x^u + x^v = 0` is equivalent to the binomial relation `x^(u-v) = -1`.  The
verifier's *binomial-propagation calculus* runs exact rational arithmetic
and an exact integer echelon lattice.  It repeats three sound deductions:

1. if the exponent difference `d` of two terms of an equation already has a
   known value `x^d = zeta`, the two terms merge exactly;
2. an equation left with one live class says `c * x^u = 0` with `c != 0`,
   which is a contradiction (*monomial kill after merging*);
3. an equation left with two live classes is a new binomial relation.
   Inserting it into the lattice is exact for torus solvability.  The
   system `x^(u_k) = zeta_k` is solvable iff every integer relation
   `sum c_k u_k = 0` has `prod zeta_k^(c_k) = 1`.  A violated relation
   is a contradiction (*holonomy*).

The constant words carry the right-hand side 1 as a term with exponent 0.

The calculus refutes all three patterns.  The `--minimality` run gives
these results inside the calculus:

| pattern | refuting singles / pairs | minimum equations | minimal refutations found |
|---|---|---|---|
| P27 | 0 / 0 | **3** | 23 triples, all of K_{2,3}-triangle shape; 2 inclusion-minimal constant-word 2x2 squares (4 equations) |
| P41 | 0 / 0 | **3** | 36 triples, all of K_{2,3}-triangle shape; no refuting square |
| P63 | 0 / 0, and no triple | **4** | 752 inclusion-minimal 2x2 word squares (731 trinomial kill, 21 constant word) |

Each "minimum" is relative to the calculus.  For two two-term forbidden
equations the calculus is complete: the lattice test is exactly torus
solvability.  So no two forbidden-word equations of P27 or P41 are jointly
inconsistent in any sense.

The P63 triple exclusion is exhaustive for the following reason.  The full
two-term forbidden subsystem is consistent (Section 3.3).  Therefore a
3-equation refutation must merge two terms of a longer equation using the
lattice generated by at most two binomial exponent vectors.  The verifier
enumerates every such merge: all vectors are 0/±1, so Cramer's rule
bounds the coefficients by 2.  It finds none.

## 3. The displayed refutations

The verifier prints each of these, eliminating one unknown per binomial and
showing the last equation collapse.

### 3.1 P27: odd K_{2,3} triangle (3 equations)

```text
[002000]  w01_00 w23_20 w45_00 + w03_00 w12_02 w45_00 = 0
[002200]  w01_00 w25_20 w34_20 + w05_00 w12_02 w34_20 = 0
[012010]  w03_00 w14_11 w25_20 + w05_00 w14_11 w23_20 = 0
```

Cancel the nonzero spectators `w45_00, w34_20, w14_11`.  Write
`x_k = W_0k[0, .]` and `y_k = W_2k[2, .]` for the leaves `k = 1, 3, 5`.
Every pair of leaves then gives a vanishing 2x2 permanent
`x_a y_b + x_b y_a = 0`.  With `r_k = x_k / y_k` this says
`r_1 = -r_3`, `r_1 = -r_5`, and `r_3 = -r_5`.  The first two give
`r_3 = r_5`, so the third gives `2 r_5 = 0`.  After substitution the
verifier gets `2 * w05_00 w14_11 w23_20 = 0`.

The hub pair is `{0,2}`, with `W_02[0,2] = 0` in the pattern.  That zero
removes the third matching term `W_02 W_ab` of each 4-vertex hafnian.

P27 also has a constant-word refutation with 4 equations: the 2x2 square
`002000, 200000, 202000 | 000000`.  It is the Section 3.3 mechanism, but it
is not minimum for P27.

### 3.2 P41: odd K_{2,3} triangle (3 equations)

```text
[000010]  w01_00 w23_00 w45_10 + w05_00 w14_01 w23_00 = 0
[001111]  w01_00 w25_11 w34_11 + w03_01 w14_01 w25_11 = 0
[002110]  w03_01 w12_02 w45_10 + w05_00 w12_02 w34_11 = 0
```

Here the hubs are `0` (colour 0) and `4` (colour 1), and the leaves are
`1, 3, 5`.  The pattern has `W_04[0,1] = 0`.  The argument is the same
signed triangle, and the substitution ends in
`2 * w05_00 w12_02 w34_11 = 0`.

### 3.3 P63: rank-one square (4 equations; no 3-equation refutation)

The 495 two-term forbidden equations of P63 are **jointly consistent** on
the torus: the integer relation lattice has no odd vector.  Sign holonomy
alone therefore cannot refute P63.  The value `-1` must be transported into
a longer equation.  Vary the colours of vertices 2 and 5 over `{0,2}` and
fix the other colours.  The matchings `M1 = {01,23,45}` and
`M2 = {05,12,34}` are live at all four corners:

```text
[000100]  w01_00 w23_01 w45_00 + w05_00 w12_00 w34_10 = 0
[000102]  w01_00 w23_01 w45_02 + w05_02 w12_00 w34_10 = 0
[002100]  w01_00 w23_21 w45_00 + w05_00 w12_02 w34_10 = 0
[002102]  w01_00 w23_21 w45_02 + w01_00 w25_22 w34_10 + w05_02 w12_02 w34_10 = 0
```

The ratio `R(c2,c5) = term_M1 / term_M2` is

```text
R(c2,c5) = (w01_00 / w34_10) * (w23[c2,1] / w12[0,c2]) * (w45[0,c5] / w05[0,c5]),
```

which is a rank-one function of `(c2,c5)`.  Hence

```text
R(2,2) = R(2,0) R(0,2) / R(0,0) = (-1)(-1)/(-1) = -1.
```

So the `M1` and `M2` terms of `[002102]` cancel exactly, leaving the
single monomial `w01_00 w25_22 w34_10 = 0`.  The matching `{01,25,34}`
is live only at that corner, because `W_25` is supported on `22` alone.
The verifier's substitution ends in
`-w05_02 w12_02 w25_22 w34_10^2 / (w23_21 w45_02) = 0`.

The same square mechanism also refutes P63 against a constant word.  Use
vertices 2 and 4 with colours `{1,2}`; the corners are
`111121, 112111, 112121`, which force `R(1,1) = -1` at `111111`.  The two
live terms of `111111` then cancel exactly: **0 = 1**.

## 4. Type of relation and all-order content

| type | description | where |
|---|---|---|
| T1 monomial kill | one forbidden equation is a single nonzero monomial | absent (support model forbids it) |
| T2 sign holonomy | an odd integer relation among two-term forbidden equations, i.e. an unbalanced cycle (Harary) of `-1` ratios | P27, P41 (minimum 3; every 3-equation instance is a K_{2,3} triangle) |
| T3 transported holonomy | an even (consistent) binomial relation forces the ratio of two terms of a longer equation, or of a constant word, to equal `-1`; the remainder is a monomial kill or `0 = 1` | P63 (minimum 4; rank-one 2x2 squares); also present, non-minimally, in P27 |

No refutation needs anything beyond T2 or T3.  None uses a Gröbner basis,
a saturation, or a numerical value other than `±1`.  The only other
coefficient is the final `2` in T2.  The support abstraction treats each
two-term equation as always satisfiable, because two nonzero terms may
cancel.  It has no variable for the **value of the ratio** (`-1`), and
cannot propagate that value around a cycle or across a square.

Both minimal mechanisms are local lemmas valid at every even order `n`:

**Lemma A (odd K_{2,3} triangle).**  Work over a field of characteristic
not 2.  Fix hubs `p, q` and leaves `a_1, a_2, a_3` with fixed colours.
Suppose that for each pair `{i,j}` some forbidden word with those colours
has exactly two live terms, `X_i Y_j S_ij` and `X_j Y_i S_ij`.  Here
`X_k = W_{p a_k}[.,.]`, `Y_k = W_{q a_k}[.,.]`, and `S_ij` is a common
nonzero spectator product.  Then one of the six entries `X_k, Y_k`
vanishes.  *Proof:* `r_k = X_k / Y_k` satisfies `r_i = -r_j` on all three
edges of a triangle, so `r_1 = 0`.

**Lemma B (rank-one square).**  Fix vertices `u != v`, two colours at
each, and the colours of the other `n - 2` vertices.  Suppose two perfect
matchings `M1, M2` that do not contain the pair `uv` are live at all four
corners, and are the only live terms at three corners, which are forbidden
words.  Then the `M1` and `M2` terms cancel exactly at the fourth corner.
If that corner is a constant word whose only live terms are `M1, M2`, this
gives `0 = 1`.  If the fourth corner has exactly one further live term,
that term must vanish.  *Proof:* each term factors as (entry at `u`)
times (entry at `v`) times (a factor independent of the two varied
colours).  So `R = term_M1 / term_M2` has rank one, and
`R(x0,y0) = R(x0,y1) R(x1,y0) / R(x1,y1) = -1`.

Both lemmas have support-expressible hypotheses: which matchings are live
is a function of the support.  They can therefore be added to any
support-level model as clause families at every order.  The calculus of
Section 2 is the uniform generalisation.  It is defined identically for
every `n` and decided by exact integer linear algebra.  This makes the
**type** (T2 and T3, a signed-toric enrichment of the support model) a
candidate for an all-order statement.

What is *not* established:

- whether the support model plus this calculus is UNSAT at `n = 6` without
  the existing certificate (the calculus has not been integrated into a
  support CEGAR loop);
- whether T2 and T3 suffice at any larger order.

The existing certificate's final refinements were "primitive Laurent-unit
cubes" plus one "rational linear-monomial cube".  The latter
resembles T3.  This correspondence has not been audited here.

P63 shows that the parity-only part of the enrichment (T2, odd cycles) is
insufficient by itself; the transport step T3 is needed.

## 5. Evidence summary

- Mathematical status: three exact pattern-level non-realisability facts.
  Each has a hand-readable refutation of 3, 3 or 4 equations, and two
  elementary all-order lemmas (A, B).  This is not a new six-vertex theorem
  (already proved, computer-assisted).
- Computational mode: exact (sympy rational substitution and an exact
  integer/rational torus lattice).  Minimality is exhaustive within the
  stated calculus.
- Independent audit: none.  The hand derivations in Section 3 are a
  different route for the displayed refutations but are not a separate
  audit.
- Formalization: none.
- Live frontier: unchanged.  `n = 6` is already closed by the existing
  certificate, and no new reduction edge or open leaf is created, so
  `docs/current-frontier.md` is not edited.
