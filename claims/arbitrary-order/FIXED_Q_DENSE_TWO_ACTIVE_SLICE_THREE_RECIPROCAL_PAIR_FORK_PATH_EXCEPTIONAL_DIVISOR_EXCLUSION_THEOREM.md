# Three-pair fork-path exceptional-divisor exclusion

## Status

**Exact characteristic-zero pointwise closure of GLD50 orbit `O4`.**  Two
surface certificates reduce its exceptional union to the surface intersection,
and a third exact curve certificate closes that intersection.  Together with
GLD50, all `24` labelled fork-path support masks are empty.

GLD51--GLD52 already close the directed-path and out-star orbits.  Ten GLD50
orbitwise exceptional unions remain open, as do four-or-more-pair supports,
proper-secondary cells, and every permanent bridge.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Dependency:

- [`GLD50`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md)

## Exceptional cover

For canonical support `(0,1),(0,2),(1,3)` with amplitudes `u,v,w`, GLD50
leaves

```text
(u+1)(uw+vw+v+w+1)=0.                               (1)
```

On `u=-1`, a fourteen-row multiplier over `Q(v,w)` leaves `1` with
denominator

```text
vw(v-1)(vw+v+1).                                     (2)
```

The first three factors are forbidden by active support; the last factor is
exactly the intersection with the second surface.

On the second surface, write

```text
v = -(uw+w+1)/(w+1),                                 (3)
```

so its reciprocal amplitude is `(uw+w+1)/(uw+2w+2)`.  A second fourteen-row
certificate over `Q(u,w)` has denominator

```text
uw(u+1)(uw+w+1)(uw+2w+2).                            (4)
```

Apart from `u+1`, every factor is forbidden by active support and the
parametrization.  Thus (2)--(4) leave only the common curve

```text
u=-1,       v=-1/(w+1).                              (5)
```

On (5), active support requires `w!=0,1,-1,-2`.  A thirteen-row exact
multiplier over `Q(w)` cancels all `81` variables and leaves `1`, with
denominator lcm

```text
w(w+2),                                               (6)
```

whose roots are forbidden.

### Theorem

Both surfaces in (1), including their intersection, are empty.  Therefore
the full GLD50 fork-path orbit `O4`, all `24` masks, is pointwise empty.
`square`

## Scope ledger

```text
GLD50 orbit O4 exceptional union:                     EMPTY;
three-pair fork-path orbit, all 24 masks:             EMPTY;
other ten GLD50 exceptional unions:                    OPEN;
four-or-more reciprocal pairs:                        OPEN;
proper-secondary cells:                               OPEN;
every permanent bridge:                               OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_fork_path_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_fork_path_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```

The primary enumerates all `945` ten-vertex perfect matchings for each row and
replays the three stored exact multipliers.  The standalone no-import audit
reconstructs recursive permanents and derives all three nullspaces.
