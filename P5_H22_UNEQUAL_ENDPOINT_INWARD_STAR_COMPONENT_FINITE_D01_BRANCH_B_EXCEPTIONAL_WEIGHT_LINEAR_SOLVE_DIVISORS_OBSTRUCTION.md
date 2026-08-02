# Component twenty-five's exceptional `B`-weight linear-solve divisors

## Status

**Exact characteristic-zero special-divisor theorem.**  On the ordinary
finite-`D01`, `B=0`, `N=0` branch of component twenty-five, none of the
retained linear-solve divisors

```text
e=0,  j=0,  s=0,  lambda=0
```

supports a weighted `H22` lift inside the normalized component chart.  The
proof includes the split component corner `e=s=0`, `k=+/-j`, and the only new
standing-chart family at `lambda=0`.  Both carry binary-side sections, but an
exact paired finite-`D23` one-marked map has rank four.

This closes only these four intersections with the exceptional divisor.  The
leading-weight divisor `A_2=0`, the opposite-diagonal and rank-norm divisors
retained by the generic exceptional theorem, and the remaining projective
component boundaries are not closed here.  This is not a counterexample.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## Algebraic intersection cover

Retain

```text
P=ej+k^2,  Q=e+j,  R=1+ejs^2,
F=PR-Q^2,
N=A_2 lambda^2+A_1 lambda+A_0.
```

Direct exact factorization gives

```text
N|_{e=0}=j^3 s (lambda-1)T,

N|_{j=0}=e^2(lambda+1)
          ((es+1)lambda+(1-es)),

N|_{s=0}=e(e+j)(lambda+1)^2,

N|_{lambda=0}=(es-1)(js+1)C_0,                    (1)
```

where

```text
T=(js-1)lambda-(js+1),

C_0=3e^2j^2s^2-e^2js-e^2-ej^3s^2
    +2ej^2s-ej-j^3s.                               (2)
```

The ordinary chart has `lambda^2!=1`.  The prior exact `T=0` and `H=0`
theorem therefore removes the `e=0`, `s!=0` possibilities in (1).  If `s=0`,
the third line of (1), together with `Q!=0`, reduces to `e=0`.  The case
`j=0` lies on `e^2-k^2=0` by the component equation and is outside the
normalized chart.  Thus the only in-chart parameter corner from the first
three divisors is

```text
e=s=0,  j!=0,  k=epsilon j,  epsilon in {+1,-1}.   (3)
```

## The split corner `e=s=0`

On either sheet (3), the `B` equation gives `z_3=0`.  The remaining binary
equations have the one-parameter section

```text
z_6=-epsilon/[2j^3(lambda-1)]-(lambda+1)w.         (4)
```

The other extension coordinates are reconstructed from the four forced
mode-zero equations.  Marking by

```text
h=(0,-1/j,0,-epsilon j)                            (5)
```

makes all fourteen mixed finite-`D01` coefficients vanish.  The normalized
first diagonal is one; the opposite diagonal is

```text
-(lambda+1)
 (4j^3(lambda^2-1)w+epsilon)/[j(lambda-1)].        (6)
```

When (6) is nonzero this is a genuine binary incidence.  Regardless of `w`,
the one-marked finite-`D23` map in mode one has the two exact `4 x 4` minors

```text
M_1=4 epsilon w^2(lambda-1)^4,

M_2=3 epsilon
    (2j^3(lambda^2-1)w+epsilon)^2/j^6.             (7)
```

They cannot vanish simultaneously: `M_1=0` forces `w=0`, and then `M_2` is
nonzero.  Hence this map has rank four for every section, including every
section with nonzero binary diagonals.

## The singular weight `lambda=0`

At `lambda=0`, the already-certified full-field `S_13,S_23` equations have
compatibility factor

```text
(es-1)(s(e-j)+2).                                  (8)
```

The factor `js+1` in (1) is the empty `H=T=0` boundary.  The branch `es=1`
in (8) satisfies `e^2-k^2=0` by `F=0`, so it leaves the normalized chart.  On
the remaining branch, substitute `j=e+2/s` into (2):

```text
C_0=2(es+1)^2((es)^2+es-4)/s^2.                   (9)
```

Since `H=(es+1)(js+1)` is a unit at `lambda=0`, the only new standing-chart
family is therefore

```text
es=u,  js=u+2,  u^2+u-4=0.                        (10)
```

Here

```text
P=4/s^2,  Q=2(u+1)/s,  R=u+5,
k^2=-u/s^2,  e^2-k^2=4/s^2.                       (11)
```

The norm of `-u` from `Q(u)` to `Q` is `-4`, so `-u` is not a square in
`Q(u)`.  Thus

```text
E=Q(s)[u,k]/(u^2+u-4, k^2+u/s^2)
```

is the full degree-four field used below.  No component-field equation is
split during the binary solve.

The complete binary section is

```text
w=t_0+t_1 k,
z_6= -s^4(u-1)k/32-w.                              (12)
```

Direct reconstruction and marking make all fourteen mixed finite-`D01`
coefficients zero.  The two diagonals are

```text
1,

-16t_0/s^2
 + ((s^4-64t_1)/(4s^2)-s^2u/4)k.                 (13)
```

The `uk` coefficient in (13) is nonzero, so the opposite diagonal never
vanishes.

For the paired finite-`D23` mode-zero map, take the four coefficient rows
indexed by `000,001,010,011`.  Put

```text
x=t_0/s^3,  y=t_1/s^4.
```

In the basis `1,u,k,uk`, its determinant has unit monomial factors times the
four quadrics

```text
q_0= 320x^2-7424xy+196x+7936y^2-312y+3,
q_1=1984x^2-3840xy+140x+2304y^2-232y+3,
q_2=1984x^2-1280xy+308x+7424y^2-392y+5,
q_3=1856x^2-7936xy+156x+3840y^2-280y+3.           (14)
```

Exact characteristic-zero reduction gives

```text
Groebner_QQ[x,y](q_0,q_1,q_2,q_3)=[1].            (15)
```

Hence the determinant cannot vanish for any `t_0,t_1`, even after algebraic
extension.  The mode-zero map always has rank four, so (10) supplies no
weighted `H22` lift.

## Remaining boundary

Combining this package with the generic exceptional-divisor theorem and the
earlier `T=0`, `H=0`, and endpoint theorems closes the `N=0` intersections
with

```text
e j s lambda T H (lambda^2-1)=0
```

inside the normalized finite-`D01` `B` analysis.  Still retained are

```text
A_2=0,
the global opposite-diagonal norm divisor,
the four global D23 rank-norm divisors,
P R Q k (e-j)(e^2-k^2)=0,
and projective component-boundary charts.          (16)
```

The first line and the intersections among the norm divisors are the next
finite-sheet residual.  Equation (16) is a boundary ledger, not a claimed
survivor or counterexample family.

## Replay

First replay the prerequisite residual and `T/H` certificates:

```text
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_residual.py
uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_residual.py
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_t_zero_and_h_boundary_obstruction.py
uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_t_zero_and_h_boundary_obstruction.py
```

Then run:

```text
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_linear_solve_divisors_obstruction.py

uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_linear_solve_divisors_obstruction.py
```

The primary expands permanents by permutations, uses a direct determinant,
and verifies (15) by a Gröbner basis over `QQ`.  The no-import audit uses
subset-dynamic-programming permanents, a recursive determinant, and an
independent resultant-gcd certificate for (15).  Both work only in exact
characteristic zero and use no finite-field evidence.
