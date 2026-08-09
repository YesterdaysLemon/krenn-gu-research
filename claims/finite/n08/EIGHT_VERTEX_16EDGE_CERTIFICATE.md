# Eight-vertex degree-four exact-16-edge exclusion

## Claim

There is no eight-vertex, three-colour complex Krenn-Gu witness whose
essential skeleton has exactly 16 edges and a degree-four vertex.

Together with `EIGHT_VERTEX_DEGREE4_FRONTIER.md`, this excludes every such
essential skeleton with at most 16 edges.  It does not exclude 17-edge or
denser skeletons, degree-five-minimum skeletons, or arbitrary even order.

An essential skeleton contains exactly the nonzero blocks that lie in at
least one perfect matching.  It is matching-covered by definition.  It must
be connected, since otherwise its perfect-matching tensor factors across a
component split while GHZ has flattening rank three.  The generic killer
theorem gives minimum degree at least three.

## Complete skeleton catalogue

nauty 2.9.3 generated every connected unlabeled graph on eight vertices
with minimum degree three and 12 through 16 edges:

```text
geng -cq -d3 8 12:16
```

The pinned output is

```text
tmp/n8_mindeg3_e12_16.g6
SHA-256 27cd1f0ce69e65fb3fee28633c75e2f7925566df7856a394c3a0ab6e096548fe
```

Its independently decoded edge-count distribution is:

| Edges | Unlabeled graphs |
|---:|---:|
| 12 | 5 |
| 13 | 35 |
| 14 | 136 |
| 15 | 309 |
| 16 | 465 |

Of the 465 exact-16 graphs, 440 have a degree-four vertex.  Requiring every
edge to lie in a perfect matching leaves 364 unlabeled essential
skeletons.

At a degree-four vertex, the singleton theorem and global colour symmetry
allow the labels

```text
centre             0
singleton neighbour 1
two other killers   2,3
spare neighbour     4
```

The remaining stabilizer is `S3` on vertices `5,6,7`, together with the
joint swap of vertices `2,3` and colours `1,2`.  Canonicalization under
these 12 symmetries gives exactly 10,241 labelled skeleton roles.

## Necessary support CNF

The base support relaxation uses:

1. nonzero indicators for the 25 allowed blocks;
2. a nonzero matching monomial for each monochromatic amplitude;
3. no forbidden amplitude with exactly one nonzero matching monomial;
4. a distinct generic killer and a diagonal anchor for every task;
5. the degree-three singleton-star theorem;
6. the degree-four singleton and proportionality theorems.

These are necessary conditions only.  Therefore SAT would not establish a
complex witness, while UNSAT soundly excludes one.

The exact-16 base used here is:

```text
tmp/eight_vertex_local_degree4_full_local_max16.cnf
variables       394,821
clauses       2,849,784
SHA-256 115904d925c3cf25ab3919f810b62a0a159749cc3bf78e0042c51fdb8148e100
```

## Exact Laurent conflict

The first support survivor selected 34 nonzero matrix entries.  Replaying
all 6,561 characteristic-zero amplitude equations on that torus gives:

```text
restricted equations    64
primitive binomials      59
binomial lattice rank    16
```

Three source amplitudes reduce to a Laurent unit.  Hence the stratum is
empty over the complex numbers.  Tracking only the entries used in that
derivation produces a 48-literal support conflict.  Its 12 stabilizer
images are sound no-goods: each fixes every surviving monomial factor
nonzero and at least one factor of every discarded monomial to zero.

Appending those 12 clauses gives:

```text
tmp/eight_vertex_local_degree4_cegar1_max16.cnf
variables       394,821
clauses       2,849,796
SHA-256 570694ce87893c68f5900bde185203b8f2d6216d82da94454936e880e81b6d59
```

`verify_eight_vertex_16edge.py` reconstructs the full amplitude system,
the Laurent reduction, the source-equation dependency set, the conflict
cube, and all 12 clauses rather than trusting the saved manifest.

## One portable selector certificate

One fresh selector was added for every canonical skeleton role.  At least
one selector is true; a true selector fixes all 25 block indicators to its
role.  This compiles the complete 10,241-case disjunction into:

```text
tmp/eight_vertex_16edge_catalogue_cegar1.cnf
variables       405,062
clauses       3,105,822
SHA-256 04f3864a50a7443009998cf9fea0bd0f780753cfa3de390e740a3892683d5cf3
```

The audit independently regenerates all roles and then compares the base
prefix, selector disjunction, and every one of the 256,025
selector-to-block implications line by line.

## Independent decisions and proof checking

MiniSat returned `UNSATISFIABLE` in 969.027 CPU seconds.  CaDiCaL 1.9.5
independently returned `s UNSATISFIABLE` and produced:

```text
tmp/eight_vertex_16edge_catalogue_cegar1_cadical195.drat
bytes   243,459,151
SHA-256 dad69926d0ac6fa23abb2c7812096990dd1dcb0c98f14c2773b3c6724f35d7e1
```

Independent `drat-trim` replay reports:

```text
713,100 of 3,105,822 input clauses in the core
178,969 of 1,806,676 lemmas in the core
211,119,420 resolution steps
0 RAT lemmas
s VERIFIED
```

## Fail-closed audit

Run:

```text
python verify_eight_vertex_16edge.py
```

It pins every source and decision artifact, replays the algebraic conflict,
rechecks the complete graph catalogue and role quotient, audits the compiled
selector CNF, and requires both solver terminal lines plus the independently
verified DRAT trace.  Its authoritative output is:

```text
tmp/eight_vertex_16edge_audit.json
```

with `"verified": true`.
