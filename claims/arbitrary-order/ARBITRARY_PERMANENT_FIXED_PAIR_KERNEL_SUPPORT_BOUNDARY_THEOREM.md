# Arbitrary permanent fixed-pair kernel-support boundary theorem

## Status

This note proves an exact characteristic-zero localization inside the
simultaneous projection-drop residual for the fixed equality-five pair of
`ARBITRARY_PERMANENT_FIXED_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md`.
For either mixed-factor projection `Phi_k`, every nonzero vector in a local
kernel has support on at most two of the three local colour coordinates.
Away from three explicit ambient kernel lines, its local support is exactly
one.  Consequently every restricted projection has rank at least two.

Combined with the two-sided predecessor, every exact `P_6 -> Delta_3`
extension of this fixed pair has a rank-**two** mode in each projection
family.  The result does not classify the remaining rank-two incidences,
does not exclude their simultaneous occurrence, and does not normalize an
arbitrary equality-five pair to the fixed pair.  Unrestricted permanent
nonrestriction remains unknown, and the global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. Fixed pair and exact target

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

At modes `0,1`, fix

```text
u_0=x_0-x_3,      u_1=x_1-x_3,      u_2=x_2-x_3,
v_0=x_1+x_2,      v_1=x_0+x_2,      v_2=x_2-x_3.
```

In edge order `(01,02,03,12,13,23)`, the two mixed and three diagonal
product classes are

```text
m_1=(0,1,-1,0,0,-1),       m_2=(0,0,0,1,-1,-1),
d_0=(1,1,0,0,-1,-1),       d_1=(1,0,-1,1,0,-1),
d_2=(0,0,0,0,0,-2).
```

Their complementary quartics are

```text
star(m_1)=x_4x_5 x_1 ell_1,
star(m_2)=x_4x_5 x_0 ell_2,

star(d_0)=x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)=x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1,                              (1)
```

where

```text
ell_1=x_3-x_2-x_0,             ell_2=x_3-x_2-x_1,
Phi_1=(x_1,x_4,x_5,ell_1),     Phi_2=(x_0,x_4,x_5,ell_2). (2)
```

Let the ordered independent triples

```text
(y_(t,0),y_(t,1),y_(t,2)),                 t=2,3,4,5,
```

span the three-dimensional local spaces `L_t`.  Assume that together with
the fixed pair they give the exact target equations

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (3)
```

All conclusions below are pointwise for data satisfying (3).

## 2. Statement

For `p in L_t`, write its unique local colour expansion as

```text
p=alpha_0 y_(t,0)+alpha_1 y_(t,1)+alpha_2 y_(t,2),
supp_t(p)={c:alpha_c!=0}.                              (4)
```

### Theorem 1 (kernel-support boundary)

For every `t in {2,3,4,5}` and `k in {1,2}`,

```text
0!=p in L_t intersect ker(Phi_k)  =>  |supp_t(p)|<=2.   (5)
```

More precisely, the two ambient kernels are

```text
ker(Phi_1)={p_1(a,b)=(a,0,b,a+b,0,0):a,b in K},
ker(Phi_2)={p_2(a,b)=(0,a,b,a+b,0,0):a,b in K}.         (6)
```

If

```text
a b (a+b)!=0,                                          (7)
```

then every `p_k(a,b)` lying in `L_t` has

```text
|supp_t(p_k(a,b))|=1.                                  (8)
```

On the three exceptional ambient lines, the exact forced zeros are

```text
                a=0       b=0       a+b=0

k=1:          alpha_2=0 alpha_0=0 alpha_1=0,
k=2:          alpha_2=0 alpha_1=0 alpha_0=0.            (9)
```

Consequently

```text
rank(Phi_k|L_t)>=2                                     (10)
```

for every `k,t`.  If `L_t intersect ker(Phi_k)` is nonzero, it is a single
line and one local colour coordinate vanishes identically on it.  If its
generator satisfies (7), the line is exactly one of the three local colour
lines.

## 3. Single contractions

Put

```text
h_0=-x_0+x_1+x_2+x_3,
h_1= x_0-x_1+x_2+x_3,
h_2= x_0-x_1-x_2+x_3,
h_2'=-x_0+x_1-x_2+x_3.                                (11)
```

Contracting the quartics (1) once with the vectors (6) gives

```text
                         m_1       m_2       d_0        d_1          d_2

