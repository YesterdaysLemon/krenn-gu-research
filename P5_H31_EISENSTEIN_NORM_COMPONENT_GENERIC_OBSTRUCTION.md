# The Eisenstein-norm component has no generic marked `H31` lift

## Status

**Exact characteristic-zero generic-component theorem.**  The complete
marked-basis fibre over the generic point of the thirteenth pure-`P_4`
component is empty for `H31`.

Consequently all thirteen currently certified pure-`P_4` component orbits
are generically closed for `H31`.  The new component's weighted `H22` fibre,
special parameter/projective boundaries, component exhaustiveness, and the
global Krenn--Gu conjecture remain open.

## Intrinsic rows on the norm quadric

Use the normal form from
[`P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md`](P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md):

```text
a=X_0+X_1,       c=X_0-X_1,
b=X_2+X_3,       b_bar=X_2-X_3,

m=alpha*a+beta*c+b,       m_r=m+r*c,
d=gamma*a+b,
x_0=b-(alpha+gamma)*a-(2*beta+r)*c.                (1)
```

On

```text
F=alpha^2+alpha*gamma+gamma^2
  -3*beta^2-3*beta*r-r^2=0,                        (2)
```

an intrinsic kernel/active marking is

```text
alpha_rows=(b_bar,m,m_r,c),
beta_rows =(x_0,a,a,d).                             (3)
```

Every marking in the affine fibre is

```text
alpha_i,
beta_i(h)=beta_i+h_i*alpha_i,
h=(h_0,h_1,h_2,h_3),                               (4)
```

and the only nonzero coefficient remains `T_1111=4`.

## A rational function field for the Eisenstein quadric

The projective quadric (2) is rational.  On the dense chart `beta=1`, project
from the rational point `(alpha,beta,r,gamma)=(2,1,1,1)`.  If the line
direction is `(u,v,1)` in `(alpha,gamma,r)`, put

```text
D=u^2+u*v+v^2-1,
lambda=(5-5u-4v)/D,
alpha=2+u*lambda,
beta=1,
r=1+lambda,
gamma=1+v*lambda.                                  (5)
```

Substitution makes `F` identically zero.  Since (5) is a dominant rational
parameterization, the component function field is `K=C(u,v)` on this chart.
The full marking ring is

```text
S=K[h_0,h_1,h_2,h_3].                              (6)
```

This avoids adjoining a square root or a primitive cube root: the
Eisenstein norm geometry supplies a purely rational chart for the module
calculation.

## The four binary extension modules

For each deleted source coordinate `j`, adjoin a fifth-coordinate entry to
each kernel and active row.  Let

```text
M_j in Mat_(14 x 8)(S)                             (7)
```

be the fourteen mixed binary coefficients, and let `A_j,B_j` be the
all-kernel and all-active diagonal rows.  A binary neighbour would require

```text
M_j z=0,             A_j(z)B_j(z)!=0.              (8)
```

Exact polynomial row-module reduction over (6) gives, simultaneously in all
four marking variables,

```text
A_j in Row_S(M_j),       B_j notin Row_S(M_j)
for j=0,1,2,3.                                         (9)
```

Every reduced module has ten generators.  Thus any solution of the fourteen
mixed equations satisfies `A_j(z)=0`, contradicting (8) before any ternary
rank condition is considered.

At the rational chart point `(u,v)=(2,0)`, with canonical marking, the mixed
ranks are

```text
(7,7,7,7).                                         (10)
```

Adjoining `A_j` leaves them unchanged, while adjoining `B_j` raises every
rank to eight.  The obstruction therefore kills one Segre vertex while
retaining the opposite active cokernel class; it is not total collapse of
the extension map.

Presentation modules and their Fitting supports are treated abstractly in
the [Stacks Project, Section 15.8](https://stacks.math.columbia.edu/tag/07Z6).
Here direct row-module membership is stronger than a generic minor: (9)
holds across the entire affine marking chart over the component function
field.

## Proof boundary

This is a generic-component theorem.  Denominators in the rational chart and
in the module reductions can vanish on special component divisors; those
special fibres are not closed here.  The weighted `H22` fibre is also not a
consequence of (9), because it is a different projection incidence.

## Verification

Run:

```text
uv run --with sympy python verify_p5_h31_eisenstein_norm_component_generic_obstruction.py
uv run --with sympy python audit_p5_h31_eisenstein_norm_component_generic_obstruction.py
```

The primary verifier proves (2)--(10) over `C(u,v)[h_0,h_1,h_2,h_3]`.  The
audit imports neither its marked-row constructor nor its extension matrix;
it rebuilds squarefree permanents by subset dynamic programming and checks
all four complete marking modules at two independent rational points of the
norm quadric.  These specializations corroborate the function-field proof;
they are not used as a replacement for it.
