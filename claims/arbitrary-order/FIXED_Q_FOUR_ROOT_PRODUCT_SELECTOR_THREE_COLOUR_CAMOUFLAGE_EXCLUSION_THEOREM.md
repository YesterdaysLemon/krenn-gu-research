# Fixed-Q four-root product-selector three-colour camouflage exclusion

## Status

**Exact characteristic-zero fixed-module exclusion and source-interface
refinement.**  A surviving `GLS17` four-port first-root class supplies more
than an abstract pure-`M` coefficient row: it supplies a legal selector that
is a product evaluation on the four root slots.  Restricting that selector to
the complete foreign labelled summands puts all six direct port blocks into
one common four-dimensional cross-Gram representation.

If the six direct blocks are target-diagonal and their four-port compound is
target-pure with all three pure coefficients nonzero, the mixed `2+2`
equations force the sharp three-matching camouflage support.  That support
would require five independent vectors in the common four-dimensional root
incidence space.  It is therefore impossible.

Consequently no complete hypothetical witness can simultaneously have all
six `GLS16` pair base shadows survive, one `GLS17` four-port first-root shadow
survive, and a three-colour-full residual-absent four-port response.  The
result removes the sharp `GLD3` matching camouflage from this product-selector
source branch without assuming projective slope synchronization,
three-colour pair-depth activity, a residual scalar, response-map visibility,
or a rank minor.

It does **not** force any leading class or response to survive.  Zero-, one-,
and two-colour four-port responses remain, as do swallowed pair or four-port
shadows, arbitrary legal selectors not factoring through a `GLS17` first-root
shadow, pure-`Z` and oblique rows, other root orders, the promoted `GLS8`
interface, and every permanent consequence.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

Dependencies:

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md),
- [`GLS16`](MAXIMAL_ROOT_SURPLUS_TWO_BASE_GRADE_PAIR_SHADOW_AND_CROSS_TARGET_SELECTOR_ANNIHILATION_THEOREM.md),
- [`GLS17`](MAXIMAL_ROOT_SURPLUS_TWO_PARTIAL_ROOT_GRADE_SHADOW_AND_COMMON_PURE_M_SELECTOR_THEOREM.md),
- [`GLS18`](MAXIMAL_ROOT_SURPLUS_TWO_LEADING_SHADOW_TARGET_COUPLING_AND_FITTING_FAILURE_THEOREM.md).

No external literature claim is used.  The new content is the product-form
selector lift, the exact common root-incidence cross-Gram identity, the
complete pure-three diagonal support reduction, and the four-dimensional
camouflage obstruction.

## 1. The product selector behind a surviving first-root class

Work over a characteristic-zero field `K` in the four-root original fixed-`Q`
chart

```text
R={1,2,3,4},       B=Q disjoint-union U,
|Q|=2,             U={1,2,3,4}.                       (1)
```

Retain the fully supported maximum-root vectors `x_i`, the fully supported
residual contraction `z_Q`, and the complete `GLD15` joint nuisance.  For the
four-port target `U`, choose one root `a` and use the `GLS17` map

```text
epsilon_a : tensor_(i in R)V_i^* -> V_a^*             (2)
```

which evaluates every root other than `a` at `x_i`.  Its leading desired
covector and complete leading nuisance are

```text
Lambda_(a,U)=epsilon_a(g_U^M),
N_(a,U)^lead=epsilon_a(N_U^J),
b_(a,U)=[Lambda_(a,U)].                               (3)
```

### Lemma 1 (factored leading selector)

If

```text
b_(a,U)!=0,                                           (4)
```

then there is a vector `y_a in V_a` such that the product functional

```text
lambda_a(T)=T(x_1,...,x_(a-1),y_a,x_(a+1),...,x_4)    (5)
```

is a normalized legal `GLD15` four-port selector with coefficient row

```text
(lambda_a(g_U^M),lambda_a(g_U^Z))=(1,0).              (6)
```

#### Proof

Condition (4) says that `Lambda_(a,U)` does not belong to
`N_(a,U)^lead`.  Choose a functional `phi in (V_a^*)^*` which annihilates
`N_(a,U)^lead` and has `phi(Lambda_(a,U))=1`.  Finite-dimensional double
duality writes `phi` as evaluation at a vector `y_a in V_a`.  Then
`lambda_a=phi compose epsilon_a` annihilates the complete nuisance because
its image under `epsilon_a` is exactly `N_(a,U)^lead`.  It evaluates the
`M` column to one, while `GLS17` gives `epsilon_a(g_U^Z)=0`.  This proves
(5)--(6).  `square`

The selector in Lemma 1 is a particular legal row supplied by the leading
shadow.  An arbitrary pure-`M` row in `C_U` need not factor as (5).

## 2. Complete foreign labels give one common cross-Gram form

Put

```text
rho_i=x_i for i!=a,              rho_a=y_a.            (7)
```

For roots `i!=j`, residual vertices `Q={q_0,q_1}`, and a port `u`, define

