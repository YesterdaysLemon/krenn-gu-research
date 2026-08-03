# Arbitrary permanent three-excess port-permutation theorem

## Status

This is an exact arbitrary-order normal form for the first support layer
permitted by the strict `3m+3` bound.  Assume a characteristic-zero
restriction

```text
P_m -> Delta_3,       support size exactly 3m+3,      m>=3. (1)
```

Choose the mandatory tricolour coordinate cover.  The three remaining cells
have either two or three distinct source endpoints.  Every alternative term
for a fixed backbone word agrees outside those exceptional sources and is
obtained by one transposition or one three-cycle of their port assignments.
Consequently every coefficient of a word induced by the chosen backbone has
at most six physical matching terms.  Pure words are sharper: every colour
has at most two perfect matchings, so the pure backbones form a Boolean cube
of dimension at most three and number at most eight, independent of `m`.

This replaces any support or word census by an `S_2` or `S_3` boundary
permutation problem.  It does not exclude the `3m+3` layer or prove the
global Krenn--Gu conjecture.

## Mandatory cover and exceptional sources

The singleton tricolour-cover theorem supplies one mandatory coordinate cell

```text
b_(p,c)=alpha_(p,c) e_c^*,       alpha_(p,c)!=0,     (2)
```

for every source `p` and colour `c`.  These `3m` physical cells form a
mandatory cover `B`.  Let `E` be the three remaining cells and let

```text
P_*={source endpoints of cells in E},
k=|P_*|<=3.                                          (3)
```

Choose one pure matching `M_c` for each colour and put

```text
H=M_0 union M_1 union M_2.                           (4)
```

Coloured states of one noncoordinate physical cell are retained while a
backbone matching is chosen and collapsed before permanent terms are
compared.

## Three-excess localization lemma

Fix a perfect matching `F` in `H` and its induced input word.  Every physical
cell eligible for that word but different from its designated backbone cell
has source endpoint in `P_*`.

Indeed, an eligible cell in `E` has such an endpoint by definition.  Otherwise
it is a mandatory coordinate cell `b_(p,c)` omitted from the selected pure
matching `M_c`.  Since `M_c` still matches source `p`, it uses another
colour-`c` eligible cell there.  No other cell of the mandatory cover at
source `p` has a `c` component, so that replacement belongs to `E`; hence
`p in P_*`.

This proof is identical for coordinate and noncoordinate excess cells.

## Exceptional-source count

In fact

```text
k in {2,3}.                                          (5)
```

Bogdanov's nonmonochromatic-matching theorem supplies a mixed perfect
matching `F` in `H` because `m>=3`.  Its target coefficient is zero, so it
requires a distinct physical perfect matching `G` for the same word.  After
physical collapse, `F symmetric-difference G` contains an alternating cycle.
Every such cycle uses at least two new physical cells with distinct source
endpoints.  The localization lemma puts those endpoints in `P_*`, proving
`k>=2`.

Thus the excess-source multiplicities are exactly

```text
k=2:  2+1,
k=3:  1+1+1.                                        (6)
```

## One-cycle permutation theorem

Let `G` be any other physical perfect matching for the input word of `F`.
Every edge of `G-F` has source in `P_*`.  The symmetric difference is a
disjoint union of alternating cycles, and each cycle consumes at least two
distinct exceptional sources.  Since `k<=3`, there is exactly one cycle.

Therefore `F` and `G` agree outside a subset `Q subset P_*` of size two or
three.  If `I=F^(-1)(Q)` is the corresponding set of port modes, `G` is
obtained by a single cyclic permutation of the assignments `I -> Q`:

```text
|Q|=2: one transposition;
|Q|=3: one of the two three-cycles.                  (7)
```

Across all possible choices of `Q`, the nonidentity alternatives are the
five nonidentity cyclic permutations in `S_3`:

```text
three transpositions and two three-cycles.           (8)
```

There cannot be two disjoint exchange cycles, a longer cycle, or a change
away from `P_*`.  Nor can two physical terms realize the same port
permutation, because a row cell is determined by its mode-source pair.

## Exact port polynomial

Freeze the common cells outside the exceptional ports and let their nonzero
monomial weight be `W_F`.  Enumerate the exceptional sources as
`p_1,...,p_k` and their `F`-preimage modes as `i_1,...,i_k`.  Put

```text
X_(r,s)=r_(i_r,p_s)[word_(i_r)].                     (9)
```

Interpret `X_(r,s)` as zero when the corresponding physical row cell is
absent.  The complete coefficient of this backbone-induced word is exactly

```text
W_F per(X)
=W_F sum_(sigma in S_k) product_(r=1)^k X_(r,sigma(r)). (10)
```

For `k=2`, (10) is the familiar two-term `2 x 2` permanent and has at most
two nonzero terms.  For `k=3`, it is

```text
per(X)=
X_11 X_22 X_33
+X_11 X_23 X_32
+X_12 X_21 X_33
+X_12 X_23 X_31
+X_13 X_21 X_32
+X_13 X_22 X_31,                                    (11)
```