i_(p_1(a,b)) star(.)      0       a h_2      b h_0     (a+b)h_1   -2a x_1
i_(p_2(a,b)) star(.)     a h_2'     0       (a+b)h_0    b h_1     -2a x_0.
                                                                    (12)
```

Every entry in (12) is to be multiplied by the common factor `x_4x_5`.
For either row, the four displayed nonzero-channel residual covectors have
determinant

```text
8 a^2 b(a+b)                                             (13)
```

in the basis `(x_0,x_1,x_2,x_3)`, when ordered as the nonidentically-zero
mixed channel followed by `d_0,d_1,d_2`.

If (7) fails, (12) proves (9) immediately.  For example, at `a=0` the
`d_2` contraction is identically zero, whereas contracting the right side
of (3) with (4) gives

```text
lambda_2 alpha_2 e_2^* tensor e_2^* tensor e_2^*.
```

Thus `alpha_2=0`.  The other five entries of (9) follow from the vanishing
`d_0` or `d_1` channel in exactly the same way.  This already proves (5)
on the exceptional lines.

## 4. The `R direct-sum A` contraction tensor

It remains to treat (7).  Decompose the six-dimensional ambient space as

```text
R direct-sum A,
R=K^{\{0,1,2,3\}},                  A=K^{\{4,5\}}.       (14)
```

Write a vector `y` as `(r(y),a(y))` under (14), and put

```text
J((s_4,s_5),(t_4,t_5))=s_4t_5+s_5t_4.                  (15)
```

This is a nondegenerate symmetric form on `A`.  Define the symmetric
`R`-valued trilinear map

```text
C(y,z,w)=r(y)J(a(z),a(w))+r(z)J(a(y),a(w))
                         +r(w)J(a(y),a(z)).             (16)
```

For every residual covector `ell in R^*`, evaluation of `ell(C)` is exactly
the coefficient of `x_4x_5 ell` in the product `yzw`.  Therefore (12)--(13)
and the exact target equations determine every value of (16) on the three
remaining local colour bases.

Indeed, remove mode `t` and write the other modes as `s,u,v`.  Under (7),
the four contraction covectors in the applicable row of (12) form a basis
of `R^*`.  The mixed target is zero, and the three diagonal targets give

```text
C(y_(s,i),y_(u,j),y_(v,l))=0               unless i=j=l,

C(y_(s,e),y_(u,e),y_(v,e))!=0
                         iff alpha_e!=0.                 (17)
