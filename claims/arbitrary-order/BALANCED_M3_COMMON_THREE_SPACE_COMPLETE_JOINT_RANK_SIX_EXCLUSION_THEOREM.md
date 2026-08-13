# Balanced `m=3` common-three-space complete joint-rank-six exclusion

## Status

**Exact characteristic-zero exclusion of every joint-cross-rank-six point on
the normalized, target-consistent physical `m=3` common-three-space
stratum.**  Let `U` be the total singleton span and put `K=image H`.  Assume

```text
dim U=3,                         rank H=6.             (1)
```

S2AB excludes one root--root block, S2AC excludes the shared-factor
derivative, and S2AE excludes the non-coordinate relation-plane alternative
of the transverse derivative.  This theorem excludes the last alternative:
the transverse two-root mechanism whose relation three-plane is contained in
a coordinate hyperplane.

Consequently every normalized target-consistent physical common-three-space
point has joint cross rank at most five.  This does **not** exclude joint rank
at most five, the other S2T/S2Q component types, higher balanced orders, the
all-rank-drop branch, a witness, or a counterexample.  Global Krenn--Gu
remains **UNRESOLVED**.

## 1. Coordinate relation and the forced rank-two row

Retain the transverse normal form, after permuting roots,

```text
B_23=B!=0,           B_13=C!=0,           B_12=0,
rank D_(B,C)=6,                                      (2)

D_(B,C)(a,b,c)=a tensor B+C tensor b.                (3)
```

As in S2AD,

```text
K=A_3 direct-sum K_12,       dim K_12=3,
U=D_(B,C)(K_12),                                    (4)
L=K_12^perp subset A_1^* direct-sum A_2^*, dim L=3. (5)
```

The remaining branch says that `L` lies in one of six coordinate
hyperplanes.  Exchange roots 1 and 2 if necessary, and rename the colour so
that

```text
L subset {u_s=0}.                                    (6)
```

Dualizing (6) gives

```text
(e_s,0) in K_12.                                     (7)
```

Write the involved transposed root rows as

```text
r_a=rho(e_a^*),              p_b=pi(e_b^*),          (8)
```

and let `Q=image theta` be the independent third-root row three-plane.
Equation (7) makes `rank pi<=2`.  The target-kernel argument of S2AD applies
without its non-coordinate hypothesis: for any `0!=v in ker pi`, the empty
permanent is killed by `v`, while target consistency can absorb `v(J)` only
on the single third-root line `(v tensor id)B`.  Every nonzero kernel vector
therefore has coordinate support one, and the kernel cannot have dimension
two.  Thus, for one colour `d`,

```text
rank pi=2,             ker pi=span(e_d^*),
p_d=0,                 B_(d,-)=kappa e_d, kappa!=0.  (9)
```

The same argument says that `rank rho` is either three or exactly two.  In
the latter case, for one colour `c`,

```text
rank rho=2,            ker rho=span(e_c^*),
r_c=0,                 C_(c,-)=kappa' e_c,
kappa'!=0.                                             (10)
```

We exclude the profiles `(3,2)` and `(2,2)` separately.

## 2. Two derivative lemmas

Let `W=X direct-sum Y direct-sum Z`.  For `u,v in W`, write

```text
M_(u,v)(q)=per(u,v,q).                                (11)
```

Thus `M_(u,v)` is the mixed-product derivative used in S2X and S2AC.

### Lemma 1 (binary five-product obstruction)

Let each of `X,Y,Z` have dimension two, let `Qbar subset W` have dimension at
least two, and suppose `r,u,v in W` satisfy

```text
M_(u,u)|Qbar=0,             M_(u,v)|Qbar=0,
M_(r,v)|Qbar=0,                                      (12)
```

while `M_(r,u)|Qbar` and `M_(v,v)|Qbar` are nonzero rank-one maps whose
decomposable image tensors have distinct factor lines in all three sources.
No such data exist.

#### Proof

Split according to the number of nonzero source components of `u`.

If all three are nonzero, write `u=(x,y,z)`.  The kernel of the square
derivative is exactly

```text
{(a x,b y,c z):a+b+c=0},                             (13)
```

