# Weighted `H22` obstruction at the rank-one projected-image collapse

## Status

This is an exact characteristic-zero theorem on the normalized ninth
pure-`P_4` component.

The rank-one weighted projection stratum

```text
rS=1,             T=rU
```

has empty marked `H22` fibre.  Together with
[`P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md`](P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md),
this closes the weighted `H22` fibre on the component's entire
normalized affine chart.

The proof uses compatibility of the two marked contractions.  The
collapsed `D_01^r` slice forces its mode-zero marking; the required
pure `D_23^r` slice then becomes an apolar insertion map at
`[S:-1:0]`.  Its Fitting support has only `S=1` and `S=-1`, and both
special kernels kill one of the two required nonzero coefficients.

The theorem does not close the component's omitted
normalization/projective boundary, prove component exhaustiveness,
produce a prize graph, or resolve the global Krenn--Gu conjecture.

## The collapse forces the marking

Use the normalized bases

```text
alpha_0=(0, 1,S,U),       beta_0=(1, 0,1,T),

alpha_1=(0,-1,1,0),       beta_1=(0,-1,0,1),
alpha_2=(0, 1,0,1),       beta_2=(0, 1,1,0),
alpha_3=(0, 0,1,1),       beta_3=(0,-1,0,1),       (1)
```

and

```text
D_01^r(z,e)=(r z_0+z_1,z_2,z_3,e),
D_23^r(z,e)=(z_0,z_1,r z_2+z_3,e).                (2)
```

On the collapse, `S!=0` and

```text
r=1/S,             T=U/S.                         (3)
```

The projected mode-zero source rows of `D_01^r` are

```text
a=(1,S,U),          b_r=r a.                      (4)
```

Let `A_01` be the all-alpha coefficient.  A genuine `Delta_2`
compression requires `A_01!=0`.  If
`beta_0(t_0)=beta_0+t_0 alpha_0`, then the coefficient with mode zero
beta and the other three modes alpha is

```text
(r+t_0) A_01.                                     (5)
```

It is an unwanted mixed coefficient, so

```text
t_0=-r.                                            (6)
```

The projected source part of the marked beta row is now zero.  Its
extension entry `y_0` supplies the opposite diagonal, exactly

```text
B_01=-2y_0,
```

so `y_0!=0`.

## The other marked contraction is an insertion matrix

In an `H22` compression, the other marked contraction must be either
pure or `Delta_2`, and at least one of the two must be `Delta_2`.
Every coefficient in the mode-zero alpha slice of `D_23^r` is
structurally zero, because all four alpha rows have source coordinate
zero equal to zero.  Hence, once `D_01^r` is the genuine `Delta_2`
slice, `D_23^r` must be a **nonzero pure all-beta** slice.

After (6), its projected mode-zero beta row is

```text
(1,-1/S,0,y_0).
```

Undo the harmless shears in modes `1,2,3`.  If their marked extension
coordinates are `(x_i,y_i)`, put

```text
z_i=y_i-t_i x_i.
```

The physical vector

```text
(beta_i+t_i alpha_i,y_i)
 =(beta_i,z_i)+t_i(alpha_i,x_i)
```

shows that being a pure all-beta tensor is unchanged by this basis
shear, and its all-beta coefficient is unchanged on the pure locus.
We may therefore set `t_1=t_2=t_3=0`.

Order the seven unwanted beta-slice words as

```text
000,001,010,011,100,101,110
```

and the extension columns as

```text
(x_1,x_2,x_3,z_1,z_2,z_3).
```

Their coefficient matrix is

```text
N_S =
[(S+1)/S, -(S+1)/S, (1-S)/S,       0,        0,       0]
[      0, -(S+1)/S,       0,       0,        0, (1-S)/S]
[(S+1)/S,        0,       0,       0, -(S+1)/S,       0]
[(S-1)/S,        0,       0,       0, -(S+1)/S,       0]
[      0, -(S+1)/S,       0, (S+1)/S,        0,       0]
[      0,         -2,       0,       0,        0,       0]
[      0,          0, (S-1)/S, (S+1)/S, -(S+1)/S,    0].
                                                               (7)
```

Its seven maximal minors, obtained by deleting one row, are

```text
4(S-1)^2(S+1)^2/S^5 times (-1,0,1,0,1,0,-1).     (8)
```

Thus `N_S` is injective unless `S=1` or `S=-1`.

## The two exceptional fibres

For `S=1`,

```text
ker N_1=<x_3,z_3>.                                (9)
```

The desired all-beta coefficient of `D_23^r` is the covector

```text
d_S=((S-1)z_1-2S z_2+(S-1)z_3)/S.                (10)
```

Equation (10) vanishes identically on (9).  Hence the `D_23^r` slice
is zero rather than nonzero pure.

For `S=-1`,

```text
ker N_{-1}=<z_1,z_2>.                             (11)
```

In particular every alpha extension `x_i` vanishes.  But the required
first diagonal of `D_01^r` is

```text
A_01=
 (1+S+U)x_1+(1-S-U)x_2+(1-S+U)x_3.               (12)
```

It therefore vanishes on (11).

If `S` is neither exceptional, (8) forces all six extensions to
vanish, and (12) again gives `A_01=0`.  Every point of the collapse
therefore loses either the genuine `D_01^r` diagonal or the nonzero
pure `D_23^r` coefficient.  No binary `H22` compatibility exists, so
no ternary lift exists.

## Cross-specialty interpretation

The collapsed projective line is not handled by taking a limit of the
rank-two factor cover.  It is a change of matrix-pencil type.  The
second marked contraction supplies the missing transverse pencil, and
its Kronecker/Fitting data are the seven minors (8).  This is the same
invariant-first viewpoint used in basis-free reductions of matrix
pencils
([Verdier](https://arxiv.org/abs/1205.1138)) and in the hierarchy of
minimal pencil ranks
([Goulart--Comon](https://arxiv.org/abs/1712.05742)).
Here the pencil has only two singular fibres, and its kernel covectors
annihilate exactly the coefficients needed by the graph problem.

## Verification

Run

```text
python claims/p5/h22/embedded-p3/verify_p5_h22_embedded_p3_component_rank_one_collapse.py
python claims/p5/h22/embedded-p3/audit_p5_h22_embedded_p3_component_rank_one_collapse.py
```

The primary verifier derives (5), reconstructs the shear law and
matrix (7), checks all seven maximal minors, and verifies both special
kernels and diagonal covectors symbolically.  The independent audit
rebuilds the permanent coefficients by squarefree subset
multiplication and checks the generic and two special fibres over two
finite fields.  The modular audit is corroboration only; the theorem
is the characteristic-zero calculation above.
