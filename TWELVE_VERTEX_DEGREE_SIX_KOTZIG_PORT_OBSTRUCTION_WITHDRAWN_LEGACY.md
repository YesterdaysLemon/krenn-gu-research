# Withdrawn legacy order-twelve exact-degree-six Kotzig-port calculation

## Status

**WITHDRAWN.**  This calculation used target-task labels as inherited
half-colours and did not impose the balanced-bridge admissibility test on
the resulting physical port unit.  The counts and residual claims below
are retained only as an audit trail.  They are not a certificate.

The corrected finite theorem is
`TWELVE_VERTEX_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`.  The convention
error is isolated in `RECIPROCAL_PORT_ORIENTATION_CORRECTION.md`, and the
stronger arbitrary-order replacement is
`ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`.

## Withdrawn historical text

This is a finite theorem in the simultaneous balanced all-bridge branch
where:

1. the three chosen monochromatic matchings are pairwise edge-disjoint;
2. the diagonal-support graph has exact degree three and is their
   distinguished perfect one-factorization; and
3. the full physical support has exact degree six, so the remaining
   units form a simple reciprocal cubic port graph.

Under these hypotheses no order-twelve witness exists.  This does not
prove the Krenn--Gu conjecture: the overlapping-matching, higher-support-
degree, and deeper-blocker branches remain outside the theorem.

## Complete finite domain

The connected cubic graph catalogue at order twelve has 85 isomorphism
classes.  Exactly 31 classes admit at least one distinguished perfect
one-factorization whose three pairwise unions are Hamiltonian.  Exact
enumeration gives

```text
labelled distinguished Kotzig colourings:       336
propagated normal assignments per colouring:      8
labelled colouring/type cells:                 2,688.
```

The automorphism group of the underlying cubic graph and the six global
colour permutations act on these cells.  Canonicalizing the complete
domain under that action gives

```text
cell-orbit representatives:                      154
cell orbits with no reciprocal port graph:         4.
```

For each representative, the port graph is an exact cover of the 36
vertex-colour stubs by 18 reciprocal pairs, subject to:

1. no port edge is a diagonal edge;
2. no physical pair is repeated;
3. every vertex-colour stub occurs exactly once; and
4. the two half-colours satisfy both normal reciprocities.

Complete exact-cover enumeration gives

```text
representative reciprocal port realizations:  15,478,610
orbit-weighted labelled realizations:        281,720,460.
```

The labelled total is used only as a census.  Every amplitude
classification is performed on the 15,478,610 orbit representatives.

## The original six potential rays

For each architecture, enumerate every perfect matching made only from:

1. the 18 forced own-colour diagonal units; and
2. the 18 forced reciprocal port units.

For each of the six colour-permuted potentials, restrict to
nonmonochromatic colourings of minimum potential.  A colouring occurring
in exactly one guaranteed perfect matching gives an uncancellable
nonzero monomial and excludes the architecture.

The exact success histogram is

```text
number of successful original rays    architectures
0                                            395
1                                          1,266
2                                          4,754
3                                          8,522
4                                         33,641
5                                        118,323
6                                     15,311,709
total                                  15,478,610.
```

Thus the original six rays immediately exclude 15,478,215
architectures.  They leave exactly 395 representatives in 13 of the 154
cells.

## Complete admissible potential cone

`FULL_ADMISSIBLE_POTENTIAL_CONE_LEMMA.md` proves that the six original
potentials form a basis of the entire local neutral-potential space, but
their nonnegative coefficient orthant is only a proper subcone of the
admissible region.  The closure of the full region has six different
extreme rays

```text
(-4, 1, 1, 1, 6,-4)   (-4, 1, 6, 1, 1,-4)
( 1,-4, 1, 1,-4, 6)   ( 1,-4, 1, 6,-4, 1)
( 1, 6,-4,-4, 1, 1)   ( 6, 1,-4,-4, 1, 1).
```

A boundary extreme ray can assign zero weight to some optional diagonal
units, so it is refined lexicographically by the strict interior
direction `(1,1,1,1,1,1)`.  On each finite architecture this lexicographic
order is realized by an actual strictly admissible potential

```text
M times extreme_ray + (1,1,1,1,1,1)
```

for sufficiently large positive integer `M`.

Applying these six valid refinements to the 395 residuals gives