of dimension two.  Hence `Qbar` equals (13).  Vanishing of `M_(u,v)` on the
two scaling differences says

```text
x tensor y' tensor z=x' tensor y tensor z
                     =x tensor y tensor z',          (14)
```

so `v` is proportional to `u`.  Its square also vanishes on (13), contrary
to (12).

If `u=(x,y,0)` has exactly two nonzero components, its square kernel is
`X direct-sum Y`, so `Qbar` lies there.  If the `Z` component `z'` of `v`
were nonzero, vanishing of `M_(u,v)` would put the at-least-two-dimensional
`Qbar` in the one-dimensional kernel of

```text
(q_X,q_Y) |-> q_X tensor y+x tensor q_Y.             (15)
```

Thus `z'=0`; but then the square of `v` also vanishes on `Qbar`.

It remains that `u=(x,0,0)` is pure.  If exactly one of the `Y,Z` components
of `v` is nonzero, the mixed zero condition kills the complementary
projection of `Qbar`, and the square of `v` vanishes.  If both are zero, its
square is zero as well.  Hence write

```text
v=(x',y',z'),                 y'z'!=0.                (16)
```

Then

```text
ker M_(u,v)=X direct-sum span(0,y',-z').             (17)
```

On this kernel, `M_(v,v)` is the map

```text
q_X |-> 2 q_X tensor y' tensor z'.                   (18)
```

Its rank-one restriction forces

```text
Qbar=span{(a,0,0),(0,y',-z')}                        (19)
```

for one nonzero `a in X`.  Vanishing of `M_(r,v)` first on `(a,0,0)` and
then on the second generator gives

```text
r_Y=lambda y',       r_Z=-lambda z',
lambda x'=0.                                         (20)
```

The map `M_(r,u)` is nonzero only if `lambda!=0`, so `x'=0`.  Its image is
the line `x tensor y' tensor z'`, while (18) has image
`a tensor y' tensor z'`.  The two target tensors share their `Y` and `Z`
factor lines, contrary to the hypothesis.  The cases are exhaustive.  QED.

### Lemma 2 (square-pencil factor sharing)

Let `X,Y,Z` be arbitrary finite-dimensional spaces, let `Q subset W` be a
three-plane, and suppose

```text
M_(u,u)|Q
```

is a nonzero rank-one map with decomposable image tensor `T`.  Then:

1. the mixed zero-divisor space

   ```text
   Z_(u,Q)={v in W:M_(u,v)|Q=0}                      (21)
   ```

   has dimension at most one;
2. if `M_(u,v)|Q` is a nonzero rank-one map with decomposable image `T'`,
   then `T` and `T'` share at least one source factor line.

#### Proof

A pure `u` has zero square, so it is impossible.

Suppose `u=(x,y,0)` has exactly two nonzero source components.  The square
is

```text
M_(u,u)(q)=2 x tensor y tensor q_Z.                  (22)
```

Thus `Q_0=Q intersect (X direct-sum Y)` has dimension two, the `Z`
projection of `Q` is one line `span(z_0)`, and

```text
T=x tensor y tensor z_0.                             (23)
```

Write `v=(x',y',z')`.  On `Q_0`,

```text
M_(u,v)(q)
 =(q_X tensor y+x tensor q_Y) tensor z'.             (24)
```

If (24) vanishes on the two-plane `Q_0`, then `z'=0`; evaluation on a lift
of `z_0` then gives

```text
x tensor y'+x' tensor y=0,
v=lambda(x,-y,0).                                    (25)
```

This proves that (21) is at most a line.  If the mixed image is instead one
nonzero decomposable line, either `z'=0`, when it shares `z_0`, or (24) has
rank one.  In the latter case its `X tensor Y` line is a decomposable point
of the Segre tangent at `x tensor y`, hence shares `x` or `y`.  This proves
the factor-sharing assertion.

Finally let `u=(x,y,z)` have three nonzero components.  Its square kernel is
the two-plane (13).  Since the restriction to `Q` has rank one,

```text
Q=ker M_(u,u) direct-sum span(q_0).                  (26)
```

The image `T` is decomposable in the Segre tangent at `x tensor y tensor z`,
so, after permuting sources, it has the form

```text
T=xi tensor y tensor z,
q_0 may be chosen as (xi,0,0).                       (27)
```

