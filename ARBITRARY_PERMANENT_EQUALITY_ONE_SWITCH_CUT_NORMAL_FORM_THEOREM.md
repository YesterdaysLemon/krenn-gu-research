# Arbitrary permanent equality one-switch cut normal-form theorem

## Status

This is an exact characteristic-zero theorem for the branch of a hypothetical
`3m+2` equality restriction in which exactly one colour has two pure perfect
matchings.  It uses no support, word, or matching enumeration.

The nonzero pure coefficient forbids every nonmonochromatic perfect matching
in either selected coloured backbone that uses both selected switch edges.
After deleting the two switch modes and the two exceptional sources, the
common residual backbone has a unique perfect matching and hence an acyclic,
triangular support form.

The two-backbone gluing condition also becomes exact.  In the bipartite
component-incidence graph of the two cancellation fibres, the only nonzero
overlap labels are the two switch states.  Equality requires those two marked
edges to form an `F_2` cut: they must both be bridges or, if nonbridges, a
two-edge cut (a graphic-matroid series pair).

This note alone does not exclude the one-switch branch.  A subsequent
pairwise-Hamilton/chord theorem uses permanent coefficients not represented
by the abstract gluing graph and excludes the branch completely; see
`ARBITRARY_PERMANENT_EQUALITY_ONE_SWITCH_EXCLUSION_THEOREM.md`.

## Switch core

Let colour `c` be the unique switchable colour.  Its two pure matchings agree
away from modes `a,b` and exceptional sources `p_1,p_2`, and use respectively

```text
M_c^0: (a,p_1),(b,p_2),
M_c^1: (a,p_2),(b,p_1).                              (1)
```

Write the four nonzero colour-`c` entries as

```text
A=r_(a,p_1)[c],  B=r_(a,p_2)[c],
C=r_(b,p_1)[c],  D=r_(b,p_2)[c].                    (2)
```

Let `M_c^circ` be the common residual perfect matching after deleting
`a,b,p_1,p_2`, and let its nonzero weight be `W_c`.  The pure coefficient is

```text
lambda_c=W_c(AD+BC) !=0.                             (3)
```

In particular,

```text
AD+BC !=0.                                          (4)
```

## Switch-core rigidity

Fix either backbone `H_t`, `t in {0,1}`.  No nonmonochromatic perfect
matching in `H_t` can use both of its selected colour-`c` switch edges.

For example, suppose a nonmonochromatic matching `F` in `H_0` uses the
`A,D` edges.  The exceptional-source rectangle theorem says that its only
possible cancellation partner has the same residual matching and replaces
`AD` by `BC`.  If the residual weight is `W_F!=0`, the forbidden mixed-word
coefficient is exactly

```text
W_F(AD+BC).                                         (5)
```

Equations (4)--(5) make (5) nonzero, a contradiction.  The argument in
`H_1` is identical with the two core pairs exchanged.

Consequently no cancellation edge in either fibre joins the two switch
states

```text
u=(a,c),        v=(b,c).                             (6)
```

Notice that this is stronger than the fact that `u,v` lie on opposite
canonical sides: the pure coefficient prevents even an `H_t`-induced mixed
matching whose terminal pair is exactly `(u,v)`.

## Unique residual matching theorem

Let `H^circ` be the common coloured backbone obtained from either `H_t` by
deleting `a,b,p_1,p_2` and collapsing coloured copies to physical cells.
Then

```text
M_c^circ is the unique perfect matching of H^circ.   (7)
```

Proof.  Suppose `K!=M_c^circ` were another residual perfect matching.  Add
the two selected colour-`c` core edges of `H_0`.  If the resulting full
matching is nonmonochromatic, switch-core rigidity gives a contradiction.
If it is monochromatic of colour `c`, it is a third pure colour-`c` physical
matching, contradicting the pure-matching theorem, which permits only the
two matchings in (1).  There is no coloured-copy ambiguity outside the
core: both nonmandatory physical cells participate in the switch, so every
cell of `H^circ` belongs to the coordinate mandatory cover.

Relabel the residual matched pairs as `x_i--y_i`.  Contract these matching
edges, and replace every other residual edge `x_i--y_j` by an arc `i -> j`.
A directed cycle is exactly an alternating cycle relative to `M_c^circ`,
and toggling it would produce a second residual perfect matching.  Thus the
dependency digraph is acyclic.  A topological ordering makes the residual
biadjacency support triangular with a nonzero matching diagonal.

Equivalently, every alternating cycle of a full backbone relative to its
selected pure colour-`c` matching meets the four-vertex switch core.  This is
the precise leaf-stripping structure available for an arbitrary-order
induction.

