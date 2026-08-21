# Maximum-root surplus-two promoted zero-anchor diagonal reconstruction and residual-shore cover

## Status

**Exact characteristic-zero arbitrary-root physical-module theorem.**  Work
on the zero top-anchor branch left by `GLS23` for one `GLS4` source pair and
probe pair.  The complete GHZ equation forces the projected three-colour
diagonal root space, of dimension two or three, into the remaining physical
top-target nuisance.  The nuisance splits exactly into labels meeting the
residual pair once and labels contained in the promoted port set.

The one-residual labels lie in a canonical residual-shore tangent space of
dimension at most seven after transverse projection.  Consequently every
zero-anchor point satisfies the following denominator-free alternative:

1. some promoted pair label has a nonzero transverse slice outside that
   tangent space; or
2. the two residual incidence shore spans cover all three coordinate lines,
   one shore or the other for each colour.

The first branch supplies a raw nonzero promoted pair coefficient and an
exact top-equation-essential physical slice.  It does **not** prove that this
coefficient survives its own complete nuisance, has nonzero response, or
enters a named downstream detector.  The coordinate-shore-cover branch is
not excluded.  Thus this theorem sharpens but does not close the zero-anchor
branch, the maximum-root supply-and-attachment node, or the global Krenn--Gu
conjecture.  The global conjecture remains **UNRESOLVED**.

## Dependencies and scope

Retain the promoted partition and notation of

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md),
- [`GLS22`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md), and
- [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md).

Thus

```text
A={a_0,a_1},                 Q={q_0,q_1},
Uhat=K_0 disjoint-union U,   Bhat=Q disjoint-union Uhat,
E_A^*=V_(a_0)^* tensor V_(a_1)^*,
epsilon_A(v)=v(x_(a_0),x_(a_1)),
q=G_Q^A(z_Q),                p=epsilon_A(q)!=0,
P_Q(v)=pv-epsilon_A(v)q.                              (1)
```

All local spaces are ternary and both root vectors are fully supported.
The theorem is pointwise on `D(p)` and divides by no response, incidence
minor, shore coordinate, or selector coefficient.

## 1. Residual shores and their tangent space

For `s in {0,1}` and `i in {0,1}`, put

```text
xi_i^s=W_(a_i,q_s)(-,z_(q_s)) in V_(a_i)^*,
X_i=span{xi_i^0,xi_i^1},        d_i=dim X_i.           (2)
```

The evaluated all-port root tensor is

```text
q=xi_0^0 tensor xi_1^1+xi_0^1 tensor xi_1^0.          (3)
```

Since `p!=0`, neither shore span is zero, so `d_i in {1,2}`.  Define

```text
T_Q=X_0 tensor V_(a_1)^*+V_(a_0)^* tensor X_1
      subset E_A^*.                                   (4)
```

### Lemma 1 (residual-shore tangent dimension)

One has

```text
q in T_Q,
dim T_Q=3d_0+3d_1-d_0d_1,
dim P_Q(T_Q)=3d_0+3d_1-d_0d_1-1 <=7.                 (5)
```

#### Proof

Equation (3) puts `q` in (4).  The intersection of the two summands in
(4) is `X_0 tensor X_1`, giving the middle formula.  On `D(p)`, `GLS22`
proves `ker P_Q=Kq`.  The line `Kq` lies in `T_Q`, so restriction of `P_Q`
to `T_Q` lowers dimension by exactly one.  Finally `d_0,d_1<=2`, with the
maximum seven attained at `(2,2)`.  `square`

For a label `D={q_s,u}`, `u in Uhat`, the evaluated two-root companion is

```text
g_D=xi_0^s tensor W_(a_1,u)
    +W_(a_0,u) tensor xi_1^s.                         (6)
```

Here the port slot `u` is retained.  Therefore every contraction of that
slot lies in

```text
xi_0^s tensor V_(a_1)^*+V_(a_0)^* tensor xi_1^s
 subset T_Q.                                         (7)
```

Let

```text
N_empty^(1)=
 sum_(s=0)^1 sum_(u in Uhat)
   Slice_{u}((P_Q tensor id)g_{q_s,u})
 subset P_Q(T_Q).                                    (8)
```

This is the exact top-target nuisance contributed by the labels meeting `Q`
in one vertex.

## 2. Projected diagonal rank

Let

```text
D_A=span{r_0,r_1,r_2},
r_c=e_(a_0,c)^* tensor e_(a_1,c)^*,
Delta_Q=P_Q(D_A) subset ker epsilon_A.                (9)
```

