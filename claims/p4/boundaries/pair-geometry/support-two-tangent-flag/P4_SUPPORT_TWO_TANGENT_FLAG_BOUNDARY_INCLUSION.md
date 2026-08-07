# Support-two tangent flags lie on the known sixfold

## Status

**Exact characteristic-zero boundary theorem.**  Every dense non-embedded
support-two polar flag in the tangent rank-two pair classification lies,
up to source and mode symmetry, in the closure of the six-dimensional
lower-pair component from
[`P4_SIX_DIMENSIONAL_PURE_COMPONENT.md`](../../../components/six-dimensional/P4_SIX_DIMENSIONAL_PURE_COMPONENT.md).

Together with the embedded-`P_3` alternative, this proves that support-two
tangent kernels create no new pure-`P_4` component.  The full-support tangent
branch is genuinely different and gives the fourteenth component.

The proof is an explicit one-parameter arc in Pluecker coordinates.  No
elimination or point search is used.

## The target polar flag

Use old source coordinates `E_0,...,E_3`, and define the new Witt basis

```text
e=E_3,
H=alpha E_0+beta E_2,
S=alpha E_0-beta E_2,
Z=tau E_1.                                           (1)
```

Here `e,H` span the tangent plane, `S` is the annihilator direction of `H`,
and `Z` is the fourth coordinate.  A dense polar flag may be written

```text
A=span(e+pS, H+lambda Z+qS),
B=span(S,   H-lambda Z+r e),                         (2)
```

with `p lambda !=0`.  The other orientation is obtained by swapping `A,B`.
The points `p=0` and the projective endpoint are in the closure of this
dense chart.

## Start inside the known six-dimensional component

Write `s=a+c` in the older component normal form.  Its four planes are

```text
V_0=span(E_0-E_3, E_2+E_3),

V_1=span(
 E_0+bE_1+(1-b(s-d))E_3,
 e_1 E_1+E_2+(1-e_1(s-d))E_3),

V_2=span(E_0-E_2, E_1-sE_2-dE_3),

V_3=span(E_0+E_3, E_2-E_3).                         (3)
```

For every finite nonzero parameter, these planes lie in the certified
sixfold and restrict `P_4` to a nonzero pure tensor on a dense open set.

Apply the source scaling

```text
diag(alpha epsilon, tau, beta epsilon, 1),           (4)
```

and choose

```text
s=sigma/epsilon+s_0,       d=D,
b=epsilon/sigma+B epsilon^2,
e_1=epsilon/sigma+C epsilon^2,
h_0=s_0-D.                                          (5)
```

The second-order tuning of `b,e_1` is the critical scale: first order makes
the two rows of `V_1` collide, while the second order remembers the radical
flag.

## The tangent edge limit

The Pluecker vectors of the scaled `V_0,V_3`, divided by `epsilon`, tend to

```text
(0,0,alpha,0,0,beta),
-(0,0,alpha,0,0,beta),                              (6)
```

in edge order `(01,02,03,12,13,23)`.  Both limits are the plane

```text
span(e,H).                                           (7)
```

Thus the two reduced kernel points of the sixfold coalesce into the tangent
Segre kernel at `e tensor e`.

## The first opposite plane remembers the full flag

The scaled `V_1` has Pluecker valuation two.  After division by
`epsilon^2`, its limit is

```text
(alpha tau/sigma,
 alpha beta,
 -alpha(C sigma^2+h_0)/sigma,
 beta tau/sigma,
 tau(B-C),
 beta(B sigma^2+h_0)/sigma).                        (8)
```

Set

```text
lambda=2/sigma,
p=-1/(sigma(B-C)),
q=2p(C sigma^2+h_0)/sigma-1.                        (9)
```

The vector (8) is exactly `1/(2p)` times the Pluecker vector of

```text
span(e+pS,H+lambda Z+qS).                           (10)
```

Conversely, for any dense target values `p,q,lambda`, take
`sigma=2/lambda`, impose `B-C=-1/(p sigma)`, and solve the remaining linear
equation in `(C,h_0)` from (9).  Hence (10) covers the whole dense `A` chart.

## The second opposite plane supplies the polar partner

The scaled `V_2` has valuation one and limiting Pluecker vector

```text
(alpha tau,-alpha beta sigma,-alpha D,
 beta tau,0,beta D).                                (11)
```

With

```text
r=2D/sigma,                                         (12)
```

(11) is `-sigma/2` times the Pluecker vector of

```text
span(S,H-lambda Z+r e).                             (13)
```

The free parameter `D` reaches every `r`.  Equations (6), (10), and (13),
with the mode order

```text
(U_0,U_1,U_2,U_3)=(V_0,V_3,V_1,V_2),               (14)
```

converge to precisely the polar flag (2).

Because every point with `epsilon!=0` belongs to the irreducible sixfold,
the limit belongs to its closure.  Swapping the last two modes handles the
other choice of distinguished radical intersection.  Taking closures adds
`p=0` and the projective chart boundary.

## A rational arc

For the representative

```text
span(e,H), span(e,H),
span(e+S,H+Z+2S), span(S,H-Z+3e),                   (15)
```

choose

```text
alpha=beta=tau=1,    sigma=2,    D=3,
B=-1/2, C=0,         h_0=3,      s_0=6.             (16)
```

Then

```text
s=2/epsilon+6,
b=epsilon/2-epsilon^2/2,
e_1=epsilon/2.                                      (17)
```

The exact Pluecker leading terms reproduce all four planes in (15).  Its
pair profile is `(2,4,3,4,3,4)` and its pure restriction is
`-2y_0y_1(x_2-3y_2)y_3`, as checked independently in the tangent
classification.

## Across the mathematical fence

This is a limit-linear-series calculation in miniature.  Ordinary limits of
the two rows lose the plane because both rows collide.  Pluecker valuation
keeps the first nonzero wedge, while a second-order parameter jet records the
missing radical direction.  The apparent extra tangent direction found by
the incidence Jacobian is therefore a genuine formal arc into the known
sixfold.

The contrast with the full-support tangent component is structural:

```text
support two:   degenerate polar form -> integrable flag arc -> old sixfold,
support three: nondegenerate polar form -> two obstructed directions -> new fivefold.
```

## Verification

Run:

```text
uv run --with sympy python claims/p4/boundaries/pair-geometry/support-two-tangent-flag/verify_p4_support_two_tangent_flag_boundary_inclusion.py
python claims/p4/boundaries/pair-geometry/support-two-tangent-flag/audit_p4_support_two_tangent_flag_boundary_inclusion.py
```

The primary verifier derives every Pluecker leading vector and matches it to
(2).  The independent audit uses rational Laurent polynomials and a separate
wedge implementation on (16)--(17).  Neither performs a search.
