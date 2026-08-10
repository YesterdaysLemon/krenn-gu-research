# All-bridge active-deck exclusivity and cubic-diagonal exclusion

## Status

This is an exact arbitrary-order theorem over characteristic zero for the
simultaneous three-colour balanced all-bridge branch.  It closes the whole
maximum-diagonal-degree-three boundary, including the previously open case in
which two selected monochromatic matchings share an edge.  It assumes the
all-bridge reduction and does not apply to the separate deeper-blocker branch.

The theorem is not a proof of the global Krenn--Gu conjecture.  A remaining
all-bridge witness must have a vertex incident with at least four physical
edges carrying saturated diagonal entries; the deeper-blocker alternative and
the all-bridge `Delta(D)>=4` boundary remain open.

## Exact inherited hypotheses

Let `V` have even size `n=2m>=6`.  In the simultaneous balanced all-bridge
normal form, let `Z^c`, `c in {0,1,2}`, be the symmetric matrix of saturated
colour-`c` diagonal entries.  The previously proved diagonal-balance,
zero-layer, and convolution-split theorems give

```text
haf(Z^c[V]) = 1,                                      (1)
```

and, for distinct colours `c,d` and every nonempty proper even subset
`A subset V`,

```text
haf(Z^c[A]) haf(Z^d[V-A]) = 0.                        (2)
```

Equation (2) is the exact coefficient of the zero-layer colouring which is
constant `c` on `A` and constant `d` on its complement.  Indeed, if both
hafnians were nonzero, choose one nonzero monomial from each and concatenate
them.  The resulting zero-potential mixed-colour monomial invokes the
universal zero-layer theorem, under which the whole coefficient is exactly
the product in (2); the target coefficient is zero.  No positivity,
genericity, support enumeration, or division by a possibly zero hafnian is
used below.

For an edge `e={i,j}`, define its colour-`c` complementary cofactor and
active-deck score by

```text
C_e^c = haf(Z^c[V-{i,j}]),
D_e^c = Z_e^c C_e^c.                                  (3)
```

Call `e` **deck-active in colour `c`** when `D_e^c!=0`, and write `E_c` for
the graph of such edges.

## The active-deck theorem

For every vertex `i` and colour `c`,

```text
sum_(j!=i) D_{ij}^c = 1.                              (4)
```

Consequently every `E_c` spans `V` and has no isolated vertex.  Moreover, if
`e` is deck-active in colour `c`, then for every `d!=c`,

```text
Z_e^d = 0,            C_e^d = 0.                      (5)
```

In particular, the three physical edge sets

```text
E_0, E_1, E_2
```

are pairwise disjoint.  Every edge in `E_c` belongs to at least one nonzero
colour-`c` perfect-matching monomial: `Z_e^c!=0`, and the nonzero cofactor
`C_e^c` contains a nonzero perfect-matching monomial in its finite expansion.

### Proof

Equation (4) is Laplace expansion of the full hafnian (1) at the prescribed
vertex `i`.  Since the sum is one, at least one incident score is nonzero.

Now fix a deck-active `e={i,j}` in colour `c` and another colour `d`.  Apply
(2) in both orientations to `A={i,j}`:

```text
Z_e^d C_e^c = 0,
Z_e^c C_e^d = 0.                                      (6)
```

Deck activity says both `Z_e^c` and `C_e^c` are nonzero, so (6) gives (5).
If one physical edge were active in two colours, (5) for either colour would
contradict the nonzero diagonal entry required by activity in the other.
This proves the theorem.

## Shared selected edges force diagonal degree four

Choose one nonzero monochromatic perfect-matching monomial `M_c` in each
colour, as in the diagonal-matching balance theorem.  Suppose a physical edge
`p` is shared by `M_a` and `M_b`, with `a!=b`.  Then

```text
Z_p^a != 0,            Z_p^b != 0.                    (7)
```

Equation (2), applied to the two orientations of the cut `p`, gives

```text
C_p^a = C_p^b = 0.                                    (8)
```

Thus `p` lies in neither `E_a` nor `E_b`.  It cannot lie in the third active
graph either, because (5) would contradict both nonzero entries in (7).

At either endpoint `v` of `p`, use (4) to choose an incident edge

```text
e_c in E_c       for c=0,1,2.
```

