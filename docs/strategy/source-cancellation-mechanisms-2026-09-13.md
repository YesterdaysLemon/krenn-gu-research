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
