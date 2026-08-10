# Rigid-colour three-block binary primitive and quadratic-bridge theorem

## Status

This note strengthens the globally rigid-colour boundary inside the `r=1`
matrix-unit branch.  It works over `C` for every even `n=2m>=6`.

If one colour `c` is rigid at every vertex, the physical edges split into a
scalar pure-`c` graph `Z` and a binary matrix-unit graph `H`.  The earlier
rigid-colour theorem says that `haf(Z)=1`, `T_H=Delta_(n,2)`, and every
nonzero proper principal hafnian of `Z` annihilates the complete induced
binary tensor on its complement.

The present note proves four new consequences.

1. At every intermediate even size there is a complementary **bi-null cut**:
   both `Z` hafnians are nonzero and both induced binary tensors are zero.
2. Every such witness contains a three-block primitive
   `Omega=A disjoint union B disjoint union C`, with `|A|=|B|=2`, on which
   all six proper block-union binary tensors vanish while the full tensor is
   `Delta_2`.
3. Every binary edge and every `Z` edge obey mutually dual exact quadratic
   bridge identities through four vertices.
4. The three-block primitive is impossible when `n=6`.  Hence the globally
   rigid `r=1` branch is excluded at order six by a short symbolic argument.

The order-six result is sharp with respect to the conjecture's lower-order
boundary: the three one-factorization matchings give an exact order-four
system.  An infinite sparse family also shows that all three pairwise pure
scalar hafnian pencils can hold while a mixed binary deletion fails.
Therefore principal-hafnian supports, adjugates, and constant-colour pencil
coefficients alone cannot close the arbitrary-order branch.

The arbitrary-order three-block primitive is not excluded here.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Rigid-colour convolution system

Let `Omega` have size `n=2m`.  Fix a colour `c` that is rigid at every
vertex.  By the rigid-endpoint lemma, each physical edge is exactly one of:

```text
a (c,c) unit, contributing to the scalar matrix Z; or
a unit whose two endpoint labels avoid c, contributing to H.   (1)
```

The two edge sets are disjoint and exhaust the complete physical graph.
Write the remaining colours as `a,b`.  The exact rigid-colour factorization
is equivalent to

```text
haf(Z[Omega])=1,
T_H[Omega]=Delta_(n,2),                               (2)

haf(Z[S])!=0  =>  T_H[Omega-S] identically zero       (3)
```

for every nonempty proper even `S`.  Empty hafnians are one and odd matching
tensors are zero.

### Lemma 1 (recalled hafnian convolution)

For every scalar symmetric matrix `Z` on `2m` vertices and every
`0<=k<=m`,

```text
sum_(S subset Omega, |S|=2k)
  haf(Z[S]) haf(Z[Omega-S])
 = binomial(m,k) haf(Z[Omega]).                       (4)
```

### Proof

Expand both hafnians on the left.  Their two disjoint matchings unite to one
perfect matching of `Omega`.  Conversely, a full perfect matching and a
choice of `k` of its `m` edges determine `S` and the two restricted
matchings.  Every monomial is therefore counted exactly `binomial(m,k)`
times.

This identity is the existing
[`hafnian convolution split lemma`](HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md),
reproved here to fix the multiplicity convention used below.  Its application
to both orientations of the rigid-colour annihilation system is the new step
in Theorem 2.

### Theorem 2 (intermediate bi-null cuts)

For every `1<=k<m`, some `S` of size `2k` satisfies

```text
haf(Z[S])!=0,                haf(Z[Omega-S])!=0,
T_H[S] identically zero,     T_H[Omega-S] identically zero.   (5)
```

### Proof

By (2), the right side of (4) is the nonzero integer `binomial(m,k)`.  Some
summand has both factors nonzero.  Apply (3) first to `S` and then to its
complement.

This is an existence theorem at every size, not a statement that every cut
is bi-null.

## 2. A forced three-block primitive

### Theorem 3 (two-pair plus mediator reduction)

There is a partition

```text
Omega=A disjoint union B disjoint union C,
|A|=|B|=2,             |C|=n-4,                      (6)
```

such that

```text
T_H[A]=T_H[B]=T_H[C]=0,
T_H[A union B]=T_H[A union C]=T_H[B union C]=0,       (7)
T_H[Omega]=Delta_(n,2).                               (8)
```

