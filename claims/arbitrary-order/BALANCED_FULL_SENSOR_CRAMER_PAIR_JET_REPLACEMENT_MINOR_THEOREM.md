# Balanced full-sensor Cramer pair-jet replacement-minor theorem

## Status

**Exact algebraic refinement of the open balanced full-sensor gate.**  On a
nonzero Cramer chart, every determinant-cleared first or second derivative of
the rational complete-deck candidate can be computed without differentiating
the determinant or adjugate.  Each coordinate of the cleared jet is one
column-replacement determinant of the selected sensor minor.

When all target rows are retained, all target residuals vanish, and the full
sensor has function-field column rank `k`, a pair jet vanishes exactly when a
named differentiated target residual lies in the span of all sensor columns
except that pair column.  Thus the finite differential-flatness gate of
[`BALANCED_FULL_SENSOR_CRAMER_PAIR_POLE_DIFFERENTIAL_FLATNESS_THEOREM.md`](BALANCED_FULL_SENSOR_CRAMER_PAIR_POLE_DIFFERENTIAL_FLATNESS_THEOREM.md)
has an equivalent target-facing column-span form.

This theorem does **not** prove that a balanced target incidence passes or
fails any span condition.  The abstract sharp controls below are Cramer
systems but are not realized balanced sensors with the GHZ target.  The
all-balanced rank-drop branch is unchanged, and the global Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. Selected Cramer system and cleared jets

Let `R` be an integral commutative differential algebra, let `F=Frac(R)`, and
let `D,E` be commuting derivations of `R`.  The intended application takes
`R` to be a polynomial coordinate ring and `D,E` to be affine-cone coordinate
partials.  The identities in this section do not require characteristic zero;
characteristic zero remains load-bearing in the downstream differential-
flatness theorem.

Let

```text
A in Mat_(k x k)(R),       j in R^k,
beta=det(A)!=0,            v=adj(A)j,
f=v/beta=A^(-1)j in F^k.                              (1)
```

For a vector numerator `v`, define the componentwise first cleared jet

```text
S_D=beta Dv-v Dbeta=beta^2 Df.                       (2)
```

For commuting `D,E`, define the componentwise cleared Hessian

```text
H_DE
 =beta^2 DEv
  -beta((Dv)(Ebeta)+(Ev)(Dbeta)+v DEbeta)
  +2v(Dbeta)(Ebeta)
 =beta^3 DEf.                                        (3)
```

The formula includes `D=E`; the first two middle terms then coincide.

Define the raw selected-row differential residuals

```text
q_D
 =beta Dj-(DA)v,                                     (4)

q_DE
 =beta^2 DEj-beta(DE A)v
  -(DA)S_E-(EA)S_D.                                  (5)
```

Neither (4) nor (5) differentiates `det(A)` or `adj(A)`.  Formula (5) is
recursive only through the first jets, which will themselves be replaced by
(4).

### Theorem 1 (jet transport through one Cramer minor)

The exact polynomial identities

```text
S_D =adj(A)q_D,
H_DE=adj(A)q_DE                                      (6)
```

hold.  If `A[e <- q]` denotes `A` with column `e` replaced by `q`, then every
deck coordinate satisfies

```text
(S_D)_e =det(A[e <- q_D]),
(H_DE)_e=det(A[e <- q_DE]).                          (7)
```

### Proof

Differentiate `Af=j` once:

```text
A Df=Dj-(DA)f.
```

Multiplication by `beta^2` and use of `v=beta f` gives

```text
A S_D=beta[beta Dj-(DA)v]=beta q_D.                  (8)
```

Multiplying by `adj(A)` and cancelling the nonzero element `beta` in the
domain gives the first identity in (6).

Differentiate `Af=j` successively by `D,E`:

```text
A DEf
 =DEj-(DE A)f-(DA)Ef-(EA)Df.                        (9)
```

Multiplication by `beta^3` gives

```text
A H_DE=beta q_DE.                                   (10)
```

The same adjugate argument proves the second identity in (6).  Finally,
Cramer's column-replacement formula says

```text
(adj(A)q)_e=det(A[e <- q]),                          (11)
```

which proves (7).

Substituting the first identity of (6) into (5) makes the Hessian residual
entirely explicit in the raw selected system:

```text
q_DE
 =beta^2 DEj-beta(DE A)v
  -(DA)adj(A)q_E-(EA)adj(A)q_D.                     (12)
```

