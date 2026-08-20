# Three-pair in-star colour-exchange exclusion

## Status

**Exact characteristic-zero pointwise closure of GLD50 orbit `O13`.**  Active-
colour exchange reverses every reciprocal arrow and gives an invertible
covariance of the complete `81`-unknown equation system.  The in-star orbit
therefore transfers to the pointwise-empty GLD52 out-star orbit.  All `4`
labelled in-star support masks are empty.

GLD51--GLD54 already close four other three-pair orbits.  Eight GLD50
orbitwise exceptional unions remain open, as do four-or-more-pair supports,
proper-secondary cells, and every permanent bridge.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD50`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md),
- [`GLD52`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_OUT_STAR_EXCEPTIONAL_DIVISOR_EXCLUSION_THEOREM.md).

## Exact colour-exchange covariance

Write

```text
f(t)=t/(t-1),             sigma=(0 1),               (1)
```

with colour `2` fixed.  The reciprocal parametrization satisfies

```text
f(f(t))=t.                                               (2)
```

Thus exchanging active colours sends an out-star reciprocal pair with
colour-zero arrow `i->j` and parameter `t` to the reversed colour-zero arrow
`j->i` with parameter `f(t)`.  The map is an involution of the active domain
`t!=0,1`.  Applied to all three pairs, it sends canonical out-star support

```text
(0,1),(0,2),(0,3)
```

to `(1,0),(2,0),(3,0)`, which becomes the GLD50 `O13` representative
`(0,1),(2,1),(3,1)` after the position swap `(0 1)`.

The fixed helper profiles obey

```text
x=(1,1,0),      x_(sigma c)=x_c;
y=(1,-1,0),     y_(sigma c)=-y_c.                      (3)
```

For each root `r`, root pair `rs`, and colours `c,d`, apply the invertible
nuisance-coordinate change

```text
P0_(r,sigma c) = -P0_(r,c),
P1_(r,sigma c) =  P1_(r,c),
W_(rs,sigma c,sigma d) = -W_(rs,c,d),
b_(sigma c) = b_c.                                     (4)
```

Every surviving ten-vertex perfect-matching term is one of four types:

```text
constant with Q0Q1;   P0 with one y edge;
P1 with no y edge;    W with one y edge.               (5)
```

The minus signs in (3) and (4) cancel exactly in the second and fourth
types; the other two types are unchanged.  Root-port cross factors agree by
(1)--(2), and the pure target term is merely colour-permuted.  Consequently,
after swapping both port and root words, every one of the `81^2=6561`
complete equations is identical under (4).

### Theorem

The complete in-star equation system is isomorphic to the complete out-star
system at the involutively transformed active parameters.  GLD52 proves that
the out-star system has no legal point.  Hence the full GLD50 in-star orbit
`O13`, all `4` masks, is pointwise empty.  `square`

## Scope ledger

```text
GLD50 orbit O13 exceptional union:                    EMPTY;
three-pair in-star orbit, all 4 masks:                EMPTY;
other eight GLD50 exceptional unions:                  OPEN;
four-or-more reciprocal pairs:                        OPEN;
proper-secondary cells:                               OPEN;
every permanent bridge:                               OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_star_colour_exchange_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_star_colour_exchange_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_out_star_exceptional_divisor_exclusion.py
```

The primary independently reconstructs recursive permanents and checks the
signed coordinate covariance on all `6561` complete equations.  The
standalone no-import audit instead enumerates all `945` perfect-matching
topologies and proves the four exhaustive surviving term types in (5), along
with the parameter, helper, coordinate, and target involutions.
