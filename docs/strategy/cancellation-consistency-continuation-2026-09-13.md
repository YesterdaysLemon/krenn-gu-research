# Cancellation-consistency continuation

## Scope and stop rule

This is an active research journal, not a resolution claim. The global
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

Six exact tests currently pass. They include direct integer evaluation of
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
n=12 cover. A matched run with the common-neighbour condition is running;
no solver-frontier improvement is presumed.

The unresolved mathematical question is whether the global two-/three-colour
partition constraints force one of these ratio graphs to be non-bipartite,
or force some more general incompatible cancellation circuit. Passing all
ratio graphs would only direct attention to larger fibres and cross-patch
integer consistency; it would not prove realizability.
