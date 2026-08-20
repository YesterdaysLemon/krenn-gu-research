# Bidirected-spur `uv=-1`, `z=1` surface exclusion

## Status

**Exact characteristic-zero pointwise exclusion of the complete `z=1`
residual surface left by `GLD32`.**  On the bidirected-spur chart

```text
A^c=I_4+uE_(0,1)-u^(-1)E_(1,0)+wE_(0,2)+E_(2,0),  u,w!=0,       (1)
```

no hypothetical witness exists.  Together with `GLD33`, this closes two of
the four `GLD32` residual surfaces.  The surfaces `z=-1` and `wz=2` outside
their overlap with the completed surfaces remain open.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

Dependencies: [`GLD31`](FIXED_Q_DENSE_BIDIRECTED_SPUR_GENERIC_CROSS_ARRAY_EXCLUSION_THEOREM.md) and [`GLD32`](FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_GENERIC_EXCLUSION_THEOREM.md).

## Exact two-row contradiction

Let `E(p;r)` denote the complete coefficient row with port word `p` and root
word `r`, retaining all `81` root-side and pure-target variables used by
`GLD31`.  Direct expansion on (1) gives

```text
E(1202;0212) - w E(2212;2212) = w.                  (2)
```

Every retained-variable coefficient on the left of (2) is zero.  Since the
chart assumption gives `w!=0`, (2) is already a contradiction.

There is also a disjoint exact check:

```text
E(0122;1022) + u^(-1) E(1222;1222) = -u^(-1).       (3)
```

Again every retained-variable coefficient cancels, and `u!=0` makes the
right side nonzero.  Either (2) or (3) closes the full surface.

### Theorem

The complete surface (1) is empty on the hypothetical witness locus.

### Proof

Equation (2) is a legal linear combination of two complete coefficient
rows.  Its left side vanishes coefficientwise while its right side is the
nonzero chart parameter `w`, a contradiction.  `square`

## Scope ledger

```text
GLD32 residual z=1:                                  INPUT;
first complete two-row certificate:                    0=w;
second complete two-row certificate:             0=-u^(-1);
entire z=1 surface:                                  EMPTY;
other two live GLD32 residual surfaces:               OPEN;
global Krenn--Gu conjecture:                    UNRESOLVED.
```

This theorem does not close `z=-1`, `wz=2`, the other `GLD31` divisors,
broader cross arrays, or any permanent bridge.

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_z_one_surface_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_uv_minus_one_z_one_surface_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_generic_exclusion.py
```

The primary uses the direct `945`-matching row engine.  The audit is a
standalone no-import implementation: it independently derives recursive
permanents and the two left nullspaces, and stores no primary witness
multipliers.
