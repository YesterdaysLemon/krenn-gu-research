# Common-kernel obstruction for adjacent one-cross normalized `q4_211`

## Status

This note exactly excludes the last common-kernel gate in the adjacent
one-cross branch of normalized `q4_211` over `C`.

Assume

```text
b c != 0.
```

Together with the direction-plane obstruction and the earlier
two-gate theorem, this proves on `abc != 0`:

> There is no adjacent one-cross normalized `q4_211` configuration on
> `abc != 0`.

The proof uses a binary bilinear polarity on
`E=span(e_1,e_2)`, followed by compatibility of the two polarized
`P_3` charts with third factors

```text
w_-=e_0-b e_3+c e_4,
w_+=e_0+b e_3-c e_4.
```

It does not use an ambient-map or Grassmannian search.

This gate lemma itself also applies when `a=0`.  It excludes neither
the separate non-kernel branches on that boundary, the parameter
boundaries `b=0`, `c=0`, nor all normalized `q4_211`,
`P_5 -> Delta_3`, or the global
Krenn--Gu conjecture.

## One-cross notation

It is enough to treat the `q` orientation.  Let:

- `A` be the original `h_1,h_2` common mode, with `h_2` pulled back
  from target `e_0^*`;
- `Y` be the mandatory opposite-pencil mode containing
  `span(h_1,n)`;
- `C` be another mode containing `h_2`; and
- `D` be the fourth mode.

Here

```text
h_1=(b,0,0,-1,0),
h_2=(c,0,0,0,-1),
n  =(0,0,0,c,b),
s=e_1+e_2,
d=e_1-e_2.                                         (1)
```

At both `A` and `Y`, the two displayed normal rows annihilate

```text
E=span(e_1,e_2).
```

Their target covectors have common annihilator `C e_1`, so

```text
L_A(E),L_Y(E) subset C e_1.                         (2)
```

Neither restriction is zero: otherwise its ambient row space would be
`E^perp=span(e_0^*,e_3^*,e_4^*)` and would contain
`h_1,h_2,n`, contrary to the previously excluded common-plus-`n`
boundary.

The two-gate theorem and the direction-plane obstruction say that the
only surviving possibility is

```text
L_A(s)=0
or
L_Y(s)=0.                                          (3)
```

## Binary polarity propagates the kernel

Repeated singleton-normal contraction gives

```text
(u_1,h_2,h_2) contract P_5
 =-2c Sym(e_1,e_2).                                 (4)
```

Use the `h_2` rows at `A,C`.  Distinguished colour one and the
target-colour-zero row at `A` are incompatible, so through `Y,D`,

```text
(L_Y tensor L_D)Sym(e_1,e_2)=0.                    (5)
```

The other repeated contraction is

```text
(u_2,h_1,h_1) contract P_5
 =-2b Sym(e_1,e_2).                                 (6)
```

Use the `h_1` rows at `A,Y`.  Both have nonzero target-colour-two
components, so through `C,D`,

```text
(L_C tensor L_D)Sym(e_1,e_2)
 =nonzero scalar * e_2 tensor e_2.                 (7)
```

Since `L_Y|E` has rank one and is nonzero, (5) makes `L_D|E` rank at
most one.  Equation (7) makes it rank exactly one and fixes its image:

```text
L_D(E)=C e_2.                                       (8)
```

Write the nonzero source functionals underlying the two rank-one maps
as

```text
L_Y|E=e_1 tensor ell_Y,
L_D|E=e_2 tensor ell_D.
```

Equation (5) is the binary polar relation

```text
ell_Y(e_1)ell_D(e_2)
+ell_Y(e_2)ell_D(e_1)=0.                            (9)
```

Fourfold differentiation now gives

```text
(u_0,h_1,h_2,n) contract P_5=-2bc s.               (10)
```

Use `h_1` at `A`, `h_2` at `C`, and `n` at `Y`.
The target contraction through the remaining mode `D` lies on
`C e_0`.  Equation (8) simultaneously puts `L_D(s)` on `C e_2`.
Therefore

```text
L_D(s)=0.                                          (11)
```

Thus `ell_D` is proportional to `(1,-1)`.  Substitution in (9) makes
`ell_Y` proportional to `(1,1)`, so

```text
L_Y(d)=0,
L_Y(s) != 0.                                       (12)
```

The gate (3) consequently occurs only at `A`:

```text
L_A(s)=0.                                          (13)
```

Finally, (7), (8), and (11) show that

```text
L_C(d) in C^* e_2.                                 (14)
```

## The selected `h_2` row at `C` is pure

Another fourfold contraction is

