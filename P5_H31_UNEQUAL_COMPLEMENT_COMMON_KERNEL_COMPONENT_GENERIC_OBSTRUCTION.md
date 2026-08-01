# Component twenty-two has no generic marked `H31` lift

## Status

**Exact characteristic-zero generic-component theorem.**  The complete
marked-basis `H31` fibre over the generic point of the unequal-complement
common-kernel component (component twenty-two) is empty.

This closes the generic `H31` side only.  The weighted `H22` fibre, special
component divisors, projective boundaries, the two star cells, and the global
Krenn--Gu conjecture remain separate and **UNRESOLVED**.

## Intrinsic marked rows

Use the first sheet from
[`P4_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT.md`](P4_UNEQUAL_COMPLEMENT_COMMON_KERNEL_COMPONENT.md),
over `K=C(A,R,D)`.  Put `s=2A+R` and

```text
alpha=(y_0,m,m_r,c),       beta^0=(x_0,a,a,d),
beta_i(h)=beta_i^0+h_i alpha_i.                    (1)
```

The rows are the exact ones in equations (15)--(17) of that component
theorem.  For each deleted source coordinate `q`, let `M_q(h)` be the
`14 x 8` mixed binary-extension matrix and let `d_0,d_1` be the two diagonal
rows.  A genuine binary neighbour requires

```text
M_q z=0,       d_0z*d_1z!=0.                       (2)
```

## Complete marking projection

Denominator-cleared elimination over `K` gives

```text
J_0=<h_2,h_1,
     8Ds h_0-2(D+1)h_3+(5-3D)s,
     4(h_3+s/2)(h_3+(2A+3R)/2)>,

J_1=<2h_3-s,h_1,
     4D h_0-R(D+1)h_2+3-D,
     h_2(Rh_2+1)>.                                 (3)
```

For `q=2,3`, the all-kernel diagonal belongs to the polynomial row module
of `M_q`; each reduced module has ten generators.  Hence only four marking
branches remain, two for each of `q=0,1`.

## Four survivor kernels and one uniform obstruction

Write every survivor kernel as `z=p e_0+w e_1`, with extension coordinates
ordered `(x_0,...,x_3;y_0,...,y_3)`.  The four markings are

```text
q0a: ((D-3)/(4D),0,0,-s/2),
q0b: ((A(D-3)-2R)/(2Ds),0,0,-(2A+3R)/2),
q1a: ((D-3)/(4D),0,0,s/2),
q1b: (-1/D,0,-1/R,s/2).                            (4)
```

The verifier records the exact bases.  In all four cases `d_1` is a nonzero
function-field multiple of `p`.  On `q0a,q0b,q1a`, the mode-three one-marked
minor on rows `0137` is, respectively,

```text
-2D d_0d_1p,       -2D d_0d_1p,       2D d_0d_1p. (5)
```

On `q1b`, rows `0237` give

```text
D d_0d_1p.                                         (6)
```

Thus (2) makes the one-marked mode-three map injective.  The pure
mode-three map retains the distinguished source coordinate with entry `D`.
The standard transverse-coordinate argument then forces the third target
row to vanish, contradicting the `H31` local rank requirement.

## Replay

```text
uv run --with sympy python verify_p5_h31_unequal_complement_common_kernel_component_generic_obstruction.py
uv run --with sympy python audit_p5_h31_unequal_complement_common_kernel_component_generic_obstruction.py
```

The primary replay proves the bidirectional elimination ideals, the two row
modules, all kernel bases, and all four minors over characteristic zero.  The
independent audit rebuilds the matrices at two rational component points.
No finite field is used.
