# Fixed-Q four-root product-selector camouflage exclusion hostile review -- 2026-08-23

## Review verdict

**SUPERSEDED / FAILED (2026-08-24).**  The acceptance below did not audit the
load-bearing distinction between the root companion `G_D` and the full
matching coefficient `F_D`.  The claimed cross-Gram bridge and downstream
exclusion are withdrawn.  See the
[interface correction review](FIXED_Q_PRODUCT_SELECTOR_ROOT_COMPANION_FULL_COEFFICIENT_INTERFACE_CORRECTION_REVIEW_2026-08-24.md).

**Historical verdict (superseded): accepted as an exact characteristic-zero conditional module/source
exclusion after focused and independent replay.**  The package proves that a
`GLS17` first-root factored four-port selector cannot coexist with six
target-diagonal direct pair blocks and a target-pure residual-absent four-port
compound having three nonzero pure colours.  Equivalently, on the all-six-pair
base-survival witness branch, every four-port first-root quotient loses at
least one pure colour.

This is not strategic-node closure and not a global result.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## Scope audited

The exact assumptions are:

1. four roots and four ports in one original fixed-`Q` `GLD15` module;
2. one fully supported residual point and the `GLS17` maximum-root data;
3. survival of one four-port first-root leading class, so a selector factoring
   through that precise partial-root evaluation exists;
4. target diagonality of all six direct `M` pair blocks; and
5. target purity and three nonzero pure coefficients of `M_U=C(B)`.

The witness corollary obtains item 4 from survival of all six `GLS16` pair
base classes.  It does not obtain items 3 or 5 universally.

## Hostile checks

### The selector really has product form

The argument does not replace an arbitrary legal row by a decomposable one.
It starts with the exact `GLS17` map
`epsilon_a:L_U^* -> V_a^*`.  A functional separating the surviving leading
class from `epsilon_a(N_U^J)` is evaluation at one vector `y_a`; composing it
with `epsilon_a` evaluates the four root slots at
`x_1,...,y_a,...,x_4`.  This is a particular legal row, including on joint
rank-two fibres.

If a pure-`M` row exists only by another route while every `GLS17` first-root
class is swallowed, this theorem does not apply.

### The full nuisance, not a selected ledger, is used

The cross-Gram identity uses the legal target-`U` operator equation on every
label whose outside set is a two-set other than `Q`, and on every
`Q union {u,v}` outside set.  These are coefficient slices of the complete
joint nuisance.  Retaining only pair labels or one chosen nuisance row would
not justify the cancellations.

### The matching expansion does not divide by an exceptional factor

Before normalization, the identity is

```text
J(ell_u^c,ell_v^d)=-m B_uv(c,d),       m!=0.
```

The proof first kills the root hafnian by the selector's exact zero `Z`
coefficient, then uses all other two-outside labelled coefficients.  It does
not divide by the root hafnian, a permanent, an incidence minor, a response,
or the bilinear-form rank.  Normalizing by the already nonzero desired
coefficient `m` is exactly the allowed constant selector normalization.

### Pure-three support is exhaustive

For diagonal pair blocks, every mixed `2+2` word has one compatible matching,
so its coefficient is a single product.  A nonzero pure coefficient is a sum
of three complementary products and therefore has at least one nonzero term.
The three colours must choose three distinct complementary matchings; every
extra edge-colour entry would immediately create a nonzero mixed `2+2` word.
The primary replay exhausts all `2^18` masks and finds exactly six colour
permutations.  The independent audit instead builds the six permutations and
checks both collision and maximality arguments.

### Degenerate root-incidence fibres are included

No rank classification of the common form `J` is used.  The matching support
isolates five vectors by four nonzero cross pairings and the nonzero partner
of the fifth vector.  Hence the vectors are independent even if `J` is
singular.  Their ambient incidence space has dimension four, giving the
contradiction on generic and exceptional fibres alike.

### The response gate is not silently strengthened

Survival of `b_(a,U)` supplies a legal selector but does not by itself make
`M_U` nonzero or three-colour-full.  The theorem and Corollary 5.1 state the
three nonzero pure coefficients explicitly.  Corollary 5.2 invokes the
stronger, named `GLS18` hypothesis that all three pure first-root quotient
classes survive; the fully supported residual weights then transfer this to
the three physical coefficients.

### No incorrect GLD64 or arbitrary-root inference

The common form here represents the direct blocks `B_uv` through root
incidences.  It is not the globally decomposable residual channel
`K_uv=a_u tensor a_v` assumed by `GLD64`, and neither theorem implies the
other.  The dimension contradiction uses exactly four root coordinates.  It
does not promote to arbitrary root order, and it does not integrate the
distinct promoted `GLS8` module.

## Independent evidence

Run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_fixed_q_four_root_product_selector_camouflage_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_four_root_product_selector_camouflage_exclusion.py
python -m py_compile claims/arbitrary-order/verify_fixed_q_four_root_product_selector_camouflage_exclusion.py claims/arbitrary-order/audit_fixed_q_four_root_product_selector_camouflage_exclusion.py
uv run --with ruff ruff check claims/arbitrary-order/verify_fixed_q_four_root_product_selector_camouflage_exclusion.py claims/arbitrary-order/audit_fixed_q_four_root_product_selector_camouflage_exclusion.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_fixed_q_four_root_product_selector_camouflage_exclusion.py claims/arbitrary-order/audit_fixed_q_four_root_product_selector_camouflage_exclusion.py
```

The primary and audit import neither one another nor any project theorem
implementation.  Their matching encodings, support traversals, and linear-
dimension derivations differ.

## Remaining boundary

The package leaves open:

- every swallowed pair base class;
- all four swallowed four-port first-root classes;
- product-selector responses with at most two active pure colours or zero
  response;
- arbitrary legal four-port rows not supplied by a first-root shadow;
- pure-`Z`, oblique, response-invisible, promoted-source, and other-root-order
  branches;
- permanent restriction, extraction, gluing, strategic node closure, and
  global resolution.

The highest-leverage successor is not another support atlas.  It is to couple
the newly forced first-root pure-column losses across the four choices of open
root, or to combine them with the existing `GLS18`/`GLS19` all-rank Fitting
profiles and complete mixed equations.  Any successor must retain zero
response and every nuisance-rank-drop fibre.
