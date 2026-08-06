# Order-14 `C6+C8`, connectivity-at-least-3, 122-orbit certificate

## Scope

This is a finite computer-assisted theorem inside the order-14
`C6+C8` equality architecture. It explicitly assumes that the support
skeleton has vertex connectivity at least three. It is not an
unconditional exclusion of all `C6+C8` supports and is not a proof of the
full Krenn--Gu conjecture.

Under that connectivity hypothesis, no support exists whose pinned first
singleton perfect matching belongs to any of these 122 census orbits:

```text
0--8
100--144
171--173, 179, 182, 185, 187--189
200--218, 220--225, 227, 232, 233, 238, 247, 269
300--327
```

The other 206 first-factor orbits remain SAT in this rule checkpoint.

This conditional frontier is relevant to the global problem because
Chandran, Gajjala, and Illickan prove that a minimal Krenn--Gu
counterexample must be 4-connected:

<https://arxiv.org/abs/2407.00303>

## Certified predecessor

The one-command verifier first reruns
`verify_fourteen_vertex_c6_8_121_orbits_kappa3.py`. That predecessor
reconstructs the v18 rule base, independently appends all 1,947
vertex-connectivity-at-least-three quotient cuts, replays the orbit-7
certificate layer, audits all selectors, and verifies its aggregate
DRAT proof.

The resulting v20 predecessor has 559 variables and 126,902 clauses. Its
SHA-256 is

```text
39e3770c6feaf67a58c873bc0d3dfc10f1f809b010389971dd51be8a256f89e6
```

## The 122nd orbit

A targeted continuation on orbit 8 produced 208 independently audited
minimum-activity factor-fork certificates across 26 SAT iterations.
Their activation premises have size one through four. Independent
symmetry transport and deduplication add exactly 238 clauses.

The resulting v21 CNF has 559 variables and 127,140 clauses. Its SHA-256
is

```text
8a03d170099f2dea4fe8fd8457dbbad4f85fdc1fc2811bb6559a1d01c0a9822d
```

An exact solve under all 328 selector assumptions reports the 122-orbit
list above as UNSAT and its 206-orbit complement as SAT.

## Aggregate UNSAT proof

Appending one positive clause containing exactly the 122 UNSAT selectors
gives a 127,141-clause conditioned CNF with SHA-256

```text
3b6b497fedfcb80433c9292b6a9def1654effdd1f923c257c8e64e80e6284819
```

Kissat generated a 2,847,347-byte DRAT proof with SHA-256

```text
06f33bde596365061a444ae4b0be6eab9b5091fb347aee1919ae2b6043013fff
```

Independent forward `drat-trim` verification returned `s VERIFIED`.

## One-command replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python verify_fourteen_vertex_c6_8_122_orbits_kappa3.py
```

The verifier recursively replays the complete 121-orbit predecessor,
independently reconstructs the 208 orbit-8 certificates and 238
transported clauses, audits all 328 selectors, compares the conditioned
DIMACS sequence exactly, and reruns forward `drat-trim`.

Its final output is
`tmp/fourteen_vertex_c6_8_122_orbits_kappa3_final_verified.json` and must
contain `"verified": true`. A fresh complete replay took 65.13 seconds.

## Boundary

This closes 122 of 328 first-factor orbits only for three-connected
supports in one remaining order-14 factor family. The other 206
`C6+C8` orbits, non-three-connected supports as a stand-alone finite
classification, the other unresolved factor types, and the global
conjecture remain unresolved.
