# `P_5` three-coordinate cycle dichotomy

## Status

This is an exact structural theorem over `C`.

Suppose a hypothetical restriction

```text
P_5 -> Delta_3
```

has at most three coordinate rows in each of its five local maps.  Then:

1. every local map has exactly three coordinate rows;
2. for every source row `p` and target colour `c`, exactly one local map
   has row `p` proportional to `e_c`;
3. every source row is non-coordinate in exactly two modes; and
4. the ten non-coordinate cells, viewed as edges of a bipartite graph
   between the five modes and five source rows, form either

   ```text
   C_10
   ```

   or

   ```text
   C_4 disjoint union C_6.
   ```

This reduces the exact-three-coordinate branch of the `P_5` problem to
two loop architectures.  It does not exclude those architectures by
itself and is not a proof of the Krenn--Gu conjecture.

## Proof

The source-row tricolour-cover theorem says that, for every one of the
`5 * 3 = 15` pairs

```text
(source row p, target colour c),
```

some local map has row `p` proportional to `e_c`.

A nonzero row cannot be proportional to two distinct coordinate
covectors.  Therefore the fifteen requirements need fifteen distinct
coordinate cells among the `5 * 5` local rows.

By hypothesis, each of the five modes has at most three coordinate rows,
so there are at most fifteen coordinate cells in total.  Equality is
forced.  Thus every mode has exactly three coordinate rows and every
source-colour requirement occurs exactly once.

For a fixed source row, its three colours occur in three distinct modes.
Consequently that source row is non-coordinate in its other two modes.
Every mode likewise has two non-coordinate rows.

Construct a simple bipartite graph `H` whose left vertices are the five
modes, whose right vertices are the five source rows, and whose edges are
the non-coordinate cells.  Every vertex of `H` has degree two.  Hence
`H` is a disjoint union of even cycles.  A simple bipartite cycle has at
least four vertices, and `H` has ten vertices total.  The only possible
partitions of ten into even integers at least four are

```text
10
```

and

```text
4 + 6.
```

This proves the dichotomy.

## Finite checks

`verify_p5_three_coordinate_cycle_dichotomy.py` chooses the two
non-coordinate sources independently in every mode, filters for source
degree two, and obtains exactly

```text
2,040 labelled graphs:
1,440 of type C_10,
  600 of type C_4 disjoint union C_6.
```

`audit_p5_three_coordinate_cycle_dichotomy.py` reconstructs the same
graphs independently as unions of two pointwise-disjoint perfect
matchings.  There are

```text
5! * !5 = 120 * 44 = 5,280
```

ordered decompositions.  A `C_10` has two ordered alternating
decompositions, while `C_4 disjoint union C_6` has four, giving

```text
1,440 * 2 + 600 * 4 = 5,280.
```

## Verification

Run:

```text
python claims/p5/coordinate-cegar/verify_p5_three_coordinate_cycle_dichotomy.py
python claims/p5/coordinate-cegar/audit_p5_three_coordinate_cycle_dichotomy.py
```

## Boundary

The remaining work is coefficient-level.  Two-term cancellation,
pair-incidence determinant relations, and exact polynomial elimination
must exclude both loop families, or produce a genuine `P_5 -> Delta_3`
restriction.
