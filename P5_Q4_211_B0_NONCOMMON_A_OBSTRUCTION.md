# Noncommon-`A` obstruction on the `b=0` boundary of `q4_211`

## Status

This note sharpens the coordinate-normal reduction on

```text
b=0,   a c != 0.                                    (1)
```

Use the two forced `e_3` incidences

```text
L_A^*e_0^*=e_3,
L_B^*e_2^*=e_3
```

from
[`P5_Q4_211_B0_COORDINATE_NORMAL_REDUCTION.md`](P5_Q4_211_B0_COORDINATE_NORMAL_REDUCTION.md).
The earlier reduction forces `h_2` at `B` and at least one of `C,D`.
The present theorem proves

```text
h_2 in R_A.                                         (2)
```

Consequently, after interchanging `C,D`,

```text
h_2 in R_A,R_B,R_C,
L_D(e_1+e_2)=0,                                     (3)
```

with possible additional containment `h_2 in R_D`.

This is a strict boundary reduction, not an exclusion of (3), all
normalized `q4_211`, `P_5 -> Delta_3`, or the global Krenn--Gu
conjecture.

## The alleged noncommon architecture

Suppose `h_2 notin R_A`.  The coordinate-normal theorem then forces
the exact containment set

```text
h_2 in R_B,R_C,R_D.                                 (4)
```

Put

```text
s=e_1+e_2,
d=e_1-e_2,
k=e_0+c e_4,
J=span(e_1,e_2,k).
```

The simultaneous mixed contraction

```text
T=(u_2,e_3) contract P_5=P_3(e_1,e_2,k)             (5)
```

maps to a nonzero pure target-colour-two cube through `A,C,D` and to
zero through `B,C,D`.

The nonzero decomposable-`P_3` theorem applies to the first triple.
Its three restricted kernels form a support-two sign chart.  The
kernel propagation in the coordinate-normal theorem already gives

```text
L_A(s)=0.                                           (6)
```

Hence the other two kernel lines belong to

```text
{C s,C d},
```

are not both `C s`, and form one of

```text
(d,d), (s,d), (d,s)                                 (7)
```

at `C,D`.

## The zero chart marks `B` by `h_0` or `u_2`

The restriction at `B` has rank one on `J`, since its row space
contains

```text
J^perp=span(e_3,h_2).
```

Let `g=(g_0,g_1,g_2)` be its nonzero source functional in the basis
`(e_1,e_2,k)`.  Contracting (5) at `B` gives the zero-diagonal
quadratic

```text
M_g=[
 [  0, g_2, g_1 ],
 [g_2,   0, g_0 ],
 [g_1, g_0,   0 ]
].                                                   (8)
```

Its restriction between the two row planes at `C,D` must vanish.
For the three kernel pairs in (7), exact two-by-two multiplication
gives:

```text
(d,d): g_2=0, g_0+g_1=0;
(s,d): g_0=g_1=0;
(d,s): g_0=g_1=0.                                   (9)
```

Thus either

```text
g in C d
or
g in C k^*.                                         (10)
```

Modulo `J^perp`, the first line is represented by

```text
h_0=e_1-e_2,
```

and the second by `e_0^*`.  Since

```text
u_2=2c e_0^*-h_2,
```

equation (10) says

```text
h_0 in R_B
or
u_2 in R_B.                                         (11)
```

The direction alternative is impossible.  If
`L_B^* beta=u_2`, symmetry of the source tensor `(u_2,e_3) contract
P_5` compares:

- distinguished `u_2` and the colour-two `e_3` row at `B`, giving a
  nonzero target `e_2^3`; and
- distinguished `e_3` and `beta`, giving a multiple of `e_1^3`.

The two pure target lines are independent.  Hence

```text
h_0 in R_B,                                         (12)
```

and (7), (9) force

```text
L_C(d)=L_D(d)=0.                                    (13)
```

Since the three rows `e_3,h_2,h_0` span `R_B`, they all annihilate
`s`, so

```text
L_B(s)=0.                                           (14)
```

## Fixing the target colour of `h_2` at `B`

The pure tensor (5), together with (6), (13), collapses to

```text
2 L_A(k) tensor L_C(e_1) tensor L_D(e_1)
 =nonzero scalar * e_2^3.                           (15)
```

In particular

```text
L_C(E)=L_D(E)=C e_2,
E=span(e_1,e_2).                                    (16)
```

The simultaneous cubic

```text
(u_0,e_3) contract P_5
```

