# Bidirected-spur `uv+wz-1=0` divisor exclusion

## Status

**Exact characteristic-zero pointwise exclusion of the complete nonzero
`uv+wz-1=0` divisor left by `GLD31`.**  On the bidirected-spur chart

```text
A^c=I_4+uE_(0,1)+((1-wz)/u)E_(1,0)+wE_(0,2)+zE_(2,0),
u,w,z,(1-wz)/u != 0.                                  (1)
```

no hypothetical witness exists.  Together with `GLD36`, this closes two of
the five `GLD31` divisors.  The divisors `uv+wz+1=0`, `uv+vw+w+1=0`, and
`p=0` remain open.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

Dependency: [`GLD31`](FIXED_Q_DENSE_BIDIRECTED_SPUR_GENERIC_CROSS_ARRAY_EXCLUSION_THEOREM.md).

## Exact two-row contradictions

Let `E(p;r)` denote the complete coefficient row with port word `p` and root
word `r`, retaining all `81` root-side and pure-target variables used by
`GLD31`.  Direct expansion on (1) gives

```text
E(0100;1000) + ((wz-1)/u) E(1222;1222) = -(wz-1)/u.  (2)
```

Since `v=(1-wz)/u`, equation (2) is exactly `0=v` after all retained-variable
coefficients cancel.  The nonzero-chart hypothesis `v!=0` is a
contradiction.

A disjoint exact check gives

```text
E(0100;0010) + (w(wz-1)/u) E(2212;2212)
  = -w(wz-1)/u,                                       (3)
```

which is `0=wv`.  Again `w,v!=0` makes the right side nonzero.

### Theorem

The complete divisor (1) is empty on the hypothetical witness locus.

### Proof

Equation (2) is a legal linear combination of two complete coefficient
rows.  Its left side vanishes coefficientwise while its right side is the
nonzero chart parameter `v`, a contradiction.  `square`

## Scope ledger

```text
GLD31 divisor uv+wz-1=0:                              EMPTY;
complete-system two-row detector:                      0=v;
disjoint two-row detector:                            0=wv;
other three GLD31 divisors:                            OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

This theorem does not close the other `GLD31` divisors, broader cross arrays,
or any permanent bridge.

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_uv_plus_wz_minus_one_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_uv_plus_wz_minus_one_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion.py
```

The primary uses the direct `945`-matching row engine.  The audit is a
standalone no-import implementation: it independently derives recursive
permanents and both left nullspaces, and stores no primary witness
multipliers.
