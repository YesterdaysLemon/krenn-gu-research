# Kernel-support covers obstruct the order-twelve cofactor torus

## Status

**Exact characteristic-zero structural obstruction.**  Let
`H_0,...,H_5` be arbitrary four-row, three-column common-row matrices and
let

```text
J_H=Lambda_H(ker Lambda_H^off) subset span{e_0^6,e_1^6,e_2^6}.
```

For any two distinct modes `u,v` and kernel vectors `z_u,z_v`, double
contraction leaves exactly a scalar restriction of `P_4`.  The exact theorem
`subrank(P_4)=2` therefore shows that two fully supported kernel vectors are
already incompatible with a torus point of `J_H`.

For any three distinct modes `p,q,r` and any choices `z_u in ker H_u`, triple
contraction kills the whole cofactor image.  Consequently, if `J_H` meets the
coefficient torus, then

```text
z_p hadamard z_q hadamard z_r=0                    (1)
```

for every such triple and every such choice of kernel vectors.

This gives two further no-torus strata.  In particular, the double-contraction
result strengthens three fully supported modes to just two.  More generally,
four common-row matrices cannot each have a kernel vector supported on at
least two target colours.  The latter conclusion follows from an exact three-
colour support cover: among four subsets of size at most one, some three fail
to cover all three colours.

The theorem applies to arbitrary blocker blocks `W_uv`; therefore it also
excludes the effective subfamily

```text
W_uv=a_u^T b_v+b_u^T a_v.
```

It does not classify cores outside these kernel-support strata, construct a
torus-intersecting `J_H`, settle effective-block realizability there, or
settle an unrestricted `P_6 -> Delta_3`.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## The cofactor map

For a target word `w in {0,1,2}^6` and an unordered pair `u<v`, put

```text
K_uv(w)
 =per([H_m[i,w_m]]_(i=0,...,3; m notin {u,v})).     (2)
```

For fifteen arbitrary `3 x 3` blocks define

```text
[w] Lambda_H(W)
 =sum_(u<v) W_uv[w_u,w_v] K_uv(w).                  (3)
```

As before, `Lambda_H^off` is obtained by deleting the three constant target
words.  If `W` lies in its kernel, then `Lambda_H(W)` is diagonal, and its
three diagonal coefficients form a point of `J_H`.

## Double-kernel contraction and `P_4`

Fix two distinct modes `u,v` and choose

```text
z_u in ker H_u,       z_v in ker H_v.                (4)
```

Contract (3) at these two modes.  Every edge summand other than `{u,v}`
contains at most one of the contracted modes.  The other contracted mode is
therefore a column of its four-row permanent, and contraction replaces that
column by zero.  Only the `{u,v}` summand survives, giving the exact identity

```text
Contr_{u,v}(Lambda_H(W);z_u,z_v)
 =W_uv(z_u,z_v) P_4(H_m:m notin {u,v}).               (5)
```

Here the tensor on the right is the pullback of the four-row permanent by the
four remaining common-row matrices.  Suppose `Lambda_H(W)` is diagonal with
all three coefficients `d_c` nonzero.  Its double contraction is

```text
sum_c d_c z_u[c]z_v[c] e_c^4.                        (6)
```

Let `S_uv=supp(z_u) intersect supp(z_v)`.  When `S_uv` is nonempty, (6) is a
weighted concise diagonal on exactly those colours.  The scalar on the right
of (5) cannot vanish, and the remaining four-mode pullback must itself be that
weighted diagonal.  The exact characteristic-zero theorem `subrank(P_4)=2`
in
[`FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md`](FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md)
therefore forces

```text
|supp(z_u) intersect supp(z_v)|<=2.                  (7)
```

Thus a torus point of `J_H` permits at most one fully supported kernel mode.
Two support-two kernel vectors missing the same colour force a binary
diagonal `P_4` deletion on their common support; if they miss distinct
colours, they force a pure one-colour deletion.  These are necessary deletion
types, not constructions.

## Triple-kernel contraction

Fix three modes

```text
S={p,q,r}
```

and vectors `z_s in ker H_s` for `s in S`.  Contract (3) by the three
vectors `z_s`.  Consider one summand indexed by an edge `{u,v}`.  The edge
can contain at most two members of `S`, so choose

```text
s in S\{u,v}.                                        (8)
```

Mode `s` occurs as one of the four columns in the permanent (2).  Summing
that target coordinate against `z_s` replaces this column by

```text
sum_c z_s[c] H_s[:,c]=H_s z_s=0.                    (9)
```

The permanent is linear in each column, so the contracted `{u,v}` summand
is zero.  This is termwise in the fifteen edge summands: it uses no
cancellation between blocks and no assumption on `W`.  Hence

