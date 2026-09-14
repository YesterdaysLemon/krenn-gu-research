# Recursive Laplace binomials and guarded integer circuits

This implements the cancellation-discovery loop on a strictly local
calibration example. It is not a global RZP countermodel, weighted witness,
or Krenn--Gu resolution. The global status remains **UNRESOLVED**.

## Exact extraction

For every colour, even subset A, and expansion vertex v, recompute all live
terms Z_vu h(A-vu) from the edge and cofactor supports. Do not treat the
Boolean product indicator as an independent numerical variable. Then:

- a zero result with exactly two live terms supplies their ratio = -1;
- a nonzero result with exactly one live term supplies h(A)/term = 1.

Both are Laurent monomial equations in nonzero edge weights and subset
hafnians. The two-element hafnian is the edge weight itself, and the empty
hafnian is 1. Duplicate equations are merged; complete expansion origins
are retained. Every potential term was inspected before calling the fibre
binomial. Larger live sums are left open, not discarded as if satisfied.

For exponent rows d_j and sign bits epsilon_j, an integer vector k with

    sum_j k_j d_j = 0,     sum_j k_j epsilon_j odd

gives 1=-1. The implementation uses the existing Smith-form integer-lattice
module to find k, then replays those two identities by direct integer
arithmetic without trusting the decomposition. The default dense calculation
is capped at 256 relations and 256 numeric variables. Larger inputs need
bounded component or circuit extraction, not an uncapped Smith matrix.

The implementation is `src/krenn_gu/recursive_hafnian_binomials.py`.
`extract_recursive_binomials` checks local recurrence support consistency;
it does not assert the global H1/H2 conditions. `find_integer_circuit`
returning None means only that the extracted binomials are consistent,
not that all remaining hafnian equations are realizable.

## Turning a circuit into a sound support cut

For each used equation choose one of its complete Laplace origins. Guard
the result-support bit and **every** incident product-support bit at that
origin, including the bits of zero terms. The conjunction of those guards
would force the impossible integer circuit, so negate it to obtain a CNF
clause. The helper re-derives the origin equations and checks truthful
product guards before emitting that clause.

Consequently a support can escape by losing a live term, changing the
result support, or introducing another cancellation term. Merely banning
the two displayed matching monomials would not have this property and
would be unsound. Negative tests reject modified integer certificates and
incomplete or contradictory support assignments.

## A longer-path obstruction invisible to four-fibre ratios

Take the induced theta support on eight vertices with three paths

    0-2-3-1,    0-4-5-1,    0-6-7-1.

All nine path edges are nonzero; all other colour-0 edges are zero.
Declare the six-hafnian on each pair of paths zero, and the full eight-
hafnian nonzero. The local recursive clauses admit this assignment.
So do all the complete four-fibre ratio-shadow clauses: this support has
no four-cycle, hence no common-neighbour pair on which those clauses fire.
The SAT assignment is independently checked against every local clause.
No global rainbow conditions are included.

For path i let A_i be the product of its first and third edge weights and
B_i its middle edge weight. The three six-hafnians are exactly

    A_1 B_2 + A_2 B_1,
    A_1 B_3 + A_3 B_1,
    A_2 B_3 + A_3 B_2.

All A_i and B_i are nonzero. Dividing by B_i B_j gives three incompatible
ratio-negation equations. Thus the local Boolean pattern has no complex
weight realization despite passing all four-fibre checks.

On the recorded model the general recursive extractor finds 87 distinct
binomials on 47 numeric variables. A replayed integer kernel vector uses
nine relations, including the one-term equations expressing smaller
hafnians. Their complete-fibre guards give a 40-literal cut. Adding this
single cut excludes the fixed local pattern.

The same graph is not banned. Set every path edge to 1 except Z_04=Z_06=-1.
Then the first two six-hafnians vanish, the third equals -2, and the full
eight-hafnian equals -1. Direct integer hafnian evaluation satisfies the
learned cut and all extracted binomials. The lattice checker also retains
the necessary control that x^2=-1 is consistent over C.

## Conditional all-order path statement

The human obstruction is not restricted to length three. Let three simple,
internally vertex-disjoint paths have common endpoints, lengths at least
two, and the same parity. Require their induced union to contain exactly
the path edges, all with nonzero weights. Each pair then forms an induced
even cycle with exactly two perfect matchings. Put A_i and B_i equal to the
alternating edge products along path i, starting consistently at the same
endpoint. Each cycle hafnian is A_i B_j + A_j B_i. The same ratio argument
proves that the three cycle hafnians cannot all vanish.

The length and induced-support hypotheses matter. A direct endpoint edge,
or a chord furnishing another matching, can introduce a third monomial;
the binomial argument then no longer applies without a sound escape guard.
This is an arbitrary-size conditional obstruction, not an occurrence
theorem. A full weighted Bogdanov proof must still force such a circuit
or a different exact inconsistency from the global colour equations.

## Bounded support search and evidence boundary

A separate sample used three relabelled copies of a fourteen-vertex cubic
bipartite support with cyclic differences {0,1,3} modulo 7. Every pair of
vertices has at most one common neighbour, checked directly. Twenty sampled
triples surviving private-incidence screening all returned UNSAT under RZP
plus the redundant four-cofactor cuts, with zero solver branching decisions.
This produced no global survivor and is not an exhaustive family exclusion.
The complete-four-fibre clauses are vacuous on these supports; passing or
failing them is not the explanation of these solver outcomes.

`python -m unittest -v tests.test_recursive_hafnian_binomials` reproduces
the local SAT model, exact integer certificate, guarded cut, and actual-
weight escape. These are calibration results. The new module and path
argument postdate the Fable review; no independent review of this delta
is claimed yet.
