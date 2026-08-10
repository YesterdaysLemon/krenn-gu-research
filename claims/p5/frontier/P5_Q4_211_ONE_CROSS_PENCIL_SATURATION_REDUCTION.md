# One-cross normal-pencil saturation in normalized `q4_211`

## Status

This is an exact characteristic-zero reduction of the sole generic
adjacent boundary left after exclusion of the marked two-cross case.

Assume `bc != 0`, a mode `A` contains both

```text
h_1=(b,0,0,-1,0),
h_2=(c,0,0,0,-1),
```

and exactly one adjacent cross residual is nonzero.  The earlier
rank-drop argument forces another mode to contain

```text
n=(0,0,0,c,b).
```

The present theorem recasts that fourth-normal incidence as a
projective pencil problem.  In the orientation where the `q` residual
is nonzero, one of the other three row spaces necessarily contains

```text
span(h_1,n).                                        (1)
```

Moreover, exactly one of the following further reductions occurs:

1. one of the other three row spaces contains `span(h_2,n)`;
2. `L_A(e_1+e_2)=0`; or
3. the other three row spaces contain, in some order, the three
   distinguished normal lines

   ```text
   C h_2,   C n,   C u_1,
   u_1=(b,0,0,1,0).                                 (2)
   ```

In alternative 3, the target covectors pulling back those three lines
all annihilate target colour two.  Among them, at least one also
annihilates target colour zero and at least one annihilates target
colour one.

At every mode containing `n`, its pullback target covector is a
nonzero multiple of `e_0^*`.

The colour-swapped statement replaces

```text
(h_2,u_1,target colour two)
```

by

```text
(h_1,u_2,target colour one),
u_2=(c,0,0,0,1).                                    (3)
```

In that orientation a mode necessarily contains `span(h_2,n)`, and
the three further alternatives use `span(h_1,n)`, the same common-mode
kernel, or the rigid lines `h_1,n,u_2`.

This is a strict reduction, not an exclusion of the three alternatives,
all adjacent incidence, normalized `q4_211`, `P_5 -> Delta_3`, or the
global Krenn--Gu conjecture.

## The target colour of the fourth normal

Put

```text
m=c u_1-b u_2=(0,0,0,c,-b).
```

The support-two direction `m` and the fourth normal satisfy

```text
(m,n) contract P_5=0.                               (4)
```

If `n=L_i^* zeta` at any remaining mode, contract the target identity
by `c e_1^*-b e_2^*` at the distinguished mode and by `zeta` at mode
`i`.  Equation (4) gives

```text
c lambda_1 zeta[1] e_1^3
-b lambda_2 zeta[2] e_2^3=0.
```

Since `b,c,lambda_1,lambda_2` are nonzero,

```text
zeta[1]=zeta[2]=0.                                  (5)
```

Thus every occurrence of `n` is the pullback of target colour zero.

## Orientation with the `q` residual

At the common mode, write the target covectors pulling back to
`h_1,h_2` as

```text
x_A=(r,0,q),
y_A=(t,p,0).
```

Consider first

```text
q != 0,   p=0.                                      (6)
```

Injectivity of pullback makes `t != 0`.  Thus `h_2` is the pullback of
a nonzero multiple of target `e_0^*`, and

```text
L_A(span(e_1,e_2)) subset C e_1.                    (7)
```

The nonzero cross identity is

```text
(tensor_(i!=A) L_i) Sym(e_1,e_2,w_-)
  =kappa e_2 tensor e_2 tensor e_2,
kappa != 0,                                         (8)
```

where

```text
w_-=e_0-b e_3+c e_4.
```

The other singleton contraction at `A` is simultaneously zero:

```text
(tensor_(i!=A) L_i) Sym(e_1,e_2,w_+)=0,
w_+=e_0+b e_3-c e_4.                                (9)
```

Indeed, `u_1` pulls back target `e_1^*` at the distinguished
mode, while `h_2` pulls back target `e_0^*` at `A`; two different
colours annihilate the target diagonal.

If every restriction to

```text
J_+=span(e_1,e_2,w_+)
```

had rank at least two, the zero-`P_3` theorem would make all three row
planes one common coordinate plane.  Killing `e_1` or `e_2` would also
kill the nonzero tensor (8).  Killing `w_+` is impossible at the
selected `h_2`-mode because

```text
h_2(w_+)=2c != 0.
```

Therefore some restricted map has rank one.  Since

```text
J_+^perp=span(h_1,n),
```

its ambient row space contains the whole plane in (1).  This proves
the mandatory opposite-pencil incidence.

Put

```text
J_-=span(e_1,e_2,w_-).
```

Its annihilator is the normal pencil

```text
J_-^perp=span(h_2,n).                               (10)
```

Let `B,C,D` denote the three modes in (8), with `C` a selected
`h_2`-mode and `X` a mode containing `n`.

If some `L_i|J_-` has rank one, then

```text
dim(R_i intersect J_-^perp)=2,
```

so its row space contains all of `span(h_2,n)`.  This is further
alternative 1.

