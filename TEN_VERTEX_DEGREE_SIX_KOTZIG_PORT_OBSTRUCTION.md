# Superseded order-ten exact-degree-six Kotzig-port calculation

## Status

**SUPERSEDED AND CORRECTED.**  The old 547,434-realization calculation
below paired target tasks correctly but emitted them as inherited
half-colours and did not impose physical-unit admissibility.  Its residual
and path/cycle claims are withdrawn.

The corrected primary and independent enumerators agree on:

```text
connected cubic classes:                  19
labelled Kotzig colourings:              102
normal-type assignments:                 816
admissible reciprocal port realizations: 374,544
identity-potential contradictions:       374,544
residuals:                                      0.
```

The finite exclusion therefore survives with no second-stage residuals.
It is subsumed by the arbitrary-order proof in
`ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`; the exact
convention correction is
`RECIPROCAL_PORT_ORIENTATION_CORRECTION.md`.

## Withdrawn historical calculation

The diagonal graph `D` is a connected cubic graph with a distinguished
proper three-edge-colouring

```text
D = M_0 disjoint union M_1 disjoint union M_2
```

such that each pairwise union is Hamiltonian.  The exact nauty command

```text
geng -cq -d3 -D3 10
```

gives 19 connected cubic isomorphism classes on ten vertices.  Ten of
those classes admit at least one distinguished colouring of the required
kind.  With the three matching colours labelled, the complete census is

```text
connected cubic classes:                19
labelled Kotzig colourings:             102
compatible normal-type assignments:    816.
```

For each distinguished colouring, the three bit-flip Hamiltonian cycles
leave exactly two choices per normal-type bit and hence eight assignments.

The port graph `K` is simple, cubic, edge-disjoint from `D`, and uses each
local target colour exactly once at every vertex.  A task `(i,c)` can be
paired with `(j,f_i(c))` only when

```text
f_j(f_i(c)) = c.
```

Direct exact-cover enumeration of the 30 coloured port tasks gives

```text
reciprocal cubic port realizations: 547,434.
```

No sampling or numerical weight solving occurs in this census.

## Minimum-potential split

Every forced own-colour diagonal unit has potential zero.  Every optional
off-diagonal unit on `D` has strictly positive potential.  The three
monochromatic matchings and at least one nonmonochromatic matching in `D`
have potential zero, so a minimum-potential nonmonochromatic guaranteed
colouring has potential at most zero.

The replacement argument in the arbitrary-order theorem proves that no
optional `D` unit can contribute to such a minimum coefficient.  It is
therefore enough at this stage to enumerate perfect matchings in the
30-unit guaranteed graph:

```text
15 forced own-colour units on D,
15 forced reciprocal singleton units on K.
```

The complete minimum-layer census is

```text
port realizations:                          547,434
with a unique minimum-layer colouring:      547,042
without a unique minimum-layer colouring:       392.
```

Here “with a unique” means that at least one minimum-potential
nonmonochromatic colouring has exactly one guaranteed perfect matching.
Its monomial is nonzero, the target coefficient is zero, and optional
`D` units are absent from that coefficient by the potential theorem.
Those 547,042 realizations are therefore excluded immediately.

## The 392 exact binomials

Every one of the remaining 392 realizations has exactly:

```text
one minimum-potential nonmonochromatic colouring,
two guaranteed perfect matchings inducing it.
```

The guaranteed filtered graph has maximum degree two.  In all 392 cases
its sole cyclic component is a four-vertex alternating `D/K` cycle; the
two matchings differ on that cycle.  The sum of the port-edge potentials
around the cycle is zero, as required by the arbitrary-order
path/cycle-factorization theorem.  Thus the minimum coefficient is one
genuine zero-potential binomial.  This binomial can in principle cancel,
so minimum-layer multiplicity alone does not exclude these cases.

The potential is not unique.  Relabelling the three colours gives the
six valid positive potentials in `SIX_PERMUTED_POTENTIALS_LEMMA.md`.
Under at least four of the five nonidentity potentials, every one of the
392 identity residuals has a minimum-potential nonmonochromatic colouring
with exactly one guaranteed matching.  More precisely:

```text
identity residuals exposed by four other potentials: 270
identity residuals exposed by all five:               122
surviving all six potentials:                           0.
```

The transposition fixing colour 0 exposes 382 residuals; the
transposition exchanging colours 0 and 1 exposes the remaining ten.
Thus all 392 are already excluded within certified minimum layers.

As a separate stronger-support check, for each residual architecture add
every optional
off-diagonal unit on every `D` edge that is permitted by all three
balanced bridge restrictions.  This is the maximally permissive support:
an actual witness can only delete some of these optional units.

Enumerating every coloured perfect-matching monomial in that maximal
support finds, in each case, a nonmonochromatic colouring with:

1. exactly one compatible matching monomial even in maximal support; and
2. every unit of that matching forced nonzero, either an own-colour
   diagonal unit or a reciprocal primary singleton.

Deleting optional units cannot remove the forced monomial and cannot
create a cancellation partner.  Hence each of the 392 residual
architectures also contradicts its zero target coefficient.

Consequently no order-ten exact-degree-six witness exists in the
pairwise-disjoint cubic diagonal branch.

## Programs and independent replay

Run:

```text
python explore_ten_vertex_degree_six_kotzig_ports.py
python analyze_ten_vertex_degree_six_kotzig_port_survivors.py
python analyze_ten_vertex_permuted_potential_survivors.py
python audit_ten_vertex_permuted_potential_survivors.py
python audit_ten_vertex_degree_six_kotzig_ports.py
```

The primary program propagates the normal-type bits along the Hamiltonian
pairwise unions, pairs reciprocal port stubs with an edge-first exact
cover, enumerates guaranteed perfect matchings, and records the complete
minimum-potential census.

The survivor analyzer reconstructs all 392 residual architectures,
checks their exact two-term minimum coefficients and four-vertex
zero-potential cycles, enlarges every diagonal block independently, and
finds the forced unique monomial in maximal support.

The two permuted-potential programs independently relabel all normal
maps, check zero potential on 35,280 diagonal transitions and strict
positivity on 33,660 optional transitions, and recompute all six minimum
layers of all 392 identity residuals.

The independent audit imports neither program.  It separately:

1. decodes and validates the 19-row graph6 catalogue;
2. lists perfect matchings and distinguished one-factorizations directly;
3. reconstructs normal types from balanced five-subset masks;
4. pairs reciprocal `(vertex,target)` tasks in a different order;
5. recomputes all 547,434 minimum layers;
6. identifies the same 392 exact binomial residuals; and
7. re-enumerates their maximal optional support.

All machine-readable outputs retain

```text
"global_conjecture_resolved": false
```

Exact SHA-256 bindings are recorded in `RESEARCH_NOTES.md`.

## Remaining boundary

The finite result leaves open:

- pairwise-overlapping selected monochromatic matchings;
- exact-degree-six cases outside the simultaneous balanced all-bridge
  normal form;
- support degree seven or larger;
- the same pairwise-disjoint Kotzig/port architecture on fourteen or more
  vertices; and
- the separate deeper-blocker alternative.

The arbitrary-order residual has nevertheless been narrowed to
zero-potential alternating `D/K` cycle binomials.  The later
`FULL_ADMISSIBLE_POTENTIAL_CONE_LEMMA.md` and
`TWELVE_VERTEX_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md` extend the finite
exclusion through order twelve.
