# Dense two-active-slice two-reciprocal-pair generic exclusion

## Status

**Exact characteristic-zero generic exclusion of every two-reciprocal-pair
support orbit inside the GLD43 two-active-slice cell.**  The `66` two-pair
support masks form five position-relabelling orbits.  On each orbit, an exact
`12`--`17`-row complete-system certificate excludes the complement of a short
explicit exceptional divisor.

This theorem does not close those exceptional divisors and therefore does not
pointwise exclude all two-pair strata.  It does not address three-or-more-pair
supports, proper-secondary cells, or a weighted-permanent bridge.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

Dependency:

- [`GLD43`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_RECIPROCAL_SUPPORT_DIVISOR_REDUCTION_THEOREM.md)

## Reciprocal parametrization

Choose two directed support pairs.  By `GLD43`, write their colour-zero
amplitudes as `u,w` and their transpose colour-one amplitudes as

```text
u/(u-1),    w/(w-1),                                  (1)
```

where `u,w` are nonzero and neither equals one.  Fix the first directed pair
as `(0,2)`.  The five possibilities for the second pair are exhaustive:

| Orbit | Second pair | Masks | Rows | New exceptional factor |
|---|---:|---:|---:|---|
| reverse | `(2,0)` | `6` | `17` | `(u+1)(w+1)(uw+1)` |
| same tail | `(0,1)` | `12` | `14` | `u+1` |
| same head | `(1,2)` | `12` | `14` | `(u+1)(u-w-1)(u+w+1)` |
| directed chain | `(2,1)` | `24` | `17` | `(u+1)(uw+w+1)` |
| disjoint | `(1,3)` | `12` | `12` | `(u+1)(w+1)` |

The counts sum to `66=binom(12,2)`.  They distinguish reverse arcs, common
tail, common head, one directed length-two chain, and disjoint arcs.

## Exact certificates

For each table row, the primary expands the listed complete equations over
`Q(u,w)` after (1), applies the exact multiplier stored alongside the row
list, cancels all `81` retained variables, and leaves `1`.  The standalone
audit reconstructs the same rows using recursive permanents and derives the
one-dimensional left nullspace rather than storing the multiplier.

The full multiplier denominator lcms are respectively

```text
2uw^2(u-1)(u+1)(w+1)(uw+1),
w(u+1)^2(w-1),
uw(u+1)(u-w-1)(u+w+1),
2uw^2(u-1)(u+1)(w-1)(uw+w+1),
uw(u-1)(u+1)(w-1)(w+1).                              (2)
```

The factors `u,w,u-1,w-1` are already absent by the legal nonzero GLD43
parametrization.  Removing them from (2) gives exactly the new exceptional
factors in the table.  Therefore each orbit is empty off its displayed
exceptional divisor.

The complete row keys and exact rational multipliers are durable executable
data in the primary verifier; the theorem depends on their checked identities,
not on a numerical rank computation.

### Theorem

Every two-reciprocal-pair hypothetical witness in the GLD43 cell must lie on
the corresponding exceptional divisor in the table.  The complement of
those five orbitwise divisors is empty.  `square`

## Scope ledger

```text
two-pair support orbit classification:                PROVED;
all 66 two-pair masks:                                COVERED;
generic complement on each orbit:                     EMPTY;
five orbitwise exceptional divisors:                   OPEN;
three-or-more reciprocal pairs:                        OPEN;
proper-secondary cells:                               OPEN;
weighted-permanent bridge:                            OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_two_reciprocal_pair_generic_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_two_reciprocal_pair_generic_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_reciprocal_support_divisor_reduction.py
```

The primary enumerates all `945` ten-vertex perfect matchings for every
selected row.  The standalone no-import audit reconstructs recursive
permanents, derives each orbit core, verifies every denominator lcm, and
independently exhausts the `66` support masks into the five orbit counts.
