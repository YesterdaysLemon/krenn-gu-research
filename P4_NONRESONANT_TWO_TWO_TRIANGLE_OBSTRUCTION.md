# A full-support `2+2` bridge cannot occur in a nonresonant triangle

## Status

This is an exact characteristic-zero obstruction for the second
full-support cut type left by
[`P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md`](P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md).
It is a proof in two hyperbolic binary planes; no elimination or
component search is used.

Let

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Suppose `U_1,U_2,U_3` form a nonresonant triangle of pair images of
dimension three, each unique pair relation having coefficient-matrix
rank two.  The cut reduction associates nonzero bridge quadrics

```text
Q_ij=b_ij y_i x_j=-c_ij x_i y_j
```

such that

```text
U_k=Ann_R1(Q_ij),                {i,j,k}={1,2,3}.                    (1)
```

If even one `Q_ij` is a full-support `2+2` cut, the triangle is
impossible.

Together with
[`P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md),
this proves:

```text
every nonresonant rank-two-relation triangle whose three bridge
cuts have full support is empty.                                    (2)
```

The proper support boundaries of the `1+3` and `2+2` bridges have
since been excluded in
[`P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md).
The remaining triangle frontier is now confined to the resonant,
trivial-holonomy divisor.

This is a component-classification advance, not a proof of component
exhaustiveness or of the global Krenn--Gu conjecture.

## Hyperbolic block notation

Let

```text
V=A direct-sum B,
A=span(X_0,X_1),                 B=span(X_2,X_3).
```

Multiplication inside either binary block is a nondegenerate
symmetric pairing with values in a one-dimensional degree-two space.
Choose fully supported forms

```text
a in A,                          b in B,
```

and their unique opposite binary directions

```text
a_bar in A,                      b_bar in B,

a a_bar=0,                       b b_bar=0.                          (3)
```

Full support means `a^2,b^2,a_bar^2,b_bar^2` are all nonzero.  The two
pairs `(a,a_bar)` and `(b,b_bar)` are bases of their blocks.

After diagonal source scaling, every full-support `2+2` cut has the
form

```text
q=ab.                                                                  (4)
```

Its multiplication catalecticant has rank two and

```text
Ann_R1(q)=span(a_bar,b_bar)=:W.                                    (5)
```

## The anchor lemma

Every factorization

```text
q=uv                                                               (6)
```

contains an anchor:

```text
u or v lies in one of the two lines C a, C b.                       (7)
```

To prove this, decompose

```text
u=u_A+u_B,                    v=v_A+v_B.
```

The internal and cross-block parts of (6) are

```text
<u_A,v_A>_A=0,
<u_B,v_B>_B=0,

u_A tensor v_B+v_A tensor u_B=a tensor b.                           (8)
```

The last matrix has rank one.  For two rank-one summands, the exterior
determinant identity gives

```text
det(u_A,v_A) det(u_B,v_B)=0.                                       (9)
```

Suppose first that `u_A,v_A` are dependent.  Their common direction
must be `a`, because the left factor of the nonzero tensor in (8) is
`a`.  Since `a^2!=0`, the first equation of (8) forces one of
`u_A,v_A` to vanish.  The cross equation then makes the corresponding
whole factor a scalar multiple of `b`.  Thus (7) holds.  The case in
which `u_B,v_B` are dependent is symmetric and produces the anchor
`a`.

The optional non-anchor part of the other factor is harmless.  For
example,

```text
b(a+t b_bar)=ab,                a(b+s a_bar)=ab,                    (10)
```

because the extra binary products vanish.  Statement (7), rather than
uniqueness of the second factor, is the invariant fact needed below.

## Planes with a rank-three product against the annihilator

Let `V'` be any plane such that

```text
dim(W V')=3
```

and the unique kernel tensor of

```text
W tensor V' -> R_2
```

has matrix rank two.  After choosing a basis `(v,w)` of `V'`, that
kernel tensor can be written

```text
a_bar tensor v+b_bar tensor w.
```

Thus

```text
a_bar v+b_bar w=0.                                                  (11)
```

Split (11) into its internal `A`, cross `A tensor B`, and internal `B`
parts.  The internal terms and (3) give

```text
v_A=alpha a,                    w_B=beta b.
```

The cross part is an equality of two rank-one tensors, so for one
scalar `tau`,

```text
v_B=tau b_bar,                  w_A=-tau a_bar.
```

Consequently every such plane has the crossed-graph normal form

```text
V'=span(
 alpha a+tau b_bar,
 -tau a_bar+beta b
).                                                                  (12)
```

Moreover,

```text
tau != 0.                                                           (13)
```

If `tau=0`, the two summands in (11) vanish separately:

```text
a_bar v=0,                      b_bar w=0.
```

They give two independent decomposable kernel tensors, so the product
image has dimension at most two, contrary to the hypothesis.

Finally, (12)--(13) show that `V'` contains neither anchor line:

```text
V' intersection C a=0,          V' intersection C b=0.             (14)
```

Indeed, in the basis `(a,a_bar,b,b_bar)`, a combination of the two
rows in (12) has coordinates

```text
(r alpha,-s tau,s beta,r tau).
```

Equality with `a` forces `r=0` from the last coordinate, and equality
with `b` forces `s=0` from the second.

## The triangle contradiction

Assume, after relabelling, that

```text
Q_12=q=ab.
```

Equation (1) gives

```text
U_3=W=span(a_bar,b_bar).                                             (15)
```

Both remaining edges have rank-three pair images and rank-two kernel
relations.  Apply (12)--(14) to `(W,U_1)` and `(W,U_2)`.  Neither
`U_1` nor `U_2` contains either anchor `a` or `b`.

But the bridge identity on edge `12` includes the factorization

```text
q=b_12 y_1x_2.
```

The anchor lemma says one of `y_1 in U_1` and `x_2 in U_2` must lie
in `C a` or `C b`.  This contradicts (14).  Hence a full-support
`2+2` bridge cannot occur.

The argument uses only one of the two factorizations of `Q_12`; the
second makes the incompatibility still more rigid.

## What was hiding over the fence

The binary blocks carry hyperbolic bilinear forms, and the annihilator
plane `W` is the orthogonal mate of the two cut factors.  Equation
(12) says that every rank-three partner of `W` is an off-diagonal
graph with nonzero coupling `tau`.  The factorization variety of
`ab`, however, is the union of anchor sheets (10).  The obstruction is
the empty intersection

```text
crossed graph plane  intersection  anchor factorization sheets.
```

This is the smallest bounded-rank matrix-pencil/compression-space
phenomenon.  De Teran--Dopico--Landsberg,
[An explicit description of the irreducible components of the set of
matrix pencils with bounded normal rank](https://arxiv.org/abs/1606.02574),
and de Seguins Pazzis,
[Large spaces of bounded rank matrices revisited](https://arxiv.org/abs/1507.05375),
provide the surrounding language.  The particular anchor and
crossed-graph lemmas above are proved directly and are not claims from
those papers.

## Verification

Run:

```text
python verify_p4_nonresonant_two_two_triangle_obstruction.py
python audit_p4_nonresonant_two_two_triangle_obstruction.py
```

The primary verifier checks the full cut and its annihilator, the
exterior determinant identity, the crossed-graph kernel relation, its
rank-three minor, and anchor avoidance.  The independent audit uses
unequal rational block weights and a different coordinate ordering.
Both are tiny exact replays of the proof, not searches.
