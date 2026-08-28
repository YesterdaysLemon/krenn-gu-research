# Four-root torus-star equal-leaf H4 L1/L2 rank-seven exclusion

## Status and exact scope

**Exact scoped characteristic-zero theorem (`GLD93`).** Work over `Q` for
the displayed equal-leaf frame and extend scalars to `C`.  On the complete
scale-fixed equal-leaf survivor chart of `GLD83`--`GLD86`, impose the Gaussian
leaf equation `H4` and use the rational chart

```text
G = [1  1       1      ]
    [p  q       s      ],
    [a  1+b     1+c    ],

s=(p+q-pq)/(p+q-1).
```

Let

```text
d0 = p+q-1,
P  = p^2-p+1,
L1 = p^2+2pq-2p-q,
L2 = 2pq-p+q^2-2q,
Omega include det(G) det(C) != 0.
```

Then, on the charted upstream open `D((p-q)d0P)`, the two coefficient
divisors are empty in the rank-at-most-six incidence branch:

```text
B intersect V(I_7(A)) intersect H4 intersect V(L1)
  intersect D(Omega (p-q)d0P) = empty,

B intersect V(I_7(A)) intersect H4 intersect V(L2)
  intersect D(Omega (p-q)d0P) = empty.                 (1)
```

Equivalently, every point in either displayed divisor with the declared
upstream open and `det(G) != 0` has `rank M(G) >= 7`.  The contradiction with
the left side of (1) uses the exact `GLD86` bridge and the scale-fixed
coordinate `C_8=1`; it is a rank obstruction, not a center-singularity
argument.

Combining (1) with `GLD87` (the collision divisors `H1,H2,H3`) and `GLD89`
(`P=0` and its `d0=0` overlap) removes the named `L1` and `L2` boundaries
from the H4 low-rank residual.  `GLD90` already removes the complementary
`Q6`-open.  The remaining named H4 coefficient boundary is `e=0`, together
with the pure `Q6=0` branch and all obligations listed in Section 6 below.
The pulled-back `GLD83` Fitting ideal is not computed.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

The statements are set-theoretic geometric-point statements after scalar
extension.  They do not assert an ideal equality, cover other gauges,
components, source branches, profiles, roots, orders, or rank-eight charts,
and do not claim that every point of the ambient chart has syndrome rank at
least seven.

## 1. Bridge, localization, and direct computation

The fixed `GLD71` annihilator basis gives a `37 x 9` syndrome matrix `M(G)`.
The exact `GLD75`/`GLD86` incidence bridge is

```text
B=0 iff M(G) C=0,
rank A = rank M(G)[:,0:8] on B,
C_8=1.                                                (2)
```

Therefore a point of `B intersect V(I_7(A))` has first-eight syndrome rank at
most six.  The relation `M(G)C=0` and `C_8=1` make the ninth syndrome column
a linear combination of the first eight, so every `7 x 7` minor of the full
matrix must vanish.  Any nonzero seven-minor below is thus a contradiction.
On `D(Omega)`, the normalized frame/center gate supplies `det(G) != 0` and
`det(C) != 0`; this theorem only needs the first of those two inequalities.

The primary verifier reconstructs all 37 rows directly from the pinned
`GLD71` relations.  It uses columns

```text
S=(0,1,3,4,6,7),
R0=(0,1,2,17,19,32),
R1=(0,1,17,19,28,32),
RA=(0,1,2,17,19,25).                                  (3)
```

The L2 calculation is performed independently in the `q` parameter.  No
naive `p <-> q` or leaf-column symmetry is used: although swapping the first
two columns sends the displayed matrix to
`G(q,p,1+b,a-1,c)`, the fixed 37-row carrier is not thereby known to be
invariant.  The two divisor computations below are direct contractions of
the same pinned syndrome map.

## 2. The `L1=0` divisor

The equation `L1=0` has no solution with `2p-1=0` and gives

```text
q=p(2-p)/(2p-1),  s=p.                                (4)
```

On this parameterization,

```text
p-q = 3p(p-1)/(2p-1),
d0  = P/(2p-1),
L2  = -3p(p-1)P/(2p-1)^2,
e   = (p-2)(p+1)P/(2p-1),
T   = -(p-2)(p+1),
Q6  = 6p^2(p-1)^2P^3/(2p-1)^4.                       (5)
```

