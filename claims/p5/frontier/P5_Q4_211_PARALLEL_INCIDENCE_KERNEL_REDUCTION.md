# Parallel-incidence kernel reduction for normalized `q4_211`

## Status

This note proves an exact characteristic-zero reduction inside the
normalized `q4_211` branch.  Assume

```text
b c != 0
```

in the normal form

```text
u_0=(a,1,1,0,0),
u_1=(b,0,0,1,0),
u_2=(c,0,0,0,1),
```

and assume that two of the four remaining modes contain both singleton
normals

```text
h_1=(b,0,0,-1,0),
h_2=(c,0,0,0,-1).
```

Then a third mode contains both `h_1` and `h_2`.  Thus the genuinely
parallel generic stratum cannot occur without strict extra incidence
and may be reselected as an adjacent type.  This does **not** exclude
normalized `q4_211`, prove
`P_5` does not restrict to `Delta_3`, or solve the arbitrary-order
Krenn--Gu conjecture.

## Pullbacks at the two common modes

Call the two modes containing both normals `A,B`, and call the other
two modes `C,D`.  Since each local map has rank three, pullback on
target covectors is injective.  Write the target covectors pulling back
to `h_1,h_2` at `i=A,B` as

```text
x_i=(r_i,0,q_i),
y_i=(s_i,p_i,0).                                    (1)
```

The zero in `x_i` follows from

```text
(u_1,h_1) contract P_5=0,
```

and the zero in `y_i` follows similarly from
`(u_2,h_2) contract P_5=0`.  Injectivity implies

```text
(p_i,q_i) != (0,0).                                 (2)
```

Let

```text
G=(L_C tensor L_D)(Sym(e_1,e_2)).                    (3)
```

Exact differentiation of `x_0 x_1 x_2 x_3 x_4` gives

```text
(u_1,h_2,h_2) contract P_5=-2c x_1 x_2,
(u_2,h_1,h_1) contract P_5=-2b x_1 x_2.             (4)
```

On the target side these are respectively proportional to

```text
p_A p_B e_1 tensor e_1,
q_A q_B e_2 tensor e_2.                             (5)
```

Because `b c != 0`, either `G=0`, or `G` is a nonzero pure tensor on
exactly one of the two singleton target lines.  In particular, the two
products in (5) cannot both be nonzero.

## A diagonal-pencil lemma

The following elementary lemma is the main change of language.  It
views the remaining equations as a two-dimensional diagonal matrix
pencil rather than as a support search.

Let

```text
V=span(s,d) direct-sum X,   dim(X)=3,
```

and let `A,B:V -> W`, with `dim(W)=3`, both have rank three.  Put

```text
p=A(s), q=B(s),
F(v)=p tensor B(v)+A(v) tensor q.                    (6)
```

Suppose `F(X)` lies in a diagonal subspace

```text
D subset span(x tensor x,y tensor y).                (7)
```

with `dim(D)<=2`.  Because adding the single vector `d` can raise rank
by at most one,

```text
dim span(p,A(X)) >= 2,
dim span(q,B(X)) >= 2.                               (8)
```

If exactly one of `p,q` is zero, (6) is a fixed-factor tensor space.
A two-dimensional fixed-factor space cannot lie in the diagonal plane:
that plane contains no two-dimensional space consisting entirely of
rank-at-most-one matrices.  This contradicts (8).

Now suppose `p,q` are both nonzero.  If both projections in (8) grow
beyond `p,q`, the linear space `F(X)` contains a rank-two diagonal
matrix.  Indeed, a rank-one diagonal can enlarge at most one of the
two factor spans; if the two enlargements came from the same diagonal
line, uniqueness of a decomposition modulo

```text
(-p,q)
```

would again enlarge at most one side.  Two distinct diagonal lines
have a rank-two linear combination.

Consequently `D` must be the full plane in (7), and the column and row
spaces of that rank-two diagonal show

```text
p,q in P=span(x,y).                                  (9)
```

Reducing (6) modulo `P` in either tensor factor then gives

```text
A(X),B(X) subset P.                                 (10)
```

Thus both images of `span(s)+X` are contained in the two-plane `P`.
Rank three forces both `A(d)` and `B(d)` to lie outside `P`.

In the application below there is also the identity

```text
G=(1/2)(p tensor q-A(d) tensor B(d)),                (11)
```

up to the harmless normalization convention for `Sym`.  If
`G in P tensor P`, then (9) and (11) put
`A(d) tensor B(d)` in `P tensor P`.  A nonzero pure tensor lies in
`P tensor P` only when both factors lie in `P`, contradicting the
rank-three conclusion.  Therefore the application of the lemma leaves
only

```text
p=q=0.                                               (12)
```

The proof uses only ranks, tensor-factor quotients, and the two
diagonal lines; it does not enumerate local maps.

## Applying the lemma

Set

```text
s=e_1+e_2,
d=e_1-e_2,
X=span(e_0,e_3,e_4),
A=L_C,
B=L_D.                                               (13)
```

The three doubled-colour contractions are

```text
(u_0,h_1,h_1) contract P_5=-2b x_4(x_1+x_2),
(u_0,h_2,h_2) contract P_5=-2c x_3(x_1+x_2),

(u_0,h_1,h_2) contract P_5
 =a x_1x_2+(x_1+x_2)(x_0-bx_3-cx_4).                (14)
```

Their target images lie on the doubled-colour line
`C(e_0 tensor e_0)`.  Combining (14) with (3) gives

