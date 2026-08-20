# Dense two-active-slice same-tail exceptional-divisor exclusion

## Status

**Exact characteristic-zero pointwise closure of the GLD44 same-tail
exceptional divisor.**  On the canonical same-tail support take

```text
A^0 = I_4 - E_(0,2) + w E_(0,1),
A^1 = I_4 + (1/2)E_(2,0) + w/(w-1) E_(1,0),
A^2 = I_4,                                             (1)
```

where `w!=0,1`.  No hypothetical witness exists on this curve.  Together
with GLD44, this proves the entire same-tail two-reciprocal-pair orbit empty,
covering all `12` position-labelled support masks.

The other four GLD44 orbitwise exceptional divisor unions remain open, as do
larger supports, proper-secondary cells, and every weighted-permanent bridge.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

Dependency:

- [`GLD44`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_TWO_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md)

## Exceptional-divisor certificate

The GLD44 same-tail generic certificate leaves only `u+1=0`.  The GLD43
reciprocal parametrization then forces the transpose amplitude of `u=-1` to
equal `1/2`, giving exactly (1).

For the twelve complete rows

```text
(1010;0110) (0010;0010) (0100;0100) (0012;0012)
(0002;0002) (0200;0200) (0020;0020) (1001;0000)
(0101;0000) (0011;0000) (0110;0000) (0000;0110),
```

the exact multiplier over `Q(w)` is

```text
(-1/w, 2, 3/2, -(w-2)/(w-1), -1/(w-1),
 -(3w-5)/(2(w-1)), -1, 1, 1, 1, -w/(w-1), -1/w).    (2)
```

It cancels all `81` retained variables and leaves `1`.  Its denominator lcm
is `2w(w-1)`, which is nonzero everywhere on the active reciprocal-pair
stratum.  Thus (2) has no further exceptional point.

### Theorem

The full curve (1) is empty.  With the generic complement proved in GLD44,
every same-tail two-reciprocal-pair support chart is pointwise empty.
`square`

## Scope ledger

```text
same-tail GLD44 exceptional divisor:                  EMPTY;
same-tail two-pair orbit, all 12 masks:               EMPTY;
reverse exceptional divisors:                         OPEN;
same-head exceptional divisors:                       OPEN;
chain exceptional divisors:                           OPEN;
disjoint exceptional divisors:                        OPEN;
three-or-more reciprocal pairs:                       OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_same_tail_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_same_tail_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_two_reciprocal_pair_generic_exclusion.py
```

The primary enumerates all `945` ten-vertex perfect matchings for every
selected row.  The standalone no-import audit reconstructs the same equations
using recursive permanents and derives the left nullspace independently.
