# Balanced `m=3` joint-rank-five Hilbert--Burch repeated-coordinate localization

## Status

**Exact characteristic-zero localization on the `(1,1,1)` Hilbert--Burch
boundary of the normalized, target-consistent physical `m=3`
common-three-space full-sensor stratum.**  Let `U` be the total singleton
span, put `K=image H`, and assume

```text
dim U=3,                         rank H=5.             (1)
```

In the three-root Hilbert--Burch `(1,1,1)` profile, normalize the derivative
kernel and the three nonzero root--root blocks as

```text
ker D_B=span{(x,0,z),(0,y,z)},

B_23=-y tensor z,       B_13=-x tensor z,
B_12= x tensor y.                                      (2)
```

S2AG proves that at least two of `x,y,z` are target-coordinate vectors.  The
new conclusion is:

> If two factors are proportional to the same target coordinate `e_s`, then
> the remaining factor has zero `e_s` coordinate.

For example, after a root permutation, write the two nonzero proportionality
scalars explicitly:

```text
x=lambda e_s, y=mu e_s,
lambda mu!=0                    implies z_s=0.        (3)
```

In particular, the all-same-coordinate triangle
`x=y=z=e_s` is impossible.  The proof uses the complete untouched binary
root cube, not a finite sample.  Its exact three-plane incidence lemma says
that a polarized `3 x 3` permanent on three two-planes cannot be the binary
diagonal `Delta_2`.  Equal planes fall to the already proved two-plane
square obstruction; the two distinct plane arrangements fall to exact
cubic-kernel calculations.

This is a localization, not a complete `(1,1,1)` exclusion.  It leaves the
boundary in which the third factor lies in the complementary coordinate
plane, the coordinate-distinct `(1,1,1)` charts, the `(1,1,2)` and
`(1,2,2)` Hilbert--Burch profiles, joint rank at most four, other physical
components and pole strata, higher orders, and the global conjecture open.
Global Krenn--Gu remains **UNRESOLVED**.

The successor S2AO now excludes a genuinely two-supported third factor on
that complementary plane.  Thus the repeated-coordinate residual is the
discrete factor-line pattern `(s,s,t)` with `s!=t`; S2AP excludes those
patterns and hence closes the repeated-coordinate chart.  These successors
do not change the scope or proof below.

## 1. The repeated-coordinate Hilbert--Burch grid

Use (2) and suppose, after permuting the three roots,

```text
x=lambda e_s, y=mu e_s,
lambda mu!=0,               z_s!=0.                  (4)
```

Let `u,v` be the two colours different from `s`.  The derivative is

```text
D_B(a,b,c)
 =-mu a tensor e_s tensor z
  -lambda e_s tensor b tensor z
  +lambda mu e_s tensor e_s tensor c.               (5)
```

Every coefficient of (5) whose first two root colours lie in `{u,v}` is
zero.  Since `U=D_B(K)`, the complete target equation therefore gives

```text
per(r_a,p_b,q_k)=delta_(a,b,k) T_k,
a,b in {u,v},                  k in {0,1,2},         (6)
```

where

```text
r_a=rho(e_a^*),        p_b=pi(e_b^*),
q_k=theta(e_k^*),      T_k=X_k tensor Y_k tensor Z_k. (7)
```

Because `z_s!=0`, there are unique covectors `gamma_u,gamma_v in z^perp`
whose restrictions to `span(e_u,e_v)` are the two coordinate covectors:

```text
gamma_i(e_j)=delta_(i,j),       i,j in {u,v}.        (8)
```

Put

```text
q'_i=theta(gamma_i).                                   (9)
```

Contracting (6) by (8) gives the exact binary cube

```text
per(r_a,p_b,q'_c)=delta_(a,b,c)T_c,
a,b,c in {u,v}.                                    (10)
```

All six rows in (10) lie in one three-plane.  Indeed
`ker D_B subset K` by S2AG, and the image under `H^T` of the covectors
annihilating `ker D_B` is

```text
V=H^T((ker D_B)^perp),

dim V=dim((ker D_B)^perp)-dim K^perp=7-4=3.         (11)
```

The first two families in (10) annihilate the two kernel generators because
their colours differ from `s`; the third family does so because
`gamma_i(z)=0`.  Thus, inside `V`, put

