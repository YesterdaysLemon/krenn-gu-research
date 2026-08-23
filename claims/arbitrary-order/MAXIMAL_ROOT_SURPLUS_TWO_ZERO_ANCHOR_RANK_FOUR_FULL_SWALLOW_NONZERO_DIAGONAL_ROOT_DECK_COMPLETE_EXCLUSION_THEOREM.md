# Maximum-root surplus-two zero-anchor rank-four full-swallow nonzero diagonal root-deck complete exclusion

## Status and scope

**Exact characteristic-zero arbitrary-root pointwise fibre exclusion.**  On
the zero-anchor full-swallow branch, nuisance rank four forces the root
companion to vanish:

```text
omega=0,
q,r_0,r_1,r_2 in B_Q^anc,
rank B_Q^anc=4
  => q=0.                                             (1)
```

The new content proves that a nonzero diagonal `q` is impossible.  The
already proved `GLS43` excludes `q notin Delta`, so (1) follows by exhaustion.
In particular, since

```text
p=epsilon_A(q),
```

every rank-four full-swallow point lies on `p=0`.  Thus the full-swallow
branch on the `GLS22/GLS40/GLS41` localization `D(p)` starts at nuisance rank
five.

The proof uses only the complete whole-domain incidence map of `GLS36`.  It
covers arbitrary port-domain dimensions and every residual-shore,
incidence-rank, deck, and divisor fibre.  It chooses no response or incidence
minor, and it neither normalizes nor divides by a chosen nonzero shore
coordinate or denominator.

The result does not exclude the surviving `q=0` rank-four fibre, ranks five
through nine, raw escape, or any nonzero-anchor branch.  It does not supply a
legal selector, physical response, synchronization, selected activity,
nuisance survival, attachment anchor, named receiver, or source cover.  The
maximum-root surplus-two strategic node and global Krenn--Gu conjecture
remain **UNRESOLVED**.

This is `GLS44`.

## Dependencies and provenance

The owning interfaces are:

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  for the promoted chart and its legal-attachment boundary;
- [`GLS35`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RAW_ROOT_DECK_QUOTIENT_AND_OUTPUT_COEFFICIENT_SEPARATION_NO_GO_THEOREM.md)
  for the raw root companion `q`, the scalar `p=epsilon_A(q)`, and the
  escape/full-swallow split;
- [`GLS36`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md)
  for `B_Q^anc=im sigma_Q` and every whole-domain labelled component;
- [`GLS39`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_COMPLETE_PAIRWISE_DIAGONAL_FAMILY_RANK_BOUND_AND_MINIMAL_RAW_SWALLOW_EXCLUSION_THEOREM.md)
  for the unconditional rank floor four on full swallow;
- [`GLS40`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_SWALLOW_AGGREGATE_DECK_EXCESS_SYZYGY_AND_TRANSVERSE_CYLINDER_THEOREM.md)
  for the rank-four `q in Delta` stratum and its one-dimensional excess
  module; and
- [`GLS43`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_FULL_SWALLOW_OFF_DIAGONAL_ROOT_DECK_COMPLETE_EXCLUSION_THEOREM.md)
  for exclusion of the complementary `q notin Delta` rank-four stratum.

`GLS41` and `GLS42` are not used in the exclusion.  Their pure-core and
full-residual excess identities remain relevant at ranks at least five; the
present rank-four `D(p)` branch dies before those response/deck gates.

No external literature claim is used.  The new content is the
rank-two-diagonal cross-block obstruction and the rank-one-diagonal quotient
column obstruction, followed by their integration with `GLS43`.

## 1. Complete incidence setting

Let `K` have characteristic zero and retain

```text
E=K^3 tensor K^3,
r_i=e_i tensor e_i,
Delta=span{r_0,r_1,r_2}.                             (2)
```

At one fixed residual contraction, write

```text
a_s=xi_0^s in K^3,              b_s=xi_1^s in K^3,
X_u:V_u -> K^3,                 Y_u:V_u -> K^3,

q=a_0 tensor b_1+a_1 tensor b_0.                    (3)
```

Put

