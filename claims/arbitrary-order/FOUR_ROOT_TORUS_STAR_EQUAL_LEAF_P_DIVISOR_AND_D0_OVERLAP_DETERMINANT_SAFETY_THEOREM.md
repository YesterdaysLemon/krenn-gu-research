# Four-root torus-star equal-leaf P divisor and d0-overlap determinant safety

## Status and exact scope

**Exact scoped divisor theorem (`GLD89`).** Work over `Q` for the displayed
equal-leaf frame and extend scalars to `C`. On the complete scale-fixed
equal-leaf survivor chart of `GLD83`--`GLD86`, intersected with the `H4`
divisor and with `D(Omega)`, the entire divisor

```text
P = p^2-p+1
```

is excluded from the rank-at-most-six center branch. The `d0` overlap

```text
d0 = p+q-1 = 0
```

is also excluded; on `H4` it is automatically contained in `P=0`, and the
overlap is handled in its own chart because the rational `H4` parameterization
has denominator `d0`. Equivalently, in the displayed chart,

```text
B intersect V(I_7(A)) intersect D(Omega) intersect H4 intersect V(P) = empty,
B intersect V(I_7(A)) intersect D(Omega) intersect H4 intersect V(d0) = empty.
```

These are set-theoretic geometric-point statements. They do not compute the
pulled-back `GLD83` Fitting ideal, do not close the remaining `H4` boundary,
and do not resolve the global Krenn--Gu conjecture, which remains
**UNRESOLVED**.

The `H1` overlap `p=q` and the exceptional `d0=0` fibres with
`s^2-s+1=0` use `GLD87` exactly where indicated below. `GLD87` is not used to
assert any unlisted `H4` closure.

## 1. Chart, notation, and upstream bridge

Use the complete scale-fixed equal-leaf chart

```text
B=Spec K[x_0,...,x_14]/(g_0,...,g_9,x_8),    K=Q(i),
```

with the exact `GLD75` survivor generators and `x_8=0`. The common leaf
frame is written in the shifted lower-row coordinates

```text
G = [1  1       1      ]
    [p  q       s      ],
    [a  1+b     1+c    ],
```

and, on the `H4` divisor,

```text
H4 = p q+p s+q s-p-q-s = 0.
```

When `d0=p+q-1 != 0`, this gives the exact rational chart

```text
s=(p+q-p q)/d0.                                      (1)
```

The fixed `GLD71` annihilator basis gives a `37 x 9` syndrome matrix
`M(G)`. `GLD86` supplies the exact bridge

```text
B=0 iff M(G) C=0,
rank A = rank M(G)[:,0:8] on B,                       (2)
```

and the scale-fixed coordinate is `C_8=1`. Thus a point in
`B intersect V(I_7(A))` has first-eight syndrome-column rank at most six;
using `M(G)C=0` and `C_8=1`, every seven-minor of the full `M(G)` vanishes as
well. On `D(Omega)`, the normalized gauge includes

```text
det(G) det(C) != 0.                                   (3)
```

The proof below uses only (2), (3), the fixed syndrome map, and the exact
`GLD87` H1/H2/H3 result. No sampled rank statement is used.

Put

```text
P  = p^2-p+1,
Q  = q^2-q+1,
L1 = p^2+2 p q-2 p-q,
L2 = 2 p q-p+q^2-2 q,
e  = 2 p q^2-2 p q-p-q^2-2 q+2,
B0 = p q^2+2 p q-2 p+q^2-4 q+1.                     (4)
```

The name `B0` here is a scalar polynomial and is unrelated to the survivor
base `B`.

## 2. The two exact six-minors on `P=0`

For `d0 != 0`, the primary verifier reconstructs `M(G)` from all 37 pinned
`GLD71` relations and checks, modulo `P`, the following two determinants. Let

```text
R_P  = (0,1,2,17,19,32),
R'_P = (0,1,2,17,19,31),
S_P  = (0,1,3,4,6,7).                                (5)
```

Then

```text
det M[R_P,S_P]
  = 6 Q^3 ((p-2)a-(q^2-1)(b+1)),

det M[R'_P,S_P]
  = -6 Q^3 ((p-2)q^3 a+(q^2-1)(b+1))                 (6)
```

in the quotient by `P`. The expressions on the right are reduced numerators;
the unreduced `H4` determinants are rational functions in `d0`, while the
displayed identities are exact after clearing their nonzero denominators.
Call the two bracketed factors `F1` and `F3`.

The identity

