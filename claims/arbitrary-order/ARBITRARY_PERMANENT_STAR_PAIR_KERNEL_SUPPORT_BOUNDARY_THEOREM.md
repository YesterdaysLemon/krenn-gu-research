# Arbitrary permanent star-pair kernel-support boundary theorem

## Status

This note proves an exact characteristic-zero localization inside the
simultaneous projection-drop residual for the explicit `(4,1)` star pair of
`ARBITRARY_PERMANENT_STAR_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md`.
Every rank-two local projection has its kernel on one of three explicit
ambient lines.  Every nonzero local kernel vector has support on at most two
local colours, while a vector away from the exceptional lines would have
support exactly one and is excluded by a one-diagonal obstruction.

Consequently every restricted projection has rank at least two.  Combined
with the two-sided predecessor, every exact `P_6 -> Delta_3` extension of this
displayed star pair has a rank-two mode in each projection family.

The result is pointwise for the displayed based frame.  It does not classify
or exclude the remaining exceptional-line incidences, does not treat all
based frames in the unbased `(4,1)` orbit, and does not normalize another
equality-five pair to this one.  Unrestricted permanent nonrestriction
remains unknown, and the global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. The star pair and exact target

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

At modes `0,1`, fix the colour bases

```text
u_0=-x_0+x_2,      u_1=x_0-x_3,       u_2=x_1-x_2,
v_0=x_0+x_1-x_2+x_3,
v_1=x_0+x_1,       v_2=-x_1+x_2.                         (1)
```

In edge order `(01,02,03,12,13,23)`, use the mixed plane and diagonal
products

```text
m_1=(-1, 1, 0,1, 0,0),       m_2=( 1,-1, 0,0,-1,1),
d_0=(-1, 2,-1,1, 0,1),       d_1=( 1, 0,-1,0,-1,0),
d_2=( 0, 0, 0,2, 0,0).                                  (2)
```

Their complementary quartics are

```text
star(m_1)=x_4x_5 x_3(x_0+x_1-x_2),
star(m_2)=x_4x_5 (x_0-x_3)(x_1-x_2),

star(d_0)=x_4x_5(
  x_0x_1+x_0x_3-x_1x_2+2x_1x_3-x_2x_3),
star(d_1)=-x_4x_5 x_2(x_0+x_1-x_3),
star(d_2)= 2x_4x_5 x_0x_3.                              (3)
```

Put

```text
ell_1=x_0+x_1-x_2,                 ell_2=x_1-x_2,
z_0=x_0-x_3,

Phi_1=(x_3,x_4,x_5,ell_1),         Phi_2=(z_0,x_4,x_5,ell_2).  (4)
```

Let the ordered independent triples

```text
(y_(t,0),y_(t,1),y_(t,2)),                   t=2,3,4,5,
```

span the local three-planes `L_t`.  Assume that together with (1) they
satisfy the full exact target equations

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (5)
```

For `0!=p in L_t`, write its unique local colour expansion as

```text
p=alpha_0 y_(t,0)+alpha_1 y_(t,1)+alpha_2 y_(t,2),
supp_t(p)={c:alpha_c!=0}.                                (6)
```

## 2. Statement

The two ambient kernels are

```text
ker(Phi_1)={p_1(a,b)=(a,b,a+b,0,0,0):a,b in K},
ker(Phi_2)={p_2(a,b)=(a,b,b,a,0,0):a,b in K}.             (7)
```

### Theorem 1 (finite kernel boundary)

For every local mode `t` and family `k`,

```text
0!=p in L_t intersect ker(Phi_k)  =>  |supp_t(p)|<=2.     (8)
```

In fact, every such `p` lies on one of the following six family-labelled
lines, with the common line `K N` occurring in both families:

```text
Phi_1: N=x_1+x_2,      B_0=x_0+x_2,      C_0=x_0-x_1,
Phi_2: N=x_1+x_2,      B_1=x_0+x_3,      C_1=x_0+x_1+x_2+x_3.  (9)
```

The forced missing local colours are

```text
N misses 2;       B_0 misses 0;       C_0 misses 1;
                  B_1 misses 1;       C_1 misses 0.      (10)
```

Consequently

```text
rank(Phi_k|L_t)>=2                                      (11)
```

for every `k,t`.  If the rank is two, its kernel is precisely one of the
family-labelled lines in (9).  The two-sided predecessor then gives

```text
min_t rank(Phi_1|L_t)=min_t rank(Phi_2|L_t)=2.           (12)
```

Equations (9)--(12) are necessary conditions, not realizability claims.

## 3. Exact single-contraction tables

Contract (3) with the generic vectors in (7), omit the common factor
`x_4x_5`, and regard the result as a covector on
`R=span{x_0,x_1,x_2,x_3}`.  Direct polarization gives

```text
                         m_1                 m_2

