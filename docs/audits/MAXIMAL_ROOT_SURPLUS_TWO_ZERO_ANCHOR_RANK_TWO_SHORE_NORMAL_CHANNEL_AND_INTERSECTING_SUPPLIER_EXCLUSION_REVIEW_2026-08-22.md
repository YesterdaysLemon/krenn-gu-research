# Hostile review: zero-anchor rank-two-shore normal channel and four-port full-activity exclusion

## Decision

**Accept as scoped theorem `GLS29` after substantive revision.**  On the
`GLS28` branch with `(d_0,d_1)=(2,2)`, the product of the two residual-shore
normals is the exact dual of the one-dimensional quotient
`E/P_Q(T_Q)`.  It turns every promoted pair supplier into a common two-channel
tensor, gives an exact image of the complete `GLS23` nuisance, and contracts
the complete physical GHZ equation to one arbitrary-root mixed-response
identity.

The first draft proved only that full normal activity plus universal useful-
row failure would force and then exclude certain support shapes.  Independent
hostile derivation found the stronger fact and exposed two omitted audit
obligations: local rank zero and the zero Hadamard-product subcase at local-
rank profile `1+2+2+2`.  The accepted revision handles both without division
and proves that the entire `r=3` full-normal-activity locus is empty.  It does
not close the normal-product divisor, higher root orders, other shore ranks,
or the strategic node.  The global conjecture remains **UNRESOLVED**.

## 1. Root quotient and tensor-type audit

Let `n_i` span `X_i^perp` and `rho=n_0 tensor n_1`.  The functional `rho`
kills `T_Q`, `q`, and therefore `P_Q(T_Q)`.  It cannot vanish on all of
`E=ker epsilon_A`: otherwise it would be proportional to `epsilon_A`, and
evaluation at `q` would force the proportionality scalar to vanish because
`epsilon_A(q)=p!=0`.  Since `P_Q(T_Q)` has dimension seven in the
eight-dimensional transverse root space, its kernel is exact.

For a promoted pair `D={u,v}`, zero anchor removes the internal `A` matching,
so the two remaining cross matchings give

```text
(rho tensor id)(t_D)
 =p(x_u tensor y_v+y_u tensor x_v)=p k_D.
```

Here `k_D` lives on the supplier pair `D`.  It is not the `GLS8` physical
response, which lives on `Uhat-D`.  The accepted theorem keeps those types
separate throughout.

## 2. Complete nuisance and selector audit

Apply `rho` label by label to the exact `GLS23` pair-target decomposition.

- The top label vanishes because `omega=0`.
- The `Q` label is zero.
- Every one-`Q` label lies in `P_Q(T_Q)` and is killed.
- A promoted pair sharing one target port gives the slice of its `k` tensor
  at the foreign port, padded by the other receiving-target factor.
- A nonzero promoted pair disjoint from the target has a nonzero full scalar
  slice and fills the entire **normal image** of the receiving target.

Thus, absent a disjoint nonzero supplier,

```text
M_(uv)=A_(u|v) tensor V_v^*+V_u^* tensor A_(v|u).
```

This is equality for `(rho tensor id)(N_D^tr)`, not equality for the full
nuisance.  A port functional separating `k_D` or a normal pure diagonal from
`M_D` yields a product selector annihilating the complete nuisance; `GLS22`
then lifts it to the full quotient.  Conversely, full useful-row failure puts
every active normal pure diagonal in `M_D`.  No converse from normal-image
absorption to full absorption is used.

## 3. Complete mixed identity and arbitrary-root consequences

Expanding the complete physical coefficient tensor by the pair matched to
`A`, then applying the two shore normals, gives exactly

```text
sum_D k_D tensor P_(Uhat-D)(H;z_Q)
 =sum_c alpha_c gamma_c e_c^(tensor Uhat).
```

No response or normal coordinate is inverted.  Its all-`c` coefficient forces
one supplier with both nonzero `(c,c)` coefficient and nonzero pure-`c`
response.  Contracting every port except `v` by annihilators of the local
channel spans proves that each active colour belongs to a channel span at a
second port.

On `gamma_0 gamma_1 gamma_2!=0`, pairwise-intersecting nonzero supplier
support is a star or triangle.  The star cylinder has root-side dimension at
most two and cannot absorb three pure diagonals.  In the triangle, pair-target
failure makes the three local channel spans the distinct coordinate planes.
Taking the missing-colour coefficient at one vertex isolates the opposite
supplier as rank one, contradicting its exact rank-two factorization.  Thus
universal useful failure at arbitrary root order needs disjoint suppliers.
Exactly two disjoint suppliers are also impossible: after contracting all
other ports, the relevant `2+2` flattening has rank at most two on the left
and rank three on the full-activity GHZ side.

## 4. Four-port annihilator certificate

For `r=3`, set

```text
Y_i=span{x_i,y_i},        K_i=ker x_i intersect ker y_i.
```

Contracting complementary ports `k,l` by arbitrary
`z_k in K_k,z_l in K_l` kills five of the six supplier terms and gives

