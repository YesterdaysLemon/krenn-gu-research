# Arbitrary permanent co-two product-sensor corank-two strengthening

## Status

This is an exact arbitrary-order characteristic-zero strengthening of the
necessary product-sensor boundary for a weighted diagonal restriction

```text
P_r -> Delta_3,                 r >= 3.                 (1)
```

Use the square-free algebra, local forms, omitted pair `{a,b}`, two-mode
product space `B_ab`, and complementary sensor `A_S` from
`ARBITRARY_PERMANENT_COTWO_PRODUCT_SENSOR_RANK_DROP_THEOREM.md`.  For every
omitted pair, this note proves

```text
dim B_ab >= 5,
dim A_S + dim B_ab <= binomial(r,2)+3,
dim A_S <= binomial(r,2)-2.                            (2)
```

Thus every co-two product sensor has corank at least two in its ambient
square-free degree space.  At `r=6`, all fifteen four-mode sensors have rank
at most `13`, improving the previous bound `14`.

This is still a necessary condition, not a nonrestriction theorem.  It does
not prove that the simultaneous corank-two locus is empty after imposing the
mixed `Delta_3` equations.  Unrestricted `P_6 -> Delta_3`, arbitrary-order
permanent nonrestriction, and the global Krenn--Gu conjecture remain
**UNKNOWN/UNRESOLVED**.

## 1. Imported pairing facts

Let `K` have characteristic zero and

```text
Z_r = K[x_0,...,x_(r-1)]/(x_0^2,...,x_(r-1)^2).       (3)
```

A putative restriction supplies independent triples

```text
u_(i,0), u_(i,1), u_(i,2) in (Z_r)_1                 (4)
```

at every mode.  For an omitted pair `{a,b}`, put

```text
B_ab = span{u_(a,c)u_(b,d) : c,d in {0,1,2}}
       subset (Z_r)_2.                                (5)
```

The complement pairing between `B_ab` and `A_S` has rank three.  Its three
diagonal products

```text
d_c = u_(a,c)u_(b,c),              c=0,1,2,           (6)
```

are independent modulo the left radical, while every mixed product

```text
u_(a,c)u_(b,d),                    c!=d,               (7)
```

belongs to that radical.  The predecessor theorem also proves

```text
dim B_ab >= 4.                                         (8)
```

We use its degree-one annihilator lemma: for nonzero `u in (Z_r)_1`,

```text
dim{v in (Z_r)_1 : uv=0} <= 1,                         (9)
```

and a nonzero annihilator exists only when `u` has coordinate support at
most two.

## 2. A support-two factor lemma

For a nonzero square-free quadratic `q`, let `V(q)` be the set of coordinate
indices incident to a monomial with nonzero coefficient in `q`.

### Lemma 1 (factor support and the four-vertex case)

Suppose

```text
0 != q = uv in (Z_r)_2,
|supp(u)| <= 2, |supp(v)| <= 2.                        (10)
```

Then

```text
V(q) = supp(u) union supp(v),                          (11)
```

so `|V(q)|<=4`.  If `|V(q)|=4`, then in every factorization of a nonzero
scalar multiple of `q` into two support-at-most-two linear forms, the two
factors lie on two fixed lines.

### Proof

Put `U=supp(u)` and `V=supp(v)`.  If `U` and `V` are disjoint, every cross
edge has a nonzero coefficient, so all vertices in `U union V` occur.  If
the supports meet in one vertex and both have size two, the two one-term
edges incident to the common vertex and the edge between the two remaining
vertices are all nonzero.  The singleton/two-support cases are the same
one-term calculation.  If `U=V` has size two, the product is supported on
their single edge, whose coefficient is nonzero because `q!=0`.  The only
remaining case, equal singleton supports, has zero product.  This proves
(11).

If `|V(q)|=4`, both factor supports have size two and are disjoint.  The
support graph of `q` is therefore a `K_(2,2)` with all four cross-edge
weights nonzero.  Its unordered bipartition is unique because the graph is
connected.  Any other factorization into two support-at-most-two forms must
use those same two shores.  On a fixed shore, ratios of the two factor
coefficients are fixed by ratios of two edge weights.  Thus the two factors
occupy the two projective lines supplied by the shores.  This proves the
lemma.

## 3. Equality four is impossible

### Lemma 2

For every omitted pair in a restriction (1),

```text
dim B_ab != 4.                                         (12)
```

