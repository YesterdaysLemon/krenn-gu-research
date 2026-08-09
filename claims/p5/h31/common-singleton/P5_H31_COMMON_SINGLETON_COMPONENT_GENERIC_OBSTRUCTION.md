# The common-singleton component has no generic marked `H31` lift

## Status

**Exact characteristic-zero generic-fibre obstruction.**  Over the function
field of the common-singleton component, every marked basis and every choice
of distinguished source coordinate has an identically zero binary diagonal.
Consequently the generic marked `H31` fibre over component eighteen is empty.

The obstruction occurs before the fourteen mixed binary equations, so it
requires neither elimination nor a Fitting cover.  This theorem closes the
generic `H31` fibre only; the companion Hall argument closes weighted `H22`:
[`P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md`](../../h22/common-singleton/P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md).
Neither theorem classifies the component's projective boundary, closes
special fibres of the universal `P_5` incidence, or proves the
arbitrary-order conjecture.

## The generic component point and its complete marking fibre

Work over the function field

```text
K=C(L,M,a,b,c)
```

subject to the dense-open conditions in
[`P4_COMMON_SINGLETON_COMPONENT.md`](../../../p4/classifications/P4_COMMON_SINGLETON_COMPONENT.md).  Put

```text
e=(1,0,0,0),
ell=(0,1,L,M),
v1=(0,1,a,b),
v2=(0,1,c,d),

d=-(L*b+M*a+M*c+b*c)/(L+a),
```

and let `v3` be the normalized vector from that component chart.  The four
planes are

```text
U0=span(e,ell),       Ui=span(e,vi),  i=1,2,3.       (1)
```

Their pure restriction has the single nonzero coefficient

```text
kappa=per(e,v1,v2,v3)=P3(v1,v2,v3) != 0.            (2)
```

Use kernel rows and pure-colour rows

```text
alpha_0=ell,          u_0=e,
alpha_i=e,            u_i=vi,       i=1,2,3.         (3)
```

Then the only nonzero binary coefficient is `uuuu=kappa`.  Because this
nonzero rank-one tensor determines its kernel line in each mode, every
marked basis over the same four planes is, up to nonzero row rescaling,

```text
beta_i=u_i+h_i*alpha_i,       h_i in K.              (4)
```

Thus the four parameters `h_0,...,h_3` cover the complete affine Borel
marking fibre, rather than one selected row basis.  Exchanging the two
binary target colours only swaps the names of the two diagonals below; the
same zero-diagonal obstruction remains.

## Binary extension after a source-coordinate deletion

Fix a distinguished source coordinate `q` in `{0,1,2,3}`.  Delete `q`,
append the fifth source coordinate `f`, and write the eight new entries as

```text
z=(x_0,x_1,x_2,x_3;y_0,y_1,y_2,y_3)^T.              (5)
```

Let `M_q(h)z` be the fourteen mixed binary coefficients, and let
`A_q(z),B_q(h;z)` be the all-kernel and all-pure-colour diagonals.  The
standard marked-basis incidence criterion is

```text
M_q(h)z=0,             A_q(z) B_q(h;z) != 0.         (6)
```

This is necessary for a genuine binary `Delta_2` neighbour and hence for an
`H31` lift.

## The all-kernel diagonal vanishes identically

After the deletion and extension, the kernel rows are

```text
alpha_i^(q)=(projection away from q of alpha_i, x_i).
```

For `i=1,2,3`, equation (3) gives `alpha_i=e`.  Therefore:

- if `q=0`, the three rows `alpha_1^(q),alpha_2^(q),alpha_3^(q)` are all
  supported on the single appended coordinate `f`;
- if `q` is `1`, `2`, or `3`, those same three rows are supported on only
  the two coordinates `{e,f}`.

Every monomial in a `4 x 4` permanent assigns distinct columns to its four
rows.  Three rows supported on at most two columns cannot all receive
distinct nonzero columns.  Hence, independently of `alpha_0`, the extension
entries, the component parameters, and the marking shifts,

```text
A_q(z)=per(alpha_0^(q),alpha_1^(q),
           alpha_2^(q),alpha_3^(q))=0

for q=0,1,2,3.                                       (7)
```

Equation (7) contradicts the nonvanishing requirement in (6) before the
mixed equations are considered.  No marked basis over the generic
common-singleton point has a binary neighbour, so none lifts to `H31`.

## Scope

The result is simultaneous in all four marking parameters and all four
distinguished coordinates.  Since no denominator is introduced in (7), the
same support obstruction also applies to any nonzero common-singleton chart
point for which (2)--(4) remain valid.  No claim is made about other
projective boundary presentations of component eighteen.

## Replay

```text
uv run --with sympy python claims/p5/h31/common-singleton/verify_p5_h31_common_singleton_component_generic_obstruction.py
python claims/p5/h31/common-singleton/audit_p5_h31_common_singleton_component_generic_obstruction.py
```

The primary verifier reconstructs the rational component chart and its
complete symbolic marking fibre, expands all sixteen pure coefficients, and
checks all four binary extension matrices.  The independent audit rebuilds
the deleted-coordinate permanents directly and exhausts their permutation
monomials without importing the primary verifier.
