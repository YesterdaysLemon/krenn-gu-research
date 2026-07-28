# High-coordinate P5 chart-orbit CEGAR

## Status

This is an active exact-computation strategy for the normalized
high-coordinate branches of a possible restriction

```text
P_5 -> Delta_3.
```

It is not a completed high-coordinate cover.  The normalized `q5_311`
branch has since been excluded analytically in
[`P5_Q5_311_EXCLUSION_THEOREM.md`](P5_Q5_311_EXCLUSION_THEOREM.md).
The computation has not been run to completion on `q5_221` or
`q4_211`, does not prove the full `P_5` obstruction, and does not solve
the arbitrary-order Krenn--Gu prize conjecture.

The `q5_221` branch now also has an analytic hyperplane-incidence
reduction to nine singleton-marked minimal types, plus an exact
paired-majority drop obstruction.  These are structural theorems, not a
completed branch cover:

- [`P5_Q5_221_HYPERPLANE_INCIDENCE_REDUCTION.md`](P5_Q5_221_HYPERPLANE_INCIDENCE_REDUCTION.md)
- [`P5_Q5_221_PAIRED_MAJORITY_DROP_OBSTRUCTION.md`](P5_Q5_221_PAIRED_MAJORITY_DROP_OBSTRUCTION.md)
- [`P5_Q5_221_MARKED_DOUBLE_ADJACENT_OBSTRUCTION.md`](P5_Q5_221_MARKED_DOUBLE_ADJACENT_OBSTRUCTION.md)
- [`P5_Q5_221_MARKED_DOUBLE_DISJOINT_OBSTRUCTION.md`](P5_Q5_221_MARKED_DOUBLE_DISJOINT_OBSTRUCTION.md)

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

## Retrospective orbit ranking and chart enlargement

`rank_p5_high_coordinate_chart_orbits.py` reconstructs every representative
orbit and evaluates its clauses on all recorded source models using exact
Boolean bitsets.  It reports both raw coverage and a deterministic greedy
set cover.  This replaces one-off visual selection by a reproducible answer
to:

```text
which certified chart family actually covers the most recorded survivors?
```

On a frozen 300-record continuation ledger, the four leading distinct
families covered 24, 23, 22, and 19 recorded models respectively.

`maximize_p5_high_coordinate_chart_closure.py` then enlarges one selected
closure while retaining its gauge forest.  It recursively tests groups of
nonpivot cells before pivot cells.  A cell is freed only after an exact
global-order unit-ideal result; a timeout or error leaves it constrained.
The four leading families were strengthened as follows:

```text
source record   old clause   relaxed clause   freed cells
146                  26              20             5
140                  27              21             4
196                  18              16             4
276                  26              20             5
```

All four relaxed sources were independently regenerated and freshly replayed
with Singular.  CaDiCaL and Glucose both accept their representative clauses
while retaining SAT, as expected for a strict intermediate cover.

## Two rare deleted-`P_4` slices

The normalized `q5_311` row has singleton multiplicities `3,1,1`.  Fixing
either rare mode-zero colour selects one source row, so the other four modes
must restrict the corresponding deleted-row `P_4` tensor to one nonzero
decomposable tensor.  The same four maps must do this for two different row
deletions and two independent target directions.

`probe_p5_q5_311_rare_slice_core.py` retains only those two mixed slices:
at most 160 mixed coefficients.  If it also retains the globally required
nonvanishing of all three pure coefficients, the frozen 300-record ledger
gives:

```text
unit ideals:                       300 / 300
certificate methods:              298 direct, 2 split
accepted elapsed range:           0.079 to 0.406 seconds
accepted elapsed mean:            0.1096 seconds
majority-colour mixed equations:  0
```

If only the two rare pure coefficients are saturated, 298 direct unit
ideals remain.  The two exceptions are exactly the two records whose full
certificates use split saturation.  One strict rare-only split system has a
proper positive-dimensional ideal.  Adding only nonvanishing of the
majority pure coefficient makes both exceptional split systems unit ideals;
none of the 80 omitted majority-colour mixed words is needed.

Thus all 300 recorded charts share one finite algebraic mechanism, with a
two-record pure-nonvanishing boundary.  This is still not a universal proof
or a complete branch cover.

One leading chart has a much shorter explanation.  Two exact affine
identities express its rare pure coefficients using five and four distinct
mixed coefficients, with six and five degree-at-most-one Macaulay rows.
All identity coefficients are `+1` or `-1`, so vanishing of the mixed
target words forces both rare pure amplitudes to vanish.  The chart and
independent symbolic verifier are in
[`P5_Q5_311_RARE_AFFINE_CORE.md`](P5_Q5_311_RARE_AFFINE_CORE.md).

The next continuation was stopped at 360 exact records and yielded 38 new
zero-gauge-forest closures, with no overlap against the earlier 34.  Direct
rare zero-forest saturation closes 36.  The two timeouts have exact
support-stratified covers of 16 and 25 charts.  Those covers use the 6,495
complex-valid local support signatures, all three pure amplitudes, and only
the same 160 rare mixed words; they use no lex leaders and no
majority-colour mixed support clauses.  Fresh Singular replay accepts all
41 charts, and both CaDiCaL and Glucose verify both support covers as
UNSAT.

Thus the rare mechanism excludes all 38 new finite closures.  The combined
72 zero-forest exclusions still leave both reconstructed branch solvers
SAT.  The frozen evidence is in
[`research_snapshots/2026-07-28-p5-q5-311-rare-zero-wave2/`](research_snapshots/2026-07-28-p5-q5-311-rare-zero-wave2/README.md).

The complete reduction, exact evidence boundary, and reproduction commands
are in
[`P5_Q5_311_RARE_SLICE_REDUCTION.md`](P5_Q5_311_RARE_SLICE_REDUCTION.md).

## Continuation checkpoint

The stopped 360-record `q5_311` continuation used:

```text
pre-orbit base representatives: 1,380
prior dynamic representatives: 560
new relaxed family representatives: 6
unique transported startup clauses: 510,198
dynamic transport: enabled
deterministic gauge alternatives: 16
short deadline per alternative: 6 seconds
host available-memory floor: 20%
```

The 560 dynamic representatives are the frozen 260-record and 300-record
ledgers from consecutive family-learning rounds.  The six relaxed
representatives are two from the first round and four from the second.

The checkpoint remains exploratory until the branch is UNSAT and the complete
representative ledger, symmetry reconstruction, two independent SAT
solvers, and fresh characteristic-zero algebra replay all pass.
