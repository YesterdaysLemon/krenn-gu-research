# Withdrawn overstrong order-eight set-tree encoding

## Status

**WITHDRAWN.**  This version incorrectly allowed a compatible partition
to reuse one tree colour on several blocks and multiplied the block
hafnians.  Same-colour blocks may have additional matching edges between
them, so that product need not equal the hafnian of their union.  Only
partitions whose blocks come from pairwise distinct trees factor
unconditionally.

The corrected classification is in
`EIGHT_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md`.  The old CNF,
UNSAT proof, and hashes below are not certificates.

## Withdrawn historical text

This is a complete finite exclusion of the simultaneous three-colour
balanced all-bridge branch on eight vertices.  It has no support-degree
bound and does not assume that the three selected monochromatic
matchings are pairwise disjoint.

The theorem does not cover the separate deeper-blocker branch and
therefore is not a complete order-eight proof or a proof of the global
Krenn--Gu conjecture.

## Saturated-diagonal reduction

By `UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md`, the sum of the
six permuted potentials is nonnegative on every balanced-bridge unit and
vanishes exactly on saturated monochromatic diagonal units.  Any
hypothetical witness therefore has a forbidden nonmonochromatic
coefficient whose entire expansion lies in the saturated-diagonal zero
layer.

For colour `c`, let `Z^c` be its zero-layer diagonal matrix and define

```text
T_c = {nonempty even U subset V : haf(Z^c[U]) != 0}.
```

The full set `V` belongs to each `T_c`, because its monochromatic
coefficient is one.

## Hafnian set trees

Each `T_c` is a set tree.  If `U` belongs to `T_c`, `|U|>=4`, and
`v in U`, the hafnian expansion

```text
haf(Z^c[U])
  = sum_(u in U minus {v})
      Z^c[v,u] haf(Z^c[U minus {v,u}])
```

is nonzero.  At least one summand is nonzero, so both `{v,u}` and
`U minus {v,u}` belong to `T_c`.

The saturated type geometry restricts which subsets can belong.  A
colour-`c` zero edge flips both normal bits other than `bc`.  If those
bits are `bj,bk`, every `U in T_c` therefore satisfies

```text
number of 00 vertices in U = number of 11 vertices in U,
number of 01 vertices in U = number of 10 vertices in U              (1)
```

when vertices are grouped by `(bj,bk)`.

The three set trees must be incompatible.  Otherwise a partition

```text
V = U_1 disjoint union ... disjoint union U_t,  t>=2,
```

with `U_i in T_(c_i)` and at least two distinct colours among the `c_i`
would define a nonmonochromatic zero-layer coefficient

```text
product_i haf(Z^(c_i)[U_i]) != 0,
```

contradicting the target zero.

## Complete order-eight SAT theorem

Bit balance leaves exactly 57 multiplicity profiles of the eight normal
types on eight vertices.  Vertex labels inside one type are immaterial,
so one canonical labelled representative per profile is complete.

For every profile, the certificate introduces a Boolean variable

```text
X(c,U)
```

for each nonempty even subset satisfying (1).  It asserts:

1. `X(c,V)` for all three colours;
2. the set-tree expansion axiom for every `X(c,U)` and every `v in U`;
3. no set partition of `V` into at least two differently coloured true
   blocks.

The expansion implication is encoded with Tseitin witnesses for the
possible partner `u`.  All even set partitions of eight vertices are
enumerated exactly.  Every one of the 57 formulas is UNSAT.

A combined selector CNF contains all 57 formulas as disjoint conditional
branches plus a clause requiring at least one branch.  It is therefore
UNSAT exactly when every profile formula is UNSAT.  Kissat produces a
raw DRAT proof for this combined CNF, and the independent `drat-trim`
checker returns `s VERIFIED`.

## Verification

Run:

```text
PYTHONPATH=tmp/python_deps python certify_eight_vertex_balanced_set_trees.py
python run_kissat_proof.py \
  --kissat tmp/kissat_wsl_lf/build/kissat \
  --cnf tmp/eight_vertex_balanced_set_trees_all_profiles.cnf \
  --proof tmp/eight_vertex_balanced_set_trees_all_profiles.drat \
  --stdout tmp/eight_vertex_balanced_set_trees_kissat.stdout.log \
  --stderr tmp/eight_vertex_balanced_set_trees_kissat.stderr.log \
  --output tmp/eight_vertex_balanced_set_trees_kissat_run.json \
  --configuration unsat
python run_drat_trim.py \
  --drat-trim tmp/drat-trim/drat-trim \
  --cnf tmp/eight_vertex_balanced_set_trees_all_profiles.cnf \
  --proof tmp/eight_vertex_balanced_set_trees_all_profiles.drat \
  --stdout tmp/eight_vertex_balanced_set_trees_drat_trim.stdout.log \
  --stderr tmp/eight_vertex_balanced_set_trees_drat_trim.stderr.log \
  --output tmp/eight_vertex_balanced_set_trees_drat_replay.json \
  --forward
PYTHONPATH=tmp/python_deps python audit_eight_vertex_balanced_set_trees.py
```

The primary generator enumerates multiplicity profiles by integer
composition, set partitions by least-vertex recursion, and independently
solves all 57 local formulas with CaDiCaL 1.9.5 before writing the
combined CNF.

The audit does not import the primary implementation.  It enumerates
profiles in reverse type order, generates set partitions by restricted
growth strings, reverses all partner orders, rebuilds fresh local CNFs,
and decides them with Glucose 4.  It also binds the combined-CNF hash,
Kissat UNSAT record, and independently replayed DRAT record.

## Boundary

Every order-eight witness remaining after this theorem must leave the
simultaneous balanced all-bridge normal form through the deeper-blocker
alternative.  At larger orders, parity-constrained incompatible set
trees are not yet excluded; that is the next combinatorial boundary.
