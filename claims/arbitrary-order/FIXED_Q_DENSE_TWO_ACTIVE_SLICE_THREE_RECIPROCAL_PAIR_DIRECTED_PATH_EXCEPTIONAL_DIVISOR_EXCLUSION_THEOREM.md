# Dense two-active-slice three-pair directed-path exceptional-divisor exclusion

## Status

**Exact characteristic-zero pointwise closure of the GLD50 directed-path
orbit `O10`.**  A fourteen-row exact surface certificate closes the sole
generic exceptional component.  Together with GLD50, the entire directed
length-three path orbit is empty, covering all `24` labelled support masks.

The other twelve GLD50 orbitwise exceptional unions remain open, as do
four-or-more-pair supports, proper-secondary cells, and every permanent
bridge.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

Dependency:

- [`GLD50`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md)

## The exceptional surface

Use the canonical path support `(0,1),(1,2),(2,3)`, with colour-zero
amplitudes `u,v,w` and reverse colour-one amplitudes
`u/(u-1),v/(v-1),w/(w-1)`.  GLD50 excludes the complement of

```text
uv+v+1=0.                                             (1)
```

Write

```text
v = -1/(u+1).                                         (2)
```

The six active amplitudes are then

```text
u, u/(u-1), -1/(u+1), 1/(u+2), w, w/(w-1),           (3)
```

so legal active reciprocal support requires

```text
u != 0,1,-1,-2,       w != 0,1.                      (4)
```

A fourteen-row exact multiplier over `Q(u,w)` cancels all `81` retained
nuisance variables and leaves `1`.  Its denominator lcm is

```text
uw(u-1).                                              (5)
```

Every root of (5) is already forbidden by (4).  Hence the whole legal
surface (1) is empty.

### Theorem

The full GLD50 `O10` exceptional surface is empty.  Therefore the entire
three-pair directed length-three path orbit, all `24` labelled masks, is
pointwise empty.  `square`

## Scope ledger

```text
GLD50 orbit O10 exceptional surface:                  EMPTY;
directed-path three-pair orbit, all 24 masks:         EMPTY;
other twelve GLD50 exceptional unions:                 OPEN;
four-or-more reciprocal pairs:                        OPEN;
proper-secondary cells:                               OPEN;
every permanent bridge:                               OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_directed_path_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_directed_path_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```

The primary enumerates all `945` ten-vertex perfect matchings for each row and
replays the stored exact multiplier.  The standalone no-import audit
reconstructs recursive permanents and derives the nullspace independently.
