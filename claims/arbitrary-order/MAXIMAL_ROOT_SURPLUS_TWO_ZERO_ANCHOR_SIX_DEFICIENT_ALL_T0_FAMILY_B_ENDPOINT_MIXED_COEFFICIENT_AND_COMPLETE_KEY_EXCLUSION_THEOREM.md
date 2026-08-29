# Maximum-root surplus-two zero-anchor six-deficient all-`T_0` Family-B endpoint mixed coefficient and complete key exclusion

## Status

This is exact characteristic-zero theorem package **GLS76**.  It closes the
P-common and Q-common outside endpoint charts left by `GLS75` and therefore excludes the
complete last Family-B single-binary key

```text
S_0^3T_0^3.
```

The endpoint rank drop of the isolated `P_0Q_0` parent map is genuine, but
it is not a source-integrability obstruction.  At a P-common endpoint, use
all three complete `P_0Q_s` coefficients together.  Their components in the
two-dimensional central row plane force every complementary pair deck to
vanish on the two outside kernel lines and every one-port correction to
vanish on its outside kernel line.  This remains true when a central `p`
shore is `P_0`-only or identically zero and when its transverse `Q`
functional is synchronized with one or all outside transverse functionals.

The support-three, support-two, and support-zero central-edge cases then
transfer from `GLS75`.  In support one, the endpoint signs are load-bearing.
Every inactive central label kills its remaining kernel row at the selected
outside endpoint.  Hence both outside kernel edges meeting that endpoint
vanish, while the active central label kills the sole spoke that could use
the opposite edge.  The nonzero binary target is impossible.

The Q-common chart follows by probe-shore exchange.  Thus the sixty labelled
Family-B `r=3` profiles and their one key are removed.  The inherited
six-deficient residual falls from `98,355 / 81` to `98,295 / 80`.  Family A
`r=1,2,3`, every other six-deficient branch, the lower-deficient branches,
and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Dependencies and exact obligation

- `GLS61` supplies the complete six-open same-source identity and every
  legal partial uncontraction.
- `GLS69` supplies the six-deficient support tower and binary target.
- `GLS70` identifies Family B as `S_0^3R_0^(3-r)T_0^r`.
- `GLS71` excludes `r<=2` and supplies the endpoint-complete pure-`P_3`
  outside classification.
- `GLS74` supplies the physical pair-deck and one-port expansions and the
  exact endpoint rank drop.
- `GLS75` excludes every outside nonendpoint and proves that every central
  label has at least one non-root probe shore.

The exact parent proposition is that no complete zero-anchor root-order-three
source realizes the Family-B `S_0^3T_0^3` key.  The only residual after
`GLS75` is a P-common or Q-common endpoint of the outside pure-`P_3`
coefficient.  Success here is a pointwise exclusion of both endpoint types,
hence removal of this one typed key.  It is not a closure of any other
six-deficient key or of the global conjecture.

Work over a characteristic-zero field.  Put

```text
T={0,1,2},                         O={3,4,5}.          (1)
```

## 1. P-common endpoint normal form

Write the complete identity as

```text
sum_({i,j} subset {0,...,5})
 (p_i tensor q_j+q_i tensor p_j) tensor H_({0,...,5}-{i,j})
 =sum_(a=0)^2 mu_a P_aQ_a tensor_(ell=0)^5 e_(ell,a),
mu_0mu_1mu_2!=0.                                      (2)
```

At every outside `T_0` port let

```text
L_u=row J_u,                         K_u=ker J_u,
dim L_u=2,                           dim K_u=1.        (3)
```

Take a P-common endpoint.  After permuting outside ports and making nonzero
local rescalings, the endpoint-complete `GLS71` normal form is

```text
p_u=P_0U_u,
q_u=sum_(s=0)^2 Q_s q_u^s,                            (4)

q_3=Q_0V_3,
h_3=-cU_3,                 h_4=cU_4,       h_5=cU_5,
c!=0.                                                    (5)
```

Here every `U_u,q_u^s` lies in `L_u`, and the coefficient rows of `q_u`
together with `U_u` span `L_u`.  Choose `V_u` completing `U_u` in `L_u` and
write, for `t=(t_0,t_1,t_2)`,

```text
q_u(t)=sum_s t_s q_u^s=A_u(t)U_u+B_u(t)V_u,
B_u in (K^3)^*,                   B_u!=0.             (6)
```

The nonzero conditions on the three `B_u` are precisely the local joint-rank
conditions.  No independence, nonsynchronization, or genericity among their
projective lines is assumed.

For `{i,j,k}=T`, `u in O`, and `{v,w}=O-{u}`, retain the physical tensors of
`GLS74`--`GLS75`:

