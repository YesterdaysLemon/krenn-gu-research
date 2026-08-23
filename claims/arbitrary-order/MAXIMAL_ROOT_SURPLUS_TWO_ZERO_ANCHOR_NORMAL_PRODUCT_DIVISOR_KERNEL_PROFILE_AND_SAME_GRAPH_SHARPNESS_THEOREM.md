# Maximum-root surplus-two zero-anchor normal-product divisor kernel profile and same-graph sharpness

## Status

**Exact characteristic-zero arbitrary-root kernel identity, four-port divisor
profile, and same-graph sharpness theorem.**  Continue `GLS29` on its remaining
normal-product divisor

```text
0<|S_gamma|<3,
S_gamma={c:gamma_c=n_0(c)n_1(c)!=0}.                  (1)
```

Contracting every complement port by its local two-channel kernel isolates one
supplier and gives a diagonal-versus-supplier identity with no division.  At
four promoted ports this yields exact one-active and two-active projected-
kernel profiles, including every zero-star and response-zero fibre.

Neither profile is contradictory from the scalar normal data.  For each of
`|S_gamma|=1,2`, there is an exact rational same-graph normal-slice control
with all six physical pair responses nonzero and every target's normal
nuisance image full.  The complete `GLS29` normal mixed identity holds
exactly.  A second one-active control additionally has a maximum torus root,
outside incidence defect four within the surplus-two bound six, and all three
pure coefficients one.  It still fails original mixed GHZ coefficients.
These controls are not points of the
complete hypothetical-witness locus: the normal slice does not certify the
full `GLS26` top reconstruction, the full `GLS22` nuisance problem, or any
other probe-root contraction.

This is `GLS30`.  It refutes exclusion from the complete scalar normal identity
plus six nonzero responses and full normal images alone.  It separately shows
that maximum-root incidence and pure normalization do not upgrade the same
scalar identity to a complete witness.  A coupling of maximum-root incidence
to simultaneous normal absorption remains open, as do another root channel
and the full physical mixed/nuisance equations.  It does not close the
zero-anchor branch, the strategic node, or the conjecture.  The global
Krenn--Gu status remains **UNRESOLVED**.

## Dependencies and notation

Use

- [`GLS22`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md) for the exact full/transverse target quotient;
- [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md) for the complete labelled nuisance;
- [`GLS26`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ZERO_ANCHOR_DIAGONAL_RECONSTRUCTION_AND_RESIDUAL_SHORE_COVER_THEOREM.md) for top reconstruction, branch P, and `L`;
- [`GLS28`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TARGET_ENVELOPE_PRODUCT_SELECTOR_AND_BOUNDED_REDUNDANT_COVER_THEOREM.md) for the redundant-cover boundary; and
- [`GLS29`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_TWO_SHORE_NORMAL_CHANNEL_AND_INTERSECTING_SUPPLIER_EXCLUSION_THEOREM.md) for the rank-two-shore normal channel and complete mixed identity.

Retain the `GLS29` pointwise hypotheses and notation

```text
(d_0,d_1)=(2,2),              L=H=E/P_Q(T_Q), dim H=1,
omega=0,                      p!=0,
k_(uv)=x_u tensor y_v+y_u tensor x_v,
Z_u=span{x_u,y_u},
sum_D k_D tensor R_(Uhat-D)
  =sum_c beta_c e_c^(tensor Uhat),
beta_c=alpha_c gamma_c.                              (2)
```

The physical source is over `K=C`; the linear-algebra statements hold over a
characteristic-zero field.  No response, kernel coordinate, supplier minor,
normal product, or nuisance minor is inverted.

Regard `x_u,y_u` as covectors and put

```text
K_u=ker x_u intersect ker y_u subset V_u.             (3)
```

For subspaces of coordinate spaces, `star` denotes the linear span of all
coordinatewise products.

## 1. Arbitrary-root complement-kernel identity

For a promoted pair `D={i,j}`, write `C=Uhat-D`.  Choose arbitrary
`z_u in K_u` for every `u in C`, and put

```text
z_C=star_(u in C) z_u,
R_C(z_C)=R_C((z_u)_(u in C)).                         (4)
```

### Theorem 1 (denominator-free supplier isolation)

The complete normal identity in (2) gives

```text
D_beta(z_C)=R_C((z_u)_(u in C)) k_D,                 (5)
```