```text
F(X) subset span(e_0 tensor e_0,G).                  (15)
```

This is exactly the diagonal-pencil lemma.  The elementary identity

```text
Sym(e_1,e_2)
 =(1/2)(s tensor s-d tensor d)                       (16)
```

gives (11).  Hence (12) holds:

```text
L_C(s)=L_D(s)=0.                                     (17)
```

There are now two exact outcomes.

### Zero residual

If `G=0`, equations (16)--(17) imply

```text
L_C(d) tensor L_D(d)=0.
```

One of `L_C,L_D` therefore kills both `s` and `d`, hence kills all of
`span(e_1,e_2)`.  Its rank is three, so its kernel is exactly that
two-plane and its row space is

```text
span(e_0^*,e_3^*,e_4^*).
```

Both `h_1` and `h_2` lie in this row space.  This is the promised third
common incidence.

### Apparent nonzero-residual boundary

If `G` is nonzero, it is proportional to either
`e_1 tensor e_1` or `e_2 tensor e_2`.  Equations (16)--(17) imply that
both `L_C(d)` and `L_D(d)` are nonzero and lie on that same target
line.  Therefore

```text
ker(L_C restricted to span(e_1,e_2))
 =ker(L_D restricted to span(e_1,e_2))
 =span(e_1+e_2),                                     (18)
```

and both restrictions have the same singleton target image line.  This
looks like a remaining common-kernel boundary, but the original two
singleton contractions rule it out.

## Quotient obstruction to the nonzero residual

Assume first that

```text
G is proportional to e_1 tensor e_1.                 (19)
```

The contraction `u_2 contract P_5` is

```text
Sym(e_1,e_2,e_3,e_0+c e_4).                          (20)
```

Quotient the target at modes `C,D` by the line `C e_1`.  Their
restrictions to `span(e_1,e_2)` vanish in the quotient by (18), so only
the assignments of `e_3,e_0+c e_4` to `C,D` survive.  The projected
four-tensor factors across `AB|CD` as

```text
(L_A tensor L_B) Sym(e_1,e_2)
tensor
(bar L_C tensor bar L_D) Sym(e_3,e_0+c e_4).         (21)
```

The target of (20) is a nonzero multiple of `e_2^4`, which remains
nonzero in this quotient.  Hence the first factor in (21) is a nonzero
pure tensor on the target `e_2` lines.

At each of `A,B`, the row space contains the independent covectors
`h_1,h_2`, both of which vanish on `span(e_1,e_2)`.  Therefore the
restriction of each of `L_A,L_B` to that source two-plane has rank at
most one.  The nonzero first factor in (21) forces both restrictions to
have rank one and image exactly `C e_2`.

Return to (1).  Since `h_1` vanishes on the source two-plane, this
forces

```text
q_A=q_B=0.
```

The hypothesis (19) and (4)--(5) force
`p_A p_B != 0`.  Thus at both `A,B`, the two pullbacks in (1) span the
target covectors annihilating `e_2`.  After quotienting the target by
`C e_2`, both induced maps from

```text
X=span(e_0,e_3,e_4)
```

therefore have the same kernel

```text
k=span(e_0+b e_3+c e_4),                             (22)
```

the common annihilator in `X` of `h_1,h_2`.

Now apply this quotient at `A,B` to (20).  Its target `e_2^4`
vanishes, while the `C,D` image of `Sym(e_1,e_2)` is the nonzero tensor
`G`.  Hence one would need

```text
(bar L_A tensor bar L_B) Sym(e_3,e_0+c e_4)=0.       (23)
```

But modulo the common kernel (22),

```text
e_0+c e_4 = -b e_3,
```

so the left side of (23) is

```text
-2b bar L_A(e_3) tensor bar L_B(e_3),                (24)
```

which is nonzero because `b != 0` and `e_3` is not in (22).  This is a
contradiction.

If instead `G` is proportional to `e_2 tensor e_2`, interchange the
two singleton colours.  The contraction

```text
u_1 contract P_5=Sym(e_1,e_2,e_4,e_0+b e_3)
```

and quotient by the target `e_1` line give the same common kernel
(22).  Modulo it,

```text
e_0+b e_3=-c e_4,
```

so the required zero quotient is the nonzero tensor

```text
-2c bar L_A(e_4) tensor bar L_B(e_4).
```

This contradicts `c != 0`.  The nonzero-residual boundary is therefore
empty.

## Consequence and remaining boundary

Only the zero-residual branch survives, and it has a third mode
containing both normals.  It can be reselected as an adjacent incidence
type: choose one pair for `h_1` and a different overlapping pair for
`h_2`.

Consequently, when `bc != 0`, the parallel type is not a separate
minimal incidence boundary.  The next exact targets are the adjacent
and disjoint types and the parameter boundaries.

The parameter boundaries `b=0` or `c=0`, and the adjacent and disjoint
incidence types, are not addressed here.

## Verification

Run:

```text
python verify_p5_q4_211_parallel_incidence.py
python audit_p5_q4_211_parallel_incidence.py
```

The primary verifier differentiates the source permanent, checks
(4), (14), (16), and the two quotient identities (24), and verifies the
matrix-pencil rank facts over `Q`.  The independent audit exhausts the
diagonal-pencil lemma and both common-kernel quotient contradictions
over `F_3` and `F_5`, and rederives the contractions from apolar
derivatives.  The finite-field census audits the linear-algebra case
split; the proof above is characteristic zero.
