# Component twenty-five's sparse paired-`D23` `w=0` obstruction

## Status

**Exact characteristic-zero finite-branch theorem.**  Retain component
twenty-five's normalized ordinary finite-`D01`, `B=0`, `N=0` sheet and all
open conditions of the sparse paired-`D23` cover, in particular

```text
G != 0,  A_0 A_2 != 0.
```

On the remaining divisor

```text
w=0,
```

the mode-one paired finite-`D23` one-marked coefficient map has rank four.
It therefore cannot have the rank at most three required by weighted `H22`.

Together with the sparse two-minor cover and its non-`w` companion, this
closes every alternative in that cover on the retained ordinary sheet.  It
does **not** treat the standing, chart, linear-solve, opposite-diagonal, or
projective boundaries excluded by those packages.  It is not a
counterexample.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Sparse cofactor frame

Normalize `s=1`, write `a=es`, `b=js`, and put

```text
Q=a+b,                 R=1+ab,
P=Q^2/R,               k^2=P-ab,
D=(lambda-1)P-(lambda+1)Q,
H=(lambda+1)R-(lambda-1)Q,
D_0=a^2b^2-a^2-ab-b^2=-Rk^2,
z_3=1/(2PD).
```

The rank of a one-marked map is unchanged by replacing any unmarked binary
row pair by another basis of the same two-plane.  Use the sparse pairs from
the prerequisite cover.  Only modes `0,2,3` occur in the cofactor rows for
the mode-one map, and on `w=0` the needed rows are

```text
mode 0: (beta_0, alpha_0-Q beta_0)
       =((1,1,0,0),(0,0,-P(lambda+1),v_0)),

mode 2: (alpha_2,beta_2)
       =((1,-1,0,0),(1,1,a(lambda+1)-k(lambda-1),z_6)),

mode 3: (alpha_3,beta_3)
       =((0,0,lambda-1,z_3),
         (1-b,1+b,b(lambda+1),z_7)),
```

where

```text
v_0=k y_0,
y_0=[P^2 z_3-1/(2(lambda-1))]/(Q k^2).
```

The coordinates `z_6,z_7` are left arbitrary.  Thus the obstruction does
not use a hidden solution formula for the residual binary section.

## Exact rank-four minor

For three-bit words in modes `(0,2,3)`, take the cofactor rows

```text
010, 100, 110, 111.
```

Expanding the four `3 x 3` permanental cofactor rows and their `4 x 4`
determinant gives

```text
delta_1=8 X_-^2 X_+,

X_- =P(lambda+1)z_3-(lambda-1)v_0,
X_+ =P(lambda+1)z_3+(lambda-1)v_0.                 (1)
```

Conjugation in the quadratic component algebra sends `k` to `-k`, hence
interchanges `X_-` and `X_+`.  Their common norm is

```text
Norm(X_-) = Norm(X_+)

 =(a-1)(a+1)(b-1)(b+1)(lambda+1)^2 R^2
   ------------------------------------------------.                 (2)
             4 Q^2 D_0 H^2
```

Every denominator in (2) is already inverted on the retained ordinary
chart.  Moreover `A_0 A_2 != 0` implies

```text
(a-1)(a+1)(b-1)(b+1) != 0,
```

because `A_0` contains `(a-1)(b+1)` and `A_2` contains
`(a+1)(b-1)`.  The standing chart also has `lambda+1 != 0` and `R != 0`.
Thus (2) is nonzero, so both `X_-` and `X_+` are nonzero in the quadratic
field.  Equation (1) proves `delta_1 != 0` and the mode-one map has rank
four.

An independent audit uses the different row set

```text
010, 100, 101, 110
```

and obtains `-8b X_-^2 X_+`; the additional factor `b` is also a retained
unit.

## Scope and replay

This theorem assumes the same normalized ordinary chart as its two
prerequisites.  In particular it does not extend through zeroes of

```text
P R k Q (a-b)(a^2-k^2)(lambda^2-1),
H, a, b, lambda, T, A_0, A_2, G,
```

or through any denominator used to obtain the sparse frame.  Projective
fibres and the already-separated zero-diagonal locus remain outside the
claim.

Run:

```text
uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b/verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_d23_w_zero_obstruction.py

uv run --with sympy python \
  claims/p5/h22/unequal-endpoint-inward-star-component-finite-d01-branch-b/audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_exceptional_weight_d23_w_zero_obstruction.py
```

The primary expands permanents by permutations and uses a direct exact
determinant.  The no-import audit evaluates permanents by subset dynamic
programming and its determinant by recursive cofactors.  Both work over
exact characteristic zero.  No finite-field evidence is used.
