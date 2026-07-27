# P5 coordinate-CEGAR research snapshot

Frozen on 2026-07-27 from the active search for a restriction
`P_5 -> Delta_3`.

## Status

**Exploratory and globally unresolved.** None of the ledgers in this
snapshot is an UNSAT certificate, a surviving complex restriction, or a
proof of the Krenn--Gu conjecture. Every state file has status
`IN_PROGRESS`.

The public theorem immediately before this snapshot proves that if all five
local maps have at most three coordinate rows, then they have exactly three
each and the ten non-coordinate cells form either `C10` or `C4+C6`. This
snapshot records the subsequent CEGAR search in that finite support layer
and in the complementary branch where a local map has four or five
coordinate rows.

## Frozen ledgers

| File | Branch | Learned exclusions | SHA-256 |
| --- | --- | ---: | --- |
| `states/p5_c10_coordinate_support_state.json` | fixed `C10` | 2,940 | `6c60ea9a4e99062d355640fef9ce15db92fe31dfa5d2fc1fb22283a68a0f5e7a` |
| `states/p5_high_coordinate_support_state.json` | at least four coordinate rows in one map | 580 | `db03ccbf0f83da9b64e08c093f23717b6519106df57720e3f14d3c615c5c6c62` |
| `states/p5_max3_coordinate_support_state.json` | earlier unrestricted maximum-three search | 960 | `46b675ae8d26b3b8fd390bf5bafdc8b8fbf8495448eddfdf044569bf5a4ffa95` |
| `states/p5_tricolour_support_cegar_state.json` | global preload | 2,650 | `17014b13cc37b387d46f267a4200481125d7a68236e0b9944fd18655ab8753a4` |
| `states/p5_pair_catalogue_cegar_state.json` | pair-signature preload | 200 | `5563ff2a63a5f3f2b68da423936e877e82a8bf5e2bfbaa77b052555518977462` |

Each record contains the exact Boolean clause, its five local supports, the
claimed contradiction mechanism, and the corresponding finite or algebraic
certificate metadata. The two active branch ledgers exclude 3,520 models;
they do not exhaust either branch.

The frozen copies differ from the live JSON only by replacing
machine-local absolute `source`/`log` paths with portable `tmp/...` paths.
The clauses, supports, certificate payloads, ordering, and status fields are
unchanged.

## Code

The active programs are deliberately tracked at their original `tmp/`
paths because they import one another from that layout:

- `tmp/probe_p5_tricolour_support_sat.py`: common SAT, lattice, closure,
  symmetry, and Singular machinery;
- `tmp/probe_p5_hall_hierarchy_csp.py` and
  `tmp/p5_local_signatures_cache.json`: finite-field construction and
  fingerprinted cache for the 6,495 local signatures;
- `tmp/probe_p5_max3_coordinate_support.py`: fixed-shape and
  high-coordinate CEGAR driver;
- `tmp/generate_p5_signature_laurent_singular.py`: exact Laurent-system
  generator;
- `tmp/audit_p5_coordinate_support_ledger.py`: fail-closed semantic ledger
  replay;
- `tmp/audit_p5_fixed_shape_symmetry.py`: fixed-shape orbit/transport
  audit;
- `tmp/audit_p5_global_preload_symmetry.py`: global preload orbit audit;
- `tmp/write_p5_fixed_shape_replay_cnf.py`: replay-CNF materializer.

The Python layer uses `python-sat` and `sympy`. Algebraic fallbacks invoke
`/usr/bin/Singular` through WSL.

## Audit boundary

The included audit outputs record:

- semantic replay of all 960 earlier maximum-three records;
- semantic replay of the first 1,400 `C10` records;
- semantic replay of all 2,650 global-preload records, with 2,647 exact
  mechanism matches and three sound alternative signature-level
  contradictions;
- independent order-150 symmetry transport of the 2,650-record global
  preload.

Additional checks performed before freezing, but not represented as a full
audit of the final frozen suffix, include a fixed-`C10` group/transport
audit at 1,910 records and semantic replay of the first 111 high-coordinate
records. Consequently the 2,940-record `C10` and 580-record high-coordinate
files are **work ledgers, not fully audited certificates**.

The raw Singular source/log collection is not included in this Git
snapshot: it comprised 3,202 generated files (about 27.8 MB) with
machine-local absolute paths. The JSON retains the exact signature tuples
and recorded outcomes, but the current default auditor expects those raw
files. A portable artifact bundle or a fresh `--rerun-singular` audit is
still required for full CAS replay from a new clone.

## Historical limitation and post-snapshot resolution

The high-coordinate run encountered a valid coefficient-relation lattice
whose selected pivot minor had determinant `2`. The current Laurent
generator supports only unimodular pivot elimination, so this case is
unprocessed—not a survivor and not a contradiction.

The runner now converts generator failures into a structured
`CAS_INCONCLUSIVE` result instead of crashing. The change passes Python
compilation. A live regression attempt advanced the high-coordinate ledger
from 430 to 580 exclusions before its bounded harness ended, but it did not
reach the determinant-2 model again; runtime confirmation of that exact
path remains pending.

