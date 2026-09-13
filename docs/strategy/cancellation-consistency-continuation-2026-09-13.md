# Cancellation-consistency continuation

**Stopped by the user at 06:32 UTC on September 13.** The final
[wind-down handoff](cancellation-consistency-handoff-2026-09-13.md) supersedes
the earlier persistence instructions and records the newest results and limits.

## Scope and stop rule

This is a research journal, not a resolution claim. The global
Krenn--Gu conjecture remains **UNRESOLVED**. The active checkout is
`codex/recursive-cancellation-consistency-20260912`, starting from local
checkpoint `acbe244771c378a3101a91bfc620d1268fd53356` on upstream
`dc4e7c9ef97e3d4d0d47e1d3403e61d66a498ddc`.

The user authorized sustained work toward resolution until the account
reaches 80 percent usage, followed by graceful wind-down and a handoff.
The live account tool reports `usedPercent`, so the stopping test is
`max(available core-window usedPercent) >= 80`, not 80 percent remaining.
Only a weekly window is currently reported; a missing second window is
unavailable, not zero. Check between bounded experiments and before starting
another substantial run. At the threshold, start no new research lane,
preserve the evidence, stop only owned processes, validate, and hand off.

The initial and subsequent checks through approximately 02:23 UTC on
2026-09-13 report 3 percent used, window length 10,080 minutes, reset Unix
time 1789832898. The value is coarse; no token-to-percentage conversion is
assumed. No reset credits have been used. The rule is a stopping ceiling,
not a target to consume unnecessary resources.

At 02:56:05 UTC the live reported usage advanced to **4 percent used**.
The weekly window and reset timestamp were unchanged; the second window
remained unavailable. This confirms the reading updates during the run.

## Parent and immediate obligations

The scientific parent remains exact weighted Bogdanov: exclude all-diagonal
complex witnesses at every even order at least six. Its downstream scope is
only that any full-model witness must have bichromatic entries. There is
no diagonalization theorem here. The unrestricted eight-vertex r=2,3
branches and the global conjecture remain separate open obligations.

The current attempt tests whether recursive cancellation consistency forces
an impossible signed configuration. A valid all-order result needs an
**occurrence theorem**, not merely more examples of impossible circuits.
The preceding finite n=10 result is in
[the experiment](recursive-cancellation-consistency-experiment-2026-09-12.md).

## Fable review repairs

Fable 5.1 found no blocking mathematical defect in the prior experiment but
identified concrete reproducibility gaps. This continuation implements:

- a typed, exact 13-case manifest cover, including both relaxation flags;
- pinned builder text (CRLF normalized to LF) and python-sat version;
- cross-platform regeneration of each original ASCII/CRLF DIMACS file,
  requiring its exact frozen byte count and hash before checking its proof;
- binary positive and negative checker controls, requiring semantic rejection
  of the false empty step rather than an accidental parser rejection;
- constructive stabilizer permutations for all 945 matchings on ten vertices;
- upstream checker source/build provenance. Recompiling commit
  `2e5e29cb0019d5cfd547d4208dca1b3ec290349f` with
  `gcc drat-trim.c -std=c99 -O2` reproduced the previously pinned executable
  hash `a48ebed7b4b6b373d3ddbeb3368dae7622a9e17bab7fe6eb751ab996757f9fbe`.

The strengthened replay passed in 560.844 seconds: all 13 source regenerations,
all 13 binary proofs, and all three semantic checker controls. Its 32,492-byte
receipt at `tmp/recursive-hafnian-rzp-replay-v2/replay.json` has SHA-256
`3714e6bd534a2043d403834c43dcc0961ca9ba4ab7ca2b12b3e0eaa3e694f6e8`.
The run was bounded by 1,200 seconds, with per-case checker timeouts of 300
seconds. The roughly 500 MB proof payload is still local, not durably published.

## A uniform signed-ratio condition

Fix one colour c and two distinct vertices a,b. Let I be their common
support neighbours. For i in I, define the nonzero ratio

    r_i = Z^c_ai / Z^c_bi.

Define a graph Q on I by putting ij in Q exactly when

    h_c({a,b,i,j}) = 0   and   Z^c_ab Z^c_ij = 0.

**Necessary-condition lemma.** For every actual complex symmetric matrix,
Q is bipartite, at every order and with no degree bound.

**Proof.** The complete four-vertex hafnian fibre is

    Z_ab Z_ij + Z_ai Z_bj + Z_aj Z_bi.

On an edge of Q the first term is zero and the other two are nonzero.
Division by Z_bi Z_bj gives r_i + r_j = 0. Along a walk of length k the
ratio changes by (-1)^k. An odd cycle would give r_i = -r_i, impossible
for nonzero r_i over C. Therefore Q has no odd cycle and is bipartite.
This proves the claim independently of a solver. Conversely, the abstract
ratio equations of this one fixed graph are satisfiable when Q is bipartite:
choose a nonzero base ratio on each component and alternate its sign.
That converse concerns only these ratio equations, not the whole matrix.

