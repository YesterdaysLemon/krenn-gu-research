# Eight-vertex degree-four exact-17-edge exclusion

## Claim

There is no eight-vertex, three-colour complex Krenn-Gu witness whose
essential skeleton has exactly 17 nonzero blocks and a degree-four vertex.

Together with the certificates linked from
`EIGHT_VERTEX_DEGREE4_FRONTIER.md`, this excludes every such essential
skeleton with at most 17 edges.  It does not exclude 18-edge or denser
skeletons, skeletons of minimum degree five, or arbitrary even order.
Accordingly, this is a finite theorem and not a solution of the full prize
conjecture.

An essential skeleton contains exactly the nonzero blocks that lie in at
least one perfect matching.  It is matching-covered by definition.  It must
be connected, since otherwise its perfect-matching tensor factors across a
component split while GHZ has flattening rank three.  The generic killer
theorem gives minimum degree at least three.

## Complete skeleton catalogue

The pinned graph6 catalogue is:

```text
tmp/n8_mindeg3_e17.g6
SHA-256 3b7c9ba5f96ac8a3e5f184fe2bdac570835d13a8b688ece60455019dc6b43caf
```

Independent decoding, matching-covered filtering, degree-four role
selection, and stabilizer canonicalization give:

```text
unlabeled connected matching-covered skeletons   420
canonical singleton/killer roles               11,051
```

The role fixes one degree-four centre, its guaranteed monochromatic
singleton, its two other selected killers, and its spare neighbour, modulo
the residual vertex and colour stabilizer.  The audit regenerates this
quotient rather than trusting the saved counts.

## Necessary support and algebraic conflicts

The base support relaxation uses only necessary conditions:

1. every skeleton block is nonzero;
2. every monochromatic amplitude has a nonzero matching monomial;
3. no forbidden amplitude has exactly one nonzero matching monomial;
4. every vertex-colour task has a distinct generic killer and diagonal
   anchor;
5. every degree-three vertex satisfies the singleton-star theorem;
6. every degree-four neighbourhood satisfies the singleton and
   proportionality theorems.

SAT in this relaxation would not establish a complex witness.  UNSAT after
sound algebraic conflict learning does exclude one.

For each support survivor, the Laurent checker restricts all characteristic-
zero amplitude equations to the selected nonzero entries.  It records an
exact integer-lattice derivation of a Laurent unit, then learns only the
support cube needed by that derivation.  All stabilizer images of each cube
are checked as support no-goods.

The initial local chain contributes four Laurent conflicts.  The complete
skeleton-role batch contributes another 53:

```text
Laurent conflicts                  57
learned support clauses           666
batch support models               53
fallback computations               0
processed/UNSAT roles   11,051/11,051
```

The complete batch manifest is:

```text
tmp/eight_vertex_skeleton_laurent_flag_batch_e17.json
```

`verify_laurent_batch_manifest.py` replays the exact algebraic derivation
behind every local conflict.  `verify_skeleton_laurent_batch.py` regenerates
the skeleton roles, checks every learned clause, and requires complete
coverage with no unresolved fallback.

## Portable selector certificate

One fresh selector is added for every canonical role.  At least one selector
must be true, and a true selector fixes all allowed block indicators to that
role.  This compiles the complete 11,051-case disjunction into:

```text
tmp/eight_vertex_17edge_catalogue_flag_laurent.cnf
variables       439,322
clauses       3,349,145
SHA-256 9a71eee2af390ef037882f8e2a07937b55847e52dc0cb1d63f71a005e9fe64b9
```

The selector manifest records 276,275 selector-to-block implications:

```text
tmp/eight_vertex_17edge_catalogue_flag_laurent.json
```

`verify_catalogue_selector.py` independently regenerates every role and
checks the base prefix, selector disjunction, and all implications.

## Independent decision and proof checking

CaDiCaL 1.9.5 returned `s UNSATISFIABLE` in 5,478.56 real seconds and
produced:

```text
tmp/eight_vertex_17edge_catalogue_flag_laurent_cadical195.drat
bytes   853,663,837
SHA-256 7b948d6972f61f659959f4ac0062efcb187cde2685f460c689c8559eeb95d4c9
```

Independent `drat-trim` backward checking reports:

```text
1,001,177 of 3,349,145 input clauses in the core
851,993 of 3,404,971 lemmas in the core
1,153,827,131 resolution steps
0 RAT lemmas
s VERIFIED
```

## Fail-closed audit

Run:

```text
python verify_eight_vertex_degree4_e17.py
```

The verifier:

1. replays the four local Laurent conflicts and confirms their CNF hash
   chain;
2. replays the 53-conflict skeleton batch and regenerates all 11,051 roles;
3. audits the complete selector compilation;
4. pins the graph catalogue, CNF, proof, solver log, and proof-checker log by
   SHA-256;
5. requires both `s UNSATISFIABLE` and the independent `s VERIFIED`.

Its authoritative output is:

```text
tmp/eight_vertex_degree4_e17_final_audit.json
```

with `"verified": true`.