```text
A_i=W_jk(e_(j,0),e_(k,0)),
R_iu=W_iu(e_(i,0),-_u),                              (7)

C_i^u=A_iW_vw+R_jv tensor R_kw+R_kv tensor R_jw,     (8)

D_i^u(z)=A_iW_iu(z,-_u)
 +W_ij(z,e_(j,0))R_ku+W_ik(z,e_(k,0))R_ju.          (9)
```

All are components of the same physical edge array.

## 2. The complete mixed endpoint coefficients

For triples `C=(C^3,C^4,C^5)` and `D=(D^3,D^4,D^5)`, put

```text
K_t(C)=sum_(u in O) q_u(t) tensor C^u,
K_U(C)=sum_(u in O) U_u tensor C^u,                  (10)

Phi_t(D)=sum_({v,w}=O-{u})
 (U_v tensor q_w(t)+q_v(t) tensor U_w) tensor D^u.  (11)
```

Tensor factors in (10)--(11) are placed in their labelled outside slots.
Contract the two central labels other than `i` at their colour-zero rows,
retain the full central `S_0` row plane at `i`, and take the linear
combination `sum_s t_s[P_0Q_s]` of (2).  Its target is zero on that central
row plane and its exact source-pair separation is

```text
Phi_t(D_i)+p_i^0 tensor K_t(C_i)+q_i(t) tensor K_U(C_i)=0.  (12)
```

The first term comes from outside--outside source pairs.  The second and
third terms are respectively the `p_i`--outside-`q` and
`q_i`--outside-`p` pairs.  Thus (12) retains precisely the terms that are
absent from an isolated `P_0Q_0` endpoint map; no proper-face or
independently chosen deck is inserted.

If some `p_i^r`, `r=1,2`, is nonzero, the complete `P_rQ_s` strict-parent
coefficients have no outside--outside term because every outside `p` shore
has only `P_0` support.  Every pair meeting either contracted central label
vanishes on its `S_0` colour-zero row, and the diagonal target vanishes
because the retained central row has colour `1` or `2` while the other two
central slots were fixed at colour zero.  The only possible source pairs are
therefore `{i,u}`, `u in O`.  Factoring the selected nonzero `p_i^r` gives

```text
K_t(C_i)=0                       for every t.         (13)
```

## 3. Endpoint kernel restriction

### Lemma 3.1 (a central mixed-`P` coefficient)

If (13) holds, then for every `u`, every central row `z`, and
`{v,w}=O-{u}`,

```text
C_i^u|_(K_v tensor K_w)=0,       D_i^u(z)|_(K_u)=0. (14)
```

### Proof

Choose one `t` outside the union of the three proper hyperplanes
`B_u(t)=0`.  Then `(U_u,q_u(t))` is a basis of `L_u` at every outside port.
Equation (12), after using (13), and the one-sided full-parent lemma of
`GLS75` apply with the two outside shores exchanged if necessary.  That
lemma gives exactly (14).  Such a `t` exists over the infinite
characteristic-zero base field. `square`

It remains to treat a central `p` shore with no non-root coefficient.  Write

```text
p_i=P_0a,                                             (15)
```

where `a` lies in the two-dimensional `S_0` row plane and may be zero.

### Lemma 3.2 (nonzero root-only central shore)

Suppose `a!=0`.  Complete it to a central basis `(a,b)` and write

```text
q_i(t)=alpha(t)a+beta(t)b,            beta!=0,
D_i=a tensor D_a+b tensor D_b.                       (16)
```

Then (12) implies (14), with no condition on the projective incidences among
`beta,B_3,B_4,B_5`.

### Proof

The two central components of (12) are

```text
Phi_t(D_b)+beta(t)K_U(C_i)=0,                         (17)
Phi_t(D_a)+K_t(C_i)+alpha(t)K_U(C_i)=0.              (18)
```

First fix `u` and evaluate (18) on `K_v tensor K_w`.  Every `Phi_t` term
vanishes, and in each Koszul sum only the term displayed at `u` survives.
If

```text
xi_u=C_i^u|_(K_v tensor K_w),
```

the result is

```text
(q_u(t)+alpha(t)U_u)xi_u=0             for every t.  (19)
```

The transverse coefficient of the displayed vector-valued functional is
`B_u!=0`, so `xi_u=0`.  This proves the first half of (14).

Now project outside slot `u` to its one-dimensional quotient by `L_u`.
Because the pair tensors already vanish on two kernel lines, write the two
possibly surviving projected pair components as

```text
pi_u(C_i^v)=N_u tensor (xU_w+yV_w),
pi_u(C_i^w)=N_u tensor (zU_v+dV_v),                  (20)
```

