# From full-word cancellation to forced subcoefficient circuits

Global Krenn--Gu status: **UNRESOLVED**. This note continues the
[full-model parent attempt](full-model-recursive-cancellation-attempt-2026-09-13.md).
It records reusable conditional mechanisms and scoped diagnostics, not an
exhaustive finite exclusion. No live-frontier promotion is made.

## A human form of the full-word quotient cuts

Fable's independent read-only review found no blocking defect in the encoder,
integer quotient, or complete-fibre cut chain, and checked the arithmetic of
three displayed certificates. It did not execute code, replay the SAT evidence,
or verify the Smith implementation. The review suggested the following useful
description of those examples, which is also immediate by direct factorization.

Let M and N be distinct perfect matchings. Let P and Q be disjoint nonempty
sets of vertices, with no edge of the symmetric difference M triangle N joining
P to Q. Independently change the colours on P and Q to form four words w_ab,
a,b in {0,1}. Suppose both matching monomials remain nonzero at all four words.
Their ratio rho=m_M/m_N obeys

```text
rho(w_00) rho(w_11) = rho(w_10) rho(w_01).
```

Indeed, common matching edges cancel from the ratio. Every remaining edge factor
depends on the P choice or the Q choice, never both. Thus rho=constant*F(a)*G(b).
If three corners are complete two-term mixed fibres, their ratios are -1, so
the fourth ratio is -1 too. The fourth corner cannot then be a pure fibre with
exactly those two terms, or a mixed fibre with precisely one additional live
matching term. This explains both `pure_vanishes` and `quotient_singleton` cuts.

The nonadjacency hypothesis is necessary for the factorization. For example,
M={04,13,25}, N={05,14,23}, P={0}, Q={5} lets the denominator W_05 depend on both
choices. Give its four selected entries values 1,1,1,2 and all other selected
edge factors value 1: the four ratios are 1,1,1,1/2, violating the grid identity.
This is a countercontrol to the factorization without its hypothesis, not a GHZ
witness. Dead fourth-corner terms or two extra terms also invalidate the stated
conclusion. Common matching edges need not satisfy the nonadjacency restriction
because their factors cancel.

This lemma is subsumed by the full-word quotient test. Its occurrence cannot be
forced by the original Boolean recursion plus killers and the full-word quotient
alone: the recorded 107-entry n8 support passes those tests. That does **not**
refute an occurrence theorem using additional exact weight equations.

## General coloured four-coefficient ratios

The earlier scalar-hafnian ratio mechanism extends to arbitrary pair blocks
without diagonalizing them. Fix physical vertices a,b and endpoint colours
alpha,beta. Each slot (i,gamma), i outside {a,b}, carries the nonzero ratio

```text
r_(i,gamma) = W_ai(alpha,gamma) / W_bi(beta,gamma),
```

when both entries are nonzero. Two slots on distinct physical neighbours give
the complete four-coefficient identity

```text
h(a_alpha,b_beta,i_gamma,j_delta)
 = W_ab(alpha,beta) W_ij(gamma,delta)
   + W_ai(alpha,gamma) W_bj(beta,delta)
   + W_aj(alpha,delta) W_bi(beta,gamma).
```

If the result and first product vanish, the ratios are negatives. Such edges
form a bipartite graph. Within a connected component, opposite parity forces
the two cross terms to cancel, so the result support equals the first-product
support. There is no direct four-fibre edge between two colour slots of the
same physical neighbour; their relations may only be transported through other
slots. Every clause is guarded by the four live cross entries.

[The coloured-slot implementation](../../src/krenn_gu/recursive_tensor_ratio_cuts.py)
adds, at n8, 4,536 parity variables and 68,040 clauses. Component closure adds
38,556 variables and 786,996 clauses. Unit tests retain the genuine n4 GHZ,
sixteen integer/Gaussian-integer source controls, and a local sharpness example
that passes recursion but fails the three-ratio triangle.

