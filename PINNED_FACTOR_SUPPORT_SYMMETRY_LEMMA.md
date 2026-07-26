# Pinned-factor support symmetry lemma

## Statement

Fix a spanning full edge-coloured factor `F` on a vertex set `V`, and
fix three singleton-colour perfect matchings

```text
P0, P1, P2.
```

Let `sigma` be a vertex permutation preserving `F`, including its full
edge-colour labels, and satisfying `sigma(P0) = P0`.  Let `tau` be either
the identity on singleton colours or the transposition of colours 1 and
2.  Then the singleton support

```text
(P0, P1, P2)
```

realizes the three-colour monochromatic perfect-matching target over
nonzero complex edge weights if and only if

```text
(P0, sigma(P_tau(1)), sigma(P_tau(2)))
```

does.

Consequently, one certified impossible support excludes its entire orbit
under the stabilizer of `P0` in `Aut(F)`, together with the colour-1/2
swap.

## Proof

Suppose the first support has nonzero edge weights realizing the target.
Relabel every vertex `v` as `sigma(v)` and carry each full-block entry
`W_uv[a,b]` to
`W_sigma(u)sigma(v)[tau(a),tau(b)]`; carry each singleton edge in the
same way.  Because `sigma` preserves the full factor, this is a
weight-preserving bijection between the perfect matchings of the two
support skeletons.  It preserves the induced vertex-colouring of every
matching up to `tau`.

The target requires the same nonzero amplitude for each monochromatic
colour and zero amplitude for every nonmonochromatic colouring.  It is
therefore invariant under swapping colours 1 and 2.  The relabelled
weights realize the target on the image support.  Applying
`sigma^{-1}` and the same colour swap proves the converse.

Finally, `sigma(P0) = P0` ensures that the pinned first singleton factor
does not change.  Thus all image supports remain under the same SAT
selector.  This proves the orbit-closure claim.

## `C4+C4+C6` orbit-8 instance

For the standard full factor

```text
01 12 23 03
45 56 67 47
89 9-10 10-11 11-12 12-13 8-13
```

the full-factor automorphism group has 1,536 elements.  The orbit-8
pinned singleton factor

```text
02 13 48 59 6-12 7-10 11-13
```

has stabilizer size 8.  Combining those eight vertex actions with the
colour-1/2 swap gives at most 16 support images.  For each of the three
mandatory-unit certificates used in the orbit-8 closure, all 16 images
are distinct.

`verify_fourteen_vertex_binomial_support_closure_augmentation.py`
independently checks that every enumerated action is a permutation,
preserves the full cycle skeleton, stabilizes the pinned factor, and
reconstructs the exact image no-goods and augmented DIMACS bytes.

## Boundary

This lemma transports a proved support obstruction.  It does not prove
that the seed support is impossible; that remains the job of the
corresponding algebraic certificate.  It also does not move between
different pinned first-factor orbits.
