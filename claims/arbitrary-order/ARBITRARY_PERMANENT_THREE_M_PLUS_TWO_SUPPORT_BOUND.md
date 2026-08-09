# Arbitrary permanent `3m+2` support bound

## Status

This is an exact characteristic-zero support theorem for every multilinear
restriction

```text
P_m -> Delta_3,                    m >= 3.
```

Every such restriction has at least

```text
3m+2
```

nonzero source-row cells.  Thus the earlier `3m` coordinate boundary and
the entire `3m+1` stratum are empty.  In particular a hypothetical
`P_7 -> Delta_3` restriction needs at least 23 nonzero row cells by the
theorem proved here; the later equality closure strengthens this to 24.

The proof is symbolic.  It combines local concision, the arbitrary-order
singleton tricolour cover, a one-exception alternating-cycle lemma, and the
published nonmonochromatic-perfect-matching theorem.  No support or word
enumeration occurs.

At equality `3m+2`, the coordinate-only stratum reduces further to a narrow
Hamilton-factorization/two-cell circuit locus.  The subsequent exceptional-
source rectangle theorem treats noncoordinate rows too: the two excess
cells must have distinct source endpoints, and every mixed backbone
coefficient cancels, if at all, by the unique cross rectangle on those
sources.  Later zero-, one-, and two-switch theorems exclude every equality
stratum.  Combining that classification with the lower bound proved here
gives the strict support bound `3m+3`; see
`ARBITRARY_PERMANENT_EQUALITY_TWO_SWITCH_EXCLUSION_THEOREM.md`.

The displayed Hall-satisfying `P_7` table has exactly 23 coordinate row
cells and realizes all three pure coefficients, local ranks, and port Hall
conditions.  It therefore shows that the numerical bound is sharp for
those prerequisites.  Its unique forbidden mixed coefficient shows why
attaining the count is not enough; it is not a `P_7 -> Delta_3`
restriction.

## Setup

Suppose

```text
P_m(phi_0(x_0),...,phi_(m-1)(x_(m-1)))
  =sum_(c=0)^2 lambda_c product_i x_i[c],
lambda_0 lambda_1 lambda_2 !=0.                        (1)
```

A **row cell** is a pair `(i,p)` consisting of an input mode and a source
row, carrying the covector

```text
r_(i,p)=e_p^* composed with phi_i.
```

It is a coordinate cell of colour `c` if it is a nonzero multiple of
`e_c^*`; otherwise it is noncoordinate.

## Two transverse lower bounds

The singleton tricolour-cover theorem gives, for every source row `p` and
colour `c`, a distinct coordinate cell of colour `c` above `p`.  Hence
there are at least `3m` coordinate cells.

Every local map `phi_i` is injective.  If `y in ker phi_i`, set every other
input equal to `e_c` in (1).  The left side is zero and the right side is

```text
lambda_c y[c].
```

This vanishes for all three colours, so `y=0`.  Thus every mode contains at
least three nonzero row cells.

These are transverse incidence bounds: the first controls every
source-row/colour pair, while the second controls every mode.

## The `3m+1` theorem

Assume for contradiction that there are exactly `3m+1` nonzero cells.
There is at most one noncoordinate cell.

### Case A: every cell is coordinate

For each colour `c`, make a bipartite graph `G_c` between modes and source
rows using the colour-`c` cells.  The source cover meets every source row;
local rank three meets every mode.  The three edge counts are therefore

```text
m, m, m+1
```

in some order.

Each `G_c` has a unique perfect matching.  The `m`-edge graphs are already
perfect matchings, and the nonzero pure coefficient in (1) supplies a
perfect matching in the `m+1`-edge graph.  Two such matchings would have an
alternating cycle; relative to either matching that cycle uses at least two
edges outside it, but only one extra edge exists.

Call the three coordinate perfect matchings `M_0,M_1,M_2`.  They are
edge-disjoint and leave one unused cell.

### Case B: there is one noncoordinate cell

Let that cell be `ell`.  The remaining `3m` coordinate cells consist of
exactly one cell for every source-row/colour pair.  By local concision one
mode has four nonzero cells and every other mode has three.

If `ell` lies at the four-cell mode, all other modes have exactly the three
coordinate colours.  Global counting then gives one coordinate cell of
each colour at the exceptional mode as well.  The coordinate cells split
into three perfect matchings and `ell` is unused.

Otherwise `ell` lies at a three-cell mode `i_*`, and a different
coordinate-only mode `j` has four cells.  The two coordinate rows at `i_*`
have different colours, or the local rank would be at most two.  Let `d`
be the missing colour.  Then `ell[d] !=0`.  Global counting forces colour
`d` to occur twice at `j`, while every other mode/colour incidence occurs
once.

Write `p_*` for the source row of `ell`.  A pure-`d` perfect matching must
use `ell`, since mode `i_*` has no coordinate `d` cell.  Pure nonvanishing
in (1) therefore forces the coordinate `d` cell above `p_*` to be one of
the two cells at `j`.  Remove that cell

