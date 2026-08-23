# Maximum-root surplus-two zero-anchor rank-two-shore normal channel and intersecting-supplier exclusion

## Status

**Exact characteristic-zero arbitrary-root physical theorem and sharpness
certificate.**  Continue the `GLS28` zero-anchor branch at the pointwise shore
rank

```text
(d_0,d_1)=(2,2),             dim(E/P_Q(T_Q))=1.       (1)
```

The two residual-shore normals define one canonical scalar root channel.  In
that channel every promoted supplier is the symmetric two-shore tensor

```text
k_(uv)=x_u tensor y_v+y_u tensor x_v.                 (2)
```

The complete `GLS23` nuisance has an exact cylinder formula, and the complete
physical GHZ equation has an exact arbitrary-root mixed-response identity.
Every active normal colour must occur at two promoted ports and has a supplier
with a nonzero pure coefficient and nonzero physical response.  On the
principal open where all three normal colour products are nonzero, an
intersecting supplier support cannot absorb all normal pure columns.  Hence
simultaneous useful-row failure forces two vertex-disjoint nonzero suppliers,
and the support cannot consist of only those two edges.

This is `GLS29`.  It excludes the full-activity star and triangle pieces of
the one-dimensional redundant cover at arbitrary root order.  At `r=3`, a
second denominator-free annihilator argument also excludes every disjoint-
supplier and local-rank fibre: the full-normal-activity locus is empty.  It
does **not** exclude the higher-root
disjoint-supplier branch, any one- or two-colour normal-product divisor, the
other shore ranks, or `C12/C21/C22`.  A displayed rational same-graph control has
all six `r=3` target nuisances full and all six responses nonzero while
violating original mixed GHZ coefficients.  Thus the original mixed equations
remain load-bearing.  The strategic node and the global Krenn--Gu conjecture
remain open; the global status is **UNRESOLVED**.

## Dependencies and exact scope

Use

- [`GLS22`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md) for the exact full/transverse selector equivalence and target coupling;
- [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md) for the complete labelled nuisance slices;
- [`GLS26`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ZERO_ANCHOR_DIAGONAL_RECONSTRUCTION_AND_RESIDUAL_SHORE_COVER_THEOREM.md) for the residual-shore tangent and zero-anchor branch; and
- [`GLS28`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TARGET_ENVELOPE_PRODUCT_SELECTOR_AND_BOUNDED_REDUNDANT_COVER_THEOREM.md) for the one-dimensional redundant-cover boundary.

Retain their notation

```text
A={a_0,a_1},                     Q={q_0,q_1},
Uhat=K_0 disjoint-union U,       m=|Uhat|=2r-2>=4,
E=E_A^tr=ker epsilon_A,          dim E=8,
q=G_Q^A(z_Q),                    p=epsilon_A(q)!=0,
P_Q(v)=pv-epsilon_A(v)q,         omega=W_(a_0,a_1)=0,
Tbar=P_Q(T_Q),                   H=E/Tbar.             (3)
```

All root and port spaces are ternary.  The pointwise theorem is valid over a
characteristic-zero field at every point satisfying the displayed source
gates and the complete contracted GHZ equation.  The actual maximum-root
source supplied by the repository is over `K=C`.  No response, normal
coordinate, supplier minor, nuisance minor, or incidence factor is divided
out.

Assume (1) and the essential branch P of `GLS26`.  Then `L=H` is the nonzero
one-dimensional reconstructed diagonal quotient.  Choose arbitrary nonzero
shore normals

```text
n_i in X_i^perp,                 dim X_i^perp=1,
rho=n_0 tensor n_1 in (E_A^*)^*,
x_u=W_(a_0,u)(n_0,-) in V_u^*,
y_u=W_(a_1,u)(n_1,-) in V_u^*.                       (4)
```

For `D={u,v}` put

```text
k_D=x_u tensor y_v+y_u tensor x_v in V_D^*,
Z_u=span{x_u,y_u} subset V_u^*,
gamma_c=n_0(c)n_1(c),
alpha_c=z_(q_0,c)z_(q_1,c),
beta_c=alpha_c gamma_c.                               (5)
```

Every `alpha_c` is a residual-torus unit.  The phrase **active normal colour**
means `gamma_c!=0`.

## 1. The one-dimensional physical normal channel

### Theorem 1 (exact quotient normal)

