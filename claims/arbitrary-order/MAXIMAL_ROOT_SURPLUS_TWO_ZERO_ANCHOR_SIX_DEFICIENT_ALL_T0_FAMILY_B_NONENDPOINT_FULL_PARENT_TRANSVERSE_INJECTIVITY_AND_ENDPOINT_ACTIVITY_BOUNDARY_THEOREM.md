# Maximum-root surplus-two zero-anchor six-deficient all-`T_0` Family-B nonendpoint full-parent transverse injectivity and endpoint-activity boundary

## Status

This is theorem package **GLS74**.  It returns to the complete six-open
same-source identity on the last Family-B single-binary key

```text
S_0^3 T_0^3
```

and excludes the **central-mixed-support nonendpoint** chart of its outside
pure-`P_3` coefficient.  Here central mixed support means that, at every
triangle label, the `p` shore has some non-`P_0` coefficient and the `q`
shore has some non-`Q_0` coefficient.  The three strict-parent pair decks
then have a one-dimensional
alternating Koszul camouflage.  That camouflage vanishes on all three
outside kernel lines, which is why the earlier descendants do not see it.
In the complete parent, however, the three one-port corrections enter the
injective map

```text
(D_3,D_4,D_5) -> G_34 D_5+G_35 D_4+G_45 D_3.
```

They therefore vanish as full covectors.  Coupling that conclusion back to
the common physical edges makes the nonzero binary triangle impossible for
every support pattern of the three central all-zero edge coefficients.

Two residuals are different.  If a central `p` shore is `P_0`-only or a
central `q` shore is `Q_0`-only, one of the two Koszul identities used below
is unavailable.  At an outside endpoint, the same full-parent map also has
a genuine kernel because one outside shore is not common.  Both residuals
remain open.  Hence this is an exact characteristic-zero source-chart
exclusion, not a profile removal.  The inherited six-deficient residual
remains `98,355 / 81`, and the global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Dependencies and parent obligation

- `GLS61` supplies the complete zero-anchor six-open identity and every
  same-source partial-uncontraction.
- `GLS69` supplies the exact six-deficient support tower.
- `GLS70` identifies Family B as the exact-three-set binary leaf
  `S_0^3R_0^(3-r)T_0^r`.
- `GLS71` excludes `r<=2` and supplies the endpoint-complete pure-`P_3`
  chart classification.

The exact parent proposition is that no complete root-order-three
zero-anchor source realizes the Family-B `S_0^3T_0^3` key.  The present
theorem resolves its central-mixed-support nonendpoint chart by combining
the three strict parents, their shared physical pair decks, the complete
`F_00` row, and the binary triangle.  Central root-axis degeneracies and the
outside endpoint charts are the declared residuals of that same parent
attempt.

## 0. Complete identity and the nonendpoint chart

Let

```text
T={0,1,2},                 O={3,4,5}
```

be the binary triangle and its outside ports.  Write the two probe variables
as `P_a,Q_a`, and let

```text
g_ij=p_i tensor q_j+q_i tensor p_j.
```

For one common physical edge array `W_ij`, let `H_I` be its perfect-matching
tensor on the even label set `I`.  The full identity is

```text
sum_({i,j} subset {0,...,5}) g_ij tensor H_({0,...,5}-{i,j})
 =sum_(a=0)^2 mu_a P_aQ_a tensor_(i=0)^5 e_(i,a),
mu_0 mu_1 mu_2!=0.                                  (1)
```

At each triangle port of type `S_0`, the row plane is
`span(e_(i,1),e_(i,2))` and its kernel is the colour-zero line.  At every
outside `T_0` port put

```text
L_u=row J_u,                    K_u=ker J_u,          (2)
```

so `dim L_u=2`, `dim K_u=1`, and `e_(u,0) in L_u`.

Take the `P_0Q_0` coefficient of (1), evaluate the three triangle slots at
`e_(0,0),e_(1,0),e_(2,0)`, and leave the outside slots open.  Only outside
source pairs survive.  Thus

```text
G_34 tensor h_5+G_35 tensor h_4+G_45 tensor h_3
 =mu_0 e_(3,0)e_(4,0)e_(5,0),                       (3)
```

where `G_uv=U_uV_v+V_uU_v` and

```text
U_u=[P_0]p_u,             V_u=[Q_0]q_u,
h_u=[e_(0,0)e_(1,0)e_(2,0)]H_(012u).                (4)
```

By the exact pure-`P_3` chart theorem, a nonendpoint of (3) has, after
nonzero scalings,

```text
p_u=P_0 U_u,               q_u=Q_0 V_u,             (5)
```

and `(U_u,V_u)` is a basis of `L_u` for every `u in O`.  This theorem treats
the subchart of (5) on which, after writing

