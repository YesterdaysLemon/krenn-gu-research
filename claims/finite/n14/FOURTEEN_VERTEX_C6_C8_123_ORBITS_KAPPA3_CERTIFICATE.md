# Order-14 `C6+C8`, connectivity-at-least-3, 123-orbit certificate

## Scope

This is a finite computer-assisted theorem inside the order-14
`C6+C8` equality architecture. It explicitly assumes that the support
skeleton has vertex connectivity at least three. It is not an
unconditional exclusion of all `C6+C8` supports and is not a proof of the
full Krenn--Gu conjecture.

Under that connectivity hypothesis, no support exists whose pinned first
singleton perfect matching belongs to any of these 123 census orbits:

```text
0--9
100--144
171--173, 179, 182, 185, 187--189
200--218, 220--225, 227, 232, 233, 238, 247, 269
300--327
```

The other 205 first-factor orbits remain SAT in this rule checkpoint.

This conditional frontier is relevant to the global problem because
Chandran, Gajjala, and Illickan prove that a minimal Krenn--Gu
counterexample must be 4-connected:

<https://arxiv.org/abs/2407.00303>

## Certified predecessor

The one-command verifier first reruns
`verify_fourteen_vertex_c6_8_122_orbits_kappa3.py`, including the
complete predecessor, explicit connectivity, selector, DIMACS, and DRAT
reconstruction chain.

The resulting v21 predecessor has 559 variables and 127,140 clauses. Its
SHA-256 is

```text
8a03d170099f2dea4fe8fd8457dbbad4f85fdc1fc2811bb6559a1d01c0a9822d
```

## Two independent closures of orbit 9

The primary targeted continuation used 17 SAT residual supports. It
produced 136 independently audited minimum-activity factor-fork
certificates whose activation premises have size one through six.
Independent symmetry transport and deduplication add exactly 360
clauses.

The resulting v22 CNF has 559 variables and 127,500 clauses. Its SHA-256
is

```text
af8b29041e787e9d59ff88bb1fa442276caf4df4b9494dbaa534df14914bc986
```

A separate direct one-extra-cycle-core search used 61 SAT residuals and
an unrelated certificate sequence. Independent replay of those 61
certificates adds 244 clauses to the same v21 predecessor, producing a
127,384-clause CNF with SHA-256

```text
ce21ca927f0d0a1dd17fb330b5b3c9374a150a40a46c9e72169c89418492845a
```

Fresh all-selector solves on both independently reconstructed CNFs report
the same 123-orbit UNSAT set above and its 205-orbit SAT complement.

## Aggregate UNSAT proof

Appending one positive clause containing exactly the 123 UNSAT selectors
to the targeted v22 CNF gives a 127,501-clause conditioned CNF with
SHA-256

```text
ac5ddf9af8608ea01da65c87758dab087c867d5c8cfd6fdeca4859c2d7f2f7bc
```

Kissat generated a 1,418,915-byte DRAT proof with SHA-256

```text
f7fe06a37effeb6f58d18795b271efda00af0944d7216ab5852b0147e8426141
```

Independent forward `drat-trim` verification returned `s VERIFIED`.

## One-command replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python verify_fourteen_vertex_c6_8_123_orbits_kappa3.py
```

The verifier recursively replays the complete 122-orbit predecessor,
independently reconstructs both orbit-9 certificate families, audits all
328 selectors on both resulting CNFs, compares the targeted conditioned
DIMACS sequence exactly, and reruns forward `drat-trim`.

Its final output is
`tmp/fourteen_vertex_c6_8_123_orbits_kappa3_final_verified.json` and must
contain `"verified": true`. A fresh complete replay took 62.94 seconds.

## Boundary

This closes 123 of 328 first-factor orbits only for three-connected
supports in one remaining order-14 factor family. The other 205
`C6+C8` orbits, non-three-connected supports as a stand-alone finite
classification, the other unresolved factor types, and the global
conjecture remain unresolved.
