# Order-eight balanced all-bridge obstruction

## Status

This is a complete finite exclusion of the simultaneous three-colour
balanced all-bridge branch on eight vertices.  It has no support-degree
bound and permits arbitrary overlap among the selected monochromatic
matchings.

The proof has two stages.  A corrected hafnian set-tree certificate
excludes 55 of the 57 balanced normal-type profiles.  The other two
profiles form one parity orbit; an exact support-level factorization into
six `K_2,2` components excludes that orbit.

The separate deeper-blocker branch remains outside the hypotheses.
Accordingly, this is not a complete order-eight theorem and not a proof
of the global Krenn--Gu conjecture.

## Sound set-tree reduction

Let `Z^c` be the saturated colour-`c` diagonal zero layer and put

```text
T_c = {nonempty even U subset V : haf(Z^c[U]) != 0}.
```

Hafnian expansion makes each `T_c` a set tree.  Every member also obeys
the saturated transition balance on the two bits other than `bc`:

```text
count_U(00) = count_U(11),
count_U(01) = count_U(10).                            (1)
```

A witness requires the three trees to be incompatible in the following
sound sense.  There is no partition of `V` into two or three blocks,
assigned to pairwise distinct tree colours, with every block in its
assigned tree.  Such a partition would give a nonmonochromatic
zero-layer coefficient

```text
product_c haf(Z^c[U_c]) != 0.
```

Tree colours must be distinct here.  Reusing a colour on separate blocks
does not justify multiplying their hafnians, because same-colour edges
may join the blocks.

## Corrected set-tree classification

Bit balance gives 57 multiplicity profiles.  Independent flips and
permutations of the three bit coordinates form a 48-element cube action
with eight profile orbits.  For each orbit representative, the corrected
SAT formula:

1. creates `X(c,U)` only for subsets satisfying (1);
2. asserts `X(c,V)` for each colour;
3. encodes every vertex-wise set-tree expansion; and
4. forbids only two- or three-block partitions using distinct colours.

Seven orbit formulas are UNSAT and cover 55 profiles.  The combined CNF
has 7,280 variables and 17,590 clauses.  Kissat's 86,018-byte DRAT proof
is independently accepted by `drat-trim`.

The eighth abstract formula is SAT and consists exactly of

```text
(0,2,2,0,2,0,0,2)
(2,0,0,2,0,2,2,0).                                  (2)
```

These are respectively two copies of every odd-parity cube type and two
copies of every even-parity cube type.  A bit flip exchanges them.  SAT
of the set-tree abstraction is not a weighted-hafnian realization, so a
second argument is needed.

## Exact obstruction for the parity orbit

Use the odd profile in (2), with vertex types

```text
1,1,2,2,4,4,7,7.
```

The saturated graph for each colour is the disjoint union of two
`K_2,2` components.  In terms of type classes, the components are

```text
colour 0:  1--7, 2--4
colour 1:  1--4, 2--7
colour 2:  1--2, 4--7.                               (3)
```

The full colour-`c` hafnian is the product of the two `2 x 2`
permanents in (3).  It is required to be nonzero, so each of the six
component permanents is nonzero.  In particular, each component support
contains a perfect matching.  A `K_2,2` has exactly seven edge-support
patterns with this property.

For an arbitrary vertex colouring, every colour factor splits over its
two components.  A component factor is:

- `1` if no component vertex is selected;
- one edge weight if one vertex on each side is selected;
- its nonzero full permanent if both vertices on each side are selected;
- structurally zero if the two selected side sizes differ.

Of the `3^8-3 = 6,558` nonmonochromatic colourings, 6,510 are already
structurally zero.  Each of the remaining 48 coefficients is a product
of nonzero full-component permanents and selected singleton edge
weights.  Its required vanishing therefore says that at least one of
those edge weights is zero.

Introduce one Boolean nonzero-support variable for each of the 24
saturated edges.  The six component-perfect-matching requirements give
24 CNF clauses, and the 48 structurally possible forbidden colourings
give 48 no-good clauses.  The resulting 24-variable, 72-clause CNF is
UNSAT.  Kissat emits a 729-byte DRAT proof, independently verified by
`drat-trim`.

A structurally different audit enumerates the seven support patterns of
each component and tests all

```text
7^6 = 117,649
```

support products.  Zero survive.  This closes the only abstract
set-tree orbit left by the first stage.

## Verification

Run:

```text
python claims/finite/n08/certify_eight_vertex_balanced_set_trees.py
python tools/generate/run_kissat_proof.py \
  --kissat tmp/kissat_wsl_lf/build/kissat \
  --cnf tmp/eight_vertex_balanced_set_trees_excluded_orbits.cnf \
  --proof tmp/eight_vertex_balanced_set_trees_excluded_orbits.drat \
  --stdout tmp/eight_vertex_balanced_set_trees_kissat.stdout.log \
  --stderr tmp/eight_vertex_balanced_set_trees_kissat.stderr.log \
  --output tmp/eight_vertex_balanced_set_trees_kissat_run.json \
  --configuration unsat
python tools/generate/run_drat_trim.py \
  --drat-trim tmp/drat-trim/drat-trim \
  --cnf tmp/eight_vertex_balanced_set_trees_excluded_orbits.cnf \
  --proof tmp/eight_vertex_balanced_set_trees_excluded_orbits.drat \
  --stdout tmp/eight_vertex_balanced_set_trees_drat_trim.stdout.log \
  --stderr tmp/eight_vertex_balanced_set_trees_drat_trim.stderr.log \
  --output tmp/eight_vertex_balanced_set_trees_drat_replay.json \
  --forward
python claims/finite/n08/audit_eight_vertex_balanced_set_trees.py

python claims/finite/n08/certify_eight_vertex_parity_hafnian_supports.py
python tools/generate/run_kissat_proof.py \
  --kissat tmp/kissat_wsl_lf/build/kissat \
  --cnf tmp/eight_vertex_parity_hafnian_supports.cnf \
  --proof tmp/eight_vertex_parity_hafnian_supports.drat \
  --stdout tmp/eight_vertex_parity_hafnian_supports_kissat.stdout.log \
  --stderr tmp/eight_vertex_parity_hafnian_supports_kissat.stderr.log \
  --output tmp/eight_vertex_parity_hafnian_supports_kissat_run.json \
  --configuration unsat
python tools/generate/run_drat_trim.py \
  --drat-trim tmp/drat-trim/drat-trim \
  --cnf tmp/eight_vertex_parity_hafnian_supports.cnf \
  --proof tmp/eight_vertex_parity_hafnian_supports.drat \
  --stdout tmp/eight_vertex_parity_hafnian_supports_drat_trim.stdout.log \
  --stderr tmp/eight_vertex_parity_hafnian_supports_drat_trim.stderr.log \
  --output tmp/eight_vertex_parity_hafnian_supports_drat_replay.json \
  --forward
python claims/finite/n08/audit_eight_vertex_parity_hafnian_supports.py
```

The set-tree primary and audit use different profile, partition, variable,
and solver enumerations.  The parity-orbit primary derives a necessary
support CNF directly from all vertex colourings; its audit instead
enumerates all six component supports.  Both external UNSAT proofs are
bound to their exact CNFs and independently replayed.

## Boundary

No order-eight witness exists in the simultaneous balanced all-bridge
branch.  An order-eight witness, if one exists, must enter the separate
deeper-blocker alternative.