## 2. All target rows and residual covariance

Return to the full balanced sensor notation.  Let

```text
Gamma in Mat_(r x k)(R),       J in R^r              (13)
```

contain every target row, and keep the selected Cramer data `(A,j,beta,v)`
from (1).  Define the determinant-cleared target residual

```text
T=Gamma v-beta J.                                   (14)
```

For the full row set define

```text
Q_D
 =beta DJ-(D Gamma)v,                               (15)

Q_DE
 =beta^2 DEJ-beta(DE Gamma)v
  -(D Gamma)S_E-(E Gamma)S_D.                       (16)
```

For any vector numerator `u`, write

```text
mathcalS_D(beta,u)=beta Du-u Dbeta,

mathcalH_DE(beta,u)
 =beta^2 DEu
  -beta((Du)(Ebeta)+(Eu)(Dbeta)+u DEbeta)
  +2u(Dbeta)(Ebeta),                                (17)
```

componentwise.

### Theorem 2 (exact target-residual transport)

Without assuming target consistency,

```text
Gamma S_D-beta Q_D
 =mathcalS_D(beta,T),                                (18)

Gamma H_DE-beta Q_DE
 =mathcalH_DE(beta,T).                              (19)
```

In particular, if every target row is consistent,

```text
T=0,                                                (20)
```

then

```text
Gamma S_D =beta Q_D,
Gamma H_DE=beta Q_DE.                               (21)
```

### Proof

In the fraction field, put

```text
t=Gamma f-J=T/beta.                                 (22)
```

The quotient rule gives

```text
beta^2 Dt =mathcalS_D(beta,T),
beta^3 DEt=mathcalH_DE(beta,T).                     (23)
```

Expanding the left sides using `f=v/beta`, (2), and (3) gives respectively
the left sides of (18) and (19).  All terms lie in `R`, so the resulting
identities are polynomial identities.  Setting `T=0` proves (21).

The residual terms in (18)--(19) are load-bearing when unselected target rows
have not yet been imposed.  Dropping them would silently assume target
consistency.

## 3. Target-column-span form of pair differential flatness

Assume now that `Gamma` has full column rank over `F` and that (20) holds.
Write `Gamma_e` for the deck column indexed by `e` and `Gamma_hat(e)` for the
matrix with that column deleted.  The lowercase residuals `q_D,q_DE` are the
restrictions of `Q_D,Q_DE` to the rows selected for `A`.

### Theorem 3 (one pair coordinate as a column-span test)

For every derivation `D` and deck coordinate `e`, the following are
equivalent:

```text
(S_D)_e=0;
Q_D lies in span_F{Gamma_I : I!=e};
rank_F[Gamma_hat(e) | Q_D]=k-1;
det(A[e <- q_D])=0.                                 (24)
```

For every commuting `D,E`, the analogous conditions

```text
(H_DE)_e=0;
Q_DE lies in span_F{Gamma_I : I!=e};
rank_F[Gamma_hat(e) | Q_DE]=k-1;
det(A[e <- q_DE])=0                                 (25)
```

are equivalent.

### Proof

The columns of `Gamma` are independent, so the `k-1` columns of
`Gamma_hat(e)` are independent.  Equation (21) writes `beta Q_D` uniquely as
the column combination with coefficient vector `S_D`.  Its `e` coefficient
vanishes exactly when `Q_D` is in the span of the other columns, which is
equivalent to the rank equality in (24).  The selected-row determinant is
equivalent by (7).  The Hessian statement is identical with `H_DE,Q_DE` in
place of `S_D,Q_D`.

The rank in (24)--(25) is a function-field column rank.  It is not a bounded
point evaluation, and the condition for one pair coordinate does not say
that the entire residual vector `Q_D` or `Q_DE` vanishes.

The span form is also Cramer-chart invariant.  If two target-consistent
charts represent the same rational deck by

```text
(beta',v')=(g beta,g v),        g in F^*,             (26)
```

then direct substitution gives

```text
Q'_D=g Q_D,             Q'_DE=g^2 Q_DE.              (27)
```

Multiplication by a nonzero function-field scalar does not change membership
in `span_F Gamma_hat(e)`.  This agrees with the already proved covariance
`S'_D=g^2 S_D`, `H'_DE=g^3 H_DE`.

