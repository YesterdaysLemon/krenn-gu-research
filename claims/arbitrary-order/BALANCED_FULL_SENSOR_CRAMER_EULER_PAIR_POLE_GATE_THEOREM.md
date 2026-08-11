# Balanced full-sensor Cramer--Euler pair-pole gate

## Status

**Exact characteristic-zero refinement of the open balanced full-sensor
branch.**  On a generically full balanced sensor, a maximal minor gives the
unique rational complete-deck candidate by Cramer's rule.  The candidate
comes from one physical nonroot graph exactly when:

1. every unused target row is consistent with that Cramer solution;
2. the empty component is one;
3. every **pair** component is pole-free at every prime divisor; and
4. one symmetric Euler--hafnian recurrence holds for each even vertex set of
   size at least four.

The recurrence family is equivalent to the complete coloured Wick criterion.
Once it holds, all higher deck components are hafnian polynomials in the pair
components, so their separate pole tests are redundant.  This reduces the
regularity part of the open gate from all `2^(m-1)` deck components to the
`binomial(m,2)` physical pair components.

This theorem does **not** prove that a target incidence violates one of these
conditions, exclude the all-balanced rank-drop branch, construct an exact
counterexample, or resolve the original conjecture.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. The unique Cramer candidate and target residuals

Use the notation and hypotheses of the
[`balanced half-sensor theorem`](BALANCED_HALF_SENSOR_COMPLETE_DECK_AND_WICK_GLOBALIZATION_THEOREM.md).
Thus

```text
X=product_(u in N) P(L_u),
E=direct-sum_(I subset N, |I| even) O(1_I),
Gamma_tilde:E -> F,                                  (1)
```

and `Gamma_tilde` has generic column rank

```text
k=2^(m-1).                                           (2)
```

Work at the generic point of `X` in product-compatible frames.  Choose `k`
rows of `Gamma_tilde` whose square matrix `A` has

```text
beta=det(A)!=0.                                      (3)
```

Let `j` be the same rows of the GHZ section `J` and put

```text
v=adj(A)j.                                           (4)
```

The selected rows automatically obey `Av=beta j`.  All target rows are
consistent with this chart exactly when

```text
Gamma_tilde v=beta J.                                (5)
```

When (5) holds, the unique rational lift is

```text
C_I=v_I/beta.                                        (6)
```

If `beta'` and `v'` come from another nonzero maximal minor, generic
injectivity and (5) give

```text
beta' v=beta v'.                                     (7)
```

Thus the formulas agree as rational sections.  Equation (7) is overlap
compatibility, not a pole-removal statement.  The affine normalization is
the separate identity

```text
v_empty=beta.                                        (8)
```

No unselected row condition, normalization, or regularity conclusion is
hidden in Cramer's rule.

## 2. A single Euler identity for the complete Wick gate

For an even rational deck `C=(C_I)` with `C_empty=1`, form the square-free
vertex-graded moment element

```text
M_C=sum_(I subset N, |I| even) C_I x_I,              (9)
```

where products with a repeated vertex vanish and products on disjoint
supports use the natural tensor product.  Put

```text
Q_C=sum_({u,v} subset N) C_uv x_u x_v,               (10)
```

and let `D` be the Euler derivation that multiplies a component supported on
`I` by `|I|`.

### Theorem 1 (Euler--Wick equivalence)

Over characteristic zero, the following conditions are equivalent.

1. `log(M_C)` has only vertex-degree two.
2. `M_C=exp(Q_C)`, so `C` is the complete principal hafnian deck of the
   unique pair family `W_uv=C_uv`.
3. The square-free Euler identity holds:

   ```text
   D M_C=2 Q_C M_C.                                  (11)
   ```

4. For every even `Q subset N` with `|Q|=2s>=4`,

   ```text
   s C_Q=sum_(e subset Q, |e|=2) C_e C_(Q-e).        (12)
   ```

Here the sum in (12) is over unordered pairs.  In particular, a perfect
matching of `Q` occurs once for each of its `s` edges on the right.

### Proof

The finite square-free exponential and logarithm are inverse in
characteristic zero.  Hence conditions 1 and 2 are equivalent by the block-
square-zero Wick completion theorem.  Differentiating `exp(Q_C)` by `D` and
using `D Q_C=2Q_C` proves (11).  Conversely, compare homogeneous vertex
degrees in (11).  Its degree-`2s` component is exactly twice (12).  Starting
with `C_empty=1` and the fixed degree-two part, induction on `s` determines
each higher component uniquely because `s` is nonzero.  The exponential has
the same degree-two part and satisfies the same recurrence, so it is that
unique solution.  This proves all four equivalences.

Equivalently, the induction can be read directly in matching language.
Assume every proper even subdeck is already hafnian.  The right side of (12)
then contains each perfect matching of `Q` exactly `s` times.  Division by
`s` gives `C_Q=haf((C_e)_(e subset Q))`.

## 3. Higher poles reduce exactly to pair poles

### Theorem 2 (pair-pole criterion)

Suppose a rational deck on `X` has `C_empty=1` and satisfies any of the
equivalent conditions in Theorem 1.  Then

```text
C is a global section of E
iff
every C_uv is a global section of O(1_{u,v}).         (13)
```

Consequently, in the Cramer frame (6), regularity is equivalent to

```text
nu_P(v_uv)>=nu_P(beta)                               (14)
```

for every pair `{u,v}`, every prime divisor `P` of `X`, and a regular local
frame of `O(1_{u,v})` at the generic point of `P`.

### Proof

The forward implication in (13) is projection onto a direct summand of `E`.
For the converse, write `W_uv=C_uv`.  Theorem 1 gives, as rational sections,