```text
g=(j,p_*)
```

and insert `ell`.  This gives the unique colour-`d` perfect matching.  The
other two coordinate colours already form perfect matchings.  Again there
are three edge-disjoint coloured perfect matchings; the only omitted
physical cell is `g`, and `g` shares source row `p_*` with `ell`.

## The mixed matching remains unique

Let

```text
H=M_0 union M_1 union M_2.
```

Bogdanov's theorem, reported as Theorem 1.7 by Chandran, Gajjala, and
Illickan in
[*Krenn-Gu conjecture for sparse graphs*](https://arxiv.org/abs/2407.00303),
gives a nonmonochromatic perfect matching `F` in `H`, since `2m>4`.
Colour each input mode by the label of its incident edge in `F`.

The labelled backbone designates exactly one cell at every mode, hence the
matching `F`.  In Case A and the first subcase of B, only one additional
physical cell can be eligible.  A different perfect matching cannot differ
from `F` in one edge: the symmetric difference of two perfect matchings is
a union of alternating cycles, each using at least two new edges.

In the repair subcase, the only two possible exceptions to the labelled
backbone are the omitted coordinate cell `g` and an off-label use of `ell`.
They share source row
`p_*`, so no perfect matching can use both.  Again no alternative to `F`
exists.

Thus the induced mixed coefficient is the single nonzero product along
`F`, while the right side of (1) has coefficient zero.  This contradiction
excludes `3m+1` and proves

```text
number of nonzero row cells >=3m+2.                    (2)
```

## Coordinate-only equality reduction

Assume now that exactly `3m+2` cells are nonzero and all are coordinate.
Choose one pure perfect matching `M_c` in each colour graph.  Their union
uses `3m` cells, leaving exactly two cells `g_1,g_2`.

For any nonmonochromatic perfect matching `F` in the coloured cubic
backbone `H`, an alternative term with the same induced word must use both
leftovers.  The symmetric difference with `F` therefore has exactly two
new edges.  It is one alternating four-cycle.  Consequently `g_1,g_2` must

1. be vertex-disjoint;
2. cross the two corresponding edges of `F`; and
3. have the colours prescribed by the word at their mode endpoints.

Their two matching monomials must then cancel exactly.

There is a further arbitrary-order restriction.  If some two-colour factor
`M_a union M_b` has at least two alternating cycles, choose a nonempty
proper subset of those cycles and orient it as `M_a`, orienting the rest as
`M_b`.  The complementary orientation gives a second, edge-disjoint mixed
perfect matching.  Both cannot contain the same two backbone edges crossed
by `g_1,g_2`, so one induced mixed coefficient remains unique.

Hence a coordinate-only equality survivor must satisfy all of:

```text
every M_a union M_b is one Hamilton cycle;
the two leftovers give a colour-compatible transposition
  against every nonmonochromatic backbone matching;
the resulting two monomials cancel exactly.            (3)
```

This is a necessary exceptional circuit locus, not a construction.

## Verification

Run:

```text
uv run --with sympy python claims/arbitrary-order/verify_arbitrary_permanent_three_m_plus_two_support_bound.py
python claims/arbitrary-order/audit_arbitrary_permanent_three_m_plus_two_support_bound.py
```

The scripts check the two incidence ledgers, the repair cell, the
one-exception symmetric-difference logic, and a representative two-cycle
orientation.  These are bounded symbolic sanity checks.  The proof of (2)
is the argument above, with Bogdanov's published theorem as its
arbitrary-order matching input.

## Boundary

```text
fewer than 3m coordinate cells:       EXCLUDED;
exactly 3m total cells:               EXCLUDED;
exactly 3m+1 total cells:             EXCLUDED;
coordinate-only 3m+2 cells:          HAMILTON/CIRCUIT LOCUS ONLY;
all 3m+2 strata classified through:  TWO-SOURCE SIGNED RECTANGLE SYSTEM;
zero-switch equality stratum:        EXCLUDED BY LATER REFINEMENT;
one-switch equality stratum:         EXCLUDED BY LATER REFINEMENT;
two-switch equality stratum:         EXCLUDED BY LATER REFINEMENT;
all 3m+2 equality existence:         EXCLUDED BY LATER REFINEMENTS;
later strict support lower bound:     3m+3;
arbitrary larger P_m restrictions:   UNKNOWN;
global Krenn-Gu conjecture:           UNRESOLVED.
```

The equality refinement and its independent replay are in
`ARBITRARY_PERMANENT_EQUALITY_EXCEPTIONAL_SOURCE_RECTANGLE_THEOREM.md`.
The zero-switch branch exclusion is in
`ARBITRARY_PERMANENT_EQUALITY_ZERO_SWITCH_EXCLUSION_THEOREM.md`.
