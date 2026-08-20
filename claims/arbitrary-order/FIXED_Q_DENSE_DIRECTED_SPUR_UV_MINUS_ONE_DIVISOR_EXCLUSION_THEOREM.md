# Fixed-Q dense directed-spur `uv=-1` divisor exclusion

## Status

**Exact characteristic-zero pointwise exclusion of one complete exceptional
divisor left by `GLD26`.**  On the directed-spur chart

```text
A^c=I_4+uE_(0,1)+vE_(1,0)+wE_(0,2),    u,v,w!=0,    (1)
```

impose `uv=-1`.  No hypothetical witness lies on this divisor.  Exact
coefficient-row certificates reduce it to a line and a quadratic family and
then close both, including every exceptional point.

This theorem removes one of the four residual divisors of `GLD26`.  The
divisors `uv=1`, `uv-u-v-1=0`, and `uv+vw+w+1=0` remain open, as do broader
cross arrays and the other `GLD21` cells.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

Dependencies:

- [`GLD21`](FIXED_Q_RESPONSE_MAP_ZERO_DEAD_COLOUR_H_GATE_AND_DENSE_COMPANION_ABSORPTION_THEOREM.md)
- [`GLD26`](FIXED_Q_DENSE_DIRECTED_SPUR_GENERIC_CROSS_ARRAY_EXCLUSION_THEOREM.md)

## 1. Complete coefficient rows

Use the canonical dense shore data and colour-diagonal cross-array convention
of `GLD26`.  All `24` root--residual entries, `54` root--root entries, and
three pure target scalars remain independent.  For each port/root word pair
`(omega,rho)`, let

```text
A_(omega,rho)(u,v,w)X=b_(omega,rho)(u,v,w)           (2)
```

be the complete ten-vertex coefficient equation, including all three
exhaustive nonzero matching types.  Set

```text
q(u)=u^2+2u-1.                                        (3)
```

## 2. Divisor detector

Because `u!=0`, substitute `v=-u^(-1)`.  A polynomial-cleared exact
combination of the twelve rows

```text
(0102,0102), (1000,1000), (0100,0100), (0100,1000),
(1000,0100), (1100,0000), (0110,0000), (0001,0001),
(1010,0000), (0101,0000), (0011,0011), (1001,0000)  (4)
```

cancels all `81` variable coefficients and leaves

```text
2uw(u-1)q(u).                                         (5)
```

The exact polynomial multipliers are stored literally in both replay
implementations.  Since `u,w!=0`, only

```text
L: u=1, v=-1,
C: q(u)=0, v=-u-2                                    (6)
```

remain.

## 3. The line `L`

On `u=1`, `v=-1`, a fourteen-row exact relation leaves

```text
2w(w+1)(w+2).                                         (7)
```

It closes the line except `w=-1,-2` (the chart already excludes `w=0`).
At each remaining point a separate twelve-row rational combination cancels
all `81` variables and leaves `1`.  Thus the entire line is empty.

The two point cores use the row/multiplier tables embedded independently in
the primary and audit scripts; both replay as literal `0=1` identities.

## 4. The quadratic family `C`

On `q(u)=0`, division by nonzero `u` gives

```text
v=-u^(-1)=-u-2.                                      (8)
```

Work in `K[u,w]/(q)`.  Use the twelve rows

```text
(0102,0102), (1100,1100), (0100,1000), (1000,0100),
(0100,0100), (0000,1100), (0110,0000), (0001,0001),
(1010,0000), (0101,0000), (0011,0011), (1001,0000)  (9)
```

with respective multipliers

```text
-4w, -4w, -4uw, 4w(u+2), 4w, -4w,
-(u+1)(w+2), -2(u+1),
-uw-2u-3w-2, -2uw, 2(u+1), 2w.                      (10)
```

Exact reduction modulo `q` gives

```text
sum lambda A = 0,
sum lambda b = 4w.                                   (11)
```

Since `w!=0`, (11) closes the quadratic family whether or not `q` splits
over the base field.

### Theorem 1 (`uv=-1` divisor exclusion)

The dense `K_4/K_4`, `h!=0` residue contains no hypothetical witness on the
directed-spur chart (1) with `uv=-1`.

### Proof

Apply (5).  Outside the two loci in (6), it is nonzero.  On `L`, apply (7)
and then the two point cores.  On `C`, apply (11).  These cases exhaust the
zero locus of (5) under `u,w!=0`, so the complete coefficient equations are
inconsistent at every point of the divisor.  `square`

## 5. Exact frontier and scope ledger

```text
GLD26 directed-spur chart:                              INPUT;
exceptional divisor:                                   uv=-1;
divisor detector:                                      2uw(u-1)q(u);
u=1 line:                                              FULLY CLOSED;
q(u)=0 quadratic family:                              FULLY CLOSED;
entire uv=-1 divisor:                                  EMPTY;
remaining GLD26 divisors:                             THREE OPEN;
entire directed-spur chart:                            OPEN;
global Krenn--Gu conjecture:                        UNRESOLVED.
```

Scope:

- **field:** characteristic zero;
- **response hypothesis and normalization:** exactly those of `GLD26`;
- **cross-array subcell:** the full `uv=-1`, `u,v,w!=0` divisor;
- **unrestricted data:** all `78` root-side entries and three pure target
  scalars;
- **excluded object:** one complete codimension-one divisor, not the other
  three exceptional divisors or the whole nonprivate dense cell;
- **permanent implication:** none.

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_directed_spur_uv_minus_one_divisor_exclusion.py
python claims/arbitrary-order/audit_fixed_q_dense_directed_spur_uv_minus_one_divisor_exclusion.py
```

The primary enumerates all `945` ten-vertex perfect matchings directly.  The
audit imports neither the primary nor a project module and instead derives
rows from recursive permanents for the three matching types.  Both use exact
SymPy polynomial/rational arithmetic and independently replay the divisor,
line, point, and quadratic-quotient certificates.  The shared algebra backend
is explicit; independence lies in the row derivation and implementation
route, not in a claim of disjoint arithmetic libraries.