```text
diag(beta_c z_k(c)z_l(c))
 =R_(kl)(z_k,z_l) k_(ij).                              (A)
```

The response notation in (A) is indexed by its actual output pair `kl`; it is
not the supplier `ij`.  Since every `beta_c` is nonzero, the diagonal map is
injective.  Therefore `dim(K_k star K_l)<=1`, and a nonzero coordinatewise
product automatically makes both factors on the right nonzero and equates
its support size with `rank k_(ij)`.  If the whole product is zero, (A) infers
neither factor.  The accepted proof never divides by the scalar.

The hostile case audit is exhaustive.

- Rank zero: two full kernels violate the product-dimension bound; one full
  kernel forces the other three kernels to coordinate axes and then produces
  rank one versus rank two in (A).
- Four rank-one local channels: their four plane kernels would have to be
  pairwise distinct coordinate planes, but only three exist.
- Three rank-one channels: the plane kernels are all coordinate planes and
  the remaining kernel line is a coordinate axis; one active colour occurs at
  only one port.
- Two rank-one channels: the two plane kernels have a nonzero rank-one
  coordinate product, while the complementary rank-two/rank-two supplier has
  rank two.
- One rank-one channel: for a non-coordinate plane, the plane-line product
  lemma forces an incompatible common two-support.  For a coordinate plane,
  every product with the remaining kernel lines must be zero; all three lines
  are then its missing axis, leaving that active colour at only the rank-one
  port.  This zero-product subcase was missing from the first draft.
- No rank-one channels: kernel lines have pairwise support intersections of
  size zero or two.  Active-colour coverage bounds each coordinate's support
  degree by two.  Four nonempty subsets of a three-set cannot meet both
  conditions.

Hence the complete equation forces
`gamma_0 gamma_1 gamma_2=0` at `r=3`.  This is a branch exclusion, not a
seven-row selector package.

## 5. Cross-identity and downstream audit

The checked exchange identity is

```text
sigma_(uv) boxtimes sigma_(wx)-sigma_(ux) boxtimes sigma_(vw)
 =-p^2 delta_(uw) boxtimes delta_(vx).
```

Regrouping the complete identity at four ports gives
`X(D,sigma)=pure`.  It is not the committed `GLD3` identity
`hT=C(D)-C(K)`, and the one-dimensional root quotient is not the `GLD16`
joint `M/Z` coefficient plane.  The normal supplier lives on `D`; the promoted
response lives on its complement.  No existing theorem target-attaches the
six normal suppliers or restores the zero top row.  The package therefore
makes no downstream detector claim.

## 6. Sharpness-certificate audit

The exact rational graph datum in Proposition 7 was replayed from its edge
matrices.  It has

```text
p=2,
rank Slice_D(t_D)=8 for all six suppliers,
N_D^tr=E tensor V_D^* for all six pair targets,
all six pair responses nonzero,
global pure coefficients (1,1,1).
```

It is not a witness: coefficient `00000010` is `-3/2`, and many other mixed
coefficients are nonzero.  This validates the claimed no-go boundary.  Full
module absorption plus response nonvanishing cannot replace the original
mixed equations.

## 7. Verification and independence

The primary SymPy verifier checks the quotient normal, symbolic pair
factorization, exact nuisance cylinders, all 81 coefficients of an independent
six-vertex matching expansion, intersecting-support classification, the
four-port kernel contraction, Hadamard plane samples, the exchange identity,
compound flattening rank, and the exact graph certificate.

The independent audit imports neither SymPy nor repository code.  It uses
standard-library `Fraction`, its own Gaussian elimination, a separately
implemented recursive perfect-matching evaluation, coordinate-support
combinatorics, a separate rational kernel-contraction fixture, and an
independent replay of the graph certificate.  The arbitrary-root tensor
contractions and infinite-field Hadamard lemmas are the written proof.

Dependency replay of `GLS8`, `GLS22`, `GLS23`, `GLS26`, and `GLS28` primary
and independent audits passes.  Focused `py_compile`, `ruff check`, and
`ruff format --check` pass after revision.

## 8. Exact accepted scope

```text
rank-two-shore quotient normal and pair factorization:       ACCEPTED;
normal image of the complete pair nuisance:                  ACCEPTED;
complete arbitrary-root normal mixed identity:               ACCEPTED;
active-colour supplier/response and two-port coverage:        ACCEPTED;
full-activity intersecting supplier support:                 EXCLUDED;
full-activity r=3 locus, all local-rank/response fibres:      EXCLUDED;
same-graph absorption/response-only sharpness certificate:   ACCEPTED;

full-activity disjoint branch at r>=4:                       OPEN;
one-/two-colour normal-product divisor at r=3 and above:      OPEN;
other shore ranks and C12/C21/C22:                           OPEN;
simultaneous attachment, synchronization, downstream entry:   OPEN;
maximum-root supply/attachment strategic node:                OPEN;
global Krenn-Gu conjecture:                                  UNRESOLVED.
```
