# Maximum-root surplus-two zero-anchor complete pairwise-diagonal rank bound and minimal raw-swallow exclusion

## Status and scope

**Exact characteristic-zero arbitrary-root pointwise fibre exclusion.**  The
zero-anchor full-swallow branch has no nuisance-rank-three point, with no
assumption on the root-companion coefficient `q`.  Equivalently, for every
fixed `GLS8`-eligible `(Q,A)` chart, every fixed residual contraction in the
owning `GLS36` scope, every eligible promoted root order `r>=3`, and every
shore-rank, incidence-rank, nuisance-rank, and divisor fibre,

```text
omega=0,
q,r_0,r_1,r_2 in B_Q^anc
  => rank B_Q^anc>=4.                                 (1)
```

The proof adjoins the two fixed residual labels to the physical promoted-port
incidence family.  A general characteristic-not-two lemma says that if every
distinct-label polarized pair map lands in the three-colour diagonal, then
their combined image has rank at most two.  Rank-three full swallow would
make that combined image contain the entire diagonal, which is impossible.

This closes the conditional `q=0` rank-three full-swallow fibre left open by
`GLS38` and subsumes the `GLS37`/`GLS38` rank-three exclusion conclusions.
Those predecessor theorems remain valid and retain their independent
sharpness/no-go evidence.  The implication `p!=0 => q!=0` was already covered
by `GLS38`; the new increment does not force a silent `p=0` source point into
full swallow.  The result
does not exclude nuisance ranks four through nine, prove that the silent
branch is fully swallowed, turn raw escape into an original legal target,
or supply any response, synchronization, activity, nuisance-survival, anchor,
or source-cover gate.

This is `GLS39`.  The maximum-root surplus-two supply-and-target-attachment
node and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Dependencies and provenance

The owning interfaces are:

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  for the grade-zero two-root/two-label companion;
- [`GLS35`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RAW_ROOT_DECK_QUOTIENT_AND_OUTPUT_COEFFICIENT_SEPARATION_NO_GO_THEOREM.md)
  for the complete raw anchor nuisance and full-swallow terminology;
- [`GLS36`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md)
  for the exact zero-anchor incidence map and equality
  `B_Q^anc=im sigma_Q`; and
- [`GLS37`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_MINIMAL_RAW_SWALLOW_INCIDENCE_CLASSIFICATION_AND_MIXED_ONLY_FAITHFULNESS_NO_GO_THEOREM.md)
  and [`GLS38`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_NONZERO_ROOT_DECK_MINIMAL_RAW_SWALLOW_EXCLUSION_THEOREM.md)
  for the previously excluded rank-three shore fibres and the corrected
  root-companion interface.

No external literature claim is used.  The new content is the arbitrary-
dimensional pairwise-diagonal family lemma and its auxiliary-residual-label
application to the complete `GLS36` incidence image.

## 1. Complete pairwise-diagonal families

Let `K` have characteristic different from two.  Let `T` be a finite label
set, let `V_t` be finite-dimensional for each `t in T`, and let

```text
X_t,Y_t:V_t -> K^3.                                  (2)
```

For distinct labels `s,t`, define

```text
mu_(s,t)(v tensor w)
 =X_s(v) tensor Y_t(w)+X_t(w) tensor Y_s(v).         (3)
```

Put

```text
r_c=e_c tensor e_c,
Delta=span{r_0,r_1,r_2}.                             (4)
```

### Theorem 1 (three-colour pairwise-diagonal rank bound)

Assume

```text
im mu_(s,t) subset Delta       for every s!=t.       (5)
```

Then

```text
dim sum_(s<t) im mu_(s,t) <=2.                       (6)
```

The conclusion includes zero maps, arbitrary label-space dimensions, and
every rank-drop fibre.  No coordinate coefficient or parameter is divided
out.

#### Proof

Write the coordinate linear forms of (2) as

```text
x_(t,i)=e_i^* X_t in V_t^*,
y_(t,j)=e_j^* Y_t in V_t^*.                         (7)
```

For colours `i!=j`, the `(i,j)` entry of (5) is the tensor identity

```text
x_(s,i) tensor y_(t,j)+y_(s,j) tensor x_(t,i)=0
in V_s^* tensor V_t^*                                (8)
```

for every `s!=t`.  Define the label supports

```text
A_i={t:x_(t,i)!=0},       B_j={t:y_(t,j)!=0}.        (9)
```

Suppose `A_i` and `B_j` are nonempty.  If some
`s in A_i setminus B_j`, choose `t in B_j`.  Then `s!=t`, and in (8) the first
simple tensor is nonzero while the second is zero, a contradiction.  Thus
`A_i subset B_j`; the transposed argument gives the reverse inclusion.  Hence

```text
A_i=B_j=:S_(i,j).                                    (10)
```

For distinct `s,t in S_(i,j)`, all four factors in (8) are nonzero.  Equality
of nonzero simple tensors gives nonzero scalars `rho_s,rho_t` such that

```text
x_(s,i)=rho_s y_(s,j),
x_(t,i)=rho_t y_(t,j),
rho_s+rho_t=0.                                       (11)
```

Three distinct supported labels would give

```text
rho_s+rho_t=rho_s+rho_u=rho_t+rho_u=0,
```

and therefore `2 rho_s=0`, contrary to the field assumption and
`rho_s!=0`.  Consequently

```text
|S_(i,j)|<=2                                         (12)
```

whenever the two supports are nonempty.

Call colour `c` active when the `r_c` coordinate of some pair map (3) is not
the zero bilinear form.  If at most two colours are active, (6) is immediate.
Assume for contradiction that all three are active.  Then every `A_i` and
every `B_i` is nonempty.  The equalities (10) for all `i!=j` connect the six
sets in (9), so they are one common set `S`; by (12), `|S|<=2`.  Every label
outside `S` has both maps in (2) equal to zero.

