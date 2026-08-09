# Order-14 `C6+C8`, connectivity-at-least-3, 130-orbit certificate

## Scope

This is a finite computer-assisted theorem inside the order-14
`C6+C8` equality architecture. It explicitly assumes that the support
skeleton has vertex connectivity at least three. It is not an
unconditional exclusion of all `C6+C8` supports and is not a proof of the
full Krenn--Gu conjecture.

Under that connectivity hypothesis, no support exists whose pinned first
singleton perfect matching belongs to any of these 130 census orbits:

```text
0--16
100--144
171--173, 179, 182, 185, 187--189
200--218, 220--225, 227, 232, 233, 238, 247, 269
300--327
```

The other 198 first-factor orbits remain SAT in this rule checkpoint.

This conditional frontier is relevant to the global problem because
Chandran, Gajjala, and Illickan prove that a minimal Krenn--Gu
counterexample must be 4-connected:

<https://arxiv.org/abs/2407.00303>

## Certified predecessor through orbit 14

The recursive verifier first replays the complete 128-orbit certificate.
That intermediate step includes the 126-orbit checkpoint and then promotes
56 independently audited orbit-13 certificates, adds exactly 212 clauses,
audits all 328 selectors, and checks a 1,611,777-byte DRAT proof. Its
559-variable, 130,066-clause v26
CNF has SHA-256

```text
66e250a13ff9241ed9809a8855a78a15896aefa5893a9926ebadcbc175acbec9
```

## Orbit-14 closure

The targeted orbit-14 continuation encountered 20 SAT residual
supports and then closed. It produced 160 independently audited
minimum-activity factor-fork certificates. Independent symmetry transport
and deduplication add exactly 296 clauses.

The resulting v27 CNF has 559 variables and 130,362 clauses. Its SHA-256
is

```text
9dccfdc03f3449ecb843401304b0689da27e1907db19f2c106752f905482310c
```

At this checkpoint, a fresh all-selector solve reports the same listed set
with `0--14` as its initial range: 128 UNSAT and 200 SAT orbits.

## Orbits 15 and 16

The orbit-15 continuation closed after 15 SAT residual supports. Its 120
independently audited minimum-activity factor-fork certificates reconstruct
exactly 288 new clauses. The resulting v28 CNF has 559 variables and
130,650 clauses, with SHA-256

```text
691b58cf5e7190113938e8f5467619cfb16b116c93b0848743a125c1f615fb28
```

The orbit-16 continuation then closed after eight residual supports. Its 64
independently audited certificates reconstruct exactly 268 new clauses.
The resulting v29 CNF has 559 variables and 130,918 clauses, with SHA-256

```text
6bef527f14379520ecdfa595d51e0d8cad8563014fe9fe09968a5d8901fb1d6a
```

A fresh all-selector solve reports exactly the 130-orbit UNSAT set above
and its 198-orbit SAT complement.

## Aggregate UNSAT proof

Appending one positive clause containing exactly the 130 UNSAT selectors
to v29 gives a 130,919-clause conditioned CNF with SHA-256

```text
dc65e77dcf468af1caade3f95efa867a37bc76127c6336d73a02df08402fa64a
```

Kissat generated a 1,634,179-byte DRAT proof with SHA-256

```text
448d413ab444582edc793984c2bbba143b4e8257d73747626ef4eec2ba71208a
```

Independent forward `drat-trim` verification returned `s VERIFIED`.

## One-command replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python claims/finite/n14/verify_fourteen_vertex_c6_8_130_orbits_kappa3.py
```

The verifier recursively replays the complete 129-orbit predecessor,
independently reconstructs the orbit-16 certificate family, audits all 328
selectors, compares the conditioned DIMACS sequence exactly, and reruns
forward `drat-trim`.

Its final output is
`tmp/fourteen_vertex_c6_8_130_orbits_kappa3_final_verified.json` and must
contain `"verified": true`.

## Boundary

This closes 130 of 328 first-factor orbits only for three-connected
supports in one remaining order-14 factor family. The other 198
`C6+C8` orbits, non-three-connected supports as a stand-alone finite
classification, the other unresolved factor types, and the global
conjecture remain unresolved.
