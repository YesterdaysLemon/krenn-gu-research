# Maximum-root surplus-two leading-shadow target coupling and Fitting failure

## Status

**Exact characteristic-zero arbitrary-root target-coupled module theorem.**
For an original fixed-`Q` even target `|S|=2t`, GLS17 leaves `t-1` roots
open and produces a leading residual-absent class `b_(A,S)` while killing the
residual-present desired column.  Applying that same quotient to the complete
GHZ witness equation gives the denominator-free identity

```text
sum_c alpha_c [d_(A,S,c)] tensor w_(S,c)
  =b_(A,S) tensor M_S.                                (1)
```

The three output words `w_(S,c)` are independent, and every scalar suppressed
in `d_(A,S,c)` is nonzero because the maximum-root vectors and residual
contraction are fully supported.  Therefore the pure leading quotient has
rank at most one, and it has rank one exactly when both the leading desired
class and the physical residual-absent response `M_S=H_S` are nonzero.

This converts GLS17's shadow survival into an exact pointwise
response-gated rank-rise criterion.  Its failure on every nuisance-rank fibre
is equivalently a family of geometric radical--Fitting containments; no
generic rank, denominator, or chosen minor replaces the exceptional fibres.
If pure `M` is absent from a target's complete operator space, every leading
desired class and every one of the three corresponding pure GHZ classes is
absorbed in every partial-root shadow.

At root order four, absence of a pure-`M` four-port row forces each of the
four first-root nuisance shadows to equal the complete three-dimensional root
covector space.  For a pair target it forces the three-dimensional diagonal
pure subspace into the base order-two nuisance.  These are exact full-mixed-
target consequences, not support classifications or exclusions.

The theorem does **not** prove that a rank rise occurs, exclude the full-shadow
branch, force selected-response activity, establish GLS15 foreign transport,
or integrate the distinct GLS8 promoted module.  It does not close the
strategic node.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Dependencies and provenance

The complete fixed-`Q` witness quotient and response ranks come from

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md).

The partial-root leading map, its complete nuisance shadow, and pure-`M`
orientation come from

- [`GLS17`](MAXIMAL_ROOT_SURPLUS_TWO_PARTIAL_ROOT_GRADE_SHADOW_AND_COMMON_PURE_M_SELECTOR_THEOREM.md).

The all-rank geometric rank-rise formulation follows the exact Fitting
method of

- [`GLS5`](MAXIMAL_ROOT_SURPLUS_TWO_POINTWISE_SELECTOR_FAILURE_AND_DECOMPOSABLE_RETRACTION_BOUNDARY_THEOREM.md).

No external literature claim is used.  The new content is the target-coupled
leading identity, its response equivalence, the smaller exact Fitting system,
and the four-root full first-shadow consequence.

## 1. Leading spaces and pure columns

Work over a characteristic-zero field `K`.  Retain the GLS17 notation

```text
R={1,...,r},       B=Q disjoint-union U,
|R|=|U|=r,         |Q|=2,
empty!=S subset U, |S|=2t,       C=U-S,               (2)
```

with fully supported maximum-root vectors `x_i` and a fully supported fixed
residual contraction `z_Q`.  Choose

```text
A subset R,         |A|=t-1.                          (3)
```

Let

```text
E_(A,S)^*=(tensor_(a in A)V_a^*) tensor
          (tensor_(u in C)V_u^*),
N_(A,S)^lead subset E_(A,S)^*,
b_(A,S)=[Lambda_(A,S)] in
  overline E_(A,S)=E_(A,S)^*/N_(A,S)^lead            (4)
```

be GLS17's complete lower-or-equal-grade shadow and leading desired class.

For a target colour `c in {0,1,2}`, put

```text
kappa_(A,c)=product_(i in R-A)e_(i,c)^*(x_i) !=0,
d_(A,S,c)=kappa_(A,c)
  (tensor_(a in A)e_(a,c)^*) tensor
  (tensor_(u in C)e_(u,c)^*) in E_(A,S)^*,
w_(S,c)=tensor_(u in S)e_(u,c)^*.                    (5)
```

The nonzero residual target weights are

```text
alpha_c=product_(q in Q)e_(q,c)^*(z_q) !=0.          (6)
```

Write

```text
q_(A,S)=dim span{[d_(A,S,0)],[d_(A,S,1)],[d_(A,S,2)]}
```

in `overline E_(A,S)`.

## 2. Complete-target leading identity

### Theorem 1 (leading-shadow witness coupling)

On every complete hypothetical-witness point,

```text
sum_(c=0)^2 alpha_c[d_(A,S,c)] tensor w_(S,c)
  =b_(A,S) tensor M_S,                                (7)
```

where

```text
M_S=H_S.                                              (8)
```

Consequently

```text
q_(A,S)<=1                                            (9)
```

and the following are equivalent:

1. `q_(A,S)=1`;
2. at least one pure leading class `[d_(A,S,c)]` is nonzero;
3. `b_(A,S)!=0` and `M_S!=0`.