If `M_(u,v)` vanishes on (13), equation (14) again makes `v` proportional to
`u`; evaluation on `q_0` then makes `v=0`.  Thus (21) is zero in this case.

For a nonzero rank-one mixed image whose factor lines were all distinct from
those of (27), evaluate on the two scaling differences

```text
(x,-y,0),             (x,0,-z).                     (28)
```

The first value has fixed `Z` factor `z` and the second fixed `Y` factor
`y`.  Both must therefore vanish.  Their vanishing is exactly (14), so
`v` is proportional to `u`, whose mixed image is proportional to `T`, a
contradiction.  This proves both statements.  QED.

## 3. Profile `(3,2)`: the graph identity

Assume `rank rho=3`.  The projection `K_12->A_1` is an isomorphism, so

```text
K_12={(a,T a):a in A_1},                             (29)
ker T=span(e_s),                 image T=e_d^perp.   (30)
```

The row relation is

```text
p_b=sum_a T_(b,a) r_a.                               (31)
```

Target consistency gives an exact identity, not merely a selected slice.
Indeed the physical row `p_d` is zero.  Contracting the coefficient of any
nonroot monomial in the second-root coordinate `d` sends
`D_(B,C)(a,Ta)` to `kappa a tensor e_d`.  Hence every graph coefficient is
zero except the one correcting `T_d E_(d,d,d)`, and

```text
G_N=J-kappa^(-1) T_d D_(B,C)(e_d,T e_d).             (32)
```

For a fixed nonroot monomial and third-root row, let `F` be its `3 x 3`
matrix in the first two roots.  Equation (31) writes

```text
F=S T^T,
S_(a,i)=per(r_a,r_i,q),          S=S^T.              (33)
```

Thus `T F` is symmetric.  Applying this to every target coefficient
`T_i E_(i,i)` with `i!=d` gives

```text
T e_i in span(e_i).                                  (34)
```

### 3.1 The kernel and missing-row colours agree

First suppose `s=d`.  Equation (34) makes

```text
T e_i=tau_i e_i,             tau_i!=0, i!=s.        (35)
```

Thus `p_i=tau_i r_i`.  The correction in (32) has first-root coordinate
`s`, while the two other diagonal target rows are unaffected.  For the two
colours `i,j!=s`,

```text
M_(r_i,r_j)|Q=0,
M_(r_i,r_i)|Q and M_(r_j,r_j)|Q
  are nonzero rank-one maps onto T_i,T_j.             (36)
```

This is exactly the symmetric binary-diagonal obstruction proved as Lemma 1
of S2AE (and replayed independently there).  The target products have
distinct factor lines, so (36) is impossible.

### 3.2 The two colours differ

Now suppose `s!=d` and call the third colour `j`.  Equation (34) and (30)
give nonzero scalars `a,tau` and some `b` such that

```text
T e_s=0,             T e_d=a e_s+b e_j,
T e_j=tau e_j,                                      (37)

p_s=a r_d,          p_d=0,
p_j=b r_d+tau r_j.                                  (38)
```

Project each nonroot source space onto its two coordinate lines different
from `d`.  The correction in (32), which carries the pure nonroot monomial
`T_d`, vanishes.  The projected target is the binary diagonal

```text
T_s E_(s,s,s)+T_j E_(j,j,j).                         (39)
```

Let bars denote projected row vectors, set

```text
u=bar r_d,          v=bar p_j,
r=bar r_s,          Qbar=projected Q.                (40)
```

The root-3 flattening of (39) has rank two and factors through `Qbar`, hence
`dim Qbar>=2`.  Equations (38)--(39) give

```text
M_(u,u)|Qbar=M_(u,v)|Qbar=M_(r,v)|Qbar=0,            (41)
```

while `M_(r,u)|Qbar` and `M_(v,v)|Qbar` map onto the two distinct product
lines `T_s,T_j`.  Lemma 1 contradicts (41).  This excludes profile `(3,2)`.

## 4. Profile `(2,2)`: two independent square zero divisors

Assume now (10).  Since every first component of `K_12` has zero `c`-th
coordinate, (7) gives `c!=s`.  Contracting target consistency first in the
zero row `r_c` and then in `p_d` shows

