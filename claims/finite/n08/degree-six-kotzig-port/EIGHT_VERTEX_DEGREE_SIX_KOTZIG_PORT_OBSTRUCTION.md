# Superseded order-eight exact-degree-six Kotzig-port calculation

## Status

**SUPERSEDED AND CORRECTED.**  The old 72-realization calculation below
used target-task labels as inherited half-colours and admitted reciprocal
units without checking the full bridge table.  It is not an authoritative
certificate.

With the corrected convention, both independent programs find:

```text
labelled Kotzig colourings:        18
normal-type assignments:         144
unused-matching / port tests:   2,016
admissible reciprocal covers:      0.
```

Thus the order-eight branch is still excluded, now because no admissible
physical port cover exists.  More strongly, the corrected port-potential
argument excludes this pairwise-disjoint exact-degree-six branch at every
even order; the authoritative theorem is
`ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`.

The orientation correction is
`RECIPROCAL_PORT_ORIENTATION_CORRECTION.md`.

## Withdrawn historical calculation

The generic killer theorem supplies, at each vertex `i` and target colour
`c`, a nonzero incident block

```text
A_i^c transpose(e_c).
```

The balanced all-bridge theorem then proves that the selected primary
vector `A_i^c` is one of the two coordinate vectors different from
`e_c`.  Writing that coordinate as `f_i(c)` turns the chosen block into
the off-diagonal singleton

```text
(f_i(c),c).
```

The three chosen killer neighbours are distinct.  In the exact-degree-six
branch they use three incident edges, while the three diagonal edges use
the other three.  Every killer edge is reciprocal at its other endpoint.
Thus the support splits as two edge-disjoint cubic graphs:

```text
D = the diagonal graph,
K = the reciprocal-primary-singleton port graph.
```

The diagonal matching-balance theorem supplies stronger information.
The three selected matchings `M_0,M_1,M_2` partition `D`; an edge in
`M_c` has exactly one nonzero diagonal colour, namely `c`; and every
pairwise union

```text
M_0 union M_1,
M_0 union M_2,
M_1 union M_2
```

is a Hamiltonian cycle.  The distinguished three-edge-colouring of `D`
is therefore a cubic perfect one-factorization.

For each normal-type bit `b_t`, the Hamiltonian cycle formed by the two
matchings other than `M_t` forces alternation.  Hence, for any fixed
distinguished colouring of `D`, each bit has only two possible global
assignments.  There are exactly

```text
2^3 = 8
```

compatible normal-type assignments.

## Order-eight reduction

On eight vertices, a 6-regular simple graph is the complement of a
perfect matching.  Once `D` is fixed, its 4-regular complement therefore
splits as

```text
complement(D) = K disjoint union U,
```

where `U` is one unused perfect matching.

There are six cubic isomorphism classes on eight vertices, five of them
connected.  The connected catalogue is `tmp/cub08.g6`; the independent
audit compares it by brute-force isomorphism with the connected part of
the six-class nauty catalogue `tmp/cub08_all_nauty.g6`.

Only two of the five connected cubic classes admit a distinguished
perfect one-factorization.  With colours labelled, the exact census is

```text
Kotzig colourings per connected class: 0,6,12,0,0
total labelled colourings:             18.
```

For every one of those 18 colourings, all eight normal-type assignments
and every possible unused matching `U` are enumerated.  Each edge of `K`
must pair a port task

```text
(i,c)
```

with the reciprocal task

```text
(j,f_i(c)),
```

and must satisfy

```text
f_j(f_i(c))=c.
```

Every vertex uses each of its three target colours exactly once.  The
complete census is

```text
unused-matching / port-graph tests:  2,016
reciprocal port realizations:            72.
```

## Unique-monomial contradiction

Fix one of the 72 realizations.  On a port edge, the reciprocal singleton
is forced nonzero.  On an edge of `M_c`, the diagonal unit `(c,c)` is
forced nonzero.  To make the test maximally permissive, also allow every
off-diagonal matrix unit that survives all three balanced bridge-plane
restrictions:

```text
(r,s)=(t,t), or r=f_i(t), or s=f_j(t)
for every target colour t.
```

The other two diagonal units on an `M_c` edge remain zero by the
cross-cofactor argument in the diagonal matching-balance theorem.

Now enumerate all `3^8` vertex colourings and all 105 perfect matchings of
`K_8`.  In each of the 72 port realizations there is a nonmonochromatic
vertex colouring for which:

1. exactly one perfect matching is compatible even with the maximally
   enlarged support; and
2. every matrix unit used by that matching is one of the forced nonzero
   diagonal or reciprocal-port units.

Deleting optional off-diagonal units cannot create a second compatible
matching and cannot remove the forced one.  Its monomial is therefore
nonzero and has nothing with which to cancel.  The corresponding target
coefficient is zero because the vertex colouring is nonmonochromatic.
This contradiction excludes all 72 realizations.

Consequently no order-eight exact-degree-six witness exists in the
pairwise-disjoint cubic diagonal branch.

## Independent audits

Run:

```text
python claims/finite/n08/degree-six-kotzig-port/explore_eight_vertex_degree_six_kotzig_ports.py
python claims/finite/n08/degree-six-kotzig-port/audit_eight_vertex_degree_six_kotzig_ports.py
```

The primary program propagates the three bit assignments along the
Hamiltonian pairwise unions and labels port edges by an edge-first exact
cover.

The second program does not import the first.  It:

1. implements a separate graph6 decoder;
2. checks all six cubic catalogue rows and their pairwise nonisomorphism;
3. identifies the same five connected classes by brute-force
   isomorphism;
4. reconstructs the eight type assignments using balanced four-subset
   masks rather than propagation;
5. pairs the 24 `(vertex,target)` port tasks directly; and
6. re-enumerates all mixed colourings and perfect matchings.

Both obtain

```text
labelled Kotzig colourings:                  18
normal-type assignments:                   144
unused-matching / port tests:             2016
reciprocal port realizations:                72
maximal-support unique-monomial conflicts:   72
survivors:                                    0
global conjecture resolved:               false
```

## Remaining boundary

At order eight, the simultaneous balanced all-bridge branch still retains:

- overlapping chosen monochromatic matchings;
- degree-seven support with non-primary extra edges;
- diagonal degree greater than three; and
- the separate deeper-blocker alternative.

At larger orders, cubic perfect one-factorizations and reciprocal port
graphs also remain.  The finite theorem above supplies a concrete
unique-monomial pattern to search for in those larger architectures, but
the present catalogue calculation alone does not establish an
arbitrary-order result.
