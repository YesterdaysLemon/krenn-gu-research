# Full-field generic-weight obstruction on component twenty-five's finite-`D01` `B` branch

## Status

**Exact characteristic-zero generic-weight theorem.**  Let

```text
F=(ej+k^2)(1+ejs^2)-(e+j)^2,
K=C(e,j,s)[k]/(F).
```

On the ordinary finite-`D01` branch `B=0`, the complete residual binary
system has no solution over `K(lambda)`.  Thus no component of this branch
dominates the ordinary weight line over the generic component point.

This theorem deliberately permits the extension coordinates `w,z_6` to take
arbitrary values in `K`.  It does **not** split a single equation into its
`1,k` coefficients.  The earlier coefficient-split calculation is only a
diagnostic for base-descending sections and is not evidence for arbitrary
`K`-valued fibres.

The theorem retains an explicit quadratic exceptional-weight divisor and
all singular determinant/chart divisors.  It therefore does not close the
complete `B` branch.  The generic weighted `H22` fibre of component
twenty-five and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Exact setup

Write

```text
P=ej+k^2,       Q=e+j,       R=1+ejs^2,
H=(lambda+1)R-(lambda-1)sQ,
T=(js-1)lambda-(js+1),
D_0=e^2j^2s^2-e^2-ej-j^2=-Rk^2.
```

The preceding residual certificate
[`P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D01_RESIDUAL_FACTOR_COVER.md`](P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D01_RESIDUAL_FACTOR_COVER.md)
gives

```text
z_2=(lambda-1)w,
z_4=-(lambda+1)w
```

and solves the four forced mode-zero equations for `z_0,z_1,z_5,z_7`.
Since

```text
(lambda-1)sP-(lambda+1)Q=-QH/R,
```

the equation `B=0` gives

```text
z_3=s/[2P((lambda-1)sP-(lambda+1)Q)].                (1)
```

The remaining binary equations are the three fixed-vertex Segre minors

```text
S_13 =C_0101 C_0000-C_0100 C_0001,
S_23 =C_0011 C_0000-C_0010 C_0001,
S_123=C_0111 C_0000^2-C_0100 C_0010 C_0001.          (2)
```

After (1), `S_13` and `S_23` are linear in `w,z_6` over the full quadratic
field `K(lambda)`.  Their exact coefficient determinant is

```text
Delta =
 -32 e j lambda s^2 Q^7 (lambda-1) T /(R^3 H).       (3)
```

On `Delta != 0`, solve this two-by-two system in `K(lambda)` itself.  The
solution is unique.  Substitution into the last equation gives

```text
S_123 =
 -k (lambda+1) R N
   /[Q(lambda-1)D_0 T H],                            (4)
```

where `N=A_2 lambda^2+A_1 lambda+A_0` and

```text
A_2=(es+1)(js-1)
    (3e^2j^2s^2+e^2js-e^2-ej^3s^2-2ej^2s-ej+j^3s),

A_1=-2
    (3e^3j^3s^4-2e^3js^2-e^2j^4s^4+e^2j^2s^2
     -e^2-ej+j^4s^2),

A_0=(es-1)(js+1)
    (3e^2j^2s^2-e^2js-e^2-ej^3s^2+2ej^2s-ej-j^3s).
                                                               (5)
```

The polynomial `N` is nonzero.  One short exact check is

```text
N(1)=-4eQ(js-1)(js+1).                              (6)
```

Consequently `N` is a unit in the weight function field `K(lambda)`, so (4)
is nonzero and the three-minor ideal is unit there.  This proves the stated
generic-weight obstruction.

## Retained divisors

The standing normalized affine chart already assumes

```text
P R k Q (e-j)(e^2-k^2)(lambda^2-1) != 0.             (7)
```

Equation (1) additionally uses `H != 0`.  If `H=0`, the original `B`
equation forces `s=0`, so that intersection must be handled without (1).

The linear solve (3) retains

```text
e=0,  j=0,  s=0,  lambda=0,  T=0                   (8)
```

as separate determinant divisors.  Finally, (4) retains the quadratic
exceptional-weight divisor

```text
N=0.                                                  (9)
```

The factors `es+/-1` and `js+1` appearing in the leading or constant
coefficients of `N` do not by themselves form a proved survivor cover.
Nothing on (7)--(9), including genuineness of the terminal section on
`N=0`, is claimed here.

## Replay

Run:

```text
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_full_field_generic_weight.py

uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_full_field_generic_weight.py
```

The primary verifier expands the four-row permanents by permutations.  The
audit imports no project code and reconstructs them independently by subset
dynamic programming.  Both solve the two linear minors inside the quadratic
field, verify (3)--(6), and use no finite-field evidence.  The earlier
[`B`-branch diagnostic](P5_H22_UNEQUAL_ENDPOINT_INWARD_STAR_COMPONENT_FINITE_D01_BRANCH_B_GENERIC_OBSTRUCTION.md)
remains withdrawn; its narrower cover is not used here.
