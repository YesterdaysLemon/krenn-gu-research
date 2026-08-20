# Dense two-active-slice chain exceptional-divisor exclusion

## Status

**Exact characteristic-zero pointwise closure of the GLD44 directed-chain
exceptional divisor union.**  Two exact curve certificates close the complete
exceptional locus.  Together with GLD44, the entire directed-chain two-pair
orbit is empty, covering all `24` labelled support masks.

GLD45--GLD48 already close the same-tail, disjoint, reverse, and same-head
orbits.  Consequently all `66` minimal two-reciprocal-pair support masks are
now pointwise empty.  Three-or-more-pair supports, proper-secondary cells, and
every permanent bridge remain open.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Dependency:

- [`GLD44`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_TWO_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md)

## Canonical chain and exceptional cover

Use the canonical directed chain `(0,2),(2,1)`.  Its colour-zero amplitudes
are `u,w`, while the reverse colour-one amplitudes are
`u/(u-1),w/(w-1)`.  Active reciprocal support requires

```text
u,w != 0,1.                                           (1)
```

The GLD44 generic certificate leaves exactly

```text
(u+1)(uw+w+1)=0.                                     (2)
```

## The `u=-1` curve

On the first component, the first reciprocal amplitude is `1/2`; the second
pair remains `w,w/(w-1)`.  A fifteen-row exact multiplier over `Q(w)` cancels
all `81` retained variables and leaves `1`.  Its denominator lcm is

```text
2w^2.                                                 (3)
```

The only root of (3) is already forbidden by active support, so this full
curve is empty.

## The `uw+w+1=0` curve

Write `w=-1/(u+1)`.  The four active amplitudes become

```text
u,  u/(u-1),  -1/(u+1),  1/(u+2).                    (4)
```

Condition (1) gives `u!=0,1,-1,-2`.  A separate seventeen-row multiplier
over `Q(u)` cancels every retained variable and leaves `1`; its denominator
lcm is

```text
2u(u-1)(u+1)(u+2).                                   (5)
```

Every root of (5) is exactly a forbidden parameter value on this component,
so it has no legal point.

### Theorem

Both components of the GLD44 directed-chain exceptional divisor union are
empty.  Hence the full directed-chain two-pair orbit is pointwise empty.
Together with GLD45--GLD48, all `66` two-pair masks are empty.  `square`

## Scope ledger

```text
chain GLD44 exceptional divisor union:                EMPTY;
chain two-pair orbit, all 24 masks:                   EMPTY;
all five two-pair orbits, all 66 masks:               EMPTY;
three-or-more reciprocal pairs:                       OPEN;
proper-secondary cells:                               OPEN;
every permanent bridge:                               OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_chain_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_chain_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_two_reciprocal_pair_generic_exclusion.py
```

The primary enumerates all `945` ten-vertex perfect matchings for each row and
replays both stored exact multipliers.  The standalone no-import audit
reconstructs recursive permanents and derives both nullspaces independently.
