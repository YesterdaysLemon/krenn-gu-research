# Fixed-Q dense directed-spur `uv=1` divisor exclusion

## Status

**Exact characteristic-zero pointwise exclusion of one complete exceptional
divisor left by `GLD26`.**  On the directed-spur chart

```text
A^c=I_4+uE_(0,1)+vE_(1,0)+wE_(0,2),    u,v,w!=0,    (1)
```

impose `uv=1`.  No hypothetical witness lies on this divisor.  Exact
coefficient-row certificates reduce it to four curves and then close their
four rational residual points and one shared quadratic family.

Together with `GLD27`, this removes two of the four residual divisors of
`GLD26`.  The divisors `uv-u-v-1=0` and `uv+vw+w+1=0` remain open, as do
broader cross arrays and the other `GLD21` cells.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD21`](FIXED_Q_RESPONSE_MAP_ZERO_DEAD_COLOUR_H_GATE_AND_DENSE_COMPANION_ABSORPTION_THEOREM.md)
- [`GLD26`](FIXED_Q_DENSE_DIRECTED_SPUR_GENERIC_CROSS_ARRAY_EXCLUSION_THEOREM.md)

## 1. Complete coefficient rows

Use the canonical dense shore data and colour-diagonal cross-array convention
of `GLD26`.  All `24` root--residual entries, `54` root--root entries, and
three pure target scalars remain independent.  For every port/root word pair
`(omega,rho)`, let

```text
A_(omega,rho)(u,v,w)X=b_(omega,rho)(u,v,w)           (2)
```

be the complete ten-vertex coefficient equation, including all three
exhaustive nonzero matching types.  Since `u!=0`, the divisor equation gives
`v=u^(-1)`.

## 2. Divisor detector and four-curve cover

A polynomial-cleared exact combination of sixteen rows cancels all `81`
variable coefficients and leaves

```text
-4u(u+w)(w+2)(u+w+1)(uw+2u+w).                      (3)
```

The rows, in order, are

```text
(0000,0011), (0011,0011), (0100,0100), (0101,0000),
(0010,0010), (0001,0001), (0002,0002), (0200,0200),
(0020,0020), (0100,1000), (1100,1100), (0000,1100),
(0110,0000), (0110,0110), (0000,0110), (0011,0000). (4)
```

Here and below a pair means `(omega,rho)`.  The primary stores every
multiplier literally, and the audit consumes that same witness table through
its separate row derivation.  Because `u!=0`, (3) reduces the divisor to

```text
C_1: u+w=0,
C_2: w=-2,
C_3: u+w+1=0,
C_4: uw+2u+w=0.                                     (5)
```

## 3. Exact curve certificates

Separate exact left relations on the four curves give the following
detectors.

| curve | substitution | rows | detector |
|---|---|---:|---:|
| `C_1` | `v=1/u, w=-u` | 16 | `4(u+1)` |
| `C_2` | `v=1/u, w=-2` | 16 | `2u(u-1)^2(u+1)` |
| `C_3` | `v=1/u, w=-u-1` | 14 | `4u(u-1)(u^2+1)` |
| `C_4` | `v=1/u, w=-2u/(u+1)` | 15 | `2(u-1)(u^2+1)` |

The substitution on `C_4` is legal: at `u=-1`, its defining polynomial is
`-2`, so every point of `C_4` has `u+1!=0`.

After using `u!=0`, the complete residual set is

```text
P_A=(-1,-1, 1),
P_B=( 1, 1,-2),
P_C=(-1,-1,-2),
P_D=( 1, 1,-1),
Q:  u^2+1=0,  v=-u,  w=-u-1.                        (6)
```

For the quadratic branch of `C_4`, the identity

```text
(u+1)(-u-1)=-2u    modulo u^2+1                     (7)
```

shows that it is exactly the same family `Q` already left by `C_3`.  Thus
(6) is exhaustive, including all curve intersections.

## 4. Rational points and quadratic family

At the four points in (6), exact rational row combinations cancel every one
of the `81` variables and leave, respectively,

```text
P_A: 4,    P_B: 2,    P_C: 4,    P_D: 2.            (8)
```

The point cores use `15`, `12`, `15`, and `13` rows.  Their complete row and
multiplier tables are literal data in the primary and are replayed by the
audit's separate matching-type implementation.

On `Q`, work in `K[u]/(u^2+1)`.  A twelve-row relation uses

```text
(0120,0120), (0020,0020), (0002,0002), (0100,0100),
(0101,0000), (0200,0200), (0100,1000), (1100,1100),
(0000,1100), (0011,0000), (1000,1000), (1100,0000)  (9)
```

with respective multipliers

```text
-2u, u-1, -1, 2u+2, u+1, -3u-1,
1-u, -2, -2, 1, u+3, u-2.                           (10)
```

Exact reduction modulo `u^2+1` gives

```text
sum lambda A = 0,
sum lambda b = 2.                                    (11)
```

The constants `2` and `4` are nonzero in characteristic zero, so (8) and
(11) are contradictions.

### Theorem 1 (`uv=1` divisor exclusion)

The dense `K_4/K_4`, `h!=0` residue contains no hypothetical witness on the
directed-spur chart (1) with `uv=1`.

### Proof

Apply (3).  Outside the four curves (5), it is nonzero.  The four curve
relations reduce their complete union to (6).  The point certificates (8)
close the four rational points, and the quotient-ring certificate (11)
closes `Q`.  The case cover is exhaustive, so the complete coefficient
equations are inconsistent at every point of the divisor.  `square`

## 5. Exact frontier and scope ledger

```text
GLD26 directed-spur chart:                              INPUT;
exceptional divisor:                                     uv=1;
divisor detector:     -4u(u+w)(w+2)(u+w+1)(uw+2u+w);
four residual curves:                              EXHAUSTED;
four rational points:                                  EMPTY;
u^2+1 quadratic family:                                EMPTY;
entire uv=1 divisor:                                   EMPTY;
remaining GLD26 divisors:                           TWO OPEN;
entire directed-spur chart:                             OPEN;
global Krenn--Gu conjecture:                      UNRESOLVED.
```

Scope:

- **field:** characteristic zero;
- **response hypothesis and normalization:** exactly those of `GLD26`;
- **cross-array subcell:** the full `uv=1`, `u,v,w!=0` divisor;
- **unrestricted data:** all `78` root-side entries and three pure target
  scalars;
- **excluded object:** one complete codimension-one divisor, not the other
  two exceptional divisors or the whole nonprivate dense cell;
- **permanent implication:** none.

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_one_divisor_exclusion.py
python claims/arbitrary-order/audit_fixed_q_dense_directed_spur_uv_one_divisor_exclusion.py
```

The primary reconstructs every selected row by directly enumerating all
`945` ten-vertex perfect matchings.  The audit reconstructs the same rows by
recursive permanents for the three exhaustive matching types.  The audit
imports the literal certificate tables from the primary module, so the
witness data and SymPy arithmetic backend are shared; the row derivation and
implementation route are separate.  This is an independent derivation check
of the coefficient system, not a claim of fully disjoint software stacks.
