# Ten-vertex `C10` equality-family certificate

## Exact claim

For `n=10` and `d=3`, consider any support with:

- a 5-regular, 25-edge skeleton;
- ten full `3 x 3` blocks forming a spanning `C10`;
- fifteen diagonal singleton blocks forming three edge-disjoint perfect
  matchings, one per colour, on the complementary cubic graph.

No assignment of nonzero complex values to such a support realizes the
Krenn--Gu target.

This covers the complete `C10` equality architecture.  It does not by
itself cover other full-factor types, supports below the 105-entry equality
bound, non-5-regular exact-25 supports, or the global conjecture.

## Exhaustive catalogue

Fix the labelled cycle

```text
0-1-2-3-4-5-6-7-8-9-0.
```

There are 293 perfect matchings disjoint from its ten edges.  Exhausting
every unordered triple of pairwise edge-disjoint matchings gives 451,751
colour-unlabelled factorizations.  Quotienting by the 20 automorphisms of
the fixed cycle gives 23,204 support orbits:

```text
orbit size     number of orbits
1                            1
5                           86
10                       1,102
20                      22,015
total                   23,204
```

Across all 181,440 labelled ten-cycles and all six global colour
assignments, this represents 491,794,208,640 labelled coloured supports.

## Three-binomial transport contradiction

Every orbit has three forbidden binomial amplitudes on the same pair of
skeleton perfect matchings.  Dividing the two nonzero monomials in each
amplitude gives signed Laurent relations

```text
x^r1 = -1,    x^r2 = -1,    x^r3 = -1.
```

A fourth forbidden colouring has exactly three active matchings.  Two are
the transported pair and the third is a distinct supported matching.  The
audited exponent identity is

```text
r_target = r1 - r2 + r3.
```

Consequently `x^r_target=-1`, so the transported pair cancels in the target
trinomial.  Its third monomial is a product of supported nonzero entries and
survives alone.  The target forbidden amplitude therefore cannot vanish.

The sweep reused 17 fixed transport patterns and discovered 38 additional
patterns adaptively.  Of the 23,204 orbit certificates, 23,166 use a fixed
pattern and 38 use a discovered one.  Every stored identity has relation
signs `(1,-1,1)`.

## Independent audit

`verify_ten_vertex_c10_equality_family.py` independently:

1. regenerates all 293 eligible singleton matchings;
2. recounts all 451,751 edge-disjoint triples;
3. reconstructs the 20 cycle automorphisms;
4. verifies every canonical representative, orbit size, perfect-matching
   mask, disjointness, and total orbit coverage;
5. reconstructs every support skeleton and all its perfect matchings;
6. recomputes every stored colouring from its equation index;
7. checks the three binomial activities and target trinomial activity;
8. reconstructs the Laurent exponent vectors and verifies
   `r_target=r1-r2+r3`.

Pinned manifests:

```text
tmp/ten_vertex_c10_equality_support_orbits.json
SHA-256
  c129c732658a58a99994666dae34c403fdec8224feb69e809f93f6b5cfcfa42c

tmp/ten_vertex_c10_equality_support_transport_final2.json
SHA-256
  90832b84158522e5d84f9b9380505b96863dcbd1c06d6c4e25a42f6a4897ac67

tmp/ten_vertex_c10_equality_family_verified.json
SHA-256
  c7da2f3ffb8d165b7225710c3ce737462d3fe6ab42d09d9339700c01493fb756
```

With the bundled dependencies on `PYTHONPATH`, run:

```text
python claims/finite/n10/verify_ten_vertex_c10_equality_family.py --certificates tmp/ten_vertex_c10_equality_support_transport_final2.json
```

Success writes a final JSON containing `"verified": true`.
