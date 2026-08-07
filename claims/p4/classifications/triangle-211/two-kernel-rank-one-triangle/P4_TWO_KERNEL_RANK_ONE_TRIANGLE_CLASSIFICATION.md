# Two kernel--kernel edges in a rank-one triangle are a component-eleven boundary

## Status

**Exact characteristic-zero classification of the two-double-edge
`triangle-(1,1,1)` stratum.**  Work over `C` in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Let `U_i=span(y_i,x_i)` be marked planes on which `P_4` restricts to a
nonzero pure tensor, with every pair image of rank at least three.  Suppose
the selected exceptional triangle on modes `1,2,3` has pair rank three and
three coefficient-rank-one relations, exactly two of which are
kernel--kernel.  After relabelling, write those two relations as

```text
y_1y_2=0,       y_1y_3=0.                          (1)
```

Then the tuple lies in the closure of component eleven.  More precisely,
up to source, mode, and marked-row symmetries, every survivor has the normal
form

```text
p=X_0+X_1,       q=X_0-X_1,
b=X_2+X_3,       b_bar=X_2-X_3,

U_0=span(b_bar,p),
U_1=span(p,b+alpha*q),
U_2=span(q,b+gamma*p),       gamma!=0,
U_3=span(q,p).                                      (2)
```

Its restriction is exactly `4*x_0*x_1*x_2*x_3`.  In mode order
`(3,0,1,2)`, formula (2) is the `p=0` boundary of the transitive rank-one
triangle family already placed in component eleven.  The divisor
`alpha=0` is the projective endpoint of the same family.

Together with the tournament classifications and the fully kernel--kernel
theorem, this leaves only the stratum with **exactly one** kernel--kernel
edge open inside `triangle-(1,1,1)`.  The two open star cells, the
`triangle-(2,1,1)` cell, special `P_5` fibres, and the global Krenn--Gu
conjecture remain unresolved.

That final stratum now has the finite, explicitly open normal-form ledger in
[`P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md`](../../../../../P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md);
the reduction does not yet place all six residual fibres in components.

## The two double edges force one genuine exact pair

For a nonzero linear zero divisor, the degree-one annihilator is one
dimensional.  Equation (1) therefore makes `y_2` and `y_3` proportional.
If their common line had square zero, it would be a singleton and
`y_2y_3=0` would be a third kernel--kernel relation.  Since the pair image
on edge `23` has one unique relation and this relation is not
kernel--kernel, that is impossible.

Thus `y_1` and the common line `y_2=y_3` are the two opposite directions of
a genuine binary exact pair.  Source scaling gives

```text
y_1=p=X_0+X_1,       y_2=y_3=q=X_0-X_1,
p q=0.                                               (3)
```

The third rank-one relation still has a kernel factor at one endpoint.
It cannot use both kernel rows.  The one-dimensional identity
`Ann_R1(q)=C*p` therefore makes one nonkernel factor proportional to `p`.
After swapping modes `2,3` and making a legal Borel shift,

```text
U_3=span(q,p).                                      (4)
```

Put `E=span(X_2,X_3)`.  Further Borel shifts give

```text
U_1=span(p,alpha*q+r_1),
U_2=span(q,beta*p+r_2),       r_1,r_2 in E.         (5)
```

Neither transverse row can vanish on the all-pair-rank locus: otherwise
one of the displayed planes equals `span(p,q)` and its product with `U_3`
has dimension at most two.

## Three forbidden cubics reduce to one binary determinant

Only three kernel-containing triple products from modes `1,2,3` can be
nonzero:

```text
p^2 r_2,       r_1 q^2,       (alpha*q+r_1)(beta*p+r_2)q.  (6)
```

The desired all-active cubic is

```text
(alpha*q+r_1)(beta*p+r_2)p.                         (7)
```

Write

```text
r_1=b_2X_2+b_3X_3,       r_2=d_2X_2+d_3X_3,
S=b_2d_3+b_3d_2,          Delta=b_2d_3-b_3d_2,      (8)
L_r(z)=r_2 z_3+r_3 z_2.
```

For `z=(z_0,z_1,z_2,z_3)`, the three forbidden covectors and the desired
covector are, up to harmless nonzero constants,

```text
F_1= 2L_(r_2),
F_2=-2L_(r_1),
F_3=-2alpha L_(r_2)-S(z_0-z_1),
X  = 2beta  L_(r_1)+S(z_0+z_1).                    (9)
```

The two possibly nonzero `3 x 3` minors of the forbidden-row matrix are

```text
 4 Delta S,       -4 Delta S.                      (10)
```

Suppose first that `r_1,r_2` are independent, so `Delta!=0`.  The first two
rows in (9) force any common two-dimensional annihilator to be
`span(X_0,X_1)`.  Equation (10) then forces `S=0`; but with `S=0`, the
desired row `X` also vanishes on that plane.  Hence the independent branch
has no nonzero pure restriction.

The only possible survivor has

```text
r_2=lambda*r_1,       lambda!=0.                   (11)
```

If `S=0`, the desired row belongs to the span of `F_1,F_2,F_3`, so the
restriction is again zero.  Nonzero purity consequently forces `r_1` to
have genuine support two.  Diagonal scaling and active-row scaling normalize

```text
r_1=b=X_2+X_3,       r_2=lambda*b,
b_bar=X_2-X_3.                                      (12)
```

Now the forbidden rows span exactly

```text
L_b(z)=z_2+z_3,       z_0-z_1.                     (13)
```

Their common annihilator is the unique plane

```text
U_0=span(p,b_bar).                                  (14)
```

The desired covector restricts to a nonzero multiple of `z_0+z_1` on this
plane.  Absorbing `lambda` into the active row and writing
`gamma=beta/lambda` gives exactly (2).  The pair-rank assumption forces
`gamma!=0`; if `gamma=0`, the image `U_0U_2` has rank two.

## Exact placement in component eleven

The survivor in
[`P4_TRANSITIVE_RANK_ONE_TRIANGLE_CLASSIFICATION.md`](../transitive-rank-one-triangle/P4_TRANSITIVE_RANK_ONE_TRIANGLE_CLASSIFICATION.md)
has planes

```text
V_0=span(p+u*b,q+v*b),
V_1=span(q,eta*p+b),
V_2=span(q,p),
V_3=span(b_bar,p).                                  (15)
```

For `alpha!=0`, set

```text
u=0,       v=1/alpha,       eta=gamma.              (16)
```

Then

```text
(U_0,U_1,U_2,U_3)=(V_3,V_0,V_1,V_2)               (17)
```

as ordered plane tuples.  The cited transitive theorem supplies an explicit
valuative arc from every tuple (15) into component eleven.

When `alpha=0`, use the same identity with `alpha=epsilon!=0` and let
`epsilon` tend to zero:

```text
span(p,b+epsilon*q) -> span(p,b).                  (18)
```

All other planes are fixed, so (18) closes the sole projective endpoint.
This proves component-eleven containment for the complete normal form (2).

## Exact replay

```text
uv run --with sympy python claims/p4/classifications/triangle-211/two-kernel-rank-one-triangle/verify_p4_two_kernel_rank_one_triangle_classification.py
python claims/p4/classifications/triangle-211/two-kernel-rank-one-triangle/audit_p4_two_kernel_rank_one_triangle_classification.py
```

The primary verifier reconstructs (6)--(10), proves the pure normal form,
checks its pair profiles, and identifies (17) symbolically.  The independent
audit imports nothing from the primary verifier: it uses exact rational
permanents and row reduction to check the independent, dependent, and
projective-endpoint branches.  The audit is corroboration; equations
(3)--(18) are the characteristic-zero proof.
