# The true generic flat binary-cubic chart is impossible

## Status

This is an exact characteristic-zero obstruction on the genuine
Borel-generic chart of the flat rank-two-relation triangle.

Purity fixes each local kernel line.  Therefore the allowed row gauge
is

```text
y_i -> scalar*y_i,
x_i -> scalar*(x_i+s_i y_i),
```

not full row `GL_2`.  The generic kernel row has full source support,
and the four affine ratios `x_j/y_j` are distinct.  On the dense
partner chart, this theorem excludes that case by an exact
binary-cubic compound identity.

This corrects the scope of
[`P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md`](P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md),
which is a valid one-kernel-zero boundary theorem.  The earlier
“complete” projective-column classification was withdrawn because it
moved the fixed kernel line:
[`P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION_WITHDRAWN_OVERSTRONG.md`](P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION_WITHDRAWN_OVERSTRONG.md).

The projective partner sheets over this same center have since been
classified and excluded from the all-rank-three-relation triangle in
[`P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md`](P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md).
Collisions among the affine ratios and smaller kernel supports remain.
Thus this is a generic theorem, not
a complete triangle classification, component-exhaustiveness proof,
or global solution of the Krenn--Gu conjecture.

## Borel normal form

On the flat branch,

```text
y_i x_j=x_i y_j,                  i<j,                            (1)
```

and the Hamming-weight triple products satisfy

```text
dim span(Y,K,J)<=2,               X notin span(Y,K,J).             (2)
```

Assume the kernel row of `A_1=(y_1;x_1)` has four nonzero entries and
the four ratios `x_{1r}/y_{1r}` are distinct.  Diagonal source scaling
makes the kernel row constant.  An active shift and scaling then give

```text
y=(1,1,1,1),
x=(0,1,p,q),

p q(p-1)(q-1)(p-q)!=0.                                            (3)
```

This uses only the Borel gauge preserving the kernel line.

## The true affine synchronizer

Solving the six coefficients of

```text
y x'-x y'=0
```

gives a two-dimensional space.  Besides `A=(y;x)`, use

```text
y^#=(0, p+q-1, p(1-p+q), q(1+p-q)),
x^#=p q(-1,1,1,1).                                                (4)
```

On the dense projective parameter chart, rescale the two partners and
write

```text
A_1=A,             A_2=A+tA^#,             A_3=A+uA^#.            (5)
```

The synchronizer is totally isotropic:

```text
y(t)x(u)=x(t)y(u).                                                 (6)
```

Thus (5) indeed gives a flat triangle, and its four triple
coefficients form

```text
C=[Y K J X].                                                       (7)
```

## The common cofactor

Put

```text
H=p^2-2pq-2p+q^2-2q+1
```

and define the symmetric biquadratic

```text
F =
 p^2 q^2 H t^2u^2
 -6p^2q^2(t^2u+tu^2)
 -pq(p+q+1)(t^2+4tu+u^2)
 -2(pq+p+q)(t+u)
 -3.                                                              (8)
```

In the `R_3` basis indexed by the omitted source coordinate, one
compression minor is

```text
det C[{1,2,3},{Y,K,J}]
 =-8(p-1)(p-q)(q-1)F.                                             (9)
```

More strongly, every `3 x 3` minor of the full matrix `C` is
divisible by `F`:

```text
C_3(C)=8F N(p,q,t,u)                                               (10)
```

for a polynomial `4 x 4` matrix `N`.  The determinant records the
same square:

```text
det C=-16pq(p-1)(p-q)(q-1)F^2.                                   (11)
```

Equations (9)--(11) are direct compound-matrix identities over
`Z[p,q,t,u]`, replayed exactly by the verifier.

Since the prefactor in (9) is nonzero, the compression half of (2)
forces

```text
F=0.
```

Equation (10) then gives

```text
rank C<=2.                                                        (12)
```

## The compressed span cannot be a line

It remains to rule out the possibility that `span(Y,K,J)` has
dimension at most one.  Three `2 x 2` minors of the `K,J` columns are

```text
M_12=-4q^2(p-1)(pt+1)(pu+1),
M_13=-4p^2(q-1)(qt+1)(qu+1),
M_23= 4(p-q)(pqt+1)(pqu+1).                                      (13)
```

If all three vanished, the two-element multiset `{t,u}` would have
to contain all three distinct values

```text
-1/p,                 -1/q,                 -1/(pq).              (14)
```

They are distinct under (3), which is impossible.  Hence

```text
dim span(Y,K,J)=2.                                                 (15)
```

The escape half of (2) now requires `rank C=3`, contradicting (12).
Therefore the full-kernel-support, distinct-affine-ratio, finite
partner chart is empty.

## Correct frontier

After the companion projective-sheet theorem, the remaining flat triangle
is confined to the union of:

1. a collision among the four affine ratios in (3);
2. a zero coordinate of a kernel row; or
3. intersections of these divisors.

The one-kernel-zero otherwise-distinct chart is already empty by the
companion kernel-zero theorem.  The other Borel boundary strata must
be classified without moving the distinguished kernel lines.

## Verification

Run:

```text
python verify_p4_resonant_flat_generic_binary_cubic.py
python audit_p4_resonant_flat_generic_binary_cubic.py
```

The primary verifier derives (4), recomputes all squarefree triple
products, and checks (8)--(13) over `Q(p,q,t,u)`.  The independent
audit uses a different subset-permanent construction and polynomial
division for all sixteen compound entries.  Neither script searches
for solutions.