The old 107-entry support is UNSAT with the parity clauses (solver status only;
no DRAT claim). The unrestricted n8 model with component closure remains SAT:
600,063 variables, 3,680,484 clauses, and a checked assignment with 136 nonzero
physical entries. This is not a physical weight realization.

## A circuit beyond the implemented four-fibre ratio closure

The 136-entry candidate passes the full-word quotient as well. Its chosen
cofactor supports nevertheless admit an exact contradiction among shared
six-vertex coefficients. Sparse integer elimination found it after eliminating
one-term hafnian definitions. Those substitutions were then removed from the
proof: the certificate consists of five **original** complete Laplace identities
(three zero/two-term six-vertex identities and two nonzero/one-term four-vertex
identities). Their integer combination has zero exponent vector and odd sign.

The resulting 26-literal cut guards the result and **every** product-support bit
of those five expansions, including zero terms. It excludes the chosen cofactor
assignment, not yet its entire physical support. Activating an additional term
or changing a guarded result support may escape it.

[The extractor and replay](../../src/krenn_gu/recursive_tensor_binomials.py)
keep the following boundaries explicit:

- one-term substitution uses integral monomial identities, with no root choice;
- sparse elimination is a one-sided discovery method, not a saturated integer
  kernel computation; finding nothing is not a consistency theorem;
- bounds on rows, sparse fill, certificate support and integer bit lengths stop
  growth; external process limits remain required;
- each found circuit is lifted to original unexpanded identities and replayed by
  integer addition and complete-fibre checks, independently of elimination;
- tests cover actual integer sources, complex-torus torsion, a theta circuit
  requiring the one-term lifting, and malformed certificates.

This extends the original cancellation package's local theta calibration into
an actual full-model Boolean survivor. It does not supply the missing global
occurrence theorem.

## Fable's proposed deterministic test, and its outcome

Fable recommended deriving exact zero/nonzero subcoefficient facts from physical
support and the GHZ target, then reusing them. This is important: freely chosen
Boolean proper-coefficient zeros cannot be treated as unconditional equations
of the physical support. The guarded recursive cut above does not do so.

We tested that recommendation on the **107-entry** support, without another SAT
search. Start with physical entries' support and the full target coefficients.
For every Laplace expansion use only these necessary rules:

- a nonzero result cannot have no live term;
- a zero result cannot have exactly one live term;
- if all but one possible term are zero, propagate the result's support to that
  cofactor (the incident entry is known nonzero);
- if a zero result has one known live term and one remaining unknown term, the
  latter must be live too; fully determined zero/one-term sums determine their
  result supports.

The monotone closure stops after six scans with 29,260 facts, including 22,447
new facts. Among proper coefficients it determines:

| Size | Forced zero | Forced nonzero | Still unknown |
| --- | ---: | ---: | ---: |
| 4 | 3,021 | 2,412 | 237 |
| 6 | 7,208 | 9,806 | 3,398 |

Nineteen distinct complete two-matching binomials come from the forced zero
coefficients. Three already give an odd integer circuit. They concern the
colour-labelled four-sets

```text
(0,1,2,3) : (2,0,0,2)
(0,1,3,6) : (2,0,2,0)
(1,2,3,6) : (0,0,2,0).
```

These are the three opposite-ratio equations between roots (1,0),(3,2) and
neighbour slots (0,2),(2,0),(6,0). Their zeros are forced, not chosen. No
crossing-fibre reuse stage was needed on this support: the test succeeded at
the peeling-plus-forced-binomial stage.

Pruning the derivation to those three zeros leaves 24 steps. The
[standalone checker](../../src/krenn_gu/source_coefficient_peeling.py) verifies
each step by a finite local truth table of the necessary Laplace support rule,
using only earlier facts or the original GHZ/entry premises. It then enumerates
the three complete induced matching fibres and adds their exponent rows with
coefficients (1,-1,1). No solver or Smith decomposition is used in replay.
The certificate yields a **57-literal physical-entry support cut**. Thus it
excludes that physical support, unlike a cut conditional on chosen cofactors.