is zero through `A,C,D` and nonzero pure target colour zero through
`B,C,D`.  Contract both versions by the `h_2` rows at `C,D`.  Since

```text
(u_0,e_3,h_2,h_2) contract P_5=-2c s,               (17)
```

equations (6), (14) imply that the target-colour-zero components of
the two `h_2` covectors at `C,D` have zero product.  Relabel them so
the row at `C` is pure target colour one.

The triple-`h_2` contraction is zero.  Its target-colour-one
coefficient now says that either the `h_2` row at `B` or the row at
`D` is pure target colour zero.  The latter option is impossible:
using the pure colour-one row at `C` and pure colour-zero row at `D`
in

```text
(u_1,h_2,h_2) contract P_5=-2c Sym(e_1,e_2)
```

would make the image through `A,B` zero.  But (6), (14) make both
restrictions on `E` nonzero rank-one maps with the same functional
`(1,-1)`, on which the binary permanent is nonzero.

Therefore

```text
h_2=L_B^*e_0^*                                      (18)
```

up to scale.  The other selected row at `B` is
`e_3=L_B^*e_2^*`, and the remaining target direction has a nonzero
`h_0` component.

## Paired zero charts determine the kernel at `A`

Using (18), the cross contraction

```text
(u_1,h_2) contract P_5
 =-P_3(e_1,e_2,e_0-c e_4)                           (19)
```

maps to zero through `A,C,D`.  Equations (6), (13), (16) cancel every
term except the one assigning the third factor to `A`.  Hence

```text
L_A(e_0-c e_4)=0.                                   (20)
```

The kernel of `L_A` is exactly the span of the independent vectors in
(6), (20).  Its row space therefore contains

```text
h_0=e_1-e_2,
u_2=c e_0+e_4.                                      (21)
```

## Final paired-chart contradiction

The pure target-colour-one row at `C` makes

```text
(u_1,h_2) contract P_5
 =-P_3(e_1,e_2,w),
w=e_0-c e_4,                                        (22)
```

map to a nonzero pure `e_1^3` tensor through `A,B,D`.  Here `A,B`
kill `s`, `A` also kills `w`, and `D` kills `d`.  The six terms cancel
except those assigning `w` to `D`:

```text
-2 L_A(e_1) tensor L_B(e_1) tensor L_D(w).          (23)
```

Both first factors are nonzero, and `L_B(E)=C e_1` because its
target-colour-zero and target-colour-two rows are `h_2,e_3`.
Consequently

```text
L_A(E)=C e_1,
L_D(w) in C^*e_1.                                   (24)
```

Now use the pure target-colour-zero `h_2` row at `B`.  The source
contraction is

```text
(u_0,h_2) contract P_5
 =-Sym(e_3,
       a Sym(e_1,e_2)-c Sym(e_1+e_2,e_4)
       +Sym(e_0,e_1+e_2)),                          (25)
```

and it must map through `A,C,D` to a nonzero pure `e_0^3` tensor.
Under (6), (13), (16), and (20), direct six-term cancellation factors
its image as

```text
-2 L_A(e_3) tensor [
     L_C(w) tensor L_D(e_1)
    +L_C(e_1) tensor L_D(w)
    +a L_C(e_1) tensor L_D(e_1)].                   (26)
```

Inspect the bracket coefficient with target colour two at `C` and
target colour one at `D`.  The first and third terms have
`L_D(e_1) in C e_2` and contribute zero.  The middle term is nonzero
by (16), (24):

```text
(e_2^*L_C(e_1))(e_1^*L_D(w)) != 0.
```

But the target of (25) is pure colour zero, so that mixed coefficient
must vanish.  This final contradiction proves (2).

## Propagating the surviving kernel

Now `h_2` occurs at both `A,B`, and exact parallel incidence has
already been excluded.  Choose a third occurrence at `C`.  Use the
zero `(u_0,e_3)` contraction with the colour-two `e_3` row at `B` and
the `h_2` rows at `A,C`.  Equation (17) leaves only mode `D`, so

```text
L_D(s)=0.
```

This proves (3).

## Verification

Run:

```text
python verify_p5_q4_211_b0_noncommon_a.py
python audit_p5_q4_211_b0_noncommon_a.py
```

The primary verifier checks the three zero-chart systems (9), all
contractions (17), (19), (22), (25), and the cancellation (26).  The
independent audit repeats the sign and rank calculations over
`F_5,F_7`.  It enumerates no ambient maps or Grassmannians.  The
finite-field calculations audit the formulas; the proof above is over
`C`.
