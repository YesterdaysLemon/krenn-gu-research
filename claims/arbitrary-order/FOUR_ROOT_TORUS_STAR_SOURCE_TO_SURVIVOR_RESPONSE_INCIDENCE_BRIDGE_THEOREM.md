# Four-root torus-star source-to-survivor response-incidence bridge

## Status

**Exact source-interface bridge and conditional source-branch exclusion
(`GLD81`).**  Work over a characteristic-zero field for the matching and
response identities, and over `C` for the Krenn--Gu witness consequence.
Retain an actual maximum torus-root configuration of root order four and
surplus two, a fully supported contraction of the residual pair
`Q={q_0,q_1}`, four rank-three open ports, and the fully supported,
nonisotropic maximal-star hypotheses of `GLD69`--`GLD70`.

For every legal ten-mode GHZ graph presentation on this source branch, the
contracted four-port tensor and the three target-prescribed legal `q_0`
response columns produce an actual point of the denominator-free incidence

```text
b alpha=T(F),                  D_q0(alpha)L=R(F).       (1)
```

After the complete interface is transported to the canonical fixed star,
this is exactly the incidence used by `GLD76`--`GLD80`.  Consequently no
hypothetical Krenn--Gu witness on this source branch can have its induced
scale-fixed survivor frame in the `GLD80` principal open `D(delta)`.

This is the missing **forward source bridge**.  It does not assert that an
arbitrary tensor in the rank-`44` nuisance space is source-integrable, compute
the existential polynomial `delta`, cover its divisor, force the maximal-star
profile, cover another survivor component or gauge, handle a triangle,
residual-coordinate boundary, isotropic slope, lower port rank, smaller
survivor family, or another root order, or resolve Krenn--Gu.  The global
conjecture remains **UNRESOLVED**.

The source inputs are the maximum-root contraction identity and the physical
star compression proved by `GLD69`--`GLD70`.  The target incidence and its
principal-open exclusion are `GLD76` and `GLD80`.  No coefficient-space
membership is used as a substitute for the source argument below.

Owning dependencies:

- [`GLD69` physical maximal-star geometry](FOUR_ROOT_MAXIMAL_BASE_SURVIVOR_COMMON_INCIDENCE_AND_SPARSE_RADICAL_DETECTOR_BOUNDARY_THEOREM.md);
- [`GLD70` complete source map and torus-star compression](FOUR_ROOT_COMPLETE_Q_LAYER_SECANT_BOUNDARY_TRAP_AND_TORUS_STAR_COMPRESSION_THEOREM.md);
- [`GLD76` complete legal response module](FOUR_ROOT_TORUS_STAR_SURVIVOR_RESPONSE_UNIVERSAL_MODULE_AND_PROJECTIVE_ESCAPE_REDUCTION_THEOREM.md); and
- [`GLD80` survivor principal-open exclusion](FOUR_ROOT_TORUS_STAR_SURVIVOR_EXISTENTIAL_PRINCIPAL_OPEN_FIRST_RESPONSE_NONEXTENSION_THEOREM.md).