```text
A=span{a_0,a_1},       C=span{b_0,b_1},
X=sum_u im X_u,        Y=sum_u im Y_u.               (4)
```

The complete `GLS36` components are

```text
sigma_(s,u)(v)
 =a_s tensor Y_u(v)+X_u(v) tensor b_s,              (5)

sigma_(u,v)(x tensor y)
 =X_u(x) tensor Y_v(y)+X_v(y) tensor Y_u(x)         (6)
```

for every residual label, every promoted label, every pair of distinct
promoted labels, and every vector in the indicated domains.  On `omega=0`,

```text
B=B_Q^anc=im sigma_Q.                                (7)
```

Assume full swallow and `rank B=4`.  If `q in Delta`, then

```text
B=Delta+K w                                          (8)
```

for some `w notin Delta`.  Every component (5)--(6) lies in this same
four-space.

Every tensor in (5)--(6) has all left factors in `A+X` and all right factors
in `C+Y`.  Since `Delta subset B`, contraction against the opposite factor
shows

```text
A+X=K^3,                 C+Y=K^3.                    (9)
```

No individual port value is assumed nonzero in (9); it is a statement about
the complete labelled image spans.

## 2. A diagonal rank-two root deck is impossible

### Lemma 1 (rank-two cross-block obstruction)

Under (2)--(9), `q` cannot have rank two.

#### Proof

Because

```text
q=[a_0|a_1] [[0,1],[1,0]] [b_0|b_1]^T,             (10)
```

rank two of `q` implies

```text
dim A=dim C=2,
A=col q,                 C=row q.                   (11)
```

A rank-two diagonal matrix has one missing colour `c`; its row and column
spaces are the same coordinate plane

```text
P=span{e_i:i!=c}.                                   (12)
```

Thus `A=C=P`.

Fix any promoted label `u`, any `v in V_u`, and abbreviate

```text
x=X_u(v),                  y=Y_u(v).
```

Take the span of the two residual--port matrices

```text
m_s=a_s y^T+x b_s^T in B,             s=0,1.        (13)
```

Project matrices to the direct sum of the two cross blocks

```text
(P tensor K e_c) direct-sum (K e_c tensor P).       (14)
```

For a residual coefficient vector `t in K^2`, the projection of the
corresponding linear combination of (13) is

```text
t -> (y_c a(t), x_c b(t)),                           (15)
```

where `t->a(t)` and `t->b(t)` are both isomorphisms from `K^2` to `P` by
(11).  If either `x_c` or `y_c` is nonzero, map (15) has rank two.

But the diagonal three-plane dies under projection to (14), while (8) has
only one non-diagonal generator.  The image of all of `B` in (14) therefore
has dimension at most one.  This contradicts rank two in (15).  Hence

```text
x_c=y_c=0                                           (16)
```

for every vector in every promoted domain.

Equations (12) and (16) put every left and right factor in (5)--(6) inside
`P`.  Thus

```text
B subset P tensor P,
```

which cannot contain `r_c`.  This contradicts full swallow. `square`

The argument uses the two-dimensional residual span as a whole.  It does not
select or divide by a nonzero residual coordinate and includes every port
rank-drop fibre.

## 3. A diagonal rank-one root deck is impossible

### Lemma 2 (rank-one quotient-column obstruction)

Under (2)--(9), `q` cannot have rank one and be nonzero.

#### Proof

A nonzero rank-one diagonal tensor is

```text
q=kappa e_c tensor e_c,                 kappa!=0.    (17)
```

The factorization (10) shows that at least one residual shore has rank one.
Transpose all tensors if necessary and assume

```text
dim A=1.
```

Since `col q subset A`, equation (17) gives

```text
A=K e_c.
```

Write

```text
a_s=lambda_s e_c.                                   (18)
```

Let

```text
pi:K^3 -> W=K^3/K e_c.                              (19)
```

By (9), the collection of all `pi(X_u(v))` spans the two-dimensional space
`W`.  Project (5) on the left by `pi`.  The first summand vanishes, leaving
the display below; `q` also projects to zero because `q in Delta`.  Thus for
every fixed `s` and every port value `x=X_u(v)`,