Tests reject forged/missing parents, missing derivations, changed facts,
coefficients, and guards; they reject null or Boolean fact values masquerading
as typed integer facts. Flipping sampled unguarded physical entries leaves the
replay valid, checking that no hidden source premise escaped the guard. The
known n4 GHZ is retained. This is a source-level conditional obstruction, not
exhaustive eight-vertex coverage.

## Review, resources, and remaining obligation

Fable's third report completed in 870.355 seconds. It reviewed the committed
full-word encoder/quotient delta, not the later coloured-slot, sparse-recursive,
or peeling implementations. Those later deltas have local exact tests but no
separate external review yet. The report's dense-core discussion and estimated
gauge dimension were not imported as theorems; nonzero entries alone do not
make edge-times-cofactor terms nonzero. Its reported block census was not used
as a proof premise.

Raw report: ignored research run
`fable51-full-recursive-cancellation-review-20260913/20260913T035303Z-25988`.
The report is 11,973 bytes with SHA-256
`af2ab6fe5d710544301758cd76fbb2b666ccb68920ac85c426e47d996b14bfe0`.
No raw model report is committed.

The 12-step six-vertex quotient loop ended at its iteration limit; the n8 loop
stopped on its second support. Later experiments were bounded single-support
tests, not an expanded chart census. Original-source circuit and peeling
certificates are retained under ignored `tmp/`; they are not publicly packaged.

The next load-bearing question is whether every full-model support must force
a reusable exact subcoefficient obstruction, or whether a support survives all
these tests and requires genuinely larger cancellation equations. A catalogue
of successful cuts does not answer that occurrence question. Global resolution
still requires a proved exhaustive implication or an exact counterexample and
the repository's dedicated resolution audit.

## Larger recursive sums, and a checked physical-support cut

The next experiment found an important escape from the five-equation circuit:
the same 136-entry physical support admits a different Boolean cofactor
assignment passing the recursive circuit search. It also passes the full-word
quotient test. Thus the earlier circuit did not by itself exclude that support.

The [recursive quotient extension](../../src/krenn_gu/recursive_tensor_quotient.py)
now transports binomial equalities through **all** recursive cancellation sums.
Write each zero/two-term or nonzero/one-term original Laplace equation as
X^r=(-1)^b, using the nonzero physical entries and nonzero subset coefficients
as shared variables X. A larger Laplace equation has the form

```text
sum_j a_j X^m_j = 0,
```

where the result coefficient, when nonzero, appears as one term with a minus
sign. If m_i-m_j is an integer combination of the binomial rows, their monomials
are equal up to the transported sign. Partition all terms by these checked
relations. If exactly one group's signed coefficient sum remains nonzero, the
equation is impossible on the complex torus. No choice of independent local
hafnians is made: each relation and target sum is an original source identity.

Discovery uses only exponent pivots +1 and -1, so each eliminated variable is
an exact signed Laurent monomial. It never divides an exponent by a nonunit or
chooses roots. Nonunit residual relations are reported and left unused; absence
of an obstruction is not a realization claim or a complete lattice verdict.
The standalone certificate checker does not run this elimination: it rederives
the complete original fibres, adds integer exponent rows, checks signs and the
full term partition, and recomputes every guard. Actual integer-source and n4
GHZ controls are retained, and malformed transport/partition tests are rejected.

On the second cofactor assignment of the 136-entry support, 21,050 selected
original binomial rows have 16,008 unit pivots and no residual nonunit rows.
Their binomial system has no discovered sign contradiction. Nevertheless seven
of those equations imply

```text
h((0,3,5,7); (0,0,2,1)) = W_07(0,1) W_35(0,2).
```

The complete four-coefficient equation on this support is