```text
A_ij=W_ij(rho_i,rho_j),
xi_i=W_(i,q_0)(rho_i,z_(q_0)),
eta_i=W_(i,q_1)(rho_i,z_(q_1)),
ell_u^c=(W_(i,u)(rho_i,e_(u,c)))_(i in R) in K^4.     (8)
```

Let `Per_R(s,t,p,q)` be the symmetric four-linear permanent which bijects the
four roots to the four displayed columns, and put

```text
J(p,q)=Per_R(xi,eta,p,q).                              (9)
```

Thus `J` is one symmetric bilinear form on the common root-coordinate space
`K^4`.  No nondegeneracy or rank is assumed.

### Lemma 2 (product-selector cross-Gram identity)

For every distinct pair of ports `u,v` and every local colours `c,d`,

```text
J(ell_u^c,ell_v^d)=-B_uv(c,d).                        (10)
```

Before the normalization in Lemma 1, if
`m=lambda_a(g_U^M)!=0`, the denominator-free identity is

```text
J(ell_u^c,ell_v^d)=-m B_uv(c,d).                      (11)
```

#### Proof

Contract every root in the companion matching coefficient with `rho` and
evaluate the `Q` slots at `z_Q`.  Write `F_D` for the resulting coefficient
on an outside set `D subset B`.

The pure-`M` operator identity on the complete labelled module gives

```text
F_empty=0,               F_Q=m,
F_D=0 for every two-set D!=Q,
F_(Q union {u,v})=0.                                  (12)
```

The first equality is the zero `Z` coefficient.  Every other zero in (12) is
the restriction of the legal target-`U` identity to a distinct nuisance
label; no foreign label has been discarded.

Expand the perfect matchings on the four roots and the four outside vertices
`q_0,q_1,u,v` by the number of outside--outside edges.  Matchings with two
such edges contain the root hafnian `F_empty` and vanish.  With one such edge
`e`, the remaining root/two-outside factor is `F_(D-e)` because
`F_empty=0`.  By (12), every one-edge family vanishes except the family with
outside edge `uv`, whose complementary coefficient is `F_Q=m`.  The
matchings with no outside edge biject the four roots to `q_0,q_1,u,v` and
sum to `J(ell_u^c,ell_v^d)`.  Hence

```text
0=F_(Q union {u,v})(c,d)
  =m B_uv(c,d)+J(ell_u^c,ell_v^d),                    (13)
```

which is (11), and normalization gives (10).  `square`

The 105 matchings in this expansion split as `24+72+9` according to zero,
one, or two outside--outside edges.  Equation (13) is pointwise on every
root-incidence and nuisance-rank fibre; no hafnian, incidence minor, or entry
of `J` is inverted.

## 3. Pure three-colour diagonal compounds have only camouflage support

Suppose six pair blocks are diagonal in fixed ternary bases:

```text
B_uv=sum_(c=0)^2 b_uv^c e_(u,c)^* tensor e_(v,c)^*.   (14)
```

Recall

```text
C(B)=B_12B_34+B_13B_24+B_14B_23.                     (15)
```

### Lemma 3 (exhaustive pure-three support)

If every mixed coefficient of `C(B)` is zero and all three pure coefficients
of `C(B)` are nonzero, then, after permuting colours, the exact edge support is

```text
colour 0: {12,34},
colour 1: {13,24},
colour 2: {14,23},                                   (16)
```

and every displayed diagonal entry is nonzero.  No edge supports a second
colour.

#### Proof

For a complementary partition `e|f` and distinct colours `c,d`, the word
which is colour `c` on `e` and colour `d` on `f` has exactly one compatible
diagonal matching.  Its coefficient is

```text
b_e^c b_f^d=0.                                       (17)
```

For each colour `c`, its nonzero pure coefficient is the sum of the three
products `b_e^c b_f^c`.  At least one product is therefore nonzero, so one
complementary matching is active in colour `c`.  Two colours cannot use the
same matching by (17).  The three colours consequently use the three
matchings bijectively.  If an edge of the matching assigned to `c` also
carried `d!=c`, its complementary edge carries `c`, again contradicting
(17).  Since the three matchings partition the six edges, this proves
(16).  `square`

This is support deduction from exact coefficients, not a support atlas used
as witness coverage.  Pure-coefficient cancellation causes no gap: a nonzero
sum has at least one nonzero summand.

## 4. Four root coordinates cannot realize the camouflage

### Lemma 4 (five-vector cross-Gram obstruction)

Let `V` have dimension at most four and let `J` be any bilinear form on `V`.
There do not exist vectors

```text
v_(u,c) in V,              u in U, c in {0,1,2},      (18)
```

whose cross-port pairings vanish except for the six nonzero entries

```text
J(v_(1,0),v_(2,0)), J(v_(3,0),v_(4,0)),
J(v_(1,1),v_(3,1)), J(v_(2,1),v_(4,1)),
J(v_(1,2),v_(4,2)), J(v_(2,2),v_(3,2)).              (19)
```

