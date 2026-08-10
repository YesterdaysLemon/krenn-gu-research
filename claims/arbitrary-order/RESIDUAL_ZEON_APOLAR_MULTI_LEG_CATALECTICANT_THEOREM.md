# Residual zeon-apolar multi-leg catalecticant theorem

## Status

**Exact arbitrary-even-residual characteristic-zero theorem with a sharp
control.**  The residual-relative response polynomial has more global
structure than the existing one-leg cross-depth rank bound records.  For
every number `k` of marked port legs, all compatible response depths factor
simultaneously through the `k`th permanental compound of the **same** residual
incidence matrix.  Consequently every disjoint square-free `k`-leg
catalecticant has rank at most

```text
binom(q,k),                                               (1)
```

where `q` is the number of residual vertices.  If the incidence restricted
to the marked port family has rank `r`, symmetric-tensor geometry sharpens
this to

```text
min{binom(q,k), binom(r+k-1,k)}.                          (2)
```

All minors one size larger vanish.  Since the relative coefficients are
recovered polynomially from the synchronized direct and residual-present
principal responses, these are exact observable all-subset equations.

For `k=1` this recovers the earlier one-leg theorem.  For `k>=2` it is a new
multi-pair/multi-leg invariant coupling the quadratic, quartic, sextic, and
higher relative layers.  It is naturally an apolar catalecticant statement,
but its middle object is a bosonic square-zero or **zeon** compound, not an
exterior compound.  Grassmannian signs and determinant identities are not
used.

The binomial bound (1) is sharp for every even `q` and every `k`: a doubled
identity-incidence chart contains a complement permutation matrix of order
`binom(q,k)`.  Thus no smaller universal catalecticant bound follows from
residual order alone.

This theorem supplies a stronger necessary test for a synchronized
all-subset response family.  It does not prove that the required deletions
are legally observable in P5/P6/P7, does not exclude the sharp identity
chart, and does not resolve Krenn--Gu.

No port family, support family, matching family, or subset profile is
enumerated in the proof.

## 1. Relative response tower

Let `Q` be an even residual set of size `q`, let `U` be scalar boundary
ports, and work in the commuting square-zero port algebra.  Retain the
notation

```text
A_pq       residual--residual edges,
R_pu       residual--port incidences,
M_B        direct principal-hafnian moment family,
Z_Q        response with all residual vertices present. (3)
```

The residual-relative polynomial is

```text
Phi=M_B^(-1) Z_Q=sum_(S subset U) phi_S x_S.             (4)
```

For every even set `S`, the residual-relative response theorem gives

```text
phi_S=sum_(T subset Q, |T|=|S|)
          haf(A[Q minus T]) per(R[T,S]),                 (5)
```

and `phi_S=0` when `|S|` is odd or exceeds `q`.

The observable response coefficients determine (4) recursively:

```text
phi_S=z_S-sum_(T proper_subset S) phi_T m_(S minus T),   (6)
```

with `phi_empty=z_empty=haf(A)`.  Therefore any polynomial equation in the
`phi_S` becomes a polynomial equation in synchronized principal deletion
data `(m_S,z_S)` after substitution of (6).

## 2. Disjoint square-free catalecticants

Choose disjoint physical port families `L,V`.  Disjointness prevents a row
port from reappearing in a column monomial; it is the square-free analogue
of polarizing the two sides of an ordinary catalecticant.

Fix `0<=k<=q`.  Define the all-depth matrix

```text
Cat_k^(L|V)(Phi)[S,W]=phi_(S union W),                   (7)
```

where

```text
S subset L, |S|=k,
W subset V, |W| congruent k (mod 2), |W|<=q-k.           (8)
```

Thus each column degree `|W|` selects the total relative depth
`k+|W|`.  Concatenating all allowed `W` puts every compatible depth into one
matrix.

For `I subset Q`, `|I|=k`, define the `k`th permanental compound

```text
P_k(R_L)[I,S]=per(R[I,S]).                              (9)
```

For a column `W` of (7), put

```text
G_k[I,W]
 =sum_(T subset Q minus I, |T|=|W|)
    haf(A[Q minus (I union T)]) per(R[T,W]).            (10)
```

The empty permanent is one.

### Theorem 1 (all-depth `k`-leg factorization)

For every `k`,

```text
Cat_k^(L|V)(Phi)=P_k(R_L)^T G_k.                        (11)
```

Consequently

```text
rank Cat_k^(L|V)(Phi)
 <=rank P_k(R_L)
 <=binom(q,k).                                          (12)
```

