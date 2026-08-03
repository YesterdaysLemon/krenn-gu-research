# Arbitrary permanent equality one-switch exclusion theorem

## Status

This is an exact arbitrary-order exclusion of the `3m+2` equality branch
with exactly one switchable colour.  It applies for every `m>=3` over
characteristic zero and performs no support, word, or matching enumeration.

Switch-core rigidity and exceptional-source localization first force every
pair of selected pure matchings to form one alternating Hamilton cycle.  The
three selected pure matchings are therefore pairwise physically edge-
disjoint.  Each exceptional edge of a nonswitch colour is then a chord of
the Hamilton cycle formed by the other two colours.  The two chord-extension
mixed matchings force both exceptional-source cross cells and create a
second pure matching in that nonswitch colour, a contradiction.

Together with the zero-switch exclusion, this proves that every hypothetical
`3m+2` equality survivor must lie in the sole two-switch branch.

## Setup

Assume a hypothetical equality restriction

```text
P_m -> Delta_3,       support size 3m+2,       m>=3, (1)
```

has exactly one switchable colour `c`.  Let `d,e` be the two nonswitch
colours.  Choose either pure `c`-matching `M_c`; the pure matchings `M_d,M_e`
are unique.

Retain coloured copies when two selected matchings use the same
noncoordinate physical cell.  On each alternating component of a pairwise
union, choosing all edges of one colour gives a perfect matching.  Before
comparing permanent terms, collapse coloured copies back to physical cells,
as required by the exceptional-source rectangle theorem.

## Pairwise Hamilton theorem

Each of

```text
M_c union M_d,
M_c union M_e,
M_d union M_e                                      (2)
```

is one spanning alternating Hamilton cycle.

First consider `M_c union M_d` and decompose it into alternating components.

- If `p_1,p_2` lie in one component and another component exists, choose
  `M_c` on the marked component and `M_d` on another.  The resulting
  matching is mixed but uses both selected `c` switch edges.  Its forbidden
  coefficient has the same nonzero local factor `AD+BC` as the pure
  `c`-coefficient, contradicting switch-core rigidity.
- If `p_1,p_2` lie in different components and at least three components
  exist, choose `M_c` on both marked components and `M_d` on a third.  The
  same contradiction applies.
- Suppose exactly two components remain, with one exceptional source in
  each.  The two complementary hybrids have terminal colour patterns
  `(c,d)` and `(d,c)`.  Their required rectangle partners respectively
  supply the two missing `d` cross cells.  Transposing the exceptional
  `M_d` edges while retaining every other `M_d` edge creates a second pure
  `d`-matching, contradicting that `d` is nonswitch.

Thus `M_c union M_d` has one component.  The same proof with `e` in place of
`d` shows that `M_c union M_e` has one component.

For `M_d union M_e`, both colours are nonswitch.  The identical component
selection argument uses the localization rule in place of switch-core
rigidity.  Choosing one nonswitch colour at both exceptional sources in a
mixed component selection forces its two cross cells and hence a second pure
matching.  In the exact two-component split case, the complementary hybrids
force both cross cells for each nonswitch colour.  All cases with more than
one component are impossible.

Since `m>=3`, the single component in each pairwise union is a spanning
cycle, not a two-cycle of parallel coloured copies.  A physical cell shared
by two selected matchings would itself form such an isolated two-cycle.
Consequently

```text
M_c,M_d,M_e are pairwise physically edge-disjoint.   (3)
```

This is a perfect-one-factorization normal form forced by equality.

## Exceptional chords

Fix the nonswitch colour `d`.  Put

```text
i_s=M_d^(-1)(p_s),
f_s=(i_s,p_s),              s in {1,2}.              (4)
```

The union

```text
C=M_c union M_e                                      (5)
```

is an even physical Hamilton cycle.  By (3), each `f_s` is a genuine chord
of `C`, joining its two bipartition classes.

Every such chord extends to a perfect matching of `C union {f_s}`.  The two
paths between the chord endpoints have odd edge length.  After removing the
endpoints, both path interiors have an even number of vertices and possess
their alternating perfect matchings.  Adjoin `f_s` and call the result
`F_s`.

Then

```text
F_s subset M_c union M_d union M_e.                  (6)
```

It contains the single `d` edge `f_s` and `m-1` selected `c/e` edges.  Since
`m>=3`, it is nonmonochromatic.  At exceptional source `p_s`, it uses colour
`d`.

## The two chords switch a nonswitch colour

The mixed coefficient containing `F_s` must vanish.  Exceptional-source
localization leaves exactly its `p_1,p_2` transposition as a possible second
term.  Therefore cancellation forces

```text
r_(i_s,p_(3-s))[d] !=0.                              (7)
```

Apply (7) for both values of `s`.  It gives

```text
r_(i_1,p_2)[d] !=0,
r_(i_2,p_1)[d] !=0.                                 (8)
```

Now transpose the two exceptional edges of `M_d`:

```text
M'_d=(M_d-{(i_1,p_1),(i_2,p_2)})
     union {(i_1,p_2),(i_2,p_1)}.                   (9)
```

This is a pure colour-`d` physical perfect matching.  It is genuinely
distinct from `M_d`: `i_1!=i_2`, the source assignments are transposed, and
all four mode-source cells are distinct.  It is not a recolouring of one
physical cell.  Equation (9) contradicts the assumption that `d` is
nonswitch.

Hence

```text
exactly one switchable colour at 3m+2 equality:
IMPOSSIBLE.                                          (10)
```

## Why the earlier cut-space countermodels survive abstractly

The one-switch cut normal form sees only the two endpoint fibres and their
component-overlap labels.  Abstract bridge or series-pair incidence graphs
can satisfy those equations.  They omit the two chord-extension coefficient
terms `F_1,F_2`.  In a physical permanent backbone, those terms force (8)
and switch the supposedly nonswitch colour.  Thus the obstruction comes
from pairwise Hamilton matching structure, not from additional gain
holonomy inside the two-fibre overlap graph.

## Literature translation

The proof is a matching-factorization argument.  Equality upgrades three
one-factors into a perfect one-factorization: every pair forms a Hamilton
cycle.  The elementary fact that a bipartite Hamilton-cycle chord extends
to a perfect matching then turns two local coefficient cancellations into a
new pure one-factor.

The unique-matching background is related to Kotzig's classical theorem;
see [*On the theory of finite graphs with a linear factor. I*](https://eudml.org/doc/29879).
The new problem-specific mechanism is the conversion

```text
Hamilton chord -> mixed backbone term -> localized cross cell -> pure switch.
```

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_equality_one_switch_exclusion_theorem.py
python audit_arbitrary_permanent_equality_one_switch_exclusion_theorem.py
```

The primary verifier checks the symbolic chord-path parity, switch-core
factor, and exceptional transposition.  The independent no-import audit
constructs a separate fixed Hamilton chord matching and its two-cell pure
switch.  These are fixed exact checks; the arbitrary-order theorem is the
component-selection, chord-extension, and localization proof above.

## Boundary

```text
pairwise selected pure unions:             HAMILTON CYCLES;
selected pure physical edge sharing:       NONE;
nonswitch exceptional edges:               HAMILTON CHORDS;
chord-extension mixed terms:               TWO;
forced nonswitch cross cells:               BOTH;
one-switch equality stratum:               EXCLUDED;
zero-switch equality stratum:              EXCLUDED PREVIOUSLY;
surviving equality stratum:                 EXACTLY TWO SWITCHES;
global Krenn--Gu conjecture:                UNRESOLVED.
```
