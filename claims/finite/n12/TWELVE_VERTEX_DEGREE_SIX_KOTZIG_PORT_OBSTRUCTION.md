# Corrected order-twelve exact-degree-six Kotzig-port obstruction

## Status

This is a corrected finite audit of the pairwise-disjoint,
exact-degree-six branch.  It supersedes the legacy 15,478,610-port and
395-residual calculation, which used target-task labels as inherited
half-colours.  With the physical half-colours oriented correctly and the
balanced-bridge table imposed, every admissible order-twelve port
realization is already excluded by each of the six original potential
rays.

The finite result is subsumed by the arbitrary-order proof in
`ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`.  It is retained
as a nontrivial computational regression, not as the main proof.

## Corrected domain

The connected cubic catalogue has 85 isomorphism classes.  The required
distinguished perfect one-factorizations and propagated normal types give

```text
labelled Kotzig colourings:               336
labelled colouring/type cells:          2,688
cell-orbit representatives:               154
cell orbits with no admissible port cover: 109.
```

For a target-`c` task at the left endpoint, put `r=f_left(c)`.  A
reciprocal partner is a target-`r` task at the right endpoint with
`f_right(r)=c`, but the physical unit is `(r,c)`, not `(c,r)`.  It is
retained only if it survives all three balanced-bridge restrictions.
Exact-cover enumeration on the 45 feasible cell orbits gives

```text
representative admissible port realizations: 51,168
orbit-weighted labelled realizations:       860,250.
```

## Corrected exclusion

Every forced own-colour diagonal unit has zero value under the base
potential.  Every permitted optional diagonal unit and every corrected
physical port unit has strictly positive value.  For every one of the
51,168 representative architectures, each of the six colour-permuted
potentials finds a nonmonochromatic zero-potential colouring with one
forced diagonal perfect matching and no competing monomial.  Equivalently,
every success mask is `63`:

```text
success mask 63: 51,168
all other masks:      0
residuals:            0.
```

This is consistent with the arbitrary-order proof: Bogdanov's matching
theorem supplies a nonmonochromatic perfect matching in the properly
three-edge-coloured diagonal graph, and the positive unit potential makes
its induced coefficient a single nonzero monomial.

## Verification

The finite chain is reconstructed by:

```text
python scout_twelve_vertex_six_potential_cells.py
python count_twelve_vertex_port_cell_orbits.py
python audit_twelve_vertex_port_cell_orbits.py
python write_twelve_vertex_orbit_input.py
g++ -O3 -std=c++20 exhaust_twelve_vertex_six_potential_orbits.cpp
g++ -O3 -std=c++20 audit_twelve_vertex_six_potential_orbits.cpp
python compare_twelve_vertex_six_potential_orbit_audit.py
```

The two compiled enumerators use different exact-cover tie orders and
different matching-classification routines.  They agree cell by cell on
port counts, the all-`63` success-mask histogram, and independent hash
aggregates.  The separate quotient audit rebuilds the graph6 catalogue,
perfect matchings, distinguished colourings, normal-type propagation,
automorphism actions, orbit sizes, and stabilizers.

Canonical artifact hashes are recorded in `docs/research-notes.md` after a
fresh replay.

## Boundary

This finite audit addresses only order twelve under the
pairwise-disjoint, exact-degree-six hypotheses.  The arbitrary-order
theorem removes that complete branch, but overlapping selected matchings,
support degree at least seven, and the separate deeper-blocker branch
remain outside both results.