## Two-fibre component-incidence graph

Let `Gamma_0,Gamma_1` be the two fixed-backbone cancellation graphs on the
common physical ratio-state set.  Include isolated states as one-vertex
components.  Let `C_t` be the set of connected components of `Gamma_t`.

Define a bipartite multigraph `B` with parts `C_0,C_1`.  For each ratio state
`z`, add an incidence edge

```text
e_z:C_0(z)--C_1(z).                                  (8)
```

For a state whose pure edge meets an exceptional source, use that source as
its canonical side label.  A state whose pure edge meets neither exceptional
source is isolated in that fibre; every nonswitch pure edge is common to the
two backbones, so give each such isolated state the same arbitrary side
label in both fibres.  With this convention only the two states (6) change
side across the switch, so the overlap label on (8) is

```text
ell(e_z)=1 if z in {u,v},
ell(e_z)=0 otherwise.                                (9)
```

The general backbone-colouring glue theorem now says that the two fibres
glue bipartitely exactly when there are component offsets
`kappa:C_0 union C_1 -> F_2` satisfying

```text
ell(e)=kappa(left(e))+kappa(right(e)).                (10)
```

Thus, writing `S={e_u,e_v}`, a hypothetical equality restriction requires

```text
chi_S is a coboundary of B,
equivalently S belongs to the cut space of B.         (11)
```

By cut--cycle orthogonality over `F_2`, (11) is equivalent to each of the
following statements.

- Every cycle of `B` contains both marked edges or neither.
- No marked edge lies on a cycle avoiding the other.
- Either both marked edges are bridges, or both are nonbridges and
  `{e_u,e_v}` is a two-edge cut, equivalently a graphic-matroid series pair.

The one-switch straddling obstruction is the smallest violation: a switched
state and an unswitched state lying in the same component in both fibres
give parallel incidence edges, and their length-two cycle contains exactly
one marked edge.  Longer cycles impose the complete remaining obstruction,
so straddling is sufficient but is not the whole cut-space criterion.

The glue theorem alone cannot force a violation.  At the abstract
cancellation-graph level, take the two switch states isolated in both fibres
and place all mixed-cancellation edges in unswitched components.  Then the
two marked incidence edges are bridges and (10) is solvable.  This is not a
permanent realization; it is an exact countermodel to any argument using
only the abstract fibre bipartitions.  A further proof must use the
triangular residual backbone or additional coefficient equations.

## Literature translation

The residual theorem is the unique-perfect-matching corner of classical
matching decomposition.  Kotzig's bridge theorem says that a connected
graph with a unique perfect matching has a matching edge that is a bridge;
the alternating-cycle/DAG proof above gives the sharper bipartite triangular
form needed here.  See:

- A. Kotzig, *On the theory of finite graphs with a linear factor I*
  (1959), [EuDML record](https://eudml.org/doc/29879);
- A. L. Dulmage and N. S. Mendelsohn, *Coverings of Bipartite Graphs*,
  Canadian Journal of Mathematics 10 (1958),
  [doi:10.4153/CJM-1958-052-0](https://doi.org/10.4153/CJM-1958-052-0).

The new problem-specific object is the two-fibre incidence graph `B`.
Equation (11) translates permanent cancellation into ordinary cut--cycle
duality: the switch pair must be a cocycle.  This identifies a more precise
symbolic target than asking only for a local straddling pair.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_equality_one_switch_cut_normal_form_theorem.py
python audit_arbitrary_permanent_equality_one_switch_cut_normal_form_theorem.py
```

The primary verifier checks the shared pure/mixed switch factor and exact
cut--cycle equations for bridge, series-pair, and unbalanced cases.  The
independent no-import audit checks the same claims by parity propagation on
fixed symbolic incidence diagrams.  Neither script enumerates supports,
words, or perfect matchings.

## Boundary

```text
H_t-induced mixed matching using both edges:  EXCLUDED;
common residual perfect matching:             UNIQUE;
residual dependency support:                  ACYCLIC / TRIANGULAR;
two-fibre overlap labels:                     EXACTLY TWO MARKED EDGES;
equality gluing condition:                    MARKED PAIR IS A CUT;
marked bridge-or-series normal form:          NECESSARY;
forced cycle separating the marked pair:     UNKNOWN;
one-switch equality stratum:                  EXCLUDED SUBSEQUENTLY;
zero-switch equality stratum:                 NOT ADDRESSED HERE;
two-switch equality stratum:                  NOT ADDRESSED HERE;
global Krenn--Gu conjecture:                  UNRESOLVED.
```