```text
Q-(q-p)d0-P=0                                          (7)
```

shows that, on `P=0,d0!=0`, `Q=0` would force `q=p`. That is precisely the
`H1` overlap, and its determinant-safe exclusion is the `GLD87` theorem.
Consequently `Q!=0` on the retained `P` branch. The exact resultants

```text
Res_p(P,d0)=Q,
Res_p(P,pq-1)=Q,
Res_p(P,e)=3Q^2,
Res_p(P,L2)=Q^2,
Res_p(P,p+1)=3                                  (8)
```

will be used without silently inverting any divisor outside the stated open.

## 3. The `P=0`, `d0!=0` branches

### 3.1 The named six-pivot open `mP != 0`

Use the first determinant in (6) as the six-pivot `mP`. Its two bordered
seven-minors, with the same six rows/columns and target column `5`, are the
two `GLD88` Schur residuals. The primary verifier reconstructs both bordered
determinants and checks their reduced numerators modulo `P`:

```text
E25 = Q e (a+c),

E31 = 6 Q J,

J = 3a(p q^2-2 p q-q^2+1)
    +3c(p q^2-p-2q+1)+B0.                             (9)
```

On `mP!=0`, rank at most six makes both bordered minors vanish. By (8) and
the `H1` exclusion, `Q e L2 != 0`; hence (9) gives

```text
c=-a,
a=B0/(3L2).                                          (10)
```

The full 37-row calculation then checks, for each root block `r=0,1,2` and
every syndrome row `i`,

```text
M(G)_(i,3r)-M(G)_(i,3r+2)=0                           (11)
```

after (10) and modulo `P`; there are `3*37=111` identities. Thus each root
block has the common kernel vector `(-1,0,1)`. Since `mP!=0`, the syndrome
rank is exactly six, so these three block-supported vectors span the complete
three-dimensional kernel. Every compatible center has two proportional rows,
and therefore `det(C)=0`, contradicting (3).

Here `b` remains free subject to `mP!=0`; it is not silently specialized.

### 3.2 The six-pivot boundary `mP=0`, `m3!=0`

Now the two identities (6) imply `F1=0` and `F3!=0`. The case `q^2=1`
would make `F1=0` force `a=0`, and then also `F3=0`; therefore this branch has
`q^2!=1` and

```text
b=a(p-2)/(q^2-1)-1.                                  (12)
```

Use the alternate six rows `R'_P` and the same columns `S_P`. The bordered
seven-minors at rows `25` and `33`, both with target column `5`, are linear in
`c` after (12). If their reduced linear forms are `F25,F33`, the exact
coefficient cross-consistency identity checked by the primary verifier is

```text
det_c(F25,F33)
 = -3 a^2(q-1)(q+1)^2 Q^2(p+1)(3a-p-1)d0^6   mod P.     (13)
```

Since `m3!=0`, (6) and (12) give
`a(p-2)(q+1)Q != 0`; (8), `d0!=0`, and `P=0` remove every other factor in
(13). Thus

```text
a=(p+1)/3.                                            (14)
```

The remaining exact linear form is checked in the factored form

```text
D = p q^3-3 p q+p-3q^2+3q = d0^2(pq-1)       mod P,
F33 = Q(3c+p+1)D                              mod P.   (15)
```

The resultants in (8) make `D!=0` on this branch, so `c=-(p+1)/3`. Substituting
in (12) gives

```text
b=q^2/(1-q^2).                                       (16)
```

The primary verifier checks again all 111 identities (11), and checks the
nonzero alternate six-minor numerator

```text
m3 = 6(q+1)Q^4                                      (17)
```

on this slice. The complete kernel is therefore the three copies of
`(-1,0,1)`, forcing `det(C)=0` and contradicting (3).

### 3.3 The zero-six-minor branch

If `mP=m3=0`, adding the two factors in (6) gives

```text
(p-2)a(q+1)Q=0  mod P.                                (18)
```

For `q^2!=1`, (8) and `p-2!=0` force `a=0`, and then `F1=0` gives `b=-1`.
The leaf determinant is checked as

```text
det(G)=(c+1)Q/d0  mod P.                               (19)
```

If also `q!=0`, the seven-minor with rows
`(0,1,2,17,19,25,28)`, columns `S_P` followed by `8`, has reduced numerator

```text
3q(c+1)Q^4(2pq-p-q-1).                                (20)
```

The last factor has resultant `3Q` with `P`; (19) and `D(Omega)` make every
factor in (20) nonzero, contradicting rank at most six. At `q=0`, the two
seven-minors with rows `(0,1,17,19,25,28,32)` and target columns `5` and `8`
have reduced numerators

