# Balanced full-sensor common-shore singleton-slice and empty-permanent compatibility theorem

## Status

**Exact characteristic-zero common-shore image parametrization at `m=3`,
with a normalized target-consistent rank-four separator.**  The three
singleton-complement sensor columns of one physical balanced shore must share
the same three root--root factors.  The empty sensor column is the six-term
permanent of the same nine root--nonroot blocks.  Conversely, these formulas
reconstruct the complete four-column `m=3` shore sensor.

An exact Latin-plane `27 x 4` system satisfies the base full-row Cramer
format isolated by the S2M boundary--correct deck-complement degrees, the
complete GHZ target equation, empty deck normalization, and function-field
rank four--but violates the shared-factor incidence.  Thus those ambient
conditions do not imply that a matrix lies in the common-shore matching-sum
image.  No retained pair-jet pattern is imposed on this separator.

This theorem does **not** decide whether any of the eight S2M coordinate
controls is realizable.  It does not force a retained pair jet to fail on
every realized incidence, construct a physical graph, or prove or disprove
the Krenn--Gu conjecture.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The exact `m=3` common-shore incidence

Work over a characteristic-zero field `K`.  Let the three root coordinate
spaces be

```text
A_1, A_2, A_3,             dim A_i=3,                 (1)
```

and let the nonroots be `N={x,y,r}`.  Write the root--root shore blocks as

```text
B_12 in A_1 tensor A_2,
B_13 in A_1 tensor A_3,
B_23 in A_2 tensor A_3.                              (2)
```

After choosing a basis at each nonroot, one root--nonroot block is exactly a
triple of root covectors.  Denote its colour slices by

```text
h_(i,u)^(c) in A_i,
i in {1,2,3}, u in {x,y,r}, c in {0,1,2}.             (3)
```

For `u in N`, let `T_(u,c)` be the coefficient of the `c`-th coordinate of
`u` in the singleton companion `G_{u}`.  In the standard even-deck order

```text
(xy,xr,yr,empty),                                    (4)
```

these singleton companions are respectively `G_r,G_y,G_x`.

Define the ordered shared-factor subspace

```text
S_B
 = A_1 tensor B_23
   + B_13 tensor A_2
   + B_12 tensor A_3
   subset A_1 tensor A_2 tensor A_3.                 (5)
```

The middle tensor factor is inserted in the displayed root order.  Explicitly,

```text
T_(u,c)
 = h_(1,u)^(c) tensor B_23
   + insert_2(B_13,h_(2,u)^(c))
   + B_12 tensor h_(3,u)^(c).                        (6)
```

In particular, all nine singleton slices lie in the **same** subspace `S_B`,
and

```text
dim S_B <= 3+3+3=9.                                  (7)
```

Now fix nonroot colours `q=(q_x,q_y,q_r)`.  The coefficient of
`x_(q_x)y_(q_y)r_(q_r)` in the empty sensor column is

```text
E_q
 = sum_(phi:{1,2,3}->N bijective)
     tensor_(i=1)^3 h_(i,phi(i))^(q_(phi(i))).        (8)
```

After evaluating a root word, (8) is the ordinary sign-free permanent of the
`3 x 3` matrix of the corresponding cross-block entries.  It has exactly six
matching terms.

The phrase **empty sensor column** in (8) means

```text
Gamma_empty=G_N.                                     (9)
```

It must not be confused with the separate deck normalization

```text
C_empty=1.                                          (10)
```

### Theorem 1 (common-shore image if and only if)

A degree-compatible four-column `m=3` sensor matrix is produced by one fixed
collection of root--root and root--nonroot shore blocks if and only if there
exist tensors (2)--(3) for which every singleton slice satisfies (6) and
every coefficient of its empty column satisfies (8).

### Proof

In the balanced matching partition, a singleton companion `G_u` uses exactly
one cross edge.  If root `1`, `2`, or `3` carries that edge, the remaining two
roots have the unique internal perfect matching `B_23`, `B_13`, or `B_12`.
Summing the three choices gives (6), with the same three internal blocks for
every nonroot and every colour.

The empty companion `G_N` uses three cross edges and no root--root edge.
Its matchings are the six bijections from the three roots to `N`; their tensor
products give (8).  This proves necessity directly from the owning balanced
matching formula.

Conversely, the nine triples `h_(i,u)^(c)` assemble uniquely into nine
bilinear root--nonroot blocks in the chosen bases, while (2) already gives the
three root--root blocks.  Formula (6) reconstructs all three singleton
companions and (8) reconstructs the empty companion.  At `m=3` these are all
four even-deck columns, proving sufficiency.  No target equation, rank,
genericity, or division is used.

## 2. A normalized full-row system outside the image

Choose bases `e_(i,a)` of `A_i`, with indices in `Z/3Z`.  Identify the
nonroots `x,y,r` with `u=0,1,2`, and define

```text
P_u(z_u)
 = sum_(c=0)^2 z_(u,c)
     e_(1,c) tensor e_(2,u) tensor e_(3,-c-u).       (11)
```

All indices in (11) are modulo three.  Put

