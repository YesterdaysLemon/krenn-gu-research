# Maximum-root surplus-two zero-anchor rank-four silent full-swallow complete-pair exclusion

## Status and scope

**Exact characteristic-zero arbitrary-root pointwise fibre exclusion.**  The
two complete-pair cores left by `GLS45` and structurally localized by `GLS46`
are both empty.  Equivalently, let `K` have characteristic zero, let `T` be a
finite label set, let `V_t` be finite-dimensional, and let

```text
X_t,Y_t:V_t -> K^3.
```

For distinct labels put

```text
mu_(s,t)(v,w)
 =X_s(v) tensor Y_t(w)+X_t(w) tensor Y_s(v).          (1)
```

Write

```text
Delta=span{r_0,r_1,r_2},       r_i=e_i tensor e_i,
B=Delta direct-sum K f,                              (2)
```

where `f` is nonzero and has zero diagonal.  Then the simultaneous conditions

```text
im mu_(s,t) subset B              for every s!=t,
sum_(s<t) im mu_(s,t)=B                              (3)
```

are impossible.

Applying the exact auxiliary-label bridge from `GLS46`, this excludes both
the residual-free `(0,0)` and sparse same-label `(1,1)` silent rank-four
cores.  Together with `GLS43`--`GLS45`, every zero-anchor rank-four
full-swallow fibre is empty, pointwise for arbitrary promoted root order and
every residual, support, shore-rank, incidence-rank, deck, and divisor fibre.
Thus zero-anchor full swallow begins at nuisance rank at least five.

The proof uses no same-label pair, selected response, rank minor, generic
support chart, or parameter denominator.  Characteristic zero is used only
through infinitude of the field and `2!=0`.

The theorem does not force a silent source point into full swallow, treat
ranks five through nine, attach raw escape, cover nonzero-anchor branches, or
supply response, selected activity, synchronization, nuisance survival, an
anchor, a named receiver, or arbitrary-root source coverage.  The strategic
node and the global Krenn--Gu conjecture remain **UNRESOLVED**.

This is `GLS47`.

## Dependencies and provenance

The owning interfaces are:

- [`GLS36`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md)
  for the complete incidence image;
- [`GLS39`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_COMPLETE_PAIRWISE_DIAGONAL_FAMILY_RANK_BOUND_AND_MINIMAL_RAW_SWALLOW_EXCLUSION_THEOREM.md)
  for the auxiliary complete-label interface;
- [`GLS43`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_FULL_SWALLOW_OFF_DIAGONAL_ROOT_DECK_COMPLETE_EXCLUSION_THEOREM.md)
  and
  [`GLS44`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_FULL_SWALLOW_NONZERO_DIAGONAL_ROOT_DECK_COMPLETE_EXCLUSION_THEOREM.md)
  for the nonzero-root-deck rank-four exclusions;
- [`GLS45`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_SILENT_FULL_SWALLOW_RESIDUAL_SHORE_PROFILE_REDUCTION_THEOREM.md)
  for the exhaustive two-core silent boundary; and
- [`GLS46`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_COMPLETE_PAIR_FAMILY_STRUCTURAL_DEGREE_CUT_AND_TRIANGLE_LOCALIZATION_THEOREM.md)
  for the all-cut diagonal-rank bound, triangle localization, and external
  diagonal silence.

No external literature claim is used.  The new content is synchronization of
arbitrary triangle-block vectors, invertible left--right normalization,
rank-one locking of the transformed physical diagonal, and complete
elimination of both the internal and external excess mechanisms.

## 1. Synchronized triangle

Let

```text
pi:B->Delta
```

be diagonal projection along `Kf`.  By `GLS46`, after renaming three labels,

```text
pi(im mu_(0,1))=K d_(0,1),
pi(im mu_(0,2))=K d_(0,2),
pi(im mu_(1,2))=K d_(1,2),                          (4)
```

where the three `d_(i,j)` form a basis of `Delta`.  Every other pair image
has zero diagonal projection.

For each triangle edge define its nonzero scalar bilinear coefficient by

```text
pi(mu_(i,j)(v_i,v_j))
 =beta_(i,j)(v_i,v_j)d_(i,j).                       (5)
```

### Lemma 1 (one common active vector at every triangle label)

There are `v_i in V_i` such that all three values

```text
beta_(0,1)(v_0,v_1),
beta_(0,2)(v_0,v_2),
beta_(1,2)(v_1,v_2)                                 (6)
```

