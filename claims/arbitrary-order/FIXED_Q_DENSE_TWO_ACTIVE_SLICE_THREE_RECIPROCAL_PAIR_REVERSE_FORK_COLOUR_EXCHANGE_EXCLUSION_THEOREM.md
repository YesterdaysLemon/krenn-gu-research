# Three-pair reverse-fork colour-exchange exclusion

## Status

**Exact characteristic-zero pointwise closure of GLD50 orbit `O12`.**  The
GLD55 active-colour covariance reverses the GLD53 fork-path support and gives
an invertible isomorphism of the complete equation systems.  All `24`
labelled reverse-fork support masks are therefore empty.

GLD51--GLD55 already close five three-pair orbits.  Seven GLD50 orbitwise
exceptional unions remain open, as do four-or-more-pair supports,
proper-secondary cells, and every permanent bridge.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD50`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md),
- [`GLD53`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_FORK_PATH_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md),
- [`GLD55`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_IN_STAR_COLOUR_EXCHANGE_EXCLUSION_THEOREM.md).

## Exact transfer

The canonical GLD50 `O4` support is

```text
(0,1),(0,2),(1,3).                                    (1)
```

Exchange the two active colours.  GLD55 proves that this reverses each
reciprocal arrow through the involution

```text
f(t)=t/(t-1)                                          (2)
```

and preserves all `81^2=6561` complete equations after an invertible signed
colour permutation of the `81` nuisance coordinates.  Reversing (1) gives

```text
(1,0),(2,0),(3,1).                                    (3)
```

The position permutation

```text
0->2, 1->1, 2->3, 3->0                               (4)
```

sends (3) to

```text
(0,1),(1,2),(3,2),                                    (5)
```

the GLD50 representative of orbit `O12`.  Both (2) and (4) are bijections of
the legal active parameter/support domain.

### Theorem

Any legal `O12` solution would pull back through (2)--(4) to a legal `O4`
solution of the complete fixed-`Q` equation system.  GLD53 proves that no such
`O4` solution exists.  Hence the full GLD50 reverse-fork orbit `O12`, all
`24` masks, is pointwise empty.  `square`

## Scope ledger

```text
GLD50 orbit O12 exceptional union:                    EMPTY;
three-pair reverse-fork orbit, all 24 masks:          EMPTY;
other seven GLD50 exceptional unions:                  OPEN;
four-or-more reciprocal pairs:                        OPEN;
proper-secondary cells:                               OPEN;
every permanent bridge:                               OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_reverse_fork_colour_exchange_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_reverse_fork_colour_exchange_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_fork_path_exceptional_divisor_exclusion.py
```

The primary reuses the GLD55 recursive-permanent row constructor and checks
the signed covariance coefficientwise on all `6561` rows for the fork and
reverse-fork supports.  The standalone no-import audit separately enumerates
the `945` matching topologies, rederives the universal sign covariance, and
checks the exact orbit permutation (4).