```text
Gamma_xy    = P_2(r),
Gamma_xr    = P_1(y),
Gamma_yr    = P_0(x),
Gamma_empty = J,                                    (12)
```

where

```text
J=sum_(c=0)^2 x_c y_c r_c
     e_(1,c) tensor e_(2,c) tensor e_(3,c).          (13)
```

Finally take the Cramer/deck vector

```text
f=(0,0,0,1).                                        (14)
```

### Theorem 2 (Latin-plane separator)

The system (11)--(14) has the following exact properties.

1. Its columns have multidegrees

   ```text
   (0,0,1), (0,1,0), (1,0,0), (1,1,1),              (15)
   ```

   in the standard order (4).

2. It satisfies every target row and empty normalization:

   ```text
   Gamma f=J,              f_empty=1.                (16)
   ```

3. It has function-field column rank four.  On root rows

   ```text
   (0,2,1), (0,1,2), (1,0,2), (0,0,0),              (17)
   ```

   the displayed maximal minor is

   ```text
   r_0^2 x_0 x_1 y_0^2 !=0.                         (18)
   ```

4. It is not in the common-shore matching-sum image of Theorem 1.

### Proof

Statements (15)--(16) are immediate from (11)--(14).  The rows in (17) give
the triangular matrix

```text
[ r_0   0    0          0       ]
[  0   y_0   0          0       ]
[  0    0   x_1         0       ]
[  0    0   x_0   x_0 y_0 r_0 ],                    (19)
```

whose determinant is (18).

The nine singleton slices in (11) are nine distinct coordinate tensors.  Their
support is the Latin plane

```text
Lambda={(a,b,c) in (Z/3Z)^3 : a+b+c=0},             (20)
```

so their span `U_Lambda` has dimension nine.  Every axis-parallel coordinate
line meets `Lambda` in exactly one point.

Suppose the system came from a common shore.  Theorem 1 would give

```text
U_Lambda subset S_B.
```

By (7), both spaces would have dimension nine and hence be equal.  In
particular,

```text
A_1 tensor B_23 subset U_Lambda.                     (21)
```

If one coefficient of `B_23` at `(b,c)` were nonzero, then (21) would place
all three coordinate tensors `(a,b,c)`, `a=0,1,2`, in `U_Lambda`.  But (20)
contains exactly one of them.  Thus `B_23=0`, after which (5) has dimension at
most six, contradicting `dim U_Lambda=9`.  This proves nonrealizability.

The contradiction occurs already in the singleton shared-factor incidence;
the empty-column permanent (8) is not needed for this particular separator.

## 3. Exact proof-topology consequence

The S2M theorem separated the ambient full-row Cramer conditions from physical
common-shore realization.  Theorem 1 now writes the missing nonlinear image
exactly at `m=3`, and Theorem 2 proves that the separation is genuine:

```text
degree-compatible target-consistent normalized rank-four system   EXISTS;
membership in the common-shore matching-sum image                  FAILS;
universal gate failure on every realized target incidence          OPEN. (22)
```

The Latin-plane proof uses nine independent singleton slices and does not
decide the lower-dimensional slice systems of the eight S2M controls.  Testing
those controls requires solving the full incidence (6)--(8), not merely the
dimension argument in Theorem 2.  No realization or nonrealizability claim is
made for them here.

Likewise, (22) does not show that a physical target incidence passes or fails
the pair-pole gate, does not address simultaneous all-pair compatibility, and
does not extend to arbitrary `m`.  The all-balanced rank-drop branch and all
unrelated proof-DAG leaves retain their previous status.  Global Krenn--Gu
remains **UNRESOLVED**.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_full_sensor_common_shore_singleton_slice_and_empty_permanent_compatibility.py
python -I claims/arbitrary-order/audit_balanced_full_sensor_common_shore_singleton_slice_and_empty_permanent_compatibility.py
python -m py_compile claims/arbitrary-order/verify_balanced_full_sensor_common_shore_singleton_slice_and_empty_permanent_compatibility.py claims/arbitrary-order/audit_balanced_full_sensor_common_shore_singleton_slice_and_empty_permanent_compatibility.py
uv run --with ruff ruff check claims/arbitrary-order/verify_balanced_full_sensor_common_shore_singleton_slice_and_empty_permanent_compatibility.py claims/arbitrary-order/audit_balanced_full_sensor_common_shore_singleton_slice_and_empty_permanent_compatibility.py
```

The primary replay checks the singleton matching formula and the six-term
empty permanent with algebraically independent SymPy symbols, then verifies
all `27` rows, the exact minor, the nine-slice rank, and the no-axis-line
certificate of the Latin separator.

The independent audit imports neither SymPy nor repository code.  It rebuilds
the two matching formulas with exact `Fraction` arithmetic, checks all `9`
singleton slices and all `27 x 27` empty-column coefficients on separate exact
data, and reconstructs all `27` rows and all nonzero entry multidegrees of the
separator.  It then verifies the target equation, normalization, rank minor,
and no-axis-line certificate with its own sparse-polynomial implementation.
