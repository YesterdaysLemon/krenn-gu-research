# Two-residual response-atlas identifying overlap and holonomy boundary

## Status

**Exact finite-atlas characteristic-zero descent theorem and sharp atlas
counterboundary.**  Fix one named pair of residual vertices, with the same
residual contractions on every chart.  Paired residual-absent and
residual-present response families recover the corrected two-port channel

```text
Phi=M^(-1)Z=h+Q_K,
K_uv=z_uv-h m_uv=a_u tensor b_v+b_u tensor a_v.        (1)
```

Scalar transversals do not identify the hidden rows.  This theorem instead
uses fully block-polarized charts.  If an overlap contains three mutually
cross-observed port groups and each group has residual incidence
rank two, then any two factorizations of the same corrected overlap channel
differ by one unique common element of

```text
O(J),       J=[[0,1],[1,0]],
O(J)={g:g^T J g=J} isomorphic to G_m semidirect C_2.   (2)
```

Consequently two such charts glue their residual rows after one legal
`O(J)` gauge change.  On a connected atlas, the unique overlap transitions
glue one common residual frame exactly when every cycle holonomy is the
identity.  Nonidentity of a displayed cycle product is an exact atlas
integrability defect.

Three identifying groups are sharp for this argument.  With two groups an
arbitrary `g in GL_2` may act on one group while the contragredient
`J g^(-T) J` acts on the other.  Moreover, three individually physical,
partition-closed dual-Wick charts can have nontrivial rational `O(J)`
holonomy.  Thus local paired-depth compatibility plus pairwise overlap
agreement does not force global gluing.

The counteratlas is not the response of one physical graph and is not a
Krenn--Gu witness.  Data actually restricted from one graph carry its global
residual rows and therefore have trivial holonomy.  The theorem does not
prove that every hypothetical witness exposes the required paired windows,
does not make the corrected channel a weighted diagonal target, does not
extract `P_t -> Delta_3`, and does not turn holonomy into a mixed GHZ
coefficient.  Those are three separate open implications.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.  The boundedness here is the
fixed residual order and the three-group overlap witness.  It is not a claim
that response compatibility at one uniformly bounded port-subset size
determines an arbitrary-order all-subset deck.

## 1. Block-polarized two-residual charts

Let `K` be an algebraically closed field of characteristic zero.  Fix two
named residual vertices `q_0,q_1` and their contracted local vectors.  Let
`U` be a finite set of physical ports, with local spaces `V_u`.

A residual incidence frame is a family of linear maps

```text
F_u:V_u -> K^2,
F_u(z)=(a_u(z),b_u(z))^T.                             (3)
```

Its corrected channel is the family of bilinear blocks

```text
K_uv(z,w)=F_u(z)^T J F_v(w)
          =a_u(z)b_v(w)+b_u(z)a_v(w),       u!=v.    (4)
```

Work in the vertex-exclusive block-square-zero response algebra: different
polarized coordinates of one physical port may be evaluated separately,
but every product using the same physical port twice is zero.  Let `M` be a
residual-absent response with empty coefficient one and let `Z` be the
response with both residual vertices present.  Put

```text
h=Z_empty,
N=Z-hM,
Psi=M^(-1)N.                                         (5)
```

The chart is a **physical q=2 response chart** when

```text
log M is a port quadratic,
Psi=Q_K=sum_(u<v) K_uv,
K_uv=F_u^T J F_v                                     (6)
```

for some frame `F`.  Equivalently `Z=M(h+Q_K)`.  This is the block-polarized
version of the residual-relative dual-Wick criterion.  In particular, the
subtraction in (5) is load-bearing: the uncorrected top cofactor contains the
arbitrary direct term `h B_uv`.

Two charts are response-compatible on an overlap when `h`, every restricted
coefficient of `M,Z`, and hence every corrected block `K_uv`, agree after the
same port labels and polarizations are identified.

## 2. Three-block overlap identifiability

For a port group `P subset U`, write

```text
F_P=[F_u]_(u in P): direct_sum_(u in P) V_u -> K^2.   (7)
```

Call an overlap **three-block identifying** when all corrected blocks between
every two distinct overlap ports are retained and it contains three disjoint
nonempty port groups `P_0,P_1,P_2` such that

```text
rank F_(P_i)=2,                    i=0,1,2,            (8)
```

The first clause in particular retains all cross blocks between different
groups and lets an identifying group observe every extra overlap port.  The
rank condition is independent of the chosen factorization once the theorem
below applies, because a common invertible row change preserves each rank.

### Lemma 1 (rank-factorization transition)

Let `A,B,A',B'` be row-rank-two matrices and suppose

```text
A'^T J B'=A^T J B.                                   (9)
```

There is a unique `g in GL_2(K)` such that

```text
A'=gA,
B'=rho(g)B,
rho(g)=J g^(-T) J.                                  (10)
```

### Proof

The matrix in (9) has rank two.  Both sides are full rank factorizations of
the same rank-two matrix:

```text
A^T (J B)=A'^T (J B').                               (11)
```

Uniqueness of a minimal rank factorization gives a unique `S in GL_2` with