for a quotient generator `N_u`.  Let `delta_b,delta_a` be the projected
coefficients of `D_b^u,D_a^u`.  Comparing the `V_vU_w`, `U_vV_w`, and
`U_vU_w` words in (17) gives the following identities of linear forms in
`t`:

```text
delta_b B_v+beta d=0,
delta_b B_w+beta y=0,
delta_b(A_v+A_w)+beta(x+z)=0.                        (21)
```

The `V_vV_w` word of (18) is

```text
yB_v+dB_w=0.                                         (22)
```

If `delta_b!=0`, the first two equations in (21) make `B_v,B_w`
nonzero multiples of `beta`; substituting those multiples into (22) gives
a nonzero multiple of

```text
2yd beta=0.
```

The same first two equations make `y,d` nonzero, so characteristic zero is
a contradiction.  Hence `delta_b=0`.  Equations (21) then give

```text
y=d=0,                         x+z=0.                (23)
```

The `V_vU_w` and `U_vV_w` words of (18), after (23), are

```text
(delta_a+x)B_v=0,              (delta_a+z)B_w=0.     (24)
```

Thus `x=z=-delta_a`; together with `x+z=0` and characteristic zero this
gives `delta_a=0`.  Therefore both central components of every `D_i^u`
vanish on `K_u`, proving the second half of (14). `square`

### Lemma 3.3 (zero central `p` shore)

Suppose `a=0`.  Then (12) still implies (14).

### Proof

Since the joint central row map has rank two, the coefficient span of `q_i`
is the whole central row plane.  Choose a basis in which

```text
q_i(t)=alpha(t)a'+beta(t)b',
```

with independent nonzero linear forms `alpha,beta`.  The two components of
(12) are

```text
Phi_t(D_alpha)+alpha(t)K_U(C_i)=0,
Phi_t(D_beta)+beta(t)K_U(C_i)=0.                     (25)
```

Evaluation on `K_v tensor K_w` in either nonzero component immediately gives
`C_i^u|_(K_v tensor K_w)=0`.

Use (20) and let `delta_gamma` be the projected coefficient of
`D_gamma^u`.  For `gamma=alpha,beta`, comparison of the three binary words
gives

```text
delta_gamma B_v+gamma d=0,
delta_gamma B_w+gamma y=0,
delta_gamma(A_v+A_w)+gamma(x+z)=0.                  (26)
```

If `delta_alpha!=0`, the first two equations make `alpha` proportional to
both `B_v` and `B_w`.  Independence makes `delta_beta=0`; the beta equations
then give `d=y=x+z=0`, and the alpha equations force
`delta_alpha=0`, a contradiction.  Thus `delta_alpha=0`, and symmetry gives
`delta_beta=0`.  This is the second half of (14). `square`

By `GLS75`, both central shores cannot be root-axis-only.  Lemmas 3.1--3.3
therefore exhaust every central label and prove

```text
C_i^u|_(K_v tensor K_w)=0,
D_i^u(z)|_(K_u)=0                    for all i,u,z.  (27)
```

Notice that the proof did not transport a restriction from a kernel line to
an off-kernel target vector.  It retained all mixed complete coefficients
and compared their labelled tensor grades directly.

The conclusion is deliberately only (27), not full vanishing of `C_i,D_i`.
Endpoint coboundaries remain.  For example, suppressing central factors and
using labelled outside slots,

```text
D_a^3=-U_3,             D_a^4=U_4,              D_a^5=0,
C^3=-U_4 tensor U_5,    C^4=U_3 tensor U_5,      C^5=0              (27a)
```

satisfies `Phi_t(D_a)+K_t(C)=0` and `K_U(C)=0` for every `q(t)`.
Every tensor in (27a) already obeys the kernel restrictions (27), which are
exactly what the common physical system below uses.  Thus the proof neither
asserts endpoint-map injectivity nor silently discards the genuine endpoint
kernel recorded by `GLS74`.

## 4. The inherited common physical system

Choose generators of the outside kernel lines and put

```text
rho_iu=R_iu|_(K_u),
b_vw=W_vw|_(K_v tensor K_w),
sigma_iu(z)=W_iu(z,-_u)|_(K_u).                     (28)
```

The endpoint rows (5), the physical expansions (7)--(9), and (27) give the
same restricted system as `GLS75`:

```text
A_0rho_0u+A_1rho_1u+A_2rho_2u=0,                    (29)

A_i b_vw+rho_jv rho_kw+rho_jw rho_kv=0,             (30)

A_i sigma_iu(z)
 +W_ij(z,e_(j,0))rho_ku+W_ik(z,e_(k,0))rho_ju=0.   (31)
```

