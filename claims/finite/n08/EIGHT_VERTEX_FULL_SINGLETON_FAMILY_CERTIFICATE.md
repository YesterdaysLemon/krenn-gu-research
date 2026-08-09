# Eight-vertex 5-regular full-2-factor/singleton certificate

## Exact claim

For `n=8` and `d=3`, consider supports with:

- a 5-regular, 20-edge skeleton;
- eight full `3 x 3` blocks forming any spanning 2-factor;
- twelve diagonal singleton blocks forming a one-factorization of the
  complementary cubic graph, one perfect matching per colour.

No complex assignment on any such support realizes the Krenn--Gu target.
This covers 7,938 labelled supports in 86 graph/colour orbits.

It does **not** prove that every exact-20-edge support has this form, and it
does not prove the global Krenn--Gu conjecture.

## Exhaustive catalogue

Both the 5-regular skeleton complement and the full-block 2-factor are
2-regular on eight vertices, so their cycle type is one of `C8`, `C5+C3`,
or `C4+C4`.  The independently checked cross-census is:

```text
skeleton     full factor   factors   factorizations   labelled   orbits
C8           C5+C3              48              80        480        7
C8           C4+C4              23              43        258       12
C8           C8                177             294      1,764       35
C5+C3        C5+C3              60              60        360        1
C5+C3        C4+C4              15              30        180        1
C5+C3        C8                180             300      1,800        7
C4+C4        C5+C3              32              64        384        1
C4+C4        C4+C4              34             108        648       10
C4+C4        C8                184             344      2,064       12
total                           753           1,323      7,938       86
```

Every support has 84 selected entries and satisfies the basic support
relaxation.  Exactly 1,086 labelled supports, in 23 orbits, are
binomial-free; these are precisely the cases whose full factor is
`C4+C4`.  The other 6,852 supports, in 63 orbits, expose at least one
two-term forbidden amplitude.

## Algebraic certificate chain

The 23 binomial-free orbits use exact four-term Laurent factorizations.
The other 63 orbits use their mandatory two-term amplitudes as signed
relations; every one closes after a single exact lattice branch.

The hard 23-orbit part now also has a much shorter direct certificate.  In
every orbit there is one four-term amplitude whose two alternating-`C4`
factor relations are each ruled out by a separate five-term amplitude.
Under the relevant relation, four terms cancel in two pairs and the fifth
nonzero monomial survives.  Thus three amplitudes close each orbit:

```text
four-term factor amplitude
  -> relation r or relation s
five-term amplitude -> not r
five-term amplitude -> not s.
```

`verify_eight_vertex_three_amplitude_forks.py` independently replays those
23 forks and binds them to the already audited orbit catalogue, hence to all
1,086 labelled binomial-free supports.  As redundant SAT evidence, the 23
compressed factor CNFs have raw DRAT proofs totalling only 6,574 bytes, and
every proof independently replays as `s VERIFIED`.

For every orbit:

1. the semantic checker reconstructs all active matching monomials and
   exponent relations;
2. exact integer-lattice reduction verifies each parity or isolated-class
   contradiction;
3. the final factor-choice CNF is UNSAT;
4. CaDiCaL 1.9.5 emits a DRAT proof;
5. `drat-trim` independently returns `s VERIFIED`;
6. the aggregate verifier checks the complete artifact hash chain.

Aggregate certificate size:

```text
factor relations      183,673
factor clauses        313,813
lattice no-goods        1,441
```

## One-command audit

With the bundled dependencies on `PYTHONPATH`, run:

```text
python claims/finite/n08/verify_five_regular_full_singleton_family.py
python claims/finite/n08/verify_unary_cycle_relation_family.py
python claims/finite/n08/verify_eight_vertex_three_amplitude_forks.py
```

Success writes:

```text
tmp/eight_vertex_five_regular_full_singleton_family_verified.json
SHA-256
  add0fb4e6cb8aca04a1a143e87a5383db28a86f9e276aa1ad1a3bbdd6490499a
```

The exhaustive producer is:

```text
tmp/eight_vertex_five_regular_full_singleton_family.json
SHA-256
  546e63334dacddfb899beffbb8536e0c6983f9ae6710d1a6bfac8a9ea96b2d96
```

The verifier independently chooses all eight-edge subgraphs of each
skeleton, checks degree two, classifies components, recursively regenerates
every one-factorization, brute-forces the vertex automorphism groups,
recomputes the colour action, validates all model/activity data, and binds
all 86 orbits to semantic factor-lattice and replayed DRAT audits.

The simplified hard-orbit manifests are:

```text
tmp/eight_vertex_unary_cycle_relation_family_verified.json
tmp/eight_vertex_three_amplitude_forks_verified.json
tmp/eight_vertex_unary_cycle_relation_family_proofs_verified.json
```

## Remaining boundary

The theorem is conditional only on the block architecture.  A complete
exact-20 or global proof still needs to force:

```text
12 reciprocal monochromatic singleton blocks
  = three colour perfect matchings,

8 remaining full blocks
  = a spanning 2-factor,
```

or eliminate every support outside that architecture.