Proof.  Fix `S,W` and expand (5).  For each residual set
`E subset Q` of order `k+|W|`, expand the permanent of `R[E,S union W]`
along the `k` columns indexed by `S`:

```text
per(R[E,S union W])
 =sum_(I subset E, |I|=k)
    per(R[I,S]) per(R[E minus I,W]).                   (13)
```

This is the unsigned two-column-family Laplace identity.  Put
`T=E minus I`; then `T subset Q minus I` and `|T|=|W|`.  Substitution into
(5), followed by grouping on `I`, is exactly (10)--(11).  The middle row
space is indexed by the `k`-subsets of `Q`, proving (12).

No invertibility or genericity of `A` or `R` is used.  The proof is a single
matching-partition identity at arbitrary order, not a verification over a
catalogue of subsets.

### Corollary 2 (observable catalecticant minors)

Every `(binom(q,k)+1)`-minor of (7) vanishes.  After the recursion (6), these
are characteristic-zero polynomial equations in the physical all-subset
response data.

Equivalently, the restricted square-free `k`th derivative space

```text
span{ (partial_S Phi)|_V : S subset L, |S|=k }          (14)
```

has dimension at most `binom(q,k)`.  This is the apolar formulation of the
same theorem: the kernel of (7) consists of square-free order-`k`
differential operators whose restrictions annihilate every compatible
response depth on `V`.

## 3. The symmetric-tensor refinement

Let

```text
r=rank R_L.                                             (15)
```

The columns of `R_L` lie in an `r`-dimensional subspace `E subset K^Q`.
Introduce commuting square-zero residual generators `eta_p`.  For a port
`u`, its incidence column represents the linear zeon

```text
ell_u=sum_(p in Q) R_pu eta_p.                          (16)
```

For `S={u_1,...,u_k}`, the coefficient of `eta_I` in
`ell_(u_1)...ell_(u_k)` is exactly `per(R[I,S])`.  Hence the column of
`P_k(R_L)` indexed by `S` is the square-free projection of the symmetric
tensor

```text
R_(u_1) symmetric_product ... symmetric_product R_(u_k)
 in Sym^k(E).                                           (17)
```

### Theorem 3 (zeon-apolar Hilbert bound)

The entire `k`-leg derivative space satisfies

```text
rank Cat_k^(L|V)(Phi)
 <=rank P_k(R_L)
 <=min{binom(q,k), dim Sym^k(E)}
 =min{binom(q,k),binom(r+k-1,k)}.                       (18)
```

Proof.  The square-free projection

```text
Sym^k(E) -> span{eta_I: I subset Q, |I|=k}             (19)
```

contains every column (17) in its image.  Its image dimension is at most
both the source dimension `binom(r+k-1,k)` and the target dimension
`binom(q,k)`.  Combine this with (11).

The symmetric dimension in (18) is essential.  An exterior compound would
give `binom(r,k)`, but permanents are symmetric products before the
square-free projection.  Importing the exterior bound would be false in
general.

For `k=2`, (18) gives the useful multi-pair equation

```text
rank Cat_2^(L|V)(Phi)
 <=min{q(q-1)/2, r(r+1)/2}.                             (20)
```

Thus a low-rank incidence chart forces all quadratic, quartic, sextic, and
higher pair-marked layers into one small row space.  Separate per-depth rank
tests do not impose this common row space.

## 4. Top-degree polar pairing

At total degree `q`, the residual cofactor is empty and

```text
phi_(S union W)=per(R[Q,S union W]),  |S|+|W|=q.        (21)
```

Let `J_k` be the complement pairing between `k`-subsets and
`(q-k)`-subsets of `Q`:

```text
J_k[I,T]=1 if T=Q minus I, and 0 otherwise.             (22)
```

The top-degree block of (11) refines to

```text
Cat_(k,q-k)^(L|V)(Phi)
 =P_k(R_L)^T J_k P_(q-k)(R_V).                          (23)
```

This is a bosonic polar pairing.  It couples two complementary permanental
compounds of the same incidence matrix and is stronger data than an
unstructured rank factorization.

## 5. Sharpness by doubled identity incidence

Take disjoint port lists

```text
L={l_1,...,l_q},       V={v_1,...,v_q},                (24)
```

put `A=0`, and use the doubled identity incidence

```text
R_(p,l_i)=R_(p,v_i)=delta_(p,i).                        (25)
```

Only the top relative layer survives.  For `I subset Q`, `|I|=k`, and
`J subset Q`, `|J|=q-k`,

```text
phi_({l_i:i in I} union {v_j:j in J})
 =1 if J=Q minus I,
 =0 otherwise.                                         (26)
```

