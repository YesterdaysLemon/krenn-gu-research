# Dense two-active-slice reciprocal-support divisor reduction

## Status

**Exact characteristic-zero pointwise support reduction on the complete
24-parameter two-active-slice affine cell.**  In the canonical dense-shore
gauge let

```text
A^0 = I_4 + sum_(i!=j) x_(ij) E_(i,j),
A^1 = I_4 + sum_(i!=j) y_(ij) E_(i,j),
A^2 = I_4.                                             (1)
```

Every hypothetical witness in (1) has transpose-matched off-diagonal support,
and every active reciprocal pair lies on one explicit rational curve.  After
the proved GLD41 and GLD42 exclusions, any residual point must contain at
least two reciprocal pairs.

This is a reduction, not an exclusion of the complete two-active-slice cell.
It does not prove that any residual support pattern occurs.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD41`](FIXED_Q_DENSE_SINGLE_ACTIVE_SLICE_AFFINE_CROSS_ARRAY_COMPLETION_THEOREM.md)
- [`GLD42`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_RECIPROCAL_SPIKE_AFFINE_EXCLUSION_THEOREM.md)

## Twelve exact reciprocal divisors

Let `E(omega;rho)` denote the complete `81`-variable coefficient equation.
For each ordered pair `i!=j`, choose a position permutation `sigma` with
`sigma(0)=i` and `sigma(2)=j`.  Write

```text
x = x_(ij),    y = y_(ji).                            (2)
```

Direct expansion over the polynomial ring in all twenty-four amplitudes gives

```text
E(sigma 1202; sigma 0212)
  - x E(sigma 2212; sigma 2212)
  - y E(sigma 0222; sigma 0222) = -(xy-x-y).          (3)
```

Every retained-variable coefficient on the left of (3) vanishes.  Both
verifier routes expand all `12` ordered pairs with every other amplitude still
present; (3) is not inferred from an untested symmetry representative.

Consequently each hypothetical witness satisfies

```text
x_(ij)y_(ji)-x_(ij)-y_(ji)=0       for every i!=j.    (4)
```

If either member of a reciprocal pair vanishes, (4) forces the other to
vanish.  If both are nonzero, neither equals one and

```text
y_(ji) = x_(ij)/(x_(ij)-1).                          (5)
```

Thus the off-diagonal support of `A^1-I_4` is exactly the transpose of the
off-diagonal support of `A^0-I_4`.

## Exhaustive support consequence

The unrestricted 24-amplitude cell has `2^24=16777216` support masks.  The
twelve reciprocal equivalences reduce this to the `2^12=4096` transpose-
matched masks.  The empty matched mask is the GLD41/GLD23 identity boundary.
Each of the twelve one-pair masks is a position relabelling of the GLD42
reciprocal-spike chart.  Hence every hypothetical residual point must use at
least two reciprocal pairs, leaving at most

```text
2^12 - 1 - 12 = 4083                                (6)
```

support patterns.  Equivalently, `16773133` of the original `2^24` masks are
excluded by (4), GLD41, and GLD42.  This count is a support-locus reduction,
not a witness enumeration.

### Theorem

Every hypothetical witness in (1) lies on the twelve-divisor locus (4), has
transpose-matched support, satisfies (5) on each active pair, and contains at
least two active reciprocal pairs.  `square`

## Scope ledger

```text
full 24-parameter two-active-slice cell:              REDUCED;
twelve reciprocal divisor equations:                 PROVED;
transpose-matched support:                            PROVED;
zero- and one-pair support masks:                     EMPTY;
residual masks with at least two pairs:         4083 / OPEN;
proper-secondary cells:                               OPEN;
weighted-permanent bridge:                            OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_reciprocal_support_divisor_reduction.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_reciprocal_support_divisor_reduction.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_reciprocal_spike_affine_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_single_active_slice_affine_cross_array_completion.py
```

The primary enumerates all `945` ten-vertex perfect matchings for every
selected row.  The standalone no-import audit reconstructs the equations by
recursive permanents, derives all twelve left nullspaces, and independently
checks the exact support-mask census.
