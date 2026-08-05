# Arbitrary permanent equality two-switch exclusion theorem

## Status

This is an exact arbitrary-order exclusion of the last possible `3m+2`
equality branch.  It applies for every `m>=3` over characteristic zero and
performs no support, word, or matching enumeration.

In the two-switch ledger, the switch colours share the common excess mode
`a`, and either pure switch can route `a` to either exceptional source.
Choose an opposite-source fibre.  The selected switch-colour
matchings then connect the exceptional sources through the length-two path
`p_1--a--p_2`.  Switch-core rigidity forces their whole two-factor to be a
Hamilton cycle.  The two exceptional edges of the unique nonswitch colour
are chords of that cycle; their mixed chord extensions force both cross
cells and switch the nonswitch colour, a contradiction.

Together with the zero- and one-switch exclusions and the pure-matching cube
theorem, this proves that no restriction `P_m -> Delta_3` has exactly
`3m+2` nonzero row cells.  The arbitrary permanent support lower bound is
therefore sharpened to `3m+3`.

## Setup and opposite-source fibre

Assume a hypothetical equality restriction

```text
P_m -> Delta_3,       support size 3m+2,       m>=3. (1)
```

Let `c,d` be the two switchable colours and `e` the unique nonswitch colour.
The pure-matching cube theorem gives:

- two noncoordinate excess cells at the common mode `a` and sources
  `p_1,p_2`;
- two pure matchings in each of colours `c,d`;
- the switch in either colour transposes the assignment of `a` and its
  mandatory partner mode to `p_1,p_2`;
- one unique pure matching `M_e`.

All four combinations of the two pure choices can be selected as coloured
backbones.  Choose `M_c,M_d` so that

```text
M_c(a)=p_1,        M_d(a)=p_2.                       (2)
```

The other opposite orientation is identical.  Equation (2) defines an
opposite-source fibre that necessarily occurs among the four backbone
choices.

## Switch-core rigidity with the other switch fixed

Fix either switch colour `h in {c,d}` and either choice of the other switch.
Write the four nonzero `h`-entries on its two exceptional modes and sources
as `A,B,C,D`, with the selected pure core using `AD` and its alternate using
`BC`.  After the common residual pure factor `W_h` is removed, the required
pure coefficient is

```text
lambda_h=W_h(AD+BC) !=0.
```

No nonmonochromatic matching in the selected backbone can use both selected
`h` core edges.  If one did, exceptional-source localization would make its
unique possible partner the same two-source transposition.  After factoring
its nonzero residual monomial `W_F`, the forbidden mixed coefficient would
be

```text
W_F(AD+BC) !=0,
```

a contradiction.  The other switch bit is fixed throughout this local
argument and changes neither factor.  Thus switch-core rigidity applies in
the present two-switch branch.

## Switch--nonswitch Hamilton factors

Both

```text
M_c union M_e,       M_d union M_e                  (3)
```

are spanning alternating Hamilton cycles.

For `M_c union M_e`, decompose the two-factor into alternating components.
If both exceptional sources lie in one component and another exists, choose
`M_c` on the marked component and `M_e` on another.  If they lie in distinct
components and at least three exist, choose `M_c` on both marked components
and `M_e` on a third.  Either selection is mixed and uses both selected `c`
switch edges, contradicting the nonzero pure switch factor.

The sole remaining disconnected case has exactly two components, one
exceptional source in each.  Its complementary hybrids have terminal colour
patterns `(c,e)` and `(e,c)`.  Their rectangle partners force both missing
`e` cross cells and create a second pure `e`-matching, contradicting that
`e` is nonswitch.  Thus `M_c union M_e` is Hamilton.  The same proof applies
to `M_d union M_e`.

Since `m>=3`, a shared physical cell would be an isolated coloured
two-cycle, incompatible with either single spanning component.  Therefore

```text
M_e is physically edge-disjoint from M_c and M_d.    (4)
```

## The opposite switch factor is Hamilton

The union `M_c union M_d` contains the alternating path

```text
p_1 --M_c-- a --M_d-- p_2.                          (5)
```

Hence both exceptional sources lie in the same alternating component.
Suppose another component existed.  Choose `M_c` on the component containing
(5) and `M_d` on any other component.  This gives a nonmonochromatic
backbone perfect matching that retains both selected `c` switch edges at
`p_1,p_2`.  Its forbidden coefficient has the same nonzero local factor as
the pure `c` coefficient, contradicting switch-core rigidity.