Every zero in (7) means the complete coloured tensor is identically zero.

### Proof

Use Theorem 2 at size four.  It gives a four-set `Q` for which

```text
haf(Z[Q])!=0,            haf(Z[Omega-Q])!=0.           (9)
```

Choose a nonzero perfect-matching monomial in `haf(Z[Q])`; its two edges
partition `Q=A disjoint union B`.  Put `C=Omega-Q`.  Then

```text
haf(Z[A]), haf(Z[B]), haf(Z[C]), haf(Z[A union B])
```

are all nonzero.  The two physical edges on `A,B` belong to `Z`, so `H[A]`
and `H[B]` have no edge and their tensors are zero.  Applying (3) to
`A,B,C,A union B` gives, respectively, the other four zeros in (7).  Equation
(8) is (2).

Thus an arbitrary-order globally rigid witness would contain a binary
three-block interaction whose two two-vertex ports and arbitrary even
mediator are individually and pairwise null but jointly equal `Delta_2`.

## 3. Fermat contact of the hafnian pencil

For arbitrary binary local vectors `y_v in C^2`, let `A(y)` be the scalar
symmetric matrix obtained by evaluating every `H` edge on its two endpoint
vectors, and put zero on the `Z` edges.

### Theorem 4 (all intermediate polars vanish)

One has the polynomial identity

```text
haf(Z+t A(y))
 = 1 + t^m
     (product_v y_v[a] + product_v y_v[b]).           (10)
```

### Proof

The coefficient of `t^k` is

```text
sum_(|S|=2k) haf(A(y)[S]) haf(Z[Omega-S]).             (11)
```

For `0<k<m`, every summand is zero: if its `Z` factor is nonzero, (3) says
the complete tensor `T_H[S]` is zero and hence so is its evaluation
`haf(A(y)[S])`; otherwise the `Z` factor itself is zero.  The constant term
is `haf Z=1`, and the top term is the evaluation of `T_H=Delta_2`, proving
(10).

This is a high-order contact identity on the physical toric family `A(y)`.
It is not a contradiction.

## 4. Quadratic bridges

For a set `R` of even size and distinct `r,s in R`, abbreviate

```text
K^Z_rs(R)=haf(Z[R-{r,s}]).                            (12)
```

### Theorem 5 (bridge from a binary edge)

Let `pq` be an `H` edge and put `R=Omega-{p,q}`.  Then

```text
sum_(r,s in R, r!=s)
  Z_pr Z_qs K^Z_rs(R) = 1.                           (13)
```

Consequently there are distinct `u,v in R` with

```text
Z_pu Z_qv haf(Z[Omega-{p,q,u,v}]) != 0.              (14)
```

For `Q={p,q,u,v}`, exactly one of the following two outcomes occurs.

1. `haf(Z[Q])!=0`.  Then both `T_H[Q]` and `T_H[Omega-Q]` are zero: `Q` is a
   `4|(n-4)` binary bi-null cut.
2. `haf(Z[Q])=0`.  Then `pq` is the only `H` edge in `Q`; the other five
   edges belong to `Z`, and

   ```text
   Z_pu Z_qv = -Z_pv Z_qu !=0.                       (15)
   ```

### Proof

The rigid avoiding-edge cofactor lemma gives

```text
haf(Z[R])=0.                                         (16)
```

Contract every vertex in `R` with `e_c` and leave `p,q` open.  Global
`c`-rigidity says that every surviving boundary leg from `p` or `q` is a
`(c,c)` edge.  The direct `pq` term is killed by (16), and the target
boundary tensor is `E_cc`.  Its `(c,c)` entry is exactly (13).  This proves
(14).

The nonzero complementary hafnian in (14) and (3) give `T_H[Q]=0`.  If
`haf(Z[Q])` is nonzero, (3) also gives `T_H[Omega-Q]=0`.

Otherwise `Z_pq=0` because `pq` is an `H` edge, so the four-vertex hafnian
equation is

```text
0=Z_pu Z_qv + Z_pv Z_qu.                             (17)
```

The first term is nonzero, proving the four cross-edge assertions and (15).
If `uv` were an `H` edge, `pq|uv` would be the unique `H` perfect matching
on `Q`, because the four cross edges are in `Z`.  Its nonzero matrix-unit
monomial would contradict `T_H[Q]=0`.  Hence `uv` is in `Z` as well.

