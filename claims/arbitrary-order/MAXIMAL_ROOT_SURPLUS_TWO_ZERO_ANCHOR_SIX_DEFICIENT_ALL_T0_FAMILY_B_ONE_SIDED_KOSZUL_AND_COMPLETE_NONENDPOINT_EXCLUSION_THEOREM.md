# Maximum-root surplus-two zero-anchor six-deficient all-`T_0` Family-B one-sided Koszul and complete nonendpoint exclusion

## Status

This is theorem package **GLS75**.  It closes the complete **nonendpoint**
outside chart of the last Family-B single-binary key

```text
S_0^3 T_0^3.
```

`GLS74` excluded the subchart on which both central probe shores have a
non-root coefficient at every triangle label.  The present theorem removes
that extra hypothesis.  First, a central label cannot have both shores
root-axis-only: the two nonzero binary target coefficients would force one
common physical four-port deck onto two independent pure-colour lines.
Thus every central label supplies at least one legal Koszul identity.

One identity is enough.  Coupling it to the complete `P_0Q_0` coefficient
forces every full one-port correction to vanish on its outside kernel line,
even though a four-dimensional full-row coboundary can remain.  It also
forces every complementary pair deck to vanish on the two appropriate
kernel lines.  Those are exactly the conclusions needed to rerun the
common-edge support argument.  In the one-central-edge case, the nonendpoint
pure-`P_3` normal form makes every active central row transverse to both
outside shore lines, so the one-sided identity kills the last kernel rows.

The P-common and Q-common outside endpoint charts remain open: their
complete parent map has a genuine kernel.  Hence the Family-B `r=3` typed
key is still open, no profile is removed, the inherited six-deficient
residual remains `98,355 / 81`, and the global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Dependencies and exact obligation

- `GLS61` supplies the complete six-open same-source identity and all legal
  partial uncontractions.
- `GLS69` supplies the six-deficient support tower and the binary target.
- `GLS70` identifies Family B as `S_0^3R_0^(3-r)T_0^r`.
- `GLS71` excludes `r<=2` and proves the endpoint-complete pure-`P_3`
  outside chart classification.
- `GLS74` supplies the full pair-deck and one-port expansions, the
  central-edge support equations, and the endpoint rank boundary.

The exact parent proposition is that no complete root-order-three
zero-anchor source realizes the Family-B `S_0^3T_0^3` key.  This theorem
proves that every such source, if one exists, lies on a P-common or Q-common
outside endpoint.  Success is a pointwise exclusion of every nonendpoint,
not a profile removal or global closure.

Work over a characteristic-zero field.  Relabel the binary triangle and
outside ports as

```text
T={0,1,2},                    O={3,4,5}.              (1)
```

## 1. Complete outside chart and physical decks

Write the two probe variables as `P_a,Q_a` and

```text
g_ij=p_i tensor q_j+q_i tensor p_j.
```

For one common physical edge array `W_ij`, the complete identity is

```text
sum_({i,j} subset {0,...,5}) g_ij tensor H_({0,...,5}-{i,j})
 =sum_(a=0)^2 mu_a P_aQ_a tensor_(i=0)^5 e_(i,a),
mu_0 mu_1 mu_2!=0.                                  (2)
```

At every outside `T_0` port put

```text
L_u=row J_u,                    K_u=ker J_u,          (3)
```

where `dim L_u=2`, `dim K_u=1`, and `e_(u,0) in L_u`.
The `P_0Q_0` coefficient at the central colour-zero word is the pure outside
equation

```text
G_34 tensor h_5+G_35 tensor h_4+G_45 tensor h_3
 =mu_0 e_(3,0)e_(4,0)e_(5,0),                       (4)
```

with `G_uv=U_uV_v+V_uU_v`.  On the nonendpoint chart of (4), after nonzero
scalings,

```text
p_u=P_0U_u,                  q_u=Q_0V_u,             (5)
```

and `(U_u,V_u)` is a basis of `L_u` at every outside port.  Transverse
projection of (4) gives

```text
h_u in L_u.                                           (6)
```

For `{i,j,k}=T`, `u in O`, and `{v,w}=O-{u}`, define