Indeed, the selected incidence columns form a permutation matrix precisely
in the complementary case; otherwise a residual row is repeated or absent.
Therefore the top-degree catalecticant contains `J_k` itself.

### Theorem 4 (universal sharpness)

For every even `q` and every `0<=k<=q`, there is a residual-relative
response with

```text
rank Cat_k^(L|V)(Phi)=binom(q,k).                       (27)
```

Thus the residual-order bound (1) cannot be lowered without additional
hypotheses on incidence rank, the target equations, port availability, or
cross-depth observability.

This is a sharp response control, not a Krenn--Gu construction.  It makes
the top relative permanent nonzero and intentionally has `haf(A)=0` and no
lower relative layers.

## 6. Gaussian/cumulant and apolar interpretation

The coefficient tower (5) is the moment tower of a formal zero-mean Gaussian
residual system in which selected residual legs are exported through `R` to
square-free ports.  Dividing by `M_B` removes the independent direct Gaussian
port sector.  Theorem 1 then says that every marked derivative of the
relative tower passes through a fixed finite residual state space; Theorem 3
identifies its order-`k` state space with a square-free projection of
`Sym^k(E)`.

This is analogous to an apolar Hilbert-function bound, but the relevant
algebra is the commuting zero-square algebra.  Feinsilver and McSorley call
the induced matrices **zeon powers** and identify their entries with
permanents ([International Journal of Combinatorics 2011](https://doi.org/10.1155/2011/539030)).
Classical and multigraded apolarity use catalecticant ranks to measure
derivative spaces ([Galazka, *Multigraded apolarity*](https://doi.org/10.1002/mana.202000484)).
Gaussian moment varieties provide the ambient algebraic-statistical language
([Amendola--Faugere--Sturmfels](https://arxiv.org/abs/1510.04654)), while the
apolar ideal of a generic permanent has its own determinantal/permanental
structure ([Shafiei](https://arxiv.org/abs/1212.0515)).

None of those papers directly states (11).  The problem-specific content is
that **all residual deletion depths use one incidence matrix and one nested
principal-hafnian cofactor tower**, so their square-free catalecticants must
factor together.

## 7. Consequence for the active bottleneck

The exact symbolic test is now:

```text
synchronized principal responses M_B,Z_Q
 -> recover Phi by (6)
 -> form one all-depth Cat_k for each useful disjoint split L|V
 -> test the binomial and incidence-rank minors (12),(18)
 -> at top depth, test the complement polar factorization (23). (28)
```

At residual order two, the previously proved dual-Wick+cumulant/channel
criterion is already a complete classification of an isolated scalar
all-subset slice.  The present theorem does not invent an additional q=2
equation; it explains why the one-leg channel is the entire residual state
space there.  New information starts at `q>=4`, when `k>=2` compounds and
multiple relative depths coexist.

For P5/P6/P7 the remaining obstacle is observational: a hypothetical witness
must expose enough synchronized deletion faces from one physical chart to
form (7).  A top response alone cannot be inserted into these minors.

## Scope wall

```text
arbitrary-k all-depth factorization (11):             PROVED;
universal rank <=binom(q,k):                           PROVED;
incidence-rank refinement (18):                       PROVED;
observable minor equations after relative recursion: PROVED;
top-degree complement polar pairing (23):             PROVED;
universal binomial bound sharp:                       PROVED;
q=2 extra isolated-slice invariant beyond prior test: NONE;
legal P5/P6/P7 observation of a nontrivial Cat_k:      UNKNOWN;
GHZ-derived violation of a multi-leg minor:            NOT YET FOUND;
classification of q>=4 relative response image:       UNKNOWN;
unrestricted P5/P6/P7 nonrestriction:                 UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_residual_zeon_apolar_multi_leg_catalecticant.py
python audit_residual_zeon_apolar_multi_leg_catalecticant.py
python -m py_compile verify_residual_zeon_apolar_multi_leg_catalecticant.py audit_residual_zeon_apolar_multi_leg_catalecticant.py
uv run --with ruff ruff check verify_residual_zeon_apolar_multi_leg_catalecticant.py audit_residual_zeon_apolar_multi_leg_catalecticant.py
```

The primary verifier checks the symbolic `q=4,k=2` all-depth factorization,
the rank-two-incidence symmetric-square factor, and every sharp doubled-
identity complement pairing at `q=4`.  The independent no-import audit uses
separate exact integer hafnian/permanent recurrences on a nontrivial
`q=4,k=2` all-depth chart and a rational Gaussian-elimination rank routine.
Neither replay searches port systems, support patterns, matchings, or subset
profiles.