where

```text
D_beta(z)=sum_(c in S_gamma) beta_c z(c)
              e_(i,c)^* tensor e_(j,c)^*.            (6)
```

Consequently the image of the multi-Hadamard space

```text
star_(u in C)K_u                                      (7)
```

under `D_beta` has dimension at most one.  If `z_C` has a nonzero active
coordinate, then both the scalar response and `k_D` in (5) are automatically
nonzero, and

```text
rank k_D=|supp(z_C) intersect S_gamma|.               (8)
```

If all active coordinates of `z_C` vanish, (5) gives `0=R_C(z_C)k_D` and no
individual factor may be inferred.

#### Proof

Contract (2) at every port of `C` by the declared `z_u`.  The desired
`D`-supplier remains and its response is evaluated at the `z_u`.  Every other
supplier contains at least one port of `C`; its local factor lies in `Z_u` and
is killed by `z_u in K_u`.  This proves (5).

The active diagonal tensors in (6) are independent and every `beta_c` on
`S_gamma` is nonzero.  Thus `D_beta` is injective on the active-coordinate
projection.  All values of (5) lie in the fixed line `K k_D`, proving the
dimension bound.  A nonzero left side forces both right factors nonzero, and
its diagonal matrix rank is its active support size, proving (8).  No
conclusion is drawn from the zero left side.  `square`

## 2. Exact four-port divisor profiles

Assume `r=3`, so `Uhat={1,2,3,4}`.  For a complementary partition
`{i,j}|{k,l}`, (5) is

```text
D_beta(z_k star z_l)=R_(kl)(z_k,z_l) k_(ij).          (9)
```

### Theorem 2 (one-active conditional profile)

Suppose `S_gamma={c}`.  Let

```text
ell_u={z(c):z in K_u} subset K.                       (10)
```

For every complementary pair:

1. if `ell_k ell_l!=0`, then `k_(ij)` is a nonzero scalar multiple of
   `e_(i,c)^* tensor e_(j,c)^*`, and the relevant response restriction is
   nonzero;
2. if `ell_k ell_l=0`, equation (9) is silent about the individual supplier
   and response factors.

Moreover, `GLS29` active-colour coverage gives

```text
ell_u=0 for at least two ports u.                     (11)
```

#### Proof

If both scalar projections are nonzero, choose kernel vectors whose
`c`-coordinates are nonzero.  Equation (9) has a nonzero rank-one pure left
side, proving the first claim without division.  If either projection is zero,
every left side vanishes and only the product equation remains.  Finally,
`ell_u=0` is equivalent to `e_(u,c)^* in Z_u`; apply Theorem 3(2) of `GLS29`.
`square`

Put

```text
T={u:e_(u,c)^* in Z_u}={u:ell_u=0}.                 (11a)
```

Then `|T|>=2`.  If `|T|=2`, with complement `I={k,l}`, equation (9) for the
kept pair `T` gives

```text
k_T in K^times e_c^* tensor e_c^*,
R_I restricted to K_k tensor K_l is nonzero.        (11b)
```

The two endpoint channel ranks on `T` are `(1,1)`, `(1,2)`, or `(2,1)`,
never `(2,2)`.  Every rank-one endpoint channel is exactly `K e_c^*`; a
rank-two endpoint contains `e_c^*`.  If `|T|=3` or `4`, every
complement-kernel contraction has zero left side and gives no supplier-rank
conclusion.

Indeed, the complement ports in `I` have nonzero `c`-coordinate projections,
so the first assertion is the nonzero branch already proved.  If both
endpoint channels on `T` had rank two, write their two independent channel
columns as full-rank `3 x 2` matrices.  Their supplier is their product through
the invertible exchange matrix, hence has rank two, contradicting (11b).  A
rank-one channel containing `e_c^*` is exactly the named coordinate line.  If
`|T|>=3`, every two-port complement meets `T`, so all its Hadamard products
have zero `c` coordinate.

The conditional pure supplier is not by itself a legal target row.  A
disjoint supplier may fill the normal image, and the statement does not prove
full-nuisance survival.

### Theorem 3 (two-active projected-kernel profile)

Suppose `S_gamma={0,1}` after relabelling colours, and put

```text
L_u=projection_(0,1)(K_u) subset K^2.                 (12)
```