Here `P=p^2-p+1`.  Thus the upstream open removes `p=0,1` and `P=0`, and
`Q6` is automatically nonzero.  The leaf determinant is

```text
det(G)=3p(p-1)(a-c-1)/(2p-1).                         (6)
```

Put

```text
H10 = 4ap^2-4ap+a -bp^2+4bp-b -p^2+4p-1,
H11 = 4ap^2-4ap+a -bp^2-2bp+2b -4p^2+4p-1.
```

The exact six-minor and bordered seven-minor identities are

```text
det M[R0,S]
  = -324 p^4(p-1)^5(p+1)P^3 H10/(2p-1)^8,

det M[R0 union {25}, S union {5}]
  =  324 p^4(p-1)^5(p+1)P^3(a-c-1)H10/(2p-1)^7,

det M[R1,S]
  = -324 p^5(p-2)(p-1)^4P^3 H11/(2p-1)^8,

det M[R1 union {25}, S union {5}]
  =  324 p^5(p-2)(p-1)^4P^3(a-c-1)H11/(2p-1)^7.        (7)
```

Away from `p=2,-1`, if either bracket is nonzero, (7) gives a nonzero
seven-minor on `D(Omega)`.  If both vanish, their exact solution is

```text
a=-(p-1)^2(p^2-4p+1)/(2p-1)^3,
b=-p^2/(2p-1).                                      (8)
```

Writing

```text
F1=(8p^3-12p^2+6p-1)c+p^4+2p^3-2p^2,
```

the auxiliary seven-minor on the rows `RA union {32}` and columns
`S union {8}` is

```text
det(G)=-3p(p-1)F1/(2p-1)^4,

det M[RA union {32},S union {8}]
  = -2916p^5(p-1)^6(p+1)P^4F1/(2p-1)^11.              (9)
```

The first identity in (9) and `det(G) != 0` force `F1 != 0`, so the second
identity gives the required rank jump.

The only L1 points where `e=T=0` are the two exceptional points
`(p,q)=(2,0)` and `(-1,1)`.  They are handled without dividing by the
vanished pivot factor or by `T`:

```text
(p,q)=(2,0):
 det M[(0,1,2,17,19,32,31),(0,1,3,4,6,7,8)]
   = -27648(a-c-1),

(p,q)=(-1,1):
 det M[(0,1,17,19,28,32,31),(0,1,3,4,6,7,8)]
   =  6912(a-c-1).                                   (10)
```

Both witnesses are nonzero on `D(Omega)`, completing the L1 divisor.

## 3. The `L2=0` divisor

The equation `L2=0` has no solution with `2q-1=0` and gives

```text
p=q(2-q)/(2q-1),  s=q.                                (11)
```

Writing `Q=q^2-q+1`, the exact restrictions are

```text
p-q = -3q(q-1)/(2q-1),
d0  = Q/(2q-1),
P   = Q^2/(2q-1)^2,
L1  = -3q(q-1)Q/(2q-1)^2,
e   = -2Q^2/(2q-1),
T   = -(q-2)(q+1),
Q6  = 6q^2(q-1)^2Q^3/(2q-1)^4,                       (12)
```

and

```text
det(G)=-3q(q-1)(b-c)/(2q-1).                         (13)
```

Thus the upstream open removes `q=0,1` and `Q=0`, and again `Q6` is
automatically nonzero.

Put

```text
H20 = aq^2-4aq+a -4bq^2+4bq-b -4q^2+4q-1,
H21 = aq^2+2aq-2a -4bq^2+4bq-b -q^2-2q+2.
```

The direct L2 six-minor and bordered seven-minor identities are

```text
det M[R0,S]
  = -324 q^4(q-1)^5(q+1)Q^3 H20/(2q-1)^8,

det M[R0 union {25}, S union {5}]
  =  324 q^4(q-1)^5(q+1)Q^3(b-c)H20/(2q-1)^7,

det M[R1,S]
  = -324 q^5(q-2)(q-1)^4Q^3 H21/(2q-1)^8,

det M[R1 union {25}, S union {5}]
  =  324 q^5(q-2)(q-1)^4Q^3(b-c)H21/(2q-1)^7.          (14)
```