```text
pi(x) tensor b_s in Bbar:=(pi tensor id)(B).         (20)
```

Linearity and the spanning statement imply

```text
W tensor K b_s subset Bbar                           (21)
```

for every `s`, including zero `b_s`.

The projected diagonal is

```text
Dbar=(pi tensor id)(Delta)
 =span{pi(e_i) tensor e_i:i!=c}.                     (22)
```

By (8),

```text
Bbar=Dbar+K wbar.                                    (23)
```

Now project the second factor of (21)--(23) onto the coordinate line
`K e_c`.  The space `Dbar` has zero image.  The extra line `K wbar` has image
of dimension at most one.  If the `c`-coordinate of `b_s` were nonzero,
however, `W tensor K b_s` would project isomorphically onto the
two-dimensional `W`.  Therefore

```text
(b_s)_c=0                  for s=0,1.                (24)
```

Finally, (3) and (18) give

```text
q=e_c tensor (lambda_0 b_1+lambda_1 b_0).           (25)
```

Equation (24) makes the `(c,c)` coordinate of (25) zero, contradicting
(17). `square`

No `b_s` is assumed nonzero and no coordinate of `b_s` is divided out.  The
dimension contradiction applies uniformly to each residual vector and
includes zero and cancelling residual slices.

## 4. Complete rank-four consequence

### Theorem 3 (nonzero diagonal rank-four full swallow is empty)

Assume pointwise that

```text
omega=0,
q,r_0,r_1,r_2 in B_Q^anc,
rank B_Q^anc=4,
0!=q in Delta.                                      (26)
```

Then (26) is impossible.

#### Proof

The matrix `q` has rank at most two by (3).  A nonzero diagonal matrix
therefore has rank one or two.  Lemmas 1 and 2 exclude the two cases.
`square`

### Corollary 3.1 (every rank-four full-swallow point is silent)

Under the first three hypotheses of (26),

```text
q=0,                    p=epsilon_A(q)=0.            (27)
```

Consequently every full-swallow point on `D(p)` satisfies

```text
rank B_Q^anc>=5.                                     (28)
```

#### Proof

`GLS43` excludes `q notin Delta`; Theorem 3 excludes
`0!=q in Delta`.  Hence `q=0`, and the definition of `p` gives (27).
The rank floor four is `GLS39`; eliminating rank four on `D(p)` gives (28).
`square`

## 5. Frontier and unresolved remainder

```text
rank-four q-outside-Delta full swallow:               EMPTY (GLS43);
rank-four nonzero q-in-Delta full swallow:            EMPTY;
rank-four full swallow on D(p):                       EMPTY;
rank-four q=0, hence p=0, full swallow:               OPEN;
rank-five through rank-nine full swallow:             OPEN;
raw escape and nonzero-anchor branches:               OPEN;
pure-core survival / response / synchronization:      OPEN;
activity / nuisance survival / anchors / receiver:    OPEN;
arbitrary-r source cover and strategic-node closure:  OPEN;
global Krenn--Gu conjecture:                           UNRESOLVED.
```

The smallest surviving full-swallow rank-four obligation is exactly `q=0`.
It lies outside the `D(p)` transverse projector used by `GLS22`, `GLS40`
Theorem 3, and `GLS41`.  Its proof cannot silently import those localized
interfaces.  It requires either a direct complete-labelled incidence/deck
contradiction on `p=0`, or a separate legal target attachment.  Ranks at
least five and raw escape remain independent obligations.

## Verification boundary

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_nonzero_diagonal_root_deck_complete_exclusion.py
```

Run the genuinely independent no-import audit:

```text
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_nonzero_diagonal_root_deck_complete_exclusion.py
```

The primary uses exact SymPy matrices to replay both projection obstructions,
the residual factorization ranks, and representative exceptional fibres.  The
audit imports no project module or third-party package; it uses independent
`Fraction` elimination, finite-field structural exhaustion, and a separate
quotient/cross-block representation.  The arbitrary-domain theorem is the
written proof above, not a finite search.
