# Four-root torus-star equal-leaf H4 Q6-open low-rank exclusion

## Status and exact scope

**Exact scoped characteristic-zero theorem (`GLD90`).** Work over `Q` in the
displayed `H4` chart and extend scalars to `C`.  Put

```text
d0 = p+q-1,
P  = p^2-p+1,
L1 = p^2+2pq-2p-q,
L2 = 2pq-p+q^2-2q,
e  = 2pq^2-2pq-p-q^2-2q+2,
Delta = (p-q)d0 P L1 L2 e.                           (1)
```

Let `Q6` be the explicit common factor in (6) below.  On the complete
scale-fixed equal-leaf survivor chart,

```text
B intersect V(I_7(A)) intersect D(Omega Delta Q6) intersect H4 = empty. (2)
```

Thus, after the prior `GLD87` collision-divisor exclusion and `GLD89`
`P,d0` closure, the only retained `H4` boundaries of this low-rank lane are
`Q6=0` and the named `L1=0`, `L2=0`, or `e=0` coefficient boundaries.  The
theorem does not compute the pulled-back `GLD83` Fitting ideal and does not
cover other charts, gauges, components, source branches, profiles, roots, or
orders.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

The conclusion is set-theoretic over geometric points.  It is not a radical
ideal equality and is not a claim that every ambient point has syndrome rank
greater than six.  On the classified rank-six families, the contradiction is
instead that every compatible actual center is singular, whereas
`D(Omega)` contains the normalized `det(C)det(G)` gate.

## 1. Upstream bridge and H4 chart

Use the `GLD75` scale-fixed equal-leaf survivor base with common leaf frame

```text
G = [1  1       1      ]
    [p  q       s      ],
    [a  1+b     1+c    ]
```

and, on `H4` and `D(d0)`,

```text
s=(p+q-pq)/d0.                                       (3)
```

The fixed `37 x 9` `GLD71` syndrome matrix is `M(G)`.  The exact
`GLD75`/`GLD86` bridge says on `B`

```text
B=0 iff M(G)C=0,
rank A = rank M(G)[:,0:8],
C_8=1.                                               (4)
```

Consequently a point of `B intersect V(I_7(A))` has full syndrome rank at
most six: the ninth column is a combination of the first eight by (4).
Every seven-minor used below must therefore vanish.

`GLD88` already excludes the named old-six-pivot open on `D(Delta)`: two
bordered residuals force its rational family, all 111 block-kernel identities
hold, and the nonzero pivot makes the complete syndrome kernel three copies
of one row line.  GLD90 classifies the complementary old-pivot boundary on
`D(Q6)` and also closes the formerly exceptional `T=0` divisor.

## 2. The two raw six-pivots

Use columns

```text
S=(0,1,3,4,6,7)
```

and rows

```text
R0=(0,1,2,17,19,32),
R1=(0,1,17,19,28,32).                                (5)
```

The primary verifier reconstructs all 37 syndrome rows and factors the two
raw determinants exactly as

```text
det M[R0,S] = -6(p-q)^2 X0 Q6,
det M[R1,S] = -6(p-q)^2 X1 Q6,

X0 = a(p^2-1)-(b+1)(q^2-1),
X1 = ap(p-2)-bq(q-2)-p(p-2),

Q6 = 2p^4q^2-2p^4q+p^4
     +2p^3q^3-7p^3q^2+5p^3q-2p^3
     +2p^2q^4-7p^2q^3+12p^2q^2-7p^2q+2p^2
     -2pq^4+5pq^3-7pq^2+2pq
     +q^4-2q^3+2q^2.                                 (6)
```

On `D((p-q)Q6)`, the old-pivot boundary is exactly `X0=0`.  If
`X1!=0`, the alternate pivot is available.  Its bordered residuals at
`(25,5)` and `(31,5)` are linear in `b,c`; their coefficient determinant is

```text
-6 Delta.                                            (7)
```

They rederive exactly the `GLD88` rational family.  The upstream 111 kernel
identities and this nonzero alternate pivot give rank six with the complete
common-row kernel, so `det(C)=0`.

## 3. The double-pivot branch away from T=0

Suppose `X0=X1=0` and put

```text
T=2pq-p-q+2.                                         (8)
```

The coefficient determinant of these two equations in `a,b` is
`(p-q)T`.  On `D((p-q)T)` they force

```text
a=(q-1)(q+1)(p+q-2)/T,
b=p(p-2)(p+q)/T.                                     (9)
```

On (9), use the two auxiliary row charts

```text
RA=(0,1,2,17,19,25),
RB=(0,1,17,19,25,28).                                (10)
```

Their six-pivots factor as

```text
det M[RA,S]
 = -3(p-q)^3 d0 Q6 (p-1)(p+1)(q-1)(q+1)(p+q-2)/T,

det M[RB,S]
 =  3(p-q)^3 d0 Q6 p q(p-2)(q-2)(p+q)/T.             (11)
```

If the first pivot is nonzero, the bordered positions `(28,2)` and `(32,8)`
have resultant in `c`

```text
-6 L1 T L2 R.                                        (12)
```

If the second is nonzero, positions `(2,8)` and `(32,8)` give

```text
-6 p q(p-2)(q-2)(p+q)L1L2 R,                         (13)
```

where

