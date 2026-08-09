# Arbitrary permanent equality zero-switch exclusion theorem

## Status

This is an exact arbitrary-order exclusion of the `3m+2` equality branch in
which every colour has a unique pure perfect matching.  It applies for every
`m>=3` over characteristic zero and uses no support, word, or matching
enumeration.

The proof has three structural steps.

1. Every full colour-eligibility graph has a unique-matching triangular form
   with at most two nonmatching edges.
2. Exceptional-source rectangle cancellation forces every pair of pure
   colour matchings to form one Hamilton cycle.
3. The two exceptional sources then impose disjoint nonempty colour sets on
   all mixed backbone matchings.  One set is a singleton, but a chord of the
   Hamilton cycle formed by the other two colours constructs a mixed matching
   avoiding the supposedly forced singleton-colour edge.

Thus a hypothetical equality restriction must have at least one and at most
two switchable colours.  The one- and two-switch branches remain unresolved.

## Full colour-eligibility graphs

Assume a hypothetical equality restriction

```text
P_m -> Delta_3,       support size 3m+2,       m>=3. (1)
```

Let `p_1,p_2` be the two exceptional sources.  For each colour `c`, define
the full eligibility graph

```text
G_c={(i,p):r_(i,p)[c]!=0}.                           (2)
```

It contains the `m` mandatory coordinate colour-`c` cells and at most the
two nonmandatory cells.  Hence

```text
|E(G_c)|=m+t_c,       0<=t_c<=2.                    (3)
```

In the zero-switch branch, `G_c` has one perfect matching `M_c`.  Every
source outside `p_1,p_2` has degree one in `G_c`, because all nonmandatory
cells have exceptional sources.  Its mandatory edge is therefore forced in
`M_c`.  These `m-2` forced edges occupy distinct modes.  After deleting them,
the matching problem has only the two exceptional sources and the two
remaining modes.

Equivalently, contract `M_c` and orient each nonmatching edge from its mode
pair to its source pair.  The dependency digraph has at most two arcs by
(3), and uniqueness of `M_c` makes it acyclic.  This is the full-support
Dulmage--Mendelsohn triangular normal form.

If

```text
i_(c,s)=M_c^(-1)(p_s),       s=1,2,                 (4)
```

then the two cross entries

```text
r_(i_(c,1),p_2)[c],
r_(i_(c,2),p_1)[c]                                  (5)
```

cannot both be nonzero: exchanging them would give a second perfect
matching of `G_c`.  More generally, a ratio state `(i,c)` consumes the
nonmatching entries at both exceptional sources unless one is the selected
edge (4).  With at most two nonmatching entries, two distinct ratio states
would force both crosses in (5).  Therefore each colour has at most one
nonisolated exceptional ratio state.

## Exceptional-port rule

Put

```text
H=M_0 union M_1 union M_2.                           (6)
```

For any nonmonochromatic perfect matching `F` in this coloured backbone,
the exceptional-source rectangle theorem supplies its unique cross partner.

The colours of the two `F`-edges incident to `p_1,p_2` must be distinct.
Indeed, if both had colour `c`, they would be the two selected `M_c` edges
in (4).  The required cross partner would make both entries (5) nonzero and
therefore create a second pure colour-`c` matching.

There is a stronger port rule.  A fixed colour `c` cannot occur at `p_1` in
one mixed backbone matching and at `p_2` in another.  The first rectangle
would require the first cross entry in (5), and the second would require the
other.  Again `G_c` would acquire a pure switch.

Let

```text
A_s={colours used at p_s by mixed perfect matchings of H}. (7)
```

Then

```text
A_1 intersect A_2=empty.                             (8)
```

After suppressing parallel cancellation edges, the gain graph consequently
has at most three active vertices, one per colour, and is a forest.  Its
Laurent gain ideal `<g_u+g_v:uv in E>` is prime: on each tree component all
variables are `+/-` one free nonzero parameter.  Thus gain or toric holonomy
alone cannot exclude this branch; the matching structure below is essential.

## Pairwise Hamilton lemma

For any distinct colours `a,b`, the coloured two-factor

```text
M_a union M_b                                         (9)
```

is one alternating Hamilton cycle.

Proof.  Decompose (9) into alternating components, retaining parallel
coloured copies until a full matching is chosen.

- If `p_1,p_2` lie in the same component and another component exists,
  choose `M_a` on their component and `M_b` on another.  Choose either colour
  on any remaining components.  The result is a nonmonochromatic backbone
  matching using colour `a` at both exceptional sources, contradicting the
  exceptional-port rule.