The restriction of `rho` to `E` is nonzero and

```text
ker(rho|_E)=Tbar.                                     (6)
```

Thus `rho` identifies `H=E/Tbar` with `K`.  For every promoted pair
`D={u,v}`, with `t_D=P_Q(g_D)` as in `GLS22`--`GLS28`, one has

```text
(rho tensor id)(t_D)=p k_D.                           (7)
```

#### Proof

The product normal kills
`T_Q=X_0 tensor V_(a_1)^*+V_(a_0)^* tensor X_1` and kills
`q in X_0 tensor X_1`.  Hence it kills `P_Q(T_Q)`.  If `rho|_E=0`, then `rho`
is proportional to `epsilon_A` on the nine-dimensional root space.  Applying
both functionals to `q` gives `0=lambda p`, so `lambda=0`, contradicting
`rho!=0`.  Since `Tbar` has codimension one in `E`, (6) follows.

Zero anchor removes the internal `A`-pair matching from `g_D`.  Contracting
its remaining two cross matchings at `n_0,n_1` gives exactly (2).  Finally
`rho(q)=0`, so applying `rho` to `P_Q(g_D)=p g_D-q epsilon_A(g_D)` gives (7).
`square`

The tensor `k_D` is an exact physical common-two-shore corrected pair block
in this normal channel.  It is not a `GLS8` response: the latter lives on the
complement `Uhat-D`.

## 2. Exact normal image of the complete target nuisance

For a receiving target `D={u,v}`, define

```text
A_(u|v)=sum_(w notin {u,v}) Slice_w(k_(uw)) subset V_u^*,
A_(v|u)=sum_(w notin {u,v}) Slice_w(k_(vw)) subset V_v^*,
M_D=(rho tensor id_(V_D^*))(N_D^tr) subset V_D^*.     (8)
```

Here `Slice_w` contracts the displayed `w` factor and retains the other port.

### Theorem 2 (normal nuisance cylinders)

If some promoted pair `E` disjoint from `D` has `k_E!=0`, then

```text
M_D=V_D^*.                                            (9)
```

Otherwise

```text
M_D=A_(u|v) tensor V_v^*+V_u^* tensor A_(v|u).        (10)
```

In particular, the following pointwise implications are exact.

1. If `k_D notin M_D`, a functional `eta in V_D` separating it from `M_D`
   makes `rho tensor eta` a legal normal-factor transverse selector.  After
   normalization, `GLS22` lifts it to a legal constant full `GLS8` selector.
2. If

   ```text
   gamma_c e_(u,c)^* tensor e_(v,c)^* notin M_D,      (11)
   ```

   the same construction applied to the corresponding transverse pure
   column gives a legal full selector with the named nonzero physical
   response.
3. If target `D` has no useful legal row at all, then every tensor in (11)
   belongs to `M_D`.

#### Proof

Apply `rho` to the exact label cases of `GLS23`.  The top label vanishes by
`omega=0`; the `Q` label is zero; and every one-`Q` label has root coefficient
in `Tbar`, so (6) kills it.  A promoted pair sharing `u` with the target gives
`Slice_w(p k_(uw)) tensor V_v^*`, and similarly at `v`.  Since `p` is a unit,
their sum is (10).  A disjoint pair gives
`Slice_E(p k_E) tensor V_D^*`; its full scalar slice is `K` exactly when
`k_E!=0`, proving (9).

A port functional annihilating `M_D` makes its product with `rho` annihilate
the complete nuisance.  Equation (7) proves the first implication.  Moreover

```text
rho(P_Q(r_c))=p gamma_c,                              (12)
```

so the second implication follows from `GLS22` target coupling.  Its
contrapositive gives the third.  No equality between the full nuisance and
the coarser normal image is asserted.  `square`

## 3. Complete mixed-response identity and forced activity

Write

```text
R_S=P_S(H;z_Q) in tensor_(u in S)V_u^*.               (13)
```

External tensor products below are canonically reordered into the fixed
`Uhat` port order.

### Theorem 3 (denominator-free complete normal identity)

The complete contracted GHZ equation implies

```text
sum_(D in binom(Uhat,2)) k_D tensor R_(Uhat-D)
  =sum_(c=0)^2 beta_c e_c^(tensor Uhat).              (14)
```

Consequently, for every active normal colour `c`:

