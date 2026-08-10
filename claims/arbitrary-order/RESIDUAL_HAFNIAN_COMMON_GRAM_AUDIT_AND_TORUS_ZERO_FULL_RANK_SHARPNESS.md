# Common residual-hafnian Gram audit and torus-zero full-rank sharpness

## Status

**Independent arbitrary-order validation, a corrected field-independent
torus proof, and a sharp characteristic-zero countermodel.**  The common
cofactor Gram factorization in
`RESIDUAL_HAFNIAN_COMMON_COFACTOR_GRAM_THEOREM.md` is correct for every even
residual set.  Its root-permanent aggregate has no missing factor of two, and
its common completion and Schur-defect bounds follow from one shared
symmetric middle form exactly as claimed.

Two refinements are essential.

1. The torus dichotomy is valid over every characteristic-zero field, but the
   displayed Nullstellensatz proof should not be used over a field that is
   not algebraically closed.  A direct multilinear finite-union argument
   proves the stated conclusion over every infinite field.
2. The branch `h=haf(A)=0` does **not** lower the rank of the cofactor matrix.
   For every even `q>=2` there is an explicit residual matrix with `h=0` and
   `rank C(A)=q`.  For `q>=4` every residual edge in the construction is
   nonzero.  Hence the common Gram rank bound `rank K<=q` is sharp even at an
   honest torus residual zero.

The new intrinsic compatibility equation is

```text
(A Hadamard C(A)) 1 = h 1.                            (1)
```

On the zero branch this is a balanced Hadamard-stress equation, but the
full-rank construction proves that it is not a determinant or rank-drop
equation for `C(A)`.

These results are necessary response identities and sharp controls.  The
full-rank residual graph is not a `P_m -> Delta_3` restriction, does not
satisfy the global mixed-colour equations, and is not a counterexample to
Krenn--Gu.  The global conjecture remains **UNRESOLVED**.

No support, graph-family, matching-family, colour-word, or tuple enumeration
is used.

## 1. Exact universal two-port statement

Let `K` be a characteristic-zero field, let `Q` be even, and let `A` be the
hollow symmetric scalar residual matrix after fixed residual contractions.
Put

```text
h=haf(A),
C_pq=haf(A[Q minus {p,q}])  (p!=q),
C_pp=0.                                               (2)
```

For a port `u`, let `R_u:V_u -> K^Q` be its residual-incidence map, and let
`B_uv` be the direct port edge.  Matching the two open ports either to one
another or to two distinct residual vertices gives

```text
H_uv=h B_uv+R_u^T C(A) R_v.                           (3)
```

This proof is exhaustive at arbitrary order.  If `u` matches `v`, the
remaining matching has weight `h`.  Otherwise the ordered choices
`u--p,v--q` leave `Q minus {p,q}` and contribute
`(R_u)_p C_pq (R_v)_q`.  The matrix product in (3) sums both orientations for
each unordered residual pair, exactly once each.  There is no factor two.

For any port family, set

```text
K_uv=H_uv-hB_uv,
K_uu=R_u^T C(A)R_u,
R=[R_u]_u.                                            (4)
```

Then

```text
K=R^T C(A)R,             rank K<=rank C(A)<=|Q|.      (5)
```

Every physical rectangular cross block has the same rank bound without
using the latent diagonal.  If a `d k x d k` anchor cross block is invertible,
the standard oblique projection through it has rank `d k`, so the associated
Schur defect has rank at most `rank C(A)-d k`.  This validates the completion,
minor, and holonomy conclusions in the audited note.

The empty residual case has `h=1`, `C` empty, and `H_uv=B_uv`.  It is the
rank-zero endpoint of the same statement.

## 2. Root-permanent aggregate and the ordered-pair check

Let `r` root rows meet `r+2` blockers.  For ports `u,v`, let `F_uv` be the
permanent of the root rows on the other `r` blockers, and let `a_p` be the
blocker row incident to residual vertex `p`.  Substitution of (3) gives

```text
sum_(u<v) F_uv H_uv
 =h sum_(u<v)F_uv B_uv
  +sum_(p<q) C_pq P_(r+2)(H_1,...,H_r,a_p,a_q).      (6)
```

Indeed, Laplace expansion of the last permanent along its two labelled rows
is

```text
sum_(u<v)F_uv
 [a_p(u)a_q(v)+a_p(v)a_q(u)].                         (7)
```

The two summands in (7) are precisely the ordered `(p,q)` and `(q,p)` terms
in `R_u^T C R_v`.  Equation (6) is therefore exact at every `r`.

## 3. The Hadamard-stress identity

Expand the residual hafnian along a fixed residual vertex `p`.  One obtains

```text
sum_(q!=p) A_pq C_pq=h.                               (8)
```

Let `W=A Hadamard C(A)`.  It is hollow and symmetric, and (8) for every row
is exactly

```text
W 1=h 1.                                              (9)
```

Summing all rows and dividing by two recovers the homogeneous Euler identity

```text
sum_(p<q) A_pq C_pq=(|Q|/2)h.                        (10)
```

### Theorem 1 (balanced cofactor stress)

