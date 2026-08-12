# Hostile review of Cramer pair-jet replacement minors

## Verdict and exact scope

This review accepts
[`BALANCED_FULL_SENSOR_CRAMER_PAIR_JET_REPLACEMENT_MINOR_THEOREM.md`](../../claims/arbitrary-order/BALANCED_FULL_SENSOR_CRAMER_PAIR_JET_REPLACEMENT_MINOR_THEOREM.md)
as an exact algebraic refinement of the verified full-sensor pair differential-
flatness gate.

The accepted result has three layers.

1. Every selected-system first or second cleared jet vector is an adjugate
   image of a raw differentiated sensor/target residual.
2. Every individual deck coordinate is exactly one selected-column
   replacement determinant.
3. After all target residuals vanish, one pair coordinate vanishes exactly
   when the corresponding full-row differential residual lies in the span of
   every sensor column except that pair column.

This is a reformulation of the existing finite pair-pole gate, not a proof
that the gate fails.  No balanced target incidence is excluded or constructed.
The all-rank-drop branch and the global conjecture remain open.  The global
Krenn--Gu status remains **UNRESOLVED**.

The primary and audit are different implementations, not independent
mathematical authors.  The written differentiation/adjugate proof carries the
arbitrary-system theorem.

A fresh read-only hostile pass from the disjoint Lumen lane found no P0 or P1
defect.  It independently confirmed the `D=E` doubled term, all target-
residual signs and powers, selected/full-row scope, full-rank requirement, and
chart covariance.  Its P2 abstract-scope correction and P3 tall-composition
hardening were incorporated before publication in both the theorem and both
replays.

## 1. Imported obligations

The theorem uses two verified predecessors.

- The Cramer--Euler gate supplies a generically full complete-deck sensor
  `Gamma`, a selected invertible row minor `A`, the target rows `J,j`, and the
  Cramer data

  ```text
  beta=det(A),       v=adj(A)j,       f=v/beta.
  ```

- The pair differential-flatness theorem proves that the relevant pair
  component is pole-free exactly when its outside first derivatives and both
  endpoint Hessians vanish.

The new theorem does not re-prove either import.  It changes how those finite
jets are expressed.  Target consistency `Gamma v=beta J` remains a separate,
load-bearing hypothesis in the full-row span statement.

## 2. First-jet transport

Differentiating `Af=j` in direction `D` gives

```text
A Df=Dj-(DA)f.
```

The definition `S_D=beta^2 Df` therefore gives

```text
A S_D=beta(beta Dj-(DA)v)=beta q_D.
```

Multiplication by `adj(A)` gives `beta S_D=beta adj(A)q_D`.  Cancellation is
valid because the coefficient ring is a domain and `beta` is nonzero.  Thus

```text
S_D=adj(A)q_D.
```

There is no missing `D beta` term in `q_D`: that term is already absorbed by
the quotient-cleared definition of `S_D`.  Direct expansion of
`beta Dv-v D beta` agrees with the displayed result.

For coordinate `e`, Cramer's formula is

```text
(adj(A)q_D)_e=det(A[e <- q_D]).
```

The determinant has no extra factor of `beta`.  A common incorrect derivation
would solve `A S_D=q_D` rather than `A S_D=beta q_D` and introduce a spurious
denominator; the theorem does not do that.

## 3. Second-jet transport

For commuting derivations `D,E`, the product rule gives exactly four terms:

```text
DE(Af)
 =(DE A)f+(DA)Ef+(EA)Df+A DEf.
```

After multiplication by `beta^3`, the raw second residual is

```text
q_DE
 =beta^2 DEj-beta(DE A)v
  -(DA)S_E-(EA)S_D.
```

Therefore `A H_DE=beta q_DE` and

```text
H_DE=adj(A)q_DE.
```

The formula is symmetric in `D,E`.  When `D=E`, the last two terms coincide,
as required; no factor two is missing.  The coefficient `2` in the direct
quotient Hessian is also retained.  Substitution

```text
S_D=adj(A)q_D
```

removes every derivative of `det(A)` and `adj(A)` from the recursive formula.
It does not remove `adj(A)` itself.

## 4. Full-row target residuals

Let

```text
T=Gamma v-beta J=beta(Gamma f-J).
```

If `T` is not zero, the tempting formulas

```text
Gamma S_D=beta Q_D,
Gamma H_DE=beta Q_DE
```

are false.  The exact correction terms are

```text
Gamma S_D-beta Q_D
 =beta DT-T D beta,

Gamma H_DE-beta Q_DE
 =beta^3 DE(T/beta).
```

The theorem writes the second right side in its fully polynomial cleared-
Hessian form.  These corrections follow by differentiating the residual
section `Gamma f-J`, so their signs and powers are fixed by the quotient rule.
Only after the separately imposed target equation `T=0` do both corrections
vanish.

The primary checks the consistent and inconsistent formulas on five full
rows with nonconstant row combinations.  The audit checks the same theorem
on a different sparse-polynomial system.  Both enumerate the two first and
three symmetric/mixed second directions.  Both also retain a separate
inconsistent row with residual exactly `1`, so the correction formulas are
not tested only when `T` is accidentally divisible by `beta`.

