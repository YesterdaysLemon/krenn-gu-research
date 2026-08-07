# A twenty-third pure `P_4` component in the common-center-kernel star

## Status

**Exact characteristic-zero component and orientation-classification
theorem.**  In the star cell with relation ranks `(2,1,1)`, take the rank-two
spoke as the center synchronizer and let both rank-one spokes use the center
kernel with active leaf endpoints.  The genuine split-support branch is a new
smooth five-dimensional irreducible component orbit, component twenty-three.

The same exact normal-form calculation exhausts every projective support
boundary in this common-center-kernel outward orientation.  Its nonzero
all-pair points lie in component twenty-three, the already classified
common-active triangle components eleven or twelve, or the certified
lower-pair locus.  The other inward or mixed-center star orientations remain
open, as do the new component's `P_5` fibres and the global local-to-global
step.  The Krenn--Gu conjecture remains **UNRESOLVED**.

## The new family

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2)
```

and put

```text
A=X_0+X_1,   C=X_0-X_1,
B=X_2+X_3,   D=X_2-X_3.                           (1)
```

The four ordered planes are

```text
U_0=<A,B>,
U_1=<A+kD,B+sC>,
U_2=<s(A-C)+B+rD,C>,
U_3=<-s(A+C)+B+tD,C>.                            (2)
```

Their only possibly nonzero tensor coefficients are

```text
T_0000=-4(-skr+skt+rt-1),    T_1111=-4.           (3)
```

Consequently the hypersurface

```text
1-rt=ks(t-r)                                             (4)
```

is pure and nonzero.  On its dense chart `s(t-r)!=0`, eliminate
`k=(1-rt)/(s(t-r))`.  The pair profile in the order
`01,02,03,12,13,23` is generically

```text
(3,3,3,4,4,4),                                    (5)
```

and the three exceptional relations are

```text
y_0 x_1-x_0 y_1=0,    y_0 x_2=0,    y_0 x_3=0,    (6)
```

of matrix ranks `(2,1,1)`.  Three convenient full-pair minors are

```text
edge 12, rows 0123:  16s(r-1)(r+1)(rt-1)/(r-t)^2,
edge 13, rows 0134: -16s(t-1)(t+1)(rt-1)/(r-t)^2,
edge 23, rows 0123:  -8s(r-t)^2.                  (7)
```

They exhibit the dense all-pair open directly.

## Smooth component certificate

At

```text
(s,r,t,k)=(1,2,3,-5),                             (8)
```

use Grassmann pivots `(02),(01),(01),(01)` and restore the diagonal source
torus `diag(q_0,q_1,q_2,1)`.  The family Jacobian has rank five.  On coordinate
rows `(g_0,g_3,g_4,g_5,g_8)` and parameter columns
`(s,r,t,q_0,q_2)`, its determinant is

```text
-3/4.                                             (9)
```

In the universal Segre-incidence chart, use tensor anchor `1001` and target
coordinate `(0,-1,0,0)`.  The Jacobian has rank fifteen.  The columns

```text
g_0,...,g_9,g_12,g_13,z_0,z_2,z_3
```

and all fifteen incidence rows give determinant

```text
-9600.                                            (10)
```

Thus the pure incidence is smooth of local dimension five, and the
irreducible parameter-hypersurface/source-torus image supplies all local
directions.  Its closure is an irreducible component.

The dense invariant stratum has a rank-three star, relation word `(2,1,1)`,
a rank-two synchronized spoke, and two outward active rank-one spokes sharing
the split-support center kernel.  This endpoint/support word does not occur
on components one through twenty-two; the pair graph and relation word first
separate the lower-pair, triangle, all-pair-three, and six-dimensional
components, and the oriented center-kernel word separates the remaining star
orbits.  Hence this is component twenty-three.

## Complete outward-orientation boundary ledger

Gauge the rank-two spoke so that its relation is the first equation in (6).
Each rank-one spoke sharing the center kernel is either `O_Y`, using its leaf
kernel endpoint, or `O_X`, using its leaf active endpoint.  The annihilator of
the center kernel has support size one or two.

### Center support one

Normalize the center kernel to `e=X_0`, take
`x_0=a=X_1+X_2`, and put `c=X_1-X_2`.  Every rank-three synchronizer is

```text
U_1=<e+tau c, v e+a>,   tau!=0.                  (11)
```

The other possible supports of `x_0` already give `r_01<=2`.  In the `YY`
flag the forbidden coefficients `T_1101=2z_3` and `T_1110=2z_2` kill the
active coefficient.  In the `YX` flag, `T_1100=2z_3=0` while the active
coefficient is `2z_2!=0`; the remaining equations

```text
T_0110=2a_3z_2,       T_0010=-2tau c_3z_2        (12)
```

make the second leaf kernel proportional to its own active leaf row `e`.  The
`XX` active coefficient contains `e^2=0`.  Thus no support-one all-pair point
survives.

### Center support two

Normalize the center kernel to `A`, its binary partner to `C`, and write

```text
x_0=alpha C+E,   E=bB+dD,   Q=b^2-d^2.           (13)
```

Solving the synchronizer equations for
`y_1=uA+vC+wB+zD` and `x_1=rA+sC+tB+qD` gives exactly

```text
r=-alpha v,  t=bu,  q=du,
alpha w+bv=alpha z+dv=dz-bw=0.                   (14)
```

There are four exhaustive cases.

- `E=0` gives `r_01<=1`.
- `Q=0` makes `E` a singleton.  Direct coefficient elimination in both
  charts `alpha=0` and `alpha!=0` excludes `YY`, `YX`, and `XX` unless a leaf
  pair drops below rank three.
- `alpha Q!=0`: `YY` and `YX` have respective constant forbidden
  coefficients `-4Q`; `XX` duplicates the two leaf edges into the complete
  common-active `triangle-(2,1,1)` orientation.  It therefore lies in
  components eleven or twelve when the duplicated edge has rank three, and
  in the lower-pair locus otherwise.
- `alpha=0,Q!=0`: normalize `E=B` and its polar partner to `D`.  Rank three on
  the synchronized spoke makes `U_1=<A+kD,B+sC>`.  The `YY` and `YX` flags
  again have constant forbidden coefficient `-4`.  For `XX`, write the two
  leaf kernels as

  ```text
  y_i=a_iA+c_iC+e_iB+f_iD.
  ```

  Purity is exactly

  ```text
  c_i=-s e_i,
  a_2e_3+a_3e_2=0,
  a_2a_3+s^2e_2e_3=0,
  k(a_2f_3+a_3f_2)-e_2e_3+f_2f_3=0.              (15)
  ```

  On the all-pair locus `(a_i,e_i)!=(0,0)`.  If either `e_i=0`, its leaf pair
  has rank at most two.  Otherwise scale `e_2=e_3=1`; the middle equations in
  (15) give the two source-symmetric signs
  `(a_2,a_3)=(s,-s)` or `(-s,s)`.  With
  `(f_2,f_3)=(r,t)`, the last equation is (4), yielding (2).

The polynomial hypersurface (4) retains the `s=0,rt=1` and
`r=t=+/-1` projective boundary points; no denominator chart is silently
dropped.  The preceding rank tests place every boundary point that leaves the
all-pair open in the lower-pair locus.

This exhausts the unordered outward flag pairs `YY,YX,XX`.  Subsequent exact
work classifies the mixed-center orientation, excludes the equal-endpoint
two-inward stratum, and finds component twenty-five on the disjoint-binary
unequal-endpoint chart.  The remaining star-`(2,1,1)` problem is its reverse
unequal-support boundary ledger.

## Replay

```text
uv run --with sympy python claims/p4/classifications/star/common-center-kernel-star-211/verify_p4_common_center_kernel_star_211_component.py
uv run --with sympy python claims/p4/classifications/star/common-center-kernel-star-211/audit_p4_common_center_kernel_star_211_component.py
```

Both scripts use exact characteristic-zero arithmetic.  The audit rebuilds
the representative after an independent source permutation and unequal
diagonal scaling.  No finite-field sample is used as proof.
