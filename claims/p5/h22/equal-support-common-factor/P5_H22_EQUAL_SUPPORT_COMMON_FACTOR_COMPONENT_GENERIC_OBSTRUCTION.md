# An exact-zero-divisor obstruction to weighted `H22` on the eleventh component

## Status

**Exact characteristic-zero generic-component theorem.**  The complete
weighted marked-basis fibre over the generic point of the equal-support
common-factor component is empty for `H22`.

In fact, one of the two required weighted binary neighbours already has zero
all-kernel diagonal for every fifth-coordinate extension, every marking,
every finite merge weight, and every diagonal source scaling in the displayed
normal-form chart.  No mixed equation, elimination, rank minor, or search is
needed.

At this checkpoint, ten of the eleven certified pure-`P_4` component orbits
were generically closed for weighted `H22`; the tenth component remained.
That final generic known-component fibre is subsequently closed by
[`P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](../two-rank-two-spoke-mixed-star/P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).

This theorem does not classify special pure-factor degenerations or the
projective boundary of the eleventh component, prove component
exhaustiveness, or resolve the global Krenn--Gu conjecture.

## The kernel rows

Put

```text
a=X_0+X_1,       a_bar=X_0-X_1,
b=X_2+X_3,       b_bar=X_2-X_3,
R=r+1,           Q=1+qR.                            (1)
```

For the component in
[`P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md`](../../../p4/classifications/P4_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT.md),
an intrinsic kernel/active marking is

```text
alpha_0=Q(a+p b)-pR(a_bar+q b)
       =(Q-pR,Q+pR,p,p),
alpha_1=a,
alpha_2=a,
alpha_3=b_bar.                                      (2)
```

The active rows may be shifted by arbitrary multiples of these rows, but the
kernel rows (2) do not change.  Thus the obstruction below is simultaneous
in the whole affine marking chart.

Restore an arbitrary diagonal source scaling

```text
diag(t_0,t_1,t_2,t_3)                               (3)
```

and let the weighted `01` neighbour merge the first two source coordinates
with arbitrary coefficients `(lambda,mu)`.  Adjoin fifth-coordinate entries
`x_i` to the four kernel rows.  In the target coordinates

```text
(lambda X_0+mu X_1, X_2, X_3, X_4),                 (4)
```

the four extended rows have the shape

```text
A_0=(*,                 p t_2, p t_3, x_0),
A_1=((lambda t_0+mu t_1),0,     0,     x_1),
A_2=((lambda t_0+mu t_1),0,     0,     x_2),
A_3=(0,                  t_2,  -t_3,   x_3).        (5)
```

The starred entry is irrelevant.

## The two-channel cut

Rows `A_1,A_2` are supported only in the merged and fifth channels.  Every
perfect matching contributing to the `4 x 4` permanent must therefore assign
those two rows to precisely those two channels.  Rows `A_0,A_3` must use the
remaining `X_2,X_3` channels.  Their residual permanent is

```text
per [[p t_2, p t_3],
     [  t_2,  -t_3]]

=p t_2(-t_3)+p t_3(t_2)=0.                         (6)
```

Consequently

```text
per(A_0,A_1,A_2,A_3)=0                              (7)
```

identically in all parameters and all extensions.

A binary `Delta_2` restriction in the marked basis requires both opposite
diagonal coefficients to be nonzero.  Equation (7) says that the all-kernel
diagonal of the weighted `01` neighbour is always zero.  Hence that neighbour
can never be binary `Delta_2`; a weighted `H22` lift, which requires both
weighted neighbours, is impossible.

The same identity covers zero or equal merge weights.  The projective
infinite-weight chart is obtained by interchanging which merge coefficient is
normalized, and (5)--(7) are homogeneous in `(lambda,mu)`, so no slope
divisor is omitted.

## Translation across the fence

Equation (6) is simultaneously three familiar objects:

```text
squarefree algebra:     b b_bar=0,
Fourier analysis on C2: trivial and sign characters cancel,
tensor-network cut:     two rows saturate two channels and leave a
                        zero two-channel transfer permanent.       (8)
```

The exact-zero-divisor language is the most informative one for this
component.  The pair `b,b_bar` is the second two-periodic block, dual to the
shared pair `a,a_bar` that created the component.  Holm's construction of
totally reflexive modules from exact zero divisors
([arXiv:1002.0419](https://arxiv.org/abs/1002.0419)) explains the periodic
homological shadow.  Here the extra weighted projection does not destroy the
annihilation: the channel cut isolates it as the literal scalar identity
(6).

## Honest frontier

The eleventh component is generically closed for both `H31` and weighted
`H22`.  The tenth component is subsequently closed by the fixed-vertex
Segre-join theorem linked above, so all eleven certified components are now
generically closed for both marked types.  The active fronts are special
parameter/projective boundaries and pure-`P_4` component exhaustiveness.
None of these finite component results is a global graph proof.

## Verification

Run:

```text
uv run --with sympy python claims/p5/h22/equal-support-common-factor/verify_p5_h22_equal_support_common_factor_component_generic_obstruction.py
uv run --with sympy python claims/p5/h22/equal-support-common-factor/audit_p5_h22_equal_support_common_factor_component_generic_obstruction.py
```

The primary verifier reconstructs the component's intrinsic marking, checks
its pure coefficient, restores symbolic source scalings and homogeneous merge
weights, and proves (5)--(7).  The independent audit imports no constructor
from the primary verifier; it uses a subset-dynamic-programming permanent,
independent row scalings, and the same arbitrary source and merge parameters.
Both are fixed-size symbolic identities, not searches.
