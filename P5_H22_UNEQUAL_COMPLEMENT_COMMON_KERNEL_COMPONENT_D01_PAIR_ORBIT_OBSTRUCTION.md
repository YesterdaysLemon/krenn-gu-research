# Generic weighted-`H22` obstruction on the component-22 `D01` pair orbit

## Status

**Exact characteristic-zero partial theorem.**  Over the generic normalized
component-twenty-two chart, the entire finite `D01` weighted binary-incidence
scheme is excluded by a three-branch radical decomposition and branchwise
rank-four one-marked minors.  The homogeneous weight-at-infinity endpoint is
the already closed marked-`H31` deletion of coordinate one.

This does **not** close the full generic weighted-`H22` fibre.  The `D23`
contraction maps by the source swap `(02)(13)` to a complementary-support
conjugate chart, not back to the same `D01` pair orbit under its stabilizer.
That second pair orbit remains **UNKNOWN**.  A direct `D23` two-minor
elimination timed out and is not theorem evidence.  Special/projective
component fibres and the global Krenn--Gu conjecture also remain
**UNRESOLVED**.

## Exact survivor decomposition

Use the normalized component basis from
[`P4_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT.md`](P4_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT.md)
over `K=C(A,R,D)`.  Put

```text
s=2A+R
```

and let `rho` be the finite `D01` weight.  Normalize the all-alpha diagonal
to one and invert the all-beta diagonal.  Eliminating the eight extension
entries gives a nonreduced twelve-generator marking ideal `J`.  Its radical
has exactly three prime branches:

```text
P1=<2h3-s,h2,Dh0+1,
    2R(A+R)(rho-1)h1+(rho+1)(s rho-(2A+3R))>,

P2=<2h3-s,h1,Dh0+1,
    R(rho-1)(s rho-R)h2+(rho+1)(s rho-(2A+3R))>,

P3=<h1,h2,F3>.                                    (1)
```

Here

```text
F3=
 8A^3 D h0 rho-8A^3 D h0-2A^3 D rho+2A^3 D+6A^3 rho-6A^3
+4A^2 D R h0 rho-20A^2 D R h0-A^2 D R rho+5A^2 D R
+8A^2 D h0 h3 rho-8A^2 D h0 h3-2A^2 D h3 rho+2A^2 D h3
+3A^2 R rho-15A^2 R+6A^2 h3 rho-6A^2 h3
-2A D R^2 h0 rho-10A D R^2 h0+2A D R^2
+8A D R h0 h3 rho-8A D R h0 h3-2A D R h3 rho+2A D R h3
-2A R^2 rho-8A R^2+6A R h3 rho-6A R h3
-D R^3 h0 rho-D R^3 h0+2D R^2 h0 h3 rho-2D R^2 h0 h3
-R^3 rho-R^3+2R^2 h3 rho-2R^2 h3.                (2)
```

The distinction between `J` and its radical is preserved: the standard basis
of `J` has size twelve, while the intersection of the three prime branches
has size ten.  Only their common point set is used below.

## Branchwise fixed-minor cover

Let `N_j` be the `8 x 4` one-marked matrix in mode `j`, with ternary rows in
lexicographic order `000,001,...,111`.  Adjoin the saturated binary equations
and the following two minors on each branch:

```text
P1: det N0[0137], det N3[0127],
P2: det N3[0127], det N2[0157],
P3: det N0[0137], det N3[0137].                   (3)
```

For `P3`, it is enough to impose only `h1=h2=0`; the equation `F3=0` is not
needed.  Each of the three exact ideals in (3) is the unit ideal over
`K[rho]`.  No value of `rho` is inverted, so exceptional finite weights are
included.  Therefore every genuine finite `D01` binary candidate makes at
least one one-marked ternary map have rank four and cannot be an `H22` lift.

At `rho=infinity`, the projected rows are precisely those obtained by deleting
source coordinate one.  The exact component-twenty-two `H31` theorem already
excludes that endpoint.

The two rational points recorded in
[`P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_SURVIVOR_RECONNAISSANCE.md`](P5_H22_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT_SURVIVOR_RECONNAISSANCE.md)
lie on `P3`; their eight nonzero one-marked minors are consistent witnesses,
not substitutes for the branchwise unit-ideal proof.

## Replay

```text
uv run --with sympy python verify_p5_h22_unequal_complement_common_kernel_component_d01_pair_orbit_obstruction.py
uv run --with sympy python audit_p5_h22_unequal_complement_common_kernel_component_d01_pair_orbit_obstruction.py
```

The primary verifier computes the exact radical decomposition and all three
unit ideals.  The independent audit specializes every branch over `Q` and
reconstructs the fixed-minor covers without importing the primary verifier.
No finite-field computation is used.