1. some supplier `D` has both

   ```text
   coefficient_(c,c)(k_D)!=0,
   coefficient_(pure c)(R_(Uhat-D))!=0;               (15)
   ```

2. for every promoted port `v`, there is a distinct port `u` such that

   ```text
   e_(u,c)^* in Z_u.                                  (16)
   ```

In particular, each active colour occurs in the channel spans at at least two
distinct promoted ports.

#### Proof

Expand the physical coefficient tensor by the pair matched to `A`.  The top
matching is killed by `omega=0`; every pair meeting `Q` is killed by a shore
normal; and `Q` itself is killed by `rho(q)=0`.  A promoted pair contributes
`k_D` by the cross-matching calculation in Theorem 1.  Contracting the pure
GHZ side at `z_Q,n_0,n_1` gives the right side of (14).  This proves (14)
without division.

Take the all-`c` coefficient.  Its nonzero right side is a sum of the products
in (15), so one product is nonzero.

For (16), suppose instead that `e_(u,c)^* notin Z_u` for every `u!=v`.
Finite-dimensional separation gives `m_u in Z_u^perp` with
`m_u(e_(u,c)^*)!=0`.  Contract (14) at all ports other than `v` by these
`m_u`.  Every left summand dies because its pair `D` contains a contracted
endpoint whose factor lies in `Z_u`.  The `c`-coordinate of the right side is

```text
beta_c product_(u!=v)m_u(e_(u,c)^*) !=0,
```

a contradiction.  `square`

The first conclusion is selected-response activity in the scalar normal
channel.  It does not attach that supplier coefficient to the receiving
`GLS8` target.

## 4. Full-activity intersecting-support exclusion

Let

```text
G={D in binom(Uhat,2):k_D!=0}.                         (17)
```

### Theorem 4 (intersecting support forces a useful row)

Assume

```text
gamma_0 gamma_1 gamma_2 !=0.                          (18)
```

If `G` has no two vertex-disjoint edges, then some target and some colour
satisfy (11).  Therefore that target has a legal full `GLS8` selector with
the named nonzero response.  Equivalently, simultaneous useful-row failure on
(18) forces two vertex-disjoint edges in `G`.

Moreover, on (18) the complete identity (14) forbids `G` from consisting of
exactly two disjoint edges.  Hence the remaining failure support has at least
three edges.

#### Proof

Suppose every tensor (11) is contained in its `M_D`.  A pairwise-intersecting
family of two-subsets is contained in a star or is exactly a triangle, after
discarding isolated vertices.

In the star case choose a support edge `D={u,v}` with centre `u`.  Formula
(10) reduces to

```text
M_D=A_u tensor V_v^*,               dim A_u<=dim Z_u<=2. (19)
```

Containment of all three pure diagonal tensors would put all three coordinate
vectors of `V_u^*` in `A_u`, impossible.

Now suppose the support is the triangle on `i,j,k`.  For each target edge,
(10) and pure-tensor projection to
`(V_i^*/A) tensor (V_j^*/B)` show that every coordinate vector belongs to at
least one of the two endpoint channel spans.  Put

```text
C_i={c:e_(i,c)^* in Z_i}.                             (20)
```

Then `|C_i|<=2` and `C_i union C_j={0,1,2}` for every pair.  The elementary
three-set check forces every `C_i` to have size two with three distinct
missing colours.  Hence the `Z_i` are the three distinct coordinate planes.

Fix the colour `c_i` missing at `i` and take the `e_(i,c_i)^*` coefficient of
(14).  Both suppliers incident with `i` vanish.  The remaining supplier
`k_(jk)` is forced to be a nonzero scalar multiple of
`e_(j,c_i)^* tensor e_(k,c_i)^*`, and therefore has matrix rank one.  But

```text
k_(jk)=[x_j y_j] [[0,1],[1,0]] [x_k y_k]^T           (21)
```

has rank two because both endpoint matrices have column rank two.  This is a
contradiction.

Finally, suppose the support consists of two disjoint edges `e,f`.  Contract
all other promoted ports in (14) by covectors nonzero on all three coordinate
vectors.  Across the bipartition `e|f`, the left side is a sum of two rank-one
matrices, whereas the right side is a three-term diagonal matrix of rank
three.  Contradiction.  `square`

Theorem 4 is pointwise and arbitrary-root.  Its open condition (18) is not a
license to discard the divisor `gamma_0 gamma_1 gamma_2=0` from a universal
failure claim.

