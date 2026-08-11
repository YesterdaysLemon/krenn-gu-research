# Hostile review of the balanced Cramer--Euler pair-pole gate

## Verdict and provenance

This record reviews
[`BALANCED_FULL_SENSOR_CRAMER_EULER_PAIR_POLE_GATE_THEOREM.md`](../../claims/arbitrary-order/BALANCED_FULL_SENSOR_CRAMER_EULER_PAIR_POLE_GATE_THEOREM.md)
as an exact characteristic-zero refinement of the balanced full-sensor
branch.

Review verdict: **accept the Cramer target-residual formulation, the
Euler--Wick equivalence, and the reduction of full-deck regularity to pair
regularity**, after the focused scripts and publication floor pass.  The
accepted conclusion is an exact gate, not failure of that gate.

This review does not accept a universal pole, normalization, or Wick
obstruction; exclusion of the all-balanced rank-drop branch; a Krenn--Gu
counterexample; or global resolution.  The global conjecture remains
**UNRESOLVED**.

Codex reconstructed the argument directly from the balanced complete-deck
bundle map and the block-square-zero Wick theorem.  This is durable
adversarial reasoning, not independent human review.  The primary script and
independent no-import audit are exact bounded stress checks; the written
Cramer, matching, induction, and normality arguments carry the arbitrary-
order proof.

## 1. Imported obligation and quantifiers

The reviewed theorem assumes one balanced partition `R|N`, `|R|=|N|=m`, for
which the bundle map

```text
Gamma_tilde:E -> F,
E=direct-sum_(I even) O(1_I)                         (1)
```

has generic column rank `k=2^(m-1)`.  It fixes the root--root and root--
nonroot shore defining (1).  It does not assert that a target incidence
exists, that every balanced partition is full, or that the complementary
all-rank-drop branch is empty on the witness locus.

The conclusion is same-shore and same-graph: passing the gate reconstructs
the nonroot pair blocks and adjoins them to the fixed shore.  It is not a
pointwise detector, injectivity, or local-to-global gluing claim imported from
the projectively constant permanent lane.

## 2. Cramer reconstruction and unused target rows

Choose `k` target rows whose square sensor matrix is `A`, write

```text
beta=det(A),        v=adj(A)j.                       (2)
```

Then `Av=beta j` is automatic.  It says nothing about an unused row.  The
full target condition is exactly

```text
Gamma_tilde v=beta J.                               (3)
```

On (3), generic injectivity makes `v/beta` the unique rational solution.
For a second chart `(beta',v')`, uniqueness gives

```text
beta'v=beta v'.                                     (4)
```

Equation (4) proves equality of rational sections on overlaps.  It does not
prove that either numerator is divisible by its determinant at a rank-drop
divisor.  The theorem keeps target residuals, overlap compatibility,
normalization `v_empty=beta`, and divisorial regularity as separate claims.

The primary check reconstructs this distinction on a generic `3 x 2` matrix:
the unused-row residual is the signed augmented determinant, while two
consistent maximal-minor charts cross-multiply exactly.  The independent
audit repeats the calculation with unrelated rational data and deliberately
perturbs the unused target row.

## 3. The symmetric recurrence really is the full Wick gate

Let `D` count vertex degree in the square-free coloured moment algebra and
let `Q_C` be its degree-two part.  A genuine hafnian deck satisfies

```text
D M_C=2 Q_C M_C.                                    (5)
```

For `|Q|=2s`, coefficient extraction gives

```text
s C_Q=sum_(e subset Q, |e|=2) C_e C_(Q-e).           (6)
```

The sum is over every unordered pair `e`.  For four labels, both `e` and its
complement occur, so each perfect matching occurs twice.  More generally,
each matching occurs once for each of its `s` edges.  This multiplicity is
the reason for the factor `s`; replacing the symmetric sum by an unqualified
fixed-vertex recurrence would change the displayed equation.

Necessity is the matching count.  Sufficiency is induction: once every
proper even component is the hafnian of the pair family, the right side of
(6) is `s` times the hafnian on `Q`; characteristic zero permits division by
`s`.  Thus one symmetric recurrence for each higher even subset reconstructs
the full complete hafnian deck.  Finite square-free exponential and logarithm
then identify this condition with the existing all-colour Wick criterion.

No scalar-colour specialization is used.  For disjoint supports, both sides
of (6) lie in the same tensor product `tensor_(u in Q)L_u^*`; coefficientwise
evaluation in local bases recovers the coloured square-free algebra.  The
proof therefore preserves endpoint labels and tensor types.

