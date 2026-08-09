# Order-14 `C6+C8`, connectivity-at-least-3, 124-orbit certificate

## Scope

This is a finite computer-assisted theorem inside the order-14
`C6+C8` equality architecture. It explicitly assumes that the support
skeleton has vertex connectivity at least three. It is not an
unconditional exclusion of all `C6+C8` supports and is not a proof of the
full Krenn--Gu conjecture.

Under that connectivity hypothesis, no support exists whose pinned first
singleton perfect matching belongs to any of these 124 census orbits:

```text
0--10
100--144
171--173, 179, 182, 185, 187--189
200--218, 220--225, 227, 232, 233, 238, 247, 269
300--327
```

The other 204 first-factor orbits remain SAT in this rule checkpoint.

This conditional frontier is relevant to the global problem because
Chandran, Gajjala, and Illickan prove that a minimal Krenn--Gu
counterexample must be 4-connected:

<https://arxiv.org/abs/2407.00303>

## Certified predecessor

The one-command verifier first reruns
`verify_fourteen_vertex_c6_8_123_orbits_kappa3.py`, including its complete
connectivity, selector, semantic-certificate, DIMACS, and DRAT
reconstruction chain.

The resulting v22 predecessor has 559 variables and 127,500 clauses. Its
SHA-256 is

```text
af8b29041e787e9d59ff88bb1fa442276caf4df4b9494dbaa534df14914bc986
```

## Orbit-10 closure

The targeted continuation used 22 SAT residual supports and then closed.
It produced 176 independently audited minimum-activity factor-fork
certificates. Independent symmetry transport and deduplication add
exactly 198 clauses.

The resulting v23 CNF has 559 variables and 127,698 clauses. Its SHA-256
is

```text
47e77a11fa5f70fbd0aa1dd8239eeff9a6c5a4658e7a06bbe58783c074afe7bc
```

A fresh all-selector solve reports exactly the 124-orbit UNSAT set above
and its 204-orbit SAT complement.

## Aggregate UNSAT proof

Appending one positive clause containing exactly the 124 UNSAT selectors
to v23 gives a 127,699-clause conditioned CNF with SHA-256

```text
93b82551f9782bddb424ff218c74ee56942e61e66396af8fc07d12d77282437e
```

Kissat generated a 1,450,493-byte DRAT proof with SHA-256

```text
83e3fadab899614908d48540cfeaa400a32d093b37fbcc85cf31f5274b6b40b2
```

Independent forward `drat-trim` verification returned `s VERIFIED`.

## One-command replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python verify_fourteen_vertex_c6_8_124_orbits_kappa3.py
```

The verifier recursively replays the complete 123-orbit predecessor,
independently reconstructs the orbit-10 certificate family, audits all
328 selectors, compares the conditioned DIMACS sequence exactly, and
reruns forward `drat-trim`.

Its final output is
`tmp/fourteen_vertex_c6_8_124_orbits_kappa3_final_verified.json` and must
contain `"verified": true`. A fresh complete replay took 63.51 seconds.

## Boundary

This closes 124 of 328 first-factor orbits only for three-connected
supports in one remaining order-14 factor family. The other 204
`C6+C8` orbits, non-three-connected supports as a stand-alone finite
classification, the other unresolved factor types, and the global
conjecture remain unresolved.
