# Residual-hafnian common cofactor Gram theorem

## Status

**Verified arbitrary-order characteristic-zero theorem.**  After contracting
an arbitrary even residual vertex set, every two-port matching tensor splits
as the direct port edge times the full residual hafnian plus a bilinear
factorization through one common residual hafnian-cofactor matrix.  For any
number of ports, all corrected port-pair tensors therefore possess a common
symmetric block completion of bounded rank.

For two residual vertices this is exactly the known formula

```text
H_uv = h B_uv + a_u tensor b_v + b_u tensor a_v.
```

The theorem below is its general residual-hafnian form.  It supplies a legal
common global object behind the current local cofactor frames.  It is a
necessary representability condition, not by itself a contradiction and not
a proof of Krenn--Gu.

## Setup

Let `K` be a characteristic-zero field.  Let `Q` be an even residual vertex
set.  Contract every residual local space against a fixed vector, producing a
hollow symmetric scalar matrix

```text
A=(A_pq)_(p,q in Q).                                  (1)
```

For a port `u` with local vector space `V_u`, define its residual incidence
map

```text
R_u : V_u -> K^Q,
(R_u x)_p = B_up(x,z_p),                              (2)
```

where `z_p` is the fixed residual contraction vector.  For two distinct
ports `u,v`, retain their direct bilinear edge block

```text
B_uv : V_u x V_v -> K.                                (3)
```

Put

```text
h = haf(A),

C(A)_pq = haf(A[Q minus {p,q}])  for p!=q,
C(A)_pp = 0.                                          (4)
```

The matrix `C(A)` is symmetric.  It is the gradient of the residual hafnian
with respect to the off-diagonal entries of `A`, with no Pfaffian signs.

Let `H_uv` be the full bilinear matching tensor on `Q union {u,v}` after the
residual contractions, leaving only the port vectors `x in V_u` and
`y in V_v` free.

## The two-port decomposition

### Theorem 1

For every pair of distinct ports,

```text
H_uv(x,y)
 = h B_uv(x,y) + (R_u x)^T C(A) (R_v y).              (5)
```

Proof.  A perfect matching of `Q union {u,v}` has exactly two possible
forms.

1. It uses `{u,v}`.  The remaining matching lies in `Q`, giving
   `h B_uv(x,y)`.
2. It uses `{u,p}` and `{v,q}` for distinct `p,q in Q`.  The remaining
   matching lies in `Q minus {p,q}`, giving

   ```text
   (R_u x)_p C(A)_pq (R_v y)_q.
   ```

Summing the second class over the ordered pair `(p,q)` gives the second term
of (5).  The classes are disjoint and exhaustive.

No planarity, positivity, invertibility, or support genericity is used.
The same proof works over any commutative ring; characteristic zero is kept
here to match the ambient programme.

### Root-permanent aggregate

Suppose `r` root rows `H_1,...,H_r` meet a blocker set `B` of size `r+2`.
For `u,v in B`, put

```text
F_uv=P_r(H_w : w in B minus {u,v}),                  (6)
```

and for every residual vertex `p in Q` write the common blocker row

```text
a_p(u)=B_up(-,z_p).                                   (7)
```

The unsigned two-row Laplace bijection and (5) give the exact aggregate

```text
sum_(u<v) F_uv H_uv
 = h sum_(u<v) F_uv B_uv
   + sum_(p<q in Q) C(A)_pq
       P_(r+2)(H_1,...,H_r,a_p,a_q).                 (8)
```

Thus the arbitrary residual set does not produce unrelated pair terms: it
produces one linear combination of honest two-row permanent extensions,
with coefficients from the common principal-hafnian cofactor matrix.  When
`Q` has two vertices and `h=0`, (8) is exactly the previously extracted
`P_(r+2)` identity.

## Common Gram completion across all ports

Choose ports `P={u_1,...,u_s}` and bases of their local spaces.  Define the
corrected off-diagonal blocks

```text
K_uv = H_uv - h B_uv = R_u^T C(A) R_v.                (9)
```

Although the graph supplies only blocks with `u!=v`, define the canonical
diagonal completion

```text
K_uu = R_u^T C(A) R_u.                               (10)
```

Let

```text
R = [R_(u_1) R_(u_2) ... R_(u_s)].                  (11)
```

### Theorem 2

The completed symmetric block matrix satisfies