### Theorem 6 (dual bridge from a `Z` edge)

Let `pq` be a `Z` edge and fix one binary colour `d in {a,b}`.  Write `A^d`
for the scalar graph of `(d,d)` edges in `H`.  There are distinct
`u,v outside {p,q}` such that

```text
A^d_pu A^d_qv
haf(A^d[Omega-{p,q,u,v}]) !=0.                       (18)
```

For `Q={p,q,u,v}` one has

```text
haf(Z[Q])=0,
Z_pq Z_uv + Z_pv Z_qu = 0.                           (19)
```

### Proof

Since `Z_pq!=0`, (3) gives `T_H[Omega-{p,q}]=0`, so the pure-`d` cofactor
of `A^d` there is zero.  But `haf(A^d[Omega])=1`.  Expanding the pure
coefficient through `p,q`, whose direct `A^d_pq` entry is zero, gives a sum
equal to one and hence a nonzero term (18).

The induced tensor on `Omega-Q` has a nonzero pure-`d` coefficient.  If
`haf(Z[Q])` were nonzero, (3) would make that tensor zero.  Thus the first
part of (19) holds.  The selected pure-`d` edges give `Z_pu=Z_qv=0`, and the
remaining four-hafnian expansion is exactly the second equation in (19).

Theorems 5 and 6 are mutually dual local constraints.  They do not assert
that the displayed four-sets are common for the two binary colours.

## 5. Complete exclusion at order six

### Theorem 7

No order-six `r=1` witness can have a colour rigid at every vertex.

### Proof

Here Theorem 3 partitions the vertices into three two-vertex blocks
`A,B,C`.  Each internal block edge belongs to `Z`, so `H` has no internal
block edge.  All three two-block induced tensors are zero.

Choose nonzero pure-`a` and pure-`b` perfect matchings of `H`.  Each matching
has exactly one edge in each of the three block-pair cells: endpoint counting
on a two-vertex block forces the cell multiplicities to be `(1,1,1)`.

At any block, compare which of its two vertices the two pure matchings send
to either neighbouring block.  The assignments are either the same at both
neighbours (`S`) or different at both (`D`).  Two adjacent `S` blocks are
impossible, because the two pure matchings would then require different
labels on the same physical cell edge.

Consider one block-pair cell.

- In a `D-D` cell, the selected pure edges are disjoint and form a mixed
  perfect matching of the four vertices.  Since the complete cell tensor is
  zero, the alternate cross pairing must induce the same word with opposite
  nonzero product.  Thus all four cross edges are present in `H`: the cell is
  a full `K_(2,2)`.
- In an `S-D` cell, the two selected pure edges share their endpoint in the
  `S` block.  The cell can contain no perfect matching.  Indeed, either cross
  perfect matching would have to cancel with the other, but at the shared
  endpoint one uses label `a` and the other label `b`, so their words cannot
  agree.  The cell therefore consists exactly of the selected two-edge star.

The triangle of blocks has either no `S` block or exactly one.

If all blocks are `D`, all three cells are full `K_(2,2)`.  A full matching
chooses one of the two endpoint assignments at each block, so there are
`2^3=8` matchings.  At a `D` block, choosing which vertex goes to one
neighbour forces the other vertex to go to the other neighbour; the local
labels forced by the two pure matchings then give the same binary colour at
both vertices.  Thus the three independent block choices index eight
distinct block-uniform words.  Two are the required pure words; the other
six are forbidden and each has one nonzero monomial.

If exactly one block is `S`, the opposite `D-D` cell is full `K_(2,2)` and
the other cells are stars.  Choosing the star incidence fixes the labels at
the `S` block and determines which residual edge is used in the full cell.
There are exactly four full matchings, with four distinct words: the two pure
words and two unique forbidden words.

Both cases contradict `T_H=Delta_(6,2)`.  This proves the theorem without
enumerating graph supports or appealing to the existing finite certificate.

## 6. Sharp boundaries and a route countermechanism

### Order four

