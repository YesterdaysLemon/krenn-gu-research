# Bidirected-spur `uv=-1`, `wz=2` surface exclusion

## Status

**Exact characteristic-zero pointwise exclusion of the complete `wz=2`
residual surface left by `GLD32`.**  On the bidirected-spur chart

```text
A^c=I_4+uE_(0,1)-u^(-1)E_(1,0)+(2/z)E_(0,2)+zE_(2,0),
u,z!=0.                                                       (1)
```

no hypothetical witness exists.  Together with `GLD32`--`GLD35`, this
exhausts the four residual surfaces and proves pointwise exclusion of the
complete nonzero `uv=-1` divisor inside `GLD31`.  The other four `GLD31`
divisors remain open.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Dependencies: [`GLD31`](FIXED_Q_DENSE_BIDIRECTED_SPUR_GENERIC_CROSS_ARRAY_EXCLUSION_THEOREM.md), [`GLD32`](FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_GENERIC_EXCLUSION_THEOREM.md), [`GLD33`](FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_U_ONE_SURFACE_EXCLUSION_THEOREM.md), [`GLD34`](FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_Z_ONE_SURFACE_EXCLUSION_THEOREM.md), and [`GLD35`](FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_Z_MINUS_ONE_SURFACE_EXCLUSION_THEOREM.md).

## Exact two-row contradiction

Let `E(p;r)` denote the complete coefficient row with port word `p` and root
word `r`, retaining all `81` root-side and pure-target variables used by
`GLD31`.  Direct expansion on (1) gives

```text
E(0100;1000) + u^(-1) E(1222;1222) = -u^(-1).       (2)
```

Every retained-variable coefficient on the left of (2) is zero.  Since the
chart assumption gives `u!=0`, the right side is nonzero.

### Theorem

The complete surface (1) is empty on the hypothetical witness locus.

### Proof

Equation (2) is a legal linear combination of two complete coefficient
rows.  Its left side vanishes coefficientwise while its right side is
nonzero, a contradiction.  `square`

### Divisor-completion corollary

`GLD32` excludes the complement of `u=1`, `z=1`, `z=-1`, and `wz=2` inside
the nonzero `uv=-1` divisor.  `GLD33`, `GLD34`, `GLD35`, and the theorem above
exclude those four surfaces respectively.  Therefore the entire divisor is
empty on the hypothetical witness locus.

## Scope ledger

```text
GLD32 generic complement:                             EMPTY;
GLD33 residual u=1:                                   EMPTY;
GLD34 residual z=1:                                   EMPTY;
GLD35 residual z=-1:                                  EMPTY;
GLD36 residual wz=2:                                  EMPTY;
complete nonzero GLD31 divisor uv=-1:                 EMPTY;
other four GLD31 divisors:                             OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

This theorem does not close the other `GLD31` divisors, broader cross arrays,
or any permanent bridge.

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_wz_two_surface_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_uv_minus_one_wz_two_surface_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_generic_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_u_one_surface_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_z_one_surface_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_z_minus_one_surface_exclusion.py
```

The primary uses the direct `945`-matching row engine.  The audit is a
standalone no-import implementation: it independently derives recursive
permanents and the left nullspace, and stores no primary witness multiplier.
