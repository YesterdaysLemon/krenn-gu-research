# Dense bidirected-spur nonzero-chart completion

## Status

**Exact characteristic-zero pointwise exclusion of the complete nonzero
`GLD31` bidirected-spur chart.**  For

```text
A^c=I_4+uE_(0,1)+vE_(1,0)+wE_(0,2)+zE_(2,0),
u,v,w,z!=0,                                          (1)
```

no hypothetical witness exists.  This closes the five-factor exceptional
locus left by `GLD31`, including the two divisors that remained after
`GLD38`.  The generic detector and divisor refinements `GLD31`--`GLD38`
remain correct separately replayable results but are subsumed on (1).

This theorem does not resolve broader cross arrays, support-drop boundaries,
root-colour-changing blocks, proper-secondary cells, or any
weighted-permanent bridge.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

Dependency: [`GLD31`](FIXED_Q_DENSE_BIDIRECTED_SPUR_GENERIC_CROSS_ARRAY_EXCLUSION_THEOREM.md).
The same row pair first appeared after specialization in
[`GLD34`](FIXED_Q_DENSE_BIDIRECTED_SPUR_UV_MINUS_ONE_Z_ONE_SURFACE_EXCLUSION_THEOREM.md);
the proof below re-expands it over the full polynomial ring and makes no
inference from that specialized theorem.

## Uniform two-row contradiction

Retain all `81` root-side and pure-target variables of the complete `GLD31`
coefficient system.  Let

```text
P_0=p_(0,2,1),   P_1=p_(1,2,1).
```

Direct expansion over `Z[u,v,w,z]` gives the complete rows

```text
E(1202;0212):  -w P_0 + w P_1 =  0,                 (2)
E(2212;2212):    -P_0 +   P_1 = -1.                 (3)
```

Every one of the other `79` retained-variable coefficients is zero in both
rows.  Subtracting `w` times (3) from (2) gives

```text
0=w.                                                 (4)
```

No divisor equation and no denominator is used.  Since `w!=0` is an original
hypothesis of (1), equation (4) is a contradiction.

### Theorem

The complete chart (1) is empty on the hypothetical witness locus.

### Proof

Equations (2)--(3) are legal rows of the complete coefficient system.
Their exact linear combination (4) contradicts `w!=0`.  `square`

## Proof-consolidation audit

The earlier `GLD34` replay substituted `v=-1/u` and `z=1` before checking
this pair.  Those substitutions are absent here.  The primary enumerates all
`945` perfect matchings and checks the two sparse rows over
`Z[u,v,w,z]`.  The standalone no-import audit reconstructs the three
matching types by recursive permanents, derives the left nullspace rather
than storing its multiplier, and independently obtains `[1,-w]` with target
`w`.

Thus the strengthening is a fresh polynomial identity on the entire chart,
not a specialization argument or a density extrapolation.

## Scope ledger

```text
GLD31 nonzero bidirected-spur chart:                 EMPTY;
uniform complete-system detector:                     0=w;
five GLD31 exceptional divisors:                     EMPTY;
GLD31--GLD38 results on this chart:       PROVED / REPLAYABLE;
broader cross arrays and support-drop boundaries:     OPEN;
weighted-permanent bridge:                            OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_nonzero_chart_completion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_nonzero_chart_completion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_generic_cross_array_exclusion.py
```