Then for every pair

```text
dim(L_k star L_l)<=1.                                 (13)
```

If a nonzero generator of `L_k star L_l`:

- lies on one active coordinate axis, the complementary `k_(ij)` is pure
  rank one on that axis;
- has both active coordinates nonzero, the complementary `k_(ij)` is rank two
  diagonal on the active coordinate plane.

At most one `L_u` can be two-dimensional.  If one is two-dimensional, every
other nonzero `L_v` is an active coordinate axis.

For reference, the local-rank interpretation is exact:

- if `dim Z_u=0`, then `K_u=K^3` and `L_u=K^2`;
- if `dim Z_u=1`, then `dim L_u=2` exactly when the rank-one channel covector
  has a nonzero inactive-colour coordinate; otherwise `L_u` is a line;
- if `dim Z_u=2`, then `L_u=0` exactly when its one-dimensional kernel is the
  inactive coordinate axis; otherwise `L_u` is a line.

#### Proof

Projection commutes with coordinatewise products, so (13) is Theorem 1 for
the two complement ports.  The rank alternatives are (8).  Two copies of
`K^2` have two-dimensional Hadamard product.  If `L_u=K^2` and `L_v` is a
nonzero line, their product has dimension equal to the coordinate-support
size of a line generator; the bound forces a coordinate axis.

The rank-zero statement is immediate.  For a rank-one channel `Z_u=Ka`, the
kernel is `a^perp`.  Its projection onto
the active plane is surjective exactly when the inactive coordinate of `a` is
nonzero; otherwise one active linear equation remains.  For a rank-two
channel the kernel is a line, and its projection is zero exactly for the
inactive axis.  `square`

These rules include every zero-star case.  They are necessary consequences,
not a contradiction or an exhaustive physical classification.

## 3. Exact same-graph divisor controls

### Theorem 4 (one-active same-graph normal-slice control)

There is an exact rational graph datum with

```text
S_gamma={0},                 p!=0, omega=0,
k_D=2 e_0^* tensor e_0^*    for all six D,
R_D=lambda_D e_0^* tensor e_0^* !=0 for all six D,
2 sum_D lambda_D=beta_0,                              (14)
```

so the complete normal identity is exactly

```text
sum_D k_D tensor R_(Uhat-D)=beta_0 e_0^(tensor 4).    (15)
```

Every target has a nonzero disjoint supplier, hence
`M_D=V_D^*` for all six targets.

One choice is `beta_0=1` and

```text
(lambda_D)=(1,1,1,1,1,-9/2).                         (16)
```

#### Proof

Set `x_u=y_u=e_0^*` at every port.  Then every supplier is the tensor in
(14).  Each complement label appears once in the six-term sum, giving (15)
exactly when the displayed scalar equation holds.  All values in (16) are
nonzero.  The unique complementary pair to any target is a nonzero disjoint
supplier, so `GLS29` Theorem 2 gives full normal image.  `square`

### Theorem 5 (two-active same-graph normal-slice control)

There is an exact rational graph datum with `S_gamma={0,1}`, all six suppliers
and all six physical pair responses nonzero, every `M_D=V_D^*`, and

```text
sum_D k_D tensor R_(Uhat-D)
  =beta_0 e_0^(tensor 4)+beta_1 e_1^(tensor 4).        (17)
```

#### Proof

At ports `1,2` set `x_u=y_u=e_0^*`; at ports `3,4` set
`x_u=y_u=e_1^*`.  Within-block suppliers are `2e_0e_0` and `2e_1e_1`; every
cross supplier is the nonzero tensor `2e_0e_1` in its port order.  Put

```text
R_(34)=(beta_0/2)e_0e_0,
R_(12)=(beta_1/2)e_1e_1.                              (18)
```

For the four cross response pairs, choose nonzero scalars with sum zero, for
example `(1,1,1,-3)`, and give each response the pure word which is colour
zero on its port in `{1,2}` and colour one on its port in `{3,4}`.  The two
within-block supplier terms give the two right-side tensors in (17).  After
canonical port reordering the four cross terms are the same mixed tensor and
cancel by the scalar sum.  Every supplier and response is nonzero.  Again the
unique disjoint supplier fills each target's normal image.  `square`

### Theorem 6 (one physical response deck realizes each control)

