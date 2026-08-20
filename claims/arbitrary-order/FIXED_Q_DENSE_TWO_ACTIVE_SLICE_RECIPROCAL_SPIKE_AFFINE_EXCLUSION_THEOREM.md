# Dense two-active-slice reciprocal-spike affine exclusion

## Status

**Exact characteristic-zero pointwise exclusion of the first reciprocal
two-active-slice affine chart.**  In the canonical dense-shore gauge take

```text
A^0 = I_4 + u E_(0,2),
A^1 = I_4 + v E_(2,0),
A^2 = I_4,                                             (1)
```

with arbitrary `u,v`.  No hypothetical witness exists on this affine plane.
Its `u,v!=0` locus is the first proved chart in this line with two colour
slices simultaneously nonprivate.

This theorem does not cover two active slices with additional support,
arbitrary two-slice cross arrays, root-colour-changing blocks,
proper-secondary cells, or a weighted-permanent bridge.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

Dependency:

- [`GLD41`](FIXED_Q_DENSE_SINGLE_ACTIVE_SLICE_AFFINE_CROSS_ARRAY_COMPLETION_THEOREM.md)

## Reciprocal divisor

Let `E(omega;rho)` denote the complete `81`-variable coefficient equation.
Direct expansion over `Z[u,v]` gives

```text
E(1202;0212)
  - u E(2212;2212)
  - v E(0222;0222) = -(uv-u-v).                       (2)
```

Every retained-variable coefficient on the left of (2) vanishes.  Therefore
any hypothetical witness in (1) lies on

```text
D: uv-u-v=0.                                          (3)
```

If either amplitude vanishes, (3) forces the other to vanish as well; all
three slices are then `I_4`, already excluded by `GLD41` (and `GLD23`).

## Generic curve certificate

On the nonzero part of `D`, necessarily `u!=1` and

```text
v = u/(u-1).                                          (4)
```

For the following thirteen rows, in displayed order,

```text
(0000;0011) (0001;0001) (0002;0002) (0010;0010)
(0011;0000) (0011;0011) (0020;0020) (0101;0000)
(0110;0000) (0200;0200) (1000;0010) (1001;0000)
(1100;0000),
```

the exact left multiplier over `Q(u)` is

```text
(-2/(u+1), 2, -1, 3, -2u-1, -2, -(u-2)/(u-1),
 1, 1, -1, -1/u, 1, 1).                              (5)
```

It cancels all `81` variables and leaves `1`.  Clearing denominators leaves
`u(u-1)(u+1)`.  On the nonzero divisor (3), the factors `u` and `u-1` cannot
vanish, so (5) excludes every point except possibly

```text
(u,v)=(-1,1/2).                                       (6)
```

## Exceptional point

At (6), the eleven rows

```text
(0002;0002) (0010;0010) (0011;0000) (0012;0012)
(0020;0020) (0101;0000) (0110;0000) (0200;0200)
(1000;0010) (1001;0000) (1100;0000)
```

with integer multiplier

```text
(2,6,2,-4,-3,2,2,-2,2,2,2)                           (7)
```

cancel every retained variable and leave `2`.  This closes the exceptional
point.

### Theorem

The complete affine chart (1), including all four support masks, is empty on
the hypothetical witness locus.  `square`

## Scope ledger

```text
two-active reciprocal-spike affine chart:             EMPTY;
reciprocal divisor uv-u-v=0:                          PROVED;
generic nonzero divisor:                              EMPTY;
exceptional point (-1,1/2):                           EMPTY;
all four support masks:                               EMPTY;
general two-active-slice affine cell:                  OPEN;
proper-secondary cells:                               OPEN;
weighted-permanent bridge:                            OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_reciprocal_spike_affine_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_reciprocal_spike_affine_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_single_active_slice_affine_cross_array_completion.py
```

The primary expands all `945` ten-vertex perfect matchings in every selected
row.  The standalone no-import audit reconstructs the equations using
recursive permanents, derives rather than stores each left nullspace, and
checks the exact divisor/generic/point case cover.
