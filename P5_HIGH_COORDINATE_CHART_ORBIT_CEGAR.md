# High-coordinate P5 chart-orbit CEGAR

## Status

This is an active exact-computation strategy for the normalized
high-coordinate branches of a possible restriction

```text
P_5 -> Delta_3.
```

It is not a completed branch cover.  In particular, it does not yet
exclude `q5_311`, has not yet been run to completion on `q5_221` or
`q4_211`, does not prove the full `P_5` obstruction, and does not solve
the arbitrary-order Krenn--Gu prize conjecture.

## From individual charts to chart orbits

The normalized `q5_311` branch has a group of 288 exact symmetries:

```text
24 permutations of modes 1,2,3,4
12 simultaneous source/target-colour stabilizers
```

Mode zero remains fixed.  A branch-stabilizing symmetry transports:

- every closure mask;
- every gauge-forest pivot;
- the permanent coefficient equations; and
- the three nonzero pure coefficients.

Consequently one characteristic-zero unit-ideal calculation certifies
the complete orbit of its SAT clause.  This applies to ordinary
gauge-forest charts as well as to zero-pivot closures.

At the current local discovery boundary, 1,380 representative charts
from the pre-orbit ledger generate 336,672 distinct transported chart
clauses.  Together with the prior exact seed clauses, the startup cover
has 351,510 distinct clauses.  CaDiCaL still finds a model, so these
figures are a finite SAT boundary, not an obstruction theorem or a
frozen public certificate package.

The continuation driver learns chart orbits dynamically.  Each new
representative is checked against its source model and then contributes
up to 288 clauses at once.  Checkpoint resume regenerates the entire
transported orbit rather than restoring only the representative clause.

## Gauge-tree portfolio

Gröbner runtime depends strongly on the spanning-tree normalization,
even when two trees describe the same actual nonzero support.

One first orbit survivor illustrates the effect:

```text
historical tree: 213 distinct mixed equations, >180 s timeout
ranked alternative: 149 distinct mixed equations, UNIT_IDEAL in 5.703 s
```

The portfolio constructs deterministic maximal forests, ranks them by
the number of distinct mixed equations after normalization, and gives
each a short exact rational `dp` calculation.  A timeout is
inconclusive.  Only an explicit `UNIT_IDEAL` result is accepted.  If
the portfolio fails, the historical long calculation remains the
fail-closed fallback.

## Exact zero-cell closures

A local support cell may be empty.  Earlier discovery code enlarged an
empty cell to full support in its chart closure.  That was safe but
needlessly weak and could add three polynomial variables.

The chart language now represents mask zero exactly:

- the coefficient system has no variables in that cell; and
- the Boolean applicability antecedent requires all three entries to
  vanish, so its negated chart clause contains the three positive entry
  literals.

The independent ledger validator accepts zero masks, checks actual
support containment, and verifies that every reconstructed clause is
false on its source model.

## Process isolation and evidence rules

On Windows, the Singular process runs inside WSL under a Linux
`timeout` wrapper.  This prevents killing only `wsl.exe` while leaving
the Linux child holding output pipes.  A bounded retry is allowed only
for the explicit transient transport failure
`WSL/Service/E_UNEXPECTED`; algebraic timeouts, errors, and survivors
remain inconclusive.

Local monomial orders are deliberately not accepted as global
unit-ideal certificates.  During exploration, Singular's local `ds`
order returned `1` immediately on a broad chart.  The control ideal
`<x-1>` also returns `1` under `ds`, while a global `dp` order correctly
returns `x-1`.  The local result was therefore rejected before it
entered any ledger, solver, commit, or public claim.

Every active driver enforces at least a 20% host-available-memory floor.

## Low-degree certificate probes

Two exploratory tools test whether the large unit-ideal calculations
hide small linear certificates:

- `probe_p5_high_coordinate_split_scalar_span.py` reconstructs the
  split-saturation equations as sparse bitmask polynomials and searches
  modular coefficient spans, with exact rational reconstruction for
  any hit.  The first 100 zero-forest records produced no scalar or
  pure-in-mixed span hit.
- `extract_p5_high_coordinate_nullstellensatz.py` profiles a global
  `dp` basis or asks Singular for a lift matrix.  One ordinary basis
  reached the unit ideal with protocol degree around eight, while a
  full `liftstd` matrix did not finish within 90 seconds.

These are negative discovery results, not lower bounds on
Nullstellensatz degree and not evidence of a surviving restriction.

## Current continuation

The active `q5_311` run uses:

```text
pre-orbit representatives: 1,380
transported startup clauses: 351,510
dynamic transport: enabled
deterministic gauge alternatives: 16
short deadline per alternative: 6 seconds
host available-memory floor: 20%
```

Its state is exploratory until the branch is UNSAT and the complete
representative ledger, symmetry reconstruction, two independent SAT
solvers, and fresh characteristic-zero algebra replay all pass.
