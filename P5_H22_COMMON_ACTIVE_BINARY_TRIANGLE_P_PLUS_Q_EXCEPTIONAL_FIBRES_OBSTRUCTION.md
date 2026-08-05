# Verified weighted-`H22` obstruction on the exceptional finite fibres

## Status and scope

**VERIFIED after a fresh no-import audit.**  This note gives a direct
characteristic-zero obstruction to
weighted `H22` on the `a=0,-1` fibres of the verified diagonal-DVR
`p+q=0` boundary.  It covers both displayed `y=0` charts `B_full,B_drop`
and every actual negative-valuation exceptional lower-pair specialization.
It never specializes a formula containing `1/a` or `1/(a+1)`.

The proof closes the necessary projective `D01` neighbour in every case, so
no `D23` calculation is needed.  It does not address weighted `H22` at other
centres, non-diagonal source transformations, arbitrary-order gluing, or the
global Krenn--Gu conjecture.

## Weighted direction and criterion

For a source row `z=(z0,z1,z2,z3)`, extension entry `u`, and finite slope
`r`, use

```text
D01^r(z,u)=(r z0+z1,z2,z3,u),
D01^infinity(z,u)=(z0,z2,z3,u).                     (1)
```

A genuine binary neighbour has both diagonal coefficients `A,B` nonzero.
A weighted-`H22` lift requires such a neighbour for every required half,
including `D01`, and its one-marked local map has rank at most three.
Consequently a fixed nonzero `4 x 4` one-marked minor on the genuine open
excludes the lift.

All affine markings are `beta_i(h)=beta_i+h_i alpha_i`.  The normalized
incidence is

```text
<M(h,r)z, A(h,r)z-1, w B(h,r)z-1>,                 (2)
```

with `r` also eliminated at finite slope.  For `B_full`, `lambda!=0` is
saturated explicitly; for the lower-pair wall, `gamma!=0` is saturated.
Thus (2) covers every projective extension direction with `A B!=0`.

## Direct `B_full` and `B_drop` fibres

Put `e=X0`, `L=A-B`, `M=A+B`, `C=X3`.  At either exceptional centre use
the direct orientations

```text
k0=(2a+1)C,
alpha=(k0,e,e,M),

B_full: beta=(e+lambda L,(a+1)L+C,aL+C,e), lambda!=0,
B_drop: beta=(L,          (a+1)L+C,aL+C,e).         (3)
```

At `a=0` the sole pure coefficients are `-2lambda,-2`; at `a=-1` they
are `2lambda,2`.  Exact saturated elimination gives, for both charts and
both finite and infinite `D01`,

```text
a=0:  J=<h3,h2,h0>,     h=(0,t,0,0),
a=-1: J=<h3,h1,h0>,     h=(0,0,t,0).               (4)
```

The complete generic kernels have the following diagonal and fixed-minor
forms.  `X,Y,Z` are homogeneous kernel coordinates; the chosen minor is in
marked mode three, on rows `0247` for `a=0` and `0147` for `a=-1`.

```text
                              A                    B                    det/(A B)
a=0,  B_full, finite       -2Yr   -2(lambda+r)(Xr+Y(rt+1))             -2Y lambda r
a=0,  B_full, infinity     -2Y    -2(X lambda+Y)                        -2Y lambda
a=0,  B_drop, finite       -2Yr   -2(Xr+Y(rt+1))                       -2Yr
a=0,  B_drop, infinity     -2Z    -2X                                  -2Z

a=-1, B_full, finite        2Yr   -2(X lambda r-Y(lambda+r))           -2Y lambda r
a=-1, B_full, infinity      2Y    -2(X lambda-Y)                        -2Y lambda
a=-1, B_drop, finite        2Yr   -2(Xr-Y)                             -2Yr
a=-1, B_drop, infinity      2Z    -2Y                                  -2Z.              (5)
```

Each ratio in (5) is nonzero whenever `A B!=0` on its stated chart open.
The finite slope `r=0` has `A|ker=0` on all four direct fibres.  The only
kernel-frame denominator occurs for `a=-1,B_full` at `lambda+r=0`; a direct
rebuild there gives `B|ker=0`.  Thus (5), plus those direct specializations,
covers every finite slope and the infinity endpoint.

