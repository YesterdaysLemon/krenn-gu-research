# Order-14 `C3+C3+C4+C4` equality-family certificate

## Theorem

There is no order-14, three-colour equality-architecture witness whose
full-block 2-factor has cycle type `C3+C3+C4+C4`.

This is a complete finite theorem for this factor type.  It is not a
proof of the remaining order-14 factor types or of the global Krenn--Gu
conjecture.

## Fixed full factor and singleton factors

Fix the labelled full factor

```text
C3 = (0,1,2)
C3 = (3,4,5)
C4 = (6,7,8,9)
C4 = (10,11,12,13).
```

In the equality architecture, each singleton colour class is a perfect
matching in the complement of this factor, and the three classes are
pairwise edge-disjoint.  The independent verifier reconstructs:

```text
eligible singleton perfect matchings                44,262
individually one-term-free singleton factors         7,974
full-factor automorphisms                            9,216
orbits of individually admissible first factors         14
```

The orbit reduction fixes the first colour factor to one representative
of each of the 14 orbits.  The second and third factors are still
enumerated exhaustively, so no support is sampled or omitted.

## Why the one-term filters are exact

Let `U` be any matching made from singleton edges of the three colour
factors.  It can be activated exactly:

1. colour the endpoints of every edge in `U` by that edge's singleton
   label;
2. on the remaining vertices, properly 2-colour the paths and even cycles
   induced by singleton factors 1 and 2, using colours 1 and 2.

An edge of factor 1 or 2 that meets a precoloured endpoint is safe: if the
endpoint has that factor's colour, its unique edge of that factor is
already the selected edge in `U`.  All remaining factor-1/factor-2 edges
have differently coloured endpoints.  Factor-0 edges cannot activate on
the remaining vertices, and the same uniqueness argument handles their
boundary edges.

Therefore, if the graph consisting of the full factor and `U` has exactly
one perfect matching, the associated nonmonochromatic coefficient is one
nonzero monomial and cannot vanish.  The verifier independently enumerates
the relevant matching catalogues:

```text
matching size       scanned       one-term
3                     27,512          1,152
4                    164,241         14,400
5                    421,197         19,008
6                    360,858              0
```

These are sound contradiction filters.  They need not catalogue every
possible one-term obstruction: retaining extra candidates only makes the
subsequent exhaustive closure harder.

## Exhaustive support funnel

After fixing the first-factor orbits, the exact bitset replay obtains:

```text
one-term-compatible second factors                  15,922
after the larger one-term filters                    12,172

size-3-compatible third factors                   2,911,352
after all catalogued one-term filters             2,863,992
connected supports                                2,862,996
disconnected supports                                   996
```

Every disconnected support is impossible by tensor factorization.  If the
skeleton splits as `L disjoint-union R`, then

```text
T(a_L,a_R) = T_L(a_L) T_R(a_R).
```

The three required monochromatic coefficients force both component
factors to be nonzero in every colour.  Choosing different colours on
`L` and `R` then gives a forbidden coefficient that is a product of two
nonzero complex numbers.

## Direct cancellation transport

For the connected candidates, 5,039 exact source certificates provide
binomial-to-trinomial cancellation transports.  The verifier:

- reconstructs every source support and both forbidden colourings;
- checks that the source colouring has exactly two active perfect
  matchings;
- checks that the target has those two matchings plus one survivor;
- verifies that the two monomial-ratio signatures are identical at the
  source and target;
- rebuilds the replacement-factor bitsets and all global colour
  relabellings.

After deduplication these certificates induce 21,837 sound transport
rules.  They close

```text
2,862,996 - 394,068 = 2,468,928
```

connected candidates.

## Stable `C4` two-to-three forks

The remaining 394,068 supports are closed by a second exact mechanism.
The catalogue contains 395,784 nested matching patterns

```text
sparse active support   -> exactly 2 perfect matchings
rich active support     -> exactly 3 perfect matchings,
```

where the two sparse perfect matchings differ precisely around one of the
two full `C4` components.  A certificate keeps that `C4` colouring fixed
between its sparse and rich equations.  Consequently the same signed
binomial relation forced by the sparse equation transports to the rich
equation; its two terms cancel and the third supported monomial survives.

Four compact shards contain exactly one such witness for every residual
support:

```text
shard 0       98,517
shard 1       98,517
shard 2       98,517
shard 3       98,517
total        394,068
survivors          0
```

The independent audit semantically replays all 394,068 witnesses.  Only
1,375 distinct stable-fork patterns are needed, although the full
395,784-pattern catalogue is validated.

## Independent replay

Run:

```text
python claims/finite/n14/verify_fourteen_vertex_c3_c3_c4_c4_family.py
```

The verifier independently regenerates the factor census, automorphisms,
one-term catalogues, pair and triple filters, direct transport pool,
stable-fork semantics, shard partition, and every activation and Laurent
transport identity.  It also hashes all source artifacts.

The final audit is

```text
tmp/fourteen_vertex_c3_c3_c4_c4_family_verified.json
```

and contains:

```json
{
  "verified": true,
  "status": "all_c3_c3_c4_c4_equality_supports_closed",
  "stable_fork_certificates_replayed": 394068,
  "residual_supports": 0
}
```
