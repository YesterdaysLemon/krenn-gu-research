# Hostile review: minimal pure-cofactor ports and conformal fans

Date: 2026-08-11

Reviewed artifact:

[`../../claims/arbitrary-order/MATRIX_UNIT_MINIMAL_PURE_COFACTOR_PORT_AGGREGATE_AND_CONFORMAL_FAN_REDUCTION_THEOREM.md`](../../claims/arbitrary-order/MATRIX_UNIT_MINIMAL_PURE_COFACTOR_PORT_AGGREGATE_AND_CONFORMAL_FAN_REDUCTION_THEOREM.md)

Review disposition: **PASS at the stated least-residual structural and
sharpness scope**.

The Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Exact obligation under review

The imported theorem leaves a least supported pure hafnian cancellation with
a connected matching-covered active core.  Its branching side has at least
one vertex of degree at least three.  The reviewed checkpoint asks what the
complete matching set does at such a vertex.

It claims:

1. perfect matchings partition exactly by their incident root edge, and each
   port sum is the corresponding nonzero first cofactor;
2. at a degree-`d` branch vertex, either all `d` ports are singletons and
   form a conformal alternating fan with one exact `d`-nomial Laurent
   relation, or some port is an unavoidable nonzero aggregate;
3. two exits at one branch vertex carry a conformal theta whose path profile
   is all odd or odd/even/even, with respectively three or two perfect
   matchings on the theta edge set;
4. the old branching-excess alternative becomes one high-valence local fan
   or at least two cubic local fans, always retaining the sparse/aggregate
   split; and
5. exact rational least-residual families realize every sparse arity, both
   cubic theta profiles, and the aggregate-port branch.

It does not claim that a pure fan is a deeper blocker, that a pure aggregate
port is an aggregate mixed-word fibre, or that any sharpness family is a
matrix-unit witness.

## 2. Adversarial proof checks

### 2.1 Does the cofactor equal the complete port sum?

Yes.  Multiplying the matching expansion of
`haf(R-{v,w})` by `z_vw` gives every support perfect matching containing
`vw`, exactly once.  Conversely, deleting `vw` from any full matching gives
one complementary matching.  The imported allowed-core identity guarantees
that no full matching is lost by writing the matching set as `PM(G)`.

### 2.2 Why is every port nonempty and nonzero?

Matching-coveredness makes every incident edge belong to a perfect matching,
so every port is nonempty.  Nonemptiness alone would not prevent cancellation
inside a multi-term port.  The stronger nonzero conclusion uses the imported
least-residual identity `G={e:C_e!=0}`.  The reviewed theorem preserves that
dependency explicitly.

### 2.3 Is the sparse/aggregate alternative exhaustive?

Yes.  The `N` perfect matchings are partitioned into `d` nonempty ports.  If
`N=d`, every port has size one.  If `N>d`, pigeonhole gives a port of size at
least two.  No genericity assumption or choice of reference matching enters
this count.

### 2.4 Why does a sparse port matching differ by only one cycle?

Compare the unique matching in a nonreference port with the reference
matching.  Their symmetric difference contains an alternating cycle through
the root.  Toggling only that component is already a full perfect matching
in the same port.  Port uniqueness forces it to be the selected matching.
Any additional disjoint exchange component would produce a second matching
in that port.  Thus the normalized ratio is one alternating-cycle Laurent
character, not an uncontrolled product of cycles.

### 2.5 Is division in the Laurent relation legitimate?

Yes.  The denominator is the monomial of a support perfect matching.  Every
edge in that matching has nonzero scalar weight.  No cofactor sum, aggregate
remainder, or possibly vanishing polynomial is divided out.

### 2.6 Why is the exchange fan conformal?

Every selected alternating cycle contains the reference `P`-edge at each of
its vertices.  Their union is therefore closed under `P`-mates.  The
restriction of `P` matches the fan vertices, and the complementary
restriction matches every vertex outside the fan.  This proves conformality.
It does not prove that the fan is induced, and the theorem makes no such
claim.

### 2.7 Does the first-return construction really give a theta?

Start down one alternating cycle through its selected nonmatching exit and
stop at the first subsequent vertex on the other cycle.  The initial path
has interior disjoint from the base cycle.  The base cycle has two internally
disjoint paths between the same endpoints.  Their union is exactly a theta
subdivision containing the reference edge and the two selected exits.

### 2.8 Is the theta itself conformal?

Yes.  Internal vertices of the first-return path contain their reference
matching edge on that path.  Both endpoints have their reference matching
edge on the base cycle.  Hence the theta vertex set is closed under the
reference matching.  Again this is a conformal subgraph, not necessarily an
induced subgraph.

### 2.9 Why must the first-return path be odd?

