# Component twenty-two: the generic finite-`D23` `H=f2=f8=0` cell is empty

## Status

**Exact characteristic-zero generic-component branch closure.**  Work over

```text
K=Q(A,R,D),                 s=2*A+R,
```

on component twenty-two's finite-`D23` divisor

```text
H=2*A*h1+1=0,
f2=s*h2+1=0,
f8=(A*D+A+R*D)*rho+A*D-A+R*D=0.                 (1)
```

Then, after every field extension `E/K`, the fourteen-by-eight mixed binary
coefficient matrix has rank eight for every `h0,h3` in `E`.  Consequently the
whole geometric generic intersection (1) is empty for weighted `H22`.  This
includes both the earlier slope intersection

```text
2*h3+s=0
```

and its requested isolated complement `2*h3+s!=0`.

This is a function-field theorem.  It does not close specializations of
`A,R,D`, projective or source-chart boundaries, the rest of the `f2=0`
residual, any other P4 component, the complete `P_5 -> Delta_3` problem, or
the global Krenn--Gu conjecture.  The generic finite-`D01` pair orbit is
separately closed by its owning theorem; it is not reproved here, and its
special/projective component fibres remain open.  The global conjecture
remains **UNRESOLVED**.

## Exact rank obligation

Let `M` be the fourteen-by-eight matrix whose rows are the mixed binary-word
coefficients and whose columns are the eight fifth-coordinate extension
variables.  A weighted binary lift supplies a nonzero extension vector in
`ker M`; hence it is necessary that

```text
rank(M) <= 7.                                             (2)
```

On (1), solve

```text
h1=-1/(2*A),
h2=-1/s,
rho=-(A*D-A+D*R)/(A*D+A+D*R).                            (3)
```

The last expression and its translate by one are nonzero in `K`:

```text
rho+1=2*A/(A*D+A+D*R).
```

Thus the requested condition `rho*(rho+1)!=0` holds at the generic point.

## First cofactor: `h0` is forced

Use all eight columns and rows

```text
(0,1,2,3,4,7,8,11).                                     (4)
```

The determinant is `u11*Q11`, where

```text
Q11 = 4*A^2*D*h0-3*A^2*D+A^2
    + 4*A*D*R*h0-3*A*D*R+A*R
    + D*R^2*h0-D*R^2,                                   (5)

u11 = 512*A^4*D^4*R^2*(A+R)^3*s^4*(4*A+R)
      *(D-1)^2*(D+1)^3*(A*D-A+D*R)
      /(A*D+A+D*R)^7.                                   (6)
```

Every displayed nonzero polynomial is a unit in the coefficient field `K`.
Condition (2) therefore forces `Q11=0`, or

```text
h0 = [D*(3*A^2+3*A*R+R^2)-A*(A+R)]/(D*s^2).             (7)
```

## Two incompatible `h3` cofactors

Substitute (7) and define

```text
C = 8*A^3+16*A^2*R+11*A*R^2+2*R^3,                     (8)

B9 = 32*A^5-4*A^4*D^2*R+100*A^4*R
     -8*A^3*D^2*R^2+116*A^3*R^2
     -6*A^2*D^2*R^3+66*A^2*R^3
     -2*A*D^2*R^4+19*A*R^4+2*R^5,

B13 = 16*A^4+2*A^3*D^2*R+38*A^3*R+34*A^2*R^2
      -2*A*D^2*R^3+15*A*R^3+2*R^4,

L9  = 2*s*C*h3+B9,
L13 = 2*C*h3+B13.                                      (9)
```

The maximal minors on rows

```text
(0,1,2,3,4,7,8,9),
(0,1,2,3,4,7,8,13)                                    (10)
```

are respectively `u9*L9` and `u13*L13`, with

```text
u9 = -512*A^5*D^4*R*(A+R)^2*s^3*(D-1)*(D+1)^3
     *(A*D-A+D*R)/(A*D+A+D*R)^7,

u13 = 256*A^4*D^4*R*(A+R)^2*s^4*(D-1)*(D+1)^3
      *(A*D-A+D*R)/(A*D+A+D*R)^7.                     (11)
```

Again these are units in `K`.  But the two forced linear equations are
incompatible, because

```text
B9-s*B13
  = -2*A^2*R*(A+R)*(4*A+R)*(D-1)*(D+1) != 0 in K.      (12)
```

Indeed, `L9-s*L13` equals the left side of (12).  Thus `L9=L13=0`
is impossible.  Equivalently,

```text
Res_h3(L9,L13)
  = 4*A^2*R*(A+R)*(4*A+R)*(D-1)*(D+1)*C != 0.          (13)
```

At least one maximal minor of `M` is therefore nonzero for every `h0,h3`,
contradicting (2).  Every coefficient used above lies in `K`, and the nonzero
elements in (6), (11), and (13) remain nonzero after every field extension
`E/K`.  The same forced-`h0` and incompatible-`h3` argument therefore holds
over every such `E`, proving the geometric generic intersection empty rather
than merely showing that it has no `K`-rational point.

## Replay and independence

Run:

```powershell
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-f2-f8-generic-complete/verify_p5_h22_unequal_complement_common_kernel_component_d23_f2_f8_generic_complete_obstruction.py
uv run --with sympy python claims/p5/h22/unequal-complement-common-kernel-component-d23-f2-f8-generic-complete/audit_p5_h22_unequal_complement_common_kernel_component_d23_f2_f8_generic_complete_obstruction.py
```

The primary verifier binds to the repository's exact component-twenty-two
finite-`D23` model and uses fraction-field `DomainMatrix` determinants.  The
audit imports no repository code: it independently reconstructs the component
rows, weighted projection, permanent coefficients, and mixed matrix, then
uses explicit Gaussian elimination.  Both verify (5)--(13) exactly.  No
finite-field, modular, numerical, or sampled inference enters the theorem.

## Exact boundary

```text
component 22, finite D23, K=Q(A,R,D), H=f2=f8=0:  EMPTY;
the 2*h3+s=0 subintersection:                       EMPTY (included);
the 2*h3+s!=0 isolated complement:                  EMPTY (included);
special component-parameter fibres:                 UNKNOWN;
remaining f2=0 residual outside f8=0:               UNKNOWN;
generic finite D01 pair orbit:                      CLOSED SEPARATELY;
special/projective/source boundaries:               UNKNOWN;
complete P5 -> Delta3 restriction:                  UNRESOLVED;
global Krenn--Gu conjecture:                        UNRESOLVED.
```
