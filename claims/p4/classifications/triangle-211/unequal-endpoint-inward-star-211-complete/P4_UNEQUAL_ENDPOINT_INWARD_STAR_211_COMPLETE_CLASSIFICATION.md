# Complete unequal-endpoint two-inward star `(2,1,1)` classification

## Status

**Exact characteristic-zero orientation-classification theorem.**  Every
nonzero pure point in the star `(2,1,1)` cell with two genuinely inward
rank-one spokes and distinct center endpoints either lies on component
twenty-five or has a pair rank at most two.  The complete projective
disjoint-binary leaf directions are included.  Overlapping and
binary/singleton support cannot produce another genuine two-inward all-pair
point.

Together with the outward, mixed-center, and equal-endpoint theorems, this
completes the entire star `(2,1,1)` cell.  The star `(1,1,1)` cell, generic
`P_5` fibres on component twenty-five, special/projective fibres, and the
arbitrary-order local-to-global step remain open.  The Krenn--Gu conjecture
remains **UNRESOLVED**.

## Universal inward normal form

Let `u,v` be the two distinct center relation factors and let `u^perp,v^perp`
be their squarefree polar partners.  The rank-two synchronizer has the same
exact syzygy normal form as in the mixed-center theorem:

```text
U_0=<u,v>,
U_1=<u+k v^perp,v+s u^perp>,
U_2=<u^perp,a>,
U_3=<v^perp,g>.                                    (1)
```

If the common syzygy coefficient used in (1) vanishes, `r_01<=2`.
Genuine inwardness means both leaf relation factors kill the pure Segre
point while neither center factor does.  Hence only coefficients `T_ab11`
may survive, their `2 x 2` matrix has rank one, and both of its center rows
are nonzero.

The ordered supports of `u,v` again have exactly eight signatures.  The four
equal/contained-coordinate-plane signatures

```text
(1,1,0), (1,2,1), (2,1,1), (2,2,2)                (2)
```

put `U_0,U_1` in one coordinate two-plane and give `r_01<=2`.

## Overlapping binary supports

For

```text
u=(1,1,0,0),  u^perp=(1,-1,0,0),
v=(0,1,1,0),  v^perp=(0,1,-1,0),                  (3)
```

the two forbidden inward coefficients are

```text
T_0010=-2a_3(k+1),   T_1101=-2g_3(s-1).           (4)
```

The center-spoke product has rank at most two on `k=-1` and on `s=1`.
Off those divisors, (4) gives `a_3=g_3=0`, after which every coefficient
vanishes.  Thus overlap is zero or lower-pair.

## Binary/singleton supports

For binary kernel and disjoint singleton active endpoint, inward support
first gives `a_3=0`.  If `s!=0`, it also gives `g_3=0` and the tensor is zero.
At `s=0`, the remaining center matrix has the form

```text
[ B C ]
[ C 0 ].                                            (5)
```

Rank one forces `C=0`, leaving a Segre factor that vanishes on the singleton
center endpoint.  The spoke has changed to the already classified
outward/mixed boundary and is not genuinely two-inward.  Reversing the two
center roles gives the transpose situation: `g_3=0`, and the only exceptional
chart `k=0` has matrix `[[0,C],[C,E]]`, again forcing a center endpoint to
vanish.  Neither ordered binary/singleton signature yields a new inward
point.

## Disjoint binary supports and component twenty-five

Put `u=A,u^perp=C,v=B,v^perp=D` and retain both complete projective leaf
directions:

```text
U_2=<C,aA+cC+eB+fD>,
U_3=<D,gA+hC+jB+nD>.                               (6)
```

The two forbidden coefficients give exactly

```text
f=-ak,  h=-js.                                     (7)
```

The surviving center matrix is four times

```text
[ ej+agk^2   aj+eg       ]
[ aj+eg      ag+ejs^2    ].                        (8)
```

It has rank one exactly on the bihomogeneous hypersurface

```text
(ej+agk^2)(ag+ejs^2)-(aj+eg)^2=0.                 (9)
```

The Borel coefficients `c,n` disappear.  On the dense leaf chart `a=g=1`,
(9) is precisely the irreducible component-twenty-five equation proved in
[`P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPONENT.md`](../../star/unequal-endpoint-inward-star-211/P4_UNEQUAL_ENDPOINT_INWARD_STAR_211_COMPONENT.md).
Equation (9) is not divisible by `a` or `g`, so its projective closure also
contains both omitted leaf hyperplanes and has no extra boundary component.
For example `(a,e,g,j,k,s)=(1,1,0,1,2,1)` is a pure all-pair point with
profile `(3,3,3,4,4,4)` on the `g=0` boundary.

This proves that component twenty-five is the sole all-pair orbit closure in
the unequal-endpoint inward orientation.

## Replay

```text
uv run --with sympy python claims/p4/classifications/triangle-211/unequal-endpoint-inward-star-211-complete/verify_p4_unequal_endpoint_inward_star_211_complete_classification.py
uv run --with sympy python claims/p4/classifications/triangle-211/unequal-endpoint-inward-star-211-complete/audit_p4_unequal_endpoint_inward_star_211_complete_classification.py
```

The primary verifier reconstructs all eight support signatures, every
forbidden coefficient, the two overlap rank drops, and the projective
hypersurface (9).  The no-import audit uses a subset-DP permanent, an
independent source permutation and unequal source scales, and the `g=0`
projective boundary point.  No finite-field output is used as proof.