```text
A_i=W_jk(e_(j,0),e_(k,0)),
R_iu=W_iu(e_(i,0),-_u),                              (7)

C_i^u=A_iW_vw+R_jv tensor R_kw+R_kv tensor R_jw.    (8)
```

For a central row vector `z in span(e_(i,1),e_(i,2))`, put

```text
S_iu(z)=W_iu(z,-_u),

D_i^u(z)=A_iS_iu(z)
 +W_ij(z,e_(j,0))R_ku+W_ik(z,e_(k,0))R_ju.          (9)
```

These are full physical tensors, not independently chosen face data.

## 2. Both central shores cannot be root-axis-only

Write

```text
p_i=sum_(r=0)^2 P_r p_i^r,
q_i=sum_(r=0)^2 Q_r q_i^r.                          (10)
```

### Lemma 2.1 (central one-sided non-root activity)

For every `i in T`, at least one of

```text
(p_i^1,p_i^2),                 (q_i^1,q_i^2)         (11)
```

is nonzero.

### Proof

Suppose both pairs vanish at one label `i`, and put `{j,k}=T-{i}`.  For
`a=1,2`, take the full `P_aQ_a` coefficient of (2).  Every source pair
meeting `i` vanishes because `p_i^a=q_i^a=0`.  Every pair meeting an outside
port vanishes because (5) has only probe bidegree `P_0Q_0` there.  The sole
possible source pair is `{j,k}`, so

```text
(p_j^a tensor q_k^a+q_j^a tensor p_k^a)
 tensor H_({i} union O)
 =mu_a tensor_(ell=0)^5 e_(ell,a).                  (12)
```

The right side is nonzero and decomposable across the cut
`{j,k}|({i} union O)`.  Hence the same probe-independent physical deck
`H_({i} union O)` is proportional to

```text
e_(i,1) tensor_(u in O)e_(u,1)
```

from `a=1`, and to the independent pure-colour-`2` tensor from `a=2`.
This is impossible. `square`

Thus every central label supplies at least one of the two mixed-root
strict-parent coefficients used next.

## 3. One-sided Koszul/full-parent lemma

Put

```text
X_i=sum_(u in O) U_u tensor C_i^u,
Y_i=sum_(u in O) V_u tensor C_i^u.                   (13)
```

If some `q_i^r!=0`, `r=1,2`, the legal `P_0Q_r` coefficient gives `X_i=0`.
If some `p_i^r!=0`, the legal `P_rQ_0` coefficient gives `Y_i=0`.  The
source-pair separation is exact: after contracting the other two central
labels at their colour-zero kernels, only the three pairs joining `i` to an
outside label remain.  Tensoring by the selected nonzero local covector is
injective.

For any central row `z`, the complete `P_0Q_0` coefficient is

```text
Phi(D_i(z))+p_i^0(z)Y_i+q_i^0(z)X_i=0,              (14)

Phi(D)=G_34D^5+G_35D^4+G_45D^3.                    (15)
```

### Lemma 3.1 (one Koszul row suffices on the kernel lines)

Let `(X_u,Y_u)` be a basis of `L_u` at every outside port.  Suppose full pair
tensors `C^u`, full rows `D^u`, and a scalar `lambda` satisfy

```text
sum_u X_u tensor C^u=0,
Phi(D)+lambda sum_u Y_u tensor C^u=0.                (16)
```

Then, for `{v,w}=O-{u}`,

```text
C^u|_(K_v tensor K_w)=0,             D^u|_(K_u)=0. (17)
```

### Proof

Contract the first equation in (16) at `K_v tensor K_w`.  The two terms
whose displayed shore lies at `v` or `w` vanish; the remaining nonzero
`X_u` factor forces the first conclusion in (17).

For the second conclusion, fix `u` and project its slot to the
one-dimensional quotient `V_u^*/L_u`.  In the first equation, write the
projected components of the two pair tensors containing `u` as
`zbar_u tensor a_w` and `zbar_u tensor b_v`.  Their coefficient is

```text
X_v tensor a_w+b_v tensor X_w=0,
```

so for one scalar `t`,