```text
number of successful full-cone rays    residuals
2                                              1
3                                              3
4                                             75
5                                            120
6                                            196
total                                        395.
```

Every residual is therefore exposed by at least two complete-cone
directions.  No residual remains, so the stated order-twelve branch is
excluded.

## Stronger maximal-support confirmation

There is a separate confirmation that does not rely on finding the
missing cone directions.  For each of the 395 original-ray residuals,
restore every optional off-diagonal diagonal-block unit permitted by the
balanced bridge table.  The maximal supports contain between 50 and 54
matrix units:

```text
maximal units    residual architectures
50                                      1
52                                      1
53                                    249
54                                    144.
```

In every maximal support there is a nonmonochromatic colouring with
exactly one compatible perfect matching, and all six units of that
matching are forced units.  Removing any subset of optional units
preserves that singleton.  Hence all 395 residuals are independently
excluded even without the full-cone refinement.

## Verification

The finite chain is reconstructed by:

```text
python tools/explore/scout_twelve_vertex_six_potential_cells.py
python tools/explore/count_twelve_vertex_port_cell_orbits.py
python claims/finite/n12/audit_twelve_vertex_port_cell_orbits.py
python tools/generate/write_twelve_vertex_orbit_input.py
g++ -O3 -std=c++20 exhaust_twelve_vertex_six_potential_orbits.cpp
python verify_full_admissible_potential_cone.py
python analyze_twelve_vertex_full_potential_cone.py
python analyze_twelve_vertex_six_potential_residuals.py
python audit_twelve_vertex_six_potential_residuals.py
```

The primary compiled pass and a separately written compiled audit use
opposite port-enumeration tie orders and different amplitude
classification strategies.  Their exact per-cell port counts, survivor
counts, all 64 success-mask counts, port hash aggregates, and
classification hash aggregates agree.  The Python audit separately
rebuilds every one of the 395 residual architectures, replays all six
old ray minima and all six full-cone refinements, and directly verifies
each maximal-support singleton.  A further independent quotient audit
uses separate graph6 and matching enumeration plus NetworkX
automorphisms to recover all 336 colourings, 2,688 cells, 154 orbits,
orbit sizes, and stabilizers.

Principal artifact hashes are:

```text
twelve_vertex_port_cell_orbits_counted.json
  e667305ffe495bf0e5aa52959d496b110be13a7b993a7cfcda0d4d253a1e87bf
twelve_vertex_port_cell_orbits_audited.json
  2c8dc39dd3d98385287c63c99cf105dde2e17139084d71ef62ce973a52b850da
twelve_vertex_port_cell_orbits_input.txt
  6c8313b452e409c0be8c7e31d661f3c698bebf53d7d007dac4132d86a956d89e
twelve_vertex_six_potential_orbits_exhausted.json
  9adab0f28ef7f0ba307471a1aa29a050fca7dfaf02080832b5f90b6db5002deb
twelve_vertex_six_potential_orbits_residuals.tsv
  1fc2dd5fa7df9a30e017f3ba1865a5d4dcae3f191be1034c13bc66edd53c3aeb
full_admissible_potential_cone_verified.json
  fe736abba2f73c4513b4bbfed3c77f7deffe10ed25c7b4ff7734ba6d9a16d016
full_admissible_potential_cone_audited.json
  ada946c100321cd3d84c4ff6e4a5a7786c826c2c300bd2f3ce685a26608ce0a6
twelve_vertex_full_potential_cone_analyzed.json
  2165471202f4929215190c7d5c02e92f3394b8f94e29197bd731200d4ee629a7
twelve_vertex_six_potential_residuals_analyzed.json
  b65a360ca1b5628f52557e263137e5d247c1ea259b8a361e88377b5a2cda78ae
twelve_vertex_six_potential_residuals_audited.json
  2448abdaef85d5d26ff888e16e21f52982233fd42c9e6ad42953e786d222c346
twelve_vertex_six_potential_orbits_independent_audit.tsv
  be61ae907ef534a18a1f7232f1eed255036344abb68edd4261b1fdf564442089
twelve_vertex_six_potential_orbits_independently_audited.json
  d84ea64eb949f97b664b347351812a0658b927a711e23deb6dc14b10f9c6c4d8
```

The order-twelve exclusion is finite.  It supplies evidence and a
stronger arbitrary-order grading lemma, but it must not be extrapolated
to larger orders or to the global conjecture without a separate proof.
