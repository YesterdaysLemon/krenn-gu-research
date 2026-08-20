# Dense single-active-slice affine cross-array completion

## Status

**Exact characteristic-zero pointwise exclusion of the complete affine
single-active-slice cross-array cell.**  Keep two colour slices equal to the
identity and allow the third to be an arbitrary matrix with unit diagonal:

```text
A^a=I_4,
A^d=I_4,
A^c=I_4 + sum_(i!=j) a_(ij) E_(i,j),                (1)
```

where all `12` off-diagonal amplitudes are arbitrary and may vanish.  No
hypothetical witness exists anywhere on this affine parameter space.

This theorem subsumes `GLD24`--`GLD40` on their coordinate subcharts; those
results remain proved and separately replayable.  It does not cover cells
where two or more colour slices are simultaneously nonprivate,
root-colour-changing blocks, proper-secondary cells, or any
weighted-permanent bridge.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Dependencies:

- [`GLD23`](FIXED_Q_DENSE_COLOUR_DEPENDENT_PRIVATE_PERMUTATION_EXCLUSION_THEOREM.md)
- [`GLD40`](FIXED_Q_DENSE_BIDIRECTED_SPUR_AFFINE_CHART_COMPLETION_THEOREM.md)

## Twelve entry detectors

Let `E(omega;rho)` denote the complete `81`-variable coefficient equation.
For a permutation `sigma` of the four root/port positions, define

```text
(sigma omega)_(sigma(k)) = omega_k.                  (2)
```

Fix any ordered pair `i!=j` and choose `sigma` with
`sigma(0)=i`, `sigma(2)=j`.  Direct expansion over the polynomial ring in
all twelve amplitudes gives

```text
E(sigma 1202; sigma 0212)
  - a_(ij) E(sigma 2212; sigma 2212) = a_(ij).       (3)
```

Every retained-variable coefficient on the left of (3) vanishes.  More
transparently, for two root--residual variables `P_0,P_1` selected by
`sigma`, the two rows are exactly

```text
-a_(ij) P_0 + a_(ij) P_1 =  0,
          -P_0 +          P_1 = -1.                 (4)
```

No other amplitude occurs in (4).  Both verifier routes expand and check all
`12` ordered pairs explicitly; the proof does not rely on symmetry alone.

## Exhaustive affine closure

If any `a_(ij)` is nonzero, relation (3) gives an immediate contradiction.
If every off-diagonal amplitude is zero, all three colour slices in (1) are
the identity private matching, excluded by `GLD23`.  These alternatives
exhaust all `2^12=4096` support masks.

### Theorem

The entire affine cell (1) is empty on the hypothetical witness locus.

### Proof

Choose a nonzero off-diagonal entry and apply its exact relation (3), or use
`GLD23` at the all-zero endpoint.  `square`

## Scope ledger

```text
single-active-slice affine cell:                      EMPTY;
all 12 entry detectors:                              PROVED;
all 4096 off-diagonal support masks:                  EMPTY;
GLD24--GLD40 coordinate subcharts:     PROVED / REPLAYABLE;
multiple simultaneously nonprivate slices:            OPEN;
proper-secondary cells:                               OPEN;
weighted-permanent bridge:                            OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_single_active_slice_affine_cross_array_completion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_single_active_slice_affine_cross_array_completion.py
python claims/arbitrary-order/verify_fixed_q_dense_colour_dependent_private_permutation_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_affine_chart_completion.py
```

The primary enumerates all `945` ten-vertex perfect matchings for each
selected row.  The standalone no-import audit reconstructs the same complete
rows through recursive permanents, derives every left nullspace instead of
storing its multiplier, and independently checks the `4096`-mask cover.
