# Arbitrary permanent star--triangle exceptional companion propagation theorem

## Status

This note proves one exact characteristic-zero incidence theorem shared by
the displayed equality-five `(4,1)` star pair and `(3,1)` triangle pair.
It strengthens the singleton companion mechanism: **every** exceptional
rank-two kernel occurrence, including support-two occurrences, forces a
companion incidence in a different local mode.

For the star pair the five exceptional ambient lines propagate to five
explicit companion lines.  For the triangle pair four distinct exceptional
lines are organized into three mutual companion cycles.  Exact
single-contraction relations force the companion's local colour support,
and every arrow has a legal reverse arrow.  In particular, every forced
pair is mutually invisible to all five double-contracted sensors.

This is a finite incidence reduction, not an exclusion.  The mutual
two-cycles are compatible with every equation obtained by contracting in
the two displayed pure-`R` directions.  Moreover, a tempting replacement
of the full second contraction by a scalar multiple of the complementary
`A`-pairing matrix is false; an exact rational countermodel is recorded in
Section 6.  Consequently this theorem does not exclude either pair, does
not identify their unbased orbits, and does not prove unrestricted
permanent nonrestriction.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. Common tensor notation

Let `K` be a field of characteristic zero and split

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5}.
```

On `A` put

```text
J((a_4,a_5),(b_4,b_5))=a_4b_5+a_5b_4.                 (1)
```

Every complementary quartic below is `x_4x_5 g_z`, where `g_z` is a
square-free quadratic on `R`.  Write

```text
B_z p = i_p g_z in R^*                                (2)
```

for polarized contraction.  Four ordered independent local triples span
`L_2,...,L_5`.  The exact target equations are

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (3)
```

For `p in L_t cap R`, write

```text
p=sum_c alpha_c y_(t,c),       S=supp(alpha).           (4)
```

The two committed kernel-support predecessors prove that every low kernel
generator in the displayed star or triangle frame has `1<=|S|<=2` and is
one of the exceptional lines listed below.

For such a vector put

```text
Q_p=span{B_zp:z=m_1,m_2,d_0,d_1,d_2} subset R^*,
H_p=ann_R(Q_p).                                         (5)
```

## 2. All-support quotient propagation

### Lemma 1 (support-one-or-two companion)

Assume `dim Q_p>=2` and `1<=|S|<=2`.  Then some distinct local mode `s`
satisfies

```text
L_s cap H_p != 0.                                      (6)
```

If `0!=q in L_s cap H_p` has local coefficient vector `beta`, then

```text
supp(alpha) cap supp(beta)=empty.                       (7)
```

### Proof

Suppose every other local plane missed `H_p`.  Put `D=R/H_p`; then
`D^*=Q_p` and each of the other three local triples embeds in

```text
W=D direct-sum A,                  dim D>=2.             (8)
```

For `y=(r(y),a(y))`, define the `D`-valued trilinear map

```text
C(y,z,w)=r(y)J(a(z),a(w))+r(z)J(a(y),a(w))
                         +r(w)J(a(y),a(z)),             (9)
```

where `r` now denotes the image in `D`.  Evaluation of (9) by every
`B_zp in Q_p` is the single contraction of `x_4x_5g_z` with `p`.
Consequently the exact targets make (9) zero away from the diagonal
colours in `S`, and its value is nonzero on every diagonal in `S`.

If `|S|=1`, this is the one-surviving-diagonal configuration.  For two
different colours in two different modes, the map from `W` to `D` obtained
by fixing those vectors kills the third embedded three-space.  Its rank is
at most `dim D-1`; on the `D` summand it is scalar multiplication by their
`J`-pairing.  Hence every cross-colour pairing is zero.  A nonzero diagonal
contains a nonzero same-colour pairing, so the two off-colour vectors in
one remaining triple lie in one line of `A`, contradicting independence.

