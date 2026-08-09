# Torus-zero residual hafnians can have full-rank cofactor transfer

## Status

**Exact arbitrary-even-order characteristic-zero counterboundary.**  The
general residual-hafnian two-port decomposition is

```text
H_uv=h B_uv+R_u^T C(A) R_v,                         (1)
```

where `h=haf(A)` and `C(A)` is the symmetric matrix of principal
two-vertex-deletion hafnians.  It is tempting to expect that choosing a
torus residual zero `h=0` also makes `C(A)` singular and strengthens the
common Gram rank bound.

That expectation is false at every even residual order `q>=4`.  An explicit
one-parameter-edge residual matrix satisfies

```text
haf(A)=0,                 det C(A)!=0.               (2)
```

Consequently the zero-hafnian hypersurface meets the open full-rank
cofactor-transfer stratum.  For the canonical completed corrected Gram
family `K=R^T C(A)R`, the universal bound

```text
rank K<=q.                                             (3)
```

is sharp even on `h=0`; no `q-1` improvement follows from the torus-zero
branch.  The anchored Schur-defect rank equations in
`RESIDUAL_HAFNIAN_COMMON_COFACTOR_GRAM_THEOREM.md` are therefore the
strongest universal **rank** equations supplied by the two-port
decomposition alone.  The congruence-surjectivity argument below is needed
for this conclusion; a single full-rank cofactor point would not suffice.
Principal-cofactor integrability and deeper deletion compatibility can still
impose equations once more response levels are retained.

This is a proof-route boundary, not a Krenn--Gu counterexample.  It does not
solve the target-compatible permanent equations, the coordinate-monomial
residual branch, or the global conjecture, which remains **UNRESOLVED**.

## The explicit residual family

Let `q>=4` be even, let the residual vertices be `0,...,q-1`, and put

```text
A_01=-(q-2),
A_ij=1                 for every other i<j,
A_ii=0.                                             (4)
```

Write

```text
g=(q-5)!!,                 alpha=(q-3)!!=(q-3)g,
beta=-2g.                                             (5)
```

As usual `(-1)!!=1`, so these formulae include `q=4`.

### Theorem 1 (zero hafnian)

The matrix (4) satisfies

```text
haf(A)=0.                                             (6)
```

Proof.  With every edge equal to one there are `(q-1)!!` perfect
matchings.  Exactly `(q-3)!!` of them use `{0,1}`.  Replacing that edge
weight `1` by `-(q-2)` changes the hafnian by

```text
(-(q-2)-1)(q-3)!!=-(q-1)(q-3)!!.
```

Since `(q-1)!!=(q-1)(q-3)!!`, the two quantities cancel.  This is a
symbolic matching partition, not a matching-family enumeration.

### Theorem 2 (full-rank cofactor matrix)

For distinct vertices, the principal cofactor matrix is

```text
C_01=alpha,
C_0j=C_1j=alpha                 for j>=2,
C_ij=beta                       for 2<=i<j,
C_ii=0.                                             (7)
```

Moreover,

```text
det C(A)
 =2^(q-2) (q-1) (q-3)^3 ((q-5)!!)^q !=0.            (8)
```

Proof.  Deleting `0` or `1` removes the exceptional edge, leaving the
all-ones hafnian of order `q-2`; this gives `alpha`.  If `i,j>=2`, the
remaining matrix still contains the exceptional edge.  Partitioning its
matchings according to that edge gives

```text
C_ij=(q-3)!!-(q-1)(q-5)!!=-2(q-5)!!=beta.            (9)
```

Put `k=q-2`.  The vector `e_0-e_1` is a `C(A)` eigenvector with eigenvalue
`-alpha`.  The `(k-1)`-dimensional space supported on `{2,...,q-1}` with
coordinate sum zero has eigenvalue `-beta=2g`.  On the remaining space
spanned by

```text
s=e_0+e_1,                t=sum_(j=2)^(q-1)e_j,
```

the matrix is

```text
[ alpha       alpha k       ]
[ 2 alpha     beta(k-1)     ].                       (10)
```

Its determinant is