## 5. Four-port full-activity exclusion

At `r=3`, number the four promoted ports `1,2,3,4`.  Regard
`x_i,y_i in V_i^*` as covectors and define

```text
Y_i=span{x_i,y_i},       r_i=dim Y_i,
K_i=ker x_i intersect ker y_i subset V_i.             (22)
```

For subspaces `K,K' subset K^3`, let `K star K'` be the span of all
coordinatewise products `z star z'`.

### Theorem 5 (four-port full-normal-activity exclusion)

Assume `r=3`.  The complete GHZ equation forces

```text
gamma_0 gamma_1 gamma_2=0.                            (23)
```

Equivalently, the full-normal-activity locus (18) is empty.  This includes
every local-channel rank, supplier-rank, response-zero, and normal-nuisance
rank-drop fibre.

#### Proof

Suppose instead that (18) holds.  For complementary pairs
`{i,j} disjoint-union {k,l}={1,2,3,4}`, choose arbitrary
`z_k in K_k` and `z_l in K_l` and contract (14) at ports `k,l`.  Every term
except the `{i,j}` supplier dies, giving the denominator-free identity

```text
diag(beta_c z_k(c)z_l(c):c=0,1,2)
  =R_{kl}(z_k,z_l) k_(ij).                            (24)
```

Consequently

```text
dim(K_k star K_l)<=1                                  (25)
```

for every pair.  If `z_k star z_l` is nonzero, injectivity of the diagonal
map in (24) shows that both the response scalar and `k_(ij)` are nonzero, and

```text
|supp(z_k star z_l)|=rank k_(ij).                     (26)
```

If the entire star product vanishes, (24) infers neither factor and we do not
divide by either one.

Write `A_i=[x_i y_i]`.  Directly from (2),

```text
rank k_(ij)=2                    if (r_i,r_j)=(2,2),
rank k_(ij)=1                    if {r_i,r_j}={1,2},
rank k_(ij)<=1                   if (r_i,r_j)=(1,1),
rank k_(ij)=0                    if r_i r_j=0.         (27)
```

We use two elementary Hadamard-product lemmas.  If planes
`P,Q subset K^3` satisfy `dim(P star Q)<=1`, then they are distinct coordinate
planes and their product is the common coordinate axis.  Otherwise an
infinite-field plane contains a fully supported vector; multiplying the other
plane coordinatewise by it preserves dimension two.  Equal coordinate planes
also have a two-dimensional product.  For a plane `P` and a line `Kz`,

```text
P star Kz=diag(z)P.                                   (28)
```

This product is zero exactly when `P` is a coordinate plane and `z` is its
missing coordinate axis.  If it is a line generated on a two-coordinate
support, the normal defining `P` and `z` have that same support.

First exclude local rank zero.  Two rank-zero ports give
`K_i star K_j=K^3`, contradicting (25).  With exactly one rank-zero port, its
kernel is `K^3`; (25) forces every other kernel to be a coordinate axis, so
the other local ranks are two.  Contracting the full kernel against any such
axis makes the left side of (24) a nonzero rank-one diagonal, while the
complementary supplier has rank two.  This is impossible.

Now every `r_i` is one or two.  Let `s` be the number of rank-one local
channels, equivalently the number of plane kernels.  The five cases are:

- `s=4`.  The plane lemma makes four kernels pairwise distinct coordinate
  planes, but only three exist.
- `s=3`.  The three plane kernels are the three coordinate planes.  Applying
  (25) to them and the remaining kernel line forces that line to be a
  coordinate axis.  The three rank-one channel spaces are the three distinct
  coordinate lines, while the rank-two channel misses the colour `t` selected
  by that axis.  Colour `t` occurs in `Z_u` at only one port, contradicting
  Theorem 3(2).
- `s=2`.  The two plane kernels are distinct coordinate planes.  Their star
  product is a nonzero coordinate line.  Equation (24) equates the resulting
  rank-one diagonal with a scalar multiple of the complementary supplier
  between two rank-two ports.  Injectivity makes both factors nonzero, but
  that supplier has rank two.