```text
h((0,3,5,7); (0,0,2,1))
 = W_05(0,2) W_37(0,1) + W_07(0,1) W_35(0,2),
```

with both displayed products nonzero. Hence a nonzero product would have to
vanish. The resulting **52-literal recursive cut** uses four full-word, two
six-vertex and one four-vertex binomial relations, plus this target four-fibre.
It guards every result and every product support in all eight expansions.

Adding this cut makes the **fixed physical support** UNSAT even with the ratio
clauses removed. The native CaDiCaL 1.7.3 binary DRAT proof was checked by the
previously pinned drat-trim build. The checker reported `s VERIFIED`, with zero
RAT lemmas in its core. Backward-mode warnings about ignored unit deletions do
not supply the acceptance criterion; the exact success line and exit code do.
The 86,551,013-byte CNF has SHA-256
`40d3fe92b7dd719639b5bba51ce5136b22be4996809af0e564749d0b1911387f`;
the 2,282,566-byte proof has SHA-256
`0e8513081ea6631f2a256e5e7b8964bf800042f6eb5424fcaebaae6d6a6288f9`.

More usefully, the proof trims to 264 premises and three RUP additions. A
[small separate replay](../../src/krenn_gu/source_quotient_core.py) checks:

- 209 premises belong to the regenerated recursive/target encoder;
- 54 premises are explicit physical-entry support units;
- the remaining premise is the independently replayed algebraic clause;
- each of the three additions is justified by plain unit propagation after
  negating that addition, and the last addition is the empty clause.

No killer, root-symmetry, or ratio clause is used. This gives a **54-literal
physical-entry cut**, valid for actual eight-vertex witnesses, not merely the
chosen cofactor assignment. The compact
[regression certificate](../../tests/fixtures/recursive_source_quotient_n8_core.json)
is tracked; it is a conditional support exclusion, not raw solver status and
not an exhaustive eight-vertex cover. Its coefficient template describes the
conditional algebraic clause only; it is explicitly not a physical witness or
a model of the whole recursive CNF.

Replay without a SAT executable:

```powershell
python tools/explore/replay_recursive_source_quotient_core.py tests/fixtures/recursive_source_quotient_n8_core.json
python -m unittest -v tests.test_recursive_tensor_quotient tests.test_source_quotient_core
```

Simple source peeling alone does not supply all the algebraic guards: two
six-coefficient nonzero facts remain undecided. The RUP bridge, rather than an
unproved promotion of those facts, is what lifts this conditional algebra to
the physical support. These later implementations have local exact replay and
controls, but have not yet received a separate external-model review.

## Negative controls on further shortcuts

The 136-entry support also passes a strict colour-slot balance test. For every
active entry an exact perfect matching in the bipartite double cover was found;
summing those covers gives positive integral entry multiplicities with load
272 at every one of the 24 colour slots. This is incidence balance only, not
physical amplitudes or phases. The existing matrix-unit diagonal-torus balance
theorem explains the candidate normal-form idea; no new balance theorem is
promoted, and no entry of this support is removed by that diagnostic.

A six-vertex, 51-entry Boolean survivor passes the implemented ratio, recursive
binomial, full-word quotient, and recursive unit-quotient tests. It is not a
weight witness. An exact localized polynomial scout excludes it: 15 independent
colour-slot gauge columns can be set to one, leaving 36 nonzero variables.
This general diagonal gauge preserves the mixed zero equations, though it may
rescale the pure coefficients; no target-preserving gauge claim is used.
Thirty mixed-word equations lead to 1=0 through a 740-node arithmetic DAG.
A separate SymPy-polynomial replay reconstructs the source hafnians by a
last-vertex recurrence and verifies all additions, monomial multiplications and
exact divisions. The scout and DAG remain ignored local artifacts at
`tmp/full-n6-laurent-spair-scout.json` and
`tmp/replay_laurent_polynomial_dag.py`; they are not a six-vertex case cover.