If `|S|<=1`, every distinct-label pair map is zero.  Otherwise
`S={s,t}`, and only `mu_(s,t)` can be nonzero.  Choose linear coordinates
`z,w` on `V_s,V_t`.  Its matrix over the polynomial ring `K[z,w]` is

```text
M(z,w)=X_s(z)Y_t(w)^T+X_t(w)Y_s(z)^T.               (13)
```

It is a sum of two rank-one matrices, so `det M=0`.  By (5) it is diagonal;
if its diagonal bilinear forms are `f_0,f_1,f_2`, then

```text
f_0 f_1 f_2=0 in K[z,w].                             (14)
```

The polynomial ring is an integral domain, so some `f_c` is identically
zero.  That colour is not active, contradicting the assumption that all
three are active.  Thus at most two diagonal coordinate lines occur in the
combined image, proving (6). `square`

The characteristic restriction is explicit.  The sign argument (11)--(12)
is not promoted to characteristic two; bounded searches there are not a
replacement for a proof.

## 2. Auxiliary residual labels recover the complete incidence family

Retain the zero-anchor notation

```text
a_s=xi_0^s in V_(a_0)^*,
b_s=xi_1^s in V_(a_1)^*,

X_u:V_u -> V_(a_0)^*,
Y_u:V_u -> V_(a_1)^*.                               (15)
```

Adjoin the two residual labels to the promoted ports:

```text
T=Q disjoint-union Uhat.                             (16)
```

Give each `q_s` an auxiliary one-dimensional domain `K`, and define

```text
X_(q_s)(lambda)=lambda a_s,
Y_(q_s)(lambda)=lambda b_s.                          (17)
```

The maps (3) are then exactly

```text
mu_(q_0,q_1)(1 tensor 1)
 =a_0 tensor b_1+a_1 tensor b_0=q,

mu_(q_s,u)(1 tensor x)
 =a_s tensor Y_u(x)+X_u(x) tensor b_s
 =sigma_(s,u)(x),

mu_(u,v)(x tensor y)
 =X_u(x) tensor Y_v(y)+X_v(y) tensor Y_u(x)
 =sigma_(u,v)(x tensor y).                           (18)
```

Consequently,

```text
sum_(s<t in T) im mu_(s,t)=im sigma_Q+Kq.            (19)
```

Thus the auxiliary construction adds only the already typed residual-pair
companion `q`; it does not invent a physical port, response, or deck.

## 3. Unconditional exclusion of minimal full-swallow rank

### Theorem 2 (every rank-three full-swallow fibre is empty)

Assume pointwise that

```text
omega=0,
q,r_0,r_1,r_2 in B_Q^anc,
rank B_Q^anc=3.                                      (20)
```

Then (20) is impossible.

#### Proof

The three `r_c` are independent, so (20) gives

```text
B_Q^anc=Delta.                                       (21)
```

The corrected `GLS36` incidence theorem gives

```text
B_Q^anc=im sigma_Q.                                  (22)
```

Every one-residual and promoted-pair map in (18) therefore lands in `Delta`.
The remaining residual-residual map has image `Kq`, also contained in
`Delta` by full swallow.  Moreover, `q in im sigma_Q`, so (19) and (22) give

```text
sum_(s<t in T) im mu_(s,t)=B_Q^anc=Delta.            (23)
```

Theorem 1 applies to the complete auxiliary label family, but this combined
image has dimension three, contradicting (6). `square`

### Corollary 2.1 (universal full-swallow rank floor)

At every zero-anchor full-swallow point in characteristic zero,

```text
rank B_Q^anc>=4.                                     (24)
```

This includes `q=0`, `p=0`, diagonal-silent, non-silent, zero-shore,
incidence-rank-drop, and every divisor fibre inside the declared full-swallow
premise.  It does not say that the full-swallow premise is forced on every
silent point.

## 4. Frontier and unresolved remainder

```text
rank-3 full swallow for every q:                           EXCLUDED;
full swallow with rank B_Q^anc in {4,...,9}:               OPEN;
silent zero-anchor point is necessarily full swallow:      UNKNOWN;
raw escape supplies an original legal target package:      NOT SUPPLIED;
nonzero-anchor marginal/double-transverse branches:         OPEN;
response/activity/synchronization/nuisance/anchor gates:     OPEN;
arbitrary-root source cover and strategic-node closure:      UNKNOWN;
global Krenn--Gu conjecture:                                UNRESOLVED.
```

The smallest continuation inside the full-swallow branch is now to exclude
or legally attach nuisance ranks four through nine using the complete
labelwise physical deck equations on the same graph.  The `GLS36` common-row
no-go remains binding: rank/Fitting membership alone supplies no separating
row.  Separately, `GLS35` raw escape isolates only the residual-absent deck,
not an original `GLS22/GLS23` target, and the `p=0` silent branch still needs
its own source-side case cover.

## Verification boundary

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
```

Run the genuinely independent no-import audit:

```text
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
```

The primary uses SymPy to replay the support-connectivity, three-label sign,
and two-label determinant leaves, then exhausts the `364` projective scalar
families over `F_3` (`700` compatible pairs) as a bounded falsification
census.  The audit imports no project module and no third-party package; it
uses an independent two-block/bipartition/triangle derivation, followed by an
exact rational auxiliary-interface replay.  The arbitrary-dimensional and
arbitrary-root result is the symbolic proof above.  Finite scalar searches
are supporting checks only and are not the proof or an exhaustive physical
source cover.
