# Complete classification of the two-double-endpoint star `(1,1,1)`

## Status

**Exact characteristic-zero orientation and projective-support
classification.**  Let a nonzero pure `P_4` compression have all six
pair-image ranks at least three.  Suppose a selected rank-one exceptional
star is centered at mode zero and exactly two spokes are kernel--kernel:

```text
y_0 y_1=0,       y_0 y_2=0.                       (1)
```

The third spoke uses exactly one pure-kernel endpoint.  Up to exchanging
leaves one and two, source-coordinate permutation, diagonal source scaling,
and projective row gauges, every such tuple lies in component 8, 16, 18, or
21.  No new component is created.

This theorem includes singleton supports, equal/overlapping/disjoint binary
supports, affine charts, and their projective leaf endpoints.  It does not
classify the one-double-endpoint orientation or settle special `P_5` fibres.
The Krenn--Gu conjecture remains **UNRESOLVED**.

## The common annihilator forced by the two double spokes

The degree-one annihilator of a nonzero degree-one zero divisor in the
squarefree Frobenius algebra is one-dimensional.  Hence (1) makes `y_1` and
`y_2` proportional.  There are only two support types.

On singleton support, normalize

```text
y_0=y_1=y_2=e=X_0.                                (2)
```

On genuine binary support, put

```text
A=X_0+X_1,       C=X_0-X_1,
B=X_2+X_3,       D=X_2-X_3,
y_0=A,           y_1=y_2=C.                       (3)
```

The third spoke is, after a legal active-row shift, exactly one of

```text
I.   y_0 x_3=0,              center-kernel spoke;
II.  x_0 y_3=0,              reverse leaf-kernel spoke.   (4)
```

## I. The center-kernel spoke

### Singleton support gives component 18

Equation `y_0x_3=0` and (2) give `x_3=e`.  Remove the `e` coordinates from
`x_0,x_1,x_2` and write `y_3=q_0e+v`.  If `P_3` denotes the ternary
squarefree permanent on `span(X_1,X_2,X_3)`, the only possibly nonzero
coefficients are

```text
T_0110=P_3(x_1,x_2,v),
T_1010=P_3(x_0,x_2,v),
T_1100=P_3(x_0,x_1,v),
T_1110=q_0 P_3(x_0,x_1,x_2),
T_1111=    P_3(x_0,x_1,x_2).                      (5)
```

Nonzero purity forces `q_0=0` and the first three entries to vanish.  Thus
all four planes contain `e`; after making mode three the distinguished mode,
these are precisely the pairwise `B_v`-orthogonality equations defining the
common-singleton component 18.

### Binary support gives component 21

Write the general Borel rows

```text
x_0=a_0C+b_0B+d_0D,
x_i=a_iA+b_iB+d_iD          (i=1,2),
y_3=pA+cC+qB+rD,            x_3=C.                (6)
```

The forbidden coefficients first give

```text
b_i q-d_i r=0                (i=0,1,2),
b_0b_i-d_0d_i=0              (i=1,2),
p=c=0.                                                (7)
```

The active coefficient is

```text
T_1111=-4a_0(b_1b_2-d_1d_2).                       (8)
```

Hence `a_0!=0`, `q^2-r^2!=0`, and (7) forces `b_0=d_0=0` and
`(b_i,d_i)=t_i(r,q)` with `t_1t_2!=0`.  Scale rows and apply

```text
diag(1,1,1/(r+q),1/(r-q)).                         (9)
```

The four planes become

```text
<A,C>,       <C,B+k_1A>,       <C,B+k_2A>,       <D,C>.  (10)
```

In the mode order `(1,2,0,3)` this is component 21 with its parameters
`q=0`, `kappa=k_1`, `[r:s]=[0:1]`, and `p=1/k_2`.  The divisor `k_2=0` is
the homogeneous `p=infinity` endpoint already included in the projective
component-21 reverse theorem.  Thus the whole binary chart, not merely its
finite part, lies in component 21.

## II. The reverse spoke on binary double support

The exact pair `x_0y_3=0` has, relative to the binary label `{0,1}` in (3),
one of five support orbits: equal binary, adjacent binary, disjoint binary,
a singleton on `{0,1}`, or a singleton outside `{0,1}`.

The equal-support orbit is empty.  With `x_0=C,y_3=A`, direct expansion gives

```text
T_0110=4E,       T_1111=-4a_3E,
E=b_1b_2-d_1d_2,                                (11)
```

so purity kills the active coefficient.

The adjacent-binary orbit is also empty.  In the normalized `{0,2}` chart,
`T_1001` first removes the last coordinate of `x_3`.  Put

```text
X=a_1(b_2-d_2)+a_2(b_1-d_1),
E=b_1b_2-d_1d_2.
```