```text
-2 g^2 (q-3)^2 (q-1).                                (11)
```

Multiplying (11) by `-alpha` and `(-beta)^(q-3)` gives (8).  Every factor is
nonzero in characteristic zero.

At the first order `q=4`, the example is

```text
A_01=-2,           every other edge=1,

C(A)=[ 0  1  1  1]
     [ 1  0  1  1]
     [ 1  1  0 -2]
     [ 1  1 -2  0],             det C(A)=12.         (12)
```

Thus even the smallest residual order beyond the automatic two-residual
case already has `h=0` and maximal cofactor rank simultaneously.

## Sharpness for the common cofactor Gram locus

For any family of ports, subtract the direct layer and concatenate their
residual incidence maps:

```text
K_uv=H_uv-hB_uv=R_u^T C(A)R_v,
K=R^T C(A)R.                                         (13)
```

Choose enough scalar port directions that their concatenated incidence map
is `R=I_q`.  Then the canonical completed response is

```text
K=C(A),                     rank K=q.                (14)
```

This has an honest loopless symmetric block realization.  Fix residual
vectors `z_p` and covectors `ell_p` with `ell_p(z_p)=1`.  Realize the
residual edge value `A_pq` by

```text
B_pq=A_pq ell_p tensor ell_q
```

and its transpose, and realize a desired port incidence coordinate by the
corresponding rank-one port--residual block.  Set every direct port edge to
zero.  Contraction against the `z_p` gives exactly (4) and (14).

For a fully observable version, take two disjoint families of `q` scalar
ports, give the `i`th port in each family incidence row `e_i^T`, and inspect
the cross-family response.  Its entire `q`-by-`q` block, including the zero
diagonal positions of `C(A)` as cross-family port pairs, is exactly `C(A)`.
Thus its observable cross-rank is `q`.

Therefore neither graph symmetry, looplessness, `h=0`, nor arbitrary port
incidence lowers the general rank bound.  This realization is only a scalar
boundary-response network.  It is not asserted to satisfy a GHZ target or
the root/blocker incidence ledgers of a hypothetical witness.

Define the **bosonic cofactor--Gram locus** at residual order `q` by

```text
G_q={ (hB_uv+R_u^T C(A)R_v)_(u<v) }.                 (15)
```

There is a stronger universality statement.  Fix the example's nonsingular
middle form `C_0=C(A)`.  Over `C`, every symmetric matrix `K` of rank at most
`q` has a factorization

```text
K=R^T C_0 R.                                           (16)
```

Indeed, complex congruence gives `C_0=S^T S`; the same classification gives
`K=L^T L` with `L` having `q` rows after zero padding, and one may take
`R=S^(-1)L`.  Hence the fixed `h=0` residual already fills the whole
symmetric rank-at-most-`q` determinantal locus as the incidence varies.
There are no stronger universal polynomial **rank** equations at the
two-port level.  Any stronger equation must use data omitted there:
prescribed root permanents, common physical incidence across additional
deletions, mixed-colour vanishing, or deeper principal-cofactor
compatibility.

## Exact canonical synchronized-channel calculus

The rank statement has an exact permanent interpretation over `C`.  For a
complex symmetric matrix `C`, define its bosonic channel number by

```text
chi(C)=min{k:C=sum_(a=1)^k
  (ell_a m_a^T+m_a ell_a^T)}.                        (17)
```

### Theorem 3 (minimal channel number)

```text
chi(C)=ceiling(rank(C)/2).                           (18)
```

The lower bound follows because each summand in (17) has rank at most two.
For the upper bound, quotient by the radical and diagonalize the complex
symmetric form by congruence as

```text
C=sum_(i=1)^rho x_i x_i^T.
```

Pair two consecutive rank-one terms by putting

```text
ell=(x_i+sqrt(-1)x_(i+1))/sqrt(2),
m  =(x_i-sqrt(-1)x_(i+1))/sqrt(2).                  (19)
```

Then `ell m^T+m ell^T=x_i x_i^T+x_(i+1)x_(i+1)^T`.
If `rho` is odd, the last term is obtained from
`ell=m=x_rho/sqrt(2)`.