```text
R=span(r_u,r_v),
P=span(p_u,p_v),
Q=span(q'_u,q'_v).                                  (12)
```

Each is a two-plane.  For example, a dependence between `r_u,r_v`, applied
to the two diagonal and crossed entries of (10), would make one nonzero
`T_i` vanish.  The other two families are symmetric.

## 2. A three-plane cannot carry a binary diagonal permanent frame

We isolate the exact obstruction used by (10).

### Lemma 1 (three-plane binary-diagonal frame obstruction)

Let `W=X direct-sum Y direct-sum Z` over a characteristic-zero field.  Let
`V subset W` have dimension three, and let `R,P,Q subset V` be two-planes
with ordered bases

```text
(r_0,r_1),              (p_0,p_1),              (q_0,q_1). (13)
```

There are no two decomposable tensors `T_0,T_1` with distinct factor lines
in all three sources such that

```text
per(r_a,p_b,q_c)=delta_(a,b,c)T_c,
a,b,c in {0,1}.                                    (14)
```

### Proof

For every source-coordinate line, restriction to `V` is a linear form on
`V`.  Choose coordinate bases extending the factor lines of `T_0,T_1` and
write these forms as

```text
xi_i, eta_j, zeta_k in V^*,        i,j,k in {0,1,2}. (15)
```

Let

```text
Res:S^3 V^* -> R^* tensor P^* tensor Q^*             (16)
```

send a cubic to its symmetric polarization restricted to `R x P x Q`.
The `(i,j,k)` source coefficient of (14) is exactly

```text
Res(xi_i eta_j zeta_k).                              (17)
```

Hence (17) vanishes for every coordinate triple except `(0,0,0)` and
`(1,1,1)`, while those two exceptions are nonzero.

Let `alpha,beta,gamma` be normals to `R,P,Q`.  We split according to their
incidence in the three-space `V`.

#### Two planes agree

Suppose first that `R=P`; the other equalities are symmetric.  There is an
invertible `2 x 2` matrix `L` with

```text
p_b=sum_i L_(b,i)r_i.                                (18)
```

For fixed `q`, put

```text
F_(a,b)=per(r_a,p_b,q),
S_(a,i)=per(r_a,r_i,q).                              (19)
```

Then `S` is symmetric, `F=S L^T`, and therefore `L F=L S L^T` is
symmetric.  At `q_0` and `q_1`, equation (14) makes `F` respectively a
nonzero multiple of `E_00` and `E_11`.  Thus `L E_00` and `L E_11` are
symmetric, so `L` is diagonal.  Equation (14) becomes

```text
per(r_0,r_1,Q)=0,

per(r_0,r_0)|Q and per(r_1,r_1)|Q are nonzero
rank-one maps onto T_0 and T_1.                      (20)
```

The exact two-plane square-pencil lemma of S2AL forbids (20), because
`T_0,T_1` are fully transverse.

We may therefore assume that `R,P,Q` are pairwise distinct.

#### Three independent normals

If `alpha,beta,gamma` are independent, use them as coordinates `A,B,C` on
`V`.  A direct eight-coefficient comparison in (16) gives

```text
ker Res=span(A^3,B^3,C^3).                           (21)
```

We use one elementary divisor fact.  If two nonzero completely split
cubics in the plane (21) share a quadratic divisor, then they are
proportional.  Indeed, a diagonal cubic with three nonzero coefficients is
smooth and cannot be a union of lines.  A nonpure split member of (21) is
therefore a binary sum `a A^3+b B^3`, up to coordinates.  Its three line
factors are distinct, and even one noncoordinate factor fixes both the
coordinate pair and the ratio `a:b`.  A pure cube sharing a repeated factor
with another diagonal cubic forces that cubic to be the same pure cube.

Now the two mixed coefficients

```text
xi_0 eta_1 zeta_0,            xi_0 eta_1 zeta_1      (22)
```

belong to (21) and share the quadratic factor `xi_0 eta_1`.  The four
factors in the two nonzero target terms make every form displayed in (22)
nonzero.  The divisor fact gives `zeta_0 proportional zeta_1`.  Using in
turn

```text
xi_0 eta_0 zeta_1,            xi_0 eta_1 zeta_1,

xi_0 eta_0 zeta_1,            xi_1 eta_0 zeta_1      (23)
```

