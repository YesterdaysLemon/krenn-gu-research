# Independent audit of the pure Q=0 support obstruction

Encoding and certificate: **PASS**, conditional on the stated full-source
pure-(3,3) hypotheses and the accepted rank-at-least-two theorem. The
[owning zero-block proof](../../claims/finite/n08/TWO_ROOT_COMMON_COORDINATE_ZERO_EXCLUSION.md)
supplies the exhaustive analytic reduction. The
[portable package](../../claims/finite/n08/two-root-zero-source-certificate/README.md)
contains the checked artifact and replay. This is not a global conjecture
resolution or formalization.

## Exact mathematical bridge

The six vertices are A0,A1,A2,B0,B1,B2, each with three independent physical coordinates. The root block is zero; Ai has only its root-1 leg and Bi only its root-2 leg. Each same-pair channel is a nonzero multiple of Eii. An outer product equal to a nonzero Eii forces both leg directions to the corresponding coordinate direction. Thus all nine root matrix entries give exactly C(Ai,Bj)=0 for i!=j and C(Ai,Bi)=a nonzero pure colour-i product on the four other modes. These are full ternary physical cofactor equations, not inactive restrictions. Nothing here asserts the outside six-hafnian vanishes.

All six AA/BB blocks are nonzero matrix units: otherwise a torus zero of an AA edge, together with old root 2 whose edges to both endpoints vanish identically, gives three fully-supported pairwise-zero roots. Over C a nonzero Laurent polynomial without a torus zero is a Laurent unit; an endpoint-bilinear unit has precisely one nonzero coordinate coefficient. The BB argument uses old root 1. This covers zero blocks by contradiction too.

The P2 row anchor is valid with zero edges. Write

    f(A,B)g(C,D)+h(A,D)l(C,B)=alpha(A)beta(C)gamma(B)delta(D) != 0.

If both first-row forms factor through alpha, that row is an anchor. Otherwise interchange f,h if needed and choose a in ker(alpha) with f(a,-)!=0. If h(a,-)=0, restriction forces g=0, and the original nonzero product h*l forces l to factor through beta. If h(a,-)!=0, the restricted crossed-product equality gives g=b(C)h(a,D) and l=-b(C)f(a,B), up to a reciprocal nonzero scalar. Substitution into the original nonzero target gives b proportional to beta. In either case the other row anchors. The column assertion follows by transposing the tensor roles. This proof does not require rank-one blocks.

To justify rank(Xij)<=1, suppose instead rank(Xij)>=2 and use Ai,Bj as new roots. For each other Ak choose Bl so the row pair {i,k} differs from column pair {j,l}; of the two choices of l!=j, at most one is forbidden. This off-diagonal rectangle's permanent equals the negative of its nonzero AA*BB monomial. Its P2 anchor cannot be row Ai, since Xij has rank at least two. Therefore Xkj and physical Ai-Ak share the same coordinate at Ak, even if Xkj=0. The symmetric column argument covers each Bl. Old root 1 and old root 2 have respectively an Eii incidence and a zero incidence, or a zero incidence and an Ejj incidence. All six new outside vertices meet the precise common-coordinate physical incidence hypothesis.

The new root pair itself admits fully-supported vectors with zero pairing: a generic fully-supported left vector evaluates the rank-at-least-two block to a covector having at least two nonzero coordinates; its hyperplane contains a fully-supported right vector over C. The maximum root cardinality remains exactly two. The accepted theorem in TWO_ROOT_COMMON_COORDINATE_EXCLUSION_THEOREM.md therefore excludes this re-rooted point. No unaccepted rank-one root theorem or star constraint is used.

A rank-one complex matrix has Cartesian-product nonzero support, and the zero matrix has empty support. Hence the rectangular support implications used by the CNF are necessary. No converse about complex coefficient feasibility is asserted.

## Independent encoding reconstruction

Frozen SHA256:

    4415ea3d243603910729098d104240ca2d6fd2fa1d2843098e3131b4088ac1ac

The separate standard-library script lab-zeroq-independent-audit.py reconstructs all clauses with arithmetic variable IDs and recursively enumerated perfect matchings. It does not import or execute the generating solver script. Its clause multiset, including multiplicities and duplicate literals, equals the frozen file exactly:

| Category | Clauses |
| --- | ---: |
| Six matrix units | 222 |
| Matching-term equivalences | 6561 |
| Coefficient necessities | 2181 |
| Cross-block rectangles | 1458 |
| P2 anchors | 972 |
| Total | 11394 |

