# Q4: global component targets coupled to four-minority sources

## Exact parent, supply and consumer

Starting checkpoint: 93d38fe3, with proof-map snapshot 1f285d68. The preceding
goal turn made progress: it excluded the complete two-K4 scaffold and proved
that every fixed minority depth has exact proper-subsystem controls at some
larger order. The global conjecture remains **UNRESOLVED**.

For every k>=2, fix a protected scaffold on n=4k vertices over C: each K4
component has its three unit matrix-edge perfect matchings, and every
intercomponent physical matrix is hollow but otherwise arbitrary.
Q4 asserts that no such array satisfies both:

1. T_W(a)=delta(a) for all 3^k component-constant words;
2. T_W(a)=delta(a) for every word differing from some constant word at at
   most four physical vertices.

All equations belong to the same physical source. A full GHZ witness
supplies them. The named downstream consumer is exclusion of the protected
scaffold family in the proposed full-source high-surplus route. There is
still no reduction from arbitrary witnesses to that scaffold, so proving
Q4 would not resolve the global conjecture.

Success means a proved Q4 implication, an exact physical countermodel to Q4
with an explicit remaining full-target failure, or a precise obstruction
that eliminates a declared mechanism and identifies a sharper load-bearing
lemma. An apparent full-target counterexample triggers dedicated adversarial
validation before any status change.

## Why these mechanisms must be combined

The third six-parameter n=8 family satisfies every component-constant target
and every independent-minority equation, but fails a four-minority word.
The all-depth graph lifts satisfy any fixed minority depth, but fail an
explicit global component-constant target. Thus neither proves nor refutes
Q4. The exact exterior-resource expansion retains the missing coupling;
cofactors and resource labels may not be replaced by independent symbols.

## Direct proof and countermodel routes

The analytic route attacks the all-k shared polynomial system, using
global component targets together with the complete exposed-partner and
one/two-resource formulas for at most four minorities.

The pair-allocation countermodel route is exact but narrower. A simple
six-regular bipartite component graph, with each of the six ordered
distinct-colour labels once at each vertex and girth at least six, already
supplies all depth-four equations through the proved forest lemma.
Its component-constant source equals the product of (1-1) over compatible
gadgets. Hence a graph with only the three constant avoiding colourings
would satisfy Q4 physically. A full non-component-constant failure must then
be exhibited exactly; otherwise the result is an apparent global
counterexample requiring escalation, not a casual subsystem claim.

Two bounded efforts address this exact route: construct such a label graph,
or prove a nonconstant avoiding colouring unavoidable. The latter would
eliminate this countermodel mechanism only; it is not a reduction of every
protected filling to pair gadgets.

The coordinator may also test the actual k=3 Q4 polynomial system to seek a
physical countermodel or a load-bearing source consequence. A Boolean SAT
support alone is not weights, and local UNSAT is not the all-k theorem.
These are direct tests of the named parent, not independent census goals.

Every computation expected to exceed one minute uses the bounded runner or
equivalent explicit containment, with an initial 900-second/8192-MiB cap
and at most three concurrent research computations. Native Windows SAT
proof export is unreliable on this host; use canonical CNF generation and
standalone Linux solvers with independent proof checking when needed.
No GPU computation is currently required by these exact symbolic routes.

## Common-centre extension and its exact resource test

An attempted extension lets all gadgets using one component share a
common physical centre and the leaf selected by that component's colour.
It allows repeated labels at a vertex and arbitrary nonzero gadget
weights. It is materially different from allocating the two protected
matching pairs to different colour ports. On a compatible forest its
source is a weighted matching partition function; on general graphs the
two physical layers can choose different perfect matchings, so the exact
formula is a sum of products of two hafnians. Treating it as a matching
partition function on cycles was an exploratory error, corrected before
any theorem promotion.

The direct route test is whether this common-centre construction can meet
the component targets while a graph of large girth supplies the U4
equations. The accepted obstruction uses one actual gadget edge, singleton
component normalizations, and a two-component word in the third-colour
background. Its exact identity is q_uv=F_uv-F_u F_v whenever uv lies in
no triangle. The target equations therefore force every nonzero gadget
edge into a triangle and exclude the triangle-free construction. The
[owning proof](../../claims/arbitrary-order/PROTECTED_SCAFFOLD_COMMON_STAR_COMPONENT_TARGET_OBSTRUCTION.md)
and [independent review](../audits/PROTECTED_SCAFFOLD_COMMON_STAR_REVIEW_2026-09-14.md)
close this declared Q4 construction route. The frontier records the new
PSCS implication and its triangle/two-resource boundary. It is not a
claimed normal form for arbitrary protected fillings.

