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

## Known limitation found at the boundary

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

## Next proof obligations

1. Extend the Laurent parametrization to non-unimodular relation lattices,
   or certify those strata with a second exact algebra system.
2. Independently replay the frozen `C10` suffix and all high-coordinate
   records.
3. Finish both `C10` and `C4+C6`, then the four/five-coordinate-row branch.
4. Only after finite exhaustion, lift the `P_5` obstruction back to the
   arbitrary-order graph problem.
