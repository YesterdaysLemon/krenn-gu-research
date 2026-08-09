# Ten-vertex `C4+C6` equality-family certificate

## Exact claim

For `n=10` and `d=3`, consider any support with:

- a 5-regular, 25-edge skeleton;
- ten full `3 x 3` blocks forming a spanning `C4+C6` 2-factor;
- fifteen diagonal singleton blocks forming three edge-disjoint perfect
  matchings, one per colour, on the complementary cubic graph.

No assignment of nonzero complex values to such a support realizes the
Krenn--Gu target.

This covers the complete `C4+C6` equality architecture.  It does not by
itself cover the `C10`, `C3+C7`, `C5+C5`, or `C3+C3+C4` full-factor types,
supports below the 105-entry equality bound, or the global conjecture.

## Exhaustive catalogue

Fix the labelled full factor

```text
C4: 0-1-2-3-0
C6: 4-5-6-7-8-9-4.
```

There are 292 perfect matchings disjoint from its ten edges.  Exhausting
every unordered triple of pairwise edge-disjoint matchings gives 446,592
colour-unlabelled factorizations.  Quotienting by the 96 automorphisms of
the fixed factor gives 4,903 support orbits:

```text
orbit size     number of orbits
8                            3
16                           1
24                          35
32                           1
48                         441
96                       4,422
total                    4,903
```

Across all 37,800 labelled `C4+C6` factors and all six global colour
assignments, this represents 101,287,065,600 labelled coloured supports.

## Direct amplitude fork

Every orbit has a three-amplitude contradiction.

For a suitable nonmonochromatic colouring, no singleton block is active.
The only four active matchings are the two alternating perfect matchings on
each even cycle.  The forbidden amplitude factors as

```text
nonzero monomial * (1 + x^r) * (1 + x^s),
```

so its required vanishing forces the alternating `C4` relation `x^r=-1` or
the alternating `C6` relation `x^s=-1`.

For each alternative, a second colouring agrees on the corresponding cycle
and has exactly five active matchings: the four full-only matchings plus one
non-full matching.  The chosen relation cancels the four full-only terms in
two pairs.  The fifth monomial contains a singleton variable, so it remains
nonzero in a distinct Laurent class.  That forbidden amplitude cannot
vanish.  Both alternatives are impossible.

The exhaustive search found between 17,954 and 40,550 such fork base
colourings per orbit; the final verifier needs and replays only one.

## Independent audit

`verify_ten_vertex_c4_c6_equality_family.py` independently:

1. regenerates all 292 eligible singleton matchings;
2. recounts all 446,592 edge-disjoint triples;
3. reconstructs the 96 factor automorphisms;
4. verifies every canonical representative, orbit size, disjointness, and
   total orbit coverage;
5. reconstructs every support skeleton and its perfect matchings;
6. checks the base and two target activities exactly;
7. verifies the Laurent relation on each paired monomial and the surviving
   singleton-containing term.

Pinned manifests:

```text
tmp/ten_vertex_c4_c6_equality_support_orbits.json
SHA-256
  6e939ddc3e17c8a1c0163a87c34d76144067390d61670579d302f612eab462a1

tmp/ten_vertex_c4_c6_equality_support_forks.json
SHA-256
  1b6cb62f51e5c3794813115332cd592404073ecc0cac72d710cb62bcef1a7e64

tmp/ten_vertex_c4_c6_equality_family_verified.json
SHA-256
  ffb260ddcb83a766eda0dab8a97c614589e36388c4f3e502cd469b4c6760ba0b
```

With the bundled dependencies on `PYTHONPATH`, run:

```text
python claims/finite/n10/verify_ten_vertex_c4_c6_equality_family.py
```

Success writes a final JSON containing `"verified": true`.
