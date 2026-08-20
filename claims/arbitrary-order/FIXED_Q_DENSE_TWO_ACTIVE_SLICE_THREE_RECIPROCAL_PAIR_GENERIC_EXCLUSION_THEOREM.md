# Dense two-active-slice three-reciprocal-pair generic exclusion

## Status

**Exact characteristic-zero generic exclusion of every three-reciprocal-pair
support orbit in the GLD43 cell.**  The `220` labelled three-pair masks split
into exactly `13` position-relabelling orbits.  One exact `14`--`18`-row
function-field certificate per orbit excludes its complement of the explicit
divisor atlas below.

This is a generic theorem, not a pointwise exclusion.  The displayed
exceptional hypersurfaces remain open, as do supports with four or more
reciprocal pairs, proper-secondary cells, and every permanent bridge.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

Dependency:

- [`GLD43`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_RECIPROCAL_SUPPORT_DIVISOR_REDUCTION_THEOREM.md)

GLD45--GLD49 separately prove all `66` two-pair masks empty.

## Reciprocal parametrization

For an ordered support arc carrying colour-zero amplitude `a`, GLD43 forces
the reverse colour-one amplitude to be

```text
a/(a-1),                                              (1)
```

with `a!=0,1`.  For each representative below, the three arcs in the written
order receive parameters `u,v,w`.  Thus throughout

```text
u,v,w != 0,1.                                         (2)
```

## Exact orbit census and certificate atlas

Write `ij` for the directed arc `(i,j)`.  In the last column, factors already
forbidden by (2), and nonzero rational constants, have been removed from the
full multiplier denominator.  `E_i=1` means that no additional factor was
removed; none of the thirteen rows has that value here.

| Orbit | Representative | Masks | Rows | Remaining exceptional factor `E_i` |
|---|---|---:|---:|---|
| `O1` | `01,02,03` | 4 | 15 | `(w+1)(v+w+1)` |
| `O2` | `01,02,10` | 24 | 16 | `(u+1)(u+v)(v+2)(uw+1)(u+v+1)(uw+vw+v+1)` |
| `O3` | `01,02,12` | 24 | 14 | `(u-v)(u+v+1)(uw+v-w-1)(uw+v+w+1)` |
| `O4` | `01,02,13` | 24 | 15 | `(u+1)(uw+vw+v+w+1)` |
| `O5` | `01,02,30` | 12 | 18 | `(u+1)(u+2)(u-v)(v+1)(v+2)(w+1)` |
| `O6` | `01,02,31` | 24 | 16 | `(u+1)(v+1)(u+v+1)(u+vw+v+w+1)` |
| `O7` | `01,10,20` | 24 | 18 | `(u+1)(uv+1)(v+w+1)(uv-v-1)P_7` |
| `O8` | `01,10,23` | 12 | 15 | `(u+1)(w+1)(2w-1)(uv+1)` |
| `O9` | `01,12,20` | 8 | 17 | `(uvw-1)(uvw+1)(uv+v+1)(vw+w+1)(uw-u-2w+1)P_9` |
| `O10` | `01,12,23` | 24 | 15 | `uv+v+1` |
| `O11` | `01,12,31` | 12 | 17 | `(u+1)(u-w-1)(u+w+1)(uv+v+1)` |
| `O12` | `01,12,32` | 24 | 17 | `(u+1)(w+1)(uv+v+1)(2uvw-2uw+2vw-w-1)` |
| `O13` | `01,21,31` | 4 | 17 | `(u-v+1)(u+v+1)(u+w+1)(2vw-v-w)(u-v-w-1)` |

The two non-short factors are

```text
P_7 = u^2 v w^2 - u^2 v w - u^2 w^2 + u^2 w
      - 4uvw^2 + uvw + 2uv + uw
      - 2vw^2 + 2vw - 2v + 4w^2 - 2w,               (3)

P_9 = uv^2w - uvw + 2v^2w - 4vw + v + 2w + 1.       (4)
```

The orbit sizes sum to

```text
4+24+24+24+12+24+24+12+8+24+12+24+4 = 220 = C(12,3). (5)
```

## Certificate statement

For each orbit representative, specialize the three reciprocal pairs by (1)
and retain the same `81` unknown nuisance variables used by GLD44.  The
recorded row core has a one-dimensional left nullspace.  Normalizing its
pairing with the right-hand side gives an exact multiplier over
`Q(u,v,w)` that cancels all `81` variables and leaves `1`.  Its full
denominator is asserted by both replay scripts; after removing only the
always-forbidden factors in (2), its remaining zero locus is exactly the
listed `E_i=0`.

### Theorem

Every hypothetical three-pair witness in the GLD43 cell belongs to one of the
thirteen orbitwise exceptional hypersurface unions `E_i=0`.  Equivalently,
the complement of that explicit divisor atlas is empty.  `square`

## Scope ledger

```text
three-pair support masks:                             220;
position-relabelling orbits:                          13;
generic complement of displayed atlas:               EMPTY;
displayed three-pair exceptional divisors:            OPEN;
four-or-more reciprocal pairs:                        OPEN;
proper-secondary cells:                               OPEN;
every permanent bridge:                               OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_reciprocal_support_divisor_reduction.py
```

The primary enumerates all `945` ten-vertex perfect matchings for every row,
derives each nullspace, factors all thirteen exact denominator lcms, and
exhausts the `220` masks.  The standalone no-import audit reconstructs
permanents recursively, reverses orbit/row/variable traversal, independently
repeats the orbit census, and derives the same thirteen contradictions.