- If `p_1,p_2` lie in different components and at least three components
  exist, choose `M_a` on both marked components and `M_b` on a third.  The
  same contradiction follows.
- Suppose exactly two components remain, one exceptional source in each.
  The two complementary hybrid matchings use terminal colours `(a,b)` and
  `(b,a)`.  Their two required rectangle partners supply both cross entries
  (5) for colour `a` and both for colour `b`.  This creates pure switches in
  both colours, again impossible.

Thus (9) has one component.  Since `m>=3`, that component cannot be a
two-cycle of parallel coloured copies.  It is a spanning alternating cycle,
and in particular the three pure matchings are pairwise physically
edge-disjoint.

This is a perfect-one-factorization normal form forced by cancellation, not
an assumption about the support.

## Zero-switch exclusion

Bogdanov's theorem, as reported in Theorem 1.7 of Chandran, Gajjala, and
Illickan,
[*Krenn--Gu conjecture for sparse graphs*](https://arxiv.org/abs/2407.00303),
supplies a nonmonochromatic perfect matching of `H`, since `2m>4`.  Hence
both sets in (7) are nonempty.  They are disjoint subsets of three colours by
(8), so one is a singleton.  Relabel the sources and colours so that

```text
A_1={c}.                                             (10)
```

Every mixed perfect matching of `H` must then contain the fixed edge

```text
e=M_c intersect delta(p_1).                          (11)
```

Let `a,b` be the other two colours.  The pairwise Hamilton lemma makes

```text
C=M_a union M_b                                      (12)
```

an even Hamilton cycle.  Choose any

```text
f in M_c-{e},                                        (13)
```

which exists because `m>=3`.  Pairwise physical edge-disjointness makes `f`
a chord of `C` joining its opposite bipartition classes.

Every such chord extends to a perfect matching of `C union {f}`.  Delete
the endpoints of `f`.  They split the even cycle into two paths, each with
an even number of internal vertices because the chord endpoints lie in
opposite bipartition classes.  Take the alternating perfect matching on each
path and add `f`.

Call the resulting perfect matching `F'`.  It is a matching in `H`, it uses
the colour-`c` edge `f` and `m-1` edges of colours `a,b`, so it is
nonmonochromatic.  But it avoids `e`, since `e` is another `M_c` edge and no
`M_c` edge lies on `C`.  At source `p_1`, `F'` therefore uses colour `a` or
`b`, contradicting (10).

Consequently

```text
zero switchable colours at 3m+2 equality: IMPOSSIBLE. (14)
```

## Literature translation

The full-support normal form is the small-excess corner of unique-perfect-
matching and Dulmage--Mendelsohn theory; see Dulmage and Mendelsohn,
[*Coverings of Bipartite Graphs*](https://doi.org/10.4153/CJM-1958-052-0).
The new problem-specific step is the exceptional-port rule: complex
permanent cancellation converts a mixed terminal colour into a forbidden
pure switch.  That rule upgrades a two-factor decomposition into pairwise
Hamiltonicity and makes the elementary chord-extension argument decisive.

The proof deliberately separates three scopes:

- the unique-matching normal form concerns the full eligibility graph `G_c`;
- Hamiltonicity and the chord construction concern the selected backbone
  `H`;
- the bridge between them is the requirement that every mixed backbone term
  receive its physical exceptional-source rectangle cancellation.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_equality_zero_switch_exclusion_theorem.py
python audit_arbitrary_permanent_equality_zero_switch_exclusion_theorem.py
```

The primary verifier checks the physical `2 x 2` cross matching, port-set
pigeonhole, and an exact cycle-chord matching.  The independent no-import
audit encodes the component selections in all three cases of the Hamilton
lemma and reconstructs a separate chord matching.  These are fixed symbolic
checks, not a search; the scripts illustrate the finite logical moves but do
not replace the arbitrary-order proof above or the cited Bogdanov theorem.

## Boundary

```text
full colour graph outside exceptional ports:    FORCED MATCHING;
nonmatching edges per colour:                   AT MOST TWO;
same terminal colour in mixed backbone:         EXCLUDED;
one colour used at both exceptional ports:      EXCLUDED;
pairwise union of pure matchings:                HAMILTON CYCLE;
zero-switch equality stratum:                   EXCLUDED;
one-switch equality stratum:                    UNRESOLVED;
two-switch equality stratum:                    UNRESOLVED;
global Krenn--Gu conjecture:                     UNRESOLVED.
```