```text
p_i=sum_(r=0)^2 P_r p_i^r,       q_i=sum_(r=0)^2 Q_r q_i^r,   i in T,
```

one has

```text
(p_i^1,p_i^2)!=(0,0),            (q_i^1,q_i^2)!=(0,0)
for every i in T.                                      (5a)
```

The central root-axis degeneracies excluded by (5a), and the P-common and
Q-common outside endpoint charts, are retained in Section 6.

Projecting (3) at port `u` to `V_u^*/L_u` leaves only
`G_vw tensor (h_u mod L_u)`.  Since `G_vw!=0`,

```text
h_u in L_u.                                          (6)
```

## 1. The strict-parent Koszul decks

For `{i,j,k}=T`, `u in O`, and `{v,w}=O-{u}`, define

```text
A_i=W_jk(e_(j,0),e_(k,0)),
R_iu=W_iu(e_(i,0),-_u),                              (7)

C_i^u=H_(jkvw)(e_(j,0),e_(k,0),-_v,-_w)
     =A_i W_vw+R_jv tensor R_kw+R_kv tensor R_jw.    (8)
```

Condition (5a) lets the two mixed-root coefficients of the exact
target-zero strict parents give

```text
sum_(u in O) U_u tensor C_i^u=0,
sum_(u in O) V_u tensor C_i^u=0.                     (9)
```

These are complete tensors, not only restrictions to the kernel lines.
Indeed, contract the other two `S_0` triangle labels at their colour-zero
kernels and retain `i` and all three outside labels.  Choose
`r in {1,2}` with the local covector `q_i^r!=0`.  The `P_0Q_r`
coefficient has exactly the three `i`--outside source pairs and is

```text
q_i^r tensor sum_u U_u tensor C_i^u=0.
```

There is no outside-pair contribution because every outside companion in
(5) has probe bidegree `P_0Q_0`.  Over a field, tensoring by a nonzero
covector is injective, so tensor-factor cancellation gives the first
equation in (9).  A nonzero
`p_i^r`, `r in {1,2}`, and the `P_rQ_0` coefficient give the second equation
in exactly the same way.  Every target coefficient is zero because the two
contracted triangle labels have colour zero while the open `i` coefficient
lies in its `S_0` row.  If either half of (5a) fails, this coefficient
separation supplies only one Koszul identity and the argument below is not
asserted.

### Lemma 1.1 (the common alternating kernel)

Equations (9) force one scalar `tau_i` such that

```text
C_i^3=tau_i(U_4 tensor V_5-V_4 tensor U_5),
C_i^4=tau_i(V_3 tensor U_5-U_3 tensor V_5),
C_i^5=tau_i(U_3 tensor V_4-V_3 tensor U_4).          (10)
```

### Proof

Complete `(U_u,V_u)` to a basis at each outside port.  The coefficient blocks
containing a third-basis vector are injective under the two shore equations
in (9), so all such coefficients vanish.  The remaining map has twelve
unknown binary coefficients.  In those binary coordinates, the
`V`-shore/`000` row and the `U`-shore/`111` row vanish identically; the other
fourteen rows have rank eleven in characteristic zero.  Direct coefficient
elimination leaves exactly the alternating generator (10).
Equivalently, the full `54 x 27` coefficient matrix has rank `26`.
`square`

The right sides of (10) vanish on `K_v tensor K_w`, because every `U,V`
belongs to `L=Ann(K)`.

## 2. Full-parent transverse injectivity

For `a in {1,2}` define the full spoke row and its one-port matching deck

```text
S_iu(a)=W_iu(e_(i,a),-_u),

D_i^u(a)=[e_(i,a)e_(j,0)e_(k,0)]H_(012u)
 =A_i S_iu(a)
  +W_ij(e_(i,a),e_(j,0))R_ku
  +W_ik(e_(i,a),e_(k,0))R_ju.                       (11)
```

Take the full `P_0Q_0` coefficient of (1) on the central local word in
(11), leaving all outside slots open.  Pairs inside `O` give

```text
G_34D_i^5(a)+G_35D_i^4(a)+G_45D_i^3(a).             (12)
```

The only possible additional pairs use `i` and one outside port.  If the
selected `P_0,Q_0` coefficients of `p_i,q_i` on `e_(i,a)` are `x_i(a)` and
`y_i(a)`, their sum is

```text
x_i(a) sum_u V_u C_i^u+y_i(a) sum_u U_u C_i^u=0     (13)
```

by (9).  Pairs using `j` or `k` have zero local colour-zero rows.  The mixed
target coefficient is zero.  Hence (12) vanishes.

### Lemma 2.1 (injectivity of the outside parent map)

If `(U_u,V_u)` is a basis of `L_u`, then

```text
G_34D_5+G_35D_4+G_45D_3=0                           (14)
```

