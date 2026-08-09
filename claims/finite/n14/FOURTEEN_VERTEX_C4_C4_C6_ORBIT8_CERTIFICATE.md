# Order-14 `C4+C4+C6` first-factor orbit-8 certificate

## Claim

Inside the order-14 equality architecture with full factor
`C4+C4+C6` and support-skeleton vertex connectivity at least three,
there is no three-colour witness whose pinned first singleton perfect
matching lies in orbit 8.

This is a finite computer-assisted theorem.  It is relevant to the
Krenn--Gu conjecture because a minimal counterexample is known to be
4-connected, but it does not prove the global conjecture.

## Predecessor frontier

The independently audited minimal-circuit frontier has 324 variables and
1,220,593 clauses:

```text
SHA-256:
9d0e0e3da2b1c759f17b0f874766af8cff8b8e921b5e1ccea236970df9a42918
```

It leaves selector 240, representing pinned first-factor orbit 8, SAT.

## Two exact relation-selection supports

The first two orbit-8 supports require disjunctive choices among their
partial-circuit relations.  Their exact selection CEGARs close:

```text
support 1: 128 inclusion-minimal branches
support 2:  32 inclusion-minimal branches
```

Independent chain replays reconstruct every initial and derived signed
integer-lattice relation, every blocking clause, and the terminal
relation-selector UNSAT decisions.  Their exact width-21 support
no-goods give:

```text
after support 1
d02bdc95cbc4a963bb22698c24c7cd3017ca66df4c7c16b9a528161c78553bf1
1,220,594 clauses

after support 2
44e5ed260e04e0cd7207691209038d5f44d0d601b02d2030f91ec8a0ca08fb3f
1,220,595 clauses
```

The branch details and their pinned hashes are in
`FOURTEEN_VERTEX_C4_C4_C6_ORBIT8_PARTIAL_BINOMIAL_SUPPORT_CERTIFICATE.md`.

## Three mandatory-unit support types

The next three inequivalent supports have unconditional cores: their
four unit partial-circuit relations are present in every admissible
relation selection.

For each support, exact signed Smith reduction starts with rank four and
all invariant factors one.  Four equal-magnitude two-coset forbidden
amplitudes produce four more signed relations.  The rank-eight lattice
then leaves one nonzero signed monomial class in a forbidden amplitude.
The independent verifier reconstructs the complete perfect-matching
census, the relation clauses, all four derived relations, the final
Smith lattice, and the isolated class.

The first such analysis and independent replay have hashes:

```text
analysis
c55cad80a33bda5c08aa6441e4369a9e41cbc0ddd50132c78315355ea307bb6d

independent replay
a6c4baf4befa3c6cd5709be8a54ca73bd961e99df0e94195f406f6ca4e7dcbe9
```

The other two support types are freshly selected from their immediately
preceding symmetry-augmented CNFs and independently replayed before use.

## Stabilizer-orbit closure

The pinned-factor support symmetry lemma transports any proved support
obstruction under:

1. a vertex automorphism of the full `C4+C4+C6` factor that stabilizes
   the pinned colour-0 singleton matching; and
2. the optional swap of singleton colours 1 and 2.

The full-factor automorphism group has 1,536 elements.  The orbit-8
pinned matching has stabilizer size 8, and each of the three certified
supports has 16 distinct images after the colour swap.

The augmentation auditor independently checks that every action is a
permutation preserving the full cycle skeleton, reconstructs every
image support, and reproduces each augmented DIMACS file byte for byte.
The three symmetry steps add 16, 15, and 15 fresh no-goods:

```text
symmetry step 1
2d497e530a2f60819ae3eb12cd6ed8a8ec448a2e37c7e1a2c6d8aaefe332d681
1,220,611 clauses

symmetry step 2
3400f37fb23b86c7ec59249ff4c1a87e5d87d36c479fa87b2bd4c0ef7250cacd
1,220,626 clauses

symmetry step 3
3c5b2cc66ebc198d3a27fa6a323ea4a4ce4aa0f9c9825ae83007a9b2b13912c7
1,220,641 clauses
```

Together with the first two exact no-goods, the continuation adds 48
sound support exclusions.

See `PINNED_FACTOR_SUPPORT_SYMMETRY_LEMMA.md` for the elementary
invariance proof.

## UNSAT proof

Appending the positive selector unit

```text
240
```

gives a 1,220,642-clause conditioned CNF:

```text
SHA-256:
edbdd2cc6151a3d831c08cc6825ee9f64e59befc67956d45a0cedb9a25d51a15
```

Kissat returns `UNSAT` and writes a raw DRAT proof:

```text
proof bytes:
58,902,708

proof SHA-256:
5555d2f3fbd3f116a05f08d50fbfefbf7a3239822a1081360c4f5c737ee98074
```

Independent forward `drat-trim` replay returns `"verified": true` in
702.50 seconds.  Its record is:

```text
tmp/fourteen_vertex_c4_c4_c6_orbit8_symbinomial3_drat_trim.json
```

The top-level verifier independently reconstructed all five DIMACS
augmentations and then performed a second forward proof replay.  It
returned `"verified": true` in 1,377.56 seconds overall; its fresh
`drat-trim` phase took 1,188.88 seconds.  The bound end-to-end record is:

```text
tmp/fourteen_vertex_c4_c4_c6_orbit8_final_verified.json
```

That record binds the 1,220,641-clause global CNF, the exact selector-240
conditioning, and the 58,902,708-byte proof to the hashes above.  This
second replay was intentionally redundant: it checks that the public
top-level entry point does not merely trust the earlier proof-check
record.

## Replay

With the repository runtime and bundled dependencies on `PYTHONPATH`,
run:

```text
python claims/finite/n14/verify_fourteen_vertex_c4_c4_c6_orbit8.py
```

This binds the predecessor frontier, reconstructs all five support
augmentations, checks the exact selector conditioning and Kissat record,
and reruns forward `drat-trim`.

For a fresh replay of all 160 relation-selection branches and all three
mandatory-unit algebra certificates before those checks, run:

```text
python claims/finite/n14/verify_fourteen_vertex_c4_c4_c6_orbit8.py \
  --full-support-replay
```

## Updated frontier and boundary

Combining this theorem with the prior 65-orbit union excludes 66 of the
93 pinned first-factor orbits in the minimum-connectivity-three regime.
The 27 selectors not excluded by these certificates are:

```text
9--11, 13--16, 22, 36--41, 44--51, 54--55, 57, 63, 68
```

Those selectors, the other all-even full-factor families, higher orders,
and the global prize conjecture remain unresolved.
