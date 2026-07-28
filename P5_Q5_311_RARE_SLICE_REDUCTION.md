# The two rare `q5_311` deleted-`P_4` slices

## Status

This is an exact structural reduction and a finite chart experiment inside
the normalized `q5_311` branch of a possible restriction

```text
P_5 -> Delta_3.
```

It does not yet exclude the complete `q5_311` branch, the other two
high-coordinate branches, `P_5 -> Delta_3`, or the arbitrary-order
Krenn--Gu prize conjecture.

## Structural reduction

The normalized mode-zero support is

```text
(1,1,1,2,4),
```

so target colour zero occurs on three source rows while target colours one
and two occur on exactly one source row apiece.  Fix one of those two rare
target colours `c`.

In every permanent term with mode-zero colour `c`, mode zero must use its
unique source row `s_c`.  The other four modes must use the remaining four
source rows.  Consequently the complete coefficient tensor in those four
modes is, up to the nonzero singleton coefficient at mode zero, a
deleted-row restriction of the order-four permanent:

```text
(A_1 without row s_c) tensor ... tensor
(A_4 without row s_c) applied to P_4.
```

The diagonal target says that this tensor is exactly

```text
lambda_c e_c tensor e_c tensor e_c tensor e_c,
lambda_c != 0.
```

Thus `q5_311` forces the same four local maps to turn two different
deleted-row copies of `P_4` into nonzero decomposable tensors in two
independent target directions.

The mixed part uses only the coefficients whose mode-zero colour is one or
two:

```text
2 * (3^4 - 1) = 160
```

mixed target words.  The global target still requires all three pure
coefficients to be nonzero.  Thus the reduced system may saturate the
majority pure coefficient without using any of the 80 mixed words in the
majority-colour slice.

## Exact chart probe

`probe_p5_q5_311_rare_slice_core.py` regenerates this subsystem on any
exact gauge chart:

1. reconstruct the chart closure and retained gauge forest;
2. expand the two sets of deleted-`P_4` coefficients directly from all
   `5!` source permutations;
3. deduplicate the nonzero mixed polynomials;
4. saturate either the two rare pure coefficients or all three pure
   coefficients; and
5. run a global degree-compatible characteristic-zero Singular
   calculation.

If product saturation is inconclusive, the probe tries the equivalent
split saturation with one inverse per selected pure coefficient.  Only an
explicit `UNIT_IDEAL` is a chart exclusion.  A timeout or infrastructure
error is unknown.

With only the two rare pure coefficients saturated, the frozen 300-record
`q5_311` continuation ledger gives:

```text
rare-slice UNIT_IDEAL: 298 / 300
direct elapsed range:  0.078 to 0.188 seconds
direct elapsed mean:   0.0981 seconds
```

The two records not certified by this strict rare-only probe are exactly
the two records whose full 240-mixed-equation certificates use split
saturation.  For record 148, the rare split system returns a proper
positive-dimensional ideal:

```text
SURVIVOR
57 basis elements
vdim = -1
```

Therefore the rare-slice equations with only the two rare pure
nonvanishing conditions do not exclude that chart.  Record 149's analogous
strict rare-only computation remained inconclusive at the tested deadline.

Adding only nonvanishing of the majority pure coefficient closes both
records:

```text
rare mixed equations plus all three pure coefficients: 300 / 300
certificate methods:                                298 direct, 2 split
accepted elapsed range:                             0.079 to 0.406 seconds
accepted elapsed mean:                              0.1096 seconds
majority-colour mixed equations used:                0
```

For records 148 and 149, the split systems return the unit ideal in 0.391
and 0.406 seconds respectively.  Thus the exceptional behaviour is a pure
nonvanishing boundary, not a need for the omitted majority-colour mixed
slice.

The 25 representatives with highest retrospective symmetry-orbit
coverage are all rare-slice unit ideals.  Four full-system relaxations
of the leading distinct families also remain rare-slice unit ideals:

```text
source record   old clause   relaxed clause   freed cells
146                  26              20             5
140                  27              21             4
196                  18              16             4
276                  26              20             5
```

The four relaxed full systems were independently regenerated and freshly
replayed as characteristic-zero unit ideals.  Their representative clauses
were checked with both CaDiCaL and Glucose before reuse.

One unrelaxed leading chart exposes a hand-sized degree-one core.  Exact
identities using six and five Macaulay rows express the two rare pure
coefficients as polynomial combinations of only nine distinct mixed
coefficients.  See
[`P5_Q5_311_RARE_AFFINE_CORE.md`](P5_Q5_311_RARE_AFFINE_CORE.md).

