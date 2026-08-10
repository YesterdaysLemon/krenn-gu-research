# Exact-three-partial `C4+C6` boundary obstruction for `P_5`

## Status

This is an exact finite computer-assisted theorem about one half of the
exact-three-partial layer in the local restriction problem

```text
P_5 -> Delta_3.
```

It excludes every support in the `C4+C6` shape with exactly three
partial noncoordinate cells.  It does **not** yet exclude the companion
`C10` shape, the branches with four or five coordinate rows in a local
map, or the global Krenn--Gu conjecture.

## Independent support census

The packed-array audit independently generated all

```text
25,194,240
```

labelled exact-three supports for the fixed `C4+C6` shape.  Quotienting
by the 144 fixed-shape and global-colour actions gave 119,966 locally
valid support orbits.  Exact pair-incidence quotas reduced them to
10,216 support orbits and 58,664 viable signature tuples.  Direct
necessary permanent semantics then left exactly 5,993 support orbits.

The independently reconstructed canonical set agrees exactly with the
separately generated SAT catalogue: no missing or extra orbit.

## Exact algebra

For each of the 5,993 survivors, the generator:

1. chooses a complex-valid local signature witness;
2. fixes the exact nonzero support stratum;
3. gauges the 42 nonzero entries to 23 Laurent parameters;
4. generates every distinct forbidden mixed permanent coefficient;
5. requires the three pure coefficients to be nonzero; and
6. saturates every nonzero parameter and pure coefficient.

Singular 4.3.2, in characteristic zero with global `dp` order and
`slimgb`, returned the unit ideal directly for all 5,993 systems.  The
recorded solver time was about 8,009 seconds.  Thus none of these
supports can realize `Delta_3` over `C`.

## Replay package

The evidence map is in
[`three_partial_c4c6_boundary/`](../../../research_snapshots/2026-07-27-p5-coordinate-cegar/three_partial_c4c6_boundary/README.md).
The normal verifier independently reconstructs every support-orbit
mapping, signature witness, pair quota, and exact Singular source, then
checks its committed hash and recorded unit-ideal result:

```text
python \
  claims/p5/boundaries/verify_p5_exact_three_c4c6_boundary_obstruction.py
```

The package intentionally stores source hashes rather than another
roughly 110 MB of mechanically regenerated text.  A fresh exact-CAS
replay can be sharded.  For example, this reruns ten cases locally:

```text
python \
  claims/p5/boundaries/verify_p5_exact_three_c4c6_boundary_obstruction.py \
  --rerun-singular --limit 10
```

Use `--start 0 --step 2` and `--start 1 --step 2` for two complete
shards.  On a system where `Singular` is not on `PATH`, pass an explicit
command such as:

```text
--singular-command "wsl.exe --exec Singular -q"
```

## Consequence and remaining boundary

Together with the already packaged zero-, one-, and two-partial
theorems, this proves that no remaining exact-three-coordinate
restriction of `C4+C6` shape has only three partial cells.  The
remaining finite exact-three work is:

1. the 11,751 `C10` exact-three survivors;
2. four through ten partial cells in both cycle shapes; and
3. the separate four/five-coordinate-row branch.

Even closing all finite `P_5` branches would not by itself prove the
arbitrary-order graph conjecture.