```text
K = R^T C(A) R,                                      (12)

rank K <= rank C(A) <= |Q|.                          (13)
```

Consequently all minors of `K` of size `|Q|+1` vanish.  More sharply, if a
residual cofactor theorem forces `rank C(A)<=rho`, then every minor of size
`rho+1` vanishes.  These are basis-independent determinantal equations on
the family of two-port tensors after the single common correction `hB_uv`.

The diagonal blocks in (10) are latent, but the same bound applies to every
entirely physical rectangular cross-block matrix

```text
(K_uv)_(u in U, v in P minus U).                     (14)
```

Thus its `(rho+1)`-minors vanish without choosing a diagonal completion.

This is naturally a symmetric-star-quiver representation: every port maps
into one residual state space `K^Q`, all pair tensors contract through the
same symmetric form `C(A)`, and the direct port edges form a separate affine
layer.  In Holant language, `C(A)` is the common two-boundary connection
matrix of the contracted residual network.

## Schur-defect and holonomy invariants

The raw rank bound can be sharpened after anchoring some port directions.
Write `G_uv=K_uv` on the `h=0` branch and put `rho=rank C(A)`.  Choose two
disjoint ordered anchor lists `A=(a_1,...,a_k)` and `D=(d_1,...,d_k)` for
which the `3k x 3k` cross block `G_DA` is invertible.  For disjoint test
lists `U,X`, define

```text
S_(U,X|D,A)
 = G_UX - G_UA (G_DA)^(-1) G_DX.                     (15)
```

### Theorem 3 (Schur-defect bound)

Every common cofactor Gram family satisfies

```text
rank S_(U,X|D,A) <= rho-3k.                           (16)
```

Proof.  Quotient `K^Q` by the radical of `C(A)` and retain the notation `C`
for the resulting nondegenerate form.  The operator

```text
P = R_A (G_DA)^(-1) R_D^T C                          (17)
```

is an idempotent of rank `3k`, because `G_DA=R_D^T C R_A`.  Direct
substitution gives

```text
S_(U,X|D,A) = R_U^T C (I-P) R_X,                     (18)
```

whose rank is at most `rho-3k`.  The condition is invariant under
independent changes of basis at every port.  Clearing the determinant of
`G_DA` with its adjugate turns the rank minors into polynomial equations.

For one anchor pair and four three-dimensional ports `u,v,w,x`, assume the
four displayed cross blocks are invertible and define

```text
X_(u,v,w,x)
 = G_uv (G_wv)^(-1) G_wx (G_ux)^(-1).                (19)
```

Equation (16) is equivalent to

```text
rank(I_3-X_(u,v,w,x)) <= rho-3.                       (20)
```

In particular, `rho=3` forces the exact quadrilateral holonomy

```text
X_(u,v,w,x)=I_3.                                      (21)
```

For `rho=4`, all `2 x 2` minors of `I-X` vanish; for `rho=5`, its determinant
vanishes.  These give small gauge-invariant equations even when the raw
`(rho+1)`-minors are too large.  For six residual vertices, one anchor pair
reduces a two-port-list `6 x 6` Schur defect to rank at most three, so its
`4 x 4` minors vanish.

## Recovery of the two-residual formula

For `Q={p,q}`,

```text
h=A_pq,
C(A) = [0 1; 1 0].                                   (22)
```

Writing the two columns of `R_u^T` as `a_u,b_u` gives

```text
R_u^T C(A) R_v
 = a_u tensor b_v + b_u tensor a_v,                  (23)
```

so (5) recovers the earlier two-residual factorization verbatim.

## Arbitrary-residual torus dichotomy

The coordinate-monomial alternative also extends beyond two residual
vertices.  For each `q in Q`, let `K_q` be its simultaneous-kernel space and
assume no `K_q` is contained in a coordinate hyperplane.  Put

```text
U_q = {z in K_q : z_0 z_1 z_2 != 0}.                 (24)
```

The restricted residual hafnian

```text
H_Q((z_q)) = haf([B_pq(z_p,z_q)]_(p,q in Q))          (25)
```

is multihomogeneous of degree one in every `z_q`.

### Theorem 4

Exactly one of the following alternatives holds:

1. `H_Q` has a zero on `product_(q in Q) U_q`;
2. on `product K_q`,

   ```text
   H_Q((z_q)) = lambda product_(q in Q) z_q[c_q]      (26)
   ```

   for some nonzero `lambda` and coordinate choices `c_q` (with associated
   coordinate restrictions identified on one-dimensional `K_q`).