## Zero-forest wave 2

A later 360-record continuation produced 38 exact closures whose
certificates need no gauge-pivot assumptions.  They are all distinct from
the earlier 34 zero-forest closures.  Fresh split-Singular replay verifies
the combined 72-record package, while both reconstructed residual branch
CNFs remain SAT.

The 38 new closures test the rare reduction without retaining a convenient
normalization tree:

```text
direct zero-forest rare UNIT_IDEAL: 36 / 38
inconclusive zero-forest probes:      2 / 38
```

The two inconclusive calculations are records 12 and 13.  They time out;
neither returns a survivor.  Exact support stratification resolves them.
For each closure, the support CNF uses the complex-valid 6,495 local
support/pair-incidence signatures, the `q5_311` branch conditions, supported
pure monomials, and one-term impossibility for only the same 160 rare mixed
words.  It deliberately uses neither lex leaders nor any majority-colour
mixed support condition.

```text
record 12: 16 exact support charts, CaDiCaL and Glucose UNSAT
record 13: 25 exact support charts, CaDiCaL and Glucose UNSAT
fresh characteristic-zero Singular replays: 41 / 41
```

Each learned chart permits all coefficients inside its closure to vanish
except the stored gauge pivots and the three pure amplitudes.  The
support-CNF UNSAT result therefore covers every complex-valid support
stratum inside the two target closures, not just the first SAT models.

Consequently the rare mixed equations plus nonvanishing of all three pure
coefficients exclude all 38 new zero-forest closures.  This is a stronger
finite closure result, not a proof that every possible `q5_311` chart has
one of these 38 closures.

## Why the reduction is useful

The finite evidence is not 300 unrelated algebraic accidents: all 300
representatives are excluded by the same pair of simultaneous deleted-`P_4`
rank-one requirements together with the three target amplitudes being
nonzero.  This identifies a smaller analytic classification problem:

> Classify four rank-three five-row maps for which two different row
> deletions restrict `P_4` to nonzero decomposable tensors in independent
> local directions while all three inherited pure amplitudes are nonzero.

The two split records identify a boundary stratum on which the majority
pure nonvanishing condition cannot be omitted.

A still coarser proposed lemma is false in finite characteristic:
two-dimensional local subspaces can compress `P_4` to a nonzero
decomposable tensor over both `F_3` and `F_5`.  Hence a proof must use the
simultaneous two-deletion compatibility, characteristic-zero structure, or
the extra `q5_311` incidence conditions rather than asserting that one
rank-one `P_4` compression is impossible by itself.

## Reproduction

Rank a frozen ledger by exact branch-symmetry coverage:

```text
python rank_p5_high_coordinate_chart_orbits.py \
  --state tmp/p5_high_tree_q5_311_v16_family_relaxed_orbits.json \
  --top 25 \
  --output tmp/p5_high_tree_q5_311_v16_orbit_ranking_300.json
```

Probe selected records:

```text
python probe_p5_q5_311_rare_slice_core.py \
  --state tmp/p5_high_tree_q5_311_v16_family_relaxed_orbits.json \
  --record-index 146 \
  --record-index 140 \
  --include-majority-pure \
  --timeout 10 \
  --output tmp/p5_q5_311_rare_slice_probe.json
```

Greedily enlarge one full-system exact chart while retaining its gauge
forest:

```text
python maximize_p5_high_coordinate_chart_closure.py \
  --branch q5_311 \
  --state tmp/p5_high_tree_q5_311_v16_family_relaxed_orbits.json \
  --record-index 146 \
  --timeout 2 \
  --min-available-percent 20 \
  --output tmp/p5_q5_311_relaxed_seed.json
```

All figures above are finite ledger statements.  A complete branch theorem
still requires an independently UNSAT reconstructed branch CNF and fresh
algebra replay for every representative used in that cover.

The frozen zero-forest wave and its independent verifier are:

```text
research_snapshots/2026-07-28-p5-q5-311-rare-zero-wave2/

python verify_p5_q5_311_rare_slice_support_cover.py \
  --state research_snapshots/2026-07-28-p5-q5-311-rare-zero-wave2/zero_forest_records.json \
  --probe research_snapshots/2026-07-28-p5-q5-311-rare-zero-wave2/rare_zero_probe.json \
  --cover research_snapshots/2026-07-28-p5-q5-311-rare-zero-wave2/rare_support_cover.json \
  --rerun-singular \
  --singular-timeout 30
```
