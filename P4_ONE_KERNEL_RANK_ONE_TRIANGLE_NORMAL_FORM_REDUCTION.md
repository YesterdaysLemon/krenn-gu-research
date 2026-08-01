# One kernel--kernel rank-one triangle reduces to three support geometries

## Status

**Exact characteristic-zero orientation and support reduction.**  Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Let `U_i=span(y_i,x_i)` be marked planes on which `P_4` restricts to a
nonzero pure tensor, with every pair image of rank at least three.  Suppose
the selected triangle on modes `1,2,3` has pair rank three on every edge,
three unique coefficient-rank-one relations, and exactly one selected
kernel--kernel relation.

Up to interchanging modes `1,2`, there are exactly three orientations.  The
common-kernel orientation has a dense branch which is exactly the `r=-2`
slice of component twelve.  The other branches reduce to the explicit
finite list of normal forms below.

This is deliberately a **reduction theorem, not a component-exhaustion
theorem**.  In particular, the common-active support boundaries, the
common-kernel vertical fibre, and both mixed-chain fibres have no component
containment asserted here.  They are precise residual targets rather than
new components.  No parameter search or elimination is used.

## The three orientations

Relabel so that the unique selected kernel--kernel relation is

```text
y_1 y_2=0.                                          (1)
```

Each of the other two rank-one relations uses a kernel row at exactly one
endpoint.  Interchanging modes `1,2` leaves only

```text
I.    y_1x_3=0,  y_2x_3=0             common active,
II.   x_1y_3=0,  x_2y_3=0             common kernel,
III.  y_1x_3=0,  x_2y_3=0             mixed chain. (2)
```

This small orientation quotient is exhaustive.

We repeatedly use the following elementary fact.  If nonzero linear forms
`a,b in R_1` satisfy `ab=0`, then their common support has size at most two.
On support one they are proportional to one coordinate; on genuine support
two, after diagonal scaling, they are `A+B` and `A-B`.  In either case
`Ann_R1(a)` is one-dimensional.

## I. Common active: a singleton flag and two exact-pair boundaries

The one-dimensional annihilator gives

```text
y_1=y_2=x_3=e=X_0.
```

Remove the `e` coordinates from the two active rows and write

```text
V=span(X_1,X_2,X_3),
U_1=span(e,u),       U_2=span(e,v),
U_3=span(gamma*e+w,e),       u,v,w in V.            (3)
```

Put

```text
q_1=vw,       q_2=uw,       q_3=uv in R_2(V),
tau=uvw in R_3(V).
```

Among the eight triple products from modes `1,2,3`, the only possibly
nonzero forbidden cubics and the desired cubic are

```text
F_1=e q_1,
F_2=e q_2,
F_3=gamma*e q_3+tau,
X  =e q_3.                                           (4)
```

Thus purity is equivalent to `dim span(F_1,F_2,F_3)<=2` and
`X notin span(F_1,F_2,F_3)`.  Formula (4) gives the complete split.

### The `tau=0` sheet

Nonzero purity first forces `gamma=0` and

```text
q_3 notin span(q_1,q_2).                            (5)
```

If `q_1,q_2` are independent, their common annihilator is a two-plane
containing `e`.  All four planes then contain the same singleton after a
mode permutation, so this branch belongs to component eighteen.

If `q_1,q_2` are dependent, the selected pair-rank assumptions make both
nonzero.  Write `u-lambda*v=h`; then `hw=0`.  The exact pair `h,w` cannot
have singleton support: `tau=0` would put `u,v,w` in one binary source
plane, contradicting (5).  Hence, after scaling,

```text
A=X_1, B=X_2, C=X_3,
w=A+B,       h=A-B,
u=t*h+C,     v=s*h+C,       s!=t.                  (6)
```

Here `uw=vw=(A+B)C`, and the forbidden annihilator is the three-space

```text
H=Ann_R1(e(A+B)C)=span(e,A-B,C).                   (7)
```

The opposite plane is any `U_0 in Gr(2,H)` on which `euv` is nonzero.
The sublocus `e in U_0` is already in component eighteen; containment of
the complementary projective fibre is open.

### The `tau!=0` sheet

Now the `R_3(V)` part of `F_3` is independent of `F_1,F_2`, so purity forces
`q_1,q_2` to be proportional.  Consequently

```text
u=lambda*v+h,       hw=0,       lambda!=0,          (8)
```

and the opposite plane is the unique plane

```text
U_0=Ann_R1(span(evw, gamma*euv+uvw)),               (9)
```

subject to the open condition `uv notin C*(vw)`.  The exact pair `h,w`
has precisely two support types:

```text
singleton:  w=h=A,
            v=rho*A+B+C,       u=lambda*v+A;

binary:     w=A+B,             h=A-B,
            v=p*A+q*B+C,       u=lambda*v+h,
            lambda*(p+q)!=0.                         (10)
```

In the binary line of (10), the additional displayed open condition from
(9) is retained.  These singleton and genuine-binary sheets are residual;
no known-component containment is claimed.

## II. Common kernel: disjoint exact pairs

