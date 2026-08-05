# Complete `e=1,j=2` slice obstruction on component twenty-five's exceptional `B` divisor

## Status

**Exact characteristic-zero nonpoint-slice theorem.**  On component
twenty-five's normalized ordinary finite-`D01`, `B=0`, `N=0` sheet, the full
one-parameter slice

```text
e=1,  j=2
```

supports no weighted `H22` lift.  In particular, the retained opposite-binary-
diagonal divisor and simultaneous paired-`D23` rank-norm divisor are both
closed everywhere that the rational section is defined.  The only extra
ordinary denominator fibre is an exact degree-four number-field fibre at
`lambda=5`; it is also obstructed by four nonzero paired rank minors.

This is a complete slice theorem, not a classification of the global
opposite-diagonal or rank-norm divisors.  It is not a counterexample.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## Exceptional curve and exact norms

Retain `s` as a transcendental parameter.  Then

```text
R=1+2s^2,
P=9/(1+2s^2),
k^2=(7-4s^2)/(1+2s^2),

N=A_2 lambda^2+A_1 lambda+A_0,

A_2=(s+1)(2s-1)(4s^2+2s-3),
A_1=-2(8s^4+16s^2-3),
A_0=(s-1)(2s+1)(4s^2-2s-3).                     (1)
```

The exact discriminant is

```text
disc_lambda(N)=4s^2(448s^4+16s^2-23),             (2)
```

whose last factor is nonconstant and squarefree.  The binary section is
therefore solved in the full algebra

```text
Q(s)[lambda,k]/(N,k^2-(7-4s^2)/(1+2s^2)),         (3)
```

without splitting equations into basis coefficients.

After normalizing the first binary diagonal to one, the iterated norm of the
opposite diagonal factors as

```text
64 s^4(2s^2+1)^4
  (112s^6-444s^4+363s^2-58)^2 / denominator.      (4)
```

The sextic in (4) is squarefree.  The verifier reconstructs fixed `4 x 4`
one-marked `D23` minors in all four modes and takes their iterated norms
`nu_0,...,nu_3` to `Q(s)`.  Their cancelled numerators satisfy

```text
gcd_Q[s](numer(nu_0),...,numer(nu_3))
  =(2s^2+1)^2.                                    (5)
```

Since `R=2s^2+1` is a standing-chart unit, (5) proves that at every defined
point at least one paired one-marked map has rank four.  Moreover, the sextic
in (4) is coprime to every individual rank-norm numerator and to every section
denominator.  Thus all four paired maps have rank four on the new
opposite-diagonal-zero fibre itself; those points are already nongenuine on
the binary side in any case.

## Complete denominator ledger

The primary and independent audit collect denominators from the component
parameters, solved extension, marking, all binary coefficients, paired rows,
four determinants, and five iterated norms.  The complete irreducible list,
up to rational scalars, is

```text
s,
2s-1,  2s+1,
2s^2+1,
4s^2+2s-3,
4s^2-2s-3,
4s^2-7,
4s^4+13s^2-8.                                    (6)
```

Every factor except one is already a named boundary:

- `s=0` is covered by the exact linear-solve-divisor theorem;
- `2s-1` and `4s^2+2s-3` lie on `A_2=0`;
- `2s^2+1=R=0` and `4s^2-7=0` (`k=0`) leave the standing chart;
- `4s^4+13s^2-8=0` is the `H=0` intersection, because the exact norm of
  `H=(lambda+1)R-(lambda-1)sQ` is

  ```text
  8s^2(2s+1)(4s^4+13s^2-8)
  /[(s+1)(4s^2+2s-3)];
  ```

- `2s+1=0` lies on `A_0=0`, where the two weights are `lambda=0,1`, both
  already closed;
- on the remaining `A_0` factor `4s^2-2s-3=0`, the two weights are
  `lambda=0,5`.  The first is covered by the linear-solve-divisor theorem;
  the second is the companion fibre below.

The omitted factors `s=+/-1` are the standing boundary `e^2-k^2=0`; the
remaining roots of `A_2`, and the ordinary weight endpoints, are covered by
their previously certified exact packages.

## The `A_0` quadratic companion

Let

```text
L=Q(s)/(4s^2-2s-3).
```

Modulo this relation, the nonzero factor of `N=lambda(A_2 lambda+A_1)` is

```text
lambda=-A_1/A_2=5,                                 (7)
```

and

```text
k^2=2-4s/3,  Norm_L/Q(k^2)=4/3.                   (8)
```

The polynomial defining `L` has nonsquare discriminant `52`.  Since `4/3`
is not a square in `Q`, (8) cannot be a square in `L`; hence

```text
E=L[k]/(k^2-2+4s/3)
```

is a degree-four field.  The new verifier and its no-import audit solve the
binary section over all of `E`, with no coefficient splitting.  The opposite
binary diagonal has norm

```text
369603/722500,                                     (9)
```

and the four fixed paired-`D23` minor norms are

```text
26343021246347/14905090843200000000,
-678776825335896383697/2471687065600000000,
-13286015627108474691/603439225000000,
198869809598195970789/154480441600000000.          (10)
```

All five values are nonzero.  Thus this final ordinary denominator fibre is
a genuine binary false positive, obstructed in every paired marked mode.

## Replay

Replay the strengthened slice calculation:

```text
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_generic_false_positive.py

uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_generic_false_positive.py
```

Then replay the quadratic companion fibre:

```text
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_a0_quadratic_companion_obstruction.py

uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_a0_quadratic_companion_obstruction.py
```

The primary uses subset-DP permanents for the transcendental slice and
permutation permanents for the companion fibre; both use direct determinant
expansion.  The audits swap these choices and use recursive cofactor
determinants.  All calculations are exact over characteristic zero.  No
finite-field evidence is used.