There are 2394 variables: 135 physical support entries, 2187 matching-term variables, and 72 existential anchor selectors. Entry IDs orient every undirected edge from its smaller vertex to its larger vertex; coordinates follow endpoints. All cross edges have A first and B second. The recursive matching generator agrees with all three four-vertex matchings. There are 9*81=729 cofactor coefficient positions, exactly three nonzero pure targets and 726 zero targets.

Each term variable is equivalent to the conjunction of its two disjoint edge-entry supports. Finite truth-table checks confirm these equivalences and confirm that the zero-target three-clause condition is exactly “the term count is not one.” A nonzero target requires at least one nonzero term. This drops coefficient cancellation constraints and therefore enlarges the physical feasible set; it cannot exclude a physical solution without a support contradiction.

Each physical AA/BB edge chooses any of its nine coordinates with exactly-one support. All labels and all choices occur; there is no symmetry fixing or hidden nonzero assumption on cross blocks. The anchor selectors imply coordinate-row or coordinate-column containment. The selected AA/BB unit clause requires one of the two relevant selectors. Conversely, whenever the physical row/column disjunction holds, set a selector for a valid anchor and leave other selectors false. Thus existential selectors impose exactly the intended support disjunction, with empty incident blocks satisfying containment.

## Certificate-checker semantics

The expected format is dpll-binary-up-v1, with null leaves and internal [literal,left,right] nodes. Both children are mandatory and correspond to the two opposite decisions. A leaf must reduce the original formula to contradiction by exact Boolean unit propagation under its decisions.

The independent checker uses functional residual clauses represented by positive/negative integer bit masks and repeated batch-unit elimination, with no watched literals, learned clauses, trail, search heuristic, or producer import. Reusing the parent residual avoids redundant propagation, while every split and leaf remains checked. This differs from the producer's mutable two-watched-literal solver and backtracking trail. Duplicate literals are interpreted as sets and tautological clauses are removed by exact Boolean identities. Metadata must pin the frozen raw CNF hash and its raw variable/clause counts. Nine positive and negative checker controls cover valid unit and split proofs, invalid leaves, satisfiable branches, duplicate and tautological clauses, out-of-range literals, and malformed nodes.

An initial version with Python sets was stopped by its 180-second containment limit, with child and runner exit code 124 after 180.037 seconds. Its run.json is retained under tmp/lab-zeroq-independent-runs/lab-zeroq-independent-tree-audit/20260904T211703Z-7364/. PIDs 7364,25964,36684 were subsequently confirmed absent. That attempt is inconclusive. The coordinator authorized one optimized bitmask run capped at 600 seconds and 2048 MiB; it uses the same exact proof semantics and retains the failed attempt's receipt.

No native UNSAT assertion, empty DRAT file, or crashed process is accepted as proof.

## Final accepted certificate receipt

The optimized independent checker completed with exit code zero. Its complete traversal accepted 6860 internal binary nodes and 6861 unit-propagation conflict leaves. The exact certificate SHA256 is:

    d73b746cbf5bafdcb1ac6e2af9bcac65475e5d7d1595f82cabca25bc8556c1fd

Reproduction:

    python claims/finite/n08/two-root-zero-source-certificate/generate_instance.py --output tmp/two-root-zero-source.cnf
    python tools/research/run_bounded.py --run-id n08-zero-source-audit --timeout-seconds 600 --memory-mb 2048 -- python claims/finite/n08/two-root-zero-source-certificate/check_certificate.py --cnf tmp/two-root-zero-source.cnf --certificate claims/finite/n08/two-root-zero-source-certificate/certificate.json

The successful run receipt and complete stdout are under tmp/lab-zeroq-independent-runs/lab-zeroq-independent-bitmask-audit/20260904T212045Z-22512/. Elapsed time was 88.619 seconds, with both child and runner exit code zero. Runner PID 22512 and child PID 14016 were confirmed absent after completion, and no matching audit command remained. The accepted checker SHA256 is 3fad19ae0bba42e40d9e77c30377da3263943dbdb14f8857f021b6ee0c10d6af. All verifier arithmetic and support logic is exact Boolean/integer computation; no external SAT solver supplies the acceptance verdict.

Thus the frozen necessary support relaxation is UNSAT. The independently audited bridge excludes a hypothetical physical point in the stated pure Q=0 common-coordinate (3,3) branch. Other Q=0 orientations require their own upstream reduction or exclusion, and arbitrary root incidences and global conjecture resolution are outside this audit.
