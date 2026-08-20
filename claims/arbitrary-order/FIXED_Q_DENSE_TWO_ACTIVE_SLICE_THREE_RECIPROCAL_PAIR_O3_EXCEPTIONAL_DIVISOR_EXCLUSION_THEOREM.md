# Three-pair O3 exceptional-divisor exclusion

## Status

**Exact characteristic-zero pointwise closure of GLD50 orbit `O3`.**  Four
surface certificates reduce the exceptional union to five intersections;
five curve certificates reduce those to two points; exact rational point
cores close both.  Together with GLD50, all `24` labelled O3 masks are empty.

GLD51--GLD59 already close nine three-pair orbits.  Three GLD50 orbitwise
exceptional unions remain open: `O2`, `O7`, and `O9`.  Four-or-more-pair
supports, proper-secondary cells, and every permanent bridge also remain
open.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

Dependency:

- [`GLD50`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md)

## Exact cover

For canonical support `(0,1),(0,2),(1,2)`, GLD50 leaves

```text
(u-v)(u+v+1)(uw+v-w-1)(uw+v+w+1)=0.                 (1)
```

The four surface cores, with `14,14,15,11` rows, have denominator lcms

```text
u=v:             uw(u-1)(u+1)^2(w-1)(w+1)^2;
v=-u-1:          w(u+1)(2u+1)(uw-u+w)(uw-u-w-2);
v=1+w-uw:        2uw(u-1)(w+1)^2(uw-u-w-2);
v=-1-w-uw:       2w(u+1)(w+1)^2(uw-u+w)(uw+w+1).     (2)
```

After removing active-forbidden factors, (2) leaves five intersections:

```text
u=v=-1;                       u=v, w=-1;
u=v=-1/2;                     v=-u-1, w=(u+2)/(u-1);
v=-u-1, w=u/(u+1).                                  (3)
```

Their exact `12,13,14,13,11`-row cores have denominator lcms

```text
2w(w-1)(w+1);
6u(u-1)(u+1)(2u+1);
3w(w-1)(w+1)^2;
2u(u-1)(u+2)(2u+1)^2;
2u(u+1)(2u+1)^2.                                    (4)
```

The only legal residues of (4) are the points

```text
(u,v,w)=(-1,-1,-1),       (-1/2,-1/2,-1).           (5)
```

Nine- and twelve-row rational cores close (5), with denominator lcms `4`
and `6`.  Every normalized multiplier cancels all `81` nuisance variables
and leaves `1`.

### Theorem

The full GLD50 orbit `O3`, all `24` masks, is pointwise empty.  `square`

## Scope ledger

```text
GLD50 orbit O3 exceptional union:                     EMPTY;
three-pair O3 orbit, all 24 masks:                    EMPTY;
GLD50 orbits O2, O7, O9:                              OPEN;
four-or-more reciprocal pairs:                        OPEN;
proper-secondary cells:                               OPEN;
every permanent bridge:                               OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_o3_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_o3_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```

The primary reuses the proved 945-matching row constructor and derives all
eleven normalized sparse multipliers.  The standalone no-import audit
reconstructs recursive permanents and independently derives the same
denominators.