gives `eta_0 proportional eta_1` and
`xi_0 proportional xi_1`.  Consequently the supposedly nonzero diagonal
product `xi_0 eta_0 zeta_0` is proportional to the mixed product
`xi_0 eta_0 zeta_1` in `ker Res`, a contradiction.

#### Three distinct normals in a pencil

It remains that the normals are pairwise distinct but span a two-plane.
After rescaling, take

```text
alpha=A,                 beta=B,              gamma=A+B. (24)
```

Another direct coefficient comparison gives

```text
ker Res=span(A^3,B^3,AB(A+B))
       subset S^3 N,
N=span(A,B) subset V^*.                              (25)
```

Every product in (17) other than the two target diagonals belongs to (25).
For any `xi_i`, choose nonzero `eta_b,zeta_c` from the two target products
so that `(i,b,c)` is not `(0,0,0)` or `(1,1,1)`.  Then

```text
0!=xi_i eta_b zeta_c in S^3 N.                      (26)
```

Unique factorization, or reduction modulo `N`, makes each of its three
linear factors belong to `N`.  Thus every nonzero `xi_i` lies in `N`.
The same argument applies to every `eta_j,zeta_k`.  But the coordinate
forms in (15) together separate points of the embedded space `V subset W`,
so they span `V^*`.  Equation (25) would put that three-space inside the
two-plane `N`, the final contradiction.

The equal-plane, independent-normal, and distinct-pencil cases exhaust all
incidences of three two-planes in a three-space.  This proves the lemma.
QED.

## 3. Repeated-coordinate localization

Equations (10)--(12) satisfy Lemma 1 with the two fully transverse pure
targets `T_u,T_v`.  This contradicts (4).  Therefore

```text
x=lambda e_s, y=mu e_s,
lambda mu!=0        implies             z_s=0.      (27)
```

The Hilbert--Burch normal form and permanent are symmetric under permutation
of the three roots.  Hence the same conclusion holds whenever any two of
`x,y,z` are the same target-coordinate line: the remaining factor lies in
the complementary coordinate hyperplane.

The hypothesis `z_s!=0` is load-bearing.  If `z_s=0`, the restriction map

```text
z^perp -> span(e_u,e_v)^*,
gamma |-> (gamma(e_u),gamma(e_v))                    (28)
```

has rank one, not two; its determinant in the natural charts is a nonzero
multiple of `z_s`.  Thus (8)--(10) do not produce a binary diagonal frame.
This is an exact boundary statement, not a witness or evidence that the
remaining hyperplane case is realizable.

## 4. Proof-topology consequence

The joint-rank-five three-root frontier now refines to

```text
Hilbert--Burch (1,1,1):
  two equal coordinate factors and remaining same-colour
  coordinate nonzero:                               IMPOSSIBLE;
  two equal coordinate factors and remaining factor
  in the complementary coordinate plane:            OPEN;
  coordinate-distinct / other allowed coordinate charts: OPEN;

Hilbert--Burch (1,1,2), (1,2,2):                    OPEN;
joint rank at most four / other physical branches:   OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.       (29)
```

The all-same-coordinate rank-one triangle is excluded as a strict special
case of (27).  No numerical specialization, finite-field promotion, or
generic-point assumption is used.

The successor S2AO further localizes the open complementary-plane line in
(29): its genuinely two-supported part is impossible, leaving only the
coordinate patterns `(s,s,t)` with `s!=t`.  S2AP excludes those discrete
patterns exactly.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_localization.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_localization.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_localization.py
```

The primary replay checks the Hilbert--Burch derivative and kernel, the
complete untouched root grid, the `z_s` contraction determinant, all three
plane-incidence kernels in (21) and (25), the diagonal-cubic divisor
calculation, and the equal-plane matrix orientation.  The independent audit
imports no repository module and no third-party package; it reconstructs
the derivative, contractions, polarization kernels, and boundary determinant
with standard-library `Fraction` elimination and a different coefficient
ordering.  The scripts replay displayed identities; the arbitrary-factor
divisor and unique-factorization arguments are the proof above.

## Dependencies

- [Joint-rank-five derivative and torus localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md)
- [Support-one higher-row-rank exclusion and two-plane square lemma](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md)
