# Order-14 `C4+C5+C5` equality-family certificate

## Theorem

There is no order-14, three-colour equality-architecture witness whose
full-block 2-factor has cycle type `C4+C5+C5`.

This is a complete finite theorem for that factor type.  It is not a proof
of the remaining order-14 factor types or of the global Krenn--Gu
conjecture.

## Exact exhaustion

Fix the labelled full factor

```text
C4 = (0,1,2,3)
C5 = (4,5,6,7,8)
C5 = (9,10,11,12,13).
```

The three singleton colour classes must be pairwise edge-disjoint perfect
matchings in the complement of this factor.  Exact enumeration gives:

```text
eligible singleton perfect matchings             44,195
individually one-term-free factors                 4,495
two-edge one-term sets                               200
matching forks of size 3                           5,600
matching forks of size 4                          63,600
matching forks of size 5                         114,600
size-3-fork-free safe factors                      3,295
full-factor orbits of those factors                   13
compatible seconds across representatives              4
compatible ordered thirds                              0
```

A two-edge one-term set activates a unique supported perfect matching in a
forbidden coefficient.  Every matching fork satisfies the arbitrary-order
cancellation-transport lemma in
[`MATCHING_FORK_TRANSPORT_LEMMA.md`](MATCHING_FORK_TRANSPORT_LEMMA.md).
Thus all eliminations are exact algebraic contradictions over the complex
numbers, not heuristic filters.

Only one of the 13 first-factor orbits admits any compatible second factor
after the one-term and size-three fork tests.  It admits four.  The
size-four and size-five catalogues eliminate every possible extension to a
third singleton colour class.

## Independent replay

Run:

```text
python verify_fourteen_vertex_c4_c5_c5_family.py
```

The verifier:

- reconstructs all 44,195 singleton factors by a separate bitmask recursion;
- independently recomputes the 128 activation counts of every factor;
- semantically replays all 200 one-term pairs and all 183,800 matching
  forks, checking their perfect-matching counts and forced full edge;
- regenerates the 1,600 full-factor automorphisms, all 3,295 surviving
  factors, and all 13 factor orbits;
- independently repeats the exact second- and third-factor compatibility
  calculation; and
- binds the replay to the raw obstruction catalogue by SHA-256.

The final audit is

```text
tmp/fourteen_vertex_c4_c5_c5_family_verified.json
```

and contains:

```json
{
  "verified": true,
  "status": "all_c4_c5_c5_equality_supports_closed",
  "compatible_ordered_thirds_across_orbits": 0
}
```