## 5. Column-span and rank equivalence

Assume `Gamma` has full column rank `k` over the function field and `T=0`.
Then `Gamma_hat(e)` has rank `k-1`.  The identity

```text
Gamma S_D=beta Q_D
```

expresses `beta Q_D` in the unique `Gamma` column basis.  Its coefficient on
`Gamma_e` is `(S_D)_e`.  Consequently

```text
(S_D)_e=0
 iff Q_D is in span Gamma_hat(e)
 iff rank[Gamma_hat(e)|Q_D]=k-1.
```

The same proof applies to `H_DE,Q_DE`.  No claim is made that `Q_D` itself is
zero.  No pointwise numerical rank is substituted for the function-field
rank.

Restricting `Q_D` or `Q_DE` to the selected rows gives `q_D` or `q_DE`.
Because `A` is invertible, the single replacement determinant on those rows
is sufficient.  The theorem is not claiming that a random maximal minor of
the full augmented matrix is sufficient; it uses the specific row set whose
sensor submatrix is `A`.

## 6. Chart covariance

On target-consistent chart overlap, suppose

```text
(beta',v')=(g beta,g v),       g!=0.
```

Direct substitution, without differentiating `g`, gives

```text
Q'_D=g Q_D,
Q'_DE=g^2 Q_DE,
```

because the second residual uses the already cleared first jets, which scale
by `g^2`.  Thus membership in the function-field span of
`Gamma_hat(e)` is invariant.  This matches the first- and second-jet scaling
by `g^2` and `g^3`, respectively.

The individual selected-row replacement determinants depend on the chosen
Cramer minor, but their vanishing is chart-independent because each equals
the corresponding cleared jet coordinate.

## 7. Reconstruction and count

For a pair `e={p,q}`, the differential-flatness layer still contains

```text
3(m-2)+6+6=3m+6
```

identities in ternary dimension.  The replacement-minor theorem does not add
conditions; it gives an equivalent representation of each one.  A mixed
endpoint replacement determinant equals

```text
beta^3 (W_pq)_(a,b)
```

after flatness, so all nine physical block entries are reconstructed exactly
as in the predecessor theorem.

## 8. Sharp controls and forbidden inference

The two diagonal `2 x 2` systems in the theorem realize the predecessor's
ambient transverse-pole and endpoint-pole sections as honest abstract Cramer
systems.  They confirm that the tautological selected equation `Af=j` does not
choose whether a replacement minor vanishes.

This does not realize the balanced complete-deck sensor or the prescribed GHZ
target.  In particular:

- an arbitrary diagonal matrix `A` is not shown to be a balanced sensor minor;
- the displayed `j` is not shown to be selected from the GHZ section;
- adding arbitrary extra target rows would not establish target consistency.

The examples therefore prove sharpness only for abstract Cramer-system
algebra.  They are not balanced target incidences or Krenn--Gu witnesses.

## 9. Implementation independence and replay scope

The primary verifier uses SymPy matrices, adjugates, determinants, and
polynomial differentiation.  It checks:

- all six first and nine second selected replacement identities on a
  nonconstant `3 x 3` system;
- all three recursive second residuals;
- selected-row restriction inside consistent tall full-row covariance;
- inconsistent full-row covariance, including a non-`beta`-divisible
  residual;
- every tall column-span/selected-determinant pass/fail control; and
- both abstract Cramer boundary systems.

The independent audit imports neither SymPy nor repository code.  It
implements:

- a sparse multivariate polynomial ring over `Fraction`;
- recursive determinants, cofactors, and adjugates;
- matrix/vector multiplication and formal derivatives;
- a different nonconstant `3 x 3` selected system;
- five consistent and five inconsistent full-row identities with selected-row
  restriction checked explicitly;
- a separate nondivisible residual control; and
- every tall span/selected-determinant control and both boundary minors.

The two implementations share the displayed identities because those are the
objects under review.  They do not share polynomial, matrix, determinant, or
derivative code.  Both are exact specialized family replays; neither bounded
example proves the universal theorem.  The written algebraic proof does.

## Accepted consequence and residual frontier

The S2 pair layer can now be attacked directly in the raw sensor and GHZ
target data:

```text
prove one Q_D or Q_DE escapes span Gamma_hat(e),
```

or equivalently prove one named selected-column replacement determinant is
nonzero.  This is a useful symbolic-elimination interface.

No such universal escape is proved.  Normalization, every pair span test, the
higher Euler--hafnian recurrences, the all-rank-drop branch, and the global
conjecture retain their previous status.  Global status is **UNRESOLVED**.

## Strongest fresh-referee objection

The strongest objection is that the target-facing span statement might be
read without first imposing `T=0`.  That would be false: the exact formulas
contain the cleared derivatives of `T`, and an unselected inconsistent row can
alter `Q_D,Q_DE` without describing a jet of the Cramer candidate.  The theorem
keeps target residuals first in the gate, displays both correction terms, and
uses the span equivalence only under full column rank and `T=0`.