- `s=1`.  Write the plane kernel as `P` and the other kernel lines as `Kz_j`.
  If `P` is not a coordinate plane, none of `P star Kz_j` is zero.  Its
  complementary supplier joins two rank-two ports, so (26) and the
  plane-line lemma force all three `z_j` to have the same two-coordinate
  support as the normal defining `P`.  Their pairwise products then have
  support two, while the complementary supplier joins rank one to rank two
  and has rank one, contradicting (26).

  If `P` is a coordinate plane, a nonzero `P star Kz_j` either has dimension
  two or is a coordinate line.  The first violates (25); the second has rank
  one while its complementary supplier has rank two.  Hence every such
  product is zero.  By (28), all three kernel lines are the missing coordinate
  axis `e_t`.  The rank-one channel is the line `e_t^*`, while the three
  rank-two channels omit colour `t`.  Again that colour occurs at only one
  port, contradicting Theorem 3(2).
- `s=0`.  Write `K_i=Kz_i` and `S_i=supp z_i`.  Every complementary supplier
  has rank two, so (24)--(26) give

  ```text
  |S_k intersect S_l| in {0,2}.                       (29)
  ```

  Theorem 3(2) says every colour belongs to at least two channel planes
  `Z_i=K_i^perp`; equivalently, each coordinate occurs in at most two of the
  four supports `S_i`.  No four nonempty subsets of a three-set meet both
  conditions.  If a maximal support has size three, the other three have size
  two and violate the coordinate-degree bound.  If a maximal support has size
  two, every other support is that two-set or its disjoint singleton; the
  intersection and degree bounds allow at most one of each, for at most three
  sets.  If all are singletons, they must be distinct, again allowing only
  three.

Every local-rank case contradicts (14).  Thus the full-activity point cannot
exist.  `square`

Theorem 5 is an exact `r=3` branch exclusion, not a selector package and not
an arbitrary-root statement.  The divisor `gamma_0 gamma_1 gamma_2=0`
remains.

## 6. Four-port cross identity and downstream boundary

At `r=3`, put `sigma_D=p k_D` and `D_e=R_e`.  For four distinct ports define
`boxtimes` to mean external tensor product followed by canonical port
reordering, and put

```text
delta_(uw)=x_u tensor y_w-y_u tensor x_w.             (30)
```

### Theorem 6 (exact exchange and cross-compound identities)

For distinct `u,v,w,x`,

```text
sigma_(uv) boxtimes sigma_(wx)
-sigma_(ux) boxtimes sigma_(vw)
  =-p^2 delta_(uw) boxtimes delta_(vx).               (31)
```

Furthermore, regrouping (14) by complementary pairs gives

```text
sum_(e|f) (sigma_e boxtimes D_f+D_e boxtimes sigma_f)
  =p sum_c beta_c e_c^(tensor 4).                     (32)
```

The compound

```text
C(sigma)=sum_(e|f)sigma_e boxtimes sigma_f            (33)
```

has every one-port flattening of rank at most two.

#### Proof

Expand (2) in (31); the common terms cancel and the four remaining terms
factor as displayed.  Equation (32) is (14) multiplied by `p` and grouped
over the three unordered complementary pair partitions.  Finally

```text
C(sigma)=2p^2 sum_(S subset {u,v,w,x}, |S|=2)
  (tensor_(s in S)x_s) boxtimes (tensor_(t notin S)y_t), (34)
```

whose factor at any fixed port lies in `span{x_u,y_u}`.  `square`

Although `sigma_D/p` is a physical common-shore corrected block, (32) is a
cross identity `X(D,sigma)=pure`, not the `GLD3` or `GLD16` detector identity.
The tensor `sigma_D` is on `D`, whereas a `GLS8` selector produces the
`Q`-residual response on `Uhat-D`.  No committed theorem target-attaches all
six `sigma_D`, supplies three-colour downstream activity, or identifies the
one-dimensional root quotient `H` with the joint `M/Z` coefficient plane.
Thus (31)--(34) do not enter `GLD3` or `GLD16` unconditionally.

## 7. Exact same-graph sharpness certificate

### Proposition 7 (full absorption and six responses are insufficient)

There is an exact rational `r=3` graph-side datum satisfying

```text
omega=0, p=2, (d_0,d_1)=(2,2), dim H=1, L=H,
rank Slice_D(t_D)=8                         for all six D,
N_D^tr=E tensor V_D^*                      for all six D,
R_(Uhat-D)!=0                              for all six D, (35)
```

