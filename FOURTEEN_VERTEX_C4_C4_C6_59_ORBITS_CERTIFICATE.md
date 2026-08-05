# Order-14 `C4+C4+C6` 59-orbit certificate

## Scope

This is a finite computer-assisted theorem inside the order-14
`C4+C4+C6` equality architecture. It explicitly assumes that the support
skeleton has vertex connectivity at least three. Under that hypothesis,
it excludes 59 of the 93 possible orbits of the pinned first singleton
perfect matching. It is not an unconditional classification of the
complete factor family and is not a proof of the Krenn--Gu conjecture.

This file is retained as the 59-orbit checkpoint. It is superseded by
[`FOURTEEN_VERTEX_C4_C4_C6_61_ORBITS_KAPPA3_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_61_ORBITS_KAPPA3_CERTIFICATE.md).

The excluded orbit set is

```text
0--5, 12, 17--21, 23--35, 52--53, 58--62, 64--66, 69--92
```

The 34 selectors not excluded by this certificate are

```text
6--11, 13--16, 22, 36--51, 54--57, 63, 67--68
```

## Aggregate 58-orbit theorem

The global reconstruction independently replays:

- 5,800 simple sources giving 982,563 transport no-goods;
- 37 audited fixed-support certificates giving 352 no-goods;
- 2,357 minimum-activity certificates giving 92,386 no-goods;
- 168 orbit-2 certificates giving 3,712 no-goods;
- 2,576 vertex-connectivity-at-least-three quotient cuts; and
- 272 orbit-3 certificates giving 5,856 no-goods.

The resulting 324-variable, 1,094,961-clause CNF has SHA-256

```text
5c798fdb3a7e5b16aeebbab7670e57ddcc6838cf461bf747da98fd9a5453facc
```

An exact per-selector audit classifies 58 orbits as UNSAT and the other
35 as SAT in this rule layer. Appending the disjunction of the 58 UNSAT
selectors gives a 1,094,962-clause conditioned CNF with SHA-256

```text
3c2f44ab2f9e0d7b31666a36006757d999ffa89382530b5c327a80ef14726f4a
```

Kissat generated a 169,361,294-byte DRAT proof with SHA-256

```text
dd9df6fd8473556eccf3042dbd6068642b8276cf823aa6a7efeaf83f25a9615c
```

Independent forward `drat-trim` verification returned `s VERIFIED`.

## The 59th orbit

Orbit 5 is not in the aggregate selector clause above. A separate
extension of the same global CNF replays 96 further independently
audited three-connected minimum-activity certificates and reconstructs
4,720 fresh clauses. Its orbit-5-conditioned CNF and 57,680,258-byte
DRAT proof independently verify. The detailed hashes and reconstruction
chain are in
[`FOURTEEN_VERTEX_C4_C4_C6_ORBIT5_CERTIFICATE.md`](FOURTEEN_VERTEX_C4_C4_C6_ORBIT5_CERTIFICATE.md).

The two proofs therefore exclude 58 plus one distinct first-factor
orbits, for 59 of 93.

## Replay

With the repository runtime and `tmp/python_deps` on `PYTHONPATH`, run:

```text
python verify_fourteen_vertex_c4_c4_c6_58_orbits.py
python verify_fourteen_vertex_c4_c4_c6_orbit5.py
```

The commands reconstruct their complete rule layers, compare the exact
conditioned DIMACS sequences, and rerun `drat-trim`.

## Boundary

These proofs certify a finite selector frontier only in the
connectivity-at-least-three regime. They do not rule out the 34 listed
selectors, the other unresolved full-factor types, or the global
conjecture.
