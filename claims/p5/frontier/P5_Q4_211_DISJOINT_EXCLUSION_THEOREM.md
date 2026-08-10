# Exclusion of exact disjoint normalized `q4_211`

## Status

This note exactly excludes the generic exact disjoint
singleton-normal incidence type of normalized `q4_211` over `C`.

Assume

```text
a b c != 0,
h_1 in R_A,R_B only,
h_2 in R_C,R_D only.
```

The conic-polarity theorem forces one normal pair to share the kernel

```text
s=e_1+e_2
```

on its ternary support.  The argument below propagates that kernel,
leaves only two exact kernel architectures, and excludes both:

```text
(s,s,s,s)
or
(s,s,d,s),   d=e_1-e_2.                             (1)
```

Consequently the exact disjoint type is empty on `abc != 0`.

This does **not** exclude the remaining adjacent one-cross gates, the
parameter boundaries `a=0`, `b=0`, `c=0`, all normalized `q4_211`,
`P_5 -> Delta_3`, or the global Krenn--Gu conjecture.

## Starting from the polarity kernel

By colour interchange, assume

```text
L_A(s)=L_B(s)=0.                                    (2)
```

The disjoint polarity theorem also says that all four restrictions to

```text
H=span(s,d,e_0-b e_3-c e_4)
```

have rank two and that all four kernel lines lie in `span(s,d)`.
In particular,

```text
L_A(d),L_B(d) != 0.                                 (3)
```

Write the target covectors pulling back to the singleton normals as

```text
x_i=(r_i,0,q_i),   i=A,B,   L_i^*x_i=h_1,
y_j=(s_j,p_j,0),   j=C,D,   L_j^*y_j=h_2.           (4)
```

Repeated `h_2` contraction gives

```text
(u_1,h_2,h_2) contract P_5=-2c Sym(e_1,e_2).        (5)
```

Through `A,B`,

```text
(L_A tensor L_B)Sym(e_1,e_2)
 =-(1/2)L_A(d) tensor L_B(d),                       (6)
```

up to the harmless convention for `Sym`.  Equations (3), (5) make
this nonzero, while the target is proportional to

```text
p_Cp_D e_1 tensor e_1.
```

Therefore

```text
p_Cp_D != 0,
L_A(d),L_B(d) in C^*e_1.                            (7)
```

The doubled-colour repetition is

```text
(u_0,h_2,h_2) contract P_5=-2c Sym(e_3,s).          (8)
```

Its image through `A,B` is zero by (2).  On the target it is
proportional to `s_Cs_D e_0^2`, so

```text
s_Cs_D=0.                                           (9)
```

Relabel `C,D` and normalize so that

```text
L_C^*e_1^* in C^*h_2.                               (10)
```

Thus the `h_2` row at `C` is a pure target-colour-one row.

## Propagating the kernel to a third mode

Fourfold differentiation gives

```text
(u_0,h_1,h_1,h_2) contract P_5=2b s.                (11)
```

Use the two `h_1` rows at `A,B` and the pure `h_2` row at `C`.
At the target, distinguished colour zero and mode-`C` colour one
cannot lie in one diagonal term, so the contraction is zero.  Equation
(11) leaves only mode `D`, hence

```text
L_D(s)=0.                                           (12)
```

The rank-two restriction at `D` has its kernel in `span(s,d)`;
therefore its kernel is exactly `C s` and

```text
L_D(d) != 0.                                        (13)
```

Using the `h_2` row at `D` rather than `C` in (11) leaves mode `C`.
The target can only be on doubled colour zero, so

```text
L_C(s) in C e_0.                                    (14)
```

Now repeat `h_1`:

```text
(u_2,h_1,h_1) contract P_5=-2b Sym(e_1,e_2).        (15)
```

Through `C,D`, equation (12) turns its image into a nonzero scalar
multiple of

```text
L_C(d) tensor L_D(d).                               (16)
```

There are two cases.

### Nonzero `L_C(d)`

Equations (13), (15)--(16) imply

```text
q_Aq_B != 0,
L_C(d),L_D(d) in C^*e_2.                            (17)
```

The kernel of `L_C|H` lies in `span(s,d)`, so
`L_C(s),L_C(d)` are linearly dependent.  Equations (14), (17) put
them on independent target coordinate lines unless