Apply (17) to the common cofactor matrix and define the synchronized port
rows

```text
g_(a,u)=R_u^T ell_a,          k_(a,u)=R_u^T m_a.
```

The corrected response becomes

```text
K_uv=sum_(a=1)^chi(C)
  (g_(a,u) tensor k_(a,v)+k_(a,u) tensor g_(a,v)).  (20)
```

For `r` root rows and `r+2` blocker columns, unsigned two-row Laplace
expansion therefore gives the exact aggregate

```text
sum_(u<v) F_uv K_uv
 =sum_(a=1)^chi(C) P_(r+2)(H;g_a;k_a).              (21)
```

This is a synchronized-channel decomposition through the common middle
form, using the minimum number of channels needed to represent `C` itself.
For a fixed port family, incidence rank collapse may let the completed
observable form `R^T C R` use fewer channels.  Thus `rank C<=2` guarantees
one synchronized `P_(r+2)`, but it is not necessary after specialization.
When several observable channels remain, the original graph equation
constrains their sum; no individual channel may be set equal to `Delta_3`.

For the family (4), Theorem 2 and (18) give, for the full canonical middle
matrix with its prescribed zero diagonal,

```text
chi(C(A))=q/2.                                       (22)
```

Thus `h=0` coexists with maximum canonical channel number.  This does not
yet say how many channels the physical off-diagonal blocks or their
permanent aggregate require.

### Canonical versus physical channel number

The graph does not expose the latent diagonal blocks `K_uu`.  Alternative
diagonal completions can lower rank, and the two-row Laplace aggregation can
collapse it further.  This already happens in the `q=4` example.  Let
`omega^2+omega+1=0` and put

```text
ell=(-omega^2,-omega,-1,-1)^T,
m  =( omega, omega^2, 1, 1)^T.                       (23)
```

Then

```text
C_tilde=ell m^T+m ell^T
       =[-2  1  1  1]
        [ 1 -2  1  1]
        [ 1  1 -2 -2]
        [ 1  1 -2 -2].                              (24)
```

The off-diagonal entries of `C_tilde` equal those of the full-rank canonical
matrix (12), but `rank C_tilde<=2`.  With four scalar ports and `R=I_4`, the
physical off-diagonal response therefore has a one-channel completion and
its root aggregate can be one `P_4`, even though `chi(C(A))=2` canonically.

Hence (22) is a sharp statement about the specified middle form `C(A)`, not
a lower bound on the number of observable permanent summands.  The latter
is a structured low-rank-completion problem followed by the Laplace map.

For a hollow scalar response matrix `M`, define its **off-diagonal bosonic
channel number** by

```text
chi_off(M)=min_(d in C^n) chi(M+diag(d))
          =min_(d in C^n) ceiling(rank(M+diag(d))/2).
```

This is the exact one-level invariant seen by physical pair responses.  The
matrix (24) proves `chi_off(C(A))=1` at `q=4`: it is at most one by the
displayed completion and at least one because the off-diagonal response is
nonzero.  The permanent aggregate can have still smaller complexity because
the unsigned Laplace map can identify different off-diagonal responses.

## Separator rank: when graph structure really lowers the channels

There is a positive graph-theoretic criterion.  Partition the contracted
scalar residual graph as

```text
Q=X disjoint_union S disjoint_union Y
```

and assume there are no `X--Y` edges.  Assign every edge internal to `S` to
the left subgraph: `G_L` contains the `X--X`, `X--S`, and `S--S` edges,
while `G_R` contains the `Y--Y` and `Y--S` edges.  For `p in X`, `q in Y`,
and `T subset S`, put

```text
L_p(T)=Z(G_L[(X minus {p}) union T]),
R_q(S minus T)=Z(G_R[(Y minus {q}) union (S minus T)]), (25)
```

where `Z` is the weighted perfect-matching sum.

### Theorem 4 (residual separator convolution)

```text
C(A)_pq=sum_(T subset S) L_p(T)R_q(S minus T).       (26)
```

Only subsets with

```text
|T| congruent |X|-1 (mod 2)                         (27)
```

can contribute.  Hence, for nonempty `S`,