The analogous eight-vertex polynomial scout hit its 240-second limit, so its
outcome is UNKNOWN. An earlier exact linear-equation scout on that support had
112 variables after a 24-column gauge, 6,558 distinct cubic/quartic equations,
and no initially linear equation; it did not perform a full ideal elimination.
These limitations motivate the cheaper shared-coefficient quotient test above,
not an inference that a surviving support has actual weights.

## Bounded global feedback and the remaining projection gap

A global n8 run seeded with the checked 54-literal cut and all implemented
four-fibre ratio closure clauses completed eight iterations in 116.581 seconds.
Each candidate assignment was checked against every current clause. All eight
had the **same** 134-entry physical support (the serialized first-252-literal
assignment hash is `ddd9d53f6edf24bca717c062dbde723a5c73d109339ef2d2470aef420571b738`).
The recursive circuit cuts changed its cofactor assignments, not its physical
support. The result is ITERATION_LIMIT, not UNSAT or a surviving weight model.

A separate exact finite orbit check tested all 8!*3!=241,920 vertex/global-colour
relabelings of the 54-literal physical cut. None excludes this 134-entry support.
This is a diagnostic limit on that one certified support pattern, not on the
underlying quotient mechanism or the full conjecture. The sharper obligation
is now to project source-coupled cofactor contradictions back to physical
support efficiently, or derive a uniform occurrence theorem. Merely appending
another long sequence of cofactor-assignment cuts does not settle it.

### Projecting the next source, rather than counting more assignments

Fixing that 134-entry support, retaining the eight already checked recursive
cuts, and re-solving its cofactors gives one larger-sum quotient contradiction
in 14.040 seconds. Nine original binomial relations force the **same target
four-coefficient equality** displayed above, through different intermediate
hafnians. Their guarded clause has 64 literals. A separate check then shows
that this one new clause suffices: none of the preceding eight circuit cuts,
the first physical cut, killers, or ratio clauses is needed to exclude the
fixed source.

The native DRAT proof passes replay. Its core has 161 recursive/target clauses,
38 physical support units, and the one algebraic clause. Plain unit propagation
already contradicts these 200 premises, so the separate source-core checker
needs only the final empty-clause addition. The
[second compact regression packet](../../tests/fixtures/recursive_source_quotient_n8_second_core.json)
preserves that **38-literal physical cut**. Its original ignored packet has
SHA-256 `37cac03c9a3176afe14efdc6e1d6b5d4d0e4514fa265184c8a05efdc3d75a2ae`.
The CNF and native proof hashes are respectively
`8edc0b4079a25c025ca10971f863ab23c81e638cb856e580b0a5072d2fb2803a`
and `53dd986036c685810792fd160aab410f7a0723ce98ec3a4f5568c3262a6a7708`.

This is a second test of the same projection mechanism, not a new theorem lane.
To test its parent coverage directly, the next run added every vertex/global-
colour relabeling of both physical cuts: 241,920 instances per cut, including
possible duplicate clauses. The full recursive/killer/ratio-closure model then
has 600,063 variables and 4,164,324 clauses. It remains SAT, with every clause
checked, in 33.625 seconds. The new **135-entry** support and assignment are
retained at `tmp/full-n8-two-source-cut-full-orbits/`. They are not weights.
Thus even the full symmetry closure of these two source obstructions does not
cover the eight-vertex parent. No such cover or global resolution is claimed.

### Additional review attempt

A single read-only Fable 5.1 audit of checkpoint `e45d289d` was attempted through
OMP with a 12-minute CLI deadline and a 13-minute outer process bound. It exited
after 721.127 seconds with `Deadline exceeded`, without a final review report.
It supplies **no review verdict**. The three earlier completed Fable reports
retain exactly their previously stated scopes; none is extended to the new
quotient/core implementation by this failed attempt. The owned process exited,
and the other user's older OMP processes were left untouched.