implies `D_3=D_4=D_5=0`.

### Proof

Project (14) at port `u` to `V_u^*/L_u`.  Only the term with `D_u` in that
slot survives, so first `D_u in L_u`.  Write

```text
D_u=c_uU_u+d_uV_u.
```

The six mixed binary words give

```text
c_3+c_4=c_3+c_5=c_4+c_5=0,
d_3+d_4=d_3+d_5=d_4+d_5=0.                           (15)
```

Characteristic zero gives every `c_u=d_u=0`.  In coordinates the complete
map in (14) has rank nine. `square`

Consequently

```text
D_i^u(a)=0       for all i,u and a=1,2.              (16)
```

## 3. Kernel equations on common physical edges

Choose nonzero generators of `K_u` and write

```text
rho_iu=R_iu|_(K_u),              b_vw=W_vw|_(K_v tensor K_w),
sigma_iu(a)=S_iu(a)|_(K_u).                              (17)
```

Equation (6), expanded with (7), gives at every outside port

```text
A_0rho_0u+A_1rho_1u+A_2rho_2u=0.                    (18)
```

Restricting (8) and (10) to `K_v tensor K_w` gives, for every
`{i,j,k}=T`,

```text
A_i b_vw+rho_jv rho_kw+rho_jw rho_kv=0.             (19)
```

Restricting (16) to `K_u` gives

```text
A_i sigma_iu(a)
 +W_ij(e_(i,a),e_(j,0))rho_ku
 +W_ik(e_(i,a),e_(k,0))rho_ju=0.                    (20)
```

Finally the two nonzero colours of the binary triangle are supplied by the
same outside edges and spokes:

```text
h_i(a)=b_45 sigma_i3(a)+b_35 sigma_i4(a)
      +b_34 sigma_i5(a).                             (21)
```

If every tensor in (21) vanishes, the binary target vanishes, which is
impossible.

## 4. Three and two nonzero central coefficients

Assume first `A_0A_1A_2!=0`.  Put

```text
x_u=A_0rho_0u,                 y_u=A_1rho_1u,
K_vw=A_0A_1A_2 b_vw.                                (22)
```

Eliminate `rho_2u` by (18).  The three equations (19) on an outside pair
`{v,w}` say

```text
K_vw=x_vy_w+x_wy_v+2y_vy_w
    =2x_vx_w+x_vy_w+x_wy_v
    =-(x_vy_w+x_wy_v).                              (23)
```

Because the characteristic is not two,

```text
x_vx_w=y_vy_w,
x_vy_w+x_wy_v+y_vy_w=0,
K_vw=y_vy_w.                                         (24)
```

If every `b_vw` is zero, (21) already contradicts the binary target.  Choose
`b_vw!=0`.  Then the ratios `r_v=x_v/y_v`, `r_w=x_w/y_w` satisfy

```text
r_vr_w=1,                    r_v+r_w+1=0.            (25)
```

Thus they are the two distinct roots of `r^2+r+1`.  Apply (24) to each pair
containing the complementary outside port `u`.  If `y_u=0`, then
`x_vx_u=y_vy_u=0` and `x_v!=0` force `x_u=0`.  If `y_u!=0`, its ratio is
defined and the two pairs force
`r_u=r_v^(-1)=r_w^(-1)`, impossible because these two inverses are distinct.
In either case,

```text
x_u=y_u=0,
rho_0u=rho_1u=rho_2u=0.                             (26)
```

Equations (24) also make the other two outside `b` values zero.  Now (20)
and `A_i!=0` kill every `sigma_iu(a)` at the complementary port.  The sole
possible term in each (21) is therefore zero, a contradiction.

Suppose exactly two central coefficients are nonzero, say
`A_0=0`, `A_1A_2!=0`.  Put `lambda=A_1/A_2`.  Equation (18) gives

```text
rho_2u=-lambda rho_1u.
```

For each outside pair let

```text
S=rho_0v rho_1w+rho_0w rho_1v.
```

The `i=1,2` instances of (19) are

```text
A_1b_vw-lambda S=0,             A_2b_vw+S=0.        (27)
```

Their difference after scaling is `2lambda S=0`; hence `S=b_vw=0`.  This holds on
all three pairs and again kills (21).

## 5. One or zero nonzero central coefficients

Suppose only `A_1` is nonzero.  Equation (18) gives `rho_1u=0`.  Moreover

```text
h_u=A_1R_1u in L_u.                                  (28)
```

At least one full row `R_1s` is nonzero, or the pure equation (3) would
vanish.  Use the complete tau forms (10), not only their kernel
restrictions.  Restrict `C_0^u` in one outside slot to its kernel.  Since
`C_0^u=R_1vR_2w+R_2vR_1w` and the alternating right side vanishes whenever
one slot is in a kernel, it gives

