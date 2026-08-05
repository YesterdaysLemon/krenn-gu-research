# Route A — sparse-resultant cores (symbolic route)

Branch: `symbolic/sparse-resultant-cores`, forked from the merged
canonical continuation (`main` @ f24782f, PR #27).

## Why this branch exists

`P5_ALTERNATIVE_STRATEGY_MAP.md` Route A is the program of converting
the large exact-three `C10`/`C4+C6` support computations into
human-scale symbolic identities.  The existing certificate union —
binary fork (1,328 orbits), triangle (+113), odd five-cycle (+74),
scalar-span, degree-one Macaulay — is itself the evidence that
sparse-template identities do the work: each is a short monomial-linear
relation like `P+Q-m*R=2` over characteristic zero, proved once and
replayed symbolically across hundreds of orbits.

The map records that ~8,101 of the 11,751 audited `C10` orbits are not
covered by that union, and names the next step explicitly:

> enumerate short monomial-linear relations directly in the sparse
> coefficient-vector matroid, then cluster the resulting exact
> certificates.

That step is symbolic linear algebra over `Q`, not support enumeration.
It is the natural continuation of the symbolic route.

## What exists

- `sat_catalogue` generation and audit scripts under
  `research_snapshots/2026-07-27-p5-coordinate-cegar/` (now gitignored
  dumps; the packaged generators remain tracked and reproduce them);
- the five template theorem docs
  (`P5_C10_BINARY_FORK_OBSTRUCTION.md`,
  `P5_C10_TRIANGLE_OBSTRUCTION.md`,
  `P5_C10_ODD_CYCLE5_OBSTRUCTION.md`,
  `P5_C10_SCALAR_SPAN_OBSTRUCTION.md`,
  `P5_C10_DEGREE_ONE_MACAULAY_OBSTRUCTION.md`)
  with their symbolic replay generators;
- `probe_p5_c10_joint_affine_class.py` — the geometry-vs-affine-class
  probe whose negative result (geometry does not determine the core)
  motivates working at the coefficient-matroid level instead.

## Attack plan (symbolic only)

1. **Coefficient-vector representation.**  For a representative sample
   of survivor orbits (start with the 15 sharing orbit 384's canonical
   backbone, already split 11 affine-unit / 4 affine-non-unit), extract
   the sparse coefficient vectors of their mixed-equation systems over
   `Q`, keyed by monomial support.  No Gröbner runs in this step.
2. **Short-relation matroid scan.**  In each coefficient vector space,
   enumerate linear dependencies of size ≤ 6 among the forbidden
   coefficient forms `1+m*A`, `A+B`, ... (the shape that made the fork
   and triangle templates characteristic-zero immediate).  Exact
   rational arithmetic only; dependencies are certificates by
   construction.
3. **Cluster and quotient.**  Quotient found relations by variable
   relabelling and torus gauge (the two equivalences the map says a
   reusable theorem must respect).  Count resulting classes; the hope
   is a small number of identity types covering a large orbit fraction.
4. **Replay generators.**  For each new class, write the
   replay-generator pattern of the existing five theorem docs: one
   symbolic proof, independently replayed per orbit, byte-checked.

Explicitly out of scope on this branch: any new support enumeration,
any SAT run, any brute-force search.  If a step degenerates into
enumerating more supports, the plan is wrong and stops there.

## Deliverables

- one theorem doc per new identity class discovered (same standard as
  the five existing: exact statement, symbolic proof, independent
  replay generator);
- a coverage ledger: union of template classes vs the 11,751-orbit
  catalogue, updated as classes land;
- no global-status claim; the conjecture stays **UNRESOLVED**.