```text
A'^T=A^T S,
J B'=S^(-1) J B.                                     (12)
```

Taking `g=S^T` yields (10).  No diagonal completion, positivity, or generic
specialization is used.

### Theorem 2 (three-block identifying-overlap theorem)

Let `F` and `F'` be two frames on a three-block identifying overlap.  If

```text
F_u'^T J F_v'=F_u^T J F_v                            (13)
```

for every observed pair of distinct ports, then there is one unique

```text
g in O(J)                                             (14)
```

such that

```text
F_u'=gF_u                                             (15)
```

for every port in the overlap.

### Proof

Apply Lemma 1 to the cross block `P_0 x P_1`.  There is a unique `g` with

```text
F'_(P_0)=g F_(P_0),
F'_(P_1)=rho(g) F_(P_1).                              (16)
```

Apply it to `P_0 x P_2`.  Uniqueness on the common full-rank first factor
gives

```text
F'_(P_2)=rho(g) F_(P_2).                              (17)
```

Now use the observed `P_1 x P_2` cross block.  Equations (13), (16), and
(17) give

```text
F_(P_1)^T (rho(g)^T J rho(g)-J) F_(P_2)=0.            (18)
```

Both aggregate frames have right inverses, so

```text
rho(g)^T J rho(g)=J.                                  (19)
```

Thus `rho(g) in O(J)`.  The map `rho` is an involution and fixes every
element of `O(J)` pointwise.  Therefore

```text
g=rho(rho(g))=rho(g) in O(J).                         (20)
```

Equations (16)--(17) now give (15) on the three identifying groups.

For any extra overlap port `u`, compare it with `P_0`.  Since `g in O(J)`,
both `F'_u` and `gF_u` have the same corrected pairing with `gF_(P_0)`.
The latter aggregate frame has row rank two, so that pairing determines the
two rows of `F'_u`; hence `F'_u=gF_u`.  Finally, row rank of `F_(P_0)` makes
`g` unique.

### Corollary 3 (two-chart descent)

Two physical q=2 response charts with a three-block identifying overlap and
compatible paired-depth data glue one common residual incidence frame on
their union after one `O(J)` gauge change.

Their port--port edge blocks also agree on every covered overlap pair,
because `log M` recovers them.  Therefore the two charts are restrictions of
one physical q=2 response graph on the covered two-skeleton.  Any port pair
which occurs in neither chart remains free and may, for example, be assigned
zero; the theorem does not infer an unobserved edge.

## 3. Connected atlases and holonomy

Let `(U_alpha)_(alpha in A)` be a finite family of physical q=2 response
charts.  Its chart graph has one edge for every nonempty pairwise overlap;
assume this graph is connected and every one of its edges has a three-block
identifying overlap and compatible paired-depth data.
Theorem 2 supplies a unique transition

```text
g_(beta,alpha) in O(J),
F^beta=g_(beta,alpha) F^alpha on U_alpha intersect U_beta.   (21)
```

The reverse transition is the inverse.  For an oriented chart cycle

```text
gamma=(alpha_0,alpha_1,...,alpha_l=alpha_0),
```

define

```text
H_gamma
 =g_(alpha_0,alpha_(l-1)) ... g_(alpha_2,alpha_1)
   g_(alpha_1,alpha_0) in O(J).                       (22)
```

Under chartwise regauging, the intermediate gauges cancel around a cycle and
the base-chart gauge conjugates its based holonomy.  Hence the assertion
`H_gamma=I` is gauge-invariant.

### Theorem 4 (atlas gluing criterion)

The local residual frames glue, up to one global `O(J)` gauge, to a common
frame on the union of the atlas if and only if

```text
H_gamma=I                                             (23)
```

for every chart cycle.  It suffices to test the fundamental cycles relative
to one spanning tree.

If (23) fails, the nonzero matrix

```text
D_gamma=H_gamma-I                                     (24)
```

is an exact overlap-integrability defect.

### Proof

A common frame restricts to every chart.  Comparing it with the chosen local
frame gives one chart gauge `k_alpha in O(J)`, and every transition is

```text
g_(beta,alpha)=k_beta^(-1) k_alpha.                   (25)
```

All cycle products telescope to the identity.

Conversely, choose a root chart and a spanning tree.  Transport its gauge
along the tree using (21).  Identity of every fundamental holonomy makes the
transport independent of the path.  The regauged frames then agree on every
chosen overlap, and hence define one frame on the union.  Uniqueness is up to
the initial global `O(J)` choice.

The same argument glues the covered port--port blocks recovered from `M`.
As in Corollary 3, uncovered pairs are not reconstructed.

## 4. Sharpness: two groups are insufficient

Retain only two mutually cross-observed row-rank-two groups with frames
`F_0,F_1`.  For arbitrary `g in GL_2`, put

```text
F'_0=gF_0,
F'_1=rho(g)F_1.                                      (26)
```

The defining identity

```text
g^T J rho(g)=J                                       (27)

```

shows that the complete cross block is unchanged.  If `g notin O(J)`, no
common orthogonal gauge carries both old groups to the new ones.

For an exact rational instance take