If these conditions hold, the complete operator space contains the legal
pure-`M` row `(1,0)`, whose physical output is the named nonzero tensor `M_S`.
Moreover, whenever `b_(A,S)!=0`, equation (7) forces `M_S` itself to lie in
the three-dimensional target-diagonal span of the `w_(S,c)`; every mixed
target-word coefficient of `M_S` is zero.

If `b_(A,S)=0` or `M_S=0`, then

```text
[d_(A,S,c)]=0                 for c=0,1,2.            (10)
```

#### Proof

Before applying the GLS17 shadow, the complete GLD15 witness quotient is

```text
sum_c alpha_c[d_(S,c)] tensor w_(S,c)
  =bar g_M tensor M_S+bar g_Z tensor Z_S.             (11)
```

Contract the roots in `R-A` with `x`.  The pure root/complement column becomes
exactly (5).  GLS17 sends `bar g_M` to `b_(A,S)` and `bar g_Z` to zero.  This
gives (7).

The right side of (7) is decomposable, so the left flattening has rank at most
one.  Because all `alpha_c` are nonzero and the `w_(S,c)` are linearly
independent, the left side is nonzero exactly when at least one displayed pure
class is nonzero.  The right side is nonzero exactly when both factors are
nonzero.  This proves (9), the equivalences, and (10).  The left side has no
mixed target-word coordinate, so comparison in any mixed target coordinate
gives `b_(A,S)` times that coordinate of `M_S` equal to zero; when `b_(A,S)`
is nonzero, the mixed coordinate vanishes.  GLS17 then supplies the pure-`M`
operator row.  `square`

The implication (10) uses the complete target equation.  It is not a
companion-grade identity on an arbitrary physical graph.

### Corollary 1.1 (absence of pure M forces simultaneous pure absorption)

Let `C_S subset K^2` be the complete operator-coefficient space.  If

```text
(1,0) notin C_S,                                      (12)
```

then for every `A in binom(R,t-1)` and every colour `c`,

```text
Lambda_(A,S) in N_(A,S)^lead,
d_(A,S,c) in N_(A,S)^lead.                            (13)
```

#### Proof

GLS17 says (12) forces `b_(A,S)=0` for every `A`.  Apply (10) to each shadow.
`square`

Thus rank zero, a pure-`Z` rank-one line, and every oblique rank-one line all
carry the same finite family of complete-target pure absorptions.  Rank two
and a pure-`M` rank-one line do not.

## 3. Exact pointwise and geometric Fitting criterion

Let the fully supported residual contraction vary on its Laurent torus

```text
T_Q=Spec Lambda,
Lambda=K[z_(q,c)^(+/-1):q in Q,c=0,1,2].             (14)
```

Work geometrically after extending to the algebraic closure.  In fixed bases,
let

```text
B_(A,S)(z)
```

be a matrix whose columns span `N_(A,S)^lead(z)`, and let

```text
D_(A,S)=[d_(A,S,0)|d_(A,S,1)|d_(A,S,2)].             (15)
```

The nonzero factors `alpha_c` are Laurent units and do not change the rank
locus.  Define the useful leading locus

```text
U_(A,S)={z in T_Q:
 rank[B_(A,S)(z)|D_(A,S)]>rank B_(A,S)(z)}.           (16)
```

### Theorem 2 (all-rank leading Fitting criterion)

On the complete witness locus, `U_(A,S)` is exactly the set of contractions
where

```text
b_(A,S)(z)!=0,             M_S(z)!=0.                 (17)
```

For every `1<=j<=dim E_(A,S)^*`, write `I_j` for the `j`-minor ideal and
`sqrt_geom` for the radical after algebraic closure.  Then `U_(A,S)` is empty
exactly when

```text
I_j([B_(A,S)|D_(A,S)])
  subset sqrt_geom(I_j(B_(A,S)))       for every j.   (18)
```

More generally, for any Laurent polynomial gate `rho`, the intersection

```text
D(rho) intersect U_(A,S)                               (19)
```

is empty exactly when

```text
rho I_j([B_(A,S)|D_(A,S)])
  subset sqrt_geom(I_j(B_(A,S)))       for every j.   (20)
```

The statements include every nuisance-rank drop and every exceptional escape
fibre.

#### Proof

The rank rise in (16) is equivalent to at least one nonzero pure leading
class.  Theorem 1 gives (17).

At a point where `rank B=j-1`, adjoining `D` raises rank exactly when all
`j`-minors of `B` vanish and some `j`-minor of `[B|D]` does not.  Taking the
union over `j` gives (16).  The Laurent Nullstellensatz converts emptiness of
each such locally closed set into (18).  Intersecting with `D(rho)` gives
(20).  No minor is inverted.  `square`

For a source gate requiring at least one member of a finite ideal
`P=(p_1,...,p_m)` to be nonzero, use (20) for every `rho=p_i` (or `h p_i`
when a nonzero residual scalar `h` is also required).  Replacing this union of
principal opens by the product of all `p_i` would be stronger and is not
licensed.

### Corollary 2.1 (finite-family failure profile)