i_(p_1(a,b))             0             a(-x_0+x_1-x_2+x_3)
i_(p_2(a,b))       a(x_0+x_1-x_2+x_3)             0

                         d_0

i_(p_1(a,b))       b(x_0-x_1-x_2+x_3)
i_(p_2(a,b))       (a+b)x_0+(3a-b)x_1-(a+b)x_2+(a+b)x_3

                         d_1                         d_2

i_(p_1(a,b))       (a+b)(-x_0-x_1-x_2+x_3)         2a x_3
i_(p_2(a,b))       b(-x_0-x_1-x_2+x_3)             2a(x_0+x_3).
                                                               (13)
```

For `Phi_1`, the nonzero mixed residual followed by the three diagonal
residuals has determinant

```text
8a^2 b(a+b).                                             (14)
```

For `Phi_2`, the analogous determinant is

```text
-8a^2 b(a-b).                                            (15)
```

Thus the residuals form a basis of `R^*` away from the three projective
directions in each row of (9).

The table also proves (10).  In the `Phi_1` family, the conditions
`a=0`, `b=0`, and `a+b=0` kill respectively the `d_2`, `d_0`, and `d_1`
contractions.  In the `Phi_2` family, `a=0` kills `d_2`, while `b=0` kills
`d_1`.  On the remaining line `a=b`, no diagonal residual vanishes, but
the exact tensor identity

```text
i_(p_2(a,a)) star(d_0)=2 i_(p_2(a,a)) star(m_1)          (16)
```

does the required work.  The mixed target is zero, so (16) makes the
contracted `d_0` target zero.  Since every `lambda_c` is nonzero, contracting
the right side of (5) with (6) forces exactly the missing-colour equations
in (10).  This proves (8) on all exceptional lines.

## 4. The residual `R direct-sum A` tensor

It remains to analyze a kernel vector for which the determinant (14) or
(15) is nonzero.  Split the ambient six-space as

```text
K^6=R direct-sum A,
R=K^{\{0,1,2,3\}},                    A=K^{\{4,5\}},       (17)
```

and put

```text
J((s_4,s_5),(t_4,t_5))=s_4t_5+s_5t_4.                  (18)
```

For `y=(r(y),a(y))`, define the symmetric `R`-valued trilinear map

```text
C(y,z,w)=r(y)J(a(z),a(w))+r(z)J(a(y),a(w))
                         +r(w)J(a(y),a(z)).              (19)
```

For every residual covector `h in R^*`, evaluation of `h(C)` is exactly
the polarization of `x_4x_5 h` on `(y,z,w)`.  Remove the mode `t` containing
`p`, and call the other three modes `s,u,v`.  Since the applicable four
residuals in (13) form a basis of `R^*`, the exact target equations determine
all values of (19):

```text
C(y_(s,i),y_(u,j),y_(v,l))=0               unless i=j=l,

C(y_(s,e),y_(u,e),y_(v,e))!=0
                                      iff alpha_e!=0.    (20)