```text
c!=d.                                                 (42)
```

If `d!=s`, the `T_d` coefficient puts `(e_d,0)` in `K_12`, independently of
the vector `(e_s,0)` in (7).  But

```text
dim(K_12 intersect A_1)=3-rank pi=1,                 (43)
```

a contradiction.  Therefore

```text
d=s.                                                  (44)
```

Let `j` be the remaining colour.  Coefficientwise contraction in the two
zero root rows gives the complete normal form

```text
K_12=span{(e_s,0),(0,e_c),(e_j,tau e_j)}, tau!=0,    (45)

r_c=0,              p_s=0,              p_j=tau r_j,
V=span(r_s,p_c,r_j),                                  (46)

G_N=J-kappa^(-1)T_s D_(B,C)(e_s,0)
       -(kappa')^(-1)T_c D_(B,C)(0,e_c).              (47)
```

The beta-zero root-block atlas of S2AD now becomes decisive.  It says that
one block is a coordinate monomial or one of the two blocks has coordinate
image.  In the latter alternative, its nonzero diagonal row in (9) or (10)
forces its common third-root form to be the same coordinate.  Hence in every
case

```text
B=kappa e_s tensor e_s
or
C=kappa' e_c tensor e_c.                              (48)
```

Exchange roots if needed and assume the first alternative.  Its term in
(47) cancels `T_s E_(s,s,s)` completely.  Put

```text
u=r_j.                                                (49)
```

The unaffected `(j,j)` root coefficient and (46) say

```text
M_(u,u)|Q is a nonzero rank-one map onto T_j.         (50)
```

The `(s,j)` coefficient is zero, so

```text
r_s in Z_(u,Q).                                       (51)
```

The `(j,c)` coefficient is either zero or a rank-one map onto the correction
line `T_c`.  If it is nonzero, Lemma 2 says its product image must share a
factor with `T_j`, whereas the two coordinate products share none.  Thus it
is zero and

```text
p_c in Z_(u,Q).                                       (52)
```

But `r_s,p_c` are independent by (46), while Lemma 2 makes `Z_(u,Q)` at most
one-dimensional.  This final contradiction excludes profile `(2,2)`.  The
case in which `C` is the monomial is symmetric.

## 5. Proof-topology consequence

Together with S2AB--S2AE, the common-three-space joint-rank frontier is now

```text
joint rank 9, 8, or 7:                                IMPOSSIBLE;
joint rank 6, one root block:                         IMPOSSIBLE;
joint rank 6, shared-factor derivative rank 5:        IMPOSSIBLE;
joint rank 6, transverse / non-coordinate relation:   IMPOSSIBLE;
joint rank 6, transverse / coordinate relation:       IMPOSSIBLE (here);

joint rank at most 5:                                 OPEN;
other physical component types and higher orders:    OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.       (53)
```

The next exact common-three-space obligation is joint rank at most five.  No
finite-field reconnaissance, numerical search, or genericity assumption is
used in the proof.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_complete_joint_rank_six_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_complete_joint_rank_six_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_complete_joint_rank_six_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_complete_joint_rank_six_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_complete_joint_rank_six_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_complete_joint_rank_six_exclusion.py
```

The primary verifier checks the coordinate-dual rank profiles, both graph
normal forms, all five binary products, the square-pencil kernels in their
two- and three-source charts, the two-rank-two normal form, and the monomial
root-block forcing.  The independent no-import audit reconstructs the maps
with `Fraction` arithmetic and separate row-oriented elimination.  The
arbitrary-vector, tangent-locus, and coefficientwise arguments above are the
proof.

## Dependencies

- [`BALANCED_M3_COMMON_THREE_SPACE_TRANSVERSE_RANK_SIX_BETA_ZERO_LOCALIZATION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_TRANSVERSE_RANK_SIX_BETA_ZERO_LOCALIZATION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_TRANSVERSE_RANK_SIX_ALIGNED_RANK_TWO_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_TRANSVERSE_RANK_SIX_ALIGNED_RANK_TWO_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_SIX_SHARED_FACTOR_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_SIX_SHARED_FACTOR_EXCLUSION_THEOREM.md)
