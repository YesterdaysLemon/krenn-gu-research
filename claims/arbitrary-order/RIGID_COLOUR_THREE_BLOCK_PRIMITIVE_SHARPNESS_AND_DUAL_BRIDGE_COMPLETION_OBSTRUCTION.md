# Rigid-colour three-block primitive sharpness and dual-bridge completion obstruction

## Status

This note proves an exact boundary for the globally rigid `r=1` route over
`C`, at every even order `n=2m>=8`.

The two-pair-plus-mediator binary primitive from the rigid-colour three-block
theorem is realizable by one alternating Hamilton cycle: all six proper block
unions have identically zero binary matching tensor, while the full tensor is
`Delta_(n,2)`.  Thus the primitive alone cannot yield an arbitrary-order
contradiction.

The same construction cannot be completed to the full globally rigid
physical system while keeping that Hamilton cycle as the entire binary
support.  Completing every missing physical pair as a pure-`c` edge violates
the rigid-colour annihilating deletion deck, equivalently the dual quadratic
bridge, on four consecutive vertices.

Nor can the construction be repaired by saturating either cycle shore with
arbitrary nonzero binary matrix-unit chords.  Those chords remain invisible
to the full tensor, but after deleting two vertices on the opposite shore
they produce distinct uniquely supported forbidden words.  The deletion
deck therefore fails without any possible cancellation.

This is a route-sharpness theorem, not a Krenn--Gu counterexample.  It does
not exclude a binary graph with additional support and exact cancellations,
the arbitrary-order globally rigid branch, the partial-flag branch, or the
global conjecture.  Global status remains **UNRESOLVED**.

## 1. The primitive

Let

```text
Omega={0,1,...,2m-1},       m>=4,
```

with indices modulo `2m`.  Let `H` have exactly the edges of the cycle

```text
0--1--2--...--(2m-1)--0.                               (1)
```

Its two alternating perfect matchings are

```text
M_a={01,23,...,(2m-2)(2m-1)},
M_b={12,34,...,(2m-1)0}.                               (2)
```

Give every edge of `M_a` the binary matrix unit `(a,a)`, every edge of
`M_b` the unit `(b,b)`, and every edge weight one.

Write the cycle bipartition as

```text
X={0,2,...,2m-2},       Y={1,3,...,2m-1}.              (3)
```

Choose disjoint two-sets `A,B subset X` and put

```text
C=Omega-(A union B).                                    (4)
```

Such a choice exists because `m>=4`.

### Theorem 1 (primitive sharpness)

The complete induced binary matching tensors satisfy

```text
T_H[A]=T_H[B]=T_H[C]=0,
T_H[A union B]=T_H[A union C]=T_H[B union C]=0,         (5)
T_H[Omega]=Delta_(n,2).                                 (6)
```

Every zero in (5) is structural: the relevant induced graph has no perfect
matching.  Consequently the six proper block-union equations of the
two-pair-plus-mediator primitive are consistent at every even order at least
eight.

### Proof

The sets `A`, `B`, and `A union B` lie in the independent cycle shore `X`,
so their induced graphs have no edges.

The induced graph on `C` has bipartition sizes `m-4` and `m`.  The graph on
`A union C=Omega-B` has sizes `m-2` and `m`, as does the graph on
`B union C=Omega-A`.  Each is bipartite with unequal shore sizes and hence
has no perfect matching.  This proves (5) coefficient by coefficient, with
no cancellation or characteristic assumption.

An even cycle has exactly the two perfect matchings in (2).  Their induced
words are the pure `a` and pure `b` words and both products are one.  This
proves (6).

The construction is therefore stronger than a scalar support example: its
entire coloured tensor has the required primitive values.

## 2. Failure of the naive physical completion

Now try to place the cycle inside a complete globally `c`-rigid matrix-unit
graph without changing `H`.  Global rigidity partitions every physical pair
into either a binary edge of `H` or a pure `(c,c)` edge of a scalar graph
`Z`.  Because (1) is assumed to be the entire binary support, every chord of
the cycle must be a nonzero `Z` edge.

### Theorem 2 (four-vertex completion obstruction)

No such completion satisfies the rigid-colour annihilating deletion system.
More precisely, on the four consecutive vertices

```text
Q={0,1,2,3},                                             (7)
```

one has

```text
haf(Z[Q])=Z_02 Z_13 !=0,                                (8)
```

while `H[Omega-Q]` has a nonzero pure-`a` perfect matching.  This contradicts

```text
haf(Z[Q])!=0  =>  T_H[Omega-Q] identically zero.         (9)
```

Equivalently, the dual quadratic bridge for the `Z` edge `02` and binary
colour `a` would require

```text
Z_02 Z_13 + Z_03 Z_12=0,                                (10)
```

but `Z_02,Z_13` are nonzero chords and `Z_12=0` because `12` belongs to
`M_b`.

### Proof

The cycle edges `01,12,23` belong to `H`, whereas `02,03,13` are chords and
therefore belong to `Z`.  The three terms in the four-vertex hafnian are

```text
Z_01 Z_23=0,       Z_02 Z_13!=0,       Z_03 Z_12=0,
```

which proves (8).

After deleting `Q`, the edges

```text
45,67,...,(2m-2)(2m-1)
```

