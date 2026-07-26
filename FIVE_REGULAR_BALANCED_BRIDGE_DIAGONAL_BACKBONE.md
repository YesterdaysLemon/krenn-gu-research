# Maximum-degree-five balanced-bridge obstruction

## Status

This is an arbitrary-order exclusion theorem for every support of maximum
degree at most five in the simultaneous three-colour balanced all-bridge
normal form.  No such witness exists at any even order `n >= 6`.  This
does not prove the full Krenn--Gu conjecture: supports containing a vertex
of degree at least six and the deeper-blocker branches remain open.

The theorem strengthens
`FOUR_REGULAR_BALANCED_BRIDGE_OBSTRUCTION.md`: it excludes not only the
4- and 5-regular cases but also every mixture of support degrees at most
five.

## Setup

Use colours `0,1,2` and the eight coordinate normal types

```text
f_i(c) in {0,1,2} minus {c}.
```

The simultaneous balanced-bridge intersection theorem says that an entry
`W_ij[r,s]` can be nonzero only if, for every colour `c`,

```text
(r,s)=(c,c), or r=f_i(c), or s=f_j(c).                 (1)
```

The singleton assertion used here is the composition of two earlier
theorems, rather than a consequence of the zero-pattern table alone.
First, the generic killer theorem supplies, for every vertex `i` and
target colour `c`, an incident nonzero block

```text
A_i^c transpose(e_c).
```

Second, the balanced all-bridge reduction proves that its selected primary
vector `A_i^c` is a coordinate vector different from `e_c`.  With the
normal notation above it is proportional to `e_(f_i(c))`.  After absorbing
the nonzero scalar, the chosen block is therefore supported only at

```text
(f_i(c),c).
```

Since `f_i(c) != c`, this is an off-diagonal singleton block.  The three
target colours require three distinct incident blocks by the generic
killer theorem: the nonzero image of one block transpose cannot lie in
two different coordinate lines.  Condition (1) also makes each such
singleton reciprocal at its other endpoint.

Assume the essential support skeleton has maximum degree at most five.
Define the diagonal backbone `D` to have the same vertices and precisely
those skeleton edges `ij` for which at least one entry

```text
W_ij[c,c]
```

is nonzero.

## Theorem

For every hypothetical witness of maximum support degree at most five in
the simultaneous balanced all-bridge normal form:

1. every vertex has diagonal-backbone degree one or two;
2. every connected component of `D` is an even path or an even cycle;
3. on an even path, the unique graph-theoretic perfect matching consists
   of edges on which all three diagonal entries are nonzero;
4. on an even cycle, for each colour `c`, at least one of the two
   alternating parity matchings consists entirely of edges with nonzero
   `(c,c)` entries;
5. every path-matching edge joins complementary normal types;
6. on each cyclic component, either

   - all three colours can be assigned to one parity, whose edges then
     carry all three diagonal entries, or
   - the colour choices split `2+1` between the two parities, so the
     majority-parity edges carry at least two fixed diagonal colours and
     the minority-parity edges carry at least the remaining fixed colour;
7. in the `2+1` case, every majority-parity edge also joins complementary
   normal types.
8. relative to any complementary-type matching `A`, an `A`-alternating
   cycle whose anchor-pair colouring uses at most two colours must in fact
   be monochromatic;
9. every pair-constant two-colour amplitude factors into principal
   hafnians on the two anchor-pair classes;
10. some nonconstant two-colour anchor-pair assignment has both principal
    hafnians nonzero, contradicting the target coefficient zero.

Consequently `D` contains a spanning perfect matching `A` joining
complementary normal types.  Every edge of `A` carries at least two
nonzero diagonal entries.  It carries all three on path components and
on `3+0` cycle components; only the minority-colour diagonal may be
absent on a `2+1` cycle component.

The same edge may contain additional entries allowed by (1).  The theorem
asserts the displayed nonzero diagonal entries, not that the backbone
blocks are diagonal matrices.

## Proof

At a fixed vertex, the three coordinate-primary killers are distinct
off-diagonal singleton blocks.  None contains a diagonal entry.  Every
diagonal edge at that vertex is among the remaining incident edges.
Since the support degree is at most five, therefore

```text
degree_D(i) <= degree_G(i) - 3 <= 2.                   (2)
```

For each colour `c`, the all-`c` target amplitude is one.  At least one
perfect-matching monomial in that amplitude is consequently nonzero.
Every edge of that matching has a nonzero `(c,c)` entry, so it lies in
`D`.  In particular every vertex meets `D`, and

```text
degree_D(i) >= 1.                                      (3)
```