```

No genericity of the three remaining local spaces is used here.

## 5. A two-dimensional cross-orthogonality lemma

The following elementary lemma is the obstruction behind (5) and (8).

### Lemma 2 (at most two active colours)

Let `A` be a two-dimensional space with a nondegenerate symmetric bilinear
form `J`.  For three modes `s,u,v`, let

```text
a_(q,e) in A,                     q in {s,u,v}, e in {0,1,2},
```

and assume

```text
J(a_(q,e),a_(q',f))=0       whenever q!=q' and e!=f.    (18)
```

Call colour `e` active if

```text
J(a_(q,e),a_(q',e))!=0
```

for some two distinct modes.  At most two colours are active.  If exactly
two colours `e,f` are active, then every vector at the third colour `h`
vanishes:

```text
a_(s,h)=a_(u,h)=a_(v,h)=0.                              (19)
```

### Proof

Let

```text
rho_q=dim span{a_(q,0),a_(q,1),a_(q,2)} subset A.
```

If all three `rho_q` are zero, there is no active colour.  Suppose next
that every `rho_q<=1`.  If `e` is active between modes `q,q'`, their two
image lines pair nontrivially.  Any nonzero different-colour column at
either endpoint would be proportional to its `e` column and simultaneously
orthogonal to the other endpoint's `e` column by (18), a contradiction.
Thus those two modes support only colour `e`.  Any second active pair among
three modes shares one of them, so no second colour can be active.

Finally suppose `rho_s=2`.  Choose independent columns `a_(s,e),a_(s,f)`
and let `h` be the remaining colour.  For each `q!=s`, the vector `a_(q,h)`
is orthogonal to both independent columns, hence is zero.  Thus `h` is not
active and at most `e,f` can be active.

If both `e` and `f` are active, some nonzero outside `e` column exists and
lies in `a_(s,f)^perp`; likewise some nonzero outside `f` column exists and
lies in `a_(s,e)^perp`.  These two orthogonal-complement lines are distinct,
so the two outside columns are independent.  Equation (18) makes
`a_(s,h)` orthogonal to both, hence zero.  Together with the preceding
vanishing at the other modes this proves (19).  The cases
`max rho_q=0,1,2` are exhaustive.

## 6. Applying the lemma

Take distinct remaining modes `s,u` and distinct colours `i!=j`.  The
linear map

```text
K_(i,j):R direct-sum A -> R,
w |-> C(y_(s,i),y_(u,j),w)                              (20)
```

kills the three-dimensional space `L_v` by the off-diagonal part of (17).
Hence `rank K_(i,j)<=3`.  On the four-dimensional `R`-summand, however,

```text
K_(i,j)(r,0)=J(a(y_(s,i)),a(y_(u,j)))r.                 (21)
```

If the scalar in (21) were nonzero, (20) would have rank at least four.
Therefore the nine `A`-arrays satisfy (18).

By (17), every colour in `supp_t(p)` is active: a nonzero value of `C` must
contain at least one nonzero same-colour `J` pairing.  (The converse is not
needed; such pairings could cancel in `C`.)  Lemma 2 first gives
`|supp_t(p)|<=2`.  Suppose equality holds.  Then those two support colours
already exhaust the at-most-two active colours, so the third colour `h` is
inactive.  The stronger conclusion (19) says that the `h`-columns at all three
remaining modes have zero `x_4,x_5` projection.  In the original pure
coefficient

```text
T_(d_h)(y_(2,h),y_(3,h),y_(4,h),y_(5,h)),              (22)
```

the common factors `x_4x_5` in (1) must be supplied by two distinct modes.
Only the removed mode can have a nonzero `A`-part, so (22) is zero.  This
contradicts `lambda_h!=0` in (3).  Thus (8) holds.

Together with the exceptional-line argument of Section 3, this proves
(5), (8), and (9) for `Phi_1`.  The second row of (12) proves them directly
for `Phi_2`; no appeal to an unstated symmetry is needed.

## 7. Finite-union consequences

Fix `k,t` and put

```text
S=L_t intersect ker(Phi_k).
```

Equation (5) places `S` in the union of the three local coordinate
hyperplanes.  A vector space over an infinite field cannot be a finite
union of proper linear subspaces.  Hence `S` is contained in one coordinate
hyperplane: one colour coefficient vanishes identically on the whole
kernel intersection.

Moreover `dim ker(Phi_k)=2`.  If `dim S>=2`, then `S=ker(Phi_k)`.  The
complement of the three exceptional lines (7) is nonempty.  Every vector
there would have to lie on one of the three local coordinate lines by (8).
This would cover the two-space `S` by the three exceptional ambient lines
and three local coordinate lines, again a finite union of proper
subspaces.  That is impossible over `K`.  Therefore `dim S<=1`, and since
`dim L_t=3`, rank-nullity proves (10).

The two-sided predecessor supplies at least one rank-drop mode in each
projection family.  Combining it with (10) gives

```text
min_t rank(Phi_1|L_t)=min_t rank(Phi_2|L_t)=2.          (23)
```

This is a necessary boundary condition, not an existence statement.

## 8. Exact boundary and replay

```text
fixed pair, every local Phi_k rank at least two:          PROVED;
every nonzero local kernel vector has colour support <=2: PROVED;
generic ambient kernel vector has colour support one:     PROVED;
one rank-two mode in each projection family:              PROVED NECESSARY;
classification/exclusion of simultaneous rank-two modes: OPEN;
unrestricted P_6 -> Delta_3:                              UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

Replay the exact checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_kernel_support_boundary.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_kernel_support_boundary.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_kernel_support_boundary.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_kernel_support_boundary.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_kernel_support_boundary.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_kernel_support_boundary.py
```

The primary verifier derives both kernel parametrizations and all ten
single contractions in exact symbolic arithmetic, checks the two generic
determinants and the `R direct-sum A` factorization, and exhausts the
two-dimensional cross-orthogonality lemma over several finite fields.  The
independent audit imports neither the primary verifier nor SymPy: it rebuilds
the complementary quartics from edge complementation, uses custom modular
row reduction for every projective kernel direction, checks the direct
square-free contraction identity, and independently exhausts the abstract
`A`-configuration.  These computations replay identities and stress-test
the case split; the written characteristic-zero argument proves the theorem.