The binary triangle uses the same physical outside edges and spokes:

```text
h_i(z)=b_45sigma_i3(z)+b_35sigma_i4(z)
      +b_34sigma_i5(z).                              (32)
```

The support-three, support-two, and support-zero cases for
`(A_0,A_1,A_2)` use only (29)--(32).  Their `GLS75` proofs therefore transfer
verbatim: support three leaves at most one outside kernel edge and kills its
only attachment, support two forces every `b_vw=0`, and support zero makes
the nonzero outside row (5) vanish.

## 5. The one-central-edge endpoint

Suppose exactly one `A_i` is nonzero.  By central permutation take

```text
A_1!=0,                       A_0=A_2=0.              (33)
```

Equation (29) gives `rho_1u=0`, and (5) gives

```text
R_13=-lambda U_3,
R_14= lambda U_4,
R_15= lambda U_5,                lambda!=0.          (34)
```

We first prove

```text
rho_03=rho_23=0.                                    (35)
```

For central label `0`, if some non-root `p_0^r` is nonzero, (13) is
available.  Choose `t` with `B_4(t)!=0` and contract `K_t(C_0)=0` at `K_3`.
Using `A_0=0` and `rho_13=0` gives

```text
rho_23(q_4(t) tensor R_15+R_14 tensor q_5(t))=0.    (36)
```

The bracket is nonzero by its transverse component at port `4`, so
`rho_23=0`.

If the `p_0` shore is root-axis-only, `GLS75` says that `q_0` has a non-root
component.  In Lemma 3.2 use its `b` component, or in Lemma 3.3 use any
nonzero component of (25).  Contract that complete equation at `K_3`.
Every `Phi_t` term vanishes by (27), so for some nonzero central functional
one obtains

```text
K_U(C_0)|_(K_3)=0.
```

Its physical expansion is

```text
rho_23(U_4 tensor R_15+R_14 tensor U_5)
 =2lambda rho_23 U_4 tensor U_5=0,                  (37)
```

and characteristic zero again gives `rho_23=0`.  Applying the same argument
to central label `2` proves `rho_03=0`, establishing (35).

Equation (30) for the active label `1` now gives

```text
b_34=b_35=0.                                         (38)
```

Finally (31) for `i=1,u=3` and (35) give

```text
sigma_13(z)=0                      for every z.       (39)
```

Equations (32), (38), and (39) make the complete binary-target flattening at
central label `1` vanish.  This contradicts the two nonzero pure-colour rows
supplied by `mu_1,mu_2`.  The other two support-one cases are central
permutations.

### Theorem 5.1 (complete Family-B `r=3` exclusion)

No complete zero-anchor root-order-three source in the Family-B
`S_0^3T_0^3` key realizes a P-common outside endpoint.  By exchanging
`p,P,U` with `q,Q,V`, no such source realizes a Q-common endpoint.  Together
with `GLS75`, the complete key is empty.

## 6. Exact frontier delta

`GLS71` counted sixty labelled profiles in the Family-B `r=3` key.  Removing
that complete key changes only the six-deficient residual:

```text
Family B r<=2:                                      EMPTY;
Family B r=3 outside nonendpoint (`GLS75`):          EMPTY;
Family B r=3 P/Q-common endpoints (`GLS76`):         EMPTY;
Family B complete single-binary family:             EMPTY;

removed here:                                  60 / 1 key;
six-deficient residual:                 98,355 / 81
                                     -> 98,295 / 80;
Family A r=1,2,3:                                    OPEN;
global Krenn--Gu conjecture:                   UNRESOLVED.              (40)
```

No claim is made about the remaining three Family-A single-binary keys,
other binary/pure/zero-triangle profiles, other deficient-map counts,
nonzero anchor, arbitrary root order, or the response/selector/receiver and
local-to-global attachment obligations.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_all_t0_family_b_endpoint_mixed_coefficient_and_complete_key_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_all_t0_family_b_endpoint_mixed_coefficient_and_complete_key_exclusion.py
```

The primary verifier reconstructs the P-common endpoint tensor, replays the
root-only projection elimination symbolically, checks the zero-shore
independence fork, verifies the selected-port support-one signs, and checks
the exact residual subtraction.  The no-import audit independently
enumerates all projective functional incidences over a finite field of odd
characteristic, rebuilds the endpoint tensor and local projected systems,
and rechecks the count delta.

The source-pair provenance of (12)--(13), the passage from full mixed rows to
the physical restrictions (27), the shared-edge expansions (29)--(32), and
the characteristic-zero support-one argument are written mathematics.  The
programs do not prove any other key empty and do not resolve the global
conjecture.
