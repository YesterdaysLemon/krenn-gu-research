# Order-14 `C4+C4+C6` first-factor orbit-5 certificate

## Scope

This is a finite computer-assisted theorem for one first-factor orbit in
the order-14 `C4+C4+C6` equality architecture. It explicitly assumes
that the support skeleton has vertex connectivity at least three. It is
not an unconditional classification of the complete family and is not a
proof of the Krenn--Gu conjecture.

Under that connectivity hypothesis, no support exists whose pinned first
singleton perfect matching belongs to census orbit 5.

## Reconstructed rule layer

The starting globally reconstructed CNF already contains the late simple
rules, rich fixed-support rules, 2,357 global minimum-activity
certificates, the orbit-2 layer, all vertex-connectivity-at-least-three
quotient cuts, and the orbit-3 layer. Its SHA-256 is

```text
5c798fdb3a7e5b16aeebbab7670e57ddcc6838cf461bf747da98fd9a5453facc
```

A targeted orbit-5 search then produced 96 independently audited
three-connected minimum-activity certificates. Independent symmetry
transport reconstructs exactly 4,720 fresh clauses and the exact DIMACS
sequence. The resulting 324-variable, 1,099,681-clause CNF has SHA-256

```text
31338df2b71b2b44eed6cd46886d48d4edda9a6cced909d3afcb2f570bb7854c
```

It remains SAT until the orbit-5 selector is imposed.

## Conditioned UNSAT proof

Appending DIMACS selector 237 gives a 1,099,682-clause conditioned CNF
with SHA-256

```text
7d3150f38f343f9a3db6800ee04b1a729befa8ead07902186309820f911f4a7e
```

Kissat generated a 57,680,258-byte DRAT proof with SHA-256

```text
a8ba52e301213d381ab889ddefec807f7d10b9f4a31f83a03ebf49b350ea2703
```

The independent `drat-trim` checker returned `s VERIFIED`.

## Replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python verify_fourteen_vertex_c4_c4_c6_orbit5.py
```

The replay independently reconstructs the orbit-5 augmentation, checks
the conditioned clause sequence, and reruns `drat-trim`. Its final audit
is `tmp/fourteen_vertex_c4_c4_c6_orbit5_final_verified.json`.

## Boundary

This excludes one pinned first-factor orbit only for three-connected
supports in the still-open `C4+C4+C6` family. Other selectors and the
global conjecture remain unresolved.
