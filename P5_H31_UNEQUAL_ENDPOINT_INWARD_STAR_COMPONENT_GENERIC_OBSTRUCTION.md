# Component twenty-five has no generic marked `H31` lift

## Status

**Exact characteristic-zero generic-component theorem.**  The complete
marked-basis fibre over the generic point of component twenty-five is empty
for `H31`.

This theorem does not close the proper parameter divisors or projective
boundary of the component, its weighted `H22` fibre, the remaining pure
`P_4` cells, or the arbitrary-order local-to-global reduction.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## The hypersurface function field

Use the normal form from
[`P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPONENT.md`](P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPONENT.md):

```text
A=X_0+X_1,  C=X_0-X_1,  B=X_2+X_3,  D=X_2-X_3,

U_0=<A,B>,
U_1=<A+kD,B+sC>,
U_2=<C,A+eB-kD>,
U_3=<D,A-sjC+jB>.                                  (1)
```

Put

```text
P=ej+k^2,       Q=e+j,
F=P(1+ejs^2)-Q^2.                                   (2)
```

The component function field is

```text
K=C(e,j,s)[k]/(F).                                  (3)
```

On the dense chart `P != 0`, choose

```text
alpha_0=Q A-P B,                 beta_0=A,
alpha_1=Q(A+kD)-P(B+sC),         beta_1=A+kD,
alpha_2=C,                       beta_2=A+eB-kD,
alpha_3=D,                       beta_3=A-sjC+jB.     (4)
```

The changes of basis in modes zero and one have determinant `P`.  Before
passing to the quotient by `F`, the only nonzero pure coefficients in (4)
are

```text
T_0011=4PF,        T_1111=4P.                       (5)
```

Thus (4) is an intrinsic pure basis over `K`, with `T_1111 != 0` at the
generic point.  Every marked basis on this chart is, up to irrelevant row
scalings,

```text
alpha_i,        beta_i(h)=beta_i+h_i alpha_i         (6)
```

for arbitrary `h_0,h_1,h_2,h_3`.

## Exact quotient-ring obstruction

For each deleted source coordinate `q=0,1,2,3`, let the eight extension
entries be `z`.  Let

```text
M_q(h) z
```

be the fourteen mixed binary coefficients after replacing coordinate `q`
by the fifth source coordinate, and let `A_q(z),B_q(z)` be the all-`alpha`
and all-`beta(h)` coefficients.  A neighbouring pure binary slice requires

```text
M_q(h)z=0,        A_q(z)B_q(z) != 0.                (7)
```

Compute the row module exactly over

```text
S=K[h_0,h_1,h_2,h_3].                              (8)
```

Quotient-ring standard-basis reduction gives

```text
q        0    1    2    3
size    10   10   12   12

NF_Mq(A_q)=0,       NF_Mq(B_q) != 0                 (9)
```

in every column.  In particular, `A_q` belongs to the row module of `M_q`.
Consequently every `z` satisfying `M_q(h)z=0` also satisfies `A_q(z)=0`, in
direct contradiction with (7).  This applies to every marking on the
generic chart and every possible deleted coordinate.  Hence the complete
generic marked `H31` fibre of component twenty-five is empty.

The calculation is performed in the quotient ring (3), rather than in the
ambient rational function field `C(e,j,k,s)`.  Therefore the reduction does
not invert `F` or silently discard the component.  The coefficient field in
(3) treats `1+ejs^2` as a generic unit, and (4) uses `P != 0`; the proper
divisors

```text
P=0        and        1+ejs^2=0                    (10)
```

remain special-fibre boundaries and are not claimed here.  No finite-field
calculation is used as proof.

## Verification

Run:

```text
uv run --with sympy python \
  verify_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction.py

uv run --with sympy python \
  audit_p5_h31_unequal_endpoint_inward_star_component_generic_obstruction.py
```

The primary verifier reconstructs (1)--(6) and performs all four exact
quotient-ring row-module reductions in Singular.  The audit imports neither
the family constructor nor the permanent/mixed-matrix helper: it rebuilds
the squarefree coefficients by subset dynamic programming and repeats all
four reductions independently.