If `|S|=2`, the same rank argument gives cross-colour orthogonality.  The
elementary two-dimensional `J` lemma then makes every `A`-column at the
third colour zero in all three remaining modes.  In the original pure
target at that third colour, the removed mode is the only possible
`A`-supplier.  One tensor slot cannot supply both distinct factors
`x_4,x_5`, so that coefficient is zero, contradicting (3).

Thus (6) holds.  Take `q` in that intersection in a distinct slot.  By
definition of `H_p`,

```text
B_zp(q)=0                         for all five z.         (10)
```

Double contraction of (3) in the two distinct slots therefore gives

```text
0=lambda_c alpha_c beta_c E_cc,          c=0,1,2.
```

Every `lambda_c` is nonzero, proving (7).  All contractions are in distinct
tensor slots; no double contraction inside one local mode is used.

### Lemma 2 (single-contraction support filter)

For `q in L_s cap R`, every relation

```text
sum_z rho_z B_zq=0                                      (11)
```

gives, after the legal single contraction in mode `s`,

```text
rho_(d_c) beta_c=0,                         c=0,1,2.     (12)
```

Indeed, mixed targets vanish and the three remaining pure three-tensors
have disjoint colour support.  Lemmas 1--2 will now reduce every `H_p` to
the explicit companion shown in the tables.

## 3. Star frame

The star quadratic cores are

```text
g_(m_1)=x_3(x_0+x_1-x_2),
g_(m_2)=(x_0-x_3)(x_1-x_2),

g_(d_0)=x_0x_1+x_0x_3-x_1x_2+2x_1x_3-x_2x_3,
g_(d_1)=-x_2(x_0+x_1-x_3),
g_(d_2)=2x_0x_3.                                       (13)
```

Its exceptional-line and companion table is

```text
family  p                         allowed S  dim Q_p  H_p
                                                    companion q / support

Phi_1   N=x_1+x_2                 {0,1}       2     span{x_2-x_1,x_1+x_3}
                                                    x_2+x_3 / {2}

Phi_1   B_0=x_0+x_2               {1,2}       3     K(x_2-x_0)
                                                    x_2-x_0 / {0}

Phi_1   C_0=x_0-x_1               {0,2}       3     K(x_0+x_1)
                                                    x_0+x_1 / {1}

Phi_2   N=x_1+x_2                 {0,1}       2     span{x_2-x_1,x_1+x_3}
                                                    x_2+x_3 / {2}

Phi_2   B_1=x_0+x_3               {0,2}       3     K(x_3-x_0)
                                                    x_3-x_0 / {1}

Phi_2   C_1=x_0+x_1+x_2+x_3       {1,2}       3     K(-x_0+x_1+x_2+x_3)
                                                    -x_0+x_1+x_2+x_3 / {0}. (14)
```

For the four one-dimensional kernels in (14), the support filters are the
following exact covector identities:

```text
q=x_2-x_0:                 B_(d_1)q=B_(m_2)q,
                           B_(d_2)q=B_(m_1)q;

q=x_0+x_1:                 B_(d_0)q=2B_(m_1)q+B_(m_2)q,
                           B_(d_2)q=B_(m_1)q;

q=x_3-x_0:                 B_(d_0)q=B_(m_1)q,
                           B_(d_2)q=2B_(m_1)q+B_(m_2)q;

q=-x_0+x_1+x_2+x_3:       B_(d_1)q=-B_(m_1)q,
                           B_(d_2)q=2B_(m_1)q+B_(m_2)q. (15)
```

Equations (12) and (15) force exactly the companion colours in (14).

For the common line, write a vector of `H_N` as

```text
q=(0,u,v,u+v).
```

Direct contraction gives

```text
2B_(m_1)q-B_(d_0)q+B_(d_1)q=0,
u B_(d_2)q=(u+v)(B_(m_1)q+B_(m_2)q).                  (16)
```

