# Arbitrary permanent equality exceptional-source rectangle theorem

## Status

This is an exact arbitrary-order refinement of the `3m+2` support bound.
It classifies the cancellation mechanism at equality for coordinate and
noncoordinate row cells alike.

For any hypothetical restriction `P_m -> Delta_3` with exactly `3m+2`
nonzero row cells, the two cells beyond a mandatory tricolour coordinate
cover must have two distinct source endpoints.  Every forbidden mixed
backbone coefficient must then cancel through one unique alternating
four-cycle supported on those two exceptional sources.  Equivalently, it
satisfies one exact `2 x 2` permanent equation whose cross-ratio is `-1`.

This reduces the whole equality stratum to a signed two-source rectangle
system.  It does not yet prove that every such system contains an odd sign
cycle, so equality and the global Krenn--Gu conjecture remain unresolved.
No support or word enumeration is used.

## Mandatory cover and two excess cells

Suppose

```text
P_m(phi_0(x_0),...,phi_(m-1)(x_(m-1)))=Delta_3.       (1)
```

By the singleton tricolour-cover theorem, choose one coordinate row cell

```text
b_(p,c)=alpha_(p,c)e_c^*, alpha_(p,c)!=0,             (2)
```

for every source row `p` and colour `c`.  These `3m` cells form the
**mandatory cover** `B`.  Exactly two physical cells remain; call their set
`E`, and let

```text
P_*={source endpoints of cells in E}.                 (3)
```

Thus `|P_*|<=2`.  The two excess cells may be coordinate or noncoordinate.

For each colour `c`, the nonzero pure coefficient in (1) supplies a perfect
matching `M_c` in the cells whose row covectors have nonzero `c` component.
If one noncoordinate physical cell is used by several `M_c`, regard its
different colour states as parallel coloured edges.  This is the standard
edge-coloured multigraph semantics and maps faithfully back to one physical
matching term at a fixed input word.  Before comparing two permanent terms,
collapse coloured copies back to physical row cells; changing only the
colour label on one physical cell is not a second term.

Put

```text
H=M_0 union M_1 union M_2.                            (4)
```

It is a three-edge-coloured cubic multigraph with one monochromatic perfect
matching in each colour.

## Exceptional-source localization lemma

Fix an input word induced by a perfect matching `F` in `H`.  Every physical
cell eligible for this word but not equal to its designated backbone cell
has source endpoint in `P_*`.

Proof.  If the eligible physical cell lies in `E`, its source is in `P_*`;
this includes coordinate and noncoordinate excess cells.  Otherwise it is
a mandatory coordinate cell `b_(p,c)` omitted from the selected pure
matching `M_c`.  Since `M_c` still matches source `p`, it uses a different
colour-`c` eligible cell at that source.  The mandatory cover has only the
one cell (2) there, so its replacement is in `E`.  Hence `p in P_*`.

This lemma is independent of how many off-label colour components the two
excess covectors have.

## Bogdanov matching and the equality rectangle

Bogdanov's theorem, reported as Theorem 1.7 by Chandran, Gajjala, and
Illickan in
[*Krenn-Gu conjecture for sparse graphs*](https://arxiv.org/abs/2407.00303),
gives a nonmonochromatic perfect matching `F` in `H`, since `2m>4`.

If `|P_*|<2`, the induced mixed coefficient has no second term.  Indeed,
the symmetric difference of two distinct perfect matchings contains an
alternating cycle, and such a cycle needs at least two non-backbone edges
with distinct source endpoints.  The localization lemma supplies fewer
than two.  Here and below the symmetric difference is taken after collapse
to physical row cells.  The unique `F` monomial is nonzero, contradicting
the zero mixed coefficient of `Delta_3`.

Therefore every equality survivor has

```text
P_*={p_1,p_2}.                                       (5)
```

In particular:

- with one coordinate and one noncoordinate excess cell, their source
  endpoints are distinct;
- with two noncoordinate excess cells, their source endpoints are distinct;
- the same holds for two coordinate excess cells.

Let `F` match modes `mu_1,mu_2` to `p_1,p_2`, with input colours `c_1,c_2`.
Any alternative matching for the same word must use non-backbone edges at
both exceptional sources.  A simple alternating cycle cannot use either
source twice, so the symmetric difference has exactly two new edges and is
the unique four-cycle

```text
(mu_1,p_1),(mu_2,p_2)
  <-> (mu_1,p_2),(mu_2,p_1).                          (6)
```

The cross cells in (6) need not themselves be the two excess cells; they
may be omitted mandatory cells.  What is fixed is their two-source support.

## Exact binomial and cross-ratio equation

Write

```text
A=r_(mu_1,p_1)[c_1], B=r_(mu_1,p_2)[c_1],
C=r_(mu_2,p_1)[c_2], D=r_(mu_2,p_2)[c_2].             (7)
```

After factoring the common product on all other matched edges, the mixed
coefficient is exactly

```text
A D+B C.                                             (8)
```

The backbone term makes `A,D` nonzero.  Cancellation requires `B,C` to be
nonzero as well and forces

```text
A D+B C=0,
(B/A)(C/D)=-1.                                       (9)
```

Thus every nonmonochromatic backbone matching either exposes a unique
forbidden coefficient or contributes one signed rectangle equation (9).
A closed odd signed cycle is impossible when its cross-ratio variables
cancel telescopically, leaving `1=(-1)^(odd)`.  An odd number of unrelated
rectangle equations is not by itself contradictory, and even rectangle
systems may survive.  The subsequent negative-gain graph theorem packages
all such ratios into one auxiliary graph and proves that it must be
bipartite.  See
`ARBITRARY_PERMANENT_EQUALITY_NEGATIVE_GAIN_GRAPH_THEOREM.md`.

## Complete mode-degree ledger

Let `q_i` be the number of noncoordinate cells at mode `i`.  Local concision
gives

```text
d_i=3+epsilon_i, epsilon_i>=0, sum_i epsilon_i=2,      (10)
```

so `epsilon` is either one `2` or two `1`s.  The coordinate degree is

```text
a_i=3+epsilon_i-q_i.                                 (11)
```

Equations (10)--(11) list every one- and two-noncoordinate mode type without
a support search.  Local rank adds only the corresponding quotient-span
condition.  For example, if `a_i=1,q_i=2`, the two noncoordinate covectors
must span the two missing coordinate directions modulo the surviving
coordinate line.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_equality_exceptional_source_rectangle_theorem.py
python audit_arbitrary_permanent_equality_exceptional_source_rectangle_theorem.py
```

The scripts check the degree ledger, source localization bookkeeping,
alternating-cycle size, and the exact `2 x 2` permanent/cross-ratio equation.
They are bounded symbolic sanity checks; the proof is the argument above
plus the cited arbitrary-order matching theorem.

## Boundary

```text
3m+2 support with one exceptional source:  EXCLUDED;
two exceptional sources:                  NECESSARY;
every H-induced mixed coefficient:         UNIQUE OR ONE RECTANGLE;
rectangle cancellation equation:          AD+BC=0;
telescoping odd signed rectangle cycle:    EXCLUDED;
equality cancellation graph:               NECESSARILY BIPARTITE;
existence of an even rectangle system:     UNKNOWN;
global Krenn-Gu conjecture:                 UNRESOLVED.
```