The three-binomial 2-by-3 obstruction is its triangle case. The full lemma
also detects arbitrarily long odd cycles with a compact existential parity
encoding. It is a necessary condition, not an all-order exclusion.

### Sound guarded encoding

For each c,{a,b},i introduce an existential parity bit t_i. For each i,j,
let G be the disjunction

    not g_ai or not g_bi or not g_aj or not g_bj
    or s_abij or b_(abij,ab).

The final product variable is truthful and means g_ab AND g_ij. Add

    G or t_i or t_j,
    G or not t_i or not t_j.

When the complete fibre is exactly the two surviving summands of the lemma,
G is false and t_i differs from t_j. Otherwise the graph edge is absent
and the clauses impose no relation. In particular, activating the third
matching monomial is a sound escape. Omitting that escape is false: take
all six cross weights 1, Z_ab=1, and the three right-right weights -2;
all three four-hafnians are then 1+1-2=0.

The clauses are in
`src/krenn_gu/recursive_hafnian_signed_cuts.py`, selected by the probe's
`--signed-common-neighbor` flag. The simpler `--signed-two-by-three` flag
adds triangle clauses only. Neither silently changes the original RZP or AP'.
The pinned n=10 evidence regenerates the original unstrengthened clauses.

The number of parity variables is 3*C(n,2)*(n-2), and the number of clauses
is 6*C(n,2)*C(n-2,2). The triangle-only version has
3*C(n,2)*C(n-2,3) clauses and no new variables.

This is not a license to replace general integer exponent relations by
mod-two linear algebra. Here the special equations are primitive ratio
differences. The existing Smith-form lattice checker independently confirms
the triangle relation d12-d13+d23=0 with odd sign. The regression suite also
checks that x^2=-1 is accepted: it has complex solutions despite a zero
mod-two exponent.

### Strictness controls, not global countermodels

Six exact tests passed for the reviewed parity checkpoint. They include direct integer evaluation of
5,184 weighted patches, the third-term escape, and 20 seeded actual integer
matrix triples at n=6,8 whose exact hafnian supports extend to the parity
encoding. There are also two local strictness tests:

1. On eight vertices, take a K2,3 patch on {0,1} versus {2,3,4}, kill its
   three four-hafnians, and allow every pair incident with {5,6,7}. The local
   RZP recurrence clauses and a nonzero full colour-0 hafnian are satisfiable.
   Adding the one triangle cut makes these fixed local conditions UNSAT.
2. Take K2,5 on {0,1} versus {2,...,6}, with vertex 7 isolated. Declare a
   four-hafnian zero precisely for adjacent pairs of the five-cycle on the
   right, and nonzero on its chords. Local RZP plus every triangle cut is
   satisfiable; the common-neighbour parity clauses make it UNSAT.

Neither test includes the global rainbow axioms. The second has a zero full
hafnian. These are exact countermodels to weaker **local mechanisms**, not
weighted witnesses or Krenn--Gu counterexamples. They establish that the
signed step adds genuine information, including information beyond triangles.

## Bounded parent triage

A 330-second, 8 GiB Glucose run testing n=12 RZP with the three selected
support matchings coincident timed out after 330.046 seconds. Its result is
**UNKNOWN**. This is one branch used to seek a survivor, not an exhaustive
n=12 cover. The matched common-neighbour run also timed out, after 330.034
seconds, so its result is also **UNKNOWN**. No solver-frontier improvement
was established.

The unresolved mathematical question is whether the global two-/three-colour
partition constraints force one of these ratio graphs to be non-bipartite,
or force some more general incompatible cancellation circuit. Passing all
ratio graphs would only direct attention to larger fibres and cross-patch
integer consistency; it would not prove realizability.

## Second Fable review and the closure repair

The read-only Fable 5.1 review completed in 899.234 seconds and found no
blocking defect in the parity lemma, guards, v2 replay, or stabilizer test.
It reviewed the material checkpointed as
`540cf9407b5a14048b9c8b9f3909f5bc2876dcb4`. It executed no code or proof replay.
Its raw report remains local under `.research-runs/`; the 12,034-byte log has
SHA-256 `cf60c5314d0c008744176719afdfbc67e9138e8240ce09b8663751f02a63cad9`.
The raw model report is not committed or treated as proof.

The most useful finding was missing path closure. A path of ratio-negation
edges forces alternating ratios even when it contains no odd cycle. For
example, on common neighbours 2,3,4,5, the three zero fibres along
2-3-4-5 force r_2=-r_5. With a dead third term, declaring the endpoint fibre
nonzero is impossible although the earlier parity graph was bipartite.