```text
C_Q=haf((W_uv)_(u,v in Q))                           (15)
```

for every even `Q`.  If all `W_uv` are global bilinear sections, every term
of (15) is a global section of `O(1_Q)`, and so is their sum.  Thus all
components of `C` are global.  Since `X` is smooth and hence normal, a
rational line-bundle section is global exactly when it has no pole at any
prime divisor.  Applying this only to (6) for pairs gives (14).

In particular, no separate deletion-locality or endpoint-multilinearity test
is needed after (14): membership in
`H^0(X,O(1_{u,v}))=L_u^* tensor L_v^*` is exactly one constant physical
bilinear edge block.  This observation uses the projective bundle type; mere
regularity of an unrelated scalar chart function would not suffice.

## 4. The exact determinant-cleared full-sensor gate

Substitute (6) into (12).  The correct cleared identity is

```text
s beta v_Q
 =sum_(e subset Q, |e|=2) v_e v_(Q-e),
|Q|=2s>=4.                                           (16)
```

There is one power of `beta` on the left, not `beta^2`: every term on the
right originally has denominator `beta^2`, whereas `C_Q` has denominator
`beta`.

### Theorem 3 (Cramer--Euler globalization gate)

For fixed root--root and root--nonroot shore blocks with a generically full
balanced sensor, the shore extends to one ternary block graph satisfying the
original GHZ tensor equality if and only if one (equivalently every) nonzero
maximal-minor Cramer chart satisfies all of the following:

```text
target:         Gamma_tilde v=beta J;                (17a)
normalization:  v_empty=beta;                        (17b)
pair poles:     nu_P(v_e)>=nu_P(beta) for every
                pair e and every prime divisor P;    (17c)
Euler--Wick:    equation (16) for every even
                Q with |Q|>=4.                       (17d)
```

### Proof

An extending graph supplies its global complete hafnian deck, so (17a)--
(17d) follow from the balanced identity, the empty hafnian, regular physical
pair blocks, and Theorem 1.

Conversely, (17a) makes `C=v/beta` the unique rational solution of
`Gamma_tilde C=J`, and (17b) gives `C_empty=1`.  The cleared identities
(17d) and Theorem 1 make `C` the complete rational hafnian deck of its pair
components.  Condition (17c) and Theorem 2 then promote the entire rational
deck to a global section of `E`, with physical pair blocks.  The exact lift
and Wick gate in the balanced half-sensor theorem now adjoins those blocks to
the same fixed shore and gives the original tensor equality.  No pointwise-
to-global or same-graph inference remains.

The gate is chart-independent.  On overlaps (7) identifies the rational
components; (17a), (17b), and (17d) are identities of those rational
sections, while divisorial regularity in (17c) is intrinsic.

## 5. Sharp boundary: cleared Wick does not remove poles

The pair-pole condition cannot be deleted from Theorem 3.  Over a discrete
valuation ring with parameter `t`, take four labels and set

```text
beta=t,             v_empty=t,
v_12=1,             v_34=t^2,
v_1234=t,           every other v_e=0.               (18)
```

Then the only nontrivial cleared recurrence is

```text
2 beta v_1234=v_12 v_34+v_34 v_12=2t^2.             (19)
```

Thus normalization and the complete four-label Euler--Wick equation hold.
The rational deck is indeed the hafnian deck of

```text
C_12=t^(-1),        C_34=t,        C_1234=1,         (20)
```

but `C_12` has a pole.  This is a counterexample only to the false inference
"determinant-cleared Wick identities imply regularity."  It is not asserted
to arise from a balanced target incidence and is not a Krenn--Gu
counterexample.

## 6. Proof-topology consequence and exact frontier

The open full-sensor branch now has the exact triangular form

```text
one full balanced sensor
  -> unique Cramer candidate and target residuals;
  -> empty normalization;
  -> prime-divisor tests only on pair components;
  -> one Euler--hafnian recurrence per higher even subset;
  -> same-graph extension iff every gate passes.                     (21)
```

Therefore a proof on this branch must show that every target incidence fails
at least one of (17b)--(17d).  An exact counterexample would have to pass all
of (17a)--(17d) and the independent validation required by the repository
contract.  At present no universal failure and no passing counterexample is
known.

The all-balanced identically-rank-deficient branch is untouched.  Detection,
fixed-root injectivity, witness exclusion, and globalization remain distinct
claims; this theorem concerns the exact globalization gate only.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_full_sensor_cramer_euler_pair_pole_gate.py
python claims/arbitrary-order/audit_balanced_full_sensor_cramer_euler_pair_pole_gate.py
python -m py_compile claims/arbitrary-order/verify_balanced_full_sensor_cramer_euler_pair_pole_gate.py claims/arbitrary-order/audit_balanced_full_sensor_cramer_euler_pair_pole_gate.py
uv run --with ruff ruff check claims/arbitrary-order/verify_balanced_full_sensor_cramer_euler_pair_pole_gate.py claims/arbitrary-order/audit_balanced_full_sensor_cramer_euler_pair_pole_gate.py
```

The primary check uses generic SymPy Cramer charts and generic four- and six-
label hafnians to verify target residuals, overlap uniqueness, the Euler
count, the single-denominator clearing, pair-regularity propagation, and the
pole counterexample.  The independent no-import audit uses exact `Fraction`
row arithmetic, a separately written recursive hafnian through eight labels,
and a tiny Laurent-polynomial implementation.  These are focused convention
and falsification checks.  The arbitrary-order proofs are the Cramer,
matching-count, induction, and normality arguments above.
