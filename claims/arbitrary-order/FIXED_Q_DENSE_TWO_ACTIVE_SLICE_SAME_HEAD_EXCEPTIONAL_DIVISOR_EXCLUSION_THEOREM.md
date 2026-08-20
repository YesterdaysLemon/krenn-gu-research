# Dense two-active-slice same-head exceptional-divisor exclusion

## Status

**Exact characteristic-zero pointwise closure of the GLD44 same-head-orbit
exceptional divisor union.**  Applying the GLD44 generic certificate in both
orders of the two same-head directed pairs reduces its exceptional union to
one rational curve and one point.  Exact certificates close both residues.
Together with GLD44, the entire same-head two-pair orbit is empty, covering
all `12` labelled support masks.

The same-tail, disjoint, and reverse orbits are already closed by
GLD45--GLD47.  The chain exceptional divisors remain open, as do larger
supports and every permanent bridge.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Dependency:

- [`GLD44`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_TWO_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md)

## Exact exceptional-locus reduction

Use the canonical same-head support `(0,2),(1,2)`.  Its colour-zero
amplitudes are `u,w`, while the reverse colour-one amplitudes are
`u/(u-1),w/(w-1)`; hence active reciprocal support requires

```text
u,w != 0,1.                                           (1)
```

The GLD44 generic certificate leaves

```text
(u+1)(u-w-1)(u+w+1)=0.                               (2)
```

Position transposition `(0 1)` exchanges the two directed pairs, so the same
proved certificate also gives

```text
(w+1)(w-u-1)(u+w+1)=0.                               (3)
```

Over characteristic zero, the common zero set of (2)--(3) inside (1) is
exactly

```text
u+w+1=0,       or       (u,w)=(-1,-1).                (4)
```

Indeed, off the common factor `u+w+1`, the four pairwise intersections give
the displayed point, one point with `w=0`, one with `u=0`, or the inconsistent
pair `u-w=1` and `w-u=1`.

## The curve certificate

On `w=-u-1`, the four active amplitudes are

```text
u,  u/(u-1),  -u-1,  (u+1)/(u+2),                    (5)
```

and (1) gives `u!=0,1,-1,-2`.  An eleven-row exact multiplier over `Q(u)`
cancels all `81` retained variables and leaves `1`.  Its denominator lcm is

```text
2u^2(u+1)^2.                                          (6)
```

Every root of (6) is forbidden on the active curve, so the whole legal curve
is empty.

## The residual point

At `u=w=-1`, both reciprocal amplitudes equal `1/2`.  A separate fourteen-row
integer multiplier cancels all `81` variables and leaves `1`, with denominator
lcm `1`.  Thus the residual point is empty as well.

### Theorem

The full GLD44 same-head exceptional divisor union is empty.  Hence the full
same-head two-pair orbit is pointwise empty.  `square`

## Scope ledger

```text
same-head GLD44 exceptional divisor union:            EMPTY;
same-head two-pair orbit, all 12 masks:               EMPTY;
same-tail two-pair orbit:                             EMPTY;
disjoint two-pair orbit:                              EMPTY;
reverse two-pair orbit:                               EMPTY;
chain exceptional divisors:                           OPEN;
three-or-more reciprocal pairs:                       OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_same_head_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_same_head_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_two_reciprocal_pair_generic_exclusion.py
```

The primary enumerates all `945` ten-vertex perfect matchings for each row and
replays both stored exact multipliers.  The standalone no-import audit
reconstructs recursive permanents and derives both nullspaces independently.