## 4. Exact finite target-facing gate

Fix a nonroot pair `e={p,q}`.  Apply Theorem 3 as follows.

1. For every cone-coordinate derivative `D=partial_(w,a)` with
   `w notin {p,q}`, impose one of the equivalent first-jet tests (24).
2. For `r=p,q` and every `0<=a<=b<d_r`, impose (25) with
   `D=partial_(r,a)` and `E=partial_(r,b)`.

By the pair-pole differential-flatness theorem, these conditions are
equivalent to prime-divisor regularity of the Cramer pair component.  In the
ternary application they are the same `3m+6` identities per pair, not a new
or additional layer.

The mixed endpoint replacement minor also reconstructs the physical block.
When the flatness identities hold,

```text
det(A[e <- q_(partial_(p,a),partial_(q,b))])
 =beta^3 (W_pq)_(a,b).                              (28)
```

Thus all nine ternary block entries are available from raw sensor and target
derivatives without differentiating `det(A)` or `adj(A)`.

This is an elimination-facing reduction.  On one selected chart a single
replacement determinant tests each jet.  With all rows retained, the same
condition is the intrinsic target-column-span test in (24)--(25).

## 5. Sharp boundary: Cramer consistency alone selects no outcome

The identities `Av=beta j` and `Af=j` are automatic on the selected Cramer
rows, so they cannot by themselves force a replacement minor to vanish or be
nonzero.  For example, over a polynomial ring in endpoint variables `x,y`
and an outside group `r`, take

```text
A=diag(r_1,1),       j=(r_0 x_0 y_0,0)^T.            (29)
```

Then

```text
beta=r_1,
f=((r_0/r_1)x_0y_0,0)^T.                            (30)
```

The first component has the correct ambient pair multidegree, passes every
endpoint Hessian, and has the nonzero transverse replacement minor

```text
det(A[first <- q_(partial r_0)])=r_1 x_0y_0.         (31)
```

Replacing (29) by

```text
A=diag(x_1,1),       j=(x_0^2 y_0,0)^T              (32)
```

gives the endpoint-pole control with every transverse replacement minor zero
and

```text
det(A[first <- q_(partial x_0,partial x_0)])
 =2x_1^2y_0.                                        (33)
```

These controls show that abstract Cramer consistency does not choose a side
of the pair gate.  They do **not** construct the balanced complete-deck sensor
or the fixed GHZ target `J`; hence they are not balanced target incidences,
graph witnesses, or counterexamples.

## 6. Proof-topology consequence and residual obligation

The verified full-sensor route now has the exact target-facing form

```text
target residuals T=0;
empty normalization;
for every pair e:
  outside Q_D belongs to span Gamma_hat(e);
  endpoint Q_DE belongs to span Gamma_hat(e);
higher Euler--hafnian recurrences.                   (34)
```

Every span condition may instead be checked by one selected-row column-
replacement determinant.  The next unresolved S2 obligation is target-
specific: prove that every balanced target-consistent full sensor violates
normalization, one of these span conditions, or a higher recurrence.  No such
universal violation is proved here.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_full_sensor_cramer_pair_jet_replacement_minor.py
python claims/arbitrary-order/audit_balanced_full_sensor_cramer_pair_jet_replacement_minor.py
python -m py_compile claims/arbitrary-order/verify_balanced_full_sensor_cramer_pair_jet_replacement_minor.py claims/arbitrary-order/audit_balanced_full_sensor_cramer_pair_jet_replacement_minor.py
uv run --with ruff ruff check claims/arbitrary-order/verify_balanced_full_sensor_cramer_pair_jet_replacement_minor.py claims/arbitrary-order/audit_balanced_full_sensor_cramer_pair_jet_replacement_minor.py
```

The primary verifier uses SymPy on a nonconstant `3 x 3` Cramer system.  It
checks every first and symmetric/mixed second direction, every replacement
minor, selected-row restriction inside a tall target-consistent sensor, exact
inconsistent-row residual covariance (including a residual equal to `1` and
not divisible by `beta`), tall column-span pass/fail controls, and both sharp
systems.  The independent audit imports no symbolic or repository code; it
uses a separately written sparse bivariate polynomial ring and determinant
implementation on a different exact system.  These scripts replay displayed
identities and conventions.  The arbitrary-system proof is the
differentiation and adjugate argument above.
