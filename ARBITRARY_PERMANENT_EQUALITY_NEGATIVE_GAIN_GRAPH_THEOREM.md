# Arbitrary permanent equality negative-gain graph theorem

## Status

This is an exact arbitrary-order reformulation of every `H`-induced rectangle
cancellation in the `3m+2` equality stratum.  Once the exceptional-source
rectangle theorem has localized the two excess source endpoints `p_1,p_2`,
all such rectangle equations live on one auxiliary signed graph.  Every edge
has gain `-1`.

A hypothetical equality restriction forces this graph to be bipartite.
For one fixed choice of the three pure matchings, however, that bipartition
is already canonical: an incident mode--colour state is labelled by whether
its pure edge ends at `p_1` or `p_2`.  Thus **no single-backbone odd-cycle
argument can work**.

The nontrivial gain object is the union over different choices of the pure
matchings.  The same ratio state can change exceptional-source side between
choices, so the union need not be canonically bipartite; a hypothetical
restriction requires it to remain bipartite.  This identifies an exact new
matching-exchange target without enumerating matchings, supports, or words.

## Setup

Assume a hypothetical restriction

```text
P_m -> Delta_3,                m>=3,                 (1)
```

has exactly `3m+2` nonzero row cells.  The exceptional-source rectangle
theorem gives two distinct source endpoints `p_1,p_2`.  Write

```text
r_(i,p)[c]
```

for the colour-`c` coefficient of the physical row cell at mode `i` and
source `p`.

Define the **ratio-state set**

```text
V_Gamma={(i,c):r_(i,p_1)[c] r_(i,p_2)[c] !=0}.       (2)
```

For every state in (2), put

```text
g_(i,c)=r_(i,p_2)[c]/r_(i,p_1)[c] in K^*.            (3)
```

## Cancellation graph

Choose one pure matching per colour and let `H` be their coloured backbone.
For every nonmonochromatic perfect matching `F` in `H`, let modes `i,j` be
matched by `F` to the two exceptional sources.  Let `c_i,c_j` be the colours
that `F` induces at those modes.  The unique alternative term for this word,
if it exists, is the cross transposition on `i,j,p_1,p_2`.

The mixed coefficient must vanish in (1), while its backbone monomial is
nonzero.  Hence the cross term exists and all four coefficients are nonzero.
Add an edge

```text
{(i,c_i),(j,c_j)}                                   (4)
```

to `Gamma`.  Parallel edges may be retained or suppressed.  There are no
loops because `i!=j`.

## Negative-gain theorem

For an edge (4), the exact rectangle coefficient is

```text
r_(i,p_1)[c_i] r_(j,p_2)[c_j]
+r_(i,p_2)[c_i] r_(j,p_1)[c_j]=0.                   (5)
```

Divide by the nonzero first product.  Equations (3) and (5) give

```text
g_(i,c_i)/g_(j,c_j)=-1,
g_(i,c_i)=-g_(j,c_j).                                (6)
```

Thus `Gamma` is a multiplicative gain graph in which every oriented edge
has gain `-1` (its own inverse).  Around a cycle of length `ell`, (6)
telescopes to

```text
g_v=(-1)^ell g_v.                                    (7)
```

Over characteristic different from two, `g_v!=0`, so every cycle is even.
Consequently

```text
Gamma is bipartite.                                  (8)
```

Conversely, if an abstract graph `Gamma` is bipartite, choose a nonzero
scalar `t_C` on each connected component and set `g_v=t_C` on one side and
`g_v=-t_C` on the other.  Then every equation (6) holds.  Hence odd-cycle
balance is the complete consistency criterion for the ratio equations
alone.

This converse does not construct row covectors, pure matchings, or the
remaining zero coefficients.  It says only that no stronger contradiction
can follow from multiplying the rectangle ratios themselves.

## Why one fixed backbone can never obstruct

For the chosen pure matching `M_c`, let `sigma_c(i)` be the source matched to
mode `i`.  If a state `(i,c)` is incident to an edge of `Gamma` as the
`p_s` endpoint of a mixed backbone matching, then

```text
sigma_c(i)=p_s.                                      (9)
```

