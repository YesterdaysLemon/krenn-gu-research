# Order-twelve complement-profile set-tree obstruction

## Status

This is a complete finite exclusion of one normal-type multiplicity
profile in the simultaneous three-colour balanced all-bridge branch on
twelve vertices:

```text
6 vertices of type 000,
6 vertices of type 111.                                (1)
```

It has no support-degree bound and allows arbitrary overlap among the
selected monochromatic matchings.  It does not exclude the other
order-twelve profiles, the separate deeper-blocker branch, or the global
Krenn--Gu conjecture.

## Sound necessary set system

For the profile in (1), every subset allowed by any of the three normal
bit-balance equations contains equally many `000` and `111` vertices.
For each colour `c`, define

```text
T_c = {nonempty even U subset V : haf(Z^c[U]) != 0}.
```

A hypothetical witness supplies three such families containing `V`.
They obey three sound necessary conditions.

1. Vertex-wise hafnian expansion makes each `T_c` a set tree: if
   `U in T_c` and `v in U`, some `w in U-{v}` has both
   `{v,w} in T_c` and `U-{v,w} in T_c`.
2. The hafnian convolution identity gives an all-size split: whenever
   `U in T_c`, at every nontrivial even split size some
   `A subset U` has both `A in T_c` and `U-A in T_c`.
3. No partition of `V` into two or three nonempty even balanced blocks
   can assign those blocks injectively to distinct tree colours.  Such
   a partition would give a forbidden nonconstant saturated-diagonal
   coefficient with a nonzero product.

The CNF uses a membership variable only for a nonempty balanced subset.
Its exact census is:

```text
membership variables                         2,769
vertex-expansion instances                  16,416
vertex-expansion witnesses                  54,216
convolution-split instances                    789
convolution-split witnesses                 24,225
eligible two/three-block partitions          5,861
injective-colour incompatibility clauses    35,166

total variables                             81,210
total clauses                              209,263
```

These are necessary conditions, not an attempted converse: proving
their joint inconsistency is therefore enough to exclude the profile.

## Symmetry-complete decision

Every set tree containing `V` exposes a perfect matching together with
a recursive deletion order.  The `S_6 x S_6` action on the two type
classes maps the exposed matching of tree 0, in deletion order, to the
six identity pairs.  The CNF fixes those pairs and the complement of the
first pair.

Expand tree 1 first at row 0.  Pairing it with column 0 immediately
violates the two-block distinct-colour incompatibility condition.
The other five columns form one orbit under the remaining diagonal
`S_5`, so normalize the first pair to row 0--column 1.

Thereafter expand at the lowest unused row.  At each step the stabilizer
of the already exposed chain partitions the unused partners into exact
orbits.  Recursing on one representative per orbit produces 16 leaves.
Their orbit weights sum to

```text
5! = 120,                                               (2)
```

so they cover every possible hard partner chain.  CaDiCaL first found
all 16 leaves UNSAT.

For an externally checkable theorem certificate, one fresh selector
represents the immediate same-partner branch and 16 selectors represent
the hard leaves.  The selector extension has 17 variables and 179
clauses, giving

```text
81,227 variables,
209,442 clauses.
```

Kissat proves this combined selector CNF UNSAT.  Its 70,573,433-byte
DRAT proof is accepted by an independent forward `drat-trim` replay:

```text
157,772 of 209,442 input clauses in core
971,733 of 1,378,510 lemmas in core
42,612,268 resolution steps
15,925 RAT lemmas
s VERIFIED
```

## Independent audit

`audit_twelve_vertex_complement_profile.py` does not reuse the primary
partition or split enumerators.  It reconstructs balanced subsets by
restricted-growth partitions and combination splits, checks the formula
census above, verifies the base prefix and all 179 selector clauses
exactly, and checks 31 local stabilizer-orbit covers.

It then solves the 17 canonical branches incrementally with Glucose 4.
Every branch is UNSAT, and the hard-leaf weights again cover all 120
chains.  This is an independent semantic reconstruction with matching
counts and decisions; it is not claimed to be a byte-for-byte
independent reconstruction of the base CNF.

## Verification

With the bundled dependencies on `PYTHONPATH`, run:

```text
python \
  explore_twelve_vertex_complement_set_tree_cnf.py
python \
  explore_twelve_vertex_complement_chain_orbits.py
python \
  certify_twelve_vertex_complement_profile.py
python run_kissat_proof.py \
  --kissat tmp/kissat_wsl_lf/build/kissat \
  --cnf tmp/twelve_vertex_complement_profile_selector.cnf \
  --proof tmp/twelve_vertex_complement_profile_selector.drat \
  --stdout tmp/twelve_vertex_complement_profile_kissat.stdout.log \
  --stderr tmp/twelve_vertex_complement_profile_kissat.stderr.log \
  --output tmp/twelve_vertex_complement_profile_kissat_run.json \
  --configuration unsat
python run_drat_trim.py \
  --drat-trim tmp/drat-trim/drat-trim \
  --cnf tmp/twelve_vertex_complement_profile_selector.cnf \
  --proof tmp/twelve_vertex_complement_profile_selector.drat \
  --stdout tmp/twelve_vertex_complement_profile_drat_trim.stdout.log \
  --stderr tmp/twelve_vertex_complement_profile_drat_trim.stderr.log \
  --output tmp/twelve_vertex_complement_profile_drat_replay.json \
  --forward
python \
  audit_twelve_vertex_complement_profile.py
```

Principal SHA-256 values are:

```text
base CNF
  6b1b77d1da94d189ef96865f319252c7398cd0c05521eb7e8bf2b2e56a78e0aa
selector CNF
  f068909260432a7e2ae7107843210cffabfb13c36634d9fd9452c63a61caedc8
raw DRAT proof
  22d560ecad355664894980d0002a6bd949ac12ef7ab8b33a3612090e4868fbe4
tmp/twelve_vertex_complement_profile_selector_manifest.json
  cd0e8ac1c9420de24fbb0c022838006dc69fb1c942b3b12cf699bf9a27755ecb
tmp/twelve_vertex_complement_profile_kissat_run.json
  c3a0c52d0698da2a5c09d7dca20d677d4bba5fc49cb322e03a766a9e7acf0458
tmp/twelve_vertex_complement_profile_drat_replay.json
  b170abcc6ab9b236dd832daf3ee1317a440f7080ab75d3a33ab237bcda767e2a
tmp/twelve_vertex_complement_profile_audited.json
  7bf711d3b94a856132d8b26d04797e5855eca4d31353525bf71f0220735f3a70
```

## Boundary

The theorem closes only the most symmetric complementary order-twelve
profile.  A full order-twelve all-bridge theorem would still have to
exclude every other balanced normal-type profile.  The deeper-blocker
branch remains a separate arbitrary-order target.