Otherwise every restricted rank is at least two.  The nonzero
decomposable-`P_3` classification applied to (8) makes all three ranks
exactly two.  Hence

```text
ell_i=R_i intersect J_-^perp
```

is one projective line at each mode.  In particular, `X != C` and

```text
ell_C=C h_2,   ell_X=C n.                           (11)
```

Let `zeta_i` be the target covector whose pullback is a generator of
`ell_i`.  Since it annihilates the rank-two image of `J_-`, which
contains the pure factor `e_2`, one has

```text
zeta_i[2]=0.                                        (12)
```

## The polarized binary cubic

All rows in the pencil (10) are supported on source coordinates
`0,3,4`.  Write

```text
ell=A h_2+B n.
```

The restriction of the ternary permanent to the diagonal of this
two-plane is the binary cubic

```text
Perm_3(ell,ell,ell)
 =6 A B c^2(-A+bB).                                 (13)
```

Its three projective roots are

```text
C h_2,   C n,   C(b h_2+n)=C u_1,                  (14)
```

because

```text
b h_2+n=c u_1.
```

To see why the third line in (11) must be the third root, contract the
original tensor identity at `B,C,D` by generators of
`ell_B,ell_C,ell_D`.  The source contraction is

```text
T(ell_B,ell_C,ell_D) Sym(e_1,e_2),                  (15)
```

where `T` is the polarization of (13).  At the distinguished mode,
both `e_1,e_2` map to target `e_0`.  By (7), their images at mode `A`
lie on target `e_1`.

If

```text
L_A(e_1+e_2)=0,
```

we are in further alternative 2.  Otherwise (15) maps to a nonzero
multiple of the off-diagonal tensor

```text
e_0 tensor e_1
```

unless its scalar is zero.  But (12) makes the target contraction a
linear combination only of

```text
e_0 tensor e_0,   e_1 tensor e_1.
```

Therefore

```text
T(ell_B,ell_C,ell_D)=0.                             (16)
```

Using (11), write the third line as `C(Ah_2+Bn)`.
Direct polarization of (13) gives

```text
T(h_2,n,Ah_2+Bn)=2c^2(-A+bB).                       (17)
```

Equations (16)--(17) force the third line to be
`C(bh_2+n)=C u_1`, proving (2).

Once the off-diagonal source scalar vanishes, the diagonal target
coefficients must vanish separately.  Since every target diagonal
coefficient is nonzero before contraction,

```text
product_i zeta_i[0]=0,
product_i zeta_i[1]=0.                              (18)
```

This is the stated two-coordinate cover among the three annihilator
covectors.

## The colour-swapped orientation

If

```text
p != 0,   q=0,
```

then `h_1` pulls back from target `e_0^*`,

```text
L_A(span(e_1,e_2)) subset C e_2,
```

and the pure residual is

```text
Sym(e_1,e_2,w_+) -> kappa e_1^3,
w_+=e_0+b e_3-c e_4.
```

Now

```text
J_+^perp=span(h_1,n).
```

The simultaneous zero residual is `Sym(e_1,e_2,w_-)`.  If all three
of its local restrictions had rank at least two, the zero-`P_3`
theorem would force a common killed coordinate.  Killing `e_1` or
`e_2` contradicts the nonzero pure residual, while killing `w_-`
contradicts the selected `h_1` incidence because

```text
h_1(w_-)=2b != 0.
```

Hence one mode contains all of

```text
J_-^perp=span(h_2,n),
```

which is the colour-swapped mandatory incidence.

The corresponding binary cubic is

```text
Perm_3(Ah_1+Bn,Ah_1+Bn,Ah_1+Bn)
 =6 A B b^2(-A+cB),                                 (19)
```

with roots

```text
C h_1,   C n,   C(c h_1+n)=C u_2,
```

because `c h_1+n=b u_2`.  The proof above applies verbatim, with the
annihilator covectors lying in `span(e_0^*,e_2^*)` and satisfying the
two corresponding coordinate-cover products.

## Consequence

The generic adjacent branch is no longer an unconstrained
fourth-normal Schubert divisor.  It is confined to:

1. a mandatory mode containing the whole opposite normal pencil;
2. possibly a second rank-one restriction containing the pure-slice
   normal pencil;
3. the common-mode kernel `e_1+e_2`; or
4. one rigid three-line incidence set `h_2,n,u_1` or `h_1,n,u_2`,
   together with a two-coordinate target cover.

The binary cubic in (13), (19) is the specialization-specific invariant:
its third root is an original singleton pullback, so the new normal
cannot wander freely in its pencil.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q4_211_one_cross_pencil_saturation.py
python claims/p5/frontier/audit_p5_q4_211_one_cross_pencil_saturation.py
```

The primary verifier differentiates both pure residuals, reconstructs
the two annihilator pencils, polarizes the binary cubics, and checks
the third-root identities.  The independent audit uses a
dynamic-programming permanent over `F_5,F_7` and checks every
projective pencil line against the polarized root equation.  It
enumerates no ambient maps or Grassmannians.  The finite-field checks
audit the formulas and projective case split; the reduction above is
over `C`.