The locally checked repair goes slightly further than that suggestion.
Whenever the path forces r_i=-r_j, the cross sum vanishes and

    h_c(abij) = Z^c_ab Z^c_ij,  hence  s_abij = b_(abij,ab).

Thus a **live** third term forces a nonzero endpoint hafnian; it is not an
unconditional escape after the cross sum has been proved zero. Two exact
local controls, with dead and live third terms respectively, pass RZP plus
the old parity clauses and fail the new closure clauses.

### Complete zero-pattern condition for one fixed pair

Restrict to common neighbours I and let s_ij denote the four-hafnian support
and b_ij its third-term support. The possible pairs are:

| b_ij | s_ij | required ratio relation |
| --- | --- | --- |
| 0 | 0 | r_i = -r_j |
| 0 | 1 | r_i != -r_j |
| 1 | 0 | r_i != -r_j |
| 1 | 1 | no ratio condition |

Form Q from the first row. The one-pair pattern is realizable over C exactly
when Q is bipartite and no pair from the middle two rows joins opposite
sides of one Q-component. Necessity follows from alternating ratios and the
complete three-term four-hafnian identity. For sufficiency, choose a distinct
nonzero base ratio, distinct up to sign, on every component and alternate
it according to the bipartition. Choose all Z_bi=1 and Z_ai=r_i. If Z_ab is
nonzero normalize it to 1; choose a live Z_ij to cancel the nonzero cross sum
when s_ij=0, and otherwise choose it nonzero avoiding the one cancelling
value. If Z_ab=0, every b_ij=0 and the right-right weights do not affect these
fibres. This constructs the requested support pattern on this one patch.

The new `--signed-ratio-closure` option includes parity and adds existential
component-equivalence variables. Three clauses per neighbour triple enforce
transitivity, zero/dead-third fibres put their endpoints in the same
component, and connected opposite-parity endpoints force s_ij=b_ij.
There are 3*C(n,2)*C(n-2,2) new component variables and
3*C(n,2)*(3*C(n-2,3)+5*C(n-2,2)) closure clauses, besides parity.

An independent constructive graph checker classifies all 4^6=4096 patterns
on four common neighbours. For every accepted pattern it explicitly builds
integer weights and checks the four-hafnians; the incremental SAT encoder
agrees on every accepted and rejected pattern. The existing seeded actual
matrix controls also pass with closure enabled. Eight signed-cut tests now
pass. This establishes local completeness for a fixed pair's tested common-
neighbour fibres, not simultaneous realizability across different pairs,
larger subsets, or colours.

Fable also suggested a source-dependent Gram formula for larger fibres.
The formula is correct off the diagonal, but any resulting rank statement
requires a **diagonal completion**: its Gram diagonal is not a principal
hafnian coefficient supplied by the witness. No hollow-matrix rank claim
or global consumer is assumed here.

### Sharper occurrence question along an active pair

If ab is active in colour d, exclusivity gives Z^c_ab=0 for c!=d. Inside the
nonzero cofactor h_d(V-ab), let E_d^(ab) consist of ij with both Z^d_ij and
h_d(V-abij) nonzero. Laplace gives this graph minimum degree at least one.
For i,j that are also common colour-c neighbours of a,b, the two-part
equation forces h_c(abij)=0. The third term is absent, so these are unguarded
ratio-negation edges. An odd cycle in the **induced common-neighbour graph**
would be impossible. An even-length path within that graph forces its
endpoint colour-c four-hafnian nonzero and hence the complementary hafnians
of both other colours zero. Paths leaving the common-neighbour set do not
support this ratio argument.

Proving that every hypothetical witness forces an odd cycle, or an
inconsistent sequence of these cofactor implications, remains the actual
occurrence obligation. Neither Fable nor the local checks prove it.

## Source controls and a closed diagnostic family

[The source-reduction controls](hafnian-source-reduction-countercontrols-2026-09-13.md)
give actual integer matrices disproving three tempting unqualified premises:
active edges need not have a perfect matching even in a bipartite source;
nonzero principal-hafnian supports need not satisfy symmetric exchange;
and naive rank-two pair contraction introduces extra matchings. The first
two countercontrols extend to all orders by isolated unit-weight pairs.
They are not three-colour witnesses.

The dense-private fixed-support n=12 and n=14 probes both collapsed by unit
propagation. [A four-vertex cofactor argument](four-vertex-cofactor-coverage-2026-09-13.md)
now explains this at every order, for every triple of disjoint private
matchings satisfying the stated dense-support hypotheses. Its local graph
counting is exhaustively checked. The written proof is independent of the
finite solver results but awaits separate review; it is not a general
all-diagonal theorem or a frontier promotion. Further orders of that
diagnostic family are unnecessary.

The closure extension, source controls, and coverage proof were developed
after Fable's reviewed checkpoint. Do not attribute independent review of
those later changes to that report.