The data in Theorems 4--5 can be realized simultaneously by the edge matrices
of one physical rational graph in each case, with

```text
d_0=d_1=2,         L=H,          p!=0,
W_(a_0,a_1)=0,     h_Q=1.                               (19)
```

#### Proof

Take residual vectors `z_(q_0)=z_(q_1)=(1,1,1)`.  Choose the shore normals

```text
one active: n_0=(1,1,0), n_1=(1,0,1),
two active: n_0=(1,1,0), n_1=(1,2,1).                (20)
```

Their products have the declared active supports, and neither is proportional
to `epsilon=(1,1,1)`.  Put `X_i=n_i^perp`.  Choose bases
`xi_i^0,xi_i^1` of `X_i` whose coordinate sums make

```text
q=xi_0^0 tensor xi_1^1+xi_0^1 tensor xi_1^0,
p=epsilon(q)
```

nonzero.  Explicitly, for `n_0` use

```text
xi_0^0=(0,0,1),       xi_0^1=(1,-1,1),               (21)
```

for the one-active `n_1` use

```text
xi_1^0=(0,1,0),       xi_1^1=(1,1,-1),               (22)
```

and for the two-active `n_1` use

```text
xi_1^0=(0,1,-2),      xi_1^1=(1,1,-3).               (23)
```

The resulting values are respectively `p=2` and `p=-2`.  Set
`W_(a_i,q_s)=xi_i^s tensor e_(q_s,0)^*`; residual evaluation gives these
shore vectors and hence the displayed `q`.

Because `n_i(e_0)=1`, setting
`W_(a_i,u)=e_(a_i,0)^* tensor x_u` or
`e_(a_i,0)^* tensor y_u` realizes the declared normal channel.  Set the
residual-pair edge to `W_(q_0,q_1)=E_00`, every `Q`-to-promoted edge to zero,
and the six promoted-port edge matrices equal to the desired `R_D`.  Then
`h_Q=1`, and the exact physical response formula is

```text
P_D(H;z_Q)=h_Q W_D=R_D.                              (24)
```

Thus all six responses belong to one graph deck.  The normal contraction kills
every label meeting `Q`, while the remaining Laplace expansion is precisely
(15) or (17).  Since the active normal diagonal is nonzero, `L=H`.
`square`

The controls deliberately verify only the declared normal slice.  They are
not claimed to satisfy the complete `GLS26` top reconstruction, to be
maximum-root sources, or to be complete GHZ witnesses.  Normal-image fullness
does not imply full `GLS22` nuisance absorption.

### Theorem 7 (maximum-root pure-normalized one-active sharpness)

There is an exact rational eight-vertex graph with root order three, surplus
two, a maximum torus root, outside incidence defect four, pure coefficients
`(1,1,1)`, six nonzero physical pair responses, rank-two residual shores,
`p=2`, zero anchor, and `S_gamma={0}`, for which the complete normal tensor is
exactly `e_0^(tensor 4)`.  The graph is not a witness: for example, two
Hamming-one coefficients are both `-1/2`.

Use vertex order

```text
(a_0,a_1,k,q_0,q_1,u_1,u_2,u_3),                    (25)
```

root and residual vectors `(1,1,1)`, and matrix units `E_ij` with the row
colour at the earlier endpoint.  The nonzero edge matrices are

```text
W_(a_0,k)=W_(a_1,k)=E_00-E_10,
W_(a_0,u_1)=W_(a_1,u_1)=E_00,
W_(a_0,u_2)=W_(a_0,u_3)=E_10,
W_(a_1,u_2)=W_(a_1,u_3)=E_21,

W_(a_0,q_0)=E_11,        W_(a_0,q_1)=E_22,
W_(a_1,q_0)=E_22,        W_(a_1,q_1)=E_11,
W_(q_0,q_1)=E_00,

W_(k,u_1)=E_01,          W_(k,u_2)=E_11,
W_(k,u_3)=E_22,          W_(u_1,u_2)=E_22,
W_(u_1,u_3)=E_11,        W_(u_2,u_3)=(1/2)E_00.      (26)
```

All unlisted edges are zero.  The root equations hold because the internal
`a_0a_1` edge is zero and each `E_00-E_10` has total sum zero.  The residual
shores are both `span{e_1^*,e_2^*}`, with normals `n_0=n_1=e_0`; hence