The source convention is the repository's [authoritative weighted perfect-
matching definition](../../README.md#the-conjecture): each unordered vertex
pair has one physical bilinear block `B_vw`, and at local vectors `(v_w)` the
graph coefficient is

```text
sum_(perfect matchings M) product_({v,w} in M) B_vw(v_v,v_w). (1a)
```

The different edge blocks are physical data of one graph; they are not
independent variables introduced by the proof.  Lemmas 1.1 and 2.1 are two
partitions of this same formula.

## 1. Physical ten-mode interface

Let the ten modes be

```text
R={r_0,r_1,r_2,r_3},       Q={q_0,q_1},
U={u_0,u_1,u_2,u_3}.                                 (2)
```

For each unordered pair of modes let `B_vw` be the physical bilinear edge
block.  Choose fully supported root vectors `x_i` and residual vectors
`z_0,z_1`.  Maximum-root saturation gives

```text
B_(r_i,r_j)(x_i,x_j)=0              for i!=j.          (3)
```

Put

```text
xi_i =B_(r_i,q_0)(x_i,z_0),
eta_i=B_(r_i,q_1)(x_i,z_1),
P_u(i,-)=B_(r_i,u)(x_i,-).                             (4)
```

The declared branch assumes every coordinate of `xi` and `eta` is nonzero,
every `P_u` has rank three, the three maximal base survivors form a star, and
its quotient slope is nonisotropic.  `GLD69`--`GLD70` then put (4), after the
declared root permutation, root-diagonal gauge, port basis changes, and
irrelevant scalings, in the canonical torus-star interface.  Those operations
are invertible on the declared open set.

From this point onward `x_i,z_j,xi,eta,P_u`, and every map built from them
denote this normalized physical presentation.  In particular the proof does
not apply a root or residual gauge to a fixed response matrix: it rebuilds
`b`, `D_q0`, `alpha`, and `ell` from the normalized edge evaluations and then
applies the matching identities below.

This preserves the source equations, not just the abstract four-port tensor.
A root permutation merely relabels matching classes.  Under
`x_i |-> d_i x_i`, put `d=product_i d_i`.  The fixed thirteen response
columns scale by `d`, the `i`-th root-response column scales by `d/d_i`, and
the corresponding root entry of `ell(y)` scales by `d_i`; hence the complete
physical response scales uniformly by `d`, exactly as the grade-zero
contraction.  Under `z_0 |-> a z_0` and `z_1 |-> c z_1`, the rebuilt raw
coordinates scale by `ac`, `a`, `c`, and `1` on the residual-pair,
`q_0`-port, `q_1`-port, and port-pair blocks respectively.  The grade-zero
contraction scales by `ac`, while the `q_0` response evaluated at
`a y` and contracted against `c z_1` also scales by `ac`.  Port basis changes
act invertibly on the open tensor factors, raw blocks, and incident response
rows.  Thus the normalized `alpha` and `ell` remain data of the same physical
graph presentation, with the displayed source equations intact.

Evaluate the six outside-outside physical blocks at `z_0,z_1` where needed:

```text
alpha_Q=B_(q_0,q_1)(z_0,z_1),
alpha_(q_j,u)=B_(q_j,u)(z_j,-),
alpha_(u,v)=B_(u,v).                                   (5)
```

In raw-label order these are `1+2*4*3+6*9=79` coefficients.  They are not an
arbitrary nuisance-space witness chosen after the fact: they are the actual
edge evaluations of the one source graph.

The residual names in the `GLD70`/`GLD73` raw order refer to the factor left
in the complementary cofactor.  Thus the explicit crosswalk is

```text
alpha_(q_0,u)=h_(eta,u)=B_(q_0,u)(z_0,-),
alpha_(q_1,u)=h_(xi,u) =B_(q_1,u)(z_1,-).              (5a)
```

### Lemma 1.1 (complete physical coefficient factorization)

Let `T_U` be the graph tensor after contracting all modes in `R union Q` and
leaving the four ports open.  Then

```text
T_U=b_(xi,eta,P) alpha.                                (6)
```

#### Proof

Every nonzero perfect matching contains no root--root edge by (3).  Hence all
four roots are paired to four distinct outside modes.  The two remaining
outside modes are paired to each other, so every surviving matching contains
exactly one of the fifteen outside--outside edges in (5).  Partition the
matchings by that edge.  Its coefficient is the permanent of the four
root--outside evaluations in (4), which is exactly the corresponding column
in the complete `1+24+54` map of `GLD70`.  Every matching occurs once, so the
sum is (6).  `square`

This argument is the source semantics behind nuisance membership.  Its
direction is only

```text
legal source presentation  ==>  a physical raw alpha satisfying (6). (7)
```

No converse is asserted.

## 2. The legal first-response factorization

Contract the four roots and `q_1`, leave `q_0` and the four ports open, and
vary the vector at `q_0`.  Its incident edge evaluations consist of

```text
four root scalars + one q_1 scalar + four port covectors,
dimension 4+1+4*3=17.                                 (8)
```

For `y in V_(q_0)`, write `ell(y) in K^17` for this list:

```text
(B_(q_0,r_i)(y,x_i))_i,
B_(q_0,q_1)(y,z_1),
(B_(q_0,u)(y,-))_u.                                   (9)
```

Let `D_q0(alpha):K^17->tensor_(u in U)V_u^*` be the complete response map of
`GLD73`--`GLD76`.

### Lemma 2.1 (source response equals the complete effective response)

For every `y`, the physical graph contraction with `q_0` replaced by `y` is

```text
D_q0(alpha) ell(y).                                   (10)
```

#### Proof

Partition the perfect matchings by the neighbor of `q_0`.

- If it is `q_1` or a port, removing that edge leaves four roots and four
  outside modes.  Every nonzero complementary matching is a root--outside
  bijection, giving respectively the one `Q` cofactor or the twelve
  eta-residual cofactor columns.  These are the fixed thirteen-column block
  of `D_q0`.
- If it is a root `r_i`, removing that edge leaves three roots and five
  outside modes.  Every nonzero complementary matching contains exactly one
  outside--outside edge from (5).  Summing those matchings gives the root
  response column `H_i(alpha)`.

The coefficient multiplying each column is precisely the corresponding
entry of (9).  Thus every physical `q_0` response factors through the
complete `17`-coordinate incident-row domain, proving (10).  For one fixed
graph the map `y |-> ell(y)` has domain dimension three; no rank-`17`
assertion about that physical map is made.  `square`

This lemma is independent of unused rows in the edge matrices.  Those rows
change the linear map `ell`, but its image still factors through the same
complete `17`-coordinate response domain.

## 3. The GHZ target supplies the lifting matrix

Suppose, for contradiction, that the physical ten-mode graph tensor is the
Krenn--Gu target in its fixed target-coordinate bases:

```text
sum_(c=0)^2 tensor_(v in R union Q union U) e_(v,c).   (11)
```

Contracting the roots and `Q` gives a concise four-port tensor

```text
T_U=sum_c tau_c tensor_(u in U) e_(u,c),
tau_c=product_(i=0)^3 x_i[c] z_0[c] z_1[c] !=0.       (12)
```

Here `x_i[c]` and `z_j[c]` are explicitly the coordinates of the source
contraction vectors in those fixed target bases; this is the coordinate
system in which fully supported means all the displayed factors are
nonzero.  The survivor frame `F` is introduced only after applying the
declared basis changes at the four open ports and absorbing `tau_c` into one
port frame.  No arbitrary frame change at a contracted source mode is used.
Write `g_(u,c)` for the transformed port vectors.  For each colour put

```text
y_c=z_0[c] e_(q_0,c).                                 (13)
```

After contracting the roots and `q_1`, the target response at `y_c` is the
`c`-th summand `tau_c tensor_u g_(u,c)` of `T(F)`.  Let

```text
L=[ell(y_0) ell(y_1) ell(y_2)] in Mat_(17 x 3)(K).     (14)
```

Lemmas 1.1 and 2.1 give exactly

```text
b alpha=T(F),                  D_q0(alpha)L=R(F),      (15)
```

where the columns of `R(F)` are the three displayed GHZ summands.  The
particular normalization in (13) is not load-bearing: any nonzero diagonal
rescaling of these three columns is absorbed into `L`.

### Theorem 3.1 (source-to-incidence bridge)

Every legal ten-mode GHZ source presentation satisfying the hypotheses of
Section 1 maps to the complete incidence (15).  After the `GLD70` canonical
normalization already incorporated in Section 1, apply only the `GLD80`
complete port-frame transport.  Then

```text
beta=S_F alpha,                 L'=J_F L                (16)
```

satisfy

```text
b_F beta=Delta_4,              D'_(q_0,F)(beta)L'=R_Delta. (17)
```

#### Proof

Equation (15) is the preceding construction.  The actual nuisance and legal
response maps obey the invertible port-frame covariance identities proved in
`GLD80`,

```text
U_F b=b_F S_F,
U_F D_q0(alpha)=D'_(q_0,F)(S_F alpha)J_F.              (18)
```

Apply `U_F` to (15) and use (16).  The target becomes the literal diagonal
and its three summands.  Explicitly, the commuting calculation is

```text
alpha --S_F--> beta,

K^17 --D_q0(alpha)--> tensor_(u in U) V_u^*
 | J_F                          | U_F
 v                              v
K^17 --D'_(q_0,F)(beta)--> tensor_(u in U) K^3,

U_F D_q0(alpha)L
  =D'_(q_0,F)(beta) J_F L
  =D'_(q_0,F)(beta)L'.                               (18a)
```

This yields (17).  The root and residual normalizations are not hidden in
`J_F`; they were performed before (15), with their exact source covariance
given in Section 1.  A permutation or nonzero diagonal rescaling of the
three displayed GHZ summands right-multiplies `R(F)` by an invertible
monomial matrix `M` and is absorbed by `L |-> L M`.  Other allowed port-frame
representatives are handled by the displayed `U_F,S_F,J_F` transport.
Arbitrary GHZ stabilizer ambiguity is not asserted to be an
interface-preserving source symmetry.  The hypothesis used below is that at
least one frame induced by the normalized physical source lies in the named
`GLD80` chart and principal open.  `square`

## 4. Principal-open source exclusion and branch cover

Let `B=Spec A` and `delta in A` be the scale-fixed equal-leaf survivor
neighborhood and existential element supplied by `GLD80`; in particular

```text
F_0 in D(delta),                  delta(F_0)!=0.        (19)
```

### Theorem 4.1 (maximal-star source branch excluded on `D(delta)`)

There is no complex Krenn--Gu witness whose maximum-root, surplus-two source
data satisfy Section 1 and whose induced survivor frame lies in `D(delta)`.

#### Proof

Such a witness would give (17) by Theorem 3.1.  `GLD80` proves that, for every
geometric `F in D(delta)` and every raw preimage `beta` of `Delta_4`, the
legal `q_0` response cannot contain the three diagonal directions.  This
contradicts the second equation of (17).  `square`

The residual alternatives for continuing beyond this named branch are:

1. root order or surplus different from `(4,2)`, or a different maximum-root
   source branch;
2. some port map has rank below three;
3. fewer than three base survivors;
4. the maximal triangle rather than the maximal star;
5. a zero coordinate of `xi` or `eta`;
6. an isotropic star quotient slope;
7. a nonisotropic star survivor outside the certified `GLD80` component or
   frame gauge;
8. the named exceptional divisor `V(delta)` inside that component.

After relaxing the hypotheses of Section 1, the complement of these eight
alternatives is empty by Theorem 4.1.  This is a proof-tree cover relative to
the root-order-four, surplus-two program, not a global exhaustive partition
of all graph sources or a claim that the alternatives are individually
nonempty or pairwise disjoint.

## 5. Verification and hostile controls

Run:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_source_to_survivor_response_incidence_bridge.py
python -I claims/arbitrary-order/audit_four_root_torus_star_source_to_survivor_response_incidence_bridge.py
```

The primary verifier replays `GLD80` and its complete interface covariance,
then independently enumerates the `945` ten-vertex perfect matchings.  It
checks the `360` non-root--root grade-zero matchings, the unique raw-edge
partition, the exhaustive `13+4=17` response-domain split, and the target
response rescaling.  The no-import audit uses a separate bitmask recurrence
and standard-library exact arithmetic.  The arbitrary-source implication is
the matching proof above, not a numerical sample.

Hostile controls:

- `GLD72` remains an exact concise GHZ tensor in `N_star`; this theorem says
  that a legal source on the excluded open would also have to pass response.
- The `GLD70` `Q` generator and epsilon are not used as GHZ-membership tests.
- Equations (6) and (10) are both derived from the same physical graph and
  matching set; raw coefficients and response directions are not chosen from
  unrelated presentations.
- The complete `17`-coordinate response domain is retained.  No response
  minor, rank chart, or selected lift is divided by, and no rank-`17` claim
  about a physical three-dimensional local response map is made.
- Every full-support, determinant, nonisotropic, survivor-gauge, and
  `delta(F)` condition is a declared open hypothesis.  Its complement is in
  the residual cover.
- Frame ambiguity acts by invertible intertwiners and preserves existence of
  (15); no decomposition is treated as unique.
- The result is a source theorem only on the named maximum-root torus-star
  branch.  It is not source integrability of arbitrary nuisance tensors, an
  explicit exceptional divisor, a graph witness, or a global theorem.