Let `F` be a finite family of even targets.  There is no contraction on a
declared principal open `D(rho)` at which every target has at least one useful
leading shadow exactly when every choice function

```text
A_S in binom(R,|S|/2-1),          S in F              (21)
```

has empty simultaneous incidence locus

```text
D(rho) intersect intersection_(S in F) U_(A_S,S).    (22)
```

Each locus in (22) is encoded without division by adjoining one shared
residual point and the corresponding rank-rise minor conditions.  This is a
finite exact incidence formulation, not a claim that any locus is empty or
nonempty.

## 4. Four-root full-shadow consequences

Take `r=4`.

### Corollary 2.2 (four-port first-root fullness)

For the four-port target `S=U`, let `A={a}`.  Then

```text
E_(a,U)^*=V_a^*,
d_(a,U,c)=kappa_(a,c)e_(a,c)^*,       c=0,1,2.       (23)
```

The three tensors in (23) form a basis.  Therefore:

1. if `(1,0) notin C_U`, then

   ```text
   N_(a,U)^lead=V_a^*                 for every a in R;   (24)
   ```

2. on a witness with `M_U!=0`, the useful locus for root `a` is exactly

   ```text
   rank B_(a,U)<3.                                      (25)
   ```

In particular, one proper first-root nuisance shadow plus `M_U!=0` supplies a
legal nonzero pure-`M` four-port row.  The converse for existence of an
arbitrary full-module pure-`M` row is not claimed.

#### Proof

The three fully supported scalars `kappa_(a,c)` are nonzero, so (23) is a
basis.  Under absence of pure `M`, Corollary 1.1 puts that basis in the
nuisance, proving (24).  If `M_U!=0`, Theorem 1 says a pure column survives
exactly when `b_(a,U)!=0`; because the pure columns span the whole three-space,
this is exactly properness of the nuisance, proving (25).  `square`

### Corollary 2.3 (pair diagonal-subspace absorption)

For a pair target `S`, `A=empty` and `C=U-S` has two vertices.  The three
pure tensors

```text
d_(empty,S,c)=kappa_c e_(C,c)^*,       c=0,1,2        (26)
```

are independent in the nine-dimensional space `tensor_(u in C)V_u^*`.  If
pure `M` is absent from `C_S`, their three-dimensional diagonal span lies in
the complete other-order-two base nuisance.  This is weaker than fullness of
that nine-space and must not be promoted to it.

Combining the six pair statements with (24) gives the exact linear bad locus
left by GLS17's conditional common-line route.  It is not yet contradicted.

## 5. Exact frontier

```text
leading-shadow complete-target identity (7):                 PROVED;
pure leading quotient rank at most one:                      PROVED;
rank one iff leading class and M response are nonzero:       PROVED;
absence of pure M forces all desired and pure shadows:       PROVED;
all-rank geometric radical-Fitting criterion:                PROVED;
finite-family shared-point incidence formulation:            PROVED;
r=4 bad four-port shadows are full V_a^*:                    PROVED;
r=4 bad pair shadows contain the diagonal three-space:       PROVED;
some useful leading shadow forced on every witness:          UNKNOWN;
simultaneous full-shadow bad locus excluded:                 UNKNOWN;
selected-response three-colour activity:                     UNKNOWN;
GLS15 foreign transport on the remaining locus:              UNKNOWN;
GLS8 promoted source integration:                            OPEN;
complete maximum-root supply/attachment node:                OPEN;
global Krenn--Gu conjecture:                                 UNRESOLVED.      (27)
```

The smallest next obligation is now a concrete target-coupled module problem:
contradict the simultaneous containments (13), including every rank-drop
fibre encoded by (18)--(22), or force a useful leading shadow for a sufficient
target family.  At `r=4`, the four-port failure is literally the four full
three-dimensional nuisance shadows (24), not an unnamed generic divisor.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_leading_shadow_target_coupling_and_fitting_failure.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_leading_shadow_target_coupling_and_fitting_failure.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_leading_shadow_target_coupling_and_fitting_failure.py claims/arbitrary-order/audit_maximal_root_surplus_two_leading_shadow_target_coupling_and_fitting_failure.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_leading_shadow_target_coupling_and_fitting_failure.py claims/arbitrary-order/audit_maximal_root_surplus_two_leading_shadow_target_coupling_and_fitting_failure.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_leading_shadow_target_coupling_and_fitting_failure.py claims/arbitrary-order/audit_maximal_root_surplus_two_leading_shadow_target_coupling_and_fitting_failure.py
```

The focused primary verifier checks exact quotient tensor ranks, all response/
leading-class branches, radical rank-rise tables, and the four-root basis/full-
shadow implications over rational matrices.  The independent no-import audit
uses a separate sparse quotient reducer, exhaustive small finite-field rank
tables followed by exact rational controls, and a distinct vanishing-set
enumeration of the Fitting criterion.  These programs audit the finite linear
algebra; the arbitrary-point quotient identity and Laurent Nullstellensatz
argument above are the proofs.
