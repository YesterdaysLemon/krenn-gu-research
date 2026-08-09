# Order-14 `C4+C4+C6`, connectivity-at-least-3, orbit-7 certificate

## Scope

This is a finite computer-assisted theorem for one first-factor orbit in
the order-14 `C4+C4+C6` equality architecture. It explicitly assumes
that the support skeleton has vertex connectivity at least three. It is
not an unconditional classification of the complete factor family and
is not a proof of the Krenn--Gu conjecture.

Under that connectivity hypothesis, no support exists whose pinned first
singleton perfect matching belongs to census orbit 7.

This conditional exclusion is relevant to the global problem because
Chandran, Gajjala, and Illickan prove that a minimal Krenn--Gu
counterexample must be 4-connected:

<https://arxiv.org/abs/2407.00303>

## Reconstructed rule layer

The recursive verifier first replays the complete orbit-6 certificate.
Its 324-variable, 1,094,929-clause predecessor has SHA-256

```text
2207a51d06e4a9b89d6062933c2195838295eed1c18b21da2d7727341945b318
```

A targeted orbit-7 continuation used 68 SAT residual supports and then
closed. It produced 536 independently audited minimum-activity
factor-fork certificates. Independent symmetry transport and
deduplication reconstruct exactly 13,600 fresh clauses.

The resulting 324-variable, 1,108,529-clause CNF has SHA-256

```text
d7875f904203aa311718d265cd1e14012c3abc9270f1557140c231ebd2713f97
```

## Conditioned UNSAT proof

Appending DIMACS selector 239 gives a 1,108,530-clause conditioned CNF
with SHA-256

```text
00a08e9f6830ffe05a8ccdb3b5a9c1be6c6651e87601cd1e2a021372bcab7199
```

Kissat generated a 57,156,850-byte DRAT proof with SHA-256

```text
3d4a5fc812beb3b166bcfd4f338e9a7b01e57d71e0f1b54a3e75dd883dd5994f
```

Independent forward `drat-trim` verification returned `s VERIFIED`.

## One-command replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python claims/finite/n14/verify_fourteen_vertex_c4_c4_c6_orbit7.py
```

The verifier recursively replays orbit 6, independently reconstructs all
536 orbit-7 certificates and all 13,600 transported clauses, compares the
conditioned DIMACS sequence exactly, and reruns forward `drat-trim`.

Its final output is
`tmp/fourteen_vertex_c4_c4_c6_orbit7_final_verified.json` and must
contain `"verified": true`. A fresh complete recursive replay took 453.38
seconds.

## Boundary

This excludes one pinned first-factor orbit only for three-connected
supports in the still-open `C4+C4+C6` family. Other selectors, the other
unresolved full-factor types, and the global conjecture remain unresolved.