```text
a_w=-tX_w,                       b_v=tX_v.           (18)
```

In the projected second equation, write `D^u mod L_u=d zbar_u`.  The two
independent binary words give

```text
d+lambda t=0,                    d-lambda t=0.       (19)
```

Characteristic zero gives `d=0`.  Thus `D^u in L_u`, proving (17).  Notice
that this holds even when `lambda=0`.  In that case `Phi` is injective and
actually gives `D=0`, while `C` lies in the eight-dimensional kernel of one
Koszul row.  If `lambda!=0`, scale it to one.  The complete `54 x 36` block
has rank `31` and nullity five: one alternating `C` parameter and four
full-row coboundaries.  Writing

```text
D^u=c_uX_u+d_uY_u,
```

those coboundaries satisfy

```text
c_3+c_4+c_5=0,                   d_3+d_4+d_5=0.      (19a)
```

They can remain as full rows, but (17) makes them invisible on the kernel
lines. `square`

Apply Lemma 3.1 at every central label, exchanging `U,V` when the available
identity is `Y_i=0`.  If both identities are present, (14) simply has
`lambda=0`; if the root-axis-only opposite shore is identically zero, the
same stronger case applies.  Lemma 2.1 guarantees at least one identity.
Consequently, for every `i,u,z`,

```text
C_i^u|_(K_v tensor K_w)=0,
D_i^u(z)|_(K_u)=0.                                  (20)
```

## 4. The common restricted physical system

Choose nonzero generators of the `K_u` and write

```text
rho_iu=R_iu|_(K_u),              b_vw=W_vw|_(K_v tensor K_w),
sigma_iu(a)=S_iu(e_(i,a))|_(K_u).                    (21)
```

Expanding (6), (8), (9), and (20) gives

```text
A_0rho_0u+A_1rho_1u+A_2rho_2u=0,                    (22)

A_i b_vw+rho_jv rho_kw+rho_jw rho_kv=0,             (23)

A_i sigma_iu(a)
 +W_ij(e_(i,a),e_(j,0))rho_ku
 +W_ik(e_(i,a),e_(k,0))rho_ju=0.                    (24)
```

The binary triangle uses the same outside physical edges:

```text
h_i(a)=b_45 sigma_i3(a)+b_35 sigma_i4(a)
      +b_34 sigma_i5(a).                             (25)
```

Contracting all three outside `T_0` kernel lines leaves nonzero target
factors in colours `1,2`.  Hence the family of rows in (25) cannot vanish
identically.

## 5. Three, two, and zero nonzero central coefficients

Assume first `A_0A_1A_2!=0`.  Put

```text
x_u=A_0rho_0u,              y_u=A_1rho_1u,
K_vw=A_0A_1A_2 b_vw.                                (26)
```

Eliminating `rho_2` from (22), the three instances of (23) give

```text
x_vx_w=y_vy_w,
x_vy_w+x_wy_v+y_vy_w=0,
K_vw=y_vy_w.                                         (27)
```

If every `b_vw` is zero, (25) is already impossible.  Choose a nonzero pair
`b_vw`.  Then `y_vy_w!=0`, and the two ratios satisfy

```text
r_vr_w=1,                       r_v+r_w+1=0.          (28)
```

They are the two distinct roots of `r^2+r+1`.  On the complementary port
`u`, if `y_u=0`, equation (27) forces `x_u=0`; otherwise the two adjacent
pairs would force the contradictory equalities
`r_u=r_v^(-1)=r_w^(-1)`.  Thus every `rho_iu` vanishes at `u`, and the other
two outside `b` values vanish.  Equation (24) kills every `sigma_iu(a)` at
the complementary port, so the sole possible term in (25) is zero.

Suppose exactly two `A_i` are nonzero, say `A_0=0` and `A_1A_2!=0`.  Put
`lambda=A_1/A_2`, so (22) gives `rho_2u=-lambda rho_1u`.  If

```text
S=rho_0v rho_1w+rho_0w rho_1v,
```

the `i=1,2` equations in (23) are

```text
A_1b_vw-lambda S=0,              A_2b_vw+S=0.       (29)
```