The same parent attempt then closes a second mechanism rather than
opening another local census. Singleton targets force every ordered
endpoint port to be nonempty and a unique port's product to equal -1.
If three specified ports around an oriented edge are unique, the actual
double-component source is -1 for distinct spoke endpoints and -2 for
a shared endpoint. Thus unique-port common-star constructions also fail,
even with triangles. Together the two proofs leave interacting triangles
with repeated ports as a necessary next common-star resource mechanism.
No implication from general Q4 fillings to common-star arrays is claimed.

## Initial actual-source calculation

The standard-library generator
`tools/explore/probe_protected_scaffold_q4.py` retains all 288 crossing
physical entries at k=3 and expands the actual matching polynomials for
29,913 selected source words. Its necessary support model has 330,048
variables and 1,943,640 clauses. The canonical LF CNF SHA-256 is
`38079fafdf36e7e105e3a08369a459930c139c0a20a197fad75017e4c0f3b4f1`;
the equation-stream SHA-256 is
`4fa2e69b6fc62bc9d34f710e2ee2bf32ba51bad8291676b30b16c591940929ce`.
At k=2, all 4,881 generated polynomials were cross-checked against the
committed matching-first source expansion after transporting variable
indices. That boundary check is not an independent audit of k=3.

Standalone Linux CaDiCaL 1.7.3, with an 880-second solver limit and a
900-second outer deadline, returned `c UNKNOWN` and exit 0. The process
exited and its identity was checked. No model or exclusion was obtained;
the incomplete proof stream is not a certificate. This attempt outcome
does not change the live mathematical frontier.

A second bounded run added the single normalization clause that physical
entry W_0,4[0,1] is nonzero. Any Q4 solution has a nonzero crossing entry;
component permutations, independent K4 translations, and simultaneous
colour/linear permutations act transitively on the 288 entries while
preserving every selected source word. An independent symmetry check
confirmed the orbit and invariance. The normalized CNF SHA-256 is
`807cfb251a89619798c6815a3c9e87327cb87ade1c8ce58b69cf46955ff0e9c9`.
CaDiCaL again returned `c UNKNOWN`, this time with a 300-second solver
limit inside a 320-second outer deadline. Both attempts are inconclusive;
neither licenses an n=12 theorem or an all-order conclusion.

## A stronger sufficient route, still open

One sufficient combinatorial lemma would say that every actual protected
U4 filling has a nonconstant component colouring for which the protected
matching has no supported alternating cycle. Such a matching would be
unique, with amplitude 1, contradicting the global target. This lemma is
stronger than Q4 and is not established by a necessary-support model.

The high-girth controls forbid an attempted shortcut: even a single
changed component can have an exact cancellation 1+(-1)=0 while every U4
equation holds. Therefore no argument from U4 alone can isolate every
nontrivial cancellation term as a forbidden monomial. Global equations
from other component colourings must enter.

## Bounded external-method check

For the pair-allocation route, form an option graph with vertices (v,c)
and one conflict edge for each labelled component edge. It is bipartite
and 2-regular; avoiding colourings are independent transversals of the
triples belonging to components. This equivalence does not settle whether
the three constant transversals can be the only ones.

Theorem 1.2 and Corollary 1.3 of Cambie--Kang,
[Independent transversals in bipartite correspondence-covers](https://doi.org/10.4153/S0008439521001004),
were inspected as possible tools. The three numerical sufficient
conditions in Theorem 1.2 all fail at part size 3, option degree 2 and
component degree 6; the corollary requires sufficiently large degree.
Neither supplies a theorem for this problem, much less a nonconstant
transversal.

Theorem 4 of Haxell--Wdowinski,
[Constructing Graphs with No Independent Transversals](https://doi.org/10.37236/12429),
was also inspected: degree-two graphs partitioned into triples can lack
an independent transversal. This is a warning against using degree two
alone. Its general constructions are not asserted to satisfy our port
labels, side-respecting partition or three known constant transversals.
These are scoped background checks, not imported proof dependencies or
a comprehensive novelty search.