Away from `q=2,-1`, a nonzero `H20` or `H21` gives rank at least seven.  If
both vanish, their exact solution is

```text
a=-(q-1)^2/(2q-1),
b=-q^2(q^2+2q-2)/(2q-1)^3.                           (15)
```

For

```text
F2=(8q^3-12q^2+6q-1)c+q^4+2q^3-2q^2,
```

the auxiliary rows `RA union {32}` and columns `S union {8}` give

```text
det(G)=3q(q-1)F2/(2q-1)^4,

det M[RA union {32},S union {8}]
  = 2916q^5(q-1)^6(q+1)Q^4F2/(2q-1)^11.              (16)
```

Again `det(G) != 0` forces the displayed seven-minor to be nonzero.

The only pivot/T exceptional points are `(p,q)=(0,2)` and `(1,-1)`.
At `(0,2)`, the vanishing `H20` branch is `a=-3b-3`, and two exact
witnesses are

```text
-62208(b+1)(b-c)^2,
-20736(3b+1)(b-c)^2.                                 (17)
```

Their linear factors have no common root, while (13) gives `b-c != 0`.
At `(1,-1)`, the vanishing `H21` branch is `a=1-3b`, and the witnesses are

```text
-1728(3b-1)(b-c)^2,
-10368(3b+7)(b-c)^2.                                 (18)
```

These linear factors also have no common root.  This completes L2 without
using a p/q symmetry or dividing by `T`.

## 4. Rank and center logic

The case splits above are exhaustive on each divisor: the denominator
`2p-1` (respectively `2q-1`) cannot vanish on the divisor; the upstream
localization removes the listed collision, `P/d0`, and quadratic factors;
the two ordinary branches are the nonzero-bracket and double-bracket cases;
and the remaining points are exactly the two displayed exceptional fibres.

Every branch provides a nonzero `7 x 7` minor under `det(G) != 0`.  By (2), a
point of `B intersect V(I_7(A))` would make every such minor vanish.  Hence
the two intersections in (1) are empty.  No assertion about `det(C)` is
needed after the rank bridge; `det(C) != 0` remains part of `D(Omega)` and
is preserved in the stated theorem scope.

## 5. Verification and independent audit

The primary exact replay is:

```text
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_l1_l2_rank_seven_exclusion.py
```

It reconstructs all 37 pinned GLD71 relations and checks the H4 identities,
the L1 and L2 parameter restrictions, all four general six-/seven-minor
identities on each divisor, both double-pivot auxiliary minors, both L1
exceptional witnesses, and all four L2 exceptional witnesses.

The independent audit is:

```text
python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_l1_l2_rank_seven_exclusion.py
```

It imports neither the primary verifier nor the GLD71 builder.  Instead it
stores the nine sparse relation supports touched by the certificates,
contracts them directly against the equal-leaf frame, and computes the same
selected determinants through a separate row/matrix representation.  It
replays every displayed six- and seven-minor identity and the exceptional
branch logic.  It intentionally does not claim an independent reconstruction
of the other 28 GLD71 rows; the full 37-row reconstruction remains the
primary verifier's evidence axis.

## 6. Residual boundaries and non-claims

| divisor or obligation | GLD93 disposition |
| --- | --- |
| `p=q` (`H1`), and the transported `H2/H3` collision charts | closed upstream by `GLD87`; no naive p/q symmetry is used here |
| `P=0` and `d0=0` overlap | closed upstream by `GLD89`; this theorem uses `d0 != 0` only in the rational H4 chart |
| `L1=0` | closed here on `D(Omega (p-q)d0P)`, including `e=T=0` points |
| `L2=0` | closed here on `D(Omega (p-q)d0P)`, including `T=0` points |
| `Q6=0` | retained; the common raw-pivot factor is not divided out here |
| `e=0` away from the handled L1 points | retained for a separate boundary theorem |
| pulled-back `GLD83` Fitting ideal | not computed |
| other equal-leaf H4 charts/gauges/components, rank-eight or lower-rank branches outside this cover | open |
| source branches, profiles, roots, orders, and global Krenn--Gu | open; global status remains **UNRESOLVED** |

The theorem is a local rank-seven exclusion inside one Gaussian equal-leaf
chart.  It is not a global source theorem or a resolution of the prize
conjecture.
