# Three-pair out-fork colour-exchange exclusion

## Status

**Exact characteristic-zero pointwise closure of GLD50 orbit `O5`.**  The
GLD55 active-colour covariance reverses the GLD57 in-fork support and gives an
invertible isomorphism of the complete equation systems.  All `12` labelled
out-fork support masks are therefore empty.

GLD51--GLD57 already close seven three-pair orbits.  Five GLD50 orbitwise
exceptional unions remain open, as do four-or-more-pair supports,
proper-secondary cells, and every permanent bridge.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD50`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md),
- [`GLD55`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_IN_STAR_COLOUR_EXCHANGE_EXCLUSION_THEOREM.md),
- [`GLD57`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_IN_FORK_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md).

## Exact transfer

The canonical GLD50 `O11` support is

```text
(0,1),(1,2),(3,1).                                    (1)
```

GLD55 proves that exchanging active colours reverses every reciprocal arrow
through `f(t)=t/(t-1)` and preserves all `6561` complete equations after an
invertible signed permutation of the `81` nuisance coordinates.  Reversing
(1) gives

```text
(1,0),(2,1),(1,3).                                    (2)
```

The position permutation

```text
0->1, 1->0, 2->3, 3->2                               (3)
```

sends (2) to `(0,1),(0,2),(3,0)`, the GLD50 representative of orbit `O5`.
The parameter involution and position permutation are bijections of the
legal active support domain.

### Theorem

Any legal `O5` solution would pull back to a legal `O11` solution of the
complete fixed-`Q` system.  GLD57 proves that no such `O11` solution exists.
Hence the full GLD50 out-fork orbit `O5`, all `12` masks, is pointwise empty.
`square`

## Scope ledger

```text
GLD50 orbit O5 exceptional union:                     EMPTY;
three-pair out-fork orbit, all 12 masks:              EMPTY;
other five GLD50 exceptional unions:                   OPEN;
four-or-more reciprocal pairs:                        OPEN;
proper-secondary cells:                               OPEN;
every permanent bridge:                               OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_out_fork_colour_exchange_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_out_fork_colour_exchange_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_fork_exceptional_divisor_exclusion.py
```

The primary checks the signed covariance coefficientwise on all `6561` rows
for the in-fork and out-fork supports.  The standalone no-import audit
separately enumerates the `945` matching topologies, rederives the universal
sign covariance, and checks the exact orbit permutation (3).
