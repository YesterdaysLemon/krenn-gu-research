# Component twenty-two: complete `H=h2=0` terminal obstruction

## Status

**Exact characteristic-zero branch closure.**  Work over
`K=Q(A,R,D)` on component twenty-two's retained finite `D23` chart and put

```text
H=2*A*h1+1=0,  h2=0,  rho*(rho+1)!=0.             (1)
```

The earlier specialized theorem closes the three rank-drop divisors

```text
rho=1,  f6=0,  f8=0.                               (2)
```

The exact sparse reduction and four six-by-six determinants below close the
entire complementary branch.  Consequently no binary extension, and hence no
weighted-`H22` lift, exists anywhere on (1).

This closes only the `h2=0` factor inside the broader `H=0` cover.  The other
factors `s*h2+1`, `f7`, `f8`, `U`, and `V` away from this intersection,
coefficient-field boundary fibres, other projective/source/ambient charts,
and the global Krenn--Gu conjecture remain **UNRESOLVED**.  No finite field,
random sample, or numerical rank is used.

## Sparse pivot and first cover

Write

```text
s=2*A+R,
f6=(D-1)*rho+D+1,
f7=(A*D+A+R)*rho+A*D-A-R,
f8=(A*D+A+R*D)*rho+A*D-A+R*D,
W=f7*h0+s-R*rho.                                    (3)
```

Mixed rows 1 and 5 have support only in extension columns 3 and 6, with
two-by-two determinant `-f6*f8`.  Therefore every selected eight-by-eight
minor below is this pivot times its complementary six-by-six minor.

On rows `(0,2,3,6,7,11)` and columns `(0,1,2,4,5,7)`, that complement is

```text
8*D^2*rho*s^4*(D-1)*(D+1)*(rho-1)*(rho+1)^2*W.     (4)
```

Away from (2), rank drop forces `W=0`.  This branch automatically has
`f7!=0`: the resultant in `rho` of `f7` and `s-R*rho` is

```text
2*A*(A+R)*(D+1),                                    (5)
```

a unit of `K`.  Hence one may substitute

```text
h0=-(s-R*rho)/f7.                                   (6)
```

## The linear `P` residue

After (6), the complementary minor on rows `(0,2,3,6,7,10)` and the same
six columns is

```text
-4*A*D*rho*s^2*(D+1)*(rho+1)^2*P,                  (7)
```

where `P` is linear in `h3`.  If `P=P0+P1*h3`, exact polynomial gcd over
`K[rho]` gives

```text
gcd(P0,P1)=1.                                       (8)
```

Thus `P=0` never meets `P1=0`, and the terminal substitution
`h3=-P0/P1` loses no point.

## Two terminal minors

After `W=P=0`, use the common columns `(0,1,2,4,5,7)` and row sets

```text
R0=(2,3,6,7,10,12),
R1=(2,3,6,7,8,10).                                  (9)
```

Their determinants have numerators `N0,N1`.  Over `K[rho]` the exact monic
gcd is

```text
gcd(N0,N1)=rho*(rho+1)^2.                          (10)
```

For replay transparency, the verifier also checks the complete factorizations

```text
N0=-D*rho*s^3*(D+1)^2*(rho+1)^2*L1*L2,
N1= 2*A*D*rho*s^2*(D+1)^2*(rho+1)^2*M1*M2*M3,
```

with the second determinant equal to `N1/f7`; all five linear factors are
printed and asserted by the scripts.  Equation (10) makes simultaneous rank
drop impossible under (1).  Together with (2), this closes the branch.

## Replay

Replay the prerequisite three-divisor closure first:

```powershell
uv run --with sympy python verify_p5_h22_unequal_complement_common_kernel_component_d23_h1_nonzero_h2_zero_partial_closure.py
uv run --with sympy python audit_p5_h22_unequal_complement_common_kernel_component_d23_h1_nonzero_h2_zero_partial_closure.py
```

Then run:

```powershell
uv run --with sympy python verify_p5_h22_unequal_complement_common_kernel_component_d23_h2_zero_terminal_complete_obstruction.py
uv run --with sympy python audit_p5_h22_unequal_complement_common_kernel_component_d23_h2_zero_terminal_complete_obstruction.py
```

The primary uses the committed mixed matrix and exact `DomainMatrix`
determinants.  The audit imports neither verifier, rebuilds the permanent model
from its low-level source rows, and uses explicit Gaussian elimination over
rational-function fields.