### Lemma 2 (two-or-three projected diagonal rows)

Exactly

```text
dim Delta_Q = 2  if q in D_A,
dim Delta_Q = 3  if q notin D_A.                     (10)
```

#### Proof

The diagonal space has dimension three.  Since `ker P_Q=Kq`, its
intersection with `D_A` is `Kq` when `q` is diagonal and is zero otherwise.
Rank--nullity gives (10).  `square`

The result includes every rank-one or rank-two realization of (3); no matrix
rank or diagonal coordinate of `q` is inverted.

## 3. Complete top-target reconstruction

Assume now that the full graph tensor is the ternary GHZ target and take the
zero-anchor branch

```text
omega=W_(a_0,a_1)=0.                                 (11)
```

For `D subset Uhat`, `|D|=2`, the transverse companion `a_D` of `GLS23` is
the desired coefficient `t_D=P_Q(g_D)` for the promoted target indexed by
`C=D`.  Put

```text
N_empty^(2)=
 sum_(D in binom(Uhat,2)) Slice_D(t_D).               (12)
```

### Theorem 3 (zero-anchor diagonal reconstruction)

The complete top-target nuisance splits exactly as

```text
N_empty^tr=N_empty^(1)+N_empty^(2),                   (13)
```

and the complete GHZ equation forces

```text
Delta_Q subset N_empty^tr.                            (14)
```

#### Proof

For the top target, `GLS23` gives

```text
N_empty^tr=sum_(D in binom(Bhat,2)) Slice_(D intersect Uhat)(a_D).
                                                               (15)
```

The label `D=Q` contributes zero.  Every remaining pair either meets `Q`
once, giving exactly (8), or is contained in `Uhat`, giving exactly (12).
This proves (13).

For the top target, `GLS22` gives in the transverse quotient

```text
sum_(c=0)^2 alpha_c [P_Q(r_c)] tensor w_(Uhat,c)
 = [P_Q(omega)] tensor P_Uhat(H;z_Q).                 (16)
```

Every `alpha_c` is a residual-torus unit and the three pure port words are
independent.  Under (11), the right side is zero.  Hence each `P_Q(r_c)` lies
in `N_empty^tr`, proving (14).  This uses the complete target equation, not
only pure normalization as an external assumption: (16) is its full
top-target quotient and the coefficient comparison is legal because the
three right-factor words are independent.  `square`

## 4. Essential-pair versus coordinate-shore-cover alternative

Define the residual-tangent defect

```text
e_Q=dim ((Delta_Q+P_Q(T_Q))/P_Q(T_Q)).                (17)
```

Because `q in T_Q` and `ker P_Q=Kq`, the quotient induced by `P_Q` gives

```text
e_Q=dim ((D_A+T_Q)/T_Q).                              (18)
```

### Theorem 4 (exhaustive zero-anchor alternative)

Every point satisfying (1)--(11) lies in exactly one of the following
branches.

#### P. Essential promoted pair

`e_Q>0`.  The images of the physical pair-label slices (12) span the
`e_Q`-dimensional image of `Delta_Q` modulo `P_Q(T_Q)`.  In particular, some
`D in binom(Uhat,2)` satisfies

```text
Slice_D(t_D) notsubset P_Q(T_Q),                     (19)
```

so `t_D!=0` and this label is essential in the projected top pure-diagonal
reconstruction after all one-residual tangent directions are removed.

#### S. Coordinate shore cover

`e_Q=0`.  Equivalently,

```text
D_A subset T_Q,                                      (20)
```

or, colour by colour,

```text
for every c in {0,1,2},
 e_(a_0,c)^* in X_0  or  e_(a_1,c)^* in X_1.         (21)
```

Thus the exceptional branch is an exact two-shore cover of the three
coordinate lines.  It includes all rank profiles `(d_0,d_1)` that can meet
(21), all overlaps between the shore assignments, and every incidence-minor
drop.

#### Proof

Equation (14), (13), and (8) imply, after quotienting by `P_Q(T_Q)`, that the
images of the summands in (12) span the image of `Delta_Q`.  If its dimension
is positive, at least one summand has nonzero image, proving branch P.  If it
is zero, (18) gives (20).

The annihilator of `T_Q` in `V_(a_0) tensor V_(a_1)` is

```text
X_0^perp tensor X_1^perp.                             (22)
```

