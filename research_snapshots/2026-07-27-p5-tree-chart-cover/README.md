# `P_5` exact-three-coordinate tree-chart package

This directory contains the hash-bound evidence for
[`P5_EXACT_THREE_COORDINATE_TREE_CHART_OBSTRUCTION.md`](../../claims/p5/coordinate-cegar/P5_EXACT_THREE_COORDINATE_TREE_CHART_OBSTRUCTION.md).

Status: exact finite branch theorem over `C`.  It excludes every
`P_5 -> Delta_3` restriction in which all five local maps have at most
three coordinate rows.  It does not exclude the four/five-coordinate
branch and does not solve the global Krenn--Gu conjecture.

Contents:

- `manifest.json`: scope, counts, raw hashes, and explicit unresolved
  boundaries;
- `c10_core_charts.json`, `c4c6_core_charts.json`: 812 retained
  deletion-stable gauge charts;
- `fresh_singular_replay.json`: fresh 812/812 exact unit-ideal replay;
- `*_cover.cnf.gz`: exact global support-cover CNFs;
- `*_cover.drat.gz`: Kissat binary DRAT traces; and
- `*_drat_trim.stdout`: independent backward replay logs containing
  `s VERIFIED`.

The authoritative verifier is:

```text
python claims/p5/coordinate-cegar/verify_p5_exact_three_coordinate_tree_chart_obstruction.py
```