Pairings between vectors at the same port are unrestricted.

#### Proof

Consider the five vectors

```text
v_(1,0), v_(1,1), v_(1,2), v_(2,1), v_(2,2).         (20)
```

In a linear relation among them, pair successively with

```text
v_(3,1), v_(4,2), v_(4,1), v_(3,2).                  (21)
```

The support pattern (19) isolates, in order, the coefficients of
`v_(1,1)`, `v_(1,2)`, `v_(2,1)`, and `v_(2,2)`; each isolating pairing is
nonzero.  All four coefficients vanish.  The remaining coefficient of
`v_(1,0)` vanishes because that vector is nonzero, as witnessed by its
nonzero pairing with `v_(2,0)`.  Thus the five vectors in (20) are independent,
contradicting `dim V<=4`.  `square`

The proof is insensitive to degeneracy of `J`.  This is why no generic
root-pairing or incidence-rank argument is needed.

### Theorem 5 (product-selector camouflage exclusion)

Assume:

1. a normalized product-form legal four-port pure-`M` selector as in Lemma 1;
2. all six physical direct blocks `B_uv` are target-diagonal; and
3. `M_U=C(B)` is target-pure with all three pure coefficients nonzero.

Then no such fixed-`Q` physical graph/module point exists.

#### Proof

Lemma 3 gives the camouflage support (16).  Lemma 2 realizes its six nonzero
entries and all its zero cross-port entries as the pairings of the twelve
vectors `ell_u^c` under one bilinear form `J` on `K^4`.  Lemma 4 says this is
impossible.  `square`

## 5. Maximum-root witness consequences and boundary

### Corollary 5.1 (all-seven leading-survival pure-three branch)

No complete four-root maximum-root surplus-two hypothetical witness satisfies

```text
b_(empty,S)!=0                 for every S in binom(U,2),
b_(a,U)!=0                     for at least one a in R,
M_U=C(B) has three nonzero pure coefficients.          (22)
```

#### Proof

The six pair hypotheses and `GLS16`/`GLS17` supply legal pure-`M` selectors;
on the complete target, their physical outputs `M_S=B_uv` are diagonal.  The
four-port hypothesis supplies the product selector of Lemma 1 and makes its
physical output `M_U=C(B)` target-diagonal.  The last condition in (22) enters
Theorem 5.  `square`

### Corollary 5.2 (pure leading-column failure)

Use the `GLS18` pure first-root classes `d_(a,U,c)`.  If all six pair base
classes survive, then for every root `a` at least one of the three classes

```text
[d_(a,U,0)], [d_(a,U,1)], [d_(a,U,2)]                (23)
```

vanishes in the complete first-root leading quotient.

#### Proof

If all three classes in (23) were nonzero, the `GLS18` target identity with
`b_(a,U)!=0` and all fully supported residual weights would make all three
pure coefficients of `M_U` nonzero.  Corollary 5.1 would apply.  `square`

The exact frontier is therefore

```text
GLS17 surviving four-port class gives product selector:       PROVED;
complete foreign labels give common K^4 cross-Gram form:      PROVED;
diagonal pure-three response has matching camouflage support: PROVED;
matching camouflage in common K^4 form:                       EXCLUDED;
all pair shadows + one full-three first-root quotient:         EXCLUDED;
zero/one/two-colour M_U response:                              OPEN;
one or more swallowed pair base shadows:                       OPEN;
all four swallowed four-port first-root shadows:               OPEN;
arbitrary non-leading legal four-port selector:                 OPEN;
pure-Z/oblique/promoted/arbitrary-root branches:                OPEN;
complete supply-and-target-attachment node:                     OPEN;
global Krenn--Gu conjecture:                                    UNRESOLVED. (24)
```

The smallest new residue on the all-six-pair-survival branch is explicit:
every four-port first-root quotient must lose at least one of its three pure
columns, unless its desired class or physical `M` response vanishes.  The
result does not say that these losses occur in a common colour, does not turn
them into full nuisance-space rank, and does not integrate the promoted
`GLS8` source.

## Verification boundary

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_fixed_q_four_root_product_selector_camouflage_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_four_root_product_selector_camouflage_exclusion.py
```

The primary exact SymPy replay constructs the generic 105-term matching
polynomial and checks the complete expansion identity, exhausts all `2^18`
diagonal edge-colour support masks,
finds exactly the six matching-colour permutations, and checks twelve
port-oriented five-vector certificates.  The genuinely independent no-import
audit uses a separate recursive integer-word matching representation,
constructs the six support profiles from colour-to-matching assignments and
maximality checks rather than scanning masks, and rederives the obstruction
from a rank-three pairing map with a two-dimensional kernel demand.

These bounded scripts audit the matching conventions, exhaustive finite
support implication, and dimension certificate.  The complete-labelled-
module restriction, arbitrary-field coefficient argument, and maximum-root
source corollaries are the written proofs.
