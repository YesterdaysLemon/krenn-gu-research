# Equal-endpoint two-inward star `(2,1,1)` obstruction

## Status

**Exact characteristic-zero orientation theorem.**  A nonzero pure `P_4`
compression in the star cell with relation ranks `(2,1,1)` and all pair
ranks at least three cannot have two genuinely inward rank-one spokes with
the same center endpoint.

Together with the subsequent complete unequal-endpoint theorem, this closes
the two-inward frontier and hence the full star `(2,1,1)` cell.  The star
`(1,1,1)` cell remains open.
The Krenn--Gu conjecture remains **UNRESOLVED**.

## Orientation test

Let the common center relation factor be `p`, and let the two leaf relation
factors be `q_2,q_3`.  If a nonzero multiplication tensor is the Segre tensor
`z_0 tensor z_1 tensor z_2 tensor z_3`, each rank-one pair relation gives

```text
(p dot z_0)(q_i dot z_i)=0.                         (1)
```

The spoke is genuinely inward when `p dot z_0!=0`, so (1) forces
`q_i dot z_i=0`.  In a leaf basis with `q_i` first, every tensor coefficient
having leaf bit zero must therefore vanish.  Both leaves being inward means
only coefficients `T_ab11` may survive.

Every nonzero linear zero divisor in the squarefree algebra has support one
or two, so the established center normal-form reduction leaves the following
exhaustive cases.

## Support one

Normalize

```text
p=X_0,  U_0=<p,X_1+X_2>,
U_1=<p+tau(X_1-X_2),nu p+X_1+X_2>,
U_2=<p,a>,  U_3=<p,g>.                              (2)
```

The two forbidden coefficients are

```text
T_1101=2g_3,   T_1110=2a_3.                        (3)
```

After (3) vanishes, every `T_ab11` vanishes too.  Thus genuine inward support
forces the zero tensor.

## Binary support with nonsingular complement

Put `p=A`, `p^perp=C`, and write the other center row as
`alpha C+E`, where `E=bB+dD` and `Q=b^2-d^2`.  Both the `alpha=0` syzygy
chart and the `alpha!=0` chart have the fixed forbidden coefficient

```text
T_1100=-4Q.                                         (4)
```

It is nonzero on `Q!=0`, contradicting the inward support requirement.

## Singleton complement

When `Q=0`, normalize `E` to a singleton.  On the `alpha=0` chart take

```text
U_0=<A,E>,  U_1=<uA+wE,sC+uE>.                     (5)
```

If `s=0`, the center-spoke product has rank at most two.  Otherwise

```text
T_1101=-2s g_3,   T_1110=-2s a_3                  (6)
```

force `a_3=g_3=0`, after which the entire tensor is zero.

On the `alpha!=0` chart the exact center-spoke minor is

```text
-16(s+u)(u-v)(u+v).                                (7)
```

All-pair rank three makes every factor in (7) nonzero.  The forbidden
coefficients are now `-4(s+u)g_3` and `-4(s+u)a_3`, so the same zero-tensor
conclusion follows.  The remaining case `E=0` was already lower-pair in the
center normal-form theorem.  This exhausts the support-one and support-two
possibilities for `p`.

## Replay

```text
uv run --with sympy python claims/p4/classifications/star/equal-endpoint-inward-star-211-obstruction/verify_p4_equal_endpoint_inward_star_211_obstruction.py
uv run --with sympy python claims/p4/classifications/star/equal-endpoint-inward-star-211-obstruction/audit_p4_equal_endpoint_inward_star_211_obstruction.py
```

The primary verifier reconstructs all coefficient identities and the rank
minor (7).  The independent audit uses a subset-dynamic-programming
permanent, then applies a source permutation and unequal source scales before
rechecking the forbidden coefficients and singleton branches.  No
finite-field output is used.