```text
q=e_1^* tensor e_1^*+e_2^* tensor e_2^*,
p=2,               gamma=(1,0,0),       L=H.         (27)
```

The five outside incidence ranks in order `(q_0,q_1,u_1,u_2,u_3)` are

```text
(2,2,2,2,3),                                           (28)
```

so their defect sum is four.  The nowhere-zero monomial cliques

```text
{a_0,q_0,q_1},       {a_1,u_2,u_3},       {k,u_1}    (29)
```

cover all vertices.  Therefore every torus root has size at most three,
while `{a_0,a_1,k}` at the displayed root vectors is a torus root.  It is
maximum.

Normal contraction gives

```text
x_k=y_k=x_(u_1)=y_(u_1)=e_0^*,
x_(u_2)=y_(u_2)=x_(u_3)=y_(u_3)=0.                  (30)
```

Thus only `k_(k,u_1)=2E_00` is nonzero, and its complementary physical
response is `R_(u_2,u_3)=(1/2)E_00`.  Since every `Q`--port edge is zero and
`h_Q=1`, all six responses are exactly the six nonzero promoted-port matrices
in (26).  The complete normal sum is therefore `e_0^(tensor 4)`.  Direct
perfect-matching evaluation gives all three pure coefficients one, but in the
vertex order (25)

```text
coefficient(01000000)=coefficient(10000000)=-1/2.    (31)
```

This proves every claim.  It does **not** assert complete top-diagonal
reconstruction, full-nuisance absorption, or simultaneous useful-row failure.
In particular it is a boundary control for the scalar normal attack, not a
counterexample to any full witness theorem.  `square`

## 4. Frontier consequence

```text
arbitrary-root complement-kernel supplier identity:          PROVED;
one-active four-port conditional profile:                    PROVED;
two-active four-port projected-kernel profile:               PROVED;
one-active all-response normal-slice control:                 PROVED;
two-active all-response normal-slice control:                 PROVED;
same-graph physical response-deck integrability:              PROVED;
one-active maximum-root/pure-normalized normal control:       PROVED;

normal identity + six responses + full normal images
  imply divisor exclusion:                                  REFUTED;
maximum-root + simultaneous scalar-normal absorption:       OPEN;
complete zero-anchor divisor exclusion:                      OPEN;
other root contractions / full mixed GHZ equations:          OPEN;
full GLS22 nuisance survival on the controls:                 OPEN;
other shore ranks and C12/C21/C22:                            OPEN;
r>=4 full-activity disjoint branch:                           OPEN;
maximum-root supply/attachment strategic node:                OPEN;
global Krenn-Gu conjecture:                                  UNRESOLVED. (32)
```

The smallest remaining load-bearing obligation on this fibre is to couple the
maximum-root incidence restrictions to simultaneous scalar-normal absorption,
or use the full `GLS26` top reconstruction together with an independent
probe-root contraction, the full target nuisance, and the original mixed
equations.  Either route must contradict the divisor profiles or retain a
genuinely surviving full selector package.

## Verification boundary

From repository root run

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_normal_product_divisor_kernel_profile_and_same_graph_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_normal_product_divisor_kernel_profile_and_same_graph_sharpness.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_normal_product_divisor_kernel_profile_and_same_graph_sharpness.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_normal_product_divisor_kernel_profile_and_same_graph_sharpness.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_normal_product_divisor_kernel_profile_and_same_graph_sharpness.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_normal_product_divisor_kernel_profile_and_same_graph_sharpness.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_normal_product_divisor_kernel_profile_and_same_graph_sharpness.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_normal_product_divisor_kernel_profile_and_same_graph_sharpness.py
```

The primary verifier checks arbitrary-port supplier isolation, the exact
one-/two-active kernel rules, both six-response controls, every normal nuisance
image, the shore bases and source scalars, and direct eight-vertex matching
evaluation of each same-graph normal slice.  The independent no-import audit
uses standard-library `Fraction`, sparse tensors, a separate matching
recursion, and independently assembled controls.  The arbitrary-root identity
and projected-kernel classifications are the written proof.

See the
[`2026-08-22 hostile review`](../../docs/audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_NORMAL_PRODUCT_DIVISOR_KERNEL_PROFILE_AND_SAME_GRAPH_SHARPNESS_REVIEW_2026-08-22.md).
