# Descent-only diagnostic on component twenty-five's finite-`D01` `B` branch

## Status

**WITHDRAWN AS A GENERIC OBSTRUCTION; VERIFIED IDENTITIES ONLY.**  The exact
quadratic-field calculations below verify a useful set of permanent and
resultant identities.  They do **not** prove that every binary candidate on
the normalized ordinary finite-`D01`, `B=0` sheet lies over

```text
e j s (e^2 s^2-1)(j s+1)=0.                         (1)
```

The original inference incorrectly split one equation into its coefficients
in the basis `1,k` while the free extension coordinates `w,z_6` may themselves
be `K`-valued.  Those two coefficients need not vanish separately at a
`K`-point.  Thus (1) is only a descent-restricted diagnostic, the full `B`
branch remains **UNKNOWN**, and the global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Exact reduction

Put

```text
P=ej+k^2,       Q=e+j,       R=1+ejs^2,
F=PR-Q^2,
K=C(e,j,s)[k]/(F).
```

The preceding finite-`D01` residual certificate gives

```text
z_2=(lambda-1)w,             z_4=-(lambda+1)w
```

and solves the four forced mode-zero equations for `z_0,z_1,z_5,z_7`.
The factor `B=0` is

```text
2P((lambda-1)sP-(lambda+1)Q)z_3-s=0.
```

On its ordinary generic chart this gives

```text
z_3=s/[2P((lambda-1)sP-(lambda+1)Q)].                (2)
```

Define

```text
H=(lambda+1)R-(lambda-1)sQ,
T=(js-1)lambda-(js+1),
D_0=e^2j^2s^2-e^2-ej-j^2=-Rk^2,

U=s^2(e^2j^2s^2-e^2-j^2),
G=U(lambda-1)^2+4ej lambda s^2+(lambda+1)^2.
```

Here `((lambda-1)sP-(lambda+1)Q)=-QH/R`.  Reconstructing the
four-row permanent tensor and reducing the fixed-vertex Segre minor

```text
S_13=C_0101 C_0000-C_0100 C_0001
```

in the basis `1,k` of `K` gives

```text
[S_13]_1 =
  2Q^3(lambda-1)((lambda+1)w+z_6)T/(RH),

[S_13]_k = jRG/(D_0 H^2).                            (3)
```

If one imposes the additional, unjustified descent restriction that the two
coefficients in (3) vanish separately, then `G=0`.  On `T != 0`, that same
restricted calculation also gives

```text
z_6=-(lambda+1)w.                                    (4)
```

After (4), the next Segre minor has exact coefficients

```text
[S_23]_1 =16ej lambda s^2 w Q^4/R^2,

[S_23]_k =
  2ej^2s(es-1)(es+1)RT/(D_0H).                       (5)
```

Away from `ejs(e^2s^2-1)=0`, the second coefficient in (5) is nonzero because
this case has `T != 0`.  This excludes only solutions satisfying the extra
coefficientwise descent condition; it does not exclude arbitrary `K`-valued
extension coordinates.

It remains to inspect `T=0`, where (4) was not used.  Since `T` is linear in
`lambda`, direct evaluation gives the denominator-cleared resultant identity

```text
(js-1)^2 G((js+1)/(js-1))
  =4 e s^2 Q (js-1)(js+1).                            (6)
```

On the standing ordinary chart, simultaneous vanishing of `T` and `G`
therefore forces `e(js+1)=0`; the factors `j=0` and `s=0` are already retained
in (1).  Combining the two cases proves the displayed cover only inside the
descent-restricted coefficientwise locus.

For reference, `G` also splits over `K`.  With

```text
a_0=U+1=(1-e^2s^2)(1-j^2s^2),
V=-U+2ejs^2+1,
```

one has

```text
a_0G=(a_0 lambda+V-2sRk)(a_0 lambda+V+2sRk).          (7)
```

No division by `a_0` is used in the obstruction; (7) records its special
base boundary honestly.

## Invalid inference, boundaries, and replay

In the polynomial ring `K[w,z_6]`, an equation

```text
a(w,z_6)+k b(w,z_6)=0
```

is one equation over `K`.  Although `1,k` are linearly independent over the
base field, a `K`-valued assignment to `w,z_6` can make the two displayed
terms cancel.  Splitting it into `a=b=0` silently restricts the coordinates to
the base field.  No descent theorem justifies that restriction here.

The calculation retains the standing affine-chart localization

```text
P R k Q (e-j)(e^2-k^2)(lambda^2-1) != 0.
```

Equation (2) also localizes at `H`.  If `H=0`, the original `B` equation
forces `s=0`, but this does not repair the invalid coefficient split on the
`H!=0` chart.  The full `B` branch, its special-base fibres, and the standing
chart boundary all remain open.

Run:

```text
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_reduction.py

uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_b_reduction.py
```

The primary verifier expands permanents by permutations in the quadratic
function field.  The audit imports no project code, independently rebuilds
the tensor, and evaluates permanents by subset dynamic programming.  Both
verify (2)--(7) exactly over characteristic zero and explicitly deny the
generic-empty conclusion.  No finite-field evidence is used.
