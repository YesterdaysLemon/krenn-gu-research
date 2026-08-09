# Fourteen-vertex `C3+C4+C7` equality-family certificate

## Status

**Theorem.**  No order-14, three-colour equality support whose full
2-factor has type `C3+C4+C7` realizes the Krenn--Gu target over the complex
numbers.

Equivalently, fix full nonzero `3 x 3` blocks on

```text
C3 = 0-1-2-0,
C4 = 3-4-5-6-3,
C7 = 7-8-9-10-11-12-13-7.
```

No choice of three pairwise edge-disjoint, colour-labelled diagonal
singleton perfect matchings disjoint from that factor can be a witness.

This is a complete finite family theorem.  It is not a proof of the global
Krenn--Gu conjecture or of every order-14 equality factor type.

## Two exact obstructions

The exhaustion uses only two value-free mechanisms.

### One-term sets

If a singleton matching `T` makes `F union T` have exactly one perfect
matching, the exact-activation lemma supplies a nonmonochromatic colouring
that activates exactly `T`.  Its forbidden amplitude is one supported
nonzero monomial, a contradiction.

### Matching forks

If removing one edge `f=xz` from a singleton matching `U` leaves a nonempty
perfect-matching family `A`, restoring `f` adds exactly one matching `Q`,
and every member of `A` pairs `x` to one common full-edge neighbour, the
adjacent exact-activation lemma gives a cancellation-transport
contradiction.  See
[`MATCHING_FORK_TRANSPORT_LEMMA.md`](../../../MATCHING_FORK_TRANSPORT_LEMMA.md).

## Stage 1: classify one colour factor

There are exactly 44,226 perfect matchings of `K14-F`, hence 44,226
possible singleton factors for one colour.

For every factor, all 128 subsets are checked.  The exact number of perfect
matchings in `F union T` is reconstructed by a subset zeta transform from
the unique/full-cycle completion counts.  The complete classification by
the number `k` of triangle-to-`C4` singleton edges is:

```text
k   individually safe   individually one-term
0          8,694                   0
1              0              23,688
2            420              10,584
3              0                 840
           ------              ------
            9,114              35,112
```

Thus every colour factor in a hypothetical one-term-free support is either:

- one of 8,694 factors with all three triangle vertices matched to the
  7-cycle; or
- one of 420 exceptional `k=2` factors.

## Stage 2: eliminate the 420 exceptions

The automorphism group of the fixed full factor is

```text
D3 x D4 x D7,
```

of order 672.  The 420 exceptional factors form four orbits of sizes

```text
84, 84, 168, 84.
```

Independently, the producer enumerates all 168 disjoint two-edge singleton
sets `T` for which `F union T` has exactly one perfect matching.

For the four exceptional orbit representatives, the numbers of
edge-disjoint, individually safe second factors avoiding every such
two-edge obstruction are:

```text
108, 100, 104, 116.
```

For every one of those second factors, the number of individually safe
third factors that is edge-disjoint and still avoids the two-edge
obstructions is exactly zero.

Therefore no one-term-free three-colour support contains an exceptional
factor.  Every singleton edge incident with the triangle must go to the
7-cycle.

## Stage 3: exhaust all-triangle-to-7-cycle factors

Among the 8,694 remaining factors, the exact matching-fork catalogue
contains 4,368 three-edge singleton matchings.

Removing factors that already contain a fork leaves:

```text
fork-free factors                         3,654
orbits under D3 x D4 x D7                    18
```

For a union of selected factors, the producer compiles every fork into two
exact bitmask tests:

1. a candidate edge may not complete a selected edge pair;
2. a candidate edge pair may not be completed by a selected edge.

The 168 two-edge one-term sets are enforced at the same time.  Across all
18 first-factor orbit representatives:

```text
compatible second factors                    36
compatible ordered third factors              0
```

Hence every remaining three-colour support contains either a one-term set
or a matching fork.  Both are impossible, proving the theorem.

## Deterministic producer

Run:

```text
python claims/finite/n14/certify_fourteen_vertex_c3_c4_c7_family.py
```

Outputs:

```text
tmp/fourteen_vertex_c3_c4_c7_obstruction_catalogue.json
SHA-256
  78b0927316943420f53e88d73f5a8bcf17b36df18ad7a1a01a3930648e20f816

tmp/fourteen_vertex_c3_c4_c7_family_certificate.json
SHA-256
  c2bc514c5a4e950f0adca99ac6a431d11d61f38ed64b431cc2ce4ffa5401c514
```

The catalogue contains all 168 two-edge one-term sets and all 4,368
matching-fork triples.  Its canonical JSON hash is

```text
7800471f23dd457947d12b4311603a8ddfdce6f1083eecc21baea6d65e4881ab.
```

## Independent replay

Run:

```text
python claims/finite/n14/verify_fourteen_vertex_c3_c4_c7_family.py
```

The verifier does not call the producer.  It:

1. uses a separate bitmask-recursive perfect-matching enumerator;
2. reconstructs all 44,226 possible singleton factors;
3. recomputes every 128-subset active-matching table;
4. rebuilds and byte-compares the 168 one-term pairs and 4,368 forks;
5. explicitly expands the four exceptional and eighteen final orbits;
6. rechecks the exceptional extension counts;
7. tests the final small second-factor lists by direct pair/triple
   obstruction membership, rather than the producer's completion-mask
   compilation.

Pinned result:

```text
tmp/fourteen_vertex_c3_c4_c7_family_verified.json
SHA-256
  80bbfb8415842d152925237f990d8422b9f22c80e77f4416d9d2df19a316306e
```

It contains `"verified": true`.

## Consequence and remaining boundary

The earlier explicit no-one-term support and every adversarial mutation of
it are now subsumed by the full family theorem.  The result adds a mixed
odd/even factor type at arbitrary singleton support, complementing the
arbitrary-order all-odd theorem.

It does not close the other mixed or all-even 2-factor partitions at order
14, the complete order-14 five-regular equality boundary, supports below
the equality entry boundary, or the global conjecture.