Proof.  Let `S=Sym(direct_sum K_q^*)` and localize it at every nonzero
restricted coordinate linear form.  If alternative 1 fails, the
Nullstellensatz says that `H_Q` is a unit in this localization.  The units
are nonzero scalars times products of the irreducible linear factors that
were inverted.  Multidegree one in each `K_q` forces exactly one such factor
from every vertex, proving (26).  The converse is immediate because every
factor in (26) is nonzero on `U_q`.

Thus at arbitrary residual order there is still a clean fork:

```text
torus residual zero h=0
    -> direct common Gram/minor constraints,

or

coordinate-monomial residual hafnian
    -> the exceptional coordinate-killer branch.      (27)
```

This generalizes the earlier two-residual torus dichotomy.  It does not
exclude the coordinate-monomial branch; the repository's slice-universality
theorem shows that off-slice or cross-depth conditions are essential there.

## Why this is stronger than pairwise local factorization

Factoring each `K_uv` separately loses the shared residual space and allows
unrelated changes of basis for different pairs.  Equations (10)--(13) require
one choice of diagonal blocks making **all** port pairs a single bounded-rank
symmetric matrix.  Thus the correct local-to-global question is a structured
low-rank completion problem, not a collection of unrelated rank bounds.

For a proposed family of port-pair cofactor frames:

1. subtract the same scalar residual contribution `hB_uv` from every pair;
2. ask whether diagonal blocks `K_uu` exist so that the completed block
   matrix has rank at most `|Q|`;
3. impose that its middle form is not arbitrary but is the principal-hafnian
   cofactor matrix `C(A)` of one residual scalar matrix;
4. combine this with the block-square-zero cumulant equations across deeper
   residual deletions.

Step 2 already imports symmetric low-rank completion, quiver
semi-invariants, and determinantal geometry.  Step 3 is the genuinely
hafnian representability layer.  The theorem does not claim that the rank
minors alone characterize that layer.

## Relation to the current bottleneck

The arbitrary lower mixed-jet theorem prescribes actual cofactor frames on
many root subsets.  Theorem 1 says that whenever those frames share a
contracted residual set, their two-port pieces must factor through the same
`C(A)`.  Theorem 2 then couples different port pairs before any support
enumeration.

This suggests the following symbolic next test on the two-residual axis
cell and its first larger residual extension:

```text
lower mixed-jet frame
 -> subtract hB on every port pair
 -> common symmetric rank completion
 -> principal-hafnian cofactor equations
 -> square-zero cumulant compatibility across deletion depth.
```

A failure of the common completion minors is an immediate obstruction.  A
successful completion is useful too: it identifies the remaining obstruction
as the narrower demand `C=C(A)`, rather than generic low rank.

## Literature interface

Holant theory treats a contracted gadget through its boundary signature,
and matchgate identities characterize the planar Pfaffian boundary class
([arXiv:1303.6729](https://arxiv.org/abs/1303.6729)).  Formula (5) is the
bosonic arbitrary-graph analogue appropriate here: its connection matrix is
a hafnian cofactor matrix and carries no crossing signs.

Polynomial semi-invariants of quiver representations can be generated by
determinantal constructions in characteristic zero
([arXiv:math/9907174](https://arxiv.org/abs/math/9907174)).  That makes the
common completion minors from (13)--(14) a natural first invariant family.  It does
not make them sufficient for the special cofactor form (4).

Tensor-network geometry studies precisely the difference between local
parameterizations, their polynomial images, and boundary degenerations
([arXiv:1105.4449](https://arxiv.org/abs/1105.4449)).  The common middle
matrix `C(A)` is the hidden global parameter whose omission made the earlier
pairwise frame models locally universal.

## Verification

Run:

```text
uv run --with sympy python claims/arbitrary-order/verify_residual_hafnian_common_cofactor_gram.py
python claims/arbitrary-order/audit_residual_hafnian_common_cofactor_gram.py
```

The primary verifier proves (5) by independent symbolic hafnian expansion
for four generic residual vertices and two three-dimensional ports, recovers
(23), and checks the completed block factorization and an anchored Schur
defect.  The independent audit
uses only exact integer arithmetic and separately written hafnian and rank
routines on six residual vertices and four two-dimensional ports.  These
finite checks audit the formulae; the matching proof is arbitrary-order.
