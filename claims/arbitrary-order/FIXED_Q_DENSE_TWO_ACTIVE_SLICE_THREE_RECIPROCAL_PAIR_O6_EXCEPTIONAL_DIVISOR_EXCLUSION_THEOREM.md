# Three-pair O6 exceptional-divisor exclusion

## Status

**Exact characteristic-zero pointwise closure of GLD50 orbit `O6`.**  Four
surface certificates reduce the generic exceptional union to two
one-parameter intersections, and exact curve certificates close both.
Together with GLD50, all `24` labelled O6 support masks are empty.

GLD51--GLD58 already close eight three-pair orbits.  Four GLD50 orbitwise
exceptional unions remain open, as do four-or-more-pair supports,
proper-secondary cells, and every permanent bridge.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Dependency:

- [`GLD50`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md)

## Exceptional cover

For canonical support `(0,1),(0,2),(3,1)` with active amplitudes `u,v,w`,
GLD50 leaves

```text
(u+1)(v+1)(u+v+1)(u+vw+v+w+1)=0.                     (1)
```

The four exact surface certificates have denominator lcms

```text
surface                              rows   denominator lcm
u=-1                                   15   2v w^2(v-1)(v+1)(vw+v+w)
v=-1                                   16   2u^2 w^2(u+1)(w-1)
v=-u-1                                 15   u^2 w(u+1)(u+2)(w-1)
u=-(v+1)(w+1)                          16   2v w^3(v-1)(v+1)^2(w-1)(w+1)(vw+v+w). (2)
```

After active-forbidden factors are removed, (2) leaves exactly

```text
u=v=-1;
u=-1,  vw+v+w=0.                                      (3)
```

The first curve has a fifteen-row exact certificate with denominator
`2w^2`.  On the second write `v=-w/(w+1)`; a separate fifteen-row
certificate has denominator `2w^3(2w+1)`.  The roots `w=0` and `w=-1/2`
are forbidden there (`v=0` and `v=1`, respectively).  Hence no legal point
remains on (1).

### Theorem

The full GLD50 orbit `O6`, all `24` masks, is pointwise empty.  `square`

## Scope ledger

```text
GLD50 orbit O6 exceptional union:                     EMPTY;
three-pair O6 orbit, all 24 masks:                    EMPTY;
other four GLD50 exceptional unions:                   OPEN;
four-or-more reciprocal pairs:                        OPEN;
proper-secondary cells:                               OPEN;
every permanent bridge:                               OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_o6_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_o6_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```

The primary expands all `945` perfect matchings and derives each normalized
multiplier from the recorded sparse row core.  The standalone no-import audit
reconstructs recursive permanents and independently derives the same six
contradiction denominators.
