# Hostile review of the fixed-pair kernel-support boundary theorem

## Verdict and scope

**PASS, for the stated fixed-pair, pointwise, characteristic-zero,
full-target scope.**  No mathematical, quantifier, case-exhaustiveness,
dependency, characteristic, or implementation blocker survived hostile
review.

For either displayed mixed-factor projection and every local mode, the new
package proves

```text
0 != p in L_t intersect ker(Phi_k)  =>  |supp_t(p)| <= 2,
rank(Phi_k|L_t) >= 2.
```

Outside the three exceptional ambient kernel lines, such a `p` has local
colour support exactly one.  Combined with the already reviewed two-sided
projection-drop predecessor, each projection family has minimum local rank
exactly two.

This is a necessary localization only.  It neither excludes simultaneous
rank-two incidences nor transports the result to the other equality-five
pair orbits.  Unrestricted `P_6 -> Delta_3` nonrestriction is unknown, and
the global Krenn--Gu conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_kernel_support_boundary.py
  audit_arbitrary_permanent_fixed_pair_kernel_support_boundary.py
```

Load-bearing predecessor:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_two_sided_projection_drop.py
  audit_arbitrary_permanent_fixed_pair_two_sided_projection_drop.py
```

## 1. Kernels, contractions, and determinant gate

Solving the four defining equations of each projection directly gives

```text
ker(Phi_1) = {(a,0,b,a+b,0,0)},
ker(Phi_2) = {(0,a,b,a+b,0,0)}.
```

Independent differentiation of the five complementary quartics reproduces
the contraction table.  Suppressing the common factor `x_4x_5`, the first
row is

```text
m_1: 0,
m_2: a( x_0-x_1-x_2+x_3),
d_0: b(-x_0+x_1+x_2+x_3),
d_1: (a+b)(x_0-x_1+x_2+x_3),
d_2: -2a x_1,
```

and the second row is

```text
m_1: a(-x_0+x_1-x_2+x_3),
m_2: 0,
d_0: (a+b)(-x_0+x_1+x_2+x_3),
d_1: b(x_0-x_1+x_2+x_3),
d_2: -2a x_0.
```

For either row, the nonidentically-zero mixed covector together with the
three diagonal covectors has determinant

```text
8 a^2 b(a+b).
```

Thus these four residual covectors form a basis of `R^*` precisely away
from `a=0`, `b=0`, and `a+b=0`.  On those exceptional lines, respectively,
one of `d_2`, `d_0/d_1`, or `d_1/d_0` contracts identically to zero.  Its
nonzero pure target forces the stated local coefficient to vanish.  This
already gives support at most two on every exceptional direction.

The factor `8` is harmless in characteristic zero but confirms that the
stated characteristic boundary is load-bearing.

## 2. The `R direct-sum A` contraction tensor

With

```text
R=K^{0,1,2,3},  A=K^{4,5},
J((s_4,s_5),(t_4,t_5))=s_4t_5+s_5t_4,
```

the polarization of `x_4x_5 ell` on three remaining inputs is exactly
`ell(C)`, where

```text
C(y,z,w)=r(y)J(a(z),a(w))
        +r(z)J(a(y),a(w))
        +r(w)J(a(y),a(z)).
```

For a generic kernel vector `p` in the removed mode, the determinant gate
therefore converts the full exact target into the vector identities

```text
C(y_(s,i),y_(u,j),y_(v,l)) = 0 unless i=j=l,
C(y_(s,e),y_(u,e),y_(v,e)) != 0 iff alpha_e != 0.
```

This uses one zero mixed coordinate and all three diagonal target
coordinates.  It is not a Hamming-shell argument, and it assumes no
genericity of the three remaining local spaces.

## 3. Cross-orthogonality and the rank gate

Fix two remaining modes `s,u` and distinct colours `i!=j`.  The linear map

```text
K_(i,j): R direct-sum A -> R,
w |-> C(y_(s,i),y_(u,j),w)
```

kills the three-dimensional third local space `L_v`, so it has rank at
most three.  On the four-dimensional `R`-summand it is scalar multiplication
by

```text
J(a(y_(s,i)),a(y_(u,j))).
```

A nonzero scalar would give rank at least four.  Hence every pair of
different colours in different modes is `J`-orthogonal.  The domain/rank
comparison is valid even if `K_(i,j)` has further kernel; it only uses the
known inclusion `L_v subset ker K_(i,j)`.

## 4. Exhaustion of the `rho=0,1,2` cases

For the three remaining modes set

```text
rho_q=dim span{a_(q,0),a_(q,1),a_(q,2)} subset A.
```

The following cases exhaust the two-dimensional `A`-geometry.

- If `max rho_q=0`, no colour is active.
- If every `rho_q<=1`, a nonzero same-colour pairing between two modes
  forces each endpoint mode to support only that colour: any nonzero
  different-colour column there would be proportional to the active column
  and also orthogonal to the active column at the other endpoint.  Since
  any second pair of three modes shares an endpoint, at most one colour is
  active.
- If `rho_s=2`, choose independent columns of colours `e,f` at mode `s`.
  Every `h`-column at either other mode is orthogonal to both and hence is
  zero.  Thus only `e,f` can be active.  If both are active, nonzero outside
  `e`- and `f`-columns lie in the two distinct lines
  `a_(s,f)^perp` and `a_(s,e)^perp`.  They are independent, so the remaining
  `h`-column at mode `s` is also zero.

