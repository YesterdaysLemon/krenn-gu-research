# Order-14 `C6+C8`, connectivity-at-least-3, 125-orbit certificate

## Scope

This is a finite computer-assisted theorem inside the order-14
`C6+C8` equality architecture. It explicitly assumes that the support
skeleton has vertex connectivity at least three. It is not an
unconditional exclusion of all `C6+C8` supports and is not a proof of the
full Krenn--Gu conjecture.

Under that connectivity hypothesis, no support exists whose pinned first
singleton perfect matching belongs to any of these 125 census orbits:

```text
0--11
100--144
171--173, 179, 182, 185, 187--189
200--218, 220--225, 227, 232, 233, 238, 247, 269
300--327
```

The other 203 first-factor orbits remain SAT in this rule checkpoint.

This conditional frontier is relevant to the global problem because
Chandran, Gajjala, and Illickan prove that a minimal Krenn--Gu
counterexample must be 4-connected:

<https://arxiv.org/abs/2407.00303>

## Certified predecessor

The one-command verifier first reruns
`verify_fourteen_vertex_c6_8_124_orbits_kappa3.py`, including its complete
connectivity, selector, semantic-certificate, DIMACS, and DRAT
reconstruction chain.

The resulting v23 predecessor has 559 variables and 127,698 clauses. Its
SHA-256 is

```text
47e77a11fa5f70fbd0aa1dd8239eeff9a6c5a4658e7a06bbe58783c074afe7bc
```

## Orbit-11 closure

The targeted continuation used 28 SAT residual supports and then closed.
It produced 216 independently audited minimum-activity factor-fork
certificates. Independent symmetry transport and deduplication add
exactly 524 clauses.

The resulting v24 CNF has 559 variables and 128,222 clauses. Its SHA-256
is

```text
22e9925fb1a222ad36e35e5e9b449dcc799ed684838ed8748c4c26bc6a0b1125
```

A fresh all-selector solve reports exactly the 125-orbit UNSAT set above
and its 203-orbit SAT complement.

## Aggregate UNSAT proof

Appending one positive clause containing exactly the 125 UNSAT selectors
to v24 gives a 128,223-clause conditioned CNF with SHA-256

```text
0497216c436226302016dd8d54a9bb4c2a13aa8a43d3c9906183e2334a9239ef
```

Kissat generated a 3,196,439-byte DRAT proof with SHA-256

```text
1e0558fbadf896d2cf4acef4945e3ac43c443a5a75dcbc5bebd0506f9bb78d10
```

Independent forward `drat-trim` verification returned `s VERIFIED`.

## One-command replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python claims/finite/n14/verify_fourteen_vertex_c6_8_125_orbits_kappa3.py
```

The verifier recursively replays the complete 124-orbit predecessor,
independently reconstructs the orbit-11 certificate family, audits all
328 selectors, compares the conditioned DIMACS sequence exactly, and
reruns forward `drat-trim`.

Its final output is
`tmp/fourteen_vertex_c6_8_125_orbits_kappa3_final_verified.json` and must
contain `"verified": true`. A fresh complete replay took 84.30 seconds.

## Boundary

This closes 125 of 328 first-factor orbits only for three-connected
supports in one remaining order-14 factor family. The other 203
`C6+C8` orbits, non-three-connected supports as a stand-alone finite
classification, the other unresolved factor types, and the global
conjecture remain unresolved.