```text
rho_2v R_1w=0,                 R_1v rho_2w=0.        (29)
```

The identical restriction of `C_2^u` gives (29) with `rho_0` in place of
`rho_2`.  Consequently, if the activity set

```text
M={u:R_1u!=0}
```

has at least two ports, every `rho_0u,rho_2u` vanishes.  If `M={s}`, those
two kernel rows can be supported only at `s`.  In either case, on every
unordered pair of distinct outside ports,

```text
rho_0v rho_2w+rho_0w rho_2v=0.
```

The `i=1` equation (19) and `A_1!=0` therefore give `b_vw=0` for all pairs,
contradicting (21).  The other one-coefficient cases are symmetric.

If all three `A_i` vanish, (7) gives `h_u=0` for every port, immediately
contradicting (3).  These four support sizes exhaust the nonendpoint chart.

### Theorem 5.1 (central-mixed-support nonendpoint Family-B `r=3` exclusion)

No complete zero-anchor root-order-three source in the Family-B
`S_0^3T_0^3` key realizes a nonendpoint outside pure-`P_3` chart satisfying
the central mixed-support condition (5a).

## 6. Central root-axis and endpoint boundaries

If some `p_i` is `P_0`-only or some `q_i` is `Q_0`-only, the corresponding
`P_rQ_0` or `P_0Q_r` coefficient used in Section 1 is identically zero.
The `F_00` coefficient cannot replace it: on the same central local word it
contains both the outside-pair aggregate (12) and the missing Koszul sum.
Thus the complete alternating form (10), the cancellation (13), and the
individual conclusion (16) are not yet available.  These central root-axis
degeneracies remain open even when the outside pure-`P_3` chart is a
nonendpoint.

The same injectivity statement is false at an endpoint.  For a P-common
endpoint write

```text
p_u=P_0U_u,
M={u:[Q_0]q_u!=0}.                                   (30)
```

In the row-basis model where every displayed nonzero `Q_0` coefficient
provides the second basis vector `V_u`, the `P_0Q_0` outside map has the
exact ranks

```text
|M|=3:                         rank 6, kernel 0;
M={3,4}:                       rank 4, kernel dimension 2;
M={3}:                         rank 3, kernel dimension 3. (31)
```

For `M={3,4}` its kernel contains, in the row bases, the two directions

```text
(-V_3,V_4,0),                 (-U_3,-U_4,U_5),       (32)
```

and for `M={3}` it has the family

```text
(D_3,-cU_4,cU_5).                                   (33)
```

These ranks are a sharp endpoint boundary control, not an exhaustive
classification of endpoint row coincidences.  Thus `F_00` alone does not
kill the endpoint corrections.  A next theorem
must use a mixed full coefficient `F_(0r)`, `r=1,2`, whose source pair on
the selected endpoint detects the kernel direction whenever the
complementary mixed edge is active.  The Q-common endpoint is symmetric.

The restricted equations themselves are sharp.  Over any characteristic-
zero field containing a primitive cube root `omega`, take `A_i=1` and

```text
(rho_03,rho_13,rho_23)=(0,0,0),
(rho_04,rho_14,rho_24)=(omega,1,omega^2),
(rho_05,rho_15,rho_25)=(omega^2,1,omega),
b_45=1,                         b_34=b_35=0.          (34)
```

Every equation (18)--(19) holds.  This is not a full source, but it proves
that the full-parent conclusion (16), rather than the kernel equations
alone, is load-bearing.

## 7. Exact frontier

```text
Family B r=3 central-mixed-support nonendpoint:        EMPTY;
Family B r=3 central root-axis degeneracies:            OPEN;
Family B r=3 P/Q-common outside endpoints:              OPEN;
Family B r=3 typed key:                                OPEN;
unchanged inherited six-deficient residual:     98,355 / 81;
global Krenn--Gu conjecture:                     UNRESOLVED.             (35)
```

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_all_t0_family_b_nonendpoint_full_parent_transverse_injectivity.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_all_t0_family_b_nonendpoint_full_parent_transverse_injectivity.py
```

The primary verifier builds the full Koszul and parent coefficient matrices,
checks their ranks and alternating generator, verifies the three- and
two-nonzero-`A` scalar eliminations, exhausts the one-`A` activity supports,
and computes the endpoint rank drop.  The no-import audit reconstructs both
maps over a finite field, exhausts the all-`A` scalar system over `F_7`, and
checks the exact cube-root boundary independently.

The source-pair provenance of (9), cancellation (13), physical expansions
(8), (11), and (21), and the conclusion that central root-axis degeneracies,
endpoint charts, and the typed key remain open are written mathematics.
Neither program proves the global conjecture or recomputes the inherited
residual.