It starts with a nonmatching edge.  If its final edge were the matching edge
at the return vertex, the preceding vertex would already be on the
alternating base cycle, contradicting first return.  Thus it ends with a
nonmatching edge and has odd length.  The two arcs of the even base cycle
have equal parity.

### 2.10 Are there only two theta profiles and are the counts correct?

Yes.  The first path is odd; the two base arcs are both odd or both even.
On an odd endpoint path a perfect matching uses both endpoints or neither;
on an even endpoint path it uses exactly one.  Three odd paths give exactly
three choices for the path using both endpoints.  One odd and two even paths
give exactly the two opposite endpoint assignments to the even paths.  In
the latter case the root edge of the odd path occurs in no theta matching.

### 2.11 Does the open-port profile contradict global allowedness?

No.  It says only that one root edge is forbidden inside the extracted theta
edge set.  The larger alternating cycle used to construct the theta supplies
an exterior completion.  The `K_4` sharpness model exhibits this distinction
exactly: the five-edge theta has two matchings, while its missing sixth edge
completes the third root port in the full fan.

### 2.12 Is the arbitrary-arity theta family really least supported?

Yes.  In `Theta_d`, a full matching chooses exactly one route for both
endpoints and uses every other route's middle edge.  Its `d` matching weights
are `1,...,1,-(d-1)`, whose full sum is zero and whose proper subsums are
nonzero.

For a principal subset, absence of one or both endpoints or the presence of
unpaired internal vertices leaves at most one support matching.  The only
multi-matching subsets contain both endpoints and complete internal pairs
from a route set `I`; their hafnian is the corresponding subsum.  Therefore
the full vertex set is the unique supported zero of least size.  The proof is
characteristic-zero exact; it is not silently asserted in characteristics
dividing `d-1`.

### 2.13 Is the aggregate example genuinely least supported?

Yes.  In the weighted `K_(3,3)`, the six full matching weights sum to zero.
A proper supported even subset has order two or four.  Order-two hafnians are
nonzero edge weights.  Every supported order-four subset is a `2 by 2`
minor with permanent `2` or `-1`.  Thus no smaller supported cancellation
exists.  The three root cofactors are the nonzero two-term sums `-4,2,2`.

### 2.14 Does this enter the deeper-blocker branch?

No.  Deeper-blocker theorems require root/killer and bridge-incidence data
not encoded by a pure matching-covered graph or its matching weights.  The
sharpness families show that the pure structures are internally consistent.
Calling them deeper blockers would silently add hypotheses and was rejected.

### 2.15 Does this close the pure-cofactor exit?

No.  It replaces the branch case by sparse fan characters or a nonzero
aggregate port and proves that both occur.  A contradiction still requires
mixed target coupling, aggregate control, or genuine deeper incidence.  The
checkpoint is a structural reduction and method boundary, not an exclusion.

## 3. Evidence independence

The primary verifier uses tuple-recursive perfect matchings and exact
`Fraction` hafnians.  It checks:

- sparse `Theta_d` residuals for `d=3,4,5`;
- least-residual selection over every principal subset;
- singleton port partitions and normalized cycle-character sums;
- explicit alternating-cycle fans and an all-odd theta;
- the `K_4` odd/even/even theta and its exterior port completion; and
- the weighted `K_(3,3)` aggregate port values.

The independent audit imports no repository module.  It enumerates disjoint
edge masks rather than recursing on the first vertex, classifies every
principal theta subset by endpoint/internal route states, audits separate
abstract theta lengths, and computes the bipartite aggregate example by
permutation sums and all `2 by 2` permanents.  It tests sparse arities through
`d=6` with different traversal logic from the primary verifier.

The bounded scripts audit the formulas and sharpness mechanisms.  The
arbitrary-order theorem rests on the written port partition, alternating
toggle, conformal closure, and first-return parity arguments.

## 4. Remaining boundary

The checkpoint leaves open:

- coupling a sparse pure fan character to a complete mixed target equation;
- controlling the extra monomials in a nonzero aggregate pure port;
- proving that either theta profile supplies root/killer data for a deeper
  blocker;
- combining the primitive pure-cycle branch with mixed response;
- aggregate active-cycle fibres and rank-at-least-two target quotients;
- exclusion of the complete nonzero `r=1` matrix-unit branch; and
- the global conjecture.

The arbitrary-arity sparse family closes only the attempted inference
"branching arity or a conformal fan is already contradictory."  The examples
are not full physical tables and do not refute Krenn--Gu.

## 5. Verdict

The theorem is accepted as an exact arbitrary-order refinement of the live
pure-cofactor branching edge.  It identifies the load-bearing next datum:
either aggregate port control or an external mixed/deeper coupling.  Its
sharpness families establish a genuine wall for arguments using only branch
degree, alternating-fan topology, or the local sparse Laurent sum.

The global Krenn--Gu conjecture remains **UNRESOLVED**.