Consequently at most two colours are active, and if two are active then all
three remaining-mode columns of the inactive colour vanish in `A`.

## 5. The corrected active-colour quantifier

The proof uses exactly the valid implication

```text
alpha_e != 0  =>  colour e is active.
```

Indeed, `alpha_e!=0` makes the all-`e` value of `C` nonzero.  In the three
summands defining `C`, this is impossible if all three same-colour `J`
pairings vanish.  Therefore at least one such pairing is nonzero, which is
precisely activity.

The converse is neither valid in general nor used: nonzero same-colour
pairings can cancel after multiplication by the three `R`-components.  The
theorem explicitly acknowledges this possible cancellation.  Thus the
active-colour quantifier is in the safe direction and does not smuggle in a
noncancellation hypothesis.

All colours in `supp_t(p)` are therefore active, so generic support has size
at most two.  If it had size exactly two, the `rho` lemma would make every
remaining-mode `A`-part at the third colour zero.  In the corresponding
pure coefficient, only the removed mode could then contribute an `A`-part,
whereas the common factors `x_4` and `x_5` must be supplied by two distinct
multilinear slots.  That pure coefficient would vanish, contradicting its
nonzero exact target.  A nonzero local vector has nonempty support, so its
generic support is exactly one.

## 6. Finite-union and rank consequences

For fixed `k,t`, let `S=L_t intersect ker(Phi_k)`.  The support-at-most-two
result places `S` in the union of the three local coordinate hyperplanes.
Because a characteristic-zero field is infinite, a vector space cannot be
a finite union of proper linear subspaces.  Therefore one local colour
coordinate vanishes identically on `S`.

If `dim S>=2`, then `S=ker(Phi_k)`, since the ambient kernel has dimension
two.  The generic directions form the complement of three lines in this
two-space.  Every such direction would have to lie on one of the three
local colour lines.  Hence the whole two-space would be covered by the
three exceptional lines and three local colour lines, another impossible
finite union of proper subspaces.  Thus `dim S<=1`, and rank-nullity on the
three-dimensional `L_t` gives

```text
rank(Phi_k|L_t) >= 2.
```

No algebraic closure, Zariski-density theorem, or unstated genericity is
needed; infinitude of the characteristic-zero base field suffices.

## 7. Predecessor dependence and exact boundary

The new lower bound is proved internally.  The immediate predecessor is
used only for its already reviewed conclusion that each projection family
has some mode of rank at most two.  Combining the two statements gives

```text
min_t rank(Phi_1|L_t)=min_t rank(Phi_2|L_t)=2.
```

This does not assert that the minimizing modes coincide, that every
rank-two incidence exists independently, or that the residual is empty.
It also does not normalize the `(3,1)` or `(4,1)` equality-five orbits to
this fixed `(4,2)` pair.

Accepted boundary:

```text
fixed pair, every local Phi_k rank at least two:          PROVED;
fixed pair, local kernel support at most two:             PROVED;
generic local kernel support exactly one:                 PROVED;
one rank-two mode in each projection family:              PROVED NECESSARY;
classification/exclusion of simultaneous rank-two modes: OPEN;
unrestricted P_6 -> Delta_3:                              UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

## 8. Computational replay and independence

The primary verifier uses SymPy exact arithmetic to derive the two kernels,
all ten contractions, both determinant factorizations, the `C` identity,
and the rank-four obstruction.  It exhausts the abstract `A`-lemma over
`F_3,F_5,F_7`.

The no-import audit imports neither the primary verifier nor SymPy.  It
rebuilds the quartics by edge complementation, multiplies directly in the
square-free algebra, uses a custom determinant and modular row reducer,
checks every projective kernel direction over `F_5,F_7,F_11`, exhausts the
`A`-lemma over `F_11`, and separately stresses the finite-union rank step.
This is meaningfully independent implementation evidence.  The finite-field
computations replay identities and case structure; the written
characteristic-zero argument is the proof.

Focused final replay passed:

```text
new primary exact verifier:                 PASS;
new independent no-import audit:            PASS;
two-sided predecessor primary:              PASS;
two-sided predecessor independent audit:    PASS;
py_compile on new and predecessor scripts:  PASS;
Ruff on new and predecessor scripts:        PASS.
```

Selected independent-audit counts were:

```text
direct square-free coefficient checks: 245760;
projective determinant checks:               96;
F_11 compatible A-triples:                28215;
F_11 two-active triples:                   1578;
F_5 full-rank local coordinate maps:      14880;
false generic coordinate-line covers:         0.
```

## Final reviewed hashes

```text
new theorem:
7AEC9CD00DEBAC1D5CFA91D44E5D3634BD6D05FF8CA755BA1C2E83D1F8C3C45B

new primary verifier:
2B5FC62CA56FA06E5CF06AAC12679CB1051CD7336E1F4B473ECB86AED48AF53C

new independent audit:
038EDA376B773687523FA0885157907725FD38EB5D63AA83BCFD0095090C6F68

two-sided predecessor theorem:
A383731E094E0D0E45482AAB889FB8B202FC7A2CF452D8534D5035E737089F36

two-sided predecessor primary verifier:
E170A513301ECD84A8989066A29B51B89635FD54B0CEF88DCEBBEEDBAAF641DE

two-sided predecessor independent audit:
47A30C8C09E3931526C4CFAC2E9ABE66B7FD10B4EA95336C93E12D63C360E6B2
```