Then `T_0110=0` gives `X=E`.  If `E=0`, the active coefficient vanishes.
If `E!=0`, the two one-leaf equations force `beta=2alpha`, while `T_0111=0`
forces `2alpha+beta=0`; characteristic zero again gives a zero active
coefficient.

Both singleton orbits are empty by shorter syzygies.  For a singleton on
`{0,1}`, purity gives `E=0`, after which `T_0111=0` is exactly the remaining
part of `T_1111`.  For an outside singleton, `T_1001=0` and `T_0110=0` give

```text
T_1111=(c_0+c_1)
        [a_1(b_2-d_2)+a_2(b_1-d_1)]=0.             (12)
```

No all-pair hypothesis is needed for these four obstructions.

### The disjoint binary survivor is component 8

The only surviving binary support is the disjoint pair.  Normalize

```text
x_0=B,       y_3=D,
x_i=a_iA+b_iB+d_iD  (i=1,2),
x_3=a_3A+c_3C+e_3B.                               (13)
```

Purity and `T_1111!=0` are exactly

```text
e_3=c_3=0,       a_3!=0,
a_1d_2+a_2d_1=0,
b_1b_2-d_1d_2=0,
F=a_1b_2+a_2b_1!=0.                               (14)
```

Scale `a_3=1`.  Besides the selected star, (14) creates the exact relations

```text
y_1x_3=0,       y_2x_3=0.                         (15)
```

On modes `(1,0,3)`, equations (1), (13), and (15) form the mixed-chain
rank-one triangle with exactly one kernel--kernel edge and two disjoint
support labels.  In the notation of the exact triangle reduction, after the
source involution `A<->C`, its three planes are

```text
<C,a_1A+b_1B+d_1D>,       <A,B>,       <D,A>.      (16)
```

If both leaf affine coefficients are nonzero, (14) puts this on the
transverse mixed-chain sheet.  If one affine coefficient vanishes, leaf
symmetry gives either the same transverse sheet or a pair image of rank two.
Indeed, `F!=0` implies that some leaf has

```text
a_i(b_i^2-d_i^2)!=0                              (17)
```

unless the opposite leaf--mode-three image has rank two.  The all-pair locus
therefore lies entirely on the transverse sheet, whose exact valuative
placement theorem puts it in component 8, including its projective endpoint
and `phi=0` boundary.

## II continued: singleton double support

Now use (2).  If the reverse exact pair has singleton support outside
`X_0`, the active coefficient is a multiple of the forbidden coefficient
`T_0110`; it vanishes.  If its binary support contains `X_0`, purity gives
the same two-step syzygy as the singleton-on-label case above, so the active
coefficient again vanishes.

It remains to take a disjoint binary support, normalized as

```text
x_0=X_1+X_2,       y_3=X_1-X_2.                   (18)
```

Write

```text
x_i=a_iX_1+b_iX_2+c_iX_3             (i=1,2),
x_3=qX_0+alpha(X_1+X_2)+gamma X_3.   (19)
```

The active coefficient is

```text
T_1111=q[(a_1+b_1)c_2+(a_2+b_2)c_1].              (20)
```

If `gamma=0`, nonzero purity forces `alpha=0`, so `x_3=qX_0` and all four
planes contain `X_0`; this is component 18.  In fact the reverse-spoke pair
then has the two relations `X_0^2=0` and
`(X_1+X_2)(X_1-X_2)=0`, so its image has rank at most two and this branch is
outside the all-pair locus.  If `gamma!=0`, the forbidden
coefficients force, up to exchanging leaves,

```text
a_1=b_2=0,       b_1a_2!=0,
c_1=-b_1 gamma/(2alpha),
c_2=-a_2 gamma/(2alpha).                           (21)
```

Modes `(0,1,2)` then have the three relations

```text
y_0y_1=y_0y_2=y_1y_2=X_0^2=0.                    (22)
```

They form the fully kernel--kernel rank-one triangle.  The fourth plane does
not contain `X_0` when `gamma!=0`, so the complete triple-kernel triangle
classification places this branch in component 16.  Any failure of a
selected rank-three condition is already in the lower-pair locus.

## Exact replay and boundaries

```text
uv run --with sympy python verify_p4_two_double_endpoint_star_111_complete_classification.py
uv run --with sympy python audit_p4_two_double_endpoint_star_111_complete_classification.py
```

The primary verifier reconstructs every displayed coefficient and placement
normal form over a symbolic characteristic-zero field.  The independent
audit rebuilds the permanent by subset dynamic programming and checks
rational representatives after an unequal diagonal source scaling and a
source permutation.  No finite-field computation is used as proof.
