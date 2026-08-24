# Fixed-Q four-root product-selector two-colour exclusion and first-root plane synchronization

## Status

**Exact characteristic-zero fixed-module exclusion and source-interface
refinement.**  A surviving `GLS17` four-port first-root class supplies the
product-form pure-`M` selector of `GLD65`.  The selector's additional foreign
two-set equations imply that every root-to-port incidence vector lies in one
common subspace `W` of dimension at most three.  The six direct port blocks
remain cross-pairings of those vectors under one bilinear form.

If the direct blocks are target-diagonal and their four-port compound is
target-pure, that compound can have **at most one** nonzero pure colour.  The
argument covers zero edge blocks, an unused third edge colour, proportional
response-anchor functionals, singular cross-pairing forms, and every
incidence- or nuisance-rank-drop fibre.  It does not select a rank minor or
divide by an incidence, response, or support factor.

Consequently, on the all-six-pair-base-survival branch of a complete
four-root maximum-root witness, survival of any four-port first-root class
forces the physical response `M_U` to be nonzero and monocolour.  Every
proper first-root nuisance shadow is then exactly the coordinate plane
spanned by the other two pure covectors; every remaining first-root shadow
is the full three-space.  The same physical response colour synchronizes all
proper planes across the four choices of open root.

The result does **not** force a pair or four-port class to survive, exclude
the all-four-full-shadow branch, constrain arbitrary non-product legal rows,
integrate pure-`Z` or oblique rows, cover other root orders or the promoted
`GLS8` source, or imply a permanent restriction.  The supply-and-attachment
node remains open.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Dependencies and provenance

The complete joint nuisance, physical response columns, and legal operator
space come from

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md).

The pair diagonality source, partial-root leading selector, and target
coupling come from

- [`GLS16`](MAXIMAL_ROOT_SURPLUS_TWO_BASE_GRADE_PAIR_SHADOW_AND_CROSS_TARGET_SELECTOR_ANNIHILATION_THEOREM.md),
- [`GLS17`](MAXIMAL_ROOT_SURPLUS_TWO_PARTIAL_ROOT_GRADE_SHADOW_AND_COMMON_PURE_M_SELECTOR_THEOREM.md), and
- [`GLS18`](MAXIMAL_ROOT_SURPLUS_TWO_LEADING_SHADOW_TARGET_COUPLING_AND_FITTING_FAILURE_THEOREM.md).

The product-selector construction and eight-vertex cross-Gram identity are
the proved starting interface of

- [`GLD65`](FIXED_Q_FOUR_ROOT_PRODUCT_SELECTOR_THREE_COLOUR_CAMOUFLAGE_EXCLUSION_THEOREM.md).

No external literature claim is used.  The new content is the response-anchor
bilinear form, the common dimension-at-most-three incidence space, the exact
zero-edge/no-zero-edge cover for two active pure colours, and the synchronized
first-root plane corollary.

## 1. Product-selector notation

Work over a characteristic-zero field `K` in one original four-root
fixed-`Q` chart

```text
R={1,2,3,4},       B=Q disjoint-union U,
Q={q_0,q_1},       U={1,2,3,4}.                       (1)
```

Fix one `GLS17` first-root selector, contract the four root slots at its
product vectors `rho_i`, and evaluate `Q` at the fixed fully supported
residual point.  For every outside set `D subset B`, let `F_D` be the
resulting companion matching coefficient.  If the desired coefficient
before normalization is `m`, legality and the complete labelled nuisance
give

```text
F_empty=0,                 F_Q=m!=0,
F_D=0 for every two-set D!=Q,
F_(Q union {u,v})=0        for u!=v in U.             (2)
```

The first equality is the selector's zero `Z` coefficient.  The second is
its nonzero `M` coefficient.  Every other equality is a distinct coefficient
slice of the complete joint nuisance; no selected subledger replaces it.

For roots `i!=j`, write

