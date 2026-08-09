# Order-14 `C6+C8`, connectivity-at-least-3, 121-orbit certificate

## Scope

This is a finite computer-assisted theorem inside the order-14
`C6+C8` equality architecture. It explicitly assumes that the support
skeleton has vertex connectivity at least three. It is not an
unconditional exclusion of all `C6+C8` supports and is not a proof of the
full Krenn--Gu conjecture.

Under that connectivity hypothesis, no support exists whose pinned first
singleton perfect matching belongs to any of these 121 census orbits:

```text
0--7
100--144
171--173, 179, 182, 185, 187--189
200--218, 220--225, 227, 232, 233, 238, 247, 269
300--327
```

The other 207 first-factor orbits remain SAT in this rule checkpoint.

This conditional frontier is relevant to the global problem because
Chandran, Gajjala, and Illickan prove that a minimal Krenn--Gu
counterexample must be 4-connected:

<https://arxiv.org/abs/2407.00303>

## Audit correction

The earlier 118- and 119-orbit documents described their exclusions
without a connectivity qualifier. Their late learned clauses were
reconstructed from certificates minimized in the scope
`three_connected_perfect_matching_edge_disjoint`, while their final CNFs
did not explicitly contain the connectivity clauses. The file and DRAT
replays were exact, but the theorem scope was overstated.

This certificate repairs that gap. It starts from the reconstructed v18
rule base, explicitly appends and independently reconstructs every
vertex-connectivity-at-least-three quotient cut, and only then promotes
the frontier.

## Explicit connectivity layer

The connectivity generator considers all 106 deleted vertex sets per
first-factor orbit and adds 1,947 distinct quotient-cut clauses. An
independent implementation reconstructs every clause, the exact DIMACS
sequence, and a SAT solve of the resulting formula.

The connectivity-augmented v19 CNF has 559 variables and 126,610 clauses.
Its SHA-256 is

```text
dbc738942cb7e2cac3af2587075d63e97fd099236f61174578035b6ba7df6561
```

At this point orbit 144 is also UNSAT, giving a 120-orbit conditional
frontier.

## The 121st orbit

A targeted continuation on orbit 7 produced 184 independently audited
minimum-activity factor-fork certificates across 23 SAT iterations. The
activation premises have size one through four. Independent symmetry
transport and deduplication add exactly 292 clauses.

The resulting v20 CNF has 559 variables and 126,902 clauses. Its SHA-256
is

```text
39e3770c6feaf67a58c873bc0d3dfc10f1f809b010389971dd51be8a256f89e6
```

An exact solve under all 328 selector assumptions reports the 121-orbit
list above as UNSAT and its 207-orbit complement as SAT.

## Aggregate UNSAT proof

Appending one positive clause containing exactly the 121 UNSAT selectors
gives a 126,903-clause conditioned CNF with SHA-256

```text
784fa389c5503c6958f0661c6013aca87dfb62fdfa7a3918997117d564524424
```

Kissat generated a 3,328,458-byte DRAT proof with SHA-256

```text
59020245f2b7c9633cdc9ebf705af01fc09ec20c413eee0c2cfebae0ee4a43d2
```

Independent forward `drat-trim` verification returned `s VERIFIED`.

## One-command replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python verify_fourteen_vertex_c6_8_121_orbits_kappa3.py
```

The verifier reconstructs the complete v18 predecessor rule base,
independently rebuilds all 1,947 connectivity clauses, independently
replays the 184 orbit-7 certificates and 292 transported clauses, audits
all 328 selectors, compares the conditioned DIMACS sequence exactly, and
reruns forward `drat-trim`.

Its final output is
`tmp/fourteen_vertex_c6_8_121_orbits_kappa3_final_verified.json` and must
contain `"verified": true`.

## Boundary

This closes 121 of 328 first-factor orbits only for three-connected
supports in one remaining order-14 factor family. The other 207
`C6+C8` orbits, non-three-connected supports as a stand-alone finite
classification, the other unresolved factor types, and the global
conjecture remain unresolved.