```text
L_C(s)=0.                                           (18)
```

Together with (2), (12), all four maps kill `s`.  This is the first
architecture in (1).

### Zero `L_C(d)`

The kernel of `L_C|H` is exactly `C d`; hence

```text
L_C(s) in C^*e_0,   q_Aq_B=0.                       (19)
```

This is the second architecture in (1).  It will be excluded before
the all-`s` case.

## Excluding the `3s+1d` architecture

Assume (19), and interchange `A,B` if necessary so that `q_A=0`.
Then `x_A` in (4) is a nonzero multiple of target `e_0^*`.
Distinguished `u_2` pulls back target `e_2^*`, so diagonality gives

```text
(tensor over B,C,D)
  ((u_2,h_1) contract P_5)=0.                       (20)
```

But

```text
(u_2,h_1) contract P_5
 =-Sym(e_1,e_2,w_-),
w_-=e_0-b e_3+c e_4.                               (21)
```

Use (2), (12), and `L_C(d)=0`.  Thus

```text
L_B(e_2)=-L_B(e_1),
L_D(e_2)=-L_D(e_1),
L_C(e_2)= L_C(e_1).
```

The six terms in (21) cancel in pairs except

```text
-2 L_B(e_1) tensor L_C(w_-) tensor L_D(e_1).        (22)
```

The two outside factors are nonzero by the exact kernel statements at
`B,D`.  Equations (20)--(22) force

```text
L_C(w_-)=0.                                         (23)
```

The ambient kernel of `L_C` has dimension two and now contains the
independent vectors `d,w_-`.  Therefore its row space contains

```text
n=(0,0,0,c,b),                                      (24)
```

which annihilates both.

Every `n` row pulls back from target `e_0^*`, by the support-two
orthogonality identity in the one-cross theorem.  At `C`, equation
(10) pulls `h_2` back from `e_1^*`.  Both rows annihilate

```text
J_-=span(e_1,e_2,w_-),
```

so `L_C(J_-)` must lie in the common target annihilator line
`C e_2`.  Yet `s` belongs to `J_-`, while (19) gives the nonzero vector

```text
L_C(s) in C^*e_0.
```

This contradiction excludes the `3s+1d` architecture.

## Excluding the all-`s` architecture

It remains to assume

```text
L_i(s)=0,   i=A,B,C,D.                              (25)
```

Equations (7), (17) give the exact doubled-factor colours

```text
L_A(d),L_B(d) in C^*e_1,
L_C(d),L_D(d) in C^*e_2.                            (26)
```

The doubled-colour contraction is

```text
u_0 contract P_5
 =Sym(e_3,e_4,
      a Sym(e_1,e_2)+Sym(e_0,s)).                   (27)
```

Every term in the second summand is killed by (25).  Modulo the common
kernel `s`, the first summand has two factors proportional to `d`.
For its target `e_0^4` coefficient, whichever two modes receive those
`d` factors contribute zero: by (26), no `L_i(d)` has a target
colour-zero component.  Hence the `e_0^4` coefficient of (27) is zero.

The normalized target requires that coefficient to be the nonzero
diagonal scalar `lambda_0`.  This final contradiction excludes the
all-`s` architecture and proves the theorem.

## Consequence

On `abc != 0`, none of the three minimal singleton-normal incidence
types remains:

- the parallel type acquires extra incidence and reselects as
  adjacent;
- the exact disjoint type is excluded here;
- the adjacent two-cross type is excluded, while its one-cross type is
  confined to four explicit gates.

Thus the generic normalized `q4_211` frontier is now entirely the
adjacent one-cross gate list plus the parameter boundaries.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q4_211_disjoint_exclusion.py
python claims/p5/frontier/audit_p5_q4_211_disjoint_exclusion.py
```

The primary verifier differentiates (5), (8), (11), (15), (21),
checks the six-term cancellation (22), the new normal (24), and the
vanishing doubled-colour coefficient.  The independent audit rebuilds
the contractions by squarefree dynamic differentiation over
`F_5,F_7` and checks the kernel-pattern cancellations without importing
the primary code.  It enumerates no ambient maps or Grassmannians.  The
finite-field calculations audit the formulas; the exclusion above is
over `C`.