```text
A_ij=W_ij(rho_i,rho_j),
xi_i=W_(i,q_0)(rho_i,z_(q_0)),
eta_i=W_(i,q_1)(rho_i,z_(q_1)),
ell_u^c=(W_(i,u)(rho_i,e_(u,c)))_(i in R) in K^4.    (3)
```

Let `H` be the root hafnian.  Define two root-coordinate forms

```text
P(p,q)=sum_({i,j} subset R) A_ij
       (p_k q_l+p_l q_k),       {k,l}=R-{i,j},       (4)

J(p,q)=Per_R(xi,eta,p,q).                              (5)
```

Thus `P` and `J` are symmetric bilinear forms on `K^4`; no rank or
nondegeneracy is assumed.

## 2. The response anchor cuts the incidence space to dimension at most three

### Lemma 1 (response-anchor common kernel)

Under (2),

```text
H=0,
P(xi,eta)=m!=0,
P(xi,ell_u^c)=P(eta,ell_u^c)=0
                    for every u in U and c in {0,1,2}. (6)
```

Consequently every `ell_u^c` lies in

```text
W=ker P(xi,-) intersect ker P(eta,-) subset K^4,
dim W<=3.                                             (7)
```

#### Proof

The coefficient on the empty outside set is the root hafnian, so (2) gives
`H=0`.  A perfect matching on the four roots plus two outside vertices is
either the outside edge times `H`, or attaches both outside vertices to
distinct roots and pairs the remaining roots.  Hence

```text
F_Q=B_(q_0q_1)H+P(xi,eta)=P(xi,eta)=m.               (8)
```

The identical expansion for `{q_0,u}` and `{q_1,u}`, together with their
zero coefficients in (2), gives the two annihilations in (6).  Since
`P(xi,eta)=m!=0`, both functionals `P(xi,-)` and `P(eta,-)` are nonzero.
Their kernels may coincide, so only the universally valid bound
`dim W<=3` is used.  This includes the proportional-functional fibre.
`square`

### Lemma 2 (common cross-pairing form)

For distinct ports `u,v` and all colours `c,d`,

```text
J(ell_u^c,ell_v^d)=-m B_uv(c,d).                     (9)
```

#### Proof

This is the denominator-free `GLD65` eight-vertex matching identity.  For
completeness, split the 105 perfect matchings on the four roots and
`q_0,q_1,u,v` according to the number of outside--outside edges.  The nine
two-edge terms contain `H=0`.  In the 72 one-edge terms, the complementary
two-outside coefficient vanishes by (2), except for the edge `uv`, whose
complement is `Q` and contributes `m B_uv(c,d)`.  The 24 zero-edge terms are
exactly `J(ell_u^c,ell_v^d)`.  The zero coefficient on
`Q union {u,v}` now gives (9).  `square`

No step divides by `m`; normalization by the already nonzero selector
coefficient is optional.

## 3. Two active pure colours are impossible

Assume the direct blocks are diagonal in the fixed target bases,

```text
B_uv=sum_(c=0)^2 b_uv^c e_(u,c)^* tensor e_(v,c)^*, (10)
```

and the compound

```text
C(B)=B_12B_34+B_13B_24+B_14B_23                    (11)
```

is target-pure.  For a complementary matching `e|f` and distinct colours
`c,d`, the unique compatible diagonal contribution to the corresponding
mixed `2+2` word is

```text
b_e^c b_f^d=0.                                       (12)
```

### Lemma 3 (two-colour local dimension data)

Suppose two distinct pure coefficients of `C(B)`, with colours `c,d`, are
nonzero.  Put

```text
x_u=ell_u^c,       y_u=ell_u^d,
E_u=span{x_u,y_u} subset W.                          (13)
```

Then, for every port `u`,

```text
dim E_u=2,
rank(W -> E_u^*)=2,
dim E_u^perp<=1,                                     (14)
```

where the displayed map sends `z` to
`(J(x_u,z),J(y_u,z))` and `E_u^perp` is its kernel.