with at most six nonzero terms.  Missing physical cells set entries to zero
and thereby delete the corresponding permutation monomials.  Equation (10)
is the entire coefficient, not a selected partial sum.

## Sharp pure matching bound

Fix one pure colour-`c` matching `M_c`.  Its full physical eligibility graph
has the `m` mandatory colour-`c` cells and at most three excess cells with a
nonzero `c` component.  If exactly `t_c` excess cells are eligible, the graph
has `m+t_c` cells.  Identify each mode `i` with the source `M_c(i)` matched
to it.  After the `m` cells of `M_c` are contracted, exactly `t_c<=3` unused
cells remain as directed nonmatching arcs: an unused cell `(i,p)`, with
`q=M_c(i)`, becomes the source arc `q -> p`.

There are no loops, because another cell at the same mode--source position
would be the same physical cell as the matching cell, and no parallel arcs,
because a mode--source position determines one physical cell.  Perfect
matchings of the eligibility graph are in bijection with vertex-disjoint
collections of directed cycles in this dependency digraph.

A loopless directed graph with at most three arcs contains at most one
directed cycle.  Indeed, two disjoint cycles use at least four arcs.  If two
distinct cycles meet, delete their common directed paths; one divergence and
reunion already leave two distinct return routes, whose union again has at
least four arcs.  Any unique cycle has length two or three.

It follows that the only possible pure alternative to `M_c` is the switch
along that unique cycle.  In the physical bipartite graph it is one
alternating four- or six-cycle.  Therefore

```text
number of pure physical matchings per colour <=2,
number of pure backbone choices <=2^3=8.             (12)
```

The pure-backbone choice space is thus a Boolean cube of dimension at most
three.  This is a symbolic dependency-digraph theorem, not an invitation to
enumerate its at most eight vertices.  The six-term `S_3` bound remains
necessary for general mixed words induced by a selected backbone.

## Pure three-cycle geometry

Suppose `k=3`, write the unique excess cell at source `p_s` as
`e_s=(a_s,p_s)`, and suppose colour `c` has a three-cycle switch.  At each
exceptional source, the two pure matchings use the only two `c`-eligible
cells, namely `e_s` and `b_(p_s,c)`.  Consequently

```text
{e_s,b_(p_s,c):s=1,2,3}                             (13)
```

is their physical alternating six-cycle, and all three excess covectors
have nonzero `c` component.

Each of the three cycle modes has degree two in (13).  If `h_u` counts
excess edges at one such mode, then `h_u<=2` and `sum h_u=3`.  The excess-
mode occupancy is therefore `1+1+1` or `2+1+0`; three co-located excess
cells cannot support a pure three-cycle.

If the excess modes are distinct, the three mandatory cells in (13) are one
of the two derangements between those modes and sources.  The two
derangements are pointwise disjoint, so at most two colours can have a
three-cycle switch.  In the `2+1+0` case, relabel so that `e_1,e_2` share
mode `u`, `e_3` has mode `v`, and `w` is the third cycle mode.  The mandatory
cell `b_(p_3,c)` is forced to `(w,p_3)`.  Both possible completions share
that cell, so at most one colour can have a three-cycle switch.

These are monochromatic pure-switch restrictions.  A general mixed
fixed-port bypass may use three different word colours, so this geometry
does not by itself exclude the bypass matrix below.

## Sharp incidence witness for the three-dimensional pure cube

No further reduction of the Boolean-cube dimension follows from the cover,
local rank, and pure coefficients alone.  At `m=4`, take modes
`a,b_0,b_1,b_2`, sources `p_1,...,p_4`, and excess covectors

```text
e_1=(a,p_1):(1,1,1),
e_2=(a,p_2):(1,2,3),
e_3=(a,p_3):(1,3,2).                                (14)
```

Their determinant is `-3`.  Place the mandatory coordinate cells as

```text
b_0: (p_1,0),(p_2,0),(p_3,1),(p_4,2),
b_1: (p_1,1),(p_2,1),(p_3,2),(p_4,0),
b_2: (p_1,2),(p_2,2),(p_3,0),(p_4,1).               (15)
```

Every source has all three mandatory colours.  Mode `a` has rank three and
degree three; each `b_c` has rank three and degree four.  In colour `c`, the
cells at `p_3,p_4` are forced, while `a,b_c` may be matched to `p_1,p_2` in
either order.  Thus each colour has exactly two pure matchings and all three
switches coexist.  Their pure coefficients are nonzero with the displayed
weights.

This is an incidence/local-rank/pure-coefficient model, not a solution of
the mixed equations and not a `P_4 -> Delta_3` restriction.  It proves that
excluding the three-switch face requires mixed-coefficient information.

## Sharp fixed-port bypass countermodel

The old two-source Hamilton-chord proof does not extend formally to three
exceptional sources.  A boundary coefficient can cancel while leaving its
distinguished chord row fixed.