```text
Contr_S(Lambda_H(W); z_p,z_q,z_r)=0                (10)
```

for every `W`.

Suppose now that

```text
Lambda_H(W)=d_0 e_0^6+d_1 e_1^6+d_2 e_2^6.         (11)
```

Contracting (11) at the same three modes leaves the diagonal three-mode
tensor

```text
sum_c d_c z_p[c]z_q[c]z_r[c] e_c^3.                (12)
```

The three displayed basis tensors are linearly independent.  If all `d_c`
are nonzero, equations (10)--(12) therefore force (1).

## Exact support consequences

Write

```text
Z(z)={c:z[c]=0}.                                    (13)
```

For a torus point of `J_H`, equation (1) is equivalent to the necessary
cover condition

```text
Z(z_p) union Z(z_q) union Z(z_r)={0,1,2}.           (14)
```

The double-contraction theorem already shows that two fully supported kernel
vectors are impossible; (14) supplies the finer three-mode support cover.

If `z` has support at least two, then `|Z(z)|<=1`.  Given four such kernel
vectors, if one zero set is empty then any triple containing it covers at
most two colours.  Otherwise the four zero sets are singletons; two of them
are equal, and a triple containing that repeated pair again covers at most
two colours.  Either case contradicts (14).  Therefore

```text
J_H meets (C^*)^3
 => at most three modes admit a kernel vector of support at least two.
                                                               (15)
```

In the extremal three-mode case, (14) says more: the three chosen vectors
must each have support exactly two and must miss three distinct colours.
Their three pairwise support intersections are the three distinct singleton
colours.  Hence every corresponding block scalar in (5) is nonzero, and the
three complementary four-mode cofactors are weighted pure tensors on those
three colours.  In particular even one fully supported vector is impossible
in that extremal triple.

For rank-two `H_u`, the kernel is a line.  Hence (15) says that, outside at
most three modes, every rank-two kernel occurring in a surviving core must
be a target coordinate line (unless that mode has rank three).  This is a
necessary condition only, not a construction.

## Application to the zero-cofactor core

The first three matrices of the exact zero-cofactor core in
[`SIX_BLOCKER_ORDER12_ZERO_QUOTIENT_COFACTOR_SYZYGY.md`](SIX_BLOCKER_ORDER12_ZERO_QUOTIENT_COFACTOR_SYZYGY.md)
have kernel generators

```text
z_0=(-3,1,1),       z_1=(2,-2,1),       z_2=(1,1,0). (16)
```

Their coordinatewise product is

```text
z_0 hadamard z_1 hadamard z_2=(-6,-2,0)!=0.          (17)
```

The first two vectors are fully supported, so the double-contraction theorem
already proves that this core's `J_H` misses the coefficient torus.  The
nonzero triple product supplies a second proof from the support cover.  The
earlier exact rank computation gives the strictly stronger fixed-core identity
`J_H=0`; the present theorem supplies independent structural explanations of
the no-torus part without row reducing the `726 x 135` cofactor matrix.

The nonzero diagonal-cofactor example deliberately lies outside this
corollary: four of its kernel lines are coordinate lines, and only two admit
support-at-least-two vectors.  Its separate exact computation
`J_H=span(-1,1,0)` is therefore consistent with, but not implied by, the
support-cover theorem.

## Boundary

```text
two fully supported common-row kernel modes: EXCLUDED by subrank(P_4)=2;
four support-at-least-two common-row kernel modes: EXCLUDED;
arbitrary W_uv on those strata: EXCLUDED before factorisation;
cores satisfying the support-cover condition: UNKNOWN;
torus-intersecting J_H outside these strata: UNKNOWN;
effective two-row factorisation on surviving cores: UNKNOWN;
global Krenn--Gu conjecture: UNRESOLVED.
```

## Replay

```text
python claims/arbitrary-order/verify_six_blocker_order12_kernel_support_cover_no_torus_p6.py
python claims/arbitrary-order/audit_six_blocker_order12_kernel_support_cover_no_torus_p6.py

uv run --with sympy python claims/arbitrary-order/verify_fourth_order_permanent_subrank.py
python claims/arbitrary-order/audit_fourth_order_permanent_subrank.py
```

The primary verifier checks the double- and triple-contraction edge ledgers,
universal permanent-column linearity, exact rational contraction instances,
the zero-core kernel application, and the complete support-cover ledger.  The
no-import audit independently reconstructs a different instance and both
contraction identities.  The separate `P_4` package proves the
characteristic-zero subrank theorem and keeps its finite-field audit
explicitly separate.  No finite-field inference is used.
