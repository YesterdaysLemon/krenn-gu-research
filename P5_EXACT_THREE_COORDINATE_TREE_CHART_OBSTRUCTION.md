# Exact-three-coordinate `P_5 -> Delta_3` obstruction

## Status

This is an exact finite-assisted theorem over `C`.

There is no restriction

```text
P_5 -> Delta_3
```

in which every one of the five local maps has at most three coordinate
rows.  Equivalently, every hypothetical restriction has a local map with
at least four coordinate rows.

This closes the complete exact-three-coordinate branch, including every
combination of full and two-colour non-coordinate rows.  It strictly
subsumes the earlier all-full and exact-one-, exact-two-, and
exact-three-partial layer theorems.

It does **not** close the branch with four or five coordinate rows in
some local map, prove that `P_5` does not restrict to `Delta_3`, or solve
the arbitrary-order Krenn--Gu prize conjecture.

## Structural reduction

The source-row tricolour-cover theorem forces at least 15 coordinate
cells among the 25 local rows.  Under the hypothesis that each local map
has at most three, equality holds: every map has exactly three
coordinate rows, and every source row occurs once in each target colour.

The ten non-coordinate cells form a two-regular bipartite graph on five
mode and five source vertices.  The cycle dichotomy leaves exactly:

```text
C10
C4 disjoint union C6.
```

For each fixed shape, the 15 coordinate colours have `6^5 = 7,776`
labelled assignments.  Quotienting by shape automorphisms and global
colour permutation gives:

```text
shape   coordinate-backbone orbits   support-semantic viable
C10                              148                       127
C4+C6                             78                        73
total                            226                       200.
```

The support semantics use only necessary consequences already covered
over `C`:

1. one of the 6,495 exact local support/pair-incidence signatures in
   `P5_PAIR_SIGNATURE_CATALOGUE_COVERAGE.md` is selected in each mode;
2. every source pair and target colour meets the pair level of the
   kernel-Hall hierarchy;
3. each pure target coefficient has a supported perfect matching; and
4. no zero mixed coefficient has exactly one supported perfect-matching
   monomial.

These conditions over-approximate complex realizability, so excluding
them is safe.

## Deletion-stable spanning-tree charts

For one coordinate backbone, start with the support closure in which all
ten non-coordinate cells have full three-colour support.  Its coefficient
support graph has:

```text
5 source nodes
15 (mode, target-colour) nodes
```

and one edge for each matrix entry.

Every semantic support in the branch is connected.  Choose a spanning
tree contained in it.  The torus action that rescales the 20 graph nodes
has a one-dimensional kernel, so its 19 effective parameters normalize
the 19 nonzero tree entries to one.

The chart ideal contains:

```text
all 240 mixed permanent coefficients
one Rabinowitsch equation making the three pure coefficients nonzero.
```

Crucially, no non-tree coefficient is saturated.  Such a coefficient may
vanish.  Therefore a unit-ideal certificate for this full-closure chart
excludes every lower support that contains its gauge tree.  If the
optional connector edges are `e_1,...,e_r`, the certified Boolean clause
is simply:

```text
not e_1 or ... or not e_r.
```

This is why the calculation does not enumerate all `3^10` partial/full
patterns.  SAT asks for one support not yet covered, exact algebra
certifies a tree chart in that support, and the learned clause removes a
whole downward-closed support family.

## Why gauge fixing is sound

Let the support graph be bipartite with source-node scalars `a_p` and
mode-colour-node scalars `b_(i,c)`.  An entry transforms by

```text
x_(i,p,c) -> a_p b_(i,c) x_(i,p,c).
```

On a spanning tree, choose a root scalar and solve outward uniquely to
make every tree entry one.  Changing the root lies in the one-dimensional
kernel and has no effect.

Every perfect-matching monomial uses each source node once.  For a fixed
inherited colour word it also uses one `(mode,colour)` node per mode.
Thus all monomials in one coefficient acquire the same nonzero factor.
The properties “mixed coefficient is zero” and “pure coefficient is
nonzero” are invariant.

