# Exact chart closure of the known pure rank-two component

## Status

This is an exact algebraic-geometric description over `C`.

In the four-Grassmannian chart used in
[`P4_PURE_RANK_TWO_COMPONENT_THEOREM.md`](P4_PURE_RANK_TWO_COMPONENT_THEOREM.md),
the closure of the known five-dimensional component is cut out by
eleven elementary equations.  Every nonzero pure compression in this
chart is either:

1. in the original five-parameter family chart; or
2. on one explicit four-dimensional boundary divisor.

Consequently any further boundary of this component must lie on the
union of four named Schubert divisors where a selected Pluecker
coordinate vanishes.

This theorem describes one component chart.  It does not assert that
there are no other pure-compression components.

## The component equations

Use the plane rows

```text
R_0=((1,0,a,b),(0,1,c,d)),
R_1=((e,1,0,f),(g,0,1,h)),
R_2=((i,1,0,j),(k,0,1,l)),
R_3=((1,m,n,0),(0,o,p,1)).                           (1)
```

The selected nonzero Pluecker coordinates are, respectively,

```text
Delta_0(01), Delta_1(12), Delta_2(12), Delta_3(03). (2)
```

Inside this chart, the component closure is exactly

```text
f=g=i=l=m=o=0,
h p+1=0,
n k+1=0,
j-h n e=0,
h c-d-j=0,
b-h(a-n)=0.                                         (3)
```

Indeed, row reduction of the known family gives

```text
a=-Q(C+EIL)/E,       b=-CQ-EI(LQ+1),
c=C/E+IL,            d=C,
e=L,                 h=E,
j=EIL,               k=-1/I,
n=I,                 p=-1/E,                        (4)
```

with the other six coordinates zero.  These expressions satisfy (3).

Conversely, (3) makes `a,d,e,h,n` free, with `h n!=0`, and determines
all other coordinates:

```text
b=h(a-n),       c=(d+hne)/h,       j=hne,
k=-1/n,         p=-1/h,                                (5)
```

plus the six zeros.  Thus the variety in (3) is irreducible of
dimension five.  The family image with

```text
D=d+h n e !=0                                    (6)
```

has the inverse

```text
E=h, I=n, L=e, C=d, Q=-a h/D.                         (7)
```

It is a dense open subset of (3), proving that (3) is exactly the chart
closure.

## The restricted tensor and its boundary

Substitute (3) into the sixteen permanent coefficients.  Only four can
be nonzero:

```text
T_0000=2 a e h n,       T_0100=2 a h,
T_1000=2 e n D,         T_1100=2 D.                  (8)
```

Equivalently, the restricted tensor factors as

```text
2 (a h x_0+D y_0)(e n x_1+y_1)x_2x_3.               (9)
```

Since `h,n!=0`, it is nonzero exactly when

```text
(a,D)!=(0,0).                                        (10)
```

The original admissible family chart is `D!=0`.  Its nonzero complement
inside the component chart is therefore the single divisor

```text
D=0,   a!=0.                                         (11)
```

This is a genuine all-rank-two pure-compression boundary; it is not
covered by finite values of the original parameter `Q`.

Finally, every component point not covered by the affine chart (1)
lies in

```text
Delta_0(01) Delta_1(12) Delta_2(12) Delta_3(03)=0.   (12)
```

Thus (11) and the Schubert boundary (12) are the complete boundary
targets supplied by this component description.

## Verification

Run:

```text
python claims/p4/classifications/pair-geometry/pure-rank-two/verify_p4_pure_rank_two_component_chart_closure.py
python claims/p4/classifications/pair-geometry/pure-rank-two/audit_p4_pure_rank_two_component_chart_closure.py
```

The primary verifier derives (3)--(9) symbolically and checks the
birational inverse.  The independent audit evaluates every point of
the five-free-variable model over `F_5` and `F_7` using a separate
dynamic-programming permanent; it confirms the tensor factorization,
the zero locus, and the family/boundary split.  The finite-field check
is independent QA; the displayed identities prove the theorem over
`C`.