```text
-18c(p-1),       18(2c+p),                            (21)
```

so one is nonzero: if `c!=0` use the first, and if `c=0` use the second.

It remains to check `q=1` and `q=-1`, where (18) already gives `a=0` but
leaves `b` free.

For `q=1`, the first two seven-minors (both with target `8`) have reduced
numerators

```text
-3b(c+1)(2p-1),
-6(c+1)(2bp-b+3p).                                   (22)
```

If `c+1!=0`, the first forces `b=0` and the second is nonzero. If `c=-1`,
the rows `(0,1,17,19,25,28,32)` with target `8` give `18(p+1)!=0`.

For `q=-1`, when `c+1!=0`, three target-`8` minors have reduced numerators
up to nonzero constants

```text
bp-2b-2,
bp-2b+3p-5,
bp-2b+1.                                             (23)
```

The last two differ by `3(p-2)!=0`, so they cannot vanish simultaneously. If
`c=-1`, the target-`5` minor gives `-3b+p+1`, while the target-`8` minor then
gives `-3(p+1)!=0`. This closes every zero-six-minor subcase.

## 4. The `d0=0` overlap chart

On `H4` and `d0=0`, the equations give `q=1-p` and `P=0`, while `s` is
free. The primary verifier rebuilds `M(G)` with an independent symbol
`sigma=s` and checks modulo `P` rows `0,1,17,19` exactly. For a kernel vector
split into its three root blocks `x,y,z`, these rows give

```text
x0+x1+x2=0,
-y0-y1+sigma^3 y2=0,
f (x2+(sigma-1)y2)=0,
f ((sigma-1)x2-sigma y2)=0,

f=sigma^2-sigma+1.                                   (24)
```

If `f!=0`, the last two equations have determinant `-f` and force
`x2=y2=0`; hence `x=(u,-u,0)` and `y=(v,-v,0)`. The first two rows of every
compatible center are proportional, so `det(C)=0`.

If `f=0`, the roots of `f` are exactly `p` and `q=1-p`, because
`P(sigma)=P(1-sigma)=f`. Thus `s=p` or `s=q`, namely `H2` or `H3`, and the
determinant-safe exclusion is exactly the `GLD87` result. This completes the
`d0=0` overlap without dividing by `d0`.

## 5. Residual boundary table and non-claims

| divisor or boundary | exact GLD89 disposition on `H4 intersect D(Omega)` |
| --- | --- |
| `p-q` (`H1`) | excluded by `GLD87`; used only to remove the `P=Q=0,d0!=0` overlap |
| `d0=p+q-1` | excluded here; `H4 intersect V(d0)` is the separate `P=0` overlap chart |
| `P=p^2-p+1` | excluded here, including `mP!=0`, `mP=0,m3!=0`, and `mP=m3=0` |
| `L1=p^2+2pq-2p-q` | prior `GLD88` principal-open closure only; `L1 intersect V(P6)` remains |
| `L2=2pq-p+q^2-2q` | prior `GLD88` principal-open closure only; `L2 intersect V(P6)` remains |
| `e=2pq^2-2pq-p-q^2-2q+2` | prior `GLD88` principal-open closure only; `e intersect V(P6)` remains |
| pure `P6` boundary with no named `Delta` factor | retained for the complementary `GLD90` lane |

The `GLD83` pulled-back Fitting ideal is not computed here. Other gauges,
components, source branches, lower-rank charts outside this equal-leaf
chart, other profiles/roots/orders, and the global conjecture remain open.

## 6. Verification and audit

The primary exact replay is:

```text
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_p_divisor_and_d0_overlap_determinant_safety.py
```

The independent no-import audit is:

```text
python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_p_divisor_and_d0_overlap_determinant_safety.py
```

The primary reconstructs the full `37 x 9` GLD71 matrix and every named
six- or seven-minor above with exact characteristic-zero arithmetic. The
audit uses a separate standard-library `Fraction` sparse quotient and
reconstructs the reduced scalar certificates, the d0 row subsystem, and the
kernel/contradiction logic; it does not import the primary or a repository
module. Therefore it is independent evidence for the displayed algebraic
implications, while the full GLD71 reconstruction remains owned by the
primary verifier.

Owning upstream facts are `GLD71`, the `GLD75` incidence certificate and
`GLD86` rank bridge, and `GLD87` for only the H1/H2/H3 uses explicitly marked
above.
