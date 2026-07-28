# Structural quotient of the exact-three-partial `P_5` survivors

## Status

This is an exploratory coarsening of the two exact-three-partial SAT
catalogues.  The motif calculation is not itself an independent
regeneration or an algebraic exclusion.  Separately, both catalogues
have now been independently regenerated from all 25,194,240 labelled
supports of their respective shapes.  All 5,993 `C4+C6` cases are
excluded by exact unit-ideal calculations; see
`P5_EXACT_THREE_C4C6_BOUNDARY_OBSTRUCTION.md`.  The independent `C10`
census agrees on 11,751 cases, but their algebraic exclusion remains in
progress; see `P5_EXACT_THREE_C10_CENSUS.md`.  None of these finite
results proves the global Krenn--Gu conjecture.

The purpose is to replace thousands of raw support patterns by a small
set of candidate structural motifs from which a human-scale obstruction
lemma might be learned.

## Input boundary

In the exact-three-coordinate branch, the ten noncoordinate
mode--source cells form either:

```text
C4 + C6
```

or

```text
C10.
```

The symmetry-broken SAT catalogues contain:

```text
C4+C6:  5,993 support-semantic survivor orbits
C10:   11,751 support-semantic survivor orbits
total: 17,744.
```

Exactly three of the ten noncoordinate cells have two target colours;
the other seven have all three.  For every source column, the remaining
three coordinate cells use singleton colours `1`, `2`, and `4` exactly
once.

## Three quotient levels

`analyze_p5_exact_three_motifs.py` validates those structural facts and
computes three increasingly detailed invariants.

### Partial-cell geometry

First retain only the positions of the three two-colour cells on the
cycle components, modulo dihedral symmetry.  This gives:

```text
C4+C6: 9 classes
C10:   8 classes
total: 17 classes.
```

This is the smallest plausible target for a support-independent lemma.

### Missing-colour geometry

Next label each partial cell by its missing target colour and quotient
by cycle symmetry and global colour permutation.  This gives:

```text
C4+C6: 32 classes
C10:   34 classes
total: 66 classes.
```

If the sparse Laurent contradictions depend only on the partial cells
and their missing colours, at most 66 symbolic templates are needed.

### Coordinate backbone

Finally retain the fifteen forced singleton rows, quotienting by the
fixed-shape automorphism group and global colour permutation.  There
are 61 backbone classes for `C4+C6` and 111 for `C10`.

Pairing the independently canonicalized backbone and missing-colour
geometry gives:

```text
C4+C6:   756 observed pairs
C10:   1,919 observed pairs
total: 2,675.
```

This last count is a coarsening invariant, not a claim that two supports
with the same pair are related by one simultaneous automorphism.  It
still compresses 17,744 raw survivors by a factor of about 6.6 and is a
reasonable fallback classification if the 17- or 66-motif lemmas are
too coarse.

## Replay

Given the two generated SAT catalogues:

```text
python analyze_p5_exact_three_motifs.py \
  tmp/p5_c4c6_exact_three_partial_supports.json \
  tmp/p5_c10_exact_three_partial_supports.json \
  --output tmp/p5_exact_three_motif_analysis.json
```

The analyzer checks the cycle shapes, exact number of partial cells,
and the forced singleton-colour condition before counting any class.

## Next test

For one `C10` representative of each missing-colour geometry:

1. deletion-minimize the exact unit ideal to a small set of mixed
   coefficient equations;
2. canonically encode the resulting monomial-incidence hypergraph;
3. test whether the identity transports to every support with the same
   geometry; and
4. only introduce the coordinate-backbone split when transport fails.

Success at the 17- or 66-class level would replace most of the
support-by-support computer algebra with a finite family of explicit
Laurent identities.  Failure is also informative: it would show that
the coordinate backbone, not merely the three partial cells, controls
the obstruction.
