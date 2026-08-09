# Order-14 `C4+C4+C6` first-factor orbit-2 certificate

## Scope

This is a finite computer-assisted theorem for one first-factor orbit in
the order-14 `C4+C4+C6` equality architecture.  It is not a proof of the
full family or of the Krenn--Gu conjecture.

No support exists whose pinned first singleton perfect matching belongs
to census orbit 2.

## Fresh reconstruction

The one-command audit independently reconstructs the complete certificate
chain.  It:

1. replays 17 rich fixed-support certificates;
2. replays 2,357 earlier minimum-activity certificates;
3. replays 168 new orbit-2 minimum-activity certificates;
4. reconstructs their 3,712 new transport clauses; and
5. confirms that the resulting global formula remains SAT before the
   orbit-2 selector is imposed.

The 324-variable, 952,108-clause global CNF has SHA-256

```text
c389a52cf9a2472a4caf5ddc193bc33ac611b7111f2f6aadede5e94189845b01
```

## Conditioned UNSAT proof

Appending the orbit-2 selector unit gives a 952,109-clause conditioned CNF
with SHA-256

```text
0469e354f262a0cf5a19330532b0ba55621a69795324a6f54e3e4628ab96fc49
```

Kissat generated a 54,151,092-byte DRAT proof with SHA-256

```text
5f1249a3c013920f308cf4f3b3820aae774d2993e7aea34d7afd8a73286c025a
```

The independent `drat-trim` checker returned `s VERIFIED`.

## One-command replay

With the pinned repository runtime (`requirements.txt`) installed, run:

```text
python claims/finite/n14/verify_fourteen_vertex_c4_c4_c6_orbit2.py
```

The final audit is
`tmp/fourteen_vertex_c4_c4_c6_orbit2_final_verified.json` and contains
`"verified": true`.

## Boundary

This excludes one pinned first-factor orbit in the remaining
`C4+C4+C6` family.  Other open selectors and the global conjecture remain
unresolved.