Every residual middle form has a common scalar matrix `A` for which (9)
holds.  On the residual-zero branch,

```text
(A Hadamard C(A))1=0.                                 (11)
```

Thus any proposed common middle form together with its claimed residual
edge matrix fails representability immediately if (9) fails.  This is
stronger than checking the Gram rank alone because it retains the actual
residual edge parameters.

Equation (11) must not be misread as `C(A)1=0` or `det C(A)=0`.  The next
section gives a full-rank zero-hafnian family.

## 4. An arbitrary-order torus-zero full-rank family

First let `q=2`.  Taking `A_12=0` gives

```text
h=0,                 C(A)=[0 1;1 0],                 (12)
```

so `C(A)` already has full rank two.

Now let `q>=4` be even.  Index the residual vertices by `1,...,q` and put

```text
A_12=-(q-2),
A_ij=1 for every other i<j.                           (13)
```

All edges are nonzero.  Write `(-1)!!=1`.  A matching containing edge `12`
has `(q-3)!!` possible complements.  The number not containing `12` is
`(q-2)(q-3)!!`.  Therefore

```text
haf(A)=[-(q-2)+(q-2)](q-3)!!=0.                      (14)
```

The cofactors have only two values:

```text
alpha=(q-3)!!,
beta=-2(q-5)!!,

C_ij=alpha if {i,j} meets {1,2},
C_ij=beta  if i,j>=3.                                 (15)
```

Here `C_12=alpha` as well.  Put `m=q-2` and `c=(q-5)!!`, so
`alpha=(q-3)c` and `beta=-2c`.

The vector `e_1-e_2` is a `C`-eigenvector of eigenvalue `-alpha`.  The
sum-zero subspace on vertices `3,...,q` has dimension `q-3` and eigenvalue
`-beta`.  On the remaining span

```text
u=e_1+e_2,              v=e_3+...+e_q,               (16)
```

the matrix is

```text
[ alpha       m alpha       ]
[ 2 alpha     beta(m-1)     ],                        (17)
```

whose determinant is

```text
alpha beta(m-1)-2m alpha^2
 =-2(q-1)(q-3)^2 c^2 !=0.                             (18)
```

Consequently

```text
det C=(-alpha)(-beta)^(q-3)
      [-2(q-1)(q-3)^2 c^2] !=0.                       (18a)
```

All factors are nonzero in characteristic zero.

### Theorem 2 (zero-hafnian full-cofactor-rank sharpness)

For every even `q>=2`, a hollow symmetric `q x q` matrix satisfies

```text
haf(A)=0,                    rank C(A)=q.              (19)
```

For `q>=4`, (13) has complete nonzero support.  Hence neither residual
hafnian cancellation, absence of support zeros, nor the Hadamard-stress
identity forces `rank C(A)<=q-1`.

This is an honest torus residual specialization.  Take every residual
kernel space to be `K_i=K^3`, choose `z_i=(1,1,1)`, and choose a covector
`ell_i` with `ell_i(z_i)=1`; define
the residual edge block to be

```text
B_ij=A_ij ell_i tensor ell_j.                         (20)
```

The contraction at the coordinatewise-nonzero vectors `z_i` is exactly
(13).  Thus alternative one of the torus dichotomy can occur while the
common cofactor form is nondegenerate.

## 5. Sharpness of the common Gram obstruction

Use the full-rank `C(A)` from Theorem 2 and choose aggregate port-incidence
maps containing the identity `K^q -> K^q`.  Then the completed corrected
Gram matrix contains `C(A)` itself and has rank exactly `q`.  Likewise, two
disjoint port lists whose aggregate incidence maps are both the identity
give a completely physical rectangular cross block

```text
K_UV=C(A),                    rank K_UV=q.             (21)
```

### Corollary 3

The universal minors of size `q+1` and the Schur-defect bounds in the common
Gram theorem are sharp on the branch `h=0`.  No universal `q x q` determinant
vanishing, rank-`q-1` completion, or stronger Schur decrement can follow from
residual cancellation alone.

Over an algebraically closed field of characteristic not two, every
nondegenerate symmetric form of dimension `q` is congruent.  Consequently,
at the level of two-port tensors, a full-rank zero-hafnian `C(A)` is as
flexible as a generic nondegenerate Gram middle form.  The remaining special
hafnian information lies in compatibility with `A`, equation (9), and deeper
cofactor levels--not in an extra rank loss.

This does not say that every off-diagonal block family has a rank-`q`
symmetric completion.  Completion remains a genuine global obstruction.

## 6. The two-residual endpoint is automatic

For `Q={p,q}`,

```text
C(A)=[0 1;1 0]
```

independently of `A_pq`.  Hence

```text
K_uv=a_u tensor b_v+b_u tensor a_v.                  (22)
```

For one port pair this is simply a rank-at-most-two factorization and is
automatic for every corrected matrix of rank at most two.  The meaningful
content is simultaneous: all port pairs must use the same two-dimensional
residual state space and admit one rank-two symmetric completion.

