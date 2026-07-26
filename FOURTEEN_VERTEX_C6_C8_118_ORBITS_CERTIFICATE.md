# Order-14 `C6+C8` 118-orbit certificate

> **Scope correction.** This artifact exactly replays its stored CNF and
> DRAT proof, but its late minimum-activity clauses were certified only
> under a three-connected support hypothesis that was not explicit in the
> final CNF. Do not cite the unqualified 118-orbit exclusion as a theorem.
> The repaired, explicitly connectivity-conditioned result is
> `FOURTEEN_VERTEX_C6_C8_121_ORBITS_KAPPA3_CERTIFICATE.md`.

## Scope

This is a finite computer-assisted theorem inside the order-14
`C6+C8` equality architecture. It is not a proof of the full family or
of the Krenn--Gu conjecture.

No support exists whose pinned first singleton perfect matching belongs
to any of these 118 census orbits:

```text
0--5
100--143
171--173, 179, 182, 185, 187--189
200--218, 220--225, 227, 232, 233, 238, 247, 269
300--327
```

The other 210 first-factor orbits remain SAT in this rule checkpoint.

## Extension from the certified 117-orbit frontier

The predecessor theorem excludes the same list with orbit 5 omitted.
From its independently reconstructed 119,949-clause CNF, nine later
augmentation layers replay 1,334 audited certificates and add 4,562
deduplicated transport clauses.

The last layer is the decisive one. Eleven independently verified
full-only/one-extra cycle-factor cores minimize to activation scores two
or three. Their stabilizer transport adds 22 clauses of width three or
four and makes selector 5 UNSAT. An older factor-fork continuation also
reached UNSAT independently, but it is not needed by the promoted proof.

The resulting 559-variable, 124,511-clause global CNF has SHA-256

```text
2c348a4e45478109a5453f55132b2b3ab78f579221a67e7970033d3380abc51f
```

## Selector audit and UNSAT proof

An exact solve under each of the 328 selector assumptions reports the
118-orbit list above as UNSAT and its 210-orbit complement as SAT.

Appending one positive clause containing exactly the 118 UNSAT selectors
gives a 124,512-clause conditioned CNF with SHA-256

```text
1214b396fe6a51b78ffa066a18cda5ef4699d492826dce89d709fdbd0900c33f
```

Kissat generated a 304,305-byte DRAT proof with SHA-256

```text
820ed6b38b69f76a8388d608a6dc122f1de490761838b10ce0cd2bd3547b5052
```

Independent forward `drat-trim` verification returned `s VERIFIED`.

## One-command replay

With the repository runtime and `tmp/python_deps` on `PYTHONPATH`, run:

```text
python verify_fourteen_vertex_c6_8_118_orbits.py
```

The verifier rebuilds the certified 117-orbit predecessor, independently
reconstructs all nine later augmentation layers, audits all 328
selectors, compares the exact conditioned DIMACS sequence, and reruns
`drat-trim`. Its final output is
`tmp/fourteen_vertex_c6_8_118_orbits_final_verified.json` and contains
`"verified": true`.

## Boundary

This closes 118 of 328 first-factor orbits in one remaining order-14
factor family. The other 210 `C6+C8` orbits, the other unresolved
factor types, and the global conjecture remain unresolved.
