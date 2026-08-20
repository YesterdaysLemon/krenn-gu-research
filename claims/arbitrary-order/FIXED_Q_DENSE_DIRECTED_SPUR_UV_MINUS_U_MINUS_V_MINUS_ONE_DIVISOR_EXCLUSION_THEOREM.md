# Fixed-Q dense directed-spur `uv-u-v-1=0` divisor exclusion

## Status

**Exact characteristic-zero pointwise exclusion of one complete exceptional
divisor left by `GLD26`.**  On the directed-spur chart

```text
A^c=I_4+uE_(0,1)+vE_(1,0)+wE_(0,2),    u,v,w!=0,    (1)
```

impose `uv-u-v-1=0`.  No hypothetical witness lies on this divisor.  Exact
coefficient-row certificates reduce it to five curves; `GLD28` closes their
`u^2+1` residuals, and new quotient certificates close the remaining
quadratic cylinder.

Together with `GLD27` and `GLD28`, this removes three of the four residual
divisors of `GLD26`.  Only `uv+vw+w+1=0` remains open on this chart, as do
broader cross arrays and the other `GLD21` cells.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD26`](FIXED_Q_DENSE_DIRECTED_SPUR_GENERIC_CROSS_ARRAY_EXCLUSION_THEOREM.md)
- [`GLD28`](FIXED_Q_DENSE_DIRECTED_SPUR_UV_ONE_DIVISOR_EXCLUSION_THEOREM.md)

## 1. Complete coefficient rows and legal parametrization

Use the canonical dense shore data and colour-diagonal cross-array convention
of `GLD26`.  All `24` root--residual entries, `54` root--root entries, and
three pure target scalars remain independent.  For every port/root word pair
`(omega,rho)`, let

```text
A_(omega,rho)(u,v,w)X=b_(omega,rho)(u,v,w)           (2)
```

be the complete ten-vertex coefficient equation, including all three
exhaustive nonzero matching types.

On the divisor, `u=1` would give `-2=0`, so `u!=1` and

```text
v=(u+1)/(u-1).                                       (3)
```

The chart conditions add `u!=0,-1`; the second exclusion follows because
`u=-1` makes `v=0` in (3).

Set

```text
q_a=u^2+1,
q_1=u^2+2u-1,
q_b=u^2-2u-1,
q_2=u^2+2uw+2u-1.                                   (4)
```

## 2. Divisor detector and five-curve cover

An exact eighteen-row relation cancels all `81` variable coefficients and
leaves

```text
2u(u+1)^2(u+w)(w+2)(u+w+1)q_1q_2.                  (5)
```

The primary stores every row and multiplier literally; the audit consumes
the same witness table through a separate row derivation.  By (3) and the
chart exclusions, the complete residual locus is

```text
C_1: u+w=0,
C_2: w=-2,
C_3: u+w+1=0,
C_4: q_1=0,
C_5: q_2=0.                                         (6)
```

## 3. Exact curve certificates

Separate exact relations on `C_1,C_2,C_3` leave the same detector

```text
2u(u-1)(u+1)^2 q_a q_1.                             (7)
```

They use `17`, `17`, and `16` rows.  On `C_5`, solve
`w=-q_1/(2u)`, which is legal because `u!=0`.  An eighteen-row relation
leaves

```text
2u(u-1)^2(u+1)^2 q_a q_b q_1.                      (8)
```

Every `q_a=0` residual is already empty by `GLD28`: modulo `q_a`, (3) gives
`v=-u`, hence `uv=-u^2=1`.

Every `q_1=0` residual belongs to the cylinder `C_4` and is handled below.
The only additional factor in (8) is `q_b`.  Modulo `q_b`, one has

```text
q_1=4u,    w=-q_1/(2u)=-2,                          (9)
```

so this branch lies on `C_2`.  There (7) is nonzero: modulo `q_b`,
`q_a=2(u+1)` and `q_1=4u`, while the chart excludes `u=0,-1` and the divisor
excludes `u=1`.  Thus (9) adds no residual case.

## 4. The quadratic cylinder

On `q_1=0`, equation (3) reduces to `v=-u-2`.  Work in
`K[u,w]/(q_1)`.  A fourteen-row exact relation gives

```text
sum lambda A = 0,
sum lambda b = 2w(w+2)(3uw+u+7w+3).                (10)
```

Since `w!=0`, only `w=-2` or `L=3uw+u+7w+3=0` remain.  In the quotient,

```text
(3u+7)^(-1)=(3u-1)/2,
L=(3u+7)(w+u),                                      (11)
```

so the second residual is exactly `w=-u`.

At `w=-u`, a thirteen-row quotient relation cancels all variables and leaves
`4`.  At `w=-2`, a twelve-row quotient relation also leaves `4`.  Every
multiplier is stored literally in the replay scripts.  These constants are
nonzero in characteristic zero, so both residual quadratic point families
are empty.

### Theorem 1 (`uv-u-v-1=0` divisor exclusion)

The dense `K_4/K_4`, `h!=0` residue contains no hypothetical witness on the
directed-spur chart (1) with `uv-u-v-1=0`.

### Proof

Apply (5), which reduces the divisor to (6).  Relations (7) and (8), together
with the proved `GLD28` `uv=1` divisor exclusion and the overlap computation
(9), reduce their union to `C_4`.  The cylinder relation (10) reduces `C_4`
to the two fibres in (11), and their quotient certificates leave `4`.
Therefore every point of the divisor contradicts the complete coefficient
system.  `square`

## 5. Exact frontier and scope ledger

```text
GLD26 directed-spur chart:                              INPUT;
exceptional divisor:                         uv-u-v-1=0;
divisor detector: 2u(u+1)^2(u+w)(w+2)(u+w+1)q_1q_2;
five residual curves:                               EXHAUSTED;
q_a residuals:                          CLOSED BY GLD28;
q_1 quadratic cylinder:                              EMPTY;
entire uv-u-v-1 divisor:                             EMPTY;
remaining GLD26 divisors:                         ONE OPEN;
entire directed-spur chart:                           OPEN;
global Krenn--Gu conjecture:                    UNRESOLVED.
```

Scope:

- **field:** characteristic zero;
- **response hypothesis and normalization:** exactly those of `GLD26`;
- **cross-array subcell:** the full `uv-u-v-1=0`, `u,v,w!=0` divisor;
- **unrestricted data:** all `78` root-side entries and three pure target
  scalars;
- **excluded object:** one complete codimension-one divisor, not the last
  exceptional divisor or the whole nonprivate dense cell;
- **permanent implication:** none.

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_minus_u_minus_v_minus_one_divisor_exclusion.py
python claims/arbitrary-order/audit_fixed_q_dense_directed_spur_uv_minus_u_minus_v_minus_one_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_one_divisor_exclusion.py
```

The primary reconstructs every selected row by directly enumerating all
`945` ten-vertex perfect matchings.  The audit reconstructs the same rows by
recursive permanents for the three exhaustive matching types.  The audit
imports the literal certificate tables from the primary module, so witness
data and SymPy arithmetic are shared; row derivation and implementation route
are separate.  `GLD28` is a stated theorem dependency for the `q_a` branch,
not silently reproduced by these two scripts.