```

No genericity of the remaining local spaces is used.

## 5. At most two active colours

We recall the elementary two-dimensional obstruction in the form needed
here.

### Lemma 2 (cross-orthogonality)

Let `A` be two-dimensional with a nondegenerate symmetric form `J`.  For
three modes `q in {s,u,v}` and colours `e in {0,1,2}`, suppose vectors
`a_(q,e) in A` satisfy

```text
J(a_(q,e),a_(q',f))=0       whenever q!=q' and e!=f.     (21)
```

Call a colour active if some same-colour pairing between distinct modes is
nonzero.  At most two colours are active.  If exactly two are active, every
vector at the third colour is zero.

### Proof

If every mode spans at most a line in `A`, a nonzero same-colour pairing
forces its two endpoint modes to contain no nonzero column of another colour.
Any second active pair shares an endpoint among three modes, so it has the
same colour.

Otherwise one mode, say `s`, contains two independent columns of colours
`e,f`.  Every other mode's column at the third colour `h` is orthogonal to
both and hence is zero.  Thus at most `e,f` are active.  If both are active,
there are nonzero outside columns on the distinct lines
`a_(s,f)^perp` and `a_(s,e)^perp`.  The column `a_(s,h)` is orthogonal to
both, so it too is zero.  This proves the stronger assertion.

### Application to a generic kernel vector

For two remaining modes and different colours `(i,j)`, the map

```text
w |-> C(y_(s,i),y_(u,j),w): R direct-sum A -> R          (22)
```

kills the independent three-space `L_v` by (20), so its rank is at most
three.  On the four-dimensional `R`-summand it is scalar multiplication by

```text
J(a(y_(s,i)),a(y_(u,j))).                                (23)
```

A nonzero scalar would give rank at least four.  Therefore (21) holds.
Every colour in `supp_t(p)` is active, because its nonzero value in (20)
contains a nonzero same-colour `J` pairing.  Lemma 2 gives
`|supp_t(p)|<=2`.

If the support had size two, those two colours would be precisely the two
active colours.  Lemma 2 would make all three remaining modes' `A`-parts
zero at the third colour.  In the original nonzero pure `d_h` coefficient
at that third colour, the two distinct factors `x_4,x_5` would then have to
come from the single removed mode.  Polarization assigns distinct factors
to distinct modes, so this coefficient is zero, contradicting (5).  Hence
every generic kernel vector would satisfy

```text
|supp_t(p)|=1.                                           (24)
```

## 6. A generic singleton is impossible

The last step is another dimension obstruction.

### Lemma 3 (one surviving diagonal)

Let `W=D direct-sum A`, where `dim D=d>=2`, `dim A=2`, and `J` is
nondegenerate on `A`.  Define the `D`-valued trilinear map by the analogue
of (19).  Three independent ordered triples in `W` cannot satisfy

```text
C(y_(s,i),y_(u,j),y_(v,l))=0 unless i=j=l=e,
C(y_(s,e),y_(u,e),y_(v,e))!=0.                          (25)
```

### Proof

For `(i,j)!=(e,e)`, the map `w |-> C(y_(s,i),y_(u,j),w)` kills the
three-space `L_v`, so its rank is at most `dim W-3=d-1`.  Its restriction
to `D` is scalar multiplication by
`J(a(y_(s,i)),a(y_(u,j)))`; hence that scalar is zero.  The same conclusion
holds after permuting the modes.

The nonzero value in (25) contains a nonzero same-colour pairing.  After a
mode permutation, assume the pairing between the `s` and `u` vectors is
nonzero.  For each `l!=e`, the two cross pairings in
`C(y_(s,e),y_(u,e),y_(v,l))` vanish, so the zero value forces
`r(y_(v,l))=0`.  Both off-`e` vectors of the independent third triple now
lie in `A` and in the one-dimensional orthogonal complement of
`a(y_(s,e))`.  They are dependent, a contradiction.

For a generic kernel vector, (24) turns (20) exactly into (25), with
`D=R` and `d=4`.  Lemma 3 therefore excludes every direction for which
(14) or (15) is nonzero.  The only possible kernel directions are (9).

## 7. Rank and finite-incidence consequences

Fix `k,t` and put

```text
S=L_t intersect ker(Phi_k).
```

Every nonzero element of `S` lies in the union of the three corresponding
lines in (9).  Over the infinite field `K`, a vector space cannot be a
finite union of proper linear subspaces.  Therefore `dim S<=1`.  Rank-nullity
on the three-space `L_t` proves (11), and a nonzero `S` must equal its one
exceptional line.

The star-pair two-sided projection-drop predecessor proves that each
projection family has at least one rank-drop mode.  Combining that fact with
(11) proves (12).

This reduction is finite but not an exclusion: modes from the two families
may coincide, and (9) records no assertion that any displayed incidence is
realizable.

## 8. Exact boundary and replay

```text
displayed star pair, all local projection ranks >=2:      PROVED;
every local kernel vector has colour support <=2:         PROVED;
generic ambient kernel directions:                        EXCLUDED;
three exceptional kernel lines per family:                PROVED NECESSARY;
a rank-two mode in each projection family:                PROVED NECESSARY;
exceptional-line incidence classification/exclusion:      OPEN;
all based frames in the unbased (4,1) orbit:                NOT TREATED;
unrestricted P_6 -> Delta_3:                               UNKNOWN;
global Krenn--Gu conjecture:                               UNRESOLVED.
```

Replay the exact checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_star_pair_kernel_support_boundary.py
python claims/arbitrary-order/audit_arbitrary_permanent_star_pair_kernel_support_boundary.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_star_pair_kernel_support_boundary.py claims/arbitrary-order/audit_arbitrary_permanent_star_pair_kernel_support_boundary.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_star_pair_kernel_support_boundary.py claims/arbitrary-order/audit_arbitrary_permanent_star_pair_kernel_support_boundary.py
```

The primary verifier reconstructs both ambient kernels, all ten exact
single contractions, both generic determinants, the exceptional tensor
identity, the `R direct-sum A` factorization, and finite-field instances of
the cross-orthogonality lemma.  The independent audit imports neither the
primary verifier nor SymPy: it rebuilds the star pair and complemented cores,
uses a separate polynomial determinant implementation, checks all exceptional
relations, and independently exhausts the two-dimensional lemma over odd
finite fields.  The computations replay identities and stress-test the case
split; the written characteristic-zero arguments prove the theorem.