## 4. Denominator clearing and the power of beta

Substituting `C_I=v_I/beta` into (6) gives

```text
s beta v_Q=sum_(e subset Q) v_e v_(Q-e).             (7)
```

There is exactly one `beta` on the left.  Multiplying the original equation
by `beta^2` produces (7); writing `beta^2 v_Q` would add an unsupported
factor.  The generic four-label primary check retains the resulting identity

```text
2 beta v_0123
 =2(v_01 v_23+v_02 v_13+v_03 v_12).                 (8)
```

The recurrence is triangular by support size but not a pole theorem.  It can
force divisibilities after the pair numerators already contain `beta`; it
cannot supply that initial pair divisibility.

## 5. Why pair poles are necessary and sufficient

Assume the rational deck satisfies the recurrence and is normalized.  Put
`W_uv=C_uv`.  The induction above gives

```text
C_Q=haf((W_uv)_(u,v in Q))                           (9)
```

as a rational section for every even `Q`.  If each `W_uv` is a global section
of `O(1_{u,v})`, every product in (9) is a global section of `O(1_Q)`, so all
higher components are automatically global.  Conversely, a global section
of the direct sum `E` has global pair projections.  This proves the exact
pair-only criterion; no cancellation or genericity claim is being used.

The physical-edge conclusion depends on the bundle type:

```text
H^0(X,O(1_{u,v}))=L_u^* tensor L_v^*.                (10)
```

Regularity of an arbitrary scalar chart expression would not imply one
constant bilinear block.  Here (10) is part of the imported projective setup.
Because `X` is smooth and normal, a rational section of this line bundle is
global exactly when it has nonnegative valuation in a regular local frame at
every prime divisor.  Codimension-at-least-two holes introduce no additional
test.

## 6. Sharp pole counterexample

At a discrete valuation with parameter `t`, the chart

```text
beta=t,   v_empty=t,   v_12=1,
v_34=t^2, v_1234=t                                    (11)
```

obeys normalization and (8), but gives

```text
C_12=t^(-1), C_34=t, C_1234=1.                       (12)
```

Thus it is an exact rational hafnian deck with a pair pole.  The independent
audit implements a separate Laurent-polynomial ring and records valuations
`(-1,1,0)` for (12).  This falsifies only the tempting inference that cleared
Wick equations remove poles.  The chart is not claimed to satisfy a balanced
target incidence and is not a graph counterexample.

## 7. Computational independence and replay meaning

The SymPy primary check verifies:

- generic Cramer target residuals and two-chart overlap;
- the symmetric matching count on every even subset through six labels;
- `D exp(Q)=2Q exp(Q)` in the six-vertex square-free quotient;
- the exact denominator power in (7);
- propagation of a common pair factor to the higher deck; and
- the retained Laurent pole example.

The independent audit imports no repository module and no computer algebra.
It uses exact `Fraction` arithmetic, a separately written recursive hafnian
on every even subset through eight labels, hand-written two-by-two Cramer
formulas, and its own Laurent-polynomial operations.  Agreement therefore
does not come from importing the primary implementation.

Neither finite replay proves the arbitrary-order equivalence or the
prime-divisor extension theorem.  The written matching induction and
normality proof do.

## 8. Acceptance and residual boundary

Accepted after publication gates:

- unused target rows are exactly the Cramer residuals (3);
- the all-colour Wick gate is exactly the recurrence family (6);
- the cleared recurrence has the denominator pattern (7);
- after Wick holds, full-deck regularity is equivalent to pair regularity;
  and
- conditions (3), normalization, pair regularity, and (7) are jointly
  necessary and sufficient for same-shore graph extension.

Explicitly **UNKNOWN**:

- whether every target incidence fails normalization, a pair-pole test, or a
  higher recurrence;
- whether any target incidence passes the entire gate;
- whether the all-balanced rank-drop branch contains a hypothetical witness;
- any global proof or exact counterexample; and
- any Lean formalization of this theorem.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Strongest fresh-referee objection

A fresh referee should first challenge the sufficiency of the *symmetric*
recurrence rather than silently replacing it by the usual fixed-vertex
hafnian expansion.  The required response is the support-size induction and
the exact `s`-fold matching count.  The referee should then transport two
Cramer charts into regular local line-bundle frames at a rank-drop divisor
and verify that cross-multiplication proves only rational equality.  The
four-label Laurent chart (11)--(12) must remain as a regression test against
any claim that the cleared equations themselves remove the pair poles.
