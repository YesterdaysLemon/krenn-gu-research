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

This uses only the coefficients whose mode-zero colour is one or two:

```text
2 * (3^4 - 1) = 160
```

mixed target words, together with nonvanishing of the two rare pure
coefficients.  It does not use the 80 mixed words in the majority-colour
slice or the majority pure coefficient.

## Exact chart probe

`probe_p5_q5_311_rare_slice_core.py` regenerates this subsystem on any
exact gauge chart:

1. reconstruct the chart closure and retained gauge forest;
2. expand the two sets of deleted-`P_4` coefficients directly from all
   `5!` source permutations;
3. deduplicate the nonzero mixed polynomials;
4. saturate only the two rare pure coefficients; and
5. run a global degree-compatible characteristic-zero Singular
   calculation.

If product saturation is inconclusive, the probe tries the equivalent
two-inverse split saturation.  Only an explicit `UNIT_IDEAL` is a chart
exclusion.  A timeout or infrastructure error is unknown.

On the frozen 300-record `q5_311` continuation ledger:

```text
rare-slice UNIT_IDEAL: 298 / 300
direct elapsed range:  0.078 to 0.188 seconds
direct elapsed mean:   0.0981 seconds
```

The two records not certified by the direct rare-slice probe are exactly
the two records whose full 240-mixed-equation certificates use split
saturation.  For record 148, the rare split system returns a proper
positive-dimensional ideal:

```text
SURVIVOR
57 basis elements
vdim = -1
```

Therefore the rare-slice equations genuinely do not exclude that chart;
the omitted majority-colour equations are essential there.  Record 149's
rare subsystem remained computationally inconclusive at the tested
deadline.

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

## Why the reduction is useful

The finite evidence is not 300 unrelated algebraic accidents:
`298/300` representatives are explained by the same pair of simultaneous
deleted-`P_4` rank-one requirements.  This identifies a smaller analytic
classification problem:

> Classify four rank-three five-row maps for which two different row
> deletions restrict `P_4` to nonzero decomposable tensors in independent
> local directions.

The two full-system split records identify the exceptional stratum that a
correct theorem must retain.

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
