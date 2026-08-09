# Eight-vertex 5-regular double-C4 family certificate

## Exact claim

For `n=8` and `d=3`, consider supports with:

- a 5-regular 20-edge skeleton;
- eight full `3 x 3` pair blocks forming a spanning `C4+C4` 2-factor;
- twelve diagonal singleton blocks forming a one-factorization of the
  complementary cubic graph, one perfect matching per colour.

No complex assignment on any such support realizes the Krenn--Gu target.
This theorem covers 1,086 labelled supports in 23 graph/colour orbits.

It does **not** prove that every exact-20-edge support has this form, and it
does not prove the global Krenn--Gu conjecture.

## Exhaustive support catalogue

The complement of a 5-regular graph on eight vertices is 2-regular.  The
only possible cycle partitions are:

```text
C8
C5 + C3
C4 + C4
```

The independently checked catalogue is:

```text
complement   C4+C4 factors   factorizations   labelled supports   orbits
C8                     23              43                 258       12
C5+C3                  15              30                 180        1
C4+C4                  34             108                 648       10
total                   72             181               1,086       23
```

Every support has 84 selected matrix entries.  Every required
monochromatic amplitude has at least one active matching, and no forbidden
amplitude has exactly one or two active matchings.

## Algebraic certificate chain

For each orbit representative:

1. every four-term forbidden Laurent parallelogram is factored as
   `x^a(1+x^r)(1+x^s)`;
2. its vanishing supplies the exact disjunction `x^r=-1` or `x^s=-1`;
3. exact integer-lattice reduction learns a no-good whenever the selected
   signed relations have inconsistent parity or isolate a nonzero monomial
   class;
4. the final factor-choice CNF is UNSAT;
5. CaDiCaL 1.9.5 emits a DRAT proof;
6. `drat-trim` independently returns `s VERIFIED`;
7. the semantic verifier reconstructs the support, every relation, every
   learned lattice conflict, the final CNF, and the full hash chain.

Across all 23 orbits the certificates contain:

```text
factor relations        3,704
factor clauses        126,044
lattice no-goods        1,378
```

## One-command audit

With the bundled dependencies on `PYTHONPATH`, run:

```text
python claims/finite/n08/verify_five_regular_double_c4_singleton_family.py
```

Success writes an aggregate JSON containing `"verified": true`:

```text
tmp/eight_vertex_five_regular_double_c4_singleton_family_verified.json
SHA-256
  92a571802b271df98e4b2c8cb7a100c96095bfeadfb5461dc2d45d28aa97b37f
```

The producer catalogue is:

```text
tmp/eight_vertex_five_regular_double_c4_singleton_family.json
SHA-256
  6162df4f1feb5b8d82b9bd791bbc7d2e751515db5ddfad017431c5f447589c99
```

The aggregate verifier intentionally reconstructs the catalogue by a
different enumeration: it chooses all eight-edge spanning subgraphs and
retains those with degree two and component sizes `4+4`, recursively
enumerates complement matchings, brute-forces all vertex automorphisms,
and checks the complete graph/colour orbit action.

## Remaining boundary

The live support search blocks all 1,086 certified supports.  A global or
full exact-20 proof still needs one of:

- a theorem forcing every balanced binomial-free support into this family;
- an exact contradiction for every support outside it; or
- a genuine complex counterexample.
