# Fixed-Q four-root product-selector two-colour exclusion hostile review -- 2026-08-23

## Review verdict

**SUPERSEDED / FAILED (2026-08-24).**  The acceptance below inherited the
invalid `GLD65` root-companion/full-coefficient substitution.  Its common
cross-pairing form, two-colour exclusion, and synchronized-plane corollaries
are withdrawn.  See the
[interface correction review](FIXED_Q_PRODUCT_SELECTOR_ROOT_COMPANION_FULL_COEFFICIENT_INTERFACE_CORRECTION_REVIEW_2026-08-24.md).

**Historical verdict (superseded): accepted as an exact characteristic-zero conditional module/source
theorem after focused and independent replay.**  The package strengthens
`GLD65`: a `GLS17` first-root product selector, six diagonal direct blocks,
and a pure four-port response permit at most one nonzero pure response
colour.  On the all-six-pair-base-survival witness branch, any proper
first-root shadow therefore forces one nonzero monocolour response and
synchronizes every proper first-root nuisance shadow to the coordinate plane
missing that same colour.

This does not close the supply-and-attachment node or the global theorem.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Scope audited

The exact module assumptions are:

1. four roots and four ports in one original fixed-`Q` `GLD15` module;
2. a legal pure-`M` selector supplied by one surviving `GLS17` four-port
   first-root class, hence factoring as product evaluation on the roots;
3. the complete labelled nuisance, including every foreign two-set and
   `Q union {u,v}` coefficient;
4. target diagonality of all six direct `M` pair blocks; and
5. target purity of `M_U=C(B)`.

Theorem 5 says only that at most one pure coefficient is nonzero.  The
complete-witness corollary obtains nonzero response and the exact shadow
planes from `GLS18`; it obtains item 4 from survival of all six `GLS16` pair
base classes.  None of those source classes is forced universally.

## Hostile checks

### The new response-anchor equations are legal

The selector already used by `GLD65` has zero `Z` coefficient, nonzero
desired `M` coefficient, and annihilates the complete nuisance.  Its labels
`{q_0,u}` and `{q_1,u}` are therefore zero for every port and colour.  After
the root hafnian is killed by the zero `Z` coefficient, the six-vertex
matching expansion is exactly

```text
F_(q_0q_1)=P(xi,eta),
F_(q_0u)=P(xi,ell_u^c),
F_(q_1u)=P(eta,ell_u^c).
```

No extra graph equation, selected nuisance submodule, or downstream target
identity is inserted.

### The common-space bound retains the proportional-functional fibre

The nonzero response gives `P(xi,eta)=m!=0`, so each anchor functional is
nonzero.  The proof claims only `dim W<=3`; it does not claim that the two
functionals are independent.  Coincident or proportional kernel hyperplanes
are therefore included.  All later maps are restricted to `W` and their rank
two is witnessed by named active-colour partner vectors, not a generic minor.

### Two active coefficients do not imply a hidden three-colour support claim

The proof treats all third-colour edge entries.  If an edge block is zero,
two independent selected-colour vectors enter a kernel of dimension at most
one.  If no block is zero, each complementary pair has the same singleton
support by the exact mixed `2+2` coefficients.  A third-colour matching again
puts two independent selected vectors in that kernel.  Only then does the
argument reduce to a surjective assignment of three matchings to the two
selected colours.

The primary replay scans all `2^18` masks.  For fixed active colours 0 and 1,
it finds 102 valid mixed-zero masks: 90 zero-edge cases and 12 no-zero-edge
matching assignments.  Thus inactive third-colour support and partial edge
support were not silently discarded.

### The one-dimensional proportionality contradiction is sound

At a base port, the active-colour partner vectors make the pairing map from
`W` rank two, leaving kernel dimension at most one.  In the final two-colour
assignment, three named nonzero off-colour neighbour vectors lie in that
kernel.  Two have a nonzero mutual pairing and another pair has zero pairing.
Nonzero vectors on one line cannot have this pattern under any bilinear form,
including a singular or nonsymmetric one.

### The plane synchronization is a witness corollary, not module algebra

The abstract exclusion does not make `M_U` nonzero.  On a complete witness,
one surviving first-root class and the fact that the three pure leading
covectors form a basis invoke the exact `GLS18` target identity, which forces
`M_U!=0`.  Once its unique colour is fixed, each root's same identity makes
its nuisance either the full basis span or exactly the plane of the other two
colours.  The shared physical tensor `M_U`, not a choice of local minor,
synchronizes the missing colour.

### Exceptional fibres and characteristic scope

The proof divides only by the already nonzero selector normalization if one
chooses to normalize; the stated identities retain the scalar `m`.  It does
not invert an incidence, hafnian, response, bilinear-form rank, edge entry,
or nuisance minor.  Zero edges and every rank drop are explicit branches.
The result is retained in the repository's characteristic-zero witness
context and makes no arbitrary-root promotion.

## Independent evidence

Run:

```powershell
uv run --with sympy python claims/arbitrary-order/verify_fixed_q_four_root_product_selector_two_colour_exclusion.py
python -I claims/arbitrary-order/audit_fixed_q_four_root_product_selector_two_colour_exclusion.py
python -m py_compile claims/arbitrary-order/verify_fixed_q_four_root_product_selector_two_colour_exclusion.py claims/arbitrary-order/audit_fixed_q_four_root_product_selector_two_colour_exclusion.py
uv run --with ruff ruff check claims/arbitrary-order/verify_fixed_q_four_root_product_selector_two_colour_exclusion.py claims/arbitrary-order/audit_fixed_q_four_root_product_selector_two_colour_exclusion.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_fixed_q_four_root_product_selector_two_colour_exclusion.py claims/arbitrary-order/audit_fixed_q_four_root_product_selector_two_colour_exclusion.py
```

The audit imports neither the primary replay nor any project theorem
implementation.  It uses different polynomial, support, and dimension
representations.

## Remaining boundary

The package leaves open:

- one or more swallowed pair base classes;
- the all-four-full first-root-shadow profile;
- the synchronized nonzero monocolour/coordinate-plane profile;
- arbitrary pure-`M` rows not supplied by a first-root product selector;
- pure-`Z`, oblique, response-invisible, promoted-source, and other-root
  branches;
- every response/activity, nuisance-survival, target-anchor, and permanent
  gate not explicitly supplied here; and
- strategic-node closure, permanent restriction, extraction/gluing, and
  global resolution.

The highest-leverage successor is to attack the two exact first-root profiles
with the still-unused complete higher nuisance labels and the simultaneous
`GLS18`/`GLS19` Fitting equations.  Another diagonal support atlas would not
address the missing source-survival and arbitrary-root gates.
