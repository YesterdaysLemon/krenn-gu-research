# Order-14 `C6+C8` 117-orbit certificate

## Scope

This is a finite computer-assisted theorem inside the order-14
`C6+C8` equality architecture.  It is not a proof of the full family or
of the Krenn--Gu conjecture.

No support exists whose pinned first singleton perfect matching belongs
to any of these 117 census orbits:

```text
0--4
100--143
171--173, 179, 182, 185, 187--189
200--218, 220--225, 227, 232, 233, 238, 247, 269
300--327
```

The other 211 first-factor orbits remain SAT in this checkpoint.

## Fresh reconstruction

The certified 108-orbit predecessor independently replays 2,019
minimized factor-fork certificates and reconstructs its 36,080 learned
clauses.  The new layer independently replays 800 additional audited
certificates and adds 25,290 deduplicated clauses.

The resulting 559-variable, 119,949-clause global CNF has SHA-256

```text
9334d8bae4a7d10c466b4c8dfab2bbcac0616de0e82a4d7012c96bfabf8e8593
```

The independent augmentation verifier reconstructs the new clause
sequence exactly and confirms that the remaining global formula is SAT.

## Selector audit and UNSAT proof

All 328 first-factor selectors are solved independently.  The exact UNSAT
set is the 117-orbit list above; its complement is SAT.

The conditioned formula appends one positive clause containing exactly
those 117 selector variables.  Since the base encoding requires exactly
one selector, this restricts the formula to the claimed orbit set.  The
119,950-clause conditioned CNF has SHA-256

```text
49a0bfbae12d6a276dff1162a263a99c4ff5d8af64d65d43a022b603b7bd7952
```

Kissat generated a 296,782-byte DRAT proof with SHA-256

```text
cac11d99876fb751ad387bc93a15ee6925e32388559104be3ee38dba89f486b9
```

The independent `drat-trim` checker returned `s VERIFIED`.

## One-command replay

With the repository runtime and `tmp/python_deps` on `PYTHONPATH`, run:

```text
python verify_fourteen_vertex_c6_8_117_orbits.py
```

The verifier first replays the complete 108-orbit predecessor, then
reconstructs the 25,290-clause extension from 800 audited certificates,
audits every selector, checks the conditioned formula clause-for-clause,
and independently replays the new DRAT proof.

## Boundary

This closes 117 of 328 first-factor orbits in one remaining order-14
factor family.  The other 211 `C6+C8` orbits and the global conjecture
remain unresolved.
