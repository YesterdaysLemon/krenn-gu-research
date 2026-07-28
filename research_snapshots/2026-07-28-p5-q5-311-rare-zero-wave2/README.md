# `q5_311` rare-slice zero-forest wave 2

## Status

This is a self-contained exact finite package inside the normalized
`q5_311` high-coordinate branch of a hypothetical restriction

```text
P_5 -> Delta_3.
```

It does not cover the complete branch, the other high-coordinate branches,
`P_5 -> Delta_3`, or the arbitrary-order Krenn--Gu prize conjecture.

## What is frozen

The stopped 360-record continuation contained 38 exact zero-gauge-forest
closures.  They are pairwise distinct and have zero closure overlap with
the earlier 34-record package.  The combined package therefore contains 72
distinct zero-forest closures.

Fresh independent replay of the combined package gives:

```text
records checked:          72
fresh Singular replays:   72
certificate methods:      72 split
gauge-forest edges:       0 on every record
CaDiCaL residual CNF:     SAT
Glucose residual CNF:     SAT
```

Thus every stored exclusion is exact, but the 72 exclusions still do not
form a complete `q5_311` cover.

## Rare-slice mechanism on the 38 new closures

The rare-slice probe keeps only the 160 mixed target words whose mode-zero
colour is one or two and requires all three pure coefficients to be
nonzero.  It uses no majority-colour mixed equation.

Direct zero-forest split saturation gives:

```text
UNIT_IDEAL:    36 / 38
inconclusive:   2 / 38
hard indices:  12, 13
```

The two inconclusive calculations are timeouts, not survivor models.  They
are resolved by an exact support-stratified cover.  The cover uses the
complex-valid 6,495 local support/pair-incidence patterns, the branch
restriction, pure-monomial support, and one-term impossibility for only
the same 160 rare mixed words.  It uses no lex leaders and no
majority-colour mixed support clauses.

```text
target record 12:  16 exact charts, CaDiCaL/Glucose UNSAT
target record 13:  25 exact charts, CaDiCaL/Glucose UNSAT
fresh Singular replays: 41 / 41
```

Consequently the rare mixed slices plus nonvanishing of all three pure
amplitudes exclude all 38 new zero-forest closures.  This is a finite
closure result, not a classification of every possible `q5_311` chart.

## Files and hashes

```text
zero_forest_records.json
9d695a6c997cd8e0cd28a8edb5a895784716accc8ad86aa14fa5591b21abad1d

q5_311_zero_forest_seeds_combined72.json
68513d26a8f942b3422a85f5fe60444d2192d1d5cddec5548a8311f69d6d5f3e

rare_zero_probe.json
69190e7b18fa7bf1c7efdb0909d7dc99e10b8163827a218a4cf6c576c74fc892

rare_support_cover.json
be8c0ba8556bc0799db79560fa3a40c9e73bdb3ddd80b29f67dcd33b8deab140
```

## Verification

With the repository Python dependencies and Singular available, run:

```text
python verify_p5_high_coordinate_chart_ledgers.py \
  --branch q5_311 \
  --state research_snapshots/2026-07-28-p5-q5-311-rare-zero-wave2/q5_311_zero_forest_seeds_combined72.json \
  --rerun-singular \
  --jobs 4 \
  --singular-timeout 60

python verify_p5_q5_311_rare_slice_support_cover.py \
  --state research_snapshots/2026-07-28-p5-q5-311-rare-zero-wave2/zero_forest_records.json \
  --probe research_snapshots/2026-07-28-p5-q5-311-rare-zero-wave2/rare_zero_probe.json \
  --cover research_snapshots/2026-07-28-p5-q5-311-rare-zero-wave2/rare_support_cover.json \
  --rerun-singular \
  --singular-timeout 30
```

Regenerate the two hard support covers:

```text
python cover_p5_q5_311_rare_slice_supports.py \
  --state research_snapshots/2026-07-28-p5-q5-311-rare-zero-wave2/zero_forest_records.json \
  --record-index 12 \
  --record-index 13 \
  --timeout 10 \
  --output tmp/rare_support_cover_rebuilt.json
```
