# Four-root torus star-equal-leaf H4/Q6 membership pilot

Date: 2026-08-29
Base: `origin/main` at `495628957040b003644e8d24fd322e9980239c36`
Experiment ID: `GLD98-membership-pilot`
Status: **exploratory fixed-fibre evidence; not a theorem**
Global Krenn--Gu status: **UNRESOLVED**

## 1. Exact question and outcome

On selected fixed rational and finite-field `(p,a)` fibres of the normalized
four-root star-equal-leaf H4/Q6 chart, the pilot asks whether the six GLD97
seven-minors generate the offset coordinates `B` and `C` in the exact
quotient algebra `K[q]/(Q6)`.  It uses copied, pinned GLD71 sparse supports,
the local GLD88 endpoint formula, the local GLD96 polynomial `Q6`, direct
sparse subset-DP determinants, and exact Macaulay linear algebra.

The three regular pilot fibres all have `B,C` membership first at total
`(B,C)` degree four:

| fibre | D4 rank | D4 rank with B | D4 rank with C | nonconstant target columns | deficiency |
| --- | ---: | ---: | ---: | ---: | ---: |
| `QQ`, `p=2`, `a=0` | 48 | 48 | 48 | 56 | 8 |
| `QQ`, `p=3`, `a=1` | 52 | 52 | 52 | 56 | 4 |
| `GF(11)`, `p=2`, `a=0` | 46 | 46 | 46 | 56 | 10 |

Thus these fixed fibres give exact evidence for the desired offset collapse,
but they also refute the tempting stronger shortcut that the bounded Macaulay
map should be surjective onto every nonconstant target column.

The rational controls `p=0,a=0` and `p=1,a=0` were skipped because `Q6`
overlaps chart/Delta factors.  The `GF(7),p=3,a=2` control was skipped because
`P=0`, all determinant denominator bounds vanish, and `Q6` overlaps chart
factors.  The script reports these exceptional gates rather than inverting
their zero divisors.

## 2. Reproducible bounded runs

The committed entry point is
[`explore_four_root_torus_star_equal_leaf_h4_q6_modular_membership_census.py`](../../../claims/arbitrary-order/explore_four_root_torus_star_equal_leaf_h4_q6_modular_membership_census.py).
Its SHA-256 in these runs was
`bd4e57c6cb4fb71a8a5c2b503980faacfd1f96994cc583d2d630780e3934ca25`.
The pinned support digest was
`c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0`.

The default census ran as:

```text
python tools/research/run_bounded.py \
  --run-id gld98-membership-census-publish-20260829a \
  --timeout-seconds 60 --memory-mb 12288 -- \
  python claims/arbitrary-order/explore_four_root_torus_star_equal_leaf_h4_q6_modular_membership_census.py \
  --progress
```

The runner exited zero after 6.185 seconds; the script reported 4.639
seconds.  CPython 3.13.14 and SymPy 1.14.0 were used on Windows 11.

The two degree-eight controls were replayed directly through the committed
CLI:

```text
python tools/research/run_bounded.py \
  --run-id gld98-census-p2a0-d8-cli-20260829a \
  --timeout-seconds 90 --memory-mb 12288 -- \
  python claims/arbitrary-order/explore_four_root_torus_star_equal_leaf_h4_q6_modular_membership_census.py \
  --sample rational:2:0 --macaulay-max-degree 8 --progress

python tools/research/run_bounded.py \
  --run-id gld98-census-p3a1-d8-cli-20260829a \
  --timeout-seconds 90 --memory-mb 12288 -- \
  python claims/arbitrary-order/explore_four_root_torus_star_equal_leaf_h4_q6_modular_membership_census.py \
  --sample rational:3:1 --macaulay-max-degree 8 --progress
```

Both exited zero.  The observed rank/nonconstant-target-column signatures
from degrees three through eight were:

```text
QQ, p=2, a=0: (20/36), (48/56), (72/80), (100/108), (132/140), (168/176)
QQ, p=3, a=1: (24/36), (52/56), (76/80), (104/108), (136/140), (172/176)
```

In both cases `B,C` enter the span at degree four and remain there through
degree eight, while the nonconstant-target deficiency stabilizes at eight
and four respectively.  Full-row or nonconstant-target surjectivity is
therefore not a valid route to the observed fixed-fibre membership.

For output comparison, the normalized structural payload SHA-256 values are:

| run ID | normalized payload SHA-256 |
| --- | --- |
| `gld98-membership-census-publish-20260829a` | `91e6e33618eba6c94cab3c9bdfbfdbcfe1fc228707efe8acb5297f9ce93c1020` |
| `gld98-census-p2a0-d8-cli-20260829a` | `c5711c23ec42768266b930d328c55c4090f9ebd511d82f062232b83097572a3a` |
| `gld98-census-p3a1-d8-cli-20260829a` | `306f8eeba31ab05af10b2e430a8a114fa48bc858ef7ca489c5c11c80148bd478` |

For these hashes, recursively delete the volatile keys `runtime_seconds`,
`runtime_environment`, `seconds`, and `determinant_seconds`, then serialize
the remaining JSON with sorted keys, ASCII escaping, and compact separators
before applying SHA-256.

## 3. Scope and nonclaims

This pilot is not a generic computation over `QQ(p,a)`, an exhaustive cover
of `(p,a)`, a theorem, a proof, or a counterexample.  It does not reprove the
GLD75/GLD86 bridge, the GLD88 endpoint, the physical Omega gates, or any
specialization from these fixed fibres.  In particular, it does not close an
exceptional divisor or establish a function-field ideal equality.

No theorem-ledger entry and no change to `docs/current-frontier.md` are
warranted: this artifact records exploratory fixed-fibre evidence and a
failed proof shortcut, but changes no live mathematical claim, scope, or
proof-topology edge.  The global conjecture remains **UNRESOLVED**.