Equations (2) and (3) already exclude a support vertex of degree at most
three.  Every vertex in a remaining hypothetical support has degree four
or five and diagonal degree one or two.

Equations (2) and (3) make every component of `D` a path or a cycle.
The nonzero monochromatic matching for any fixed colour restricts to a
perfect matching on each component.  Hence every component has even
order.

An even path has exactly one perfect matching.  The restriction of a
nonzero monochromatic matching must equal it for each of the three
colours.  Thus every edge of the path matching has all three diagonal
entries nonzero.

An even cycle has exactly two perfect matchings, its two alternating edge
parities.  For every colour, the restriction of some nonzero
monochromatic matching chooses one of them.  Three colour choices placed
into two parity classes are either `3+0` or `2+1`, which gives the stated
cycle alternatives.

Finally, direct application of (1) to the eight normal types shows that
all three diagonal positions are simultaneously permitted exactly for
the eight ordered complementary pairs

```text
100 <-> 221,
101 <-> 220,
120 <-> 201,
121 <-> 200.
```

Every path-matching edge therefore joins complementary normal types.

It remains to prove the stronger complementary-type statement in a
`2+1` cycle.  By permuting colours, suppose the majority colours are
`0,1` and the minority colour is `2`.  Encode a normal type by three bits

```text
b0 = 0 for f(0)=1,  b0 = 1 for f(0)=2,
b1 = 0 for f(1)=0,  b1 = 1 for f(1)=2,
b2 = 0 for f(2)=0,  b2 = 1 for f(2)=1.
```

An edge permitting diagonals `0,1` must flip `b2`; on each of `b0,b1`
it cannot have endpoint pattern `11`.  An edge permitting diagonal `2`
cannot have endpoint pattern `00` on either `b0` or `b1`.

Fix one of `b0,b1` around the alternating cycle.  If `a` majority edges
have pattern `00`, `p` majority edges flip, `q` minority edges flip, and
`b` minority edges have pattern `11`, then counting zero incidences once
through each parity gives

```text
2a + p = q,
```

while counting one incidences gives

```text
p = q + 2b.
```

Hence `a=b=0`.  Every edge flips that bit.  Applying this to both
`b0,b1`, every majority edge flips all three bits and therefore joins
complementary types.  The same proof applies after any colour
permutation.

## Two-colour alternating-cycle separation

There is a second exact consequence of the 64 type-pair table.  Orient a
complementary anchor pair as

```text
(f,bar(f))
```

and record which physical endpoint an alternating cycle uses to leave the
pair.  A cycle state is therefore

```text
(f, outgoing side, pair colour).
```

If the next state is `(g,t,b)`, the external edge runs from side `s` of
the first pair to side `1-t` of the second.  It is structurally possible
only when entry `(a,b)` survives condition (1) between those two endpoint
types.

For any fixed two-colour set this gives a 32-state directed automaton.
Direct reconstruction gives

```text
384 directed transitions,
8 strongly connected components, each of size 4,
0 strongly connected components containing both colours.
```

Thus no closed alternating walk can change between the two colours.
This is an arbitrary-length conclusion: a directed edge lies on a closed
walk exactly when its endpoints lie in the same strongly connected
component.

The automaton has a useful amplitude corollary.  Let `A` be any
complementary-type perfect matching and let `g` be any pair-constant
colouring that uses at most two colours.  The matching `A` is only a
combinatorial reference here: its edges need not themselves support
`g`.  For a colour `c`, let `V_c` be the union of the anchor pairs
coloured `c`, and put

```text
L^c_ij = W_ij[c,c].
```

For every perfect matching `M` that supports `g`, every nontrivial
component of its symmetric difference with `A` is an `A`-alternating
cycle.  The automaton says that each component is monochromatic.  Common
edges of `M` and `A` also stay inside one anchor pair.  Hence `M` never
crosses between two distinct sets `V_c`, and the complete amplitude
factors exactly as

```text
T_W(g) = product over used colours c of haf(L^c[V_c]).       (4)
```

For every nonconstant such colouring the left side is zero.  Equation
(4) is therefore a family of complementary-principal-hafnian
orthogonality equations for every binary partition of the anchor pairs,
without an anchor-weight support hypothesis.

There is an immediate cofactor consequence.  Write `P` for the set of
anchor pairs and

```text
H_c(S) = haf(L^c[union of the pairs in S]).
```

Fix a pair `p` and a colour `d`.  At least two diagonal colours are
nonzero on the anchor edge `p`, so there is a colour `c != d` with
`H_c({p}) != 0`.  Colour `p` by `c` and every other pair by `d`.  The
target coefficient is zero, while (4) gives

```text
0 = H_c({p}) H_d(P \ {p}).
```