are nonzero.

#### Proof

Each `beta_(i,j)` is a nonzero polynomial on `V_i direct-sum V_j`.  Their
product, viewed in the polynomial ring on
`V_0 direct-sum V_1 direct-sum V_2`, is nonzero because that ring is an
integral domain.  A nonzero polynomial over the infinite field `K` cannot
vanish on every `K`-point.  Any point where the product is nonzero gives the
required common triple. `square`

Fix such a triple and put

```text
x_i=X_i(v_i),       y_i=Y_i(v_i),
X=[x_0|x_1|x_2],    Y=[y_0|y_1|y_2],
M_(i,j)=x_i y_j^T+x_j y_i^T.                        (7)
```

The diagonal projections of the three `M_(i,j)` form a basis of `Delta`.
Consequently their span `U` is a three-space whose diagonal projection is an
isomorphism, so for one linear functional `ell:Delta->K`,

```text
U={D+ell(D)f:D in Delta}.                           (8)
```

This is a graph over the physical diagonal, not an assertion that `U=Delta`.

## 2. Invertible left--right normalization

### Lemma 2 (both selected factor matrices are invertible)

The matrices `X,Y` in (7) are invertible.

#### Proof

Suppose `h^T X=0`.  Then `h^T M_(i,j)=0` on the three generators of `U`, so
by (8),

```text
h^T D=-ell(D)h^T f                  for every D in Delta. (9)
```

As `D` varies, the image of `D |-> h^T D` is the coordinate row space on
`supp h` and has dimension `|supp h|`.  Equation (9) confines it to one
line, so `|supp h|<=1`.  If `supp h={k}`, take `D=r_k`.  The `k`th entry of
the left side is `h_k`, whereas the `k`th entry of the right side is zero
because `f_(k,k)=0`.  Thus `h_k=0`, a contradiction.  Therefore `X` has no
left kernel and is invertible.  The right-annihilator transpose proves the
same for `Y`. `square`

Apply the invertible transformation

```text
Theta(M)=X^(-1) M Y^(-T).                           (10)
```

Then

```text
Theta(M_(i,j))=S_(i,j):=e_i e_j^T+e_j e_i^T,
Theta(U)=Sym_0,                                      (11)
```

where `Sym_0` is the three-space of symmetric zero-diagonal matrices.  Since
`B=U direct-sum Kf`, put

```text
G=Theta(f),             B'=Theta(B)=Sym_0 direct-sum K G. (12)
```

The transformed physical diagonal is spanned by the three rank-one matrices

```text
A_k=Theta(r_k)
 =(X^(-1)e_k)(Y^(-1)e_k)^T.                         (13)
```

Their left factors form a basis, and their right factors form a basis.

## 3. The transformed excess is a full diagonal

### Lemma 3 (rank-one physical diagonal locks the complement)

After changing the representative of the quotient line in (12),

```text
B'=Sym_0 direct-sum K D,
D=diag(d_0,d_1,d_2),           d_0d_1d_2!=0.        (14)
```

#### Proof

No nonzero matrix in `Sym_0` has rank one.  Indeed, for

```text
[[0,a,b],[a,0,c],[b,c,0]],
```

the principal `2 by 2` minors are `-a^2,-b^2,-c^2`.  Therefore each rank-one
`A_k` in (13) has a nonzero coefficient modulo `Sym_0`.  Write

```text
A_k=S_k+lambda_k G,       lambda_k!=0,
C_k=lambda_k^(-1)A_k=G+S'_k,       S'_k in Sym_0.  (15)
```

Absorbing `lambda_k^(-1)` into one rank-one factor preserves independence of
the three left and three right factor families.

All `C_k` have the same skew part

```text
K_0=G-G^T=C_k-C_k^T.                                (16)
```

If `K_0!=0` and `C_k=u_k v_k^T`, then `u_k,v_k` are independent and

```text
col K_0=span{u_k,v_k}.                              (17)
```

Thus every left factor `u_k` lies in one fixed two-plane, contradicting their
independence.  Hence `K_0=0` and `G` is symmetric.

Replace `G` by its diagonal part `D`; the difference `G-D` lies in `Sym_0`,
so this does not change `B'`.  Every `C_k` is now a symmetric rank-one matrix
with common diagonal `(d_0,d_1,d_2)`.  If `d_i=0`, symmetry makes the two
rank-one factors of every `C_k` proportional, and its `i`th diagonal entry
then forces the `i`th coordinate of every left factor to vanish.  That
contradicts independence of the three left factors.  Therefore every `d_i`
is nonzero, proving (14). `square`

