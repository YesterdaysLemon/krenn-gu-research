# Three-pair in-fork exceptional-divisor exclusion

## Status

**Exact characteristic-zero pointwise closure of GLD50 orbit `O11`.**  Four
surface certificates reduce the generic exceptional union to three
one-parameter intersections, and three further exact certificates close
those curves.  Together with GLD50, all `12` labelled in-fork support masks
are empty.

GLD51--GLD56 already close six three-pair orbits.  Six GLD50 orbitwise
exceptional unions remain open, as do four-or-more-pair supports,
proper-secondary cells, and every permanent bridge.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Dependency:

- [`GLD50`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md)

## Exceptional cover

For canonical support `(0,1),(1,2),(3,1)` with active amplitudes `u,v,w`,
GLD50 leaves

```text
(u+1)(u-w-1)(u+w+1)(uv+v+1)=0.                       (1)
```

The four surface certificates have the following exact denominator lcms:

```text
surface                         rows   denominator lcm
u=-1                              16   2v^3 w^2(w-1)(w+2)
w=u-1                             17   2u^2 v^3(u-2)(u-1)^3(u+1)(uv+v+1)
w=-u-1                            17   4u^2 v^3(u+1)^2(u+2)(uv+v+1)
v=-1/(u+1)                        17   2u w^2(u+1)(w-1)(u-w-1)(u+w+1).   (2)
```

Each normalized multiplier cancels all `81` nuisance variables and leaves
`1`.  Removing active-forbidden factors from (2) leaves exactly three
intersections:

```text
u=-1, w=-2;
w=u-1,  v=-1/(u+1);
w=-u-1, v=-1/(u+1).                               (3)
```

The exact curve cores are:

```text
intersection                      rows   denominator lcm
u=-1, w=-2                          16   8v^3
w=u-1, v=-1/(u+1)                   17   4u^2(u-2)(u-1)^3(u+1)
w=-u-1, v=-1/(u+1)                  17   4u^2(u+1)^2(u+2).             (4)
```

On the first curve `v!=0,1`.  On the second, legality excludes
`u=-2,-1,0,1,2`; on the third it excludes `u=-2,-1,0,1`.  Therefore every
root in (4) is forbidden, and no legal point remains on (1).

### Theorem

The full GLD50 in-fork orbit `O11`, all `12` masks, is pointwise empty.
`square`

## Scope ledger

```text
GLD50 orbit O11 exceptional union:                    EMPTY;
three-pair in-fork orbit, all 12 masks:               EMPTY;
other six GLD50 exceptional unions:                    OPEN;
four-or-more reciprocal pairs:                        OPEN;
proper-secondary cells:                               OPEN;
every permanent bridge:                               OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_fork_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_fork_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```

The primary expands all `945` perfect matchings and derives each normalized
nullspace multiplier from the recorded sparse row core.  The standalone
no-import audit reconstructs recursive permanents and independently derives
the same seven contradiction denominators.