## Why deletion stability is sound

Suppose an actual solution has a lower support containing the chosen
tree.  Set every closure coefficient outside that lower support to zero.
The closure mixed polynomials then specialize exactly to the actual
mixed coefficients.  The three pure coefficients remain nonzero, and
the tree normalization remains valid.  Hence the actual solution would
give a point of the closure chart.

If the saturated closure ideal is the unit ideal over `Q`, it has no
point over `C`, so no such lower-support solution exists.

## Exact algebraic cover

Adaptive chart CEGAR and deletion minimization retain:

```text
shape   viable backbones   core charts   direct   split saturation
C10                  127           401      399                  2
C4+C6                 73           411      399                 12
total                 200           812      798                 14.
```

Every chart has 45 closure entries, 19 gauge-fixed entries, 26 free
coefficient variables, 240 mixed equations, and saturation by only the
three pure coefficients.

All 812 retained sources were regenerated and freshly replayed with
characteristic-zero Singular:

```text
812 / 812 UNIT_IDEAL
```

The 14 split cases replace one inverse of a three-factor product by
three separate inverse variables.  This is the same localization, not a
weaker system.

## Global SAT certificate

The final replay does not trust the discovery loop or the claimed
backbone list.  It rebuilds the full necessary-condition CNF from the
6,495-signature catalogue, fixes the cycle shape, adds exact
coordinate-backbone lex leaders, and inserts the retained chart clauses.

```text
shape   variables   clauses     chart clauses   result
C10       100,254   1,293,318             401   UNSAT
C4+C6     107,898   1,323,652             411   UNSAT.
```

Both CaDiCaL and Glucose independently return UNSAT.  Kissat additionally
emits binary DRAT traces:

```text
C10    45,389,314 bytes
C4+C6  48,012,550 bytes.
```

Backward `drat-trim` replay accepts both exact CNF/proof pairs with
`s VERIFIED`.  Because a disconnected semantic support contains no
spanning tree, it would satisfy every learned tree clause and survive as
a SAT model.  Global UNSAT therefore also certifies the connectivity
claim needed by the chart argument.

## Packaged evidence

The deterministic package is:

```text
research_snapshots/2026-07-27-p5-tree-chart-cover/
```

It contains:

- all 812 core chart descriptors and exact source hashes;
- the complete fresh Singular replay ledger;
- gzip-compressed exact DIMACS inputs and binary DRAT traces;
- independent `drat-trim` logs; and
- a hash-bound manifest that keeps the global conjecture and
  high-coordinate branch explicitly unresolved.

The compressed package is about 34 MB.  Decompression is checked against
the raw CNF and proof byte counts and SHA-256 hashes.

## Verification

Install `python-sat`, make Singular available through WSL or the native
path used by the verifier, then run:

```text
python verify_p5_exact_three_coordinate_tree_chart_obstruction.py
```

The default audit:

1. checks every packaged hash;
2. reconstructs all 812 algebra sources;
3. reconstructs both exact DIMACS files byte for byte;
4. checks canonical backbone and signature witnesses; and
5. reruns both CNFs with CaDiCaL and Glucose.

Freshly rerun all 812 Singular calculations with:

```text
python verify_p5_exact_three_coordinate_tree_chart_obstruction.py \
  --rerun-singular --jobs 4
```

Fresh DRAT replay is deliberately optional because it takes about 20
minutes per shape on the reference host:

```text
python verify_p5_exact_three_coordinate_tree_chart_obstruction.py \
  --rerun-drat --drat-trim tmp/drat-trim/drat-trim \
  --drat-timeout 1800
```

## Remaining boundary

The `P_5` problem is now concentrated on local maps with four or five
coordinate rows.  This is a qualitatively smaller structural branch:
the 15-coordinate pigeonhole equality is broken, so its non-coordinate
cell graph is no longer the `C10`/`C4+C6` two-factor.

After that finite branch, a proof of the prize conjecture still requires
an arbitrary-order lift, or a genuine counterexample.  Finite `P_5`
certificates alone do not provide either.
