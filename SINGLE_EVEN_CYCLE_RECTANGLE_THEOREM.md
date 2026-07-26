# Single `4k+2` cycle rectangle theorem

## Theorem

Let a three-colour equality support have:

- full blocks on one spanning cycle `F=C_n`;
- three pairwise edge-disjoint diagonal singleton perfect matchings
  `S0,S1,S2`;
- `n = 4k+2`.

Then the support cannot realize the Krenn--Gu target over any field.  In
particular, no order-14 equality support with full factor `C14` is a
witness.

## Crossing chord

The bipartition classes of `C_(4k+2)` both have odd size `2k+1`.  Every
perfect matching `S0` therefore contains an edge

```text
f = xz
```

joining the two bipartition classes: otherwise `S0` would separately
perfect-match two odd sets.  The singleton factors are disjoint from `F`,
so `x` and `z` are nonadjacent on the cycle.

The graph `F+f` has exactly three perfect matchings:

- the two alternating cycle matchings `A,B`;
- one matching `Q` that uses `f`.

Indeed, deleting the opposite-parity vertices `x,z` splits the cycle into
two even paths, each with a unique perfect matching.

## Four colouring corners

Give `f` singleton colour 0.  The union `S1 union S2` is a disjoint union
of even alternating cycles, so properly 2-colour it with colours 1 and 2.
Call this base colouring `b00`.  Form:

```text
b10: change x to colour 0
b01: change z to colour 0
b11: change both x and z to colour 0.
```

The first three colourings activate no singleton edge:

- every `S1`/`S2` edge is bichromatic unless one endpoint was changed to
  0, in which case it is still inactive;
- at most one endpoint of `f` has colour 0;
- no other `S0` edge has two colour-0 endpoints.

The target corner `b11` activates exactly `f`.  All four colourings are
nonmonochromatic.  Thus the first three forbidden amplitudes contain
exactly `A,B`, while the fourth contains exactly `A,B,Q`.

## Exponent rectangle

Let `r(b)` be the Laurent exponent difference between the monomials of
`A` and `B` at colouring `b`.  A full-cycle entry depends only on the
colours at the endpoints of its edge.  Since `x,z` are nonadjacent on
`F`, no full edge depends on both changed coordinates.  The mixed discrete
difference is therefore zero:

```text
r(b11) = r(b10) + r(b01) - r(b00).
```

Each of the three binomial equations says its monomial ratio is `-1`.
The coordinate sum `1+1-1` is odd, hence the transported ratio at `b11`
is also `-1`.  The `A` and `B` terms cancel in the target amplitude,
leaving the supported monomial of `Q` alone.  It is nonzero, a
contradiction.

## Order-14 audit

`verify_fourteen_vertex_c14_rectangle_theorem.py` independently:

- enumerates all 44,189 perfect matchings in `K14-C14`;
- checks that every one contains a bipartition-crossing chord;
- records the exact crossing-chord histogram
  `1:7875, 3:24885, 5:10850, 7:579`;
- reconstructs three support samples from different first-factor orbits;
- verifies all four singleton-activation sets and perfect-matching
  activities;
- checks the exact Laurent exponent rectangle entry by entry.

Run:

```text
python verify_fourteen_vertex_c14_rectangle_theorem.py
```

The output

```text
tmp/fourteen_vertex_c14_rectangle_theorem_verified.json
```

contains `"verified": true`.  The finite enumeration audits the order-14
instance; the `4k+2` statement itself is the analytic parity-and-rectangle
argument above.
