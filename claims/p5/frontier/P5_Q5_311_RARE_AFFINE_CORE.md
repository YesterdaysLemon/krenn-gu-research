# A short rare-slice affine core in `q5_311`

## Status

This is a hand-sized exact identity excluding one gauge chart in the
normalized `q5_311` branch of a possible restriction

```text
P_5 -> Delta_3.
```

Branch symmetries transport the identity to the complete orbit of that
chart.  It does not exclude every `q5_311` chart, either other
high-coordinate branch, `P_5 -> Delta_3`, or the arbitrary-order
Krenn--Gu conjecture.

## The chart

Write a three-bit mask for the target-coordinate support of each local
source row.  The chart closure is

```text
1 1 1 2 4
7 7 7 1 2
7 7 4 7 1
2 2 7 7 7
4 4 2 4 7.
```

Its 45 supported entries form a connected bipartite coefficient graph.
Normalize a 19-edge spanning tree to one, leaving variables

```text
u0,...,u25.
```

Only six variable names enter the final identities:

```text
u16 = entry(mode 3, source 1, colour 1)
u17 = entry(mode 3, source 2, colour 1)
u18 = entry(mode 3, source 2, colour 2)
u20 = entry(mode 3, source 4, colour 1)
u24 = entry(mode 4, source 4, colour 1)
u25 = entry(mode 4, source 4, colour 2).
```

The verifier pins the complete closure, source support, gauge tree, and
free-variable order.  The normalization is the deletion-stable gauge
normalization used by the high-coordinate chart cover.

## Coefficients

For a target word `abcde`, let

```text
F_abcde
```

be the corresponding coefficient of the restricted permanent tensor.
Every coefficient below whose word is not constant must vanish in a
restriction to `Delta_3`.  Put

```text
P_1 = F_11111,
P_2 = F_22222.
```

The two rare mode-zero slices obey the exact polynomial identities

```text
P_1
 = (1+u17) F_10000
   - F_10010
   + u16 F_10100
   + u20 F_11100
   + u24 F_11110,                                    (1)
```

and

```text
P_2
 = -u25 F_12200
   + (1-u18) F_12202
   + u25 F_12220
   + u18 F_22202.                                    (2)
```

Identity (1) uses five distinct mixed coefficients and six degree-at-most-one
Macaulay rows.  Identity (2) uses four distinct mixed coefficients and five
Macaulay rows.  Every scalar coefficient is `+1` or `-1`.

## Contradiction

All nine `F` terms on the right sides of (1) and (2) are mixed target
coefficients, so a diagonal target makes them zero.  The identities then
give

```text
P_1 = P_2 = 0.
```

Both coefficients must instead be nonzero in `Delta_3`.  This excludes the
entire gauge chart without a Gröbner-basis or saturation calculation.

The identities were discovered by an exact degree-one Macaulay span search
and are verified directly by expanding all `5!` permanent terms for every
coefficient.  Discovery does not certify itself: the verifier independently
reconstructs the chart and checks both symbolic residuals are identically
zero.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q5_311_rare_affine_core.py
```

The verifier checks:

1. the source support lies inside the closure;
2. the pinned 19 edges are an actual spanning tree on the 20 gauge nodes;
3. the closure has 45 entries and exactly 26 free variables;
4. the six named variables retain their intended matrix entries;
5. every displayed `F` is a mixed coefficient;
6. both identities expand to zero over the integers.

## Boundary

This core explains one high-coverage chart motif and all its branch
symmetries.  It does not persist unchanged after the currently known
five-cell enlargement of that chart; the larger closure still has an exact
unit-ideal certificate, but its contradiction needs higher-degree
polynomial multipliers.

The uniform finite observation in
[`P5_Q5_311_RARE_SLICE_REDUCTION.md`](P5_Q5_311_RARE_SLICE_REDUCTION.md)
is broader: rare-colour mixed equations plus all three pure nonvanishing
conditions exclude all 300 charts in one frozen continuation ledger.  A
human proof still needs to transport identities such as (1)--(2) across
all possible support/incidence strata, not merely the currently recorded
charts.