```text
g=diag(2,3),
rho(g)=diag(1/3,1/2).                                (28)
```

Then `g^T J g=6J`, so `g notin O(J)`, while (27) holds.  This proves that a
two-group overlap cannot support Theorem 2 without additional observed
within-side data or another identifiability hypothesis.

Scalar transversals are weaker still.  Off-diagonal scalar Gram data may
have several rank-two diagonal completions, and the hidden completions need
not be `O(J)`-equivalent.  The theorem therefore requires block polarization
and aggregate row-rank hypotheses; it does not infer them from a scalar
pentad or from the number of ports.

## 5. Sharpness: a nontrivial physical-chart counteratlas

Let `P:K^3 -> K^2` be

```text
P=[[1,0,0],[0,1,0]].                                  (29)
```

Make three disjoint overlap clusters `A,B,C`, each containing three ternary
ports.  Give every port in an untwisted cluster the frame `P`.  Each of the
three singleton port groups in a cluster has row rank two, so the cluster is
three-block identifying.

Use three charts

```text
U_0=A union C,
U_1=A union B,
U_2=B union C.                                       (30)
```

On `U_0` use frame `P` on both clusters.  On `U_1` use `P` on both clusters.
On `U_2` use `P` on `B` and

```text
tP on C,          t=diag(2,1/2).                     (31)
```

Since `t^T J t=J`, the corrected blocks agree on every overlap.  Set on
each chart

```text
M=1,
h=0,
Z=Q_K.                                               (32)
```

Every chart is the complete partition-closed q=2 response of a physical
local graph with zero port--port and residual--residual edges and the
displayed residual incidence rows.  All higher response coefficients vanish,
so every dual-Wick insertion equation holds.

The transitions on the cycle `U_0 -> U_1 -> U_2 -> U_0` are

```text
I, I, t^(-1),                                        (33)
```

up to orientation.  Their holonomy is nonidentity.  Theorem 4 therefore
proves that no common residual frame restricts to all three local charts.

This construction is a counterexample to pairwise-atlas gluing, not to the
physical response theorem.  It cannot be the restriction of one graph:
one graph's globally defined incidence rows would themselves trivialize the
transition torsor.  It has no GHZ target equation and is not a graph witness.

## 6. Exact GL consequence and remaining obligations

The theorem supplies the first bounded response-atlas transition statement
in the live GL lane:

```text
breadth:
  two charts for descent; a connected chart graph for holonomy;

depth:
  paired residual-absent/present q=2 responses, equivalently the complete
  corrected degrees zero and two plus the dual-Wick higher-subset tests;

common hidden data:
  the fixed residual edge h, covered port--port blocks B_uv, and the two
  residual incidence rows;

transition group:
  O(J) on a three-block identifying overlap;

agreement:
  glues a common physical q=2 response frame on the covered two-skeleton;

disagreement:
  gives a nonzero cross-depth coefficient defect, an overlap coefficient
  defect, or the displayed holonomy matrix D_gamma.                 (34)
```

Three further implications are not part of this theorem.

1. **Universal supply.**  The maximal-root theorem supplies one fixed
   surplus layer, not the paired partition-closed windows assumed here.
   The balanced full-sensor branch supplies a complete same-graph deck, but
   the all-balanced rank-drop branch remains open.
2. **Permanent extraction.**  A common corrected channel becomes the last
   two rows of `P_(r+2)` only after a legal selector proves that the corrected
   aggregate itself is a weighted diagonal tensor with three nonzero weights.
   The uncorrected top tensor cannot be used.
3. **Mixed-target detection.**  Failure of (6), response compatibility, or
   (23) is an atlas defect.  Calling it a nonzero mixed GHZ coefficient
   requires a separate nuisance-free coefficient-selection identity.  The
   nontrivial counteratlas proves that such an implication is not formal.

Thus this theorem refines GL without closing it.  It neither proves a local
permanent nonrestriction theorem nor changes the global status.

## Replay

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_two_residual_response_atlas_identifying_overlap_and_holonomy_boundary.py
python -I claims/arbitrary-order/audit_two_residual_response_atlas_identifying_overlap_and_holonomy_boundary.py
python -m py_compile claims/arbitrary-order/verify_two_residual_response_atlas_identifying_overlap_and_holonomy_boundary.py claims/arbitrary-order/audit_two_residual_response_atlas_identifying_overlap_and_holonomy_boundary.py
python -m ruff check claims/arbitrary-order/verify_two_residual_response_atlas_identifying_overlap_and_holonomy_boundary.py claims/arbitrary-order/audit_two_residual_response_atlas_identifying_overlap_and_holonomy_boundary.py
```

The primary replay checks the symbolic contragredient identity, the exact
three-group recovery, the rational two-group ambiguity, every block overlap
in the three-chart counteratlas, and its nontrivial holonomy.  The independent
`python -I` audit imports neither the primary nor SymPy.  It uses exact
`Fraction` matrices and a separately written matching recurrence to verify
that each local counteratlas chart has the claimed partition-closed physical
q=2 response.  These bounded checks audit the displayed linear algebra and
sharpness controls; the written rank-factorization and spanning-tree
arguments prove the theorem.