```text
rank C(A)_(X,Y)<=2^(|S|-1).                         (28)
```

Proof.  In a matching of `G-{p,q}`, let `T` be the separator vertices used
by the left matching.  With the internal `S` edges assigned left, the two
restrictions are disjoint and exhaustive, and conversely their union is one
matching.  This gives (26).  The left vertex count gives (27), leaving at
most `2^(|S|-1)` outer-product columns in (26).

An articulation separator `|S|=1` therefore forces the cross-cofactor block
to have rank at most one.  If two port families attach only through `X` and
`Y`, the physical corrected response cross-block inherits the same bound.
A rank-`r` rectangular cross-block and its transpose have a symmetric
completion of rank at most `2r`, so (18) gives at most `r` synchronized
left--right channels.  Equation (28) therefore supplies at most
`2^(|S|-1)` such channels.

This is the correct limited role for locality: `h=0` alone does not lower
the cofactor rank, while a small residual separator lowers the designated
`X--Y` cross-response.  It does **not** lower the full cofactor rank or total
`P_7` channel count unless every relevant blocker pair and port incidence is
proved to cross that separator.  Under a unique residual perfect matching,
the same cross-response refines to a weighted alternating-path matrix; the
marked-response separator theorem in
`ARBITRARY_PERMANENT_THREE_EXCESS_MARKED_RESPONSE_TORIC_HOLONOMY_BOUNDARY.md`
is its boundary analogue.

## The strongest exact obstruction left by the decomposition

Let `rho=rank C(A)`.  For disjoint lists of three-dimensional anchor ports
`D,A` of length `k`, assume the physical cross-block `K_DA` is invertible.
The common Gram theorem gives

```text
S=K_UX-K_UA(K_DA)^(-1)K_DX,
rank S<=rho-3k.                                      (29)
```

Equivalently, after clearing `det K_DA`, all minors of size
`rho-3k+1` vanish.  The present theorem proves that on `h=0` one must still
allow `rho=q`.  Hence the unconditional residual-order consequences are

```text
q=2:  rank K<=2; the factorization is universally realizable;
q=4:  one invertible 3D anchor leaves rank S<=1;
q=6:  one invertible 3D anchor leaves rank S<=3;
q=6:  two invertible 3D anchors force S=0;
general q: use rho=q unless an independent cofactor-rank theorem applies.
                                                               (30)
```

For `q=2`, `h=0` gives

```text
C(A)=[0 1;1 0],
K_uv=a_u tensor b_v+b_u tensor a_v.                 (31)
```

That is the only residual order at which one channel is automatic before
incidence or completion collapse, and the two residual rows combine into
one honest `P_(r+2)` Laplace expansion.  For arbitrary `q`, the root
aggregate is instead a `C(A)_pq`-weighted **sum** of `P_(r+2)` extensions.
It is not one permanent restriction and does not equal `Delta_3` without a
separate equation inherited from the hypothetical full graph witness.
The `q=2` statement concerns this corrected two-port slice only; its isolated
legal realization does not construct the tangent-completed or globally
legal `P_7` system.

## Consequences for the active branches

The theorem changes the proof priorities but closes no global branch.

1. **Two-residual `P_7` cell.**  The cofactor--Gram representation is
   automatic and legally realizable.  The useful equations must come from
   lower-root deletion values, mixed-colour cancellation, Hall incidence,
   or a target-compatible cumulant.  Rank alone cannot close it.
2. **Four-or-more-residual cells.**  Choosing `h=0` removes the direct layer
   but does not reduce the middle rank.  An obstruction needs an exposed
   invertible anchor and the Schur defect (29), or deeper cofactor
   integrability; a bare `det C=0` claim is false.
3. **Coordinate-monomial residual branch.**  The torus-zero construction is
   unavailable there by definition.  Its off-slice and coordinate-boundary
   equations remain `UNKNOWN`.
4. **Small residual separators.**  Equation (28) can reduce a designated
   cross-response.  It becomes a `P_7` obstruction only after proving that
   all relevant blocker pairs and port incidences are cross-localized.