```text
R = 2p^4q^2-2p^4q-p^4
    +2p^3q^3-7p^3q^2+p^3q+4p^3
    +2p^2q^4-7p^2q^3+6p^2q^2+5p^2q-4p^2
    -2pq^4+pq^3+5pq^2-4pq
    -q^4+4q^3-4q^2.                                  (14)
```

All factors outside `R` in (12)--(13) are nonzero on the active chart and
declared open, so rank at most six forces `R=0`.

Modulo `R`, the value of `b` in (9) agrees exactly with the `GLD88` family:

```text
b_double-b_GLD88 = (p-q)d0 R/(P T e).                 (15)
```

The two chart-A residuals and the two retained chart-B residuals vanish at
the same `c_GLD88` modulo `R`.  The anchor coefficient is `U V T`, where

```text
U=pq-p-q,
V=pq+p+q-2.                                          (16)
```

The possible failures are exact, not generic omissions:

```text
R|_(U=0) = -p^2(p-2)^2 P^2,
R|_(V=0) = 3p(p-2)(p^2+2)P^2.                        (17)
```

The `p=0,2` cases in (17) lie on already excluded factors.  On
`V=0,p^2+2=0`, chart A remains open and its backup `c` coefficient is
coprime to `p^2+2`; it therefore still forces `c=c_GLD88`.  This is the
correct exceptional chart check; no pivot from the vanishing chart B is
used.

The `GLD88` 111 common-kernel identities now apply, while the active
auxiliary pivot supplies rank exactly six.  Hence the compatible centers
again have proportional rows and are excluded by `D(Omega)`.

If both auxiliary pivots in (11) vanish, exact enumeration of their five by
five factor pairs on `D(Delta Q6 T)` leaves only

```text
(p,q)=(1,2), (-1,0), (2,1), (0,-1).                  (18)
```

At each point the primary reconstructs two or three explicit seven-minors
in the remaining coordinate `c`.  Their polynomial gcd is `1`, so at least
one seven-minor is nonzero for every `c`.  These four corners have syndrome
rank at least seven and cannot lie in `V(I_7(A))`.

## 4. The T=0 divisor

The apparent denominator in (9) is a closed branch, not a residual.  Since
`T` is linear in `q` and has no solution when `2p-1=0`,

```text
T=0  implies  q=(p-2)/(2p-1).                         (19)
```

On this divisor the verifier checks

```text
Q6 = 8P^4/(2p-1)^4,
p-q = 2P/(2p-1),
L1 = (p-2)(p+1),
L2 = -9p(p-1)/(2p-1)^2,
e  = -3(p-2)(p+1)/(2p-1).                            (20)
```

Thus `Q6!=0` automatically on `D(Delta)`.  The two pivot factors become,
up to the displayed nonzero factors,

```text
X0 = (p-1)(p+1)((2p-1)^2 a+3b+3)/(2p-1)^2,
X1 = p(p-2)((2p-1)^2(a-1)+3b)/(2p-1)^2.              (21)
```

The two bracketed expressions differ by

```text
4P.                                                   (22)
```

They therefore cannot vanish simultaneously on `D(Delta)`.  If `X0!=0`,
the prior GLD88 pivot and residual argument applies.  If `X0=0`, then
`X1!=0`; the alternate residual system (7) applies.  In either case the
forced family has the complete common-row kernel and every compatible center
is singular.  This closes the full `T=0` branch in (2).

The rational point

```text
p=3, q=1/5, a=48/1331, b=-1731/1331, c=-3/11
```

lies on `T=X0=0` with `X1 Delta Q6 det(G)!=0`.  Its exact syndrome rank is
six and its three blocks have common kernel

```text
(-81/1331, -1250/1331, 1).                           (23)
```

This confirms that the alternate-pivot `T` subcase is nonempty before the
center determinant gate; it is excluded by center singularity, not by an
ambient-rank assertion.

## 5. Residual table and non-claims

| locus | disposition after GLD90 on `H4 intersect D(Omega)` |
| --- | --- |
| old pivot nonzero | excluded by `GLD88` on `D(Delta)` |
| old pivot zero, `Q6 T!=0` | excluded here by alternate/auxiliary pivots, the exact `R` curve, or corner seven-minors |
| `T=0` | excluded here on `D(Delta)` by the two-pivot obstruction |
| `P=0` or `d0=0` | excluded separately by `GLD89` |
| `Q6=0` | retained |
| `L1=0`, `L2=0`, or `e=0` | retained |
| pulled-back `GLD83` Fitting ideal | not computed here |
| other charts/components/source branches | open |
| global Krenn--Gu conjecture | **UNRESOLVED** |

## 6. Verification and independent audit

Primary exact replay:

```text
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_open_low_rank_exclusion.py
```

Independent carrier audit:

```text
python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_open_low_rank_exclusion.py
```

The primary rebuilds the full fixed `37 x 9` syndrome map, every named pivot,
Schur resultant, exceptional coefficient, corner seven-minor, and both exact
samples.  It imports the owning `GLD88` family only for the already proved
111-kernel interface.

The audit does not import the primary or the `GLD71` builder.  It parses the
immutable `GLD75` sparse carrier with SHA-256
`05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57`,
independently reconstructs the scale-fixed center-linear system, checks the
`R`-family inside that carrier, replays the four-corner factor cover, and
rederives the `T=0` two-pivot obstruction plus the complete rational sample
center family.  It does not independently rebuild the primary Schur
resultants or corner seven-minors; those remain primary-verifier evidence.
