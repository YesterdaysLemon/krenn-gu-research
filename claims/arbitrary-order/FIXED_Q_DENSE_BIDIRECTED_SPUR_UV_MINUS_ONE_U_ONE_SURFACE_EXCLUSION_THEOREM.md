# Bidirected-spur `uv=-1`, `u=1` surface exclusion

## Status

**Exact characteristic-zero pointwise exclusion of the complete `u=1`
residual surface left by `GLD32`.**  On the bidirected-spur chart

```text
A^c=I_4+E_(0,1)-E_(1,0)+wE_(0,2)+zE_(2,0),  w,z!=0, (1)
```

no hypothetical witness exists.  This closes one of four `GLD32` residual
surfaces; `z=1`, `z=-1`, and `wz=2` outside their overlap with (1) remain
open.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

Dependencies: [`GLD31`](FIXED_Q_DENSE_BIDIRECTED_SPUR_GENERIC_CROSS_ARRAY_EXCLUSION_THEOREM.md) and [`GLD32`](FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_GENERIC_EXCLUSION_THEOREM.md).

## Exact case cover

Keep all `81` root-side and pure-target variables.  Two independent exact
row relations on (1) leave

```text
D_1=4wz(wz-2)(wz+1),
D_2=-2wz(z+1)(wz-2).                                (2)
```

Since `w,z!=0`, simultaneous vanishing of (2) gives exactly

```text
wz=2,  or  (w,z)=(1,-1).                            (3)
```

Indeed, away from `wz=2`, the first detector forces `wz=-1` and the second
forces `z=-1`, hence `w=1`.

On the curve `w=2/z`, a thirteen-row polynomial-cleared certificate leaves
the constant `24`.  At `(w,z)=(1,-1)`, a twelve-row rational certificate
leaves `6`.  Both constants are nonzero in characteristic zero.

### Theorem

The complete surface (1) is empty on the hypothetical witness locus.

### Proof

Relations (2) reduce every possible point exhaustively to (3).  The curve
and point certificates contradict the complete coefficient system on the
two remaining pieces.  `square`

## Scope ledger

```text
GLD32 residual u=1:                                  INPUT;
two surface detectors:                    D_1 and D_2;
wz=2 residual curve:                         EMPTY (24);
(w,z)=(1,-1) residual point:                  EMPTY (6);
entire u=1 surface:                                EMPTY;
other three GLD32 residual surfaces:                OPEN;
global Krenn--Gu conjecture:                  UNRESOLVED.
```

This theorem does not close the other `GLD32` surfaces, the other `GLD31`
divisors, broader cross arrays, or any permanent bridge.

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_u_one_surface_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_uv_minus_one_u_one_surface_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_minus_one_generic_exclusion.py
```

The primary uses the direct `945`-matching row engine.  The audit is a
standalone no-import implementation: it independently derives recursive
permanents, recomputes each left nullspace, and stores no primary witness
multipliers.
