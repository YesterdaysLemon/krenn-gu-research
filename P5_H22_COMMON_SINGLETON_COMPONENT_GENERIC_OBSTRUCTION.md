# A Hall-deficiency obstruction to weighted `H22` on component eighteen

## Status

This note proves an exact characteristic-zero generic-fibre theorem for the
common-singleton pure-`P_4` component constructed in
`P4_COMMON_SINGLETON_COMPONENT.md`.  Its complete weighted marked-basis
`H22` fibre is empty on the dense component chart.

The obstruction occurs before any mixed-coefficient or ternary-rank
calculation.  In the intrinsic pure marking, three kernel rows are the same
singleton.  Under either weighted `H22` source contraction, their extended
images use at most two target channels.  Hall deficiency then makes the
all-kernel `4 x 4` permanent identically zero.  Hence neither contraction can
be a genuine binary `Delta_2` neighbour.

The proof is simultaneous in every affine marking, every fifth-coordinate
extension, every source diagonal scaling, and every homogeneous merge weight,
including both projective slope endpoints.  No search, specialization,
elimination, or finite-field inference is used.

## The intrinsic common-singleton marking

Write

```text
e=(1,0,0,0),
ell=(0,1,L,M),
v1=(0,1,a,b),
v2=(0,1,c,d),
```

where

```text
d=-(L*b+M*a+M*c+b*c)/(L+a).
```

Let `B_ell` be the ternary polar matrix

```text
B_ell=[[0,M,L],[M,0,1],[L,1,0]],
```

and obtain `v3=(0,w3)` by normalizing

```text
w3=(B_ell*(1,a,b)) cross (B_ell*(1,c,d)).
```

On the dense open where the displayed normalizations and the pure coefficient
below are nonzero, orient the four plane bases as

```text
alpha_0=ell,       beta_0=e,
alpha_1=e,         beta_1=v1,
alpha_2=e,         beta_2=v2,
alpha_3=e,         beta_3=v3.                       (1)
```

The common-singleton component identities say

```text
T_w=0 for w!=1111,
T_1111=kappa=per(e,v1,v2,v3)!=0.                   (2)
```

For example, at `(L,M,a,b,c)=(-3,-2,-1,-1,-1)` one has

```text
d=2,       v3=(0,1,3,-1),       kappa=4.
```

The kernel lines in modes `1,2,3` are therefore all `C e`.  Every affine
marking of the same pure tensor has the form

```text
beta_i(h_i)=beta_i+h_i alpha_i.                    (3)
```

This changes none of the four `alpha_i` and preserves (2).

## Both homogeneous weighted contractions

Restore arbitrary diagonal source scalings `s_0,s_1,s_2,s_3`.  For
homogeneous weights `(lambda:mu)`, the first weighted direction is

```text
D_01^(lambda:mu)(z,x)=
 (lambda*s_0*z_0+mu*s_1*z_1, s_2*z_2, s_3*z_3, x). (4)
```

For homogeneous weights `(nu:omega)`, the opposite direction is

```text
D_23^(nu:omega)(z,x)=
 (s_0*z_0, s_1*z_1, nu*s_2*z_2+omega*s_3*z_3, x). (5)
```

Append arbitrary extension entries `x_i` to the kernel rows.  Their exact
images in direction `01` are

```text
A_0^01=(mu*s_1, s_2*L, s_3*M, x_0),
A_i^01=(lambda*s_0, 0, 0, x_i),       i=1,2,3.     (6)
```

In direction `23` they are

```text
A_0^23=(0, s_1, nu*s_2*L+omega*s_3*M, x_0),
A_i^23=(s_0, 0, 0, x_i),               i=1,2,3.   (7)
```

Independent rescaling of any `alpha_i` only rescales the corresponding
nonextension entry in (6)--(7), so it does not change the support argument.

## The Hall-deficient diagonal

In either (6) or (7), the three rows `A_1,A_2,A_3` are supported on the same
two columns: the first target channel and the extension channel.  A nonzero
monomial in a `4 x 4` permanent would have to assign these three rows to three
distinct columns.  This is impossible because their column neighbourhood has
cardinality two.  Equivalently, every one of the twenty-four permanent
summands contains a zero entry.  Therefore

```text
per(A_0^01,A_1^01,A_2^01,A_3^01)=0,
per(A_0^23,A_1^23,A_2^23,A_3^23)=0                 (8)
```

as polynomial identities in all family, marking, source-scaling, merge, and
extension variables.  Notice that neither the entries of `A_0` nor any mixed
equation are needed.  A mode relabeling merely permutes the four rows; the
three-row Hall-deficient subset, and hence (8), survives on every orbit
representative.

The left sides of (8) are the all-alpha, or all-kernel, binary diagonal
coefficients.  A genuine binary `Delta_2` restriction in a marked basis
requires both its all-alpha and all-beta diagonal coefficients to be nonzero.
Thus each weighted contraction already fails at the binary level.  The
`H22` local reduction allows both weighted neighbours to be pure but requires
at least one of them to be genuinely binary.  Here neither is genuine, so the
complete generic weighted `H22` fibre over component eighteen is empty.

## Scope of the theorem

The support identity (8) is stronger than a generic calculation and remains
valid on every specialization for which (1) is still the intrinsic pure
marking.  The theorem is stated generically because when `kappa=0`, a family
normalization denominator vanishes, or one passes to an omitted projective
component boundary, the pure tensor and its kernel marking may change and
must be classified separately.

Together with the existing componentwise results, this closes the generic
weighted `H22` fibre on all eighteen currently certified pure-`P_4`
component orbits.  The companion support obstruction closes component
eighteen's marked `H31` fibre:
[`P5_H31_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md).
The remaining all-pair-rank cells, component exhaustiveness, special `P_5`
fibres, contraction/gluing to the graph problem, and the global Krenn--Gu
conjecture remain open.

## Replay

Run

```text
uv run --with sympy python \
  verify_p5_h22_common_singleton_component_generic_obstruction.py

python audit_p5_h22_common_singleton_component_generic_obstruction.py
```

The primary verifier reconstructs the rational component chart, checks the
pure marked tensor at the generic point and the integral sample, constructs
both homogeneous weighted contractions, and verifies (8) symbolically and
summand by summand.  The independent audit imports no primary code or external
package and uses exact rational arithmetic, a tiny sparse-polynomial
subset-dynamic-program permanent, and the explicit Hall neighbourhood.
