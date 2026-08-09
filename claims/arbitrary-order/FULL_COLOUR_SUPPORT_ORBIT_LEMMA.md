# Full-colour support-orbit lemma

## Statement

Fix a spanning full factor `F` and three edge-disjoint singleton perfect
matchings

```text
P0, P1, P2.
```

Let `sigma` be any vertex automorphism of `F`, and let `tau` be any
permutation of the three colours.  The singleton support

```text
(P0, P1, P2)
```

realizes the three-colour monochromatic perfect-matching target over
nonzero complex supported entries if and only if the support obtained by
applying `sigma` to every factor and permuting the three factor roles by
`tau` does.

Consequently, one certified impossible support excludes its complete
orbit under

```text
Aut(F) x S3.
```

## Proof

Relabel every vertex `v` as `sigma(v)` and carry every supported matrix
entry on `uv` to the corresponding entry on
`sigma(u)sigma(v)`.  Simultaneously apply the common colour-coordinate
permutation `tau` to both indices of every full block and to the label of
every singleton edge.

Because `sigma` preserves `F`, this gives a bijection between the perfect
matchings of the two support skeletons.  The product weight of each
matching is preserved after the entry relabelling, while its inherited
vertex colouring is transformed by the common permutation `tau`.

The target tensor

```text
e0 tensor ... tensor e0
+ e1 tensor ... tensor e1
+ e2 tensor ... tensor e2
```

is invariant under every common permutation of its three colour
coordinates.  Thus the transported entries realize the target on the
image support.  Applying the inverse vertex and colour permutations proves
the converse.

## `C4+C4+C6` consequence

For the standard order-14 `C4+C4+C6` full factor,
`|Aut(F)| = 1536`.  A certified support therefore has at most

```text
1536 * 6 = 9216
```

images.  The exact orbit can be smaller when the support itself has a
nontrivial stabilizer; the first two full-colour closures encountered in
the current orbit-9 continuation have sizes 9,216 and 4,608.

The augmentation producer reconstructs all images and converts them to
width-21 support no-goods.  The standalone verifier independently
reconstructs `Aut(F)`, all six colour permutations, the exact clause set,
and either:

- the clause-set manifest used between batched materializations; or
- the byte-identical augmented DIMACS at a materialization checkpoint.

## Boundary

This lemma transports an already proved support obstruction.  It does not
establish that the seed support is impossible; that requires its
independent algebraic certificate.  It also stays within one fixed
full-factor type.  The resulting finite exclusions do not by themselves
resolve the `C4+C4+C6` family or the global Krenn--Gu conjecture.
