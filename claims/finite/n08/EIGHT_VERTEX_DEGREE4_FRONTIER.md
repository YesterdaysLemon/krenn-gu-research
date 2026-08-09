# Eight-vertex degree-four sparse frontier

## Claim

There is no eight-vertex, three-colour complex Krenn-Gu witness whose
essential skeleton has a degree-four vertex and at most 17 edges.

“Essential” means that edges lying in no perfect matching have been deleted;
they never occur in the perfect-matching tensor.  A disconnected essential
skeleton is also impossible: its tensor factors across components, whereas
the GHZ tensor has flattening rank three across every nontrivial component
split.

The at-most-15 part is one direct support certificate.  The exact-16 and
exact-17 parts use complete nauty skeleton catalogues, replayed Laurent
conflicts, and portable selector DRAT proofs; see
`EIGHT_VERTEX_16EDGE_CERTIFICATE.md` and
`EIGHT_VERTEX_17EDGE_CERTIFICATE.md`.  This theorem does not exclude
18-edge or denser skeletons.

## Necessary analytic conditions

The CNF uses four proved local consequences of an exact witness:

1. every `(vertex,colour)` has a distinct nonzero rank-one column killer;
2. every `(vertex,colour)` has a diagonal anchor;
3. a degree-three vertex has exactly three monochromatic singleton incident
   blocks, one of each colour;
4. a degree-four vertex has an incident monochromatic singleton, and every
   non-coordinate selected killer is proportional to each nonzero
   nonmatching-colour column of the spare block.

The proofs are in `docs/research-notes.md`.

By vertex, neighbour, and global-colour symmetry, a hypothetical
degree-four vertex is labelled as vertex 0 with neighbours 1,2,3,4:

```text
W_01 = alpha e_0 outer(e_0)
W_02 = a_1 outer(e_1)
W_03 = a_2 outer(e_2)
```

and `W_04` is the spare block.

## Support CNF

`eight_vertex_local_degree4_support.py --maximum-edges 15` materializes:

```text
tmp/eight_vertex_local_degree4_full_local_max15.cnf
variables       394,797
clauses       2,849,737
SHA-256 7f42f33aeee7349dd3a2b97e142f5a25f258115f8ffcf2fd1c593e8271f15fff
```

In addition to the local lemmas, it requires every monochromatic amplitude
to have a nonzero matching monomial and forbids a nonmonochromatic amplitude
from having exactly one.  These are necessary over every field, so CNF
UNSAT excludes every exact complex solution in scope.

The sequential at-most counter is exhaustively regression-tested on all
assignments through six variables.

## Independent decisions and proof

MiniSat returned UNSAT in 1,139.49 CPU seconds.  CaDiCaL 1.9.5 independently
returned `s UNSATISFIABLE` in 2,488.77 real seconds and produced:

```text
tmp/eight_vertex_local_degree4_full_local_max15_cadical195.drat
bytes   225,486,354
SHA-256 ab03b1dd1d02293f199e28a271909addee4e41f46076dffe6baf341c0e091417
```

Independent `drat-trim` backward checking reports:

```text
557,963 of 2,849,737 input clauses in the core
302,742 of 2,761,071 lemmas in the core
46,200,153 resolution steps
0 RAT lemmas
s VERIFIED
```

## Fail-closed audit

Run:

```text
python claims/finite/n08/verify_eight_vertex_degree4_frontier.py
```

It pins the CNF, both solver outputs, the proof, and the proof-checker log,
then writes:

```text
tmp/eight_vertex_degree4_frontier_audit.json
```

with `"verified": true`.

## Exact 16 edges

The complete exact-16 certificate independently enumerates 364 unlabeled
connected matching-covered skeletons with a degree-four vertex and 10,241
canonical singleton/killer roles.  A replayed 48-literal Laurent conflict
and its 12 symmetries reduce every role to UNSAT in one selector CNF:

```text
tmp/eight_vertex_16edge_catalogue_cegar1.cnf
variables       405,062
clauses       3,105,822
SHA-256 04f3864a50a7443009998cf9fea0bd0f780753cfa3de390e740a3892683d5cf3
```

CaDiCaL's 243,459,151-byte proof was independently replayed by
`drat-trim`, which returned `s VERIFIED` after 211,119,420 resolution
steps.  The fail-closed audit is:

```text
python claims/finite/n08/verify_eight_vertex_16edge.py
tmp/eight_vertex_16edge_audit.json: "verified": true
```

## Exact 17 edges

The complete exact-17 certificate independently enumerates 420 unlabeled
connected matching-covered skeletons with a degree-four vertex and 11,051
canonical singleton/killer roles.  Fifty-seven replayed Laurent conflicts
produce 666 learned support clauses and reduce every role to UNSAT.  One
selector CNF compiles the complete case split:

```text
tmp/eight_vertex_17edge_catalogue_flag_laurent.cnf
variables       439,322
clauses       3,349,145
SHA-256 9a71eee2af390ef037882f8e2a07937b55847e52dc0cb1d63f71a005e9fe64b9
```

CaDiCaL's 853,663,837-byte proof was independently replayed by
`drat-trim`, which returned `s VERIFIED` after 1,153,827,131 resolution
steps.  The fail-closed audit is:

```text
python claims/finite/n08/verify_eight_vertex_degree4_e17.py
tmp/eight_vertex_degree4_e17_final_audit.json: "verified": true
```
