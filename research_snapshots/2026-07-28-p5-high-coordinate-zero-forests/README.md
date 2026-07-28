# High-coordinate P5 zero-pivot seed set

## Status

This is an exact finite certificate set inside the normalized `q5_311`
high-coordinate branch.  It is not a complete branch cover and does not
prove `P_5` has subrank at most two.  The Krenn--Gu prize conjecture
remains unresolved.

The package contains 34 distinct support closures.  For each closure,
all mixed coefficients of a putative local restriction are set to zero
and the product of the three required pure coefficients is saturated.
The resulting characteristic-zero ideal is the unit ideal even when
the gauge forest is empty.

Thus these are stronger than ordinary gauge-chart certificates:

```text
ordinary chart:
  entries outside the closure vanish
  and selected gauge pivots are present

zero-pivot closure:
  entries outside the closure vanish
  with no coefficient-presence assumptions
```

Each record therefore excludes every coefficient support contained in
its closure, provided the three required pure amplitudes remain nonzero.

## Frozen artifact

```text
q5_311_zero_forest_seeds.json
records                 34
unique clauses          34
unique closures         34
unique source hashes    34
gauge-forest edges       0 in every record
SHA-256
  952fc788b171174020917f0c2287c172a8e4dd88b89f80ecb35c1f4ed6216bce
```

Every record is self-contained: it includes the closure, source support,
five local-signature witnesses, exact generated-source hash, split-source
hash, and the recorded Singular result.

## Replay

With `python-sat` available, run:

```text
python verify_p5_high_coordinate_chart_ledgers.py \
  --branch q5_311 \
  --state research_snapshots/2026-07-28-p5-high-coordinate-zero-forests/q5_311_zero_forest_seeds.json \
  --rerun-singular \
  --jobs 1 \
  --singular-timeout 60
```

The fresh replay regenerates all 34 rational systems and their exactly
equivalent split saturations.  It reports:

```text
verified                    true
records checked                34
certificate method          split: 34
gauge-forest edges              0: 34
fresh Singular replays            34
CaDiCaL branch result             SAT
Glucose branch result             SAT
```

The two SAT results are expected and important: this package certifies
the 34 closures, not the full `q5_311` branch.

## Discovery and continuation

`minimize_p5_high_coordinate_gauge_forest.py` greedily deletes pivots
from one exact chart.  The direct mode tests the empty forest in one
step.  `certify_p5_high_coordinate_zero_forest_batch.py` applies that
test to selected records in one process, and
`package_p5_high_coordinate_zero_forest_seeds.py` builds this frozen
package.

The live driver now has `--try-empty-forest-first`.  It gives every new
SAT model a bounded split-only zero-pivot probe and falls back to the
maximal gauge forest after an inconclusive probe.  Both outcomes remain
exact; a timeout is never treated as a survivor or a proof.