Therefore

```text
H_d(P \ {p}) = 0 for every colour d and every anchor pair p,   (5)
H_d(P) = 1 for every colour d.                                (6)
```

Thus all anchor-pair-deleted principal hafnian cofactors vanish even
though every full principal hafnian is one.  Equations (4)--(6) still do
not alone force an individual proper factor to be nonzero: cancellation
inside a monochromatic class is the precise remaining obstruction to
turning the two-colour separation into a one-term proof.

No cancellation, positivity, genericity, or choice of numerical weights
is used.  The only amplitude fact is that a nonzero sum contains at least
one nonzero monomial.

## No-cancellation contradiction

The degree-two backbone removes the apparent cancellation obstruction.
For each anchor pair `p`, let

```text
C_p = {c : the anchor edge p has nonzero entry (c,c)}.
```

The backbone theorem gives `|C_p| >= 2`.  Choose two distinct anchor pairs
`p,q`.  Select `c in C_p` and `d in C_q` with `c != d`; this is always
possible because both lists have size at least two.  Every other list
`C_r` meets `{c,d}`, since a subset of a three-element colour set with
size at least two cannot omit both.  Hence there is a nonconstant
pair-colouring `g` using only `c,d`, supported by the anchor edge at every
pair.

It remains to show that both factors in (4) are nonzero.  Fix a colour
`e` and a connected component `K` of `D`.

- If the `e`-coloured class contains every anchor pair of `K`, its factor
  is `haf(L^e[K])`.  Since `L^e` has no nonzero entries between distinct
  components of `D`,

  ```text
  1 = haf(L^e) = product over components K of haf(L^e[K]).
  ```

  Thus every full-component factor is nonzero.
- If the class contains a proper subset of the anchor pairs of `K`, the
  induced subgraph is a disjoint union of paths.  Each path begins and
  ends with a selected anchor edge and has that set of anchor edges as
  its unique perfect matching.  Its hafnian is therefore exactly the
  product of the selected nonzero `(e,e)` anchor weights.

This applies independently to every component and to both nonempty
colour classes.  Consequently

```text
haf(L^c[V_c]) != 0,
haf(L^d[V_d]) != 0.
```

Equation (4) makes `T_W(g)` their nonzero product, whereas the
nonconstant target coefficient requires `T_W(g)=0`.  This contradiction
excludes every maximum-degree-five simultaneous balanced all-bridge
support at every even order `n >= 6`.

## Exact local tables

Across the 64 ordered endpoint-type pairs, the number of structurally
permitted diagonal entries has distribution

```text
0 diagonals:  2 pairs
1 diagonal:  24 pairs
2 diagonals: 30 pairs
3 diagonals:  8 pairs
```

For any fixed one-colour set, exactly 36 ordered pairs permit it.  For any
fixed two-colour set, exactly 18 ordered pairs permit both colours.  All
three colours are permitted on exactly the eight complementary ordered
pairs.

These counts give a finite transition alphabet for the cyclic `2+1`
branch.  The bit-incidence proof further removes every noncomplementary
two-colour transition from a closed alternating component, even though
such transitions occur in the local 18-pair table.  The path/cycle
support argument above then eliminates cancellation and completes the
maximum-degree-five contradiction.

## Independent audits

Run:

```text
python verify_five_regular_balanced_bridge_diagonal_backbone.py
python audit_five_regular_balanced_bridge_diagonal_backbone.py
```

The primary verifier reconstructs condition (1), all 64 diagonal sets,
reciprocity of every allowed off-diagonal singleton, the subset-transition
counts, the path/cycle matching statements, and a finite-state proof that
no noncomplementary majority transition belongs to a closed alternating
type walk of any length.  It also constructs the 32-state two-colour
anchor automata and verifies that no colour-changing transition belongs
to a directed cycle.

The second program does not import the first.  It builds the normal types
from binary choices, tests each matrix unit directly on the six
coordinate-plane restrictions, and recursively enumerates path and cycle
perfect matchings in a separate implementation.

The finite path/cycle and proper-subset enumerations are regression checks
of the elementary arbitrary-order matching argument above.  Both output
records retain

```text
"global_conjecture_resolved": false
```

because supports containing a vertex of degree at least six and the
deeper-blocker branch remain unresolved.

## New boundary

The simultaneous balanced all-bridge branch now has no support of maximum
degree at most five at any even order.  A remaining witness must therefore
contain a support vertex of degree at least six.  The double-star analysis
also retains its separate deeper-blocker branch.  The exact bit balance
of three chosen monochromatic matchings at the next diagonal-degree
boundary is in
`THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md`.