## Actual exceptional lower-pair specializations

Use the verified residue normal forms

```text
e=X0, L=A-B, M=A+B, C=X3, W=xL+yM.

baseline:
  alpha=(e,M,e,C-W), beta=(L,e,C+W,L);

wall, gamma!=0:
  alpha=(e,M,e,C-W), beta=(L,e,C+W,L+gamma e).      (6)
```

Both have sole pure coefficient `T_1111=-2`.  These families exhaust the
non-embedded exceptional strata:

```text
valuation(y0)>-R:       x=y=0,
valuation(y0)=-R, R<d: x=pi,y=0,
valuation(y0)=-R, R=d: x=(pi-theta)/2, y=Delta/2!=0.               (7)
```

At `R=d`, the cases `P<Q`, `Q<P`, and `P=Q` give respectively `x=y`,
`x=-y`, and `x^2!=y^2`.  The compulsory mode-zero Pluecker coefficient is
`p12=-2y=-Delta`.

Parametric elimination over `Q[x,y]`, without generic residue assumptions,
gives

```text
baseline finite:   J=<h3,h2,h1>,  h=(t,0,0,0),
baseline infinity: J=<h3,h2,h1>,  h=(t,0,0,0),
wall finite:       J=<h3,h2,h1>,  h=(t,0,0,0),
wall infinity:     J=<h3,h2,h1,h0>, h=0.           (8)
```

Hence (8) includes `x=0`, `x=+/-y`, `y=0`, and `x=y=0` without a
specialization argument.  Complete kernels give, in marked mode one on rows
`0137`,

```text
family/direction         A                         B                         det
baseline finite        -2Xr                    -2X(rt+1)            8X^3 r^2(rt+1)
baseline infinity      -2X                     -2(Xt+Z)             8X^2(Xt+Z)
wall finite            -2Yr/[gamma(rt+1)]      -2Y(gamma r+1)/gamma
                                                                    8Y^3 r^2(gamma r+1)
                                                                      /[gamma^3(rt+1)^2]
wall infinity          -2X                     -2Z                   8X^2Z.              (9)
```

The wall finite formula is used only on `r(rt+1)gamma!=0`.  Direct rebuilds
give `A|ker=0` at `r=0` and `B|ker=0` at `rt+1=0`; if
`gamma r+1=0` in the remaining open, (9) itself gives `B=0`.  Thus every
genuine lower-pair `D01` neighbour has marked rank four.

At `a=-1`, swapping the two lower tensor modes and applying the allowed
diagonal source sign `e -> -e` gives the same two families.  Projective
finite slopes are merely reparametrized, and infinity is preserved.

## Consequence and retained failures

Equations (4)--(9) exclude the necessary `D01` neighbour on every direct or
lower-pair exceptional fibre.  Therefore the marked weighted-`H22` fibre is
empty on the entire `a=0,-1` diagonal-DVR exceptional finite boundary,
conditional on the verified `P4` residue classification.

- The generic formulas with `1/a` and `1/(a+1)` are not specialized.
- Projection ideals are closures; every special slope or residue branch is
  checked by a complete direct kernel.
- An initial exploratory import from the partial verifier failed because the
  reconstruction helper lives in its independent audit.  It produced no
  mathematical evidence.
- No broad minor scan or finite-field inference is used.
- A separate verifier independently rebuilt all twelve projections, every
  complete generic and residue kernel, thirty singular-slope fibres, fixed
  minors, projective scaling, the `a=-1` symmetry, and the residue exhaustion.

## Exact replay

```text
uv run --with sympy python verify_p5_h22_common_active_binary_triangle_p_plus_q_exceptional_fibres_obstruction.py
uv run --with sympy python audit_p5_h22_common_active_binary_triangle_p_plus_q_exceptional_fibres_obstruction.py
uv run --with sympy python audit_p5_h22_common_active_binary_triangle_p_plus_q_exceptional_fibres_independent.py
```
