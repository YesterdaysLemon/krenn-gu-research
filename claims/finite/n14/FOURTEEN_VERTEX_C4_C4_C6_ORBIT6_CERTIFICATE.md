# Order-14 `C4+C4+C6`, connectivity-at-least-3, orbit-6 certificate

## Scope

This is a finite computer-assisted theorem for one first-factor orbit in
the order-14 `C4+C4+C6` equality architecture. It explicitly assumes
that the support skeleton has vertex connectivity at least three. It is
not an unconditional classification of the complete factor family and
is not a proof of the Krenn--Gu conjecture.

Under that connectivity hypothesis, no support exists whose pinned first
singleton perfect matching belongs to census orbit 6.

This conditional exclusion is relevant to the global problem because
Chandran, Gajjala, and Illickan prove that a minimal Krenn--Gu
counterexample must be 4-connected:

<https://arxiv.org/abs/2407.00303>

## Reconstructed rule layer

The clean predecessor contains the matching, disjointness, selector, and
previously certified semantic rule layers together with all explicit
vertex-connectivity-at-least-three quotient cuts. Its SHA-256 is

```text
e2d315a63071a22fc4ef148871a1dc52ae879c290f6e004c0b4a203c2e4aea07
```

A targeted orbit-6 continuation used 50 SAT residual supports and then
closed. It produced 400 independently audited minimum-activity
factor-fork certificates. Independent symmetry transport and
deduplication reconstruct exactly 5,824 fresh clauses.

The resulting 324-variable, 1,094,929-clause CNF has SHA-256

```text
2207a51d06e4a9b89d6062933c2195838295eed1c18b21da2d7727341945b318
```

## Conditioned UNSAT proof

Appending DIMACS selector 238 gives a 1,094,930-clause conditioned CNF
with SHA-256

```text
4bd437f90a55ddeaf8bf8a6386aa7083005149fc2a98cb1d828d61dbd287665b
```

Kissat generated a 58,660,074-byte DRAT proof with SHA-256

```text
5052aa97e3fb07a88701b96582662c599e8c0e851f3c07abef3c8db0803ee1a4
```

Independent forward `drat-trim` verification returned `s VERIFIED`.

## One-command replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python claims/finite/n14/verify_fourteen_vertex_c4_c4_c6_orbit6.py
```

The verifier checks the connectivity prerequisite and source hashes,
independently reconstructs all 400 certificates and all 5,824 transported
clauses, compares the conditioned DIMACS sequence exactly, and reruns
forward `drat-trim`.

Its final output is
`tmp/fourteen_vertex_c4_c4_c6_orbit6_final_verified.json` and must
contain `"verified": true`. A fresh complete replay took 163.69 seconds.

## Boundary

This excludes one pinned first-factor orbit only for
three-connected supports in the still-open `C4+C4+C6` family. Other
selectors, the other unresolved full-factor types, and the global
conjecture remain unresolved.
