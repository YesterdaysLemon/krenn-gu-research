# Three-pair reverse-disjoint exceptional-divisor exclusion

## Status

**Exact characteristic-zero pointwise closure of GLD50 orbit `O8`.**  Four
surface certificates and two overlap certificates exhaust the exceptional
union left by the generic theorem.  Together with GLD50, all `12` labelled
reverse-disjoint support masks are empty.

GLD51--GLD53 already close the directed-path, out-star, and fork-path orbits.
Nine GLD50 orbitwise exceptional unions remain open, as do four-or-more-pair
supports, proper-secondary cells, and every permanent bridge.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

Dependency:

- [`GLD50`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md)

## Exceptional cover

For canonical support `(0,1),(1,0),(2,3)` with amplitudes `u,v,w`, active
reciprocal support requires

```text
u,v,w != 0,1.
```

GLD50 leaves

```text
(u+1)(w+1)(2w-1)(uv+1)=0.                           (1)
```

The four surface certificates have the following exact denominator lcms:

```text
surface                         rows   denominator lcm
u=-1                              14   2v^2 w(v-1)(w-1)(w+1)(2w-1)
w=-1                              12   4uv(u-1)(u+1)(uv+1)
w=1/2                             14   4uv(u-1)(u+1)(uv+1)
uv=-1, v=-1/u                    11   2uw(u-1)(w-1).                 (2)
```

Each multiplier cancels all `81` retained variables and leaves `1`.  The
last row of (2) has no denominator root in its legal active domain, so the
whole product surface `uv=-1` is empty.  After removing that surface and the
active-forbidden factors, the first three rows leave only

```text
u=-1, w=-1             and             u=-1, w=1/2.                 (3)
```

On the first overlap in (3), a nine-row exact multiplier over `Q(v)` leaves
`1` with denominator lcm

```text
4v(v-1).                                                        (4)
```

On the second overlap, a thirteen-row multiplier over `Q(v)` leaves `1` with
denominator lcm

```text
4v^2(v-1).                                                      (5)
```

The roots of (4)--(5) are precisely active-forbidden values.  Therefore no
legal point remains on any factor of (1).

### Theorem

The full GLD50 reverse-disjoint orbit `O8`, all `12` masks, is pointwise
empty.  `square`

## Scope ledger

```text
GLD50 orbit O8 exceptional union:                     EMPTY;
three-pair reverse-disjoint orbit, all 12 masks:      EMPTY;
other nine GLD50 exceptional unions:                   OPEN;
four-or-more reciprocal pairs:                        OPEN;
proper-secondary cells:                               OPEN;
every permanent bridge:                               OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_reverse_disjoint_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_reverse_disjoint_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```

The primary enumerates all `945` ten-vertex perfect matchings for every stored
row and replays the six exact multipliers.  The standalone no-import audit
reconstructs recursive permanents and independently derives all six
nullspaces.
