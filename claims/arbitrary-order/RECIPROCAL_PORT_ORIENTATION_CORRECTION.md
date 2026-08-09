# Reciprocal-port target/half-colour correction

## Status

This note corrects the finite Kotzig/port pipeline.  The arbitrary-order
balanced-bridge and diagonal-matching structural theorems are unaffected.
Earlier order-eight, order-ten, order-twelve, and exploratory
order-fourteen port-amplitude artifacts were withdrawn.  The order-eight,
order-ten, and order-twelve canonical artifacts have now been regenerated
with this convention and independently replayed.  The old order-fourteen
scouts remain withdrawn because the arbitrary-order theorem makes their
finite continuation unnecessary.

## Target tasks versus inherited colours

At a vertex `u`, the primary killer for target colour `c` is the singleton
matrix unit

```text
(f_u(c), c)
```

on an oriented edge `uv`.  Put `r=f_u(c)`.  The same physical singleton is
reciprocal at `v` exactly when

```text
f_v(r)=c.
```

Thus the exact-cover tasks paired across the edge are

```text
(u,c) and (v,r),
```

but the inherited half-colours on the oriented edge are

```text
(r,c).
```

They are swapped.  The legacy finite code paired the target tasks
correctly but then emitted `(c,r)` as the inherited colouring.

There is a second necessary check.  Reciprocity does not imply that the
physical singleton survives all three balanced-bridge restrictions.  The
unit `(r,c)` must still satisfy, for every target `t`,

```text
(r,c)=(t,t), or r=f_u(t), or c=f_v(t).
```

Across all eight normal types and all ordered endpoint pairs there are 96
reciprocal target-task transitions.  Exactly 72 have an admissible
swapped physical unit; the other 24 are forbidden by the bridge table.
Only 18 of the 96 legacy unswapped units happen to be allowed.

## Exact diagnostic

For endpoint types

```text
f_u=(2,0,1),  f_v=(2,2,0),
```

the legacy unit `(2,1)` is forbidden by the balanced-bridge table, while
the correctly swapped unit `(1,2)` is allowed.  This record appeared in
the archived order-twelve residual stream and directly exposed the
orientation mismatch.

Scanning all 395 archived residual architectures gave 7,110 stored port
units.  Only 1,546 legacy units survived the bridge table, and every one
of the 395 architectures contained a forbidden stored unit.  Merely
swapping without imposing admissibility was still insufficient: 391
architectures retained at least one reciprocal-but-forbidden unit.

## Verification and consequence

Run:

```text
python verify_reciprocal_port_orientation.py
```

The corrected generators now:

1. pair the target tasks `(c,r)`;
2. emit inherited half-colours `(r,c)`; and
3. reject the edge unless that physical unit survives the exact
   balanced-bridge table.

The physical-state involution asserted in the earlier
`STATE_LIFT_CYCLE_FIBRE_LEMMA.md` also fails under the corrected convention:
the three target killers at a vertex need not use the three inherited
colours once each, because the map `c -> f_u(c)` need not be a
permutation.  That lemma is therefore withdrawn rather than patched by
renaming states.

No global proof or counterexample follows from this correction.  Its
purpose is to restore a sound finite boundary before the search
continues.
