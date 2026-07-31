# Krenn--Gu literature and translation review (30 July 2026)

## Scope and evidence boundary

This review concerns the complex-weighted monochromatic quantum-graph
equation, not only ordinary edge-colourings with no cancellation.  The
target is

```text
T_W(a_1,...,a_n)
 = sum_(perfect matchings M)
     product_({i,j} in M) W_ij[a_i,a_j]
 = Delta_(n,d).
```

The global statement for even `n>=6,d>=3` remains open.  No source below
contains either a global counterexample or a global nonexistence proof.

## Primary problem and physics sources

1. Krenn, Gu, and Zeilinger,
   [Quantum Experiments and Graphs: Multiparty States as Coherent
   Superpositions of Perfect Matchings](https://arxiv.org/abs/1705.06646)
   (2017), identifies graph edges with pair sources and perfect
   matchings with coherent state terms.  This is the origin of the
   hafnian/matching-tensor formulation.
2. Krenn, Gu, and Soltész,
   [Questions on the Structure of Perfect Matchings inspired by Quantum
   Physics](https://arxiv.org/abs/1902.06023) (2019), gives the
   graph-theoretic inherited-colouring formulation and the original
   family of open questions.
3. Krenn's maintained
   [problem page](https://mariokrenn.wordpress.com/graph-theory-question/)
   records the prize problem and later public updates.  It is useful for
   provenance, but theorem claims here are checked against papers or
   proof artifacts where possible.

## Published combinatorial frontier

1. Chandran and Gajjala,
   [Edge-coloured graphs with only monochromatic perfect matchings and
   their connection to quantum
   physics](https://arxiv.org/abs/2202.05562) (2022/2023), classifies the
   cancellation-free `PMValid` colouring problem.  Its support
   structure is relevant, but arbitrary complex destructive
   interference is strictly more general.
2. Chandran, Gajjala, and Illickan,
   [Krenn--Gu conjecture for sparse
   graphs](https://arxiv.org/abs/2407.00303) (MFCS 2024), proves the
   conjecture for skeletons of vertex connectivity at most two and for
   cubic graphs, and shows a minimal counterexample must be
   four-connected.
3. The current Google DeepMind
   [`MonochromaticQuantumGraph.lean`](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/Paper/MonochromaticQuantumGraph.lean)
   formalizes the exact complete-graph equation system.  As checked on
   30 July 2026, its public registry still labels the complex
   `(n,d)=(6,3)`, `(8,3)`, and general even-order statements as open,
   while recording the `d=n` obstruction as solved.

## Results in this repository that go beyond that published frontier

Subject to the repository's exact replay artifacts and still needing
external mathematical review, the strongest additional claims are:

- exact complex nonexistence for six vertices and therefore every
  `d>=3` by colour restriction;
- several exact eight- and ten-vertex support/skeleton exclusions;
- arbitrary-order blocker, balanced-bridge, and reciprocal-port
  obstruction theorems;
- a complete exact-three-coordinate obstruction for
  `P_5 -> Delta_3`;
- exact exclusions of normalized `q5_311`, `q5_221`, and `q4_211`;
- at least eight inequivalent components of the pure rank-two
  `P_4`-compression variety, with generic `H31` and now generic weighted
  `H22` fibres empty on all eight; on the eighth component the equal-
  and opposite-weight `H22` fibres are additionally empty already at
  the binary-incidence level, twelve generic parameter/coordinate
  branches are empty by exact Fitting ideals, and the principal
  coupled slope-parameter divisor is empty by a cross-mode minor.  An
  intrinsic maximal-minor content calculation further closes the four
  rational sheets `af=+/-1,a phi=+/-1`; on those sheets the `D_23`
  binary incidence itself is generically empty.  A second intrinsic
  content ledger closes the compactified slope endpoint `r=0`: `D_01`
  fails already at binary level, while the rank-six `D_23` degeneration
  fails a two-minor marked-rank test.  Normalizing a further coefficient
  divisor exposes a new irreducible quadratic component branch; full
  unsplit Fitting ideals exclude both weighted directions there.

The first item is stronger than the currently cited paper frontier and
than the status labels in the current public formal-conjectures file.
It should therefore be presented as a repository computer-assisted
theorem, not silently attributed to those authors and not treated as a
peer-reviewed global result.

## Translating the problem into other mathematical languages

| Original surface | Translated object | Tool exposed |
|---|---|---|
| coherent sum over perfect matchings | coloured hafnian / matching tensor | tensor contractions, flattenings, subrank |
| local colour changes | `GL(d)^n` tensor restriction | representation theory and invariant/covariant modules |
| deleted roots and blockers | restrictions of permanent tensors `P_k` | apolarity, Frobenius algebras, zero-product geometry |
| existence of a binary neighbour | rank drop of a `14 x 8` matrix | determinantal varieties and Fitting ideals |
| pure tensor target | Segre variety | secants, tangents, incidence geometry |
| local two-planes | points of `Gr(2,4)` | Plücker coordinates and matroid strata |
| support cancellations | binomial/toric relations | lattice ideals and circuit elimination |
| several simultaneous roots | multihomogeneous zero loci in products of projective planes | Chow rings and intersection numbers |
| blocker allocation | transversal problem | Hall-type and matroid-intersection inequalities |
| mode/colour symmetry | finite group action | orbit normal forms and equivariant stratification |

The determinantal step used in the new `H22` theorem is standard Fitting
geometry: rank-drop loci are cut out by minors, and the construction is
stable under base change.  See the Stacks Project,
[Fitting ideals, Section 15.8](https://stacks.math.columbia.edu/tag/07Z6).

The tensor-subrank translation also has a mature algebraic-complexity
literature.  Useful orientation includes Kopparty--Moshkovitz--Zuiddam,
[Geometric rank of tensors and subrank of matrix
multiplication](https://arxiv.org/abs/2002.09472), and
Derksen--Makam--Zuiddam,
[Subrank and Optimal Reduction of Scalar Multiplications to Generic
Tensors](https://arxiv.org/abs/2205.15168).  Those papers do not solve
the Krenn--Gu restriction problem, but their monotonicity and
rank-variety viewpoint is the right language for turning local
permanent restrictions into invariant obstructions.

## What the review changes strategically

The published graph-theoretic papers extract strong consequences from
support and connectivity, but they do not classify cancellation
varieties over `C`.  The repository's most productive symbolic route
has instead been:

```text
matching graph
 -> hafnian tensor
 -> deleted permanent restriction
 -> squarefree apolar algebra
 -> Grassmann/Fitting incidence
 -> a few exact minors.
```

The new weighted `H22` theorem is a clean example.  A broad
extension-variable elimination had timed out.  Passing first to the
Fitting scheme of the mixed matrix turns one direction into a line and
the other into a degree-five scheme; three factor charts and two small
minors then finish the generic component.

The next high-value translation is not a larger graph search.  It is a
global classification of the pure `P_4` compression variety, preferably
as an orbit/degeneracy-locus theorem in `Gr(2,4)^4`, followed by a
simultaneous-root Grassmannian formulation of the blocker hierarchy.
