# Toric boundary fan of the known pure rank-two component

## Status

This is an exact polyhedral and Grassmannian reduction over `C`.

After separating the first-plane fiber, the last three planes of the
known pure-compression component form a coupled projective toric
threefold.  Its boundary has twelve toric divisors.  One is the
internal `E=0` divisor in the preferred component chart.  The other
eleven are exactly the base-Schubert boundary at the level of plane
geometry.

For `H31`, the complete rank-one gate theorem immediately excludes 21
of the 44 divisor/distinguished-source pairs, independently of marked
basis.  The all-rank **plane** candidates are contained in 23 divisor
orientations, together with their lower-dimensional intersections.

This theorem itself is a reduction, not an exclusion of those 23
divisor strata.  The later Segre slice theorem reduces all genuine
toric base specializations to 21 plane/orientation cases, and the
complete marked-fibre theorem now excludes all 21:

- [`P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md`](P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md)
- [`P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md)

The full marked fibre over the internal `E=0` divisor has since been
excluded in
[`P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md).
A second pure-compression component has since been proved in
[`P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md`](claims/p4/components/diagonal-quadric/P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md);
it is outside the toric geometry of this theorem.  Its generic marked
fibre and the existence of any further component remain open.

## Three monomial plane maps

Use Pluecker coordinates in the order

```text
01,02,03,12,13,23.
```

On the dense base torus with coordinates `(E,H,N)`, the last three
planes have nonzero coordinates

```text
P_1: 02=E,   03=EH,   12=1,   13=H;
P_2: 01=N^-1, 03=EH,  12=1,   23=-EHN;
P_3: 02=-H^-1, 03=1,  23=N.                         (1)
```

Their exponent polytopes in the character lattice with coordinates
`(E,H,N)` are

```text
Q_1=conv{(1,0,0),(1,1,0),(0,0,0),(0,1,0)},
Q_2=conv{(0,0,-1),(1,1,0),(0,0,0),(1,1,1)},
Q_3=conv{(0,-1,0),(0,0,0),(0,0,1)}.                 (2)
```

The closure of the diagonal torus in the product of the three
Pluecker spaces is the projective toric variety governed by the common
normal fan, equivalently the normal fan of

```text
Q=Q_1+Q_2+Q_3.                                      (3)
```

The Minkowski sum has 28 lattice points and twelve facets.

## Facet and support table

For an outward primitive facet normal `rho`, retain in each plane the
Pluecker coordinates whose exponent maximizes pairing with `rho`.
The exact table is:

| `rho` | `P_1` support | `P_2` support | `P_3` support | all-rank distinguished `q` |
| --- | --- | --- | --- | --- |
| `(-1,0,0)` | `12,13` | `01,12` | `02,03,23` | `0,2,3` |
| `(-1,0,1)` | `12,13` | `12,23` | `23` | `0` |
| `(-1,1,0)` | `13` | `01,03,12,23` | `03,23` | `0,2` |
| `(0,-1,0)` | `02,12` | `01,12` | `02` | `3` |
| `(0,-1,1)` | `02,12` | `12,23` | `02,23` | `0,1,3` |
| `(0,0,-1)` | `02,03,12,13` | `01` | `02,03` | `2,3` |
| `(0,0,1)` | `02,03,12,13` | `23` | `23` | `0,1` |
| `(0,1,-1)` | `03,13` | `01,03` | `03` | `1,2` |
| `(0,1,0)` | `03,13` | `03,23` | `03,23` | `0,1,2` |
| `(1,-1,0)` | `02` | `01,03,12,23` | `02` | `1,3` |
| `(1,0,-1)` | `02,03` | `01,03` | `02,03` | `1,2,3` |
| `(1,0,0)` | `02,03` | `03,23` | `02,03,23` | `1,2` |

The first row, `rho=(-1,0,0)`, is `E=0`.  It lies inside the preferred
Grassmann chart.  Its canonical marked section is excluded by
[`P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md`](P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md);
its full marked-basis fibre has since been excluded in
[`P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md).

## Gate criterion

Deleting distinguished source coordinate `q` leaves a rank-two pair in
a plane exactly when at least one surviving Pluecker coordinate avoids
`q`.  The relevant coordinate sets are

```text
q=0: {12,13,23},
q=1: {02,03,23},
q=2: {01,03,13},
q=3: {01,02,12}.                                    (4)
```

Apply (4) to each of `P_1,P_2,P_3` in the table.  If any plane fails,
its common-three restriction has rank one.  The complete primary and
secondary gate theorems then exclude the `H31` lift.

Across the eleven genuine boundary divisors there are

```text
44 total divisor/orientation pairs,
21 gate-excluded pairs,
23 all-rank pairs.                                  (5)
```

Specialization to a smaller torus orbit can only delete supported
Pluecker coordinates.  Thus a gate-excluded generic divisor
orientation remains excluded on its entire closure.  The residual
known-component problem is therefore contained in the closures of the
23 all-rank pairs listed in the last column.

## Verification

Run:

```text
python verify_p4_pure_rank_two_component_toric_boundary.py
python audit_p4_pure_rank_two_component_toric_boundary.py
```

The primary verifier constructs the three exponent configurations,
forms the Minkowski sum, recovers all primitive facet normals by exact
integer arithmetic, and checks every support and gate entry.  The
independent audit reconstructs the convex hull facets using a separate
supporting-plane implementation and rechecks the deletion ranks.  This
is a finite polyhedral calculation, not an enumeration of tensor maps
or Grassmannians.
