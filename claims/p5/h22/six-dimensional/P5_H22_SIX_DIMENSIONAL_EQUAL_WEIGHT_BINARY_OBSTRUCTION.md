# Equal-weight binary `H22` obstruction on the six-dimensional `P_4` component

## Status

This is an exact characteristic-zero obstruction on the equal-weight
diagonal-source chart of the six-dimensional pure-compression component
proved in
[`P4_SIX_DIMENSIONAL_PURE_COMPONENT.md`](claims/p4/components/six-dimensional/P4_SIX_DIMENSIONAL_PURE_COMPONENT.md).

The two neighboring `H22` contractions meet the pure `P_4` slice along
the diagonal hyperplanes

```text
x_0=x_1,                  x_2=x_3.                   (1)
```

With the two displayed contractions normalized to equal weights, no
choice of binary marking and no extension in the fifth source direction
can make either neighboring restriction a nonzero `Delta_2`.  The
binary incidence is already empty, before the third target row is
considered.

This is **not** a generic component obstruction.  Restoring the
diagonal-source torus changes (1) to weighted pencils.  Those weighted
pencils have genuine binary survivor loci, so the equal-weight result
must not be promoted to the full component orbit.  Nothing here closes
those weighted slopes, the component's parameter/projective boundaries,
all of `H22`, or the global conjecture.

## Why the deletion is diagonal

Use the normalized `H22` source vectors

```text
v_0=e_0+e_1,        v_1=e_2+e_3,        v_2=e_4.     (2)
```

Contracting `P_5` with `v_2` gives the pure slice

```text
Sym(e_0,e_1,e_2,e_3).
```

The other two contractions are

```text
Sym(e_0+e_1,e_2,e_3,e_4),
Sym(e_0,e_1,e_2+e_3,e_4).                           (3)
```

Thus a covector

```text
r=(r_0,r_1,r_2,r_3,r_4)
```

restricts to the two neighboring `P_4` source bases as

```text
D_01(r)=(r_0+r_1,r_2,r_3,r_4),
D_23(r)=(r_0,r_1,r_2+r_3,r_4).                      (4)
```

This is the important difference from `H31`: the common three-space is
not a coordinate hyperplane in the factor basis of the pure `P_4`.
The problem is a diagonal-hyperplane incidence, not a coordinate
deletion with target colors renamed.

## The six-dimensional apolar basis

Over

```text
K=C(s,d,u,v)
```

put `h=s-d` and use the canonical basis

```text
alpha_0=(1,0,0,-1)
beta_0 =(0,0,1,1)

alpha_1=(s v,v-u,-s u,d(v-u))
beta_1 =(s,1-u,0,d+u h)

alpha_2=(1,0,-1,0)
beta_2 =(0,1,-s,-d)

alpha_3=(0,0,1,-1)
beta_3 =(1,0,0,1).                                  (5)
```

Its binary permanent has the single nonzero coefficient

```text
T_1111=2 s u.                                       (6)
```

The kernel line at each mode is `K alpha_i`.  Every representative of
the nonzero pure marking is therefore, after harmless scaling,

```text
beta_i(t_i)=beta_i+t_i alpha_i.                     (7)
```

Hence the four affine parameters `t_0,...,t_3` cover every marked basis
on this function-field normal-form chart; there is no missing
projective infinity chart.

## Exact incidence ideals

Write the fifth-coordinate extensions as

```text
alpha_i -> (alpha_i,x_i),
beta_i(t_i) -> (beta_i(t_i),y_i).                   (8)
```

For each map in (4), expand the sixteen binary permanent
coefficients.  A nonzero `Delta_2` neighbor requires:

1. all fourteen mixed coefficients to vanish;
2. the `0000` diagonal to be nonzero; and
3. the `1111` diagonal to be nonzero.

All sixteen coefficients are linear in

```text
z=(x_0,x_1,x_2,x_3,y_0,y_1,y_2,y_3).               (9)
```

The `D_23` direction has an especially short obstruction.  Let `A`
be the coefficient row of the desired `0000` diagonal, and let
`M_b` be the coefficient row of the mixed word `b`.  Exact expansion
gives

```text
A=(0,0,0,2(u-v),0,0,0,0),
M_1000=(t_0-1)A,
(u-v)M_1110=-G A,                                  (10)
```

where

```text
G|_(t_0=1)=-s u.                                   (11)
```

If all mixed coefficients vanish while `A z!=0`, the `1000` equation
first forces `t_0=1`.  The `1110` equation then reads

```text
M_1110 z=(s u/(u-v)) A z!=0,
```

a contradiction on the equal-weight chart.  Thus this diagonal needs only
two mixed rows; its three-dimensional extension kernel can carry the
`1111` diagonal but never the `0000` diagonal.

For a uniform certificate covering both directions, scale `z` so the
first diagonal is one and saturate by the second diagonal using an
inverse variable `w`.  Eliminating `(z,w)` over `K` gives

```text
I_01 intersect K[t_0,t_1,t_2,t_3] = (1),
I_23 intersect K[t_0,t_1,t_2,t_3] = (1).            (12)
```

The two unit ideals prove that neither equal-weight diagonal admits
even a binary `Delta_2` extension on this chart.  In particular, no
choice of a third target row can repair this equal-weight obstruction.

## Consequence for `H22`

In the normalized `H22` pencil,

```text
Phi(v_2)=(lambda_2/c)E_2^4,
Phi(v_0)=lambda_0 E_0^4-(a lambda_2/c)E_2^4,
Phi(v_1)=lambda_1 E_1^4-(b lambda_2/c)E_2^4.        (13)
```

At least one of `a,b` is nonzero.  If `a!=0`, the target-color
`{0,2}` binary plane must give a `D_01` extension to `Delta_2`; if
`b!=0`, the `{1,2}` binary plane must give a `D_23` extension.
Equation (12) excludes either requirement in the equal-weight
normalization (2).

It does not exclude a general component-orbit point.  After restoring
the diagonal-source torus, the two contractions take the weighted forms

```text
D_01^rho(r)=(rho r_0+r_1,r_2,r_3,r_4),
D_23^sigma(r)=(r_0,r_1,sigma r_2+r_3,r_4).          (14)
```

Exact and modular reconnaissance finds survivor loci for (14).
Closing their ternary marked maps and simultaneous second-slice
compatibility is the honest next problem.

## Verification

Run

```text
python verify_p5_h22_six_dimensional_equal_weight_binary_obstruction.py
python audit_p5_h22_six_dimensional_equal_weight_binary_obstruction.py
```

The primary verifier reconstructs (5)--(6), performs both exact
function-field eliminations, and requires the two projected ideals to
be unit.  The independent audit uses a separate dynamic-programming
permanent and modular row reduction.  At independent parameter samples
over `F_5` and `F_7`, it tests all `p^4` marked bases at equal weight for both
diagonals and finds no extension kernel on which both diagonal
functionals are nonzero.  The finite-field calculation is
corroboration only; the theorem is the characteristic-zero identities
(10)--(11) and eliminations (12).
