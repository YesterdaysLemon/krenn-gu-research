# Full-field obstruction on the finite-`D01` `B` branch at `T=0` and `H=0`

## Status

**Exact characteristic-zero special-weight theorem.**  On component
twenty-five's normalized ordinary finite-`D01` `B=0` branch, the retained
linear weight divisor

```text
T=(js-1)lambda-(js+1)=0                             (1)
```

is empty.  The denominator boundary

```text
H=(lambda+1)R-(lambda-1)sQ=0                        (2)
```

is also empty in the ordinary chart.  Both statements allow the free
extension coordinates to take arbitrary values in the full quadratic
component field; no `1,k` coefficient splitting is used.

The quadratic exceptional divisor `N=0`, the other determinant divisors,
and the standing component-chart boundary remain separate.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## Exact `T=0` reduction

Put

```text
P=ej+k^2,       Q=e+j,       R=1+ejs^2,
F=PR-Q^2,
K=C(e,j,s)[k]/(F),
D_0=e^2j^2s^2-e^2-ej-j^2=-Rk^2.
```

Equation (1) gives

```text
lambda=(js+1)/(js-1).                               (3)
```

The denominator `js-1` cannot vanish on `T=0` in characteristic zero.  At
the weight (3), direct simplification gives

```text
H=2es(js+1),
(lambda-1)sP-(lambda+1)Q=-QH/R.                     (4)
```

Use the original `B` equation

```text
2P((lambda-1)sP-(lambda+1)Q)z_3-s=0.                (5)
```

On a hypothetical ordinary candidate, (4)--(5) make `H` nonzero and give

```text
z_3=s/[2P((lambda-1)sP-(lambda+1)Q)].               (6)
```

Retain completely arbitrary elements

```text
w=w_0+w_1k,       z_6=z_60+z_61k                    (7)
```

of `K`, and recover `z_0,z_1,z_5,z_7` from the four forced extension
equations.  Exact reconstruction of the permanent tensor then makes the
first residual Segre minor independent of all four parameters in (7):

```text
S_13=C_0101 C_0000-C_0100 C_0001
    = k j Q R/[e(js-1)(js+1)D_0].                  (8)
```

Every factor in (8) is a unit on a hypothetical standing-chart candidate.
Indeed `j=0` or `s=0` would make (1) the excluded endpoint `lambda=-1`;
`js=1` is incompatible with `T=0`; and `e=0` or `js=-1` makes `H=0`, which
is excluded directly below.  Finally `D_0=-Rk^2`, while `Q,R,k` are standing
chart units.  Thus (8) cannot vanish, proving the `T=0` obstruction over the
full field `K`.

## The `H=0` boundary

The identity in (4) before specializing `T` is

```text
(lambda-1)sP-(lambda+1)Q=-QH/R.                    (9)
```

If `H=0`, equation (5) reduces to `-s=0`.  Setting `s=0` in (2) gives

```text
H=lambda+1.
```

Hence `H=0` forces `lambda=-1`, already outside the ordinary chart
`lambda^2!=1`.  This argument uses the original denominator-free `B`
equation and therefore loses no point by division through `H`.

## Boundaries and replay

The standing chart is

```text
P R k Q (e-j)(e^2-k^2)(lambda^2-1) != 0.
```

This package closes only (1)--(2).  It does not classify

```text
e=0, j=0, s=0, lambda=0, N=0
```

away from their intersections with the two closed loci, nor any projective
component boundary.

Run:

```text
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_t_zero_and_h_boundary_obstruction.py

uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_t_zero_and_h_boundary_obstruction.py
```

The primary expands permanents by permutations in the quadratic field with
the four free scalar parameters (7).  The no-import audit reconstructs the
same tensor by subset dynamic programming.  Both verify (4), (6), and (8)
exactly over characteristic zero.  No finite-field evidence is used.