Put every nonisolated state satisfying `sigma_c(i)=p_1` on the left and
every state satisfying `sigma_c(i)=p_2` on the right.  These sets are
disjoint because `M_c` is a matching, and every edge has one endpoint in
each.  This proves (8) combinatorially before using any ratios.

Therefore the fixed-backbone gain graph is a normalization of its rectangle
equations, not a new obstruction.  In particular, attaching exchange
two-cells whose boundaries are already closed walks in this graph cannot
create new odd holonomy.

## The all-backbone gluing graph

Now allow every possible choice

```text
H=M_0 union M_1 union M_2                         (10)
```

of one pure matching in each colour graph.  Form `Gamma^*` on the same
ratio-state vertices by taking the union of the edges obtained from every
such `H`.  The numerical ratio `g_(i,c)` in (3) depends only on the physical
row cells, not on the choice of pure matching.  Hence every edge of
`Gamma^*` still satisfies (6), and

```text
Gamma^* must be bipartite.                            (11)
```

Unlike a single fibre, `Gamma^*` has no automatic source bipartition.  A
state `(i,c)` can lie on the `p_1` side for one `M_c` and the `p_2` side for
another exactly when two pure colour-`c` matchings route mode `i` to the two
different exceptional sources.  Their symmetric difference then contains
an alternating cycle transporting `i` between `p_1,p_2`.

Thus the exact remaining gain-graph question is:

> Do the alternating-cycle transports among all pure matchings force an odd
> cycle in `Gamma^*`, or can every transport be globally two-coloured?

The first outcome excludes `3m+2` equality.  The second gives a global
two-colouring normal form that must be intersected with the remaining
permanent coefficients.  Neither outcome has yet been proved.

The pure-matching cube theorem reduces this gluing problem further.  Every
nontrivial pure switch is the exceptional-source four-cycle, and at most two
colours can switch.  Thus `Gamma^*` is the union of at most four backbone
fibres.  The two-switch case is confined to the branch in which both excess
cells are noncoordinate and co-located at one mode.  See
`ARBITRARY_PERMANENT_EQUALITY_PURE_MATCHING_CUBE_THEOREM.md`.

The backbone-colouring glue theorem gives the exact descent criterion for
those fibres.  It reduces global bipartiteness to balance of an `F_2`-labelled
component-overlap graph and yields a two-state one-switch straddling
obstruction.  See
`ARBITRARY_PERMANENT_EQUALITY_BACKBONE_COLORING_GLUE_THEOREM.md`.

## Translation to the literature

The gain-graph language is standard: an oriented edge carries a group
element, reversing orientation inverts it, and a cycle is balanced when its
gain product is the identity.  See Zaslavsky, *Biased graphs. I. Bias,
balance, and gains*, JCTB 47 (1989),
[doi:10.1016/0095-8956(89)90063-4](https://doi.org/10.1016/0095-8956(89)90063-4).

What is new here is the translation: the permanent coefficient equation
canonically produces the gain `-1` on mode--colour ratio states.  Standard
gain-graph switching changes the vertex potentials and all incident edge
gains together; the fixed all-negative gauge used in (6) is one convenient
representative.  The fixed-backbone source bipartition is an exact route
exclusion, while the all-backbone gluing graph `Gamma^*` is the surviving
object.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_equality_negative_gain_graph_theorem.py
python audit_arbitrary_permanent_equality_negative_gain_graph_theorem.py
```

The primary verifier checks the rectangle-to-gain identity, odd-cycle
holonomy, an even-cycle switching solution, and the possibility that
bipartite backbone fibres glue to a nonbipartite union.  The independent
audit repeats the balance criterion with exact rational propagation.  These
are fixed symbolic checks; the theorem is the argument above.

## Boundary

```text
every equality rectangle gain:             -1;
odd cancellation cycle:                    EXCLUDED;
fixed-backbone cancellation graph:         CANONICALLY BIPARTITE;
single-backbone gain obstruction:          NONE;
all-backbone gluing graph:                  NECESSARILY BIPARTITE;
forced odd cycle in all-backbone graph:     UNKNOWN;
bipartite ratio equations:                  ABSTRACTLY CONSISTENT;
bipartite full permanent realization:       UNKNOWN;
global Krenn--Gu conjecture:                 UNRESOLVED.
```
