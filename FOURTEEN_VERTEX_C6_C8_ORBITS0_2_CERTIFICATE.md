# Order-14 `C6+C8` first-factor orbits 0--2 certificate

This certificate is retained as an earlier reproducible checkpoint.  It
is strictly subsumed by
`FOURTEEN_VERTEX_C6_C8_108_ORBITS_CERTIFICATE.md`.

## Scope

This is a finite computer-assisted theorem inside the order-14 equality
architecture.  It is not a proof of the Krenn--Gu conjecture and does not
close the full `C6+C8` family.

Within the architecture whose full factor is `C6+C8`, no support exists
whose pinned first singleton perfect matching belongs to census orbit 0,
1, or 2.  The other 325 first-factor orbits remain SAT in this checkpoint.

## Fresh reconstruction

The reconstruction starts from
`tmp/fourteen_vertex_c6_8_rule_sat_base20.cnf`, whose SHA-256 is

```text
6e2f86f6ebcc69ae54c22cf2ce5a54bee0c3b7076b60522e62fa46915c92b053
```

It independently replays 400 minimized factor-fork certificates and their
400 independent audits.  Symmetry transport and exact deduplication add
794 clauses, producing a 559-variable, 59,373-clause global CNF with
SHA-256

```text
3a547f660fb98edad883b355706c57be02f40414453e96708841c36f71334c4f
```

`verify_fourteen_vertex_two_even_cycle_minimum_activity_augmentation.py`
reconstructs the exact clause sequence and independently solves the
remaining global CNF as SAT.

## Selector audit and UNSAT proof

An assumption solve for each of all 328 first-factor selectors returns
exactly

```text
UNSAT: 0, 1, 2
SAT:   3, 4, ..., 327
```

The conditioned formula appends the single selector clause
`232 233 234 0`, which restricts the exactly-one selector encoding to
orbits 0--2.  Its SHA-256 is

```text
205cbb3b64b7c2997b9031808472aed88533b3a1ff01d5b317d9c744669df492
```

Kissat generated a 375,964-byte DRAT proof with SHA-256

```text
783980f915bbd1d52fa08ad63d311dd987e54d6855566e0015f42b124d21a8a8
```

The independent `drat-trim` checker returned `s VERIFIED`.

## One-command replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python verify_fourteen_vertex_c6_8_orbits0_2.py
```

The verifier reconstructs all 400 learned-certificate transports, audits
all 328 selectors, checks that the conditioned CNF is exactly the global
CNF plus the three-selector clause, and replays the DRAT proof.

## Boundary

This result excludes three of 328 first-factor orbits in one remaining
order-14 factor family.  It neither excludes the other 325 `C6+C8`
orbits nor resolves the global conjecture.
