# Order-14 `C4+C10` first-factor orbit-1 certificate

## Scope

This is a finite computer-assisted theorem for one first-factor orbit in
the order-14 `C4+C10` equality architecture.  It is not a proof of the
full family or of the Krenn--Gu conjecture.

## Fresh reconstruction

Starting from the original 425-selector base CNF, the reconstruction
independently replays 882 minimized factor-fork certificates and their
audits.  Exact symmetry transport and deduplication add 19,632 clauses.
The resulting global CNF has 656 variables and 118,308 clauses.  Its
SHA-256 is

```text
55735d617a4b10a74d67849aacce1c473015759df3699245a7629b1694b38c64
```

The independent reconstruction verifier checks every source hash, audit,
transport, and output clause, then confirms that the global formula
remains SAT.

## Exact selector frontier

All 425 selector assumptions are solved independently.  The result is
exactly

```text
UNSAT: 1
SAT:   0, 2, 3, ..., 424
```

Orbit 0 is absent from this particular rule reconstruction; it has its own
independently replayed certificate in
`FOURTEEN_VERTEX_C4_C10_ORBIT0_CERTIFICATE.md`.

## DRAT proof

Appending the orbit-1 selector unit gives a conditioned CNF with SHA-256

```text
13e8e36757723cd48a0d2906189b0123b3e0b520a7248ccc58e4db0e9e558735
```

Kissat generated a 1,673,263-byte DRAT proof with SHA-256

```text
e24177dab35d0b6efb271dba03f5af4910f3b808e60fa0af0729fd5cac5a101b
```

The independent `drat-trim` checker returned `s VERIFIED`.

## One-command replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python claims/finite/n14/verify_fourteen_vertex_c4_10_orbit1.py
```

The verifier reconstructs all learned clauses, audits all selectors,
checks the conditioned formula, and replays the DRAT proof.

## Boundary

Together with the separate orbit-0 certificate, this excludes two of 425
first-factor orbits in the `C4+C10` family.  The other 423 orbits and the
global conjecture remain unresolved.
