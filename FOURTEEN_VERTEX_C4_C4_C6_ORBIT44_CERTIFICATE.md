# Order-14 `C4+C4+C6` first-factor orbit-44 certificate

## Claim

Inside the order-14 equality architecture with full factor
`C4+C4+C6` and support-skeleton vertex connectivity at least three,
there is no three-colour witness whose pinned first singleton perfect
matching lies in orbit 44.

This is a finite computer-assisted theorem.  The connectivity hypothesis
contains the known 4-connected minimal-counterexample regime, but the
claim does not close the other 26 first-factor orbits, the other
architectures, higher orders, or the global Krenn--Gu conjecture.

## Predecessor frontier

The independently accumulated full-colour predecessor is

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit16_symbinomial300_orbit49support1.cnf
```

with 324 variables, 4,716,109 clauses, and SHA-256

```text
e9482392e9c6568190ba6a1a4cd6c23025e7c8fd5a17fc5ff0c582cf864adb35
```

Selector 276 represents pinned first-factor orbit 44.  It is SAT in the
predecessor.

## Exact 24-model boundary

Fresh exhaustive enumeration under selector 276 finds exactly 24 factor
assignments.  Negating the 21 selected factor-edge variables in each
assignment gives 24 width-21 support no-goods, and the enumerated clause
set exactly equals the deletion-irredundant core mined from the later
UNSAT extension.

This is not merely a solver core assertion.  Every one of the 24 clauses
occurs verbatim in an independently verified algebraic support-symmetry
clause set:

```text
8 clauses from the first certified support orbit;
16 clauses from the second certified support orbit.
```

Those two source orbits contain 2,304 and 4,608 clauses respectively.
Their standalone verifiers reconstruct the perfect-matching support,
mandatory signed integer-lattice relations, terminal forbidden amplitude,
all full-factor automorphisms, all six colour permutations, and every
transported no-good.

The 24 factor assignments have a rigid cycle classification:

```text
unique factors by singleton role: 1, 16, 16

roles 0+1: C6+C8       in all 24 assignments
roles 0+2: C6+C8       in all 24 assignments
roles 1+2: C4+C4+C6    in all 24 assignments
```

The exact enumeration and source binding are in

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_core24_models_verified.json
```

with SHA-256

```text
b329e7d6d69e9c336a5d11a046377b3affd11b387701b0860dd0cc9f3a77c2a7
```

## Minimal DIMACS extension

`materialize_verified_dimacs_clause_subset.py` admits a selected clause
only when it occurs in at least one independently verified source.  It
then streams the predecessor, removes duplicates, and appends the selected
clauses deterministically.

`verify_materialized_dimacs_clause_subset.py` independently checks all
source hashes and verifier bindings, recomputes the 8/16 memberships,
rescans the predecessor, and rebuilds the complete output byte for byte.
No selected clause was already present.  The result is

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_core24.cnf
```

with 4,716,133 clauses and SHA-256

```text
5bea81cd27ae21111f9466c7088694fd3732e1ecae718f0229ef3e08a934cd2b
```

A fresh CaDiCaL assumption solve for every selector `232,...,324` gives
exactly 67 UNSAT and 26 SAT first-factor orbits.  Orbit 44 is the newly
excluded selector.  The survivors are

```text
9--11, 13--16, 22, 36--41, 45--51, 54--55, 57, 63, 68.
```

## UNSAT proof

Appending the exact selector unit

```text
276
```

gives the 4,716,134-clause conditioned CNF

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_core24_conditioned.cnf
```

with SHA-256

```text
d1b390a66aee3d748bd12799850fd3a153df8b45872a33f30c2a8f49072a4739
```

Kissat returns `UNSAT` and writes a raw DRAT proof:

```text
proof bytes:
192,160,906

proof SHA-256:
26ec2bbc5100d11a4e8b3cc181189c78643ba1563e68688f67869a7c12ba7c0b
```

Independent forward `drat-trim` replay returns `"verified": true` in
1,204.85 seconds.  Its bound record is

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_core24_drat_trim.json
```

with SHA-256

```text
419f0e33e3a169f291e0b740734a13a02e704071a4b9c74908336aeba2a09702
```

The compact top-level verifier freshly enumerates the 24 predecessor
models, reruns the byte-identical materialization audit, decides all 93
selectors, checks exact streamed conditioning, binds the Kissat manifest
and raw proof, and verifies the stored forward replay.  That complete
nonredundant invocation returned `"verified": true`:

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_core24_final_stored_replay_verified.json

SHA-256:
825c4033a3e3a1d259e45832a5150fe732a04d8db295fac2d04733320f37a8c6
```

By default, the same entry point also launches a redundant fresh forward
DRAT replay.  The option `--skip-fresh-drat-replay` is what produced the
faster bound record above.  The default invocation has now also finished:

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_core24_final_verified.json

SHA-256:
1d0720cbaff4f4f12b119dda26f2cd338f2011badf47d75a5adf2845552130cb
```

That record binds a newly generated forward-replay result

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_core24_drat_trim_fresh_recheck.json

SHA-256:
b71b909e8285f0c15bf5bd78cdce7eeb68c6c1cca4be2a2a7f4770ca04a094af
```

and returned `"verified": true`.  Thus the compact path has both a stored
forward replay and a later fresh forward replay of the same bound raw
proof.

## Redundant full-extension path

The original discovery-independent route keeps all 6,912 sound symmetry
images from the two algebraic support types rather than the minimized 24.
Its final CNF has 4,723,021 clauses.  A separate 192,421,858-byte DRAT
proof passes two forward replays, including a fresh replay launched by the
top-level extension verifier.

The resulting end-to-end record is

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_extension_verified.json
```

with SHA-256

```text
73f2d102b79fe279eed0cd360cfa63b126578db378a3d60de51b2da6d8ad7ac6
```

It independently reconstructs both algebra certificates, the full
6,912-clause augmentation, all 93 selector decisions, exact conditioning,
and the fresh DRAT replay.  Thus the minimized theorem is backed by two
different materialized extensions and two different raw proofs.

## Replay

With the bundled dependencies on `PYTHONPATH`, run:

```text
python verify_fourteen_vertex_c4_c4_c6_orbit44_core24.py
```

This performs the compact end-to-end audit and a redundant fresh forward
DRAT replay.  To check every stage while trusting the already verified
stored replay record, run:

```text
python verify_fourteen_vertex_c4_c4_c6_orbit44_core24.py \
  --skip-fresh-drat-replay
```

The independent larger path is:

```text
python verify_fourteen_vertex_c4_c4_c6_orbit44_extension.py
```

Both theorem paths retain `"global_conjecture_resolved": false`.

## Updated finite frontier

Combining orbit 44 with the prior 66-orbit union excludes 67 of the 93
pinned first-factor orbits under vertex connectivity at least three.  The
26 selectors listed above remain open in this Boolean/algebraic frontier.
The finite theorem is a strict advance, not a proof of the complete
`C4+C4+C6` family.
