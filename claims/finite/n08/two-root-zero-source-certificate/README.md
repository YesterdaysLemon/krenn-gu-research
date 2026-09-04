# Exact support certificate for the pure zero-root source

This package certifies one finite necessary-support instance, not the
global Krenn--Gu conjecture. Its mathematical input is the pure `(3,3)`
orientation branch of an eight-vertex, maximum-two-root, common-coordinate
source with zero root block. The
[owning zero-block theorem](../TWO_ROOT_COMMON_COORDINATE_ZERO_EXCLUSION.md)
supplies the reduction and exhaustive branch cover, while the
[completion theorem](../TWO_ROOT_COMMON_COORDINATE_COMPLETION_THEOREM.md)
combines all root ranks.

The six outside vertices are `A0,A1,A2,B0,B1,B2`. The six AA/BB physical
blocks are nonzero matrix units. The nine full four-vertex cofactor tensors
are zero off the diagonal and nonzero pure colour-i tensors on the diagonal.
The P2 pure-tensor anchor lemma and re-rooting into the
[accepted rank-at-least-two theorem](../TWO_ROOT_COMMON_COORDINATE_EXCLUSION_THEOREM.md)
force rectangular support in every cross block and the stated row/column
anchor disjunctions. These are necessary conditions only; no converse
claim about complex coefficients is made.

## Exact instance

The standard-library [generator](generate_instance.py) produces all 729
cofactor word constraints, with no symmetry fixing or omitted coordinate
choices. The raw instance has 2,394 variables and 11,394 clauses:

| Clause family | Count |
| --- | ---: |
| Six nonzero matrix units | 222 |
| Matching-term definitions | 6,561 |
| Coefficient necessities | 2,181 |
| Rectangular cross supports | 1,458 |
| P2 anchors | 972 |

The generator explicitly emits CRLF bytes on every platform to preserve
the independently audited frozen instance hash. Generated DIMACS files
belong in ignored scratch and are not tracked.

## Certificate and checker

[certificate.json](certificate.json) is deliberately retained as durable
proof data. Its exact bytes are protected by the package `.gitattributes`.
It is a full binary DPLL tree with 6,860 branches and 6,861 leaves. Every
internal node is `[literal, left, right]`, covering both signs of the
decision. A null leaf is accepted only after exact unit propagation
derives a conflict. Thus accepted leaves exclude all branches exhaustively.

The [checker](check_certificate.py) independently reconstructs the clause
multiset using arithmetic IDs and recursive perfect matchings, then checks
the tree with functional positive/negative bit masks. It imports no solver,
producer, or primary instance constructor. Tautological clauses are removed
and duplicate literals collapsed by exact Boolean identities. Both input
and certificate hashes are checked. Nine small positive/negative controls
test the checker, and Python optimization is rejected because assertions
are load-bearing. The metadata counts do not substitute for traversal.

The [manifest](manifest.json) pins the objects and their exact scope. A native
solver first suggested UNSAT without a usable trace and exited abnormally;
that result supplies no proof. The accepted certificate was produced by a
separate exact DPLL search and fully checked independently. No SAT solver
or native algebra dependency is required for replay. No Lean formalization
is claimed.

## Replay from repository root

```text
python claims/finite/n08/two-root-zero-source-certificate/generate_instance.py --output tmp/two-root-zero-source.cnf
python tools/research/run_bounded.py --run-id n08-zero-source-certificate --timeout-seconds 600 --memory-mb 2048 -- python claims/finite/n08/two-root-zero-source-certificate/check_certificate.py --cnf tmp/two-root-zero-source.cnf --certificate claims/finite/n08/two-root-zero-source-certificate/certificate.json
```

Use a different run ID if that ID is active. The independent reference
replay took about 89 seconds; timing is not evidence of mathematical scope.
`--encoding-only` checks instance reconstruction without accepting a proof.
`--self-test-only` runs the small checker controls only. Neither mode should
be reported as a full certificate replay.
