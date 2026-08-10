# Ternary false-positive certificate for the component-twenty-five `A` survivor

## Status

**Exact characteristic-zero point obstruction.**  The rational terminal
survivor

```text
(e,j,k,s,lambda)=(-5,2,3,-1,1/3),
(z0,z1,z2,z3,z4,z5,z6,z7)
 =(13/448,-33/56,-1/56,-3/64,
   -1/28,79/448,1/28,5/32)                       (1)
```

on component twenty-five's finite-`D01`, exceptional `A` divisor is a false
positive.  Its unique normalized affine marking passes the four local `D01`
one-marked rank tests, but all four paired `D23` one-marked maps have rank
four.  A fixed exact minor is

```text
det N^D23_1[0456]=-1/28224 != 0.                  (2)
```

Therefore (1) is not a ternary weighted-`H22` lift and is not a counterexample
to the Krenn--Gu conjecture.  This point certificate does not close the entire
exceptional divisor, the parallel `B=0` branch, or any component-special or
projective fibre.  The global conjecture remains **UNRESOLVED**.

## Unique marking

Let `C_w` be the unmarked finite-`D01` binary coefficients of (1).  The
normalization is `C_0000=1`.  If

```text
beta_i -> beta_i+h_i alpha_i,
```

then vanishing of the four marked singleton coefficients uniquely forces

```text
h_i=-C_{e_i},
h=(0,5/16,2,-38/21).                              (3)
```

The extension entry is marked at the same time: the full projected row is
`beta'_i+h_i alpha'_i`, including its fifth-coordinate extension.  Omitting
that extension shift gives the wrong rank calculation.

At (3), the marked finite-`D01` tensor has all fourteen mixed coefficients
zero and pure diagonals

```text
(C_0000,C_1111)=(1,0).                            (4)
```

Thus the point already misses the nonzero opposite diagonal required of a
genuine binary neighbour.  Consistently, its four `D01` one-marked `8 x 4`
maps have ranks

```text
(3,3,3,3).                                        (5)
```

Because `C_0000` is nonzero, (3) is the only marking in the affine complement
chart.  A marking-at-infinity would collapse a complement vector to the
chosen alpha row and is not another basis marking of this normalized point.

## Paired ternary obstruction

Project the same fully marked lifted rows through the finite `D23` contraction
at `lambda=1/3`.  The four one-marked ranks, in modes zero through three, are

```text
(4,4,4,4).                                        (6)
```

For mode one and ternary row words `000,100,101,110`, whose lexicographic row
indices are `0,4,5,6`, the complete four-column submatrix is

```text
[ 31/672   -79/672     0       0   ]
[-1/84       1/28      0       0   ]
[ 61/882   -61/294    3/28     0   ]
[131/672    65/224   -3/32   -4/3 ].              (7)
```

Its determinant is (2).  A ternary lift would factor this map through a
three-dimensional target, forcing rank at most three.  Equation (2) is
therefore an exact obstruction.

For completeness, the `0123` minors in the four `D23` modes are

```text
(-380369/9261,
 -97669/903168,
 -505/451584,
 -6829/8232),                                     (8)
```

so the conclusion does not depend on a single distinguished mode.

## Replay and boundary

Run:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-a-exceptional-divisor/verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a_exceptional_divisor_ternary_false_positive.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-a-exceptional-divisor/audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a_exceptional_divisor_ternary_false_positive.py
```

The primary verifier reconstructs the certified component basis and both
finite contractions.  The audit imports no project code and independently
rebuilds the basis, contractions, permanents, marking, and one-marked maps.
All arithmetic is over `Q`; no finite-field computation is used.

Only the rational point (1) is excluded here.  Extending (2) symbolically
along `(js-1)lambda-(js+1)=0` is a separate task; no full-divisor theorem is
inferred from this specialization.