The first identity forces `beta_0=beta_1=0`.  Since `q!=0`, the surviving
`beta_2` is nonzero; the second identity and the zero mixed targets force
`u=0`.  Hence `q` is exactly on `K(x_2+x_3)` at colour `2`.

## 4. Triangle frame

The triangle quadratic cores are

```text
g_(m_1)=x_3(x_2-x_1-x_0),       g_(m_2)=x_0(x_2-x_1),
g_(d_0)=2x_0x_3,
g_(d_1)=x_2(x_0+x_1),           g_(d_2)=x_1(x_0-x_2). (17)
```

Its distinct exceptional-line and companion table is

```text
family  p                         allowed S  dim Q_p  H_p
                                                    companion q / support

Phi_1   N=x_1+x_2                 {1,2}       2     span{x_2-x_1,x_3}
                                                    x_3 / {0}

Phi_1   B_0=x_0+x_2               {0,1}       3     K(x_2-x_0)
                                                    x_2-x_0 / {2}

Phi_1   C_0=x_0-x_1               {0,2}       3     K(x_0+x_1)
                                                    x_0+x_1 / {1}

Phi_2   N=x_1+x_2                 {1,2}       2     span{x_2-x_1,x_3}
                                                    x_3 / {0}

Phi_2   X=x_3                     {0}          2     span{x_1+x_2,x_3}
                                                    x_1+x_2 / nonempty subset of {1,2}. (18)
```

For `q=x_2-x_0` one has

```text
B_(d_0)q=-B_(m_1)q,              B_(d_1)q=B_(m_2)q,   (19)
```

which forces colour `2`.  For `q=x_0+x_1`,

```text
B_(d_0)q=-B_(m_1)q,              B_(d_2)q=-B_(m_2)q, (20)
```

which forces colour `1`.

For `p=N`, write `q in H_N` as

```text
q=(0,-a,a,b).
```

The relation `B_(d_1)q+B_(d_2)q=0` forces
`beta_1=beta_2=0`.  Also

```text
b B_(m_2)q=a B_(d_0)q.                                (21)
```

The mixed target vanishes and the colour-`0` coefficient is nonzero, so
`a=0`; hence `q in KX` at colour `0`.

Conversely, for `p=X`, write

```text
q=(0,a,a,b) in H_X.
```

Equation (7) first gives `beta_0=0`.  If `b!=0`, the identity

```text
-a B_(d_0)q+b(B_(d_1)q+B_(d_2)q)=0                   (22)
```

would force `beta_1=beta_2=0`, impossible.  Thus `b=0` and `q in KN`,
with nonempty support contained in `{1,2}`.

## 5. Exact return cycles

Contracting once with every displayed companion gives the reverse common
kernels

```text
star:
  x_2+x_3                    -> span{N,x_1+x_3},
  x_2-x_0                    -> K B_0,
  x_0+x_1                    -> K C_0,
  x_3-x_0                    -> K B_1,
  -x_0+x_1+x_2+x_3          -> K C_1;

triangle:
  X                           -> span{N,X},
  x_2-x_0                    -> K B_0,
  x_0+x_1                    -> K C_0.                  (23)
```

The same support-filter relations, together with disjointness (7), select
the original exceptional line in every row.  Thus every arrow in
(14) and (18) closes an allowed two-cycle.

The only reverse plane requiring a parameter check is the star common
cycle.  Write a vector of the first plane in (23) as

```text
q=(0,a+b,a,b).
```

Besides `B_(d_2)q=B_(m_1)q+B_(m_2)q`, direct contraction gives

```text
(a+2b)B_(m_1)q+aB_(m_2)q-bB_(d_0)q+bB_(d_1)q=0.       (24)
```

Disjointness from the colour-`2` companion first gives `beta_2=0`.  If
`b!=0`, the independent colour-`0` and colour-`1` targets in (24) then
give `beta_0=beta_1=0`, impossible.  Hence `b=0` and `q in KN`, proving
the asserted return exactly.

