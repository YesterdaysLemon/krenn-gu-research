# No `H31` lift on the first-plane Schubert divisor

## Status

This is an exact characteristic-zero obstruction.

The known five-dimensional pure-compression component is a
two-dimensional linear first-plane fiber over a coupled three-plane
base.  The preferred-chart boundary

```text
Delta_0(01)=0
```

is the line at infinity of that fiber.  For the displayed marked row
normal form, every nonzero point of this Schubert divisor for which the
other three preferred Pluecker coordinates remain nonzero is
incompatible with an `H31` pure/`Delta_2` pencil, in all four
distinguished-source orientations.

This canonical-section result has since been upgraded to a complete
exclusion of the marked-basis fibre over those planes in
[`P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md`](../../../../P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md).
Kernel-row shifts preserve the plane and pure deletion but change the
neighbouring `Delta_2` equations; the newer theorem includes all of
them.
At the level of plane geometry, the other Schubert boundary is the
toric base boundary

```text
Delta_1(12) Delta_2(12) Delta_3(03)=0,
```

including its intersections with the divisor treated here.  Its
genuine toric marked-basis fibres have since been excluded in
[`P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md`](../toric-marked-fibre/P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md).
The internal `E=0` divisor has since been closed at complete
marked-fibre level.  A second pure-compression component has since been
proved separately; this first-component Schubert theorem does not
address it.

## Fiber-at-infinity normal form

Use the preferred component-chart parameters `h,n!=0` and `a,d,e`.
Put `a=tA`, `d=tD` and let `t` tend to infinity, with `(A,D)!=(0,0)`.
The first plane tends to

```text
span{
  (0,0,1,H),
  (-D/H,A,A N E,D N)
},                                                     (1)
```

where `H,N!=0` and `E` is arbitrary.  Its Pluecker coordinates are

```text
(0,D/H,D,-A,-HA,N(D-AHE)).                            (2)
```

Together with the other three preferred-chart planes, direct permanent
expansion gives

```text
2H(x_0+AEN y_0)(EN x_1+y_1)x_2x_3.                  (3)
```

After binary target-basis changes, take

```text
alpha_0=(0,0,1,H),
 beta_0=(-D/H,A,0,N(D-AEH)),

alpha_1=(0,0,1,H),
 beta_1=(E,1,-EN,-EHN),

alpha_2=(0,1,0,HNE),
 beta_2=(-1/N,0,1,0),

alpha_3=(1,0,N,0),
 beta_3=(0,0,-1/H,1).                                (4)
```

The only nonzero binary coefficient is then

```text
AAAA=2H.                                               (5)
```

## Mixed-extension strata

For distinguished source coordinate `q`, let `N_q` be the usual
`14 x 8` mixed binary-extension matrix.

### `A E D !=0`

For `q=0,1,2`, the mixed kernel kills the `BBBB` diagonal.  For `q=3`,
write its two-dimensional kernel coordinates as `(t,u)`.  The
diagonals are nonzero only if

```text
A u(t+EHN u)!=0.
```

The mode-three one-marked map has determinant

```text
8 A H^2 u^2(t+EHN u)/N^3.                            (6)
```

### `A!=0`, `E=0`

The only binary survivors occur for `q=0,2,3`.

For `q=0`, the diagonal conditions force `t u!=0`, and a mode-three
minor is

```text
-8 A H^3 t u^2.                                      (7)
```

For `q=2`, use kernel coordinates `(t,u,v)`.  The two diagonals are
nonzero exactly when

```text
v S!=0,
S=A H t+D H N v+D N u.
```

A mode-three minor is

```text
8 H^4 v^2 S/N^3.                                     (8)
```

For `q=3`, the diagonal conditions again force `t u!=0`, and a
mode-three minor is

```text
8 A H^2 t u^2/N^3.                                   (9)
```

These formulas include the intersection `D=0`.

### `A E !=0`, `D=0`

The new survivor beyond the `q=3` case is `q=2`.  With kernel
coordinates `(t,u)`, the diagonal conditions are

```text
u(t+H u)!=0,
```

and a mode-three marked minor is

```text
-8 A E H^5 u^2(t+H u)/N^2.                          (10)
```

### `A=0`

Now `D!=0`.  If `E!=0`, every mixed kernel kills one diagonal.  If
`E=0`, only `q=2` survives.  Its diagonal conditions are

```text
u(t+H u)!=0,
```

and a mode-two marked minor is

```text
-8 D^2 H^2 N^2 u^2(t+H u).                          (11)
```

The four cases exhaust `(A,D)!=(0,0)`.

## Ternary contradiction

Each displayed determinant is nonzero under exactly the corresponding
binary `Delta_2` conditions.  The third target row at that mode must
therefore vanish on the neighbouring hyperplane and be supported only
on the distinguished source coordinate.

The one-marked map on the pure hyperplane has a nonzero entry in that
coordinate in every case.  Hence the third row vanishes globally,
contradicting rank three of the full local map.  This proves the
obstruction.

## Verification

Run:

```text
python claims/p5/h31/component-fiber-infinity/verify_p5_h31_component_fiber_infinity.py
python claims/p5/h31/component-fiber-infinity/audit_p5_h31_component_fiber_infinity.py
```

The primary verifier derives (1)--(5), reconstructs every mixed-kernel
stratum, and checks (6)--(11) symbolically.  The independent audit uses
a dynamic-programming permanent and modular row reduction over `F_5`
and `F_7`; it checks every boundary parameter tuple and every
projective binary extension with two nonzero diagonals.  No ambient
local maps or Grassmannians are enumerated.