### Proof

Assume `dim B_ab=4`.  Since the restricted pairing has rank three, its left
radical is a line `Kq`.  The three diagonal products (6) are independent
modulo that line.  Every mixed product (7) lies in it.

Fix a colour `c` at mode `a`, and let `d,e` be the other two colours.  The
two products

```text
u_(a,c)u_(b,d), u_(a,c)u_(b,e)                        (13)
```

are linearly dependent because both lie in `Kq`.  The two second factors
are independent.  Hence a nonzero element of their span annihilates
`u_(a,c)`, and the annihilator lemma gives

```text
|supp(u_(a,c))| <= 2.                                  (14)
```

The two products in (13) cannot both vanish, since that would put two
independent forms in the at-most-one-dimensional annihilator.  Consequently
one of them is a nonzero scalar multiple of `q`.  This holds for every `c`.
The symmetric argument at mode `b` gives support at most two for every
`u_(b,d)` and makes each of those forms a factor of a nonzero scalar multiple
of the same `q`.

Apply Lemma 1.

- If `|V(q)|<=2`, the three independent forms at mode `a` lie in a
  coordinate space of dimension at most two, a contradiction.
- If `|V(q)|=3`, all six local forms lie in the same three-coordinate space.
  All nine products (5) then lie in its three-dimensional square-free
  degree-two part, contradicting `dim B_ab=4`.
- If `|V(q)|=4`, Lemma 1 places the three independent forms at mode `a` on
  only two factor lines, again a contradiction.

These cases exhaust `|V(q)|<=4`, proving (12).

## 4. The strengthened sensor bound

### Theorem 3 (co-two product-sensor corank at least two)

For every `S` of size `r-2` in every restriction (1), equations (2) hold.

### Proof

Equations (8) and (12), together with integral dimension, give

```text
dim B_ab >= 5.                                         (15)
```

Let `N=dim (Z_r)_2=binomial(r,2)`.  For subspaces of the perfect complement
pairing, the restricted rank is at least

```text
dim B_ab + dim A_S - N.                                (16)
```

The actual restricted rank is three, so

```text
dim A_S <= N+3-dim B_ab <= N-2.                        (17)
```

This proves (2).  Notice that the general dimension-sum inequality in (2)
has not changed; the gain comes only from the stronger lower bound on
`dim B_ab`.

## 5. Exact boundary and failed stronger inference

For the live zero-surplus permanent node:

```text
every P_r -> Delta_3 co-two pair space dim >=5:        PROVED;
every co-two complementary sensor corank >=2:          PROVED;
every P_6 four-mode product sensor rank <=13:           PROVED;
simultaneous corank-two plus local rank/nonvanishing:   NOT SHOWN SUFFICIENT;
unrestricted P_6 -> Delta_3:                           UNKNOWN;
arbitrary-r permanent nonrestriction:                  UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

The predecessor's explicit P6 non-target model still saturates
`dim A_S+dim B_ab=N+3`; it does not satisfy the mixed `Delta_3` equations and
therefore does not test sharpness of (15) inside the restriction locus.

This theorem concerns the square-free permanent restriction algebra.  It is
not the balanced physical hafnian sensor, supplies no graph-extraction or
case-cover theorem, and does not reduce `P_6` to a smaller order.

## Replay

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_cotwo_product_sensor_corank_two_strengthening.py
python claims/arbitrary-order/audit_arbitrary_permanent_cotwo_product_sensor_corank_two_strengthening.py
python claims/arbitrary-order/verify_arbitrary_permanent_cotwo_product_sensor_rank_drop.py
python claims/arbitrary-order/audit_arbitrary_permanent_cotwo_product_sensor_rank_drop.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_cotwo_product_sensor_corank_two_strengthening.py claims/arbitrary-order/audit_arbitrary_permanent_cotwo_product_sensor_corank_two_strengthening.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_cotwo_product_sensor_corank_two_strengthening.py claims/arbitrary-order/audit_arbitrary_permanent_cotwo_product_sensor_corank_two_strengthening.py
```

The primary verifier symbolically enumerates the support graph cases, checks
the unique `K_(2,2)` bipartition, and performs an exact rational factor-line
regression.  The independent no-import audit uses a separate graph walk and
exact arithmetic over `Q(omega)`.  These finite checks audit conventions and
cancellation-sensitive cases; the written arguments prove the arbitrary-
order characteristic-zero theorem.