On four vertices, label the three matchings in the one-factorization of
`K_4` by `(c,c)`, `(a,a)`, and `(b,b)`, with each matching product normalized
to one.  The `a/b` edges form a four-cycle whose only perfect matchings are
the two pure ones, so `T_H=Delta_(4,2)`.  The only nonzero proper principal
hafnians of `Z` are its two edges, and each complementary two-vertex binary
tensor is zero because that physical edge belongs to `Z`.  Thus the rigid
annihilating system exists exactly at this lower-order boundary.  The global
conjecture starts at order six.

### Infinite pure-pencil countermechanism

Let `m>=3` be odd, with bipartition vertices `a_i,b_i` indexed modulo `m`,
and define three shift matchings

```text
M_j={a_i b_(i+j):i in Z/mZ},       j=0,1,2.           (20)
```

Put `Z` on `M_0`, the pure binary colour `a` on `M_1`, and pure colour `b`
on `M_2`, normalizing all three matching products to one.  Every pairwise
union is one Hamilton cycle because the shift differences `1,2` are units
modulo odd `m`.  Therefore every pairwise scalar hafnian pencil has exactly
its endpoint terms, and `M_1 union M_2` by itself realizes `Delta_(2m,2)`.

Nevertheless the full tensor deletion deck fails.  The Bogdanov matching
theorem, in the exact form recorded in the
[`universal zero-layer theorem`](UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md)
and originating in
[Chandran--Gajjala--Illickan, Theorem 1.7](https://arxiv.org/abs/2407.00303),
gives a nonmonochromatic perfect matching in the union of all three
matchings.  Every pairwise union is a Hamilton cycle with only its two
alternating pure matchings, so this matching uses all three `M_j`.  Deleting
the selected `M_0` endpoints leaves disjoint paths in `M_1 union M_2`; their
compatible binary matching is unique, nonzero, and uses both binary colours.
Hence a proper nonzero `Z` principal term meets a nonzero mixed binary
deletion.

This sparse system omits the required nonzero matrix unit on every unused
physical pair and is not an `r=1` witness.  It proves only that the three
pairwise pure scalar pencils, including every intermediate coefficient in
the constant-colour specializations of (10), are insufficient.
Cancellation-sensitive mixed binary deletion tensors and physical completion
are essential.

## 7. Scope and provenance

The global rigid-colour factorization and annihilation system (2)--(3) are
imported from
[`RIGID_COLOUR_COFACTOR_ANNIHILATION_AND_BACKBONE_CANCELLATION_BOUNDARY.md`](RIGID_COLOUR_COFACTOR_ANNIHILATION_AND_BACKBONE_CANCELLATION_BOUNDARY.md).
The convolution identity (4) is imported from
[`HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md`](HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md).
The general two-boundary identity underlying Theorem 5 is equation (16) of
[`MATRIX_UNIT_FOUR_SWITCH_MINIMAL_PORT_AND_PARTIAL_BRIDGE_REDUCTION_THEOREM.md`](MATRIX_UNIT_FOUR_SWITCH_MINIMAL_PORT_AND_PARTIAL_BRIDGE_REDUCTION_THEOREM.md).
Its globally rigid quadratic consequence, the bi-null application,
three-block primitive, Fermat contact, dual bridge consequences, and
order-six exclusion are new here.

```text
global c-rigid factorization/deletion system: PROVED UPSTREAM;
bi-null cut at every intermediate size:       PROVED;
two-pair plus mediator primitive:             PROVED;
Fermat contact identity:                      PROVED;
binary-edge quadratic bridge:                 PROVED;
Z-edge dual quadratic bridge:                 PROVED;
globally rigid r=1 branch at n=6:             EXCLUDED;
globally rigid r=1 branch at arbitrary n:     UNKNOWN;
order-four boundary system:                   EXACT;
infinite shift family is a KG witness:        FALSE;
global Krenn--Gu conjecture:                   UNRESOLVED.
```

## Focused checks

Run from repository root:

```text
python claims/arbitrary-order/verify_rigid_colour_three_block_binary_primitive_and_quadratic_bridge.py
python claims/arbitrary-order/audit_rigid_colour_three_block_binary_primitive_and_quadratic_bridge.py
```

The primary check audits the convolution multiplicity, the order-six
`S/D` incidence classification, the order-four boundary, and odd shift
families.  The independent no-import audit uses a separate edge-set matching
representation and reconstructs the order-six word tables directly.  These
are bounded convention checks.  The arbitrary-order force comes from the
written convolution, matching-partition, and two-boundary proofs.