Their scaled difference is `2lambda S=0`, hence `S=b_vw=0` on every pair,
contradicting (25).

If all `A_i` vanish, then `h_u=sum_i A_iR_iu=0` in (4), contradicting its
nonzero pure target.

## 6. Exactly one nonzero central coefficient

Suppose only `A_1` is nonzero.  Equation (22) gives `rho_1u=0`, while

```text
h_u=A_1R_1u.                                          (30)
```

Because (4) is a **nonendpoint** pure-`P_3` chart, its exact six-edge normal
form has two nonzero chart parameters.  In one representative orientation,
after nonzero scalings,

```text
e_(3,0) proportional V_3,
e_(4,0) proportional U_4,
e_(5,0) proportional rU_5+sV_5,       rs!=0,

2h_3=-rU_3+sV_3,
2h_4= rU_4-sV_4,
2h_5= rU_5+sV_5.                                  (30a)
```

The other five orientations only permute ports and exchange the two shores.
Consequently, in every oriented chart,

```text
R_1u=a_uU_u+b_uV_u,                 a_u b_u!=0       (31)
```

at all three outside ports.  This is the precise point where the endpoint
boundary is retained.

Take the one available Koszul identity for central label `0`; its displayed
outside shore is either `X_u=U_u` for every `u` or `X_u=V_u` for every `u`.
Since `A_0=0`, contract that full identity at `K_v`.  The physical expansion
of `C_0` gives

```text
rho_2v (X_u tensor R_1w+R_1u tensor X_w)=0,
{u,v,w}=O.                                           (32)
```

The bracket is nonzero.  Indeed, `R_1u` is not proportional to either
`U_u` or `V_u` by (31); applying a functional that kills `X_u` but not
`R_1u` leaves a nonzero multiple of `X_w`.  Hence `rho_2v=0` for every `v`.

The same argument with the available identity for central label `2` gives
`rho_0v=0` for every `v`.  Finally (23) for central label `1`, which follows
from its own one available identity, reduces to

```text
A_1b_vw=0.
```

Thus every `b_vw=0`, contradicting (25).  The other one-coefficient cases
are symmetric.

### Theorem 6.1 (complete Family-B nonendpoint exclusion)

No complete zero-anchor root-order-three source in the Family-B
`S_0^3T_0^3` key realizes an outside nonendpoint pure-`P_3` chart.

## 7. Exact retained endpoint and frontier

At a P-common or Q-common outside endpoint, equation (31) fails in the
selected orientation and the parent map `Phi` has a genuine kernel.  In the
row-basis endpoint activity model, the exact ranks from `GLS74` are

```text
opposite-shore activity 3:       rank 6, kernel 0;
opposite-shore activity 2:       rank 4, kernel dimension 2;
opposite-shore activity 1:       rank 3, kernel dimension 3.             (33)
```

The lower two ranks are sharp for the `P_0Q_0` row.  A next theorem must use
mixed complete coefficients to detect these endpoint kernel directions; it
may not reuse the nonendpoint transverse argument silently.

```text
Family B r=3 outside nonendpoint:                    EMPTY;
Family B r=3 P/Q-common outside endpoints:            OPEN;
Family B r=3 typed key:                               OPEN;
unchanged inherited six-deficient residual:    98,355 / 81;
global Krenn--Gu conjecture:                    UNRESOLVED.              (34)
```

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_all_t0_family_b_one_sided_koszul_and_complete_nonendpoint_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_all_t0_family_b_one_sided_koszul_and_complete_nonendpoint_exclusion.py
```

The primary verifier builds the one-sided Koszul/full-parent matrix over the
rationals, checks its five-dimensional alternating-plus-coboundary kernel,
proves that every one-port transverse coordinate is forced to zero, and
replays the central support eliminations.  The no-import audit reconstructs
the block over a finite field, checks every forced-zero coordinate by row
space membership, and independently exhausts the nonendpoint transversality
and binary source-pair support controls.

The legality of the mixed-root coefficient rows, the full-source support in
(12), the physical expansions (8)--(9) and (25), and the endpoint scope are
written mathematics.  Neither program proves the endpoint charts empty,
removes the typed key, or proves the global conjecture.