Consequently `M_c union M_d` has one component.  In the opposite-source
fibre the two matchings use distinct excess physical cells at `a`; outside
`a`, their cells are coordinate-only and of different colours.  Thus the
component is a genuine physical Hamilton cycle

```text
C=M_c union M_d.                                    (6)
```

There is no coloured-copy collapse hidden in (6).

## Nonswitch chords give the contradiction

For `s in {1,2}`, let

```text
i_s=M_e^(-1)(p_s),       f_s=(i_s,p_s).              (7)
```

By (4), each `f_s` is a genuine chord of the bipartite Hamilton cycle `C`.
Every such chord extends to a perfect matching: delete its endpoints, take
the alternating perfect matchings on the two even-vertex path interiors of
`C`, and adjoin the chord.  Call the resulting matching `F_s`.

Then

```text
F_s subset M_c union M_d union M_e.                  (8)
```

It contains the single `e` edge `f_s` and `m-1` selected `c/d` edges, so it
is mixed.  Exceptional-source localization says that cancellation of its
mixed coefficient requires the unique two-source transposition, and in
particular forces

```text
r_(i_s,p_(3-s))[e] !=0.                              (9)
```

Applying (9) for `s=1,2` supplies both cross cells.  The transposed matching

```text
M'_e=(M_e-{(i_1,p_1),(i_2,p_2)})
     union {(i_1,p_2),(i_2,p_1)}                    (10)
```

is a genuinely distinct pure colour-`e` physical perfect matching.  This
contradicts the assumption that `e` is nonswitch.

Therefore

```text
exactly two switchable colours at 3m+2 equality:
IMPOSSIBLE.                                          (11)
```

## Strict support corollary

The pure-matching cube theorem proves that equality has at most two
switchable colours.  The zero-switch, one-switch, and (11) theorems exclude
all three possibilities.  Hence

```text
P_m -> Delta_3 has no 3m+2-cell restriction.         (12)
```

The preceding arbitrary-order support theorem already gives at least
`3m+2` nonzero row cells.  Since support size is integral, (12) sharpens it
to

```text
every P_m -> Delta_3 restriction has at least 3m+3
nonzero row cells, for every m>=3.                   (13)
```

In particular, hypothetical restrictions of `P_5,P_6,P_7` require at least
`18,21,24` nonzero row cells respectively.  This is an exact strict support
theorem, not a proof of the full Krenn--Gu conjecture: larger-support
permanent restrictions and the graph-to-local contraction problem remain.

## Relation to the completed-shore theorem

The earlier Hall-shore analysis independently proves that a hypothetical
two-switch equality survivor would contain a residual perfect matching and
obey the cross-colour rectangle

```text
g_(b_c,c)=-g_(b_d,d).
```

Those scalar relations are consistent in an abstract four-state gain model.
The present proof bypasses that algebraic dead end: it uses an
opposite-source pure fibre and the two nonswitch chord coefficients.  Thus
the contradiction is topological matching exchange, not scalar monodromy.

## Literature translation

The proof combines two classical matching moves into a problem-specific
boundary obstruction:

1. componentwise exchange in a two-factor;
2. extension of a bipartite Hamilton-cycle chord to a perfect matching.

The common excess mode forces the exceptional sources into one component,
while permanent localization converts the two chord matchings into a
forbidden new one-factor.  This is naturally a perfect-one-factorization
and Kempe-exchange argument.  It requires neither a Pfaffian orientation nor
a matching census.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_equality_two_switch_exclusion_theorem.py
python audit_arbitrary_permanent_equality_two_switch_exclusion_theorem.py
```

The primary verifier checks the opposite-source length-two connection,
nonzero switch-core factor, symbolic chord parity, exceptional transposition,
and integral support increment.  The independent no-import audit constructs
a separate fixed Hamilton chord matching and checks the switch-core product
and two-cell pure switch.  These are fixed exact checks; the arbitrary-order
theorem is the component-selection, opposite-source, chord-extension, and
localization proof above.

## Boundary

```text
opposite-source pure fibre:                 EXISTS;
exceptional-source path through a:          FORCED;
opposite switch-colour two-factor:          HAMILTON CYCLE;
nonswitch exceptional edges:                HAMILTON CHORDS;
forced nonswitch cross cells:                BOTH;
two-switch equality stratum:                EXCLUDED;
all 3m+2 equality strata:                   EXCLUDED;
arbitrary permanent support lower bound:    3m+3;
larger-support permanent restrictions:      UNRESOLVED;
global Krenn--Gu conjecture:                 UNRESOLVED.
```
