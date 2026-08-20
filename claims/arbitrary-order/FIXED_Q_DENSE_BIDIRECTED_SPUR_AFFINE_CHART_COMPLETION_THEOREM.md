# Dense bidirected-spur affine-chart completion

## Status

**Exact characteristic-zero pointwise exclusion of the complete affine
four-parameter bidirected-spur coordinate family.**  For arbitrary
`u,v,w,z` in the field, set

```text
A^c=I_4+uE_(0,1)+vE_(1,0)+wE_(0,2)+zE_(2,0).       (1)
```

Together with the two unchanged identity slices in the other colours, no
hypothetical witness exists for any parameter tuple.  This removes the
nonzero hypotheses from `GLD39` and closes every support-drop face of (1).
It subsumes `GLD24`--`GLD39` on their coordinate subcharts; those results
remain proved and separately replayable.

Broader cross arrays, further support entries, root-colour-changing blocks,
proper-secondary cells, and every weighted-permanent bridge remain open.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

Dependencies:

- [`GLD23`](FIXED_Q_DENSE_COLOUR_DEPENDENT_PRIVATE_PERMUTATION_EXCLUSION_THEOREM.md)
- [`GLD39`](FIXED_Q_DENSE_BIDIRECTED_SPUR_NONZERO_CHART_COMPLETION_THEOREM.md)

## Four exact two-row detectors

Write `P_(epsilon,r,s)=p_(epsilon,r,s)` for the root--residual variables in
the complete `81`-variable coefficient system.  Direct expansion over
`Z[u,v,w,z]` gives

```text
E(1022;0122):  -uP_(0,1,1)+uP_(1,1,1)= 0,
E(2122;2122):    -P_(0,1,1)+ P_(1,1,1)=-1,          (2)

E(1202;0212):  -wP_(0,2,1)+wP_(1,2,1)= 0,
E(2212;2212):    -P_(0,2,1)+ P_(1,2,1)=-1.          (3)
```

Thus (2) gives `0=u` and (3) gives `0=w`, with no assumptions on the other
parameters.

On the residual face `u=w=0`, two further complete row pairs give

```text
E(0100;1000):  -vP_(0,0,1)+vP_(1,0,1)= 0,
E(1222;1222):    -P_(0,0,1)+ P_(1,0,1)=-1,          (4)

E(0010;1000):  -zP_(0,0,1)+zP_(1,0,1)= 0,
E(1222;1222):    -P_(0,0,1)+ P_(1,0,1)=-1.          (5)
```

Hence (4) gives `0=v` and (5) gives `0=z` on that face.  Every omitted
retained-variable coefficient in (2)--(5) is exactly zero.

## Exhaustive support split

For any parameter tuple:

1. if `u!=0`, (2) is a contradiction;
2. otherwise, if `w!=0`, (3) is a contradiction;
3. on `u=w=0`, if `v!=0`, (4) is a contradiction;
4. on `u=w=v=0`, if `z!=0`, (5) is a contradiction;
5. if `u=v=w=z=0`, all three colour slices are the identity private
   matching, excluded pointwise by `GLD23`.

These five cases exhaust all `16` zero/nonzero support masks.

### Theorem

The entire affine family (1) is empty on the hypothetical witness locus.

### Proof

Apply the first applicable case in the exhaustive split above.  Each of the
first four cases is contradicted by an exact complete-system row relation;
the last case is the proved `GLD23` identity private-permutation chart.
`square`

## Scope ledger

```text
four-parameter affine coordinate family:             EMPTY;
all 16 off-diagonal support masks:                   EMPTY;
GLD24--GLD39 coordinate subcharts:     PROVED / REPLAYABLE;
broader nonprivate cross arrays:                       OPEN;
proper-secondary cells:                               OPEN;
weighted-permanent bridge:                            OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_affine_chart_completion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_bidirected_spur_affine_chart_completion.py
python claims/arbitrary-order/verify_fixed_q_dense_colour_dependent_private_permutation_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_bidirected_spur_nonzero_chart_completion.py
```

The primary checks the four sparse identities with the direct `945`-matching
engine.  The standalone no-import audit reconstructs recursive permanents,
derives all four left nullspaces without stored multipliers, and independently
enumerates the `16` support masks.  The all-zero endpoint is replayed through
the independent `GLD23` certificate census.
