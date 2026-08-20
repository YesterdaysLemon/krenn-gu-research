# Three-pair out-star exceptional-divisor exclusion

## Status

**Exact characteristic-zero pointwise closure of the GLD50 three-out-star
orbit `O1`.**  Two exact surface certificates close its complete generic
exceptional union.  Together with GLD50, all `4` labelled out-star support
masks are empty.

GLD51 already closes the `24` directed-path masks.  The other eleven GLD50
orbitwise exceptional unions remain open, as do four-or-more-pair supports,
proper-secondary cells, and every permanent bridge.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Dependency:

- [`GLD50`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md)

## Canonical support and exceptional cover

Use the canonical support `(0,1),(0,2),(0,3)`, with colour-zero amplitudes
`u,v,w` and reverse colour-one amplitudes
`u/(u-1),v/(v-1),w/(w-1)`.  GLD50 leaves exactly

```text
(w+1)(v+w+1)=0.                                      (1)
```

## The `w=-1` surface

Here the third reciprocal amplitude is `1/2`, while active support requires
`u,v!=0,1`.  A fifteen-row multiplier over `Q(u,v)` cancels all `81` retained
variables and leaves `1`; its denominator lcm is

```text
2uv(u-1)(v-1).                                       (2)
```

Every root is forbidden by the active domain.

## The `v+w+1=0` surface

Write `v=-w-1`, so `v/(v-1)=(w+1)/(w+2)`.  The legal domain is

```text
u != 0,1,       w != 0,1,-1,-2.                     (3)
```

A separate fourteen-row multiplier over `Q(u,w)` leaves `1` after cancelling
all `81` variables.  Its denominator lcm is

```text
uw(u-1)(w-1)(w+1)(w+2),                             (4)
```

whose roots are exactly forbidden by (3).

### Theorem

Both components of the GLD50 `O1` exceptional union are empty.  Therefore
the full three-pair out-star orbit, all `4` labelled masks, is pointwise
empty.  `square`

## Scope ledger

```text
GLD50 orbit O1 exceptional union:                     EMPTY;
three-pair out-star orbit, all 4 masks:               EMPTY;
other eleven GLD50 exceptional unions:                 OPEN;
four-or-more reciprocal pairs:                        OPEN;
proper-secondary cells:                               OPEN;
every permanent bridge:                               OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_out_star_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_out_star_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```

The primary enumerates all `945` ten-vertex perfect matchings for each row and
replays both stored exact multipliers.  The standalone no-import audit
reconstructs recursive permanents and derives both nullspaces independently.
