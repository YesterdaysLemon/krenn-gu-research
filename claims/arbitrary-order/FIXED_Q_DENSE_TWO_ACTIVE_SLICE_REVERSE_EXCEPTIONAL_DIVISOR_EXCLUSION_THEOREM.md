# Dense two-active-slice reverse exceptional-divisor exclusion

## Status

**Exact characteristic-zero pointwise closure of the GLD44 reverse-orbit
exceptional divisor union.**  Two exact curve certificates close `u=-1` and
`uw=-1`; exchanging the two reverse directed pairs closes `w=-1`.  Together
with GLD44, the entire reverse two-pair orbit is empty, covering all `6`
labelled support masks.

The same-tail and disjoint orbits are already closed by GLD45--GLD46.
Same-head and chain exceptional divisors remain open, as do larger supports
and every permanent bridge.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Dependency:

- [`GLD44`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_TWO_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md)

## The `u=-1` curve

On the canonical reverse support, `u=-1` forces its reciprocal amplitude to
`1/2`; the second pair has amplitudes `w,w/(w-1)`, with `w!=0,1`.  A
seventeen-row exact multiplier over `Q(w)` cancels all `81` variables and
leaves `1`.  Its denominator lcm is

```text
2w^2(w-1),                                            (1)
```

which has no root on the active reciprocal domain.  The primary verifier
stores and replays the full row/multiplier list; the independent audit derives
it from recursive permanents.

The position transposition `(0 2)` exchanges the two reverse directed pairs,
so the GLD44 component `w=-1` is the same proved curve with pair labels
exchanged.

## The `uw=-1` curve

Write `w=-1/u`.  The reciprocal amplitudes become

```text
u/(u-1),    1/(u+1),                                  (2)
```

and the active domain has `u!=0,1,-1`.  A separate fifteen-row multiplier
over `Q(u)` cancels all retained variables and leaves `1`; its denominator
lcm is

```text
2u(u-1)(u+1).                                         (3)
```

Every root of (3) is already forbidden on this component, so it has no
residual point.

### Theorem

All three GLD44 reverse exceptional components
`(u+1)(w+1)(uw+1)=0` are empty.  Hence the full reverse two-pair orbit is
pointwise empty.  `square`

## Scope ledger

```text
reverse GLD44 exceptional divisor union:              EMPTY;
reverse two-pair orbit, all 6 masks:                  EMPTY;
same-tail two-pair orbit:                             EMPTY;
disjoint two-pair orbit:                              EMPTY;
same-head exceptional divisors:                       OPEN;
chain exceptional divisors:                           OPEN;
three-or-more reciprocal pairs:                       OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_reverse_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_reverse_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_two_reciprocal_pair_generic_exclusion.py
```

The primary enumerates all `945` ten-vertex perfect matchings for each row and
replays both stored exact multipliers.  The standalone no-import audit
reconstructs recursive permanents and derives both nullspaces independently.