That pending runtime confirmation is now complete. The live generator
retains a non-unimodular relation lattice as an implicit saturated binomial
ideal. A guarded deterministic replay reproduced all 430 historical clauses
and then reached three actual determinant-`2` strata. Singular `slimgb`, an
independent Singular `std` regeneration, and `msolve 0.6.5` all return the
unit ideal for all three. A focused semantic audit also replays the three
resulting five-literal clauses exactly.

The sources, logs, msolve inputs/outputs, normalized ledger, mathematical
equivalence argument, and portable verifier are in
[`nonunimodular_boundary/`](nonunimodular_boundary/README.md). This closes
the implementation limitation; it does not complete either finite branch.

## Proper all-full tricolour boundary

A later exact calculation closes one structured part of both
exact-three-coordinate cycle families.  If every non-coordinate cell is
fully supported and the singleton coordinate colours occur once per colour
in every mode and source row, there are exactly three support orbits: two
with full-cell graph `C10` and one with graph `C4+C6`.

For every orbit, the 150 mixed permanent coefficients using all three
target colours, together with the nonzero-entry and nonzero-pure-amplitude
conditions, generate the unit ideal over `Q`.  No two-colour mixed equation
is used.  Singular `slimgb` and an independent `msolve` conversion both
certify all three cases, and a separate orbit census proves coverage.

The portable sources, inputs, outputs, and verifier are in
[`all_full_tricolour_boundary/`](all_full_tricolour_boundary/README.md).
This is an exact finite theorem, but it does not cover partial
non-coordinate supports, non-proper singleton colours, or the
four/five-coordinate-row branch.

## Entire all-full boundary

The apparent non-proper singleton-colour boundary is now closed as well.
The source-row tricolour cover already forces the singleton colours in
each source column to be `0,1,2`.  An exhaustive quotient by the
automorphisms of `C10` and `C4+C6`, together with global colour
permutation, gives 226 support orbits.

The complex pair-incidence catalogue and Hall quotas exclude 213 support
orbits.  Three row-proper orbits are exactly those covered by the earlier
theorem.  The other ten supports contain 198 viable five-tuples of local
pair signatures.  Their exact Laurent systems all generate the unit ideal
over `Q`, and hence have no solutions over `C`.

The finite audit, semantic system regenerator, hashes, Singular results,
and partial second-engine cross-check are in
[`all_full_boundary/`](all_full_boundary/README.md).  This imports one
sound all-full blocking clause into each fixed-shape search; it does not
make either ledger an exhaustive certificate.

## Exact-one-partial boundary

The next complete support layer is also impossible.  Choose exactly one
of the ten non-coordinate cells to have mask `3`, `5`, or `6`, leaving
the other nine with mask `7`.  The two fixed graphs have 466,560 labelled
supports and exactly 5,676 support orbits.  Of these, 224 are absent from
the complex-valid local catalogue and 5,133 fail the 30 pair Hall quotas.

For each of the remaining 319 supports, an exact support-only coefficient
system retains every nonzero mixed permanent coefficient and saturates by
all 25 Laurent parameters and the three pure coefficients.  Singular
returns the unit ideal directly for 307 systems and via an exactly
equivalent split saturation for 12.  Because the systems omit all
pair-incidence relations, each contradiction excludes the entire support
stratum rather than only one local-signature tuple.

The exhaustive audit, semantic regenerator, hashes, and exact outputs are
in [`one_partial_boundary/`](one_partial_boundary/README.md).  Together
with the all-full result, this imports the sound condition that every
remaining fixed-shape model has at least two partial non-coordinate
cells.

## Exact-two-partial boundary

The next layer is impossible too.  Across `C10` and `C4+C6`, exactly two
partial cells give 6,298,560 labelled supports and 76,098 fixed-shape
support orbits.  The local catalogue rejects 11,614 orbits, the 30 pair
Hall quotas reject 59,911, and the pure/unique-mixed support semantics
reject another 1,265.

For each of the remaining 3,308 supports, a connected gauge graph leaves
24 Laurent parameters.  The exact support-only coefficient ideal retains
every nonzero mixed permanent coefficient and saturates by all parameters
and the three pure coefficients.  Singular returns the unit ideal
directly for 3,307 systems and through one exactly equivalent split
saturation for the last system.

The independent audits, semantic regenerator, hashes, manifest, and exact
outputs are in [`two_partial_boundary/`](two_partial_boundary/README.md).
Together with the two preceding layers, this forces every remaining
fixed-shape model to have at least three partial non-coordinate cells.

## Exact-three-partial boundary

The next layer is impossible too.  Independent fixed-shape audits
regenerate 25,194,240 labelled supports per shape and agree with the
symmetry-broken catalogues on 5,993 final `C4+C6` orbits and 11,751 final
`C10` orbits.  Exact characteristic-zero support-only coefficient ideals
are the unit ideal for every one of the 17,744 systems.

The `C4+C6` and `C10` replay packages are in
[`three_partial_c4c6_boundary/`](three_partial_c4c6_boundary/README.md)
and
[`three_partial_c10_boundary/`](three_partial_c10_boundary/README.md).
Together with the preceding layers, this forces every remaining
fixed-shape model to have at least four partial non-coordinate cells.

## Next proof obligations

1. Independently replay the frozen `C10` suffix and all high-coordinate
   records.
2. Close the four-through-ten-partial layers in both shapes, then the
   four/five-coordinate-row branch.
3. Only after finite exhaustion, lift the `P_5` obstruction back to the
   arbitrary-order graph problem.