form the restriction of `M_a` and give a nonzero pure-`a` coefficient of
`T_H[Omega-Q]`.  This contradicts (9).  The same calculation is the
four-hafnian identity (10) in the dual-bridge theorem.

No claim is made about a completion that adds further binary chords and
uses cancellation to preserve the full `Delta_2` tensor.  Such a completion
changes `H` and lies beyond this obstruction.

## 3. One-shore binary saturation also fails

It is natural to try to repair Theorem 2 by adding binary chords without
changing the full tensor.  Relabel the cycle shores as

```text
X={x_0,...,x_(m-1)},       Y={y_0,...,y_(m-1)},         (11)
```

so that

```text
M_a={x_i y_i:i mod m},
M_b={y_i x_(i+1):i mod m}.                              (12)
```

Add every edge `y_i y_j` to `H`, with an arbitrary nonzero matrix unit over
the binary alphabet `{a,b}` and an arbitrary nonzero weight.  Add no other
binary edge.

### Theorem 3 (one-shore saturation obstruction)

The augmented binary graph still satisfies

```text
T_H[Omega]=Delta_(n,2).                                 (13)
```

However, after deleting

```text
S={x_0,x_1},                                            (14)
```

the graph `H[Omega-S]` has exactly `m-1` perfect matchings.  They induce
`m-1` distinct binary words, each with a single nonzero monomial.  Hence

```text
T_H[Omega-S] is not identically zero.                   (15)
```

In any complete globally `c`-rigid physical completion, `x_0x_1` is not a
binary edge and must therefore be a nonzero pure-`c` edge.  Thus
`haf(Z[S])!=0`, and (15) contradicts the annihilating deletion deck.

### Proof

A perfect matching of all `2m` vertices cannot use a `Y--Y` chord.  If it
used `q>0` such chords, the remaining graph would have all `m` vertices of
`X` but only `m-2q` vertices of `Y`, and there are no `X--X` edges.  Thus the
only full perfect matchings remain `M_a` and `M_b`, proving (13).

After deleting `x_0,x_1`, the two shores have sizes `m-2` and `m`, so every
perfect matching uses exactly one `Y--Y` chord.  The cycle neighbours of
`y_0` were precisely `x_0,x_1`; therefore the chord must be

```text
y_0 y_j,       1<=j<=m-1.                              (16)
```

For each `j`, deleting `y_0,y_j` leaves two even paths in the cycle, each
with a unique perfect matching.  On the ordered surviving `X` vertices
`x_2,...,x_(m-1)`, the induced word is

```text
b^(j-1) a^(m-1-j).                                     (17)
```

These `m-1` patterns are pairwise distinct, independently of the endpoint
labels on the chord.  Every coefficient therefore contains exactly one
nonzero monomial, proving (15) over any field.

The same argument applies after interchanging `X` and `Y`.

## 4. Consequence for the proof programme

Theorem 1 refutes the proposed implication

```text
three-block primitive  =>  contradiction for arbitrary mediator.          (18)
```

Theorem 2 shows exactly why this does not create a witness.  The primitive
forgets the complement relation between the scalar graph `Z` and binary graph
`H`.  That relation is already detected by a four-vertex dual bridge.

Therefore a viable arbitrary-order rigid-colour proof must use at least one
of:

```text
the full Z/H complement partition;
the dual quadratic bridges for all Z edges and both binary colours;
the complete annihilating principal-deletion deck;
cancellation constraints introduced by additional binary chords.          (19)
```

Pure block-union nullity, even at all six unions, is insufficient.
Theorem 3 excludes the specific repair obtained by saturating exactly one
shore and adding no other binary edges.  It does not exclude partial
same-shore support, support on both shores, or added noncycle cross-shore
edges; any survivor must still satisfy the dual bridge/deletion equations.

## Scope and provenance

The primitive and dual bridges are imported from
[`RIGID_COLOUR_THREE_BLOCK_BINARY_PRIMITIVE_AND_QUADRATIC_BRIDGE_THEOREM.md`](RIGID_COLOUR_THREE_BLOCK_BINARY_PRIMITIVE_AND_QUADRATIC_BRIDGE_THEOREM.md).
The exact rigid-colour factorization and annihilating deletion deck are
imported from
[`RIGID_COLOUR_COFACTOR_ANNIHILATION_AND_BACKBONE_CANCELLATION_BOUNDARY.md`](RIGID_COLOUR_COFACTOR_ANNIHILATION_AND_BACKBONE_CANCELLATION_BOUNDARY.md).

```text
primitive-alone arbitrary-order exclusion:          REFUTED;
Hamilton primitive at every even n>=8:              EXACT;
naive complete rigid physical completion:           EXCLUDED;
one-shore binary saturation:                         EXCLUDED;
completion with extra cancelling binary support:    UNKNOWN;
arbitrary-order globally rigid branch:              UNKNOWN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

## Focused checks

Run from repository root:

```text
python claims/arbitrary-order/verify_rigid_colour_three_block_primitive_sharpness.py
python claims/arbitrary-order/audit_rigid_colour_three_block_primitive_sharpness.py
```

The primary check reconstructs the sparse coloured cycle tensors, the
four-vertex completion failure, and one-shore saturation for small
representative orders.  The independent no-import audit checks the shore
counts, forced chord, residual path matchings, and staircase words using a
separate representation.  These are bounded convention checks; the
arbitrary-order theorem is the written parity and cycle argument.
