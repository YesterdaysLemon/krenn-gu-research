# Generic weighted `H22` obstruction on the first rank-two component

## Status

This is an exact characteristic-zero obstruction on the generic
diagonal-source orbit of the first all-rank-two pure-compression
component proved in
[`P4_PURE_RANK_TWO_COMPONENT_THEOREM.md`](claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_THEOREM.md).

The weighted `01` mixed-coefficient matrix has full column rank for
every marked basis.  The weighted `23` binary projection has two
rational sheets; fixed mode-two marked minors exclude every genuine
extension on both sheets from a ternary local map.

Thus the generic weighted `H22` incidence is empty on this component.

This does **not** close its parameter/slope divisors or projective
boundary, the second diagonal-quadric component, component
exhaustiveness, all of `H22`, or the global prize problem.

## Canonical family and weighted pencils

Put

```text
D=C+L,        A=1+LQ
```

and work over

```text
K=C(L,Q,C,r).
```

Use the canonical marked basis

```text
alpha_0=( 1,Q, 0,-A)      beta_0=(0,1,D,C)
alpha_1=( L,1,-L,-L)      beta_1=(0,0,1,1)
alpha_2=(-1,0, 1, 0)      beta_2=(0,1,0,L)
alpha_3=( 0,0,-1, 1)      beta_3=(1,0,1,0).        (1)
```

Its only nonzero pure coefficient is

```text
T_1111=2(C+L).                                     (2)
```

Every marked representative over the same plane tuple is

```text
beta_i(t_i)=beta_i+t_i alpha_i.                    (3)
```

The residual diagonal-source slope gives the two neighboring bases

```text
D_01^r(u)=(r u_0+u_1,u_2,u_3,u_4),
D_23^r(u)=(u_0,u_1,r u_2+u_3,u_4).                 (4)
```

Write the fifth-coordinate extensions as

```text
z=(x_0,x_1,x_2,x_3,y_0,y_1,y_2,y_3).
```

## The `01` projective-kernel obstruction

Let `M_01(t)` be the `14 x 8` matrix of mixed binary coefficients.
The exact statement is

```text
ker M_01(t)=0 for every t in Kbar^4.                (5)
```

As in the mixed-orientation component, a hierarchical affine cover of
the projective extension kernel proves (5):

1. the charts `x_2=1` and `x_3=1` are unit;
2. after `x_2=x_3=0`, the charts `y_2=1,y_3=1` are unit;
3. after `x_2=x_3=y_2=y_3=0`, the four residual charts
   `x_0=1,x_1=1,y_0=1,y_1=1` are unit.

These eight exact ideals cover `P^7`.  Hence the weighted `01` pencil
has no nonzero binary extension for any marking.  This is a
projective determinantal certificate, not an enumeration.

## The exact `23` projection

Normalize the `0000` diagonal, invert the `1111` diagonal, and
eliminate `(z,w)`.  Define

```text
Z=Q(L+C)(r+1),
H=Z-r+1,

U=LQZ+2LQ+QC(r+1)-r+1,

P=C[LQ(r+1)(Z-r+2)+QC(r+1)-r+1],
R=L^2(r-1)(Z+1),
E=LC(r-1-Z).                                       (6)
```

The projected marking ideal is

```text
P t_2+R t_3+E,
t_1,
Q U t_0+(r-1)t_3+U,
t_3((r-1)t_3+H).                                  (7)
```

Thus every genuine marking lies on one of two rational sheets:

```text
A: t_3=0,
B: (r-1)t_3+H=0,                                  (8)
```

with `t_1=0` and `t_2,t_0` determined by the two linear equations in
(7) on the generic open set.

## Two one-minor Fitting obstructions

Let `N_2(z)` be the mode-two one-marked `8 x 4` contraction matrix.
On sheet `A`, adjoin

```text
det (N_2)_{0147}
```

to the fourteen mixed equations and invert the product of the two
binary diagonals.  The resulting ideal over `K` is `(1)`.

On sheet `B`, the corresponding certificate is

```text
det (N_2)_{0137},
```

and its saturated ideal is again `(1)`.  Hence every genuine binary
extension on either sheet has marked rank four and cannot factor
through three target coordinates.

Combining (5), (7), and the two unit ideals proves the generic weighted
`H22` obstruction on the first rank-two component.

## Honest frontier

Generic weighted `H22` incidence is now empty on six of the seven
certified pure-`P_4` component orbits.  The remaining generic target is
the diagonal-quadric component.  Parameter/slope divisors and
projective boundaries of the six closed families remain, the seven
components are not known to be exhaustive, and the global prize
problem remains unresolved.

## Verification

Run

```text
python \
  verify_p5_h22_first_rank_two_component_generic_obstruction.py

python audit_p5_h22_first_rank_two_component_generic_obstruction.py
```

The primary verifier reconstructs (1)--(2), proves all eight exact
projective-chart unit ideals behind (5), verifies the exact projection
(7), and proves the two characteristic-zero saturated one-minor unit
ideals.

The independent audit imports no primary verifier.  Over `F_5,F_7` it
exhausts every affine marking in the `01` pencil at generic component
samples and finds rank eight throughout.  It then reconstructs the two
exact `23` sheets directly and checks rank seven, both nonzero binary
diagonals, marked rank four, and the selected nonzero minor.  These
finite-field calculations are corroboration only; the theorem is the
function-field computation above.