```text
(u_0,h_2,h_2,n) contract P_5=-2c^2 s.              (15)
```

Use `h_2` at `A,C` and `n` at `Y`.  By (11), the source side vanishes
after applying `L_D`.  On the target, the rows at the distinguished
mode, `A`, and `Y` are all target colour zero.  Hence the
target-colour-zero component of the `h_2` covector at `C` must vanish.
The general `h_2` covector has the form

```text
(r_C,p_C,0),
```

and is nonzero, so it is a multiple of `e_1^*`.  Consequently

```text
L_C(E) subset span(e_0,e_2).                        (16)
```

## The doubled-colour coefficient forces colour zero

The doubled-colour contraction is

```text
u_0 contract P_5
 =Sym(e_3,e_4,
      a Sym(e_1,e_2)+Sym(e_0,s)).                  (17)
```

By (2), (8), the target-colour-zero rows of `A,Y,D` vanish on all of
`E`.  In the first summand of (17), two distinct modes receive
`E` factors, so its `e_0^4` target coefficient is zero.  In the second
summand, the unique `E` factor `s` must be received by `C`.

Equivalently, if `rho_i=L_i^*e_0^*`, direct polarization factors that
coefficient as

```text
rho_C(s) *
Perm_3(rho_A|X,rho_Y|X,rho_D|X),
X=span(e_0,e_3,e_4).                               (18)
```

The normalized target coefficient `lambda_0` is nonzero.  Therefore

```text
e_0^* L_C(s) != 0.                                  (19)
```

In particular `L_C(s)` is nonzero and, by (16), has a nonzero
target-colour-zero component.

## The two `P_3` charts are incompatible

The nonzero one-cross residual at `A` is

```text
(u_2,h_1) contract P_5
 =-P_3(e_1,e_2,w_-)
 -> nonzero scalar * e_2^3                         (20)
```

through `Y,C,D`.  From (8), (11)--(12), write

```text
L_Y(e_1)= L_Y(e_2)=v_Y in C^*e_1,
L_D(e_1)=-L_D(e_2)=v_D in C^*e_2.
```

Expanding the six terms of the polarized permanent gives, for either
`w=w_-` or `w=w_+`,

```text
(L_Y tensor L_C tensor L_D)P_3(e_1,e_2,w)
 =-L_Y(w) tensor L_C(d) tensor v_D
  +v_Y tensor L_C(s) tensor L_D(w).                (21)
```

In (20), inspect the target coefficient whose `Y` coordinate is
colour one and whose `C` coordinate is colour zero.  The first term of
(21) has `C` coordinate colour two by (14), while the second has the
nonzero colour-zero component (19).  Since the target of (20) is pure
colour two,

```text
L_D(w_-)=0.                                        (22)
```

The simultaneous residual at `A` is zero:

```text
(u_1,h_2) contract P_5
 =-P_3(e_1,e_2,w_+)
 ->0.                                              (23)
```

Equation (21) now says

```text
L_Y(w_+) tensor L_C(d) tensor v_D
 =v_Y tensor L_C(s) tensor L_D(w_+).               (24)
```

The three vectors `s,w_-,w_+` are independent on `bc != 0`.  Since
`L_D` has a two-dimensional kernel, (11), (22) imply

```text
L_D(w_+) != 0.                                     (25)
```

Both sides of (24) are therefore nonzero decomposable tensors.  Equality
forces equality of their factor lines at every mode.  At mode `C`,
(14) then gives

```text
L_C(s) in C e_2,
```

contradicting (19).  This excludes the common-kernel gate.

## Colour-swapped orientation and consequence

The `p` orientation is obtained by interchanging singleton colours,
`h_1` with `h_2`, and source coordinates `3,4`.  The same binary
polarity and the same `w_+`,`w_-` compatibility give the identical
contradiction.

Hence adjacent one-cross incidence is empty on `abc != 0`.  Combined
with the exact parallel, disjoint, and two-cross analyses, every
singleton-normal incidence type in normalized `q4_211` is excluded on
this open parameter stratum.  Only the parameter boundary

```text
a b c=0
```

remains.

## Verification

Run:

```text
python verify_p5_q4_211_one_cross_common_kernel.py
python audit_p5_q4_211_one_cross_common_kernel.py
```

The primary verifier differentiates (4), (6), (10), (15), (20), and
(23), factors the `e_0^4` coefficient in (18), and checks the six-term
identity (21).  The independent audit reconstructs the contractions,
binary polarity, coefficient factor, and kernel independence over
`F_5,F_7`.  It enumerates no ambient maps or Grassmannians.  The
finite-field calculations audit the formulas; the proof above is over
`C`.
