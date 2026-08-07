# Segre classification on every toric base orbit

## Status

This is an exact projective-geometric reduction over `C`.

The toric base boundary of the known pure rank-two component has

```text
12 divisor orbits,
26 edge orbits,
16 vertex orbits.                                    (1)
```

For each orbit, contract `P_4` through the three fixed base planes and
regard the result as a linear slice map

```text
Phi : (C^4)^* -> (C^2) tensor (C^2) tensor (C^2).    (2)
```

A nonzero pure four-tensor can occur only if `im(Phi)` meets the
`2 x 2 x 2` Segre variety.  Exact flattening-minor calculations give:

- six divisor images are disjoint from the Segre variety;
- four divisor images are secant lines, meeting it in two reduced
  points;
- one divisor image is tangent, meeting it in one double point;
- the internal `E=0` divisor image is another secant line;
- four edge images are secant lines;
- all other 22 edge images are disjoint;
- fifteen vertex images are disjoint and the last image is zero.

After setting aside the `E=0` divisor's already analysed canonical
marking, the Segre-capable genuine toric base planes are confined to
exactly

```text
five divisor orbits and four edge orbits.             (3)
```

Their all-rank `H31` plane orientations total 21: thirteen on divisors
and eight on edges.  There are no vertex cases.

This theorem itself is a plane-level reduction.  Its 21 residual cases
are now closed at the complete marked-fibre level, including both
first-plane charts and every binary extension direction:

- [`P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md`](../../../../../P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md)

The marked-plane distinction is explained and witnessed in
[`P5_H31_MARKED_BASIS_OPEN_BRANCH.md`](../../../../../P5_H31_MARKED_BASIS_OPEN_BRANCH.md).
The internal `E=0` divisor and first-plane Schubert boundary have since
been closed at complete marked-fibre level.  The second
diagonal-quadric pure-compression component, and any further component,
remain outside these theorems.

## Orbit invariance

The last three plane configurations are the monomial maps recorded in
[`P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md`](boundaries/P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md).
Inside a toric orbit, changing its torus parameters acts by invertible
diagonal transformations on source coordinates and target row bases.
It preserves:

1. whether `im(Phi)` meets the Segre variety;
2. intersection multiplicity and secant/tangent type; and
3. the common-three deletion ranks.

It therefore suffices to use the unit-coefficient representative of
each orbit.

## Divisor classification

For the eleven genuine base-boundary normals:

| type | normals |
| --- | --- |
| Segre-disjoint | `(-1,0,1)`, `(0,-1,0)`, `(0,0,1)`, `(0,1,-1)`, `(1,-1,0)`, `(1,0,0)` |
| secant | `(-1,1,0)`, `(0,0,-1)`, `(0,1,0)`, `(1,0,-1)` |
| tangent | `(0,-1,1)` |

The internal normal `(-1,0,0)`, corresponding to `E=0`, is secant.

For a secant representative, coordinates `(z_0,z_1)` on
`im(Phi)` reduce all Segre flattening minors to

```text
z_0^2-z_1^2=0,                                      (4)
```

up to a nonzero scalar and an invertible coordinate change.  The two
pure directions are `z_0=+z_1` and `z_0=-z_1`.

For the tangent divisor `(0,-1,1)`, the restriction is

```text
z_0^2=0,                                             (5)
```

so `z_0=0` is a double pure direction.

For each disjoint divisor the nonzero restricted equation is a square
of the only image coordinate, or an equivalent anisotropic expression
with no nonzero projective solution.  Thus no first plane can turn the
four-tensor into a nonzero pure tensor there.

## Lower toric orbits

The only Segre-capable edge orbits are the intersections

```text
(-1,0,0) with (-1,1,0),   all-rank q={0,2};
(-1,0,0) with (0,0,-1),   all-rank q={2,3};
(-1,1,0) with (0,1,0),    all-rank q={0,2};
(0,0,-1) with (1,0,-1),   all-rank q={2,3}.          (6)
```

Every edge in (6) is secant.  The other 22 edge images are disjoint
from the Segre variety.

No vertex orbit supports a nonzero pure slice.  Consequently (3) and
(6) include every toric base specialization; there is no unexamined
lower-dimensional escape.

## Exact frontier count

The five genuine Segre-capable divisors have all-rank plane
orientations

```text
(-1,1,0): q={0,2};
(0,-1,1): q={0,1,3};
(0,0,-1): q={2,3};
(0,1,0):  q={0,1,2};
(1,0,-1): q={1,2,3}.                                (7)
```

This gives thirteen divisor/orientation pairs.  The four edges in (6)
give eight more.  Hence the exact Segre-capable toric **plane**
frontier is

```text
13+8=21                                             (8)
```

all-rank orbit/orientation pairs, before imposing the neighbouring
`Delta_2` and ternary lift equations.

## Verification

Run:

```text
python claims/p4/classifications/pair-geometry/pure-rank-two/verify_p4_pure_rank_two_toric_slice_segre.py
python claims/p4/classifications/pair-geometry/pure-rank-two/audit_p4_pure_rank_two_toric_slice_segre.py
```

The primary verifier reconstructs the full face lattice, builds every
slice map, and restricts the Segre flattening minors exactly.  The
independent audit rebuilds the face lattice and counts projective pure
directions over `F_5`, which distinguishes disjoint, tangent, and
secant lines.  Neither verifier enumerates local maps or
Grassmannians.