The three `e_c` are physically distinct by (5), and none equals `p` by
(5), (7), and (8).  Hence each endpoint of a shared selected edge is incident
with at least four distinct physical diagonal-support edges:

```text
deg_D(v) >= 4.                                        (9)
```

Here `D={e : Z_e^c!=0 for some c}` is the physical graph of edges carrying at
least one saturated diagonal entry.  Statement (9) is local at both endpoints
and has no total support-degree assumption.

## Exclusion of the cubic diagonal boundary

Assume for contradiction that the physical saturated-diagonal graph satisfies

```text
Delta(D) <= 3.                                        (10)
```

No two selected matchings can share an edge, by (9).  Therefore
`M_0,M_1,M_2` are pairwise physically edge-disjoint.  Their union already has
degree three at every vertex and hence exhausts `D` under (10).

This last conclusion follows directly from (2)--(5), without invoking a
degree bound on the full (possibly nonsaturated) diagonal support.  At a
vertex `v`, write `p_t(v)` for its incident edge in `M_t`.  Fix `c`.  For
each `t!=c`, apply (2) with colour `t` on the two-point set `p_t(v)` and
colour `c` on its complement.  Since `Z^t_{p_t(v)}!=0`, this gives

```text
C^c_{p_t(v)} = 0.                                    (11)
```

Every nonzero summand in the colour-`c` Laplace sum (4) lies on `D`.
The union `M_0 union M_1 union M_2` exhausts `D`, and (11) kills the two
summands at `v` belonging to colours other than `c`.  Therefore

```text
D^c_{p_c(v)} = 1.                                    (12)
```

Thus every edge of `M_c` is active in colour `c`; active-deck exclusivity
(5) kills its entries in the other saturated colours.  Since the selected
matchings exhaust `D`, it follows that

```text
support(Z^c) = M_c.                                   (13)
```

The selected coloured cubic graph has three differently coloured perfect
matchings.  Bogdanov's nonmonochromatic-perfect-matching theorem, in the form
used by the existing universal zero-layer theorem, supplies a
nonmonochromatic perfect matching `F` because `n>4`.  Let `chi` be its induced
vertex colouring.

Every monomial contributing to the coefficient of `chi` is confined to the
saturated zero layer by the universal potential theorem.  But (13) makes `F`
the unique zero-layer matching inducing `chi`: at a vertex coloured `c`, its
edge is forced to be the sole incident `M_c` edge.  The coefficient is
therefore the one nonzero monomial of `F`, while the Krenn--Gu target requires
it to vanish.  This contradiction proves

```text
every simultaneous balanced all-bridge witness has
Delta(D) >= 4.                                        (14)
```

This uses the arbitrary-order matching theorem only through the already
proved zero-layer dependency.  The primary and independent programs named
below are bounded sanity checks of the hafnian Laplace identity, the
two-colour cut implications, the local degree count, and uniqueness on the
cubic layer; the displayed symbolic proof is the theorem.

## Dependency and scope ledger

The load-bearing inputs are:

1. [`THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md`](THREE_COLOUR_DIAGONAL_MATCHING_BALANCE_THEOREM.md): the simultaneous balanced all-bridge normal form and saturated pure
   matching setup (no full-support degree conclusion is imported);
2. [`UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md`](UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md): nonnegative universal potential, zero-layer confinement, and the
   Bogdanov matching input;
3. [`HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md`](HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md): the mixed complementary-product equation (2).

Focused checks:

```text
python claims/arbitrary-order/verify_all_bridge_active_deck_exclusivity_and_cubic_diagonal_exclusion.py
python claims/arbitrary-order/audit_all_bridge_active_deck_exclusivity_and_cubic_diagonal_exclusion.py
```

The second script shares no imports with the first.

## Boundary

```text
active deck at every vertex and colour:       PROVED;
active physical edge sets across colours:     PAIRWISE DISJOINT;
shared selected edge endpoint degree:         AT LEAST FOUR;
all-bridge maximum diagonal degree <=3:       EXCLUDED;
all-bridge Delta(D)>=4 boundary:               UNKNOWN;
deeper-blocker branch:                        UNKNOWN;
forced sparse P5/P6/P7 extraction:            NOT PROVED;
global Krenn--Gu conjecture:                   UNRESOLVED.
```
