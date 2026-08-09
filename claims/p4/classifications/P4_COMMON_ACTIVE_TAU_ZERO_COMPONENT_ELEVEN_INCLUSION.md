# The dependent common-active `tau=0` sheet is a component-eleven boundary

## Status

**Exact characteristic-zero closure theorem.**  In the exactly-one-kernel
rank-one triangle reduction, the common-active branch with `tau=0` and
dependent products, equations (6)--(7) of
[`P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md`](P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md),
lies in the closure of component eleven.

The proof is an explicit Laurent arc in the already certified
equal-support common-factor family.  It uses no parameter census or
elimination.  This closes one of the six residual families in that note; the
other five residual families and the global Krenn--Gu conjecture remain open.

## The residual family

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2)
```

and set

```text
e=X_0,       h=X_1-X_2,       w=X_1+X_2,       C=X_3.       (1)
```

Every opposite plane in the complementary projective fibre of equations
(6)--(7) has a unique graph presentation

```text
U_0=span(h+alpha*e, C+beta*e).                           (2)
```

The four planes are therefore

```text
U_0=span(h+alpha*e, C+beta*e),
U_1=span(e,t*h+C),
U_2=span(e,s*h+C),
U_3=span(w,e),              s!=t.                       (3)
```

Indeed, a two-plane in `span(e,h,C)` which does not contain `e` projects
isomorphically to `span(h,C)`, giving (2).  In the displayed row order the
only nonzero coefficients of the restricted permanent are

```text
T_0111=-2(s+t),       T_1111=-2st.                      (4)
```

Thus (3) is pure and nonzero throughout the residual open set.  At a general
point its pair profile is

```text
(4,4,4,3,3,3),                                       (5)
```

and the last three pair relations are precisely the three rank-one relations
of the common-active orientation.

## A symmetry-translated component-eleven chart

Use the following exact pairs instead of the coordinate ordering used in the
original component-eleven theorem:

```text
a=e+C,       a_bar=e-C,
b=h,         b_bar=w.                                  (6)
```

This is obtained from the standard two-block chart by a source permutation
and one coordinate sign.  Hence the planes

```text
V_0=span(a+p*b, a_bar+q*b),
V_1=span(a,a_bar+b),
V_2=span(a,r*a_bar+b),
V_3=span(b_bar,a_bar)                                  (7)
```

belong to component eleven whenever their pure coefficient is nonzero.

On the dense parameter open set

```text
alpha*s*t!=0,                                         (8)
```

introduce a parameter `epsilon` and set

```text
p_epsilon=-1/(2*t*alpha*epsilon),
q_epsilon=p_epsilon-beta/(t*alpha),
r=t/s,
D_epsilon=diag(1,-2*t*epsilon,-2*t*epsilon,epsilon).  (9)
```

Let `V_i(epsilon)` be (7), with the parameters from (9), followed by the
source diagonal map `D_epsilon`.  For every nonzero `epsilon`, this is a
point of the component-eleven family.  The apparent poles in (9) disappear
in Grassmann Pluecker coordinates.

## Exact Pluecker limits

Order Pluecker coordinates as

```text
(01,02,03,12,13,23).                                  (10)
```

After division by harmless nonzero projective scalars, direct exterior
multiplication gives

```text
Pl(V_0(epsilon))/(-2epsilon/alpha)
  =(-beta,beta,alpha,0,1+epsilon*beta,-1-epsilon*beta),

Pl(V_1(epsilon))/(-2epsilon)
  =(t,-t,1,0,-epsilon*t,epsilon*t),

Pl(V_2(epsilon))/(-2epsilon*t/s)
  =(s,-s,1,0,-epsilon*s,epsilon*s),

Pl(V_3(epsilon))/(-2epsilon*t)
  =(-1,-1,0,0,-epsilon,-epsilon).                    (11)
```

At `epsilon=0`, these are exactly the Pluecker vectors of the four planes in
(3).  Therefore every point satisfying (8) is in the projective closure of
component eleven.

The parameter space `(alpha,beta,s,t)` is irreducible.  Conditions `s!=t`,
nonvanishing of the pure coefficient, and the all-pair-rank conditions only
remove proper closed subsets.  The subopen (8) is dense, and component eleven
is closed.  Consequently the same containment holds for the entire residual
sheet (3), including `alpha*s*t=0` points which remain in its prescribed
nonzero all-pair-rank open set.

## Consequence for the residual ledger

The common-active part of the ledger is now

```text
tau=0, independent products   -> component 18,
tau=0, dependent products     -> component 11,
tau!=0, singleton exact pair  -> open,
tau!=0, binary exact pair     -> open.               (12)
```

Together with the already known transverse common-kernel sheet, this reduces
the exactly-one-kernel triangle from six open residual families to five.  It
does not settle the other all-pair star/triangle cells, special `P_5` fibres,
or the local-to-global graph step.

## Replay

Run:

```text
uv run --with sympy python verify_p4_common_active_tau_zero_component_eleven_inclusion.py
uv run --with sympy python audit_p4_common_active_tau_zero_component_eleven_inclusion.py
```

The primary verifier proves (4)--(5) and all four symbolic identities in
(11).  The independent audit uses subset-dictionary multiplication and a
separate exterior-coordinate implementation.  Both are fixed exact checks,
not searches.