5. **Existing `P_5/P_6` strict-support consequences.**  They are unchanged.
   This note supplies no new nonrestriction theorem for unrestricted
   `P_5`, `P_6`, or `P_7`.

The next exact test should impose one actual lower mixed-Hessian or
four-point square-zero cumulant on the `q=2` cofactor frame.  That is the
first deletion depth not already absorbed by the universally realizable
two-port Gram layer.

## Literature boundary

Graphical condensation expresses matching counts through Pfaffian or
determinantal identities under planar boundary hypotheses, or after some
other independently proved Pfaffian orientation with deletion-compatible
signs; see Ciucu,
[*A generalization of Kuo
condensation*](https://arxiv.org/abs/1404.5003), and Fulmek,
[*Graphical Condensation, Overlapping Pfaffians and Superpositions of
Matchings*](https://doi.org/10.37236/355).  For `q>=6`, the complete support
of (4) is nonplanar.  At `q=4`, its `K_4` support is planar, but the required
cofacial/deletion-sign hypotheses are not supplied.  In neither case does
planarity by itself force the all-plus cofactor matrix to be singular.

The newly exposed physical invariant belongs instead to symmetric
minimum-rank completion.  Bernstein, Blekherman, and Lee's
[*Typical ranks in symmetric matrix
completion*](https://arxiv.org/abs/1909.06593) studies how minimum complex
completion rank depends generically on the specified-entry pattern.  Here
the specified entries are all off-diagonal pair responses, the diagonal is
latent, and the particular cofactor array (12) is highly nongeneric; the exact
`chi_off` stratum, rather than generic completion rank, is the relevant
object.  Positive-semidefinite Gram dimension provides a nearby
graph-minor/treewidth language (Laurent and Varvitsiotis,
[*A new graph parameter related to bounded rank positive semidefinite matrix
completions*](https://arxiv.org/abs/1204.0734)), but positivity is absent from
the complex bilinear hafnian problem, so its bounds do not transfer without
a new argument.

The correct universal framework is bosonic Wick expansion: the two-port
response is the first polarization of `haf(A)`, and deeper deletion
compatibility comes from higher square-zero derivatives.  The explicit
full-rank point above shows why determinant-adjugate intuition does not
transfer to the hafnian gradient.

## Scope wall

```text
general residual-hafnian two-port decomposition:        PROVED PREVIOUSLY;
explicit h=0 residual family for every even q>=4:        CONSTRUCTED;
principal cofactor determinant formula (8):              PROVED;
h=0 implies rank C(A)<=q-1:                              FALSE;
common Gram rank bound <=q on h=0:                       SHARP;
minimal canonical channel number over C:                 ceil(rank C/2);
full-rank h=0 family canonical channel number:            q/2;
physical off-diagonal q=4 channel number:                 CAN DROP TO ONE;
off-diagonal bosonic channel number chi_off:              DEFINED EXACTLY;
separator cross-rank bound 2^(|S|-1):                    PROVED;
separator lowers full C or total P_7 channels:            NOT AUTOMATIC;
q=2 corrected factorization legal realization:           PROVED PREVIOUSLY;
q>=4 stronger rank from torus zero alone:                IMPOSSIBLE;
Schur-defect obstruction after an invertible anchor:      PROVED PREVIOUSLY;
lower mixed-jet/cumulant incompatibility:                 UNKNOWN;
coordinate-monomial residual branch:                     UNKNOWN;
unrestricted P_5, P_6, or P_7 nonrestriction:            UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_residual_hafnian_torus_zero_full_rank_cofactor_boundary.py
python audit_residual_hafnian_torus_zero_full_rank_cofactor_boundary.py
```

The primary verifier checks the symbolic determinant factorization, the
closed deletion formula through several exact even orders, the paired-channel
identity and a representative four-column two-row Laplace identity by
square-zero coefficient extraction, the `q=4` one-channel off-diagonal
completion, and a representative symbolic articulation-separator
factorization.  The
independent no-import audit rebuilds the matrices and determinants with
integer row elimination and separately checks the rank-one separator block.
Neither replay enumerates perfect matchings, port supports, or colour words;
the written matching partitions prove every even order.