and with all three global pure coefficients equal to one.  It is not a GHZ
witness: in vertex order
`(a_0,a_1,k,q_0,q_1,u_1,u_2,u_3)`, its coefficient at `00000010` is
`-3/2` instead of zero.

#### Certificate

All contraction vectors are `(1,1,1)`.  Let `W_(a_0,a_1)=0`, and for both
`i=0,1` put

```text
W_(a_i,q_0)=E_00,                  W_(a_i,q_1)=E_10. (36)
```

The `A`-to-`Uhat` matrices are

```text
a0-k  = [-1 -1 -1;  1  0  1;  1  1 -1]
a1-k  = [-1  1  1; -1 -1  0;  1 -1  1]
a0-u1 = [ 1  0  0;  1  1  1;  1 -1  1]
a0-u2 = [-1  1 -1; -1 -1 -1; -1  1 -1]
a0-u3 = [ 0  0  0;  1 -1  1; -1  1  0]
a1-u1 = [ 1 -1  0; -1  0  0; -1 -1  1]
a1-u2 = [-1 -1 -1; -1  0  0;  1  0  0]
a1-u3 = [-1  1  1; -1  1  0;  0 -1  0].             (37)
```

The remaining nonzero matrices are

```text
k-u1=[-1 -1 -1; 0 -1 1; 1 0 0]
k-u2=[ 1 -1  1;-1  1 1;-1 0 1]
k-u3=[ 0  1  1; 0  1 0; 1 0 -1]
k-q0=E_01,                   k-q1=E_02,
q0-q1=diag(-1/2,1/2,1),
u1-u2=u1-u3=u2-u3=E_01.                              (38)
```

All `q_s-u_i` matrices are zero.  Direct exact evaluation gives (35), the
six displayed nonzero response coefficients `1,1,1,1,1,-1`, and the failed
mixed coefficient above.  A disjoint complementary supplier fills each
complete transverse pair nuisance by `GLS23`.  Thus this is a same-graph
sharpness certificate for module/response-only arguments, not a witness or a
counterexample to the conjecture.  `square`

## 8. Frontier and non-closure boundary

```text
rank-two-shore quotient normal and pair factorization:       PROVED;
exact normal image of every complete pair nuisance:          PROVED;
complete arbitrary-root normal mixed-response identity:      PROVED;
active colour -> supplier coefficient and response activity: PROVED;
active colour occurs at at least two promoted ports:         PROVED;
full-activity intersecting supplier support:                 EXCLUDED;
support consisting of exactly two disjoint edges:            EXCLUDED;
full-activity r=3 all local-rank/response fibres:             EXCLUDED;
same-graph full-absorption/nonzero-response control:          VERIFIED;

full-activity disjoint-supplier branch with >=3 edges, r>=4:  OPEN;
one-/two-colour normal-product divisor fibres:                OPEN;
other shore-rank and C12/C21/C22 branches:                    OPEN;
full target attachment and synchronization:                  OPEN;
arbitrary-root downstream detector entry:                    OPEN;
maximum-root supply/attachment strategic node:                OPEN;
global Krenn-Gu conjecture:                                  UNRESOLVED. (39)
```

## Verification boundary

From repository root run

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_two_shore_normal_channel_and_intersecting_supplier_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_two_shore_normal_channel_and_intersecting_supplier_exclusion.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_two_shore_normal_channel_and_intersecting_supplier_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_two_shore_normal_channel_and_intersecting_supplier_exclusion.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_two_shore_normal_channel_and_intersecting_supplier_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_two_shore_normal_channel_and_intersecting_supplier_exclusion.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_two_shore_normal_channel_and_intersecting_supplier_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_two_shore_normal_channel_and_intersecting_supplier_exclusion.py
```

The primary verifier checks the normal quotient, pair factorization, nuisance
cylinders, complete matching expansion, support combinatorics, exchange
identity, rank bounds, and the rational same-graph certificate.  The
independent no-import audit uses standard-library rational arithmetic, sparse
tensors, its own elimination and matching recursion, and a separate
combinatorial proof representation.  These finite scripts audit the displayed
mechanisms; the arbitrary-root contractions and support exclusion are the
written proofs.

See the
[`2026-08-22 hostile review`](../../docs/audits/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_TWO_SHORE_NORMAL_CHANNEL_AND_INTERSECTING_SUPPLIER_EXCLUSION_REVIEW_2026-08-22.md).