Every matrix in the normal form (14) is symmetric, and its standard diagonal
lies on the one line `K(d_0,d_1,d_2)`.

## 4. External labels and triangle multiplicities lock

For any label vector `v`, use transformed factor coordinates

```text
a=X^(-1)X_t(v),              b=Y^(-1)Y_t(v).        (18)
```

### Lemma 4 (every external label is effectively zero)

If `t` is not one of the three triangle labels, then `a=b=0` for every
`v in V_t`.

#### Proof

Pair `v` with the selected vector at triangle label `i`.  Its transformed
matrix is

```text
N_i=a e_i^T+e_i b^T in B'.                          (19)
```

All matrices in (14) are symmetric, so (19) gives

```text
a-b in K e_i.                                       (20)
```

This holds for all three values of `i`, hence `a=b`.  The standard diagonal
of `N_i` is `2a_i e_i`.  It must lie on the full-support line `Kd` from
(14), so it is zero and `a_i=0`.  Doing this for all three `i` gives `a=b=0`.
`square`

### Lemma 5 (every triangle label is effectively one-dimensional)

For an arbitrary vector at triangle label `i`, its transformed factors have
the form

```text
a=b=c e_i.                                          (21)
```

#### Proof

Use only the two distinct-label pairs with the selected vectors at the other
triangle labels `j,k`.  Their transformed matrices have the form (19).
Symmetry gives

```text
a-b in K e_j intersect K e_k=0,
```

so `a=b`.  The standard diagonal gates at `j,k`, exactly as in Lemma 4, give
`a_j=a_k=0`.  Hence (21).  No pair of two vectors from label `i` is used.
`square`

## 5. Complete exclusion

### Theorem 6 (rank-four complete-pair family is impossible)

Conditions (2)--(3) cannot hold.

#### Proof

Lemmas 1--3 put the family into the normal form (14).  Lemma 4 deletes every
external label.  Lemma 5 makes each triangle label effectively one-dimensional
with paired factor `(e_i,e_i)`.  Every remaining distinct-label output is
therefore a scalar multiple of `S_(i,j)` and lies in `Sym_0`.  The complete
image has dimension at most three, contradicting
`dim B'=dim B=4`. `square`

### Corollary 6.1 (complete zero-anchor rank-four full-swallow exclusion)

Every zero-anchor full-swallow point has nuisance rank at least five.

#### Proof

`GLS39` gives the rank floor four.  `GLS43` and `GLS44` exclude every
rank-four point with `q!=0`.  On `q=0`, `GLS45` leaves exactly the
residual-free and sparse same-label complete-pair cores, and `GLS46` maps
both exactly into (2)--(3).  Theorem 6 excludes them. `square`

## 6. Frontier and unresolved remainder

```text
zero-anchor rank-3 full swallow:                      EMPTY (GLS39);
zero-anchor rank-4 q!=0 full swallow:                 EMPTY (GLS43/44);
zero-anchor rank-4 q=0 residual-free core:            EMPTY;
zero-anchor rank-4 q=0 sparse same-label core:        EMPTY;
zero-anchor rank-4 full swallow:                      EMPTY;
zero-anchor full-swallow rank floor:                  >=5;
ranks five through rank nine:                         OPEN;
silent source point is necessarily full swallow:     UNKNOWN;
raw escape / nonzero anchor:                          OPEN;
response / synchronization / nuisance / receiver:    OPEN;
arbitrary-r source cover / strategic-node closure:    OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.
```

The smallest continuation inside zero-anchor full swallow is nuisance rank
five, where the excess over `Delta` has dimension two and the one-line
normalization used here no longer applies.  A separate route may instead
attach raw escape or another source branch.  No such continuation is claimed
by `GLS47`.

## Verification boundary

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_complete_pair_family_exclusion.py
```

Run the genuinely independent no-import audit:

```text
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_complete_pair_family_exclusion.py
```

The primary uses exact symbolic matrices to replay synchronization,
left--right normalization, the rank-one/skew identities, full-support
diagonal gate, and external/block locking.  The audit imports no repository
module or third-party package; it exhausts the transformed quotient and
rank-one-basis conditions over `F_3`, then independently exhausts every
external and triangle-block vector in each admissible normal form.  The
arbitrary-dimensional characteristic-zero theorem is the written proof, not
the finite audit.
