# Exact-three-partial `C10` boundary obstruction for `P_5`

## Status

This is an exact finite computer-assisted theorem about the second half
of the exact-three-partial layer in the local restriction problem

```text
P_5 -> Delta_3.
```

It excludes every support in the `C10` shape with exactly three partial
noncoordinate cells.  Together with the previously closed `C4+C6`
shape, it closes the complete exact-three-partial layer.

It does **not** exclude the layers with four through ten partial cells,
the branches with four or five coordinate rows in a local map, an
arbitrary-order lift, or the global Krenn--Gu conjecture.

## Independent support census

The packed-array audit independently generated all

```text
25,194,240
```

labelled exact-three supports for the fixed `C10` shape.  Quotienting by
the 60 fixed-shape and global-colour actions gave 281,896 locally valid
support orbits.  Exact pair-incidence quotas reduced them to 23,112
support orbits and 137,405 viable signature tuples.  Direct necessary
permanent semantics then left exactly 11,751 support orbits.

The independently reconstructed canonical set agrees exactly with the
separately generated symmetry-broken SAT catalogue.

## Exact algebra

For each of the 11,751 survivors, the generator:

1. chooses a complex-valid local signature witness;
2. fixes the exact 42-entry nonzero support stratum;
3. gauges the connected support graph to 23 Laurent parameters;
4. generates every distinct forbidden mixed permanent coefficient;
5. requires the three pure coefficients to be nonzero; and
6. saturates every nonzero parameter and pure coefficient.

Singular 4.3.2, in characteristic zero with global `dp` order and
`slimgb`, returned the unit ideal directly for all 11,751 systems.  No
split-saturation fallback was needed.  Thus none of these supports can
realize `Delta_3` over `C`.

The smaller public affine certificates explain 3,650 of these systems
without the saturation equation.  The full Singular theorem is
strictly stronger and supplies the remaining 8,101 exclusions.

## Replay package

The compact evidence map is in
[`three_partial_c10_boundary/`](research_snapshots/2026-07-27-p5-coordinate-cegar/three_partial_c10_boundary/README.md).
It stores source hashes rather than duplicating roughly 200 MB of
deterministically regenerated Singular input.

The normal verifier reconstructs every support-orbit mapping, signature
witness, pair quota, and exact Singular source, then checks its committed
hash and recorded unit-ideal result:

```text
PYTHONPATH=tmp/python_deps python \
  verify_p5_exact_three_c10_boundary_obstruction.py
```

A fresh exact-CAS replay can be sharded.  For example, this reruns ten
cases:

```text
PYTHONPATH=tmp/python_deps python \
  verify_p5_exact_three_c10_boundary_obstruction.py \
  --rerun-singular --limit 10
```

Use `--start 0 --step 2` and `--start 1 --step 2` for two complete
shards.  On a system where `Singular` is not on `PATH`, pass an explicit
command such as:

```text
--singular-command "wsl.exe --exec /usr/bin/Singular -q"
```

## Consequence and remaining boundary

Together with the zero-, one-, and two-partial theorems and the
companion exact-three `C4+C6` theorem, this proves:

> In the exact-three-coordinate `P_5 -> Delta_3` branch, every remaining
> local-map support has at least four partial noncoordinate cells.

The remaining finite `P_5` work is:

1. four through ten partial cells in both cycle shapes; and
2. the separate four/five-coordinate-row branch.

Even closing every finite `P_5` branch would not by itself prove the
arbitrary-order graph conjecture.