On `h=0`, one merely has `A_pq=0`; the middle matrix (12) remains invertible.
Thus the automatic `q=2` formula is the smallest instance of the full-rank
escape, not evidence for a stronger zero-branch obstruction.

## 7. Field-independent proof of the torus dichotomy

Let each `K_i` be a finite-dimensional vector space over an infinite field,
and let `U_i` be the complement of finitely many coordinate hyperplanes.
Let `F` be multilinear, of degree one in every `K_i`.

### Lemma 4 (multilinear torus-unit lemma)

If `F` has no zero on `product U_i`, then

```text
F=lambda product_i ell_i,                             (23)
```

where every `ell_i` is proportional to one of the coordinate forms defining
the excluded hyperplanes.

Proof.  Induct on the number of factors.  The one-factor assertion follows
because the kernel of a nonzero linear form is a hyperplane.  If it is not
one of the finitely many excluded coordinate hyperplanes, it cannot be
covered by their proper intersections over an infinite field and therefore
meets `U_1`.

For the induction step, regard `F` as the linear map

```text
Phi:K_1 -> Multilinear(K_2,...,K_n).                  (24)
```

For every `x in U_1`, the form `Phi(x)` has no zero on the remaining product.
By induction it lies on one of the finitely many lines spanned by coordinate
monomials in factors `2,...,n`.  If the image of `Phi` were contained in none
of these lines, then `K_1` would be covered by their finitely many proper
linear preimages together with the excluded coordinate hyperplanes.  That is
impossible over an infinite field.  Hence `Phi(K_1)` lies in one coordinate-
monomial line and `F=ell_1 product_(i>1)ell_i`.  Finally `ell_1` has no zero
on `U_1`, so the one-factor argument makes it a coordinate form as well.
This proves (23).

Apply the lemma to the multihomogeneous residual hafnian on the spaces
`K_q`.  Characteristic zero implies the field is infinite, so the torus
dichotomy in the audited note is valid as stated.  This proof replaces the
Nullstellensatz/localization sentence when the ground field is not assumed
algebraically closed.

## 8. Exact boundary for the global problem

What is proved is

```text
arbitrary even Q two-port decomposition:      VALID;
one common Gram completion across all ports:  VALID;
root-permanent aggregate normalization:       VALID, NO FACTOR TWO;
Schur-defect and holonomy bounds:              VALID;
torus dichotomy over characteristic zero:      VALID BY LEMMA 4;
residual zero => rank C(A)<|Q|:                FALSE;
zero-branch common Gram rank bound:            |Q|, SHARP;
Hadamard cofactor stress (9):                   PROVED.
```

The full-rank family controls only the contracted residual response.  It is
not asserted to satisfy local concision, the pure GHZ coefficients, every
mixed word, or any full `P_m -> Delta_3` restriction.  It rules out an
overstrong proof route; it is not a Krenn--Gu counterexample.

The next viable use of the common Gram theorem must combine its sharp
rank-`q` completion with at least one genuinely hafnian layer:

1. the Hadamard stress (9) with a legally observed residual edge matrix;
2. four-deletion cofactors and their common derivative compatibility;
3. block-square-zero cumulants across residual depths; or
4. target equations that force a smaller residual cofactor rank for reasons
   stronger than `h=0`.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Scope wall

```text
common residual cofactor Gram theorem:                 AUDITED AND VALID;
arbitrary-order matching proof:                        PROVED;
Hadamard-stress identity:                              PROVED;
q=2 corrected factorization:                           AUTOMATIC;
q=2 middle-form rank on h=0:                           TWO, FULL;
q>=4 complete-support h=0 cofactor family:             CONSTRUCTED;
rank C(A) in that family:                              |Q|, FULL;
rank improvement from torus residual zero:             IMPOSSIBLE;
rank-|Q| common completion bound:                      SHARP;
torus dichotomy over every characteristic-zero field: PROVED;
full-rank family is a GHZ restriction:                 NOT CLAIMED;
new deeper cofactor/cumulant obstruction:              UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.
```

## Replay

Run from the repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_residual_hafnian_common_gram_audit_and_torus_zero_full_rank_sharpness.py
python claims/arbitrary-order/audit_residual_hafnian_common_gram_audit_and_torus_zero_full_rank_sharpness.py
python -m py_compile claims/arbitrary-order/verify_residual_hafnian_common_gram_audit_and_torus_zero_full_rank_sharpness.py claims/arbitrary-order/audit_residual_hafnian_common_gram_audit_and_torus_zero_full_rank_sharpness.py
uv run --with ruff ruff check claims/arbitrary-order/verify_residual_hafnian_common_gram_audit_and_torus_zero_full_rank_sharpness.py claims/arbitrary-order/audit_residual_hafnian_common_gram_audit_and_torus_zero_full_rank_sharpness.py
```

The primary verifier checks the generic two-port formula, the root-permanent
aggregate normalization, the Hadamard row identities, the full-rank family,
and sharp common Gram realizations.  The independent no-project-import audit
uses separately written integer hafnian, permanent, matrix-product, and exact
rank routines.  Its fixed small matrices audit the displayed identities;
neither replay searches supports, graphs, words, or tuple families.