The diagonal tensor `r_c` pairs with `v_0 tensor v_1` as
`v_0(c)v_1(c)`.  Therefore all three `r_c` lie in `T_Q` exactly when, for
each `c`, one of the coordinate evaluations vanishes identically on
`X_0^perp` or on `X_1^perp`.  In finite dimension this is exactly
`e_(a_0,c)^* in X_0` or `e_(a_1,c)^* in X_1`, proving (21).  The two branches
are complementary by definition of `e_Q`.  `square`

### Corollary 4.1 (generic rank-two shores)

If `d_0=d_1=2`, choose nonzero normals

```text
n_i in X_i^perp.                                     (23)
```

Then `e_Q=0` exactly when

```text
n_0(c)n_1(c)=0 for c=0,1,2.                          (24)
```

Thus any common nonzero coordinate of the two normal vectors forces branch
P.  Formula (24) is homogeneous in both normals and introduces no chart or
normalization.

### Corollary 4.2 (low-rank shore boundary)

Branch S forces

```text
d_0+d_1>=3.                                          (25)
```

Hence the `(1,1)` shore-rank fibre always lies in branch P.  On a `(1,2)`
shore cover, the rank-one shore is one coordinate line and the rank-two shore
is the coordinate plane spanned by the other two; the transpose statement
holds for `(2,1)`.

#### Proof

A `d_i`-dimensional shore contains at most `d_i` of the three independent
coordinate lines.  Cover (21) therefore implies (25).  If equality is split
as `(1,2)`, all three available line slots are used with no overlap, giving
the stated coordinate line and complementary coordinate plane.  `square`

## 5. Exact scope and remaining obligation

```text
one-residual nuisance lies in P_Q(T_Q), dim <=7:        PROVED;
projected diagonal rank is two or three:                 PROVED;
zero anchor forces full diagonal reconstruction:         PROVED;
essential-pair / coordinate-shore-cover split:            PROVED;
all incidence-rank and coordinate exceptional fibres:     INCLUDED;

essential raw t_D survives its own complete nuisance:     NOT PROVED;
physical response of the essential pair is nonzero:       NOT PROVED;
coordinate-shore-cover branch is empty on witnesses:      NOT PROVED;
common selector line and selected-response activity:       NOT PROVED;
r>=4 named downstream detector for promoted targets:       OPEN;
complete maximum-root supply/attachment node:              OPEN;
global Krenn--Gu conjecture:                               UNRESOLVED.       (26)
```

The next zero-anchor obligation is now sharply typed.  On branch P, use the
complete mixed equations to promote (19) from tangent-essential raw supply to
survival in the target's own complete nuisance and nonzero response, or
derive a mixed contradiction.  On branch S, use the coordinate shore cover
(21), together with maximum-root blocking and the same physical graph, to
exclude or attach every exceptional fibre.  Neither task is a support atlas,
and neither may replace the complete nuisance by `P_Q(T_Q)`.

The subsequent
[`GLS27` residual-family theorem](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RESIDUAL_FAMILY_GENERIC_ESCAPE_AND_COORDINATE_SHORE_NORMAL_FORM_THEOREM.md)
shows that branch P occurs on a nonempty principal open unless the shore cover
holds over the residual function field.  In the latter case only the exact
`C12`, `C21`, and `C22` generic normal forms remain.  It does not promote the
essential slice to target survival or exclude those forms.

## Verification boundary

From repository root run

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_zero_anchor_diagonal_reconstruction_and_residual_shore_cover.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_zero_anchor_diagonal_reconstruction_and_residual_shore_cover.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_zero_anchor_diagonal_reconstruction_and_residual_shore_cover.py claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_zero_anchor_diagonal_reconstruction_and_residual_shore_cover.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_zero_anchor_diagonal_reconstruction_and_residual_shore_cover.py claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_zero_anchor_diagonal_reconstruction_and_residual_shore_cover.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_zero_anchor_diagonal_reconstruction_and_residual_shore_cover.py claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_zero_anchor_diagonal_reconstruction_and_residual_shore_cover.py
```

The primary verifier checks the exact tangent/image dimensions, singleton
matching formula, diagonal rank, quotient defect, and both branches over
rational fixtures.  The independent no-import audit uses standard-library
`Fraction`, a separate row-reduction implementation, dual annihilators, and
different fixtures.  The scripts audit finite-dimensional mechanisms; the
arbitrary-root statement is the written matching and linear-algebra proof.

See the
[`2026-08-20 hostile review`](../../docs/audits/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ZERO_ANCHOR_DIAGONAL_RECONSTRUCTION_AND_RESIDUAL_SHORE_COVER_REVIEW_2026-08-20.md).
