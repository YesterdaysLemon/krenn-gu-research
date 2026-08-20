# Dense two-active-slice disjoint exceptional-divisor exclusion

## Status

**Exact characteristic-zero pointwise closure of the GLD44 disjoint-orbit
exceptional divisor union.**  On one canonical branch take

```text
A^0 = I_4 - E_(0,2) + w E_(1,3),
A^1 = I_4 + (1/2)E_(2,0) + w/(w-1) E_(3,1),
A^2 = I_4,                                             (1)
```

where `w!=0,1`.  No hypothetical witness exists on this curve.  The position
permutation `(0 1)(2 3)` exchanges the two directed support pairs, so the same
certificate also closes the GLD44 branch `w=-1`.  Together with GLD44, this
proves the entire disjoint two-pair orbit empty, covering all `12` labelled
support masks.

Reverse, same-head, and chain exceptional divisors remain open; the same-tail
orbit is already closed by GLD45.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Dependency:

- [`GLD44`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_TWO_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md)

## Exceptional-curve certificate

For the eleven complete rows

```text
(1100;0000) (1000;0010) (0010;0010) (0100;0001)
(0002;0002) (0001;0001) (0020;0020) (0012;0012)
(1001;0000) (0011;0000) (0110;0000),
```

the exact multiplier over `Q(w)` is

```text
(1,1,2,-1/w,1/(w-1),1,-3/2,-1,1,1,1).               (2)
```

It cancels all `81` retained variables and leaves `1`.  Its denominator lcm
is `2w(w-1)`, nonzero everywhere on the active reciprocal-pair stratum.  Thus
the canonical `u=-1` branch has no further exception.

The support-pair exchange maps the other GLD44 exceptional component `w=-1`
to the proved `u=-1` branch.  Therefore the union `(u+1)(w+1)=0` is empty.

### Theorem

The full disjoint two-reciprocal-pair support orbit is pointwise empty.
`square`

## Scope ledger

```text
disjoint GLD44 exceptional divisor union:             EMPTY;
disjoint two-pair orbit, all 12 masks:                EMPTY;
same-tail two-pair orbit:                             EMPTY;
reverse exceptional divisors:                         OPEN;
same-head exceptional divisors:                       OPEN;
chain exceptional divisors:                           OPEN;
three-or-more reciprocal pairs:                       OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_disjoint_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_disjoint_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_two_reciprocal_pair_generic_exclusion.py
```

The primary enumerates all `945` ten-vertex perfect matchings for every row.
The standalone no-import audit reconstructs recursive permanents and derives
the nullspace independently.  The second exceptional branch is covered by an
explicit position permutation, not by an additional numerical sample.