For any `t!=0`, take

```text
    [ 1  0  0 ]
L = [ t  1  1 ].                                    (16)
    [ 0 -1  1 ]
```

The diagonal is nonzero and the three off-diagonal nonzero cells have all
three source endpoints.  Nevertheless

```text
per(L)=1-1=0.                                        (17)
```

The only partner of the diagonal term is the transposition of ports `2,3`.
It fixes row `1`, while `L_12=L_13=0`.  Thus a chord-extension matching
using the first diagonal cell can cancel without producing any cross cell
for that chord.

This is an exact three-port boundary signature consistent with localization
and the three-excess count.  It is not a full `P_m -> Delta_3` construction.
It proves that localization, support count, and Hamilton chords alone cannot
exclude the next layer.

## Complementary-minor forcing lemma

For a chord extension at exceptional source `p_s`, order its boundary matrix
`L^(s)` so that the distinguished pure-colour chord is diagonal cell `(s,s)`.
The complete amplitude of the channel that retains that chord is

```text
D_s=L^(s)_(s,s) per(L^(s)_(hat s,hat s)).            (18)
```

Therefore the sharp sufficient condition

```text
per(L^(s)_(hat s,hat s)) !=0                         (19)
```

forces some cancelling term to move row `s`: the full mixed coefficient is
zero, while its fixed-row channel (18) is nonzero.  Hence some cross cell

```text
r_(M_e^(-1)(p_s),p_t)[e] !=0,       t!=s,            (20)
```

must exist.

If (19) holds for chord extensions at all three exceptional sources, choose
one forced arc `s -> t` from (20) at each source.  A loopless directed graph
on three vertices with outdegree at least one contains a directed two- or
three-cycle.  Reassigning the selected pure `e` edges along that cycle gives
a second pure `e` perfect matching.

Thus a three-port Hamilton-chord argument succeeds once all three
complementary `2 x 2` permanents in (19) are proved nonzero.  Matrix (16)
shows that this is not a formal consequence of `per(L)=0`, diagonal
nonvanishing, or the support ledger.  Excluding these fixed-port bypass
rectangles is the exact new coefficient problem.

## Mode-degree ledger

Local concision forces at least three physical cells at each input mode.  If
`d_i` is the number at mode `i`, write

```text
d_i=3+epsilon_i,       epsilon_i>=0,
sum_i epsilon_i=3.                                  (21)
```

Thus the complete degree-excess partition is one of

```text
3,
2+1,
1+1+1.                                              (22)
```

Equations (5), (12), and (22) give a finite structural normal form at every
order: two or three exceptional sources, at most two pure choices per
colour, at most eight pure backbones, and three possible mode-excess
partitions.

## Literature translation

Perfect matchings are vertices of the assignment polytope, and their
symmetric differences are cycles.  Localization collapses the relevant face
to the permutation group on at most three ports.  The coefficient boundary
is therefore the group-algebra support of `S_2` or `S_3`, evaluated by a
bosonic permanent rather than a determinant or Pfaffian.

Changing which of these terms is distinguished is an `S_3` projective chart
action, not an additional coefficient equation.  The exact action and its
abelian-transport countermodels are in
`ARBITRARY_PERMANENT_THREE_EXCESS_B3_PHASE_HOLONOMY_NOGO.md`.

This is also a small matching-toric normal form: its cycle-exchange monomials
are indexed by transpositions and oriented three-cycles, and the complete
mixed coefficient may contain up to six terms.  The arbitrary-order graph
interior contributes a common monomial and no additional combinatorial
choices on the localized backbone face.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_three_excess_port_permutation_theorem.py
python audit_arbitrary_permanent_three_excess_port_permutation_theorem.py
```

The primary verifier checks the exact six-term `3 x 3` permanent, its cycle-
type grouping, the fixed-port bypass matrix and complementary-minor
expansion, the sharp pure-choice bounds, and the degree partitions.  The
independent no-import audit evaluates the six port monomials with exact
integers and separately checks the five nonidentity cycles and bypass
signature.  These are fixed boundary checks; the arbitrary-order theorem is
the localization and one-cycle proof above.

## Boundary

```text
mandatory coordinate cells:               3m;
excess physical cells:                     3;
exceptional sources:                       2 OR 3;
alternative cycles per backbone-word term: AT MOST ONE;
port exchange type:                        TRANSPOSITION OR THREE-CYCLE;
physical terms per H-induced coefficient:  AT MOST SIX;
pure matchings per colour:                  AT MOST TWO;
pure switch type:                           ONE C4 OR C6;
pure backbone choices:                     AT MOST EIGHT;
mode-excess partitions:                    3, 2+1, OR 1+1+1;
fixed-chord bypass at three ports:          POSSIBLE;
missing sufficient lemma:                  THREE NONZERO COMPLEMENT MINORS;
3m+3 equality existence:                   UNRESOLVED;
global Krenn--Gu conjecture:                UNRESOLVED.
```