The coverage argument also supplies 27*C(n,4) short clauses already implied
by full RZP and the global partition axioms. They forbid a live (n-4)-cofactor
when both other colour supports match its complementary four-set. The
`--four-cofactor-coverage` option is a redundant proof shortcut, unlike the
strict signed-ratio strengthening. The matched n=12 shared-branch probe with
ratio closure and these shortcuts also timed out, after 330.028 seconds.
All three bounded shared-branch variants therefore remain UNKNOWN. No
further run on that branch is justified merely by extending its deadline.

At this checkpoint the focused suite has 30 passing tests, and the migration
and existing integer-lattice suites have 205 passing tests. The complete
candidate-index hygiene and link-rewrite gates pass. The new source and
proof material remains local; the full conjecture is unresolved.

## General binomial loop beyond four-fibres

[The recursive binomial module](recursive-laplace-binomial-circuits-2026-09-13.md)
now extracts complete zero/two-term and nonzero/one-term Laplace fibres,
checks their integer exponent lattice, replays a contradictory integer
dependency, and emits a cut guarded by every term of each used expansion.
A local eight-vertex theta pattern passes RZP and complete four-fibre
consistency but is excluded by a nine-relation integer certificate and one
40-literal guarded cut. An actual integer-weight specialization on the same
graph escapes the cut when the formerly forced third zero is allowed to
be nonzero. This tests the general loop without claiming a global survivor.

Twenty sampled fourteen-vertex four-cycle-free cubic support triples all
returned UNSAT without solver branching. This is bounded diagnostic evidence,
not an exhaustive exclusion. There is still no full RZP survivor on which the
binomial loop has been load-bearing. The conditional longer-path obstruction
and its occurrence requirement are stated separately in the linked note.

## Full-model source-cancellation checkpoint, 04:22 UTC

The live core usage meter reached 5% used at 03:59 UTC and remained 5% at 04:20
UTC. The user-directed 80% wind-down threshold has not been reached. The global
goal remains active; no reset credit has been consumed. Remote main was checked
again and remains at the same base commit; this work is local and unpublished.

The separate full-model n8 parent diagnostic now has two source-coupled
mechanisms beyond the first full-word quotient cuts: complete coloured
four-fibre ratio components, and lifted sparse circuits among original subset
Laplace identities. A deterministic test suggested by Fable derives three
forced four-coefficient zeros from one physical support, yielding a 24-step,
three-binomial certificate and a 57-literal physical support cut. Details and
evidence boundaries are in
[the source-cancellation mechanism note](source-cancellation-mechanisms-2026-09-13.md).

This is not an eight-vertex exclusion. It is a successful source-level test of
the cancellation-consistency regime, with the global occurrence theorem still
open. Fable found no blocker in the earlier full-word encoder/quotient delta;
the newest three implementations postdate that review and are not represented
as independently reviewed.

## Checkpoint continuation, 05:16 UTC

Live core usage first reached 6% at 04:32 UTC and is now **7% used** at
05:16:44 UTC. The only reported core window is still weekly; the 80% wind-down
threshold is not reached. No new task, publication, or reset-credit action was
taken. The exact-resolution goal remains active.

The original 136-entry support can escape the first recursive circuit by
changing cofactor supports. A larger-sum recursive quotient then supplies a
seven-binomial transport contradiction. Its one learned clause closes the
fixed physical support even without ratio constraints. A checked native DRAT
trace and a separate 264-clause/three-RUP-addition core replay lift this to a
54-literal physical support cut. The compact core is preserved as a regression
certificate with a replay path that does not require a SAT executable.

The [mechanism note](source-cancellation-mechanisms-2026-09-13.md) records the
proof bridge, its exact scope, and negative balance/linear-algebra controls.
This is still a conditional source-support exclusion, not an exhaustive n8
cover or a uniform occurrence theorem. The live frontier is unchanged for
that reason. The newly implemented quotient/core deltas postdate Fable's third
review, and that earlier review is not attributed to them.

At checkpoint `e45d289d`, all 63 focused tests, all 205 migration/lattice tests,
complete-index hygiene, and the no-change link pass were green. The next
source-projection test produced a second replayed physical cut (38 literals),
with only a 200-clause unit-propagation core. The full symmetry orbits of both
physical cuts still leave a checked 135-entry Boolean support at n8. This
negative parent-coverage test, not another catalogue of cofactor assignments,
defines the current gap. The second compact core is retained as another
regression fixture of the same mechanism.

The additional Fable review of `e45d289d` timed out at its 12-minute CLI deadline
on 2026-09-13 at 05:39 UTC and returned no review verdict. All owned research
processes from that attempt and the full-orbit probe have exited. The live usage
meter remained 7% used at 05:33 UTC; the global goal and 80% stop rule remain
active. There has been no global-status promotion or publication.
