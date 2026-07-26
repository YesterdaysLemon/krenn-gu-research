# Order-ten balanced all-bridge set-tree obstruction

## Status

This is a complete finite exclusion of the simultaneous three-colour
balanced all-bridge branch on ten vertices.  It has no support-degree
bound and allows arbitrary overlap among the selected monochromatic
matchings.

It does not cover the separate deeper-blocker branch, so it is not a
complete order-ten theorem or a proof of the global Krenn--Gu
conjecture.

## Reduction to constrained set trees

The universal `0/10/20` potential restricts a forbidden
nonmonochromatic minimum coefficient to saturated monochromatic
diagonal units.  For each colour `c`, define

```text
T_c = {nonempty even U subset V : haf(Z^c[U]) != 0}.
```

As proved in the order-eight theorem, hafnian expansion makes `T_c` a
set tree.  If `bj,bk` are the two normal bits other than `bc`, every
member satisfies

```text
count_U(00) = count_U(11),
count_U(01) = count_U(10)                              (1)
```

on the bit pair `(bj,bk)`.  A witness would require the three trees to be
incompatible: no partition of `V` into two or three true blocks may
assign those blocks to pairwise distinct tree colours.

## Complete order-ten SAT theorem

There are 104 balanced multiplicity profiles of the eight normal types
on ten vertices.  Independent flips of the three bit coordinates and
permutations of the coordinates preserve (1), the set-tree axioms, and
incompatibility.  The resulting 48-element cube-symmetry group has
exactly 10 profile orbits.

For one representative of each orbit, the certificate creates variables
`X(c,U)` only for subsets satisfying (1), asserts all three full sets,
encodes every vertex-wise set-tree expansion, and forbids every two- or
three-block even set partition assigned injectively to the tree colours.
All 10 representative formulas are UNSAT in the corrected enumeration.

A combined selector CNF conditionally contains the 10 formulas and
requires at least one selector.  Kissat proves this combined CNF UNSAT.
The raw DRAT proof is independently replayed by `drat-trim`.

The corrected CNF has 49,216 variables and 122,539 clauses.  Kissat's
39,164,774-byte DRAT proof is accepted by an independent forward
`drat-trim` replay.

## Verification

Run:

```text
PYTHONPATH=tmp/python_deps python certify_ten_vertex_balanced_set_trees.py
python run_kissat_proof.py \
  --kissat tmp/kissat_wsl_lf/build/kissat \
  --cnf tmp/ten_vertex_balanced_set_trees_all_orbits.cnf \
  --proof tmp/ten_vertex_balanced_set_trees_all_orbits.drat \
  --stdout tmp/ten_vertex_balanced_set_trees_kissat.stdout.log \
  --stderr tmp/ten_vertex_balanced_set_trees_kissat.stderr.log \
  --output tmp/ten_vertex_balanced_set_trees_kissat_run.json \
  --configuration unsat
python run_drat_trim.py \
  --drat-trim tmp/drat-trim/drat-trim \
  --cnf tmp/ten_vertex_balanced_set_trees_all_orbits.cnf \
  --proof tmp/ten_vertex_balanced_set_trees_all_orbits.drat \
  --stdout tmp/ten_vertex_balanced_set_trees_drat_trim.stdout.log \
  --stderr tmp/ten_vertex_balanced_set_trees_drat_trim.stderr.log \
  --output tmp/ten_vertex_balanced_set_trees_drat_replay.json \
  --forward
PYTHONPATH=tmp/python_deps python audit_ten_vertex_balanced_set_trees.py
```

The primary generator uses integer compositions, least-vertex recursive
partitions, and CaDiCaL 1.9.5.  The independent audit uses reverse
compositions, restricted-growth partitions, reversed coordinate and
partner orders, and Glucose 4.  It separately recovers all 104 profiles,
the 2,460 two- or three-block even partitions, the same 10 cube orbits,
and 10 UNSAT decisions, then binds the external proof replay.

## Boundary

Every order-ten witness remaining after this theorem must enter the
separate deeper-blocker alternative.  At order twelve the
parity-constrained set-tree system has not yet been exhaustively decided.
