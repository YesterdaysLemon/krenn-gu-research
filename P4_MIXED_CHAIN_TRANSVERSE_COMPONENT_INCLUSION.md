# The transverse mixed chain is a boundary of component eight

## Status

**Exact characteristic-zero component-containment theorem.**  The
`(4,3,3,3,3,3)` mixed-chain residual in equations (20)--(21) of
`P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md` lies in the
closure of the eighth pure-`P_4` component, the disjoint mixed-star
component of `P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`.

This removes the transverse mixed-chain entry from the residual ledger.  It
does not classify the vertical mixed-chain fibre, prove component
exhaustiveness, or prove the global Krenn--Gu conjecture.

There is one small open-condition correction to the earlier ledger.  Its
displayed profile (21) is valid when `phi!=0`.  At `phi=0` the full edge
`01` acquires a rank-one relation and the profile is
`(3,3,3,3,3,3)`.  That specialization is nevertheless in the same component
closure by closedness.

## The residual and its complete relation word

Work in the squarefree Frobenius algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2)
```

and put

```text
A=X_0+X_1,       C=X_0-X_1,
B=X_2+X_3,       D=X_2-X_3.                       (1)
```

For parameters satisfying

```text
P*phi*(phi-1)*(phi+1) != 0,                        (2)
```

the transverse mixed-chain normal form is

```text
w= P*C+B+phi*D,
z=-P*C+phi*D+phi^2*B,

U_0=span(A,z),       U_1=span(A,w),
U_2=span(C,B),       U_3=span(D,C).                (3)
```

Use the displayed row order `(y_i,x_i)`.  The restriction has the exact
identity

```text
P_4|_(U_0 x U_1 x U_2 x U_3)
   =-4 P (phi-1)(phi+1) x_0x_1x_2x_3.             (4)
```

The five exceptional edges have the complete relation word

```text
02: y_0y_2=0,       03: y_0x_3=0,
12: y_1y_2=0,       13: y_1x_3=0,
23: x_2y_3=0.                                      (5)
```

Every relation in (5) has coefficient rank one.  Edge `01` has rank four:
one exact maximal minor of its pair-product matrix is

```text
8 P phi (phi-1)^2(phi+1)^2.                        (6)
```

The other five pair matrices have rank three.  For example, exact nonzero
three-minors can be chosen as

```text
-4P^2,       4P^2,       -4,       4P,       4     (7)
```

in the edge order in (5).  Thus (2) gives precisely the profile
`(4,3,3,3,3,3)`.  If `phi=0`, then `z=-P*C` and the additional relation is
`x_0y_1=0`, explaining the corrected boundary profile.

## The disjoint mixed-star family

Recall the normalized family defining component eight.  Use parameters
`a,b,f,psi` and set

```text
j=f+b*psi^2,       kappa=psi*(b*f+1),
eta=-(b*f+1),

V_0=span(D, a*A+b*C+B-D),
V_1=span(C-a*f*A+f*B+psi*D, A),
V_2=span(-a*j*A+eta*C+j*B+kappa*D, A),
V_3=span(C,B).                                      (8)
```

Its only two potentially nonzero marked coefficients are

```text
T_1001=-4*Phi,       T_1111=4,

Phi=a^2*b*f*psi^2+a^2*f^2
    -b^2*f^2+b^2*psi^2-b*f-1.                     (9)
```

Consequently `Phi=0` is a dense pure family whose closure is component
eight.

## An exact valuative arc

Let `K=C(P,phi)` under condition (2), and let `t` be a uniformizer.  In a
finite algebraic extension of `K[[t]]`, choose the unit `q=q(t)` satisfying

```text
q^2 =
 [P*(1-phi^2)+P^2*t^2+P^3*t^4]/[phi^2+P*t^2].     (10)
```

The right side is a unit: its value at `t=0` is
`P*(1-phi^2)/phi^2`.  Such a formal square root therefore exists over the
algebraic closure of `K`.  Substitute in (8)--(9)

```text
b=t^(-2),       f=P^(-1),       psi=phi/P,
a=t^(-1)*q(t).                                    (11)
```

Then direct simplification gives

```text
Phi = ((phi^2+P*t^2)q^2
       -P*(1-phi^2)-P^2*t^2-P^3*t^4)/(P^3*t^4)
    =0.                                            (12)
```

Thus every nonzero point of the arc is in the pure family of component
eight.  The four Grassmann limits require no elimination.  In (8), perform
only invertible row operations for `t!=0` and rescale the indicated second
generators:

```text
t^2(a*A+b*C+B-D)
    =t*q*A+C+t^2(B-D)                       -> C,

(C-a*f*A+f*B+psi*D)+a*f*A
    =P^(-1)w,

P^2*t^2(eta*C+j*B+kappa*D)
    =(-P-P^2*t^2)C+(phi^2+P*t^2)B
      +(phi+P*phi*t^2)D                    -> z,

V_3=span(C,B).                                      (13)
```

It follows that

```text
(V_2,V_1,V_3,V_0) -> (U_0,U_1,U_2,U_3).           (14)
```

The permutation `(2,1,3,0)` of the component-eight modes is an allowed mode
symmetry.

The marked pure factors also have the correct limit.  The kernel rows of
`V_1,V_2` in (8) satisfy, with `q_0=q(0)!=0`,

```text
t*(C-a*f*A+f*B+psi*D)              -> -(q_0/P)A,
t^3*(-a*j*A+eta*C+j*B+kappa*D)     ->
                                      -(q_0*phi^2/P^2)A.       (15)
```

Together with the fixed kernel rows `C,D`, the order (14) therefore limits
to `(A,A,C,D)`, exactly the kernel marking of (3).  Equation (4) shows that
the special restriction is nonzero.

Equations (10)--(15) give a valuative point of the component-eight closure
whose special point is the generic transverse mixed-chain normal form.
Since the target parameter space in `(P,phi)` is irreducible and the
component closure is closed, the whole family (3) is contained in component
eight.  In particular the `phi=0` lower-profile specialization is included
as the closure of the `phi!=0` points, although it is not part of the
`433333` cell.

## Replay

```text
uv run --with sympy python verify_p4_mixed_chain_transverse_component_inclusion.py
uv run --with sympy python audit_p4_mixed_chain_transverse_component_inclusion.py
```

The primary verifier reconstructs the target restriction and all six pair
matrices, rechecks the component-eight pure identity, and verifies the
symbolic valuative substitution and four plane limits.  The independent
audit uses a separate permanent implementation and an exact rational sample
of the generic target to recheck the relation word, the algebraic arc
equation, its Pluecker limits, and the marked-kernel limits.
