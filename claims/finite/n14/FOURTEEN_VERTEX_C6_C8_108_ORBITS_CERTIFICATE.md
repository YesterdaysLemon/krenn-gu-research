# Order-14 `C6+C8` 108-orbit certificate

## Scope

This is a finite computer-assisted theorem inside the order-14
`C6+C8` equality architecture.  It is not a proof of the full family or
of the Krenn--Gu conjecture.

No support exists whose pinned first singleton perfect matching belongs
to any of these 108 census orbits:

```text
0--4
100--143
200--218, 220--225, 227, 232, 233, 238, 247, 269
300--327
```

The other 220 first-factor orbits remain SAT in this checkpoint.

## Fresh reconstruction

The reconstruction starts from the original 328-selector base CNF with
SHA-256

```text
6e2f86f6ebcc69ae54c22cf2ce5a54bee0c3b7076b60522e62fa46915c92b053
```

It independently replays 2,019 minimized factor-fork certificates and
their independent audits.  Exact symmetry transport and deduplication add
36,080 clauses.  The resulting 559-variable, 94,659-clause global CNF has
SHA-256

```text
ad4b3b335db334f8f0b66b03966d3909f1c4009cf69f4ec85c4b68503cfde615
```

The independent augmentation verifier reconstructs the complete clause
sequence and confirms that the remaining global formula is SAT.

## Selector audit and UNSAT proof

All 328 first-factor selectors are solved independently.  The exact UNSAT
set is the 108-orbit list above; its complement is SAT.

The conditioned formula appends one positive clause containing exactly
those 108 selector variables.  Because the base encoding requires exactly
one selector, this restricts the formula to the claimed orbit set.  The
conditioned CNF has SHA-256

```text
119074488c59adc4857dd87ec9cdc0ecf90273709d60881aa2a25da7affb3fd9
```

Kissat generated a 400,169-byte DRAT proof with SHA-256

```text
ed936f1c1e0a85991fd582718e672712d00ba2c2507e373cf9e3b9c33b1e2b25
```

The independent `drat-trim` checker returned `s VERIFIED`.

## One-command replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python claims/finite/n14/verify_fourteen_vertex_c6_8_108_orbits.py
```

The verifier rebuilds all 36,080 learned clauses from 2,019 audited
certificates, audits every selector, checks the conditioned formula
clause-for-clause, and replays the DRAT proof.

## Audit correction

Older range-local audit artifacts for 200--299, 300--326, and 327 used an
orbit label offset that was not always paired with the corresponding
DIMACS selector offset.  They are not used here.  This theorem starts from
the original base, transports every source afresh, and audits selectors
0--327 directly.  The audit tool now derives range starts safely from
`--selector-zero`.

## Boundary

This closes 108 of 328 first-factor orbits in one remaining order-14
factor family.  The other 220 `C6+C8` orbits and the global conjecture
remain unresolved.