Equivalently, if `(p,q)` is one of these directed pairs, then

```text
B_zp(q)=B_zq(p)=0                    for all five z.     (25)
```

Their local supports are disjoint, so the doubly contracted right side of
(3) is also zero.  Therefore (25) imposes no condition on the pairing of
the two uncontracted modes.  This is an exact boundary, not evidence that
the complete four-mode targets are realizable.

The star and triangle common cycles have the same contracted covector
matroid after a colour permutation and harmless nonzero rescalings.  In the
star cycle, with active colours `0,1` and missing colour `2`, the two active
residuals `h_0,h_1`, the zero-slice residual `k`, and the missing residual
`x_0` satisfy

```text
x_0=(h_0-h_1)/2.
```

For the triangle cycle, with active colours `1,2` and missing colour `0`,
the corresponding residuals satisfy

```text
x_0=(h_1+h_2)/2.                                       (26)
```

This is a shared local slice pattern only.  It is not an equivalence of the
star and triangle pair orbits.

## 6. The full second-contraction tensor

For a residual covector `h in R^*` and three distinct remaining modes, the
correct trilinear tensor is

```text
C_h(y,z,w)=h(r(y))J(a(z),a(w))+h(r(z))J(a(y),a(w))
                              +h(r(w))J(a(y),a(z)).     (27)
```

After contracting a second vector `y_b=(r_b,a_b)`, the bilinear tensor on
two further modes `c,d` is

```text
h(r_b) M_(cd)
+ h_c tensor (a_b^T J A_d)
+ (a_b^T J A_c) tensor h_d,                             (28)
```

where `h_c,h_d` are the restrictions of `h` to the two local modes and
`A_c,A_d` are their `A`-projection matrices.  Tensor slots are in their
original order.  The last two summands do not vanish merely because the
first contracted vector lies in `R`.

An exact rational countermodel to the scalar-only replacement is immediate.
Take `a_b=x_4`, `r_b=0`; take `a_c=0` and `h(r_c)=1`; and take
`a_d=x_5`, `r_d=0`.  Then

```text
C_h(y_b,y_c,y_d)=1,
h(r_b)J(a_c,a_d)=0.                                    (29)
```

Thus a proof that replaces (27) or (28) by only the first term is invalid.
In particular, the closed two-cycles in Section 5 require a full slice or
tensor-rank argument; pairwise scalar incidence cannot exclude them.

## 7. Exact boundary and replay

```text
star exceptional lows, support one or two:              PROPAGATE;
triangle exceptional lows, support one or two:          PROPAGATE;
companion ambient line/plane and local support:          CLASSIFIED;
all displayed companion arrows:                         MUTUAL TWO-CYCLES;
all five double contractions on a cycle:                ZERO;
scalar-only complementary-M shortcut:                   REFUTED EXACTLY;
same-mode or distinct-mode cycle exclusion:             OPEN HERE;
star fixed-frame full extension:                         NOT EXCLUDED HERE;
triangle fixed-frame full extension:                     NOT EXCLUDED HERE;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.   (30)
```

Replay the exact checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py
python claims/arbitrary-order/audit_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py claims/arbitrary-order/audit_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py claims/arbitrary-order/audit_arbitrary_permanent_star_triangle_exceptional_companion_propagation.py
```

The primary verifier reconstructs both quadratic-core systems, every
residual rank and common kernel, all companion relations, every mutual
cycle, the contracted covector matroid, and the scalarization countermodel
with exact symbolic arithmetic.  The independent audit imports neither the
primary verifier nor SymPy.  It uses explicit integer Hessian matrices,
standalone rational row reduction, direct relation checks, and exhaustive
projective scans over `F_3,F_5,F_7`.  The finite scans are audits of the
case tables only; the written field-linear arguments prove the
characteristic-zero theorem.