Here `x_1,x_2` both annihilate `y_3`, hence are proportional.  The pairs
`(y_1,y_2)` and `(x_1,y_3)` must both have genuine support two.  Equal
supports put a pair image in one binary quadratic line; adjacent supports
give the identity

```text
(A+B)(A+C)+(A-B)(A+C)=(A+C)^2,
```

and again lower the selected pair rank.  Therefore the supports are
disjoint.  Normalize

```text
A=X_0+X_1,       A_bar=X_0-X_1,
B=X_2+X_3,       B_bar=X_2-X_3,

U_1=span(B,A),
U_2=span(B_bar,A),
U_3=span(A_bar,w),
w=P*A+r*B+s*B_bar.                                 (11)
```

The only two forbidden cubics and the desired cubic have covectors

```text
C_1=(2r,2r,2P,2P),
C_2=(-2s,-2s,-2P,2P),
D  =(0,0,2(r-s),2(r+s)).                           (12)
```

The nonzero maximal minors of the stacked matrix `(C_1,C_2,D)` are

```text
-16 P(r-s)(r+s),       -16 P(r-s)(r+s).            (13)
```

On `P(r^2-s^2)!=0`, normalize `r=1`, put `phi=s/r`, and obtain the unique
opposite plane

```text
U_0=span(A_bar,-P*A+B+phi*B_bar),       phi!=+-1.  (14)
```

This dense sheet is already known.  Apply the source diagonal map

```text
diag(P^(-1),-P^(-1),(1+phi)^(-1),(1-phi)^(-1))
```

and reorder the modes as `(2,3,0,1)`.  Formulae (11),(14) become exactly
the family in `P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md` at its parameter
`r=-2`, with `k=(1+phi)/(1-phi)`.  Hence this sheet lies in component
twelve.

There is also a genuine vertical fibre, which determinant (13) alone must
not discard:

```text
P=0,       r*s!=0,
U_0 in Gr(2,span(A_bar,B,B_bar)),                  (15)
```

where `U_0` must detect `A^2(rB+sB_bar)` and satisfy the ambient all-pair
rank open conditions.  If `P!=0` and `r^2=s^2`, the desired covector belongs
to `span(C_1,C_2)` and the restriction is zero.  If `P=0` and `rs=0`, a
selected pair rank drops below three.  Containment of (15) is open.

## III. Mixed chain: two disjoint exact pairs

The first two relations force `y_2=x_3`.  Write the two exact pairs as
`ab=0` and `cd=0`; then

```text
U_1=span(a,w),       U_2=span(b,c),
U_3=span(d,b).                                      (16)
```

Singleton, equal-support, and adjacent-support choices give a second
relation on one selected edge.  Thus the rank-three hypothesis forces two
genuine disjoint supports.  Normalize

```text
U_1=span(A,w),
U_2=span(A_bar,B),
U_3=span(B_bar,A_bar),
w=P*A_bar+r*B+s*B_bar.                             (17)
```

The two forbidden cubics and the desired cubic have covectors

```text
E_1=(2s,-2s,2P,-2P),
E_2=(0,0,-2r+2s,-2r-2s),
D  =(-2r,2r,-2P,-2P).                             (18)
```

Again the nonzero maximal minors are, up to sign,

```text
16 P(r-s)(r+s).                                    (19)
```

On `P(r^2-s^2)!=0`, normalize `r=1`, set `phi=s/r`, and obtain

```text
z=-P*A_bar+phi*B_bar+phi^2*B,
U_0=span(A,z).                                     (20)
```

Direct row reduction gives the pair profile, in edge order
`01,02,03,12,13,23`,

```text
(4,3,3,3,3,3).                                    (21)
```

Its selected triangle has exactly the relations

```text
y_1y_2=0,       y_1x_3=0,       x_2y_3=0.
```

The determinant-zero locus has one additional all-pair-rank survivor:

```text
w=P*A_bar,       P!=0,
U_0 in Gr(2,span(A,A_bar,B)),                      (22)
```

where `U_0` kills `A_bar^2 B_bar`, detects `A_bar^2 B`, and remains in the
all-pair-rank open set.  The other determinant-zero cases are zero or have
a selected pair image of rank at most two.  Both (20) and (22) remain open
component-containment problems.

## Exact residual ledger

The exactly-one-kernel selected triangle is therefore reduced to the
following finite list:

```text
common active, tau=0, independent products      -> component 18,
common active, tau=0, dependent products        -> (6)--(7), open,
common active, tau!=0, singleton exact pair     -> (9)--(10), open,
common active, tau!=0, binary exact pair        -> (9)--(10), open,
common kernel, transverse branch                -> component 12,
common kernel, vertical branch                  -> (15), open,
mixed chain, transverse branch                  -> (20)--(21), open,
mixed chain, vertical branch                    -> (22), open.   (23)
```

Equations (4), (12), and (18) are transparent exact replay data for the
reduction.  A separate computer verifier was intentionally not added in
this bounded pass; the next useful task is component placement of one of
the explicitly listed residual fibres, not another broad elimination.