#### Proof

A nonzero pure coefficient contains a nonzero complementary-edge product.
Thus, for each port `u`, the `c`-matching partner witnesses `x_u!=0`, and
the `d`-matching partner witnesses `y_u!=0`.  If `y_u=t x_u`, pairing with
the `c` partner gives `t=0` by target diagonality, contradicting `y_u!=0`.
Hence `dim E_u=2`.

The `c`- and `d`-matching partner vectors have respectively a nonzero first
and a nonzero second coordinate under the map in (14), while their other
coordinate is zero by diagonality.  The map therefore has rank two.  Lemma 1
gives `dim W<=3`, so rank-nullity gives `dim E_u^perp<=1`.  `square`

### Lemma 4 (exhaustive edge-support split)

Under the assumptions of Lemma 3, either:

1. some direct edge block is zero; or
2. every complementary matching has both edges supported in the same single
   colour.  Equivalently, the three complementary matchings carry an
   assignment

   ```text
   kappa:{12|34,13|24,14|23}->{0,1,2}                (15)
   ```

   and both selected colours `c,d` occur in its image.

#### Proof

Suppose no edge block is zero.  On a complementary pair `e|f`, let their
nonempty colour supports be `S_e,S_f`.  Equation (12) says every element of
`S_e` equals every element of `S_f`.  Hence both supports are the same
singleton.  This gives (15).  Each selected nonzero pure coefficient must
have a live complementary product, so both `c,d` occur.  `square`

### Theorem 5 (product-selector two-colour exclusion)

Assume:

1. a legal product-form four-port pure-`M` selector satisfying (2);
2. all six physical direct blocks `B_uv` are target-diagonal; and
3. `M_U=C(B)` is target-pure.

Then `M_U` has at most one nonzero pure coefficient.

#### Proof

Suppose distinct colours `c,d` have nonzero pure coefficients and use the
spaces `E_u` from Lemma 3.

If `B_uv=0` for some edge, diagonality and (9) give
`E_v subset E_u^perp`.  This contradicts
`dim E_v=2>1>=dim E_u^perp`.

It remains to use case 2 of Lemma 4.  If one matching is assigned a third
colour outside `{c,d}`, then at any base port `u` its partner `v` in that
matching has both `x_v,y_v in E_u^perp`.  Their independence again
contradicts `dim E_u^perp<=1`.

Therefore all three matchings are assigned to `{c,d}`, and both colours
occur.  Fix a base port `u`.  For each neighbour `v`, let `z_v` be the
incidence vector at `v` in the selected colour opposite the colour assigned
to `uv`.  Diagonality gives `z_v in E_u^perp`, and Lemma 3 gives `z_v!=0`.
All three vectors are consequently proportional in a space of dimension at
most one.

Of the three matching colours, two equal one colour `s` and the remaining
one equals the other colour `t`.  The two neighbours reached from `u` along
the `s` matchings have `z`-colour `t`; their connecting edge is the remaining
`t` matching, so their `J` pairing is nonzero by (9).  Pairing either one
with the third neighbour uses different colours and is zero.  Nonzero
proportional vectors cannot have one mutual bilinear pairing nonzero and
another zero.  This is the final contradiction.  `square`

The split is pointwise and exhaustive.  It uses neither a support atlas nor
a nonzero minor.  The primary replay scans all `2^18` diagonal support masks:
with two fixed active pure colours, 102 masks satisfy all mixed equations,
90 have a zero edge, and the other 12 are exactly the matching assignments
in (15).

## 4. Complete-witness first-root consequences

### Corollary 5.1 (monocolour response and synchronized planes)

On a complete four-root maximum-root surplus-two hypothetical witness,
assume all six pair base classes survive:

```text
b_(empty,S)!=0          for every S in binom(U,2).    (16)
```

If at least one four-port first-root class `b_(a,U)` survives, then there is
a unique colour `c_*` such that:

```text
M_U=mu w_(U,c_*)                  with mu!=0,          (17)
```

and for every root `a` the complete first-root nuisance shadow is exactly

```text
N_(a,U)^lead = V_a^*                         if b_(a,U)=0,
N_(a,U)^lead = span{e_(a,c)^*:c!=c_*}        if b_(a,U)!=0. (18)
```

In particular, every proper first-root shadow is the coordinate plane
missing the same physical colour `c_*`.

#### Proof

The six pair classes and `GLS16` make every `B_uv` target-diagonal.  A
surviving `b_(a,U)` supplies the product selector and, by `GLS18`, makes
`M_U` target-pure.  At four ports the three pure leading covectors form a
basis of `V_a^*`; hence a surviving desired class forces `M_U!=0`.
Theorem 5 now gives the unique form (17).

Apply the `GLS18` leading identity separately at every root.  If
`b_(a,U)=0`, all three pure leading classes vanish and their basis lies in
the nuisance, giving the first line of (18).  If `b_(a,U)!=0`, the two
classes with colours different from `c_*` vanish, while the `c_*` class is
nonzero.  The nuisance is proper and contains the other two independent
basis vectors, so it is exactly their plane.  The response `M_U` is one
physical tensor shared by all four shadows, which synchronizes the missing
colour.  `square`

### Corollary 5.2 (sharp all-six-pair first-root profile)

Under (16), exactly one of the following holds:

1. every first-root nuisance shadow is the full three-space; or
2. `M_U` is nonzero monocolour and every first-root shadow is either the
   corresponding synchronized coordinate plane or the full three-space,
   with at least one plane.

This is an exhaustive profile for the four first-root `GLS17` shadows on the
all-six-pair-base-survival branch.  It is not an exclusion of either profile.

#### Proof

If no first-root class survives, its defining leading desired covector lies
in each nuisance.  The `GLS18` pure classes also lie there, and at four roots
they form a basis, so all four shadows are full.  Otherwise Corollary 5.1
applies.  `square`

## 5. Exact boundary

```text
product selector and complete cross-Gram identity:           PROVED (GLD65);
response-anchor common space dim W<=3:                       PROVED;
zero-edge and all no-zero-edge two-colour profiles:          EXCLUDED;
product-selector pure response has at most one colour:       PROVED;
all-pair-survival first-root shadow profile:                  PROVED;
existence of any surviving pair/four-port source class:      OPEN;
all-four-full-shadow profile:                                OPEN;
nonzero monocolour synchronized-plane profile:               OPEN;
arbitrary non-product, pure-Z, and oblique rows:              OPEN;
promoted GLS8 and arbitrary-root source coverage:            OPEN;
permanent restriction/extraction/gluing:                     NOT ENTERED;
complete supply-and-target-attachment strategic node:        OPEN;
global Krenn--Gu conjecture:                                 UNRESOLVED.      (19)
```

The smallest remaining obligation on this branch is no longer a missing
colour census.  It is to contradict the two exact profiles in Corollary 5.2
using the complete mixed witness equations, or to derive a legal downstream
row from one of them with every response, activity, synchronization,
nuisance-survival, anchor, and exceptional-fibre gate intact.

## Verification boundary

Run from repository root:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_fixed_q_four_root_product_selector_two_colour_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_four_root_product_selector_two_colour_exclusion.py
```

The primary exact SymPy replay checks the generic six-vertex response-anchor
identity and the 105-term eight-vertex expansion, scans all `2^18` diagonal
edge-colour masks, and checks all 48 no-zero-edge port-oriented dimension
certificates.  The genuinely independent no-import audit uses integer edge-
word dictionaries, proves the local nonempty-support lemma by the 49 subset
pairs rather than scanning masks, and derives the 12 matching assignments and
their kernel contradictions directly.

These bounded programs audit the matching conventions, finite support cover,
and linear-dimension certificates.  The complete-module restriction,
arbitrary-field rank argument, and witness-shadow synchronization are the
written proofs.
